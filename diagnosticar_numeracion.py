#!/usr/bin/env python3
"""
Script de diagnóstico para verificar la numeración de partes
"""
import sys
from pathlib import Path

# Añadir directorio raíz al path
root_dir = Path(__file__).parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from script.db_connection import get_project_connection

# Conectar a la base de datos
schema = 'cert_dev'
user = 'aperez'
password = 'WGueXNk9'

print("=" * 100)
print("DIAGNÓSTICO DE NUMERACIÓN DE PARTES")
print("=" * 100)

with get_project_connection(user, password, schema) as conn:
    cursor = conn.cursor()

    # 1. Contar total de partes por tipo
    print("\n1. TOTAL DE PARTES POR TIPO:")
    print("-" * 100)
    cursor.execute("""
        SELECT
            t.id,
            t.tipo_codigo,
            t.descripcion,
            COUNT(p.id) as total_partes
        FROM dim_tipo_trabajo t
        LEFT JOIN tbl_partes p ON t.id = p.tipo_trabajo_id
        GROUP BY t.id, t.tipo_codigo, t.descripcion
        ORDER BY t.id
    """)

    print(f"{'TIPO_ID':<10} {'PREFIJO':<10} {'DESCRIPCION':<40} {'TOTAL':<10}")
    print("-" * 100)
    for row in cursor.fetchall():
        print(f"{row[0]:<10} {row[1] or 'NULL':<10} {row[2]:<40} {row[3]:<10}")

    # 2. Últimos 20 códigos generados
    print("\n2. ÚLTIMOS 20 CÓDIGOS GENERADOS:")
    print("-" * 100)
    cursor.execute("""
        SELECT
            p.id,
            p.codigo,
            p.tipo_trabajo_id,
            t.tipo_codigo,
            p.creado_en
        FROM tbl_partes p
        LEFT JOIN dim_tipo_trabajo t ON p.tipo_trabajo_id = t.id
        ORDER BY p.id DESC
        LIMIT 20
    """)

    print(f"{'ID':<8} {'CODIGO':<15} {'TIPO_ID':<10} {'PREFIJO':<10} {'FECHA_CREACION':<25}")
    print("-" * 100)
    for row in cursor.fetchall():
        print(f"{row[0]:<8} {row[1] or 'NULL':<15} {row[2] or 'NULL':<10} {row[3] or 'NULL':<10} {str(row[4]):<25}")

    # 3. Número máximo por cada prefijo (la consulta que usa el código)
    print("\n3. NÚMERO MÁXIMO POR PREFIJO (lo que calcula el código):")
    print("-" * 100)

    # Obtener todos los prefijos
    cursor.execute("SELECT id, tipo_codigo FROM dim_tipo_trabajo WHERE tipo_codigo IS NOT NULL")
    tipos = cursor.fetchall()

    print(f"{'PREFIJO':<10} {'MAX_NUM':<10} {'SIGUIENTE':<10} {'QUERY_USADA':<60}")
    print("-" * 100)

    for tipo_id, prefijo in tipos:
        # Esta es la MISMA query que usa el código
        query = """
            SELECT COALESCE(MAX(
                CAST(SUBSTRING_INDEX(codigo, '-', -1) AS UNSIGNED)
            ), 0) + 1
            FROM tbl_partes
            WHERE codigo LIKE %s
        """
        pattern = f"{prefijo}-%"
        cursor.execute(query, (pattern,))
        siguiente_num = cursor.fetchone()[0]
        max_num = siguiente_num - 1 if siguiente_num > 1 else 0

        print(f"{prefijo:<10} {max_num:<10} {siguiente_num:<10} LIKE '{pattern}'")

    # 4. Verificar si hay códigos con formato incorrecto
    print("\n4. CÓDIGOS CON FORMATO POTENCIALMENTE INCORRECTO:")
    print("-" * 100)
    cursor.execute("""
        SELECT codigo, tipo_trabajo_id, id
        FROM tbl_partes
        WHERE codigo IS NOT NULL
          AND codigo NOT REGEXP '^[A-Z]+-[0-9]+$'
        LIMIT 20
    """)

    incorrectos = cursor.fetchall()
    if incorrectos:
        print(f"{'CODIGO':<20} {'TIPO_ID':<10} {'ID':<10}")
        print("-" * 100)
        for row in incorrectos:
            print(f"{row[0]:<20} {row[1] or 'NULL':<10} {row[2]:<10}")
    else:
        print("✓ No se encontraron códigos con formato incorrecto")

    # 5. Analizar distribución de números por prefijo
    print("\n5. DISTRIBUCIÓN DE NÚMEROS POR PREFIJO:")
    print("-" * 100)

    for tipo_id, prefijo in tipos:
        cursor.execute("""
            SELECT
                MIN(CAST(SUBSTRING_INDEX(codigo, '-', -1) AS UNSIGNED)) as min_num,
                MAX(CAST(SUBSTRING_INDEX(codigo, '-', -1) AS UNSIGNED)) as max_num,
                COUNT(*) as total,
                MAX(CAST(SUBSTRING_INDEX(codigo, '-', -1) AS UNSIGNED)) - MIN(CAST(SUBSTRING_INDEX(codigo, '-', -1) AS UNSIGNED)) + 1 as rango_esperado
            FROM tbl_partes
            WHERE codigo LIKE %s
        """, (f"{prefijo}-%",))

        result = cursor.fetchone()
        if result and result[2] > 0:
            min_num, max_num, total, rango_esperado = result
            huecos = rango_esperado - total
            print(f"\nPrefijo: {prefijo}")
            print(f"  Rango: {min_num} - {max_num}")
            print(f"  Total partes: {total}")
            print(f"  Rango esperado: {rango_esperado}")
            print(f"  Huecos/saltos: {huecos}")

            if huecos > 0:
                print(f"  ⚠️  HAY {huecos} NÚMEROS SALTADOS O ELIMINADOS")

    # 6. Buscar huecos específicos en la numeración
    print("\n6. HUECOS EN LA NUMERACIÓN (primeros 10 por prefijo):")
    print("-" * 100)

    for tipo_id, prefijo in tipos:
        # Obtener todos los números usados
        cursor.execute("""
            SELECT CAST(SUBSTRING_INDEX(codigo, '-', -1) AS UNSIGNED) as num
            FROM tbl_partes
            WHERE codigo LIKE %s
            ORDER BY num
        """, (f"{prefijo}-%",))

        numeros = [row[0] for row in cursor.fetchall()]

        if numeros:
            max_num = max(numeros)
            todos_numeros = set(range(1, max_num + 1))
            usados = set(numeros)
            huecos = sorted(todos_numeros - usados)

            if huecos:
                print(f"\n{prefijo}: {len(huecos)} huecos encontrados")
                print(f"  Primeros 10 huecos: {huecos[:10]}")
            else:
                print(f"\n{prefijo}: ✓ Sin huecos (numeración consecutiva perfecta)")

    # 7. Simular la creación del próximo código
    print("\n7. SIMULACIÓN: PRÓXIMO CÓDIGO A GENERAR:")
    print("-" * 100)

    from script.db_partes import _get_tipo_trabajo_prefix

    for tipo_id, prefijo_db in tipos:
        # Obtener prefijo usando la función del código
        prefijo_codigo = _get_tipo_trabajo_prefix(user, password, schema, tipo_id)

        # Obtener siguiente número usando la query del código
        cursor.execute("""
            SELECT COALESCE(MAX(
                CAST(SUBSTRING_INDEX(codigo, '-', -1) AS UNSIGNED)
            ), 0) + 1
            FROM tbl_partes
            WHERE codigo LIKE %s
        """, (f"{prefijo_codigo}-%",))

        siguiente_num = int(cursor.fetchone()[0])
        proximo_codigo = f"{prefijo_codigo}-{siguiente_num:04d}"

        print(f"Tipo ID {tipo_id}: Prefijo='{prefijo_codigo}' → Próximo código: {proximo_codigo}")

        if prefijo_db != prefijo_codigo:
            print(f"  ⚠️  ADVERTENCIA: Prefijo en BD ('{prefijo_db}') ≠ Prefijo en código ('{prefijo_codigo}')")

    cursor.close()

print("\n" + "=" * 100)
print("DIAGNÓSTICO COMPLETO")
print("=" * 100)
