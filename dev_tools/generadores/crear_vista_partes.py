#!/usr/bin/env python3
"""
Script ROBUSTO para crear la vista vw_partes_completo.
Verifica TODAS las columnas antes de usarlas.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from script.db_config import get_config
import mysql.connector


def crear_vista_robusta(user: str, password: str, schema: str):
    """Crea la vista verificando absolutamente todo."""

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
    print("  CREACIÓN DE VISTA vw_partes_completo (VERSIÓN ROBUSTA)")
    print("=" * 80)

    # 1. Obtener columnas de tbl_partes
    print("\n📋 Analizando estructura de tbl_partes:")
    cursor.execute(f"""
        SELECT COLUMN_NAME
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = '{schema}'
        AND TABLE_NAME = 'tbl_partes'
    """)
    columnas_partes = {row[0] for row in cursor.fetchall()}

    print(f"   ✅ {len(columnas_partes)} columnas encontradas")

    # Verificar columnas FK importantes
    fk_info = {
        'id_ot': ('dim_ot', 'tbl_ot'),
        'id_red': ('dim_red', 'tbl_red'),
        'id_tipo_trabajo': ('dim_tipo_trabajo', 'tbl_tipo_trabajo'),
        'id_cod_trabajo': ('dim_cod_trabajo', 'tbl_cod_trabajo'),
        'id_municipio': ('tbl_municipios',),
        'id_estado': ('tbl_parte_estados',),
    }

    print("\n📋 Columnas FK en tbl_partes:")
    for fk_col, _ in fk_info.items():
        icono = "✅" if fk_col in columnas_partes else "⚠️ "
        print(f"   {icono} {fk_col}")

    # 2. Verificar qué tablas existen
    def tabla_existe(nombre_tabla):
        cursor.execute(f"""
            SELECT COUNT(*)
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = '{schema}'
            AND TABLE_NAME = '{nombre_tabla}'
        """)
        return cursor.fetchone()[0] > 0

    def get_columnas(tabla):
        cursor.execute(f"""
            SELECT COLUMN_NAME
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = '{schema}'
            AND TABLE_NAME = '{tabla}'
        """)
        return {row[0] for row in cursor.fetchall()}

    def get_columna_texto(tabla):
        """Encuentra la mejor columna de texto en una tabla."""
        cols = get_columnas(tabla)
        # Prioridad: nombre > descripcion > primera columna no-id
        if 'nombre' in cols:
            return 'nombre'
        elif 'descripcion' in cols:
            return 'descripcion'
        else:
            col = next((c for c in sorted(cols) if c not in ['id', 'codigo'] and not c.startswith('id_')), None)
            return col if col else 'id'

    # 3. Construir SELECT base con columnas que SIEMPRE existen
    select_parts = [
        "p.id",
        "p.codigo" if 'codigo' in columnas_partes else "p.id AS codigo"
    ]

    # Columnas nuevas de la migración
    nuevas_columnas = [
        'titulo', 'descripcion', 'descripcion_larga', 'descripcion_corta',
        'fecha_inicio', 'fecha_fin', 'fecha_prevista_fin',
        'finalizada', 'localizacion'
    ]

    for col in nuevas_columnas:
        if col in columnas_partes:
            if col == 'descripcion':
                select_parts.append("p.descripcion AS descripcion_original")
            else:
                select_parts.append(f"p.{col}")

    # Cálculos
    if 'fecha_inicio' in columnas_partes and 'fecha_fin' in columnas_partes:
        select_parts.append("""CASE
            WHEN p.fecha_fin IS NOT NULL AND p.fecha_inicio IS NOT NULL
            THEN DATEDIFF(p.fecha_fin, p.fecha_inicio)
            ELSE NULL
        END AS dias_duracion""")

    if 'fecha_prevista_fin' in columnas_partes and 'fecha_fin' in columnas_partes:
        select_parts.append("""CASE
            WHEN p.fecha_fin IS NULL AND p.fecha_prevista_fin IS NOT NULL
            THEN DATEDIFF(CURDATE(), p.fecha_prevista_fin)
            ELSE NULL
        END AS dias_retraso""")

    # 4. Construir JOINs solo para FKs que existen
    joins = []

    # Estado (debe existir por la migración)
    if 'id_estado' in columnas_partes and tabla_existe('tbl_parte_estados'):
        select_parts.extend([
            "pe.nombre AS estado",
            "pe.descripcion AS estado_descripcion"
        ])
        joins.append("LEFT JOIN tbl_parte_estados pe ON p.id_estado = pe.id")
    else:
        select_parts.extend([
            "NULL AS estado",
            "NULL AS estado_descripcion"
        ])

    # Municipio
    if 'id_municipio' in columnas_partes and tabla_existe('tbl_municipios'):
        col_municipio = get_columna_texto('tbl_municipios')
        select_parts.append(f"m.{col_municipio} AS municipio")
        joins.append("LEFT JOIN tbl_municipios m ON p.id_municipio = m.id")
    else:
        select_parts.append("NULL AS municipio")

    # OT
    if 'id_ot' in columnas_partes:
        if tabla_existe('dim_ot'):
            col_ot = get_columna_texto('dim_ot')
            select_parts.append(f"ot.{col_ot} AS ot")
            joins.append("LEFT JOIN dim_ot ot ON p.id_ot = ot.id")
        elif tabla_existe('tbl_ot'):
            col_ot = get_columna_texto('tbl_ot')
            select_parts.append(f"ot.{col_ot} AS ot")
            joins.append("LEFT JOIN tbl_ot ot ON p.id_ot = ot.id")
        else:
            select_parts.append("NULL AS ot")
    else:
        select_parts.append("NULL AS ot")

    # Red
    if 'id_red' in columnas_partes:
        if tabla_existe('dim_red'):
            col_red = get_columna_texto('dim_red')
            select_parts.append(f"r.{col_red} AS red")
            joins.append("LEFT JOIN dim_red r ON p.id_red = r.id")
        elif tabla_existe('tbl_red'):
            col_red = get_columna_texto('tbl_red')
            select_parts.append(f"r.{col_red} AS red")
            joins.append("LEFT JOIN tbl_red r ON p.id_red = r.id")
        else:
            select_parts.append("NULL AS red")
    else:
        select_parts.append("NULL AS red")

    # Tipo de trabajo
    if 'id_tipo_trabajo' in columnas_partes:
        if tabla_existe('dim_tipo_trabajo'):
            col_tipo = get_columna_texto('dim_tipo_trabajo')
            select_parts.append(f"tt.{col_tipo} AS tipo_trabajo")
            joins.append("LEFT JOIN dim_tipo_trabajo tt ON p.id_tipo_trabajo = tt.id")
        elif tabla_existe('tbl_tipo_trabajo'):
            col_tipo = get_columna_texto('tbl_tipo_trabajo')
            select_parts.append(f"tt.{col_tipo} AS tipo_trabajo")
            joins.append("LEFT JOIN tbl_tipo_trabajo tt ON p.id_tipo_trabajo = tt.id")
        else:
            select_parts.append("NULL AS tipo_trabajo")
    else:
        select_parts.append("NULL AS tipo_trabajo")

    # Código de trabajo
    if 'id_cod_trabajo' in columnas_partes:
        if tabla_existe('dim_cod_trabajo'):
            col_cod = get_columna_texto('dim_cod_trabajo')
            select_parts.append(f"ct.{col_cod} AS cod_trabajo")
            joins.append("LEFT JOIN dim_cod_trabajo ct ON p.id_cod_trabajo = ct.id")
        elif tabla_existe('tbl_cod_trabajo'):
            col_cod = get_columna_texto('tbl_cod_trabajo')
            select_parts.append(f"ct.{col_cod} AS cod_trabajo")
            joins.append("LEFT JOIN tbl_cod_trabajo ct ON p.id_cod_trabajo = ct.id")
        else:
            select_parts.append("NULL AS cod_trabajo")
    else:
        select_parts.append("NULL AS cod_trabajo")

    # Campos de auditoría opcionales
    if 'fecha_creacion' in columnas_partes:
        select_parts.append("p.fecha_creacion")
    if 'fecha_modificacion' in columnas_partes:
        select_parts.append("p.fecha_modificacion")

    # 5. Construir SQL final
    sql = f"""DROP VIEW IF EXISTS vw_partes_completo;

CREATE VIEW vw_partes_completo AS
SELECT
    {',\n    '.join(select_parts)}
FROM tbl_partes p
{'\n'.join(joins)}
ORDER BY {'p.fecha_inicio DESC, ' if 'fecha_inicio' in columnas_partes else ''}p.id DESC;"""

    print("\n📄 SQL generado:")
    print("-" * 80)
    print(sql)
    print("-" * 80)

    # 6. Ejecutar
    print("\n🚀 Ejecutando...")
    try:
        for statement in sql.split(';'):
            statement = statement.strip()
            if statement:
                cursor.execute(statement)

        conn.commit()
        print("✅ Vista creada exitosamente!")

        # Probar la vista
        print("\n🧪 Probando vista...")
        cursor.execute("SELECT COUNT(*) FROM vw_partes_completo")
        count = cursor.fetchone()[0]
        print(f"   ✅ Vista funciona correctamente ({count} registros)")

        # Mostrar columnas de la vista
        cursor.execute("SHOW COLUMNS FROM vw_partes_completo")
        columnas_vista = [row[0] for row in cursor.fetchall()]
        print(f"\n📊 Vista creada con {len(columnas_vista)} columnas:")
        for col in columnas_vista:
            print(f"   • {col}")

    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

    print("\n" + "=" * 80)
    print("✅ VISTA CREADA CON ÉXITO")
    print("=" * 80)
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Crear vista vw_partes_completo (versión robusta)'
    )
    parser.add_argument('--user', required=True, help='Usuario de MySQL')
    parser.add_argument('--password', required=True, help='Contraseña de MySQL')
    parser.add_argument('--schema', required=True, help='Esquema donde crear')

    args = parser.parse_args()

    try:
        exito = crear_vista_robusta(args.user, args.password, args.schema)
        sys.exit(0 if exito else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
