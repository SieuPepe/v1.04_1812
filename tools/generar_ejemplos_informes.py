#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de ejemplos de informes para análisis exhaustivo
(Sin necesidad de base de datos MySQL)

Este script genera archivos de ejemplo que simulan los informes del sistema
con datos realistas para poder analizar todas las funcionalidades y formatos.
"""

import os
import sys
import random
import json
import csv
from pathlib import Path
from datetime import datetime, timedelta
from decimal import Decimal

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

OUTPUT_DIR = Path(__file__).parent / "ejemplos_informes_generados"
OUTPUT_DIR.mkdir(exist_ok=True)

# =============================================================================
# GENERADORES DE DATOS
# =============================================================================

class GeneradorDatos:
    """Genera datos de ejemplo realistas"""

    def __init__(self):
        self.redes = [
            "RED-MT-01 - Red Media Tensión Zona Industrial",
            "RED-MT-02 - Red Media Tensión Zona Residencial",
            "RED-BT-01 - Red Baja Tensión Centro Ciudad",
            "RED-AT-01 - Red Alta Tensión Línea Principal",
            "RED-DIST-01 - Red Distribución Sector Norte"
        ]

        self.tipos_trabajo = [
            ("OT", "Órdenes de Trabajo"),
            ("GF", "Garantía y Fallos"),
            ("TP", "Trabajos Programados")
        ]

        self.codigos_trabajo = [
            "CT-001 - Revisión General",
            "CT-002 - Instalación de Equipos",
            "CT-003 - Reparación de Averías",
            "CT-004 - Calibración de Instrumentos",
            "CT-005 - Cambio de Componentes"
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
            "Gipuzkoa": ["Donostialdea", "Tolosaldea", "Urola Kosta"]
        }

        self.municipios = {
            "Barcelonés": ["Barcelona", "L'Hospitalet de Llobregat"],
            "Vallès Occidental": ["Sabadell", "Terrassa", "Cerdanyola del Vallès"],
            "Gran Bilbao": ["Bilbao", "Barakaldo", "Getxo", "Portugalete"],
            "Donostialdea": ["Donostia", "Errenteria", "Pasaia"]
        }

    def generar_parte(self, numero):
        """Genera un parte aleatorio"""
        tipo_codigo, tipo_desc = random.choice(self.tipos_trabajo)
        año = random.choice([2024, 2025])
        codigo = f"{tipo_codigo}-{año}-{numero:04d}"

        provincia = random.choice(self.provincias)
        comarca = random.choice(self.comarcas.get(provincia, ["Sin comarca"]))
        municipio = random.choice(self.municipios.get(comarca, ["Sin municipio"]))

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
            'descripcion': f"Trabajo de {tipo_desc.lower()} en {municipio}",
            'estado': estado,
            'red': random.choice(self.redes),
            'tipo_trabajo': tipo_desc,
            'cod_trabajo': random.choice(self.codigos_trabajo),
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

    def generar_partes(self, cantidad=100):
        """Genera múltiples partes"""
        return [self.generar_parte(i+1) for i in range(cantidad)]

# =============================================================================
# GENERADORES DE INFORMES
# =============================================================================

def generar_informe_basico(partes, nombre_archivo):
    """Genera un informe básico con todos los partes"""
    filepath = OUTPUT_DIR / nombre_archivo

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        if partes:
            writer = csv.DictWriter(f, fieldnames=partes[0].keys())
            writer.writeheader()
            writer.writerows(partes)

    return filepath

def generar_informe_por_partidas(partes, nombre, partidas_seleccionadas):
    """Genera informe filtrado por partidas específicas"""
    partes_filtrados = [p for p in partes if p['codigo'] in partidas_seleccionadas]

    # Crear subdirectorio
    subdir = OUTPUT_DIR / "por_partidas"
    subdir.mkdir(exist_ok=True)

    # Generar CSV
    nombre_limpio = nombre.replace('#', '').replace(' ', '_')
    csv_path = subdir / f"{nombre_limpio}.csv"

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        if partes_filtrados:
            writer = csv.DictWriter(f, fieldnames=partes_filtrados[0].keys())
            writer.writeheader()
            writer.writerows(partes_filtrados)

    # Generar JSON con metadatos
    json_path = subdir / f"{nombre_limpio}_metadata.json"
    metadata = {
        'nombre': nombre,
        'tipo_informe': 'Listado de Partes',
        'filtro': 'Por Partidas Seleccionadas',
        'partidas_seleccionadas': partidas_seleccionadas,
        'num_resultados': len(partes_filtrados),
        'fecha_generacion': datetime.now().isoformat(),
        'estadisticas': {
            'total_presupuesto': sum(p['presupuesto'] for p in partes_filtrados),
            'total_certificado': sum(p['certificado'] for p in partes_filtrados),
            'total_pendiente': sum(p['pendiente'] for p in partes_filtrados),
            'estados': {
                'Pendiente': len([p for p in partes_filtrados if p['estado'] == 'Pendiente']),
                'En curso': len([p for p in partes_filtrados if p['estado'] == 'En curso']),
                'Finalizado': len([p for p in partes_filtrados if p['estado'] == 'Finalizado'])
            }
        }
    }

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    return csv_path, json_path

def agrupar_por_campo(partes, campo):
    """Agrupa partes por un campo específico"""
    grupos = {}

    for parte in partes:
        valor = parte.get(campo, 'Sin especificar')
        if valor not in grupos:
            grupos[valor] = {
                'grupo': valor,
                'cantidad': 0,
                'total_presupuesto': 0.0,
                'total_certificado': 0.0,
                'total_pendiente': 0.0
            }

        grupos[valor]['cantidad'] += 1
        grupos[valor]['total_presupuesto'] += parte['presupuesto']
        grupos[valor]['total_certificado'] += parte['certificado']
        grupos[valor]['total_pendiente'] += parte['pendiente']

    # Redondear valores
    for grupo in grupos.values():
        grupo['total_presupuesto'] = round(grupo['total_presupuesto'], 2)
        grupo['total_certificado'] = round(grupo['total_certificado'], 2)
        grupo['total_pendiente'] = round(grupo['total_pendiente'], 2)

    return list(grupos.values())

def generar_informes_agrupados(partes):
    """Genera informes con diferentes agrupaciones"""
    subdir = OUTPUT_DIR / "por_periodos_y_grupos"
    subdir.mkdir(exist_ok=True)

    informes_generados = []

    # Agrupaciones simples
    agrupaciones = [
        ('mes', 'Informe_Por_Mes.csv'),
        ('año', 'Informe_Por_Año.csv'),
        ('estado', 'Informe_Por_Estado.csv'),
        ('provincia', 'Informe_Por_Provincia.csv'),
        ('comarca', 'Informe_Por_Comarca.csv'),
        ('municipio', 'Informe_Por_Municipio.csv'),
        ('tipo_trabajo', 'Informe_Por_Tipo_Trabajo.csv')
    ]

    for campo, nombre_archivo in agrupaciones:
        grupos = agrupar_por_campo(partes, campo)
        filepath = subdir / nombre_archivo

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if grupos:
                writer = csv.DictWriter(f, fieldnames=grupos[0].keys())
                writer.writeheader()
                writer.writerows(grupos)

        informes_generados.append(filepath)
        print(f"   ✅ {nombre_archivo}: {len(grupos)} grupos")

    # Agrupación combinada: Provincia + Estado
    print(f"\n   Generando agrupación combinada: Provincia + Estado...")
    grupos_combinados = {}

    for parte in partes:
        clave = (parte['provincia'], parte['estado'])
        if clave not in grupos_combinados:
            grupos_combinados[clave] = {
                'provincia': parte['provincia'],
                'estado': parte['estado'],
                'cantidad': 0,
                'total_presupuesto': 0.0,
                'total_certificado': 0.0,
                'total_pendiente': 0.0
            }

        grupos_combinados[clave]['cantidad'] += 1
        grupos_combinados[clave]['total_presupuesto'] += parte['presupuesto']
        grupos_combinados[clave]['total_certificado'] += parte['certificado']
        grupos_combinados[clave]['total_pendiente'] += parte['pendiente']

    # Redondear y convertir a lista
    for grupo in grupos_combinados.values():
        grupo['total_presupuesto'] = round(grupo['total_presupuesto'], 2)
        grupo['total_certificado'] = round(grupo['total_certificado'], 2)
        grupo['total_pendiente'] = round(grupo['total_pendiente'], 2)

    grupos_lista = list(grupos_combinados.values())
    filepath = subdir / "Informe_Por_Provincia_y_Estado.csv"

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        if grupos_lista:
            writer = csv.DictWriter(f, fieldnames=grupos_lista[0].keys())
            writer.writeheader()
            writer.writerows(grupos_lista)

    informes_generados.append(filepath)
    print(f"   ✅ Informe_Por_Provincia_y_Estado.csv: {len(grupos_lista)} combinaciones")

    return informes_generados

def generar_resumen_ejecutivo(partes):
    """Genera un resumen ejecutivo con estadísticas generales"""
    filepath = OUTPUT_DIR / "RESUMEN_EJECUTIVO.json"

    total_presupuesto = sum(p['presupuesto'] for p in partes)
    total_certificado = sum(p['certificado'] for p in partes)
    total_pendiente = sum(p['pendiente'] for p in partes)

    resumen = {
        'fecha_generacion': datetime.now().isoformat(),
        'total_partes': len(partes),
        'importes_totales': {
            'presupuesto': round(total_presupuesto, 2),
            'certificado': round(total_certificado, 2),
            'pendiente': round(total_pendiente, 2),
            'porcentaje_certificado': round((total_certificado / total_presupuesto * 100) if total_presupuesto > 0 else 0, 2)
        },
        'distribucion_estados': {
            'Pendiente': {
                'cantidad': len([p for p in partes if p['estado'] == 'Pendiente']),
                'presupuesto': round(sum(p['presupuesto'] for p in partes if p['estado'] == 'Pendiente'), 2)
            },
            'En curso': {
                'cantidad': len([p for p in partes if p['estado'] == 'En curso']),
                'presupuesto': round(sum(p['presupuesto'] for p in partes if p['estado'] == 'En curso'), 2)
            },
            'Finalizado': {
                'cantidad': len([p for p in partes if p['estado'] == 'Finalizado']),
                'presupuesto': round(sum(p['presupuesto'] for p in partes if p['estado'] == 'Finalizado'), 2)
            }
        },
        'distribucion_temporal': {
            'por_año': {},
            'por_mes': {}
        },
        'distribucion_geografica': {
            'por_provincia': {},
            'por_comarca': {},
            'por_municipio': {}
        },
        'top_provincias': [],
        'top_tipos_trabajo': []
    }

    # Distribución temporal
    for parte in partes:
        año = str(parte['año'])
        mes = parte['mes']

        if año not in resumen['distribucion_temporal']['por_año']:
            resumen['distribucion_temporal']['por_año'][año] = {'cantidad': 0, 'presupuesto': 0}
        resumen['distribucion_temporal']['por_año'][año]['cantidad'] += 1
        resumen['distribucion_temporal']['por_año'][año]['presupuesto'] += parte['presupuesto']

        if mes not in resumen['distribucion_temporal']['por_mes']:
            resumen['distribucion_temporal']['por_mes'][mes] = {'cantidad': 0, 'presupuesto': 0}
        resumen['distribucion_temporal']['por_mes'][mes]['cantidad'] += 1
        resumen['distribucion_temporal']['por_mes'][mes]['presupuesto'] += parte['presupuesto']

    # Redondear valores temporales
    for año_data in resumen['distribucion_temporal']['por_año'].values():
        año_data['presupuesto'] = round(año_data['presupuesto'], 2)
    for mes_data in resumen['distribucion_temporal']['por_mes'].values():
        mes_data['presupuesto'] = round(mes_data['presupuesto'], 2)

    # Distribución geográfica
    for parte in partes:
        provincia = parte['provincia']
        if provincia not in resumen['distribucion_geografica']['por_provincia']:
            resumen['distribucion_geografica']['por_provincia'][provincia] = {'cantidad': 0, 'presupuesto': 0}
        resumen['distribucion_geografica']['por_provincia'][provincia]['cantidad'] += 1
        resumen['distribucion_geografica']['por_provincia'][provincia]['presupuesto'] += parte['presupuesto']

    # Redondear y ordenar
    for prov_data in resumen['distribucion_geografica']['por_provincia'].values():
        prov_data['presupuesto'] = round(prov_data['presupuesto'], 2)

    # Top 5 provincias
    provincias_ordenadas = sorted(
        resumen['distribucion_geografica']['por_provincia'].items(),
        key=lambda x: x[1]['presupuesto'],
        reverse=True
    )[:5]
    resumen['top_provincias'] = [
        {'nombre': prov, 'cantidad': data['cantidad'], 'presupuesto': data['presupuesto']}
        for prov, data in provincias_ordenadas
    ]

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(resumen, f, indent=2, ensure_ascii=False)

    return filepath

def analizar_archivos(output_dir):
    """Analiza todos los archivos generados"""
    print(f"\n{'=' * 80}")
    print("  📊 ANÁLISIS DE ARCHIVOS GENERADOS")
    print(f"{'=' * 80}\n")

    archivos_csv = list(output_dir.rglob("*.csv"))
    archivos_json = list(output_dir.rglob("*.json"))

    print(f"Total de archivos generados:")
    print(f"  - CSV: {len(archivos_csv)}")
    print(f"  - JSON: {len(archivos_json)}")
    print(f"  - TOTAL: {len(archivos_csv) + len(archivos_json)}")

    # Análisis detallado de CSV
    print(f"\n{'─' * 80}")
    print("  ANÁLISIS DETALLADO DE ARCHIVOS CSV")
    print(f"{'─' * 80}\n")

    for csv_file in sorted(archivos_csv):
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                num_rows = len(rows) - 1  # Restar cabecera
                num_cols = len(rows[0]) if rows else 0
                tamaño_kb = csv_file.stat().st_size / 1024

                print(f"  📄 {csv_file.relative_to(output_dir)}")
                print(f"     • Filas: {num_rows}")
                print(f"     • Columnas: {num_cols}")
                print(f"     • Tamaño: {tamaño_kb:.2f} KB")

                # Mostrar cabecera
                if rows:
                    print(f"     • Campos: {', '.join(rows[0][:5])}{'...' if len(rows[0]) > 5 else ''}")
                print()
        except Exception as e:
            print(f"  ❌ {csv_file.name}: Error al analizar ({e})\n")

    # Análisis de JSON
    if archivos_json:
        print(f"\n{'─' * 80}")
        print("  ANÁLISIS DE ARCHIVOS JSON")
        print(f"{'─' * 80}\n")

        for json_file in sorted(archivos_json):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    tamaño_kb = json_file.stat().st_size / 1024

                    print(f"  📋 {json_file.relative_to(output_dir)}")
                    print(f"     • Tamaño: {tamaño_kb:.2f} KB")

                    # Mostrar claves principales
                    if isinstance(data, dict):
                        print(f"     • Claves: {', '.join(list(data.keys())[:5])}{'...' if len(data.keys()) > 5 else ''}")
                    print()
            except Exception as e:
                print(f"  ❌ {json_file.name}: Error al analizar ({e})\n")

    # Crear reporte en texto
    reporte_path = output_dir / "ANALISIS_COMPLETO.txt"
    with open(reporte_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("  ANÁLISIS EXHAUSTIVO DE INFORMES GENERADOS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Directorio: {output_dir}\n\n")

        f.write("RESUMEN:\n")
        f.write(f"  Total archivos: {len(archivos_csv) + len(archivos_json)}\n")
        f.write(f"  - CSV: {len(archivos_csv)}\n")
        f.write(f"  - JSON: {len(archivos_json)}\n\n")

        f.write("ARCHIVOS CSV:\n")
        f.write("-" * 80 + "\n")
        for csv_file in sorted(archivos_csv):
            try:
                with open(csv_file, 'r', encoding='utf-8') as csvf:
                    reader = csv.reader(csvf)
                    rows = list(reader)
                    num_rows = len(rows) - 1
                    num_cols = len(rows[0]) if rows else 0

                    f.write(f"\n{csv_file.relative_to(output_dir)}\n")
                    f.write(f"  Filas: {num_rows}\n")
                    f.write(f"  Columnas: {num_cols}\n")
                    f.write(f"  Tamaño: {csv_file.stat().st_size} bytes\n")
                    if rows:
                        f.write(f"  Campos: {', '.join(rows[0])}\n")
            except:
                f.write(f"\n{csv_file.name}: Error al analizar\n")

        f.write("\n\n" + "=" * 80 + "\n")
        f.write("FIN DEL ANÁLISIS\n")
        f.write("=" * 80 + "\n")

    print(f"\n  ✅ Reporte completo guardado en: {reporte_path.relative_to(output_dir.parent)}\n")
    return reporte_path

# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def main():
    """Función principal"""
    print("=" * 80)
    print("  🚀 GENERADOR DE EJEMPLOS DE INFORMES")
    print("=" * 80)

    # Paso 1: Generar datos
    print(f"\n{'─' * 80}")
    print("  1️⃣  Generando datos de ejemplo")
    print(f"{'─' * 80}\n")

    generador = GeneradorDatos()
    partes = generador.generar_partes(100)
    print(f"   ✅ Generados 100 partes de ejemplo")

    # Estadísticas
    print(f"\n   Estadísticas:")
    print(f"   • Total presupuesto: €{sum(p['presupuesto'] for p in partes):,.2f}")
    print(f"   • Total certificado: €{sum(p['certificado'] for p in partes):,.2f}")
    print(f"   • Pendiente: €{sum(p['pendiente'] for p in partes):,.2f}")

    # Paso 2: Generar informe básico
    print(f"\n{'─' * 80}")
    print("  2️⃣  Generando informe básico")
    print(f"{'─' * 80}\n")

    informe_basico = generar_informe_basico(partes, "Listado_Completo_Partes.csv")
    print(f"   ✅ {informe_basico.name}")

    # Paso 3: Generar informes por partidas (selecciones aleatorias)
    print(f"\n{'─' * 80}")
    print("  3️⃣  Generando informes por partidas (5 selecciones aleatorias)")
    print(f"{'─' * 80}\n")

    todos_codigos = [p['codigo'] for p in partes]

    for i in range(5):
        num_partidas = random.randint(5, 15)
        partidas_selec = random.sample(todos_codigos, num_partidas)
        nombre = f"Selección_Aleatoria_#{i+1}"

        csv_path, json_path = generar_informe_por_partidas(partes, nombre, partidas_selec)
        print(f"   ✅ {nombre}: {num_partidas} partidas → 2 archivos")

    # Paso 4: Generar informes agrupados
    print(f"\n{'─' * 80}")
    print("  4️⃣  Generando informes agrupados (períodos y dimensiones)")
    print(f"{'─' * 80}\n")

    generar_informes_agrupados(partes)

    # Paso 5: Generar resumen ejecutivo
    print(f"\n{'─' * 80}")
    print("  5️⃣  Generando resumen ejecutivo")
    print(f"{'─' * 80}\n")

    resumen_path = generar_resumen_ejecutivo(partes)
    print(f"   ✅ {resumen_path.name}")

    # Paso 6: Analizar archivos generados
    print(f"\n{'─' * 80}")
    print("  6️⃣  Analizando archivos generados")
    print(f"{'─' * 80}")

    analizar_archivos(OUTPUT_DIR)

    # Resumen final
    print("=" * 80)
    print("  ✅ PROCESO COMPLETADO")
    print("=" * 80)
    print(f"\n  Todos los ejemplos han sido generados en:")
    print(f"    {OUTPUT_DIR}\n")
    print(f"  Revisa el archivo ANALISIS_COMPLETO.txt para ver el análisis detallado.\n")

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
