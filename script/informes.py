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

    # DEBUG: Imprimir información del filtro
    print(f"\n[DEBUG FILTRO]")
    print(f"  Campo: {campo_key}")
    print(f"  Tipo campo: {tipo_campo}")
    print(f"  Operador: {operador}")
    print(f"  Valor: {valor}")
    print(f"  Columna BD: {columna_bd}")

    # Construir condición según operador y tipo
    if operador == "Igual a":
        if tipo_campo in ['texto', 'dimension', 'fecha', 'calculado']:
            condicion = f"{columna_bd} = '{valor}'"
            print(f"  Condición generada (CON comillas): {condicion}\n")
            return condicion
        else:
            condicion = f"{columna_bd} = {valor}"
            print(f"  Condición generada (SIN comillas): {condicion}\n")
            return condicion

    elif operador == "Diferente de":
        if tipo_campo in ['texto', 'dimension', 'fecha', 'calculado']:
            return f"{columna_bd} != '{valor}'"
        else:
            return f"{columna_bd} != {valor}"

    elif operador == "Contiene":
        return f"{columna_bd} LIKE '%{valor}%'"

    elif operador == "No contiene":
        return f"{columna_bd} NOT LIKE '%{valor}%'"

    elif operador == "Mayor a":
        if tipo_campo in ['fecha', 'calculado']:
            return f"{columna_bd} > '{valor}'"
        else:
            return f"{columna_bd} > {valor}"

    elif operador == "Menor a":
        if tipo_campo in ['fecha', 'calculado']:
            return f"{columna_bd} < '{valor}'"
        else:
            return f"{columna_bd} < {valor}"

    elif operador == "Mayor o igual a":
        if tipo_campo in ['fecha', 'calculado']:
            return f"{columna_bd} >= '{valor}'"
        else:
            return f"{columna_bd} >= {valor}"

    elif operador == "Menor o igual a":
        if tipo_campo in ['fecha', 'calculado']:
            return f"{columna_bd} <= '{valor}'"
        else:
            return f"{columna_bd} <= {valor}"

    elif operador == "Entre":
        valor1, valor2 = valor  # Espera tupla (min, max)
        # Para fechas, textos y calculados, necesitamos comillas
        if tipo_campo in ['fecha', 'texto', 'dimension', 'calculado']:
            return f"{columna_bd} BETWEEN '{valor1}' AND '{valor2}'"
        else:
            # Para numéricos, sin comillas
            return f"{columna_bd} BETWEEN {valor1} AND {valor2}"

    elif operador == "Posterior a":
        return f"{columna_bd} > '{valor}'"

    elif operador == "Anterior a":
        return f"{columna_bd} < '{valor}'"

    else:
        return ""


def build_query(informe_nombre, filtros=None, ordenaciones=None, campos_seleccionados=None, schema="", user="", password=""):
    """
    Construye un query SQL dinámico para un informe

    Args:
        informe_nombre: Nombre del informe (ej: "Resumen de Partes")
        filtros: Lista de dicts con filtros aplicados
        ordenaciones: Lista de dicts con ordenaciones aplicadas
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

    # 3. Dimensiones usadas en ordenaciones
    if ordenaciones:
        for clasif in ordenaciones:
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

    if ordenaciones:
        order_parts = []
        for clasif in ordenaciones:
            campo_key = clasif['campo']
            orden = clasif.get('orden', 'Ascendente')

            # VALIDACIÓN: Solo permitir ordenar por campos que están en el SELECT
            if campo_key not in campos_seleccionados:
                print(f"⚠ Advertencia: Campo '{campo_key}' en ORDER BY no está en SELECT, se omite")
                continue

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


def build_query_with_sql_aggregation(informe_nombre, filtros=None, ordenaciones=None, campos_seleccionados=None,
                                      agrupaciones=None, schema="", user="", password=""):
    """
    Construye un query SQL dinámico con GROUP BY y agregaciones en SQL
    Específico para informes de tipo Recursos que requieren SUM de cantidades

    Args:
        informe_nombre: Nombre del informe
        filtros: Lista de filtros
        ordenaciones: Lista de ordenaciones
        campos_seleccionados: Lista de campos a mostrar
        agrupaciones: Lista de campos por los que agrupar
        schema: Schema de la BD
        user: Usuario de BD
        password: Contraseña de BD

    Returns:
        String con el query SQL con GROUP BY
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

    # Añadir automáticamente campos de agrupación a los seleccionados
    if agrupaciones:
        for agrup in agrupaciones:
            if agrup not in campos_seleccionados:
                campos_seleccionados.append(agrup)

    # Cachear detección de columnas de dimensiones
    dimension_columns_cache = {}

    # ========== DETECTAR TABLAS RELACIONADAS NECESARIAS ==========
    tablas_necesarias = set()
    tablas_necesarias.add('principal')  # La tabla principal siempre

    for campo_key in campos_seleccionados:
        campo = campos_def.get(campo_key)
        if campo and campo.get('tabla_relacion'):
            tablas_necesarias.add(campo['tabla_relacion'])

    # También revisar filtros y ordenaciones
    if filtros:
        for filtro in filtros:
            campo_key = filtro.get('campo')
            campo = campos_def.get(campo_key)
            if campo and campo.get('tabla_relacion'):
                tablas_necesarias.add(campo['tabla_relacion'])

    if ordenaciones:
        for clasif in ordenaciones:
            campo_key = clasif.get('campo')
            campo = campos_def.get(campo_key)
            if campo and campo.get('tabla_relacion'):
                tablas_necesarias.add(campo['tabla_relacion'])

    # ========== DETERMINAR SI NECESITAMOS AGREGACIONES ==========
    # Si hay agrupaciones O si hay campos de múltiples tablas relacionadas, necesitamos GROUP BY
    usar_group_by = bool(agrupaciones) or len(tablas_necesarias) > 1

    # ========== CONSTRUIR SELECT ==========
    select_parts = []
    group_by_parts = []  # Para el GROUP BY

    # Mapeo de alias de tablas
    tabla_aliases = {
        'principal': 'p',
        'precio': 'precio',
        'parte': 'parte'
    }

    for campo_key in campos_seleccionados:
        campo = campos_def.get(campo_key)
        if not campo:
            continue

        tabla_rel = campo.get('tabla_relacion', 'principal')
        alias_tabla = tabla_aliases.get(tabla_rel, 'p')

        # Usar el nombre bonito del campo para el alias SQL
        # Esto hace que las columnas en el resultado tengan los nombres correctos
        nombre_alias = campo.get('nombre', campo_key)

        if campo['tipo'] == 'calculado':
            # Campo calculado
            formula = campo['formula']

            # Reemplazar alias 'p' en la fórmula con el alias correcto
            formula_procesada = formula

            # Reemplazar referencias a tablas en subconsultas
            tablas_a_reemplazar = [
                'tbl_part_presupuesto', 'tbl_part_certificacion', 'tbl_partes',
                'tbl_pres_precios', 'dim_red', 'dim_tipo_trabajo', 'dim_cod',
                'dim_comarcas', 'dim_municipios', 'tbl_pres_naturaleza', 'tbl_pres_capitulos'
            ]
            for tabla in tablas_a_reemplazar:
                formula_procesada = formula_procesada.replace(f"FROM {tabla}", f"FROM {schema}.{tabla}")

            # Si usamos GROUP BY y el campo es numérico/moneda, aplicar SUM
            if usar_group_by and campo.get('formato') in ['moneda', 'decimal', 'numerico']:
                select_parts.append(f"SUM({formula_procesada}) AS `{nombre_alias}`")
            else:
                select_parts.append(f"({formula_procesada}) AS `{nombre_alias}`")

        elif campo['tipo'] == 'dimension':
            # Campo de dimensión
            tabla_dim = campo['tabla_dimension']
            columna_bd = campo['columna_bd']
            alias_dim = f"{campo_key}_dim"

            # Detectar columna automáticamente
            if user and password and tabla_dim not in dimension_columns_cache:
                dimension_columns_cache[tabla_dim] = _detectar_columna_texto(user, password, schema, tabla_dim)

            if tabla_dim in dimension_columns_cache and dimension_columns_cache[tabla_dim]:
                campo_nombre = dimension_columns_cache[tabla_dim]
            else:
                campo_nombre = campo.get('campo_nombre', 'descripcion')

            select_parts.append(f"{alias_dim}.{campo_nombre} AS `{nombre_alias}`")

            # Añadir al GROUP BY si es necesario
            if usar_group_by:
                group_by_parts.append(f"{alias_dim}.{campo_nombre}")

        elif campo['tipo'] == 'numerico':
            # Campo numérico directo
            columna = campo['columna_bd']

            # Si usamos GROUP BY, solo aplicar SUM si es de la tabla principal
            # Los campos numéricos de tablas relacionadas (ej: precio.coste) NO se suman
            if usar_group_by:
                if tabla_rel == 'principal':
                    # Campos de tabla principal (ej: cantidad) → SUM
                    select_parts.append(f"SUM({alias_tabla}.{columna}) AS `{nombre_alias}`")
                else:
                    # Campos de tablas relacionadas (ej: precio.coste) → NO SUM, incluir en GROUP BY
                    select_parts.append(f"{alias_tabla}.{columna} AS `{nombre_alias}`")
                    if f"{alias_tabla}.{columna}" not in group_by_parts:
                        group_by_parts.append(f"{alias_tabla}.{columna}")
            else:
                select_parts.append(f"{alias_tabla}.{columna} AS `{nombre_alias}`")

        else:
            # Campo directo (texto, etc.)
            columna = campo['columna_bd']
            select_parts.append(f"{alias_tabla}.{columna} AS `{nombre_alias}`")

            # Añadir al GROUP BY si no es numérico
            if usar_group_by and campo.get('formato') not in ['moneda', 'decimal', 'numerico']:
                group_by_parts.append(f"{alias_tabla}.{columna}")

    select_clause = "SELECT " + ", ".join(select_parts)

    # ========== CONSTRUIR FROM + JOINS ==========
    from_clause = f"FROM {schema}.{tabla_principal} p"

    # JOINs con tablas relacionadas
    if 'precio' in tablas_necesarias and tabla_principal != 'tbl_pres_precios':
        from_clause += f"\nLEFT JOIN {schema}.tbl_pres_precios precio ON p.precio_id = precio.id"

    if 'parte' in tablas_necesarias and tabla_principal != 'tbl_partes':
        from_clause += f"\nLEFT JOIN {schema}.tbl_partes parte ON p.parte_id = parte.id"

    # ========== RECOPILAR DIMENSIONES NECESARIAS ==========
    dimensiones_necesarias = set()

    for campo_key in campos_seleccionados:
        campo = campos_def.get(campo_key)
        if campo and campo['tipo'] == 'dimension':
            dimensiones_necesarias.add(campo_key)

    if filtros:
        for filtro in filtros:
            campo_key = filtro.get('campo')
            campo = campos_def.get(campo_key)
            if campo and campo['tipo'] == 'dimension':
                dimensiones_necesarias.add(campo_key)

    if ordenaciones:
        for clasif in ordenaciones:
            campo_key = clasif.get('campo')
            campo = campos_def.get(campo_key)
            if campo and campo['tipo'] == 'dimension':
                dimensiones_necesarias.add(campo_key)

    # Agregar agrupaciones a dimensiones necesarias (para que se hagan los JOINs)
    if agrupaciones:
        for campo_key in agrupaciones:
            campo = campos_def.get(campo_key)
            if campo and campo['tipo'] == 'dimension':
                dimensiones_necesarias.add(campo_key)

    # JOINs con dimensiones
    for campo_key in dimensiones_necesarias:
        campo = campos_def.get(campo_key)
        if campo and campo['tipo'] == 'dimension':
            tabla_dim = campo['tabla_dimension']
            columna_bd = campo['columna_bd']
            alias_dim = f"{campo_key}_dim"

            tabla_rel = campo.get('tabla_relacion', 'principal')
            alias_tabla = tabla_aliases.get(tabla_rel, 'p')

            from_clause += f"\nLEFT JOIN {schema}.{tabla_dim} {alias_dim} ON {alias_tabla}.{columna_bd} = {alias_dim}.id"

    # ========== CONSTRUIR WHERE ==========
    where_conditions = []

    # Filtros de usuario
    if filtros:
        for filtro in filtros:
            condicion = build_filter_condition(filtro, definicion, schema, user, password)
            if condicion:
                where_conditions.append((condicion, filtro))

    # Filtros automáticos de la definición
    if definicion.get('filtro_cantidad_cero'):
        # Usar campo correcto según la tabla principal
        if tabla_principal == 'tbl_part_certificacion':
            where_conditions.append(("p.cantidad_cert > 0", {'logica': 'Y'}))
        else:
            where_conditions.append(("p.cantidad > 0", {'logica': 'Y'}))

    if definicion.get('filtro_certificada'):
        where_conditions.append(("p.certificada = 1", {'logica': 'Y'}))

    where_clause = ""
    if where_conditions:
        where_parts = []
        for i, (condicion, filtro) in enumerate(where_conditions):
            if i == 0:
                where_parts.append(condicion)
            else:
                logica = filtro.get('logica', 'Y')
                operador_sql = 'AND' if logica == 'Y' else 'OR'
                where_parts.append(f"{operador_sql} {condicion}")

        where_clause = "WHERE " + " ".join(where_parts)

    # ========== CONSTRUIR GROUP BY ==========
    # Agregar agrupaciones explícitas al GROUP BY aunque no estén en SELECT
    if agrupaciones and usar_group_by:
        for campo_key in agrupaciones:
            if campo_key not in campos_seleccionados:  # Solo si no está ya en SELECT
                campo = campos_def.get(campo_key)
                if campo:
                    if campo['tipo'] == 'dimension':
                        # Campo de dimensión
                        alias_dim = f"{campo_key}_dim"
                        if alias_dim in [part.split('.')[0] for part in group_by_parts if '.' in part]:
                            continue  # Ya está en group_by_parts

                        tabla_dim = campo.get('tabla_dimension')
                        if tabla_dim in dimension_columns_cache and dimension_columns_cache[tabla_dim]:
                            campo_nombre = dimension_columns_cache[tabla_dim]
                        else:
                            campo_nombre = campo.get('campo_nombre', 'descripcion')

                        group_by_parts.append(f"{alias_dim}.{campo_nombre}")
                    else:
                        # Campo normal (texto, etc.)
                        tabla_rel = campo.get('tabla_relacion', 'principal')
                        alias_tabla = tabla_aliases.get(tabla_rel, 'p')
                        columna = campo.get('columna_bd', campo_key)

                        campo_completo = f"{alias_tabla}.{columna}"
                        if campo_completo not in group_by_parts:
                            group_by_parts.append(campo_completo)

    group_by_clause = ""
    if usar_group_by and group_by_parts:
        group_by_clause = "GROUP BY " + ", ".join(group_by_parts)

    # ========== CONSTRUIR ORDER BY ==========
    order_by_clause = ""
    order_parts = []

    # Si hay agrupaciones, SIEMPRE ordenar primero por los campos de agrupación
    if agrupaciones:
        for agrup_key in agrupaciones:
            campo = campos_def.get(agrup_key)
            if campo:
                if campo['tipo'] == 'dimension':
                    alias_dim = f"{agrup_key}_dim"
                    tabla_dim = campo.get('tabla_dimension')

                    if tabla_dim in dimension_columns_cache and dimension_columns_cache[tabla_dim]:
                        campo_nombre = dimension_columns_cache[tabla_dim]
                    else:
                        campo_nombre = campo.get('campo_nombre', 'descripcion')

                    order_parts.append(f"{alias_dim}.{campo_nombre} ASC")
                elif campo['tipo'] == 'calculado' or campo['tipo'] == 'numerico':
                    # Usar el nombre bonito del campo (alias en SELECT)
                    nombre_alias = campo.get('nombre', agrup_key)
                    order_parts.append(f"`{nombre_alias}` ASC")
                else:
                    tabla_rel = campo.get('tabla_relacion', 'principal')
                    alias_tabla = tabla_aliases.get(tabla_rel, 'p')
                    columna = campo.get('columna_bd', agrup_key)
                    order_parts.append(f"{alias_tabla}.{columna} ASC")

    # Agregar ordenaciones adicionales especificadas por el usuario
    if ordenaciones:
        for clasif in ordenaciones:
            campo_key = clasif['campo']
            orden = clasif.get('orden', 'Ascendente')

            if campo_key not in campos_seleccionados:
                continue

            # No duplicar si ya está en order_parts por agrupación
            if agrupaciones and campo_key in agrupaciones:
                continue

            campo = campos_def.get(campo_key)
            if campo:
                if campo['tipo'] == 'dimension':
                    alias_dim = f"{campo_key}_dim"
                    tabla_dim = campo.get('tabla_dimension')

                    if tabla_dim in dimension_columns_cache and dimension_columns_cache[tabla_dim]:
                        campo_nombre = dimension_columns_cache[tabla_dim]
                    else:
                        campo_nombre = campo.get('campo_nombre', 'descripcion')

                    order_parts.append(f"{alias_dim}.{campo_nombre} {'ASC' if orden == 'Ascendente' else 'DESC'}")
                elif campo['tipo'] == 'calculado' or campo['tipo'] == 'numerico':
                    # Para campos calculados/numéricos, usar el alias del SELECT
                    nombre_alias = campo.get('nombre', campo_key)
                    order_parts.append(f"`{nombre_alias}` {'ASC' if orden == 'Ascendente' else 'DESC'}")
                else:
                    tabla_rel = campo.get('tabla_relacion', 'principal')
                    alias_tabla = tabla_aliases.get(tabla_rel, 'p')
                    columna = campo.get('columna_bd', campo_key)
                    order_parts.append(f"{alias_tabla}.{columna} {'ASC' if orden == 'Ascendente' else 'DESC'}")

    if order_parts:
        order_by_clause = "ORDER BY " + ", ".join(order_parts)

    # ========== QUERY FINAL ==========
    query = f"{select_clause}\n{from_clause}"
    if where_clause:
        query += f"\n{where_clause}"
    if group_by_clause:
        query += f"\n{group_by_clause}"
    if order_by_clause:
        query += f"\n{order_by_clause}"

    return query


def calcular_agregacion(funcion, datos, campo_idx, campo_def):
    """
    Calcula una función de agregación sobre un conjunto de datos

    Args:
        funcion: Nombre de la función (COUNT, SUM, AVG, MIN, MAX, COUNT_DISTINCT)
        datos: Lista de filas (tuplas)
        campo_idx: Índice de la columna en las tuplas (None para COUNT)
        campo_def: Definición del campo para validar tipos

    Returns:
        Valor calculado de la agregación
    """
    if not datos:
        return 0

    if funcion == "COUNT":
        return len(datos)

    if funcion == "COUNT_DISTINCT":
        valores = [fila[campo_idx] for fila in datos if fila[campo_idx] is not None]
        return len(set(valores))

    # Para el resto de funciones, necesitamos los valores numéricos
    valores = []
    for fila in datos:
        valor = fila[campo_idx] if campo_idx is not None else None
        if valor is not None:
            try:
                valores.append(float(valor))
            except (ValueError, TypeError):
                pass

    if not valores:
        return 0

    if funcion == "SUM":
        return sum(valores)
    elif funcion == "AVG":
        return sum(valores) / len(valores)
    elif funcion == "MIN":
        return min(valores)
    elif funcion == "MAX":
        return max(valores)

    return 0


def procesar_agrupacion(datos, columnas, agrupaciones, agregaciones_config, campos_def):
    """
    Procesa los datos aplicando agrupación visual y agregaciones

    Args:
        datos: Lista de tuplas con los datos
        columnas: Lista de nombres de columnas
        agrupaciones: Lista de campos por los que agrupar (en orden jerárquico)
        agregaciones_config: Lista de dicts con configuración de agregaciones
                            [{"funcion": "SUM", "campo": "presupuesto"}, ...]
        campos_def: Diccionario con definiciones de campos

    Returns:
        Dict con estructura:
        {
            "grupos": [
                {
                    "nivel": 0,
                    "clave": "Saneamiento",
                    "campo": "red",
                    "datos": [...],  # Filas de este grupo
                    "subtotales": {"presupuesto": 12345.67, ...},
                    "subgrupos": [...]  # Grupos de nivel inferior
                }
            ],
            "totales_generales": {"presupuesto": 50000.00, ...}
        }
    """
    if not agrupaciones:
        # Sin agrupaciones, devolver datos planos con totales
        totales = {}
        if agregaciones_config:
            for agg in agregaciones_config:
                funcion = agg['funcion']
                campo = agg.get('campo')
                campo_idx = columnas.index(campo) if campo and campo in columnas else None
                campo_def = campos_def.get(campo, {})
                totales[f"{funcion}({campo or '*'})"] = calcular_agregacion(funcion, datos, campo_idx, campo_def)

        # Crear mapa de formatos para cada columna
        formatos_columnas = {}
        for col in columnas:
            campo_def = campos_def.get(col, {})
            formato = campo_def.get('formato', 'ninguno')
            formatos_columnas[col] = formato

        # Crear mapa de formatos para agregaciones
        formatos_agregaciones = {}
        if agregaciones_config:
            for agg in agregaciones_config:
                funcion = agg['funcion']
                campo = agg.get('campo', '*')
                key = f"{funcion}({campo})"

                # COUNT siempre es entero, nunca moneda
                if funcion == 'COUNT' or funcion == 'COUNT_DISTINCT':
                    formatos_agregaciones[key] = 'entero'
                else:
                    # Heredar formato del campo base
                    campo_def = campos_def.get(campo, {})
                    formatos_agregaciones[key] = campo_def.get('formato', 'ninguno')

        return {
            "grupos": [],
            "datos_planos": datos,
            "totales_generales": totales,
            "formatos_columnas": formatos_columnas,
            "formatos_agregaciones": formatos_agregaciones
        }

    # Crear índices de columnas para agrupación
    indices_agrupacion = []
    for campo in agrupaciones:
        if campo in columnas:
            indices_agrupacion.append((campo, columnas.index(campo)))

    if not indices_agrupacion:
        # No hay campos válidos de agrupación
        # Crear mapa de formatos para cada columna
        formatos_columnas = {}
        for col in columnas:
            campo_def = campos_def.get(col, {})
            formato = campo_def.get('formato', 'ninguno')
            formatos_columnas[col] = formato

        return {
            "grupos": [],
            "datos_planos": datos,
            "totales_generales": {},
            "formatos_columnas": formatos_columnas,
            "formatos_agregaciones": {}
        }

    def agrupar_recursivo(datos_grupo, nivel=0):
        """Agrupa datos recursivamente por niveles"""
        if nivel >= len(indices_agrupacion):
            return None

        campo, idx = indices_agrupacion[nivel]
        grupos_dict = {}

        # Agrupar por el campo actual
        for fila in datos_grupo:
            clave = fila[idx] if fila[idx] is not None else "(vacío)"
            if clave not in grupos_dict:
                grupos_dict[clave] = []
            grupos_dict[clave].append(fila)

        # Procesar cada grupo
        grupos_resultado = []
        for clave, filas in grupos_dict.items():
            # Calcular subtotales para este grupo
            subtotales = {}
            if agregaciones_config:
                for agg in agregaciones_config:
                    funcion = agg['funcion']
                    campo_agg = agg.get('campo')
                    campo_idx = columnas.index(campo_agg) if campo_agg and campo_agg in columnas else None
                    campo_def = campos_def.get(campo_agg, {})
                    subtotales[f"{funcion}({campo_agg or '*'})"] = calcular_agregacion(funcion, filas, campo_idx, campo_def)

            # Procesar subgrupos si hay más niveles
            subgrupos = None
            if nivel + 1 < len(indices_agrupacion):
                subgrupos = agrupar_recursivo(filas, nivel + 1)

            grupos_resultado.append({
                "nivel": nivel,
                "clave": clave,
                "campo": campo,
                "datos": filas,
                "subtotales": subtotales,
                "subgrupos": subgrupos
            })

        return grupos_resultado

    # Agrupar todos los datos
    grupos = agrupar_recursivo(datos)

    # Calcular totales generales (sobre TODOS los datos, no suma de subtotales)
    totales_generales = {}
    if agregaciones_config:
        for agg in agregaciones_config:
            funcion = agg['funcion']
            campo = agg.get('campo')
            campo_idx = columnas.index(campo) if campo and campo in columnas else None
            campo_def = campos_def.get(campo, {})
            totales_generales[f"{funcion}({campo or '*'})"] = calcular_agregacion(funcion, datos, campo_idx, campo_def)

    # Crear mapa de formatos para cada columna
    formatos_columnas = {}
    for col in columnas:
        campo_def = campos_def.get(col, {})
        formato = campo_def.get('formato', 'ninguno')
        formatos_columnas[col] = formato

    # Crear mapa de formatos para agregaciones
    formatos_agregaciones = {}
    if agregaciones_config:
        for agg in agregaciones_config:
            funcion = agg['funcion']
            campo = agg.get('campo', '*')
            key = f"{funcion}({campo})"

            # COUNT siempre es entero, nunca moneda
            if funcion == 'COUNT' or funcion == 'COUNT_DISTINCT':
                formatos_agregaciones[key] = 'entero'
            else:
                # Heredar formato del campo base
                campo_def = campos_def.get(campo, {})
                formatos_agregaciones[key] = campo_def.get('formato', 'ninguno')

    return {
        "grupos": grupos,
        "totales_generales": totales_generales,
        "formatos_columnas": formatos_columnas,
        "formatos_agregaciones": formatos_agregaciones
    }


def ejecutar_informe(user, password, schema, informe_nombre, filtros=None, ordenaciones=None, campos_seleccionados=None):
    """
    Ejecuta un informe y devuelve los datos con totales

    Args:
        user: Usuario de BD
        password: Contraseña de BD
        schema: Nombre del schema/proyecto
        informe_nombre: Nombre del informe
        filtros: Lista de filtros
        ordenaciones: Lista de ordenaciones
        campos_seleccionados: Lista de campos a mostrar

    Returns:
        Tuple (columnas, datos, totales)
        - columnas: Lista de nombres de columnas
        - datos: Lista de tuplas con los datos
        - totales: Dict con totales por columna totalizable {nombre_col: total}
    """
    try:
        # Obtener definición del informe para determinar el método de ejecución
        definicion = INFORMES_DEFINICIONES.get(informe_nombre)
        usar_agregacion_sql = definicion.get('usar_agregacion_sql', False) if definicion else False
        campos_def = definicion.get('campos', {}) if definicion else {}

        # Decidir qué query builder usar
        if usar_agregacion_sql:
            # NUEVO: Usar query con GROUP BY y SUM en SQL (sin agrupaciones visuales)
            query = build_query_with_sql_aggregation(
                informe_nombre, filtros, ordenaciones, campos_seleccionados,
                agrupaciones=None,  # Sin agrupaciones visuales en este caso
                schema=schema, user=user, password=password
            )
        else:
            # ORIGINAL: Query simple sin GROUP BY
            query = build_query(informe_nombre, filtros, ordenaciones, campos_seleccionados, schema, user, password)

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

            # Calcular totales para campos totalizables (numéricos, moneda)
            totales = {}
            formatos_columnas = {}

            # Las columnas ahora tienen nombres bonitos, necesitamos mapear de nombre a key
            nombre_a_key = {campo.get('nombre', key): key for key, campo in campos_def.items()}

            print(f"DEBUG ejecutar_informe - Columnas: {columnas}")
            print(f"DEBUG ejecutar_informe - nombre_a_key: {nombre_a_key}")
            print(f"DEBUG ejecutar_informe - campos_seleccionados: {campos_seleccionados}")

            if datos and campos_seleccionados:
                for i, col_name in enumerate(columnas):
                    # Buscar el campo por nombre bonito
                    campo_key = nombre_a_key.get(col_name, col_name)
                    campo_def = campos_def.get(campo_key)
                    print(f"DEBUG ejecutar_informe - Col '{col_name}' -> key '{campo_key}' -> def {campo_def is not None}")
                    if campo_def:
                        formato = campo_def.get('formato', '')
                        tipo = campo_def.get('tipo', '')

                        # Guardar formato de la columna
                        formatos_columnas[col_name] = formato if formato else 'ninguno'

                        # Solo totalizar campos numéricos o de moneda
                        if formato in ['moneda', 'numerico'] or tipo in ['numerico', 'calculado']:
                            try:
                                # Calcular suma de la columna
                                total = sum(float(fila[i]) if fila[i] is not None else 0 for fila in datos)
                                totales[col_name] = total
                            except (ValueError, TypeError):
                                # Si no se puede convertir a número, omitir
                                pass

            # Crear un resultado_agrupacion compatible con el que devuelve ejecutar_informe_con_agrupacion
            resultado_agrupacion = {
                "grupos": [],
                "datos_planos": datos,
                "totales_generales": totales,
                "modo": "detalle",
                "formatos_columnas": formatos_columnas,
                "formatos_agregaciones": {}
            }

            return columnas, datos, resultado_agrupacion

    except Exception as e:
        print(f"Error al ejecutar informe: {e}")
        import traceback
        traceback.print_exc()
        return [], [], {}


def ejecutar_informe_con_agrupacion(user, password, schema, informe_nombre, filtros=None,
                                     ordenaciones=None, campos_seleccionados=None,
                                     agrupaciones=None, agregaciones=None, modo="detalle"):
    """
    Ejecuta un informe con agrupaciones y agregaciones

    Args:
        user: Usuario de BD
        password: Contraseña de BD
        schema: Nombre del schema/proyecto
        informe_nombre: Nombre del informe
        filtros: Lista de filtros
        ordenaciones: Lista de ordenaciones
        campos_seleccionados: Lista de campos a mostrar
        agrupaciones: Lista de campos por los que agrupar (ej: ["red", "provincia"])
        agregaciones: Lista de agregaciones (ej: [{"funcion": "SUM", "campo": "presupuesto"}])
        modo: "detalle" (mostrar registros + subtotales) o "resumen" (solo subtotales)

    Returns:
        Tuple (columnas, datos, resultado_agrupacion)
        - columnas: Lista de nombres de columnas
        - datos: Lista de tuplas con los datos originales
        - resultado_agrupacion: Dict con estructura de grupos y totales
    """
    try:
        # Obtener definición del informe para determinar el método de ejecución
        definicion = INFORMES_DEFINICIONES.get(informe_nombre)
        usar_agregacion_sql = definicion.get('usar_agregacion_sql', False) if definicion else False

        # IMPORTANTE: Incluir automáticamente los campos de agrupación en campos_seleccionados
        # Esto es NECESARIO para SQL - los campos en GROUP BY deben estar en SELECT
        # Luego se filtrarán antes de generar el PDF en informes_exportacion.py
        campos_a_incluir = list(campos_seleccionados) if campos_seleccionados else []
        campos_fijos = definicion.get('campos_fijos', False) if definicion else False

        if agrupaciones:
            # SIEMPRE agregar campos de agrupación al SELECT (requerido por SQL)
            for campo_agrupacion in agrupaciones:
                if campo_agrupacion not in campos_a_incluir:
                    campos_a_incluir.append(campo_agrupacion)
                    print(f"DEBUG: Añadiendo campo de agrupación '{campo_agrupacion}' al SELECT (requerido por SQL GROUP BY)")

            if campos_fijos:
                print(f"DEBUG: Informe con campos_fijos=True - campos de agrupación {agrupaciones} se filtrarán en PDF")

        # Decidir qué método usar para obtener los datos
        if usar_agregacion_sql:
            # NUEVO: Usar query con GROUP BY y SUM en SQL
            query = build_query_with_sql_aggregation(
                informe_nombre, filtros, ordenaciones, campos_a_incluir,
                agrupaciones, schema, user, password
            )

            print(f"\n{'='*60}")
            print(f"QUERY CON AGREGACIÓN SQL PARA: {informe_nombre}")
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

                # Calcular totales (opcional)
                totales = {}
                cursor.close()
        else:
            # ORIGINAL: Ejecutar informe normal y agrupar en Python
            columnas, datos, totales = ejecutar_informe(
                user, password, schema, informe_nombre,
                filtros, ordenaciones, campos_a_incluir
            )

        # Si no hay datos, devolver vacío
        if not datos:
            return columnas, datos, {
                "grupos": [],
                "datos_planos": [],
                "totales_generales": {},
                "modo": modo
            }

        # Obtener definición del informe para las definiciones de campos (si no se obtuvo antes)
        if not definicion:
            definicion = INFORMES_DEFINICIONES.get(informe_nombre)
        campos_def = definicion.get('campos', {}) if definicion else {}

        # Procesar agrupación según el método usado
        if usar_agregacion_sql and agrupaciones:
            # Los datos YA vienen agrupados y sumados desde SQL
            # Necesitamos reorganizarlos en la estructura jerárquica que espera pdf_agrupaciones.py

            # Crear mapa de formatos de columnas
            nombre_a_key = {campo.get('nombre', key): key for key, campo in campos_def.items()}
            formatos_columnas = {}
            for col in columnas:
                campo_key = nombre_a_key.get(col, col)
                campo_def = campos_def.get(campo_key, {})
                formato = campo_def.get('formato', 'ninguno')
                formatos_columnas[col] = formato

            # Identificar columnas de agrupación y columnas de datos
            columnas_agrupacion = []
            for agrup_key in agrupaciones:
                campo_agrup = campos_def.get(agrup_key, {})
                nombre_col_agrup = campo_agrup.get('nombre', agrup_key)
                if nombre_col_agrup in columnas:
                    columnas_agrupacion.append(nombre_col_agrup)

            # Columnas de datos (sin agrupaciones)
            columnas_datos = [col for col in columnas if col not in columnas_agrupacion]

            # Construir estructura de grupos
            grupos = []
            totales_generales = {}

            # Agrupar datos por el primer campo de agrupación
            if columnas_agrupacion:
                col_agrup = columnas_agrupacion[0]  # Por ahora solo primer nivel
                idx_agrup = columnas.index(col_agrup)

                # Indices de columnas de datos
                indices_datos = [columnas.index(col) for col in columnas_datos]

                # Agrupar filas por valor de agrupación
                from collections import defaultdict
                grupos_dict = defaultdict(list)

                for fila in datos:
                    clave_grupo = fila[idx_agrup]
                    # Extraer solo datos (sin columna de agrupación)
                    fila_datos = tuple(fila[i] for i in indices_datos)
                    grupos_dict[clave_grupo].append(fila_datos)

                # Crear estructura de grupos
                # Ordenar grupos manejando valores None (los ponemos al final)
                def ordenar_clave(item):
                    clave = item[0]
                    if clave is None:
                        return (1, '')  # None va al final
                    return (0, str(clave))  # Los demás se ordenan alfabéticamente

                for clave, filas_grupo in sorted(grupos_dict.items(), key=ordenar_clave):
                    # Calcular subtotales del grupo
                    subtotales = {}
                    for i, col_nombre in enumerate(columnas_datos):
                        formato = formatos_columnas.get(col_nombre, 'ninguno')
                        # Solo calcular subtotales de campos tipo moneda que sean importes/costes totales
                        # NO calcular subtotales de Cantidad ni Precio unitario
                        es_campo_subtotalizable = (
                            formato == 'moneda' and
                            ('importe' in col_nombre.lower() or 'coste_total' in col_nombre.lower() or 'total' in col_nombre.lower())
                        )

                        if es_campo_subtotalizable:
                            try:
                                total = sum(float(fila[i]) if fila[i] is not None else 0 for fila in filas_grupo)
                                subtotales[col_nombre] = total
                                # Acumular en totales generales
                                totales_generales[col_nombre] = totales_generales.get(col_nombre, 0) + total
                            except (ValueError, TypeError):
                                pass

                    # Agregar grupo
                    grupos.append({
                        'campo': col_agrup,
                        'clave': str(clave) if clave is not None else 'Sin especificar',
                        'datos': filas_grupo,
                        'subtotales': subtotales,
                        'subgrupos': None
                    })

            resultado_agrupacion = {
                "grupos": grupos,
                "datos_planos": datos,
                "totales_generales": totales_generales,
                "modo": modo,
                "formatos_columnas": formatos_columnas,
                "formatos_agregaciones": formatos_columnas,  # Usar los mismos formatos
                "agrupaciones": agrupaciones,
                "columnas_datos": columnas_datos  # Columnas sin agrupación para el PDF
            }

        elif usar_agregacion_sql:
            # Sin agrupaciones, solo devolver datos planos
            nombre_a_key = {campo.get('nombre', key): key for key, campo in campos_def.items()}
            formatos_columnas = {}
            for col in columnas:
                campo_key = nombre_a_key.get(col, col)
                campo_def = campos_def.get(campo_key, {})
                formato = campo_def.get('formato', 'ninguno')
                formatos_columnas[col] = formato

            resultado_agrupacion = {
                "grupos": [],
                "datos_planos": datos,
                "totales_generales": {},
                "modo": modo,
                "formatos_columnas": formatos_columnas,
                "formatos_agregaciones": {}
            }

        else:
            # ORIGINAL: Procesar agrupación en Python (post-procesamiento)
            resultado_agrupacion = procesar_agrupacion(
                datos, columnas, agrupaciones or [], agregaciones or [], campos_def
            )

            # Añadir el modo al resultado
            resultado_agrupacion['modo'] = modo

        return columnas, datos, resultado_agrupacion

    except Exception as e:
        print(f"Error al ejecutar informe con agrupación: {e}")
        import traceback
        traceback.print_exc()
        return [], [], {
            "grupos": [],
            "datos_planos": [],
            "totales_generales": {},
            "modo": modo
        }


def ejecutar_informe_ordenes_recursos(user, password, schema, informe_nombre, filtros=None,
                                       ordenaciones=None, agrupaciones=None):
    """
    Ejecuta el informe especial de Órdenes de Trabajo con sus recursos presupuestados

    Este informe muestra cada orden con su cabecera (código, título, fecha, localización, etc.)
    seguida de una tabla de recursos presupuestados específicos de esa orden.

    Args:
        user: Usuario de BD
        password: Contraseña de BD
        schema: Nombre del schema/proyecto
        informe_nombre: Nombre del informe (debe ser "Presupuesto Detallado")
        filtros: Lista de filtros a aplicar sobre las órdenes
        ordenaciones: Lista de ordenaciones
        agrupaciones: Lista de campos por los que agrupar (opcional)

    Returns:
        Dict con estructura especial:
        {
            "tipo": "ordenes_con_recursos",
            "ordenes": [
                {
                    "id": 1,
                    "datos_orden": {"codigo": "OT-001", "titulo": "...", "fecha_fin": "...", ...},
                    "recursos": [
                        {"codigo": "R001", "cantidad": 12.5, "unidad": "m", ...},
                        ...
                    ],
                    "total_orden": 1234.56
                },
                ...
            ],
            "grupos": [...],  # Si hay agrupaciones
            "gran_total": 12345.67,
            "formatos": {...}
        }
    """
    try:
        definicion = INFORMES_DEFINICIONES.get(informe_nombre)
        if not definicion:
            raise ValueError(f"No se encontró definición para informe: {informe_nombre}")

        campos_orden = definicion.get('campos_orden', {})
        campos_recursos = definicion.get('campos_recursos', {})
        campos_filtro = definicion.get('campos', {})

        # PASO 1: Construir query para obtener órdenes según filtros y agrupaciones
        query_ordenes = _build_query_ordenes(
            definicion, filtros, ordenaciones, agrupaciones, schema, user, password
        )

        print(f"\n{'='*60}")
        print(f"QUERY ÓRDENES PARA: {informe_nombre}")
        print(f"{'='*60}")
        print(query_ordenes)
        print(f"{'='*60}\n")

        # Ejecutar query de órdenes
        with get_project_connection(user, password, schema) as conn:
            cursor = conn.cursor()
            cursor.execute(query_ordenes)
            ordenes_data = cursor.fetchall()
            ordenes_columns = [desc[0] for desc in cursor.description]

            # PASO 2: Para cada orden, obtener sus recursos
            ordenes_con_recursos = []
            gran_total = 0

            for orden_row in ordenes_data:
                # Crear dict con datos de la orden
                orden_dict = dict(zip(ordenes_columns, orden_row))
                orden_id = orden_dict.get('id')

                if not orden_id:
                    print(f"ADVERTENCIA: Orden sin ID, omitiendo: {orden_dict}")
                    continue

                # Query para obtener recursos de esta orden específica
                query_recursos = _build_query_recursos(orden_id, campos_recursos)

                cursor.execute(query_recursos)
                recursos_data = cursor.fetchall()

                # Convertir recursos a lista de diccionarios
                recursos_list = []
                total_orden = 0

                for recurso_row in recursos_data:
                    recurso_dict = {
                        'codigo': recurso_row[0],
                        'cantidad': recurso_row[1],
                        'unidad': recurso_row[2],
                        'resumen': recurso_row[3],
                        'coste': recurso_row[4],
                        'coste_total': recurso_row[5]
                    }
                    recursos_list.append(recurso_dict)
                    total_orden += float(recurso_dict['coste_total'] or 0)

                # Agregar orden con sus recursos
                ordenes_con_recursos.append({
                    'id': orden_id,
                    'datos_orden': orden_dict,
                    'recursos': recursos_list,
                    'total_orden': total_orden
                })

                gran_total += total_orden

            cursor.close()

        # PASO 3: Si hay agrupaciones, organizar órdenes en grupos
        grupos = []
        if agrupaciones and ordenes_con_recursos:
            grupos = _agrupar_ordenes(ordenes_con_recursos, agrupaciones, ordenes_columns)

        # Resultado
        resultado = {
            'tipo': 'ordenes_con_recursos',
            'ordenes': ordenes_con_recursos,
            'grupos': grupos,
            'agrupaciones': agrupaciones or [],
            'gran_total': gran_total,
            'campos_orden': campos_orden,
            'campos_recursos': campos_recursos,
            'formatos': {
                'coste': 'moneda',
                'coste_total': 'moneda',
                'cantidad': 'decimal',
                'latitud': 'decimal',
                'longitud': 'decimal'
            }
        }

        return resultado

    except Exception as e:
        print(f"Error al ejecutar informe de órdenes con recursos: {e}")
        import traceback
        traceback.print_exc()
        return {
            'tipo': 'ordenes_con_recursos',
            'ordenes': [],
            'grupos': [],
            'agrupaciones': [],
            'gran_total': 0,
            'campos_orden': {},
            'campos_recursos': {},
            'formatos': {}
        }


def _build_query_ordenes(definicion, filtros, ordenaciones, agrupaciones, schema, user, password):
    """Construye query SQL para obtener las órdenes de trabajo"""
    campos = definicion.get('campos', {})
    campos_orden = definicion.get('campos_orden', {})

    # Campos a seleccionar (incluir id, campos de orden y campos de agrupación)
    select_fields = ['p.id']

    # Agregar campos de la orden
    for campo_key, campo_def in campos_orden.items():
        columna_bd = campo_def.get('columna_bd')
        if columna_bd:
            select_fields.append(f'p.{columna_bd} AS {campo_key}')
        elif campo_def.get('tipo') == 'dimension':
            tabla_dim = campo_def.get('tabla_dimension')
            campo_nombre = campo_def.get('campo_nombre', 'descripcion')
            alias_tabla = campo_key + '_dim'
            select_fields.append(f'{alias_tabla}.{campo_nombre} AS {campo_key}')

    # Agregar campos de agrupación si existen
    joins = []
    if agrupaciones:
        for agrup_key in agrupaciones:
            campo_def = campos.get(agrup_key)
            if not campo_def:
                continue

            if campo_def.get('tipo') == 'calculado':
                formula = campo_def.get('formula', '')
                select_fields.append(f'{formula} AS {agrup_key}')
            elif campo_def.get('tipo') == 'dimension':
                tabla_dim = campo_def.get('tabla_dimension')
                campo_nombre = campo_def.get('campo_nombre', 'descripcion')
                columna_bd = campo_def.get('columna_bd')
                alias_tabla = agrup_key + '_agrup_dim'
                select_fields.append(f'{alias_tabla}.{campo_nombre} AS {agrup_key}')
                joins.append(f'LEFT JOIN {tabla_dim} {alias_tabla} ON p.{columna_bd} = {alias_tabla}.id')
            else:
                columna_bd = campo_def.get('columna_bd')
                if columna_bd:
                    select_fields.append(f'p.{columna_bd} AS {agrup_key}')

    # Construir FROM y JOINs para dimensiones de orden
    from_clause = 'tbl_partes p'
    for campo_key, campo_def in campos_orden.items():
        if campo_def.get('tipo') == 'dimension':
            tabla_dim = campo_def.get('tabla_dimension')
            columna_bd = campo_def.get('columna_bd')
            alias_tabla = campo_key + '_dim'
            joins.append(f'LEFT JOIN {tabla_dim} {alias_tabla} ON p.{columna_bd} = {alias_tabla}.id')

    # Construir WHERE (filtros)
    where_clauses = []
    if filtros:
        where_clauses = _build_where_clauses(filtros, campos, schema, user, password)

    # Construir ORDER BY
    order_by_clauses = []
    if agrupaciones:
        # Ordenar primero por campos de agrupación
        order_by_clauses.extend(agrupaciones)
    if ordenaciones:
        for ord_campo, ord_dir in ordenaciones:
            if ord_campo not in order_by_clauses:  # Evitar duplicados
                direccion = 'ASC' if ord_dir == 'Ascendente' else 'DESC'
                order_by_clauses.append(f'{ord_campo} {direccion}')

    # Construir query final
    query = f"SELECT {', '.join(select_fields)} FROM {from_clause}"
    if joins:
        query += ' ' + ' '.join(joins)
    if where_clauses:
        query += f" WHERE {' AND '.join(where_clauses)}"
    if order_by_clauses:
        query += f" ORDER BY {', '.join(order_by_clauses)}"

    return query


def _build_query_recursos(orden_id, campos_recursos):
    """Construye query SQL para obtener recursos de una orden específica"""
    # Query fijo para obtener los 6 campos de recursos
    query = f"""
        SELECT
            precio.codigo AS codigo,
            pres.cantidad AS cantidad,
            unidad_dim.unidad AS unidad,
            precio.resumen AS resumen,
            precio.coste AS coste,
            (pres.cantidad * precio.coste) AS coste_total
        FROM tbl_part_presupuesto pres
        LEFT JOIN tbl_pres_precios precio ON pres.precio_id = precio.id
        LEFT JOIN tbl_pres_unidades unidad_dim ON precio.id_unidades = unidad_dim.id
        WHERE pres.parte_id = {orden_id}
          AND pres.cantidad > 0
        ORDER BY precio.codigo
    """
    return query


def _agrupar_ordenes(ordenes_con_recursos, agrupaciones, ordenes_columns):
    """Organiza las órdenes en grupos jerárquicos según los campos de agrupación"""
    if not agrupaciones or not ordenes_con_recursos:
        return []

    # Construir estructura jerárquica de grupos
    grupos = []

    def _obtener_valor_agrupacion(orden, campo_agrupacion):
        """Obtiene el valor del campo de agrupación de una orden"""
        return orden['datos_orden'].get(campo_agrupacion, 'Sin especificar')

    def _agrupar_recursivo(ordenes, niveles_agrupacion, nivel=0):
        """Agrupa órdenes recursivamente por múltiples niveles"""
        if nivel >= len(niveles_agrupacion):
            return ordenes

        campo_actual = niveles_agrupacion[nivel]
        grupos_nivel = {}

        # Agrupar por el campo actual
        for orden in ordenes:
            valor = _obtener_valor_agrupacion(orden, campo_actual)
            if valor not in grupos_nivel:
                grupos_nivel[valor] = []
            grupos_nivel[valor].append(orden)

        # Construir resultado
        resultado = []
        for valor, ordenes_grupo in sorted(grupos_nivel.items()):
            # Calcular subtotal del grupo
            subtotal = sum(orden['total_orden'] for orden in ordenes_grupo)

            grupo = {
                'nivel': nivel,
                'campo': campo_actual,
                'valor': valor,
                'ordenes': ordenes_grupo,
                'subtotal': subtotal,
                'subgrupos': []
            }

            # Si hay más niveles, agrupar recursivamente
            if nivel + 1 < len(niveles_agrupacion):
                grupo['subgrupos'] = _agrupar_recursivo(ordenes_grupo, niveles_agrupacion, nivel + 1)
                # Si hay subgrupos, no incluir órdenes directamente
                grupo['ordenes'] = []

            resultado.append(grupo)

        return resultado

    grupos = _agrupar_recursivo(ordenes_con_recursos, agrupaciones)
    return grupos


def _build_where_clauses(filtros, campos_def, schema, user, password):
    """Construye las cláusulas WHERE para los filtros"""
    where_clauses = []

    for filtro in filtros:
        campo = filtro.get('campo')
        operador = filtro.get('operador')
        valor = filtro.get('valor')
        valor2 = filtro.get('valor2')  # Para operador "Entre"

        campo_def = campos_def.get(campo)
        if not campo_def:
            continue

        # Determinar la expresión SQL del campo
        if campo_def.get('tipo') == 'calculado':
            campo_sql = campo_def.get('formula', campo)
        elif campo_def.get('tipo') == 'dimension':
            alias_tabla = campo + '_dim'
            campo_nombre = campo_def.get('campo_nombre', 'descripcion')
            campo_sql = f'{alias_tabla}.{campo_nombre}'
        else:
            columna_bd = campo_def.get('columna_bd', campo)
            campo_sql = f'p.{columna_bd}'

        # Construir cláusula WHERE según operador
        if operador == 'Igual a':
            where_clauses.append(f"{campo_sql} = '{valor}'")
        elif operador == 'Diferente de':
            where_clauses.append(f"{campo_sql} != '{valor}'")
        elif operador == 'Contiene':
            where_clauses.append(f"{campo_sql} LIKE '%{valor}%'")
        elif operador == 'No contiene':
            where_clauses.append(f"{campo_sql} NOT LIKE '%{valor}%'")
        elif operador == 'Mayor a':
            where_clauses.append(f"{campo_sql} > {valor}")
        elif operador == 'Menor a':
            where_clauses.append(f"{campo_sql} < {valor}")
        elif operador == 'Mayor o igual a':
            where_clauses.append(f"{campo_sql} >= {valor}")
        elif operador == 'Menor o igual a':
            where_clauses.append(f"{campo_sql} <= {valor}")
        elif operador == 'Entre' and valor2:
            where_clauses.append(f"{campo_sql} BETWEEN {valor} AND {valor2}")
        elif operador == 'Posterior a':
            where_clauses.append(f"{campo_sql} > '{valor}'")
        elif operador == 'Anterior a':
            where_clauses.append(f"{campo_sql} < '{valor}'")

    return where_clauses
