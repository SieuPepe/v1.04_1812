#!/usr/bin/env python3
"""
Test de flujo completo end-to-end - HydroFlow Manager v1.04

Este test valida el flujo completo de trabajo:
1. Crear un parte nuevo
2. Agregar presupuesto al parte
3. Generar certificación del presupuesto
4. Generar informe con este parte
5. Verificar datos en cada paso
6. Limpiar datos de prueba

CRÍTICO: Este test valida que todo el sistema funciona de forma integrada

Ejecutar: python test_flujo_completo.py

ACTUALIZADO: Adaptado a la estructura real de cert_dev
- Tabla presupuesto: tbl_part_presupuesto
- Tabla certificación: tbl_part_certificacion
- Catálogo: tbl_pres_precios
"""

import os
import sys
from pathlib import Path
from datetime import date

# Cargar .env
try:
    from dotenv import load_dotenv
    project_root = Path(__file__).resolve().parent.parent
    load_dotenv(dotenv_path=project_root / '.env')
except ImportError:
    pass

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

# Configuración desde .env
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
SCHEMA = os.getenv('DB_SCHEMA', 'cert_dev')

# Código único para el parte de prueba
TEST_CODIGO = f'TEST-FLUJO-{date.today().strftime("%Y%m%d%H%M%S")}'

# Imports
try:
    from script.db_connection import get_project_connection
    from script.informes import build_query
except ImportError as e:
    print(f"❌ ERROR: No se pudo importar módulos necesarios: {e}")
    sys.exit(1)

# Utilidades
def print_test_header(step, title):
    """Imprime encabezado de paso"""
    print("\n" + "=" * 80)
    print(f"PASO {step}: {title}")
    print("=" * 80)

def print_success(message):
    """Imprime mensaje de éxito"""
    print(f"✅ {message}")

def print_error(message):
    """Imprime mensaje de error"""
    print(f"❌ {message}")

def print_info(message):
    """Imprime mensaje informativo"""
    print(f"ℹ️  {message}")

# Variables globales
parte_id = None
presupuesto_items = []

# Tests

def paso_1_crear_parte():
    """Paso 1: Crear un parte nuevo"""
    global parte_id
    print_test_header(1, "Crear parte nuevo")

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Crear parte básico
            sql = f"""
                INSERT INTO {SCHEMA}.tbl_partes
                (codigo, titulo, descripcion, fecha_inicio, estado, finalizada)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                TEST_CODIGO,
                'Parte de prueba - Test flujo completo',
                'Este parte fue creado automáticamente por test_flujo_completo.py',
                date.today(),
                'Pendiente',
                False
            )

            cursor.execute(sql, values)
            parte_id = cursor.lastrowid
            conn.commit()
            cursor.close()

        print_success(f"Parte creado exitosamente")
        print_info(f"  ID: {parte_id}")
        print_info(f"  Código: {TEST_CODIGO}")
        return True

    except Exception as e:
        print_error(f"Error al crear parte: {e}")
        import traceback
        traceback.print_exc()
        return False

def paso_2_verificar_parte():
    """Paso 2: Verificar que el parte existe"""
    print_test_header(2, "Verificar parte creado")

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT id, codigo, titulo, estado
                FROM {SCHEMA}.tbl_partes
                WHERE id = {parte_id}
            """)
            row = cursor.fetchone()
            cursor.close()

        if row is None:
            print_error(f"Parte ID {parte_id} no encontrado en la base de datos")
            return False

        print_success("Parte verificado en la base de datos")
        print_info(f"  ID: {row[0]}")
        print_info(f"  Código: {row[1]}")
        print_info(f"  Título: {row[2]}")
        print_info(f"  Estado: {row[3]}")
        return True

    except Exception as e:
        print_error(f"Error al verificar parte: {e}")
        import traceback
        traceback.print_exc()
        return False

def paso_3_agregar_presupuesto():
    """Paso 3: Agregar presupuesto al parte"""
    global presupuesto_items
    print_test_header(3, "Agregar presupuesto al parte")

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Obtener 3 precios del catálogo
            cursor.execute(f"SELECT id, resumen, coste FROM {SCHEMA}.tbl_pres_precios LIMIT 3")
            precios = cursor.fetchall()

            if not precios:
                print_error("No hay precios en el catálogo")
                cursor.close()
                return False

            # Agregar líneas al presupuesto
            for precio in precios:
                precio_id, desc, coste = precio
                cantidad = 10.0
                precio_unit = float(coste if coste else 100.0)

                cursor.execute(f"""
                    INSERT INTO {SCHEMA}.tbl_part_presupuesto
                    (parte_id, precio_id, cantidad, precio_unit)
                    VALUES (%s, %s, %s, %s)
                """, (parte_id, precio_id, cantidad, precio_unit))

                presupuesto_items.append((cursor.lastrowid, precio_id, cantidad, precio_unit))

            conn.commit()
            cursor.close()

        print_success("Presupuesto agregado exitosamente")
        print_info(f"  Conceptos agregados: {len(precios)}")
        for precio in precios:
            print_info(f"  - {precio[1][:50]}")
        return True

    except Exception as e:
        print_error(f"Error al agregar presupuesto: {e}")
        import traceback
        traceback.print_exc()
        return False

def paso_4_verificar_presupuesto():
    """Paso 4: Verificar presupuesto"""
    print_test_header(4, "Verificar presupuesto")

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Contar líneas
            cursor.execute(f"""
                SELECT COUNT(*)
                FROM {SCHEMA}.tbl_part_presupuesto
                WHERE parte_id = {parte_id}
            """)
            total_lineas = cursor.fetchone()[0]

            # Calcular total
            cursor.execute(f"""
                SELECT SUM(cantidad * precio_unit)
                FROM {SCHEMA}.tbl_part_presupuesto
                WHERE parte_id = {parte_id}
            """)
            total_importe = cursor.fetchone()[0]

            cursor.close()

        print_success("Presupuesto verificado")
        print_info(f"  Líneas: {total_lineas}")
        print_info(f"  Importe total: {total_importe:.2f} €")
        return True

    except Exception as e:
        print_error(f"Error al verificar presupuesto: {e}")
        import traceback
        traceback.print_exc()
        return False

def paso_5_crear_certificacion():
    """Paso 5: Crear certificación del presupuesto"""
    print_test_header(5, "Crear certificación del presupuesto")

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Certificar 100% de cada línea de presupuesto
            for presup_id, precio_id, cantidad, precio_unit in presupuesto_items:
                cursor.execute(f"""
                    INSERT INTO {SCHEMA}.tbl_part_certificacion
                    (parte_id, precio_id, cantidad_cert, certificada)
                    VALUES (%s, %s, %s, %s)
                """, (parte_id, precio_id, cantidad, 1))  # 1 = certificada

            conn.commit()
            cursor.close()

        print_success("Certificación creada exitosamente")
        print_info(f"  Líneas certificadas: {len(presupuesto_items)}")
        return True

    except Exception as e:
        print_error(f"Error al crear certificación: {e}")
        import traceback
        traceback.print_exc()
        return False

def paso_6_verificar_certificacion():
    """Paso 6: Verificar certificación"""
    print_test_header(6, "Verificar certificación")

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Contar líneas certificadas
            cursor.execute(f"""
                SELECT COUNT(*)
                FROM {SCHEMA}.tbl_part_certificacion
                WHERE parte_id = {parte_id}
            """)
            total_lineas = cursor.fetchone()[0]

            # Calcular total certificado
            cursor.execute(f"""
                SELECT SUM(pc.cantidad_cert * pp.precio_unit)
                FROM {SCHEMA}.tbl_part_certificacion pc
                INNER JOIN {SCHEMA}.tbl_part_presupuesto pp ON pc.precio_id = pp.precio_id AND pc.parte_id = pp.parte_id
                WHERE pc.parte_id = {parte_id}
            """)
            total_certificado = cursor.fetchone()[0]

            cursor.close()

        print_success("Certificación verificada")
        print_info(f"  Líneas certificadas: {total_lineas}")
        print_info(f"  Importe certificado: {total_certificado:.2f} €")
        return True

    except Exception as e:
        print_error(f"Error al verificar certificación: {e}")
        import traceback
        traceback.print_exc()
        return False

def paso_7_generar_informe():
    """Paso 7: Generar informe con este parte"""
    print_test_header(7, "Generar informe con el parte de prueba")

    try:
        # Filtrar por el código del parte de prueba
        filtros = [
            {
                'campo': 'codigo',
                'operador': 'Igual a',
                'valor': TEST_CODIGO
            }
        ]

        query = build_query(
            "Resumen de Partes",
            filtros=filtros,
            clasificaciones=None,
            campos_seleccionados=None,
            schema=SCHEMA
        )

        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()

        if len(resultados) == 0:
            print_error("El informe no encontró el parte de prueba")
            return False

        if len(resultados) != 1:
            print_error(f"El informe encontró {len(resultados)} registros (debería ser 1)")
            return False

        print_success("Informe generado correctamente")
        print_info(f"  Registros encontrados: {len(resultados)}")
        print_info(f"  Primer registro: {resultados[0][:3]}...")
        return True

    except Exception as e:
        print_error(f"Error al generar informe: {e}")
        import traceback
        traceback.print_exc()
        return False

def paso_8_limpiar_datos():
    """Paso 8: Limpiar datos de prueba"""
    print_test_header(8, "Limpiar datos de prueba")

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Eliminar en orden inverso por foreign keys

            # 1. Eliminar certificaciones
            if parte_id:
                cursor.execute(f"""
                    DELETE FROM {SCHEMA}.tbl_part_certificacion
                    WHERE parte_id = {parte_id}
                """)
                print_info("  ✓ Certificaciones eliminadas")

            # 2. Eliminar presupuesto
            if parte_id:
                cursor.execute(f"""
                    DELETE FROM {SCHEMA}.tbl_part_presupuesto
                    WHERE parte_id = {parte_id}
                """)
                print_info("  ✓ Presupuesto eliminado")

            # 3. Eliminar parte
            if parte_id:
                cursor.execute(f"""
                    DELETE FROM {SCHEMA}.tbl_partes
                    WHERE id = {parte_id}
                """)
                print_info("  ✓ Parte eliminado")

            conn.commit()
            cursor.close()

        print_success("Datos de prueba eliminados exitosamente")
        return True

    except Exception as e:
        print_error(f"Error al limpiar datos: {e}")
        import traceback
        traceback.print_exc()
        return False

# Ejecución principal

def main():
    """Ejecutar test de flujo completo"""
    print("\n" + "=" * 80)
    print(" TEST DE FLUJO COMPLETO END-TO-END - HydroFlow Manager v1.04")
    print("=" * 80)
    print(f"\nConfiguración:")
    print(f"  Usuario: {USER}")
    print(f"  Esquema: {SCHEMA}")
    print(f"  Código de prueba: {TEST_CODIGO}")
    print()

    # Verificar credenciales
    if not USER or not PASSWORD:
        print_error("ERROR: Se requieren credenciales de base de datos")
        print_info("Configure DB_USER y DB_PASSWORD en el archivo .env")
        print_info("Consulte INSTALACION.md para más detalles")
        return False

    # Lista de pasos
    pasos = [
        ("Crear parte nuevo", paso_1_crear_parte),
        ("Verificar parte creado", paso_2_verificar_parte),
        ("Agregar presupuesto", paso_3_agregar_presupuesto),
        ("Verificar presupuesto", paso_4_verificar_presupuesto),
        ("Crear certificación", paso_5_crear_certificacion),
        ("Verificar certificación", paso_6_verificar_certificacion),
        ("Generar informe", paso_7_generar_informe),
        ("Limpiar datos de prueba", paso_8_limpiar_datos),
    ]

    # Ejecutar pasos
    resultados = []
    for nombre, paso_func in pasos:
        try:
            resultado = paso_func()
            resultados.append((nombre, resultado))

            # Si un paso falla, intentar limpiar y salir
            if not resultado:
                print_error(f"\n⚠️  Paso '{nombre}' falló. Intentando limpiar datos...")
                try:
                    paso_8_limpiar_datos()
                except:
                    pass
                break

        except Exception as e:
            print_error(f"Excepción no capturada en paso '{nombre}': {e}")
            resultados.append((nombre, False))
            break

    # Resumen
    print("\n" + "=" * 80)
    print(" RESUMEN DE RESULTADOS")
    print("=" * 80)

    passed = sum(1 for _, result in resultados if result)
    total = len(resultados)

    for nombre, resultado in resultados:
        status = "✅ PASS" if resultado else "❌ FAIL"
        print(f"{status} - {nombre}")

    print("\n" + "=" * 80)
    print(f"Resultado Final: {passed}/{total} pasos completados ({(passed/total)*100:.1f}%)")

    if passed == total:
        print("✅ ¡FLUJO COMPLETO FUNCIONA CORRECTAMENTE!")
        print("   El sistema está listo para producción (desde el punto de vista funcional)")
    else:
        print("❌ EL FLUJO COMPLETO FALLÓ")
        print("   Revisar los errores arriba antes de pasar a producción")

    print("=" * 80)
    print()

    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrumpido por el usuario")
        print("   Intentando limpiar datos de prueba...")
        try:
            paso_8_limpiar_datos()
        except:
            print("   ⚠️  No se pudieron limpiar los datos automáticamente")
            print(f"   Ejecuta manualmente: DELETE FROM tbl_partes WHERE codigo = '{TEST_CODIGO}';")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
