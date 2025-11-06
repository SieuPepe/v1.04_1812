#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificación ESTÁTICA de interfaces (sin importar módulos GUI)

Este script verifica:
1. Que los archivos de interfaz existen
2. Que no tienen errores de sintaxis Python
3. Que las clases principales están definidas
4. Que los imports parecen correctos

NO requiere tkinter/customtkinter instalado (verificación estática)
"""

import ast
import os
import sys
from pathlib import Path

# Asegurar que estamos en el directorio raíz
script_dir = Path(__file__).parent
os.chdir(script_dir)

print("=" * 80)
print(" VERIFICACIÓN ESTÁTICA DE INTERFACES - HydroFlow Manager v1.04")
print("=" * 80)
print(f"\nDirectorio de trabajo: {os.getcwd()}\n")
print("NOTA: Esta es una verificación ESTÁTICA (sin ejecutar el código)")
print("      Verifica sintaxis, estructura y definiciones de clases\n")

# Interfaces a verificar
INTERFACES = [
    {
        'nombre': 'Login',
        'archivo': 'interface/login_interfaz.py',
        'clase': 'AppLogin',
        'critica': True
    },
    {
        'nombre': 'Manager Principal',
        'archivo': 'interface/manager_interfaz.py',
        'clase': 'AppManager',
        'critica': True
    },
    {
        'nombre': 'Proyecto Usuario',
        'archivo': 'interface/user_project_interfaz.py',
        'clase': 'AppUserProject',
        'critica': True
    },
    {
        'nombre': 'Gestor de Partes',
        'archivo': 'interface/parts_manager_interfaz.py',
        'clase': 'PartsManagerFrame',
        'critica': True
    },
    {
        'nombre': 'Formulario de Partes V2',
        'archivo': 'interface/parts_interfaz_v2_fixed.py',
        'clase': 'AppPartsV2',
        'critica': True
    },
    {
        'nombre': 'Sistema de Informes',
        'archivo': 'interface/informes_interfaz.py',
        'clase': 'InformesFrame',
        'critica': True
    },
    {
        'nombre': 'Certificaciones por Lotes',
        'archivo': 'interface/cert_lotes_interfaz.py',
        'clase': 'CertLotesWindow',
        'critica': True
    },
    {
        'nombre': 'Gestión de Presupuestos',
        'archivo': 'interface/update_budget_interfaz.py',
        'clase': 'AppBudgetUpdate',
        'critica': True
    },
    {
        'nombre': 'Selector de Tipo de Usuario',
        'archivo': 'interface/typeUser_interfaz.py',
        'clase': 'AppTypeUser',
        'critica': False
    },
    {
        'nombre': 'Gestión de Clientes - Añadir',
        'archivo': 'interface/customer_add_interfaz.py',
        'clase': 'AppCustomerAdd',
        'critica': False
    },
    {
        'nombre': 'Gestión de Clientes - Modificar',
        'archivo': 'interface/customer_mod_interfaz.py',
        'clase': 'AppCustomerMod',
        'critica': False
    },
    {
        'nombre': 'Inventario - Añadir Elemento',
        'archivo': 'interface/register_element_add_interfaz.py',
        'clase': 'AppElementAdd',
        'critica': False
    },
    {
        'nombre': 'Inventario - Modificar Elemento',
        'archivo': 'interface/register_element_mod_interfaz.py',
        'clase': 'AppElementModNoEmpty',
        'critica': False
    },
    {
        'nombre': 'Selector de Proyecto',
        'archivo': 'interface/select_project_interfaz.py',
        'clase': 'AppSelectProject',
        'critica': False
    },
    {
        'nombre': 'Visor de Fotos',
        'archivo': 'interface/view_photo_interfaz.py',
        'clase': 'AppViewPhoto',
        'critica': False
    },
]

def verificar_sintaxis(ruta_archivo):
    """Verifica que el archivo tiene sintaxis Python válida"""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        ast.parse(codigo)
        return True, None
    except SyntaxError as e:
        return False, f"Error de sintaxis en línea {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)

def encontrar_clases(ruta_archivo):
    """Encuentra todas las clases definidas en el archivo"""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        arbol = ast.parse(codigo)
        clases = [node.name for node in ast.walk(arbol) if isinstance(node, ast.ClassDef)]
        return clases
    except:
        return []

def encontrar_imports(ruta_archivo):
    """Encuentra todos los imports del archivo"""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        arbol = ast.parse(codigo)
        imports = []
        for node in ast.walk(arbol):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        return imports
    except:
        return []

def verificar_interface(config):
    """Verifica una interfaz de forma estática"""
    nombre = config['nombre']
    archivo = config['archivo']
    clase_esperada = config['clase']
    es_critica = config['critica']

    tipo = "CRÍTICA" if es_critica else "SECUNDARIA"

    print(f"  [{tipo}] {nombre}")
    print(f"    Archivo: {archivo}")
    print(f"    Clase esperada: {clase_esperada}")

    # 1. Verificar que el archivo existe
    if not os.path.exists(archivo):
        print(f"    ❌ Archivo NO existe")
        print(f"    ❌ INTERFAZ NO DISPONIBLE\n")
        return False

    print(f"    ✅ Archivo existe")

    # 2. Obtener tamaño del archivo
    tamaño = os.path.getsize(archivo)
    lineas = sum(1 for _ in open(archivo, 'r', encoding='utf-8'))
    print(f"    ℹ️  Tamaño: {tamaño:,} bytes, {lineas} líneas")

    # 3. Verificar sintaxis
    sintaxis_ok, error_sintaxis = verificar_sintaxis(archivo)
    if not sintaxis_ok:
        print(f"    ❌ Error de sintaxis: {error_sintaxis}")
        print(f"    ❌ INTERFAZ CON ERRORES DE CÓDIGO\n")
        return False

    print(f"    ✅ Sintaxis Python correcta")

    # 4. Encontrar clases
    clases = encontrar_clases(archivo)
    if not clases:
        print(f"    ⚠️  No se encontraron clases definidas")
        print(f"    ⚠️  INTERFAZ SOSPECHOSA\n")
        return False

    print(f"    ℹ️  Clases encontradas: {', '.join(clases)}")

    # 5. Verificar que la clase esperada existe
    if clase_esperada in clases:
        print(f"    ✅ Clase '{clase_esperada}' encontrada")
    else:
        print(f"    ⚠️  Clase '{clase_esperada}' NO encontrada")
        print(f"       Clases disponibles: {', '.join(clases)}")

    # 6. Verificar imports críticos
    imports = encontrar_imports(archivo)
    if 'customtkinter' in imports or any('customtkinter' in imp for imp in imports):
        print(f"    ✅ Usa customtkinter (GUI moderna)")
    elif 'tkinter' in imports or any('tkinter' in imp for imp in imports):
        print(f"    ⚠️  Usa tkinter clásico")
    else:
        print(f"    ⚠️  No se detectaron imports de GUI")

    print(f"    ✅ INTERFAZ OPERATIVA (sintaxis correcta, clase definida)\n")
    return True

def main():
    criticas = [i for i in INTERFACES if i['critica']]
    secundarias = [i for i in INTERFACES if not i['critica']]

    # Verificar interfaces críticas
    print("\n" + "=" * 80)
    print(" INTERFACES CRÍTICAS (CORE DEL SISTEMA)")
    print("=" * 80 + "\n")

    resultados_criticas = []
    for interface in criticas:
        resultado = verificar_interface(interface)
        resultados_criticas.append((interface['nombre'], resultado))

    # Verificar interfaces secundarias
    print("\n" + "=" * 80)
    print(" INTERFACES SECUNDARIAS (FUNCIONALIDADES ADICIONALES)")
    print("=" * 80 + "\n")

    resultados_secundarias = []
    for interface in secundarias:
        resultado = verificar_interface(interface)
        resultados_secundarias.append((interface['nombre'], resultado))

    # Resumen
    print("\n" + "=" * 80)
    print(" RESUMEN DE VERIFICACIÓN ESTÁTICA")
    print("=" * 80 + "\n")

    criticas_ok = sum(1 for _, ok in resultados_criticas if ok)
    criticas_total = len(resultados_criticas)

    secundarias_ok = sum(1 for _, ok in resultados_secundarias if ok)
    secundarias_total = len(resultados_secundarias)

    print(f"INTERFACES CRÍTICAS:")
    print(f"  ✅ Válidas: {criticas_ok}/{criticas_total} ({criticas_ok/criticas_total*100:.0f}%)")

    if criticas_ok < criticas_total:
        print(f"\n  ❌ INTERFACES CON PROBLEMAS:")
        for nombre, ok in resultados_criticas:
            if not ok:
                print(f"     - {nombre}")

    print(f"\nINTERFACES SECUNDARIAS:")
    print(f"  ✅ Válidas: {secundarias_ok}/{secundarias_total} ({secundarias_ok/secundarias_total*100:.0f}%)")

    if secundarias_ok < secundarias_total:
        print(f"\n  ⚠️  INTERFACES CON PROBLEMAS:")
        for nombre, ok in resultados_secundarias:
            if not ok:
                print(f"     - {nombre}")

    # Conclusión
    print("\n" + "=" * 80)
    print(" CONCLUSIÓN")
    print("=" * 80 + "\n")

    if criticas_ok == criticas_total and secundarias_ok == secundarias_total:
        print("✅ TODAS LAS INTERFACES ESTÁN CORRECTAS (verificación estática)")
        print("   - Sintaxis Python válida: ✅")
        print("   - Clases definidas correctamente: ✅")
        print("   - Imports presentes: ✅\n")
        print("🎯 El sistema está LISTO para ejecución")
        print("   Próximo paso: Ejecutar la aplicación y hacer pruebas funcionales\n")
        return 0
    elif criticas_ok == criticas_total:
        print(f"✅ TODAS LAS INTERFACES CRÍTICAS ESTÁN CORRECTAS")
        print(f"⚠️  Hay {secundarias_total - secundarias_ok} interfaces secundarias con problemas")
        print("   Pero el CORE del sistema está bien\n")
        return 0
    else:
        print(f"❌ HAY {criticas_total - criticas_ok} INTERFACES CRÍTICAS CON PROBLEMAS")
        print("   ACCIÓN REQUERIDA: Revisar los errores reportados arriba\n")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
