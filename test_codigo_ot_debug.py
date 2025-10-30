#!/usr/bin/env python3
"""
Script de debug para probar la generación de código OT
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from script.db_partes import _get_tipo_trabajo_prefix
from script.db_connection import get_project_connection

USER = "root"
PASSWORD = "NuevaPass!2025"
SCHEMA = "cert_dev"

print("="*60)
print("TEST 1: Verificar función _get_tipo_trabajo_prefix()")
print("="*60)

# Obtener tipos de trabajo disponibles
try:
    with get_project_connection(USER, PASSWORD, SCHEMA) as cn:
        cur = cn.cursor()
        cur.execute("SELECT id, tipo_codigo FROM dim_tipo_trabajo")
        tipos = cur.fetchall()
        cur.close()

        print(f"\nTipos de trabajo disponibles:")
        for tipo_id, tipo_nombre in tipos:
            print(f"  ID {tipo_id}: {tipo_nombre}")

        print("\n" + "="*60)
        print("TEST 2: Obtener prefijos para cada tipo")
        print("="*60)

        for tipo_id, tipo_nombre in tipos:
            try:
                prefix = _get_tipo_trabajo_prefix(USER, PASSWORD, SCHEMA, tipo_id)
                print(f"  Tipo '{tipo_nombre}' (ID {tipo_id}) -> Prefijo: {prefix}")
            except Exception as e:
                print(f"  ❌ Error con tipo '{tipo_nombre}' (ID {tipo_id}): {e}")

except Exception as e:
    print(f"❌ Error general: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("TEST 3: Simular generación de código completo")
print("="*60)

# Probar con el primer tipo de trabajo
try:
    tipo_id = 1  # Cambiar según necesites
    prefix = _get_tipo_trabajo_prefix(USER, PASSWORD, SCHEMA, tipo_id)

    with get_project_connection(USER, PASSWORD, SCHEMA) as cn:
        cur = cn.cursor()

        # Consulta que usa la interfaz
        print(f"\nEjecutando consulta para prefijo '{prefix}'...")
        cur.execute("""
            SELECT COALESCE(
                MAX(
                    CAST(
                        REPLACE(codigo, %s, '') AS UNSIGNED
                    )
                ),
                0
            ) + 1
            FROM tbl_partes
            WHERE codigo IS NOT NULL
              AND codigo LIKE %s
        """, (prefix + '-', prefix + '-%'))

        next_num = int(cur.fetchone()[0])  # Convertir a int para evitar ValueError con Decimal
        codigo = f"{prefix}-{next_num:05d}"

        print(f"✓ Siguiente número: {next_num}")
        print(f"✓ Código generado: {codigo}")

        cur.close()

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("TEST 4: Verificar códigos existentes en tbl_partes")
print("="*60)

try:
    with get_project_connection(USER, PASSWORD, SCHEMA) as cn:
        cur = cn.cursor()
        cur.execute("SELECT COUNT(*) FROM tbl_partes")
        total = cur.fetchone()[0]
        print(f"\nTotal de partes en tbl_partes: {total}")

        if total > 0:
            cur.execute("""
                SELECT codigo, red_id, tipo_trabajo_id, cod_trabajo_id
                FROM tbl_partes
                ORDER BY id DESC
                LIMIT 5
            """)
            partes = cur.fetchall()
            print("\nÚltimos 5 partes:")
            for parte in partes:
                print(f"  Código: {parte[0]}, Red: {parte[1]}, Tipo: {parte[2]}, Cod: {parte[3]}")
        else:
            print("  (Tabla vacía)")

        cur.close()

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("FIN DE TESTS")
print("="*60)
