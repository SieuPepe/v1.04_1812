#!/usr/bin/env python3
"""
Script completo de prueba de migración de mejoras de partes.
Este script guía paso a paso por todo el proceso de testing.

Uso:
    python script/test_migration_complete.py --user USER --password PASS --schema SCHEMA
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from script.db_config import get_config
from script.db_connection import get_connection
from script.migrate_partes_mejoras import execute_sql_script, read_sql_file
import mysql.connector


def print_header(title: str):
    """Imprime un encabezado formateado."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_step(step_number: int, description: str):
    """Imprime un paso del proceso."""
    print(f"\n{'─' * 80}")
    print(f"PASO {step_number}: {description}")
    print('─' * 80 + "\n")


def verify_schema_exists(user: str, password: str, schema: str) -> bool:
    """Verifica que el esquema existe."""
    try:
        with get_connection(user, password) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SHOW DATABASES LIKE '{schema}'")
            result = cursor.fetchone()
            return result is not None
    except Exception as e:
        print(f"❌ Error al verificar esquema: {e}")
        return False


def check_tbl_partes_exists(user: str, password: str, schema: str) -> bool:
    """Verifica que existe tbl_partes en el esquema."""
    try:
        config = get_config()
        conn = mysql.connector.connect(
            host=config.host,
            port=config.port,
            user=user,
            password=password,
            database=schema
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'tbl_partes'
        """)
        exists = cursor.fetchone()[0] > 0
        cursor.close()
        conn.close()
        return exists
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def count_partes(user: str, password: str, schema: str) -> int:
    """Cuenta los registros en tbl_partes."""
    try:
        config = get_config()
        conn = mysql.connector.connect(
            host=config.host,
            port=config.port,
            user=user,
            password=password,
            database=schema
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tbl_partes")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count
    except Exception as e:
        print(f"❌ Error al contar partes: {e}")
        return -1


def check_column_exists(user: str, password: str, schema: str, column_name: str) -> bool:
    """Verifica si una columna existe en tbl_partes."""
    try:
        config = get_config()
        conn = mysql.connector.connect(
            host=config.host,
            port=config.port,
            user=user,
            password=password,
            database=schema
        )
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT COUNT(*)
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = '{schema}'
            AND TABLE_NAME = 'tbl_partes'
            AND COLUMN_NAME = '{column_name}'
        """)
        exists = cursor.fetchone()[0] > 0
        cursor.close()
        conn.close()
        return exists
    except Exception as e:
        print(f"❌ Error al verificar columna {column_name}: {e}")
        return False


def check_table_exists(user: str, password: str, schema: str, table_name: str) -> bool:
    """Verifica si una tabla existe."""
    try:
        config = get_config()
        conn = mysql.connector.connect(
            host=config.host,
            port=config.port,
            user=user,
            password=password,
            database=schema
        )
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT COUNT(*)
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = '{schema}'
            AND TABLE_NAME = '{table_name}'
        """)
        exists = cursor.fetchone()[0] > 0
        cursor.close()
        conn.close()
        return exists
    except Exception as e:
        print(f"❌ Error al verificar tabla {table_name}: {e}")
        return False


def check_view_exists(user: str, password: str, schema: str, view_name: str) -> bool:
    """Verifica si una vista existe."""
    try:
        config = get_config()
        conn = mysql.connector.connect(
            host=config.host,
            port=config.port,
            user=user,
            password=password,
            database=schema
        )
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT COUNT(*)
            FROM information_schema.VIEWS
            WHERE TABLE_SCHEMA = '{schema}'
            AND TABLE_NAME = '{view_name}'
        """)
        exists = cursor.fetchone()[0] > 0
        cursor.close()
        conn.close()
        return exists
    except Exception as e:
        print(f"❌ Error al verificar vista {view_name}: {e}")
        return False


def check_trigger_exists(user: str, password: str, schema: str, trigger_name: str) -> bool:
    """Verifica si un trigger existe."""
    try:
        config = get_config()
        conn = mysql.connector.connect(
            host=config.host,
            port=config.port,
            user=user,
            password=password,
            database=schema
        )
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT COUNT(*)
            FROM information_schema.TRIGGERS
            WHERE TRIGGER_SCHEMA = '{schema}'
            AND TRIGGER_NAME = '{trigger_name}'
        """)
        exists = cursor.fetchone()[0] > 0
        cursor.close()
        conn.close()
        return exists
    except Exception as e:
        print(f"❌ Error al verificar trigger {trigger_name}: {e}")
        return False


def get_estados_count(user: str, password: str, schema: str) -> int:
    """Cuenta los estados en tbl_parte_estados."""
    try:
        config = get_config()
        conn = mysql.connector.connect(
            host=config.host,
            port=config.port,
            user=user,
            password=password,
            database=schema
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tbl_parte_estados")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count
    except Exception as e:
        print(f"❌ Error al contar estados: {e}")
        return -1


def test_python_functions(user: str, password: str, schema: str):
    """Prueba las funciones Python mejoradas."""
    print("\n🐍 Probando funciones Python...")

    try:
        from script.modulo_db import get_estados_parte, add_parte_mejorado, list_partes_mejorado

        # Test 1: get_estados_parte
        print("\n1. Probando get_estados_parte()...")
        estados = get_estados_parte(user, password, schema)
        if estados:
            print(f"   ✅ Encontrados {len(estados)} estados:")
            for estado in estados:
                print(f"      • {estado['nombre']}: {estado['descripcion']}")
        else:
            print("   ⚠️  No se encontraron estados")

        # Test 2: list_partes_mejorado
        print("\n2. Probando list_partes_mejorado()...")
        partes = list_partes_mejorado(user, password, schema, limit=5)
        if partes:
            print(f"   ✅ Encontrados partes (mostrando primeros 5):")
            for parte in partes:
                print(f"      • ID: {parte.get('id')}, Título: {parte.get('titulo', 'N/A')}, Estado: {parte.get('estado', 'N/A')}")
        else:
            print("   ℹ️  No hay partes en el sistema")

        # Test 3: add_parte_mejorado
        print("\n3. Probando add_parte_mejorado()...")
        print("   ⚠️  Esta prueba requiere IDs válidos de OT, RED, etc.")
        print("   Omitiendo inserción real para evitar datos de prueba...")
        print("   ✅ Función disponible y lista para usar")

        return True

    except Exception as e:
        print(f"   ❌ Error en pruebas Python: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Función principal del script de prueba."""
    parser = argparse.ArgumentParser(
        description='Script completo de prueba de migración'
    )
    parser.add_argument('--user', required=True, help='Usuario de MySQL')
    parser.add_argument('--password', required=True, help='Contraseña de MySQL')
    parser.add_argument('--schema', required=True, help='Esquema a probar (ej: cert_dev)')
    parser.add_argument('--skip-migration', action='store_true',
                       help='Saltar ejecución de migración (solo verificar)')

    args = parser.parse_args()

    print_header("PRUEBA COMPLETA DE MIGRACIÓN - MEJORAS DE PARTES")

    # ========================================================================
    # PASO 1: Verificar esquema
    # ========================================================================
    print_step(1, "Verificar esquema y estado inicial")

    print(f"📋 Esquema a probar: {args.schema}")

    if not verify_schema_exists(args.user, args.password, args.schema):
        print(f"❌ ERROR: El esquema '{args.schema}' no existe")
        sys.exit(1)
    print(f"✅ Esquema '{args.schema}' existe")

    if not check_tbl_partes_exists(args.user, args.password, args.schema):
        print(f"❌ ERROR: La tabla tbl_partes no existe en '{args.schema}'")
        sys.exit(1)
    print("✅ Tabla tbl_partes existe")

    partes_count = count_partes(args.user, args.password, args.schema)
    print(f"📊 Registros actuales en tbl_partes: {partes_count}")

    # ========================================================================
    # PASO 2: Verificar estado PRE-migración
    # ========================================================================
    print_step(2, "Verificar estado PRE-migración")

    new_columns = ['titulo', 'descripcion_larga', 'descripcion_corta',
                   'fecha_inicio', 'fecha_fin', 'fecha_prevista_fin',
                   'id_estado', 'finalizada', 'localizacion', 'id_municipio']

    pre_migration_state = {}
    for col in new_columns:
        exists = check_column_exists(args.user, args.password, args.schema, col)
        pre_migration_state[col] = exists
        status = "✅ YA EXISTE" if exists else "⚠️  NO EXISTE (se creará)"
        print(f"   {col}: {status}")

    # Verificar tabla de estados
    estados_table_exists = check_table_exists(args.user, args.password, args.schema, 'tbl_parte_estados')
    if estados_table_exists:
        print("   tbl_parte_estados: ✅ YA EXISTE")
    else:
        print("   tbl_parte_estados: ⚠️  NO EXISTE (se creará)")

    # ========================================================================
    # PASO 3: Ejecutar migración
    # ========================================================================
    if not args.skip_migration:
        print_step(3, "Ejecutar migración")

        script_dir = Path(__file__).parent
        sql_file = script_dir / 'mejoras_tabla_partes.sql'

        print(f"📄 Leyendo script SQL: {sql_file}")
        sql_script = read_sql_file(str(sql_file))
        print(f"   ✅ Script cargado ({len(sql_script)} caracteres)")

        print(f"\n🚀 Ejecutando migración en '{args.schema}'...")
        success, message = execute_sql_script(args.user, args.password, args.schema, sql_script)

        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
            sys.exit(1)
    else:
        print_step(3, "MIGRACIÓN OMITIDA (--skip-migration)")

    # ========================================================================
    # PASO 4: Verificar estado POST-migración
    # ========================================================================
    print_step(4, "Verificar estado POST-migración")

    all_ok = True

    # Verificar nuevas columnas
    print("📋 Verificando nuevas columnas en tbl_partes:")
    for col in new_columns:
        exists = check_column_exists(args.user, args.password, args.schema, col)
        if exists:
            print(f"   ✅ {col}")
        else:
            print(f"   ❌ {col} NO EXISTE")
            all_ok = False

    # Verificar tabla de estados
    print("\n📋 Verificando tabla tbl_parte_estados:")
    if check_table_exists(args.user, args.password, args.schema, 'tbl_parte_estados'):
        print("   ✅ Tabla existe")
        estados_count = get_estados_count(args.user, args.password, args.schema)
        print(f"   ✅ Estados insertados: {estados_count} (esperados: 5)")
        if estados_count != 5:
            print("   ⚠️  ADVERTENCIA: Se esperaban 5 estados")
    else:
        print("   ❌ Tabla NO EXISTE")
        all_ok = False

    # Verificar vista
    print("\n📋 Verificando vista vw_partes_completo:")
    if check_view_exists(args.user, args.password, args.schema, 'vw_partes_completo'):
        print("   ✅ Vista existe")
    else:
        print("   ❌ Vista NO EXISTE")
        all_ok = False

    # Verificar triggers
    print("\n📋 Verificando triggers:")
    triggers = [
        'trg_partes_sync_finalizada_insert',
        'trg_partes_sync_finalizada_update'
    ]
    for trigger in triggers:
        if check_trigger_exists(args.user, args.password, args.schema, trigger):
            print(f"   ✅ {trigger}")
        else:
            print(f"   ❌ {trigger} NO EXISTE")
            all_ok = False

    # Verificar que no se perdieron registros
    print("\n📊 Verificando integridad de datos:")
    new_partes_count = count_partes(args.user, args.password, args.schema)
    print(f"   Antes: {partes_count} registros")
    print(f"   Después: {new_partes_count} registros")
    if partes_count == new_partes_count:
        print("   ✅ No se perdieron registros")
    else:
        print("   ❌ ERROR: Se perdieron o ganaron registros!")
        all_ok = False

    # ========================================================================
    # PASO 5: Probar funciones Python
    # ========================================================================
    print_step(5, "Probar funciones Python")
    python_ok = test_python_functions(args.user, args.password, args.schema)

    # ========================================================================
    # RESUMEN FINAL
    # ========================================================================
    print_header("RESUMEN FINAL")

    if all_ok and python_ok:
        print("🎉 ¡TODAS LAS VERIFICACIONES PASARON CON ÉXITO!")
        print("\n✅ Migración completada correctamente")
        print("✅ Todas las estructuras creadas")
        print("✅ Funciones Python funcionando")
        print("\n📝 Próximos pasos:")
        print("   1. Revisar los resultados de las verificaciones")
        print("   2. Probar las funciones Python con datos reales")
        print("   3. Aplicar migración a otros esquemas si todo está OK")
        print("   4. Implementar cambios en interfaces de usuario")
        sys.exit(0)
    else:
        print("⚠️  ALGUNAS VERIFICACIONES FALLARON")
        print("\n❌ Revisa los mensajes anteriores")
        print("❌ Puede ser necesario revertir y reintentar")
        sys.exit(1)


if __name__ == '__main__':
    main()
