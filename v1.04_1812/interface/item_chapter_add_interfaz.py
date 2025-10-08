import customtkinter
from PIL import Image
from CTkMessagebox import CTkMessagebox
from script.modulo_db import add_item_chapter, get_id_item_bd
import os

# Obtener la ruta actual
current_path = os.path.dirname(os.path.realpath(__file__))

# Subir un nivel en la estructura de carpetas
parent_path = os.path.dirname(current_path)

customtkinter.set_appearance_mode("dark")

class AppItemChapterAdd(customtkinter.CTkToplevel): #Toplevel
    width = 650
    height = 250

    def __init__(self, select_data):
        super().__init__()

        self.title("Añadir capítulo")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        common_fg_color = "#171717"

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # almacena precio
        self.code_label = customtkinter.CTkLabel(self, text="CÓDIGO CAPÍTULO:",
                                                  anchor="e", font=customtkinter.CTkFont(size=13, weight="bold"),
                                                  width=50)
        self.code_label.grid(row=0, column=0, padx=(30, 5), pady=10, sticky="e")
        self.code_entry = customtkinter.CTkEntry(self, placeholder_text="añada código",
                                                  fg_color=common_fg_color, text_color="#FFFFFF")
        self.code_entry.grid(row=0, column=1, padx=(5, 30), pady=10, sticky="ew")

        # almacena descripción
        self.description_label = customtkinter.CTkLabel(self, text="NOMBRE CAPÍTULO:",
                                                        anchor="e", font=customtkinter.CTkFont(size=13, weight="bold"),
                                                        width=50)
        self.description_label.grid(row=1, column=0, padx=(30, 5), pady=(10, 10), sticky="e")
        self.description_entry = customtkinter.CTkTextbox(self, fg_color=common_fg_color, height=100,
                                                          border_width=2, border_color="#565B5E", text_color="#FFFFFF")
        self.description_entry.grid(row=1, column=1, padx=(5, 30), pady=(10, 10), sticky="ew")

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_BOTONES_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        # boton de guardar
        save_path = parent_path +"/source/guardar.png"
        self.save_image = customtkinter.CTkImage(Image.open(save_path))
        self.save_button = customtkinter.CTkButton(self, text="Guardar", image=self.save_image, compound="left",
                                                   fg_color="green",
                                                   font=("default", 14, "bold"),
                                                   command=lambda: self.save(select_data), height=40)
        self.save_button.grid(row=3, column=0, padx=(30, 1), pady=10, sticky="ew")

        # boton de cancelar
        cancel_path = parent_path +"/source/cancelar.png"
        self.cancel_image = customtkinter.CTkImage(Image.open(cancel_path))
        self.cancel_button = customtkinter.CTkButton(self, text="Cancelar", image=self.cancel_image, compound="left",
                                                     fg_color="red",
                                                     font=("default", 14, "bold"),
                                                     command=self.cancel, height=40)
        self.cancel_button.grid(row=3, column=1, padx=(10, 30), pady=10, sticky="ew")

        self.lift()


    def cancel(self):
        self.destroy()


    def save(self, select_data):
        code=self.code_entry.get()
        id_type=get_id_item_bd(select_data[0], select_data[1], 'tbl_pres_naturaleza', select_data[2],
                                 'tipo', 'Capítulo')
        description=self.description_entry.get("1.0", "end-1c")
        data=[code,id_type,description]

        result=add_item_chapter(select_data[0], select_data[1], select_data[2], data)

        if result=='ok':
            mssg="Se ha añadido el capítulo a la base de datos."
            self.destroy()
            CTkMessagebox(title="Successfull Message!", message=mssg,
                          icon="check")
        else:
            mssg="ERROR: "+str(result)
            self.destroy()
            CTkMessagebox(title="Error Message!", message=mssg,
                          icon="cancel")

