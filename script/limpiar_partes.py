#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpiar datos de las tablas de partes.

Elimina TODOS los datos de:
- tbl_partes
- tbl_part_presupuesto
- tbl_part_certificacion

NO toca:
- tbl_pres_naturaleza, tbl_pres_unidades, tbl_pres_capitulos, tbl_pres_precios (catálogos de presupuesto maestro)
- Tablas de dimensiones (dim_red, dim_tipo_trabajo, etc.)
"""

import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from script.db_connection import get_project_connection


def mostrar_estadisticas_antes(cursor):
    """Muestra estadísticas antes de borrar."""
    print("\n" + "=" * 70)
    print("ESTADÍSTICAS ANTES DE BORRAR")
    print("=" * 70)

    # Contar registros en cada tabla
    tablas = [
        ('tbl_partes', 'Partes/Órdenes de Trabajo'),
        ('tbl_part_presupuesto', 'Presupuestos de Partes'),
        ('tbl_part_certificacion', 'Certificaciones de Partes')
    ]

    for tabla, descripcion in tablas:
        cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
        count = cursor.fetchone()[0]
        print(f"  {descripcion:40} {count:>10} registros")

    # Mostrar rango de fechas en tbl_partes
    cursor.execute("""
        SELECT
            MIN(creado_en) AS fecha_min,
            MAX(creado_en) AS fecha_max
        FROM tbl_partes
        WHERE creado_en IS NOT NULL
    """)
    resultado = cursor.fetchone()
    if resultado and resultado[0]:
        print(f"\n  Rango de fechas: {resultado[0]} a {resultado[1]}")


def mostrar_estadisticas_despues(cursor):
    """Muestra estadísticas después de borrar."""
    print("\n" + "=" * 70)
    print("ESTADÍSTICAS DESPUÉS DE BORRAR")
    print("=" * 70)

    tablas = [
        ('tbl_partes', 'Partes/Órdenes de Trabajo'),
        ('tbl_part_presupuesto', 'Presupuestos de Partes'),
        ('tbl_part_certificacion', 'Certificaciones de Partes')
    ]

    for tabla, descripcion in tablas:
        cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
        count = cursor.fetchone()[0]
        estado = "✓ LIMPIA" if count == 0 else "⚠ TIENE DATOS"
        print(f"  {descripcion:40} {count:>10} registros  {estado}")


def verificar_tablas_no_afectadas(cursor):
    """Verifica que las otras tablas no se modificaron."""
    print("\n" + "=" * 70)
    print("VERIFICACIÓN DE TABLAS NO AFECTADAS")
    print("=" * 70)

    tablas = [
        ('tbl_pres_naturaleza', 'Catálogo de Naturalezas'),
        ('tbl_pres_unidades', 'Catálogo de Unidades'),
        ('tbl_pres_capitulos', 'Catálogo de Capítulos'),
        ('tbl_pres_precios', 'Catálogo de Precios'),
        ('dim_red', 'Catálogo de Redes'),
        ('dim_tipo_trabajo', 'Catálogo de Tipos de Trabajo'),
        ('dim_codigo_trabajo', 'Catálogo de Códigos de Trabajo')
    ]

    for tabla, descripcion in tablas:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cursor.fetchone()[0]
            print(f"  {descripcion:40} {count:>10} registros  (OK)")
        except Exception as e:
            print(f"  {descripcion:40} ERROR: {e}")


def limpiar_datos_partes(user, password, schema):
    """
    Limpia los datos de las 3 tablas de partes.

    Args:
        user: Usuario de MySQL
        password: Contraseña
        schema: Esquema/base de datos a limpiar
    """
    print(f"\n{'=' * 70}")
    print(f"LIMPIEZA DE DATOS DE PARTES - Esquema: {schema}")
    print(f"{'=' * 70}")

    try:
        with get_project_connection(user, password, schema) as conexion:
            cursor = conexion.cursor()

            # Mostrar estadísticas ANTES
            mostrar_estadisticas_antes(cursor)

            # Confirmar antes de continuar
            print("\n" + "⚠" * 35)
            print("⚠  ADVERTENCIA: Esta operación es IRREVERSIBLE")
            print("⚠  Se eliminarán TODOS los datos de las 3 tablas de partes")
            print("⚠" * 35)

            respuesta = input("\n¿Estás seguro de que quieres continuar? (escribe 'SI' para confirmar): ")

            if respuesta.strip().upper() != 'SI':
                print("\n✗ Operación cancelada por el usuario")
                return False

            print("\n" + "=" * 70)
            print("ELIMINANDO DATOS...")
            print("=" * 70)

            # Desactivar verificación de FK temporalmente
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

            # Eliminar datos en orden
            tablas_a_limpiar = [
                'tbl_part_certificacion',
                'tbl_part_presupuesto',
                'tbl_partes'
            ]

            for tabla in tablas_a_limpiar:
                cursor.execute(f"DELETE FROM {tabla}")
                registros_eliminados = cursor.rowcount
                print(f"  ✓ {tabla}: {registros_eliminados} registros eliminados")

                # Reiniciar AUTO_INCREMENT
                cursor.execute(f"ALTER TABLE {tabla} AUTO_INCREMENT = 1")

            # Reactivar verificación de FK
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

            # Commit de los cambios
            conexion.commit()

            print("\n  ✓ Cambios confirmados (COMMIT)")

            # Mostrar estadísticas DESPUÉS
            mostrar_estadisticas_despues(cursor)

            # Verificar tablas no afectadas
            verificar_tablas_no_afectadas(cursor)

            cursor.close()

            print("\n" + "=" * 70)
            print("✓ LIMPIEZA COMPLETADA EXITOSAMENTE")
            print("=" * 70)

            return True

    except Exception as e:
        print(f"\n✗ ERROR durante la limpieza: {e}")
        import traceback
        traceback.print_exc()
        return False


def listar_esquemas_disponibles(user, password):
    """Lista los esquemas/bases de datos disponibles."""
    try:
        from script.db_connection import get_connection

        with get_connection(user, password) as conexion:
            cursor = conexion.cursor()
            cursor.execute("SHOW DATABASES")

            esquemas = [row[0] for row in cursor.fetchall()]

            # Filtrar esquemas del sistema
            esquemas_sistema = ['information_schema', 'mysql', 'performance_schema', 'sys']
            esquemas_disponibles = [e for e in esquemas if e not in esquemas_sistema]

            print("\n" + "=" * 70)
            print("ESQUEMAS/BASES DE DATOS DISPONIBLES")
            print("=" * 70)

            for i, esquema in enumerate(esquemas_disponibles, 1):
                print(f"  {i}. {esquema}")

            cursor.close()
            return esquemas_disponibles

    except Exception as e:
        print(f"\n✗ ERROR al listar esquemas: {e}")
        return []


def main():
    """Función principal."""
    print("\n" + "=" * 70)
    print("SCRIPT DE LIMPIEZA DE DATOS DE PARTES")
    print("=" * 70)

    # Solicitar credenciales
    user = input("\nUsuario de MySQL (default: root): ").strip() or 'root'

    import getpass
    password = getpass.getpass("Contraseña: ")

    # Listar esquemas disponibles
    esquemas = listar_esquemas_disponibles(user, password)

    if not esquemas:
        print("\n✗ No se encontraron esquemas disponibles")
        return 1

    # Solicitar esquema a limpiar
    print("\n" + "=" * 70)
    esquema = input("Introduce el nombre del esquema a limpiar: ").strip()

    if not esquema:
        print("\n✗ Debes especificar un esquema")
        return 1

    if esquema not in esquemas:
        print(f"\n⚠ ADVERTENCIA: El esquema '{esquema}' no está en la lista")
        confirmar = input("¿Continuar de todas formas? (SI/NO): ")
        if confirmar.strip().upper() != 'SI':
            print("\n✗ Operación cancelada")
            return 1

    # Ejecutar limpieza
    exito = limpiar_datos_partes(user, password, esquema)

    return 0 if exito else 1


if __name__ == '__main__':
    sys.exit(main())
