#!/usr/bin/env python3
"""
Script para leer el archivo Excel "Para exportar.xlsx" y mostrar su estructura
"""

import pandas as pd
import sys

def main():
    excel_file = "Para exportar.xlsx"

    try:
        # Leer el archivo Excel
        xls = pd.ExcelFile(excel_file)

        print(f"Hojas en el archivo: {xls.sheet_names}")
        print()

        # Leer la primera hoja (o la que contenga los datos)
        for sheet_name in xls.sheet_names:
            print(f"\n{'='*80}")
            print(f"HOJA: {sheet_name}")
            print('='*80)

            df = pd.read_excel(excel_file, sheet_name=sheet_name)

            print(f"\nDimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
            print(f"\nColumnas: {list(df.columns)}")
            print(f"\nPrimeras 5 filas:")
            print(df.head())
            print(f"\nÚltimas 3 filas:")
            print(df.tail(3))
            print(f"\nTipos de datos:")
            print(df.dtypes)
            print(f"\nValores nulos por columna:")
            print(df.isnull().sum())

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
