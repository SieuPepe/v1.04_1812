# script/informes_header_config.py
"""
Configuración de encabezados y pies de página para informes
HydroFlow Manager v1.04
"""

import os
from pathlib import Path

# Rutas de logos
IMAGES_DIR = Path(__file__).parent.parent / "resources" / "images"
LOGO_REDES_URBIDE = IMAGES_DIR / "logo artanda.png"  # Logo izquierdo - Logo Redes Urbide
LOGO_URBIDE = IMAGES_DIR / "logo artanda2.png"  # Logo derecho - Logo Urbide

# Configuración por defecto del encabezado
HEADER_CONFIG_DEFAULT = {
    "logo_izquierdo": str(LOGO_REDES_URBIDE),
    "logo_derecho": str(LOGO_URBIDE),
    "altura_logos": 50,  # px
    "mostrar_titulo": True,
    "fuente_titulo": {
        "nombre": "Arial",
        "tamano": 10,  # Reducido de 16 a 10pt según especificación
        "negrita": True,
        "color": "#1f6aa5"
    },
    "incluir_fecha": True,
    "incluir_usuario": True,
    "fondo_header": "#f0f0f0",
    "borde_header": True
}

# Configuración por defecto del pie de página
FOOTER_CONFIG_DEFAULT = {
    "mostrar_paginacion": True,
    "texto_izquierdo": "HydroFlow Manager v1.04",
    "texto_centro": "",
    "texto_derecho": "Generado: {fecha}",
    "fuente": {
        "nombre": "Arial",
        "tamano": 9,
        "color": "#666666"
    },
    "fondo_footer": "#f0f0f0",
    "borde_footer": True
}

# Configuración del cuadro informativo (criterios de filtrado/clasificación)
INFO_BOX_CONFIG = {
    "mostrar": True,
    "titulo": "CRITERIOS APLICADOS",
    "incluir_filtros": True,
    "incluir_clasificaciones": True,
    "incluir_agrupaciones": True,
    "fondo": "#e8f4f8",
    "borde": True,
    "color_borde": "#1f6aa5"
}


class HeaderFooterConfig:
    """Gestor de configuración de encabezados y pies de página"""

    def __init__(self):
        self.header_config = HEADER_CONFIG_DEFAULT.copy()
        self.footer_config = FOOTER_CONFIG_DEFAULT.copy()
        self.info_box_config = INFO_BOX_CONFIG.copy()

    def actualizar_header(self, **kwargs):
        """Actualiza configuración del encabezado"""
        self.header_config.update(kwargs)

    def actualizar_footer(self, **kwargs):
        """Actualiza configuración del pie de página"""
        self.footer_config.update(kwargs)

    def actualizar_info_box(self, **kwargs):
        """Actualiza configuración del cuadro informativo"""
        self.info_box_config.update(kwargs)

    def get_header_config(self):
        """Obtiene configuración actual del encabezado"""
        return self.header_config.copy()

    def get_footer_config(self):
        """Obtiene configuración actual del pie de página"""
        return self.footer_config.copy()

    def get_info_box_config(self):
        """Obtiene configuración actual del cuadro informativo"""
        return self.info_box_config.copy()

    def guardar_configuracion(self, archivo="header_footer_config.json"):
        """Guarda configuración en archivo JSON"""
        import json
        config = {
            "header": self.header_config,
            "footer": self.footer_config,
            "info_box": self.info_box_config
        }
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

    def cargar_configuracion(self, archivo="header_footer_config.json"):
        """Carga configuración desde archivo JSON"""
        import json
        if os.path.exists(archivo):
            with open(archivo, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.header_config = config.get("header", HEADER_CONFIG_DEFAULT.copy())
                self.footer_config = config.get("footer", FOOTER_CONFIG_DEFAULT.copy())
                self.info_box_config = config.get("info_box", INFO_BOX_CONFIG.copy())
            return True
        return False
