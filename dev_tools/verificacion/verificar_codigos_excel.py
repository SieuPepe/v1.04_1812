#!/usr/bin/env python3
"""
Script para verificar que todos los códigos del Excel MEDICIONES OTS.xlsx
existen en la tabla tbl_partes de la base de datos.

Uso:
    python verificar_codigos_excel.py
"""

import pandas as pd
import mysql.connector
from pathlib import Path
import sys

# Configuración
EXCEL_FILE = Path(__file__).parent.parent / "MEDICIONES OTS.xlsx"
DB_CONFIG = {
    'host': 'localhost',
    'user': 'cert_dev',
    'password': 'urbide',
    'database': 'cert_dev'
}


def conectar_bd():
    """Conecta a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print(f"✓ Conectado a la base de datos: {DB_CONFIG['database']}")
        return conn
    except mysql.connector.Error as e:
        print(f"✗ Error al conectar a la base de datos: {e}")
        sys.exit(1)


def leer_codigos_excel():
    """Lee todos los códigos únicos del Excel."""
    try:
        df = pd.read_excel(EXCEL_FILE)
        print(f"\n✓ Excel leído: {EXCEL_FILE.name}")
        print(f"  Total de registros: {len(df)}")

        # Obtener códigos únicos de la columna parte_id
        if 'parte_id' not in df.columns:
            print(f"✗ Error: No se encuentra la columna 'parte_id' en el Excel")
            print(f"  Columnas disponibles: {', '.join(df.columns)}")
            sys.exit(1)

        # Eliminar valores nulos y obtener únicos
        codigos = df['parte_id'].dropna().unique()

        # Normalizar códigos: convertir / a - y quitar espacios
        codigos_normalizados = []
        for codigo in codigos:
            codigo_str = str(codigo).strip()
            # Convertir formato OT/0121 a OT-0121
            codigo_normalizado = codigo_str.replace('/', '-')
            codigos_normalizados.append(codigo_normalizado)

        codigos_unicos = sorted(set(codigos_normalizados))

        print(f"  Códigos únicos encontrados: {len(codigos_unicos)}")

        return codigos_unicos

    except FileNotFoundError:
        print(f"✗ Error: No se encuentra el archivo {EXCEL_FILE}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error al leer el Excel: {e}")
        sys.exit(1)


def obtener_codigos_bd(conn):
    """Obtiene todos los códigos de tbl_partes."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT codigo FROM tbl_partes")
        codigos_bd = [row[0] for row in cursor.fetchall()]
        cursor.close()

        print(f"\n✓ Códigos en tbl_partes: {len(codigos_bd)}")

        return set(codigos_bd)

    except mysql.connector.Error as e:
        print(f"✗ Error al consultar la base de datos: {e}")
        sys.exit(1)


def verificar_codigos(codigos_excel, codigos_bd):
    """Verifica qué códigos del Excel están o no en la BD."""

    print("\n" + "="*70)
    print("VERIFICACIÓN DE CÓDIGOS")
    print("="*70)

    codigos_encontrados = []
    codigos_faltantes = []

    for codigo in codigos_excel:
        if codigo in codigos_bd:
            codigos_encontrados.append(codigo)
        else:
            codigos_faltantes.append(codigo)

    # Resumen
    print(f"\nTotal de códigos en Excel: {len(codigos_excel)}")
    print(f"  ✓ Códigos encontrados en BD: {len(codigos_encontrados)}")
    print(f"  ✗ Códigos faltantes en BD: {len(codigos_faltantes)}")

    porcentaje = (len(codigos_encontrados) / len(codigos_excel) * 100) if codigos_excel else 0
    print(f"\nPorcentaje de cobertura: {porcentaje:.1f}%")

    # Mostrar códigos faltantes
    if codigos_faltantes:
        print("\n" + "="*70)
        print("CÓDIGOS FALTANTES EN tbl_partes")
        print("="*70)

        for i, codigo in enumerate(codigos_faltantes, 1):
            print(f"{i:3d}. {codigo}")

        # Agrupar por prefijo
        print("\n" + "-"*70)
        print("RESUMEN POR TIPO")
        print("-"*70)

        prefijos = {}
        for codigo in codigos_faltantes:
            prefijo = codigo.split('-')[0] if '-' in codigo else 'SIN-PREFIJO'
            prefijos[prefijo] = prefijos.get(prefijo, 0) + 1

        for prefijo, cantidad in sorted(prefijos.items()):
            print(f"  {prefijo}: {cantidad} códigos faltantes")

    else:
        print("\n✓✓✓ ¡TODOS LOS CÓDIGOS DEL EXCEL ESTÁN EN LA BASE DE DATOS! ✓✓✓")

    return codigos_encontrados, codigos_faltantes


def generar_sql_verificacion(codigos_excel):
    """Genera un archivo SQL completo con todos los códigos para verificación."""
    sql_file = Path(__file__).parent / "sql" / "verificar_codigos_excel.sql"

    # Leer plantilla base
    plantilla = """-- ============================================================================
-- SCRIPT DE VERIFICACIÓN: Códigos de Excel en tbl_partes
-- ============================================================================
--
-- Este script verifica qué códigos del archivo MEDICIONES OTS.xlsx
-- existen en la tabla tbl_partes y cuáles faltan.
--
-- Total de códigos en Excel: {total_codigos}
--
-- Uso en MySQL Workbench:
--   1. Abrir este archivo
--   2. Ejecutar todo el script (Ctrl+Shift+Enter)
--   3. Revisar los resultados en la pestaña de salida
-- ============================================================================

USE cert_dev;

-- Crear tabla temporal con los códigos del Excel
DROP TEMPORARY TABLE IF EXISTS tmp_codigos_excel;

CREATE TEMPORARY TABLE tmp_codigos_excel (
    codigo VARCHAR(50) PRIMARY KEY,
    origen VARCHAR(20) DEFAULT 'EXCEL'
);

-- Insertar los {total_codigos} códigos únicos encontrados en MEDICIONES OTS.xlsx
-- Formato normalizado: convertido de OT/0121 a OT-0121

INSERT INTO tmp_codigos_excel (codigo) VALUES
{valores_codigos};


-- ============================================================================
-- ANÁLISIS 1: Resumen General
-- ============================================================================

SELECT
    'RESUMEN GENERAL' as Analisis,
    COUNT(*) as Total_Codigos_Excel,
    (SELECT COUNT(*) FROM tbl_partes) as Total_Codigos_BD,
    SUM(CASE WHEN p.id IS NOT NULL THEN 1 ELSE 0 END) as Codigos_Encontrados,
    SUM(CASE WHEN p.id IS NULL THEN 1 ELSE 0 END) as Codigos_Faltantes,
    ROUND(SUM(CASE WHEN p.id IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) as Porcentaje_Cobertura
FROM tmp_codigos_excel e
LEFT JOIN tbl_partes p ON e.codigo = p.codigo;


-- ============================================================================
-- ANÁLISIS 2: Códigos que SÍ están en tbl_partes (ENCONTRADOS)
-- ============================================================================

SELECT
    'CÓDIGOS ENCONTRADOS' as Estado,
    e.codigo as Codigo_Excel,
    p.id as Parte_ID,
    p.descripcion as Descripcion,
    tt.nombre as Tipo_Trabajo
FROM tmp_codigos_excel e
INNER JOIN tbl_partes p ON e.codigo = p.codigo
LEFT JOIN dim_tipo_trabajo tt ON p.tipo_trabajo_id = tt.id
ORDER BY e.codigo;


-- ============================================================================
-- ANÁLISIS 3: Códigos que NO están en tbl_partes (FALTANTES)
-- ============================================================================

SELECT
    'CÓDIGOS FALTANTES' as Estado,
    e.codigo as Codigo_Excel,
    SUBSTRING_INDEX(e.codigo, '-', 1) as Prefijo,
    'NO EXISTE EN BD' as Observacion
FROM tmp_codigos_excel e
LEFT JOIN tbl_partes p ON e.codigo = p.codigo
WHERE p.id IS NULL
ORDER BY e.codigo;


-- ============================================================================
-- ANÁLISIS 4: Resumen por tipo de código (prefijo)
-- ============================================================================

SELECT
    SUBSTRING_INDEX(e.codigo, '-', 1) as Prefijo,
    COUNT(*) as Total_Excel,
    SUM(CASE WHEN p.id IS NOT NULL THEN 1 ELSE 0 END) as Encontrados,
    SUM(CASE WHEN p.id IS NULL THEN 1 ELSE 0 END) as Faltantes,
    ROUND(SUM(CASE WHEN p.id IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) as Porcentaje_OK
FROM tmp_codigos_excel e
LEFT JOIN tbl_partes p ON e.codigo = p.codigo
GROUP BY SUBSTRING_INDEX(e.codigo, '-', 1)
ORDER BY Prefijo;


-- ============================================================================
-- ANÁLISIS 5: Primeros y últimos códigos faltantes (vista rápida)
-- ============================================================================

-- Primeros 10 faltantes
SELECT
    'PRIMEROS 10 FALTANTES' as Lista,
    e.codigo
FROM tmp_codigos_excel e
LEFT JOIN tbl_partes p ON e.codigo = p.codigo
WHERE p.id IS NULL
ORDER BY e.codigo
LIMIT 10;

-- Últimos 10 faltantes
SELECT
    'ÚLTIMOS 10 FALTANTES' as Lista,
    e.codigo
FROM tmp_codigos_excel e
LEFT JOIN tbl_partes p ON e.codigo = p.codigo
WHERE p.id IS NULL
ORDER BY e.codigo DESC
LIMIT 10;


-- ============================================================================
-- LIMPIEZA
-- ============================================================================

-- La tabla temporal se eliminará automáticamente al cerrar la conexión
-- DROP TEMPORARY TABLE IF EXISTS tmp_codigos_excel;

-- ============================================================================
-- FIN DEL SCRIPT
-- ============================================================================
"""

    try:
        # Generar los valores para el INSERT
        valores = []
        for codigo in sorted(codigos_excel):
            valores.append(f"('{codigo}')")

        # Unir valores (máximo 100 por línea para legibilidad)
        lineas_valores = []
        for i in range(0, len(valores), 100):
            chunk = valores[i:i+100]
            linea = ',\n'.join(chunk)
            lineas_valores.append(linea)

        valores_sql = ',\n'.join(lineas_valores)

        # Completar la plantilla
        sql_completo = plantilla.format(
            total_codigos=len(codigos_excel),
            valores_codigos=valores_sql
        )

        # Guardar archivo
        with open(sql_file, 'w', encoding='utf-8') as f:
            f.write(sql_completo)

        print(f"\n✓ Script SQL generado: {sql_file}")
        print(f"  Puedes ejecutarlo directamente en MySQL Workbench")

    except Exception as e:
        print(f"✗ Error al generar el SQL: {e}")


def guardar_reporte(codigos_faltantes):
    """Guarda un reporte de los códigos faltantes."""
    if not codigos_faltantes:
        return

    reporte_file = Path(__file__).parent / "codigos_faltantes.txt"

    try:
        with open(reporte_file, 'w', encoding='utf-8') as f:
            f.write("CÓDIGOS FALTANTES EN tbl_partes\n")
            f.write("="*70 + "\n\n")

            for codigo in sorted(codigos_faltantes):
                f.write(f"{codigo}\n")

        print(f"\n✓ Reporte guardado en: {reporte_file}")

    except Exception as e:
        print(f"✗ Error al guardar el reporte: {e}")


def main():
    """Función principal."""
    print("="*70)
    print("VERIFICACIÓN DE CÓDIGOS: EXCEL → tbl_partes")
    print("="*70)

    # Paso 1: Leer códigos del Excel
    codigos_excel = leer_codigos_excel()

    # Paso 2: Generar SQL de verificación (siempre)
    generar_sql_verificacion(codigos_excel)

    # Paso 3: Intentar conectar a la BD y verificar (opcional)
    try:
        conn = conectar_bd()
        codigos_bd = obtener_codigos_bd(conn)

        # Verificar códigos
        codigos_encontrados, codigos_faltantes = verificar_codigos(codigos_excel, codigos_bd)

        # Guardar reporte si hay faltantes
        if codigos_faltantes:
            guardar_reporte(codigos_faltantes)

        # Cerrar conexión
        conn.close()

        print("\n" + "="*70)
        print("VERIFICACIÓN COMPLETADA")
        print("="*70 + "\n")

        # Retornar código de salida según resultado
        return 0 if not codigos_faltantes else 1

    except SystemExit:
        # No se pudo conectar a la BD, pero el SQL ya fue generado
        print("\n" + "="*70)
        print("SQL GENERADO - Ejecuta el script SQL en MySQL Workbench")
        print("="*70 + "\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())
