#!/usr/bin/env python3
"""
Script para importar partes desde base de datos Microsoft Access
HydroFlow Manager v1.04 - FASE 1: PREPARACIÓN DE DATOS

REQUISITOS:
  - Linux: mdbtools (para .mdb) o conversión previa a CSV
  - Windows: pyodbc + Microsoft Access Database Engine

NOTA: Este script está preparado para múltiples escenarios:
  1. Lectura directa con pyodbc (Windows o Linux con drivers ODBC)
  2. Conversión previa a CSV usando mdbtools (Linux)
  3. Importación desde CSV exportado manualmente
"""
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import csv

# Añadir directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from script.db_connection import get_project_connection


def tiene_pyodbc():
    """Verifica si pyodbc está disponible."""
    try:
        import pyodbc
        return True
    except ImportError:
        return False


def tiene_mdbtools():
    """Verifica si mdbtools está instalado (Linux)."""
    try:
        result = subprocess.run(['which', 'mdb-tables'],
                              capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False


def listar_tablas_mdbtools(archivo_accdb):
    """Lista las tablas de un archivo Access usando mdbtools."""
    try:
        result = subprocess.run(
            ['mdb-tables', '-1', archivo_accdb],
            capture_output=True,
            text=True,
            check=True
        )
        tablas = [t.strip() for t in result.stdout.strip().split('\n') if t.strip()]
        return tablas
    except subprocess.CalledProcessError as e:
        print(f"Error al listar tablas: {e}")
        return []


def exportar_tabla_csv_mdbtools(archivo_accdb, tabla, archivo_csv):
    """Exporta una tabla de Access a CSV usando mdbtools."""
    try:
        with open(archivo_csv, 'w') as f:
            subprocess.run(
                ['mdb-export', archivo_accdb, tabla],
                stdout=f,
                check=True
            )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al exportar tabla {tabla}: {e}")
        return False


def importar_partes_desde_pyodbc(archivo_accdb, user, password, schema):
    """Importa partes usando pyodbc (requiere drivers ODBC)."""
    import pyodbc

    print("Conectando a Access con pyodbc...")

    # Construir connection string
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        f'DBQ={archivo_accdb};'
    )

    try:
        access_conn = pyodbc.connect(conn_str)
        access_cursor = access_conn.cursor()

        # Listar tablas
        print("\nTablas encontradas en Access:")
        tablas = [row.table_name for row in access_cursor.tables(tableType='TABLE')]
        for tabla in tablas:
            print(f"  - {tabla}")

        # TODO: Implementar mapeo e importación de datos
        print("\nNOTA: Importación desde pyodbc requiere implementación del mapeo específico.")
        print("Por favor, proporcione información sobre las tablas de origen en Access.")

        access_cursor.close()
        access_conn.close()

    except Exception as e:
        print(f"Error al conectar a Access: {e}")
        return False


def importar_partes_desde_csv(archivo_csv, user, password, schema):
    """
    Importa partes desde un archivo CSV.

    El CSV debe tener las siguientes columnas (adaptable):
    - codigo: Código del parte
    - descripcion: Descripción
    - estado: Estado del parte
    - red: Red
    - tipo_trabajo: Tipo de trabajo
    - cod_trabajo: Código de trabajo
    - municipio: Municipio
    - provincia: Provincia
    - fecha_inicio: Fecha de inicio (YYYY-MM-DD)
    - fecha_fin: Fecha de fin (YYYY-MM-DD)
    - presupuesto: Importe presupuestado
    - certificado: Importe certificado
    """
    print(f"Importando partes desde CSV: {archivo_csv}")

    try:
        with get_project_connection(user, password, schema) as conn:
            cursor = conn.cursor()

            # Leer CSV
            with open(archivo_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                filas = list(reader)

            print(f"Encontradas {len(filas)} filas en el CSV")
            print(f"Columnas: {', '.join(filas[0].keys() if filas else [])}")

            # TODO: Implementar inserción de datos
            # Este es un esqueleto que debe adaptarse según la estructura real del CSV

            for idx, fila in enumerate(filas[:5], 1):  # Mostrar primeras 5 filas
                print(f"\nFila {idx}:")
                for key, value in fila.items():
                    print(f"  {key}: {value}")

            print("\nNOTA: Importación desde CSV requiere mapeo específico de columnas.")
            print("Por favor, revise la estructura del CSV y adapte el script.")

            cursor.close()

    except Exception as e:
        print(f"Error al importar desde CSV: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Punto de entrada del script."""
    print("=" * 70)
    print("IMPORTAR PARTES DESDE MICROSOFT ACCESS")
    print("=" * 70)
    print()

    if len(sys.argv) < 2:
        print("Uso:")
        print(f"  {sys.argv[0]} <archivo_access.accdb> [metodo]")
        print()
        print("Métodos disponibles:")
        print("  auto     - Detectar automáticamente el mejor método (por defecto)")
        print("  pyodbc   - Usar pyodbc (requiere drivers ODBC)")
        print("  mdbtools - Usar mdbtools (Linux)")
        print("  csv      - Importar desde CSV exportado manualmente")
        print()
        print("Ejemplos:")
        print(f"  {sys.argv[0]} 'APLICACION CERTIFICACIONES UTE REDES URBIDE.accdb'")
        print(f"  {sys.argv[0]} database.accdb csv")
        print()
        sys.exit(1)

    archivo_accdb = sys.argv[1]
    metodo = sys.argv[2] if len(sys.argv) > 2 else 'auto'

    archivo_path = Path(archivo_accdb)
    if not archivo_path.exists():
        print(f"ERROR: El archivo '{archivo_accdb}' no existe")
        sys.exit(1)

    # Configuración de base de datos MySQL
    USER = 'root'
    PASSWORD = 'root'
    SCHEMA = 'cert_dev'

    print(f"Archivo Access: {archivo_path.name}")
    print(f"Esquema MySQL: {SCHEMA}")
    print(f"Método: {metodo}")
    print()

    # Determinar método a usar
    if metodo == 'auto':
        if tiene_pyodbc():
            metodo = 'pyodbc'
            print("Método detectado: pyodbc")
        elif tiene_mdbtools():
            metodo = 'mdbtools'
            print("Método detectado: mdbtools")
        else:
            print("ADVERTENCIA: No se detectó pyodbc ni mdbtools")
            print("Opciones:")
            print("  1. Instalar pyodbc: pip install pyodbc")
            print("  2. Instalar mdbtools (Linux): apt-get install mdbtools")
            print("  3. Exportar manualmente las tablas a CSV desde Access")
            print()
            metodo = input("¿Usar importación desde CSV? (s/n): ")
            if metodo.lower() == 's':
                metodo = 'csv'
            else:
                sys.exit(1)

    # Ejecutar importación según método
    if metodo == 'pyodbc':
        if not tiene_pyodbc():
            print("ERROR: pyodbc no está instalado")
            print("Instalar con: pip install pyodbc")
            sys.exit(1)
        importar_partes_desde_pyodbc(str(archivo_path), USER, PASSWORD, SCHEMA)

    elif metodo == 'mdbtools':
        if not tiene_mdbtools():
            print("ERROR: mdbtools no está instalado")
            print("Instalar con: apt-get install mdbtools")
            sys.exit(1)

        print("\nListando tablas...")
        tablas = listar_tablas_mdbtools(str(archivo_path))
        print(f"Tablas encontradas: {len(tablas)}")
        for tabla in tablas:
            print(f"  - {tabla}")

        print("\nNOTA: Para continuar, exporte las tablas necesarias a CSV:")
        print(f"  mdb-export '{archivo_path}' <nombre_tabla> > tabla.csv")
        print(f"Luego ejecute: {sys.argv[0]} tabla.csv csv")

    elif metodo == 'csv':
        # Si el archivo es .csv, usarlo directamente
        if archivo_path.suffix.lower() == '.csv':
            importar_partes_desde_csv(str(archivo_path), USER, PASSWORD, SCHEMA)
        else:
            print("ERROR: Para usar método CSV, proporcione un archivo .csv")
            sys.exit(1)

    else:
        print(f"ERROR: Método '{metodo}' no reconocido")
        sys.exit(1)


if __name__ == "__main__":
    main()
