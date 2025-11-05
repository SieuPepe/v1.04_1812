#!/usr/bin/env python3
"""
Test del módulo de Certificaciones - HydroFlow Manager v1.04

Valida:
- Crear certificación desde presupuesto
- Marcar conceptos como certificados
- Calcular pendiente correctamente
- Certificación parcial y completa
- Eliminar certificación

Ejecutar: python test_certificaciones.py

ACTUALIZADO: Adaptado a la estructura real de cert_dev
- Tabla presupuesto: tbl_part_presupuesto
- Tabla certificación: tbl_part_certificacion
- Relación: parte_id y precio_id (del presupuesto)
"""

import os
import sys
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent))

# Configuración
USER = os.getenv('DB_USER', 'root')
PASSWORD = os.getenv('DB_PASSWORD', 'TU_PASSWORD_AQUI')  # ⚠️ CAMBIAR
SCHEMA = os.getenv('DB_EXAMPLE_SCHEMA', 'cert_dev')  # ⚠️ CAMBIAR

try:
    from script.db_connection import get_project_connection
except ImportError as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)

# Variables globales
parte_id = None
presupuesto_items = []

def test_01_crear_presupuesto_completo():
    """Crear parte y presupuesto completo"""
    global parte_id, presupuesto_items
    print("\n" + "=" * 70)
    print("TEST 1: Crear parte y presupuesto completo")
    print("=" * 70)

    try:
        codigo = f'TEST-CERT-{date.today().strftime("%Y%m%d%H%M%S")}'
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Crear parte
            cursor.execute(f"""
                INSERT INTO {SCHEMA}.tbl_partes (codigo, titulo, fecha_inicio, estado)
                VALUES ('{codigo}', 'Test certificación', CURDATE(), 'Pendiente')
            """)
            parte_id = cursor.lastrowid
            print(f"   ✓ Parte creado: ID={parte_id}")

            # Obtener 5 precios del catálogo
            cursor.execute(f"SELECT id, descripcion, precio_unit FROM {SCHEMA}.tbl_pres_precios LIMIT 5")
            precios = cursor.fetchall()

            if not precios:
                print("⚠️  No hay precios en el catálogo")
                cursor.close()
                return False

            # Crear líneas de presupuesto
            for precio in precios:
                precio_id, desc, precio_unit = precio
                cantidad = 20.0
                precio_unit = float(precio_unit if precio_unit else 100.0)

                cursor.execute(f"""
                    INSERT INTO {SCHEMA}.tbl_part_presupuesto
                    (parte_id, precio_id, cantidad, precio_unit)
                    VALUES (%s, %s, %s, %s)
                """, (parte_id, precio_id, cantidad, precio_unit))

                presupuesto_items.append((cursor.lastrowid, precio_id, cantidad, precio_unit))

            conn.commit()
            cursor.close()

        print(f"✅ Presupuesto creado: {len(precios)} conceptos")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_02_certificar_parcial():
    """Certificar parcialmente (50% de cada concepto)"""
    print("\n" + "=" * 70)
    print("TEST 2: Certificar parcialmente (50%)")
    print("=" * 70)

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Certificar 50% de cada concepto
            for presup_id, precio_id, cantidad, precio_unit in presupuesto_items:
                cant_cert = cantidad * 0.5

                cursor.execute(f"""
                    INSERT INTO {SCHEMA}.tbl_part_certificacion
                    (parte_id, precio_id, cantidad_cert, certificada)
                    VALUES (%s, %s, %s, %s)
                """, (parte_id, precio_id, cant_cert, 0))  # 0 = no certificada todavía

            conn.commit()
            cursor.close()

        print(f"✅ Certificados {len(presupuesto_items)} conceptos al 50%")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_03_verificar_pendiente():
    """Verificar cálculo de pendiente de certificar"""
    print("\n" + "=" * 70)
    print("TEST 3: Verificar pendiente")
    print("=" * 70)

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Total presupuestado
            cursor.execute(f"""
                SELECT SUM(cantidad * precio_unit)
                FROM {SCHEMA}.tbl_part_presupuesto
                WHERE parte_id = {parte_id}
            """)
            total_pres = float(cursor.fetchone()[0] or 0)

            # Total certificado
            cursor.execute(f"""
                SELECT SUM(pc.cantidad_cert * pp.precio_unit)
                FROM {SCHEMA}.tbl_part_certificacion pc
                INNER JOIN {SCHEMA}.tbl_part_presupuesto pp ON pc.precio_id = pp.precio_id AND pc.parte_id = pp.parte_id
                WHERE pc.parte_id = {parte_id}
            """)
            total_cert = float(cursor.fetchone()[0] or 0)

            pendiente = total_pres - total_cert
            porcentaje_cert = (total_cert / total_pres * 100) if total_pres > 0 else 0

            cursor.close()

        print(f"✅ Presupuestado: {total_pres:.2f} €")
        print(f"✅ Certificado: {total_cert:.2f} € ({porcentaje_cert:.1f}%)")
        print(f"✅ Pendiente: {pendiente:.2f} €")

        # Verificar que es aproximadamente 50%
        return 45 <= porcentaje_cert <= 55

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_04_marcar_certificadas():
    """Marcar certificaciones como certificadas"""
    print("\n" + "=" * 70)
    print("TEST 4: Marcar certificaciones como certificadas")
    print("=" * 70)

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Marcar todas las certificaciones como certificadas
            cursor.execute(f"""
                UPDATE {SCHEMA}.tbl_part_certificacion
                SET certificada = 1
                WHERE parte_id = {parte_id}
            """)

            updated = cursor.rowcount
            conn.commit()
            cursor.close()

        print(f"✅ {updated} certificaciones marcadas como certificadas")
        return updated > 0

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_05_verificar_vista():
    """Verificar vista vw_part_certificaciones"""
    print("\n" + "=" * 70)
    print("TEST 5: Verificar vista vw_part_certificaciones")
    print("=" * 70)

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Verificar que la vista existe y devuelve datos
            cursor.execute(f"""
                SELECT COUNT(*)
                FROM {SCHEMA}.vw_part_certificaciones
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

            # Eliminar certificaciones
            if parte_id:
                cursor.execute(f"DELETE FROM {SCHEMA}.tbl_part_certificacion WHERE parte_id = {parte_id}")
                print(f"   - Eliminadas certificaciones")

            # Eliminar presupuesto
            if parte_id:
                cursor.execute(f"DELETE FROM {SCHEMA}.tbl_part_presupuesto WHERE parte_id = {parte_id}")
                print(f"   - Eliminado presupuesto")

            # Eliminar parte
            if parte_id:
                cursor.execute(f"DELETE FROM {SCHEMA}.tbl_partes WHERE id = {parte_id}")
                print(f"   - Eliminado parte")

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
    print(" TEST DE MÓDULO DE CERTIFICACIONES")
    print("=" * 70)
    print(f"\nEsquema: {SCHEMA}")
    print(f"Usuario: {USER}")

    if PASSWORD == 'TU_PASSWORD_AQUI':
        print("❌ ERROR: Configurar PASSWORD en la sección CONFIGURACIÓN")
        return False

    tests = [
        ("Crear presupuesto completo", test_01_crear_presupuesto_completo),
        ("Certificar parcial (50%)", test_02_certificar_parcial),
        ("Verificar pendiente", test_03_verificar_pendiente),
        ("Marcar certificadas", test_04_marcar_certificadas),
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
        print("   El módulo de certificaciones funciona correctamente")
    else:
        print("\n⚠️  ALGUNOS TESTS FALLARON")
        print("   Revisar los errores arriba")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
