#!/usr/bin/env python3
"""
Script rápido para ver estructura de tbl_part_certificacion
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from script.db_connection import get_project_connection

USER = 'root'
PASSWORD = 'NuevaPass!2025'
SCHEMA = 'cert_dev'

try:
    with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
        cursor = conn.cursor()

        print("\n" + "="*80)
        print("ESTRUCTURA DE tbl_part_certificacion")
        print("="*80)

        cursor.execute(f"DESCRIBE {SCHEMA}.tbl_part_certificacion")
        columns = cursor.fetchall()

        print(f"\n{'Columna':<30} {'Tipo':<20} {'Null':<10} {'Key':<10}")
        print("-" * 80)
        for col in columns:
            print(f"{col[0]:<30} {col[1]:<20} {col[2]:<10} {col[3]:<10}")

        cursor.close()

except Exception as e:
    print(f"Error: {e}")
