import customtkinter
from PIL import Image, ImageTk
import base64
from io import BytesIO
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
from script.modulo_db import get_option_item_sub_bd,get_id_item_bd,add_photo_site_register
from interface.combox_photo_interfaz import AppPhotoCombox

customtkinter.set_appearance_mode("dark")
image_base64=None

class AppPhotoUpload(customtkinter.CTkToplevel):

    def __init__(self, select_data,id_register):
        super().__init__()
        self.title("Information")
        self.geometry("400x150")
        self.resizable(False, False)
        self.attributes('-topmost', True)

        self.label = customtkinter.CTkLabel(self, text="¿Desea añadir una foto existente en la base de datos?")
        self.label.pack(pady=(30,10))

        self.confirm_button = customtkinter.CTkButton(self, text="Si", command=lambda :self.confirm(select_data,id_register), width=100)
        self.confirm_button.pack(side="left", expand=True, padx=10)

        self.cancel_button = customtkinter.CTkButton(self, text="No", command=lambda :self.cancel(select_data,id_register),width=100)
        self.cancel_button.pack(side="right", expand=True, padx=10)

        self.lift()

    def confirm(self,select_data,id_register):
        global image_base64
        list_photo= get_option_item_sub_bd(select_data[0], select_data[1], "tbl_inv_fotografias", select_data[2], 'base64', id_register, "id_inventario")
        if len(list_photo)!=0:
            self.withdraw()
            appAux = AppPhotoCombox(item_list=list_photo, callback=self.handle_selected_images)
            self.wait_window(appAux)
            self.destroy()
        else:
            self.cancel(select_data,id_register)


    def cancel(self, select_data,id_register):
        global image_base64
        self.withdraw()

        path = filedialog.askopenfilename(
            title="Selecciona una imagen",
            filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )

        if path:
            # Cargar la imagen seleccionada
            imagen = Image.open(path)
            original_width, original_height = imagen.size
            # Calcular el nuevo ancho manteniendo la proporción
            aspect_ratio = original_width / original_height
            new_width = int(200 * aspect_ratio)
            imagen = imagen.resize((new_width, 200))
            # Convertir la imagen a un objeto BytesIO
            buffered = BytesIO()
            imagen.save(buffered, format="PNG")
            # Codificar la imagen a Base64
            image_base64 = base64.b64encode(buffered.getvalue()).decode()
            imagen.close()
            id_project = get_id_item_bd(select_data[0], select_data[1], "tbl_proyectos", select_data[2],
                                        "codigo", select_data[2])
            type_photo = 'emplazamiento'
            id_type_photo = get_id_item_bd(select_data[0], select_data[1], "tbl_inv_foto_tipo", select_data[2],
                                        "tipo_foto", type_photo)

            data=(str(id_project),str(id_register),str(id_type_photo),image_base64,path)
            #añadimos foto a la base de datos
            add_photo_site_register(select_data[0], select_data[1], select_data[2], data)
            self.destroy()
            return image_base64

        else:
            CTkMessagebox(title="Warning Message!", message="No se ha seleccionado ningún archivo",
                          icon="warning")


    def handle_selected_images(self,selected_image):
        global image_base64
        image_base64 = selected_image


    def get_result(self):
        return image_base64



