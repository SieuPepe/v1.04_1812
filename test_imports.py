#!/usr/bin/env python3
"""
Test de verificación de imports - Módulo DB Refactorizado

Este script verifica que todos los módulos se importan correctamente
y que la configuración está funcionando.

Ejecutar desde PyCharm:
    Click derecho → Run 'test_imports'

Ejecutar desde terminal:
    python test_imports.py
"""

import sys
from pathlib import Path

# Asegurarse de que el directorio actual está en el path
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

def test_base_modules():
    """Prueba 1: Importar módulos base"""
    print("=" * 70)
    print("Prueba 1: Importando módulos base...")
    print("=" * 70)

    try:
        from script.db_config import get_config
        from script.db_connection import get_connection, get_manager_connection, get_project_connection
        print("✅ Módulos base importados correctamente")
        print(f"   - db_config.get_config: {get_config}")
        print(f"   - db_connection.get_connection: {get_connection}")
        print(f"   - db_connection.get_manager_connection: {get_manager_connection}")
        print(f"   - db_connection.get_project_connection: {get_project_connection}")
        return True
    except ImportError as e:
        print(f"❌ Error importando módulos base: {e}")
        return False

def test_configuration():
    """Prueba 2: Verificar configuración"""
    print("\n" + "=" * 70)
    print("Prueba 2: Verificando configuración...")
    print("=" * 70)

    try:
        from script.db_config import get_config
        config = get_config()

        print(f"✅ Configuración cargada correctamente:")
        print(f"   - Host: {config.host}")
        print(f"   - Puerto: {config.port}")
        print(f"   - Schema Manager: {config.manager_schema}")
        print(f"   - Schema Ejemplo: {config.example_schema}")

        # Verificar que los valores no están vacíos
        assert config.host, "Host no debe estar vacío"
        assert config.port, "Puerto no debe estar vacío"
        assert config.manager_schema, "Manager schema no debe estar vacío"

        return True
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def test_modulo_db_imports():
    """Prueba 3: Importar desde modulo_db (compatibilidad)"""
    print("\n" + "=" * 70)
    print("Prueba 3: Importando desde modulo_db (compatibilidad)...")
    print("=" * 70)

    try:
        from script.modulo_db import (
            # Core functions
            login_db,
            get_schemas_db,
            create_schemas_db,
            # Project functions
            add_project_item,
            mod_project_item,
            # Partes functions
            add_parte_with_code,
            list_partes
        )
        print("✅ Funciones importadas desde modulo_db correctamente")
        print(f"   - login_db: {login_db}")
        print(f"   - add_project_item: {add_project_item}")
        print(f"   - add_parte_with_code: {add_parte_with_code}")
        return True
    except ImportError as e:
        print(f"❌ Error importando desde modulo_db: {e}")
        return False

def test_mysql_connector():
    """Prueba 4: Verificar mysql.connector"""
    print("\n" + "=" * 70)
    print("Prueba 4: Verificando mysql.connector...")
    print("=" * 70)

    try:
        import mysql.connector
        print(f"✅ mysql.connector instalado correctamente")
        print(f"   - Versión: {mysql.connector.__version__}")
        return True
    except ImportError:
        print("❌ mysql.connector no está instalado")
        print("\n   Para instalar, ejecuta:")
        print("   pip install mysql-connector-python")
        return False

def test_all_functions_available():
    """Prueba 5: Verificar que todas las funciones están disponibles"""
    print("\n" + "=" * 70)
    print("Prueba 5: Verificando disponibilidad de funciones...")
    print("=" * 70)

    try:
        from script import modulo_db

        # Contar funciones disponibles
        all_items = dir(modulo_db)
        functions = [item for item in all_items if not item.startswith('_')]

        print(f"✅ Total de funciones disponibles: {len(functions)}")

        # Verificar algunas funciones clave de cada módulo
        key_functions = [
            'login_db', 'get_schemas_db',  # db_core
            'add_project_item', 'add_customer_item',  # db_projects
            'add_parte_with_code', 'list_partes'  # db_partes
        ]

        missing = [f for f in key_functions if f not in functions]

        if missing:
            print(f"⚠️  Funciones clave faltantes: {missing}")
            return False
        else:
            print("✅ Todas las funciones clave están disponibles:")
            for func in key_functions:
                print(f"   - {func}")
            return True

    except Exception as e:
        print(f"❌ Error verificando funciones: {e}")
        return False

def test_environment_variables():
    """Prueba 6: Verificar variables de entorno (opcional)"""
    print("\n" + "=" * 70)
    print("Prueba 6: Verificando variables de entorno...")
    print("=" * 70)

    import os

    env_vars = ['DB_HOST', 'DB_PORT', 'DB_MANAGER_SCHEMA', 'DB_EXAMPLE_SCHEMA']
    found = []
    missing = []

    for var in env_vars:
        value = os.getenv(var)
        if value:
            found.append(f"{var}={value}")
        else:
            missing.append(var)

    if found:
        print(f"✅ Variables de entorno encontradas:")
        for var in found:
            print(f"   - {var}")

    if missing:
        print(f"\nℹ️  Variables de entorno no definidas (usando valores por defecto):")
        for var in missing:
            print(f"   - {var}")
        print("\n   Para configurar variables de entorno:")
        print("   1. Copia .env.example a .env")
        print("   2. Edita .env con tus valores")
        print("   3. Instala python-dotenv: pip install python-dotenv")

    return True  # No es crítico

def main():
    """Ejecutar todas las pruebas"""
    print("\n" + "=" * 70)
    print("VERIFICACIÓN DE CONFIGURACIÓN - MÓDULO DB REFACTORIZADO")
    print("=" * 70)

    results = []

    # Ejecutar pruebas
    results.append(("Módulos base", test_base_modules()))
    results.append(("Configuración", test_configuration()))
    results.append(("Compatibilidad modulo_db", test_modulo_db_imports()))
    results.append(("MySQL Connector", test_mysql_connector()))
    results.append(("Funciones disponibles", test_all_functions_available()))
    results.append(("Variables de entorno", test_environment_variables()))

    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN DE PRUEBAS")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")

    print("\n" + "=" * 70)
    print(f"Resultado: {passed}/{total} pruebas pasadas")

    if passed == total:
        print("✅ CONFIGURACIÓN COMPLETA - TODO FUNCIONANDO CORRECTAMENTE")
    elif passed >= total - 1:
        print("⚠️  CONFIGURACIÓN CASI COMPLETA - Revisa las advertencias arriba")
    else:
        print("❌ CONFIGURACIÓN INCOMPLETA - Revisa los errores arriba")

    print("=" * 70)

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
