import customtkinter
from PIL import Image
from CTkMessagebox import CTkMessagebox
from script.modulo_db import add_item_aux
import os

# Obtener la ruta actual
current_path = os.path.dirname(os.path.realpath(__file__))

# Subir un nivel en la estructura de carpetas
parent_path = os.path.dirname(current_path)

customtkinter.set_appearance_mode("dark")

class AppItemAdd(customtkinter.CTkToplevel): #Toplevel
    width = 400
    height = 180

    def __init__(self, select_data, table,field,type):
        super().__init__()

        self.title("Añadir item")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        common_fg_color = "#171717"

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #almacena item
        self.item_label = customtkinter.CTkLabel(self, text=type,
                                                         anchor="center", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.item_label.grid(row=0,  padx=10, pady=10, sticky= "news", columnspan=2)

        self.item_entry = customtkinter.CTkEntry(self, placeholder_text="añada "+type,
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.item_entry.grid(row=1, padx=10, pady=10, sticky= "news", columnspan=2)

        self.grid_rowconfigure(2,weight=1)

        # boton de guardar
        save_path = parent_path +"/source/guardar.png"
        self.save_image = customtkinter.CTkImage(Image.open(save_path))
        self.save_button = customtkinter.CTkButton(self, text="Guardar",image=self.save_image, compound="left",fg_color="green",
                                                   font=("default", 14, "bold"),
                                                   command=lambda: self.save(select_data,table,field),  height=40)
        self.save_button.grid(row=3, column=0, padx=(30,10), pady=(10,30), sticky= "ew")

        # boton de cancelar
        cancel_path = parent_path +"/source/cancelar.png"
        self.cancel_image = customtkinter.CTkImage(Image.open(cancel_path))
        self.cancel_button = customtkinter.CTkButton(self, text="Cancelar",image=self.cancel_image, compound="left",fg_color="red",
                                                   font=("default", 14, "bold"),
                                                   command=self.cancel,  height=40)
        self.cancel_button.grid(row=3, column=1, padx=(10,30), pady=(10,30), sticky= "ew")

        self.lift()


    def cancel(self):
        self.destroy()


    def save(self, select_data,table,field):
        item=self.item_entry.get()
        result=add_item_aux(select_data[0], select_data[1], table, select_data[2], field, item)
        if result=='ok':
            mssg="Se ha añadido a la base de datos."
            self.destroy()
            CTkMessagebox(title="Successfull Message!", message=mssg,
                          icon="check")
        else:
            mssg="ERROR: "+str(result)
            self.destroy()
            CTkMessagebox(title="Error Message!", message=mssg,
                          icon="cancel")

