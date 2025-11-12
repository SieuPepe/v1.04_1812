#!/usr/bin/env python3
"""
Script para generar sentencias ALTER TABLE que convierten campos DOUBLE/FLOAT a DECIMAL(10,2).

Este script se conecta a la base de datos y genera automáticamente
todas las sentencias ALTER TABLE necesarias para convertir campos numéricos
a DECIMAL(10,2) para garantizar precisión de 2 decimales.
"""

import mysql.connector
from mysql.connector import Error
import getpass


def get_numeric_columns(cursor, database):
    """
    Obtiene todas las columnas de tipo DOUBLE o FLOAT de todas las tablas.

    Args:
        cursor: Cursor de MySQL
        database: Nombre de la base de datos

    Returns:
        list: Lista de tuplas (tabla, columna, tipo_datos)
    """
    query = """
        SELECT
            TABLE_NAME,
            COLUMN_NAME,
            DATA_TYPE,
            IS_NULLABLE,
            COLUMN_DEFAULT,
            COLUMN_COMMENT
        FROM
            INFORMATION_SCHEMA.COLUMNS
        WHERE
            TABLE_SCHEMA = %s
            AND (DATA_TYPE = 'double' OR DATA_TYPE = 'float')
            AND TABLE_NAME LIKE 'tbl_%'
        ORDER BY
            TABLE_NAME, ORDINAL_POSITION
    """

    cursor.execute(query, (database,))
    return cursor.fetchall()


def generate_alter_statements(columns):
    """
    Genera sentencias ALTER TABLE para convertir columnas a DECIMAL(10,2).

    Args:
        columns: Lista de tuplas (tabla, columna, tipo_datos, nullable, default, comment)

    Returns:
        str: Script SQL con todas las sentencias ALTER TABLE
    """
    script = """-- ============================================================================
-- Script para establecer precisión de 2 decimales en todos los campos numéricos
-- Generado automáticamente desde la estructura de la base de datos
-- ============================================================================
-- Fecha: 2025-11-08
-- Descripción: Convierte todos los campos DOUBLE y FLOAT a DECIMAL(10,2)
-- ============================================================================

"""

    # Agrupar por tabla
    tables = {}
    for row in columns:
        table_name = row[0]
        col_name = row[1]
        is_nullable = row[3]
        col_default = row[4]
        col_comment = row[5] if row[5] else ''

        if table_name not in tables:
            tables[table_name] = []

        tables[table_name].append({
            'name': col_name,
            'nullable': is_nullable,
            'default': col_default,
            'comment': col_comment
        })

    # Generar ALTER TABLE para cada tabla
    for table_name in sorted(tables.keys()):
        script += f"\n-- Tabla: {table_name}\n"
        script += f"ALTER TABLE `{table_name}`\n"

        modifications = []
        for col in tables[table_name]:
            null_clause = "NULL" if col['nullable'] == 'YES' else "NOT NULL"
            default_clause = f" DEFAULT {col['default']}" if col['default'] else " DEFAULT NULL" if col['nullable'] == 'YES' else ""
            comment_clause = f" COMMENT '{col['comment']}'" if col['comment'] else ""

            modifications.append(
                f"    MODIFY COLUMN `{col['name']}` DECIMAL(10,2) {null_clause}{default_clause}{comment_clause}"
            )

        script += ",\n".join(modifications)
        script += ";\n"

    script += """
-- ============================================================================
-- Fin del script
-- ============================================================================
SELECT 'Script de corrección de precisión decimal completado' AS status;
SELECT 'Todos los campos numéricos ahora usan DECIMAL(10,2) para garantizar 2 decimales' AS info;
"""

    return script


def main():
    """Función principal."""
    print("=" * 80)
    print("GENERADOR DE SCRIPT SQL PARA CONVERSIÓN A DECIMAL(10,2)")
    print("=" * 80)
    print()

    # Solicitar datos de conexión
    host = input("Host [localhost]: ").strip() or "localhost"
    port = input("Puerto [3307]: ").strip() or "3307"
    database = input("Base de datos [cert_dev]: ").strip() or "cert_dev"
    user = input("Usuario [root]: ").strip() or "root"
    password = getpass.getpass("Contraseña: ")

    try:
        # Conectar a la base de datos
        print(f"\nConectando a {host}:{port}/{database}...")
        conn = mysql.connector.connect(
            host=host,
            port=int(port),
            database=database,
            user=user,
            password=password
        )

        if conn.is_connected():
            print("✓ Conectado correctamente\n")

            cursor = conn.cursor()

            # Obtener columnas numéricas
            print("Buscando columnas DOUBLE/FLOAT...")
            columns = get_numeric_columns(cursor, database)

            if not columns:
                print("✗ No se encontraron columnas DOUBLE/FLOAT en tablas tbl_*")
                return

            print(f"✓ Se encontraron {len(columns)} columnas numéricas\n")

            # Mostrar columnas encontradas
            print("Columnas encontradas:")
            print("-" * 80)
            for row in columns:
                print(f"  {row[0]}.{row[1]} ({row[2]})")
            print()

            # Generar script
            print("Generando script SQL...")
            script = generate_alter_statements(columns)

            # Guardar script
            output_file = "/home/user/v1.04_1812/script/sql/fix_decimal_precision_auto.sql"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(script)

            print(f"✓ Script generado: {output_file}\n")
            print("=" * 80)
            print("Para aplicar los cambios, ejecuta:")
            print(f"  mysql -h {host} -P {port} -u {user} -p {database} < {output_file}")
            print("=" * 80)

            cursor.close()
            conn.close()

    except Error as e:
        print(f"✗ Error: {e}")
    except Exception as e:
        print(f"✗ Error inesperado: {e}")


if __name__ == "__main__":
    main()
