#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar un script SQL a partir del archivo Excel 'Para exportar.xlsx'
para importar datos en la tabla tbl_partes
"""

import pandas as pd
import sys
from datetime import datetime

def leer_excel():
    """Lee el archivo Excel y retorna un DataFrame"""
    try:
        df = pd.read_excel('Para exportar.xlsx')
        print(f"✓ Archivo Excel leído correctamente: {len(df)} registros encontrados")
        print(f"✓ Columnas: {', '.join(df.columns.tolist())}")
        return df
    except Exception as e:
        print(f"❌ Error al leer el archivo Excel: {e}")
        sys.exit(1)

def generar_valor_sql(valor):
    """Convierte un valor de Python a formato SQL"""
    if pd.isna(valor) or valor is None or valor == '':
        return 'NULL'
    elif isinstance(valor, bool):
        # Convertir booleanos a 1/0 para MySQL
        return '1' if valor else '0'
    elif isinstance(valor, str):
        # Escapar comillas simples
        valor_escapado = valor.replace("'", "''")
        return f"'{valor_escapado}'"
    elif isinstance(valor, (int, float)):
        return str(valor)
    elif isinstance(valor, datetime):
        return f"'{valor.strftime('%Y-%m-%d')}'"
    elif hasattr(valor, 'strftime'):  # Para fechas de pandas
        return f"'{valor.strftime('%Y-%m-%d')}'"
    else:
        return f"'{str(valor)}'"

def generar_script_sql(df, schema='cert_dev'):
    """Genera el script SQL de inserción"""

    # Mapeo de columnas del Excel a nombres correctos de SQL
    mapeo_columnas = {
        'descripion': 'descripcion',  # Corregir typo del Excel
        'creado_en': 'created_at',
        'actualizado_en': 'updated_at'
    }

    # Renombrar columnas según el mapeo
    df_renamed = df.rename(columns=mapeo_columnas)

    # Obtener nombres de columnas (excluyendo id si existe)
    columnas = [col for col in df_renamed.columns if col.lower() != 'id']

    print(f"\n📝 Generando script SQL para {len(df_renamed)} registros...")
    print(f"📋 Columnas a importar: {', '.join(columnas)}")

    # Crear archivo SQL
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archivo_sql = f'importar_partes_{timestamp}.sql'

    with open(archivo_sql, 'w', encoding='utf-8') as f:
        # Encabezado del script
        f.write(f"""-- ============================================================================
-- Script de importación de datos para tbl_partes
-- Generado automáticamente desde: Para exportar.xlsx
-- Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-- Total de registros: {len(df_renamed)}
-- ============================================================================

-- Configuración inicial
SET FOREIGN_KEY_CHECKS = 0;
SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';
SET AUTOCOMMIT = 0;
START TRANSACTION;

-- Usar el schema correcto
USE {schema};

-- ============================================================================
-- AÑADIR CAMPOS ADICIONALES SI NO EXISTEN
-- ============================================================================

-- Procedimiento auxiliar para añadir columnas
DELIMITER //

DROP PROCEDURE IF EXISTS add_column_if_not_exists//
CREATE PROCEDURE add_column_if_not_exists(
    IN p_table_name VARCHAR(64),
    IN p_column_name VARCHAR(64),
    IN p_column_definition TEXT
)
BEGIN
    DECLARE column_count INT;

    SELECT COUNT(*) INTO column_count
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = p_table_name
    AND COLUMN_NAME = p_column_name;

    IF column_count = 0 THEN
        SET @sql = CONCAT('ALTER TABLE ', p_table_name,
                         ' ADD COLUMN ', p_column_name, ' ', p_column_definition);
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END IF;
END//

DELIMITER ;

-- Añadir campos que podrían no existir
CALL add_column_if_not_exists('tbl_partes', 'titulo', 'VARCHAR(255)');
CALL add_column_if_not_exists('tbl_partes', 'descripcion_larga', 'TEXT');
CALL add_column_if_not_exists('tbl_partes', 'descripcion_corta', 'VARCHAR(100)');
CALL add_column_if_not_exists('tbl_partes', 'id_estado', 'INT');
CALL add_column_if_not_exists('tbl_partes', 'finalizada', 'BOOLEAN DEFAULT 0');
CALL add_column_if_not_exists('tbl_partes', 'localizacion', 'VARCHAR(255)');
CALL add_column_if_not_exists('tbl_partes', 'id_municipio', 'INT');
CALL add_column_if_not_exists('tbl_partes', 'latitud', 'DECIMAL(10,8)');
CALL add_column_if_not_exists('tbl_partes', 'longitud', 'DECIMAL(11,8)');
CALL add_column_if_not_exists('tbl_partes', 'observaciones', 'TEXT');
CALL add_column_if_not_exists('tbl_partes', 'trabajadores', 'INT DEFAULT 0');
CALL add_column_if_not_exists('tbl_partes', 'estado', 'VARCHAR(50)');

-- Limpiar procedimiento
DROP PROCEDURE IF EXISTS add_column_if_not_exists;

-- ============================================================================
-- INSERCIÓN DE DATOS EN tbl_partes
-- ============================================================================

""")

        # Generar INSERTs
        for idx, row in df_renamed.iterrows():
            # Crear lista de valores
            valores = []
            for col in columnas:
                valores.append(generar_valor_sql(row[col]))

            # Generar INSERT
            columnas_str = ', '.join(columnas)
            valores_str = ', '.join(valores)

            f.write(f"-- Registro {idx + 1}/{len(df_renamed)}\n")
            f.write(f"INSERT INTO {schema}.tbl_partes ({columnas_str})\n")
            f.write(f"VALUES ({valores_str});\n\n")

        # Pie del script
        f.write(f"""
-- ============================================================================
-- FINALIZACIÓN
-- ============================================================================

COMMIT;
SET FOREIGN_KEY_CHECKS = 1;

-- Verificar inserción
SELECT COUNT(*) as 'Total registros en tbl_partes' FROM {schema}.tbl_partes;

-- Mostrar últimos registros insertados
SELECT * FROM {schema}.tbl_partes ORDER BY id DESC LIMIT 10;

-- ============================================================================
-- Script completado exitosamente
-- ============================================================================
""")

    print(f"\n✅ Script SQL generado exitosamente: {archivo_sql}")
    print(f"📊 Total de registros a importar: {len(df)}")
    print(f"\n📌 Para ejecutar en MySQL Workbench:")
    print(f"   1. Abre MySQL Workbench")
    print(f"   2. Conecta a tu servidor MySQL")
    print(f"   3. Abre el archivo: {archivo_sql}")
    print(f"   4. Ejecuta el script (Ctrl+Shift+Enter)")

    return archivo_sql

def main():
    """Función principal"""
    print("\n" + "="*80)
    print("🔧 GENERADOR DE SCRIPT SQL DESDE EXCEL")
    print("="*80 + "\n")

    # Leer Excel
    df = leer_excel()

    # Mostrar información del DataFrame
    print(f"\n📊 Información del archivo:")
    print(f"   - Registros: {len(df)}")
    print(f"   - Columnas: {len(df.columns)}")

    # Mostrar primeras filas
    print(f"\n👀 Vista previa de los primeros 3 registros:")
    print(df.head(3).to_string())

    # Preguntar schema
    print(f"\n")
    schema = input("Nombre del schema/base de datos (default: cert_dev): ").strip()
    if not schema:
        schema = 'cert_dev'

    # Generar script
    archivo_sql = generar_script_sql(df, schema)

    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
