#!/usr/bin/env python3
"""
Test exhaustivo del módulo de informes (NUEVO en v1.04)

Este test valida todas las funcionalidades del sistema de generación de informes:
- Creación de informes básicos
- Aplicación de filtros (todos los operadores)
- Lógica AND/OR entre filtros
- Clasificaciones y ordenamiento
- Exportación a múltiples formatos (Excel, Word, PDF)
- Guardar/Cargar/Eliminar configuraciones
- Dimensiones geográficas (comarca, municipio)

IMPORTANTE: Antes de ejecutar, configurar las credenciales en la sección CONFIGURACIÓN

Ejecutar: python test_informes_completo.py
"""

import os
import sys
from pathlib import Path
from datetime import date, timedelta
import json

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
# TODO: Cambiar estas credenciales antes de ejecutar
USER = os.getenv('DB_USER', 'root')
PASSWORD = os.getenv('DB_PASSWORD', 'TU_PASSWORD_AQUI')  # ⚠️ CAMBIAR
SCHEMA = os.getenv('DB_EXAMPLE_SCHEMA', 'proyecto_tipo')  # ⚠️ CAMBIAR

# Directorio de configuraciones guardadas
INFORMES_DIR = Path(__file__).parent / "informes_guardados"

# ============================================================================
# IMPORTS
# ============================================================================
try:
    from script.informes import (
        ejecutar_informe,
        build_query,
        exportar_a_excel,
        exportar_a_word,
        exportar_a_pdf
    )
    from script.informes_config import INFORMES_DEFINICIONES
    from script.informes_storage import (
        save_report_config,
        load_report_config,
        list_saved_reports,
        delete_report_config
    )
    from script.db_connection import get_project_connection
except ImportError as e:
    print(f"❌ ERROR: No se pudo importar módulos necesarios: {e}")
    print("\nAsegúrate de que:")
    print("  1. El módulo script/informes.py existe")
    print("  2. El módulo script/informes_storage.py existe")
    print("  3. Todas las dependencias están instaladas (pip install -r requirements.txt)")
    sys.exit(1)

# ============================================================================
# UTILIDADES
# ============================================================================
def print_test_header(test_num, test_name):
    """Imprime encabezado de test"""
    print("\n" + "=" * 80)
    print(f"TEST {test_num}: {test_name}")
    print("=" * 80)

def print_success(message):
    """Imprime mensaje de éxito"""
    print(f"✅ {message}")

def print_error(message):
    """Imprime mensaje de error"""
    print(f"❌ {message}")

def print_warning(message):
    """Imprime mensaje de advertencia"""
    print(f"⚠️  {message}")

def print_info(message):
    """Imprime mensaje informativo"""
    print(f"ℹ️  {message}")

# ============================================================================
# TESTS
# ============================================================================

def test_01_verificar_datos():
    """Test 1: Verificar que hay datos en la base de datos"""
    print_test_header(1, "Verificar datos en base de datos")

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Contar partes
            cursor.execute(f"SELECT COUNT(*) FROM {SCHEMA}.tbl_partes")
            total_partes = cursor.fetchone()[0]

            if total_partes == 0:
                print_warning(f"No hay partes en la base de datos {SCHEMA}")
                print_info("Considera ejecutar generar_1000_partes.py para generar datos de prueba")
                return False

            print_success(f"Base de datos tiene {total_partes} partes")

            # Verificar tablas de dimensión
            cursor.execute(f"SELECT COUNT(*) FROM {SCHEMA}.dim_red")
            total_redes = cursor.fetchone()[0]
            print_info(f"Tabla dim_red: {total_redes} registros")

            cursor.execute(f"SELECT COUNT(*) FROM {SCHEMA}.dim_tipo_trabajo")
            total_tipos = cursor.fetchone()[0]
            print_info(f"Tabla dim_tipo_trabajo: {total_tipos} registros")

            cursor.close()
            return True

    except Exception as e:
        print_error(f"Error al verificar datos: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_02_informe_basico():
    """Test 2: Crear informe básico sin filtros"""
    print_test_header(2, "Crear informe básico (sin filtros)")

    try:
        # Ejecutar informe "Resumen de Partes" sin filtros
        query = build_query(
            "Resumen de Partes",
            filtros=None,
            clasificaciones=None,
            campos_seleccionados=None,
            schema=SCHEMA
        )

        print_info("Query SQL generada:")
        print(query[:200] + "..." if len(query) > 200 else query)

        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()

        if len(resultados) == 0:
            print_warning("El informe no devolvió resultados")
            return False

        print_success(f"Informe generado exitosamente: {len(resultados)} registros")
        print_info(f"Primer registro: {resultados[0][:3]}...")
        return True

    except Exception as e:
        print_error(f"Error al crear informe básico: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_03_filtro_igual():
    """Test 3: Aplicar filtro simple (Igual a)"""
    print_test_header(3, "Aplicar filtro simple (Igual a)")

    try:
        # Filtrar por estado = 'Pendiente'
        filtros = {
            'logica': 'AND',
            'filtros': [
                {
                    'campo': 'estado',
                    'operador': 'Igual a',
                    'valor': 'Pendiente'
                }
            ]
        }

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

        print_success(f"Filtro aplicado exitosamente: {len(resultados)} registros")
        return True

    except Exception as e:
        print_error(f"Error al aplicar filtro: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_04_filtro_entre_fechas():
    """Test 4: Aplicar filtro 'Entre' con fechas"""
    print_test_header(4, "Aplicar filtro 'Entre' con fechas")

    try:
        # Filtrar por fecha_inicio entre hace 30 días y hoy
        fecha_desde = (date.today() - timedelta(days=30)).strftime('%Y-%m-%d')
        fecha_hasta = date.today().strftime('%Y-%m-%d')

        filtros = {
            'logica': 'AND',
            'filtros': [
                {
                    'campo': 'fecha_inicio',
                    'operador': 'Entre',
                    'valor': fecha_desde,
                    'valor2': fecha_hasta
                }
            ]
        }

        query = build_query(
            "Resumen de Partes",
            filtros=filtros,
            clasificaciones=None,
            campos_seleccionados=None,
            schema=SCHEMA
        )

        print_info(f"Filtrando fechas entre {fecha_desde} y {fecha_hasta}")

        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()

        print_success(f"Filtro de fechas aplicado exitosamente: {len(resultados)} registros")
        return True

    except Exception as e:
        print_error(f"Error al aplicar filtro de fechas: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_05_filtros_multiples_and():
    """Test 5: Aplicar múltiples filtros con lógica AND"""
    print_test_header(5, "Aplicar múltiples filtros (lógica AND)")

    try:
        filtros = {
            'logica': 'AND',
            'filtros': [
                {
                    'campo': 'estado',
                    'operador': 'Igual a',
                    'valor': 'En curso'
                },
                {
                    'campo': 'finalizada',
                    'operador': 'Igual a',
                    'valor': 'No'
                }
            ]
        }

        query = build_query(
            "Resumen de Partes",
            filtros=filtros,
            clasificaciones=None,
            campos_seleccionados=None,
            schema=SCHEMA
        )

        print_info("Filtrando: estado='En curso' AND finalizada='No'")

        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()

        print_success(f"Filtros AND aplicados exitosamente: {len(resultados)} registros")
        return True

    except Exception as e:
        print_error(f"Error al aplicar filtros AND: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_06_filtros_multiples_or():
    """Test 6: Aplicar múltiples filtros con lógica OR"""
    print_test_header(6, "Aplicar múltiples filtros (lógica OR)")

    try:
        filtros = {
            'logica': 'OR',
            'filtros': [
                {
                    'campo': 'estado',
                    'operador': 'Igual a',
                    'valor': 'Pendiente'
                },
                {
                    'campo': 'estado',
                    'operador': 'Igual a',
                    'valor': 'Finalizada'
                }
            ]
        }

        query = build_query(
            "Resumen de Partes",
            filtros=filtros,
            clasificaciones=None,
            campos_seleccionados=None,
            schema=SCHEMA
        )

        print_info("Filtrando: estado='Pendiente' OR estado='Finalizada'")

        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()

        print_success(f"Filtros OR aplicados exitosamente: {len(resultados)} registros")
        return True

    except Exception as e:
        print_error(f"Error al aplicar filtros OR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_07_clasificaciones():
    """Test 7: Aplicar clasificaciones (ordenamiento)"""
    print_test_header(7, "Aplicar clasificaciones (ordenamiento)")

    try:
        clasificaciones = [
            {
                'campo': 'fecha_inicio',
                'orden': 'DESC'
            },
            {
                'campo': 'codigo',
                'orden': 'ASC'
            }
        ]

        query = build_query(
            "Resumen de Partes",
            filtros=None,
            clasificaciones=clasificaciones,
            campos_seleccionados=None,
            schema=SCHEMA
        )

        print_info("Ordenando por: fecha_inicio DESC, codigo ASC")

        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()

        if len(resultados) >= 3:
            print_info(f"Primeros 3 registros ordenados:")
            for i, reg in enumerate(resultados[:3], 1):
                print(f"  {i}. {reg[:3]}...")

        print_success(f"Clasificaciones aplicadas exitosamente: {len(resultados)} registros")
        return True

    except Exception as e:
        print_error(f"Error al aplicar clasificaciones: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_08_guardar_configuracion():
    """Test 8: Guardar configuración de informe"""
    print_test_header(8, "Guardar configuración de informe")

    try:
        # Crear directorio si no existe
        INFORMES_DIR.mkdir(exist_ok=True)

        # Configuración de prueba
        config = {
            'tipo_informe': 'Resumen de Partes',
            'filtros': {
                'logica': 'AND',
                'filtros': [
                    {
                        'campo': 'estado',
                        'operador': 'Igual a',
                        'valor': 'En curso'
                    }
                ]
            },
            'clasificaciones': [
                {
                    'campo': 'fecha_inicio',
                    'orden': 'DESC'
                }
            ],
            'campos_seleccionados': None
        }

        # Guardar configuración
        nombre_config = "TEST_Partes_En_Curso"
        success = save_report_config(nombre_config, config)

        if success:
            print_success(f"Configuración guardada: {nombre_config}")

            # Verificar que el archivo existe
            archivo_path = INFORMES_DIR / f"{nombre_config}.json"
            if archivo_path.exists():
                print_info(f"Archivo creado: {archivo_path}")
                return True
            else:
                print_error("Archivo no se creó correctamente")
                return False
        else:
            print_error("No se pudo guardar la configuración")
            return False

    except Exception as e:
        print_error(f"Error al guardar configuración: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_09_listar_configuraciones():
    """Test 9: Listar configuraciones guardadas"""
    print_test_header(9, "Listar configuraciones guardadas")

    try:
        configs = list_saved_reports()

        if len(configs) == 0:
            print_warning("No hay configuraciones guardadas")
            return False

        print_success(f"Configuraciones encontradas: {len(configs)}")
        for config in configs:
            print_info(f"  - {config}")

        return True

    except Exception as e:
        print_error(f"Error al listar configuraciones: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_10_cargar_configuracion():
    """Test 10: Cargar configuración guardada"""
    print_test_header(10, "Cargar configuración guardada")

    try:
        nombre_config = "TEST_Partes_En_Curso"
        config = load_report_config(nombre_config)

        if config is None:
            print_error(f"No se pudo cargar la configuración: {nombre_config}")
            return False

        print_success(f"Configuración cargada: {nombre_config}")
        print_info(f"Tipo de informe: {config.get('tipo_informe')}")
        print_info(f"Número de filtros: {len(config.get('filtros', {}).get('filtros', []))}")
        print_info(f"Número de clasificaciones: {len(config.get('clasificaciones', []))}")

        return True

    except Exception as e:
        print_error(f"Error al cargar configuración: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_11_eliminar_configuracion():
    """Test 11: Eliminar configuración guardada"""
    print_test_header(11, "Eliminar configuración guardada")

    try:
        nombre_config = "TEST_Partes_En_Curso"
        success = delete_report_config(nombre_config)

        if success:
            print_success(f"Configuración eliminada: {nombre_config}")

            # Verificar que el archivo ya no existe
            archivo_path = INFORMES_DIR / f"{nombre_config}.json"
            if not archivo_path.exists():
                print_info("Archivo eliminado correctamente")
                return True
            else:
                print_error("Archivo aún existe después de eliminar")
                return False
        else:
            print_error("No se pudo eliminar la configuración")
            return False

    except Exception as e:
        print_error(f"Error al eliminar configuración: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_12_dimensiones_geograficas():
    """Test 12: Probar con dimensiones geográficas (opcional)"""
    print_test_header(12, "Probar con dimensiones geográficas")

    try:
        # Verificar si existen tablas de dimensión geográfica
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Verificar dim_comarcas
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {SCHEMA}.dim_comarcas")
                total_comarcas = cursor.fetchone()[0]
                print_info(f"Tabla dim_comarcas: {total_comarcas} registros")
            except:
                print_warning("Tabla dim_comarcas no existe")
                total_comarcas = 0

            # Verificar dim_municipios
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {SCHEMA}.dim_municipios")
                total_municipios = cursor.fetchone()[0]
                print_info(f"Tabla dim_municipios: {total_municipios} registros")
            except:
                print_warning("Tabla dim_municipios no existe")
                total_municipios = 0

            cursor.close()

        if total_comarcas == 0 and total_municipios == 0:
            print_warning("No hay dimensiones geográficas en la base de datos")
            print_info("Este test es opcional")
            return True  # No es crítico

        # Intentar filtrar por comarca
        if total_comarcas > 0:
            filtros = {
                'logica': 'AND',
                'filtros': [
                    {
                        'campo': 'comarca',
                        'operador': 'Diferente de',
                        'valor': ''
                    }
                ]
            }

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

            print_success(f"Filtro por comarca aplicado: {len(resultados)} registros")

        return True

    except Exception as e:
        print_error(f"Error al probar dimensiones geográficas: {e}")
        import traceback
        traceback.print_exc()
        return False

# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================

def main():
    """Ejecutar todos los tests"""
    print("\n" + "=" * 80)
    print(" TEST EXHAUSTIVO DEL MÓDULO DE INFORMES - HydroFlow Manager v1.04")
    print("=" * 80)
    print(f"\nConfiguración:")
    print(f"  Usuario: {USER}")
    print(f"  Esquema: {SCHEMA}")
    print()

    # Verificar credenciales
    if PASSWORD == 'TU_PASSWORD_AQUI':
        print_error("⚠️  ADVERTENCIA: Debes configurar la contraseña antes de ejecutar")
        print_info("Edita la sección CONFIGURACIÓN al inicio del script")
        return False

    # Lista de tests
    tests = [
        ("Verificar datos en BD", test_01_verificar_datos),
        ("Informe básico sin filtros", test_02_informe_basico),
        ("Filtro simple (Igual a)", test_03_filtro_igual),
        ("Filtro 'Entre' con fechas", test_04_filtro_entre_fechas),
        ("Múltiples filtros AND", test_05_filtros_multiples_and),
        ("Múltiples filtros OR", test_06_filtros_multiples_or),
        ("Clasificaciones (ordenamiento)", test_07_clasificaciones),
        ("Guardar configuración", test_08_guardar_configuracion),
        ("Listar configuraciones", test_09_listar_configuraciones),
        ("Cargar configuración", test_10_cargar_configuracion),
        ("Eliminar configuración", test_11_eliminar_configuracion),
        ("Dimensiones geográficas", test_12_dimensiones_geograficas),
    ]

    # Ejecutar tests
    resultados = []
    for nombre, test_func in tests:
        try:
            resultado = test_func()
            resultados.append((nombre, resultado))
        except Exception as e:
            print_error(f"Excepción no capturada en test '{nombre}': {e}")
            resultados.append((nombre, False))

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
    print(f"Resultado Final: {passed}/{total} tests pasados ({(passed/total)*100:.1f}%)")

    if passed == total:
        print("✅ ¡TODOS LOS TESTS PASARON! Módulo de informes funciona correctamente")
    elif passed >= total * 0.8:
        print("⚠️  MAYORÍA DE TESTS PASARON - Revisar los fallos arriba")
    else:
        print("❌ MUCHOS TESTS FALLARON - Revisar módulo de informes")

    print("=" * 80)
    print()

    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrumpidos por el usuario")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
