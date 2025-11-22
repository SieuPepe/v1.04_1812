#!/usr/bin/env python3
"""
HydroFlow Manager v2.0 - Script de Preparación de Base de Datos

Este script ayuda a preparar la base de datos para producción:
1. Crear backups de esquemas limpios (proyecto_tipo y manager)
2. Validar que proyecto_tipo no tiene datos de prueba
3. Generar reportes de validación
4. Preparar scripts SQL para instalación

IMPORTANTE: Ejecutar ANTES de compilar y distribuir

Requisitos:
- MySQL Client (mysqldump) instalado y en PATH
- Archivo .env configurado con credenciales
- Acceso a base de datos con permisos de lectura

Uso:
    python dev_tools/preparacion/preparar_bd_produccion.py
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import shutil

# Agregar directorio raíz al path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Cargar .env
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=project_root / '.env')
except ImportError:
    print("⚠️  python-dotenv no instalado, intentando cargar .env manualmente...")
    env_file = project_root / '.env'
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()


# ============================================================================
# Utilidades
# ============================================================================

def print_header(message):
    """Imprime encabezado de sección"""
    print()
    print("=" * 80)
    print(message)
    print("=" * 80)


def print_success(message):
    """Imprime mensaje de éxito"""
    print(f"✓ {message}")


def print_error(message):
    """Imprime mensaje de error"""
    print(f"✗ {message}")


def print_warning(message):
    """Imprime mensaje de advertencia"""
    print(f"⚠ {message}")


def print_info(message):
    """Imprime mensaje informativo"""
    print(f"ℹ {message}")


def run_mysql_command(host, port, user, password, command, database=None):
    """
    Ejecuta un comando MySQL y retorna el resultado.

    Args:
        host: Host de MySQL
        port: Puerto de MySQL
        user: Usuario de MySQL
        password: Contraseña
        command: Comando SQL a ejecutar
        database: Base de datos opcional

    Returns:
        tuple: (success, output)
    """
    cmd = [
        'mysql',
        '-h', host,
        '-P', str(port),
        '-u', user,
        f'-p{password}',
        '-N',  # No column names
        '-e', command
    ]

    if database:
        cmd.extend([database])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()
    except FileNotFoundError:
        return False, "mysql command not found in PATH"


def run_mysqldump(host, port, user, password, database, output_file, structure_only=False):
    """
    Ejecuta mysqldump para crear un backup.

    Args:
        host: Host de MySQL
        port: Puerto de MySQL
        user: Usuario
        password: Contraseña
        database: Base de datos a respaldar
        output_file: Archivo de salida
        structure_only: Si True, solo exporta estructura (sin datos)

    Returns:
        bool: True si exitoso
    """
    cmd = [
        'mysqldump',
        '-h', host,
        '-P', str(port),
        '-u', user,
        f'-p{password}',
        '--single-transaction',
        '--routines',
        '--triggers',
        '--events',
        '--databases', database,
        '--result-file', str(output_file)
    ]

    if structure_only:
        cmd.append('--no-data')

    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Error en mysqldump: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        print_error("mysqldump not found in PATH")
        return False


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Función principal"""

    # ========================================================================
    # PASO 1: Verificar requisitos
    # ========================================================================

    print_header("PASO 1: Verificación de Requisitos")

    # Verificar que estamos en el directorio raíz
    if not (project_root / 'main.py').exists():
        print_error("Este script debe ejecutarse desde el directorio raíz del proyecto")
        return 1
    print_success("Directorio correcto")

    # Verificar .env
    if not (project_root / '.env').exists():
        print_error("Archivo .env no encontrado")
        print_info("  Cree el archivo .env desde .env.example")
        print_info("  Consulte INSTALACION.md para más detalles")
        return 1
    print_success("Archivo .env encontrado")

    # Cargar configuración
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_MANAGER_SCHEMA = os.getenv('DB_MANAGER_SCHEMA', 'manager')
    DB_EXAMPLE_SCHEMA = os.getenv('DB_EXAMPLE_SCHEMA', 'proyecto_tipo')

    # Validar credenciales
    if not DB_USER or not DB_PASSWORD:
        print_error("DB_USER o DB_PASSWORD no configurados en .env")
        return 1
    print_success("Credenciales cargadas desde .env")

    # Verificar comandos MySQL
    if not shutil.which('mysql'):
        print_error("mysql client no encontrado en PATH")
        return 1
    print_success(f"mysql client disponible: {shutil.which('mysql')}")

    if not shutil.which('mysqldump'):
        print_error("mysqldump no encontrado en PATH")
        return 1
    print_success(f"mysqldump disponible: {shutil.which('mysqldump')}")

    # ========================================================================
    # PASO 2: Verificar conexión
    # ========================================================================

    print_header("PASO 2: Verificación de Conexión a Base de Datos")

    print_info(f"Conectando a {DB_HOST}:{DB_PORT} como {DB_USER}...")

    success, output = run_mysql_command(
        DB_HOST, DB_PORT, DB_USER, DB_PASSWORD,
        "SELECT VERSION();"
    )

    if not success:
        print_error("No se pudo conectar a la base de datos")
        print_info("  Verifique las credenciales en .env")
        print_info("  Verifique que MySQL esté ejecutándose")
        return 1

    print_success("Conexión exitosa")
    print_info(f"  Versión de MySQL: {output}")

    # ========================================================================
    # PASO 3: Validar esquemas
    # ========================================================================

    print_header("PASO 3: Validación de Esquemas")

    # Verificar manager
    print_info(f"Verificando esquema '{DB_MANAGER_SCHEMA}'...")
    success, output = run_mysql_command(
        DB_HOST, DB_PORT, DB_USER, DB_PASSWORD,
        f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{DB_MANAGER_SCHEMA}';"
    )

    if not success or DB_MANAGER_SCHEMA not in output:
        print_error(f"Esquema '{DB_MANAGER_SCHEMA}' no existe")
        print_info("  Cree el esquema manager antes de continuar")
        return 1
    print_success(f"Esquema '{DB_MANAGER_SCHEMA}' encontrado")

    # Verificar proyecto_tipo
    print_info(f"Verificando esquema '{DB_EXAMPLE_SCHEMA}'...")
    success, output = run_mysql_command(
        DB_HOST, DB_PORT, DB_USER, DB_PASSWORD,
        f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{DB_EXAMPLE_SCHEMA}';"
    )

    if not success or DB_EXAMPLE_SCHEMA not in output:
        print_error(f"Esquema '{DB_EXAMPLE_SCHEMA}' no existe")
        print_info("  Cree el esquema proyecto_tipo antes de continuar")
        return 1
    print_success(f"Esquema '{DB_EXAMPLE_SCHEMA}' encontrado")

    # ========================================================================
    # PASO 4: Validar datos
    # ========================================================================

    print_header("PASO 4: Validación de Datos en proyecto_tipo")

    print_info(f"Verificando que '{DB_EXAMPLE_SCHEMA}' no tiene datos de prueba...")

    tablas_datos = [
        'tbl_partes',
        'tbl_part_presupuesto',
        'tbl_part_certificacion'
    ]

    datos_encontrados = False
    conteos = {}

    for tabla in tablas_datos:
        success, output = run_mysql_command(
            DB_HOST, DB_PORT, DB_USER, DB_PASSWORD,
            f"SELECT COUNT(*) FROM {DB_EXAMPLE_SCHEMA}.{tabla};"
        )

        if success:
            count = int(output.strip())
            conteos[tabla] = count
            if count > 0:
                print_warning(f"Tabla '{tabla}' tiene {count} registros")
                datos_encontrados = True
            else:
                print_success(f"Tabla '{tabla}' está vacía")

    if datos_encontrados:
        print_warning(f"Se encontraron datos de prueba en '{DB_EXAMPLE_SCHEMA}'")
        print_info("  RECOMENDACIÓN: Limpie los datos antes de crear el backup")
        print_info("  Las tablas de catálogos (tbl_pres_precios, etc.) pueden tener datos")
        print()
        continuar = input("¿Desea continuar de todos modos? (s/n): ")
        if continuar.lower() != 's':
            print_info("Operación cancelada por el usuario")
            return 0
    else:
        print_success(f"Esquema '{DB_EXAMPLE_SCHEMA}' está limpio (sin datos transaccionales)")

    # ========================================================================
    # PASO 5: Crear directorio de backups
    # ========================================================================

    print_header("PASO 5: Preparación de Directorio de Backups")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = project_root / 'backups' / 'produccion' / timestamp

    backup_path.mkdir(parents=True, exist_ok=True)
    print_success(f"Directorio creado: {backup_path}")

    # ========================================================================
    # PASO 6: Backup de manager
    # ========================================================================

    print_header("PASO 6: Backup de Esquema 'manager'")

    manager_backup = backup_path / 'manager_estructura_y_datos.sql'

    print_info(f"Creando backup de '{DB_MANAGER_SCHEMA}' (estructura + datos)...")
    print_info(f"  Destino: {manager_backup}")

    if not run_mysqldump(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD,
                        DB_MANAGER_SCHEMA, manager_backup):
        return 1

    file_size = manager_backup.stat().st_size / 1024
    print_success(f"Backup creado: {manager_backup} ({file_size:.2f} KB)")

    # ========================================================================
    # PASO 7: Backup de proyecto_tipo
    # ========================================================================

    print_header("PASO 7: Backup de Esquema 'proyecto_tipo'")

    # Backup completo
    proyecto_tipo_backup = backup_path / 'proyecto_tipo_completo.sql'

    print_info(f"Creando backup de '{DB_EXAMPLE_SCHEMA}' (estructura + datos de catálogo)...")
    print_info(f"  Destino: {proyecto_tipo_backup}")

    if not run_mysqldump(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD,
                        DB_EXAMPLE_SCHEMA, proyecto_tipo_backup):
        return 1

    file_size = proyecto_tipo_backup.stat().st_size / 1024
    print_success(f"Backup creado: {proyecto_tipo_backup} ({file_size:.2f} KB)")

    # Backup solo estructura
    proyecto_tipo_estructura = backup_path / 'proyecto_tipo_solo_estructura.sql'

    print_info("Creando backup de estructura (sin datos)...")
    print_info(f"  Destino: {proyecto_tipo_estructura}")

    if not run_mysqldump(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD,
                        DB_EXAMPLE_SCHEMA, proyecto_tipo_estructura,
                        structure_only=True):
        return 1

    file_size = proyecto_tipo_estructura.stat().st_size / 1024
    print_success(f"Backup de estructura creado: {proyecto_tipo_estructura} ({file_size:.2f} KB)")

    # ========================================================================
    # PASO 8: Generar reporte
    # ========================================================================

    print_header("PASO 8: Generación de Reporte de Validación")

    reporte_path = backup_path / 'reporte_validacion.txt'

    print_info("Generando reporte de validación...")

    # Obtener info de catálogos
    tablas_catalogo = ['tbl_pres_precios']
    conteos_catalogo = {}

    for tabla in tablas_catalogo:
        success, output = run_mysql_command(
            DB_HOST, DB_PORT, DB_USER, DB_PASSWORD,
            f"SELECT COUNT(*) FROM {DB_EXAMPLE_SCHEMA}.{tabla};"
        )
        if success:
            conteos_catalogo[tabla] = int(output.strip())

    # Crear reporte
    reporte = f"""================================================================================
REPORTE DE VALIDACIÓN - PREPARACIÓN PARA PRODUCCIÓN
================================================================================

Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Usuario: {os.getenv('USER', os.getenv('USERNAME', 'desconocido'))}
Host BD: {DB_HOST}:{DB_PORT}

================================================================================
ESQUEMAS PROCESADOS
================================================================================

1. ESQUEMA MANAGER: {DB_MANAGER_SCHEMA}
   - Backup completo: manager_estructura_y_datos.sql
   - Contiene: Tabla de proyectos y configuración global

2. ESQUEMA PROYECTO_TIPO: {DB_EXAMPLE_SCHEMA}
   - Backup completo: proyecto_tipo_completo.sql
   - Backup estructura: proyecto_tipo_solo_estructura.sql
   - Contiene: Estructura de tablas + catálogos de precios

================================================================================
VALIDACIÓN DE DATOS
================================================================================

Tablas transaccionales en '{DB_EXAMPLE_SCHEMA}':

"""

    for tabla in tablas_datos:
        count = conteos.get(tabla, 0)
        status = "✓ OK (vacía)" if count == 0 else f"⚠ ADVERTENCIA ({count} registros)"
        reporte += f"  - {tabla}: {status}\n"

    reporte += f"""
================================================================================
CATÁLOGOS EN '{DB_EXAMPLE_SCHEMA}'
================================================================================

"""

    for tabla, count in conteos_catalogo.items():
        reporte += f"  - {tabla}: {count} registros\n"

    reporte += f"""
================================================================================
ARCHIVOS GENERADOS
================================================================================

  - {manager_backup.name}
  - {proyecto_tipo_backup.name}
  - {proyecto_tipo_estructura.name}
  - {reporte_path.name}

================================================================================
PRÓXIMOS PASOS
================================================================================

1. Revisar este reporte de validación

2. Si hay advertencias, considere limpiar datos de prueba:
   - DELETE FROM tbl_partes WHERE codigo LIKE 'TEST%';
   - DELETE FROM tbl_part_presupuesto WHERE parte_id NOT IN (SELECT id FROM tbl_partes);
   - DELETE FROM tbl_part_certificacion WHERE parte_id NOT IN (SELECT id FROM tbl_partes);

3. Si todo está correcto, puede proceder con la compilación:
   - Windows: .\\build.ps1
   - Linux/Mac: python -m PyInstaller HydroFlowManager.spec
   - Consulte: docs/COMPILACION_Y_DISTRIBUCION.md

4. Los backups están listos para:
   - Instalación en nuevos servidores
   - Recuperación de desastres
   - Distribución con la aplicación

================================================================================
FIN DEL REPORTE
================================================================================
"""

    with open(reporte_path, 'w', encoding='utf-8') as f:
        f.write(reporte)

    print_success(f"Reporte generado: {reporte_path}")

    # ========================================================================
    # Resumen final
    # ========================================================================

    print()
    print("=" * 80)
    print("PREPARACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 80)
    print()
    print_info(f"Backups creados en: {backup_path}")
    print_info("  - manager_estructura_y_datos.sql")
    print_info("  - proyecto_tipo_completo.sql")
    print_info("  - proyecto_tipo_solo_estructura.sql")
    print_info("  - reporte_validacion.txt")
    print()
    print_info("Revise el reporte de validación para verificar que todo está correcto")
    print()
    print_success("Proceso completado. La base de datos está lista para producción.")
    print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
