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
        # Construir query (pasando user y password para detectar columnas de dimensiones)
        query = build_query(informe_nombre, filtros, ordenaciones, campos_seleccionados, schema, user, password)

        print(f"\n{'='*60}")
        print(f"QUERY GENERADO PARA INFORME: {informe_nombre}")
        print(f"{'='*60}")
        print(query)
        print(f"{'='*60}\n")

        # Obtener definición del informe para identificar campos totalizables
        definicion = INFORMES_DEFINICIONES.get(informe_nombre)
        campos_def = definicion.get('campos', {}) if definicion else {}

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
            if datos and campos_seleccionados:
                for i, col_name in enumerate(columnas):
                    # Buscar la definición del campo
                    campo_def = campos_def.get(col_name)
                    if campo_def:
                        formato = campo_def.get('formato', '')
                        tipo = campo_def.get('tipo', '')

                        # Solo totalizar campos numéricos o de moneda
                        if formato in ['moneda', 'numerico'] or tipo in ['numerico', 'calculado']:
                            try:
                                # Calcular suma de la columna
                                total = sum(float(fila[i]) if fila[i] is not None else 0 for fila in datos)
                                totales[col_name] = total
                            except (ValueError, TypeError):
                                # Si no se puede convertir a número, omitir
                                pass

            return columnas, datos, totales

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
        # IMPORTANTE: Incluir automáticamente los campos de agrupación en campos_seleccionados
        # para que estén disponibles en el SELECT incluso si el usuario no los seleccionó explícitamente
        campos_a_incluir = list(campos_seleccionados) if campos_seleccionados else []

        if agrupaciones:
            for campo_agrupacion in agrupaciones:
                if campo_agrupacion not in campos_a_incluir:
                    campos_a_incluir.append(campo_agrupacion)
                    print(f"DEBUG: Añadiendo campo de agrupación '{campo_agrupacion}' al SELECT")

        # Primero ejecutar el informe normal para obtener los datos
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

        # Obtener definición del informe para las definiciones de campos
        definicion = INFORMES_DEFINICIONES.get(informe_nombre)
        campos_def = definicion.get('campos', {}) if definicion else {}

        # Procesar agrupación si se especificó
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
