#!/usr/bin/env python3
"""
Script maestro para ejecutar la FASE 1: PREPARACIÓN DE DATOS
HydroFlow Manager v1.04

Este script coordina todos los pasos de la FASE 1:
1. Verificar BBDD limpia → Crear backup_nopres_nopartes.sql
2. Cargar presupuesto → Crear backup_con_presupuesto.sql
3. Cargar partes (Access viejo) → Crear backup_completo_pruebas.sql
4. Testing completo de informes y comparación con los del cliente
"""
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Configuración
SCHEMA = 'proyecto_tipo'
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent


def print_header(titulo):
    """Imprime un encabezado formateado."""
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70 + "\n")


def print_step(numero, titulo):
    """Imprime un paso numerado."""
    print(f"\n{'─' * 70}")
    print(f"  PASO {numero}: {titulo}")
    print(f"{'─' * 70}\n")


def ejecutar_comando(comando, descripcion):
    """
    Ejecuta un comando y retorna True si tuvo éxito.

    Args:
        comando: Lista con el comando y argumentos
        descripcion: Descripción de lo que hace el comando

    Returns:
        bool: True si el comando tuvo éxito
    """
    print(f"Ejecutando: {descripcion}")
    print(f"Comando: {' '.join(comando)}\n")

    try:
        result = subprocess.run(
            comando,
            check=True,
            capture_output=False,
            text=True
        )
        print(f"✓ {descripcion} - EXITOSO\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {descripcion} - FALLÓ")
        print(f"Código de salida: {e.returncode}\n")
        return False
    except FileNotFoundError:
        print(f"✗ ERROR: Comando no encontrado")
        print(f"Verifica que el script existe: {comando[0]}\n")
        return False


def verificar_mysql_disponible():
    """Verifica que el servidor MySQL esté disponible."""
    print("Verificando disponibilidad de MySQL...")
    try:
        result = subprocess.run(
            ['python3', str(SCRIPT_DIR / 'verificar_db_limpia.py'), SCHEMA],
            capture_output=True,
            text=True
        )
        # Si el script se ejecuta sin error de conexión, MySQL está disponible
        if 'ERROR DE CONEXIÓN' in result.stderr:
            print("✗ MySQL no está disponible")
            print("Por favor, inicie el servidor MySQL antes de continuar.\n")
            return False
        print("✓ MySQL está disponible\n")
        return True
    except:
        print("✗ No se pudo verificar la disponibilidad de MySQL\n")
        return False


def paso1_verificar_y_backup_limpio():
    """PASO 1: Verificar BBDD limpia y crear backup."""
    print_step(1, "Verificar BBDD limpia y crear backup_nopres_nopartes.sql")

    # Verificar que la BBDD está limpia
    if not ejecutar_comando(
        ['python3', str(SCRIPT_DIR / 'verificar_db_limpia.py'), SCHEMA],
        "Verificar que la base de datos está limpia"
    ):
        print("ADVERTENCIA: La base de datos NO está limpia")
        respuesta = input("¿Desea continuar de todos modos? (s/n): ")
        if respuesta.lower() != 's':
            return False

    # Crear backup de BBDD limpia
    return ejecutar_comando(
        ['python3', str(SCRIPT_DIR / 'crear_backup.py'),
         'backup_nopres_nopartes', SCHEMA,
         'BBDD limpia sin presupuestos ni partes'],
        "Crear backup de base de datos limpia"
    )


def paso2_cargar_presupuesto():
    """PASO 2: Cargar presupuesto y crear backup."""
    print_step(2, "Cargar presupuesto y crear backup_con_presupuesto.sql")

    # Solicitar archivo de presupuesto
    print("Proporcione la ruta al archivo Excel con el presupuesto")
    print("El archivo debe contener las hojas: tbl_pres_capitulos, tbl_pres_precios,")
    print("tbl_pres_naturaleza, tbl_pres_unidades\n")

    archivo_presupuesto = input("Ruta al archivo Excel: ").strip()

    if not archivo_presupuesto:
        print("✗ No se proporcionó archivo de presupuesto")
        return False

    archivo_path = Path(archivo_presupuesto)
    if not archivo_path.exists():
        print(f"✗ El archivo no existe: {archivo_presupuesto}")
        return False

    # Cargar presupuesto
    if not ejecutar_comando(
        ['python3', str(SCRIPT_DIR / 'cargar_presupuesto.py'),
         str(archivo_path)],
        "Cargar presupuesto desde Excel"
    ):
        return False

    # Crear backup con presupuesto
    return ejecutar_comando(
        ['python3', str(SCRIPT_DIR / 'crear_backup.py'),
         'backup_con_presupuesto', SCHEMA,
         'BBDD con presupuesto cargado'],
        "Crear backup con presupuesto"
    )


def paso3_cargar_partes():
    """PASO 3: Cargar partes desde Access y crear backup."""
    print_step(3, "Cargar partes (Access viejo) y crear backup_completo_pruebas.sql")

    # Verificar si existe el archivo Access en la raíz
    archivo_access = ROOT_DIR / 'APLICACION CERTIFICACIONES UTE REDES URBIDE.accdb'

    if archivo_access.exists():
        print(f"Archivo Access encontrado: {archivo_access.name}\n")
        usar_este = input("¿Usar este archivo? (s/n): ")
        if usar_este.lower() != 's':
            archivo_access = None

    if not archivo_access or not archivo_access.exists():
        print("Proporcione la ruta al archivo Access (.accdb) con los partes\n")
        ruta = input("Ruta al archivo Access: ").strip()
        if not ruta:
            print("✗ No se proporcionó archivo Access")
            return False
        archivo_access = Path(ruta)
        if not archivo_access.exists():
            print(f"✗ El archivo no existe: {archivo_access}")
            return False

    # Cargar partes
    print("\nNOTA: La importación desde Access puede requerir configuración manual")
    print("dependiendo de la estructura del archivo Access.\n")

    if not ejecutar_comando(
        ['python3', str(SCRIPT_DIR / 'importar_partes_access.py'),
         str(archivo_access)],
        "Importar partes desde Access"
    ):
        print("\nSi la importación falló, puede:")
        print("1. Exportar las tablas necesarias desde Access a CSV")
        print("2. Ejecutar el script manualmente con más opciones")
        print("3. Revisar y adaptar el script de importación\n")
        respuesta = input("¿Desea continuar de todos modos? (s/n): ")
        if respuesta.lower() != 's':
            return False

    # Crear backup completo
    return ejecutar_comando(
        ['python3', str(SCRIPT_DIR / 'crear_backup.py'),
         'backup_completo_pruebas', SCHEMA,
         'BBDD completa con presupuestos y partes de prueba'],
        "Crear backup completo de pruebas"
    )


def paso4_testing_informes():
    """PASO 4: Testing completo de informes."""
    print_step(4, "Testing completo de informes y comparación")

    print("Este paso requiere:")
    print("  1. Ejecutar la aplicación")
    print("  2. Generar todos los informes disponibles")
    print("  3. Comparar con los informes del cliente")
    print("  4. Verificar que todos los datos se muestran correctamente")
    print()
    print("El testing debe incluir:")
    print("  - Informes de partes")
    print("  - Informes de certificaciones")
    print("  - Informes agrupados por red, municipio, tipo de trabajo, etc.")
    print("  - Verificación de cálculos y totales")
    print("  - Comparación con datos originales del Access")
    print()

    print("NOTA: Este paso debe realizarse manualmente")
    print("Ejecute la aplicación y verifique todos los informes")
    print()

    input("Presione Enter cuando haya completado el testing...")
    return True


def main():
    """Ejecuta la FASE 1 completa."""
    print_header("FASE 1: PREPARACIÓN DE DATOS")
    print("HydroFlow Manager v1.04")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Esquema: {SCHEMA}")
    print()

    # Verificar que MySQL está disponible
    if not verificar_mysql_disponible():
        print("\n✗ ABORTADO: MySQL no está disponible")
        print("\nAntes de continuar:")
        print("  1. Inicie el servidor MySQL")
        print("  2. Verifique la configuración de conexión")
        print("  3. Ejecute este script nuevamente")
        sys.exit(1)

    # Mostrar resumen de pasos
    print("Este script ejecutará los siguientes pasos:\n")
    print("  1. Verificar BBDD limpia → backup_nopres_nopartes.sql")
    print("  2. Cargar presupuesto → backup_con_presupuesto.sql")
    print("  3. Cargar partes → backup_completo_pruebas.sql")
    print("  4. Testing de informes (manual)")
    print()

    respuesta = input("¿Desea continuar? (s/n): ")
    if respuesta.lower() != 's':
        print("\nProceso cancelado por el usuario")
        sys.exit(0)

    # Ejecutar pasos
    exitos = 0
    fallos = 0

    if paso1_verificar_y_backup_limpio():
        exitos += 1
    else:
        fallos += 1
        print("✗ PASO 1 FALLÓ")
        respuesta = input("¿Continuar con el siguiente paso? (s/n): ")
        if respuesta.lower() != 's':
            sys.exit(1)

    if paso2_cargar_presupuesto():
        exitos += 1
    else:
        fallos += 1
        print("✗ PASO 2 FALLÓ")
        respuesta = input("¿Continuar con el siguiente paso? (s/n): ")
        if respuesta.lower() != 's':
            sys.exit(1)

    if paso3_cargar_partes():
        exitos += 1
    else:
        fallos += 1
        print("✗ PASO 3 FALLÓ")
        respuesta = input("¿Continuar con el siguiente paso? (s/n): ")
        if respuesta.lower() != 's':
            sys.exit(1)

    if paso4_testing_informes():
        exitos += 1
    else:
        fallos += 1

    # Resumen final
    print_header("RESUMEN DE FASE 1")
    print(f"Pasos exitosos: {exitos}/4")
    print(f"Pasos fallidos:  {fallos}/4")
    print()

    if fallos == 0:
        print("✓ FASE 1 COMPLETADA EXITOSAMENTE")
        print()
        print("Próximos pasos:")
        print("  - FASE 2: Limpieza del proyecto")
        print("  - FASE 3: Desarrollo de manuales")
        print("  - FASE 4: Empaquetado")
        print("  - FASE 5: Datos definitivos")
        print("  - FASE 6: Instalación Synology")
    else:
        print("⚠ FASE 1 COMPLETADA CON ERRORES")
        print()
        print("Revise los errores y vuelva a ejecutar los pasos fallidos")

    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
