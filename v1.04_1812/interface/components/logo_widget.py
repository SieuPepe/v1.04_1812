"""
Componente de logo reutilizable.

Elimina duplicación de código de imagen base64 en 8+ archivos.
"""
import base64
from io import BytesIO
from PIL import Image
import customtkinter


def create_logo_widget(
    parent,
    image_base64,
    size=(80, 80),
    row=5,
    column=1,
    padx=30,
    pady=(15, 15),
    columnspan=2,
    text=""
):
    """
    Crea un widget de logo desde imagen base64.

    Elimina 15-20 líneas de código duplicado en cada archivo que usa logo.
    Archivos afectados:
    - customer_add_interfaz.py
    - customer_mod_interfaz.py
    - confirm_photo_interfaz.py
    - ... y 5+ archivos más

    Args:
        parent: Widget padre donde colocar el logo
        image_base64: String base64 de la imagen
        size: Tupla (width, height) del tamaño del logo
        row: Fila del grid
        column: Columna del grid
        padx: Padding horizontal
        pady: Padding vertical (puede ser tupla)
        columnspan: Número de columnas a ocupar
        text: Texto a mostrar junto al logo (default: "")

    Returns:
        CTkLabel: Widget del logo creado y posicionado

    Example:
        ```python
        logo = create_logo_widget(
            self.frame,
            image_base64="iVBORw0KGgoAAAANSUhEUgAA...",
            size=(100, 100),
            row=0,
            column=0
        )
        ```
    """
    # Decodificar imagen base64
    image_data = base64.b64decode(image_base64)
    image = Image.open(BytesIO(image_data))

    # Crear CTkImage
    ctk_image = customtkinter.CTkImage(image, size=size)

    # Crear y posicionar label
    logo_label = customtkinter.CTkLabel(
        parent,
        image=ctk_image,
        text=text
    )

    logo_label.grid(
        row=row,
        column=column,
        padx=padx,
        pady=pady,
        columnspan=columnspan
    )

    return logo_label


def create_logo_from_file(
    parent,
    image_path,
    size=(80, 80),
    row=5,
    column=1,
    padx=30,
    pady=(15, 15),
    columnspan=2,
    text=""
):
    """
    Crea un widget de logo desde archivo de imagen.

    Alternativa a create_logo_widget para cuando se tiene archivo en disco.

    Args:
        parent: Widget padre donde colocar el logo
        image_path: Ruta al archivo de imagen
        size: Tupla (width, height) del tamaño del logo
        row: Fila del grid
        column: Columna del grid
        padx: Padding horizontal
        pady: Padding vertical (puede ser tupla)
        columnspan: Número de columnas a ocupar
        text: Texto a mostrar junto al logo

    Returns:
        CTkLabel: Widget del logo creado y posicionado
    """
    # Cargar imagen desde archivo
    image = Image.open(image_path)

    # Crear CTkImage
    ctk_image = customtkinter.CTkImage(image, size=size)

    # Crear y posicionar label
    logo_label = customtkinter.CTkLabel(
        parent,
        image=ctk_image,
        text=text
    )

    logo_label.grid(
        row=row,
        column=column,
        padx=padx,
        pady=pady,
        columnspan=columnspan
    )

    return logo_label
