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
"""

import os
import sys
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent))

# Configuración
USER = os.getenv('DB_USER', 'root')
PASSWORD = os.getenv('DB_PASSWORD', 'TU_PASSWORD_AQUI')  # ⚠️ CAMBIAR
SCHEMA = os.getenv('DB_EXAMPLE_SCHEMA', 'proyecto_tipo')  # ⚠️ CAMBIAR

try:
    from script.db_connection import get_project_connection, get_manager_connection
except ImportError as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)

# Variables globales
parte_id = None
presupuesto_id = None

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

def test_02_crear_presupuesto():
    """Crear presupuesto vinculado al parte"""
    global presupuesto_id
    print("\n" + "=" * 70)
    print("TEST 2: Crear presupuesto")
    print("=" * 70)

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO {SCHEMA}.tbl_presupuesto
                (parte_id, codigo, descripcion, fecha_creacion, estado)
                VALUES ({parte_id}, 'PRES-TEST-001', 'Presupuesto de prueba', CURDATE(), 'Pendiente')
            """)
            presupuesto_id = cursor.lastrowid
            conn.commit()
            cursor.close()

        print(f"✅ Presupuesto creado: ID={presupuesto_id}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_03_agregar_conceptos():
    """Agregar conceptos del catálogo al presupuesto"""
    print("\n" + "=" * 70)
    print("TEST 3: Agregar conceptos del catálogo")
    print("=" * 70)

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Obtener 3 conceptos del catálogo
            cursor.execute("SELECT id, codigo, descripcion, precio_unitario, unidad FROM manager.tbl_catalogo LIMIT 3")
            conceptos = cursor.fetchall()

            if not conceptos:
                print("⚠️  No hay conceptos en el catálogo")
                cursor.close()
                return False

            # Agregar cada concepto
            for concepto in conceptos:
                cat_id, codigo, desc, precio, unidad = concepto
                cantidad = 10.0
                precio = float(precio if precio else 100.0)
                importe = cantidad * precio

                cursor.execute(f"""
                    INSERT INTO {SCHEMA}.tbl_pres_precios
                    (presupuesto_id, catalogo_id, descripcion, cantidad, precio_unitario, unidad, importe)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (presupuesto_id, cat_id, desc, cantidad, precio, unidad or 'ud', importe))

            conn.commit()
            cursor.close()

        print(f"✅ {len(conceptos)} conceptos agregados")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_04_calcular_totales():
    """Calcular y verificar totales del presupuesto"""
    print("\n" + "=" * 70)
    print("TEST 4: Calcular totales")
    print("=" * 70)

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT COUNT(*), SUM(importe)
                FROM {SCHEMA}.tbl_pres_precios
                WHERE presupuesto_id = {presupuesto_id}
            """)
            lineas, total = cursor.fetchone()
            cursor.close()

        print(f"✅ Líneas: {lineas}, Total: {total:.2f} €")
        return total > 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_05_modificar_cantidades():
    """Modificar cantidades y recalcular"""
    print("\n" + "=" * 70)
    print("TEST 5: Modificar cantidades")
    print("=" * 70)

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Obtener primera línea
            cursor.execute(f"""
                SELECT id, cantidad, precio_unitario
                FROM {SCHEMA}.tbl_pres_precios
                WHERE presupuesto_id = {presupuesto_id}
                LIMIT 1
            """)
            linea = cursor.fetchone()

            if not linea:
                print("❌ No hay líneas para modificar")
                cursor.close()
                return False

            linea_id, cant_ant, precio = linea
            nueva_cant = 25.0
            nuevo_importe = nueva_cant * float(precio)

            # Actualizar
            cursor.execute(f"""
                UPDATE {SCHEMA}.tbl_pres_precios
                SET cantidad = {nueva_cant}, importe = {nuevo_importe}
                WHERE id = {linea_id}
            """)
            conn.commit()
            cursor.close()

        print(f"✅ Cantidad modificada: {cant_ant} → {nueva_cant}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
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
            if presupuesto_id:
                cursor.execute(f"DELETE FROM {SCHEMA}.tbl_pres_precios WHERE presupuesto_id = {presupuesto_id}")

            # Eliminar presupuesto
            if presupuesto_id:
                cursor.execute(f"DELETE FROM {SCHEMA}.tbl_presupuesto WHERE id = {presupuesto_id}")

            # Eliminar parte
            if parte_id:
                cursor.execute(f"DELETE FROM {SCHEMA}.tbl_partes WHERE id = {parte_id}")

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

    if PASSWORD == 'TU_PASSWORD_AQUI':
        print("❌ ERROR: Configurar PASSWORD en la sección CONFIGURACIÓN")
        return False

    tests = [
        ("Crear parte base", test_01_crear_parte_base),
        ("Crear presupuesto", test_02_crear_presupuesto),
        ("Agregar conceptos", test_03_agregar_conceptos),
        ("Calcular totales", test_04_calcular_totales),
        ("Modificar cantidades", test_05_modificar_cantidades),
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

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
