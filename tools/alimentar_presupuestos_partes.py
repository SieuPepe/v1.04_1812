#!/usr/bin/env python3
"""
Script para alimentar partes existentes con partidas del presupuesto
HydroFlow Manager v1.04
"""

import os
import sys
from pathlib import Path
import random

# Añadir directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from script.db_connection import get_project_connection

# Configuración
USER = os.getenv('DB_USER', 'root')
PASSWORD = os.getenv('DB_PASSWORD', 'Lauburu1969')
SCHEMA = os.getenv('DB_SCHEMA', 'cert_dev')


def obtener_partes_sin_presupuesto(conn):
    """Obtiene partes que no tienen presupuesto asignado"""
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT p.id, p.codigo, p.descripcion
        FROM {SCHEMA}.tbl_partes p
        LEFT JOIN {SCHEMA}.tbl_part_presupuesto pp ON p.id = pp.parte_id
        WHERE pp.id IS NULL
        ORDER BY p.id
        LIMIT 20
    """)
    partes = cursor.fetchall()
    cursor.close()
    return partes


def obtener_partidas_aleatorias(conn, n=5):
    """Obtiene n partidas aleatorias del catálogo de precios"""
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT id, codigo, resumen, coste
        FROM {SCHEMA}.tbl_pres_precios
        WHERE coste IS NOT NULL AND coste > 0
        ORDER BY RAND()
        LIMIT {n}
    """)
    partidas = cursor.fetchall()
    cursor.close()
    return partidas


def asignar_presupuesto_a_parte(conn, parte_id, partidas):
    """Asigna partidas de presupuesto a un parte"""
    cursor = conn.cursor()

    total_presupuesto = 0
    partidas_insertadas = 0

    for partida in partidas:
        precio_id, codigo, resumen, coste = partida

        # Cantidad aleatoria entre 1 y 50
        cantidad = round(random.uniform(1.0, 50.0), 2)
        precio_unit = float(coste)

        cursor.execute(f"""
            INSERT INTO {SCHEMA}.tbl_part_presupuesto
            (parte_id, precio_id, cantidad, precio_unit)
            VALUES (%s, %s, %s, %s)
        """, (parte_id, precio_id, cantidad, precio_unit))

        total_presupuesto += cantidad * precio_unit
        partidas_insertadas += 1

    conn.commit()
    cursor.close()

    return partidas_insertadas, total_presupuesto


def main():
    print("="*70)
    print("ALIMENTAR PARTES CON PARTIDAS DEL PRESUPUESTO")
    print("="*70)
    print()

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            # 1. Obtener partes sin presupuesto
            print("📋 Buscando partes sin presupuesto...")
            partes = obtener_partes_sin_presupuesto(conn)

            if not partes:
                print("✅ Todos los partes ya tienen presupuesto asignado.")
                return

            print(f"   Encontrados {len(partes)} partes sin presupuesto")
            print()

            # 2. Procesar cada parte
            total_procesados = 0
            total_partidas = 0
            total_importe = 0

            for parte_id, codigo, descripcion in partes:
                print(f"📦 Procesando parte {codigo}...")
                print(f"   {descripcion[:60]}...")

                # Obtener entre 3 y 8 partidas aleatorias
                num_partidas = random.randint(3, 8)
                partidas = obtener_partidas_aleatorias(conn, num_partidas)

                # Asignar presupuesto
                n_partidas, importe = asignar_presupuesto_a_parte(conn, parte_id, partidas)

                print(f"   ✅ Asignadas {n_partidas} partidas (Total: {importe:,.2f} €)")
                print()

                total_procesados += 1
                total_partidas += n_partidas
                total_importe += importe

            # 3. Resumen
            print("="*70)
            print("✅ PROCESO COMPLETADO")
            print("="*70)
            print(f"Partes procesados:    {total_procesados}")
            print(f"Partidas asignadas:   {total_partidas}")
            print(f"Importe total:        {total_importe:,.2f} €")
            print(f"Promedio por parte:   {total_importe/total_procesados:,.2f} €")
            print()

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
