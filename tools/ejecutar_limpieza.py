#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script wrapper para ejecutar la limpieza de partes sin interacción.
"""
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from script.limpiar_partes import limpiar_datos_partes

if __name__ == '__main__':
    import getpass

    # Obtener credenciales de forma segura
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD')
    schema = os.getenv('DB_SCHEMA', 'cert_dev')

    # Si no hay password en variable de entorno, solicitar
    if not password:
        password = getpass.getpass(f"Password for {user}: ")

    print(f"\nEjecutando limpieza en esquema: {schema}")
    print(f"Usuario: {user}")
    print("\nNOTA: La operación continuará automáticamente (modo no interactivo)")

    # Ejecutar limpieza directamente
    exito = limpiar_datos_partes(user, password, schema)

    sys.exit(0 if exito else 1)
