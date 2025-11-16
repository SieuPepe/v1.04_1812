# script/plantillas_config.py
"""
Configuración de plantillas Word para generación de PDFs
Define qué plantilla usar para cada tipo de informe
"""

import os

# ============================================================
# MAPEO DE INFORMES A PLANTILLAS
# ============================================================

PLANTILLAS_POR_INFORME = {
    # Categoría: PARTES
    "Listado de Partes": "Plantilla_Partes.docx",

    # Categoría: RECURSOS
    "Listado de Partidas del Presupuesto": "Plantilla_Recursos.docx",
    "Consumo de Recursos": "Plantilla_Recursos.docx",
    "Trabajos por Actuación": "Plantilla_Recursos.docx",

    # Categoría: PRESUPUESTOS
    "Contrato": "Plantilla_Presupuesto.docx",
    "Presupuesto Detallado": "Plantilla_Presupuesto.docx",
    "Presupuesto Resumen": "Plantilla_Presupuesto.docx",

    # Categoría: CERTIFICACIONES
    "Certificación Detallado": "Plantilla_Certificacion.docx",
    "Certificación Resumen": "Plantilla_Certificacion.docx",

    # Categoría: PLANIFICACIÓN
    "Informe de Avance": "Plantilla_Planificacion.docx",
}

# Plantilla por defecto si no se encuentra una específica
PLANTILLA_DEFAULT = "Plantilla_Generica.docx"

# Plantilla fallback si tampoco existe la por defecto
PLANTILLA_FALLBACK = "Plantilla Listado Partes.docx"


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def obtener_plantilla_para_informe(informe_nombre: str, base_dir: str = None) -> str:
    """
    Obtiene la ruta completa de la plantilla apropiada para un informe

    Args:
        informe_nombre: Nombre del informe (ej: "Listado de Partes")
        base_dir: Directorio base del proyecto (opcional)

    Returns:
        str: Ruta completa a la plantilla a usar
    """
    if base_dir is None:
        # Obtener directorio base del proyecto
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    plantillas_dir = os.path.join(base_dir, "plantillas")

    # Buscar plantilla específica para este informe
    plantilla_nombre = PLANTILLAS_POR_INFORME.get(informe_nombre)

    if plantilla_nombre:
        plantilla_path = os.path.join(plantillas_dir, plantilla_nombre)
        if os.path.exists(plantilla_path):
            print(f"✓ Usando plantilla específica: {plantilla_nombre}")
            return plantilla_path
        else:
            print(f"⚠ Plantilla específica no encontrada: {plantilla_nombre}")

    # Intentar con plantilla por defecto
    plantilla_default_path = os.path.join(plantillas_dir, PLANTILLA_DEFAULT)
    if os.path.exists(plantilla_default_path):
        print(f"✓ Usando plantilla por defecto: {PLANTILLA_DEFAULT}")
        return plantilla_default_path

    # Intentar con plantilla fallback
    plantilla_fallback_path = os.path.join(plantillas_dir, PLANTILLA_FALLBACK)
    if os.path.exists(plantilla_fallback_path):
        print(f"✓ Usando plantilla fallback: {PLANTILLA_FALLBACK}")
        return plantilla_fallback_path

    # Si no existe ninguna plantilla, retornar None
    print(f"✗ No se encontró ninguna plantilla en: {plantillas_dir}")
    return None


def listar_plantillas_disponibles(base_dir: str = None) -> list:
    """
    Lista todas las plantillas .docx disponibles

    Args:
        base_dir: Directorio base del proyecto (opcional)

    Returns:
        list: Lista de nombres de archivos de plantillas
    """
    if base_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    plantillas_dir = os.path.join(base_dir, "plantillas")

    if not os.path.exists(plantillas_dir):
        return []

    plantillas = []
    for archivo in os.listdir(plantillas_dir):
        if archivo.endswith('.docx') and not archivo.startswith('~'):
            plantillas.append(archivo)

    return sorted(plantillas)


def verificar_plantillas_necesarias(base_dir: str = None) -> dict:
    """
    Verifica qué plantillas necesarias existen y cuáles faltan

    Args:
        base_dir: Directorio base del proyecto (opcional)

    Returns:
        dict: Diccionario con 'existentes' y 'faltantes'
    """
    if base_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    plantillas_dir = os.path.join(base_dir, "plantillas")

    # Obtener plantillas únicas necesarias
    plantillas_necesarias = set(PLANTILLAS_POR_INFORME.values())
    plantillas_necesarias.add(PLANTILLA_DEFAULT)
    plantillas_necesarias.add(PLANTILLA_FALLBACK)

    existentes = []
    faltantes = []

    for plantilla in plantillas_necesarias:
        plantilla_path = os.path.join(plantillas_dir, plantilla)
        if os.path.exists(plantilla_path):
            existentes.append(plantilla)
        else:
            faltantes.append(plantilla)

    return {
        'existentes': sorted(existentes),
        'faltantes': sorted(faltantes)
    }


# ============================================================
# MARCADORES ESTÁNDAR EN PLANTILLAS
# ============================================================

MARCADORES_PLANTILLA = {
    "[TITULO_DEL_INFORME]": "Nombre del informe en mayúsculas",
    "[FECHA]": "Fecha de generación del informe",
    "[PROYECTO_NOMBRE]": "Nombre del proyecto actual",
    "[PROYECTO_CODIGO]": "Código del proyecto",
    "[TABLA_DE_DATOS]": "Tabla con los datos del informe (se reemplaza por tabla completa)",
    "[TOTAL_REGISTROS]": "Número total de registros en el informe",
    "[FILTROS_APLICADOS]": "Descripción de los filtros aplicados",
}


def obtener_info_marcadores() -> str:
    """Retorna información formateada sobre los marcadores disponibles"""
    info = "MARCADORES DISPONIBLES PARA PLANTILLAS:\n"
    info += "=" * 60 + "\n\n"

    for marcador, descripcion in MARCADORES_PLANTILLA.items():
        info += f"  {marcador}\n"
        info += f"    → {descripcion}\n\n"

    info += "\nUSO:\n"
    info += "  1. Abra su plantilla Word\n"
    info += "  2. Inserte los marcadores donde desee que aparezcan los datos\n"
    info += "  3. Guarde la plantilla en la carpeta 'plantillas/'\n"
    info += "  4. El sistema reemplazará automáticamente los marcadores\n"

    return info
