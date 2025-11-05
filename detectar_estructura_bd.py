#!/usr/bin/env python3
"""
Script para detectar la estructura real de la base de datos
y adaptar los tests automáticamente.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

USER = os.getenv('DB_USER', 'root')
PASSWORD = input("Contraseña MySQL: ") if len(sys.argv) < 2 else sys.argv[1]
SCHEMA = input("Esquema (ej: cert_dev): ") if len(sys.argv) < 3 else sys.argv[2]

try:
    from script.db_connection import get_project_connection
except ImportError as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

def detect_schema_structure():
    """Detecta la estructura real del esquema"""
    print("\n" + "="*80)
    print("DETECTANDO ESTRUCTURA DE BASE DE DATOS")
    print("="*80)
    print(f"Esquema: {SCHEMA}\n")

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # 1. Listar todas las tablas
            print("\n1️⃣  TABLAS EXISTENTES:")
            print("-" * 80)
            cursor.execute(f"SHOW TABLES FROM {SCHEMA}")
            tables = [row[0] for row in cursor.fetchall()]

            tables_by_type = {
                'partes': [],
                'presupuesto': [],
                'certificacion': [],
                'dimension': [],
                'otras': []
            }

            for table in sorted(tables):
                if 'parte' in table.lower():
                    tables_by_type['partes'].append(table)
                elif 'presup' in table.lower() or 'budget' in table.lower() or 'pres_' in table.lower():
                    tables_by_type['presupuesto'].append(table)
                elif 'cert' in table.lower():
                    tables_by_type['certificacion'].append(table)
                elif 'dim_' in table.lower():
                    tables_by_type['dimension'].append(table)
                else:
                    tables_by_type['otras'].append(table)

            print("\n📋 Tablas de PARTES:")
            for t in tables_by_type['partes']:
                print(f"  - {t}")

            print("\n💰 Tablas de PRESUPUESTO:")
            for t in tables_by_type['presupuesto']:
                print(f"  - {t}")

            print("\n✅ Tablas de CERTIFICACIÓN:")
            for t in tables_by_type['certificacion']:
                print(f"  - {t}")

            print(f"\n📊 Tablas de DIMENSIONES: {len(tables_by_type['dimension'])} tablas")

            # 2. Detectar estructura de tabla principal de presupuestos
            print("\n\n2️⃣  ESTRUCTURA DE TABLAS DE PRESUPUESTO:")
            print("-" * 80)

            presup_tables = tables_by_type['presupuesto']
            if presup_tables:
                main_presup = presup_tables[0]  # Tomar la primera
                print(f"\n📄 Tabla: {main_presup}")
                cursor.execute(f"DESCRIBE {SCHEMA}.{main_presup}")
                columns = cursor.fetchall()

                print(f"\n{'Columna':<30} {'Tipo':<20} {'Null':<10} {'Key':<10}")
                print("-" * 80)
                for col in columns:
                    print(f"{col[0]:<30} {col[1]:<20} {col[2]:<10} {col[3]:<10}")

                # Detectar nombre de columna de relación con partes
                parte_col = None
                for col in columns:
                    col_name = col[0].lower()
                    if 'parte' in col_name and 'id' in col_name:
                        parte_col = col[0]
                        break

                if parte_col:
                    print(f"\n✅ Columna de relación con partes: {parte_col}")
                else:
                    print(f"\n⚠️  No se encontró columna de relación con partes")
            else:
                print("⚠️  No hay tablas de presupuesto")

            # 3. Detectar estructura de tablas de certificación
            print("\n\n3️⃣  ESTRUCTURA DE TABLAS DE CERTIFICACIÓN:")
            print("-" * 80)

            cert_tables = tables_by_type['certificacion']
            if cert_tables:
                main_cert = cert_tables[0]  # Tomar la primera
                print(f"\n📄 Tabla: {main_cert}")
                cursor.execute(f"DESCRIBE {SCHEMA}.{main_cert}")
                columns = cursor.fetchall()

                print(f"\n{'Columna':<30} {'Tipo':<20} {'Null':<10} {'Key':<10}")
                print("-" * 80)
                for col in columns:
                    print(f"{col[0]:<30} {col[1]:<20} {col[2]:<10} {col[3]:<10}")
            else:
                print("⚠️  No hay tablas de certificación")

            # 4. Generar recomendaciones
            print("\n\n4️⃣  RECOMENDACIONES:")
            print("-" * 80)

            if not presup_tables:
                print("❌ PROBLEMA: No hay tablas de presupuesto")
                print("   Los tests de presupuesto NO pueden funcionar")

            if not cert_tables:
                print("❌ PROBLEMA: No hay tablas de certificación")
                print("   Los tests de certificación NO pueden funcionar")

            if presup_tables and not parte_col:
                print("⚠️  ADVERTENCIA: No se detectó columna de relación parte-presupuesto")
                print("   Puede causar problemas en los tests")

            print("\n\n5️⃣  ESTRUCTURA DETECTADA (para corregir tests):")
            print("-" * 80)
            print(f"""
ESQUEMA: {SCHEMA}
TABLAS_PRESUPUESTO: {presup_tables}
TABLAS_CERTIFICACION: {cert_tables}
COLUMNA_PARTE_ID: {parte_col if 'parte_col' in locals() else 'NO DETECTADA'}
""")

            cursor.close()
            return True

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print(f"\nUsuario: {USER}")
    print(f"Esquema: {SCHEMA}")

    if PASSWORD == 'TU_PASSWORD_AQUI':
        print("\n❌ ERROR: Debes proporcionar la contraseña")
        print(f"Uso: python {sys.argv[0]} <password> <schema>")
        sys.exit(1)

    success = detect_schema_structure()
    sys.exit(0 if success else 1)
