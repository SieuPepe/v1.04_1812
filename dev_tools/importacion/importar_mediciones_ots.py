#!/usr/bin/env python3
"""
Script para importar mediciones desde Excel a tbl_part_presupuesto
HydroFlow Manager v1.04

DESCRIPCIÓN:
  Importa las mediciones de trabajos realizados desde MEDICIONES OTS.xlsx
  a la tabla tbl_part_presupuesto. El archivo Excel contiene:
  - precio_id: ID del precio en tbl_pres_precios
  - cantidad: Cantidad de unidades
  - fecha_unidad: Fecha de la medición (opcional)
  - parte_id: Código del parte (OT/xxxx, TP/xxxx, etc.)

IMPORTANTE:
  - El ID se genera automáticamente
  - El precio_unit se obtiene de tbl_pres_precios.coste
  - Los códigos de parte deben existir en tbl_partes

USO:
  python3 script/importar_mediciones_ots.py [--dry-run] [--schema SCHEMA]
"""

import os
import sys
import argparse
from pathlib import Path
import pandas as pd
from datetime import datetime

# Añadir directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from script.db_connection import get_project_connection

# Configuración por defecto
DEFAULT_SCHEMA = 'cert_dev'
EXCEL_FILE = 'MEDICIONES OTS.xlsx'

# Cargar .env
try:
    from dotenv import load_dotenv
    project_root = Path(__file__).parent.parent.parent
    load_dotenv(dotenv_path=project_root / '.env')
except ImportError:
    pass


def validar_archivo_excel(archivo_path):
    """Valida que el archivo Excel existe y tiene la estructura correcta."""
    if not archivo_path.exists():
        print(f"❌ ERROR: El archivo '{archivo_path}' no existe")
        return False

    try:
        df = pd.read_excel(archivo_path)
        columnas_requeridas = ['precio_id', 'cantidad', 'fecha_unidad', 'parte_id']

        for col in columnas_requeridas:
            if col not in df.columns:
                print(f"❌ ERROR: Falta la columna requerida: {col}")
                return False

        print(f"✅ Archivo Excel válido: {len(df)} registros encontrados")
        return True

    except Exception as e:
        print(f"❌ ERROR al leer el archivo Excel: {e}")
        return False


def obtener_precio_unitario(cursor, precio_id):
    """Obtiene el precio unitario desde tbl_pres_precios."""
    cursor.execute("""
        SELECT coste
        FROM tbl_pres_precios
        WHERE id = %s
    """, (int(precio_id),))

    result = cursor.fetchone()
    return float(result[0]) if result else None


def obtener_parte_id_interno(cursor, codigo_parte):
    """Obtiene el ID interno del parte a partir de su código."""
    cursor.execute("""
        SELECT id
        FROM tbl_partes
        WHERE codigo = %s
    """, (codigo_parte,))

    result = cursor.fetchone()
    return result[0] if result else None


def importar_mediciones(schema, user, password, dry_run=False):
    """
    Importa las mediciones desde el archivo Excel a la base de datos.

    Args:
        schema: Esquema de la base de datos
        user: Usuario de la base de datos
        password: Contraseña del usuario
        dry_run: Si es True, solo simula la importación sin insertar datos

    Returns:
        tuple: (éxito: bool, registros_procesados: int, registros_insertados: int)
    """
    archivo_excel = root_dir / EXCEL_FILE

    # Validar archivo
    if not validar_archivo_excel(archivo_excel):
        return False, 0, 0

    # Leer Excel
    print(f"\n📖 Leyendo archivo {EXCEL_FILE}...")
    df = pd.read_excel(archivo_excel)

    # Limpiar datos
    # Convertir precio_id a int, eliminando NaN
    df = df[df['precio_id'].notna()]
    df['precio_id'] = df['precio_id'].astype(int)

    # Convertir fecha_unidad a formato compatible con MySQL
    df['fecha_unidad'] = pd.to_datetime(df['fecha_unidad'], errors='coerce')

    print(f"   Total de registros a procesar: {len(df)}")
    print(f"   Registros con fecha: {df['fecha_unidad'].notna().sum()}")
    print(f"   Registros sin fecha: {df['fecha_unidad'].isna().sum()}")

    # Conectar a la base de datos
    try:
        with get_project_connection(user, password, schema) as conn:
            cursor = conn.cursor()

            # Estadísticas
            total_procesados = 0
            total_insertados = 0
            total_errores = 0
            partes_no_encontrados = set()
            precios_no_encontrados = set()

            print(f"\n{'🔄 SIMULACIÓN' if dry_run else '💾 IMPORTANDO'} mediciones...")
            print("-" * 80)

            # Procesar cada registro
            for idx, row in df.iterrows():
                total_procesados += 1

                precio_id = int(row['precio_id'])
                cantidad = float(row['cantidad'])
                fecha = row['fecha_unidad'] if pd.notna(row['fecha_unidad']) else None
                codigo_parte = str(row['parte_id']).strip()

                # Obtener parte_id interno
                parte_id_interno = obtener_parte_id_interno(cursor, codigo_parte)
                if parte_id_interno is None:
                    partes_no_encontrados.add(codigo_parte)
                    total_errores += 1
                    continue

                # Obtener precio_unit
                precio_unit = obtener_precio_unitario(cursor, precio_id)
                if precio_unit is None:
                    precios_no_encontrados.add(precio_id)
                    total_errores += 1
                    continue

                # Insertar registro
                if not dry_run:
                    try:
                        cursor.execute("""
                            INSERT INTO tbl_part_presupuesto
                            (parte_id, precio_id, cantidad, fecha, precio_unit)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (
                            parte_id_interno,
                            precio_id,
                            cantidad,
                            fecha,
                            precio_unit
                        ))
                        total_insertados += 1
                    except Exception as e:
                        print(f"   ⚠️  Error al insertar registro {idx + 1}: {e}")
                        total_errores += 1
                else:
                    # En modo dry-run, solo contamos
                    total_insertados += 1

                # Mostrar progreso cada 100 registros
                if total_procesados % 100 == 0:
                    print(f"   Procesados: {total_procesados}/{len(df)} registros...")

            # Commit si no es dry-run
            if not dry_run:
                conn.commit()
                print("\n✅ Transacción confirmada (COMMIT)")
            else:
                print("\n🔄 Modo simulación - No se realizaron cambios en la BD")

            cursor.close()

            # Mostrar resumen
            print("\n" + "=" * 80)
            print("📊 RESUMEN DE IMPORTACIÓN")
            print("=" * 80)
            print(f"Registros procesados:     {total_procesados}")
            print(f"Registros insertados:     {total_insertados}")
            print(f"Registros con errores:    {total_errores}")

            if partes_no_encontrados:
                print(f"\n⚠️  Partes no encontrados ({len(partes_no_encontrados)}):")
                for codigo in sorted(partes_no_encontrados)[:10]:
                    print(f"   - {codigo}")
                if len(partes_no_encontrados) > 10:
                    print(f"   ... y {len(partes_no_encontrados) - 10} más")

            if precios_no_encontrados:
                print(f"\n⚠️  Precios no encontrados ({len(precios_no_encontrados)}):")
                for precio_id in sorted(precios_no_encontrados)[:10]:
                    print(f"   - ID: {precio_id}")
                if len(precios_no_encontrados) > 10:
                    print(f"   ... y {len(precios_no_encontrados) - 10} más")

            print("\n")

            return True, total_procesados, total_insertados

    except Exception as e:
        print(f"\n❌ ERROR durante la importación: {e}")
        import traceback
        traceback.print_exc()
        return False, 0, 0


def main():
    """Punto de entrada del script."""
    parser = argparse.ArgumentParser(
        description='Importar mediciones desde Excel a tbl_part_presupuesto',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Importar mediciones
  python3 script/importar_mediciones_ots.py

  # Simulación sin insertar datos
  python3 script/importar_mediciones_ots.py --dry-run

  # Especificar esquema diferente
  python3 script/importar_mediciones_ots.py --schema mi_esquema
        """
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simula la importación sin insertar datos en la BD'
    )

    parser.add_argument(
        '--schema',
        default=DEFAULT_SCHEMA,
        help=f'Esquema de la base de datos (default: {DEFAULT_SCHEMA})'
    )

    parser.add_argument(
        '--user',
        default=None,
        help='Usuario de la base de datos (default: desde .env DB_USER)'
    )

    parser.add_argument(
        '--password',
        default=None,
        help='Contraseña de la base de datos (default: desde .env DB_PASSWORD)'
    )

    args = parser.parse_args()

    # Obtener credenciales desde variables de entorno si no se especificaron
    if args.user is None:
        args.user = os.getenv('DB_USER')
    if args.password is None:
        args.password = os.getenv('DB_PASSWORD')

    # Validar credenciales
    if not args.user or not args.password:
        print("\nERROR: Se requieren credenciales de base de datos")
        print("Especifíquelas con --user y --password")
        print("O configúrelas en el archivo .env (DB_USER y DB_PASSWORD)")
        sys.exit(1)

    # Banner
    print("=" * 80)
    print("IMPORTAR MEDICIONES DE OTS A TBL_PART_PRESUPUESTO")
    print("HydroFlow Manager v1.04")
    print("=" * 80)
    print(f"Esquema: {args.schema}")
    print(f"Modo: {'SIMULACIÓN (dry-run)' if args.dry_run else 'IMPORTACIÓN REAL'}")
    print()

    # Ejecutar importación
    exito, procesados, insertados = importar_mediciones(
        schema=args.schema,
        user=args.user,
        password=args.password,
        dry_run=args.dry_run
    )

    # Resultado final
    if exito:
        if args.dry_run:
            print("✅ Simulación completada exitosamente")
            print("   Ejecuta sin --dry-run para realizar la importación real")
        else:
            print(f"✅ Importación completada: {insertados} mediciones insertadas")
        sys.exit(0)
    else:
        print("❌ La importación falló")
        sys.exit(1)


if __name__ == "__main__":
    main()
