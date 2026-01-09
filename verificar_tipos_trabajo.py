#!/usr/bin/env python3
"""
Script temporal para verificar los tipos de trabajo y códigos de partes en la BD
"""
import sys
from pathlib import Path

# Añadir directorio raíz al path
root_dir = Path(__file__).parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from script.db_connection import get_project_connection
from script.db_config import load_db_config
import os

# Cargar configuración desde .env
config = load_db_config()

# Usar credenciales del .env
schema = os.getenv('DB_SCHEMA', 'cert_dev')
user = os.getenv('DB_USER', 'root')
password = os.getenv('DB_PASSWORD', '')

print(f"Conectando como: {user}@localhost al schema: {schema}")
print("="*80)

with get_project_connection(user, password, schema) as conn:
    cursor = conn.cursor()

    print("=" * 80)
    print("TIPOS DE TRABAJO EN LA BASE DE DATOS")
    print("=" * 80)
    cursor.execute("""
        SELECT id, codigo, tipo_codigo, descripcion, activo
        FROM dim_tipo_trabajo
        ORDER BY id
    """)

    print(f"{'ID':<5} {'CODIGO':<10} {'TIPO_COD':<12} {'DESCRIPCION':<40} {'ACTIVO':<8}")
    print("-" * 80)
    tipos_trabajo = cursor.fetchall()
    for row in tipos_trabajo:
        print(f"{row[0]:<5} {row[1] or 'NULL':<10} {row[2] or 'NULL':<12} {row[3]:<40} {row[4]:<8}")

    print("\n" + "=" * 80)
    print("PARTES EXISTENTES EN LA BASE DE DATOS (últimos 20)")
    print("=" * 80)
    cursor.execute("""
        SELECT p.id, p.codigo, p.tipo_trabajo_id, t.descripcion as tipo_desc
        FROM tbl_partes p
        LEFT JOIN dim_tipo_trabajo t ON p.tipo_trabajo_id = t.id
        ORDER BY p.id DESC
        LIMIT 20
    """)

    print(f"{'ID':<8} {'CODIGO':<15} {'TIPO_ID':<10} {'TIPO_DESCRIPCION':<40}")
    print("-" * 80)
    partes = cursor.fetchall()
    for row in partes:
        print(f"{row[0]:<8} {row[1] or 'NULL':<15} {row[2] or 'NULL':<10} {row[3] or 'NULL':<40}")

    print("\n" + "=" * 80)
    print("CONTEO DE PARTES POR TIPO Y PREFIJO")
    print("=" * 80)
    cursor.execute("""
        SELECT
            SUBSTRING_INDEX(codigo, '-', 1) as prefijo,
            tipo_trabajo_id,
            COUNT(*) as total
        FROM tbl_partes
        WHERE codigo IS NOT NULL
        GROUP BY SUBSTRING_INDEX(codigo, '-', 1), tipo_trabajo_id
        ORDER BY prefijo, tipo_trabajo_id
    """)

    print(f"{'PREFIJO':<10} {'TIPO_ID':<10} {'TOTAL':<10}")
    print("-" * 80)
    conteo = cursor.fetchall()
    for row in conteo:
        print(f"{row[0]:<10} {row[1] or 'NULL':<10} {row[2]:<10}")

    cursor.close()

print("\n" + "=" * 80)
print("ANÁLISIS COMPLETO")
print("=" * 80)

# Análisis del mapeo ID -> Prefijo
print("\nANÁLISIS DEL MAPEO ID → PREFIJO:")
print("-" * 80)
for row in tipos_trabajo:
    tipo_id = row[0]
    tipo_codigo = row[2]
    descripcion = row[3]
    print(f"ID {tipo_id} → '{descripcion}' → Prefijo '{tipo_codigo or 'NULL'}'")

print("\nCÓDIGO ESPERADO EN db_partes.py:")
print("-" * 80)
print("id_to_prefix = {")
for row in tipos_trabajo:
    tipo_id = row[0]
    tipo_codigo = row[2] or "??"
    print(f"    {tipo_id}: \"{tipo_codigo}\",  # {row[3]}")
print("}")
