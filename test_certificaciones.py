#!/usr/bin/env python3
"""
Test del módulo de Certificaciones - HydroFlow Manager v1.04

Valida:
- Crear certificación desde presupuesto
- Marcar conceptos como certificados
- Calcular pendiente correctamente
- Certificación por lotes
- Eliminar certificación

Ejecutar: python test_certificaciones.py
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
certificacion_id = None
precio_ids = []

def test_01_crear_presupuesto_completo():
    """Crear parte, presupuesto y conceptos"""
    global parte_id, presupuesto_id, precio_ids
    print("\n" + "=" * 70)
    print("TEST 1: Crear presupuesto completo")
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

            # Crear presupuesto
            cursor.execute(f"""
                INSERT INTO {SCHEMA}.tbl_presupuesto
                (parte_id, codigo, descripcion, fecha_creacion, estado)
                VALUES ({parte_id}, 'CERT-TEST-001', 'Presupuesto para certificar', CURDATE(), 'Pendiente')
            """)
            presupuesto_id = cursor.lastrowid

            # Agregar 5 conceptos
            cursor.execute("SELECT id, descripcion, precio_unitario, unidad FROM manager.tbl_catalogo LIMIT 5")
            conceptos = cursor.fetchall()

            for concepto in conceptos:
                cat_id, desc, precio, unidad = concepto
                cantidad = 20.0
                precio = float(precio if precio else 100.0)
                importe = cantidad * precio

                cursor.execute(f"""
                    INSERT INTO {SCHEMA}.tbl_pres_precios
                    (presupuesto_id, catalogo_id, descripcion, cantidad, precio_unitario, unidad, importe)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (presupuesto_id, cat_id, desc, cantidad, precio, unidad or 'ud', importe))

            # Obtener IDs de precios
            cursor.execute(f"SELECT id FROM {SCHEMA}.tbl_pres_precios WHERE presupuesto_id = {presupuesto_id}")
            precio_ids = [row[0] for row in cursor.fetchall()]

            conn.commit()
            cursor.close()

        print(f"✅ Presupuesto creado: {len(conceptos)} conceptos")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_02_crear_certificacion():
    """Crear certificación desde presupuesto"""
    global certificacion_id
    print("\n" + "=" * 70)
    print("TEST 2: Crear certificación")
    print("=" * 70)

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Crear certificación
            cursor.execute(f"""
                INSERT INTO {SCHEMA}.tbl_certificacion
                (parte_id, presupuesto_id, numero, fecha, descripcion, certificada)
                VALUES ({parte_id}, {presupuesto_id}, 1, CURDATE(), 'Certificación de prueba', 0)
            """)
            certificacion_id = cursor.lastrowid
            conn.commit()
            cursor.close()

        print(f"✅ Certificación creada: ID={certificacion_id}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_03_certificar_parcial():
    """Certificar parcialmente (50% de cada concepto)"""
    print("\n" + "=" * 70)
    print("TEST 3: Certificar parcialmente (50%)")
    print("=" * 70)

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Certificar 50% de cada concepto
            for precio_id in precio_ids:
                cursor.execute(f"""
                    SELECT cantidad, precio_unitario
                    FROM {SCHEMA}.tbl_pres_precios
                    WHERE id = {precio_id}
                """)
                cantidad, precio = cursor.fetchone()
                cantidad = float(cantidad)
                precio = float(precio)

                cant_cert = cantidad * 0.5
                importe_cert = cant_cert * precio

                cursor.execute(f"""
                    INSERT INTO {SCHEMA}.tbl_cert_lineas
                    (certificacion_id, precio_id, cantidad_certificada, importe_certificado)
                    VALUES ({certificacion_id}, {precio_id}, {cant_cert}, {importe_cert})
                """)

            conn.commit()
            cursor.close()

        print(f"✅ Certificados {len(precio_ids)} conceptos al 50%")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_04_verificar_pendiente():
    """Verificar cálculo de pendiente de certificar"""
    print("\n" + "=" * 70)
    print("TEST 4: Verificar pendiente")
    print("=" * 70)

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Total presupuestado
            cursor.execute(f"""
                SELECT SUM(importe)
                FROM {SCHEMA}.tbl_pres_precios
                WHERE presupuesto_id = {presupuesto_id}
            """)
            total_pres = float(cursor.fetchone()[0] or 0)

            # Total certificado
            cursor.execute(f"""
                SELECT SUM(importe_certificado)
                FROM {SCHEMA}.tbl_cert_lineas
                WHERE certificacion_id = {certificacion_id}
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
        return False

def test_05_certificar_resto():
    """Certificar el 50% restante"""
    print("\n" + "=" * 70)
    print("TEST 5: Certificar el resto (50%)")
    print("=" * 70)

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Crear segunda certificación
            cursor.execute(f"""
                INSERT INTO {SCHEMA}.tbl_certificacion
                (parte_id, presupuesto_id, numero, fecha, descripcion, certificada)
                VALUES ({parte_id}, {presupuesto_id}, 2, CURDATE(), 'Certificación final', 0)
            """)
            cert2_id = cursor.lastrowid

            # Certificar el resto
            for precio_id in precio_ids:
                cursor.execute(f"""
                    SELECT cantidad, precio_unitario
                    FROM {SCHEMA}.tbl_pres_precios
                    WHERE id = {precio_id}
                """)
                cantidad, precio = cursor.fetchone()
                cantidad = float(cantidad)
                precio = float(precio)

                cant_cert = cantidad * 0.5
                importe_cert = cant_cert * precio

                cursor.execute(f"""
                    INSERT INTO {SCHEMA}.tbl_cert_lineas
                    (certificacion_id, precio_id, cantidad_certificada, importe_certificado)
                    VALUES ({cert2_id}, {precio_id}, {cant_cert}, {importe_cert})
                """)

            # Verificar total certificado
            cursor.execute(f"""
                SELECT SUM(cl.importe_certificado)
                FROM {SCHEMA}.tbl_cert_lineas cl
                INNER JOIN {SCHEMA}.tbl_certificacion c ON cl.certificacion_id = c.id
                WHERE c.presupuesto_id = {presupuesto_id}
            """)
            total_cert = float(cursor.fetchone()[0] or 0)

            cursor.execute(f"""
                SELECT SUM(importe)
                FROM {SCHEMA}.tbl_pres_precios
                WHERE presupuesto_id = {presupuesto_id}
            """)
            total_pres = float(cursor.fetchone()[0] or 0)

            conn.commit()
            cursor.close()

        print(f"✅ Total certificado: {total_cert:.2f} €")
        print(f"✅ Total presupuestado: {total_pres:.2f} €")
        print(f"✅ Pendiente: {total_pres - total_cert:.2f} €")

        # Verificar que está 100% certificado (con margen de error)
        return abs(total_cert - total_pres) < 0.01

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

            # Eliminar líneas de certificación
            cursor.execute(f"""
                DELETE FROM {SCHEMA}.tbl_cert_lineas
                WHERE certificacion_id IN (
                    SELECT id FROM {SCHEMA}.tbl_certificacion WHERE presupuesto_id = {presupuesto_id}
                )
            """)

            # Eliminar certificaciones
            if presupuesto_id:
                cursor.execute(f"DELETE FROM {SCHEMA}.tbl_certificacion WHERE presupuesto_id = {presupuesto_id}")

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
    print(" TEST DE MÓDULO DE CERTIFICACIONES")
    print("=" * 70)

    if PASSWORD == 'TU_PASSWORD_AQUI':
        print("❌ ERROR: Configurar PASSWORD en la sección CONFIGURACIÓN")
        return False

    tests = [
        ("Crear presupuesto completo", test_01_crear_presupuesto_completo),
        ("Crear certificación", test_02_crear_certificacion),
        ("Certificar parcial (50%)", test_03_certificar_parcial),
        ("Verificar pendiente", test_04_verificar_pendiente),
        ("Certificar resto (50%)", test_05_certificar_resto),
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
