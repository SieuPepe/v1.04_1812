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
        "Informe Tipo 1",
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
