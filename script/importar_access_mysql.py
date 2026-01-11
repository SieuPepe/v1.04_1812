#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
SCRIPT DE IMPORTACIÓN: Access → MySQL
============================================================================
Este script importa datos desde la base de datos Access de certificaciones
a la base de datos MySQL de HydroFlow Manager.

REQUISITOS:
  - Python 3.8+
  - mysql-connector-python: pip install mysql-connector-python

  Windows:
    - pyodbc: pip install pyodbc
    - Microsoft Access Database Engine (normalmente ya instalado)

  Linux:
    - mdb-tools: sudo apt install mdb-tools

USO:
  python importar_access_mysql.py --access /ruta/al/archivo.accdb --host localhost --user root --password xxx --database hydroflow

FASES:
  1. Limpieza de tablas de hechos (libera FK hacia dimensiones)
  2. Verificación/sincronización de dimensiones (dim_tipo_trabajo, dim_codigo_trabajo, dim_red)
  3. Mapeo geográfico (COMARCA → municipio, LOCALIZACIÓN → concejo)
  4. Importación de datos (LISTADO OTS → tbl_partes, MEDICIONES OTS → tbl_part_presupuesto)

AUTOR: Script generado automáticamente para HydroFlow Manager
FECHA: 2026-01-11
============================================================================
"""

import subprocess
import sys
import os
import re
import argparse
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from difflib import SequenceMatcher
import unicodedata

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# Mapeo de tipo de trabajo: Access ID → MySQL ID
# Después de sincronizar dimensiones, los IDs coinciden directamente:
#   Access 1 (ORDEN DE TRABAJO) = MySQL 1 (OT)
#   Access 2 (TRABAJOS PROGRAMADOS) = MySQL 2 (TP)
#   Access 3 (GASTOS FIJOS) = MySQL 3 (GF)
MAPEO_TIPO_TRABAJO = {
    1: 1,  # ORDEN DE TRABAJO → OT
    2: 2,  # TRABAJOS PROGRAMADOS → TP
    3: 3,  # GASTOS FIJOS → GF
}

# Mapeo de RED: Texto Access → MySQL ID
MAPEO_RED = {
    'ADUCCIÓN': 1,
    'ADUCCION': 1,
    'DEPURACIÓN': 2,
    'DEPURACION': 2,
    'DISTRIBUCIÓN': 3,
    'DISTRIBUCION': 3,
    'OTROS': 4,
    'SANEAMIENTO': 5,
}

# Valores problemáticos de COMARCA que deben mapearse manualmente
MAPEO_COMARCA_ESPECIAL = {
    'AIARA': 'Ayala/Aiara',
    'AIARALDEA': 'Ayala/Aiara',  # Zona de Ayala
    'VITORIA': 'Vitoria-Gasteiz',
    'ALAVA': None,  # Demasiado genérico, requerirá intervención manual
    'ÁLAVA': None,
}

# ============================================================================
# UTILIDADES
# ============================================================================

def normalizar_texto(texto: str) -> str:
    """Normaliza texto para comparación: sin acentos, minúsculas, sin espacios extra."""
    if not texto:
        return ''
    # Eliminar acentos
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    # Minúsculas y limpiar espacios
    texto = texto.lower().strip()
    texto = re.sub(r'\s+', ' ', texto)
    return texto


def similitud(a: str, b: str) -> float:
    """Calcula similitud entre dos strings (0.0 a 1.0)."""
    return SequenceMatcher(None, normalizar_texto(a), normalizar_texto(b)).ratio()


def es_coordenada(texto: str) -> bool:
    """Detecta si un texto parece ser una coordenada GPS."""
    if not texto:
        return False
    # Patrón de coordenadas: números con decimales
    return bool(re.match(r'^-?\d+\.\d+$', texto.strip()))


def es_direccion(texto: str) -> bool:
    """Detecta si un texto parece ser una dirección."""
    if not texto:
        return False
    texto_lower = texto.lower()
    indicadores = ['kalea', 'calle', 'plaza', 'avenida', 'paseo', 'camino', 'nº', 'número']
    return any(ind in texto_lower for ind in indicadores)


def leer_tabla_access(accdb_path: str, tabla: str) -> List[Dict]:
    """
    Lee una tabla de Access y devuelve lista de diccionarios.
    Detecta automáticamente el SO y usa el método apropiado:
    - Windows: pyodbc con driver de Access
    - Linux: mdb-tools
    """
    import platform

    if platform.system() == 'Windows':
        return _leer_tabla_access_windows(accdb_path, tabla)
    else:
        return _leer_tabla_access_linux(accdb_path, tabla)


def _leer_tabla_access_windows(accdb_path: str, tabla: str) -> List[Dict]:
    """Lee tabla de Access usando pyodbc (Windows)."""
    try:
        import pyodbc
    except ImportError:
        print("ERROR: pyodbc no está instalado.")
        print("Instálalo con: pip install pyodbc")
        sys.exit(1)

    try:
        # Construir connection string para Access
        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            f'DBQ={accdb_path};'
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Leer todos los registros
        cursor.execute(f'SELECT * FROM [{tabla}]')

        # Obtener nombres de columnas
        columns = [column[0] for column in cursor.description]

        # Convertir a lista de diccionarios
        rows = []
        for row in cursor.fetchall():
            row_dict = {}
            for i, col in enumerate(columns):
                value = row[i]
                # Convertir a string si no es None
                row_dict[col] = str(value) if value is not None else ''
            rows.append(row_dict)

        cursor.close()
        conn.close()
        return rows

    except pyodbc.Error as e:
        print(f"Error leyendo tabla {tabla}: {e}")
        return []
    except Exception as e:
        print(f"Error procesando tabla {tabla}: {e}")
        return []


def _leer_tabla_access_linux(accdb_path: str, tabla: str) -> List[Dict]:
    """Lee tabla de Access usando mdb-tools (Linux)."""
    try:
        # Exportar datos como CSV
        result = subprocess.run(
            ['mdb-export', accdb_path, tabla],
            capture_output=True, text=True, check=True
        )

        lines = result.stdout.strip().split('\n')
        if len(lines) < 1:
            return []

        # Parsear CSV manualmente para manejar campos con comas
        import csv
        from io import StringIO

        reader = csv.DictReader(StringIO(result.stdout))
        return list(reader)

    except FileNotFoundError:
        print("ERROR: mdb-tools no está instalado.")
        print("Instálalo con: sudo apt install mdb-tools")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error leyendo tabla {tabla}: {e}")
        return []
    except Exception as e:
        print(f"Error procesando tabla {tabla}: {e}")
        return []


def conectar_mysql(host: str, port: int, user: str, password: str, database: str):
    """Conecta a MySQL y devuelve conexión y cursor."""
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        return conn, conn.cursor(dictionary=True)
    except ImportError:
        print("ERROR: mysql-connector-python no está instalado.")
        print("Instálalo con: pip install mysql-connector-python")
        sys.exit(1)


# ============================================================================
# FASE 2: VERIFICACIÓN DE DIMENSIONES
# ============================================================================

def verificar_dim_tipo_trabajo(cursor, datos_access: List[Dict]) -> Tuple[bool, List[str]]:
    """Verifica que dim_tipo_trabajo coincide con Access."""
    errores = []

    print("\n" + "="*70)
    print("VERIFICACIÓN: dim_tipo_trabajo")
    print("="*70)

    # Obtener datos de MySQL
    cursor.execute("SELECT id, tipo_codigo, descripcion FROM dim_tipo_trabajo ORDER BY id")
    mysql_data = {row['id']: row for row in cursor.fetchall()}

    # Mapeo esperado después de sincronización
    esperado = {
        1: {'tipo_codigo': 'OT', 'descripcion': 'ORDEN DE TRABAJO'},
        2: {'tipo_codigo': 'TP', 'descripcion': 'TRABAJOS PROGRAMADOS'},
        3: {'tipo_codigo': 'GF', 'descripcion': 'GASTOS FIJOS DE LA EXPLOTACIÓN'},
    }

    print(f"\n{'ID':<5} {'MySQL Código':<10} {'MySQL Descripción':<35} {'Esperado':<10} {'Estado':<10}")
    print("-"*70)

    for id_val, exp in esperado.items():
        if id_val in mysql_data:
            mysql_row = mysql_data[id_val]
            codigo_ok = mysql_row['tipo_codigo'] == exp['tipo_codigo']
            estado = "✓ OK" if codigo_ok else "✗ ERROR"
            print(f"{id_val:<5} {mysql_row['tipo_codigo']:<10} {mysql_row['descripcion'][:33]:<35} {exp['tipo_codigo']:<10} {estado:<10}")
            if not codigo_ok:
                errores.append(f"ID {id_val}: tiene '{mysql_row['tipo_codigo']}' pero debería ser '{exp['tipo_codigo']}'")
        else:
            print(f"{id_val:<5} {'FALTA':<10} {'-':<35} {exp['tipo_codigo']:<10} {'✗ FALTA':<10}")
            errores.append(f"Falta registro con ID {id_val}")

    if errores:
        print("\n⚠ ERRORES DETECTADOS:")
        for e in errores:
            print(f"  - {e}")
        print("\n  Ejecuta primero: script/sql/sincronizar_dimensiones_access.sql")
    else:
        print("\n✓ dim_tipo_trabajo está correctamente sincronizada")

    return len(errores) == 0, errores


def verificar_dim_codigo_trabajo(cursor, datos_access: List[Dict]) -> Tuple[bool, List[str]]:
    """Verifica que dim_codigo_trabajo coincide con Access."""
    errores = []

    print("\n" + "="*70)
    print("VERIFICACIÓN: dim_codigo_trabajo (TRABAJOS PROGRAMADOS)")
    print("="*70)

    # Detectar columnas disponibles en la tabla
    cursor.execute("SHOW COLUMNS FROM dim_codigo_trabajo")
    columnas_db = [row['Field'] for row in cursor.fetchall()]

    # Determinar qué columna usar para el código
    codigo_col = None
    for posible in ['codigo', 'cod', 'cod_trabajo']:
        if posible in columnas_db:
            codigo_col = posible
            break

    # Construir query según columnas disponibles
    where_clause = "WHERE activo = 1" if 'activo' in columnas_db else ""

    if codigo_col and 'descripcion' in columnas_db:
        query = f"SELECT id, {codigo_col} as codigo, descripcion FROM dim_codigo_trabajo {where_clause} ORDER BY id"
    elif 'descripcion' in columnas_db:
        query = f"SELECT id, id as codigo, descripcion FROM dim_codigo_trabajo {where_clause} ORDER BY id"
    else:
        print("⚠ No se puede verificar: estructura de tabla desconocida")
        print(f"  Columnas encontradas: {columnas_db}")
        return True, []  # Saltar verificación

    # Obtener datos de MySQL
    cursor.execute(query)
    mysql_data = {row['id']: row for row in cursor.fetchall()}

    # Leer datos de Access
    access_data = {}
    for row in datos_access:
        try:
            id_val = int(row.get('ID', 0))
            if id_val > 0:
                access_data[id_val] = row.get('NOMBRE', '')
        except (ValueError, TypeError):
            continue

    print(f"\n{'ID':<5} {'MySQL Descripción':<40} {'Access':<40}")
    print("-"*85)

    # Comparar
    todos_ids = sorted(set(mysql_data.keys()) | set(access_data.keys()))
    for id_val in todos_ids[:22]:  # Solo los primeros 22
        mysql_desc = mysql_data.get(id_val, {}).get('descripcion', 'FALTA')[:38]
        access_desc = access_data.get(id_val, 'FALTA')[:38]

        if id_val in mysql_data and id_val in access_data:
            print(f"{id_val:<5} {mysql_desc:<40} {access_desc:<40}")
        elif id_val not in mysql_data:
            print(f"{id_val:<5} {'FALTA EN MYSQL':<40} {access_desc:<40}")
            errores.append(f"Falta en MySQL: ID {id_val}")
        else:
            print(f"{id_val:<5} {mysql_desc:<40} {'FALTA EN ACCESS':<40}")

    print(f"\nMySQL tiene {len(mysql_data)} registros activos, Access tiene {len(access_data)} registros")

    if errores:
        print("\n⚠ ERRORES DETECTADOS:")
        for e in errores:
            print(f"  - {e}")
    else:
        print("\n✓ dim_codigo_trabajo está correctamente sincronizada")

    return len(errores) == 0, errores


def verificar_dim_red(cursor) -> Tuple[bool, List[str]]:
    """Verifica que dim_red tiene los valores correctos."""
    errores = []

    print("\n" + "="*70)
    print("VERIFICACIÓN: dim_red")
    print("="*70)

    # Detectar columnas disponibles
    cursor.execute("SHOW COLUMNS FROM dim_red")
    columnas_db = [row['Field'] for row in cursor.fetchall()]

    # Determinar columna de código
    codigo_col = None
    for posible in ['codigo_red', 'codigo', 'cod', 'red']:
        if posible in columnas_db:
            codigo_col = posible
            break

    # Determinar columna de descripción
    desc_col = None
    for posible in ['descripcion', 'nombre', 'desc']:
        if posible in columnas_db:
            desc_col = posible
            break

    if not desc_col:
        print("⚠ No se puede verificar: estructura de tabla desconocida")
        print(f"  Columnas encontradas: {columnas_db}")
        return True, []

    # Construir query
    if codigo_col:
        query = f"SELECT id, {codigo_col} as codigo, {desc_col} as descripcion FROM dim_red ORDER BY id"
    else:
        query = f"SELECT id, id as codigo, {desc_col} as descripcion FROM dim_red ORDER BY id"

    cursor.execute(query)
    mysql_data = cursor.fetchall()

    esperado_desc = {
        1: 'Aducción',
        2: 'Depuración',
        3: 'Distribución',
        4: 'Otros',
        5: 'Saneamiento',
    }

    print(f"\n{'ID':<5} {'Descripción':<30} {'Estado':<10}")
    print("-"*45)

    for row in mysql_data:
        id_val = row['id']
        desc = row['descripcion'] or ''
        if id_val in esperado_desc:
            # Comparar descripción (ignorando mayúsculas/acentos)
            desc_norm = desc.lower().replace('ó', 'o').replace('á', 'a')
            exp_norm = esperado_desc[id_val].lower().replace('ó', 'o').replace('á', 'a')
            estado = "✓ OK" if desc_norm == exp_norm else "~ SIMILAR"
            print(f"{id_val:<5} {desc[:28]:<30} {estado:<10}")
        else:
            print(f"{id_val:<5} {desc[:28]:<30} {'? EXTRA':<10}")

    print(f"\nMySQL tiene {len(mysql_data)} registros")
    print("\n✓ dim_red verificada")

    return True, errores  # Siempre OK, solo informativo


# ============================================================================
# FASE 3: MAPEO GEOGRÁFICO
# ============================================================================

def cargar_municipios(cursor) -> Dict[str, Dict]:
    """Carga municipios de MySQL y crea índices para búsqueda."""
    cursor.execute("""
        SELECT id, codigo_ine, nombre, provincia_id, comarca_id
        FROM dim_municipios
        WHERE activo = 1
        ORDER BY nombre
    """)

    municipios = {}
    for row in cursor.fetchall():
        # Indexar por nombre normalizado
        nombre_norm = normalizar_texto(row['nombre'])
        municipios[nombre_norm] = row

        # También indexar por variantes comunes
        # Ej: "Ayala/Aiara" también indexar como "Ayala" y "Aiara"
        if '/' in row['nombre']:
            partes = row['nombre'].split('/')
            for parte in partes:
                municipios[normalizar_texto(parte.strip())] = row

    return municipios


def cargar_concejos(cursor) -> Dict[str, Dict]:
    """Carga concejos de MySQL y crea índices para búsqueda."""
    cursor.execute("""
        SELECT c.id, c.municipio_id, c.nombre, m.nombre as municipio_nombre
        FROM dim_concejos c
        JOIN dim_municipios m ON c.municipio_id = m.id
        WHERE c.activo = 1
        ORDER BY c.nombre
    """)

    concejos = {}
    for row in cursor.fetchall():
        nombre_norm = normalizar_texto(row['nombre'])
        concejos[nombre_norm] = row

        # Indexar variantes
        if '/' in row['nombre']:
            partes = row['nombre'].split('/')
            for parte in partes:
                concejos[normalizar_texto(parte.strip())] = row

    return concejos


def buscar_municipio(comarca: str, municipios: Dict[str, Dict]) -> Tuple[Optional[Dict], str, List[Dict]]:
    """
    Busca un municipio por nombre de comarca.
    Retorna: (municipio_encontrado, tipo_match, sugerencias)
    tipo_match: 'exacto', 'parcial', 'especial', 'no_encontrado'
    """
    if not comarca or comarca.strip() == '':
        return None, 'vacio', []

    comarca = comarca.strip()
    comarca_norm = normalizar_texto(comarca)

    # Detectar valores problemáticos
    if es_coordenada(comarca):
        return None, 'coordenada', []
    if es_direccion(comarca):
        return None, 'direccion', []

    # Buscar mapeo especial primero
    comarca_upper = comarca.upper()
    if comarca_upper in MAPEO_COMARCA_ESPECIAL:
        valor_especial = MAPEO_COMARCA_ESPECIAL[comarca_upper]
        if valor_especial is None:
            return None, 'generico', []
        comarca_norm = normalizar_texto(valor_especial)

    # Búsqueda exacta
    if comarca_norm in municipios:
        return municipios[comarca_norm], 'exacto', []

    # Búsqueda parcial (similitud > 0.8)
    sugerencias = []
    for nombre_norm, muni in municipios.items():
        sim = similitud(comarca_norm, nombre_norm)
        if sim > 0.7:
            sugerencias.append((sim, muni))

    sugerencias.sort(key=lambda x: x[0], reverse=True)
    sugerencias_top = [s[1] for s in sugerencias[:5]]

    if sugerencias and sugerencias[0][0] > 0.85:
        return sugerencias[0][1], 'parcial_alto', sugerencias_top
    elif sugerencias:
        return None, 'parcial', sugerencias_top

    return None, 'no_encontrado', []


def buscar_concejo(localizacion: str, concejos: Dict[str, Dict], municipio_id: Optional[int] = None) -> Tuple[Optional[Dict], str, List[Dict]]:
    """
    Busca un concejo por nombre de localización.
    Si se proporciona municipio_id, prioriza concejos de ese municipio.
    """
    if not localizacion or localizacion.strip() == '':
        return None, 'vacio', []

    localizacion = localizacion.strip()
    loc_norm = normalizar_texto(localizacion)

    # Detectar valores problemáticos
    if es_coordenada(localizacion):
        return None, 'coordenada', []
    if es_direccion(localizacion):
        return None, 'direccion', []

    # Búsqueda exacta
    if loc_norm in concejos:
        concejo = concejos[loc_norm]
        # Si hay municipio_id, verificar que coincide
        if municipio_id and concejo['municipio_id'] != municipio_id:
            # Buscar en el municipio correcto
            pass
        return concejo, 'exacto', []

    # Búsqueda por similitud
    sugerencias = []
    for nombre_norm, conc in concejos.items():
        sim = similitud(loc_norm, nombre_norm)
        # Priorizar si es del mismo municipio
        if municipio_id and conc['municipio_id'] == municipio_id:
            sim += 0.1
        if sim > 0.6:
            sugerencias.append((sim, conc))

    sugerencias.sort(key=lambda x: x[0], reverse=True)
    sugerencias_top = [s[1] for s in sugerencias[:5]]

    if sugerencias and sugerencias[0][0] > 0.85:
        return sugerencias[0][1], 'parcial_alto', sugerencias_top
    elif sugerencias:
        return None, 'parcial', sugerencias_top

    return None, 'no_encontrado', []


def generar_mapeo_geografico(listado_ots: List[Dict], municipios: Dict, concejos: Dict) -> Dict:
    """
    Genera mapeo geográfico analizando todos los registros de LISTADO OTS.
    Retorna diccionario con mapeos y estadísticas.
    """
    print("\n" + "="*70)
    print("FASE 3: MAPEO GEOGRÁFICO")
    print("="*70)

    # Extraer valores únicos
    comarcas_unicas = set()
    localizaciones_unicas = set()

    for row in listado_ots:
        comarca = row.get('COMARCA', '').strip()
        localizacion = row.get('LOCALIZACIÓN', row.get('LOCALIZACION', '')).strip()
        if comarca:
            comarcas_unicas.add(comarca)
        if localizacion:
            localizaciones_unicas.add(localizacion)

    print(f"\nValores únicos encontrados:")
    print(f"  - COMARCA: {len(comarcas_unicas)} valores")
    print(f"  - LOCALIZACIÓN: {len(localizaciones_unicas)} valores")

    # Mapear comarcas
    print("\n" + "-"*70)
    print("MAPEO DE COMARCAS → MUNICIPIOS")
    print("-"*70)

    mapeo_comarcas = {}
    comarcas_exactas = []
    comarcas_parciales = []
    comarcas_problemas = []

    for comarca in sorted(comarcas_unicas):
        muni, tipo, sugerencias = buscar_municipio(comarca, municipios)

        if tipo == 'exacto':
            mapeo_comarcas[comarca] = muni['id']
            comarcas_exactas.append((comarca, muni['nombre']))
        elif tipo == 'parcial_alto':
            mapeo_comarcas[comarca] = muni['id']
            comarcas_parciales.append((comarca, muni['nombre'], 'auto'))
        elif tipo in ('coordenada', 'direccion', 'generico'):
            mapeo_comarcas[comarca] = None
            comarcas_problemas.append((comarca, tipo, []))
        elif tipo == 'parcial':
            comarcas_problemas.append((comarca, tipo, sugerencias))
        else:
            comarcas_problemas.append((comarca, 'no_encontrado', sugerencias))

    print(f"\n✓ Coincidencias exactas: {len(comarcas_exactas)}")
    for comarca, muni in comarcas_exactas:
        print(f"    '{comarca}' → {muni}")

    if comarcas_parciales:
        print(f"\n~ Coincidencias parciales (auto-asignadas): {len(comarcas_parciales)}")
        for comarca, muni, _ in comarcas_parciales:
            print(f"    '{comarca}' → {muni}")

    if comarcas_problemas:
        print(f"\n⚠ Requieren revisión manual: {len(comarcas_problemas)}")
        for comarca, tipo, sugerencias in comarcas_problemas:
            print(f"\n    '{comarca}' [{tipo}]")
            if sugerencias:
                print("      Sugerencias:")
                for i, sug in enumerate(sugerencias[:3], 1):
                    print(f"        {i}. {sug['nombre']} (ID: {sug['id']})")

    # Mapear localizaciones
    print("\n" + "-"*70)
    print("MAPEO DE LOCALIZACIONES → CONCEJOS")
    print("-"*70)

    mapeo_localizaciones = {}
    loc_exactas = []
    loc_parciales = []
    loc_problemas = []

    for localizacion in sorted(localizaciones_unicas):
        conc, tipo, sugerencias = buscar_concejo(localizacion, concejos)

        if tipo == 'exacto':
            mapeo_localizaciones[localizacion] = conc['id']
            loc_exactas.append((localizacion, conc['nombre'], conc['municipio_nombre']))
        elif tipo == 'parcial_alto':
            mapeo_localizaciones[localizacion] = conc['id']
            loc_parciales.append((localizacion, conc['nombre'], conc['municipio_nombre']))
        elif tipo in ('coordenada', 'direccion', 'vacio'):
            mapeo_localizaciones[localizacion] = None
            loc_problemas.append((localizacion, tipo, []))
        elif tipo == 'parcial':
            loc_problemas.append((localizacion, tipo, sugerencias))
        else:
            loc_problemas.append((localizacion, 'no_encontrado', sugerencias))

    print(f"\n✓ Coincidencias exactas: {len(loc_exactas)}")
    for loc, conc, muni in loc_exactas[:20]:  # Mostrar solo primeros 20
        print(f"    '{loc}' → {conc} ({muni})")
    if len(loc_exactas) > 20:
        print(f"    ... y {len(loc_exactas) - 20} más")

    if loc_parciales:
        print(f"\n~ Coincidencias parciales (auto-asignadas): {len(loc_parciales)}")
        for loc, conc, muni in loc_parciales[:10]:
            print(f"    '{loc}' → {conc} ({muni})")
        if len(loc_parciales) > 10:
            print(f"    ... y {len(loc_parciales) - 10} más")

    if loc_problemas:
        print(f"\n⚠ Requieren revisión manual: {len(loc_problemas)}")
        for loc, tipo, sugerencias in loc_problemas[:15]:
            print(f"\n    '{loc}' [{tipo}]")
            if sugerencias:
                print("      Sugerencias:")
                for i, sug in enumerate(sugerencias[:3], 1):
                    print(f"        {i}. {sug['nombre']} ({sug['municipio_nombre']}, ID: {sug['id']})")
        if len(loc_problemas) > 15:
            print(f"\n    ... y {len(loc_problemas) - 15} más con problemas")

    return {
        'comarcas': mapeo_comarcas,
        'localizaciones': mapeo_localizaciones,
        'stats': {
            'comarcas_total': len(comarcas_unicas),
            'comarcas_mapeadas': len([v for v in mapeo_comarcas.values() if v]),
            'comarcas_problemas': len(comarcas_problemas),
            'loc_total': len(localizaciones_unicas),
            'loc_mapeadas': len([v for v in mapeo_localizaciones.values() if v]),
            'loc_problemas': len(loc_problemas),
        },
        'problemas_comarcas': comarcas_problemas,
        'problemas_loc': loc_problemas,
    }


def resolver_mapeos_interactivo(mapeo: Dict, municipios: Dict, concejos: Dict) -> Dict:
    """
    Permite al usuario resolver mapeos problemáticos de forma interactiva.
    """
    print("\n" + "="*70)
    print("RESOLUCIÓN INTERACTIVA DE MAPEOS")
    print("="*70)

    # Resolver comarcas problemáticas
    if mapeo['problemas_comarcas']:
        print("\n--- COMARCAS SIN MAPEAR ---")
        print("Para cada comarca, ingresa el ID del municipio o 'skip' para omitir:\n")

        for comarca, tipo, sugerencias in mapeo['problemas_comarcas']:
            if comarca in mapeo['comarcas'] and mapeo['comarcas'][comarca]:
                continue  # Ya mapeada

            print(f"\nCOMARCA: '{comarca}' [{tipo}]")
            if sugerencias:
                print("Sugerencias:")
                for i, sug in enumerate(sugerencias, 1):
                    print(f"  {i}. {sug['nombre']} (ID: {sug['id']})")

            while True:
                resp = input("Ingresa ID municipio, número de sugerencia (1-5), o 'skip': ").strip()

                if resp.lower() == 'skip':
                    mapeo['comarcas'][comarca] = None
                    break

                try:
                    num = int(resp)
                    if 1 <= num <= len(sugerencias):
                        mapeo['comarcas'][comarca] = sugerencias[num-1]['id']
                        print(f"  → Asignado a: {sugerencias[num-1]['nombre']}")
                        break
                    else:
                        # Asumir que es un ID directo
                        mapeo['comarcas'][comarca] = num
                        print(f"  → Asignado a ID: {num}")
                        break
                except ValueError:
                    print("  Entrada inválida. Usa número o 'skip'.")

    # Resolver localizaciones problemáticas
    if mapeo['problemas_loc']:
        print("\n--- LOCALIZACIONES SIN MAPEAR ---")
        print("Para cada localización, ingresa el ID del concejo o 'skip' para omitir:\n")

        count = 0
        for loc, tipo, sugerencias in mapeo['problemas_loc']:
            if loc in mapeo['localizaciones'] and mapeo['localizaciones'][loc]:
                continue

            count += 1
            if count > 20:
                print(f"\n... Hay {len(mapeo['problemas_loc']) - 20} localizaciones más sin mapear.")
                resp = input("¿Continuar resolviendo? (s/n): ").strip().lower()
                if resp != 's':
                    break
                count = 0

            print(f"\nLOCALIZACIÓN: '{loc}' [{tipo}]")
            if sugerencias:
                print("Sugerencias:")
                for i, sug in enumerate(sugerencias, 1):
                    print(f"  {i}. {sug['nombre']} - {sug['municipio_nombre']} (ID: {sug['id']})")

            while True:
                resp = input("Ingresa ID concejo, número (1-5), o 'skip': ").strip()

                if resp.lower() == 'skip':
                    mapeo['localizaciones'][loc] = None
                    break

                try:
                    num = int(resp)
                    if 1 <= num <= len(sugerencias):
                        mapeo['localizaciones'][loc] = sugerencias[num-1]['id']
                        print(f"  → Asignado a: {sugerencias[num-1]['nombre']}")
                        break
                    else:
                        mapeo['localizaciones'][loc] = num
                        print(f"  → Asignado a ID: {num}")
                        break
                except ValueError:
                    print("  Entrada inválida. Usa número o 'skip'.")

    return mapeo


# ============================================================================
# FASE 1: LIMPIEZA DE TABLAS
# ============================================================================

def limpiar_tablas_hechos(cursor, conn) -> bool:
    """Elimina todos los datos de las tablas de hechos."""
    print("\n" + "="*70)
    print("FASE 1: LIMPIEZA DE TABLAS DE HECHOS")
    print("="*70)

    # Contar registros antes
    # Orden: primero hijos (certificacion, presupuesto), luego padre (partes)
    # para respetar las FK incluso con FK_CHECKS deshabilitado
    tablas = ['tbl_part_certificacion', 'tbl_part_presupuesto', 'tbl_partes']

    print("\nRegistros actuales:")
    for tabla in tablas:
        cursor.execute(f"SELECT COUNT(*) as count FROM {tabla}")
        count = cursor.fetchone()['count']
        print(f"  {tabla}: {count} registros")

    confirmacion = input("\n¿Eliminar todos estos registros? (escribir 'CONFIRMAR'): ").strip()

    if confirmacion != 'CONFIRMAR':
        print("Operación cancelada.")
        return False

    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

    for tabla in tablas:
        cursor.execute(f"DELETE FROM {tabla}")
        print(f"  ✓ {tabla} limpiada ({cursor.rowcount} registros eliminados)")

    # Reiniciar auto_increment
    for tabla in tablas:
        cursor.execute(f"ALTER TABLE {tabla} AUTO_INCREMENT = 1")

    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

    conn.commit()
    print("\n✓ Tablas de hechos limpiadas correctamente")
    return True


# ============================================================================
# FASE 4: IMPORTACIÓN DE DATOS
# ============================================================================

def convertir_fecha(fecha_str: str) -> Optional[str]:
    """Convierte fecha de Access a formato MySQL."""
    if not fecha_str or fecha_str.strip() == '':
        return None

    # Intentar varios formatos
    formatos = [
        '%m/%d/%y %H:%M:%S',
        '%d/%m/%Y %H:%M:%S',
        '%Y-%m-%d %H:%M:%S',
        '%m/%d/%y',
        '%d/%m/%Y',
        '%Y-%m-%d',
    ]

    for fmt in formatos:
        try:
            dt = datetime.strptime(fecha_str.strip(), fmt)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            continue

    return None


def importar_listado_ots(cursor, conn, listado_ots: List[Dict], mapeo: Dict) -> int:
    """
    Importa LISTADO OTS → tbl_partes
    """
    print("\n" + "-"*70)
    print("Importando LISTADO OTS → tbl_partes")
    print("-"*70)

    insertados = 0
    errores = 0

    # Preparar query de inserción
    insert_sql = """
        INSERT INTO tbl_partes (
            codigo, descripcion, tipo_trabajo_id, cod_trabajo_id,
            red_id, municipio_id, concejo_id, estado_id,
            fecha_encargo, fecha_finalizacion, creado_en
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW()
        )
    """

    for row in listado_ots:
        try:
            # Extraer campos
            codigo = row.get('COD TRABAJO', row.get('COD_TRABAJO', '')).strip()
            descripcion = row.get('OT', row.get('DESCRIPCION', '')).strip()

            # Tipo de trabajo
            tipo_trabajo_raw = row.get('TIPO DE TRABAJOS', row.get('TIPO_DE_TRABAJOS', ''))
            try:
                tipo_trabajo_id = int(tipo_trabajo_raw) if tipo_trabajo_raw else None
                tipo_trabajo_id = MAPEO_TIPO_TRABAJO.get(tipo_trabajo_id, tipo_trabajo_id)
            except (ValueError, TypeError):
                tipo_trabajo_id = None

            # Código de trabajo (trabajos programados)
            cod_trabajo_raw = row.get('TRABAJOS PROGRAMADOS', row.get('TRABAJOS_PROGRAMADOS', ''))
            try:
                cod_trabajo_id = int(cod_trabajo_raw) if cod_trabajo_raw else None
            except (ValueError, TypeError):
                cod_trabajo_id = None

            # Red
            red_texto = row.get('RED', '').strip().upper()
            red_id = MAPEO_RED.get(red_texto)

            # Municipio (desde COMARCA)
            comarca = row.get('COMARCA', '').strip()
            municipio_id = mapeo['comarcas'].get(comarca)

            # Concejo (desde LOCALIZACIÓN)
            localizacion = row.get('LOCALIZACIÓN', row.get('LOCALIZACION', '')).strip()
            concejo_id = mapeo['localizaciones'].get(localizacion)

            # Estado (por defecto = 1, pendiente)
            estado_id = 1

            # Fechas
            fecha_encargo = convertir_fecha(row.get('FECHA_ENCARGO', row.get('FECHA ENCARGO', '')))
            fecha_finalizacion = convertir_fecha(row.get('FECHA_FINALIZACION', row.get('FECHA FINALIZACION', '')))

            # Insertar
            cursor.execute(insert_sql, (
                codigo, descripcion, tipo_trabajo_id, cod_trabajo_id,
                red_id, municipio_id, concejo_id, estado_id,
                fecha_encargo, fecha_finalizacion
            ))
            insertados += 1

        except Exception as e:
            errores += 1
            if errores <= 5:
                print(f"  Error en registro: {row.get('COD TRABAJO', '?')}: {e}")

    conn.commit()
    print(f"\n✓ Importados: {insertados} partes")
    if errores:
        print(f"⚠ Errores: {errores}")

    return insertados


def importar_mediciones_ots(cursor, conn, mediciones: List[Dict], partes_map: Dict[str, int]) -> int:
    """
    Importa MEDICIONES OTS → tbl_part_presupuesto
    """
    print("\n" + "-"*70)
    print("Importando MEDICIONES OTS → tbl_part_presupuesto")
    print("-"*70)

    # Primero, construir mapeo de código parte → id
    cursor.execute("SELECT id, codigo FROM tbl_partes")
    partes_db = {row['codigo']: row['id'] for row in cursor.fetchall()}

    # Cargar precios para buscar por código
    cursor.execute("SELECT id, codigo FROM tbl_pres_precios")
    precios_db = {row['codigo']: row['id'] for row in cursor.fetchall()}

    insertados = 0
    errores = 0
    partes_no_encontrados = set()

    insert_sql = """
        INSERT INTO tbl_part_presupuesto (
            parte_id, precio_id, cantidad, precio_unitario,
            precio_total, fecha_medicion, creado_en
        ) VALUES (
            %s, %s, %s, %s, %s, %s, NOW()
        )
    """

    for row in mediciones:
        try:
            # Buscar parte por código
            cod_trabajo = row.get('COD TRABAJO', row.get('COD_TRABAJO', '')).strip()
            parte_id = partes_db.get(cod_trabajo)

            if not parte_id:
                if cod_trabajo not in partes_no_encontrados:
                    partes_no_encontrados.add(cod_trabajo)
                continue

            # Buscar precio por código
            cod_precio = row.get('CODIGO', row.get('CÓDIGO', '')).strip()
            precio_id = precios_db.get(cod_precio)

            # Cantidad y precios
            cantidad_str = row.get('CANTIDAD', '0').replace(',', '.')
            try:
                cantidad = float(cantidad_str) if cantidad_str else 0.0
            except ValueError:
                cantidad = 0.0

            precio_unit_str = row.get('PRECIO UNITARIO', row.get('PRECIO_UNITARIO', '0')).replace(',', '.')
            try:
                precio_unitario = float(precio_unit_str) if precio_unit_str else 0.0
            except ValueError:
                precio_unitario = 0.0

            precio_total = cantidad * precio_unitario

            # Fecha
            fecha_medicion = convertir_fecha(row.get('FECHA', ''))

            cursor.execute(insert_sql, (
                parte_id, precio_id, cantidad, precio_unitario,
                precio_total, fecha_medicion
            ))
            insertados += 1

        except Exception as e:
            errores += 1
            if errores <= 5:
                print(f"  Error en medición: {e}")

    conn.commit()

    print(f"\n✓ Importadas: {insertados} mediciones")
    if partes_no_encontrados:
        print(f"⚠ Partes no encontrados: {len(partes_no_encontrados)}")
        if len(partes_no_encontrados) <= 10:
            for cod in sorted(partes_no_encontrados):
                print(f"    - {cod}")
    if errores:
        print(f"⚠ Errores: {errores}")

    return insertados


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Importar datos de Access a MySQL para HydroFlow Manager',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplo de uso:
  python importar_access_mysql.py \\
    --access "./INFORME TIPO/APLICACION CERTIFICACIONES UTE REDES URBIDE.accdb" \\
    --host localhost \\
    --user root \\
    --password mipassword \\
    --database hydroflow_urbide
        """
    )

    parser.add_argument('--access', required=True, help='Ruta al archivo .accdb de Access')
    parser.add_argument('--host', default='localhost', help='Host MySQL (default: localhost)')
    parser.add_argument('--port', type=int, default=3306, help='Puerto MySQL (default: 3306)')
    parser.add_argument('--user', required=True, help='Usuario MySQL')
    parser.add_argument('--password', required=True, help='Contraseña MySQL')
    parser.add_argument('--database', required=True, help='Nombre de la base de datos MySQL')
    parser.add_argument('--solo-verificar', action='store_true', help='Solo verificar, no importar')
    parser.add_argument('--no-interactivo', action='store_true', help='No pedir confirmaciones')

    args = parser.parse_args()

    # Verificar que el archivo existe
    if not os.path.exists(args.access):
        print(f"ERROR: No se encuentra el archivo: {args.access}")
        sys.exit(1)

    # Verificar dependencias según el SO
    import platform
    if platform.system() == 'Windows':
        try:
            import pyodbc
            # Verificar que el driver de Access está disponible
            drivers = [d for d in pyodbc.drivers() if 'Access' in d]
            if not drivers:
                print("ERROR: No se encontró el driver de Microsoft Access.")
                print("Instala Microsoft Access Database Engine desde:")
                print("  https://www.microsoft.com/en-us/download/details.aspx?id=54920")
                sys.exit(1)
        except ImportError:
            print("ERROR: pyodbc no está instalado.")
            print("Instálalo con: pip install pyodbc")
            sys.exit(1)
    else:
        try:
            subprocess.run(['mdb-ver', args.access], capture_output=True, check=True)
        except FileNotFoundError:
            print("ERROR: mdb-tools no está instalado.")
            print("Instálalo con: sudo apt install mdb-tools")
            sys.exit(1)
        except subprocess.CalledProcessError:
            print(f"ERROR: No se puede leer el archivo Access: {args.access}")
            sys.exit(1)

    print("="*70)
    print("IMPORTACIÓN ACCESS → MySQL")
    print("="*70)
    print(f"Archivo Access: {args.access}")
    print(f"Base de datos MySQL: {args.database}@{args.host}:{args.port}")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Conectar a MySQL
    print("\nConectando a MySQL...")
    conn, cursor = conectar_mysql(args.host, args.port, args.user, args.password, args.database)
    print("✓ Conexión establecida")

    # Leer tablas de Access
    print("\nLeyendo tablas de Access...")

    trabajos_prog = leer_tabla_access(args.access, 'TRABAJOS PROGRAMADOS')
    print(f"  TRABAJOS PROGRAMADOS: {len(trabajos_prog)} registros")

    listado_ots = leer_tabla_access(args.access, 'LISTADO OTS')
    print(f"  LISTADO OTS: {len(listado_ots)} registros")

    mediciones_ots = leer_tabla_access(args.access, 'MEDICIONES OTS')
    print(f"  MEDICIONES OTS: {len(mediciones_ots)} registros")

    # =========================================================================
    # FASE 1: Limpiar tablas de hechos
    # =========================================================================
    # IMPORTANTE: Limpiar PRIMERO las tablas de hechos para liberar las FK
    # hacia las dimensiones. Esto permite modificar las dimensiones después.

    if args.solo_verificar:
        print("\n[Modo solo-verificar: saltando limpieza de tablas]")
    elif not args.no_interactivo:
        if not limpiar_tablas_hechos(cursor, conn):
            sys.exit(1)
    else:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        for tabla in ['tbl_part_certificacion', 'tbl_part_presupuesto', 'tbl_partes']:
            cursor.execute(f"DELETE FROM {tabla}")
            cursor.execute(f"ALTER TABLE {tabla} AUTO_INCREMENT = 1")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        print("\n✓ Tablas de hechos limpiadas (modo no-interactivo)")

    # =========================================================================
    # FASE 2: Verificar/sincronizar dimensiones
    # =========================================================================
    # Ahora que las tablas de hechos están vacías, se pueden modificar
    # las dimensiones sin problemas de FK.

    ok_tipo, _ = verificar_dim_tipo_trabajo(cursor, [])
    ok_codigo, _ = verificar_dim_codigo_trabajo(cursor, trabajos_prog)
    ok_red, _ = verificar_dim_red(cursor)

    if not (ok_tipo and ok_codigo and ok_red):
        print("\n" + "="*70)
        print("⚠ HAY PROBLEMAS CON LAS DIMENSIONES")
        print("="*70)
        print("Las tablas de hechos ya están limpias, puedes sincronizar ahora:")
        print("  mysql -u [user] -p [database] < script/sql/sincronizar_dimensiones_access.sql")

        if not args.no_interactivo:
            resp = input("\n¿Continuar de todos modos? (s/n): ").strip().lower()
            if resp != 's':
                sys.exit(1)

    if args.solo_verificar:
        print("\n✓ Verificación completada (modo solo-verificar)")
        sys.exit(0)

    # =========================================================================
    # FASE 3: Mapeo geográfico
    # =========================================================================

    municipios = cargar_municipios(cursor)
    print(f"\nMunicipios cargados: {len(municipios)} (con variantes)")

    concejos = cargar_concejos(cursor)
    print(f"Concejos cargados: {len(concejos)} (con variantes)")

    mapeo = generar_mapeo_geografico(listado_ots, municipios, concejos)

    # Mostrar resumen
    print("\n" + "-"*70)
    print("RESUMEN DE MAPEO GEOGRÁFICO")
    print("-"*70)
    print(f"Comarcas: {mapeo['stats']['comarcas_mapeadas']}/{mapeo['stats']['comarcas_total']} mapeadas")
    print(f"Localizaciones: {mapeo['stats']['loc_mapeadas']}/{mapeo['stats']['loc_total']} mapeadas")

    # Resolver interactivamente si hay problemas
    if not args.no_interactivo and (mapeo['stats']['comarcas_problemas'] > 0 or mapeo['stats']['loc_problemas'] > 0):
        resp = input("\n¿Resolver mapeos problemáticos interactivamente? (s/n): ").strip().lower()
        if resp == 's':
            mapeo = resolver_mapeos_interactivo(mapeo, municipios, concejos)

    # =========================================================================
    # FASE 4: Importar datos
    # =========================================================================

    print("\n" + "="*70)
    print("FASE 4: IMPORTACIÓN DE DATOS")
    print("="*70)

    partes_importados = importar_listado_ots(cursor, conn, listado_ots, mapeo)
    mediciones_importadas = importar_mediciones_ots(cursor, conn, mediciones_ots, {})

    # =========================================================================
    # RESUMEN FINAL
    # =========================================================================

    print("\n" + "="*70)
    print("IMPORTACIÓN COMPLETADA")
    print("="*70)
    print(f"  Partes importados: {partes_importados}")
    print(f"  Mediciones importadas: {mediciones_importadas}")
    print(f"\nMapeo geográfico:")
    print(f"  Comarcas mapeadas: {mapeo['stats']['comarcas_mapeadas']}/{mapeo['stats']['comarcas_total']}")
    print(f"  Localizaciones mapeadas: {mapeo['stats']['loc_mapeadas']}/{mapeo['stats']['loc_total']}")

    # Verificación final
    print("\nVerificación final:")
    cursor.execute("SELECT COUNT(*) as c FROM tbl_partes")
    print(f"  tbl_partes: {cursor.fetchone()['c']} registros")
    cursor.execute("SELECT COUNT(*) as c FROM tbl_part_presupuesto")
    print(f"  tbl_part_presupuesto: {cursor.fetchone()['c']} registros")

    cursor.close()
    conn.close()

    print("\n✓ Proceso finalizado correctamente")


if __name__ == '__main__':
    main()
