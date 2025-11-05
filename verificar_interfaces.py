#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificación completa de todas las interfaces del sistema HydroFlow Manager

Este script verifica:
1. Que las interfaces principales pueden importarse sin errores
2. Que las clases principales existen
3. Que no hay problemas de sintaxis
4. Que las dependencias están correctas
"""

import sys
import os
import importlib
from pathlib import Path

# Asegurar que estamos en el directorio raíz
script_dir = Path(__file__).parent
os.chdir(script_dir)
sys.path.insert(0, str(script_dir))

print("=" * 80)
print(" VERIFICACIÓN COMPLETA DE INTERFACES - HydroFlow Manager v1.04")
print("=" * 80)
print(f"\nDirectorio de trabajo: {os.getcwd()}\n")

# Interfaces a verificar (en orden de importancia)
INTERFACES_CRITICAS = [
    {
        'nombre': 'Login',
        'modulo': 'interface.login_interfaz',
        'clase': 'AppLogin',
        'descripcion': 'Interfaz de inicio de sesión'
    },
    {
        'nombre': 'Manager Principal',
        'modulo': 'interface.manager_interfaz',
        'clase': 'AppManager',
        'descripcion': 'Interfaz principal de gestión del sistema'
    },
    {
        'nombre': 'Proyecto Usuario',
        'modulo': 'interface.user_project_interfaz',
        'clase': 'AppUserProject',
        'descripcion': 'Interfaz principal de proyecto para usuarios'
    },
    {
        'nombre': 'Gestor de Partes',
        'modulo': 'interface.parts_manager_interfaz',
        'clase': 'PartsManagerFrame',
        'descripcion': 'Interfaz de gestión de partes de trabajo'
    },
    {
        'nombre': 'Formulario de Partes V2',
        'modulo': 'interface.parts_interfaz_v2_fixed',
        'clase': 'AppPartsV2',
        'descripcion': 'Formulario completo de partes (con provincias)'
    },
    {
        'nombre': 'Sistema de Informes',
        'modulo': 'interface.informes_interfaz',
        'clase': 'InformesFrame',
        'descripcion': 'Sistema de informes dinámicos'
    },
    {
        'nombre': 'Certificaciones por Lotes',
        'modulo': 'interface.cert_lotes_interfaz',
        'clase': 'CertLotesWindow',
        'descripcion': 'Interfaz de certificaciones masivas'
    },
    {
        'nombre': 'Gestión de Presupuestos',
        'modulo': 'interface.update_budget_interfaz',
        'clase': 'AppBudgetUpdate',
        'descripcion': 'Interfaz de actualización de presupuestos'
    },
]

INTERFACES_SECUNDARIAS = [
    {
        'nombre': 'Selector de Tipo de Usuario',
        'modulo': 'interface.typeUser_interfaz',
        'clase': 'AppTypeUser',
        'descripcion': 'Selector de tipo de usuario después del login'
    },
    {
        'nombre': 'Gestión de Clientes',
        'modulo': 'interface.customer_add_interfaz',
        'clase': 'AppCustomerAdd',
        'descripcion': 'Añadir nuevo cliente'
    },
    {
        'nombre': 'Modificar Cliente',
        'modulo': 'interface.customer_mod_interfaz',
        'clase': 'AppCustomerMod',
        'descripcion': 'Modificar datos de cliente'
    },
    {
        'nombre': 'Añadir Elemento de Inventario',
        'modulo': 'interface.register_element_add_interfaz',
        'clase': 'AppElementAdd',
        'descripcion': 'Añadir nuevo elemento al inventario'
    },
    {
        'nombre': 'Modificar Elemento de Inventario',
        'modulo': 'interface.register_element_mod_interfaz',
        'clase': 'AppElementModNoEmpty',
        'descripcion': 'Modificar elemento existente del inventario'
    },
    {
        'nombre': 'Selector de Proyecto',
        'modulo': 'interface.select_project_interfaz',
        'clase': 'AppSelectProject',
        'descripcion': 'Selector de proyecto para trabajar'
    },
    {
        'nombre': 'Visor de Fotos',
        'modulo': 'interface.view_photo_interfaz',
        'clase': 'AppViewPhoto',
        'descripcion': 'Visor de fotografías'
    },
]

def verificar_interface(config):
    """Verifica una interfaz específica"""
    nombre = config['nombre']
    modulo_nombre = config['modulo']
    clase_nombre = config['clase']
    descripcion = config['descripcion']

    print(f"  {nombre}")
    print(f"    Descripción: {descripcion}")
    print(f"    Módulo: {modulo_nombre}")
    print(f"    Clase: {clase_nombre}")

    try:
        # Intentar importar el módulo
        modulo = importlib.import_module(modulo_nombre)
        print(f"    ✅ Módulo importado correctamente")

        # Verificar que la clase existe
        if hasattr(modulo, clase_nombre):
            clase = getattr(modulo, clase_nombre)
            print(f"    ✅ Clase {clase_nombre} encontrada")
            print(f"    ✅ INTERFAZ OPERATIVA")
            return True
        else:
            print(f"    ❌ Clase {clase_nombre} NO encontrada en el módulo")
            print(f"    ❌ INTERFAZ CON PROBLEMAS")
            return False

    except ImportError as e:
        print(f"    ❌ Error al importar módulo: {e}")
        print(f"    ❌ INTERFAZ NO DISPONIBLE")
        return False
    except Exception as e:
        print(f"    ❌ Error inesperado: {e}")
        print(f"    ❌ INTERFAZ CON PROBLEMAS")
        return False
    finally:
        print()  # Línea en blanco

def main():
    resultados_criticas = []
    resultados_secundarias = []

    # Verificar interfaces críticas
    print("\n" + "=" * 80)
    print(" INTERFACES CRÍTICAS (CORE DEL SISTEMA)")
    print("=" * 80 + "\n")

    for interface in INTERFACES_CRITICAS:
        resultado = verificar_interface(interface)
        resultados_criticas.append((interface['nombre'], resultado))

    # Verificar interfaces secundarias
    print("\n" + "=" * 80)
    print(" INTERFACES SECUNDARIAS (FUNCIONALIDADES ADICIONALES)")
    print("=" * 80 + "\n")

    for interface in INTERFACES_SECUNDARIAS:
        resultado = verificar_interface(interface)
        resultados_secundarias.append((interface['nombre'], resultado))

    # Resumen
    print("\n" + "=" * 80)
    print(" RESUMEN DE VERIFICACIÓN")
    print("=" * 80 + "\n")

    # Interfaces críticas
    criticas_ok = sum(1 for _, ok in resultados_criticas if ok)
    criticas_total = len(resultados_criticas)

    print(f"INTERFACES CRÍTICAS:")
    print(f"  ✅ Operativas: {criticas_ok}/{criticas_total}")

    if criticas_ok < criticas_total:
        print(f"\n  ❌ INTERFACES CRÍTICAS CON PROBLEMAS:")
        for nombre, ok in resultados_criticas:
            if not ok:
                print(f"     - {nombre}")

    # Interfaces secundarias
    secundarias_ok = sum(1 for _, ok in resultados_secundarias if ok)
    secundarias_total = len(resultados_secundarias)

    print(f"\nINTERFACES SECUNDARIAS:")
    print(f"  ✅ Operativas: {secundarias_ok}/{secundarias_total}")

    if secundarias_ok < secundarias_total:
        print(f"\n  ⚠️  INTERFACES SECUNDARIAS CON PROBLEMAS:")
        for nombre, ok in resultados_secundarias:
            if not ok:
                print(f"     - {nombre}")

    # Conclusión
    print("\n" + "=" * 80)
    print(" CONCLUSIÓN")
    print("=" * 80 + "\n")

    if criticas_ok == criticas_total:
        print("✅ TODAS LAS INTERFACES CRÍTICAS ESTÁN OPERATIVAS")
        print("   El sistema está LISTO PARA PRODUCCIÓN desde el punto de vista de interfaces\n")

        if secundarias_ok == secundarias_total:
            print("✅ TODAS LAS INTERFACES SECUNDARIAS TAMBIÉN ESTÁN OPERATIVAS")
            print("   El sistema tiene FUNCIONALIDAD COMPLETA\n")
        else:
            print(f"⚠️  Algunas interfaces secundarias tienen problemas ({secundarias_total - secundarias_ok})")
            print("   Pero el CORE del sistema funciona correctamente\n")

        return 0
    else:
        print(f"❌ HAY {criticas_total - criticas_ok} INTERFACES CRÍTICAS CON PROBLEMAS")
        print("   El sistema NO está listo para producción\n")
        print("   ACCIÓN REQUERIDA: Revisar y corregir las interfaces marcadas arriba\n")

        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
