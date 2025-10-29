#!/usr/bin/env python3
"""
Script de migración para aplicar mejoras a la tabla tbl_partes
en todos los proyectos existentes.

Este script:
1. Lee el archivo mejoras_tabla_partes.sql
2. Lo ejecuta en todos los esquemas de proyecto (excluyendo 'manager')
3. Reporta el éxito/fallo de cada migración

Uso:
    python script/migrate_partes_mejoras.py --user USER --password PASS
    python script/migrate_partes_mejoras.py --user USER --password PASS --schema proyecto_especifico
"""

import argparse
import sys
import os
from pathlib import Path
import mysql.connector
from mysql.connector import Error

# Añadir el directorio raíz al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent))

from script.db_config import get_config
from script.db_connection import get_connection


def read_sql_file(file_path: str) -> str:
    """Lee el archivo SQL y retorna su contenido."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ ERROR: Archivo no encontrado: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR al leer archivo: {e}")
        sys.exit(1)


def get_project_schemas(user: str, password: str) -> list:
    """Obtiene lista de esquemas de proyectos (excluyendo manager, information_schema, etc.)."""
    config = get_config()
    excluded_schemas = [
        'information_schema',
        'mysql',
        'performance_schema',
        'sys',
        config.manager_schema
    ]

    try:
        with get_connection(user, password) as conn:
            cursor = conn.cursor()
            cursor.execute("SHOW DATABASES")
            all_schemas = [row[0] for row in cursor.fetchall()]

            # Filtrar esquemas excluidos
            project_schemas = [
                schema for schema in all_schemas
                if schema not in excluded_schemas
            ]

            return project_schemas
    except Error as e:
        print(f"❌ ERROR al obtener esquemas: {e}")
        return []


def check_table_exists(cursor, table_name: str) -> bool:
    """Verifica si una tabla existe en el esquema actual."""
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = '{table_name}'
    """)
    return cursor.fetchone()[0] > 0


def execute_sql_script(user: str, password: str, schema: str, sql_script: str) -> tuple:
    """
    Ejecuta el script SQL en un esquema específico.

    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Conectar al esquema específico
        config = get_config()
        conn = mysql.connector.connect(
            host=config.host,
            port=config.port,
            user=user,
            password=password,
            database=schema
        )

        cursor = conn.cursor()

        # Verificar si existe la tabla tbl_partes
        if not check_table_exists(cursor, 'tbl_partes'):
            conn.close()
            return False, "Tabla tbl_partes no existe (no es un proyecto con partes)"

        # Ejecutar el script línea por línea para manejar DELIMITER
        statements = []
        current_statement = []
        delimiter = ';'

        for line in sql_script.split('\n'):
            line = line.strip()

            # Ignorar comentarios y líneas vacías
            if not line or line.startswith('--'):
                continue

            # Detectar cambio de DELIMITER
            if line.upper().startswith('DELIMITER'):
                delimiter = line.split()[1]
                continue

            current_statement.append(line)

            # Si la línea termina con el delimiter, ejecutar el statement
            if line.endswith(delimiter):
                statement = ' '.join(current_statement)
                statement = statement[:-len(delimiter)].strip()

                if statement:
                    statements.append(statement)

                current_statement = []

        # Ejecutar cada statement
        results = []
        for statement in statements:
            if statement.strip():
                try:
                    # Ejecutar múltiples statements si es necesario
                    for result in cursor.execute(statement, multi=True):
                        if result.with_rows:
                            result.fetchall()  # Consumir resultados
                    conn.commit()
                except Error as e:
                    # Algunos errores son esperados (ej: IF NOT EXISTS)
                    if 'Duplicate' not in str(e) and 'already exists' not in str(e):
                        results.append(f"⚠️  {str(e)[:100]}")

        cursor.close()
        conn.close()

        if results:
            return True, f"Completado con avisos: {'; '.join(results)}"
        else:
            return True, "Completado exitosamente"

    except Error as e:
        return False, f"Error: {e}"
    except Exception as e:
        return False, f"Error inesperado: {e}"


def main():
    """Función principal del script de migración."""
    parser = argparse.ArgumentParser(
        description='Aplicar mejoras de tabla tbl_partes a proyectos'
    )
    parser.add_argument('--user', required=True, help='Usuario de MySQL')
    parser.add_argument('--password', required=True, help='Contraseña de MySQL')
    parser.add_argument('--schema', help='Esquema específico (opcional, si no se indica se aplica a todos)')
    parser.add_argument('--dry-run', action='store_true', help='Simular sin ejecutar cambios')

    args = parser.parse_args()

    # Banner
    print("=" * 80)
    print("  MIGRACIÓN: Mejoras de Órdenes de Trabajo (tbl_partes)")
    print("=" * 80)
    print()

    # Leer script SQL
    script_dir = Path(__file__).parent
    sql_file = script_dir / 'mejoras_tabla_partes.sql'

    print(f"📄 Leyendo script SQL: {sql_file}")
    sql_script = read_sql_file(str(sql_file))
    print(f"   ✅ Script cargado ({len(sql_script)} caracteres)")
    print()

    # Obtener esquemas a migrar
    if args.schema:
        schemas = [args.schema]
        print(f"🎯 Esquema específico: {args.schema}")
    else:
        print("🔍 Detectando esquemas de proyectos...")
        schemas = get_project_schemas(args.user, args.password)
        print(f"   ✅ Encontrados {len(schemas)} esquemas")

    print()

    if not schemas:
        print("⚠️  No se encontraron esquemas para migrar")
        return

    if args.dry_run:
        print("🔸 MODO DRY-RUN: No se ejecutarán cambios")
        print()
        print("Esquemas que se migrarían:")
        for schema in schemas:
            print(f"  • {schema}")
        return

    # Aplicar migración a cada esquema
    print("🚀 Iniciando migración...")
    print()

    success_count = 0
    skip_count = 0
    error_count = 0

    for i, schema in enumerate(schemas, 1):
        print(f"[{i}/{len(schemas)}] {schema}...", end=' ')

        success, message = execute_sql_script(args.user, args.password, schema, sql_script)

        if success:
            if "no existe" in message:
                print(f"⏭️  OMITIDO: {message}")
                skip_count += 1
            else:
                print(f"✅ {message}")
                success_count += 1
        else:
            print(f"❌ {message}")
            error_count += 1

    # Resumen final
    print()
    print("=" * 80)
    print("  RESUMEN DE MIGRACIÓN")
    print("=" * 80)
    print(f"  ✅ Exitosos:  {success_count}")
    print(f"  ⏭️  Omitidos:  {skip_count}")
    print(f"  ❌ Errores:   {error_count}")
    print(f"  📊 Total:     {len(schemas)}")
    print("=" * 80)

    if error_count > 0:
        print()
        print("⚠️  Algunos esquemas tuvieron errores. Revisa los mensajes anteriores.")
        sys.exit(1)
    else:
        print()
        print("🎉 ¡Migración completada exitosamente!")
        sys.exit(0)


if __name__ == '__main__':
    main()
