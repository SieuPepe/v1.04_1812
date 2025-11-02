# script/informes.py
"""
Lógica de generación de informes
Construcción de queries SQL dinámicos, obtención de datos, etc.
"""

from script.db_connection import get_project_connection
from script.informes_config import INFORMES_DEFINICIONES


def _detectar_columna_texto(user, password, schema, tabla_dimension):
    """
    Detecta automáticamente qué columna de texto usar para mostrar valores de una dimensión.

    Estrategia:
    1. Buscar por nombres comunes según el tipo de tabla
    2. Si no encuentra, usar la primera columna VARCHAR/TEXT que no sea 'id'

    Returns:
        str: Nombre de la columna o None si no encuentra
    """
    try:
        with get_project_connection(user, password, schema) as conn:
            cursor = conn.cursor()

            # Obtener todas las columnas de la tabla
            cursor.execute(f"""
                SELECT COLUMN_NAME, DATA_TYPE
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                ORDER BY ORDINAL_POSITION
            """, (schema, tabla_dimension))

            columnas = cursor.fetchall()
            cursor.close()

            if not columnas:
                return None

            # Mapeo de nombres comunes por tipo de tabla
            nombres_comunes = {
                'dim_provincias': ['nombre', 'provincia', 'descripcion'],
                'dim_comarcas': ['comarca_nombre', 'nombre', 'comarca', 'descripcion'],
                'dim_municipios': ['municipio_nombre', 'nombre', 'municipio', 'descripcion'],
                'dim_red': ['descripcion', 'red_codigo', 'nombre'],
                'dim_tipo_trabajo': ['descripcion', 'tipo_codigo', 'nombre'],
                'dim_codigo_trabajo': ['descripcion', 'cod_trabajo', 'codigo', 'nombre']
            }

            # Obtener lista de nombres a buscar
            nombres_a_buscar = nombres_comunes.get(tabla_dimension, ['descripcion', 'nombre'])

            # 1. Buscar por nombres comunes
            columnas_lower = {col[0].lower(): col[0] for col in columnas}
            for nombre in nombres_a_buscar:
                if nombre.lower() in columnas_lower:
                    return columnas_lower[nombre.lower()]

            # 2. Buscar la primera columna VARCHAR/TEXT que no sea 'id'
            for col_name, col_type in columnas:
                if col_name.lower() != 'id' and col_type.lower() in ('varchar', 'text', 'char', 'tinytext', 'mediumtext', 'longtext'):
                    return col_name

            # 3. Última opción: primera columna que no sea 'id'
            for col_name, col_type in columnas:
                if col_name.lower() != 'id':
                    return col_name

            return None

    except Exception as e:
        print(f"Error al detectar columna de texto para {tabla_dimension}: {e}")
        return None


def get_dimension_values(user, password, schema, tabla_dimension):
    """
    Obtiene todos los valores de una tabla de dimensión.
    Detecta automáticamente la columna de texto correcta.

    Args:
        user: Usuario de BD
        password: Contraseña de BD
        schema: Nombre del schema/proyecto
        tabla_dimension: Nombre de la tabla de dimensión (ej: 'dim_red', 'dim_provincias')

    Returns:
        Lista de tuplas (id, texto)
    """
    try:
        # Detectar la columna de texto correcta
        campo_texto = _detectar_columna_texto(user, password, schema, tabla_dimension)

        if not campo_texto:
            print(f"No se pudo detectar columna de texto para {tabla_dimension}")
            return []

        with get_project_connection(user, password, schema) as conn:
            cursor = conn.cursor()

            # Query para obtener valores
            query = f"""
                SELECT id, {campo_texto}
                FROM {schema}.{tabla_dimension}
                ORDER BY {campo_texto}
            """

            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()

            return result if result else []

    except Exception as e:
        print(f"Error al obtener valores de dimensión {tabla_dimension}: {e}")
        return []


def build_filter_condition(filtro, definicion_informe, schema="", user="", password=""):
    """
    Construye una condición SQL para un filtro específico

    Args:
        filtro: Dict con {campo, operador, valor(es)}
        definicion_informe: Definición del informe desde INFORMES_DEFINICIONES
        schema: Nombre del schema/proyecto
        user: Usuario de BD (para detectar columnas de dimensiones)
        password: Contraseña de BD (para detectar columnas de dimensiones)

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

    # Obtener columna de BD o fórmula para campos calculados
    tipo_campo = campo_def.get('tipo', 'texto')
    if tipo_campo == 'calculado':
        # Reemplazar nombres de tablas en la fórmula con schema.tabla
        formula = campo_def['formula']
        tablas_a_reemplazar = [
            'tbl_part_presupuesto',
            'tbl_part_certificacion',
            'tbl_partes',
            'dim_ot',
            'dim_red',
            'dim_tipo_trabajo',
            'dim_codigo_trabajo',
            'dim_provincias',
            'dim_comarcas',
            'dim_municipios'
        ]
        for tabla in tablas_a_reemplazar:
            formula = formula.replace(f"FROM {tabla}", f"FROM {schema}.{tabla}")
        columna_bd = f"({formula})"
    elif tipo_campo == 'dimension':
        # Para dimensiones, detectar automáticamente la columna si tenemos credenciales
        alias_dim = f"{campo_key}_dim"
        tabla_dim = campo_def.get('tabla_dimension')

        # Detectar columna automáticamente
        if user and password and tabla_dim:
            campo_nombre = _detectar_columna_texto(user, password, schema, tabla_dim)
            if not campo_nombre:
                campo_nombre = campo_def.get('campo_nombre', 'descripcion')
        else:
            campo_nombre = campo_def.get('campo_nombre', 'descripcion')

        columna_bd = f"{alias_dim}.{campo_nombre}"
    else:
        columna_bd = f"p.{campo_def.get('columna_bd', campo_key)}"

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


def build_query(informe_nombre, filtros=None, clasificaciones=None, campos_seleccionados=None, schema="", user="", password=""):
    """
    Construye un query SQL dinámico para un informe

    Args:
        informe_nombre: Nombre del informe (ej: "Resumen de Partes")
        filtros: Lista de dicts con filtros aplicados
        clasificaciones: Lista de dicts con clasificaciones aplicadas
        campos_seleccionados: Lista de campos a mostrar
        schema: Nombre del schema/proyecto
        user: Usuario de BD (necesario para detectar columnas de dimensiones)
        password: Contraseña de BD (necesario para detectar columnas de dimensiones)

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

    # Cachear la detección de columnas de dimensiones
    dimension_columns_cache = {}

    # ========== CONSTRUIR SELECT ==========
    select_parts = []
    tabla_alias = "p"  # Alias de la tabla principal

    for campo_key in campos_seleccionados:
        campo = campos_def.get(campo_key)
        if not campo:
            continue

        if campo['tipo'] == 'calculado':
            # Campo calculado (ej: Pendiente = Presupuesto - Certificado)
            # Reemplazar nombres de tablas en la fórmula con schema.tabla
            formula = campo['formula']
            # Reemplazar referencias a tablas comunes con schema.tabla
            tablas_a_reemplazar = [
                'tbl_part_presupuesto',
                'tbl_part_certificacion',
                'tbl_partes',
                'dim_ot',
                'dim_red',
                'dim_tipo_trabajo',
                'dim_codigo_trabajo',
                'dim_provincias',
                'dim_comarcas',
                'dim_municipios'
            ]
            for tabla in tablas_a_reemplazar:
                # Reemplazar "FROM tabla" con "FROM schema.tabla"
                formula = formula.replace(f"FROM {tabla}", f"FROM {schema}.{tabla}")
            select_parts.append(f"({formula}) AS {campo_key}")
        elif campo['tipo'] == 'dimension':
            # Campo de dimensión (hacer JOIN)
            tabla_dim = campo['tabla_dimension']
            alias_dim = f"{campo_key}_dim"

            # Detectar automáticamente la columna correcta si tenemos credenciales
            if user and password and tabla_dim not in dimension_columns_cache:
                dimension_columns_cache[tabla_dim] = _detectar_columna_texto(user, password, schema, tabla_dim)

            # Usar la columna detectada o la especificada en config
            if tabla_dim in dimension_columns_cache and dimension_columns_cache[tabla_dim]:
                campo_nombre = dimension_columns_cache[tabla_dim]
            else:
                campo_nombre = campo.get('campo_nombre', 'descripcion')

            select_parts.append(f"{alias_dim}.{campo_nombre} AS {campo_key}")
        else:
            # Campo directo - usar alias de tabla
            select_parts.append(f"{tabla_alias}.{campo['columna_bd']} AS {campo_key}")

    select_clause = "SELECT " + ", ".join(select_parts)

    # ========== RECOPILAR DIMENSIONES NECESARIAS ==========
    # Necesitamos JOINs para dimensiones usadas en SELECT y también en filtros
    dimensiones_necesarias = set()

    # 1. Dimensiones de campos seleccionados
    for campo_key in campos_seleccionados:
        campo = campos_def.get(campo_key)
        if campo and campo['tipo'] == 'dimension':
            dimensiones_necesarias.add(campo_key)

    # 2. Dimensiones usadas en filtros
    if filtros:
        for filtro in filtros:
            campo_key = filtro.get('campo')
            campo = campos_def.get(campo_key)
            if campo and campo['tipo'] == 'dimension':
                dimensiones_necesarias.add(campo_key)

    # 3. Dimensiones usadas en clasificaciones
    if clasificaciones:
        for clasif in clasificaciones:
            campo_key = clasif.get('campo')
            campo = campos_def.get(campo_key)
            if campo and campo['tipo'] == 'dimension':
                dimensiones_necesarias.add(campo_key)

    # ========== CONSTRUIR FROM + JOINS ==========
    from_clause = f"FROM {schema}.{tabla_principal} p"

    # Añadir JOINs para TODAS las dimensiones necesarias
    for campo_key in dimensiones_necesarias:
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
            condicion = build_filter_condition(filtro, definicion, schema, user, password)
            if condicion:
                where_conditions.append((condicion, filtro))

    where_clause = ""
    if where_conditions:
        # Construir WHERE con lógica AND/OR personalizada
        where_parts = []
        for i, (condicion, filtro) in enumerate(where_conditions):
            if i == 0:
                # Primera condición, no lleva operador lógico antes
                where_parts.append(condicion)
            else:
                # Condiciones siguientes, usar la lógica del filtro
                logica = filtro.get('logica', 'Y')  # Por defecto 'Y' (AND)
                operador_sql = 'AND' if logica == 'Y' else 'OR'
                where_parts.append(f"{operador_sql} {condicion}")

        where_clause = "WHERE " + " ".join(where_parts)

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
                    tabla_dim = campo.get('tabla_dimension')

                    # Detectar columna automáticamente
                    if user and password and tabla_dim and tabla_dim in dimension_columns_cache:
                        campo_nombre = dimension_columns_cache[tabla_dim]
                    elif user and password and tabla_dim:
                        campo_nombre = _detectar_columna_texto(user, password, schema, tabla_dim)
                        if campo_nombre:
                            dimension_columns_cache[tabla_dim] = campo_nombre
                        else:
                            campo_nombre = campo.get('campo_nombre', 'descripcion')
                    else:
                        campo_nombre = campo.get('campo_nombre', 'descripcion')

                    order_parts.append(f"{alias_dim}.{campo_nombre} {'ASC' if orden == 'Ascendente' else 'DESC'}")
                elif campo['tipo'] == 'calculado':
                    # Para campos calculados, usar el alias del campo en el SELECT
                    order_parts.append(f"{campo_key} {'ASC' if orden == 'Ascendente' else 'DESC'}")
                else:
                    columna = campo.get('columna_bd', campo_key)
                    order_parts.append(f"{tabla_alias}.{columna} {'ASC' if orden == 'Ascendente' else 'DESC'}")

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
        # Construir query (pasando user y password para detectar columnas de dimensiones)
        query = build_query(informe_nombre, filtros, clasificaciones, campos_seleccionados, schema, user, password)

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
