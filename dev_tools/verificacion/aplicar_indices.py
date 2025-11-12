"""
Script para aplicar índices recomendados a los esquemas de proyectos.

Este script aplica los índices definidos en indices_recomendados.sql
a todos los esquemas de proyectos activos en la base de datos.

Uso:
    python script/aplicar_indices.py --user <usuario> --password <contraseña> [--schema <esquema>]

Argumentos:
    --user: Usuario de MySQL con permisos de CREATE INDEX
    --password: Contraseña del usuario
    --schema: Esquema específico (opcional, aplica a todos los proyectos si no se especifica)
    --dry-run: Simula la ejecución sin aplicar cambios
    --verbose: Muestra información detallada
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Tuple, Optional
import mysql.connector
from mysql.connector import Error

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('aplicar_indices.log')
    ]
)
logger = logging.getLogger(__name__)

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from script.db_config import get_config
from script.db_connection import get_connection


def get_project_schemas(user: str, password: str) -> List[str]:
    """
    Obtiene la lista de esquemas de proyectos activos.

    Args:
        user: Usuario de MySQL
        password: Contraseña del usuario

    Returns:
        Lista de nombres de esquemas de proyectos
    """
    try:
        with get_connection(user, password) as cn:
            cur = cn.cursor()

            # Obtener esquemas que no son del sistema
            cur.execute("""
                SELECT SCHEMA_NAME
                FROM information_schema.SCHEMATA
                WHERE SCHEMA_NAME NOT IN (
                    'information_schema', 'mysql', 'performance_schema',
                    'sys', 'manager', 'phpmyadmin'
                )
                AND SCHEMA_NAME NOT LIKE 'tmp%'
                ORDER BY SCHEMA_NAME
            """)

            schemas = [row[0] for row in cur.fetchall()]
            cur.close()

            logger.info(f"Encontrados {len(schemas)} esquemas de proyectos")
            return schemas

    except Error as e:
        logger.error(f"Error obteniendo esquemas: {e}")
        return []


def check_index_exists(cur, schema: str, table: str, index_name: str) -> bool:
    """
    Verifica si un índice ya existe en una tabla.

    Args:
        cur: Cursor de MySQL
        schema: Nombre del esquema
        table: Nombre de la tabla
        index_name: Nombre del índice

    Returns:
        True si el índice existe, False en caso contrario
    """
    try:
        cur.execute("""
            SELECT COUNT(*)
            FROM information_schema.STATISTICS
            WHERE TABLE_SCHEMA = %s
            AND TABLE_NAME = %s
            AND INDEX_NAME = %s
        """, (schema, table, index_name))

        count = cur.fetchone()[0]
        return count > 0

    except Error as e:
        logger.error(f"Error verificando índice {index_name}: {e}")
        return False


def check_table_exists(cur, schema: str, table: str) -> bool:
    """
    Verifica si una tabla existe en un esquema.

    Args:
        cur: Cursor de MySQL
        schema: Nombre del esquema
        table: Nombre de la tabla

    Returns:
        True si la tabla existe, False en caso contrario
    """
    try:
        cur.execute("""
            SELECT COUNT(*)
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = %s
            AND TABLE_NAME = %s
        """, (schema, table))

        count = cur.fetchone()[0]
        return count > 0

    except Error as e:
        logger.error(f"Error verificando tabla {table}: {e}")
        return False


def apply_indexes_to_schema(user: str, password: str, schema: str,
                            dry_run: bool = False) -> Tuple[int, int, int]:
    """
    Aplica los índices recomendados a un esquema específico.

    Args:
        user: Usuario de MySQL
        password: Contraseña del usuario
        schema: Nombre del esquema
        dry_run: Si es True, solo simula sin aplicar cambios

    Returns:
        Tupla (índices_creados, índices_existentes, índices_fallidos)
    """
    # Definición de índices recomendados
    indexes = [
        # Índices para tbl_partes
        ("tbl_partes", "idx_partes_tipo_codigo",
         "CREATE INDEX idx_partes_tipo_codigo ON tbl_partes(tipo_trabajo_id, codigo)"),

        ("tbl_partes", "idx_partes_municipio",
         "CREATE INDEX idx_partes_municipio ON tbl_partes(municipio_id)"),

        ("tbl_partes", "idx_partes_fecha_estado",
         "CREATE INDEX idx_partes_fecha_estado ON tbl_partes(fecha_inicio DESC, id_estado)"),

        ("tbl_partes", "idx_partes_codigo",
         "CREATE INDEX idx_partes_codigo ON tbl_partes(codigo)"),

        # Índices para tbl_part_presupuesto
        ("tbl_part_presupuesto", "idx_part_presupuesto_parte_precio",
         "CREATE INDEX idx_part_presupuesto_parte_precio ON tbl_part_presupuesto(parte_id, precio_id, cantidad, precio_unit)"),

        ("tbl_part_presupuesto", "idx_part_presupuesto_parte",
         "CREATE INDEX idx_part_presupuesto_parte ON tbl_part_presupuesto(parte_id)"),

        # Índices para tbl_part_certificacion
        ("tbl_part_certificacion", "idx_part_cert_parte_certificada",
         "CREATE INDEX idx_part_cert_parte_certificada ON tbl_part_certificacion(parte_id, certificada, cantidad_cert, precio_unit)"),

        ("tbl_part_certificacion", "idx_part_cert_pendientes",
         "CREATE INDEX idx_part_cert_pendientes ON tbl_part_certificacion(certificada, parte_id)"),

        # Índices para dim_municipios
        ("dim_municipios", "idx_municipios_comarca",
         "CREATE INDEX idx_municipios_comarca ON dim_municipios(comarca_id)"),

        ("dim_municipios", "idx_municipios_provincia",
         "CREATE INDEX idx_municipios_provincia ON dim_municipios(provincia_id)"),

        # Índices para tablas dimensionales
        ("dim_red", "idx_red_descripcion",
         "CREATE INDEX idx_red_descripcion ON dim_red(descripcion)"),

        ("dim_tipo_trabajo", "idx_tipo_trabajo_descripcion",
         "CREATE INDEX idx_tipo_trabajo_descripcion ON dim_tipo_trabajo(descripcion)"),

        ("dim_codigo_trabajo", "idx_codigo_trabajo_descripcion",
         "CREATE INDEX idx_codigo_trabajo_descripcion ON dim_codigo_trabajo(descripcion)"),

        ("dim_tipos_rep", "idx_tipos_rep_descripcion",
         "CREATE INDEX idx_tipos_rep_descripcion ON dim_tipos_rep(descripcion)"),

        # Índice para tbl_parte_estados
        ("tbl_parte_estados", "idx_parte_estados_nombre",
         "CREATE INDEX idx_parte_estados_nombre ON tbl_parte_estados(nombre)"),
    ]

    created = 0
    existing = 0
    failed = 0

    try:
        with get_connection(user, password, schema) as cn:
            cur = cn.cursor()

            logger.info(f"\n{'='*70}")
            logger.info(f"Procesando esquema: {schema}")
            logger.info(f"{'='*70}")

            for table, index_name, create_sql in indexes:
                # Verificar si la tabla existe
                if not check_table_exists(cur, schema, table):
                    logger.debug(f"  ⊘ Tabla {table} no existe, saltando índice {index_name}")
                    continue

                # Verificar si el índice ya existe
                if check_index_exists(cur, schema, table, index_name):
                    logger.info(f"  ⚠ Índice {index_name} ya existe en {table}")
                    existing += 1
                    continue

                # Crear el índice
                if dry_run:
                    logger.info(f"  [DRY-RUN] Crearía índice {index_name} en {table}")
                    created += 1
                else:
                    try:
                        logger.info(f"  ⟳ Creando índice {index_name} en {table}...")
                        cur.execute(create_sql)
                        logger.info(f"  ✓ Índice {index_name} creado exitosamente")
                        created += 1
                    except Error as e:
                        logger.error(f"  ✗ Error creando índice {index_name}: {e}")
                        failed += 1

            # Ejecutar ANALYZE TABLE si se crearon índices
            if created > 0 and not dry_run:
                logger.info(f"\n  Ejecutando ANALYZE TABLE para actualizar estadísticas...")

                tables_to_analyze = set([idx[0] for idx in indexes])
                for table in tables_to_analyze:
                    if check_table_exists(cur, schema, table):
                        try:
                            cur.execute(f"ANALYZE TABLE {schema}.{table}")
                            logger.info(f"  ✓ ANALYZE TABLE {table} completado")
                        except Error as e:
                            logger.warning(f"  ⚠ Error en ANALYZE TABLE {table}: {e}")

            cur.close()

    except Error as e:
        logger.error(f"Error procesando esquema {schema}: {e}")
        return (0, 0, len(indexes))

    return (created, existing, failed)


def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(
        description='Aplica índices recomendados a esquemas de proyectos'
    )
    parser.add_argument('--user', required=True, help='Usuario de MySQL')
    parser.add_argument('--password', required=True, help='Contraseña del usuario')
    parser.add_argument('--schema', help='Esquema específico (opcional)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Simula la ejecución sin aplicar cambios')
    parser.add_argument('--verbose', action='store_true',
                       help='Muestra información detallada')

    args = parser.parse_args()

    # Configurar nivel de logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info("="*70)
    logger.info("APLICACIÓN DE ÍNDICES RECOMENDADOS")
    logger.info("="*70)

    if args.dry_run:
        logger.info("MODO DRY-RUN: No se aplicarán cambios reales")

    # Obtener lista de esquemas
    if args.schema:
        schemas = [args.schema]
        logger.info(f"Procesando esquema específico: {args.schema}")
    else:
        schemas = get_project_schemas(args.user, args.password)
        if not schemas:
            logger.error("No se encontraron esquemas de proyectos")
            return 1

    # Aplicar índices a cada esquema
    total_created = 0
    total_existing = 0
    total_failed = 0

    for schema in schemas:
        created, existing, failed = apply_indexes_to_schema(
            args.user, args.password, schema, args.dry_run
        )
        total_created += created
        total_existing += existing
        total_failed += failed

    # Resumen final
    logger.info("\n" + "="*70)
    logger.info("RESUMEN FINAL")
    logger.info("="*70)
    logger.info(f"Esquemas procesados: {len(schemas)}")
    logger.info(f"Índices creados: {total_created}")
    logger.info(f"Índices ya existentes: {total_existing}")
    logger.info(f"Índices fallidos: {total_failed}")
    logger.info("="*70)

    if args.dry_run:
        logger.info("\nEjecuta sin --dry-run para aplicar los cambios")

    return 0 if total_failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
