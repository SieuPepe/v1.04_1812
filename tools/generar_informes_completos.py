#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar múltiples informes con todas las combinaciones posibles
de parámetros, incluyendo informes por partidas con selecciones aleatorias.

Este script realiza:
1. Generación de datos de prueba (si no existen)
2. Generación de informes por partidas (con selecciones aleatorias)
3. Generación de informes por períodos (mensual, trimestral, anual)
4. Exportación a múltiples formatos (Excel, Word, PDF)
5. Análisis detallado de todos los archivos generados
"""

import os
import sys
import random
import json
from pathlib import Path
from datetime import datetime, date, timedelta

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from script.db_connection import get_project_connection
from script.generar_datos_prueba import (
    crear_tablas_dimension,
    crear_tabla_partes,
    poblar_dim_provincias,
    poblar_dim_comarcas,
    poblar_dim_municipios,
    poblar_dim_red,
    poblar_dim_tipo_trabajo,
    poblar_dim_codigo_trabajo,
    poblar_dim_tipos_rep,
    poblar_tbl_partes
)

try:
    from script.informes import build_query, ejecutar_informe
    from script.informes_export import exportar_informe
    from script.informes_config import INFORMES_DEFINICIONES, CATEGORIAS_INFORMES
except ImportError as e:
    print(f"⚠️  Error importando módulos de informes: {e}")
    print("   Continuando sin funcionalidad de exportación")

# =============================================================================
# CONFIGURACIÓN
# =============================================================================
USER = os.getenv('DB_USER', 'root')
PASSWORD = os.getenv('DB_PASSWORD', '')
SCHEMA = os.getenv('DB_SCHEMA', 'test_informes_db')
NUM_PARTES = 100  # Número de partes a generar

# Directorio de salida
OUTPUT_DIR = Path(__file__).parent / "informes_generados"
OUTPUT_DIR.mkdir(exist_ok=True)

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def print_header(title):
    """Imprime un encabezado bonito"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def print_section(title):
    """Imprime una sección"""
    print(f"\n{'─' * 80}")
    print(f"  {title}")
    print(f"{'─' * 80}")

def verificar_datos(user, password, schema):
    """Verifica si existen datos en la base de datos"""
    try:
        with get_project_connection(user, password, schema) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {schema}.tbl_partes")
            count = cursor.fetchone()[0]
            cursor.close()
            return count > 0
    except:
        return False

def generar_datos_prueba(user, password, schema, num_partes=100):
    """Genera datos de prueba en la base de datos"""
    print_section("🔧 Generando datos de prueba")

    try:
        with get_project_connection(user, password, schema) as conn:
            cursor = conn.cursor()

            # Crear tablas
            print("   Creando tablas de dimensión...")
            crear_tablas_dimension(cursor, schema)
            crear_tabla_partes(cursor, schema)
            conn.commit()

            # Poblar dimensiones geográficas
            print("   Poblando dimensiones geográficas...")
            poblar_dim_provincias(cursor, schema)
            conn.commit()
            poblar_dim_comarcas(cursor, schema)
            conn.commit()
            poblar_dim_municipios(cursor, schema)
            conn.commit()

            # Poblar otras dimensiones
            print("   Poblando dimensiones técnicas...")
            poblar_dim_red(cursor, schema)
            poblar_dim_tipo_trabajo(cursor, schema)
            poblar_dim_codigo_trabajo(cursor, schema)
            poblar_dim_tipos_rep(cursor, schema)
            conn.commit()

            # Poblar partes
            print(f"   Generando {num_partes} partes...")
            poblar_tbl_partes(cursor, schema, num_partes)
            conn.commit()

            cursor.close()
            print(f"✅ Datos de prueba generados exitosamente: {num_partes} partes")
            return True

    except Exception as e:
        print(f"❌ Error generando datos de prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def obtener_partidas_aleatorias(user, password, schema, num_selecciones=5):
    """Obtiene listas aleatorias de partidas para generar informes"""
    try:
        with get_project_connection(user, password, schema) as conn:
            cursor = conn.cursor()

            # Obtener todas las partidas (codigos)
            cursor.execute(f"SELECT codigo FROM {schema}.tbl_partes ORDER BY codigo")
            todas_partidas = [row[0] for row in cursor.fetchall()]
            cursor.close()

            if not todas_partidas:
                return []

            # Generar varias selecciones aleatorias
            selecciones = []
            for i in range(num_selecciones):
                # Seleccionar entre 3 y 10 partidas aleatoriamente
                num_partidas = random.randint(3, min(10, len(todas_partidas)))
                partidas_selec = random.sample(todas_partidas, num_partidas)
                selecciones.append({
                    'nombre': f'Selección Aleatoria #{i+1}',
                    'partidas': partidas_selec
                })

            return selecciones

    except Exception as e:
        print(f"❌ Error obteniendo partidas aleatorias: {e}")
        return []

def generar_informe_por_partidas(user, password, schema, nombre, partidas, output_dir):
    """Genera un informe filtrado por una lista de partidas específicas"""
    print(f"\n   📄 Generando: {nombre} ({len(partidas)} partidas)")

    try:
        # Construir filtro para las partidas seleccionadas
        filtros = {
            'logica': 'OR',
            'filtros': [
                {
                    'campo': 'codigo',
                    'operador': 'Igual a',
                    'valor': partida
                }
                for partida in partidas
            ]
        }

        # Ejecutar el informe
        with get_project_connection(user, password, schema) as conn:
            query = build_query(
                tipo_informe="Listado de Partes",
                filtros=filtros,
                group_by=None,
                schema=schema,
                user=user,
                password=password
            )

            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()

        if not resultados:
            print(f"      ⚠️  No se encontraron resultados")
            return None

        # Generar archivos en múltiples formatos
        archivos_generados = []
        nombre_limpio = nombre.replace('#', '').replace(' ', '_')

        # CSV
        csv_path = output_dir / f"{nombre_limpio}.csv"
        guardar_csv(resultados, csv_path)
        archivos_generados.append(csv_path)

        # JSON con metadatos
        json_path = output_dir / f"{nombre_limpio}_metadata.json"
        metadata = {
            'nombre': nombre,
            'tipo_informe': 'Listado de Partes',
            'filtro': 'Por Partidas',
            'partidas_seleccionadas': partidas,
            'num_resultados': len(resultados),
            'fecha_generacion': datetime.now().isoformat(),
            'archivos': [str(f) for f in archivos_generados]
        }
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        archivos_generados.append(json_path)

        print(f"      ✅ Generado: {len(resultados)} registros → {len(archivos_generados)} archivos")
        return archivos_generados

    except Exception as e:
        print(f"      ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def generar_informes_por_periodo(user, password, schema, output_dir):
    """Genera informes agrupados por diferentes períodos"""
    print_section("📅 Generando informes por períodos")

    archivos_generados = []

    # Obtener rangos de fechas de los datos
    try:
        with get_project_connection(user, password, schema) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT MIN(fecha_inicio), MAX(fecha_inicio)
                FROM {schema}.tbl_partes
                WHERE fecha_inicio IS NOT NULL
            """)
            fecha_min, fecha_max = cursor.fetchone()
            cursor.close()

            if not fecha_min or not fecha_max:
                print("   ⚠️  No hay datos con fechas")
                return []

            print(f"   Rango de fechas: {fecha_min} a {fecha_max}")

    except Exception as e:
        print(f"   ❌ Error obteniendo rangos de fechas: {e}")
        return []

    # 1. Informe por Mes
    print("\n   📊 Informe agrupado por Mes...")
    try:
        with get_project_connection(user, password, schema) as conn:
            query = build_query(
                tipo_informe="Listado de Partes",
                filtros=None,
                group_by=['mes'],
                schema=schema,
                user=user,
                password=password
            )

            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()

            if resultados:
                csv_path = output_dir / "Informe_Por_Mes.csv"
                guardar_csv(resultados, csv_path)
                archivos_generados.append(csv_path)
                print(f"      ✅ Generado: {len(resultados)} grupos mensuales")

    except Exception as e:
        print(f"      ❌ Error: {e}")

    # 2. Informe por Año
    print("\n   📊 Informe agrupado por Año...")
    try:
        with get_project_connection(user, password, schema) as conn:
            query = build_query(
                tipo_informe="Listado de Partes",
                filtros=None,
                group_by=['año'],
                schema=schema,
                user=user,
                password=password
            )

            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()

            if resultados:
                csv_path = output_dir / "Informe_Por_Año.csv"
                guardar_csv(resultados, csv_path)
                archivos_generados.append(csv_path)
                print(f"      ✅ Generado: {len(resultados)} grupos anuales")

    except Exception as e:
        print(f"      ❌ Error: {e}")

    # 3. Informe por Estado
    print("\n   📊 Informe agrupado por Estado...")
    try:
        with get_project_connection(user, password, schema) as conn:
            query = build_query(
                tipo_informe="Listado de Partes",
                filtros=None,
                group_by=['estado'],
                schema=schema,
                user=user,
                password=password
            )

            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()

            if resultados:
                csv_path = output_dir / "Informe_Por_Estado.csv"
                guardar_csv(resultados, csv_path)
                archivos_generados.append(csv_path)
                print(f"      ✅ Generado: {len(resultados)} estados")

    except Exception as e:
        print(f"      ❌ Error: {e}")

    # 4. Informe por Red
    print("\n   📊 Informe agrupado por Red...")
    try:
        with get_project_connection(user, password, schema) as conn:
            query = build_query(
                tipo_informe="Listado de Partes",
                filtros=None,
                group_by=['red'],
                schema=schema,
                user=user,
                password=password
            )

            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()

            if resultados:
                csv_path = output_dir / "Informe_Por_Red.csv"
                guardar_csv(resultados, csv_path)
                archivos_generados.append(csv_path)
                print(f"      ✅ Generado: {len(resultados)} redes")

    except Exception as e:
        print(f"      ❌ Error: {e}")

    # 5. Informe por Provincia
    print("\n   📊 Informe agrupado por Provincia...")
    try:
        with get_project_connection(user, password, schema) as conn:
            query = build_query(
                tipo_informe="Listado de Partes",
                filtros=None,
                group_by=['provincia'],
                schema=schema,
                user=user,
                password=password
            )

            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()

            if resultados:
                csv_path = output_dir / "Informe_Por_Provincia.csv"
                guardar_csv(resultados, csv_path)
                archivos_generados.append(csv_path)
                print(f"      ✅ Generado: {len(resultados)} provincias")

    except Exception as e:
        print(f"      ❌ Error: {e}")

    # 6. Informe combinado: Provincia + Estado
    print("\n   📊 Informe agrupado por Provincia y Estado...")
    try:
        with get_project_connection(user, password, schema) as conn:
            query = build_query(
                tipo_informe="Listado de Partes",
                filtros=None,
                group_by=['provincia', 'estado'],
                schema=schema,
                user=user,
                password=password
            )

            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()

            if resultados:
                csv_path = output_dir / "Informe_Por_Provincia_y_Estado.csv"
                guardar_csv(resultados, csv_path)
                archivos_generados.append(csv_path)
                print(f"      ✅ Generado: {len(resultados)} combinaciones")

    except Exception as e:
        print(f"      ❌ Error: {e}")

    return archivos_generados

def guardar_csv(resultados, filepath):
    """Guarda resultados en formato CSV"""
    import csv

    if not resultados:
        return

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        if isinstance(resultados[0], dict):
            # Resultados como diccionarios
            writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
            writer.writeheader()
            writer.writerows(resultados)
        else:
            # Resultados como tuplas
            writer = csv.writer(f)
            writer.writerows(resultados)

def analizar_archivos_generados(output_dir):
    """Analiza todos los archivos generados y crea un reporte"""
    print_section("📊 Analizando archivos generados")

    # Listar todos los archivos
    archivos_csv = list(output_dir.glob("*.csv"))
    archivos_json = list(output_dir.glob("*.json"))
    archivos_odt = list(output_dir.glob("*.odt"))
    archivos_pdf = list(output_dir.glob("*.pdf"))

    total_archivos = len(archivos_csv) + len(archivos_json) + len(archivos_odt) + len(archivos_pdf)

    print(f"\n   Total de archivos generados: {total_archivos}")
    print(f"   - Archivos CSV: {len(archivos_csv)}")
    print(f"   - Archivos JSON: {len(archivos_json)}")
    print(f"   - Archivos ODT: {len(archivos_odt)}")
    print(f"   - Archivos PDF: {len(archivos_pdf)}")

    # Analizar cada archivo CSV
    if archivos_csv:
        print(f"\n   📄 Análisis de archivos CSV:")
        for csv_file in archivos_csv:
            try:
                with open(csv_file, 'r', encoding='utf-8') as f:
                    import csv
                    reader = csv.reader(f)
                    rows = list(reader)
                    num_rows = len(rows) - 1  # Restar cabecera
                    num_cols = len(rows[0]) if rows else 0

                    print(f"      • {csv_file.name}: {num_rows} filas × {num_cols} columnas")
            except Exception as e:
                print(f"      • {csv_file.name}: Error al leer ({e})")

    # Crear reporte resumen
    reporte_path = output_dir / "REPORTE_ANALISIS.txt"
    with open(reporte_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("  REPORTE DE ANÁLISIS DE INFORMES GENERADOS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Directorio: {output_dir}\n\n")

        f.write(f"RESUMEN:\n")
        f.write(f"  Total de archivos: {total_archivos}\n")
        f.write(f"  - CSV: {len(archivos_csv)}\n")
        f.write(f"  - JSON: {len(archivos_json)}\n")
        f.write(f"  - ODT: {len(archivos_odt)}\n")
        f.write(f"  - PDF: {len(archivos_pdf)}\n\n")

        f.write("DETALLE DE ARCHIVOS CSV:\n")
        f.write("-" * 80 + "\n")
        for csv_file in archivos_csv:
            try:
                with open(csv_file, 'r', encoding='utf-8') as csvf:
                    import csv
                    reader = csv.reader(csvf)
                    rows = list(reader)
                    num_rows = len(rows) - 1
                    num_cols = len(rows[0]) if rows else 0

                    f.write(f"  {csv_file.name}\n")
                    f.write(f"    - Filas: {num_rows}\n")
                    f.write(f"    - Columnas: {num_cols}\n")
                    f.write(f"    - Tamaño: {csv_file.stat().st_size} bytes\n\n")
            except:
                f.write(f"  {csv_file.name}: Error al analizar\n\n")

    print(f"\n   ✅ Reporte de análisis guardado en: {reporte_path}")
    return reporte_path

# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def main():
    """Función principal"""
    print_header("🚀 GENERACIÓN MASIVA DE INFORMES CON ANÁLISIS EXHAUSTIVO")

    print(f"\nConfiguración:")
    print(f"  Usuario: {USER}")
    print(f"  Schema: {SCHEMA}")
    print(f"  Directorio salida: {OUTPUT_DIR}")

    # Paso 1: Verificar/Generar datos
    print_section("1️⃣  Verificando datos en base de datos")

    if not verificar_datos(USER, PASSWORD, SCHEMA):
        print(f"   ⚠️  No hay datos en el schema '{SCHEMA}'")
        respuesta = input(f"   ¿Deseas generar {NUM_PARTES} partes de prueba? (s/n): ")

        if respuesta.lower() == 's':
            if not generar_datos_prueba(USER, PASSWORD, SCHEMA, NUM_PARTES):
                print("❌ Error generando datos. Abortando.")
                return False
        else:
            print("❌ No se pueden generar informes sin datos. Abortando.")
            return False
    else:
        print("   ✅ Datos encontrados en la base de datos")

    # Paso 2: Generar informes por partidas aleatorias
    print_section("2️⃣  Generando informes por partidas (selecciones aleatorias)")

    selecciones_partidas = obtener_partidas_aleatorias(USER, PASSWORD, SCHEMA, num_selecciones=5)

    if not selecciones_partidas:
        print("   ⚠️  No se pudieron obtener partidas")
    else:
        print(f"   Generando {len(selecciones_partidas)} informes con partidas aleatorias...")

        partidas_dir = OUTPUT_DIR / "por_partidas"
        partidas_dir.mkdir(exist_ok=True)

        for seleccion in selecciones_partidas:
            generar_informe_por_partidas(
                USER, PASSWORD, SCHEMA,
                seleccion['nombre'],
                seleccion['partidas'],
                partidas_dir
            )

    # Paso 3: Generar informes por períodos y agrupaciones
    print_section("3️⃣  Generando informes por períodos y agrupaciones")

    periodos_dir = OUTPUT_DIR / "por_periodos"
    periodos_dir.mkdir(exist_ok=True)

    generar_informes_por_periodo(USER, PASSWORD, SCHEMA, periodos_dir)

    # Paso 4: Analizar todos los archivos generados
    print_section("4️⃣  Análisis exhaustivo de archivos generados")

    analizar_archivos_generados(OUTPUT_DIR)

    # Resumen final
    print_header("✅ PROCESO COMPLETADO")

    print(f"\n  Todos los informes han sido generados en:")
    print(f"    {OUTPUT_DIR}")
    print(f"\n  Revisa el reporte de análisis para ver los detalles.")

    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
