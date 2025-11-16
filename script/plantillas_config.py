# script/plantillas_config.py
"""
Configuración de plantillas Word para generación de PDFs
Define qué plantilla usar para cada tipo de informe
"""

import os
import sys

# ============================================================
# MAPEO DE INFORMES A PLANTILLAS
# ============================================================

PLANTILLAS_POR_INFORME = {
    # Categoría: PARTES
    "Listado de Partes": "Plantilla_Partes.docx",

    # Categoría: RECURSOS
    "Listado de Partidas del Presupuesto": "Plantilla_Recursos.docx",
    "Consumo de Recursos": "Plantilla_Recursos.docx",

    # Categoría: PRESUPUESTO
    "Contrato": "Plantilla_Presupuesto.docx",
    "Presupuesto Detallado": "Plantilla_Presupuesto.docx",
    "Presupuesto Resumen": "Plantilla_Presupuesto.docx",

    # Categoría: CERTIFICACIÓN
    "Certificación Detallado": "Plantilla_Certificacion.docx",
    "Certificación Resumen": "Plantilla_Certificacion.docx",

    # Categoría: PLANIFICACIÓN
    "Informe de Avance": "Plantilla_Planificacion.docx",
}

# Plantilla por defecto si no se encuentra el tipo de informe
PLANTILLA_DEFAULT = "Plantilla_Generica.docx"

# Plantilla legacy para compatibilidad con código antiguo
PLANTILLA_LEGACY = "Plantilla Listado Partes.docx"

# ============================================================
# FUNCIONES DE UTILIDAD
# ============================================================

def obtener_directorio_plantillas():
    """
    Obtiene la ruta absoluta del directorio de plantillas

    Returns:
        str: Ruta completa del directorio de plantillas
    """
    # Obtener directorio base (puede ser diferente en PyInstaller)
    if getattr(sys, 'frozen', False):
        # Ejecutándose como ejecutable PyInstaller
        base_dir = sys._MEIPASS
    else:
        # Ejecutándose como script Python
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_dir, "resources", "plantillas")


def obtener_plantilla_para_informe(tipo_informe):
    """
    Obtiene el nombre de archivo de plantilla apropiado para un tipo de informe

    Args:
        tipo_informe (str): Tipo de informe (ej: "Listado de Partes")

    Returns:
        str: Nombre de archivo de la plantilla (ej: "Plantilla_Partes.docx")
    """
    return PLANTILLAS_POR_INFORME.get(tipo_informe, PLANTILLA_DEFAULT)


def obtener_ruta_plantilla(tipo_informe=None):
    """
    Obtiene la ruta completa de la plantilla para un tipo de informe

    Args:
        tipo_informe (str, optional): Tipo de informe. Si None, usa plantilla por defecto

    Returns:
        str: Ruta completa del archivo de plantilla
    """
    dir_plantillas = obtener_directorio_plantillas()

    if tipo_informe:
        nombre_plantilla = obtener_plantilla_para_informe(tipo_informe)
        ruta_plantilla = os.path.join(dir_plantillas, nombre_plantilla)

        # Si la plantilla específica no existe, intentar con plantilla legacy
        if not os.path.exists(ruta_plantilla):
            ruta_plantilla = os.path.join(dir_plantillas, PLANTILLA_LEGACY)

            # Si tampoco existe legacy, usar plantilla por defecto
            if not os.path.exists(ruta_plantilla):
                ruta_plantilla = os.path.join(dir_plantillas, PLANTILLA_DEFAULT)

        return ruta_plantilla
    else:
        # Sin tipo de informe, usar plantilla por defecto
        return os.path.join(dir_plantillas, PLANTILLA_DEFAULT)


def verificar_plantillas():
    """
    Verifica que existan las plantillas necesarias

    Returns:
        tuple: (bool, list) - (todas_existen, plantillas_faltantes)
    """
    dir_plantillas = obtener_directorio_plantillas()

    # Plantillas únicas que deben existir
    plantillas_necesarias = set(PLANTILLAS_POR_INFORME.values())
    plantillas_necesarias.add(PLANTILLA_DEFAULT)
    plantillas_necesarias.add(PLANTILLA_LEGACY)

    plantillas_faltantes = []

    for plantilla in plantillas_necesarias:
        ruta = os.path.join(dir_plantillas, plantilla)
        if not os.path.exists(ruta):
            plantillas_faltantes.append(plantilla)

    return (len(plantillas_faltantes) == 0, plantillas_faltantes)


def listar_plantillas_disponibles():
    """
    Lista todas las plantillas .docx disponibles en el directorio

    Returns:
        list: Lista de nombres de archivos de plantillas disponibles
    """
    dir_plantillas = obtener_directorio_plantillas()

    if not os.path.exists(dir_plantillas):
        return []

    plantillas = []
    for archivo in os.listdir(dir_plantillas):
        if archivo.endswith('.docx') and not archivo.startswith('~$'):
            plantillas.append(archivo)

    return sorted(plantillas)


# ============================================================
# MARCADORES DISPONIBLES EN PLANTILLAS
# ============================================================

MARCADORES_DISPONIBLES = {
    "[TITULO_DEL_INFORME]": "Nombre del informe (ej: 'Listado de Partes')",
    "[FECHA]": "Fecha de generación del informe",
    "[PROYECTO_NOMBRE]": "Nombre del proyecto",
    "[PROYECTO_CODIGO]": "Código del proyecto",
    "[TABLA_DE_DATOS]": "Tabla con los datos del informe",
    "[TOTAL_REGISTROS]": "Número total de registros en el informe",
    "[FILTROS_APLICADOS]": "Descripción de los filtros aplicados",
    "[EMPRESA]": "Nombre de la empresa",
    "[USUARIO]": "Usuario que genera el informe",
}


def obtener_descripcion_marcadores():
    """
    Obtiene una descripción formateada de los marcadores disponibles

    Returns:
        str: Descripción de todos los marcadores disponibles
    """
    lineas = ["Marcadores disponibles para usar en plantillas Word:\n"]

    for marcador, descripcion in MARCADORES_DISPONIBLES.items():
        lineas.append(f"  {marcador:25} → {descripcion}")

    return "\n".join(lineas)
