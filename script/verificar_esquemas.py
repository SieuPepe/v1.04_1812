#!/usr/bin/env python3
"""
Script para verificar qué esquemas existen en la base de datos
"""
import mysql.connector

try:
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user='root',
        password='Cretus2021*'
    )

    cursor = conexion.cursor()
    cursor.execute("SHOW DATABASES")
    schemas = [schema[0] for schema in cursor.fetchall()]

    print("=== TODOS LOS ESQUEMAS ===")
    for schema in sorted(schemas):
        print(f"  - {schema}")

    print("\n=== ESQUEMAS QUE EMPIEZAN CON 'cert' ===")
    cert_schemas = [s for s in schemas if s.startswith('cert')]
    for schema in sorted(cert_schemas):
        print(f"  - {schema}")

    cursor.close()
    conexion.close()

    print("\n✓ Verificación completada")

except Exception as e:
    print(f"✗ Error: {e}")
