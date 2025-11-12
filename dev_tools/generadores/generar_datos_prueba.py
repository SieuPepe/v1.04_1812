#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar datos de prueba en las tablas del sistema de informes.
Crea tablas de dimensión y registros en tbl_partes con datos aleatorios.

ESTRUCTURA CORRECTA:
- tbl_partes.codigo: Código único generado automáticamente (no FK)
- Dimensiones: red, tipo_trabajo, codigo_trabajo, comarca, municipio, provincia
- NO existe dim_ot (cada parte tiene código único)
"""

import random
import sys
import os
from datetime import datetime, timedelta

# Añadir el directorio raíz al path para poder importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from script.db_connection import get_project_connection


def crear_tablas_dimension(cursor, schema):
    """Crea las tablas de dimensión si no existen"""
    print("Creando tablas de dimensión...")

    # Tabla dim_red
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {schema}.dim_red (
            id INT AUTO_INCREMENT PRIMARY KEY,
            codigo VARCHAR(50),
            descripcion VARCHAR(255) NOT NULL,
            activo TINYINT DEFAULT 1
        )
    """)

    # Tabla dim_tipo_trabajo
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {schema}.dim_tipo_trabajo (
            id INT AUTO_INCREMENT PRIMARY KEY,
            codigo VARCHAR(50),
            tipo_codigo VARCHAR(10) COMMENT 'Prefijo para numeración: OT, GF, TP',
            descripcion VARCHAR(255) NOT NULL,
            activo TINYINT DEFAULT 1
        )
    """)

    # Tabla dim_codigo_trabajo (dim_cod_trabajo)
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {schema}.dim_codigo_trabajo (
            id INT AUTO_INCREMENT PRIMARY KEY,
            codigo VARCHAR(50),
            descripcion VARCHAR(255) NOT NULL,
            activo TINYINT DEFAULT 1
        )
    """)

    # Tabla dim_tipos_rep (Tipos de Reparación)
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {schema}.dim_tipos_rep (
            id INT AUTO_INCREMENT PRIMARY KEY,
            codigo VARCHAR(50),
            descripcion VARCHAR(255) NOT NULL,
            activo TINYINT DEFAULT 1
        )
    """)

    # Tabla dim_provincias
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {schema}.dim_provincias (
            id INT AUTO_INCREMENT PRIMARY KEY,
            codigo VARCHAR(10),
            nombre VARCHAR(100) NOT NULL,
            nombre_euskera VARCHAR(100) COMMENT 'Nombre en euskera',
            activo TINYINT DEFAULT 1
        )
    """)

    # Tabla dim_comarcas
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {schema}.dim_comarcas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            codigo VARCHAR(20),
            nombre VARCHAR(100) NOT NULL,
            provincia_id INT,
            activo TINYINT DEFAULT 1,
            FOREIGN KEY (provincia_id) REFERENCES {schema}.dim_provincias(id)
        )
    """)

    # Tabla dim_municipios
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {schema}.dim_municipios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            codigo VARCHAR(20),
            nombre VARCHAR(100) NOT NULL,
            comarca_id INT,
            provincia_id INT,
            activo TINYINT DEFAULT 1,
            FOREIGN KEY (comarca_id) REFERENCES {schema}.dim_comarcas(id),
            FOREIGN KEY (provincia_id) REFERENCES {schema}.dim_provincias(id)
        )
    """)

    print("✓ Tablas de dimensión creadas")


def crear_tabla_partes(cursor, schema):
    """Crea la tabla tbl_partes si no existe"""
    print("Creando tabla tbl_partes...")

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {schema}.tbl_partes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            codigo VARCHAR(50) NOT NULL UNIQUE,
            descripcion TEXT,
            estado VARCHAR(50),
            red_id INT,
            tipo_trabajo_id INT,
            cod_trabajo_id INT,
            tipo_rep_id INT,
            comarca_id INT,
            municipio_id INT,
            provincia_id INT,
            presupuesto DECIMAL(10,2),
            certificado DECIMAL(10,2),
            fecha_inicio DATE,
            fecha_fin DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (red_id) REFERENCES {schema}.dim_red(id),
            FOREIGN KEY (tipo_trabajo_id) REFERENCES {schema}.dim_tipo_trabajo(id),
            FOREIGN KEY (cod_trabajo_id) REFERENCES {schema}.dim_codigo_trabajo(id),
            FOREIGN KEY (tipo_rep_id) REFERENCES {schema}.dim_tipos_rep(id),
            FOREIGN KEY (comarca_id) REFERENCES {schema}.dim_comarcas(id),
            FOREIGN KEY (municipio_id) REFERENCES {schema}.dim_municipios(id),
            FOREIGN KEY (provincia_id) REFERENCES {schema}.dim_provincias(id)
        )
    """)

    print("✓ Tabla tbl_partes creada")


def poblar_dim_provincias(cursor, schema):
    """Pobla la tabla dim_provincias con provincias españolas de ejemplo"""
    print("Poblando dim_provincias...")

    # Primero verificar si la columna nombre_euskera existe
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = %s
        AND TABLE_NAME = 'dim_provincias'
        AND COLUMN_NAME = 'nombre_euskera'
    """, (schema,))

    tiene_nombre_euskera = cursor.fetchone()[0] > 0

    # Si no existe nombre_euskera, agregarla
    if not tiene_nombre_euskera:
        print("  Agregando columna nombre_euskera a dim_provincias...")
        cursor.execute(f"""
            ALTER TABLE {schema}.dim_provincias
            ADD COLUMN nombre_euskera VARCHAR(100) AFTER nombre
        """)

    # Provincias con formato: (codigo, nombre, nombre_euskera)
    provincias = [
        ("01", "Álava", "Araba"),
        ("48", "Bizkaia", "Bizkaia"),
        ("20", "Gipuzkoa", "Gipuzkoa"),
        ("31", "Navarra", "Nafarroa"),
        ("08", "Barcelona", None),
        ("17", "Girona", None),
        ("25", "Lleida", None),
        ("43", "Tarragona", None),
        ("28", "Madrid", None),
        ("46", "Valencia", None)
    ]

    for codigo, nombre, nombre_euskera in provincias:
        if nombre_euskera:
            cursor.execute(f"""
                INSERT INTO {schema}.dim_provincias (codigo, nombre, nombre_euskera, activo)
                VALUES (%s, %s, %s, 1)
                ON DUPLICATE KEY UPDATE
                    nombre = VALUES(nombre),
                    nombre_euskera = VALUES(nombre_euskera)
            """, (codigo, nombre, nombre_euskera))
        else:
            cursor.execute(f"""
                INSERT INTO {schema}.dim_provincias (codigo, nombre, activo)
                VALUES (%s, %s, 1)
                ON DUPLICATE KEY UPDATE nombre = VALUES(nombre)
            """, (codigo, nombre))

    print(f"✓ {len(provincias)} provincias insertadas")


def poblar_dim_comarcas(cursor, schema):
    """Pobla la tabla dim_comarcas con comarcas de ejemplo"""
    print("Poblando dim_comarcas...")

    # Obtener IDs de provincias
    cursor.execute(f"SELECT id, nombre FROM {schema}.dim_provincias")
    provincias_map = {nombre: id for id, nombre in cursor.fetchall()}

    comarcas = [
        ("BARCELONES", "Barcelonés", "Barcelona"),
        ("VALLES-OCC", "Vallès Occidental", "Barcelona"),
        ("VALLES-OR", "Vallès Oriental", "Barcelona"),
        ("BAIX-LLOB", "Baix Llobregat", "Barcelona"),
        ("MARESME", "Maresme", "Barcelona"),
        ("GARROTXA", "La Garrotxa", "Girona"),
        ("SELVA", "La Selva", "Girona"),
        ("ALT-EMPORDA", "Alt Empordà", "Girona"),
        ("SEGARRA", "La Segarra", "Lleida"),
        ("URGELL", "L'Urgell", "Lleida"),
        ("BAIX-EBRE", "Baix Ebre", "Tarragona"),
        ("TARRAGONÈS", "Tarragonès", "Tarragona")
    ]

    for codigo, nombre, provincia_nombre in comarcas:
        provincia_id = provincias_map.get(provincia_nombre)
        if provincia_id:
            cursor.execute(f"""
                INSERT INTO {schema}.dim_comarcas (codigo, nombre, provincia_id, activo)
                VALUES (%s, %s, %s, 1)
                ON DUPLICATE KEY UPDATE nombre = VALUES(nombre)
            """, (codigo, nombre, provincia_id))

    print(f"✓ {len(comarcas)} comarcas insertadas")


def poblar_dim_municipios(cursor, schema):
    """Pobla la tabla dim_municipios con municipios de ejemplo"""
    print("Poblando dim_municipios...")

    # Obtener IDs de comarcas y provincias
    cursor.execute(f"SELECT id, nombre FROM {schema}.dim_comarcas")
    comarcas_map = {nombre: id for id, nombre in cursor.fetchall()}

    cursor.execute(f"SELECT id, nombre FROM {schema}.dim_provincias")
    provincias_map = {nombre: id for id, nombre in cursor.fetchall()}

    municipios = [
        ("08019", "Barcelona", "Barcelonés", "Barcelona"),
        ("08096", "Hospitalet de Llobregat", "Barcelonés", "Barcelona"),
        ("08245", "Sabadell", "Vallès Occidental", "Barcelona"),
        ("08279", "Terrassa", "Vallès Occidental", "Barcelona"),
        ("08307", "Granollers", "Vallès Oriental", "Barcelona"),
        ("08121", "Cornellà de Llobregat", "Baix Llobregat", "Barcelona"),
        ("08194", "Sant Boi de Llobregat", "Baix Llobregat", "Barcelona"),
        ("08169", "Mataró", "Maresme", "Barcelona"),
        ("17007", "Banyoles", "La Garrotxa", "Girona"),
        ("17079", "Girona", "La Selva", "Girona"),
        ("25120", "Lleida", "La Segarra", "Lleida"),
        ("43148", "Tarragona", "Tarragonès", "Tarragona"),
        ("43123", "Reus", "Baix Ebre", "Tarragona")
    ]

    for codigo, nombre, comarca_nombre, provincia_nombre in municipios:
        comarca_id = comarcas_map.get(comarca_nombre)
        provincia_id = provincias_map.get(provincia_nombre)
        if comarca_id and provincia_id:
            cursor.execute(f"""
                INSERT INTO {schema}.dim_municipios (codigo, nombre, comarca_id, provincia_id, activo)
                VALUES (%s, %s, %s, %s, 1)
                ON DUPLICATE KEY UPDATE nombre = VALUES(nombre)
            """, (codigo, nombre, comarca_id, provincia_id))

    print(f"✓ {len(municipios)} municipios insertados")


def poblar_dim_red(cursor, schema):
    """Pobla la tabla dim_red con datos de prueba"""
    print("Poblando dim_red...")

    redes = [
        ("RED-MT-01", "Red Media Tensión Zona Industrial"),
        ("RED-MT-02", "Red Media Tensión Zona Residencial"),
        ("RED-BT-01", "Red Baja Tensión Centro Ciudad"),
        ("RED-BT-02", "Red Baja Tensión Polígono A"),
        ("RED-AT-01", "Red Alta Tensión Línea Principal"),
        ("RED-AT-02", "Red Alta Tensión Circuito Secundario"),
        ("RED-DIST-01", "Red Distribución Sector Norte"),
        ("RED-DIST-02", "Red Distribución Sector Sur"),
        ("RED-SUB-01", "Subestación Transformadora Principal"),
        ("RED-SUB-02", "Subestación Transformadora Auxiliar")
    ]

    for codigo, descripcion in redes:
        cursor.execute(f"""
            INSERT INTO {schema}.dim_red (codigo, descripcion, activo)
            VALUES (%s, %s, 1)
            ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion)
        """, (codigo, descripcion))

    print(f"✓ {len(redes)} redes insertadas")


def poblar_dim_tipo_trabajo(cursor, schema):
    """Pobla la tabla dim_tipo_trabajo con datos de prueba

    IMPORTANTE: Los códigos OT, GF, TP se usan para generar numeración independiente:
    - OT (Órdenes de Trabajo): OT-2025-0001, OT-2025-0002, ...
    - GF (Garantía y Fallos): GF-2025-0001, GF-2025-0002, ...
    - TP (Trabajos Programados): TP-2025-0001, TP-2025-0002, ...
    """
    print("Poblando dim_tipo_trabajo...")

    # Primero verificar si la columna tipo_codigo existe
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = %s
        AND TABLE_NAME = 'dim_tipo_trabajo'
        AND COLUMN_NAME = 'tipo_codigo'
    """, (schema,))

    tiene_tipo_codigo = cursor.fetchone()[0] > 0

    # Si no existe tipo_codigo, agregarla
    if not tiene_tipo_codigo:
        print("  Agregando columna tipo_codigo a dim_tipo_trabajo...")
        cursor.execute(f"""
            ALTER TABLE {schema}.dim_tipo_trabajo
            ADD COLUMN tipo_codigo VARCHAR(10) AFTER codigo
        """)

    # Datos con formato: (codigo, tipo_codigo, descripcion)
    # tipo_codigo es el prefijo que se usa para generar el número de parte
    tipos = [
        ("001", "OT", "Órdenes de Trabajo"),
        ("002", "GF", "Garantía y Fallos"),
        ("003", "TP", "Trabajos Programados")
    ]

    for codigo, tipo_codigo, descripcion in tipos:
        cursor.execute(f"""
            INSERT INTO {schema}.dim_tipo_trabajo (codigo, tipo_codigo, descripcion, activo)
            VALUES (%s, %s, %s, 1)
            ON DUPLICATE KEY UPDATE
                tipo_codigo = VALUES(tipo_codigo),
                descripcion = VALUES(descripcion)
        """, (codigo, tipo_codigo, descripcion))

    print(f"✓ {len(tipos)} tipos de trabajo insertados (OT, GF, TP)")


def poblar_dim_codigo_trabajo(cursor, schema):
    """Pobla la tabla dim_codigo_trabajo con códigos de trabajo"""
    print("Poblando dim_codigo_trabajo...")

    codigos = [
        ("1", "Mantenimiento preventivo saneamiento"),
        ("2", "Limpieza captaciones"),
        ("3", "Mantenimiento fosas sépticas"),
        ("4", "Inventario y digitalización redes abastecimiento"),
        ("5", "Inventario y digitalización redes saneamiento"),
        ("6", "Inventario y digitalización aducción"),
        ("7", "Localización fugas abastecimiento"),
        ("8", "Instalación contadores"),
        ("9", "Desinstalación contadores"),
        ("10", "Sustitución contadores"),
        ("11", "Lectura contadores sectoriales"),
        ("12", "Cortes de agua"),
        ("13", "Asistencia técnica a URBIDE y organismos públicos"),
        ("14", "Maniobras válvulas"),
        ("15", "Gestión de la explotación"),
        ("16", "Limpieza colectores pluviales"),
        ("17", "Limpieza de red abastecimiento"),
        ("18", "Ejecución y conexión acometida"),
        ("19", "Revisión de sectores"),
        ("20", "Localización de fugas en Saneamiento"),
        ("21", "Realización de informes de Saneamiento"),
        ("22", "Realización de informes de Abastecimiento")
    ]

    for codigo, descripcion in codigos:
        cursor.execute(f"""
            INSERT INTO {schema}.dim_codigo_trabajo (codigo, descripcion, activo)
            VALUES (%s, %s, 1)
            ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion)
        """, (codigo, descripcion))

    print(f"✓ {len(codigos)} códigos de trabajo insertados")


def poblar_dim_tipos_rep(cursor, schema):
    """Pobla la tabla dim_tipos_rep con los tipos de reparación"""
    print("Poblando dim_tipos_rep...")

    tipos_rep = [
        ("FUGA", "Fuga"),
        ("ATASCO", "Atasco"),
        ("OTROS", "Otros")
    ]

    for codigo, descripcion in tipos_rep:
        cursor.execute(f"""
            INSERT INTO {schema}.dim_tipos_rep (codigo, descripcion, activo)
            VALUES (%s, %s, 1)
            ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion)
        """, (codigo, descripcion))

    print(f"✓ {len(tipos_rep)} tipos de reparación insertados")


def generar_codigo_parte(tipo_codigo, correlativo):
    """
    Genera código único del parte según tipo de intervención y correlativo.
    Ejemplo: MANT-PREV-2024-0001
    """
    año = datetime.now().year
    return f"{tipo_codigo}-{año}-{correlativo:04d}"


def poblar_tbl_partes(cursor, schema, num_partes=50):
    """Pobla la tabla tbl_partes con datos aleatorios"""
    print(f"Generando {num_partes} partes de prueba...")

    # Obtener IDs de las dimensiones
    cursor.execute(f"SELECT id, codigo FROM {schema}.dim_red")
    red_data = cursor.fetchall()
    red_ids = [row[0] for row in red_data]

    cursor.execute(f"SELECT id, codigo FROM {schema}.dim_tipo_trabajo")
    tipo_data = cursor.fetchall()
    tipo_ids = [row[0] for row in tipo_data]
    tipo_codigos = {row[0]: row[1] for row in tipo_data}

    cursor.execute(f"SELECT id FROM {schema}.dim_codigo_trabajo")
    cod_trabajo_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute(f"SELECT id FROM {schema}.dim_tipos_rep")
    tipo_rep_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute(f"SELECT id FROM {schema}.dim_provincias")
    provincia_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute(f"SELECT id FROM {schema}.dim_comarcas")
    comarca_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute(f"SELECT id FROM {schema}.dim_municipios")
    municipio_ids = [row[0] for row in cursor.fetchall()]

    estados = ["Pendiente", "En curso", "Finalizado"]

    descripciones_base = [
        "Instalación de transformador trifásico",
        "Revisión de línea aérea",
        "Reparación de subestación",
        "Mantenimiento de equipos de control",
        "Conexión de nuevo cliente",
        "Actualización de sistema SCADA",
        "Inspección de torres",
        "Cambio de conductores",
        "Instalación de medidores inteligentes",
        "Refuerzo de protecciones",
        "Limpieza de aisladores",
        "Calibración de relés",
        "Pruebas de resistencia",
        "Revisión de puestas a tierra",
        "Instalación de seccionadores",
        "Modernización de celdas MT",
        "Reparación de averías",
        "Extensión de red BT",
        "Instalación de sistemas anti-hurto",
        "Verificación de tensiones"
    ]

    # Fecha base para generar fechas aleatorias
    fecha_base = datetime(2024, 1, 1)

    partes_insertados = 0
    for i in range(1, num_partes + 1):
        # Generar código según tipo de trabajo
        tipo_trabajo_id = random.choice(tipo_ids) if tipo_ids else None
        tipo_codigo = tipo_codigos.get(tipo_trabajo_id, "PARTE")
        codigo = generar_codigo_parte(tipo_codigo, i)

        descripcion = random.choice(descripciones_base) + f" - Zona {random.randint(1, 20)}"
        estado = random.choice(estados)
        red_id = random.choice(red_ids) if red_ids else None
        cod_trabajo_id = random.choice(cod_trabajo_ids) if cod_trabajo_ids else None
        tipo_rep_id = random.choice(tipo_rep_ids) if tipo_rep_ids else None
        provincia_id = random.choice(provincia_ids) if provincia_ids else None
        comarca_id = random.choice(comarca_ids) if comarca_ids else None
        municipio_id = random.choice(municipio_ids) if municipio_ids else None

        # Generar presupuesto entre 1000 y 50000
        presupuesto = round(random.uniform(1000, 50000), 2)

        # Certificado depende del estado
        if estado == "Finalizado":
            certificado = round(presupuesto * random.uniform(0.85, 1.05), 2)
        elif estado == "En curso":
            certificado = round(presupuesto * random.uniform(0.2, 0.7), 2)
        else:  # Pendiente
            certificado = 0.0

        # Generar fechas
        dias_offset = random.randint(0, 300)
        fecha_inicio = fecha_base + timedelta(days=dias_offset)

        if estado == "Finalizado":
            duracion = random.randint(5, 60)
            fecha_fin = fecha_inicio + timedelta(days=duracion)
        elif estado == "En curso":
            if random.random() > 0.5:
                duracion = random.randint(10, 90)
                fecha_fin = fecha_inicio + timedelta(days=duracion)
            else:
                fecha_fin = None
        else:  # Pendiente
            fecha_fin = None

        try:
            cursor.execute(f"""
                INSERT INTO {schema}.tbl_partes
                (codigo, descripcion, estado, red_id, tipo_trabajo_id, cod_trabajo_id, tipo_rep_id,
                 comarca_id, municipio_id, provincia_id, presupuesto, certificado,
                 fecha_inicio, fecha_fin)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (codigo, descripcion, estado, red_id, tipo_trabajo_id, cod_trabajo_id, tipo_rep_id,
                  comarca_id, municipio_id, provincia_id, presupuesto, certificado,
                  fecha_inicio, fecha_fin))
            partes_insertados += 1
        except Exception as e:
            print(f"Error insertando parte {codigo}: {e}")

    print(f"✓ {partes_insertados} partes insertados")


def generar_estadisticas(cursor, schema):
    """Muestra estadísticas de los datos generados"""
    print("\n" + "="*70)
    print("ESTADÍSTICAS DE DATOS GENERADOS")
    print("="*70)

    # Contar partes por estado
    cursor.execute(f"""
        SELECT estado, COUNT(*) as cantidad,
               SUM(presupuesto) as total_presupuesto,
               SUM(certificado) as total_certificado
        FROM {schema}.tbl_partes
        GROUP BY estado
    """)

    print("\n📊 Partes por Estado:")
    print("-" * 70)
    for row in cursor.fetchall():
        estado, cantidad, total_pres, total_cert = row
        pendiente = (total_pres or 0) - (total_cert or 0)
        print(f"  {estado:15} → {cantidad:3} partes | "
              f"Presup: €{total_pres:,.2f} | Cert: €{total_cert:,.2f} | "
              f"Pend: €{pendiente:,.2f}")

    # Total general
    cursor.execute(f"""
        SELECT COUNT(*) as total,
               SUM(presupuesto) as total_presupuesto,
               SUM(certificado) as total_certificado,
               SUM(presupuesto - certificado) as total_pendiente
        FROM {schema}.tbl_partes
    """)

    row = cursor.fetchone()
    print("\n💰 Totales Generales:")
    print("-" * 70)
    print(f"  Total Partes:      {row[0]}")
    print(f"  Presupuesto Total: €{row[1]:,.2f}")
    print(f"  Certificado Total: €{row[2]:,.2f}")
    print(f"  Pendiente Total:   €{row[3]:,.2f}")

    # Contar por Tipo de Trabajo
    cursor.execute(f"""
        SELECT tt.descripcion, COUNT(p.id) as cantidad
        FROM {schema}.tbl_partes p
        JOIN {schema}.dim_tipo_trabajo tt ON p.tipo_trabajo_id = tt.id
        GROUP BY tt.descripcion
        ORDER BY cantidad DESC
        LIMIT 5
    """)

    print("\n🔧 Top 5 Tipos de Trabajo con más partes:")
    print("-" * 70)
    for idx, (tipo_desc, cantidad) in enumerate(cursor.fetchall(), 1):
        print(f"  {idx}. {tipo_desc[:50]:50} → {cantidad} partes")

    # Contar por Provincia
    cursor.execute(f"""
        SELECT pr.nombre, COUNT(p.id) as cantidad
        FROM {schema}.tbl_partes p
        LEFT JOIN {schema}.dim_provincias pr ON p.provincia_id = pr.id
        GROUP BY pr.nombre
        ORDER BY cantidad DESC
        LIMIT 5
    """)

    print("\n🗺️  Top 5 Provincias con más partes:")
    print("-" * 70)
    for idx, (provincia, cantidad) in enumerate(cursor.fetchall(), 1):
        print(f"  {idx}. {provincia if provincia else '(Sin provincia)':30} → {cantidad} partes")

    print("\n" + "="*70)


def main():
    """Función principal"""
    print("\n" + "="*70)
    print("🔧 GENERADOR DE DATOS DE PRUEBA - SISTEMA DE INFORMES")
    print("="*70 + "\n")

    # Solicitar credenciales
    print("Por favor, introduce las credenciales de la base de datos:\n")
    user = input("Usuario MySQL: ").strip() or "root"
    password = input("Contraseña MySQL: ").strip()
    schema = input("Nombre del schema/base de datos: ").strip() or "hydroflow_db"
    num_partes = input("Número de partes a generar (default: 50): ").strip()
    num_partes = int(num_partes) if num_partes else 50

    print(f"\n📡 Conectando a la base de datos '{schema}'...")

    try:
        with get_project_connection(user, password, schema) as conn:
            cursor = conn.cursor()

            # Crear tablas
            crear_tablas_dimension(cursor, schema)
            crear_tabla_partes(cursor, schema)
            conn.commit()

            # Poblar tablas de dimensión geográficas (primero porque tienen dependencias)
            poblar_dim_provincias(cursor, schema)
            conn.commit()
            poblar_dim_comarcas(cursor, schema)
            conn.commit()
            poblar_dim_municipios(cursor, schema)
            conn.commit()

            # Poblar otras dimensiones
            poblar_dim_red(cursor, schema)
            poblar_dim_tipo_trabajo(cursor, schema)
            poblar_dim_codigo_trabajo(cursor, schema)
            poblar_dim_tipos_rep(cursor, schema)
            conn.commit()

            # Poblar tabla de partes
            poblar_tbl_partes(cursor, schema, num_partes)
            conn.commit()

            # Mostrar estadísticas
            generar_estadisticas(cursor, schema)

            print("\n✅ ¡Datos de prueba generados exitosamente!\n")
            print("Ahora puedes probar el sistema de informes con:")
            print("  - Filtros por Estado, Red, Tipo Trabajo, Presupuesto, Fecha")
            print("  - Filtros geográficos por Provincia, Comarca, Municipio")
            print("  - Clasificaciones por cualquier campo")
            print("  - Exportaciones a Excel, Word y PDF")
            print("\n" + "="*70 + "\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
