#!/usr/bin/env python3
"""
Script de entrada para ejecutar el formulario de partes simple.
Este script asegura que los imports funcionen correctamente.
"""
import sys
import os

# Añadir el directorio raíz al path para que los imports funcionen
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Ahora importar la aplicación
from interface.parts_interfaz import AppParts

if __name__ == "__main__":
    # Credenciales de base de datos
    # IMPORTANTE: Cambiar estos valores según tu configuración
    USER = "root"
    PASSWORD = "NuevaPass!2025"
    SCHEMA = "cert_dev"

    # Crear y ejecutar la aplicación
    app = AppParts(user=USER, password=PASSWORD, default_schema=SCHEMA)
    app.mainloop()
