#!/usr/bin/env python3
"""
Script para diagnosticar la conectividad con MySQL.

Este script intenta conectarse a MySQL con diferentes configuraciones
y proporciona información detallada sobre el problema si falla.
"""
import mysql.connector
import os
import sys
from pathlib import Path

# Agregar el directorio script al path para importar db_config
sys.path.insert(0, str(Path(__file__).parent))

try:
    from db_config import get_config
    USE_DB_CONFIG = True
except ImportError:
    USE_DB_CONFIG = False


def print_header(text):
    """Imprime un encabezado formateado."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def check_connection(host, port, user, password, database=None):
    """
    Intenta conectarse a MySQL y reporta el resultado.

    Args:
        host: Host del servidor MySQL
        port: Puerto del servidor MySQL
        user: Usuario de MySQL
        password: Contraseña de MySQL
        database: Base de datos opcional

    Returns:
        bool: True si la conexión fue exitosa
    """
    print(f"Intentando conectar a MySQL...")
    print(f"  Host: {host}")
    print(f"  Puerto: {port}")
    print(f"  Usuario: {user}")
    print(f"  Contraseña: {'*' * len(password) if password else '(vacía)'}")
    if database:
        print(f"  Base de datos: {database}")
    print()

    try:
        # Intentar conexión
        if database:
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
        else:
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password
            )

        # Obtener información del servidor
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]

        print("✓ CONEXIÓN EXITOSA")
        print(f"  Versión de MySQL: {version}")

        # Listar bases de datos
        cursor.execute("SHOW DATABASES")
        databases = [row[0] for row in cursor.fetchall()]
        print(f"  Bases de datos disponibles: {', '.join(databases)}")

        cursor.close()
        conn.close()

        return True

    except mysql.connector.Error as err:
        print("✗ ERROR DE CONEXIÓN")
        print(f"  Tipo de error: {type(err).__name__}")
        print(f"  Mensaje: {err}")
        print()

        # Diagnóstico según el tipo de error
        error_str = str(err)
        if "Can't connect" in error_str or "Connection refused" in error_str:
            print("POSIBLES CAUSAS:")
            print("  1. El servidor MySQL no está ejecutándose")
            print("  2. MySQL está escuchando en un puerto diferente")
            print("  3. El firewall está bloqueando la conexión")
            print()
            print("SOLUCIONES:")
            print("  • En Windows, inicie MySQL desde:")
            print("    - Services (services.msc)")
            print("    - XAMPP Control Panel")
            print("    - MySQL Workbench")
            print("  • Verifique que MySQL esté escuchando en el puerto correcto")

        elif "Access denied" in error_str:
            print("POSIBLES CAUSAS:")
            print("  1. Usuario o contraseña incorrectos")
            print("  2. El usuario no tiene permisos")
            print()
            print("SOLUCIONES:")
            print("  • Verifique las credenciales de MySQL")
            print("  • Configure las variables de entorno DB_USER y DB_PASSWORD")

        elif "Unknown database" in error_str:
            print("POSIBLES CAUSAS:")
            print("  1. La base de datos no existe")
            print()
            print("SOLUCIONES:")
            print("  • Cree la base de datos primero")
            print(f"  • Ejecute: CREATE DATABASE {database};")

        return False


def main():
    """Ejecuta el diagnóstico de conectividad."""
    print_header("DIAGNÓSTICO DE CONECTIVIDAD MYSQL")

    # Obtener configuración
    if USE_DB_CONFIG:
        print("Usando configuración centralizada (db_config.py)")
        config = get_config()
        host = config.host
        port = config.port
    else:
        print("Usando variables de entorno o valores por defecto")
        host = os.getenv('DB_HOST', 'localhost')
        port = int(os.getenv('DB_PORT', '3307'))

    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', 'root')

    print()

    # Test 1: Conexión básica sin base de datos
    print_header("TEST 1: Conexión básica a MySQL")
    if not check_connection(host, port, user, password):
        print("\n✗ No se puede conectar al servidor MySQL")
        print("\nPor favor, corrija los problemas anteriores antes de continuar.")
        return False

    # Test 2: Conexión a base de datos proyecto_tipo
    print_header("TEST 2: Conexión a base de datos 'proyecto_tipo'")
    database = 'proyecto_tipo'
    if not check_connection(host, port, user, password, database):
        print(f"\n⚠ El servidor MySQL está disponible, pero la base de datos '{database}' no existe")
        print(f"\nPara crear la base de datos, ejecute:")
        print(f"  mysql -u {user} -p{password} -e \"CREATE DATABASE {database};\"")
        return False

    # Si llegamos aquí, todo está bien
    print_header("RESULTADO FINAL")
    print("✓ MySQL está correctamente configurado y disponible")
    print(f"✓ La base de datos '{database}' está accesible")
    print()
    print("Puede ejecutar el script de preparación de datos sin problemas.")

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nDiagnóstico interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
