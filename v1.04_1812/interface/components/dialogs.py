"""
Componentes de diálogos reutilizables.

Elimina duplicación de CTkMessagebox presente en 61+ ubicaciones.
"""
from CTkMessagebox import CTkMessagebox


def show_error(message, title="Error Message!"):
    """
    Muestra un diálogo de error.

    Reemplaza 33 repeticiones de:
    CTkMessagebox(title="Error Message!", message=mssg, icon="cancel")

    Args:
        message: Mensaje de error a mostrar
        title: Título del diálogo (default: "Error Message!")

    Returns:
        Resultado del diálogo
    """
    return CTkMessagebox(title=title, message=message, icon="cancel")


def show_success(message, title="Successful Message!"):
    """
    Muestra un diálogo de éxito.

    Reemplaza 12 repeticiones de:
    CTkMessagebox(title="Successful Message!", message=mssg, icon="check")

    Args:
        message: Mensaje de éxito a mostrar
        title: Título del diálogo (default: "Successful Message!")

    Returns:
        Resultado del diálogo
    """
    return CTkMessagebox(title=title, message=message, icon="check")


def show_warning(message, title="Warning!"):
    """
    Muestra un diálogo de advertencia.

    Reemplaza 10 repeticiones de warnings con error icon.

    Args:
        message: Mensaje de advertencia
        title: Título del diálogo (default: "Warning!")

    Returns:
        Resultado del diálogo
    """
    return CTkMessagebox(title=title, message=message, icon="warning")


def show_info(message, title="Information"):
    """
    Muestra un diálogo informativo.

    Args:
        message: Mensaje informativo
        title: Título del diálogo (default: "Information")

    Returns:
        Resultado del diálogo
    """
    return CTkMessagebox(title=title, message=message, icon="info")


def show_question(message, title="Question", option_1="Yes", option_2="No"):
    """
    Muestra un diálogo de confirmación con opciones.

    Args:
        message: Pregunta a mostrar
        title: Título del diálogo
        option_1: Texto del primer botón (default: "Yes")
        option_2: Texto del segundo botón (default: "No")

    Returns:
        Respuesta del usuario (option_1 o option_2)
    """
    return CTkMessagebox(
        title=title,
        message=message,
        icon="question",
        option_1=option_1,
        option_2=option_2
    )
