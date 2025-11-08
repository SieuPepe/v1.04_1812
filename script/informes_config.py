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
        "Listado de Partes"
    ],

    "📦 Recursos": [
        "Listado de Partidas del Presupuesto",
        "Consumo de Recursos",
        "Trabajos por Actuación"
    ],

    "💰 Presupuestos": [
        "Contrato",
        "Presupuesto Detallado",
        "Presupuesto Resumen"
    ],

    "✅ Certificaciones": [
        "Certificación Detallado",
        "Certificación Resumen"
    ],

    "📅 Planificación": [
        "Informe de Avance"
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
                "tipo": "fecha",
                "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
            },
            "año": {
                "campo": "año",
                "tipo": "numerico",
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
                "campo_nombre": "descripcion",
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

    "Consumo de Recursos": {
        "categoria": "📦 Recursos",
        "descripcion": "Partidas del presupuesto con cantidad presupuestada e importe presupuesto, cantidad certificada e importe certificado.",
        "tabla_principal": "tbl_pres_precios",
        "require_joins": ["tbl_part_presupuesto", "tbl_part_certificacion"],

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
                "campo_nombre": "descripcion",
                "grupo": "Información Básica"
            },
            "resumen": {
                "nombre": "Recurso/Material",
                "tipo": "texto",
                "columna_bd": "resumen",
                "grupo": "Información Básica"
            },
            "precio_unitario": {
                "nombre": "Precio",
                "tipo": "numerico",
                "columna_bd": "coste",
                "formato": "moneda",
                "grupo": "Económico"
            },
            "cantidad_presupuesto": {
                "nombre": "Cant. Presupuesto",
                "tipo": "calculado",
                "formula": "COALESCE((SELECT SUM(pp.cantidad) FROM tbl_part_presupuesto pp WHERE pp.precio_id = pr.id), 0)",
                "formato": "decimal",
                "grupo": "Presupuesto"
            },
            "importe_presupuesto": {
                "nombre": "Imp. Presupuesto",
                "tipo": "calculado",
                "formula": "COALESCE((SELECT SUM(pp.cantidad * pp.precio_unit) FROM tbl_part_presupuesto pp WHERE pp.precio_id = pr.id), 0)",
                "formato": "moneda",
                "grupo": "Presupuesto"
            },
            "cantidad_certificado": {
                "nombre": "Cant. Certificado",
                "tipo": "calculado",
                "formula": "COALESCE((SELECT SUM(pc.cantidad_cert) FROM tbl_part_certificacion pc WHERE pc.precio_id = pr.id AND pc.certificada = 1), 0)",
                "formato": "decimal",
                "grupo": "Certificación"
            },
            "importe_certificado": {
                "nombre": "Imp. Certificado",
                "tipo": "calculado",
                "formula": "COALESCE((SELECT SUM(pc.cantidad_cert * pc.precio_unit) FROM tbl_part_certificacion pc WHERE pc.precio_id = pr.id AND pc.certificada = 1), 0)",
                "formato": "moneda",
                "grupo": "Certificación"
            }
        },

        "filtros": {
            "capitulo": {
                "campo": "capitulo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "tbl_pres_capitulos"
            },
            "codigo": {
                "campo": "codigo",
                "tipo": "texto",
                "operadores": ["Contiene", "Empieza con"]
            }
        },

        "ordenaciones": [
            "capitulo",
            "codigo",
            "cantidad_presupuesto",
            "cantidad_certificado"
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
            "cantidad_presupuesto",
            "importe_presupuesto",
            "cantidad_certificado",
            "importe_certificado"
        ]
    },

    "Trabajos por Actuación": {
        "categoria": "📦 Recursos",
        "descripcion": "Listado de partes en los que está presupuestada una unidad de obra específica.",
        "tabla_principal": "tbl_partes",
        "require_selector": True,  # Requiere selector especial de partida
        "selector_config": {
            "tipo": "partida_presupuesto",
            "tabla": "tbl_pres_precios",
            "campo_mostrar": "codigo",
            "campo_descripcion": "resumen"
        },

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
            "partida_seleccionada": {
                "nombre": "Partida",
                "tipo": "texto",
                "columna_bd": "codigo",
                "grupo": "Información Básica"
            },
            "codigo_parte": {
                "nombre": "Código Parte",
                "tipo": "texto",
                "columna_bd": "codigo",
                "grupo": "Información Básica"
            },
            "descripcion_parte": {
                "nombre": "Descripción Parte",
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
            "cantidad_presupuestada": {
                "nombre": "Cantidad",
                "tipo": "calculado",
                "formula": "(SELECT pp.cantidad FROM tbl_part_presupuesto pp WHERE pp.parte_id = p.id AND pp.precio_id = @partida_id)",
                "formato": "decimal",
                "grupo": "Presupuesto"
            },
            "importe": {
                "nombre": "Importe",
                "tipo": "calculado",
                "formula": "(SELECT pp.cantidad * pp.precio_unit FROM tbl_part_presupuesto pp WHERE pp.parte_id = p.id AND pp.precio_id = @partida_id)",
                "formato": "moneda",
                "grupo": "Presupuesto"
            },
            "fecha_inicio": {
                "nombre": "Fecha Inicio",
                "tipo": "fecha",
                "columna_bd": "fecha_inicio",
                "grupo": "Fechas"
            }
        },

        "filtros": {
            "estado": {
                "campo": "estado",
                "tipo": "select",
                "operadores": ["Igual a", "Diferente de"],
                "valores": ["Pendiente", "En curso", "Finalizado"]
            },
            "fecha_inicio": {
                "campo": "fecha_inicio",
                "tipo": "fecha",
                "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
            }
        },

        "ordenaciones": [
            "mes",
            "año",
            "estado",
            "fecha_inicio",
            "cantidad_presupuestada"
        ],

        "agrupaciones": {
            "campos_permitidos": [
                "mes",
                "año",
                "estado"
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
            "partida_seleccionada",
            "codigo_parte",
            "descripcion_parte",
            "estado",
            "cantidad_presupuestada",
            "importe"
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
                "campo_nombre": "descripcion",
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
            "codigo_parte": {
                "nombre": "Código Parte",
                "tipo": "texto",
                "columna_bd": "codigo",
                "grupo": "Información Básica"
            },
            "descripcion_parte": {
                "nombre": "Descripción Parte",
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
            "codigo_recurso": {
                "nombre": "Código Recurso",
                "tipo": "texto",
                "columna_bd": "codigo",
                "relacionado": "tbl_pres_precios",
                "grupo": "Detalle"
            },
            "recurso": {
                "nombre": "Recurso/Material",
                "tipo": "texto",
                "columna_bd": "resumen",
                "relacionado": "tbl_pres_precios",
                "grupo": "Detalle"
            },
            "unidad": {
                "nombre": "Ud",
                "tipo": "dimension",
                "columna_bd": "id_unidades",
                "relacionado": "tbl_pres_precios",
                "tabla_dimension": "tbl_pres_unidades",
                "campo_nombre": "descripcion",
                "grupo": "Detalle"
            },
            "cantidad": {
                "nombre": "Cantidad",
                "tipo": "numerico",
                "columna_bd": "cantidad",
                "relacionado": "tbl_part_presupuesto",
                "formato": "decimal",
                "grupo": "Detalle"
            },
            "precio_unitario": {
                "nombre": "Precio Unit.",
                "tipo": "numerico",
                "columna_bd": "precio_unit",
                "relacionado": "tbl_part_presupuesto",
                "formato": "moneda",
                "grupo": "Detalle"
            },
            "importe": {
                "nombre": "Importe",
                "tipo": "calculado",
                "formula": "(cantidad * precio_unitario)",
                "formato": "moneda",
                "grupo": "Detalle"
            },
            "subtotal_parte": {
                "nombre": "Subtotal Parte",
                "tipo": "calculado",
                "formula": "COALESCE((SELECT SUM(pp.cantidad * pp.precio_unit) FROM tbl_part_presupuesto pp WHERE pp.parte_id = p.id), 0)",
                "formato": "moneda",
                "grupo": "Totales"
            }
        },

        "filtros": {
            "estado": {
                "campo": "estado",
                "tipo": "select",
                "operadores": ["Igual a", "Diferente de"],
                "valores": ["Pendiente", "En curso", "Finalizado"]
            }
        },

        "ordenaciones": [
            "mes",
            "año",
            "codigo_parte",
            "estado"
        ],

        "agrupaciones": {
            "campos_permitidos": [
                "mes",
                "año",
                "codigo_parte",
                "estado"
            ],
            "max_niveles": 3,
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
            "codigo_parte",
            "descripcion_parte",
            "codigo_recurso",
            "recurso",
            "unidad",
            "cantidad",
            "precio_unitario",
            "importe"
        ]
    },

    "Presupuesto Resumen": {
        "categoria": "💰 Presupuestos",
        "descripcion": "Resumen de presupuesto mostrando únicamente los partes con sus totales.",
        "tabla_principal": "tbl_partes",

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
                "grupo": "Dimensiones"
            },
            "total_presupuesto": {
                "nombre": "Total Presupuesto",
                "tipo": "calculado",
                "formula": "COALESCE((SELECT SUM(pp.cantidad * pp.precio_unit) FROM tbl_part_presupuesto pp WHERE pp.parte_id = p.id), 0)",
                "formato": "moneda",
                "grupo": "Económico"
            }
        },

        "filtros": {
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
            }
        },

        "ordenaciones": [
            "mes",
            "año",
            "estado",
            "red",
            "total_presupuesto"
        ],

        "agrupaciones": {
            "campos_permitidos": [
                "mes",
                "año",
                "estado",
                "red"
            ],
            "max_niveles": 3,
            "modo_default": "resumen"
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
            },
            "AVG": {
                "nombre": "Promedio",
                "aplicable_a": ["numerico", "calculado"],
                "tipo_resultado": "numerico",
                "formato": "decimal"
            }
        },

        "campos_default": [
            "codigo",
            "descripcion",
            "estado",
            "red",
            "total_presupuesto"
        ]
    },

    # ============================================================
    # CATEGORÍA: CERTIFICACIONES
    # ============================================================

    "Certificación Detallado": {
        "categoria": "✅ Certificaciones",
        "descripcion": "Relación de partes con sus mediciones certificadas. Subtotal por parte y total general.",
        "tabla_principal": "tbl_partes",

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
            "codigo_parte": {
                "nombre": "Código Parte",
                "tipo": "texto",
                "columna_bd": "codigo",
                "grupo": "Información Básica"
            },
            "descripcion_parte": {
                "nombre": "Descripción Parte",
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
            "codigo_recurso": {
                "nombre": "Código Recurso",
                "tipo": "texto",
                "columna_bd": "codigo",
                "relacionado": "tbl_pres_precios",
                "grupo": "Detalle"
            },
            "recurso": {
                "nombre": "Recurso/Material",
                "tipo": "texto",
                "columna_bd": "resumen",
                "relacionado": "tbl_pres_precios",
                "grupo": "Detalle"
            },
            "unidad": {
                "nombre": "Ud",
                "tipo": "dimension",
                "columna_bd": "id_unidades",
                "relacionado": "tbl_pres_precios",
                "tabla_dimension": "tbl_pres_unidades",
                "campo_nombre": "descripcion",
                "grupo": "Detalle"
            },
            "cantidad_certificada": {
                "nombre": "Cantidad Cert.",
                "tipo": "numerico",
                "columna_bd": "cantidad_cert",
                "relacionado": "tbl_part_certificacion",
                "formato": "decimal",
                "grupo": "Detalle"
            },
            "precio_unitario": {
                "nombre": "Precio Unit.",
                "tipo": "numerico",
                "columna_bd": "precio_unit",
                "relacionado": "tbl_part_certificacion",
                "formato": "moneda",
                "grupo": "Detalle"
            },
            "importe": {
                "nombre": "Importe",
                "tipo": "calculado",
                "formula": "(cantidad_certificada * precio_unitario)",
                "formato": "moneda",
                "grupo": "Detalle"
            },
            "subtotal_parte": {
                "nombre": "Subtotal Parte",
                "tipo": "calculado",
                "formula": "COALESCE((SELECT SUM(pc.cantidad_cert * pc.precio_unit) FROM tbl_part_certificacion pc WHERE pc.parte_id = p.id AND pc.certificada = 1), 0)",
                "formato": "moneda",
                "grupo": "Totales"
            }
        },

        "filtros": {
            "estado": {
                "campo": "estado",
                "tipo": "select",
                "operadores": ["Igual a", "Diferente de"],
                "valores": ["Pendiente", "En curso", "Finalizado"]
            }
        },

        "ordenaciones": [
            "mes",
            "año",
            "codigo_parte",
            "estado"
        ],

        "agrupaciones": {
            "campos_permitidos": [
                "mes",
                "año",
                "codigo_parte",
                "estado"
            ],
            "max_niveles": 3,
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
            "codigo_parte",
            "descripcion_parte",
            "codigo_recurso",
            "recurso",
            "unidad",
            "cantidad_certificada",
            "precio_unitario",
            "importe"
        ]
    },

    "Certificación Resumen": {
        "categoria": "✅ Certificaciones",
        "descripcion": "Resumen de certificación mostrando únicamente los partes con sus totales certificados.",
        "tabla_principal": "tbl_partes",

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
                "grupo": "Dimensiones"
            },
            "total_certificado": {
                "nombre": "Total Certificado",
                "tipo": "calculado",
                "formula": "COALESCE((SELECT SUM(pc.cantidad_cert * pc.precio_unit) FROM tbl_part_certificacion pc WHERE pc.parte_id = p.id AND pc.certificada = 1), 0)",
                "formato": "moneda",
                "grupo": "Económico"
            }
        },

        "filtros": {
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
            }
        },

        "ordenaciones": [
            "mes",
            "año",
            "estado",
            "red",
            "total_certificado"
        ],

        "agrupaciones": {
            "campos_permitidos": [
                "mes",
                "año",
                "estado",
                "red"
            ],
            "max_niveles": 3,
            "modo_default": "resumen"
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
            },
            "AVG": {
                "nombre": "Promedio",
                "aplicable_a": ["numerico", "calculado"],
                "tipo_resultado": "numerico",
                "formato": "decimal"
            }
        },

        "campos_default": [
            "codigo",
            "descripcion",
            "estado",
            "red",
            "total_certificado"
        ]
    },

    # ============================================================
    # CATEGORÍA: PLANIFICACIÓN
    # ============================================================

    "Informe de Avance": {
        "categoria": "📅 Planificación",
        "descripcion": "Importes presupuestados por cada mes, mostrando la evolución temporal del proyecto.",
        "tabla_principal": "tbl_partes",

        "campos": {
            "mes": {
                "nombre": "Mes",
                "tipo": "calculado",
                "formula": "DATE_FORMAT(p.fecha_inicio, '%Y-%m')",
                "grupo": "Temporal"
            },
            "num_partes": {
                "nombre": "Nº Partes",
                "tipo": "calculado",
                "formula": "COUNT(p.id)",
                "formato": "entero",
                "grupo": "Indicadores"
            },
            "importe_presupuestado": {
                "nombre": "Importe Presupuestado",
                "tipo": "calculado",
                "formula": "COALESCE(SUM((SELECT SUM(pp.cantidad * pp.precio_unit) FROM tbl_part_presupuesto pp WHERE pp.parte_id = p.id)), 0)",
                "formato": "moneda",
                "grupo": "Económico"
            },
            "importe_certificado": {
                "nombre": "Importe Certificado",
                "tipo": "calculado",
                "formula": "COALESCE(SUM((SELECT SUM(pc.cantidad_cert * pc.precio_unit) FROM tbl_part_certificacion pc WHERE pc.parte_id = p.id AND pc.certificada = 1)), 0)",
                "formato": "moneda",
                "grupo": "Económico"
            },
            "porcentaje_avance": {
                "nombre": "% Avance",
                "tipo": "calculado",
                "formula": "CASE WHEN SUM((SELECT SUM(pp.cantidad * pp.precio_unit) FROM tbl_part_presupuesto pp WHERE pp.parte_id = p.id)) > 0 THEN (COALESCE(SUM((SELECT SUM(pc.cantidad_cert * pc.precio_unit) FROM tbl_part_certificacion pc WHERE pc.parte_id = p.id AND pc.certificada = 1)), 0) / SUM((SELECT SUM(pp.cantidad * pp.precio_unit) FROM tbl_part_presupuesto pp WHERE pp.parte_id = p.id))) * 100 ELSE 0 END",
                "formato": "porcentaje",
                "grupo": "Indicadores"
            }
        },

        "filtros": {
            "mes": {
                "campo": "mes",
                "tipo": "fecha",
                "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
            }
        },

        "ordenaciones": [
            "mes"
        ],

        "agrupaciones": {
            "campos_permitidos": [
                "mes"
            ],
            "max_niveles": 1,
            "modo_default": "resumen"
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
            },
            "AVG": {
                "nombre": "Promedio",
                "aplicable_a": ["numerico", "calculado"],
                "tipo_resultado": "numerico",
                "formato": "decimal"
            }
        },

        "campos_default": [
            "mes",
            "num_partes",
            "importe_presupuestado",
            "importe_certificado",
            "porcentaje_avance"
        ]
    }
}


# ============================================================
# CAMPOS DISPONIBLES POR CATEGORÍA
# ============================================================

CAMPOS_PARTES = {
    "Información Básica": [
        "Código del parte",
        "Descripción",
        "Estado"
    ],
    "Dimensiones": [
        "OT",
        "Red",
        "Tipo de Trabajo",
        "Código de Trabajo",
        "Municipio"
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

CAMPOS_PLANIFICACION = {
    "Información Básica": [
        "Código del parte",
        "Descripción",
        "Estado"
    ],
    "Fechas Planificadas": [
        "Fecha inicio planificada",
        "Fecha fin planificada",
        "Duración planificada"
    ],
    "Fechas Reales": [
        "Fecha inicio real",
        "Fecha fin real",
        "Duración real"
    ],
    "Avance": [
        "% Avance",
        "Desviación temporal",
        "En plazo"
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
