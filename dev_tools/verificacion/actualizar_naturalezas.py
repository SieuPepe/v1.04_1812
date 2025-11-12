#!/usr/bin/env python3
"""
Script para actualizar id_naturaleza en script_cargar_precios_unitarios.sql
según el patrón de código de la partida:
- Códigos 1xxxx → id_naturaleza=2 (Gastos Fijos)
- Códigos 2xxxx → id_naturaleza=3 (Personal)
- Códigos 3xxxx → id_naturaleza=6 (Maquinaria)
- Códigos 4xxxx → id_naturaleza=5 (Material)
"""

import re

def determinar_naturaleza(codigo):
    """
    Determina el id_naturaleza según el código de la partida.

    Args:
        codigo: Código de la partida (ej: '10001', '20001', '30001', '40001')

    Returns:
        int: id_naturaleza correspondiente
    """
    # Limpiar comillas del código
    codigo_limpio = codigo.strip("'\"")

    # Determinar naturaleza según el primer dígito
    if codigo_limpio.startswith('1'):
        return 2  # Gastos Fijos
    elif codigo_limpio.startswith('2'):
        return 3  # Personal
    elif codigo_limpio.startswith('3'):
        return 6  # Maquinaria
    elif codigo_limpio.startswith('4'):
        return 5  # Material
    else:
        return 4  # Por defecto (Capítulo)


def actualizar_script():
    """Lee el script SQL y actualiza los id_naturaleza"""

    archivo_entrada = 'script_cargar_precios_unitarios.sql'
    archivo_salida = 'script_cargar_precios_unitarios_actualizado.sql'

    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Patrón para encontrar las líneas de INSERT VALUES
    # Formato: ('CODIGO', id_naturaleza, id_unidades, 'resumen', 'descripcion', coste, id_capitulo)
    patron = r"\('(\d+)',\s*(\d+),\s*(\d+),\s*'([^']*)',\s*'([^']*)',\s*([0-9.]+),\s*(\d+)\)"

    def reemplazar(match):
        codigo = match.group(1)
        id_naturaleza_viejo = match.group(2)
        id_unidades = match.group(3)
        resumen = match.group(4)
        descripcion = match.group(5)
        coste = match.group(6)
        id_capitulo = match.group(7)

        # Determinar nueva naturaleza
        id_naturaleza_nuevo = determinar_naturaleza(codigo)

        # Reconstruir la línea con el nuevo id_naturaleza
        return f"('{codigo}', {id_naturaleza_nuevo}, {id_unidades}, '{resumen}', '{descripcion}', {coste}, {id_capitulo})"

    # Aplicar el reemplazo
    contenido_actualizado = re.sub(patron, reemplazar, contenido)

    # Guardar el archivo actualizado
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write(contenido_actualizado)

    print(f"✓ Script actualizado generado: {archivo_salida}")

    # Mostrar estadísticas
    stats = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    matches = re.finditer(patron, contenido_actualizado)
    for match in matches:
        codigo = match.group(1)
        naturaleza = determinar_naturaleza(codigo)
        stats[naturaleza] += 1

    print("\nEstadísticas de actualización:")
    print(f"  - Gastos Fijos (id_naturaleza=2): {stats[2]} registros")
    print(f"  - Personal (id_naturaleza=3): {stats[3]} registros")
    print(f"  - Material (id_naturaleza=5): {stats[5]} registros")
    print(f"  - Maquinaria (id_naturaleza=6): {stats[6]} registros")
    print(f"  - TOTAL: {sum(stats.values())} registros actualizados")


if __name__ == '__main__':
    actualizar_script()
