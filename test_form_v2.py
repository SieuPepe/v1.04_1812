#!/usr/bin/env python3
"""
Script para probar el nuevo formulario de partes mejorado.
Ejecutar desde el directorio raíz: python test_form_v2.py
"""
import sys
from pathlib import Path

# Añadir directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from interface.parts_interfaz_v2_fixed import AppPartsV2

if __name__ == "__main__":
    # Ajusta estas credenciales
    USER = "root"
    PASSWORD = "NuevaPass!2025"
    SCHEMA = "cert_dev"

    print("=" * 60)
    print("  FORMULARIO DE PARTES MEJORADO - VERSIÓN CORREGIDA")
    print("=" * 60)
    print(f"Schema: {SCHEMA}")
    print(f"Usuario: {USER}")
    print()
    print("Cargando formulario...")
    print()

    app = AppPartsV2(USER, PASSWORD, SCHEMA)
    app.mainloop()
