#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar datos de prueba en las tablas del sistema de informes.
Crea tablas de dimensión y registros en tbl_partes con datos aleatorios.
"""

import random
from datetime import datetime, timedelta
from script.bbdd import get_project_connection


def crear_tablas_dimension(cursor, schema):
    """Crea las tablas de dimensión si no existen"""
    print("Creando tablas de dimensión...")

    # Tabla dim_ot
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {schema}.dim_ot (
            id INT AUTO_INCREMENT PRIMARY KEY,
            descripcion VARCHAR(255) NOT NULL,
            codigo VARCHAR(50),
            activo TINYINT DEFAULT 1
        )
    """)

    # Tabla dim_red
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {schema}.dim_red (
            id INT AUTO_INCREMENT PRIMARY KEY,
            descripcion VARCHAR(255) NOT NULL,
            codigo VARCHAR(50),
            activo TINYINT DEFAULT 1
        )
    """)

    # Tabla dim_tipo_trabajo
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {schema}.dim_tipo_trabajo (
            id INT AUTO_INCREMENT PRIMARY KEY,
            descripcion VARCHAR(255) NOT NULL,
            codigo VARCHAR(50),
            activo TINYINT DEFAULT 1
        )
    """)

    print("✓ Tablas de dimensión creadas")


def crear_tabla_partes(cursor, schema):
    """Crea la tabla tbl_partes si no existe"""
    print("Creando tabla tbl_partes...")

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {schema}.tbl_partes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            codigo VARCHAR(50) NOT NULL,
            descripcion TEXT,
            estado VARCHAR(50),
            ot_id INT,
            red_id INT,
            tipo_trabajo_id INT,
            codigo_trabajo VARCHAR(50),
            presupuesto DECIMAL(10,2),
            certificado DECIMAL(10,2),
            fecha_inicio DATE,
            fecha_fin DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (ot_id) REFERENCES {schema}.dim_ot(id),
            FOREIGN KEY (red_id) REFERENCES {schema}.dim_red(id),
            FOREIGN KEY (tipo_trabajo_id) REFERENCES {schema}.dim_tipo_trabajo(id)
        )
    """)

    print("✓ Tabla tbl_partes creada")


def poblar_dim_ot(cursor, schema):
    """Pobla la tabla dim_ot con datos de prueba"""
    print("Poblando dim_ot...")

    ots = [
        ("OT-2024-001", "Renovación Red Eléctrica Zona Norte"),
        ("OT-2024-002", "Mantenimiento Subestación Central"),
        ("OT-2024-003", "Expansión Red Distribución Sur"),
        ("OT-2024-004", "Modernización Sistema Control"),
        ("OT-2024-005", "Reparación Líneas AT Sector Este"),
        ("OT-2024-006", "Instalación Transformadores Nuevos"),
        ("OT-2024-007", "Actualización Equipos Medición"),
        ("OT-2024-008", "Refuerzo Red Media Tensión"),
        ("OT-2024-009", "Conexiones Nuevos Clientes Industriales"),
        ("OT-2024-010", "Mejora Infraestructura Telecomunicaciones")
    ]

    for codigo, descripcion in ots:
        cursor.execute(f"""
            INSERT INTO {schema}.dim_ot (codigo, descripcion, activo)
            VALUES (%s, %s, 1)
            ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion)
        """, (codigo, descripcion))

    print(f"✓ {len(ots)} OTs insertadas")


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
    """Pobla la tabla dim_tipo_trabajo con datos de prueba"""
    print("Poblando dim_tipo_trabajo...")

    tipos = [
        ("MANT-PREV", "Mantenimiento Preventivo"),
        ("MANT-CORR", "Mantenimiento Correctivo"),
        ("INSTALACION", "Instalación Nueva"),
        ("REPARACION", "Reparación"),
        ("MODERNIZACION", "Modernización"),
        ("INSPECCION", "Inspección Técnica"),
        ("EMERGENCIA", "Atención de Emergencia"),
        ("EXPANSION", "Expansión de Red"),
        ("REEMPLAZO", "Reemplazo de Equipos"),
        ("MEJORA", "Mejora de Infraestructura")
    ]

    for codigo, descripcion in tipos:
        cursor.execute(f"""
            INSERT INTO {schema}.dim_tipo_trabajo (codigo, descripcion, activo)
            VALUES (%s, %s, 1)
            ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion)
        """, (codigo, descripcion))

    print(f"✓ {len(tipos)} tipos de trabajo insertados")


def poblar_tbl_partes(cursor, schema, num_partes=50):
    """Pobla la tabla tbl_partes con datos aleatorios"""
    print(f"Generando {num_partes} partes de prueba...")

    # Obtener IDs de las dimensiones
    cursor.execute(f"SELECT id FROM {schema}.dim_ot")
    ot_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute(f"SELECT id FROM {schema}.dim_red")
    red_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute(f"SELECT id FROM {schema}.dim_tipo_trabajo")
    tipo_trabajo_ids = [row[0] for row in cursor.fetchall()]

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
        codigo = f"PARTE-{2024}-{i:04d}"
        descripcion = random.choice(descripciones_base) + f" - Zona {random.randint(1, 20)}"
        estado = random.choice(estados)
        ot_id = random.choice(ot_ids) if ot_ids else None
        red_id = random.choice(red_ids) if red_ids else None
        tipo_trabajo_id = random.choice(tipo_trabajo_ids) if tipo_trabajo_ids else None
        codigo_trabajo = f"CT-{random.randint(1000, 9999)}"

        # Generar presupuesto entre 1000 y 50000
        presupuesto = round(random.uniform(1000, 50000), 2)

        # Certificado depende del estado
        if estado == "Finalizado":
            certificado = round(presupuesto * random.uniform(0.85, 1.05), 2)  # 85% a 105% del presupuesto
        elif estado == "En curso":
            certificado = round(presupuesto * random.uniform(0.2, 0.7), 2)  # 20% a 70% del presupuesto
        else:  # Pendiente
            certificado = 0.0

        # Generar fechas
        dias_offset = random.randint(0, 300)
        fecha_inicio = fecha_base + timedelta(days=dias_offset)

        if estado == "Finalizado":
            duracion = random.randint(5, 60)
            fecha_fin = fecha_inicio + timedelta(days=duracion)
        elif estado == "En curso":
            # Algunos tienen fecha fin estimada, otros no
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
                (codigo, descripcion, estado, ot_id, red_id, tipo_trabajo_id,
                 codigo_trabajo, presupuesto, certificado, fecha_inicio, fecha_fin)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (codigo, descripcion, estado, ot_id, red_id, tipo_trabajo_id,
                  codigo_trabajo, presupuesto, certificado, fecha_inicio, fecha_fin))
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

    # Contar por OT
    cursor.execute(f"""
        SELECT o.descripcion, COUNT(p.id) as cantidad
        FROM {schema}.tbl_partes p
        JOIN {schema}.dim_ot o ON p.ot_id = o.id
        GROUP BY o.descripcion
        ORDER BY cantidad DESC
        LIMIT 5
    """)

    print("\n🔧 Top 5 OTs con más partes:")
    print("-" * 70)
    for idx, (ot_desc, cantidad) in enumerate(cursor.fetchall(), 1):
        print(f"  {idx}. {ot_desc[:50]:50} → {cantidad} partes")

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

            # Poblar tablas de dimensión
            poblar_dim_ot(cursor, schema)
            poblar_dim_red(cursor, schema)
            poblar_dim_tipo_trabajo(cursor, schema)
            conn.commit()

            # Poblar tabla de partes
            poblar_tbl_partes(cursor, schema, num_partes)
            conn.commit()

            # Mostrar estadísticas
            generar_estadisticas(cursor, schema)

            print("\n✅ ¡Datos de prueba generados exitosamente!\n")
            print("Ahora puedes probar el sistema de informes con:")
            print("  - Filtros por Estado, OT, Red, Presupuesto, Fecha")
            print("  - Clasificaciones por cualquier campo")
            print("  - Exportaciones a Excel, Word y PDF")
            print("\n" + "="*70 + "\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
