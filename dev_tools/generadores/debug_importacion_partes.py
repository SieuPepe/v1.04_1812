#!/usr/bin/env python3
"""
Script de depuración para entender por qué no se encuentran los partes
"""

import sys
from pathlib import Path
import pandas as pd

# Añadir directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from script.db_connection import get_project_connection

EXCEL_FILE = 'MEDICIONES OTS.xlsx'
DEFAULT_USER = 'root'
DEFAULT_PASSWORD = 'Lauburu1969'
DEFAULT_SCHEMA = 'cert_dev'


def debug_busqueda_partes():
    """Debug detallado de búsqueda de partes."""

    print("=" * 80)
    print("DEBUG: BÚSQUEDA DE PARTES - Análisis Detallado")
    print("=" * 80)

    # 1. Leer primeros códigos del Excel
    excel_path = root_dir / EXCEL_FILE
    print(f"\n📖 Leyendo {EXCEL_FILE}...")
    df = pd.read_excel(excel_path)
    df = df[df['parte_id'].notna()]

    # Tomar solo los primeros 10 códigos únicos para debug
    codigos_muestra = df['parte_id'].astype(str).unique()[:10]
    print(f"   Códigos de muestra del Excel (primeros 10):")
    for i, codigo in enumerate(codigos_muestra, 1):
        print(f"      {i}. '{codigo}' (len={len(codigo)}, repr={repr(codigo)})")

    # 2. Conectar a la BD y buscar
    print(f"\n🔍 Conectando a esquema '{DEFAULT_SCHEMA}'...")
    try:
        with get_project_connection(DEFAULT_USER, DEFAULT_PASSWORD, DEFAULT_SCHEMA) as conn:
            cursor = conn.cursor()

            # Verificar esquema actual
            cursor.execute("SELECT DATABASE()")
            esquema_actual = cursor.fetchone()[0]
            print(f"   ✅ Esquema activo: {esquema_actual}")

            # Verificar total de partes
            cursor.execute("SELECT COUNT(*) FROM tbl_partes")
            total = cursor.fetchone()[0]
            print(f"   📊 Total de registros en tbl_partes: {total}")

            # Mostrar primeros 10 códigos de la BD
            cursor.execute("SELECT id, codigo FROM tbl_partes ORDER BY id LIMIT 10")
            print(f"\n   Primeros 10 códigos en tbl_partes:")
            codigos_bd = []
            for row in cursor.fetchall():
                id_parte, codigo = row
                codigos_bd.append(codigo)
                print(f"      ID={id_parte}, codigo='{codigo}' (len={len(codigo) if codigo else 0}, repr={repr(codigo)})")

            # 3. Buscar cada código del Excel en la BD
            print("\n" + "=" * 80)
            print("🔬 PRUEBA DE BÚSQUEDA EXACTA")
            print("=" * 80)

            for codigo_excel in codigos_muestra:
                # Limpiar el código (como hace el script)
                codigo_limpio = str(codigo_excel).strip()

                # Búsqueda exacta (como en el script original)
                cursor.execute("""
                    SELECT id, codigo
                    FROM tbl_partes
                    WHERE codigo = %s
                """, (codigo_limpio,))

                result = cursor.fetchone()

                if result:
                    print(f"   ✅ '{codigo_limpio}' → ENCONTRADO (ID={result[0]})")
                else:
                    print(f"   ❌ '{codigo_limpio}' → NO ENCONTRADO")

                    # Intentar búsqueda case-insensitive
                    cursor.execute("""
                        SELECT id, codigo
                        FROM tbl_partes
                        WHERE UPPER(codigo) = UPPER(%s)
                    """, (codigo_limpio,))
                    result_upper = cursor.fetchone()

                    if result_upper:
                        print(f"      ⚠️  PERO existe con diferente case: '{result_upper[1]}' (ID={result_upper[0]})")
                    else:
                        # Buscar similares con LIKE
                        cursor.execute("""
                            SELECT id, codigo
                            FROM tbl_partes
                            WHERE codigo LIKE %s
                            LIMIT 5
                        """, (f"%{codigo_limpio}%",))
                        similares = cursor.fetchall()

                        if similares:
                            print(f"      🔍 Códigos similares encontrados:")
                            for sim_id, sim_codigo in similares:
                                print(f"         - '{sim_codigo}' (ID={sim_id})")
                        else:
                            print(f"      ❌ No hay códigos similares")

            # 4. Verificar collation de la columna
            print("\n" + "=" * 80)
            print("⚙️  CONFIGURACIÓN DE LA COLUMNA 'codigo'")
            print("=" * 80)
            cursor.execute("""
                SELECT COLUMN_TYPE, COLLATION_NAME, IS_NULLABLE
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = %s
                AND TABLE_NAME = 'tbl_partes'
                AND COLUMN_NAME = 'codigo'
            """, (esquema_actual,))

            col_info = cursor.fetchone()
            if col_info:
                print(f"   Tipo: {col_info[0]}")
                print(f"   Collation: {col_info[1]}")
                print(f"   Nullable: {col_info[2]}")

            cursor.close()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n")


if __name__ == "__main__":
    debug_busqueda_partes()
