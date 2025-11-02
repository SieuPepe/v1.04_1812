#!/usr/bin/env python3
"""
Script de diagnóstico para verificar por qué no se ven los cambios
"""

import sys
import os
import hashlib

print("=" * 70)
print("DIAGNÓSTICO DE INTERFAZ DE INFORMES")
print("=" * 70)

# 1. Verificar que estamos en el directorio correcto
print(f"\n1. Directorio actual: {os.getcwd()}")

# 2. Verificar que el archivo existe y su contenido
interface_file = "interface/informes_interfaz.py"
print(f"\n2. Verificando archivo: {interface_file}")

if os.path.exists(interface_file):
    with open(interface_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Hash del archivo para verificar versión
    file_hash = hashlib.md5(content.encode()).hexdigest()
    print(f"   ✓ Archivo existe")
    print(f"   - Tamaño: {len(content)} caracteres")
    print(f"   - Líneas: {len(content.splitlines())} líneas")
    print(f"   - Hash MD5: {file_hash}")

    # Buscar marcadores específicos de las mejoras
    print(f"\n3. Buscando marcadores de las mejoras UI:")

    markers = {
        "TreeView 12pt": "font=('Segoe UI', 12)",
        "Panel 280px": "width=280",
        "Scroll clasificaciones": "self.clasificaciones_container = customtkinter.CTkScrollableFrame",
        "Scroll filtros": "self.filtros_container = customtkinter.CTkScrollableFrame",
        "Padding 15px": "padx=15, pady=3",
    }

    for name, marker in markers.items():
        if marker in content:
            # Encontrar en qué línea está
            lines = content.splitlines()
            line_num = None
            for i, line in enumerate(lines, 1):
                if marker in line:
                    line_num = i
                    break
            print(f"   ✓ {name} - ENCONTRADO (línea {line_num})")
        else:
            print(f"   ✗ {name} - NO ENCONTRADO")
else:
    print(f"   ✗ Archivo NO existe en: {os.path.abspath(interface_file)}")
    sys.exit(1)

# 4. Verificar el archivo parts_manager
print(f"\n4. Verificando integración en parts_manager_interfaz.py:")
pm_file = "interface/parts_manager_interfaz.py"

if os.path.exists(pm_file):
    with open(pm_file, 'r', encoding='utf-8') as f:
        pm_content = f.read()

    checks = {
        "Import InformesFrame": "from interface.informes_interfaz import InformesFrame",
        "Método main_informes": "def main_informes(self):",
        "Botón Informes": "self.informes_button",
        "Frame informes": "self.informes_frame",
    }

    for name, marker in checks.items():
        if marker in pm_content:
            lines = pm_content.splitlines()
            line_num = None
            for i, line in enumerate(lines, 1):
                if marker in line:
                    line_num = i
                    break
            print(f"   ✓ {name} - ENCONTRADO (línea {line_num})")
        else:
            print(f"   ✗ {name} - NO ENCONTRADO")
else:
    print(f"   ✗ Archivo NO existe")

# 5. Verificar archivos .pyc en interface/
print(f"\n5. Verificando archivos de caché Python:")
cache_files = []
for root, dirs, files in os.walk("interface"):
    for file in files:
        if file.endswith('.pyc'):
            cache_files.append(os.path.join(root, file))

if cache_files:
    print(f"   ⚠ ENCONTRADOS {len(cache_files)} archivos .pyc en interface/")
    for cf in cache_files[:5]:  # Mostrar solo los primeros 5
        print(f"     - {cf}")
    if len(cache_files) > 5:
        print(f"     - ... y {len(cache_files) - 5} más")
    print(f"\n   ⚠ ESTOS ARCHIVOS PUEDEN ESTAR CAUSANDO EL PROBLEMA")
    print(f"   Ejecuta este comando para eliminarlos:")
    if os.name == 'nt':  # Windows
        print(f"   Get-ChildItem -Path interface -Recurse -Filter '*.pyc' | Remove-Item -Force")
    else:  # Linux/Mac
        print(f"   find interface -name '*.pyc' -delete")
else:
    print(f"   ✓ No hay archivos .pyc en interface/")

# 6. Verificar directorios __pycache__
print(f"\n6. Verificando directorios __pycache__:")
pycache_dirs = []
for root, dirs, files in os.walk("interface"):
    if "__pycache__" in dirs:
        pycache_dirs.append(os.path.join(root, "__pycache__"))

if pycache_dirs:
    print(f"   ⚠ ENCONTRADOS {len(pycache_dirs)} directorios __pycache__")
    for pd in pycache_dirs:
        print(f"     - {pd}")
    print(f"\n   ⚠ ESTOS DIRECTORIOS PUEDEN ESTAR CAUSANDO EL PROBLEMA")
    print(f"   Ejecuta este comando para eliminarlos:")
    if os.name == 'nt':  # Windows
        print(f"   Get-ChildItem -Path interface -Recurse -Directory -Filter '__pycache__' | Remove-Item -Recurse -Force")
    else:  # Linux/Mac
        print(f"   find interface -type d -name '__pycache__' -exec rm -rf {{}} +")
else:
    print(f"   ✓ No hay directorios __pycache__ en interface/")

# 7. Intentar importar el módulo
print(f"\n7. Intentando importar el módulo InformesFrame:")
sys.path.insert(0, os.getcwd())

try:
    import importlib
    import interface.informes_interfaz as inf_module

    # Forzar recarga
    importlib.reload(inf_module)

    print(f"   ✓ Módulo importado correctamente")
    print(f"   - Archivo módulo: {inf_module.__file__}")

    # Verificar atributos de la clase
    InformesFrame = inf_module.InformesFrame
    print(f"   - Clase InformesFrame disponible: {InformesFrame}")

except Exception as e:
    print(f"   ✗ Error al importar: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("RESUMEN DEL DIAGNÓSTICO")
print("=" * 70)

if cache_files or pycache_dirs:
    print("\n⚠️  PROBLEMA DETECTADO: Archivos de caché Python")
    print("\nEstos archivos están haciendo que Python use código antiguo.")
    print("\nSOLUCIÓN:")
    print("1. Cierra completamente la aplicación main.py")
    print("2. Ejecuta los comandos de limpieza mostrados arriba")
    print("3. Vuelve a ejecutar: python main.py")
    print("4. Navega a: Generador de Partes > Botón 'Informes' en el sidebar")
else:
    print("\n✓ No se detectaron archivos de caché")
    print("\nOtras posibles causas:")
    print("1. ¿Estás mirando la pestaña correcta?")
    print("   - NO es una pestaña arriba del contenido")
    print("   - ES un botón en el menú lateral izquierdo")
    print("2. ¿La aplicación muestra algún error al iniciar?")
    print("3. ¿Has ejecutado 'git merge' correctamente?")

print("\nPara más ayuda, proporciona:")
print("- Captura de pantalla de la interfaz que ves")
print("- Output de: git log --oneline -3")
print("- Este diagnóstico completo")
print("=" * 70)
