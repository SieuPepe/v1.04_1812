#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GENERADOR EXHAUSTIVO DE TODAS LAS COMBINACIONES DE INFORMES

Este script genera TODAS las combinaciones posibles de informes:
- Todos los tipos de agrupaciones (1, 2 y 3 niveles)
- Todos los filtros posibles
- Todas las selecciones de partidas
- Todas las combinaciones de campos

ADVERTENCIA: Este script generará CIENTOS de archivos.
"""

import os
import sys
import random
import json
import csv
from pathlib import Path
from datetime import datetime, timedelta
from itertools import combinations
from decimal import Decimal

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

OUTPUT_DIR = Path(__file__).parent / "informes_exhaustivos"
OUTPUT_DIR.mkdir(exist_ok=True)

# =============================================================================
# GENERADOR DE DATOS (Reutilizado)
# =============================================================================

class GeneradorDatos:
    """Genera datos de ejemplo realistas"""

    def __init__(self):
        self.redes = [
            "RED-MT-01",
            "RED-MT-02",
            "RED-BT-01",
            "RED-AT-01",
            "RED-DIST-01"
        ]

        self.tipos_trabajo = [
            ("OT", "Órdenes de Trabajo"),
            ("GF", "Garantía y Fallos"),
            ("TP", "Trabajos Programados")
        ]

        self.codigos_trabajo = [
            "CT-001", "CT-002", "CT-003", "CT-004", "CT-005"
        ]

        self.tipos_rep = [
            "FUGA", "ATASCO", "OTROS"
        ]

        self.estados = ["Pendiente", "En curso", "Finalizado"]

        self.provincias = [
            "Álava", "Bizkaia", "Gipuzkoa", "Navarra",
            "Barcelona", "Girona", "Madrid", "Valencia"
        ]

        self.comarcas = {
            "Barcelona": ["Barcelonés", "Vallès Occidental", "Baix Llobregat", "Maresme"],
            "Álava": ["Cuadrilla de Vitoria", "Rioja Alavesa"],
            "Bizkaia": ["Gran Bilbao", "Duranguesado", "Lea-Artibai"],
            "Gipuzkoa": ["Donostialdea", "Tolosaldea", "Urola Kosta"],
            "Girona": ["La Garrotxa", "La Selva"],
            "Madrid": ["Área Metropolitana"],
            "Valencia": ["Horta Nord", "Horta Sud"],
            "Navarra": ["Cuenca de Pamplona"]
        }

        self.municipios = {
            "Barcelonés": ["Barcelona", "L'Hospitalet de Llobregat"],
            "Vallès Occidental": ["Sabadell", "Terrassa", "Cerdanyola del Vallès"],
            "Gran Bilbao": ["Bilbao", "Barakaldo", "Getxo", "Portugalete"],
            "Donostialdea": ["Donostia", "Errenteria", "Pasaia"],
            "Cuenca de Pamplona": ["Pamplona", "Barañain"],
            "Cuadrilla de Vitoria": ["Vitoria-Gasteiz"],
            "Área Metropolitana": ["Madrid"],
            "Horta Nord": ["Valencia"]
        }

    def generar_parte(self, numero):
        """Genera un parte aleatorio"""
        tipo_codigo, tipo_desc = random.choice(self.tipos_trabajo)
        año = random.choice([2024, 2025])
        codigo = f"{tipo_codigo}-{año}-{numero:04d}"

        provincia = random.choice(self.provincias)
        comarcas_disponibles = self.comarcas.get(provincia, ["Sin comarca"])
        comarca = random.choice(comarcas_disponibles)
        municipios_disponibles = self.municipios.get(comarca, ["Sin municipio"])
        municipio = random.choice(municipios_disponibles)

        fecha_inicio = datetime(año, 1, 1) + timedelta(days=random.randint(0, 300))
        estado = random.choice(self.estados)

        presupuesto = round(random.uniform(1000, 50000), 2)

        if estado == "Finalizado":
            certificado = round(presupuesto * random.uniform(0.85, 1.05), 2)
            duracion = random.randint(5, 60)
            fecha_fin = fecha_inicio + timedelta(days=duracion)
        elif estado == "En curso":
            certificado = round(presupuesto * random.uniform(0.2, 0.7), 2)
            if random.random() > 0.5:
                duracion = random.randint(10, 90)
                fecha_fin = fecha_inicio + timedelta(days=duracion)
            else:
                fecha_fin = None
        else:  # Pendiente
            certificado = 0.0
            fecha_fin = None

        return {
            'codigo': codigo,
            'descripcion': f"Trabajo {numero} - {municipio}",
            'estado': estado,
            'red': random.choice(self.redes),
            'tipo_trabajo': tipo_desc,
            'tipo_trabajo_codigo': tipo_codigo,
            'cod_trabajo': random.choice(self.codigos_trabajo),
            'tipo_rep': random.choice(self.tipos_rep),
            'provincia': provincia,
            'comarca': comarca,
            'municipio': municipio,
            'presupuesto': presupuesto,
            'certificado': certificado,
            'pendiente': presupuesto - certificado,
            'fecha_inicio': fecha_inicio.strftime('%Y-%m-%d'),
            'fecha_fin': fecha_fin.strftime('%Y-%m-%d') if fecha_fin else '',
            'mes': fecha_inicio.strftime('%Y-%m'),
            'año': año
        }

    def generar_partes(self, cantidad=200):
        """Genera múltiples partes"""
        return [self.generar_parte(i+1) for i in range(cantidad)]

# =============================================================================
# FUNCIONES DE AGRUPACIÓN
# =============================================================================

def agrupar_por_campos(partes, campos):
    """Agrupa partes por uno o más campos"""
    if not campos:
        return partes

    grupos = {}

    for parte in partes:
        # Crear clave compuesta con los valores de los campos
        valores = tuple(parte.get(campo, 'Sin especificar') for campo in campos)

        if valores not in grupos:
            grupo_dict = {campo: parte.get(campo, 'Sin especificar') for campo in campos}
            grupo_dict.update({
                'cantidad': 0,
                'total_presupuesto': 0.0,
                'total_certificado': 0.0,
                'total_pendiente': 0.0
            })
            grupos[valores] = grupo_dict

        grupos[valores]['cantidad'] += 1
        grupos[valores]['total_presupuesto'] += parte['presupuesto']
        grupos[valores]['total_certificado'] += parte['certificado']
        grupos[valores]['total_pendiente'] += parte['pendiente']

    # Redondear valores
    for grupo in grupos.values():
        grupo['total_presupuesto'] = round(grupo['total_presupuesto'], 2)
        grupo['total_certificado'] = round(grupo['total_certificado'], 2)
        grupo['total_pendiente'] = round(grupo['total_pendiente'], 2)

    return list(grupos.values())

# =============================================================================
# GENERADORES DE INFORMES
# =============================================================================

def guardar_csv(datos, filepath):
    """Guarda datos en CSV"""
    if not datos:
        return

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        if isinstance(datos[0], dict):
            writer = csv.DictWriter(f, fieldnames=datos[0].keys())
            writer.writeheader()
            writer.writerows(datos)
        else:
            writer = csv.writer(f)
            writer.writerows(datos)

def generar_informes_sin_agrupacion(partes, output_dir):
    """Genera informes sin agrupación (listado completo)"""
    print("\n🔹 Informes SIN agrupación")

    subdir = output_dir / "01_sin_agrupacion"
    subdir.mkdir(exist_ok=True)

    archivos = []

    # Informe completo
    filepath = subdir / "Listado_Completo.csv"
    guardar_csv(partes, filepath)
    archivos.append(filepath)
    print(f"   ✅ Listado_Completo.csv ({len(partes)} registros)")

    return archivos

def generar_informes_agrupacion_simple(partes, output_dir):
    """Genera informes con agrupación por 1 campo"""
    print("\n🔹 Informes con agrupación SIMPLE (1 campo)")

    subdir = output_dir / "02_agrupacion_simple"
    subdir.mkdir(exist_ok=True)

    archivos = []

    # Campos de agrupación
    campos_agrupacion = [
        'mes', 'año', 'estado', 'red', 'tipo_trabajo',
        'cod_trabajo', 'tipo_rep', 'provincia', 'comarca', 'municipio'
    ]

    for campo in campos_agrupacion:
        grupos = agrupar_por_campos(partes, [campo])
        filename = f"Por_{campo.capitalize()}.csv"
        filepath = subdir / filename
        guardar_csv(grupos, filepath)
        archivos.append(filepath)
        print(f"   ✅ {filename} ({len(grupos)} grupos)")

    return archivos

def generar_informes_agrupacion_doble(partes, output_dir):
    """Genera informes con agrupación por 2 campos"""
    print("\n🔹 Informes con agrupación DOBLE (2 campos)")

    subdir = output_dir / "03_agrupacion_doble"
    subdir.mkdir(exist_ok=True)

    archivos = []

    # Combinaciones más relevantes de 2 campos
    combinaciones_relevantes = [
        ('provincia', 'estado'),
        ('provincia', 'tipo_trabajo'),
        ('provincia', 'comarca'),
        ('año', 'mes'),
        ('año', 'estado'),
        ('año', 'provincia'),
        ('mes', 'estado'),
        ('mes', 'provincia'),
        ('estado', 'tipo_trabajo'),
        ('estado', 'red'),
        ('tipo_trabajo', 'estado'),
        ('tipo_trabajo', 'provincia'),
        ('red', 'estado'),
        ('red', 'tipo_trabajo'),
        ('comarca', 'municipio'),
        ('provincia', 'tipo_rep'),
        ('tipo_rep', 'estado'),
        ('cod_trabajo', 'estado'),
        ('cod_trabajo', 'tipo_trabajo')
    ]

    for campo1, campo2 in combinaciones_relevantes:
        grupos = agrupar_por_campos(partes, [campo1, campo2])
        filename = f"Por_{campo1}_y_{campo2}.csv"
        filepath = subdir / filename
        guardar_csv(grupos, filepath)
        archivos.append(filepath)
        print(f"   ✅ {filename} ({len(grupos)} grupos)")

    return archivos

def generar_informes_agrupacion_triple(partes, output_dir):
    """Genera informes con agrupación por 3 campos"""
    print("\n🔹 Informes con agrupación TRIPLE (3 campos)")

    subdir = output_dir / "04_agrupacion_triple"
    subdir.mkdir(exist_ok=True)

    archivos = []

    # Combinaciones relevantes de 3 campos
    combinaciones_relevantes = [
        ('año', 'provincia', 'estado'),
        ('año', 'tipo_trabajo', 'estado'),
        ('provincia', 'comarca', 'municipio'),
        ('provincia', 'comarca', 'estado'),
        ('provincia', 'tipo_trabajo', 'estado'),
        ('mes', 'provincia', 'estado'),
        ('mes', 'tipo_trabajo', 'estado'),
        ('año', 'mes', 'provincia'),
        ('red', 'tipo_trabajo', 'estado'),
        ('tipo_trabajo', 'cod_trabajo', 'estado')
    ]

    for campo1, campo2, campo3 in combinaciones_relevantes:
        grupos = agrupar_por_campos(partes, [campo1, campo2, campo3])
        filename = f"Por_{campo1}_{campo2}_{campo3}.csv"
        filepath = subdir / filename
        guardar_csv(grupos, filepath)
        archivos.append(filepath)
        print(f"   ✅ {filename} ({len(grupos)} grupos)")

    return archivos

def generar_informes_filtrados(partes, output_dir):
    """Genera informes filtrados por diferentes dimensiones"""
    print("\n🔹 Informes FILTRADOS (por cada valor de dimensión)")

    subdir = output_dir / "05_filtrados"
    subdir.mkdir(exist_ok=True)

    archivos = []

    # Obtener valores únicos de cada dimensión
    estados_unicos = list(set(p['estado'] for p in partes))
    provincias_unicas = list(set(p['provincia'] for p in partes))
    tipos_trabajo_unicos = list(set(p['tipo_trabajo'] for p in partes))
    redes_unicas = list(set(p['red'] for p in partes))

    # Informes filtrados por estado
    print("\n   Por Estado:")
    for estado in estados_unicos:
        partes_filtradas = [p for p in partes if p['estado'] == estado]
        filename = f"Estado_{estado.replace(' ', '_')}.csv"
        filepath = subdir / filename
        guardar_csv(partes_filtradas, filepath)
        archivos.append(filepath)
        print(f"      ✅ {filename} ({len(partes_filtradas)} registros)")

    # Informes filtrados por provincia
    print("\n   Por Provincia:")
    for provincia in sorted(provincias_unicas):
        partes_filtradas = [p for p in partes if p['provincia'] == provincia]
        filename = f"Provincia_{provincia.replace(' ', '_')}.csv"
        filepath = subdir / filename
        guardar_csv(partes_filtradas, filepath)
        archivos.append(filepath)
        print(f"      ✅ {filename} ({len(partes_filtradas)} registros)")

    # Informes filtrados por tipo de trabajo
    print("\n   Por Tipo de Trabajo:")
    for tipo in sorted(tipos_trabajo_unicos):
        partes_filtradas = [p for p in partes if p['tipo_trabajo'] == tipo]
        filename = f"TipoTrabajo_{tipo.replace(' ', '_')}.csv"
        filepath = subdir / filename
        guardar_csv(partes_filtradas, filepath)
        archivos.append(filepath)
        print(f"      ✅ {filename} ({len(partes_filtradas)} registros)")

    # Informes filtrados por red
    print("\n   Por Red:")
    for red in sorted(redes_unicas):
        partes_filtradas = [p for p in partes if p['red'] == red]
        filename = f"Red_{red.replace('-', '_')}.csv"
        filepath = subdir / filename
        guardar_csv(partes_filtradas, filepath)
        archivos.append(filepath)
        print(f"      ✅ {filename} ({len(partes_filtradas)} registros)")

    return archivos

def generar_informes_filtros_combinados(partes, output_dir):
    """Genera informes con filtros combinados"""
    print("\n🔹 Informes con FILTROS COMBINADOS")

    subdir = output_dir / "06_filtros_combinados"
    subdir.mkdir(exist_ok=True)

    archivos = []

    # Obtener valores únicos
    estados = list(set(p['estado'] for p in partes))
    provincias = list(set(p['provincia'] for p in partes))
    tipos_trabajo = list(set(p['tipo_trabajo'] for p in partes))

    # Combinaciones Estado + Provincia (las más comunes)
    print("\n   Estado × Provincia:")
    for estado in estados[:3]:  # Primeros 3 estados
        for provincia in sorted(provincias)[:5]:  # Primeras 5 provincias
            partes_filtradas = [p for p in partes if p['estado'] == estado and p['provincia'] == provincia]
            if len(partes_filtradas) > 0:
                filename = f"Estado_{estado.replace(' ', '_')}_Provincia_{provincia.replace(' ', '_')}.csv"
                filepath = subdir / filename
                guardar_csv(partes_filtradas, filepath)
                archivos.append(filepath)
                print(f"      ✅ {filename} ({len(partes_filtradas)} registros)")

    # Combinaciones Estado + Tipo Trabajo
    print("\n   Estado × Tipo Trabajo:")
    for estado in estados:
        for tipo in tipos_trabajo:
            partes_filtradas = [p for p in partes if p['estado'] == estado and p['tipo_trabajo'] == tipo]
            if len(partes_filtradas) > 0:
                filename = f"Estado_{estado.replace(' ', '_')}_Tipo_{tipo.replace(' ', '_')}.csv"
                filepath = subdir / filename
                guardar_csv(partes_filtradas, filepath)
                archivos.append(filepath)
                print(f"      ✅ {filename} ({len(partes_filtradas)} registros)")

    return archivos

def generar_informes_por_partidas(partes, output_dir, num_selecciones=20):
    """Genera informes con selecciones aleatorias de partidas"""
    print(f"\n🔹 Informes por PARTIDAS SELECCIONADAS ({num_selecciones} selecciones)")

    subdir = output_dir / "07_por_partidas"
    subdir.mkdir(exist_ok=True)

    archivos = []
    todos_codigos = [p['codigo'] for p in partes]

    for i in range(num_selecciones):
        # Seleccionar entre 5 y 20 partidas aleatoriamente
        num_partidas = random.randint(5, 20)
        codigos_selec = random.sample(todos_codigos, num_partidas)

        # Filtrar partes
        partes_filtradas = [p for p in partes if p['codigo'] in codigos_selec]

        # Guardar CSV
        filename = f"Seleccion_{i+1:02d}.csv"
        filepath = subdir / filename
        guardar_csv(partes_filtradas, filepath)
        archivos.append(filepath)

        # Guardar metadata JSON
        metadata = {
            'seleccion_numero': i+1,
            'partidas_seleccionadas': codigos_selec,
            'num_partidas': len(partes_filtradas),
            'total_presupuesto': round(sum(p['presupuesto'] for p in partes_filtradas), 2),
            'total_certificado': round(sum(p['certificado'] for p in partes_filtradas), 2),
            'total_pendiente': round(sum(p['pendiente'] for p in partes_filtradas), 2),
            'distribucion_estados': {
                'Pendiente': len([p for p in partes_filtradas if p['estado'] == 'Pendiente']),
                'En curso': len([p for p in partes_filtradas if p['estado'] == 'En curso']),
                'Finalizado': len([p for p in partes_filtradas if p['estado'] == 'Finalizado'])
            }
        }

        json_path = subdir / f"Seleccion_{i+1:02d}_metadata.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        archivos.append(json_path)

        print(f"   ✅ Selección #{i+1}: {num_partidas} partidas → 2 archivos")

    return archivos

def generar_resumen_global(partes, archivos_generados, output_dir):
    """Genera un resumen global de todos los informes generados"""
    print("\n🔹 Generando RESUMEN GLOBAL")

    resumen = {
        'fecha_generacion': datetime.now().isoformat(),
        'total_partes': len(partes),
        'total_archivos_generados': len(archivos_generados),
        'importes_totales': {
            'presupuesto': round(sum(p['presupuesto'] for p in partes), 2),
            'certificado': round(sum(p['certificado'] for p in partes), 2),
            'pendiente': round(sum(p['pendiente'] for p in partes), 2)
        },
        'distribucion_estados': {
            estado: len([p for p in partes if p['estado'] == estado])
            for estado in set(p['estado'] for p in partes)
        },
        'distribucion_provincias': {
            provincia: len([p for p in partes if p['provincia'] == provincia])
            for provincia in sorted(set(p['provincia'] for p in partes))
        },
        'categorias_informes': {
            '01_sin_agrupacion': len([f for f in archivos_generados if '01_sin_agrupacion' in str(f)]),
            '02_agrupacion_simple': len([f for f in archivos_generados if '02_agrupacion_simple' in str(f)]),
            '03_agrupacion_doble': len([f for f in archivos_generados if '03_agrupacion_doble' in str(f)]),
            '04_agrupacion_triple': len([f for f in archivos_generados if '04_agrupacion_triple' in str(f)]),
            '05_filtrados': len([f for f in archivos_generados if '05_filtrados' in str(f)]),
            '06_filtros_combinados': len([f for f in archivos_generados if '06_filtros_combinados' in str(f)]),
            '07_por_partidas': len([f for f in archivos_generados if '07_por_partidas' in str(f)])
        }
    }

    # Guardar JSON
    json_path = output_dir / "RESUMEN_GLOBAL.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(resumen, f, indent=2, ensure_ascii=False)

    print(f"\n   ✅ RESUMEN_GLOBAL.json")
    return json_path

# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def main():
    """Función principal"""
    print("=" * 80)
    print("  🚀 GENERADOR EXHAUSTIVO DE TODAS LAS COMBINACIONES DE INFORMES")
    print("=" * 80)
    print(f"\nDirectorio de salida: {OUTPUT_DIR}\n")

    # Paso 1: Generar datos
    print("─" * 80)
    print("  PASO 1: Generando datos de prueba")
    print("─" * 80)

    generador = GeneradorDatos()
    partes = generador.generar_partes(200)  # 200 partes para más variedad

    print(f"\n✅ Generados {len(partes)} partes de ejemplo")
    print(f"   • Presupuesto total: €{sum(p['presupuesto'] for p in partes):,.2f}")
    print(f"   • Certificado total: €{sum(p['certificado'] for p in partes):,.2f}")

    # Paso 2: Generar todos los tipos de informes
    print("\n" + "=" * 80)
    print("  PASO 2: Generando TODOS los informes")
    print("=" * 80)

    archivos_generados = []

    # 1. Sin agrupación
    archivos_generados.extend(generar_informes_sin_agrupacion(partes, OUTPUT_DIR))

    # 2. Agrupación simple (1 campo)
    archivos_generados.extend(generar_informes_agrupacion_simple(partes, OUTPUT_DIR))

    # 3. Agrupación doble (2 campos)
    archivos_generados.extend(generar_informes_agrupacion_doble(partes, OUTPUT_DIR))

    # 4. Agrupación triple (3 campos)
    archivos_generados.extend(generar_informes_agrupacion_triple(partes, OUTPUT_DIR))

    # 5. Filtrados
    archivos_generados.extend(generar_informes_filtrados(partes, OUTPUT_DIR))

    # 6. Filtros combinados
    archivos_generados.extend(generar_informes_filtros_combinados(partes, OUTPUT_DIR))

    # 7. Por partidas
    archivos_generados.extend(generar_informes_por_partidas(partes, OUTPUT_DIR, num_selecciones=20))

    # Paso 3: Generar resumen global
    print("\n" + "=" * 80)
    print("  PASO 3: Generando resumen global")
    print("=" * 80)

    resumen_path = generar_resumen_global(partes, archivos_generados, OUTPUT_DIR)

    # Resumen final
    print("\n" + "=" * 80)
    print("  ✅ PROCESO COMPLETADO")
    print("=" * 80)

    print(f"\n  📊 ESTADÍSTICAS:")
    print(f"     • Total de partes generados: {len(partes)}")
    print(f"     • Total de archivos generados: {len(archivos_generados)}")
    print(f"     • Directorio de salida: {OUTPUT_DIR}")

    # Desglose por categoría
    print(f"\n  📁 ARCHIVOS POR CATEGORÍA:")
    categorias = [
        ('Sin agrupación', '01_sin_agrupacion'),
        ('Agrupación simple (1 campo)', '02_agrupacion_simple'),
        ('Agrupación doble (2 campos)', '03_agrupacion_doble'),
        ('Agrupación triple (3 campos)', '04_agrupacion_triple'),
        ('Filtrados', '05_filtrados'),
        ('Filtros combinados', '06_filtros_combinados'),
        ('Por partidas', '07_por_partidas')
    ]

    for nombre, patron in categorias:
        count = len([f for f in archivos_generados if patron in str(f)])
        print(f"     • {nombre}: {count} archivos")

    print(f"\n  ✨ ¡Todos los informes generados exitosamente!")
    print(f"     Ver resumen completo en: RESUMEN_GLOBAL.json\n")

    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
