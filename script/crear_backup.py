#!/usr/bin/env python3
"""
Script para crear backups de la base de datos MySQL
HydroFlow Manager v1.04 - FASE 1: PREPARACIÓN DE DATOS
"""
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Configuración por defecto
HOST = 'localhost'
PORT = 3307
USER = 'root'
PASSWORD = 'root'
SCHEMA = 'proyecto_tipo'  # Esquema por defecto
BACKUP_DIR = Path(__file__).parent.parent / 'backup'


def crear_backup(schema, nombre_backup, descripcion=""):
    """
    Crea un backup de un esquema MySQL usando mysqldump.

    Args:
        schema: Nombre del esquema a respaldar
        nombre_backup: Nombre del archivo de backup (sin extensión)
        descripcion: Descripción opcional del backup

    Returns:
        bool: True si el backup fue exitoso, False en caso contrario
    """
    # Asegurar que existe el directorio de backup
    BACKUP_DIR.mkdir(exist_ok=True)

    # Nombre del archivo de backup
    backup_file = BACKUP_DIR / f"{nombre_backup}.sql"

    print("=" * 70)
    print(f"CREAR BACKUP: {nombre_backup}")
    print("=" * 70)
    if descripcion:
        print(f"Descripción: {descripcion}")
    print(f"Esquema: {schema}")
    print(f"Archivo: {backup_file}")
    print()

    try:
        # Comando mysqldump
        cmd = [
            'mysqldump',
            f'--host={HOST}',
            f'--port={PORT}',
            f'--user={USER}',
            f'--password={PASSWORD}',
            '--single-transaction',
            '--routines',
            '--triggers',
            '--events',
            '--hex-blob',
            '--default-character-set=utf8mb4',
            schema
        ]

        # Ejecutar mysqldump y guardar en archivo
        print("Ejecutando mysqldump...")
        with open(backup_file, 'w', encoding='utf-8') as f:
            result = subprocess.run(
                cmd,
                stdout=f,
                stderr=subprocess.PIPE,
                text=True
            )

        if result.returncode != 0:
            print(f"ERROR al crear backup:")
            print(result.stderr)
            return False

        # Verificar que se creó el archivo
        if not backup_file.exists():
            print("ERROR: El archivo de backup no se creó")
            return False

        # Mostrar tamaño del backup
        size_mb = backup_file.stat().st_size / (1024 * 1024)
        print(f"✓ Backup creado exitosamente")
        print(f"  Tamaño: {size_mb:.2f} MB")
        print(f"  Ruta: {backup_file}")
        print("=" * 70)
        print()

        return True

    except FileNotFoundError:
        print("ERROR: mysqldump no está disponible")
        print("Instale MySQL client tools")
        return False
    except Exception as e:
        print(f"ERROR inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Punto de entrada del script."""
    if len(sys.argv) < 2:
        print("Uso:")
        print(f"  {sys.argv[0]} <nombre_backup> [schema] [descripcion]")
        print()
        print("Ejemplos:")
        print(f"  {sys.argv[0]} backup_nopres_nopartes proyecto_tipo 'BBDD limpia sin presupuestos ni partes'")
        print(f"  {sys.argv[0]} backup_con_presupuesto proyecto_tipo 'BBDD con presupuesto cargado'")
        print(f"  {sys.argv[0]} backup_completo_pruebas proyecto_tipo 'BBDD completa con presupuestos y partes'")
        sys.exit(1)

    nombre_backup = sys.argv[1]
    schema = sys.argv[2] if len(sys.argv) > 2 else SCHEMA
    descripcion = sys.argv[3] if len(sys.argv) > 3 else ""

    exito = crear_backup(schema, nombre_backup, descripcion)
    sys.exit(0 if exito else 1)


if __name__ == "__main__":
    main()
