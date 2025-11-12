#!/usr/bin/env python3
"""
Script para aplicar la corrección de decimales en la base de datos.

Este script aplica las modificaciones a la base de datos para convertir
todos los campos DOUBLE y FLOAT a DECIMAL(10,2), garantizando precisión
de 2 decimales en todos los campos numéricos monetarios y de cantidad.
"""

import mysql.connector
from mysql.connector import Error
import getpass
import os


def aplicar_script_sql(host: str, port: int, database: str, user: str, password: str, script_path: str) -> bool:
    """
    Aplica un script SQL a la base de datos.

    Args:
        host: Host de la base de datos
        port: Puerto de la base de datos
        database: Nombre de la base de datos
        user: Usuario de la base de datos
        password: Contraseña
        script_path: Ruta al archivo SQL

    Returns:
        True si se aplicó correctamente
    """
    try:
        # Conectar a la base de datos
        print(f"Conectando a {host}:{port}/{database}...")
        conn = mysql.connector.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )

        if not conn.is_connected():
            print("✗ No se pudo conectar a la base de datos")
            return False

        print("✓ Conectado correctamente\n")

        # Leer el script SQL
        if not os.path.exists(script_path):
            print(f"✗ No se encontró el archivo SQL: {script_path}")
            return False

        print(f"Leyendo script SQL: {script_path}")
        with open(script_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # Dividir por sentencias (separadas por ;)
        sentencias = [s.strip() for s in sql_script.split(';') if s.strip() and not s.strip().startswith('--')]

        cursor = conn.cursor()
        total_sentencias = len(sentencias)
        ejecutadas = 0
        errores = 0

        print(f"\nEjecutando {total_sentencias} sentencias SQL...\n")
        print("-" * 80)

        for i, sentencia in enumerate(sentencias, 1):
            # Saltar comentarios y sentencias vacías
            if sentencia.strip().startswith('/*') or not sentencia.strip():
                continue

            # Extraer el nombre de la tabla si es un ALTER TABLE
            tabla_nombre = ""
            if "ALTER TABLE" in sentencia.upper():
                try:
                    parts = sentencia.split()
                    tabla_idx = next(i for i, word in enumerate(parts) if word.upper() == "TABLE")
                    tabla_nombre = parts[tabla_idx + 1].strip('`')
                except:
                    tabla_nombre = "desconocida"

            try:
                print(f"[{i}/{total_sentencias}] Procesando: {tabla_nombre if tabla_nombre else 'Consulta SQL'}...")

                cursor.execute(sentencia)
                conn.commit()

                print(f"  ✓ Completado")
                ejecutadas += 1

            except Error as e:
                # Algunos errores pueden ser aceptables (ej: tabla no existe)
                if "doesn't exist" in str(e).lower() or "unknown table" in str(e).lower():
                    print(f"  ⚠ Tabla no existe (esto es normal si la tabla es opcional)")
                else:
                    print(f"  ✗ Error: {e}")
                    errores += 1

        print("-" * 80)
        print(f"\nResumen:")
        print(f"  Sentencias ejecutadas: {ejecutadas}/{total_sentencias}")
        print(f"  Errores: {errores}")

        # Verificar los cambios
        print("\nVerificando cambios aplicados...")
        cursor.execute("""
            SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, NUMERIC_PRECISION, NUMERIC_SCALE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = %s
            AND DATA_TYPE = 'decimal'
            AND TABLE_NAME LIKE 'tbl_%'
            ORDER BY TABLE_NAME, COLUMN_NAME
        """, (database,))

        columnas_modificadas = cursor.fetchall()

        if columnas_modificadas:
            print(f"\n✓ Se encontraron {len(columnas_modificadas)} columnas DECIMAL(10,2):")
            print("-" * 80)
            for tabla, columna, tipo, precision, scale in columnas_modificadas:
                print(f"  {tabla}.{columna}: {tipo}({precision},{scale})")
        else:
            print("\n⚠ No se encontraron columnas DECIMAL")

        cursor.close()
        conn.close()

        print("\n" + "=" * 80)
        if errores == 0:
            print("✓ Script aplicado correctamente")
        else:
            print(f"⚠ Script aplicado con {errores} errores (revisar detalles arriba)")
        print("=" * 80)

        return errores == 0

    except Error as e:
        print(f"\n✗ Error de base de datos: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Función principal."""
    print("=" * 80)
    print("APLICACIÓN DE CORRECCIÓN DE DECIMALES EN BASE DE DATOS")
    print("=" * 80)
    print()
    print("Este script modificará la estructura de la base de datos para")
    print("convertir campos DOUBLE/FLOAT a DECIMAL(10,2)")
    print()

    # Solicitar datos de conexión
    host = input("Host [localhost]: ").strip() or "localhost"
    port = input("Puerto [3307]: ").strip() or "3307"
    database = input("Base de datos [cert_dev]: ").strip() or "cert_dev"
    user = input("Usuario [root]: ").strip() or "root"
    password = getpass.getpass("Contraseña: ")

    print()
    print("⚠ ADVERTENCIA: Este script modificará la estructura de la base de datos.")
    print("  Se recomienda hacer un backup antes de continuar.")
    print()

    confirmar = input("¿Desea continuar? (s/N): ").strip().lower()
    if confirmar != 's' and confirmar != 'si':
        print("\n✗ Operación cancelada")
        return

    # Ruta al script SQL
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, 'sql', 'fix_decimal_precision.sql')

    print()
    if aplicar_script_sql(host, int(port), database, user, password, script_path):
        print("\n✓ ¡Proceso completado exitosamente!")
        print("\nAhora todos los campos numéricos utilizan DECIMAL(10,2)")
        print("para garantizar precisión de 2 decimales.")
    else:
        print("\n✗ El proceso finalizó con errores")
        print("Revise los mensajes anteriores para más detalles")


if __name__ == "__main__":
    main()
