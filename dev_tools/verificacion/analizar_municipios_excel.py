#!/usr/bin/env python3
"""
Script para analizar qué municipios se necesitan en tbl_municipios
"""

import pandas as pd
import sys

def main():
    excel_file = "Para exportar.xlsx"

    try:
        print(f"Leyendo archivo: {excel_file}")
        df = pd.read_excel(excel_file, sheet_name='LISTADO OTS')

        print(f"\n{'='*80}")
        print("ANÁLISIS DE COLUMNAS MUNICIPIO")
        print('='*80)

        # Verificar qué columnas de municipio existen
        cols_municipio = [col for col in df.columns if 'municipio' in col.lower()]
        print(f"\nColumnas relacionadas con municipio: {cols_municipio}")

        # Analizar cada columna
        for col in cols_municipio:
            print(f"\n--- Análisis de columna '{col}' ---")
            valores_unicos = sorted(df[col].dropna().unique())
            print(f"Valores únicos: {valores_unicos}")
            print(f"Total valores únicos: {len(valores_unicos)}")
            print(f"Valores nulos: {df[col].isna().sum()}")
            print(f"Tipo de datos: {df[col].dtype}")

        # Si existe id_municipio, mostrar distribución
        if 'id_municipio' in df.columns:
            print(f"\n{'='*80}")
            print("DISTRIBUCIÓN DE id_municipio")
            print('='*80)
            print(df['id_municipio'].value_counts().sort_index())

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
