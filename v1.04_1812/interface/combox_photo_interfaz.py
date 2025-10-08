import customtkinter
import base64
from io import BytesIO
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("dark")


class ScrollableRadioFrame(customtkinter.CTkScrollableFrame):

    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.radio_buttons = []
        self.image_list = []
        self.selected_image = customtkinter.StringVar()


        for i, item in enumerate(item_list):
            self.add_item(item)


    def add_item(self, image_base64):
        # Decodificar la imagen Base64
        image_data = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_data))

        original_width, original_height = image.size
        # Calcular el nuevo ancho manteniendo la proporción
        aspect_ratio = original_width / original_height
        new_width = int(80* aspect_ratio)
        img_resized = image.resize((new_width, 80))
        tk_img = ImageTk.PhotoImage(img_resized)

        # Crear un Frame para contener la imagen y el botón de radio
        item_frame = customtkinter.CTkFrame(self)
        item_frame.grid(row=len(self.radio_buttons), column=0, pady=(10, 10), padx=10, sticky="w")

        # Crear el RadioButton
        radio_button = customtkinter.CTkRadioButton(item_frame, text="", variable=self.selected_image,
                                                    value=image_base64)
        radio_button.grid(row=0, column=0, padx=10)

        # Crear la etiqueta para mostrar la imagen
        image_label = customtkinter.CTkLabel(item_frame, image=tk_img, text="",height=80)
        image_label.grid(row=0, column=1, padx=10)
        image_label.image = tk_img  # Necesario para que la imagen no sea eliminada por el recolector de basura

        self.radio_buttons.append(radio_button)
        self.image_list.append(image_base64)  # Guardar las imágenes en base64


    def get_checked_item(self):

        return self.selected_image.get()


    def clear_selection(self):
        self.selected_image.set(None)



class AppPhotoCombox(customtkinter.CTkToplevel):
    width = 700
    height = 500

    def __init__(self, item_list, callback):
        super().__init__()

        self.callback = callback
        self.selected_item = None

        self.title("Seleccionar foto de emplazamiento")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0, weight=1)


        self.scrollable_radio_frame = ScrollableRadioFrame(master=self,
                                                           command=self.radio_frame_event,
                                                           item_list=item_list)
        self.scrollable_radio_frame.grid(row=0, padx=20, pady=10, sticky="nsew")

        widthButton2 = int(self.width / 2) - 80
        self.cancel_button = customtkinter.CTkButton(self, text="Cancel", width=widthButton2,
                                                     command=self.destroy)
        self.cancel_button.grid(row=1, padx=60, pady=20, sticky="nw")
        self.save_button = customtkinter.CTkButton(self, text="Ok", width=widthButton2,
                                                   command=self.confirm_save)
        self.save_button.grid(row=1, padx=60, pady=20, sticky="ne")

        self.lift()

    def confirm_save(self):
        selected_image = self.scrollable_radio_frame.get_checked_item()
        if selected_image:
            self.callback(selected_image)
        self.destroy()

    def clear_selection(self):
        self.scrollable_radio_frame.clear_selection()

    def radio_frame_event(self):
        pass  # No es necesario para esta implementación

def image_to_base64(img):
    """Convierte una imagen PIL a Base64."""
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")