#!/usr/bin/env python3
"""
Script para verificar la discrepancia entre códigos de partes en Excel y BD
"""

import os
import sys
from pathlib import Path
import pandas as pd

# Añadir directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from script.db_connection import get_project_connection

# Cargar .env
try:
    from dotenv import load_dotenv
    project_root = Path(__file__).parent.parent.parent
    load_dotenv(dotenv_path=project_root / '.env')
except ImportError:
    pass

EXCEL_FILE = 'MEDICIONES OTS.xlsx'
DEFAULT_SCHEMA = 'cert_dev'


def main():
    """Verificar códigos de partes."""

    # Obtener credenciales desde variables de entorno
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    schema = os.getenv('DB_SCHEMA', DEFAULT_SCHEMA)

    if not user or not password:
        print("ERROR: Se requieren credenciales en variables de entorno")
        print("Configure DB_USER y DB_PASSWORD en el archivo .env")
        sys.exit(1)

    print("=" * 80)
    print("VERIFICAR CÓDIGOS DE PARTES - Excel vs Base de Datos")
    print("=" * 80)

    # 1. Leer códigos del Excel
    excel_path = root_dir / EXCEL_FILE
    print(f"\n📖 Leyendo {EXCEL_FILE}...")
    df = pd.read_excel(excel_path)
    df = df[df['parte_id'].notna()]
    codigos_excel = set(df['parte_id'].astype(str).str.strip().unique())
    print(f"   Códigos únicos en Excel: {len(codigos_excel)}")
    print(f"   Primeros 10 códigos: {sorted(list(codigos_excel))[:10]}")

    # 2. Leer códigos de la BD
    print(f"\n🔍 Consultando tabla tbl_partes en esquema '{schema}'...")
    try:
        with get_project_connection(user, password, schema) as conn:
            cursor = conn.cursor()

            # Contar total de partes
            cursor.execute("SELECT COUNT(*) FROM tbl_partes")
            total_partes = cursor.fetchone()[0]
            print(f"   Total de partes en BD: {total_partes}")

            # Obtener todos los códigos
            cursor.execute("SELECT codigo FROM tbl_partes WHERE codigo IS NOT NULL")
            codigos_bd = set(row[0] for row in cursor.fetchall())
            print(f"   Códigos únicos en BD: {len(codigos_bd)}")
            print(f"   Primeros 10 códigos: {sorted(list(codigos_bd))[:10]}")

            cursor.close()

    except Exception as e:
        print(f"❌ Error al consultar BD: {e}")
        return

    # 3. Comparar
    print("\n" + "=" * 80)
    print("📊 ANÁLISIS DE DISCREPANCIAS")
    print("=" * 80)

    # Códigos en Excel pero no en BD
    solo_en_excel = codigos_excel - codigos_bd
    print(f"\n❌ Códigos en Excel que NO están en BD: {len(solo_en_excel)}")
    if solo_en_excel:
        print(f"   Primeros 20:")
        for codigo in sorted(list(solo_en_excel))[:20]:
            print(f"      - {codigo}")
        if len(solo_en_excel) > 20:
            print(f"      ... y {len(solo_en_excel) - 20} más")

    # Códigos en BD pero no en Excel
    solo_en_bd = codigos_bd - codigos_excel
    print(f"\n✅ Códigos en BD que NO están en Excel: {len(solo_en_bd)}")
    if solo_en_bd:
        print(f"   Primeros 20:")
        for codigo in sorted(list(solo_en_bd))[:20]:
            print(f"      - {codigo}")
        if len(solo_en_bd) > 20:
            print(f"      ... y {len(solo_en_bd) - 20} más")

    # Códigos en común
    en_comun = codigos_excel & codigos_bd
    print(f"\n✅ Códigos que coinciden: {len(en_comun)}")
    if en_comun:
        print(f"   Primeros 10:")
        for codigo in sorted(list(en_comun))[:10]:
            print(f"      - {codigo}")

    # 4. Análisis de patrones
    print("\n" + "=" * 80)
    print("🔍 ANÁLISIS DE PATRONES")
    print("=" * 80)

    # Patrones en Excel
    print("\nPatrones en Excel:")
    patrones_excel = {}
    for codigo in codigos_excel:
        prefijo = codigo.split('/')[0] if '/' in codigo else 'SIN_PREFIJO'
        patrones_excel[prefijo] = patrones_excel.get(prefijo, 0) + 1
    for prefijo, count in sorted(patrones_excel.items()):
        print(f"   {prefijo}: {count} códigos")

    # Patrones en BD
    print("\nPatrones en BD:")
    patrones_bd = {}
    for codigo in codigos_bd:
        prefijo = codigo.split('/')[0] if '/' in codigo else 'SIN_PREFIJO'
        patrones_bd[prefijo] = patrones_bd.get(prefijo, 0) + 1
    for prefijo, count in sorted(patrones_bd.items()):
        print(f"   {prefijo}: {count} códigos")

    print("\n")


if __name__ == "__main__":
    main()
