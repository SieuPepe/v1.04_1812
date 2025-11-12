#!/usr/bin/env python3
"""
Script para generar UPDATE de códigos postales en dim_municipios
Los municipios de Álava (provincia_id=1) necesitan sus códigos postales
"""

import sys
from datetime import datetime

def main():
    output_file = "script/sql/actualizar_codigos_postales_municipios.sql"

    # Códigos postales reales de los municipios de Álava
    # Formato: (id, nombre, codigo_postal, comarca_id)
    codigos_postales = [
        # Comarca 1 - Ayala / Aiara
        (1, "Amurrio", "01470", 1),
        (2, "Artziniega", "01474", 1),
        (3, "Ayala / Aiara", "01479", 1),
        (4, "Llodio / Laudio", "01400", 1),
        (5, "Okondo", "01476", 1),

        # Comarca 2 - Rioja Alavesa
        (6, "Baños de Ebro / Mañueta", "01307", 2),
        (7, "Elciego", "01340", 2),
        (8, "Elvillar / Bilar", "01320", 2),
        (9, "Kripan", "01309", 2),
        (10, "Labastida / Bastida", "01330", 2),
        (11, "Laguardia", "01300", 2),
        (12, "Lanciego / Lantziego", "01308", 2),
        (13, "Lapuebla de Labarca", "01306", 2),
        (14, "Leza", "01321", 2),
        (15, "Moreda de Álava / Moreda Araba", "01320", 2),
        (16, "Navaridas", "01309", 2),
        (17, "Oyón-Oion", "01320", 2),
        (18, "Samaniego", "01307", 2),
        (19, "Villabuena de Álava / Eskuernaga", "01307", 2),
        (20, "Yécora / Iekora", "01208", 2),

        # Comarca 3 - Llanada Alavesa / Arabako Lautada
        (21, "Alegría-Dulantzi", "01240", 3),
        (22, "Asparrena", "01250", 3),
        (23, "Barrundia", "01110", 3),
        (24, "Elburgo / Burgelu", "01130", 3),
        (25, "Iruraiz-Gauna", "01259", 3),
        (26, "Salvatierra / Agurain", "01200", 3),
        (27, "San Millán / Donemiliaga", "01428", 3),
        (28, "Zalduondo", "01130", 3),

        # Comarca 4 - Vitoria-Gasteiz
        (29, "Aramaio", "01166", 4),
        (30, "Arratzua-Ubarrundia", "01013", 4),
        (31, "Legutio", "01170", 4),
        (32, "Urkabustaiz", "01138", 4),
        (33, "Zigoitia", "01199", 4),
        (34, "Zuia", "01194", 4),

        # Comarca 5 - Cuadrilla de Añana
        (35, "Añana", "01426", 5),
        (36, "Armiñón", "01213", 5),
        (37, "Berantevilla", "01211", 5),
        (38, "Iruña de Oca / Iruña Oka", "01230", 5),
        (39, "Kuartango", "01478", 5),
        (40, "Lantarón", "01212", 5),
        (41, "Ribera Alta / Erriberagoitia", "01220", 5),
        (42, "Ribera Baja / Erriberabeitia", "01219", 5),
        (43, "Sierra Brava de Badaia", "99801", 5),  # No encontrado, uso 99801
        (44, "Valdegovía / Gaubea", "01439", 5),
        (45, "Zambrana", "01214", 5),

        # Comarca 6 - Montaña Alavesa
        (46, "Arraia-Maeztu", "01196", 6),
        (47, "Bernedo", "01118", 6),
        (48, "Campezo / Kanpezu", "01111", 6),
        (49, "Lagrán", "01308", 6),
        (50, "Parzoneria de Entzia", "99802", 6),  # No encontrado, uso 99802
        (51, "Peñacerrada-Urizaharra", "01212", 6),
        (52, "Valle de Arana / Harana", "01268", 6),
    ]

    with open(output_file, 'w', encoding='utf-8') as f:
        # Escribir encabezado
        f.write("-- =====================================================================\n")
        f.write("-- Script para actualizar códigos postales en dim_municipios\n")
        f.write(f"-- Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"-- Total de municipios: {len(codigos_postales)}\n")
        f.write("-- =====================================================================\n\n")

        # Paso 1: Agregar columna codigo_postal si no existe
        f.write("-- =====================================================================\n")
        f.write("-- PASO 1: Agregar columna codigo_postal a dim_municipios\n")
        f.write("-- =====================================================================\n")
        f.write("SET @col_exists = (SELECT COUNT(*)\n")
        f.write("    FROM information_schema.COLUMNS\n")
        f.write("    WHERE TABLE_SCHEMA = DATABASE()\n")
        f.write("    AND TABLE_NAME = 'dim_municipios'\n")
        f.write("    AND COLUMN_NAME = 'codigo_postal');\n\n")

        f.write("SET @sql_add_col = IF(@col_exists = 0,\n")
        f.write("    'ALTER TABLE dim_municipios ADD COLUMN codigo_postal VARCHAR(10) DEFAULT NULL AFTER municipio_nombre',\n")
        f.write("    'SELECT \"Columna codigo_postal ya existe en dim_municipios\" AS mensaje');\n\n")

        f.write("PREPARE stmt FROM @sql_add_col;\n")
        f.write("EXECUTE stmt;\n")
        f.write("DEALLOCATE PREPARE stmt;\n\n")

        # Verificar códigos postales duplicados
        f.write("-- Verificar duplicados en los códigos postales\n")
        cp_set = set()
        duplicados = []
        for id_mun, nombre, codigo_postal, comarca_id in codigos_postales:
            if codigo_postal in cp_set and not codigo_postal.startswith("998"):
                duplicados.append((codigo_postal, nombre))
            cp_set.add(codigo_postal)

        if duplicados:
            f.write("-- ADVERTENCIA: Códigos postales duplicados encontrados:\n")
            for cp, nombre in duplicados:
                f.write(f"-- {cp}: {nombre}\n")
        else:
            f.write("-- No se encontraron duplicados en los códigos postales\n")
        f.write("\n")

        # Paso 2: Actualizar provincia_id para municipios 1-52
        f.write("-- =====================================================================\n")
        f.write("-- PASO 2: Actualizar provincia_id para municipios de Álava (1-52)\n")
        f.write("-- =====================================================================\n")
        f.write("UPDATE dim_municipios SET provincia_id = 1 WHERE id >= 1 AND id <= 52;\n\n")

        # Paso 3: Actualizar códigos postales
        f.write("-- =====================================================================\n")
        f.write("-- PASO 3: Actualizar códigos postales de municipios de Álava\n")
        f.write("-- =====================================================================\n\n")

        for id_mun, nombre, codigo_postal, comarca_id in codigos_postales:
            f.write(f"-- {nombre}\n")
            f.write(f"UPDATE dim_municipios SET codigo_postal = '{codigo_postal}' WHERE id = {id_mun};\n\n")

        # Verificación
        f.write("-- =====================================================================\n")
        f.write("-- Verificación: Mostrar municipios con códigos postales\n")
        f.write("-- =====================================================================\n")
        f.write("SELECT \n")
        f.write("    m.id,\n")
        f.write("    m.municipio_nombre,\n")
        f.write("    m.codigo_postal,\n")
        f.write("    m.provincia_id,\n")
        f.write("    c.nombre AS comarca,\n")
        f.write("    p.nombre AS provincia\n")
        f.write("FROM dim_municipios m\n")
        f.write("LEFT JOIN dim_comarcas c ON m.comarca_id = c.id\n")
        f.write("LEFT JOIN dim_provincias p ON m.provincia_id = p.id\n")
        f.write("WHERE m.id >= 1 AND m.id <= 52\n")
        f.write("ORDER BY m.comarca_id, m.id;\n\n")

        f.write("-- Contar municipios sin código postal\n")
        f.write("SELECT COUNT(*) AS municipios_sin_cp\n")
        f.write("FROM dim_municipios\n")
        f.write("WHERE provincia_id = 1 AND (codigo_postal IS NULL OR codigo_postal = '');\n")

    print(f"Script SQL generado exitosamente: {output_file}")
    print(f"Total de municipios con códigos postales: {len(codigos_postales)}")
    print("\nCódigos postales especiales asignados:")
    print("  99801 - Sierra Brava de Badaia (no encontrado)")
    print("  99802 - Parzoneria de Entzia (no encontrado)")

if __name__ == "__main__":
    main()
