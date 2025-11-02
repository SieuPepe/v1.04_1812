#!/usr/bin/env python3
"""
Script para generar 1000 partes aleatorias para pruebas del sistema de informes.
Distribuye los datos entre todos los estados, provincias, municipios, tipos de red, etc.
"""

import sys
import os
from pathlib import Path
import random
from datetime import datetime, timedelta

# Añadir directorio raíz al path
root_dir = Path(__file__).parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from script.db_partes import (
    add_parte_mejorado,
    get_estados_parte,
    get_dim_all,
    get_provincias,
    get_comarcas_by_provincia,
    get_municipios_by_provincia
)
from script.db_connection import get_project_connection

# Configuración
SCHEMA = "cert_dev"

# Permitir pasar credenciales como argumentos o usar valores por defecto
if len(sys.argv) >= 3:
    USER = sys.argv[1]
    PASSWORD = sys.argv[2]
    NUM_PARTES = int(sys.argv[3]) if len(sys.argv) >= 4 else 1000
else:
    USER = "aperez"
    PASSWORD = "WGueXNk9"
    NUM_PARTES = 1000
    print(f"ℹ️  Usando credenciales por defecto: {USER}")
    print(f"ℹ️  Uso: python generar_1000_partes.py <user> <password> [num_partes]")
    print()

# Datos aleatorios para generar contenido realista
TITULOS_BASE = [
    "Reparación de tubería",
    "Instalación nueva",
    "Mantenimiento preventivo",
    "Revisión de sistema",
    "Sustitución de válvula",
    "Reparación de fuga",
    "Instalación de contador",
    "Limpieza de red",
    "Renovación de tramo",
    "Inspección de red",
    "Reparación de arqueta",
    "Instalación de hidrante",
    "Reparación de acometida",
    "Sustitución de tramo",
    "Instalación de válvula",
    "Reparación de junta",
    "Limpieza de depósito",
    "Reparación de bomba",
    "Instalación de medidor",
    "Reparación urgente"
]

DESCRIPCIONES_BASE = [
    "Trabajos de mantenimiento en la red de distribución",
    "Reparación de elemento deteriorado por el paso del tiempo",
    "Instalación de nuevo equipamiento según proyecto",
    "Revisión periódica del sistema de abastecimiento",
    "Sustitución de componente obsoleto",
    "Reparación de avería detectada en inspección",
    "Obras de mejora en infraestructura existente",
    "Trabajos de renovación de red antigua",
    "Instalación según ampliación de red",
    "Reparación de daño por terceros"
]

TRABAJADORES_BASE = [
    "Juan Pérez, Carlos García",
    "María López, Ana Martínez",
    "Pedro Sánchez",
    "Laura Fernández, Miguel Díaz",
    "Antonio Ruiz",
    "Carmen Moreno, José Gil",
    "Francisco Torres, Isabel Romero",
    "Manuel Navarro",
    "Rosa Jiménez, David Muñoz",
    "Elena Álvarez"
]

LOCALIZACIONES_BASE = [
    "Calle Mayor",
    "Avenida Principal",
    "Plaza del Ayuntamiento",
    "Calle San Juan",
    "Avenida de la Constitución",
    "Calle Real",
    "Plaza España",
    "Calle Nueva",
    "Camino Viejo",
    "Carretera Nacional"
]

ESTADOS = ["Pendiente", "En curso", "Finalizado", "Cerrado"]

# Coordenadas GPS del País Vasco (rangos aproximados)
# Álava: lat 42.5-43.1, lon -3.2 a -2.4
# Bizkaia: lat 43.0-43.5, lon -3.2 a -2.6
# Gipuzkoa: lat 43.0-43.4, lon -2.3 a -1.7
GPS_RANGOS = {
    1: {"lat": (42.5, 43.1), "lon": (-3.2, -2.4)},  # Álava
    2: {"lat": (43.0, 43.5), "lon": (-3.2, -2.6)},  # Bizkaia
    3: {"lat": (43.0, 43.4), "lon": (-2.3, -1.7)}   # Gipuzkoa
}

def generar_fecha_aleatoria(inicio, fin):
    """Genera fecha aleatoria entre dos fechas"""
    delta = fin - inicio
    random_days = random.randint(0, delta.days)
    return inicio + timedelta(days=random_days)

def generar_coordenadas_gps(provincia_id):
    """Genera coordenadas GPS dentro del rango de la provincia"""
    rangos = GPS_RANGOS.get(provincia_id, GPS_RANGOS[1])
    lat = round(random.uniform(rangos["lat"][0], rangos["lat"][1]), 6)
    lon = round(random.uniform(rangos["lon"][0], rangos["lon"][1]), 6)
    return lat, lon

def main():
    print("=" * 80)
    print("🔧 GENERADOR DE 1000 PARTES ALEATORIAS")
    print("=" * 80)
    print(f"\nConectando a schema: {SCHEMA}")
    print(f"Usuario: {USER}\n")

    try:
        # Obtener todas las dimensiones
        print("📊 Obteniendo dimensiones de la base de datos...")
        dims = get_dim_all(USER, PASSWORD, SCHEMA)
        provincias = get_provincias(USER, PASSWORD, SCHEMA)

        # Extraer IDs de cada dimensión
        red_ids = [int(item.split(" - ")[0]) for item in dims.get("RED", [])]
        tipo_ids = [int(item.split(" - ")[0]) for item in dims.get("TIPO_TRABAJO", [])]
        cod_ids = [int(item.split(" - ")[0]) for item in dims.get("COD_TRABAJO", [])]
        provincia_ids = [int(item.split(" - ")[0]) for item in provincias]

        print(f"  ✅ Redes disponibles: {len(red_ids)}")
        print(f"  ✅ Tipos de trabajo: {len(tipo_ids)}")
        print(f"  ✅ Códigos de trabajo: {len(cod_ids)}")
        print(f"  ✅ Provincias: {len(provincia_ids)}")

        # Obtener todos los municipios agrupados por provincia
        municipios_por_provincia = {}
        for prov_id in provincia_ids:
            comarcas = get_comarcas_by_provincia(USER, PASSWORD, SCHEMA, prov_id)
            municipios_prov = []
            for comarca in comarcas:
                comarca_id = int(comarca.split(" - ")[0])
                municipios = get_municipios_by_provincia(USER, PASSWORD, SCHEMA, comarca_id=comarca_id)
                municipios_ids = [int(m.split(" - ")[0]) for m in municipios]
                municipios_prov.extend(municipios_ids)
            municipios_por_provincia[prov_id] = municipios_prov
            print(f"  ✅ Municipios provincia {prov_id}: {len(municipios_prov)}")

        print(f"\n🚀 Generando {NUM_PARTES} partes aleatorias...\n")

        # Fechas base para generar partes
        fecha_inicio_base = datetime(2023, 1, 1)
        fecha_fin_base = datetime(2025, 12, 31)

        exitos = 0
        errores = 0

        for i in range(1, NUM_PARTES + 1):
            try:
                # Seleccionar dimensiones aleatorias
                red_id = random.choice(red_ids)
                tipo_id = random.choice(tipo_ids)
                cod_id = random.choice(cod_ids)
                provincia_id = random.choice(provincia_ids)

                # Obtener comarca y municipio de esa provincia
                municipios_disponibles = municipios_por_provincia.get(provincia_id, [])
                if not municipios_disponibles:
                    print(f"  ⚠️  Parte {i}: Sin municipios para provincia {provincia_id}, saltando...")
                    continue

                municipio_id = random.choice(municipios_disponibles)

                # Generar contenido aleatorio
                titulo = random.choice(TITULOS_BASE) + f" #{i}"
                descripcion = random.choice(DESCRIPCIONES_BASE)
                descripcion_corta = descripcion[:100]
                descripcion_larga = descripcion + f". Parte generada automáticamente para pruebas del sistema. ID: {i}"

                # Estado aleatorio (distribución realista)
                estado_weights = [0.30, 0.35, 0.25, 0.10]  # Pendiente, En curso, Finalizado, Cerrado
                estado = random.choices(ESTADOS, weights=estado_weights)[0]

                # Generar fechas lógicas
                fecha_inicio = generar_fecha_aleatoria(fecha_inicio_base, fecha_fin_base - timedelta(days=60))
                fecha_prevista_fin = fecha_inicio + timedelta(days=random.randint(7, 90))

                # Solo asignar fecha_fin si el estado es Finalizado o Cerrado
                fecha_fin = None
                if estado in ["Finalizado", "Cerrado"]:
                    fecha_fin = generar_fecha_aleatoria(fecha_inicio, fecha_prevista_fin + timedelta(days=30))

                # Otros campos
                trabajadores = random.choice(TRABAJADORES_BASE)
                localizacion = random.choice(LOCALIZACIONES_BASE) + f", {random.randint(1, 200)}"
                latitud, longitud = generar_coordenadas_gps(provincia_id)

                # Crear parte
                parte_id, codigo = add_parte_mejorado(
                    USER, PASSWORD, SCHEMA,
                    red_id, tipo_id, cod_id,
                    titulo=titulo,
                    descripcion=descripcion,
                    descripcion_larga=descripcion_larga,
                    descripcion_corta=descripcion_corta,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    fecha_prevista_fin=fecha_prevista_fin,
                    estado_id=ESTADOS.index(estado) + 1,  # Asumiendo IDs 1-4
                    localizacion=localizacion,
                    provincia_id=provincia_id,
                    municipio_id=municipio_id,
                    trabajadores=trabajadores,
                    latitud=latitud,
                    longitud=longitud
                )

                exitos += 1

                # Mostrar progreso cada 50 partes
                if i % 50 == 0:
                    progreso = (i / NUM_PARTES) * 100
                    print(f"  ✅ Progreso: {i}/{NUM_PARTES} ({progreso:.1f}%) - Último: {codigo}")

            except Exception as e:
                errores += 1
                if errores <= 10:  # Solo mostrar primeros 10 errores
                    print(f"  ❌ Error en parte {i}: {e}")

        print("\n" + "=" * 80)
        print("🎉 GENERACIÓN COMPLETADA")
        print("=" * 80)
        print(f"\n✅ Partes creadas exitosamente: {exitos}")
        print(f"❌ Errores: {errores}")
        print(f"📊 Tasa de éxito: {(exitos/NUM_PARTES)*100:.1f}%")

        # Estadísticas de distribución
        print("\n📈 DISTRIBUCIÓN ESPERADA:")
        print(f"  • Estados:")
        print(f"    - Pendiente: ~{int(NUM_PARTES * 0.30)} partes (30%)")
        print(f"    - En curso: ~{int(NUM_PARTES * 0.35)} partes (35%)")
        print(f"    - Finalizado: ~{int(NUM_PARTES * 0.25)} partes (25%)")
        print(f"    - Cerrado: ~{int(NUM_PARTES * 0.10)} partes (10%)")
        print(f"  • Provincias: Distribuido uniformemente entre {len(provincia_ids)} provincias")
        print(f"  • Redes: Distribuido uniformemente entre {len(red_ids)} redes")
        print(f"  • Tipos de trabajo: Distribuido uniformemente entre {len(tipo_ids)} tipos")

        print("\n✨ ¡Listo para probar el sistema de informes!")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
