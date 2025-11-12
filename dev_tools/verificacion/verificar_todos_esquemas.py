#!/usr/bin/env python3
"""
Script para verificar TODOS los esquemas y encontrar dónde están los partes
"""

import sys
from pathlib import Path

# Añadir directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from script.db_connection import get_connection

DEFAULT_USER = 'root'
DEFAULT_PASSWORD = 'Lauburu1969'


def verificar_todos_esquemas():
    """Verificar todos los esquemas disponibles."""

    print("=" * 80)
    print("VERIFICAR TODOS LOS ESQUEMAS - Búsqueda de tbl_partes")
    print("=" * 80)

    try:
        # Conectarse sin especificar esquema
        with get_connection(DEFAULT_USER, DEFAULT_PASSWORD, None) as conn:
            cursor = conn.cursor()

            # 1. Listar todos los esquemas
            print("\n📊 Esquemas disponibles:")
            cursor.execute("""
                SELECT SCHEMA_NAME
                FROM information_schema.SCHEMATA
                WHERE SCHEMA_NAME NOT IN ('information_schema', 'mysql', 'performance_schema', 'sys')
                ORDER BY SCHEMA_NAME
            """)

            esquemas = [row[0] for row in cursor.fetchall()]
            for i, esquema in enumerate(esquemas, 1):
                print(f"   {i}. {esquema}")

            # 2. Buscar tbl_partes en cada esquema
            print("\n" + "=" * 80)
            print("🔍 BUSCANDO tbl_partes EN CADA ESQUEMA")
            print("=" * 80)

            for esquema in esquemas:
                print(f"\n📁 Esquema: {esquema}")

                # Verificar si existe la tabla
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM information_schema.TABLES
                    WHERE TABLE_SCHEMA = %s
                    AND TABLE_NAME = 'tbl_partes'
                """, (esquema,))

                existe = cursor.fetchone()[0] > 0

                if existe:
                    # Contar registros
                    cursor.execute(f"SELECT COUNT(*) FROM {esquema}.tbl_partes")
                    total = cursor.fetchone()[0]
                    print(f"   ✅ tbl_partes existe - {total} registros")

                    if total > 0:
                        # Mostrar primeros 5 códigos
                        cursor.execute(f"SELECT id, codigo FROM {esquema}.tbl_partes ORDER BY id LIMIT 5")
                        print(f"      Primeros 5 códigos:")
                        for row in cursor.fetchall():
                            print(f"         - ID={row[0]}: '{row[1]}'")
                else:
                    print(f"   ❌ tbl_partes NO existe")

            # 3. Buscar específicamente cert_dev
            print("\n" + "=" * 80)
            print("🎯 VERIFICACIÓN ESPECÍFICA DE cert_dev")
            print("=" * 80)

            # Cambiar a cert_dev explícitamente
            cursor.execute("USE cert_dev")
            cursor.execute("SELECT DATABASE()")
            print(f"   Esquema actual: {cursor.fetchone()[0]}")

            # Mostrar todas las tablas en cert_dev
            cursor.execute("""
                SELECT TABLE_NAME, TABLE_ROWS
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA = 'cert_dev'
                ORDER BY TABLE_NAME
            """)

            print(f"\n   Tablas en cert_dev:")
            tablas = cursor.fetchall()
            if tablas:
                for tabla, rows in tablas:
                    print(f"      - {tabla}: ~{rows} registros")
            else:
                print(f"      ⚠️  No hay tablas en cert_dev")

            cursor.close()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n")


if __name__ == "__main__":
    verificar_todos_esquemas()
