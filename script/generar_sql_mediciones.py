#!/usr/bin/env python3
"""
Script para generar SQL de inserción de mediciones desde Excel
Genera un archivo SQL listo para ejecutar en MySQL Workbench
"""

import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# Configuración
root_dir = Path(__file__).parent.parent
EXCEL_FILE = root_dir / 'MEDICIONES OTS.xlsx'
OUTPUT_SQL = root_dir / 'script' / 'sql' / 'insertar_mediciones_ots.sql'

def generar_sql_mediciones():
    """Genera archivo SQL desde el Excel."""

    print("=" * 80)
    print("GENERAR SQL DE MEDICIONES DESDE EXCEL")
    print("=" * 80)

    # 1. Leer Excel
    print(f"\n📖 Leyendo {EXCEL_FILE.name}...")
    df = pd.read_excel(EXCEL_FILE)

    # Limpiar datos
    df = df[df['precio_id'].notna()]
    df['precio_id'] = df['precio_id'].astype(int)
    df['cantidad'] = df['cantidad'].astype(float)
    df['fecha_unidad'] = pd.to_datetime(df['fecha_unidad'], errors='coerce')
    df['parte_id'] = df['parte_id'].astype(str).str.strip()

    print(f"   Total de registros: {len(df)}")
    print(f"   Registros con fecha: {df['fecha_unidad'].notna().sum()}")
    print(f"   Registros sin fecha: {df['fecha_unidad'].isna().sum()}")

    # 2. Obtener códigos únicos de partes
    codigos_unicos = sorted(df['parte_id'].unique())
    print(f"\n   Códigos únicos de partes: {len(codigos_unicos)}")
    print(f"   Primeros 10: {codigos_unicos[:10]}")

    # 3. Generar SQL
    print(f"\n💾 Generando archivo SQL...")

    with open(OUTPUT_SQL, 'w', encoding='utf-8') as f:
        # Encabezado
        f.write("-- " + "=" * 77 + "\n")
        f.write("-- Script de importación de mediciones desde Excel a tbl_part_presupuesto\n")
        f.write(f"-- Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"-- Total de registros: {len(df)}\n")
        f.write("-- " + "=" * 77 + "\n\n")

        f.write("USE cert_dev;\n\n")

        # IMPORTANTE: Explicar el proceso
        f.write("-- IMPORTANTE:\n")
        f.write("-- Este script usa subconsultas para obtener el parte_id interno desde tbl_partes\n")
        f.write("-- basándose en el código del parte (OT/xxxx, TP/xxxx, GF/xxxx, etc.)\n")
        f.write("-- Si algún código no existe en tbl_partes, ese INSERT fallará\n\n")

        # Opcional: limpiar tabla (comentado por seguridad)
        f.write("-- Descomentar la siguiente línea si quieres LIMPIAR la tabla antes de insertar:\n")
        f.write("-- TRUNCATE TABLE tbl_part_presupuesto;\n\n")

        # Contar registros actuales
        f.write("-- Mostrar registros actuales antes de insertar\n")
        f.write("SELECT COUNT(*) AS 'Registros actuales en tbl_part_presupuesto' FROM tbl_part_presupuesto;\n\n")

        # Generar INSERTs
        f.write("-- Insertar mediciones\n")
        f.write("-- Formato: (parte_id, precio_id, cantidad, fecha, precio_unit)\n")
        f.write("-- El parte_id se obtiene desde tbl_partes.codigo\n")
        f.write("-- El precio_unit se obtiene desde tbl_pres_precios.coste\n\n")

        # Agrupar por lotes de 100 para mejor rendimiento
        batch_size = 100
        total_batches = (len(df) + batch_size - 1) // batch_size

        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min((batch_num + 1) * batch_size, len(df))
            batch_df = df.iloc[start_idx:end_idx]

            f.write(f"-- Lote {batch_num + 1}/{total_batches} (registros {start_idx + 1}-{end_idx})\n")
            f.write("INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)\n")
            f.write("SELECT * FROM (\n")

            for idx, row in batch_df.iterrows():
                codigo_parte = row['parte_id']
                precio_id = int(row['precio_id'])
                cantidad = float(row['cantidad'])
                fecha = row['fecha_unidad']

                # Formatear fecha
                if pd.notna(fecha):
                    fecha_str = f"'{fecha.strftime('%Y-%m-%d')}'"
                else:
                    fecha_str = "NULL"

                # Generar SELECT con subconsultas
                f.write("    SELECT\n")
                f.write(f"        (SELECT id FROM tbl_partes WHERE codigo = '{codigo_parte}') AS parte_id,\n")
                f.write(f"        {precio_id} AS precio_id,\n")
                f.write(f"        {cantidad} AS cantidad,\n")
                f.write(f"        {fecha_str} AS fecha,\n")
                f.write(f"        (SELECT coste FROM tbl_pres_precios WHERE id = {precio_id}) AS precio_unit")

                # Añadir UNION ALL excepto en el último registro del lote
                if idx < batch_df.index[-1]:
                    f.write("\n    UNION ALL\n")
                else:
                    f.write("\n")

            f.write(") AS temp\n")
            f.write("WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;\n\n")

        # Verificación final
        f.write("-- Verificación: contar registros después de insertar\n")
        f.write("SELECT COUNT(*) AS 'Registros totales después de insertar' FROM tbl_part_presupuesto;\n\n")

        f.write("-- Verificación: mostrar primeros 10 registros insertados\n")
        f.write("SELECT\n")
        f.write("    pp.id,\n")
        f.write("    p.codigo AS parte_codigo,\n")
        f.write("    pr.codigo AS precio_codigo,\n")
        f.write("    pp.cantidad,\n")
        f.write("    pp.fecha,\n")
        f.write("    pp.precio_unit\n")
        f.write("FROM tbl_part_presupuesto pp\n")
        f.write("LEFT JOIN tbl_partes p ON pp.parte_id = p.id\n")
        f.write("LEFT JOIN tbl_pres_precios pr ON pp.precio_id = pr.id\n")
        f.write("ORDER BY pp.id DESC\n")
        f.write("LIMIT 10;\n\n")

        f.write("-- FIN DEL SCRIPT\n")

    print(f"   ✅ Archivo generado: {OUTPUT_SQL}")
    print(f"\n" + "=" * 80)
    print("📋 INSTRUCCIONES:")
    print("=" * 80)
    print(f"1. Abre MySQL Workbench")
    print(f"2. Conéctate a tu servidor MySQL")
    print(f"3. Abre el archivo: {OUTPUT_SQL}")
    print(f"4. Ejecuta el script completo (Ctrl+Shift+Enter)")
    print(f"\n⚠️  NOTA: Si algún código de parte no existe en tbl_partes,")
    print(f"   ese registro no se insertará (se omitirá silenciosamente)")
    print(f"\n")

if __name__ == "__main__":
    generar_sql_mediciones()
