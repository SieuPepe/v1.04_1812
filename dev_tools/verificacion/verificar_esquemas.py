#!/usr/bin/env python3
"""
Script para verificar qué esquemas existen en la base de datos
"""
import mysql.connector
import os
import sys
import getpass
from pathlib import Path

# Añadir directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))
from script.db_config import get_config

def get_credentials():
    """Solicita credenciales al usuario"""
    config = get_config()

    # Intentar obtener de variables de entorno primero
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')

    # Si no están en variables de entorno, solicitar al usuario
    if not user:
        user = input("Usuario MySQL: ").strip()

    if not password:
        password = getpass.getpass("Contraseña: ")

    return user, password

try:
    config = get_config()
    user, password = get_credentials()

    conexion = mysql.connector.connect(
        host=config.host,
        port=config.port,
        user=user,
        password=password
    )

    cursor = conexion.cursor()
    cursor.execute("SHOW DATABASES")
    schemas = [schema[0] for schema in cursor.fetchall()]

    print("=== TODOS LOS ESQUEMAS ===")
    for schema in sorted(schemas):
        print(f"  - {schema}")

    print("\n=== ESQUEMAS QUE EMPIEZAN CON 'cert' ===")
    cert_schemas = [s for s in schemas if s.startswith('cert')]
    for schema in sorted(cert_schemas):
        print(f"  - {schema}")

    cursor.close()
    conexion.close()

    print("\n✓ Verificación completada")

except Exception as e:
    print(f"✗ Error: {e}")
