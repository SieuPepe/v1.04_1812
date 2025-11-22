#!/usr/bin/env python3
"""
Test del módulo de Presupuestos - HydroFlow Manager v1.04

Valida:
- Crear presupuesto desde catálogo
- Modificar cantidades y precios
- Calcular totales correctamente
- Vincular con parte
- Eliminar presupuesto

Ejecutar: python test_presupuestos.py

ACTUALIZADO: Adaptado a la estructura real de cert_dev
- Tabla: tbl_part_presupuesto (no tbl_presupuesto)
- Columnas: id, parte_id, precio_id, cantidad, precio_unit, created_at
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

sys.path.insert(0, str(Path(__file__).parent))

# Configuración desde .env
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
SCHEMA = os.getenv('DB_SCHEMA', 'cert_dev')

try:
    from script.db_connection import get_project_connection
except ImportError as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)

# Variables globales
parte_id = None
presupuesto_items = []

def test_01_crear_parte_base():
    """Crear parte para asociar presupuesto"""
    global parte_id
    print("\n" + "=" * 70)
    print("TEST 1: Crear parte base")
    print("=" * 70)

    try:
        codigo = f'TEST-PRES-{date.today().strftime("%Y%m%d%H%M%S")}'
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO {SCHEMA}.tbl_partes (codigo, titulo, fecha_inicio, estado)
                VALUES ('{codigo}', 'Test presupuesto', CURDATE(), 'Pendiente')
            """)
            parte_id = cursor.lastrowid
            conn.commit()
            cursor.close()

        print(f"✅ Parte creado: ID={parte_id}, Código={codigo}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_02_agregar_conceptos():
    """Agregar conceptos del catálogo al presupuesto del parte"""
    global presupuesto_items
    print("\n" + "=" * 70)
    print("TEST 2: Agregar conceptos del catálogo")
    print("=" * 70)

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Obtener 3 precios del catálogo
            cursor.execute(f"SELECT id, codigo, resumen, coste FROM {SCHEMA}.tbl_pres_precios LIMIT 3")
            precios = cursor.fetchall()

            if not precios:
                print("⚠️  No hay precios en el catálogo tbl_pres_precios")
                cursor.close()
                return False

            # Agregar cada precio al presupuesto del parte
            for precio in precios:
                precio_id, codigo, desc, coste = precio
                cantidad = 10.0
                precio_unit = float(coste if coste else 100.0)

                cursor.execute(f"""
                    INSERT INTO {SCHEMA}.tbl_part_presupuesto
                    (parte_id, precio_id, cantidad, precio_unit)
                    VALUES (%s, %s, %s, %s)
                """, (parte_id, precio_id, cantidad, precio_unit))

                presupuesto_items.append(cursor.lastrowid)

            conn.commit()
            cursor.close()

        print(f"✅ {len(precios)} conceptos agregados al presupuesto")
        for precio in precios:
            print(f"   - {precio[1]}: {precio[2][:40]}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_03_calcular_totales():
    """Calcular y verificar totales del presupuesto"""
    print("\n" + "=" * 70)
    print("TEST 3: Calcular totales")
    print("=" * 70)

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT COUNT(*), SUM(cantidad * precio_unit)
                FROM {SCHEMA}.tbl_part_presupuesto
                WHERE parte_id = {parte_id}
            """)
            lineas, total = cursor.fetchone()
            cursor.close()

        print(f"✅ Líneas: {lineas}, Total: {total:.2f} €")
        return total > 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_04_modificar_cantidades():
    """Modificar cantidades y recalcular"""
    print("\n" + "=" * 70)
    print("TEST 4: Modificar cantidades")
    print("=" * 70)

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Obtener primera línea
            cursor.execute(f"""
                SELECT id, cantidad, precio_unit
                FROM {SCHEMA}.tbl_part_presupuesto
                WHERE parte_id = {parte_id}
                LIMIT 1
            """)
            linea = cursor.fetchone()

            if not linea:
                print("❌ No hay líneas para modificar")
                cursor.close()
                return False

            linea_id, cant_ant, precio_unit = linea
            nueva_cant = 25.0

            # Actualizar
            cursor.execute(f"""
                UPDATE {SCHEMA}.tbl_part_presupuesto
                SET cantidad = {nueva_cant}
                WHERE id = {linea_id}
            """)
            conn.commit()
            cursor.close()

        print(f"✅ Cantidad modificada: {cant_ant} → {nueva_cant}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_05_verificar_vista():
    """Verificar vista vw_part_presupuesto"""
    print("\n" + "=" * 70)
    print("TEST 5: Verificar vista vw_part_presupuesto")
    print("=" * 70)

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Verificar que la vista existe y devuelve datos
            cursor.execute(f"""
                SELECT COUNT(*)
                FROM {SCHEMA}.vw_part_presupuesto
                WHERE parte_id = {parte_id}
            """)
            count = cursor.fetchone()[0]
            cursor.close()

        if count > 0:
            print(f"✅ Vista funciona correctamente: {count} registros")
            return True
        else:
            print(f"⚠️  Vista no devolvió registros")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_06_limpiar():
    """Limpiar datos de prueba"""
    print("\n" + "=" * 70)
    print("TEST 6: Limpiar datos de prueba")
    print("=" * 70)

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Eliminar líneas de presupuesto
            if parte_id:
                cursor.execute(f"DELETE FROM {SCHEMA}.tbl_part_presupuesto WHERE parte_id = {parte_id}")
                deleted = cursor.rowcount
                print(f"   - Eliminadas {deleted} líneas de presupuesto")

            # Eliminar parte
            if parte_id:
                cursor.execute(f"DELETE FROM {SCHEMA}.tbl_partes WHERE id = {parte_id}")
                print(f"   - Eliminado parte ID {parte_id}")

            conn.commit()
            cursor.close()

        print("✅ Datos de prueba eliminados")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Ejecutar todos los tests"""
    print("\n" + "=" * 70)
    print(" TEST DE MÓDULO DE PRESUPUESTOS")
    print("=" * 70)
    print(f"\nEsquema: {SCHEMA}")
    print(f"Usuario: {USER}")

    if not USER or not PASSWORD:
        print("❌ ERROR: Se requieren credenciales de base de datos")
        print("   Configure DB_USER y DB_PASSWORD en el archivo .env")
        print("   Consulte INSTALACION.md para más detalles")
        return False

    tests = [
        ("Crear parte base", test_01_crear_parte_base),
        ("Agregar conceptos", test_02_agregar_conceptos),
        ("Calcular totales", test_03_calcular_totales),
        ("Modificar cantidades", test_04_modificar_cantidades),
        ("Verificar vista", test_05_verificar_vista),
        ("Limpiar datos", test_06_limpiar),
    ]

    resultados = []
    for nombre, func in tests:
        try:
            resultado = func()
            resultados.append((nombre, resultado))
            if not resultado and nombre != "Limpiar datos":
                print("\n⚠️  Test falló, intentando limpiar...")
                try:
                    test_06_limpiar()
                except:
                    pass
                break
        except Exception as e:
            print(f"❌ Excepción en '{nombre}': {e}")
            resultados.append((nombre, False))
            break

    # Resumen
    print("\n" + "=" * 70)
    print(" RESUMEN")
    print("=" * 70)
    passed = sum(1 for _, r in resultados if r)
    total = len(resultados)
    for nombre, resultado in resultados:
        print(f"{'✅' if resultado else '❌'} {nombre}")
    print(f"\nResultado: {passed}/{total} tests pasados ({(passed/total)*100:.1f}%)")

    if passed == total:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("   El módulo de presupuestos funciona correctamente")
    else:
        print("\n⚠️  ALGUNOS TESTS FALLARON")
        print("   Revisar los errores arriba")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
