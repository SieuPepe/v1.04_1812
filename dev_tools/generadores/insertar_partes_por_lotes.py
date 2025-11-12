#!/usr/bin/env python3
"""
Script para insertar registros en tbl_partes por lotes pequeños
para identificar problemas de integridad referencial
"""

import pandas as pd
import sys
import mysql.connector
from datetime import datetime

def format_value(val, dtype):
    """Formatea un valor según su tipo para SQL"""
    if pd.isna(val) or val == '' or (isinstance(val, str) and val.strip() == ''):
        return 'NULL'

    if dtype == 'bool':
        return '1' if val else '0'

    if dtype in ['int64', 'float64']:
        if pd.isna(val):
            return 'NULL'
        return str(val)

    if isinstance(val, str):
        val = val.replace("'", "''").replace("\\", "\\\\")
        return f"'{val}'"

    return f"'{val}'"

def main():
    excel_file = "Para exportar.xlsx"

    # Conectar a la base de datos
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  # Ajustar según tu configuración
            password='',  # Ajustar según tu configuración
            database='cert_dev'  # Ajustar según tu configuración
        )
        cursor = conn.cursor()
        print("✓ Conectado a la base de datos")
    except Exception as e:
        print(f"✗ Error al conectar a la base de datos: {e}")
        print("\nNOTA: Ajusta las credenciales en el script antes de ejecutar")
        sys.exit(1)

    try:
        print(f"\nLeyendo archivo: {excel_file}")
        df = pd.read_excel(excel_file, sheet_name='LISTADO OTS')

        # Renombrar columna con error de ortografía
        df = df.rename(columns={'descripion': 'descripcion'})

        print(f"Total de registros a insertar: {len(df)}")

        # Primero, verificar qué municipios existen
        print("\nVerificando municipios en la base de datos...")
        municipios_excel = sorted(df['id_municipio'].unique())
        print(f"Municipios referenciados en el Excel: {municipios_excel}")

        placeholders = ','.join(['%s'] * len(municipios_excel))
        cursor.execute(f"SELECT id FROM dim_municipios WHERE id IN ({placeholders})", municipios_excel)
        municipios_existentes = [row[0] for row in cursor.fetchall()]
        print(f"Municipios que existen en la BD: {municipios_existentes}")

        municipios_faltantes = set(municipios_excel) - set(municipios_existentes)
        if municipios_faltantes:
            print(f"\n✗ ERROR: Faltan estos municipios en dim_municipios: {sorted(municipios_faltantes)}")
            print("\nSolución: Primero debes insertar estos municipios en dim_municipios")
            cursor.close()
            conn.close()
            sys.exit(1)

        print("✓ Todos los municipios existen")

        # Preparar columnas
        columns = list(df.columns)
        columns_str = ', '.join(columns)

        # Insertar por lotes de 50
        lote_size = 50
        total_insertados = 0
        total_lotes = (len(df) + lote_size - 1) // lote_size

        for lote_num in range(total_lotes):
            inicio = lote_num * lote_size
            fin = min((lote_num + 1) * lote_size, len(df))
            df_lote = df.iloc[inicio:fin]

            print(f"\nProcesando lote {lote_num + 1}/{total_lotes} (registros {inicio + 1}-{fin})...")

            # Generar VALUES para este lote
            values_list = []
            for idx, row in df_lote.iterrows():
                values = []
                for col in columns:
                    val = row[col]
                    dtype = str(df[col].dtype)
                    values.append(format_value(val, dtype))
                values_list.append(f"({', '.join(values)})")

            values_str = ',\n    '.join(values_list)

            # Generar UPDATE parte
            update_parts = [f"{col} = VALUES({col})" for col in columns if col != 'id']
            update_str = ',\n    '.join(update_parts)

            # Construir query completa
            query = f"""
INSERT INTO tbl_partes (
    {columns_str}
) VALUES
    {values_str}
ON DUPLICATE KEY UPDATE
    {update_str}
"""

            try:
                cursor.execute(query)
                conn.commit()
                total_insertados += len(df_lote)
                print(f"  ✓ Lote {lote_num + 1} insertado correctamente ({len(df_lote)} registros)")
            except Exception as e:
                print(f"  ✗ Error en lote {lote_num + 1}: {e}")
                conn.rollback()
                print("\nGuardando query fallida en error_query.sql...")
                with open('error_query.sql', 'w', encoding='utf-8') as f:
                    f.write(query)
                cursor.close()
                conn.close()
                sys.exit(1)

        print(f"\n{'='*80}")
        print(f"✓ Inserción completada exitosamente")
        print(f"Total de registros insertados/actualizados: {total_insertados}")
        print('='*80)

        # Verificación final
        cursor.execute("SELECT COUNT(*) FROM tbl_partes")
        total = cursor.fetchone()[0]
        print(f"\nTotal de registros en tbl_partes: {total}")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
