# script/informes_config.py
"""
Configuración del módulo de Informes
Define categorías, tipos de informes, campos, operadores, etc.
"""

# ============================================================
# CATEGORÍAS E INFORMES
# ============================================================

CATEGORIAS_INFORMES = {
    "📊 Partes": [
        "Listado de Partes",
        "Trabajos Programados"
    ],

    "📦 Recursos": [
        "Listado de Partidas del Presupuesto",
        "Recursos Presupuestados",
        "Recursos Certificados",
        "Recursos Pendientes"
    ],

    "💰 Presupuestos": [
        "Contrato",
        "Presupuesto Detallado",
        "Presupuesto Resumen"
    ],

    "✅ Certificaciones": [
        "Certificación Detallado",
        "Certificación Resumen"
    ]
}


# ============================================================
# DEFINICIONES COMPLETAS DE INFORMES
# ============================================================

INFORMES_DEFINICIONES = {
    # ============================================================
    # CATEGORÍA: PARTES
    # ============================================================

    "Listado de Partes": {
        "categoria": "📊 Partes",
        "descripcion": "Relación de todos los partes con campos de tbl_partes, importes de presupuesto y certificado. Total al final de presupuesto y certificación.",
        "tabla_principal": "tbl_partes",

        # Campos disponibles para mostrar
        "campos": {
            "mes": {
                "nombre": "Mes",
                "tipo": "calculado",
                "formula": "DATE_FORMAT(p.fecha_inicio, '%Y-%m')",
                "grupo": "Temporal"
            },
            "año": {
                "nombre": "Año",
                "tipo": "calculado",
                "formula": "YEAR(p.fecha_inicio)",
                "grupo": "Temporal"
            },
            "codigo": {
                "nombre": "Código",
                "tipo": "texto",
                "columna_bd": "codigo",
                "grupo": "Información Básica"
            },
            "titulo": {
                "nombre": "Título",
                "tipo": "texto",
                "columna_bd": "titulo",
                "grupo": "Información Básica"
            },
            "descripcion": {
                "nombre": "Descripción",
                "tipo": "texto",
                "columna_bd": "descripcion",
                "grupo": "Información Básica"
            },
            "estado": {
                "nombre": "Estado",
                "tipo": "texto",
                "columna_bd": "estado",
                "grupo": "Información Básica"
            },
            "red": {
                "nombre": "Red",
                "tipo": "dimension",
                "columna_bd": "red_id",
                "tabla_dimension": "dim_red",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "tipo_trabajo": {
                "nombre": "Tipo de Trabajo",
                "tipo": "dimension",
                "columna_bd": "tipo_trabajo_id",
                "tabla_dimension": "dim_tipo_trabajo",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "codigo_trabajo": {
                "nombre": "Código de Trabajo",
                "tipo": "dimension",
                "columna_bd": "cod_trabajo_id",
                "tabla_dimension": "dim_codigo_trabajo",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "provincia": {
                "nombre": "Provincia",
                "tipo": "dimension",
                "columna_bd": "provincia_id",
                "tabla_dimension": "dim_provincias",
                "campo_nombre": "nombre",
                "grupo": "Ubicación Geográfica"
            },
            "comarca": {
                "nombre": "Comarca",
                "tipo": "dimension",
                "columna_bd": "comarca_id",
                "tabla_dimension": "dim_comarcas",
                "campo_nombre": "nombre",
                "grupo": "Ubicación Geográfica"
            },
            "municipio": {
                "nombre": "Municipio",
                "tipo": "dimension",
                "columna_bd": "municipio_id",
                "tabla_dimension": "dim_municipios",
                "campo_nombre": "nombre",
                "grupo": "Ubicación Geográfica"
            },
            "concejo": {
                "nombre": "Concejo",
                "tipo": "dimension",
                "columna_bd": "concejo_id",
                "tabla_dimension": "dim_concejos",
                "campo_nombre": "nombre",
                "grupo": "Ubicación Geográfica"
            },
            "presupuesto": {
                "nombre": "Presupuesto",
                "tipo": "calculado",
                "formula": "COALESCE((SELECT SUM(pp.cantidad * pp.precio_unit) FROM tbl_part_presupuesto pp WHERE pp.parte_id = p.id), 0)",
                "formato": "moneda",
                "grupo": "Económico"
            },
            "certificado": {
                "nombre": "Certificado",
                "tipo": "calculado",
                "formula": "COALESCE((SELECT SUM(pc.cantidad_cert * pc.precio_unit) FROM tbl_part_certificacion pc WHERE pc.parte_id = p.id AND pc.certificada = 1), 0)",
                "formato": "moneda",
                "grupo": "Económico"
            },
            "pendiente": {
                "nombre": "Pendiente",
                "tipo": "calculado",
                "formula": "COALESCE((SELECT SUM(pp.cantidad * pp.precio_unit) FROM tbl_part_presupuesto pp WHERE pp.parte_id = p.id), 0) - COALESCE((SELECT SUM(pc.cantidad_cert * pc.precio_unit) FROM tbl_part_certificacion pc WHERE pc.parte_id = p.id AND pc.certificada = 1), 0)",
                "formato": "moneda",
                "grupo": "Económico"
            },
            "fecha_inicio": {
                "nombre": "Fecha Inicio",
                "tipo": "fecha",
                "columna_bd": "fecha_inicio",
                "grupo": "Fechas"
            },
            "fecha_fin": {
                "nombre": "Fecha Fin",
                "tipo": "fecha",
                "columna_bd": "fecha_fin",
                "grupo": "Fechas"
            },
            "localizacion": {
                "nombre": "Localización",
                "tipo": "texto",
                "columna_bd": "localizacion",
                "grupo": "Ubicación Geográfica"
            },
            "latitud": {
                "nombre": "Latitud",
                "tipo": "numerico",
                "columna_bd": "latitud",
                "formato": "decimal",
                "grupo": "Ubicación Geográfica"
            },
            "longitud": {
                "nombre": "Longitud",
                "tipo": "numerico",
                "columna_bd": "longitud",
                "formato": "decimal",
                "grupo": "Ubicación Geográfica"
            },
            "trabajadores": {
                "nombre": "Trabajadores",
                "tipo": "texto",
                "columna_bd": "trabajadores",
                "grupo": "Recursos Humanos"
            },
            "tipo_rep": {
                "nombre": "Tipo de Reparación",
                "tipo": "dimension",
                "columna_bd": "tipo_rep_id",
                "tabla_dimension": "dim_tipos_rep",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "creado_en": {
                "nombre": "Fecha Creación",
                "tipo": "fecha",
                "columna_bd": "creado_en",
                "grupo": "Fechas"
            },
            "actualizado_en": {
                "nombre": "Fecha Actualización",
                "tipo": "fecha",
                "columna_bd": "actualizado_en",
                "grupo": "Fechas"
            },
            "finalizada": {
                "nombre": "Finalizada",
                "tipo": "booleano",
                "columna_bd": "finalizada",
                "grupo": "Información Básica"
            }
        },

        # Filtros disponibles
        "filtros": {
            "mes": {
                "campo": "mes",
                "tipo": "mes_anio",
                "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
            },
            "año": {
                "campo": "año",
                "tipo": "anio",
                "operadores": ["Igual a", "Mayor a", "Menor a", "Entre"]
            },
            "titulo": {
                "campo": "titulo",
                "tipo": "texto",
                "operadores": ["Igual a", "Diferente de", "Contiene", "No contiene"]
            },
            "estado": {
                "campo": "estado",
                "tipo": "select",
                "operadores": ["Igual a", "Diferente de"],
                "valores": ["Pendiente", "En curso", "Finalizado"]
            },
            "red": {
                "campo": "red",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_red"
            },
            "tipo_trabajo": {
                "campo": "tipo_trabajo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_tipo_trabajo"
            },
            "codigo_trabajo": {
                "campo": "codigo_trabajo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_codigo_trabajo"
            },
            "provincia": {
                "campo": "provincia",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_provincias"
            },
            "comarca": {
                "campo": "comarca",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_comarcas"
            },
            "municipio": {
                "campo": "municipio",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_municipios"
            },
            "concejo": {
                "campo": "concejo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_concejos"
            },
            "presupuesto": {
                "campo": "presupuesto",
                "tipo": "numerico",
                "operadores": ["Igual a", "Mayor a", "Menor a", "Mayor o igual a", "Menor o igual a", "Entre"]
            },
            "fecha_inicio": {
                "campo": "fecha_inicio",
                "tipo": "fecha",
                "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
            },
            "localizacion": {
                "campo": "localizacion",
                "tipo": "texto",
                "operadores": ["Igual a", "Diferente de", "Contiene", "No contiene"]
            },
            "latitud": {
                "campo": "latitud",
                "tipo": "numerico",
                "operadores": ["Igual a", "Mayor a", "Menor a", "Mayor o igual a", "Menor o igual a", "Entre"]
            },
            "longitud": {
                "campo": "longitud",
                "tipo": "numerico",
                "operadores": ["Igual a", "Mayor a", "Menor a", "Mayor o igual a", "Menor o igual a", "Entre"]
            },
            "trabajadores": {
                "campo": "trabajadores",
                "tipo": "texto",
                "operadores": ["Igual a", "Diferente de", "Contiene", "No contiene"]
            },
            "tipo_rep": {
                "campo": "tipo_rep",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_tipos_rep"
            },
            "creado_en": {
                "campo": "creado_en",
                "tipo": "fecha",
                "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
            },
            "actualizado_en": {
                "campo": "actualizado_en",
                "tipo": "fecha",
                "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
            },
            "finalizada": {
                "campo": "finalizada",
                "tipo": "booleano",
                "operadores": ["Sí", "No"]
            }
        },

        # Ordenaciones disponibles (ORDER BY)
        "ordenaciones": [
            "mes",
            "año",
            "estado",
            "red",
            "tipo_trabajo",
            "provincia",
            "comarca",
            "municipio",
            "fecha_inicio",
            "tipo_rep",
            "creado_en",
            "actualizado_en",
            "finalizada"
        ],

        # Agrupaciones disponibles (GROUP BY visual)
        "agrupaciones": {
            # Campos permitidos para agrupar
            "campos_permitidos": [
                "mes",
                "año",
                "estado",
                "red",
                "tipo_trabajo",
                "codigo_trabajo",
                "tipo_rep",
                "provincia",
                "comarca",
                "municipio",
                "trabajadores"
            ],

            # Máximo de niveles de agrupación permitidos
            "max_niveles": 3,

            # Modo de visualización por defecto
            "modo_default": "detalle"  # "detalle" o "resumen"
        },

        # Agregaciones disponibles (funciones)
        "agregaciones": {
            "COUNT": {
                "nombre": "Contar registros",
                "descripcion": "Cuenta el número de registros",
                "aplicable_a": ["*"],  # Aplicable a cualquier campo
                "tipo_resultado": "numerico",
                "formato": "entero"
            },
            "COUNT_DISTINCT": {
                "nombre": "Contar valores únicos",
                "descripcion": "Cuenta valores únicos del campo",
                "aplicable_a": ["texto", "dimension"],
                "tipo_resultado": "numerico",
                "formato": "entero"
            },
            "SUM": {
                "nombre": "Suma",
                "descripcion": "Suma los valores del campo",
                "aplicable_a": ["numerico", "calculado"],
                "tipo_resultado": "numerico",
                "formato": "original"
            },
            "AVG": {
                "nombre": "Promedio",
                "descripcion": "Calcula el promedio de los valores",
                "aplicable_a": ["numerico", "calculado"],
                "tipo_resultado": "numerico",
                "formato": "decimal"
            },
            "MIN": {
                "nombre": "Mínimo",
                "descripcion": "Encuentra el valor mínimo",
                "aplicable_a": ["numerico", "calculado", "fecha"],
                "tipo_resultado": "original",
                "formato": "original"
            },
            "MAX": {
                "nombre": "Máximo",
                "descripcion": "Encuentra el valor máximo",
                "aplicable_a": ["numerico", "calculado", "fecha"],
                "tipo_resultado": "original",
                "formato": "original"
            }
        },

        # Campos por defecto seleccionados
        "campos_default": [
            "codigo",
            "titulo",
            "descripcion",
            "estado",
            "red",
            "tipo_trabajo",
            "provincia",
            "presupuesto",
            "certificado",
            "pendiente"
        ]
    },

    "Trabajos Programados": {
        "categoria": "📊 Partes",
        "descripcion": "Listado de trabajos programados agrupados por Código de Trabajo. En Excel genera una pestaña por cada código, en PDF una sección por código.",
        "tabla_principal": "tbl_partes",

        # Flag especial: agrupar por codigo_trabajo al exportar
        "agrupar_export_por": "codigo_trabajo",

        # Campos fijos - el usuario no puede modificar la selección
        "campos_fijos": True,

        # Campos disponibles para mostrar (mismo que Listado de Partes pero solo los necesarios)
        "campos": {
            "codigo": {
                "nombre": "Código",
                "tipo": "texto",
                "columna_bd": "codigo",
                "grupo": "Información Básica"
            },
            "fecha_inicio": {
                "nombre": "Fecha Inicio",
                "tipo": "fecha",
                "columna_bd": "fecha_inicio",
                "grupo": "Fechas"
            },
            "fecha_fin": {
                "nombre": "Fecha Fin",
                "tipo": "fecha",
                "columna_bd": "fecha_fin",
                "grupo": "Fechas"
            },
            "titulo": {
                "nombre": "Título",
                "tipo": "texto",
                "columna_bd": "titulo",
                "grupo": "Información Básica"
            },
            "descripcion": {
                "nombre": "Descripción",
                "tipo": "texto",
                "columna_bd": "descripcion",
                "grupo": "Información Básica"
            },
            "red": {
                "nombre": "Red",
                "tipo": "dimension",
                "columna_bd": "red_id",
                "tabla_dimension": "dim_red",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "comarca": {
                "nombre": "Comarca",
                "tipo": "dimension",
                "columna_bd": "comarca_id",
                "tabla_dimension": "dim_comarcas",
                "campo_nombre": "comarca_nombre",
                "grupo": "Ubicación Geográfica"
            },
            "municipio": {
                "nombre": "Municipio",
                "tipo": "dimension",
                "columna_bd": "municipio_id",
                "tabla_dimension": "dim_municipios",
                "campo_nombre": "municipio_nombre",
                "grupo": "Ubicación Geográfica"
            },
            "concejo": {
                "nombre": "Concejo",
                "tipo": "dimension",
                "columna_bd": "concejo_id",
                "tabla_dimension": "dim_concejos",
                "campo_nombre": "nombre",
                "grupo": "Ubicación Geográfica"
            },
            "tipo_trabajo": {
                "nombre": "Tipo de Trabajo",
                "tipo": "dimension",
                "columna_bd": "tipo_trabajo_id",
                "tabla_dimension": "dim_tipo_trabajo",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "codigo_trabajo": {
                "nombre": "Código de Trabajo",
                "tipo": "dimension",
                "columna_bd": "cod_trabajo_id",
                "tabla_dimension": "dim_codigo_trabajo",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "mes": {
                "nombre": "Mes",
                "tipo": "calculado",
                "formula": "DATE_FORMAT(p.fecha_inicio, '%Y-%m')",
                "grupo": "Temporal"
            }
        },

        # Solo filtro de mes disponible
        "filtros": {
            "mes": {
                "campo": "mes",
                "tipo": "mes_anio",
                "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
            }
        },

        # Ordenaciones por defecto
        "ordenaciones": [
            "codigo_trabajo",
            "fecha_inicio",
            "codigo"
        ],

        # Sin agrupaciones para este informe
        "agrupaciones": {
            "campos_permitidos": [],
            "max_niveles": 0,
            "modo_default": "detalle"
        },

        # Sin agregaciones para este informe
        "agregaciones": {},

        # Campos por defecto seleccionados (en el orden especificado)
        "campos_default": [
            "codigo",
            "fecha_inicio",
            "fecha_fin",
            "titulo",
            "descripcion",
            "red",
            "comarca",
            "municipio",
            "concejo",
            "tipo_trabajo",
            "codigo_trabajo"
        ]
    },

    # ============================================================
    # CATEGORÍA: RECURSOS
    # ============================================================

    "Listado de Partidas del Presupuesto": {
        "categoria": "📦 Recursos",
        "descripcion": "Partidas clasificadas en base a los capítulos del presupuesto. Con unidad de medición, descripción, y precio unitario.",
        "tabla_principal": "tbl_pres_precios",

        "campos": {
            "capitulo": {
                "nombre": "Capítulo",
                "tipo": "dimension",
                "columna_bd": "id_capitulo",
                "tabla_dimension": "tbl_pres_capitulos",
                "campo_nombre": "descripcion",
                "grupo": "Ordenación"
            },
            "codigo": {
                "nombre": "Código",
                "tipo": "texto",
                "columna_bd": "codigo",
                "grupo": "Información Básica"
            },
            "unidad": {
                "nombre": "Ud",
                "tipo": "dimension",
                "columna_bd": "id_unidades",
                "tabla_dimension": "tbl_pres_unidades",
                "campo_nombre": "unidad",
                "grupo": "Información Básica"
            },
            "resumen": {
                "nombre": "Recurso/Material",
                "tipo": "texto",
                "columna_bd": "resumen",
                "grupo": "Información Básica"
            },
            "descripcion": {
                "nombre": "Descripción Completa",
                "tipo": "texto",
                "columna_bd": "descripcion",
                "grupo": "Información Básica"
            },
            "precio_unitario": {
                "nombre": "Precio",
                "tipo": "numerico",
                "columna_bd": "coste",
                "formato": "moneda",
                "grupo": "Económico"
            },
            "naturaleza": {
                "nombre": "Naturaleza",
                "tipo": "dimension",
                "columna_bd": "id_naturaleza",
                "tabla_dimension": "tbl_pres_naturaleza",
                "campo_nombre": "descripcion",
                "grupo": "Ordenación"
            }
        },

        "filtros": {
            "capitulo": {
                "campo": "capitulo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "tbl_pres_capitulos"
            },
            "naturaleza": {
                "campo": "naturaleza",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "tbl_pres_naturaleza"
            },
            "codigo": {
                "campo": "codigo",
                "tipo": "texto",
                "operadores": ["Contiene", "Empieza con", "Termina con", "Igual a"]
            }
        },

        "ordenaciones": [
            "capitulo",
            "naturaleza",
            "codigo",
            "precio_unitario"
        ],

        "agrupaciones": {
            "campos_permitidos": [
                "capitulo",
                "naturaleza"
            ],
            "max_niveles": 2,
            "modo_default": "detalle"
        },

        "agregaciones": {
            "COUNT": {
                "nombre": "Contar registros",
                "aplicable_a": ["*"],
                "tipo_resultado": "numerico",
                "formato": "entero"
            },
            "AVG": {
                "nombre": "Promedio",
                "aplicable_a": ["numerico"],
                "tipo_resultado": "numerico",
                "formato": "decimal"
            },
            "MIN": {
                "nombre": "Mínimo",
                "aplicable_a": ["numerico"],
                "tipo_resultado": "numerico",
                "formato": "original"
            },
            "MAX": {
                "nombre": "Máximo",
                "aplicable_a": ["numerico"],
                "tipo_resultado": "numerico",
                "formato": "original"
            }
        },

        "campos_default": [
            "capitulo",
            "codigo",
            "unidad",
            "resumen",
            "precio_unitario"
        ]
    },

    "Recursos Presupuestados": {
        "categoria": "📦 Recursos",
        "descripcion": "Listado de recursos/partidas presupuestadas con cantidad y coste total",
        "tabla_principal": "tbl_part_presupuesto",
        "require_joins": ["tbl_pres_precios", "tbl_partes"],
        "formato_pdf": "vertical",  # Formato vertical para PDF
        "campos_fijos": True,  # No permite selección de campos
        "filtro_cantidad_cero": True,  # Excluir registros con cantidad = 0
        "usar_agregacion_sql": True,  # Usar GROUP BY y SUM en SQL
        "campos_default": ["codigo", "cantidad", "unidad", "resumen", "coste", "coste_total"],  # Campos que siempre se muestran

        "campos": {
            # Campos de tbl_pres_precios (tabla de precios)
            "capitulo": {
                "nombre": "Capítulo",
                "tipo": "dimension",
                "tabla_relacion": "precio",
                "columna_bd": "id_capitulo",
                "tabla_dimension": "tbl_pres_capitulos",
                "campo_nombre": "descripcion",
                "grupo": "Precio"
            },
            "codigo": {
                "nombre": "Código",
                "tipo": "texto",
                "tabla_relacion": "precio",
                "columna_bd": "codigo",
                "grupo": "Precio"
            },
            "unidad": {
                "nombre": "Ud.",
                "tipo": "dimension",
                "tabla_relacion": "precio",
                "columna_bd": "id_unidades",
                "tabla_dimension": "tbl_pres_unidades",
                "campo_nombre": "unidad",
                "grupo": "Precio"
            },
            "resumen": {
                "nombre": "Recurso / Material",
                "tipo": "texto",
                "tabla_relacion": "precio",
                "columna_bd": "resumen",
                "grupo": "Precio"
            },
            "coste": {
                "nombre": "Precio unitario",
                "tipo": "numerico",
                "tabla_relacion": "precio",
                "columna_bd": "coste",
                "formato": "moneda",
                "grupo": "Económico"
            },
            "naturaleza": {
                "nombre": "Naturaleza",
                "tipo": "dimension",
                "tabla_relacion": "precio",
                "columna_bd": "id_naturaleza",
                "tabla_dimension": "tbl_pres_naturaleza",
                "campo_nombre": "descripcion",
                "grupo": "Precio"
            },
            # Campos de tbl_part_presupuesto (mediciones)
            "cantidad": {
                "nombre": "Cantidad",
                "tipo": "numerico",
                "columna_bd": "cantidad",
                "formato": "decimal",
                "grupo": "Medición"
            },
            "coste_total": {
                "nombre": "Importe",
                "tipo": "calculado",
                "formula": "p.cantidad * precio.coste",
                "formato": "moneda",
                "grupo": "Económico"
            },
            # Campos de tbl_partes para agrupación
            "red": {
                "nombre": "Red",
                "tipo": "dimension",
                "tabla_relacion": "parte",
                "columna_bd": "red_id",
                "tabla_dimension": "dim_red",
                "campo_nombre": "descripcion",
                "grupo": "Parte"
            },
            "tipo_trabajo": {
                "nombre": "Tipo de Trabajo",
                "tipo": "dimension",
                "tabla_relacion": "parte",
                "columna_bd": "tipo_trabajo_id",
                "tabla_dimension": "dim_tipo_trabajo",
                "campo_nombre": "descripcion",
                "grupo": "Parte"
            },
            "cod": {
                "nombre": "COD",
                "tipo": "dimension",
                "tabla_relacion": "parte",
                "columna_bd": "cod_id",
                "tabla_dimension": "dim_cod",
                "campo_nombre": "descripcion",
                "grupo": "Parte"
            },
            "comarca": {
                "nombre": "Comarca",
                "tipo": "dimension",
                "tabla_relacion": "parte",
                "columna_bd": "comarca_id",
                "tabla_dimension": "dim_comarcas",
                "campo_nombre": "descripcion",
                "grupo": "Parte"
            },
            "municipio": {
                "nombre": "Municipio",
                "tipo": "dimension",
                "tabla_relacion": "parte",
                "columna_bd": "municipio_id",
                "tabla_dimension": "dim_municipios",
                "campo_nombre": "descripcion",
                "grupo": "Parte"
            },
            "mes": {
                "nombre": "Mes",
                "tipo": "calculado",
                "tabla_relacion": "parte",
                "formula": "DATE_FORMAT(parte.fecha_inicio, '%Y-%m')",
                "grupo": "Parte"
            },
            "año": {
                "nombre": "Año",
                "tipo": "calculado",
                "tabla_relacion": "parte",
                "formula": "YEAR(parte.fecha_inicio)",
                "grupo": "Parte"
            }
        },

        "filtros": {
            "codigo": {
                "campo": "codigo",
                "tipo": "texto",
                "operadores": ["Contiene", "Empieza con"]
            },
            "resumen": {
                "campo": "resumen",
                "tipo": "texto",
                "operadores": ["Contiene", "Empieza con"]
            },
            "red": {
                "campo": "red",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_red"
            },
            "tipo_trabajo": {
                "campo": "tipo_trabajo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_tipo_trabajo"
            },
            "cod": {
                "campo": "cod",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_cod"
            },
            "comarca": {
                "campo": "comarca",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_comarcas"
            },
            "municipio": {
                "campo": "municipio",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_municipios"
            },
            "naturaleza": {
                "campo": "naturaleza",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "tbl_pres_naturaleza"
            },
            "capitulo": {
                "campo": "capitulo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "tbl_pres_capitulos"
            }
        },

        "ordenaciones": [
            "codigo",
            "cantidad",
            "coste_total",
            "red",
            "tipo_trabajo",
            "municipio",
            "mes"
        ],

        "agrupaciones": {
            "campos_permitidos": [
                "red",
                "tipo_trabajo",
                "cod",
                "comarca",
                "municipio",
                "mes",
                "año",
                "naturaleza",
                "capitulo"
            ],
            "max_niveles": 2,
            "modo_default": "detalle"
        },

        "agregaciones": {},  # No permitir agregaciones

        "campos_default": [
            "codigo",
            "cantidad",
            "unidad",
            "resumen",
            "coste",
            "coste_total"
        ]
    },

    "Recursos Certificados": {
        "categoria": "📦 Recursos",
        "descripcion": "Listado de recursos/partidas certificadas con cantidad y coste total",
        "tabla_principal": "tbl_part_certificacion",
        "require_joins": ["tbl_pres_precios", "tbl_partes"],
        "formato_pdf": "vertical",  # Formato vertical para PDF
        "campos_fijos": True,  # No permite selección de campos
        "filtro_cantidad_cero": True,  # Excluir registros con cantidad = 0
        "filtro_certificada": True,  # Solo registros certificados
        "usar_agregacion_sql": True,  # Usar GROUP BY y SUM en SQL

        "campos": {
            # Campos de tbl_pres_precios (tabla de precios)
            "capitulo": {
                "nombre": "Capítulo",
                "tipo": "dimension",
                "tabla_relacion": "precio",
                "columna_bd": "id_capitulo",
                "tabla_dimension": "tbl_pres_capitulos",
                "campo_nombre": "descripcion",
                "grupo": "Precio"
            },
            "codigo": {
                "nombre": "Código",
                "tipo": "texto",
                "tabla_relacion": "precio",
                "columna_bd": "codigo",
                "grupo": "Precio"
            },
            "unidad": {
                "nombre": "Ud.",
                "tipo": "dimension",
                "tabla_relacion": "precio",
                "columna_bd": "id_unidades",
                "tabla_dimension": "tbl_pres_unidades",
                "campo_nombre": "unidad",
                "grupo": "Precio"
            },
            "resumen": {
                "nombre": "Recurso / Material",
                "tipo": "texto",
                "tabla_relacion": "precio",
                "columna_bd": "resumen",
                "grupo": "Precio"
            },
            "coste": {
                "nombre": "Precio unitario",
                "tipo": "numerico",
                "tabla_relacion": "precio",
                "columna_bd": "coste",
                "formato": "moneda",
                "grupo": "Económico"
            },
            "naturaleza": {
                "nombre": "Naturaleza",
                "tipo": "dimension",
                "tabla_relacion": "precio",
                "columna_bd": "id_naturaleza",
                "tabla_dimension": "tbl_pres_naturaleza",
                "campo_nombre": "descripcion",
                "grupo": "Precio"
            },
            # Campos de tbl_part_certificacion (mediciones)
            "cantidad": {
                "nombre": "Cantidad",
                "tipo": "numerico",
                "columna_bd": "cantidad_cert",
                "formato": "decimal",
                "grupo": "Medición"
            },
            "coste_total": {
                "nombre": "Importe",
                "tipo": "calculado",
                "formula": "p.cantidad_cert * precio.coste",
                "formato": "moneda",
                "grupo": "Económico"
            },
            # Campos de tbl_partes para agrupación
            "red": {
                "nombre": "Red",
                "tipo": "dimension",
                "tabla_relacion": "parte",
                "columna_bd": "red_id",
                "tabla_dimension": "dim_red",
                "campo_nombre": "descripcion",
                "grupo": "Parte"
            },
            "tipo_trabajo": {
                "nombre": "Tipo de Trabajo",
                "tipo": "dimension",
                "tabla_relacion": "parte",
                "columna_bd": "tipo_trabajo_id",
                "tabla_dimension": "dim_tipo_trabajo",
                "campo_nombre": "descripcion",
                "grupo": "Parte"
            },
            "cod": {
                "nombre": "COD",
                "tipo": "dimension",
                "tabla_relacion": "parte",
                "columna_bd": "cod_id",
                "tabla_dimension": "dim_cod",
                "campo_nombre": "descripcion",
                "grupo": "Parte"
            },
            "comarca": {
                "nombre": "Comarca",
                "tipo": "dimension",
                "tabla_relacion": "parte",
                "columna_bd": "comarca_id",
                "tabla_dimension": "dim_comarcas",
                "campo_nombre": "descripcion",
                "grupo": "Parte"
            },
            "municipio": {
                "nombre": "Municipio",
                "tipo": "dimension",
                "tabla_relacion": "parte",
                "columna_bd": "municipio_id",
                "tabla_dimension": "dim_municipios",
                "campo_nombre": "descripcion",
                "grupo": "Parte"
            },
            "mes": {
                "nombre": "Mes",
                "tipo": "calculado",
                "tabla_relacion": "parte",
                "formula": "DATE_FORMAT(parte.fecha_inicio, '%Y-%m')",
                "grupo": "Parte"
            },
            "año": {
                "nombre": "Año",
                "tipo": "calculado",
                "tabla_relacion": "parte",
                "formula": "YEAR(parte.fecha_inicio)",
                "grupo": "Parte"
            }
        },

        "filtros": {
            "codigo": {
                "campo": "codigo",
                "tipo": "texto",
                "operadores": ["Contiene", "Empieza con"]
            },
            "resumen": {
                "campo": "resumen",
                "tipo": "texto",
                "operadores": ["Contiene", "Empieza con"]
            },
            "red": {
                "campo": "red",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_red"
            },
            "tipo_trabajo": {
                "campo": "tipo_trabajo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_tipo_trabajo"
            },
            "cod": {
                "campo": "cod",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_cod"
            },
            "comarca": {
                "campo": "comarca",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_comarcas"
            },
            "municipio": {
                "campo": "municipio",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_municipios"
            },
            "naturaleza": {
                "campo": "naturaleza",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "tbl_pres_naturaleza"
            },
            "capitulo": {
                "campo": "capitulo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "tbl_pres_capitulos"
            }
        },

        "ordenaciones": [
            "codigo",
            "cantidad",
            "coste_total",
            "red",
            "tipo_trabajo",
            "municipio",
            "mes"
        ],

        "agrupaciones": {
            "campos_permitidos": [
                "red",
                "tipo_trabajo",
                "cod",
                "comarca",
                "municipio",
                "mes",
                "año",
                "naturaleza",
                "capitulo"
            ],
            "max_niveles": 2,
            "modo_default": "detalle"
        },

        "agregaciones": {},  # No permitir agregaciones

        "campos_default": [
            "codigo",
            "cantidad",
            "unidad",
            "resumen",
            "coste",
            "coste_total"
        ]
    },

    "Recursos Pendientes": {
        "categoria": "📦 Recursos",
        "descripcion": "Listado de recursos/partidas pendientes de certificar (diferencia entre presupuesto y certificado)",
        "tabla_principal": "tbl_part_presupuesto",
        "require_joins": ["tbl_pres_precios", "tbl_partes"],
        "formato_pdf": "vertical",  # Formato vertical para PDF
        "campos_fijos": True,  # No permite selección de campos
        "filtro_cantidad_cero": True,  # Excluir registros con cantidad = 0
        "usar_agregacion_sql": True,  # Usar GROUP BY y SUM en SQL

        "campos": {
            # Campos de tbl_pres_precios (tabla de precios)
            "capitulo": {
                "nombre": "Capítulo",
                "tipo": "dimension",
                "tabla_relacion": "precio",
                "columna_bd": "id_capitulo",
                "tabla_dimension": "tbl_pres_capitulos",
                "campo_nombre": "descripcion",
                "grupo": "Precio"
            },
            "codigo": {
                "nombre": "Código",
                "tipo": "texto",
                "tabla_relacion": "precio",
                "columna_bd": "codigo",
                "grupo": "Precio"
            },
            "unidad": {
                "nombre": "Ud.",
                "tipo": "dimension",
                "tabla_relacion": "precio",
                "columna_bd": "id_unidades",
                "tabla_dimension": "tbl_pres_unidades",
                "campo_nombre": "unidad",
                "grupo": "Precio"
            },
            "resumen": {
                "nombre": "Recurso / Material",
                "tipo": "texto",
                "tabla_relacion": "precio",
                "columna_bd": "resumen",
                "grupo": "Precio"
            },
            "coste": {
                "nombre": "Precio unitario",
                "tipo": "numerico",
                "tabla_relacion": "precio",
                "columna_bd": "coste",
                "formato": "moneda",
                "grupo": "Económico"
            },
            "naturaleza": {
                "nombre": "Naturaleza",
                "tipo": "dimension",
                "tabla_relacion": "precio",
                "columna_bd": "id_naturaleza",
                "tabla_dimension": "tbl_pres_naturaleza",
                "campo_nombre": "descripcion",
                "grupo": "Precio"
            },
            # Campos calculados: cantidad pendiente = presupuestada - certificada
            "cantidad": {
                "nombre": "Cantidad",
                "tipo": "calculado",
                "formula": "p.cantidad - COALESCE((SELECT pc.cantidad_cert FROM tbl_part_certificacion pc WHERE pc.parte_id = parte.id AND pc.precio_id = precio.id AND pc.certificada = 1), 0)",
                "formato": "decimal",
                "grupo": "Medición"
            },
            "coste_total": {
                "nombre": "Importe",
                "tipo": "calculado",
                "formula": "(p.cantidad * precio.coste) - COALESCE((SELECT pc.cantidad_cert * precio.coste FROM tbl_part_certificacion pc WHERE pc.parte_id = parte.id AND pc.precio_id = precio.id AND pc.certificada = 1), 0)",
                "formato": "moneda",
                "grupo": "Económico"
            },
            # Campos de tbl_partes para agrupación
            "red": {
                "nombre": "Red",
                "tipo": "dimension",
                "tabla_relacion": "parte",
                "columna_bd": "red_id",
                "tabla_dimension": "dim_red",
                "campo_nombre": "descripcion",
                "grupo": "Parte"
            },
            "tipo_trabajo": {
                "nombre": "Tipo de Trabajo",
                "tipo": "dimension",
                "tabla_relacion": "parte",
                "columna_bd": "tipo_trabajo_id",
                "tabla_dimension": "dim_tipo_trabajo",
                "campo_nombre": "descripcion",
                "grupo": "Parte"
            },
            "cod": {
                "nombre": "COD",
                "tipo": "dimension",
                "tabla_relacion": "parte",
                "columna_bd": "cod_id",
                "tabla_dimension": "dim_cod",
                "campo_nombre": "descripcion",
                "grupo": "Parte"
            },
            "comarca": {
                "nombre": "Comarca",
                "tipo": "dimension",
                "tabla_relacion": "parte",
                "columna_bd": "comarca_id",
                "tabla_dimension": "dim_comarcas",
                "campo_nombre": "descripcion",
                "grupo": "Parte"
            },
            "municipio": {
                "nombre": "Municipio",
                "tipo": "dimension",
                "tabla_relacion": "parte",
                "columna_bd": "municipio_id",
                "tabla_dimension": "dim_municipios",
                "campo_nombre": "descripcion",
                "grupo": "Parte"
            },
            "mes": {
                "nombre": "Mes",
                "tipo": "calculado",
                "tabla_relacion": "parte",
                "formula": "DATE_FORMAT(parte.fecha_inicio, '%Y-%m')",
                "grupo": "Parte"
            },
            "año": {
                "nombre": "Año",
                "tipo": "calculado",
                "tabla_relacion": "parte",
                "formula": "YEAR(parte.fecha_inicio)",
                "grupo": "Parte"
            }
        },

        "filtros": {
            "codigo": {
                "campo": "codigo",
                "tipo": "texto",
                "operadores": ["Contiene", "Empieza con"]
            },
            "resumen": {
                "campo": "resumen",
                "tipo": "texto",
                "operadores": ["Contiene", "Empieza con"]
            },
            "red": {
                "campo": "red",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_red"
            },
            "tipo_trabajo": {
                "campo": "tipo_trabajo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_tipo_trabajo"
            },
            "cod": {
                "campo": "cod",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_cod"
            },
            "comarca": {
                "campo": "comarca",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_comarcas"
            },
            "municipio": {
                "campo": "municipio",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_municipios"
            },
            "naturaleza": {
                "campo": "naturaleza",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "tbl_pres_naturaleza"
            },
            "capitulo": {
                "campo": "capitulo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "tbl_pres_capitulos"
            }
        },

        "ordenaciones": [
            "codigo",
            "cantidad",
            "coste_total",
            "red",
            "tipo_trabajo",
            "municipio",
            "mes"
        ],

        "agrupaciones": {
            "campos_permitidos": [
                "red",
                "tipo_trabajo",
                "cod",
                "comarca",
                "municipio",
                "mes",
                "año",
                "naturaleza",
                "capitulo"
            ],
            "max_niveles": 2,
            "modo_default": "detalle"
        },

        "agregaciones": {},  # No permitir agregaciones

        "campos_default": [
            "codigo",
            "cantidad",
            "unidad",
            "resumen",
            "coste",
            "coste_total"
        ]
    },

    # ============================================================
    # CATEGORÍA: PRESUPUESTOS
    # ============================================================

    "Contrato": {
        "categoria": "💰 Presupuestos",
        "descripcion": "Presupuesto de contrato completo con todas las partidas ordenadas por capítulos, con medición, precio unitario e importe contratado.",
        "tabla_principal": "tbl_pres_precios",

        "campos": {
            "capitulo": {
                "nombre": "Capítulo",
                "tipo": "dimension",
                "columna_bd": "id_capitulo",
                "tabla_dimension": "tbl_pres_capitulos",
                "campo_nombre": "descripcion",
                "grupo": "Ordenación"
            },
            "codigo": {
                "nombre": "Código",
                "tipo": "texto",
                "columna_bd": "codigo",
                "grupo": "Información Básica"
            },
            "unidad": {
                "nombre": "Ud",
                "tipo": "dimension",
                "columna_bd": "id_unidades",
                "tabla_dimension": "tbl_pres_unidades",
                "campo_nombre": "unidad",
                "grupo": "Información Básica"
            },
            "resumen": {
                "nombre": "Recurso/Material",
                "tipo": "texto",
                "columna_bd": "resumen",
                "grupo": "Información Básica"
            },
            "precio_unitario": {
                "nombre": "Precio Unitario",
                "tipo": "numerico",
                "columna_bd": "coste",
                "formato": "moneda",
                "grupo": "Económico"
            },
            "medicion_contrato": {
                "nombre": "Medición",
                "tipo": "calculado",
                "formula": "COALESCE((SELECT SUM(pp.cantidad) FROM tbl_part_presupuesto pp WHERE pp.precio_id = pr.id), 0)",
                "formato": "decimal",
                "grupo": "Contrato"
            },
            "importe_contratado": {
                "nombre": "Importe Contratado",
                "tipo": "calculado",
                "formula": "COALESCE((SELECT SUM(pp.cantidad * pp.precio_unit) FROM tbl_part_presupuesto pp WHERE pp.precio_id = pr.id), 0)",
                "formato": "moneda",
                "grupo": "Contrato"
            }
        },

        "filtros": {
            "capitulo": {
                "campo": "capitulo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "tbl_pres_capitulos"
            }
        },

        "ordenaciones": [
            "capitulo",
            "codigo"
        ],

        "agrupaciones": {
            "campos_permitidos": [
                "capitulo"
            ],
            "max_niveles": 1,
            "modo_default": "detalle"
        },

        "agregaciones": {
            "COUNT": {
                "nombre": "Contar registros",
                "aplicable_a": ["*"],
                "tipo_resultado": "numerico",
                "formato": "entero"
            },
            "SUM": {
                "nombre": "Suma",
                "aplicable_a": ["numerico", "calculado"],
                "tipo_resultado": "numerico",
                "formato": "original"
            }
        },

        "campos_default": [
            "capitulo",
            "codigo",
            "unidad",
            "resumen",
            "precio_unitario",
            "medicion_contrato",
            "importe_contratado"
        ]
    },

    "Presupuesto Detallado": {
        "categoria": "💰 Presupuestos",
        "descripcion": "Relación de partes con sus mediciones presupuestadas. Subtotal por parte y total general.",
        "tabla_principal": "tbl_partes",
        "require_joins": ["tbl_part_presupuesto", "tbl_pres_precios", "tbl_pres_unidades"],
        "formato_pdf": "vertical",
        "tipo_especial": "ordenes_con_recursos",
        "campos_fijos": True,
        "subtabla_recursos": True,

        # Campos de la ORDEN DE TRABAJO (cabecera)
        "campos_orden": {
            "codigo": {
                "nombre": "",
                "tipo": "texto",
                "columna_bd": "codigo",
                "grupo": "Orden",
                "posicion": "izquierda_primera_fila"
            },
            "titulo": {
                "nombre": "",
                "tipo": "texto",
                "columna_bd": "titulo",
                "grupo": "Orden",
                "posicion": "derecha_primera_fila"
            },
            "fecha_fin": {
                "nombre": "FECHA:",
                "tipo": "fecha",
                "columna_bd": "fecha_fin",
                "grupo": "Orden"
            },
            "municipio": {
                "nombre": "LOCALIZACIÓN:",
                "tipo": "dimension",
                "columna_bd": "municipio_id",
                "tabla_dimension": "dim_municipios",
                "campo_nombre": "nombre",
                "grupo": "Orden",
                "combinar_con": "localizacion"
            },
            "localizacion": {
                "nombre": "",
                "tipo": "texto",
                "columna_bd": "localizacion",
                "grupo": "Orden",
                "parte_de": "municipio"
            },
            "latitud": {
                "nombre": "LATITUD:",
                "tipo": "numerico",
                "columna_bd": "latitud",
                "formato": "decimal",
                "grupo": "Orden",
                "misma_fila_que": "longitud"
            },
            "longitud": {
                "nombre": "LONGITUD:",
                "tipo": "numerico",
                "columna_bd": "longitud",
                "formato": "decimal",
                "grupo": "Orden",
                "misma_fila_que": "latitud"
            }
        },

        # Campos de la TABLA DE RECURSOS
        "campos_recursos": {
            "codigo": {
                "nombre": "Código",
                "tipo": "texto",
                "tabla_relacion": "precio",
                "columna_bd": "codigo",
                "grupo": "Recurso"
            },
            "cantidad": {
                "nombre": "Cantidad",
                "tipo": "numerico",
                "columna_bd": "cantidad",
                "formato": "decimal",
                "grupo": "Recurso"
            },
            "unidad": {
                "nombre": "Ud.",
                "tipo": "dimension",
                "tabla_relacion": "precio",
                "columna_bd": "id_unidades",
                "tabla_dimension": "tbl_pres_unidades",
                "campo_nombre": "unidad",
                "grupo": "Recurso"
            },
            "resumen": {
                "nombre": "Recurso / Material",
                "tipo": "texto",
                "tabla_relacion": "precio",
                "columna_bd": "resumen",
                "grupo": "Recurso"
            },
            "coste": {
                "nombre": "Precio unitario",
                "tipo": "numerico",
                "tabla_relacion": "precio",
                "columna_bd": "coste",
                "formato": "moneda",
                "grupo": "Recurso"
            },
            "coste_total": {
                "nombre": "Importe",
                "tipo": "calculado",
                "formula": "pres.cantidad * precio.coste",
                "formato": "moneda",
                "grupo": "Recurso"
            }
        },

        # Campos para FILTRADO Y AGRUPACIÓN
        "campos": {
            "mes": {
                "nombre": "Mes",
                "tipo": "calculado",
                "formula": "DATE_FORMAT(p.fecha_inicio, '%Y-%m')",
                "grupo": "Temporal"
            },
            "año": {
                "nombre": "Año",
                "tipo": "calculado",
                "formula": "YEAR(p.fecha_inicio)",
                "grupo": "Temporal"
            },
            "codigo": {
                "nombre": "Código",
                "tipo": "texto",
                "columna_bd": "codigo",
                "grupo": "Información Básica"
            },
            "titulo": {
                "nombre": "Título",
                "tipo": "texto",
                "columna_bd": "titulo",
                "grupo": "Información Básica"
            },
            "estado": {
                "nombre": "Estado",
                "tipo": "texto",
                "columna_bd": "estado",
                "grupo": "Información Básica"
            },
            "red": {
                "nombre": "Red",
                "tipo": "dimension",
                "columna_bd": "red_id",
                "tabla_dimension": "dim_red",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "tipo_trabajo": {
                "nombre": "Tipo de Trabajo",
                "tipo": "dimension",
                "columna_bd": "tipo_trabajo_id",
                "tabla_dimension": "dim_tipo_trabajo",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "codigo_trabajo": {
                "nombre": "Código de Trabajo",
                "tipo": "dimension",
                "columna_bd": "cod_trabajo_id",
                "tabla_dimension": "dim_codigo_trabajo",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "provincia": {
                "nombre": "Provincia",
                "tipo": "dimension",
                "columna_bd": "provincia_id",
                "tabla_dimension": "dim_provincias",
                "campo_nombre": "nombre",
                "grupo": "Ubicación Geográfica"
            },
            "comarca": {
                "nombre": "Comarca",
                "tipo": "dimension",
                "columna_bd": "comarca_id",
                "tabla_dimension": "dim_comarcas",
                "campo_nombre": "nombre",
                "grupo": "Ubicación Geográfica"
            },
            "municipio": {
                "nombre": "Municipio",
                "tipo": "dimension",
                "columna_bd": "municipio_id",
                "tabla_dimension": "dim_municipios",
                "campo_nombre": "nombre",
                "grupo": "Ubicación Geográfica"
            },
            "concejo": {
                "nombre": "Concejo",
                "tipo": "dimension",
                "columna_bd": "concejo_id",
                "tabla_dimension": "dim_concejos",
                "campo_nombre": "nombre",
                "grupo": "Ubicación Geográfica"
            },
            "trabajadores": {
                "nombre": "Trabajadores",
                "tipo": "texto",
                "columna_bd": "trabajadores",
                "grupo": "Recursos Humanos"
            },
            "tipo_rep": {
                "nombre": "Tipo de Reparación",
                "tipo": "dimension",
                "columna_bd": "tipo_rep_id",
                "tabla_dimension": "dim_tipos_rep",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "fecha_inicio": {
                "nombre": "Fecha Inicio",
                "tipo": "fecha",
                "columna_bd": "fecha_inicio",
                "grupo": "Fechas"
            },
            "fecha_fin": {
                "nombre": "Fecha Fin",
                "tipo": "fecha",
                "columna_bd": "fecha_fin",
                "grupo": "Fechas"
            },
            "finalizada": {
                "nombre": "Finalizada",
                "tipo": "booleano",
                "columna_bd": "finalizada",
                "grupo": "Información Básica"
            }
        },

        "filtros": {
            "mes": {
                "campo": "mes",
                "tipo": "mes_anio",
                "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
            },
            "año": {
                "campo": "año",
                "tipo": "anio",
                "operadores": ["Igual a", "Mayor a", "Menor a", "Entre"]
            },
            "estado": {
                "campo": "estado",
                "tipo": "select",
                "operadores": ["Igual a", "Diferente de"],
                "valores": ["Pendiente", "En curso", "Finalizado"]
            },
            "red": {
                "campo": "red",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_red"
            },
            "tipo_trabajo": {
                "campo": "tipo_trabajo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_tipo_trabajo"
            },
            "codigo_trabajo": {
                "campo": "codigo_trabajo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_codigo_trabajo"
            },
            "provincia": {
                "campo": "provincia",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_provincias"
            },
            "comarca": {
                "campo": "comarca",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_comarcas"
            },
            "municipio": {
                "campo": "municipio",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_municipios"
            },
            "concejo": {
                "campo": "concejo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_concejos"
            },
            "trabajadores": {
                "campo": "trabajadores",
                "tipo": "texto",
                "operadores": ["Igual a", "Diferente de", "Contiene", "No contiene"]
            },
            "tipo_rep": {
                "campo": "tipo_rep",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_tipos_rep"
            },
            "fecha_inicio": {
                "campo": "fecha_inicio",
                "tipo": "fecha",
                "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
            },
            "fecha_fin": {
                "campo": "fecha_fin",
                "tipo": "fecha",
                "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
            },
            "finalizada": {
                "campo": "finalizada",
                "tipo": "booleano",
                "operadores": ["Sí", "No"]
            }
        },

        "ordenaciones": [
            "mes",
            "año",
            "estado",
            "red",
            "tipo_trabajo",
            "provincia",
            "comarca",
            "municipio",
            "fecha_inicio",
            "fecha_fin",
            "tipo_rep"
        ],

        "agrupaciones": {
            "campos_permitidos": [
                "mes",
                "año",
                "estado",
                "red",
                "tipo_trabajo",
                "codigo_trabajo",
                "tipo_rep",
                "provincia",
                "comarca",
                "municipio",
                "trabajadores"
            ],
            "max_niveles": 3,
            "modo_default": "detalle"
        },

        # No se usan agregaciones
        "agregaciones": {},

        # Campos que siempre se muestran en la cabecera de cada orden
        "campos_orden_default": [
            "codigo",
            "titulo",
            "fecha_fin",
            "municipio",
            "localizacion",
            "latitud",
            "longitud"
        ],

        # Campos que siempre se muestran en la tabla de recursos
        "campos_recursos_default": [
            "codigo",
            "cantidad",
            "unidad",
            "resumen",
            "coste",
            "coste_total"
        ]
    },

    "Presupuesto Resumen": {
        "categoria": "💰 Presupuestos",
        "descripcion": "Resumen de presupuesto por partes con cálculo de PEM, Gastos Generales y Beneficio Industrial.",
        "tabla_principal": "tbl_partes",
        "formato_pdf": "vertical",
        "campos_fijos": True,
        "usar_agregacion_sql": True,  # Usar agregación SQL para calcular subtotales automáticamente
        "calcular_resumen_economico": True,  # Flag para activar cálculos PEM, GG, BI
        "porcentaje_gastos_generales": 8,    # 8%
        "porcentaje_beneficio": 3,            # 3%

        "campos": {
            "mes": {
                "nombre": "Mes",
                "tipo": "calculado",
                "formula": "DATE_FORMAT(p.fecha_inicio, '%Y-%m')",
                "grupo": "Temporal"
            },
            "año": {
                "nombre": "Año",
                "tipo": "calculado",
                "formula": "YEAR(p.fecha_inicio)",
                "grupo": "Temporal"
            },
            "codigo": {
                "nombre": "Código",
                "tipo": "texto",
                "columna_bd": "codigo",
                "grupo": "Información Básica"
            },
            "fecha": {
                "nombre": "Fecha",
                "tipo": "fecha",
                "columna_bd": "fecha_fin",
                "grupo": "Información Básica"
            },
            "titulo": {
                "nombre": "Título",
                "tipo": "texto",
                "columna_bd": "titulo",
                "grupo": "Información Básica"
            },
            "estado": {
                "nombre": "Estado",
                "tipo": "texto",
                "columna_bd": "estado",
                "grupo": "Información Básica"
            },
            "red": {
                "nombre": "Red",
                "tipo": "dimension",
                "columna_bd": "red_id",
                "tabla_dimension": "dim_red",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "tipo_trabajo": {
                "nombre": "Tipo de Trabajo",
                "tipo": "dimension",
                "columna_bd": "tipo_trabajo_id",
                "tabla_dimension": "dim_tipo_trabajo",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "codigo_trabajo": {
                "nombre": "Código de Trabajo",
                "tipo": "dimension",
                "columna_bd": "cod_trabajo_id",
                "tabla_dimension": "dim_codigo_trabajo",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "provincia": {
                "nombre": "Provincia",
                "tipo": "dimension",
                "columna_bd": "provincia_id",
                "tabla_dimension": "dim_provincias",
                "campo_nombre": "nombre",
                "grupo": "Ubicación Geográfica"
            },
            "comarca": {
                "nombre": "Comarca",
                "tipo": "dimension",
                "columna_bd": "comarca_id",
                "tabla_dimension": "dim_comarcas",
                "campo_nombre": "nombre",
                "grupo": "Ubicación Geográfica"
            },
            "municipio": {
                "nombre": "Municipio",
                "tipo": "dimension",
                "columna_bd": "municipio_id",
                "tabla_dimension": "dim_municipios",
                "campo_nombre": "nombre",
                "grupo": "Ubicación Geográfica"
            },
            "concejo": {
                "nombre": "Concejo",
                "tipo": "dimension",
                "columna_bd": "concejo_id",
                "tabla_dimension": "dim_concejos",
                "campo_nombre": "nombre",
                "grupo": "Ubicación Geográfica"
            },
            "localizacion": {
                "nombre": "Localización",
                "tipo": "texto",
                "columna_bd": "localizacion",
                "grupo": "Ubicación Geográfica"
            },
            "trabajadores": {
                "nombre": "Trabajadores",
                "tipo": "texto",
                "columna_bd": "trabajadores",
                "grupo": "Recursos Humanos"
            },
            "tipo_rep": {
                "nombre": "Tipo de Reparación",
                "tipo": "dimension",
                "columna_bd": "tipo_rep_id",
                "tabla_dimension": "dim_tipos_rep",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "fecha_inicio": {
                "nombre": "Fecha Inicio",
                "tipo": "fecha",
                "columna_bd": "fecha_inicio",
                "grupo": "Fechas"
            },
            "fecha_fin": {
                "nombre": "Fecha Fin",
                "tipo": "fecha",
                "columna_bd": "fecha_fin",
                "grupo": "Fechas"
            },
            "importe": {
                "nombre": "Importe",
                "tipo": "calculado",
                "formula": "COALESCE((SELECT SUM(pp.cantidad * pp.precio_unit) FROM tbl_part_presupuesto pp WHERE pp.parte_id = p.id), 0)",
                "formato": "moneda",
                "grupo": "Económico"
            },
            "finalizada": {
                "nombre": "Finalizada",
                "tipo": "booleano",
                "columna_bd": "finalizada",
                "grupo": "Información Básica"
            }
        },

        "filtros": {
            "mes": {
                "campo": "mes",
                "tipo": "mes_anio",
                "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
            },
            "año": {
                "campo": "año",
                "tipo": "anio",
                "operadores": ["Igual a", "Mayor a", "Menor a", "Entre"]
            },
            "estado": {
                "campo": "estado",
                "tipo": "select",
                "operadores": ["Igual a", "Diferente de"],
                "valores": ["Pendiente", "En curso", "Finalizado"]
            },
            "red": {
                "campo": "red",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_red"
            },
            "tipo_trabajo": {
                "campo": "tipo_trabajo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_tipo_trabajo"
            },
            "codigo_trabajo": {
                "campo": "codigo_trabajo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_codigo_trabajo"
            },
            "provincia": {
                "campo": "provincia",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_provincias"
            },
            "comarca": {
                "campo": "comarca",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_comarcas"
            },
            "municipio": {
                "campo": "municipio",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_municipios"
            },
            "concejo": {
                "campo": "concejo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_concejos"
            },
            "trabajadores": {
                "campo": "trabajadores",
                "tipo": "texto",
                "operadores": ["Igual a", "Diferente de", "Contiene", "No contiene"]
            },
            "tipo_rep": {
                "campo": "tipo_rep",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_tipos_rep"
            },
            "fecha_inicio": {
                "campo": "fecha_inicio",
                "tipo": "fecha",
                "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
            },
            "fecha_fin": {
                "campo": "fecha_fin",
                "tipo": "fecha",
                "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
            },
            "finalizada": {
                "campo": "finalizada",
                "tipo": "booleano",
                "operadores": ["Sí", "No"]
            }
        },

        "ordenaciones": [
            "mes",
            "año",
            "estado",
            "red",
            "tipo_trabajo",
            "provincia",
            "comarca",
            "municipio",
            "fecha_inicio",
            "fecha_fin",
            "tipo_rep"
        ],

        "agrupaciones": {
            "campos_permitidos": [
                "mes",
                "año",
                "estado",
                "red",
                "tipo_trabajo",
                "codigo_trabajo",
                "tipo_rep",
                "provincia",
                "comarca",
                "municipio",
                "trabajadores"
            ],
            "max_niveles": 3,
            "modo_default": "detalle"
        },

        "agregaciones": {},  # No permitir agregaciones

        "campos_default": [
            "codigo",
            "titulo",
            "fecha",
            "municipio",
            "localizacion",
            "importe"
        ]
    },

    # ============================================================
    # CATEGORÍA: CERTIFICACIONES
    # ============================================================

    "Certificación Detallado": {
        "categoria": "✅ Certificaciones",
        "descripcion": "Relación de partes con sus mediciones certificadas. Subtotal por parte y total general.",
        "tabla_principal": "tbl_partes",
        "require_joins": ["tbl_part_certificacion", "tbl_pres_precios", "tbl_pres_unidades"],
        "formato_pdf": "vertical",
        "tipo_especial": "ordenes_con_recursos",
        "campos_fijos": True,
        "subtabla_recursos": True,

        # Campos de la ORDEN DE TRABAJO (cabecera)
        "campos_orden": {
            "codigo": {
                "nombre": "",
                "tipo": "texto",
                "columna_bd": "codigo",
                "grupo": "Orden",
                "posicion": "izquierda_primera_fila"
            },
            "titulo": {
                "nombre": "",
                "tipo": "texto",
                "columna_bd": "titulo",
                "grupo": "Orden",
                "posicion": "derecha_primera_fila"
            },
            "fecha_fin": {
                "nombre": "FECHA:",
                "tipo": "fecha",
                "columna_bd": "fecha_fin",
                "grupo": "Orden"
            },
            "municipio": {
                "nombre": "LOCALIZACIÓN:",
                "tipo": "dimension",
                "columna_bd": "municipio_id",
                "tabla_dimension": "dim_municipios",
                "campo_nombre": "nombre",
                "grupo": "Orden",
                "combinar_con": "localizacion"
            },
            "localizacion": {
                "nombre": "",
                "tipo": "texto",
                "columna_bd": "localizacion",
                "grupo": "Orden",
                "parte_de": "municipio"
            },
            "latitud": {
                "nombre": "LATITUD:",
                "tipo": "numerico",
                "columna_bd": "latitud",
                "formato": "decimal",
                "grupo": "Orden",
                "misma_fila_que": "longitud"
            },
            "longitud": {
                "nombre": "LONGITUD:",
                "tipo": "numerico",
                "columna_bd": "longitud",
                "formato": "decimal",
                "grupo": "Orden",
                "misma_fila_que": "latitud"
            }
        },

        # Campos de la TABLA DE RECURSOS (certificados)
        "campos_recursos": {
            "codigo": {
                "nombre": "Código",
                "tipo": "texto",
                "tabla_relacion": "precio",
                "columna_bd": "codigo",
                "grupo": "Recurso"
            },
            "cantidad": {
                "nombre": "Cantidad",
                "tipo": "numerico",
                "columna_bd": "cantidad_cert",
                "formato": "decimal",
                "grupo": "Recurso"
            },
            "unidad": {
                "nombre": "Ud.",
                "tipo": "dimension",
                "tabla_relacion": "precio",
                "columna_bd": "id_unidades",
                "tabla_dimension": "tbl_pres_unidades",
                "campo_nombre": "unidad",
                "grupo": "Recurso"
            },
            "resumen": {
                "nombre": "Recurso / Material",
                "tipo": "texto",
                "tabla_relacion": "precio",
                "columna_bd": "resumen",
                "grupo": "Recurso"
            },
            "coste": {
                "nombre": "Precio unitario",
                "tipo": "numerico",
                "tabla_relacion": "precio",
                "columna_bd": "coste",
                "formato": "moneda",
                "grupo": "Recurso"
            },
            "coste_total": {
                "nombre": "Importe",
                "tipo": "calculado",
                "formula": "cert.cantidad_cert * precio.coste",
                "formato": "moneda",
                "grupo": "Recurso"
            }
        },

        # Campos para FILTRADO Y AGRUPACIÓN
        "campos": {
            "mes": {
                "nombre": "Mes",
                "tipo": "calculado",
                "formula": "DATE_FORMAT(p.fecha_inicio, '%Y-%m')",
                "grupo": "Temporal"
            },
            "año": {
                "nombre": "Año",
                "tipo": "calculado",
                "formula": "YEAR(p.fecha_inicio)",
                "grupo": "Temporal"
            },
            "codigo": {
                "nombre": "Código",
                "tipo": "texto",
                "columna_bd": "codigo",
                "grupo": "Información Básica"
            },
            "titulo": {
                "nombre": "Título",
                "tipo": "texto",
                "columna_bd": "titulo",
                "grupo": "Información Básica"
            },
            "estado": {
                "nombre": "Estado",
                "tipo": "texto",
                "columna_bd": "estado",
                "grupo": "Información Básica"
            },
            "red": {
                "nombre": "Red",
                "tipo": "dimension",
                "columna_bd": "red_id",
                "tabla_dimension": "dim_red",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "tipo_trabajo": {
                "nombre": "Tipo de Trabajo",
                "tipo": "dimension",
                "columna_bd": "tipo_trabajo_id",
                "tabla_dimension": "dim_tipo_trabajo",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "codigo_trabajo": {
                "nombre": "Código de Trabajo",
                "tipo": "dimension",
                "columna_bd": "cod_trabajo_id",
                "tabla_dimension": "dim_codigo_trabajo",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "provincia": {
                "nombre": "Provincia",
                "tipo": "dimension",
                "columna_bd": "provincia_id",
                "tabla_dimension": "dim_provincias",
                "campo_nombre": "nombre",
                "grupo": "Ubicación Geográfica"
            },
            "comarca": {
                "nombre": "Comarca",
                "tipo": "dimension",
                "columna_bd": "comarca_id",
                "tabla_dimension": "dim_comarcas",
                "campo_nombre": "nombre",
                "grupo": "Ubicación Geográfica"
            },
            "municipio": {
                "nombre": "Municipio",
                "tipo": "dimension",
                "columna_bd": "municipio_id",
                "tabla_dimension": "dim_municipios",
                "campo_nombre": "nombre",
                "grupo": "Ubicación Geográfica"
            },
            "concejo": {
                "nombre": "Concejo",
                "tipo": "dimension",
                "columna_bd": "concejo_id",
                "tabla_dimension": "dim_concejos",
                "campo_nombre": "nombre",
                "grupo": "Ubicación Geográfica"
            },
            "trabajadores": {
                "nombre": "Trabajadores",
                "tipo": "texto",
                "columna_bd": "trabajadores",
                "grupo": "Recursos Humanos"
            },
            "tipo_rep": {
                "nombre": "Tipo de Reparación",
                "tipo": "dimension",
                "columna_bd": "tipo_rep_id",
                "tabla_dimension": "dim_tipos_rep",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "fecha_inicio": {
                "nombre": "Fecha Inicio",
                "tipo": "fecha",
                "columna_bd": "fecha_inicio",
                "grupo": "Fechas"
            },
            "fecha_fin": {
                "nombre": "Fecha Fin",
                "tipo": "fecha",
                "columna_bd": "fecha_fin",
                "grupo": "Fechas"
            },
            "finalizada": {
                "nombre": "Finalizada",
                "tipo": "booleano",
                "columna_bd": "finalizada",
                "grupo": "Información Básica"
            }
        },

        "filtros": {
            "mes": {
                "campo": "mes",
                "tipo": "mes_anio",
                "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
            },
            "año": {
                "campo": "año",
                "tipo": "anio",
                "operadores": ["Igual a", "Mayor a", "Menor a", "Entre"]
            },
            "estado": {
                "campo": "estado",
                "tipo": "select",
                "operadores": ["Igual a", "Diferente de"],
                "valores": ["Pendiente", "En curso", "Finalizado"]
            },
            "red": {
                "campo": "red",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_red"
            },
            "tipo_trabajo": {
                "campo": "tipo_trabajo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_tipo_trabajo"
            },
            "codigo_trabajo": {
                "campo": "codigo_trabajo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_codigo_trabajo"
            },
            "provincia": {
                "campo": "provincia",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_provincias"
            },
            "comarca": {
                "campo": "comarca",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_comarcas"
            },
            "municipio": {
                "campo": "municipio",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_municipios"
            },
            "concejo": {
                "campo": "concejo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_concejos"
            },
            "trabajadores": {
                "campo": "trabajadores",
                "tipo": "texto",
                "operadores": ["Igual a", "Diferente de", "Contiene", "No contiene"]
            },
            "tipo_rep": {
                "campo": "tipo_rep",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_tipos_rep"
            },
            "fecha_inicio": {
                "campo": "fecha_inicio",
                "tipo": "fecha",
                "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
            },
            "fecha_fin": {
                "campo": "fecha_fin",
                "tipo": "fecha",
                "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
            },
            "finalizada": {
                "campo": "finalizada",
                "tipo": "booleano",
                "operadores": ["Sí", "No"]
            }
        },

        "ordenaciones": [
            "mes",
            "año",
            "estado",
            "red",
            "tipo_trabajo",
            "provincia",
            "comarca",
            "municipio",
            "fecha_inicio",
            "fecha_fin",
            "tipo_rep"
        ],

        "agrupaciones": {
            "campos_permitidos": [
                "mes",
                "año",
                "estado",
                "red",
                "tipo_trabajo",
                "codigo_trabajo",
                "tipo_rep",
                "provincia",
                "comarca",
                "municipio",
                "trabajadores"
            ],
            "max_niveles": 3,
            "modo_default": "detalle"
        },

        # No se usan agregaciones
        "agregaciones": {},

        # Campos que siempre se muestran en la cabecera de cada orden
        "campos_orden_default": [
            "codigo",
            "titulo",
            "fecha_fin",
            "municipio",
            "localizacion",
            "latitud",
            "longitud"
        ],

        # Campos que siempre se muestran en la tabla de recursos
        "campos_recursos_default": [
            "codigo",
            "cantidad",
            "unidad",
            "resumen",
            "coste",
            "coste_total"
        ]
    },

    "Certificación Resumen": {
        "categoria": "✅ Certificaciones",
        "descripcion": "Resumen de certificación por partes con cálculo de PEM, Gastos Generales y Beneficio Industrial.",
        "tabla_principal": "tbl_partes",
        "formato_pdf": "vertical",
        "campos_fijos": True,
        "usar_agregacion_sql": True,  # Usar agregación SQL para calcular subtotales automáticamente
        "calcular_resumen_economico": True,  # Flag para activar cálculos PEM, GG, BI
        "porcentaje_gastos_generales": 8,    # 8%
        "porcentaje_beneficio": 3,            # 3%
        "filtro_importe_cero": True,          # Excluir partes con importe = 0

        "campos": {
            "mes": {
                "nombre": "Mes",
                "tipo": "calculado",
                "formula": "DATE_FORMAT(p.fecha_inicio, '%Y-%m')",
                "grupo": "Temporal"
            },
            "año": {
                "nombre": "Año",
                "tipo": "calculado",
                "formula": "YEAR(p.fecha_inicio)",
                "grupo": "Temporal"
            },
            "codigo": {
                "nombre": "Código",
                "tipo": "texto",
                "columna_bd": "codigo",
                "grupo": "Información Básica"
            },
            "fecha": {
                "nombre": "Fecha",
                "tipo": "fecha",
                "columna_bd": "fecha_fin",
                "grupo": "Información Básica"
            },
            "titulo": {
                "nombre": "Título",
                "tipo": "texto",
                "columna_bd": "titulo",
                "grupo": "Información Básica"
            },
            "estado": {
                "nombre": "Estado",
                "tipo": "texto",
                "columna_bd": "estado",
                "grupo": "Información Básica"
            },
            "red": {
                "nombre": "Red",
                "tipo": "dimension",
                "columna_bd": "red_id",
                "tabla_dimension": "dim_red",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "tipo_trabajo": {
                "nombre": "Tipo de Trabajo",
                "tipo": "dimension",
                "columna_bd": "tipo_trabajo_id",
                "tabla_dimension": "dim_tipo_trabajo",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "codigo_trabajo": {
                "nombre": "Código de Trabajo",
                "tipo": "dimension",
                "columna_bd": "cod_trabajo_id",
                "tabla_dimension": "dim_codigo_trabajo",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "provincia": {
                "nombre": "Provincia",
                "tipo": "dimension",
                "columna_bd": "provincia_id",
                "tabla_dimension": "dim_provincias",
                "campo_nombre": "nombre",
                "grupo": "Ubicación Geográfica"
            },
            "comarca": {
                "nombre": "Comarca",
                "tipo": "dimension",
                "columna_bd": "comarca_id",
                "tabla_dimension": "dim_comarcas",
                "campo_nombre": "nombre",
                "grupo": "Ubicación Geográfica"
            },
            "municipio": {
                "nombre": "Municipio",
                "tipo": "dimension",
                "columna_bd": "municipio_id",
                "tabla_dimension": "dim_municipios",
                "campo_nombre": "nombre",
                "grupo": "Ubicación Geográfica"
            },
            "concejo": {
                "nombre": "Concejo",
                "tipo": "dimension",
                "columna_bd": "concejo_id",
                "tabla_dimension": "dim_concejos",
                "campo_nombre": "nombre",
                "grupo": "Ubicación Geográfica"
            },
            "localizacion": {
                "nombre": "Localización",
                "tipo": "texto",
                "columna_bd": "localizacion",
                "grupo": "Ubicación Geográfica"
            },
            "trabajadores": {
                "nombre": "Trabajadores",
                "tipo": "texto",
                "columna_bd": "trabajadores",
                "grupo": "Recursos Humanos"
            },
            "tipo_rep": {
                "nombre": "Tipo de Reparación",
                "tipo": "dimension",
                "columna_bd": "tipo_rep_id",
                "tabla_dimension": "dim_tipos_rep",
                "campo_nombre": "descripcion",
                "grupo": "Dimensiones Técnicas"
            },
            "fecha_inicio": {
                "nombre": "Fecha Inicio",
                "tipo": "fecha",
                "columna_bd": "fecha_inicio",
                "grupo": "Fechas"
            },
            "fecha_fin": {
                "nombre": "Fecha Fin",
                "tipo": "fecha",
                "columna_bd": "fecha_fin",
                "grupo": "Fechas"
            },
            "importe": {
                "nombre": "Importe",
                "tipo": "calculado",
                "formula": "COALESCE((SELECT SUM(pc.cantidad_cert * pc.precio_unit) FROM tbl_part_certificacion pc WHERE pc.parte_id = p.id AND pc.certificada = 1), 0)",
                "formato": "moneda",
                "grupo": "Económico"
            },
            "finalizada": {
                "nombre": "Finalizada",
                "tipo": "booleano",
                "columna_bd": "finalizada",
                "grupo": "Información Básica"
            }
        },

        "filtros": {
            "mes": {
                "campo": "mes",
                "tipo": "mes_anio",
                "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
            },
            "año": {
                "campo": "año",
                "tipo": "anio",
                "operadores": ["Igual a", "Mayor a", "Menor a", "Entre"]
            },
            "estado": {
                "campo": "estado",
                "tipo": "select",
                "operadores": ["Igual a", "Diferente de"],
                "valores": ["Pendiente", "En curso", "Finalizado"]
            },
            "red": {
                "campo": "red",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_red"
            },
            "tipo_trabajo": {
                "campo": "tipo_trabajo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_tipo_trabajo"
            },
            "codigo_trabajo": {
                "campo": "codigo_trabajo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_codigo_trabajo"
            },
            "provincia": {
                "campo": "provincia",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_provincias"
            },
            "comarca": {
                "campo": "comarca",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_comarcas"
            },
            "municipio": {
                "campo": "municipio",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_municipios"
            },
            "concejo": {
                "campo": "concejo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_concejos"
            },
            "trabajadores": {
                "campo": "trabajadores",
                "tipo": "texto",
                "operadores": ["Igual a", "Diferente de", "Contiene", "No contiene"]
            },
            "tipo_rep": {
                "campo": "tipo_rep",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_tipos_rep"
            },
            "fecha_inicio": {
                "campo": "fecha_inicio",
                "tipo": "fecha",
                "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
            },
            "fecha_fin": {
                "campo": "fecha_fin",
                "tipo": "fecha",
                "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
            },
            "finalizada": {
                "campo": "finalizada",
                "tipo": "booleano",
                "operadores": ["Sí", "No"]
            }
        },

        "ordenaciones": [
            "mes",
            "año",
            "estado",
            "red",
            "tipo_trabajo",
            "provincia",
            "comarca",
            "municipio",
            "fecha_inicio",
            "fecha_fin",
            "tipo_rep"
        ],

        "agrupaciones": {
            "campos_permitidos": [
                "mes",
                "año",
                "estado",
                "red",
                "tipo_trabajo",
                "codigo_trabajo",
                "tipo_rep",
                "provincia",
                "comarca",
                "municipio",
                "trabajadores"
            ],
            "max_niveles": 3,
            "modo_default": "detalle"
        },

        "agregaciones": {},  # No permitir agregaciones

        "campos_default": [
            "codigo",
            "titulo",
            "fecha",
            "municipio",
            "localizacion",
            "importe"
        ]
    }
}


# ============================================================
# CAMPOS DISPONIBLES POR CATEGORÍA
# ============================================================

CAMPOS_PARTES = {
    "Información Básica": [
        "Código del parte",
        "Título",
        "Descripción",
        "Estado"
    ],
    "Dimensiones": [
        "OT",
        "Red",
        "Tipo de Trabajo",
        "Código de Trabajo",
        "Tipo de Reparación",
        "Municipio",
        "Comarca",
        "Provincia"
    ],
    "Económico": [
        "Presupuesto",
        "Certificado",
        "Pendiente",
        "% Avance",
        "Desviación"
    ],
    "Fechas": [
        "Fecha Creación",
        "Fecha Inicio",
        "Fecha Fin",
        "Fecha Actualización"
    ],
    "Adicionales": [
        "Observaciones",
        "Fotografías",
        "N° Items"
    ]
}

CAMPOS_RECURSOS = {
    "Información Básica": [
        "Código del registro",
        "Tipo de elemento",
        "Descripción",
        "Estado"
    ],
    "Ubicación": [
        "Coordenadas",
        "Municipio",
        "Zona/Sector"
    ],
    "Fechas": [
        "Fecha de instalación",
        "Fecha última inspección"
    ],
    "Adicionales": [
        "Observaciones",
        "Fotografías",
        "Parte asociado"
    ]
}

CAMPOS_PRESUPUESTOS = {
    "Información Básica": [
        "Código del parte",
        "Código de partida",
        "Descripción",
        "Capítulo"
    ],
    "Cantidades": [
        "Unidad",
        "Cantidad presupuestada",
        "Cantidad certificada",
        "Cantidad pendiente"
    ],
    "Económico": [
        "Precio unitario",
        "Coste total",
        "% sobre presupuesto",
        "Desviación"
    ]
}

CAMPOS_CERTIFICACIONES = {
    "Información Básica": [
        "ID certificación",
        "Código del parte",
        "Código de partida",
        "Descripción"
    ],
    "Cantidades": [
        "Cantidad certificada",
        "Precio unitario",
        "Coste certificado"
    ],
    "Fechas": [
        "Fecha certificación",
        "Días desde presupuesto"
    ],
    "Dimensiones": [
        "OT",
        "Red",
        "Tipo",
        "Estado"
    ]
}


# ============================================================
# OPERADORES POR TIPO DE DATO
# ============================================================

OPERADORES = {
    "texto_bd": [
        "Igual a",
        "Diferente de",
        "Contiene",
        "No contiene"
    ],

    "numerico": [
        "Igual a",
        "Mayor a",
        "Menor a",
        "Mayor o igual a",
        "Menor o igual a",
        "Entre"
    ],

    "fecha": [
        "Igual a",
        "Posterior a",
        "Anterior a",
        "Entre",
        "Último mes",
        "Últimos 3 meses",
        "Último año"
    ],

    "booleano": [
        "Sí",
        "No"
    ]
}


# ============================================================
# TIPOS DE DATO POR CAMPO
# ============================================================

TIPOS_CAMPO = {
    # Partes
    "Código del parte": "texto_bd",
    "Descripción": "texto_bd",
    "Estado": "texto_bd",
    "OT": "texto_bd",
    "Red": "texto_bd",
    "Tipo de Trabajo": "texto_bd",
    "Código de Trabajo": "texto_bd",
    "Municipio": "texto_bd",
    "Presupuesto": "numerico",
    "Certificado": "numerico",
    "Pendiente": "numerico",
    "% Avance": "numerico",
    "Desviación": "numerico",
    "Fecha Creación": "fecha",
    "Fecha Inicio": "fecha",
    "Fecha Fin": "fecha",
    "Fecha Actualización": "fecha",
    "Observaciones": "texto_bd",
    "Fotografías": "booleano",
    "N° Items": "numerico",

    # Recursos
    "Código del registro": "texto_bd",
    "Tipo de elemento": "texto_bd",
    "Coordenadas": "texto_bd",
    "Zona/Sector": "texto_bd",
    "Fecha de instalación": "fecha",
    "Fecha última inspección": "fecha",
    "Parte asociado": "booleano",

    # Presupuestos
    "Código de partida": "texto_bd",
    "Capítulo": "texto_bd",
    "Unidad": "texto_bd",
    "Cantidad presupuestada": "numerico",
    "Cantidad certificada": "numerico",
    "Cantidad pendiente": "numerico",
    "Precio unitario": "numerico",
    "Coste total": "numerico",
    "% sobre presupuesto": "numerico",

    # Certificaciones
    "ID certificación": "numerico",
    "Cantidad certificada": "numerico",
    "Coste certificado": "numerico",
    "Fecha certificación": "fecha",
    "Días desde presupuesto": "numerico",
    "Tipo": "texto_bd",

    # Planificación
    "Fecha inicio planificada": "fecha",
    "Fecha fin planificada": "fecha",
    "Duración planificada": "numerico",
    "Fecha inicio real": "fecha",
    "Fecha fin real": "fecha",
    "Duración real": "numerico",
    "Desviación temporal": "numerico",
    "En plazo": "booleano"
}


# ============================================================
# OPCIONES DE FORMATO
# ============================================================

FORMATOS_SALIDA = ["Tabla", "Lista", "Tarjetas"]

ORDEN_OPCIONES = ["Ascendente", "Descendente"]

LOGICA_FILTROS = ["Y", "O"]


# ============================================================
# CONFIGURACIÓN DE CABECERA (valores por defecto)
# ============================================================

CONFIG_CABECERA_DEFAULT = {
    "empresa_nombre": "",
    "empresa_cif": "",
    "empresa_direccion": "",
    "empresa_telefono": "",
    "empresa_email": "",
    "empresa_web": "",
    "proyecto_nombre": "",
    "proyecto_codigo": "",
    "proyecto_cliente": "",
    "logo_path": "",
    "pie_pagina": ""
}


# ============================================================
# COLORES Y ESTILOS
# ============================================================

COLORES = {
    "primary": "#1976D2",
    "secondary": "#424242",
    "success": "#4CAF50",
    "warning": "#FF9800",
    "danger": "#F44336",
    "info": "#2196F3",
    "light": "#F5F5F5",
    "dark": "#212121"
}
