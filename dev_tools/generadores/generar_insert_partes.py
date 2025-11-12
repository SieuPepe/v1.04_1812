#!/usr/bin/env python3
"""
Script para generar INSERT INTO tbl_partes desde el archivo Excel
"""

import pandas as pd
import sys
from datetime import datetime

def format_value(val, dtype):
    """Formatea un valor según su tipo para SQL"""
    # Manejar valores nulos
    if pd.isna(val) or val == '' or (isinstance(val, str) and val.strip() == ''):
        return 'NULL'

    # Manejar booleanos
    if dtype == 'bool':
        return '1' if val else '0'

    # Manejar números
    if dtype in ['int64', 'float64']:
        if pd.isna(val):
            return 'NULL'
        return str(val)

    # Manejar strings y objetos
    if isinstance(val, str):
        # Escapar comillas simples
        val = val.replace("'", "''").replace("\\", "\\\\")
        return f"'{val}'"

    return f"'{val}'"

def main():
    excel_file = "Para exportar.xlsx"
    output_file = "script/sql/insertar_partes_desde_excel.sql"

    try:
        print(f"Leyendo archivo: {excel_file}")
        df = pd.read_excel(excel_file, sheet_name='LISTADO OTS')

        print(f"Registros encontrados: {len(df)}")
        print(f"Columnas: {list(df.columns)}")

        # Renombrar columnas con errores de ortografía
        df = df.rename(columns={'descripion': 'descripcion'})
        print(f"Columnas después de renombrar: {list(df.columns)}")

        # Abrir archivo de salida
        with open(output_file, 'w', encoding='utf-8') as f:
            # Escribir encabezado
            f.write("-- =====================================================================\n")
            f.write("-- Script de importación de datos desde Excel a tbl_partes\n")
            f.write(f"-- Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"-- Total de registros: {len(df)}\n")
            f.write("-- NOTA: Este script NO hace TRUNCATE. Usa ON DUPLICATE KEY UPDATE.\n")
            f.write("-- =====================================================================\n\n")

            # Preparar columnas
            columns = list(df.columns)
            columns_str = ', '.join(columns)

            # Escribir INSERT
            f.write("-- Insertar/actualizar los datos\n")
            f.write(f"INSERT INTO tbl_partes (\n    {columns_str}\n) VALUES\n")

            # Generar VALUES
            for idx, row in df.iterrows():
                values = []
                for col in columns:
                    val = row[col]
                    dtype = str(df[col].dtype)
                    values.append(format_value(val, dtype))

                values_str = ', '.join(values)

                # Determinar si es la última fila
                if idx < len(df) - 1:
                    f.write(f"    ({values_str}),\n")
                else:
                    f.write(f"    ({values_str})\n")

                # Imprimir progreso cada 100 registros
                if (idx + 1) % 100 == 0:
                    print(f"  Procesados: {idx + 1}/{len(df)} registros")

            # Escribir ON DUPLICATE KEY UPDATE
            f.write("ON DUPLICATE KEY UPDATE\n")
            update_parts = []
            for col in columns:
                if col != 'id':  # No actualizar el ID
                    update_parts.append(f"    {col} = VALUES({col})")
            f.write(',\n'.join(update_parts))
            f.write(";\n\n")

            # Escribir verificación
            f.write("-- =====================================================================\n")
            f.write("-- Verificación\n")
            f.write("-- =====================================================================\n")
            f.write("SELECT COUNT(*) AS total_registros FROM tbl_partes;\n")
            f.write("SELECT 'Primeros 5 registros insertados:' AS mensaje;\n")
            f.write("SELECT * FROM tbl_partes ORDER BY id LIMIT 5;\n")
            f.write("SELECT 'Últimos 5 registros insertados:' AS mensaje;\n")
            f.write("SELECT * FROM tbl_partes ORDER BY id DESC LIMIT 5;\n")

        print(f"\nScript SQL generado exitosamente: {output_file}")
        print(f"Total de registros: {len(df)}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
