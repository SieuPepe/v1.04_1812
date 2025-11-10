#!/usr/bin/env python3
"""
Script para verificar que las tablas de presupuesto y partes están vacías.
"""
import mysql.connector
import sys
import os
from pathlib import Path

# Agregar el directorio script al path para importar db_config
sys.path.insert(0, str(Path(__file__).parent))

try:
    from db_config import get_config
    USE_DB_CONFIG = True
except ImportError:
    USE_DB_CONFIG = False

def verificar_tablas_vacias(host, port, user, password, database):
    """Verifica que las tablas de presupuesto y partes estén vacías."""

    # Tablas a verificar
    tablas_presupuesto = [
        'tbl_presupuesto',
        'tbl_pres_certificacion',
        'tbl_proy_presupuesto'
    ]

    tablas_partes = [
        'tbl_partes',
        'tbl_partes_materiales',
        'tbl_partes_maquinaria',
        'tbl_partes_mano_obra'
    ]

    todas_tablas = tablas_presupuesto + tablas_partes

    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

        cursor = conn.cursor()

        print(f"\n{'='*70}")
        print(f"VERIFICANDO BASE DE DATOS: {database}")
        print(f"{'='*70}\n")

        tiene_datos = False

        for tabla in todas_tablas:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cursor.fetchone()[0]

                estado = "✓ VACÍA" if count == 0 else f"✗ TIENE {count} REGISTROS"
                print(f"  {tabla:<30} {estado}")

                if count > 0:
                    tiene_datos = True

            except mysql.connector.Error as e:
                print(f"  {tabla:<30} ⚠ ERROR: {e}")

        cursor.close()
        conn.close()

        print(f"\n{'='*70}")
        if tiene_datos:
            print("⚠ LA BASE DE DATOS CONTIENE DATOS EN ALGUNAS TABLAS")
            print("{'='*70}\n")
            return False
        else:
            print("✓ LA BASE DE DATOS ESTÁ LIMPIA (SIN PRESUPUESTOS NI PARTES)")
            print(f"{'='*70}\n")
            return True

    except mysql.connector.Error as e:
        print(f"\n✗ ERROR DE CONEXIÓN: {e}\n")
        print(f"Intentando conectar a: {host}:{port} como {user}")
        print(f"Base de datos: {database}\n")
        return False

if __name__ == "__main__":
    # Configuración desde variables de entorno o valores por defecto
    if USE_DB_CONFIG:
        config = get_config()
        HOST = config.host
        PORT = config.port
    else:
        HOST = os.getenv('DB_HOST', 'localhost')
        PORT = int(os.getenv('DB_PORT', '3307'))

    USER = os.getenv('DB_USER', 'root')
    PASSWORD = os.getenv('DB_PASSWORD', 'root')

    # Si se pasa un esquema como argumento, usarlo
    DATABASE = sys.argv[1] if len(sys.argv) > 1 else 'proyecto_tipo'

    resultado = verificar_tablas_vacias(HOST, PORT, USER, PASSWORD, DATABASE)
    sys.exit(0 if resultado else 1)
