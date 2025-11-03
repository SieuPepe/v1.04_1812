#!/usr/bin/env python3
"""
Script para analizar el archivo Access y extraer información de informes/queries
"""

import os
import sys

accdb_file = "APLICACION CERTIFICACIONES UTE REDES URBIDE.accdb"

print(f"Analizando archivo: {accdb_file}")
print(f"Tamaño: {os.path.getsize(accdb_file) / (1024*1024):.2f} MB")
print()

# Intentar con access_parser
try:
    from access_parser import AccessParser

    parser = AccessParser(accdb_file)

    print("=== TABLAS ===")
    tables = parser.get_tables()
    for table in tables:
        print(f"  - {table}")

    print()
    print("=== QUERIES/CONSULTAS ===")
    queries = parser.get_queries()
    for query in queries:
        print(f"  - {query}")

except Exception as e:
    print(f"Error con access_parser: {e}")

# Método alternativo: usar comtypes (Windows) o msaccessdb
try:
    import pypyodbc

    conn_str = f'Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={os.path.abspath(accdb_file)};'
    conn = pypyodbc.connect(conn_str)
    cursor = conn.cursor()

    print("=== TABLAS (pypyodbc) ===")
    for row in cursor.tables(tableType='TABLE'):
        print(f"  - {row.table_name}")

    print()
    print("=== QUERIES (pypyodbc) ===")
    for row in cursor.tables(tableType='VIEW'):
        print(f"  - {row.table_name}")

    conn.close()

except Exception as e:
    print(f"Error con pypyodbc: {e}")

# Como último recurso, leer el archivo binario y buscar patrones
print("\n=== ANÁLISIS BINARIO (búsqueda de nombres) ===")
print("Buscando nombres de objetos en el archivo...")

try:
    with open(accdb_file, 'rb') as f:
        content = f.read()

    # Buscar strings que parezcan nombres de informes/queries
    # En Access, los nombres suelen estar cerca de ciertos marcadores

    # Convertir a string (ignorando errores)
    text = content.decode('latin-1', errors='ignore')

    # Buscar patrones comunes
    keywords = ['Informe', 'Consulta', 'Query', 'Report', 'Form', 'Formulario']

    lines = text.split('\x00')
    potential_names = set()

    for line in lines:
        line_clean = line.strip()
        if len(line_clean) > 3 and len(line_clean) < 100:
            for keyword in keywords:
                if keyword.lower() in line_clean.lower():
                    potential_names.add(line_clean)

    print(f"\nNombres potenciales encontrados ({len(potential_names)}):")
    for name in sorted(potential_names)[:50]:  # Limitar a 50
        if len(name) < 80:  # Ignorar líneas muy largas
            print(f"  ? {name[:80]}")

except Exception as e:
    print(f"Error en análisis binario: {e}")

print("\n" + "="*80)
print("NOTA: Para un análisis completo, se recomienda abrir el archivo en")
print("Microsoft Access y revisar manualmente los informes/consultas disponibles.")
print("="*80)
