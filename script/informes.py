# script/informes.py
"""
Lógica de generación de informes
Construcción de queries SQL dinámicos, obtención de datos, etc.
"""

from script.db_connection import get_project_connection
from script.informes_config import INFORMES_DEFINICIONES


def get_dimension_values(user, password, schema, tabla_dimension):
    """
    Obtiene todos los valores de una tabla de dimensión.
    Detecta automáticamente si usa 'descripcion' o 'nombre' como columna de texto.

    Args:
        user: Usuario de BD
        password: Contraseña de BD
        schema: Nombre del schema/proyecto
        tabla_dimension: Nombre de la tabla de dimensión (ej: 'dim_red', 'dim_provincias')

    Returns:
        Lista de tuplas (id, texto)
    """
    try:
        with get_project_connection(user, password, schema) as conn:
            cursor = conn.cursor()

            # Detectar qué columna usar: 'descripcion' o 'nombre'
            # Tablas geográficas usan 'nombre', otras usan 'descripcion'
            if tabla_dimension in ['dim_provincias', 'dim_comarcas', 'dim_municipios']:
                campo_texto = 'nombre'
            else:
                campo_texto = 'descripcion'

            # Query para obtener valores
            query = f"""
                SELECT id, {campo_texto}
                FROM {schema}.{tabla_dimension}
                ORDER BY {campo_texto}
            """

            cursor.execute(query)
            result = cursor.fetchall()

            return result if result else []

    except Exception as e:
        print(f"Error al obtener valores de dimensión {tabla_dimension}: {e}")
        return []


def build_filter_condition(filtro, definicion_informe):
    """
    Construye una condición SQL para un filtro específico

    Args:
        filtro: Dict con {campo, operador, valor(es)}
        definicion_informe: Definición del informe desde INFORMES_DEFINICIONES

    Returns:
        String con la condición SQL (ej: "estado = 'Pendiente'")
    """
    campo_key = filtro['campo']
    operador = filtro['operador']
    valor = filtro['valor']

    # Obtener definición del campo
    campo_def = definicion_informe['campos'].get(campo_key)
    if not campo_def:
        return ""

    # Obtener columna de BD
    columna_bd = campo_def.get('columna_bd', campo_key)
    tipo_campo = campo_def.get('tipo', 'texto')

    # Construir condición según operador y tipo
    if operador == "Igual a":
        if tipo_campo in ['texto', 'dimension']:
            return f"{columna_bd} = '{valor}'"
        else:
            return f"{columna_bd} = {valor}"

    elif operador == "Diferente de":
        if tipo_campo in ['texto', 'dimension']:
            return f"{columna_bd} != '{valor}'"
        else:
            return f"{columna_bd} != {valor}"

    elif operador == "Contiene":
        return f"{columna_bd} LIKE '%{valor}%'"

    elif operador == "No contiene":
        return f"{columna_bd} NOT LIKE '%{valor}%'"

    elif operador == "Mayor a":
        return f"{columna_bd} > {valor}"

    elif operador == "Menor a":
        return f"{columna_bd} < {valor}"

    elif operador == "Mayor o igual a":
        return f"{columna_bd} >= {valor}"

    elif operador == "Menor o igual a":
        return f"{columna_bd} <= {valor}"

    elif operador == "Entre":
        valor1, valor2 = valor  # Espera tupla (min, max)
        return f"{columna_bd} BETWEEN {valor1} AND {valor2}"

    elif operador == "Posterior a":
        return f"{columna_bd} > '{valor}'"

    elif operador == "Anterior a":
        return f"{columna_bd} < '{valor}'"

    else:
        return ""


def build_query(informe_nombre, filtros=None, clasificaciones=None, campos_seleccionados=None, schema=""):
    """
    Construye un query SQL dinámico para un informe

    Args:
        informe_nombre: Nombre del informe (ej: "Resumen de Partes")
        filtros: Lista de dicts con filtros aplicados
        clasificaciones: Lista de dicts con clasificaciones aplicadas
        campos_seleccionados: Lista de campos a mostrar
        schema: Nombre del schema/proyecto

    Returns:
        String con el query SQL completo
    """
    # Obtener definición del informe
    definicion = INFORMES_DEFINICIONES.get(informe_nombre)
    if not definicion:
        raise ValueError(f"Informe '{informe_nombre}' no definido")

    tabla_principal = definicion['tabla_principal']
    campos_def = definicion['campos']

    # Si no se especifican campos, usar los por defecto
    if not campos_seleccionados:
        campos_seleccionados = definicion.get('campos_default', list(campos_def.keys()))

    # ========== CONSTRUIR SELECT ==========
    select_parts = []
    for campo_key in campos_seleccionados:
        campo = campos_def.get(campo_key)
        if not campo:
            continue

        if campo['tipo'] == 'calculado':
            # Campo calculado (ej: Pendiente = Presupuesto - Certificado)
            select_parts.append(f"({campo['formula']}) AS {campo_key}")
        elif campo['tipo'] == 'dimension':
            # Campo de dimensión (hacer JOIN)
            tabla_dim = campo['tabla_dimension']
            campo_nombre = campo.get('campo_nombre', 'descripcion')
            alias_dim = f"{campo_key}_dim"
            select_parts.append(f"{alias_dim}.{campo_nombre} AS {campo_key}")
        else:
            # Campo directo
            select_parts.append(f"p.{campo['columna_bd']} AS {campo_key}")

    select_clause = "SELECT " + ", ".join(select_parts)

    # ========== CONSTRUIR FROM + JOINS ==========
    from_clause = f"FROM {schema}.{tabla_principal} p"

    # Añadir JOINs para dimensiones
    for campo_key in campos_seleccionados:
        campo = campos_def.get(campo_key)
        if campo and campo['tipo'] == 'dimension':
            tabla_dim = campo['tabla_dimension']
            columna_bd = campo['columna_bd']
            alias_dim = f"{campo_key}_dim"
            from_clause += f"\nLEFT JOIN {schema}.{tabla_dim} {alias_dim} ON p.{columna_bd} = {alias_dim}.id"

    # ========== CONSTRUIR WHERE ==========
    where_conditions = []

    if filtros:
        for filtro in filtros:
            condicion = build_filter_condition(filtro, definicion)
            if condicion:
                where_conditions.append(condicion)

    where_clause = ""
    if where_conditions:
        # TODO: Implementar lógica AND/OR según configuración
        where_clause = "WHERE " + " AND ".join(where_conditions)

    # ========== CONSTRUIR ORDER BY ==========
    order_by_clause = ""

    if clasificaciones:
        order_parts = []
        for clasif in clasificaciones:
            campo_key = clasif['campo']
            orden = clasif.get('orden', 'Ascendente')

            campo = campos_def.get(campo_key)
            if campo:
                if campo['tipo'] == 'dimension':
                    alias_dim = f"{campo_key}_dim"
                    campo_nombre = campo.get('campo_nombre', 'descripcion')
                    order_parts.append(f"{alias_dim}.{campo_nombre} {'ASC' if orden == 'Ascendente' else 'DESC'}")
                else:
                    columna = campo.get('columna_bd', campo_key)
                    order_parts.append(f"p.{columna} {'ASC' if orden == 'Ascendente' else 'DESC'}")

        if order_parts:
            order_by_clause = "ORDER BY " + ", ".join(order_parts)

    # ========== QUERY FINAL ==========
    query = f"{select_clause}\n{from_clause}"
    if where_clause:
        query += f"\n{where_clause}"
    if order_by_clause:
        query += f"\n{order_by_clause}"

    return query


def ejecutar_informe(user, password, schema, informe_nombre, filtros=None, clasificaciones=None, campos_seleccionados=None):
    """
    Ejecuta un informe y devuelve los datos

    Args:
        user: Usuario de BD
        password: Contraseña de BD
        schema: Nombre del schema/proyecto
        informe_nombre: Nombre del informe
        filtros: Lista de filtros
        clasificaciones: Lista de clasificaciones
        campos_seleccionados: Lista de campos a mostrar

    Returns:
        Tuple (columnas, datos)
        - columnas: Lista de nombres de columnas
        - datos: Lista de tuplas con los datos
    """
    try:
        # Construir query
        query = build_query(informe_nombre, filtros, clasificaciones, campos_seleccionados, schema)

        print(f"\n{'='*60}")
        print(f"QUERY GENERADO PARA INFORME: {informe_nombre}")
        print(f"{'='*60}")
        print(query)
        print(f"{'='*60}\n")

        # Ejecutar query
        with get_project_connection(user, password, schema) as conn:
            cursor = conn.cursor()
            cursor.execute(query)

            # Obtener nombres de columnas
            columnas = [desc[0] for desc in cursor.description]

            # Obtener datos
            datos = cursor.fetchall()

            return columnas, datos

    except Exception as e:
        print(f"Error al ejecutar informe: {e}")
        import traceback
        traceback.print_exc()
        return [], []
