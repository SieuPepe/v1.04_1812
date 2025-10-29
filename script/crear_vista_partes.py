#!/usr/bin/env python3
"""
Script para crear la vista vw_partes_completo adaptándose a las tablas disponibles.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from script.db_config import get_config
import mysql.connector


def crear_vista(user: str, password: str, schema: str):
    """Crea la vista vw_partes_completo adaptándose a las tablas existentes."""

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
    print("  CREACIÓN DE VISTA vw_partes_completo")
    print("=" * 80)

    # Función auxiliar para obtener columnas de una tabla
    def get_columnas(tabla):
        """Obtiene las columnas de una tabla."""
        cursor.execute(f"""
            SELECT COLUMN_NAME
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = '{schema}'
            AND TABLE_NAME = '{tabla}'
        """)
        return {row[0] for row in cursor.fetchall()}

    # Verificar qué tablas existen
    print("\n📋 Verificando tablas y columnas disponibles:")

    tablas_a_verificar = [
        'tbl_municipios',
        'dim_ot',
        'dim_red',
        'dim_tipo_trabajo',
        'dim_cod_trabajo',
        'tbl_ot',
        'tbl_red',
        'tbl_tipo_trabajo',
        'tbl_cod_trabajo'
    ]

    tablas_existentes = {}
    columnas_tablas = {}

    for tabla in tablas_a_verificar:
        cursor.execute(f"""
            SELECT COUNT(*)
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = '{schema}'
            AND TABLE_NAME = '{tabla}'
        """)
        existe = cursor.fetchone()[0] > 0
        tablas_existentes[tabla] = existe

        if existe:
            columnas_tablas[tabla] = get_columnas(tabla)
            icono = "✅"
        else:
            icono = "⚠️ "

        print(f"   {icono} {tabla}")

    # Construir la vista adaptándose a las tablas disponibles
    print("\n🔨 Construyendo vista adaptada...")

    # Selecciones base
    select_parts = [
        "p.id",
        "p.codigo",
        "p.titulo",
        "p.descripcion AS descripcion_original",
        "p.descripcion_larga",
        "p.descripcion_corta",
        "p.fecha_inicio",
        "p.fecha_fin",
        "p.fecha_prevista_fin",
        """CASE
            WHEN p.fecha_fin IS NOT NULL AND p.fecha_inicio IS NOT NULL
            THEN DATEDIFF(p.fecha_fin, p.fecha_inicio)
            ELSE NULL
        END AS dias_duracion""",
        """CASE
            WHEN p.fecha_fin IS NULL AND p.fecha_prevista_fin IS NOT NULL
            THEN DATEDIFF(CURDATE(), p.fecha_prevista_fin)
            ELSE NULL
        END AS dias_retraso""",
        "pe.nombre AS estado",
        "pe.descripcion AS estado_descripcion",
        "p.finalizada"
    ]

    # Joins base (siempre necesarios)
    joins = [
        "LEFT JOIN tbl_parte_estados pe ON p.id_estado = pe.id"
    ]

    # Añadir campos y joins según tablas disponibles
    if tablas_existentes.get('tbl_municipios'):
        columnas = columnas_tablas.get('tbl_municipios', set())
        select_parts.append("p.localizacion")

        # Intentar diferentes nombres de columna
        if 'nombre' in columnas:
            select_parts.append("m.nombre AS municipio")
        elif 'municipio' in columnas:
            select_parts.append("m.municipio AS municipio")
        elif 'descripcion' in columnas:
            select_parts.append("m.descripcion AS municipio")
        else:
            # Usar la primera columna que no sea id
            col_texto = next((c for c in columnas if c not in ['id', 'codigo']), None)
            if col_texto:
                select_parts.append(f"m.{col_texto} AS municipio")
            else:
                select_parts.append("NULL AS municipio")

        joins.append("LEFT JOIN tbl_municipios m ON p.id_municipio = m.id")
    else:
        select_parts.extend([
            "p.localizacion",
            "NULL AS municipio"
        ])

    # Función auxiliar para obtener columna de nombre
    def get_columna_nombre(tabla):
        """Obtiene la columna apropiada para el nombre de una tabla."""
        cols = columnas_tablas.get(tabla, set())
        if 'nombre' in cols:
            return 'nombre'
        elif 'descripcion' in cols:
            return 'descripcion'
        else:
            # Buscar primera columna de texto que no sea id/codigo
            col_texto = next((c for c in cols if c not in ['id', 'codigo'] and not c.startswith('id_')), None)
            return col_texto if col_texto else 'id'

    # Tablas de dimensiones (probar primero con prefijo dim_, luego tbl_)
    if tablas_existentes.get('dim_ot') or tablas_existentes.get('tbl_ot'):
        tabla_ot = 'dim_ot' if tablas_existentes.get('dim_ot') else 'tbl_ot'
        col_nombre = get_columna_nombre(tabla_ot)
        select_parts.append(f"ot.{col_nombre} AS ot")
        joins.append(f"LEFT JOIN {tabla_ot} ot ON p.id_ot = ot.id")
    else:
        select_parts.append("NULL AS ot")

    if tablas_existentes.get('dim_red') or tablas_existentes.get('tbl_red'):
        tabla_red = 'dim_red' if tablas_existentes.get('dim_red') else 'tbl_red'
        col_nombre = get_columna_nombre(tabla_red)
        select_parts.append(f"r.{col_nombre} AS red")
        joins.append(f"LEFT JOIN {tabla_red} r ON p.id_red = r.id")
    else:
        select_parts.append("NULL AS red")

    if tablas_existentes.get('dim_tipo_trabajo') or tablas_existentes.get('tbl_tipo_trabajo'):
        tabla_tipo = 'dim_tipo_trabajo' if tablas_existentes.get('dim_tipo_trabajo') else 'tbl_tipo_trabajo'
        col_nombre = get_columna_nombre(tabla_tipo)
        select_parts.append(f"tt.{col_nombre} AS tipo_trabajo")
        joins.append(f"LEFT JOIN {tabla_tipo} tt ON p.id_tipo_trabajo = tt.id")
    else:
        select_parts.append("NULL AS tipo_trabajo")

    if tablas_existentes.get('dim_cod_trabajo') or tablas_existentes.get('tbl_cod_trabajo'):
        tabla_cod = 'dim_cod_trabajo' if tablas_existentes.get('dim_cod_trabajo') else 'tbl_cod_trabajo'
        col_nombre = get_columna_nombre(tabla_cod)
        select_parts.append(f"ct.{col_nombre} AS cod_trabajo")
        joins.append(f"LEFT JOIN {tabla_cod} ct ON p.id_cod_trabajo = ct.id")
    else:
        select_parts.append("NULL AS cod_trabajo")

    # Campos de auditoría (si existen)
    select_parts.extend([
        "p.fecha_creacion",
        "p.fecha_modificacion"
    ])

    # Construir SQL completo
    sql = f"""
DROP VIEW IF EXISTS vw_partes_completo;

CREATE VIEW vw_partes_completo AS
SELECT
    {',\n    '.join(select_parts)}
FROM tbl_partes p
{'\n'.join(joins)}
ORDER BY p.fecha_inicio DESC, p.id DESC;
"""

    print("\n📄 SQL generado:")
    print("-" * 80)
    print(sql)
    print("-" * 80)

    # Ejecutar
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

        # Mostrar ejemplo
        if count > 0:
            print("\n📊 Ejemplo de registro:")
            cursor.execute("SELECT * FROM vw_partes_completo LIMIT 1")
            columns = [desc[0] for desc in cursor.description]
            row = cursor.fetchone()

            for col, val in zip(columns, row):
                print(f"   {col}: {val}")

    except Exception as e:
        print(f"❌ Error al crear vista: {e}")
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
        description='Crear vista vw_partes_completo'
    )
    parser.add_argument('--user', required=True, help='Usuario de MySQL')
    parser.add_argument('--password', required=True, help='Contraseña de MySQL')
    parser.add_argument('--schema', required=True, help='Esquema donde crear')

    args = parser.parse_args()

    try:
        exito = crear_vista(args.user, args.password, args.schema)
        sys.exit(0 if exito else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
