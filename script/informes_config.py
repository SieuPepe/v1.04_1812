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
        "Resumen de Partes",  # ← INFORME MODELO (completamente funcional)
        "Informe Tipo 2",
        "Informe Tipo 3",
        "Informe Tipo 4",
        "Informe Tipo 5"
    ],

    "📦 Recursos": [
        "Informe Tipo 1",
        "Informe Tipo 2",
        "Informe Tipo 3",
        "Informe Tipo 4"
    ],

    "💰 Presupuestos": [
        "Informe Tipo 1",
        "Informe Tipo 2",
        "Informe Tipo 3",
        "Informe Tipo 4"
    ],

    "✅ Certificaciones": [
        "Informe Tipo 1",
        "Informe Tipo 2",
        "Informe Tipo 3",
        "Informe Tipo 4"
    ],

    "📅 Planificación": [
        "Informe Tipo 1",
        "Informe Tipo 2",
        "Informe Tipo 3"
    ]
}


# ============================================================
# DEFINICIONES COMPLETAS DE INFORMES
# ============================================================

INFORMES_DEFINICIONES = {
    "Resumen de Partes": {
        "categoria": "📊 Partes",
        "descripcion": "Listado completo de partes con filtros, agrupación y totales",
        "tabla_principal": "tbl_partes",

        # Campos disponibles para mostrar
        "campos": {
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
            }
        },

        # Filtros disponibles
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
            },
            "tipo_trabajo": {
                "campo": "tipo_trabajo",
                "tipo": "select_bd",
                "operadores": ["Igual a", "Diferente de"],
                "tabla": "dim_tipo_trabajo"
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
            }
        },

        # Clasificaciones disponibles
        "clasificaciones": [
            "estado",
            "red",
            "tipo_trabajo",
            "provincia",
            "comarca",
            "municipio",
            "fecha_inicio"
        ],

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
