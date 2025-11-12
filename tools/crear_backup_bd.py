#!/usr/bin/env python3
"""
Script de Backup de Base de Datos HydroFlow Manager
====================================================

Crea una copia de seguridad completa de la base de datos incluyendo:
- Esquema 'manager' con todos los datos
- Esquema 'cert_dev' con todos los datos (ejemplo con partes y presupuestos)
- Todos los esquemas de proyectos activos

El backup se puede usar para:
- Restaurar en la misma máquina
- Instalar en una nueva máquina
- Migración de servidor

Uso:
    python crear_backup_bd.py
    python crear_backup_bd.py --output /ruta/personalizada
    python crear_backup_bd.py --restore backup_20250112_103045.sql
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
import getpass

# Añadir el directorio raíz al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent))

from script.db_config import get_config
from script import db_core


class Colors:
    """Colores ANSI para output en terminal"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_step(message):
    """Imprime un paso del proceso"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")


def print_success(message):
    """Imprime mensaje de éxito"""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")


def print_error(message):
    """Imprime mensaje de error"""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")


def print_warning(message):
    """Imprime mensaje de advertencia"""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")


def print_info(message):
    """Imprime mensaje informativo"""
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")


def get_credentials():
    """Solicita credenciales de forma segura al usuario"""
    print_step("Credenciales de Base de Datos")

    config = get_config()

    print_info(f"Servidor: {config.host}:{config.port}")
    print_info("Se requieren credenciales de administrador (con privilegios de backup)")
    print()

    user = input("Usuario MySQL: ").strip()
    password = getpass.getpass("Contraseña: ")

    return user, password


def test_connection(user, password):
    """Prueba la conexión a la base de datos"""
    print_step("Verificando conexión a la base de datos")

    try:
        conn, error = db_core.login_db(user, password)
        if error:
            print_error(f"Error de conexión: {error}")
            return False

        print_success("Conexión exitosa")
        return True

    except Exception as e:
        print_error(f"Error al conectar: {e}")
        return False


def get_all_schemas(user, password):
    """Obtiene lista de todos los esquemas relevantes"""
    print_step("Identificando esquemas a respaldar")

    try:
        all_schemas = db_core.get_schemas_db(user, password)

        # Filtrar esquemas del sistema
        system_schemas = ['information_schema', 'mysql', 'performance_schema', 'sys']
        project_schemas = [s for s in all_schemas if s not in system_schemas]

        config = get_config()

        # Asegurar que manager y cert_dev estén incluidos
        critical_schemas = [config.manager_schema, config.example_schema]

        print_info(f"Esquemas críticos: {', '.join(critical_schemas)}")
        print_info(f"Esquemas de proyectos: {len([s for s in project_schemas if s not in critical_schemas])}")
        print_success(f"Total de esquemas a respaldar: {len(project_schemas)}")

        return project_schemas

    except Exception as e:
        print_error(f"Error al obtener esquemas: {e}")
        return None


def create_backup(user, password, schemas, output_file):
    """Crea el backup usando mysqldump"""
    print_step("Creando backup de la base de datos")

    config = get_config()

    # Preparar comando mysqldump
    cmd = [
        'mysqldump',
        f'--host={config.host}',
        f'--port={config.port}',
        f'--user={user}',
        f'--password={password}',
        '--single-transaction',
        '--routines',
        '--triggers',
        '--events',
        '--add-drop-database',
        '--databases'
    ] + schemas

    print_info("Ejecutando mysqldump...")
    print_info(f"Esquemas: {', '.join(schemas)}")
    print_info(f"Archivo destino: {output_file}")

    try:
        # Ejecutar mysqldump y guardar en archivo
        with open(output_file, 'w', encoding='utf-8') as f:
            # Agregar comentario de cabecera
            f.write(f"-- HydroFlow Manager - Backup de Base de Datos\n")
            f.write(f"-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"-- Servidor: {config.host}:{config.port}\n")
            f.write(f"-- Esquemas: {', '.join(schemas)}\n")
            f.write(f"-- \n")
            f.write(f"-- Este backup incluye:\n")
            f.write(f"--   - Estructura de tablas\n")
            f.write(f"--   - Datos completos\n")
            f.write(f"--   - Triggers, procedures y events\n")
            f.write(f"-- \n")
            f.write(f"-- Para restaurar:\n")
            f.write(f"--   mysql -h HOST -P PORT -u USER -p < {Path(output_file).name}\n")
            f.write(f"-- \n\n")

            # Ejecutar mysqldump
            result = subprocess.run(
                cmd,
                stdout=f,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode != 0:
                print_error(f"Error en mysqldump: {result.stderr}")
                return False

        # Verificar tamaño del archivo
        file_size = Path(output_file).stat().st_size
        size_mb = file_size / (1024 * 1024)

        print_success(f"Backup creado exitosamente: {output_file}")
        print_success(f"Tamaño: {size_mb:.2f} MB")

        # Comprimir el backup
        print_info("\nComprimiendo backup...")
        try:
            import gzip
            import shutil

            gz_file = f"{output_file}.gz"
            with open(output_file, 'rb') as f_in:
                with gzip.open(gz_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            gz_size = Path(gz_file).stat().st_size / (1024 * 1024)
            compression_ratio = (1 - gz_size / size_mb) * 100

            print_success(f"Backup comprimido: {gz_file}")
            print_success(f"Tamaño comprimido: {gz_size:.2f} MB (reducción: {compression_ratio:.1f}%)")
            print_info("\n💡 Usa el archivo .gz para ahorrar espacio en disco")

        except Exception as e:
            print_warning(f"No se pudo comprimir: {e}")

        return True

    except subprocess.CalledProcessError as e:
        print_error(f"Error al ejecutar mysqldump: {e}")
        return False
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        return False


def restore_backup(user, password, backup_file):
    """Restaura un backup desde archivo"""
    print_step("Restaurando backup de la base de datos")

    # Verificar que el archivo existe
    if not Path(backup_file).exists():
        print_error(f"Archivo no encontrado: {backup_file}")
        return False

    # Si es .gz, descomprimir primero
    if backup_file.endswith('.gz'):
        print_info("Descomprimiendo backup...")
        import gzip
        sql_file = backup_file[:-3]  # Quitar .gz

        try:
            with gzip.open(backup_file, 'rb') as f_in:
                with open(sql_file, 'wb') as f_out:
                    f_out.write(f_in.read())
            print_success(f"Backup descomprimido: {sql_file}")
            backup_file = sql_file
        except Exception as e:
            print_error(f"Error al descomprimir: {e}")
            return False

    config = get_config()

    # Confirmar restauración
    print_warning("\n⚠️  ADVERTENCIA: Esta operación sobrescribirá los datos existentes")
    confirm = input("¿Desea continuar con la restauración? (escriba 'SI' para confirmar): ")

    if confirm != 'SI':
        print_info("Restauración cancelada")
        return False

    # Preparar comando mysql
    cmd = [
        'mysql',
        f'--host={config.host}',
        f'--port={config.port}',
        f'--user={user}',
        f'--password={password}'
    ]

    print_info(f"Restaurando desde: {backup_file}")

    try:
        with open(backup_file, 'r', encoding='utf-8') as f:
            result = subprocess.run(
                cmd,
                stdin=f,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode != 0:
                print_error(f"Error en restauración: {result.stderr}")
                return False

        print_success("Backup restaurado exitosamente")
        return True

    except Exception as e:
        print_error(f"Error al restaurar: {e}")
        return False


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Script de Backup/Restore para HydroFlow Manager',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--output', '-o',
                        help='Directorio de salida para el backup (default: ./backups)')
    parser.add_argument('--restore', '-r',
                        help='Restaurar desde un archivo de backup')

    args = parser.parse_args()

    print(f"""
{Colors.HEADER}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════╗
║         HYDROFLOW MANAGER - BACKUP/RESTORE DE BASE DE DATOS       ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
    """)

    # Obtener credenciales
    user, password = get_credentials()

    # Verificar conexión
    if not test_connection(user, password):
        print_error("\nNo se pudo conectar a la base de datos")
        sys.exit(1)

    # MODO RESTAURACIÓN
    if args.restore:
        if restore_backup(user, password, args.restore):
            print(f"""
{Colors.OKGREEN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════╗
║                  ✓ RESTAURACIÓN EXITOSA                           ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
            """)
        else:
            print(f"""
{Colors.FAIL}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════╗
║                  ✗ RESTAURACIÓN FALLIDA                           ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
            """)
            sys.exit(1)
        return

    # MODO BACKUP
    # Obtener esquemas
    schemas = get_all_schemas(user, password)
    if not schemas:
        print_error("\nNo se pudieron obtener los esquemas")
        sys.exit(1)

    # Preparar directorio y nombre de archivo
    output_dir = Path(args.output) if args.output else Path('./backups')
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_dir / f'hydroflow_backup_{timestamp}.sql'

    # Crear backup
    if create_backup(user, password, schemas, str(output_file)):
        print(f"""
{Colors.OKGREEN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════╗
║                  ✓ BACKUP COMPLETADO EXITOSAMENTE                 ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.ENDC}

{Colors.OKCYAN}📁 Archivo de backup:{Colors.ENDC}
   {output_file}
   {output_file}.gz (comprimido)

{Colors.OKCYAN}📝 Para restaurar en otra máquina:{Colors.ENDC}
   1. Copiar el archivo .gz a la nueva máquina
   2. Ejecutar: python crear_backup_bd.py --restore {Path(output_file).name}.gz

{Colors.OKCYAN}💾 Para restaurar en esta máquina:{Colors.ENDC}
   python crear_backup_bd.py --restore {output_file}.gz

{Colors.WARNING}⚠️  Importante:{Colors.ENDC}
   - Guardar este backup en un lugar seguro
   - Este backup contiene todos los datos del sistema
   - Incluye partes de trabajo y presupuestos
        """)
    else:
        print(f"""
{Colors.FAIL}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════╗
║                  ✗ BACKUP FALLIDO                                 ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
        """)
        sys.exit(1)


if __name__ == '__main__':
    main()
