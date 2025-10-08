import customtkinter
from PIL import Image, ImageTk
import base64
import io
from io import BytesIO
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox
from script.modulo_db import get_option_item_sub_bd,get_id_item_bd,add_photo_register


customtkinter.set_appearance_mode("dark")

class AppViewPhoto(customtkinter.CTkToplevel):
    width = 800
    height = 600


    def __init__(self, select_data,id_register_select):
        super().__init__()

        password = select_data[1]
        user = select_data[0]
        schema = select_data[2]

        self.image_label = None
        self.current_index = 0

        self.title("HydroFlow Manager")
        self.geometry(f"{self.width}x{self.height}")
        self.lift()
        self.attributes('-topmost', True)


        # Crear el frame para mostrar la imagen
        self.image_frame = customtkinter.CTkFrame(self, height=400, fg_color="transparent")
        self.image_frame.pack(pady=20)

        # Botones para navegar entre las imágenes
        self.button_frame = customtkinter.CTkFrame(self,fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.prev_button = customtkinter.CTkButton(self.button_frame, text="Anterior", command=lambda: self.prev_image(self.images_base64))
        self.prev_button.grid(row=0, column=0, padx=10)

        self.next_button = customtkinter.CTkButton(self.button_frame, text="Siguiente", command=lambda: self.next_image(self.images_base64))
        self.next_button.grid(row=0, column=1, padx=10)

        # Botón para añadir una nueva imagen
        self.add_button = customtkinter.CTkButton(self, text="Añadir Imagen", command=lambda: self.add_image(select_data, id_register_select))
        self.add_button.pack(pady=10)

        self.images_base64=get_option_item_sub_bd(user, password, "tbl_inv_fotografias", schema, "base64",id_register_select,"id_inventario")
        # Mostrar la primera imagen (si existe)
        
        if self.images_base64:
            self.show_image(self.current_index, self.images_base64)

    def show_image(self,index,images_base64):

        if 0 <= index < len(images_base64):
            img = self.base64_to_image(images_base64[index])
            aspect_ratio = img.width / img.height
            new_width = int(400 * aspect_ratio)
            img = img.resize((new_width, 400))  # Ajustar el tamaño de la imagen
            img_tk = ImageTk.PhotoImage(img)

            if self.image_label is not None:
                self.image_label.destroy()

            self.image_label = customtkinter.CTkLabel(self.image_frame, image=img_tk, text="")
            self.image_label.image = img_tk
            self.image_label.pack(pady=20)

    def base64_to_image(self,base64_string):
        img_data = base64.b64decode(base64_string)
        img = Image.open(io.BytesIO(img_data))
        return img

    # Funciones para navegar entre las imágenes
    def next_image(self,images_base64):
        if self.current_index < len(images_base64) - 1:
            self.current_index += 1
            self.show_image(self.current_index,images_base64)

    def prev_image(self,images_base64):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image(self.current_index,images_base64)

    # Función para añadir una nueva imagen
    def add_image(self,select_data, id_register):
        id_project=get_id_item_bd(select_data[0], select_data[1], "tbl_proyectos", select_data[2],
                       "codigo", select_data[2])
        self.after(1, lambda: self.attributes('-topmost', False))
        path_photo = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        self.after(1, lambda: self.attributes('-topmost', True))
        if len(path_photo) > 0:
            # Cargar la imagen seleccionada
            imagen = Image.open(path_photo)
            original_width, original_height = imagen.size
            # Calcular el nuevo ancho manteniendo la proporción
            aspect_ratio = original_width / original_height
            new_width = int(200 * aspect_ratio)
            imagen = imagen.resize((new_width, 200))
            # Convertir la imagen a un objeto BytesIO
            buffered = BytesIO()
            imagen.save(buffered, format="PNG")
            # Codificar la imagen a Base64
            img_64 = base64.b64encode(buffered.getvalue()).decode()

            data_photo = []
            if len(path_photo) != 0 and len(img_64) != 0:
                sub_data = []
                id_type = 2
                id_project_item = id_project
                id_inventory = id_register
                item_base64 = img_64
                item_path = path_photo
                sub_data.append(id_project_item)
                sub_data.append(id_inventory)
                sub_data.append(id_type)
                sub_data.append(item_base64)
                sub_data.append(item_path)
                data_photo.append(sub_data)
            result=add_photo_register(select_data[0], select_data[1], select_data[2], data_photo)
            if result=="ok":
                CTkMessagebox(title="Successfull Message!",
                              message="Se han subido la fotografia al registro",
                              icon="check")

            else:
                CTkMessagebox(title="Warning Message!", message=result,
                              icon="warning")
            self.images_base64 = get_option_item_sub_bd(select_data[0], select_data[1], "tbl_inv_fotografias",select_data[2], "base64",
                                                        id_register, "id_inventario")
            if self.images_base64:
                self.show_image(self.current_index, self.images_base64)



