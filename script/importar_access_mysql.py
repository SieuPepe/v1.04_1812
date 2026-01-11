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

MAPEO GEOGRÁFICO:
  - COMARCA (Access) → Municipio (MySQL dim_municipios)
  - LOCALIZACIÓN (Access) → Concejo (MySQL dim_concejos)
  - Comarca MySQL: Se deriva automáticamente del municipio encontrado

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

MAPEO_TIPO_TRABAJO = {
    1: 1,  # ORDEN DE TRABAJO → OT
    2: 2,  # TRABAJOS PROGRAMADOS → TP
    3: 3,  # GASTOS FIJOS → GF
}

MAPEO_RED = {
    'ADUCCIÓN': 1, 'ADUCCION': 1,
    'DEPURACIÓN': 2, 'DEPURACION': 2,
    'DISTRIBUCIÓN': 3, 'DISTRIBUCION': 3,
    'OTROS': 4,
    'SANEAMIENTO': 5,
}

# ============================================================================
# UTILIDADES
# ============================================================================

def normalizar_texto(texto: str) -> str:
    """Normaliza texto para comparación: sin acentos, minúsculas, sin espacios extra."""
    if not texto:
        return ''
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    texto = texto.lower().strip()
    texto = re.sub(r'\s+', ' ', texto)
    return texto


def similitud(a: str, b: str) -> float:
    """Calcula similitud entre dos strings (0.0 a 1.0)."""
    return SequenceMatcher(None, normalizar_texto(a), normalizar_texto(b)).ratio()


def leer_tabla_access(accdb_path: str, tabla: str) -> List[Dict]:
    """Lee una tabla de Access y devuelve lista de diccionarios."""
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
        print("ERROR: pyodbc no está instalado. Instálalo con: pip install pyodbc")
        sys.exit(1)

    try:
        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            f'DBQ={accdb_path};'
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM [{tabla}]')
        columns = [column[0] for column in cursor.description]
        rows = []
        for row in cursor.fetchall():
            row_dict = {}
            for i, col in enumerate(columns):
                value = row[i]
                row_dict[col] = str(value) if value is not None else ''
            rows.append(row_dict)
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"Error leyendo tabla {tabla}: {e}")
        return []


def _leer_tabla_access_linux(accdb_path: str, tabla: str) -> List[Dict]:
    """Lee tabla de Access usando mdb-tools (Linux)."""
    try:
        result = subprocess.run(
            ['mdb-export', accdb_path, tabla],
            capture_output=True, text=True, check=True
        )
        import csv
        from io import StringIO
        reader = csv.DictReader(StringIO(result.stdout))
        return list(reader)
    except FileNotFoundError:
        print("ERROR: mdb-tools no está instalado. Instálalo con: sudo apt install mdb-tools")
        sys.exit(1)
    except Exception as e:
        print(f"Error leyendo tabla {tabla}: {e}")
        return []


def conectar_mysql(host: str, port: int, user: str, password: str, database: str):
    """Conecta a MySQL y devuelve conexión y cursor."""
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host=host, port=port, user=user, password=password,
            database=database, charset='utf8mb4'
        )
        return conn, conn.cursor(dictionary=True)
    except ImportError:
        print("ERROR: mysql-connector-python no está instalado.")
        sys.exit(1)


# ============================================================================
# CARGA DE DATOS GEOGRÁFICOS
# ============================================================================

def cargar_comarcas(cursor, incluir_especiales: bool = False) -> List[Dict]:
    """Carga comarcas de MySQL. Si incluir_especiales=True, incluye Todo/Varios."""
    if incluir_especiales:
        cursor.execute("""
            SELECT id, comarca_codigo, comarca_nombre
            FROM dim_comarcas
            ORDER BY
                CASE WHEN comarca_nombre LIKE 'Todo%' THEN 0
                     WHEN comarca_nombre LIKE 'Varios%' THEN 1
                     ELSE 2 END,
                comarca_nombre
        """)
    else:
        cursor.execute("""
            SELECT id, comarca_codigo, comarca_nombre
            FROM dim_comarcas
            WHERE comarca_nombre NOT LIKE 'Todo%'
              AND comarca_nombre NOT LIKE 'Varios%'
            ORDER BY comarca_nombre
        """)
    return cursor.fetchall()


def cargar_municipios(cursor, incluir_especiales: bool = False) -> List[Dict]:
    """Carga municipios de MySQL con su comarca. Si incluir_especiales=True, incluye Todo/Varios."""
    if incluir_especiales:
        cursor.execute("""
            SELECT m.id, m.codigo_ine, m.municipio_nombre, m.comarca_id, c.comarca_nombre
            FROM dim_municipios m
            JOIN dim_comarcas c ON m.comarca_id = c.id
            WHERE m.activo = 1
            ORDER BY
                CASE WHEN m.municipio_nombre LIKE 'Todo%' THEN 0
                     WHEN m.municipio_nombre LIKE 'Varios%' THEN 1
                     ELSE 2 END,
                m.municipio_nombre
        """)
    else:
        cursor.execute("""
            SELECT m.id, m.codigo_ine, m.municipio_nombre, m.comarca_id, c.comarca_nombre
            FROM dim_municipios m
            JOIN dim_comarcas c ON m.comarca_id = c.id
            WHERE m.activo = 1
              AND m.municipio_nombre NOT LIKE 'Todo%'
              AND m.municipio_nombre NOT LIKE 'Varios%'
            ORDER BY m.municipio_nombre
        """)
    return cursor.fetchall()


def cargar_concejos(cursor, incluir_especiales: bool = False) -> List[Dict]:
    """Carga concejos de MySQL con su municipio. Si incluir_especiales=True, incluye Varios."""
    if incluir_especiales:
        cursor.execute("""
            SELECT c.id, c.municipio_id, c.nombre, m.municipio_nombre
            FROM dim_concejos c
            JOIN dim_municipios m ON c.municipio_id = m.id
            WHERE c.activo = 1
            ORDER BY
                CASE WHEN c.nombre LIKE 'Todo%' THEN 0
                     WHEN c.nombre LIKE 'Varios%' THEN 1
                     ELSE 2 END,
                c.nombre
        """)
    else:
        cursor.execute("""
            SELECT c.id, c.municipio_id, c.nombre, m.municipio_nombre
            FROM dim_concejos c
            JOIN dim_municipios m ON c.municipio_id = m.id
            WHERE c.activo = 1
              AND c.nombre NOT LIKE 'Varios%'
            ORDER BY c.nombre
        """)
    return cursor.fetchall()


def buscar_mejor_coincidencia(texto: str, lista: List[Dict], campo_nombre: str) -> List[Tuple[float, Dict]]:
    """Busca las mejores coincidencias por similitud."""
    if not texto:
        return []

    texto_norm = normalizar_texto(texto)
    resultados = []

    for item in lista:
        nombre = item.get(campo_nombre, '')
        if not nombre:
            continue

        # Calcular similitud
        nombre_norm = normalizar_texto(nombre)
        sim = similitud(texto_norm, nombre_norm)

        # También buscar coincidencia parcial
        if texto_norm in nombre_norm or nombre_norm in texto_norm:
            sim = max(sim, 0.8)

        # Buscar en variantes (si tiene /)
        if '/' in nombre:
            for parte in nombre.split('/'):
                sim_parte = similitud(texto_norm, normalizar_texto(parte.strip()))
                sim = max(sim, sim_parte)

        if sim > 0.5:
            resultados.append((sim, item))

    resultados.sort(key=lambda x: x[0], reverse=True)
    return resultados[:5]


# ============================================================================
# FASE 3: MAPEO GEOGRÁFICO INTERACTIVO
# ============================================================================

def mostrar_registro_access(registro: Dict):
    """Muestra información del registro de Access."""
    print("\n" + "="*80)
    print("REGISTRO DE ACCESS SIN COINCIDENCIA")
    print("="*80)

    id_val = registro.get('ID', registro.get('Id', '?'))
    titulo = registro.get('TITULO OT', registro.get('OT', ''))[:60]
    descripcion = registro.get('DESCRIPCION OT', registro.get('DESCRIPCION', ''))[:80]
    localizacion = registro.get('LOCALIZACIÓN', registro.get('LOCALIZACION', ''))
    comarca = registro.get('COMARCA', '')

    print(f"  [ID]: {id_val}")
    print(f"  [TITULO OT]: {titulo}")
    print(f"  [DESCRIPCION OT]: {descripcion}")
    print(f"  [LOCALIZACIÓN]: {localizacion}")
    print(f"  [COMARCA]: {comarca}")


def mostrar_sugerencias(sugerencias: List[Tuple[float, Dict]], campo_nombre: str, titulo: str):
    """Muestra sugerencias numeradas."""
    print(f"\n  {titulo}:")
    if not sugerencias:
        print("    (Sin sugerencias)")
        return

    for i, (sim, item) in enumerate(sugerencias, 1):
        nombre = item.get(campo_nombre, '?')
        id_val = item.get('id', '?')
        extra = ""
        if 'comarca_nombre' in item and campo_nombre != 'comarca_nombre':
            extra = f" (Comarca: {item['comarca_nombre']})"
        elif 'municipio_nombre' in item and campo_nombre != 'municipio_nombre':
            extra = f" (Municipio: {item['municipio_nombre']})"
        print(f"    {i}. {nombre} [ID: {id_val}]{extra} - Similitud: {sim:.0%}")


def seleccionar_de_lista(lista: List[Dict], campo_nombre: str, titulo: str, filtro_campo: str = None, filtro_valor: int = None) -> Optional[Dict]:
    """Permite al usuario seleccionar un elemento de la lista completa."""
    # Filtrar si es necesario
    if filtro_campo and filtro_valor:
        lista_filtrada = [item for item in lista if item.get(filtro_campo) == filtro_valor]
    else:
        lista_filtrada = lista

    if not lista_filtrada:
        print(f"    No hay {titulo} disponibles con el filtro actual.")
        return None

    print(f"\n  Selecciona {titulo}:")
    print("-" * 60)

    # Mostrar en páginas de 20
    pagina = 0
    items_por_pagina = 20
    total_paginas = (len(lista_filtrada) - 1) // items_por_pagina + 1

    while True:
        inicio = pagina * items_por_pagina
        fin = min(inicio + items_por_pagina, len(lista_filtrada))

        for i, item in enumerate(lista_filtrada[inicio:fin], inicio + 1):
            nombre = item.get(campo_nombre, '?')
            id_val = item.get('id', '?')
            extra = ""
            if 'comarca_nombre' in item and campo_nombre != 'comarca_nombre':
                extra = f" ({item['comarca_nombre']})"
            print(f"    {i}. {nombre} [ID: {id_val}]{extra}")

        print(f"\n  Página {pagina + 1}/{total_paginas}")
        print("  Opciones: [número] seleccionar | [n] siguiente | [p] anterior | [q] cancelar")

        resp = input("  > ").strip().lower()

        if resp == 'q':
            return None
        elif resp == 'n' and pagina < total_paginas - 1:
            pagina += 1
        elif resp == 'p' and pagina > 0:
            pagina -= 1
        else:
            try:
                num = int(resp)
                if 1 <= num <= len(lista_filtrada):
                    return lista_filtrada[num - 1]
            except ValueError:
                pass
            print("  Opción inválida.")


def procesar_registro_interactivo(registro: Dict, comarcas: List[Dict], municipios: List[Dict], concejos: List[Dict],
                                   comarcas_todas: List[Dict] = None, municipios_todos: List[Dict] = None,
                                   concejos_todos: List[Dict] = None) -> Optional[Dict]:
    """
    Procesa un registro de forma interactiva y devuelve el mapeo geográfico.

    Lógica de mapeo:
    - COMARCA (Access) → Municipio (MySQL)
    - LOCALIZACIÓN (Access) → Concejo (MySQL)
    - Comarca MySQL se deriva del municipio

    Args:
        comarcas, municipios, concejos: Listas filtradas (sin Todo/Varios) para sugerencias automáticas
        comarcas_todas, municipios_todos, concejos_todos: Listas completas para selección manual
    """
    # Usar listas completas para selección manual si están disponibles
    comarcas_manual = comarcas_todas if comarcas_todas else comarcas
    municipios_manual = municipios_todos if municipios_todos else municipios
    concejos_manual = concejos_todos if concejos_todos else concejos
    localizacion = registro.get('LOCALIZACIÓN', registro.get('LOCALIZACION', '')).strip()
    comarca_access = registro.get('COMARCA', '').strip()

    mostrar_registro_access(registro)

    # Buscar sugerencias para municipio (desde COMARCA del Access)
    sug_municipios = buscar_mejor_coincidencia(comarca_access, municipios, 'municipio_nombre')

    # Buscar sugerencias para concejo (desde LOCALIZACIÓN del Access)
    sug_concejos = buscar_mejor_coincidencia(localizacion, concejos, 'nombre')

    print("\n  SUGERENCIAS BASADAS EN LOS DATOS:")
    print("\n  Opción | Municipio (de COMARCA) | Concejo (de LOCALIZACIÓN) | Comarca MySQL")
    print("  " + "-"*80)

    opciones = []
    num_opcion = 1

    # Generar opciones combinando municipio + concejo
    for sim_m, municipio in sug_municipios[:5]:
        # Buscar concejos que coincidan y pertenezcan a este municipio
        for sim_c, concejo in sug_concejos[:5]:
            if concejo['municipio_id'] == municipio['id']:
                # ¡Match perfecto! Municipio y concejo coinciden
                print(f"  {num_opcion:^6} | {municipio['municipio_nombre'][:22]:<22} | {concejo['nombre'][:25]:<25} | {municipio['comarca_nombre'][:15]}")
                opciones.append({
                    'municipio': municipio,
                    'concejo': concejo
                })
                num_opcion += 1

    # Si no hay match municipio-concejo, mostrar solo opciones de municipio con "Todo X"
    if not opciones:
        print("\n  (No hay coincidencia directa municipio-concejo, mostrando municipios)")
        for sim_m, municipio in sug_municipios[:5]:
            # Buscar concejo "Todo X" para este municipio
            concejo_todo = None
            for c in concejos:
                if c['municipio_id'] == municipio['id'] and c['nombre'].startswith('Todo '):
                    concejo_todo = c
                    break

            concejo_nombre = concejo_todo['nombre'] if concejo_todo else f"Todo {municipio['municipio_nombre']}"
            print(f"  {num_opcion:^6} | {municipio['municipio_nombre'][:22]:<22} | {concejo_nombre[:25]:<25} | {municipio['comarca_nombre'][:15]}")
            opciones.append({
                'municipio': municipio,
                'concejo': concejo_todo,
                'concejo_nombre': concejo_nombre
            })
            num_opcion += 1

    # Mostrar sugerencias adicionales si no hay opciones
    if not opciones:
        print("\n  No se encontraron coincidencias.")
        mostrar_sugerencias(sug_municipios, 'municipio_nombre', "Sugerencias de Municipio (desde COMARCA)")
        mostrar_sugerencias(sug_concejos, 'nombre', "Sugerencias de Concejo (desde LOCALIZACIÓN)")

    # Opción de selección manual (siguiente número después de las opciones)
    opcion_manual = num_opcion
    print(f"\n  {opcion_manual}. Ninguna de las anteriores (selección manual)")
    print(f"  0. Saltar este registro")

    while True:
        try:
            resp = input("\n  Selecciona opción: ").strip()

            if resp == '0':
                return None

            num = int(resp)

            if 1 <= num < opcion_manual and num <= len(opciones):
                opcion = opciones[num - 1]
                municipio = opcion['municipio']
                concejo = opcion.get('concejo')
                concejo_nombre = opcion.get('concejo_nombre') or (concejo['nombre'] if concejo else f"Todo {municipio['municipio_nombre']}")

                print(f"\n  ✓ Seleccionado:")
                print(f"    Comarca: {municipio['comarca_nombre']}")
                print(f"    Municipio: {municipio['municipio_nombre']}")
                print(f"    Concejo: {concejo_nombre}")

                return {
                    'comarca_id': municipio['comarca_id'],
                    'comarca_nombre': municipio['comarca_nombre'],
                    'municipio_id': municipio['id'],
                    'municipio_nombre': municipio['municipio_nombre'],
                    'concejo_id': concejo['id'] if concejo else None,
                    'concejo_nombre': concejo_nombre
                }

            elif num == opcion_manual:  # Selección manual
                print("\n  === SELECCIÓN MANUAL ===")

                # 1. Seleccionar Comarca (usando lista completa con Todo/Varios)
                comarca_sel = seleccionar_de_lista(comarcas_manual, 'comarca_nombre', 'COMARCA')
                if not comarca_sel:
                    continue

                # 2. Seleccionar Municipio (filtrado por comarca, usando lista completa)
                municipio_sel = seleccionar_de_lista(
                    municipios_manual, 'municipio_nombre', 'MUNICIPIO',
                    filtro_campo='comarca_id', filtro_valor=comarca_sel['id']
                )
                if not municipio_sel:
                    continue

                # 3. Seleccionar Concejo (filtrado por municipio, usando lista completa)
                concejos_municipio = [c for c in concejos_manual if c['municipio_id'] == municipio_sel['id']]

                concejo_id = None
                concejo_nombre = f"Todo {municipio_sel['municipio_nombre']}"

                if concejos_municipio:
                    concejo_sel = seleccionar_de_lista(concejos_municipio, 'nombre', 'CONCEJO')
                    if concejo_sel:
                        concejo_nombre = concejo_sel['nombre']
                        concejo_id = concejo_sel['id']
                    else:
                        # Buscar "Todo X"
                        for c in concejos_municipio:
                            if c['nombre'].startswith('Todo '):
                                concejo_id = c['id']
                                concejo_nombre = c['nombre']
                                break

                print(f"\n  ✓ Selección manual completada:")
                print(f"    Comarca: {comarca_sel['comarca_nombre']}")
                print(f"    Municipio: {municipio_sel['municipio_nombre']}")
                print(f"    Concejo: {concejo_nombre}")

                return {
                    'comarca_id': comarca_sel['id'],
                    'comarca_nombre': comarca_sel['comarca_nombre'],
                    'municipio_id': municipio_sel['id'],
                    'municipio_nombre': municipio_sel['municipio_nombre'],
                    'concejo_id': concejo_id,
                    'concejo_nombre': concejo_nombre
                }
            else:
                print("  Opción inválida.")

        except ValueError:
            print("  Entrada inválida.")


def procesar_mapeo_geografico(listado_ots: List[Dict], comarcas: List[Dict], municipios: List[Dict], concejos: List[Dict],
                               comarcas_todas: List[Dict] = None, municipios_todos: List[Dict] = None,
                               concejos_todos: List[Dict] = None) -> Tuple[Dict, List[Dict]]:
    """
    Procesa el mapeo geográfico de todos los registros.

    Lógica de mapeo:
    - COMARCA (Access) → Municipio (MySQL)
    - LOCALIZACIÓN (Access) → Concejo (MySQL)
    - Comarca MySQL se deriva del municipio encontrado

    Args:
        comarcas, municipios, concejos: Listas filtradas para matching automático
        comarcas_todas, municipios_todos, concejos_todos: Listas completas para selección manual

    Retorna: (mapeo_por_registro, correcciones_realizadas)
    """
    print("\n" + "="*80)
    print("FASE 3: MAPEO GEOGRÁFICO")
    print("="*80)

    mapeo = {}  # id_registro -> {comarca_id, municipio_id, concejo_id}
    correctos = []
    problematicos = []
    correcciones = []  # Lista de correcciones para mostrar al final

    # Crear índices para búsqueda rápida de municipios por nombre
    municipios_por_nombre = {}
    for m in municipios:
        nombre_norm = normalizar_texto(m['municipio_nombre'])
        municipios_por_nombre[nombre_norm] = m
        if '/' in m['municipio_nombre']:
            for parte in m['municipio_nombre'].split('/'):
                municipios_por_nombre[normalizar_texto(parte.strip())] = m

    # Crear índices para búsqueda rápida de concejos por nombre y por municipio
    concejos_por_nombre = {}
    concejos_por_municipio = {}
    for c in concejos:
        # Índice por nombre
        nombre_norm = normalizar_texto(c['nombre'])
        if nombre_norm not in concejos_por_nombre:
            concejos_por_nombre[nombre_norm] = []
        concejos_por_nombre[nombre_norm].append(c)
        if '/' in c['nombre']:
            for parte in c['nombre'].split('/'):
                parte_norm = normalizar_texto(parte.strip())
                if parte_norm not in concejos_por_nombre:
                    concejos_por_nombre[parte_norm] = []
                concejos_por_nombre[parte_norm].append(c)

        # Índice por municipio
        muni_id = c['municipio_id']
        if muni_id not in concejos_por_municipio:
            concejos_por_municipio[muni_id] = []
        concejos_por_municipio[muni_id].append(c)

    print(f"\nProcesando {len(listado_ots)} registros...")

    # DEBUG: Mostrar algunos valores de ejemplo del Access
    if listado_ots:
        print("\n  DEBUG - Ejemplos de datos del Access:")
        for reg in listado_ots[:3]:
            loc = reg.get('LOCALIZACIÓN', reg.get('LOCALIZACION', '')).strip()
            com = reg.get('COMARCA', '').strip()
            print(f"    ID={reg.get('ID', '?')}: COMARCA='{com}', LOCALIZACIÓN='{loc}'")

    # DEBUG: Mostrar algunos municipios disponibles
    print("\n  DEBUG - Algunos municipios en MySQL:")
    for nombre in list(municipios_por_nombre.keys())[:5]:
        print(f"    '{nombre}'")

    # Primera pasada: intentar mapeo automático
    for registro in listado_ots:
        id_reg = registro.get('ID', registro.get('Id', ''))
        localizacion = registro.get('LOCALIZACIÓN', registro.get('LOCALIZACION', '')).strip()
        comarca_access = registro.get('COMARCA', '').strip()

        # 1. Buscar MUNICIPIO por COMARCA (Access)
        municipio_encontrado = None
        com_norm = normalizar_texto(comarca_access)
        if com_norm in municipios_por_nombre:
            municipio_encontrado = municipios_por_nombre[com_norm]
        else:
            # Buscar por similitud alta
            mejor_sim_muni = 0.0
            mejor_nombre_muni = ""
            for nombre, muni in municipios_por_nombre.items():
                sim = similitud(com_norm, nombre)
                if sim > mejor_sim_muni:
                    mejor_sim_muni = sim
                    mejor_nombre_muni = nombre
                if sim > 0.85:
                    municipio_encontrado = muni
                    break

            # DEBUG: Si no encontró, mostrar la mejor aproximación
            if not municipio_encontrado and len(correctos) + len(problematicos) < 3:
                print(f"    DEBUG ID {id_reg}: COMARCA '{comarca_access}' (norm: '{com_norm}')")
                print(f"           Mejor match: '{mejor_nombre_muni}' con {mejor_sim_muni:.0%} similitud")

        # 2. Buscar CONCEJO por LOCALIZACIÓN (Access)
        concejo_encontrado = None
        loc_norm = normalizar_texto(localizacion)

        # Buscar coincidencia exacta primero
        if loc_norm in concejos_por_nombre:
            candidatos = concejos_por_nombre[loc_norm]
            # Si hay municipio encontrado, priorizar concejos de ese municipio
            if municipio_encontrado:
                for c in candidatos:
                    if c['municipio_id'] == municipio_encontrado['id']:
                        concejo_encontrado = c
                        break
            # Si no hay match con municipio, tomar el primer candidato
            if not concejo_encontrado and candidatos:
                concejo_encontrado = candidatos[0]
        else:
            # Buscar por similitud alta
            mejor_sim = 0.0
            for nombre, lista_concejos in concejos_por_nombre.items():
                sim = similitud(loc_norm, nombre)
                if sim > 0.85 and sim > mejor_sim:
                    # Priorizar concejos del municipio encontrado
                    if municipio_encontrado:
                        for c in lista_concejos:
                            if c['municipio_id'] == municipio_encontrado['id']:
                                concejo_encontrado = c
                                mejor_sim = sim
                                break
                    if not concejo_encontrado and lista_concejos:
                        concejo_encontrado = lista_concejos[0]
                        mejor_sim = sim

        # 3. Verificar coincidencia: ¿El concejo pertenece al municipio?
        if municipio_encontrado and concejo_encontrado:
            if concejo_encontrado['municipio_id'] == municipio_encontrado['id']:
                # ¡Coincidencia perfecta! El concejo pertenece al municipio
                mapeo[id_reg] = {
                    'comarca_id': municipio_encontrado['comarca_id'],
                    'comarca_nombre': municipio_encontrado['comarca_nombre'],
                    'municipio_id': municipio_encontrado['id'],
                    'municipio_nombre': municipio_encontrado['municipio_nombre'],
                    'concejo_id': concejo_encontrado['id'],
                    'concejo_nombre': concejo_encontrado['nombre']
                }
                correctos.append(registro)
            else:
                # Concejo y municipio no coinciden - requiere revisión
                problematicos.append(registro)
        elif municipio_encontrado:
            # Solo encontramos municipio, buscar concejo "Todo X"
            concejo_id = None
            concejo_nombre = f"Todo {municipio_encontrado['municipio_nombre']}"

            if municipio_encontrado['id'] in concejos_por_municipio:
                for c in concejos_por_municipio[municipio_encontrado['id']]:
                    if c['nombre'].startswith('Todo '):
                        concejo_id = c['id']
                        concejo_nombre = c['nombre']
                        break

            mapeo[id_reg] = {
                'comarca_id': municipio_encontrado['comarca_id'],
                'comarca_nombre': municipio_encontrado['comarca_nombre'],
                'municipio_id': municipio_encontrado['id'],
                'municipio_nombre': municipio_encontrado['municipio_nombre'],
                'concejo_id': concejo_id,
                'concejo_nombre': concejo_nombre
            }
            correctos.append(registro)
        else:
            # No se encontró municipio - requiere revisión manual
            problematicos.append(registro)

    # Mostrar resumen de coincidencias automáticas
    print(f"\n✓ Coincidencias automáticas: {len(correctos)} registros")

    if correctos:
        print("\n  Ejemplos de coincidencias correctas:")
        for reg in correctos[:10]:
            id_reg = reg.get('ID', reg.get('Id', ''))
            if id_reg in mapeo:
                m = mapeo[id_reg]
                print(f"    ID {id_reg}: {m['comarca_nombre']} > {m['municipio_nombre']} > {m['concejo_nombre']}")
        if len(correctos) > 10:
            print(f"    ... y {len(correctos) - 10} más")

    # Procesar problemáticos interactivamente
    if problematicos:
        print(f"\n⚠ Registros que requieren revisión: {len(problematicos)}")

        for i, registro in enumerate(problematicos, 1):
            print(f"\n--- Registro {i}/{len(problematicos)} ---")

            resultado = procesar_registro_interactivo(
                registro, comarcas, municipios, concejos,
                comarcas_todas, municipios_todos, concejos_todos
            )

            if resultado:
                id_reg = registro.get('ID', registro.get('Id', ''))
                mapeo[id_reg] = resultado

                # Guardar corrección para tabla final
                correcciones.append({
                    'id': id_reg,
                    'titulo': registro.get('TITULO OT', registro.get('OT', ''))[:40],
                    'descripcion': registro.get('DESCRIPCION OT', registro.get('DESCRIPCION', ''))[:50],
                    'comarca': resultado['comarca_nombre'],
                    'municipio': resultado['municipio_nombre'],
                    'concejo': resultado['concejo_nombre']
                })

            # Preguntar si continuar después de cada 10
            if i % 10 == 0 and i < len(problematicos):
                resp = input(f"\n¿Continuar con los siguientes? ({len(problematicos) - i} restantes) [s/n]: ").strip().lower()
                if resp != 's':
                    print(f"  Saltando {len(problematicos) - i} registros restantes.")
                    break

    return mapeo, correcciones


def mostrar_tabla_correcciones(correcciones: List[Dict]):
    """Muestra tabla resumen de todas las correcciones realizadas."""
    if not correcciones:
        print("\n✓ No hubo correcciones manuales.")
        return

    print("\n" + "="*120)
    print("TABLA DE CORRECCIONES REALIZADAS")
    print("="*120)

    print(f"\n{'ID':<8} {'Título OT':<40} {'Comarca':<20} {'Municipio':<25} {'Concejo':<25}")
    print("-"*120)

    for corr in correcciones:
        print(f"{corr['id']:<8} {corr['titulo']:<40} {corr['comarca']:<20} {corr['municipio']:<25} {corr['concejo']:<25}")

    print("-"*120)
    print(f"Total correcciones: {len(correcciones)}")


# ============================================================================
# FASE 1: LIMPIEZA DE TABLAS
# ============================================================================

def limpiar_tablas_hechos(cursor, conn) -> bool:
    """Elimina todos los datos de las tablas de hechos."""
    print("\n" + "="*70)
    print("FASE 1: LIMPIEZA DE TABLAS DE HECHOS")
    print("="*70)

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
        cursor.execute(f"ALTER TABLE {tabla} AUTO_INCREMENT = 1")

    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    conn.commit()
    print("\n✓ Tablas de hechos limpiadas correctamente")
    return True


# ============================================================================
# FASE 2: VERIFICACIÓN DE DIMENSIONES
# ============================================================================

def verificar_dimensiones(cursor) -> bool:
    """Verifica que las dimensiones básicas existen."""
    print("\n" + "="*70)
    print("FASE 2: VERIFICACIÓN DE DIMENSIONES")
    print("="*70)

    # Verificar dim_tipo_trabajo
    cursor.execute("SELECT COUNT(*) as c FROM dim_tipo_trabajo")
    count = cursor.fetchone()['c']
    print(f"  dim_tipo_trabajo: {count} registros")

    # Verificar dim_red
    cursor.execute("SELECT COUNT(*) as c FROM dim_red")
    count = cursor.fetchone()['c']
    print(f"  dim_red: {count} registros")

    # Verificar geografía
    cursor.execute("SELECT COUNT(*) as c FROM dim_comarcas")
    count_com = cursor.fetchone()['c']
    cursor.execute("SELECT COUNT(*) as c FROM dim_municipios")
    count_mun = cursor.fetchone()['c']
    cursor.execute("SELECT COUNT(*) as c FROM dim_concejos")
    count_con = cursor.fetchone()['c']

    print(f"  dim_comarcas: {count_com} registros")
    print(f"  dim_municipios: {count_mun} registros")
    print(f"  dim_concejos: {count_con} registros")

    if count_com < 5 or count_mun < 50 or count_con < 100:
        print("\n⚠ Las dimensiones geográficas parecen incompletas.")
        print("  Ejecuta primero: script/sql/recrear_dimensiones_geograficas.sql")
        return False

    print("\n✓ Dimensiones verificadas")
    return True


# ============================================================================
# FASE 4: IMPORTACIÓN DE DATOS
# ============================================================================

def convertir_fecha(fecha_str: str) -> Optional[str]:
    """Convierte fecha de Access a formato MySQL."""
    if not fecha_str or fecha_str.strip() == '':
        return None

    formatos = [
        '%m/%d/%y %H:%M:%S', '%d/%m/%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S',
        '%m/%d/%y', '%d/%m/%Y', '%Y-%m-%d',
    ]

    for fmt in formatos:
        try:
            dt = datetime.strptime(fecha_str.strip(), fmt)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            continue
    return None


def importar_listado_ots(cursor, conn, listado_ots: List[Dict], mapeo: Dict) -> int:
    """Importa LISTADO OTS → tbl_partes"""
    print("\n" + "-"*70)
    print("Importando LISTADO OTS → tbl_partes")
    print("-"*70)

    insertados = 0
    errores = 0
    sin_mapeo = 0

    insert_sql = """
        INSERT INTO tbl_partes (
            codigo, descripcion, tipo_trabajo_id, cod_trabajo_id,
            red_id, provincia_id, comarca_id, municipio_id, concejo_id,
            estado_id, fecha_encargo, fecha_finalizacion, creado_en
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW()
        )
    """

    for row in listado_ots:
        try:
            id_reg = row.get('ID', row.get('Id', ''))
            codigo = row.get('COD TRABAJO', row.get('COD_TRABAJO', '')).strip()
            descripcion = row.get('OT', row.get('DESCRIPCION', '')).strip()

            # Tipo de trabajo
            tipo_trabajo_raw = row.get('TIPO DE TRABAJOS', row.get('TIPO_DE_TRABAJOS', ''))
            try:
                tipo_trabajo_id = int(tipo_trabajo_raw) if tipo_trabajo_raw else None
                tipo_trabajo_id = MAPEO_TIPO_TRABAJO.get(tipo_trabajo_id, tipo_trabajo_id)
            except (ValueError, TypeError):
                tipo_trabajo_id = None

            # Código de trabajo
            cod_trabajo_raw = row.get('TRABAJOS PROGRAMADOS', row.get('TRABAJOS_PROGRAMADOS', ''))
            try:
                cod_trabajo_id = int(cod_trabajo_raw) if cod_trabajo_raw else None
            except (ValueError, TypeError):
                cod_trabajo_id = None

            # Red
            red_texto = row.get('RED', '').strip().upper()
            red_id = MAPEO_RED.get(red_texto)

            # Datos geográficos del mapeo
            geo = mapeo.get(id_reg, {})
            provincia_id = 1  # Álava por defecto
            comarca_id = geo.get('comarca_id')
            municipio_id = geo.get('municipio_id')
            concejo_id = geo.get('concejo_id')

            if not municipio_id:
                sin_mapeo += 1
                continue

            # Estado y fechas
            estado_id = 1
            fecha_encargo = convertir_fecha(row.get('FECHA_ENCARGO', row.get('FECHA ENCARGO', '')))
            fecha_finalizacion = convertir_fecha(row.get('FECHA_FINALIZACION', row.get('FECHA FINALIZACION', '')))

            cursor.execute(insert_sql, (
                codigo, descripcion, tipo_trabajo_id, cod_trabajo_id,
                red_id, provincia_id, comarca_id, municipio_id, concejo_id,
                estado_id, fecha_encargo, fecha_finalizacion
            ))
            insertados += 1

        except Exception as e:
            errores += 1
            if errores <= 5:
                print(f"  Error en registro: {row.get('ID', '?')}: {e}")

    conn.commit()
    print(f"\n✓ Importados: {insertados} partes")
    if sin_mapeo:
        print(f"⚠ Sin mapeo geográfico: {sin_mapeo}")
    if errores:
        print(f"⚠ Errores: {errores}")

    return insertados


def importar_mediciones_ots(cursor, conn, mediciones: List[Dict]) -> int:
    """Importa MEDICIONES OTS → tbl_part_presupuesto"""
    print("\n" + "-"*70)
    print("Importando MEDICIONES OTS → tbl_part_presupuesto")
    print("-"*70)

    cursor.execute("SELECT id, codigo FROM tbl_partes")
    partes_db = {row['codigo']: row['id'] for row in cursor.fetchall()}

    cursor.execute("SELECT id, codigo FROM tbl_pres_precios")
    precios_db = {row['codigo']: row['id'] for row in cursor.fetchall()}

    insertados = 0
    errores = 0
    partes_no_encontrados = set()

    insert_sql = """
        INSERT INTO tbl_part_presupuesto (
            parte_id, precio_id, cantidad, precio_unitario,
            precio_total, fecha_medicion, creado_en
        ) VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """

    for row in mediciones:
        try:
            cod_trabajo = row.get('COD TRABAJO', row.get('COD_TRABAJO', '')).strip()
            parte_id = partes_db.get(cod_trabajo)

            if not parte_id:
                if cod_trabajo not in partes_no_encontrados:
                    partes_no_encontrados.add(cod_trabajo)
                continue

            cod_precio = row.get('CODIGO', row.get('CÓDIGO', '')).strip()
            precio_id = precios_db.get(cod_precio)

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
    --access "./CERTIFICACIONES.accdb" \\
    --host localhost --port 3306 \\
    --user root --password mipassword \\
    --database hydroflow_urbide
        """
    )

    parser.add_argument('--access', required=True, help='Ruta al archivo .accdb de Access')
    parser.add_argument('--host', default='localhost', help='Host MySQL')
    parser.add_argument('--port', type=int, default=3306, help='Puerto MySQL')
    parser.add_argument('--user', required=True, help='Usuario MySQL')
    parser.add_argument('--password', required=True, help='Contraseña MySQL')
    parser.add_argument('--database', required=True, help='Base de datos MySQL')
    parser.add_argument('--solo-verificar', action='store_true', help='Solo verificar, no importar')
    parser.add_argument('--no-interactivo', action='store_true', help='No pedir confirmaciones')

    args = parser.parse_args()

    if not os.path.exists(args.access):
        print(f"ERROR: No se encuentra el archivo: {args.access}")
        sys.exit(1)

    print("="*80)
    print("IMPORTACIÓN ACCESS → MySQL")
    print("="*80)
    print(f"Archivo Access: {args.access}")
    print(f"Base de datos MySQL: {args.database}@{args.host}:{args.port}")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Conectar a MySQL
    print("\nConectando a MySQL...")
    conn, cursor = conectar_mysql(args.host, args.port, args.user, args.password, args.database)
    print("✓ Conexión establecida")

    # Leer tablas de Access
    print("\nLeyendo tablas de Access...")
    listado_ots = leer_tabla_access(args.access, 'LISTADO OTS')
    print(f"  LISTADO OTS: {len(listado_ots)} registros")

    mediciones_ots = leer_tabla_access(args.access, 'MEDICIONES OTS')
    print(f"  MEDICIONES OTS: {len(mediciones_ots)} registros")

    # FASE 1: Limpiar tablas
    if not args.solo_verificar:
        if not args.no_interactivo:
            if not limpiar_tablas_hechos(cursor, conn):
                sys.exit(1)
        else:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            for tabla in ['tbl_part_certificacion', 'tbl_part_presupuesto', 'tbl_partes']:
                cursor.execute(f"DELETE FROM {tabla}")
                cursor.execute(f"ALTER TABLE {tabla} AUTO_INCREMENT = 1")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            conn.commit()

    # FASE 2: Verificar dimensiones
    if not verificar_dimensiones(cursor):
        if not args.no_interactivo:
            resp = input("\n¿Continuar de todos modos? (s/n): ").strip().lower()
            if resp != 's':
                sys.exit(1)

    if args.solo_verificar:
        print("\n✓ Verificación completada")
        sys.exit(0)

    # FASE 3: Mapeo geográfico
    # Listas filtradas para matching automático (sin Todo/Varios)
    comarcas = cargar_comarcas(cursor, incluir_especiales=False)
    municipios = cargar_municipios(cursor, incluir_especiales=False)
    concejos = cargar_concejos(cursor, incluir_especiales=False)

    # Listas completas para selección manual (con Todo/Varios)
    comarcas_todas = cargar_comarcas(cursor, incluir_especiales=True)
    municipios_todos = cargar_municipios(cursor, incluir_especiales=True)
    concejos_todos = cargar_concejos(cursor, incluir_especiales=True)

    print(f"\nDatos geográficos cargados:")
    print(f"  Comarcas: {len(comarcas)} (+ {len(comarcas_todas) - len(comarcas)} especiales)")
    print(f"  Municipios: {len(municipios)} (+ {len(municipios_todos) - len(municipios)} especiales)")
    print(f"  Concejos: {len(concejos)} (+ {len(concejos_todos) - len(concejos)} especiales)")

    mapeo, correcciones = procesar_mapeo_geografico(
        listado_ots, comarcas, municipios, concejos,
        comarcas_todas, municipios_todos, concejos_todos
    )

    # FASE 4: Importar datos
    print("\n" + "="*70)
    print("FASE 4: IMPORTACIÓN DE DATOS")
    print("="*70)

    partes_importados = importar_listado_ots(cursor, conn, listado_ots, mapeo)
    mediciones_importadas = importar_mediciones_ots(cursor, conn, mediciones_ots)

    # Mostrar tabla de correcciones
    mostrar_tabla_correcciones(correcciones)

    # RESUMEN FINAL
    print("\n" + "="*80)
    print("IMPORTACIÓN COMPLETADA")
    print("="*80)
    print(f"  Partes importados: {partes_importados}")
    print(f"  Mediciones importadas: {mediciones_importadas}")
    print(f"  Correcciones manuales: {len(correcciones)}")

    cursor.close()
    conn.close()
    print("\n✓ Proceso finalizado correctamente")


if __name__ == '__main__':
    main()
