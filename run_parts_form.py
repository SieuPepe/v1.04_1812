#!/usr/bin/env python3
"""
Script de entrada para ejecutar el formulario de partes mejorado.
Este script asegura que los imports funcionen correctamente.
"""
import sys
import os

# Añadir el directorio raíz al path para que los imports funcionen
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Ahora importar la aplicación
from interface.parts_interfaz_v2_fixed import AppPartsV2

if __name__ == "__main__":
    # Credenciales de base de datos
    # IMPORTANTE: Cambiar estos valores según tu configuración
    USER = "root"
    PASSWORD = "NuevaPass!2025"
    SCHEMA = "cert_dev"

    # Crear y ejecutar la aplicación
    app = AppPartsV2(user=USER, password=PASSWORD, default_schema=SCHEMA)
    app.mainloop()
