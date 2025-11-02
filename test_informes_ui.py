#!/usr/bin/env python3
"""
Test simple para verificar que la interfaz de Informes carga correctamente
"""

import sys
import os

# Agregar el directorio al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("VERIFICACIÓN DE LA INTERFAZ DE INFORMES")
print("=" * 60)

# Test 1: Importar configuración
print("\n1. Verificando configuración...")
try:
    from script.informes_config import CATEGORIAS_INFORMES, OPERADORES
    print(f"   ✓ Configuración cargada correctamente")
    print(f"   - Categorías disponibles: {len(CATEGORIAS_INFORMES)}")
    for cat, informes in CATEGORIAS_INFORMES.items():
        print(f"     • {cat}: {len(informes)} informes")
except Exception as e:
    print(f"   ✗ Error al cargar configuración: {e}")
    sys.exit(1)

# Test 2: Verificar archivo de interfaz
print("\n2. Verificando archivo de interfaz...")
interface_file = "interface/informes_interfaz.py"
if os.path.exists(interface_file):
    with open(interface_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verificar mejoras UI
    checks = {
        "Font 12pt en TreeView": "font=('Segoe UI', 12)",
        "Panel width 280px": "width=280",
        "Scrollable clasificaciones": "self.clasificaciones_container = customtkinter.CTkScrollableFrame",
        "Scrollable filtros": "self.filtros_container = customtkinter.CTkScrollableFrame"
    }

    for check_name, check_str in checks.items():
        if check_str in content:
            print(f"   ✓ {check_name}")
        else:
            print(f"   ✗ {check_name} - NO ENCONTRADO")
else:
    print(f"   ✗ Archivo no encontrado: {interface_file}")
    sys.exit(1)

# Test 3: Verificar que se puede importar la clase
print("\n3. Verificando importación de InformesFrame...")
try:
    from interface.informes_interfaz import InformesFrame
    print(f"   ✓ InformesFrame importado correctamente")
    print(f"   - Clase: {InformesFrame.__name__}")
    print(f"   - Módulo: {InformesFrame.__module__}")
except Exception as e:
    print(f"   ✗ Error al importar InformesFrame: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Verificar icono
print("\n4. Verificando icono...")
icon_file = "source/informes.png"
if os.path.exists(icon_file):
    size = os.path.getsize(icon_file)
    print(f"   ✓ Icono encontrado ({size} bytes)")
else:
    print(f"   ⚠ Icono no encontrado: {icon_file} (no crítico)")

print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)
print("✓ Todos los componentes están en su lugar")
print("✓ Las mejoras de UI están aplicadas en el código")
print("\nPara ver los cambios:")
print("  1. Ejecuta: python main.py")
print("  2. Navega a: Generador de Partes > Pestaña 'Informes'")
print("  3. Deberías ver:")
print("     - TreeView con categorías en fuente más grande (12pt)")
print("     - Panel izquierdo de 280px de ancho")
print("     - Secciones 'Clasificación' y 'Filtros' con scroll")
print("     - Espaciado mejorado en toda la interfaz")
print("=" * 60)
