# script/pdf_config.py
"""
Configuración de Plantillas PDF por Tipo de Informe
Define diseños específicos para cada tipo de informe (similar a Access)
"""

from reportlab.lib import colors


# ============================================================
# CONFIGURACIONES POR TIPO DE INFORME
# ============================================================

CONFIGURACIONES_PDF = {
    # ============================================================
    # PARTES
    # ============================================================

    "Listado de Partes": {
        "orientacion": "horizontal",  # landscape
        "esquema_colores": "azul",
        "mostrar_logos": True,
        "mostrar_fecha": True,
        "mostrar_proyecto": True,
        "fuente_titulo": "Helvetica-Bold",
        "tamaño_titulo": 20,
        "color_titulo": "#003366",
        "color_header_tabla": "#D9E2F3",
        "color_grupo_nivel0": "#003366",
        "color_grupo_nivel1": "#4472C4",
        "color_grupo_nivel2": "#8FAADC",
        "bordes_tabla": True,
        "filas_alternadas": True,
        "pie_pagina_personalizado": None
    },

    # ============================================================
    # RECURSOS
    # ============================================================

    "Listado de Partidas del Presupuesto": {
        "orientacion": "horizontal",
        "esquema_colores": "verde",
        "mostrar_logos": True,
        "mostrar_fecha": True,
        "mostrar_proyecto": True,
        "fuente_titulo": "Helvetica-Bold",
        "tamaño_titulo": 18,
        "color_titulo": "#2E7D32",  # Verde oscuro
        "color_header_tabla": "#E8F5E9",  # Verde claro
        "color_grupo_nivel0": "#2E7D32",
        "color_grupo_nivel1": "#66BB6A",
        "color_grupo_nivel2": "#A5D6A7",
        "bordes_tabla": True,
        "filas_alternadas": True,
        "pie_pagina_personalizado": None
    },

    "Consumo de Recursos": {
        "orientacion": "horizontal",
        "esquema_colores": "verde",
        "mostrar_logos": True,
        "mostrar_fecha": True,
        "mostrar_proyecto": True,
        "fuente_titulo": "Helvetica-Bold",
        "tamaño_titulo": 18,
        "color_titulo": "#2E7D32",
        "color_header_tabla": "#E8F5E9",
        "color_grupo_nivel0": "#2E7D32",
        "color_grupo_nivel1": "#66BB6A",
        "color_grupo_nivel2": "#A5D6A7",
        "bordes_tabla": True,
        "filas_alternadas": True,
        "pie_pagina_personalizado": None
    },

    "Recursos Presupuestados": {
        "orientacion": "vertical",  # A4 vertical para anchos de 18cm
        "esquema_colores": "verde",
        "mostrar_logos": True,
        "mostrar_fecha": False,  # NO mostrar fecha antes de la tabla
        "mostrar_proyecto": True,
        "fuente_titulo": "Helvetica-Bold",
        "tamaño_titulo": 18,
        "color_titulo": "#2E7D32",
        "color_header_tabla": "#E8F5E9",
        "color_grupo_nivel0": "#2E7D32",
        "color_grupo_nivel1": "#66BB6A",
        "color_grupo_nivel2": "#A5D6A7",
        "bordes_tabla": True,
        "filas_alternadas": True,
        "pie_pagina_personalizado": None
    },

    "Recursos Certificados": {
        "orientacion": "vertical",  # A4 vertical para anchos de 18cm
        "esquema_colores": "verde",
        "mostrar_logos": True,
        "mostrar_fecha": False,  # NO mostrar fecha antes de la tabla
        "mostrar_proyecto": True,
        "fuente_titulo": "Helvetica-Bold",
        "tamaño_titulo": 18,
        "color_titulo": "#2E7D32",
        "color_header_tabla": "#E8F5E9",
        "color_grupo_nivel0": "#2E7D32",
        "color_grupo_nivel1": "#66BB6A",
        "color_grupo_nivel2": "#A5D6A7",
        "bordes_tabla": True,
        "filas_alternadas": True,
        "pie_pagina_personalizado": None
    },

    "Recursos Pendientes": {
        "orientacion": "vertical",  # A4 vertical para anchos de 18cm
        "esquema_colores": "verde",
        "mostrar_logos": True,
        "mostrar_fecha": False,  # NO mostrar fecha antes de la tabla
        "mostrar_proyecto": True,
        "fuente_titulo": "Helvetica-Bold",
        "tamaño_titulo": 18,
        "color_titulo": "#2E7D32",
        "color_header_tabla": "#E8F5E9",
        "color_grupo_nivel0": "#2E7D32",
        "color_grupo_nivel1": "#66BB6A",
        "color_grupo_nivel2": "#A5D6A7",
        "bordes_tabla": True,
        "filas_alternadas": True,
        "pie_pagina_personalizado": None
    },

    # ============================================================
    # PRESUPUESTOS
    # ============================================================

    "Contrato": {
        "orientacion": "horizontal",
        "esquema_colores": "naranja",
        "mostrar_logos": True,
        "mostrar_fecha": True,
        "mostrar_proyecto": True,
        "fuente_titulo": "Helvetica-Bold",
        "tamaño_titulo": 20,
        "color_titulo": "#E65100",  # Naranja oscuro
        "color_header_tabla": "#FFF3E0",  # Naranja muy claro
        "color_grupo_nivel0": "#E65100",
        "color_grupo_nivel1": "#FF9800",
        "color_grupo_nivel2": "#FFB74D",
        "bordes_tabla": True,
        "filas_alternadas": True,
        "pie_pagina_personalizado": "DOCUMENTO CONTRACTUAL - CONFIDENCIAL"
    },

    "Presupuesto Detallado": {
        "orientacion": "horizontal",
        "esquema_colores": "naranja",
        "mostrar_logos": True,
        "mostrar_fecha": True,
        "mostrar_proyecto": True,
        "fuente_titulo": "Helvetica-Bold",
        "tamaño_titulo": 18,
        "color_titulo": "#E65100",
        "color_header_tabla": "#FFF3E0",
        "color_grupo_nivel0": "#E65100",
        "color_grupo_nivel1": "#FF9800",
        "color_grupo_nivel2": "#FFB74D",
        "bordes_tabla": True,
        "filas_alternadas": True,
        "pie_pagina_personalizado": None
    },

    "Presupuesto Resumen": {
        "orientacion": "horizontal",
        "esquema_colores": "naranja",
        "mostrar_logos": True,
        "mostrar_fecha": True,
        "mostrar_proyecto": True,
        "fuente_titulo": "Helvetica-Bold",
        "tamaño_titulo": 18,
        "color_titulo": "#E65100",
        "color_header_tabla": "#FFF3E0",
        "color_grupo_nivel0": "#E65100",
        "color_grupo_nivel1": "#FF9800",
        "color_grupo_nivel2": "#FFB74D",
        "bordes_tabla": True,
        "filas_alternadas": True,
        "pie_pagina_personalizado": None
    },

    # ============================================================
    # CERTIFICACIONES
    # ============================================================

    "Certificación Detallado": {
        "orientacion": "horizontal",
        "esquema_colores": "morado",
        "mostrar_logos": True,
        "mostrar_fecha": True,
        "mostrar_proyecto": True,
        "fuente_titulo": "Helvetica-Bold",
        "tamaño_titulo": 18,
        "color_titulo": "#6A1B9A",  # Morado oscuro
        "color_header_tabla": "#F3E5F5",  # Morado muy claro
        "color_grupo_nivel0": "#6A1B9A",
        "color_grupo_nivel1": "#9C27B0",
        "color_grupo_nivel2": "#BA68C8",
        "bordes_tabla": True,
        "filas_alternadas": True,
        "pie_pagina_personalizado": "DOCUMENTO OFICIAL DE CERTIFICACIÓN"
    },

    "Certificación Resumen": {
        "orientacion": "horizontal",
        "esquema_colores": "morado",
        "mostrar_logos": True,
        "mostrar_fecha": True,
        "mostrar_proyecto": True,
        "fuente_titulo": "Helvetica-Bold",
        "tamaño_titulo": 18,
        "color_titulo": "#6A1B9A",
        "color_header_tabla": "#F3E5F5",
        "color_grupo_nivel0": "#6A1B9A",
        "color_grupo_nivel1": "#9C27B0",
        "color_grupo_nivel2": "#BA68C8",
        "bordes_tabla": True,
        "filas_alternadas": True,
        "pie_pagina_personalizado": "DOCUMENTO OFICIAL DE CERTIFICACIÓN"
    },

    # ============================================================
    # PLANIFICACIÓN
    # ============================================================

    "Informe de Avance": {
        "orientacion": "horizontal",
        "esquema_colores": "teal",
        "mostrar_logos": True,
        "mostrar_fecha": True,
        "mostrar_proyecto": True,
        "fuente_titulo": "Helvetica-Bold",
        "tamaño_titulo": 18,
        "color_titulo": "#00695C",  # Teal oscuro
        "color_header_tabla": "#E0F2F1",  # Teal muy claro
        "color_grupo_nivel0": "#00695C",
        "color_grupo_nivel1": "#00897B",
        "color_grupo_nivel2": "#4DB6AC",
        "bordes_tabla": True,
        "filas_alternadas": True,
        "pie_pagina_personalizado": None
    }
}


# ============================================================
# CONFIGURACIÓN POR DEFECTO
# ============================================================

CONFIGURACION_DEFAULT = {
    "orientacion": "horizontal",
    "esquema_colores": "azul",
    "mostrar_logos": True,
    "mostrar_fecha": True,
    "mostrar_proyecto": True,
    "fuente_titulo": "Helvetica-Bold",
    "tamaño_titulo": 18,
    "color_titulo": "#003366",
    "color_header_tabla": "#D9E2F3",
    "color_grupo_nivel0": "#003366",
    "color_grupo_nivel1": "#4472C4",
    "color_grupo_nivel2": "#8FAADC",
    "bordes_tabla": True,
    "filas_alternadas": True,
    "pie_pagina_personalizado": None
}


# ============================================================
# FUNCIONES DE UTILIDAD
# ============================================================

def obtener_configuracion_pdf(tipo_informe: str) -> dict:
    """
    Obtiene la configuración PDF para un tipo de informe específico

    Args:
        tipo_informe: Nombre del tipo de informe

    Returns:
        Diccionario con la configuración del PDF
    """
    # Buscar configuración específica
    if tipo_informe in CONFIGURACIONES_PDF:
        return CONFIGURACIONES_PDF[tipo_informe].copy()

    # Usar configuración por defecto
    return CONFIGURACION_DEFAULT.copy()


def obtener_color_reportlab(color_hex: str):
    """
    Convierte un color hexadecimal a un objeto Color de ReportLab

    Args:
        color_hex: Color en formato hexadecimal (ej: "#003366" o "003366")

    Returns:
        Objeto Color de ReportLab
    """
    if not color_hex.startswith('#'):
        color_hex = '#' + color_hex

    return colors.HexColor(color_hex)


def aplicar_configuracion_a_plantilla(plantilla, config: dict):
    """
    Aplica una configuración a una plantilla PDF existente

    Args:
        plantilla: Instancia de PDFTemplate o PDFAgrupaciones
        config: Diccionario de configuración

    Returns:
        Plantilla modificada
    """
    # Aplicar colores
    if 'color_titulo' in config:
        plantilla.style_titulo.textColor = obtener_color_reportlab(config['color_titulo'])

    if 'tamaño_titulo' in config:
        plantilla.style_titulo.fontSize = config['tamaño_titulo']

    if 'color_header_tabla' in config:
        plantilla.color_header_tabla = obtener_color_reportlab(config['color_header_tabla'])

    if 'color_grupo_nivel0' in config:
        plantilla.color_grupo_nivel0 = obtener_color_reportlab(config['color_grupo_nivel0'])
        plantilla.style_grupo_nivel0.textColor = colors.white

    if 'color_grupo_nivel1' in config:
        plantilla.color_grupo_nivel1 = obtener_color_reportlab(config['color_grupo_nivel1'])
        plantilla.style_grupo_nivel1.textColor = colors.white

    if 'color_grupo_nivel2' in config:
        plantilla.color_grupo_nivel2 = obtener_color_reportlab(config['color_grupo_nivel2'])
        plantilla.style_grupo_nivel2.textColor = colors.white

    return plantilla
