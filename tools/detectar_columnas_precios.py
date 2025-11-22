#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para detectar la estructura exacta de tbl_pres_precios
"""

import os
import sys
from script.db_connection import get_project_connection

# Configuración - requiere variables de entorno
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
SCHEMA = os.getenv('DB_SCHEMA', 'cert_dev')

# Validar que se proporcionaron credenciales
if not USER or not PASSWORD:
    print("=" * 80)
    print("ERROR: Se requieren credenciales de base de datos")
    print("=" * 80)
    print("\nConfigure las variables de entorno DB_USER y DB_PASSWORD")
    print("O en el archivo .env del proyecto")
    print("=" * 80)
    sys.exit(1)

def detectar_columnas_precios():
    """Detecta las columnas exactas de tbl_pres_precios"""
    print("=" * 80)
    print(" ESTRUCTURA DE TABLA: tbl_pres_precios")
    print("=" * 80)

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Mostrar estructura de la tabla
            print("\n1. COLUMNAS DE LA TABLA:")
            print("-" * 80)
            cursor.execute(f"DESCRIBE {SCHEMA}.tbl_pres_precios")
            columnas = cursor.fetchall()

            for col in columnas:
                field, tipo, null, key, default, extra = col
                print(f"  • {field:30s} {tipo:20s} NULL:{null:3s} KEY:{key:4s}")

            # Mostrar datos de ejemplo
            print("\n2. DATOS DE EJEMPLO (primeros 3 registros):")
            print("-" * 80)
            cursor.execute(f"SELECT * FROM {SCHEMA}.tbl_pres_precios LIMIT 3")
            rows = cursor.fetchall()

            # Obtener nombres de columnas
            column_names = [desc[0] for desc in cursor.description]
            print(f"  Columnas: {', '.join(column_names)}")
            print()

            for i, row in enumerate(rows, 1):
                print(f"  Registro {i}:")
                for col_name, value in zip(column_names, row):
                    print(f"    {col_name:30s} = {value}")
                print()

            # Buscar columnas relacionadas con precio
            print("\n3. COLUMNAS RELACIONADAS CON PRECIO:")
            print("-" * 80)
            precio_cols = [col[0] for col in columnas if 'precio' in col[0].lower() or 'price' in col[0].lower()]
            if precio_cols:
                for col in precio_cols:
                    print(f"  ✓ {col}")
            else:
                print("  ⚠️  No se encontraron columnas con 'precio' en el nombre")

            # Buscar columnas relacionadas con unidad
            print("\n4. COLUMNAS RELACIONADAS CON UNIDAD:")
            print("-" * 80)
            unidad_cols = [col[0] for col in columnas if 'unidad' in col[0].lower() or 'unit' in col[0].lower()]
            if unidad_cols:
                for col in unidad_cols:
                    print(f"  ✓ {col}")
            else:
                print("  ⚠️  No se encontraron columnas con 'unidad' en el nombre")

            print("\n" + "=" * 80)
            print("✅ Detección completada")
            print("=" * 80)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    detectar_columnas_precios()
