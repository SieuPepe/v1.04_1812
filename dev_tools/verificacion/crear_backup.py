#!/usr/bin/env python3
"""
Script para crear backups de la base de datos MySQL
HydroFlow Manager v2.0 - FASE 1: PREPARACIÓN DE DATOS

Este script crea backups usando Python + mysql.connector (no requiere mysqldump)
Usa la configuración centralizada de db_config.py
"""
import sys
import os
import getpass
from datetime import datetime
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from script.db_config import get_config

# Configuración usando valores centralizados
config = get_config()
HOST = config.host
PORT = config.port
USER = 'root'
PASSWORD = None  # Se solicitará si no se proporciona
SCHEMA = 'cert_dev'  # Esquema por defecto
BACKUP_DIR = Path(__file__).parent.parent / 'backup'


def solicitar_credenciales():
    """
    Solicita credenciales al usuario si no están configuradas.

    Returns:
        tuple: (user, password)
    """
    user = input(f"Usuario de MySQL [{USER}]: ").strip() or USER
    password = getpass.getpass(f"Contraseña para {user}@{HOST}:{PORT}: ")
    return user, password


def crear_backup_python(schema, nombre_backup, descripcion="", user=None, password=None):
    """
    Crea un backup de un esquema MySQL usando Python puro (sin mysqldump).

    Args:
        schema: Nombre del esquema a respaldar
        nombre_backup: Nombre del archivo de backup (sin extensión)
        descripcion: Descripción opcional del backup
        user: Usuario MySQL (None = solicitar)
        password: Contraseña MySQL (None = solicitar)

    Returns:
        bool: True si el backup fue exitoso, False en caso contrario
    """
    try:
        import mysql.connector
        from mysql.connector import Error
    except ImportError:
        print("ERROR: mysql-connector-python no está instalado")
        print("Instale con: pip install mysql-connector-python")
        return False

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

    # Solicitar credenciales si no se proporcionaron
    if user is None or password is None:
        user, password = solicitar_credenciales()
        print()

    connection = None
    try:
        # Conectar a MySQL
        print("Conectando a MySQL...")
        connection = mysql.connector.connect(
            host=HOST,
            port=PORT,
            user=user,
            password=password,
            database=schema
        )
        cursor = connection.cursor()

        # Crear archivo de backup
        print("Generando backup...")
        with open(backup_file, 'w', encoding='utf-8') as f:
            # Encabezado del backup
            f.write(f"-- MySQL Backup\n")
            f.write(f"-- Esquema: {schema}\n")
            f.write(f"-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            if descripcion:
                f.write(f"-- Descripción: {descripcion}\n")
            f.write(f"-- Generado por: crear_backup.py (Python)\n")
            f.write("\n")
            f.write("SET NAMES utf8mb4;\n")
            f.write("SET FOREIGN_KEY_CHECKS = 0;\n")
            f.write("\n")

            # Obtener lista de tablas
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            print(f"  Tablas encontradas: {len(tables)}")

            # Exportar estructura y datos de cada tabla
            for table_name in tables:
                print(f"  - Exportando: {table_name}")

                # Estructura de la tabla
                f.write(f"\n-- Estructura de tabla: {table_name}\n")
                f.write(f"DROP TABLE IF EXISTS `{table_name}`;\n")

                cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
                create_table = cursor.fetchone()[1]
                f.write(f"{create_table};\n\n")

                # Datos de la tabla
                cursor.execute(f"SELECT * FROM `{table_name}`")
                rows = cursor.fetchall()

                if rows:
                    f.write(f"-- Datos de tabla: {table_name}\n")

                    # Obtener nombres de columnas
                    cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
                    columns = [col[0] for col in cursor.fetchall()]
                    columns_str = ", ".join([f"`{col}`" for col in columns])

                    # Insertar datos en lotes de 100 filas
                    batch_size = 100
                    for i in range(0, len(rows), batch_size):
                        batch = rows[i:i + batch_size]
                        f.write(f"INSERT INTO `{table_name}` ({columns_str}) VALUES\n")

                        values_list = []
                        for row in batch:
                            # Convertir cada valor a string SQL apropiado
                            values = []
                            for value in row:
                                if value is None:
                                    values.append("NULL")
                                elif isinstance(value, (int, float)):
                                    values.append(str(value))
                                elif isinstance(value, bytes):
                                    # Para BLOB/BINARY, usar formato hexadecimal
                                    values.append(f"0x{value.hex()}")
                                else:
                                    # Para strings, escapar comillas y usar comillas simples
                                    escaped = str(value).replace("\\", "\\\\").replace("'", "\\'")
                                    values.append(f"'{escaped}'")
                            values_list.append(f"({', '.join(values)})")

                        f.write(",\n".join(values_list))
                        f.write(";\n\n")

                    print(f"    {len(rows)} filas exportadas")

            # Exportar vistas
            cursor.execute("""
                SELECT TABLE_NAME
                FROM information_schema.VIEWS
                WHERE TABLE_SCHEMA = %s
            """, (schema,))
            views = cursor.fetchall()

            if views:
                print(f"  Vistas encontradas: {len(views)}")
                f.write("\n-- Vistas\n")
                for view in views:
                    view_name = view[0]
                    print(f"  - Exportando vista: {view_name}")
                    f.write(f"\nDROP VIEW IF EXISTS `{view_name}`;\n")
                    cursor.execute(f"SHOW CREATE VIEW `{view_name}`")
                    create_view = cursor.fetchone()[1]
                    f.write(f"{create_view};\n")

            # Exportar procedimientos almacenados
            cursor.execute("""
                SELECT ROUTINE_NAME
                FROM information_schema.ROUTINES
                WHERE ROUTINE_SCHEMA = %s AND ROUTINE_TYPE = 'PROCEDURE'
            """, (schema,))
            procedures = cursor.fetchall()

            if procedures:
                print(f"  Procedimientos encontrados: {len(procedures)}")
                f.write("\n-- Procedimientos almacenados\n")
                f.write("DELIMITER $$\n\n")
                for proc in procedures:
                    proc_name = proc[0]
                    print(f"  - Exportando procedimiento: {proc_name}")
                    f.write(f"DROP PROCEDURE IF EXISTS `{proc_name}`$$\n")
                    cursor.execute(f"SHOW CREATE PROCEDURE `{proc_name}`")
                    create_proc = cursor.fetchone()[2]  # [0]=Procedure, [1]=sql_mode, [2]=Create Procedure
                    f.write(f"{create_proc}$$\n\n")
                f.write("DELIMITER ;\n")

            # Exportar funciones
            cursor.execute("""
                SELECT ROUTINE_NAME
                FROM information_schema.ROUTINES
                WHERE ROUTINE_SCHEMA = %s AND ROUTINE_TYPE = 'FUNCTION'
            """, (schema,))
            functions = cursor.fetchall()

            if functions:
                print(f"  Funciones encontradas: {len(functions)}")
                f.write("\n-- Funciones\n")
                f.write("DELIMITER $$\n\n")
                for func in functions:
                    func_name = func[0]
                    print(f"  - Exportando función: {func_name}")
                    f.write(f"DROP FUNCTION IF EXISTS `{func_name}`$$\n")
                    cursor.execute(f"SHOW CREATE FUNCTION `{func_name}`")
                    create_func = cursor.fetchone()[2]
                    f.write(f"{create_func}$$\n\n")
                f.write("DELIMITER ;\n")

            # Exportar triggers
            cursor.execute("""
                SELECT TRIGGER_NAME
                FROM information_schema.TRIGGERS
                WHERE TRIGGER_SCHEMA = %s
            """, (schema,))
            triggers = cursor.fetchall()

            if triggers:
                print(f"  Triggers encontrados: {len(triggers)}")
                f.write("\n-- Triggers\n")
                f.write("DELIMITER $$\n\n")
                for trig in triggers:
                    trig_name = trig[0]
                    print(f"  - Exportando trigger: {trig_name}")
                    f.write(f"DROP TRIGGER IF EXISTS `{trig_name}`$$\n")
                    cursor.execute(f"SHOW CREATE TRIGGER `{trig_name}`")
                    create_trig = cursor.fetchone()[2]  # [0]=Trigger, [1]=sql_mode, [2]=SQL Original Statement
                    f.write(f"{create_trig}$$\n\n")
                f.write("DELIMITER ;\n")

            # Pie del backup
            f.write("\nSET FOREIGN_KEY_CHECKS = 1;\n")
            f.write(f"-- Fin del backup\n")

        cursor.close()

        # Verificar que se creó el archivo
        if not backup_file.exists():
            print("ERROR: El archivo de backup no se creó")
            return False

        # Mostrar tamaño del backup
        size_mb = backup_file.stat().st_size / (1024 * 1024)
        print(f"\n✓ Backup creado exitosamente")
        print(f"  Tamaño: {size_mb:.2f} MB")
        print(f"  Ruta: {backup_file}")
        print("=" * 70)
        print()

        return True

    except Error as e:
        print(f"\nERROR DE MySQL: {e}")
        return False
    except Exception as e:
        print(f"\nERROR inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if connection and connection.is_connected():
            connection.close()


def crear_backup(schema, nombre_backup, descripcion=""):
    """
    Función de compatibilidad que llama a crear_backup_python.

    Args:
        schema: Nombre del esquema a respaldar
        nombre_backup: Nombre del archivo de backup (sin extensión)
        descripcion: Descripción opcional del backup

    Returns:
        bool: True si el backup fue exitoso, False en caso contrario
    """
    return crear_backup_python(schema, nombre_backup, descripcion)


def main():
    """Punto de entrada del script."""
    if len(sys.argv) < 2:
        print("Uso:")
        print(f"  {sys.argv[0]} <nombre_backup> [schema] [descripcion]")
        print()
        print("Ejemplos:")
        print(f"  {sys.argv[0]} backup_nopres_nopartes cert_dev 'BBDD limpia sin presupuestos ni partes'")
        print(f"  {sys.argv[0]} backup_con_presupuesto cert_dev 'BBDD con presupuesto cargado'")
        print(f"  {sys.argv[0]} backup_completo_pruebas cert_dev 'BBDD completa con presupuestos y partes'")
        sys.exit(1)

    nombre_backup = sys.argv[1]
    schema = sys.argv[2] if len(sys.argv) > 2 else SCHEMA
    descripcion = sys.argv[3] if len(sys.argv) > 3 else ""

    exito = crear_backup(schema, nombre_backup, descripcion)
    sys.exit(0 if exito else 1)


if __name__ == "__main__":
    main()
