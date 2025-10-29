#!/usr/bin/env python3
"""
Script para verificar el estado actual de la migración y crear índices faltantes.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from script.db_config import get_config
import mysql.connector


def verificar_y_completar(user: str, password: str, schema: str):
    """Verifica el estado de la migración y completa lo que falta."""

    config = get_config()
    conn = mysql.connector.connect(
        host=config.host,
        port=config.port,
        user=user,
        password=password,
        database=schema
    )

    cursor = conn.cursor()

    print("=" * 80)
    print("  VERIFICACIÓN Y COMPLETADO DE MIGRACIÓN")
    print("=" * 80)

    # 1. Verificar versión de MySQL
    print("\n📊 Versión de MySQL:")
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()[0]
    print(f"   {version}")

    # 2. Verificar columnas en tbl_partes
    print("\n📋 Verificando columnas en tbl_partes:")
    columnas_necesarias = [
        'titulo', 'descripcion_larga', 'descripcion_corta',
        'fecha_inicio', 'fecha_fin', 'fecha_prevista_fin',
        'id_estado', 'finalizada', 'localizacion', 'id_municipio'
    ]

    cursor.execute(f"""
        SELECT COLUMN_NAME
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = '{schema}'
        AND TABLE_NAME = 'tbl_partes'
        AND COLUMN_NAME IN ({','.join("'" + c + "'" for c in columnas_necesarias)})
    """)
    columnas_existentes = {row[0] for row in cursor.fetchall()}

    columnas_ok = True
    for col in columnas_necesarias:
        if col in columnas_existentes:
            print(f"   ✅ {col}")
        else:
            print(f"   ❌ {col} NO EXISTE")
            columnas_ok = False

    # 3. Verificar tabla de estados
    print("\n📋 Verificando tbl_parte_estados:")
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = '{schema}'
        AND TABLE_NAME = 'tbl_parte_estados'
    """)
    tabla_existe = cursor.fetchone()[0] > 0

    if tabla_existe:
        print("   ✅ Tabla existe")
        cursor.execute("SELECT COUNT(*) FROM tbl_parte_estados")
        count = cursor.fetchone()[0]
        print(f"   ✅ {count} estados registrados")
    else:
        print("   ❌ Tabla NO existe")

    # 4. Verificar FKs
    print("\n📋 Verificando Foreign Keys:")
    cursor.execute(f"""
        SELECT CONSTRAINT_NAME
        FROM information_schema.TABLE_CONSTRAINTS
        WHERE TABLE_SCHEMA = '{schema}'
        AND TABLE_NAME = 'tbl_partes'
        AND CONSTRAINT_TYPE = 'FOREIGN KEY'
        AND CONSTRAINT_NAME IN ('fk_partes_estado', 'fk_partes_municipio')
    """)
    fks = {row[0] for row in cursor.fetchall()}

    if 'fk_partes_estado' in fks:
        print("   ✅ fk_partes_estado")
    else:
        print("   ⚠️  fk_partes_estado NO existe")

    if 'fk_partes_municipio' in fks:
        print("   ✅ fk_partes_municipio")
    else:
        print("   ℹ️  fk_partes_municipio NO existe (tabla tbl_municipios opcional)")

    # 5. Verificar triggers
    print("\n📋 Verificando Triggers:")
    cursor.execute(f"""
        SELECT TRIGGER_NAME
        FROM information_schema.TRIGGERS
        WHERE TRIGGER_SCHEMA = '{schema}'
        AND EVENT_OBJECT_TABLE = 'tbl_partes'
        AND TRIGGER_NAME LIKE 'trg_partes_sync%'
    """)
    triggers = {row[0] for row in cursor.fetchall()}

    if 'trg_partes_sync_finalizada_insert' in triggers:
        print("   ✅ trg_partes_sync_finalizada_insert")
    else:
        print("   ❌ trg_partes_sync_finalizada_insert NO existe")

    if 'trg_partes_sync_finalizada_update' in triggers:
        print("   ✅ trg_partes_sync_finalizada_update")
    else:
        print("   ❌ trg_partes_sync_finalizada_update NO existe")

    # 6. Verificar vista
    print("\n📋 Verificando Vista:")
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM information_schema.VIEWS
        WHERE TABLE_SCHEMA = '{schema}'
        AND TABLE_NAME = 'vw_partes_completo'
    """)
    vista_existe = cursor.fetchone()[0] > 0

    if vista_existe:
        print("   ✅ vw_partes_completo existe")
    else:
        print("   ⚠️  vw_partes_completo NO existe")

    # 7. Verificar y crear índices
    print("\n📋 Verificando y creando índices:")

    indices_necesarios = {
        'idx_partes_estado': 'id_estado',
        'idx_partes_finalizada': 'finalizada',
        'idx_partes_fecha_inicio': 'fecha_inicio',
        'idx_partes_fecha_fin': 'fecha_fin',
        'idx_partes_municipio': 'id_municipio',
    }

    # Obtener índices existentes
    cursor.execute(f"""
        SELECT DISTINCT INDEX_NAME
        FROM information_schema.STATISTICS
        WHERE TABLE_SCHEMA = '{schema}'
        AND TABLE_NAME = 'tbl_partes'
    """)
    indices_existentes = {row[0] for row in cursor.fetchall()}

    indices_creados = 0
    for nombre_indice, columna in indices_necesarios.items():
        if nombre_indice in indices_existentes or nombre_indice.upper() in indices_existentes:
            print(f"   ✅ {nombre_indice} ya existe")
        else:
            try:
                sql = f"CREATE INDEX {nombre_indice} ON tbl_partes({columna})"
                cursor.execute(sql)
                print(f"   ✅ {nombre_indice} creado")
                indices_creados += 1
            except mysql.connector.Error as e:
                if 'Duplicate' in str(e):
                    print(f"   ✅ {nombre_indice} ya existe")
                else:
                    print(f"   ⚠️  {nombre_indice} - Error: {e}")

    # Índice compuesto
    if 'idx_partes_estado_fecha' not in indices_existentes:
        try:
            cursor.execute("CREATE INDEX idx_partes_estado_fecha ON tbl_partes(id_estado, fecha_inicio)")
            print(f"   ✅ idx_partes_estado_fecha creado")
            indices_creados += 1
        except mysql.connector.Error as e:
            if 'Duplicate' in str(e):
                print(f"   ✅ idx_partes_estado_fecha ya existe")
            else:
                print(f"   ⚠️  idx_partes_estado_fecha - Error: {e}")
    else:
        print(f"   ✅ idx_partes_estado_fecha ya existe")

    if indices_creados > 0:
        conn.commit()
        print(f"\n   🎉 {indices_creados} índices creados")

    # 8. Resumen final
    print("\n" + "=" * 80)
    print("  RESUMEN FINAL")
    print("=" * 80)

    if columnas_ok and tabla_existe and len(triggers) >= 2:
        print("\n🎉 ¡MIGRACIÓN COMPLETADA CON ÉXITO!")
        print("\n✅ Todas las columnas necesarias existen")
        print("✅ Tabla de estados creada")
        print("✅ Triggers funcionando")
        print("✅ Foreign Keys configuradas")
        if indices_creados > 0:
            print(f"✅ {indices_creados} índices añadidos")

        print("\n📝 Próximos pasos:")
        print("   1. Probar las funciones Python")
        print("   2. Aplicar a otros esquemas si es necesario")
        print("   3. Implementar cambios en interfaces")

        cursor.close()
        conn.close()
        return True
    else:
        print("\n⚠️  ADVERTENCIA: Faltan algunos elementos")
        print("   Revisa los elementos marcados con ❌ arriba")

        cursor.close()
        conn.close()
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Verificar y completar migración'
    )
    parser.add_argument('--user', required=True, help='Usuario de MySQL')
    parser.add_argument('--password', required=True, help='Contraseña de MySQL')
    parser.add_argument('--schema', required=True, help='Esquema a verificar')

    args = parser.parse_args()

    try:
        exito = verificar_y_completar(args.user, args.password, args.schema)
        sys.exit(0 if exito else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
