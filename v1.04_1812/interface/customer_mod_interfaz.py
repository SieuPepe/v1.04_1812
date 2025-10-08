import customtkinter
from PIL import Image
import base64
from io import BytesIO
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
import tkinter as tk
from script.modulo_db  import get_customer_data ,mod_customer_item, get_id_item_bd
import os

# Obtener la ruta actual
current_path = os.path.dirname(os.path.realpath(__file__))

# Subir un nivel en la estructura de carpetas
parent_path = os.path.dirname(current_path)

customtkinter.set_appearance_mode("dark")
image_base64=None

class AppCustomerMod(customtkinter.CTkToplevel):
    width = 800
    height = 450

    def __init__(self, select_data):
        super().__init__()
        global image_base64
        password = select_data[1]
        user = select_data[0]
        customer =select_data[2]


        self.title("Modificación de empresa seleccionada")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        common_fg_color = "#171717"

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        customer_data=get_customer_data(user, password, customer)
        self.select_customer = [tk.StringVar(value=data) for data in customer_data]

        #almacena nombre empresa
        self.name_customer_label = customtkinter.CTkLabel(self, text="NOMBRE EMPRESA:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.name_customer_label.grid(row=0, column=0, padx=(30,5), pady=(30,10), sticky= "e")
        self.name_customer_entry = customtkinter.CTkEntry(self, textvariable= self.select_customer[1],
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.name_customer_entry.grid(row=0, column=1, padx=(5,30), pady=(30,10), sticky= "ew", columnspan=3)

        #almacena cif empresa
        self.cif_customer_label = customtkinter.CTkLabel(self, text="CIF:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.cif_customer_label.grid(row=1, column=0, padx=(30,5), pady=(10,10), sticky= "e")
        self.cif_customer_entry = customtkinter.CTkEntry(self, textvariable= self.select_customer[2],
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.cif_customer_entry.grid(row=1, column=1, padx=(5,30), pady=(10,10), sticky= "ew", columnspan=3)

        #almacena direccion empresa
        self.street_customer_label = customtkinter.CTkLabel(self, text="DIRECCIÓN:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.street_customer_label.grid(row=2, column=0, padx=(30,5), pady=(10,10), sticky= "e")
        self.street_customer_entry = customtkinter.CTkEntry(self, textvariable= self.select_customer[3],
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.street_customer_entry.grid(row=2, column=1, padx=(5,30), pady=(10,10), sticky= "ew", columnspan=3)

        #almacena municipio empresa
        self.locality_customer_label = customtkinter.CTkLabel(self, text="MUNICIPIO:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.locality_customer_label.grid(row=3, column=0, padx=(30,5), pady=(10,10), sticky= "e")
        self.locality_customer_entry = customtkinter.CTkEntry(self, textvariable= self.select_customer[4],
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.locality_customer_entry.grid(row=3, column=1, padx=(5,30), pady=(10,10), sticky= "ew", columnspan=3)

        #almacena c.postal empresa
        self.cp_customer_label = customtkinter.CTkLabel(self, text="C.POSTAL:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.cp_customer_label.grid(row=4, column=0, padx=(30,5), pady=(10,10), sticky= "e")
        self.cp_customer_entry = customtkinter.CTkEntry(self, textvariable= self.select_customer[5],                                                         fg_color=common_fg_color,text_color="#FFFFFF", width=200)
        self.cp_customer_entry.grid(row=4, column=1, padx=(5,5), pady=(10,10), sticky= "ew")

        #almacena telefono empresa
        self.phone_customer_label = customtkinter.CTkLabel(self, text="TELÉFONO:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.phone_customer_label.grid(row=4, column=2, padx=(5,5), pady=(10,10), sticky= "e")
        self.phone_customer_entry = customtkinter.CTkEntry(self, textvariable= self.select_customer[6],
                                                         fg_color=common_fg_color,text_color="#FFFFFF", width=200)
        self.phone_customer_entry.grid(row=4, column=3, padx=(5,30), pady=(10,10), sticky= "ew")

        # almacena logo empresa
        self.lg_customer_label = customtkinter.CTkLabel(self, text="LOGO:",
                                                           anchor="e",
                                                           font=customtkinter.CTkFont(size=15, weight="bold"),
                                                           width=50)
        self.lg_customer_label.grid(row=5, column=0, padx=(30, 5), pady=(10, 10), sticky="e")

        image_base64 = customer_data[7].replace("'",'"""')
        padding_needed = len(image_base64) % 4

        if padding_needed:
            image_base64 += '=' * (4 - padding_needed)
            image_data = base64.b64decode(image_base64)
            image = Image.open(BytesIO(image_data))
        else:
            image = Image.open(BytesIO(base64.b64decode(image_base64)))

        original_width, original_height = image.size
        # Calcular el nuevo ancho manteniendo la proporción
        aspect_ratio = original_width / original_height
        new_width = int(80 * aspect_ratio)
        # Convertir a PhotoImage
        self.lg_image = customtkinter.CTkImage(image, size=(new_width, 80))
        self.lg_image_label = customtkinter.CTkLabel(self, text=" ", image=self.lg_image, height=80)
        self.lg_image_label.grid(row=5, column=1, padx=30, pady=(15, 15), columnspan =2)
        # Crear un botón para abrir el diálogo de selección de directorio
        self.lg_button = customtkinter.CTkButton(self, text="Añadir Logo",
                                                 font=("default", 14, "bold"), command=self.select_file, width=50)
        self.lg_button.grid(row=5, column=3, padx=(10,30), pady=10, sticky= "ew")

        self.grid_rowconfigure(6, weight=1)

        # boton de guardar
        save_path = parent_path +"/source/guardar.png"
        self.save_image = customtkinter.CTkImage(Image.open(save_path))
        self.save_button = customtkinter.CTkButton(self, text="Guardar",image=self.save_image, compound="left",fg_color="green",
                                                   font=("default", 14, "bold"),
                                                   command=lambda: self.save(select_data),  height=40)
        self.save_button.grid(row=7, column=0, padx=(30,1), pady=10, sticky= "ew", columnspan =2)

        # boton de cancelar
        cancel_path = parent_path +"/source/cancelar.png"
        self.cancel_image = customtkinter.CTkImage(Image.open(cancel_path))
        self.cancel_button = customtkinter.CTkButton(self, text="Cancelar",image=self.cancel_image, compound="left",fg_color="red",
                                                   font=("default", 14, "bold"),
                                                   command=self.cancel,  height=40)
        self.cancel_button.grid(row=7, column=2, padx=(10,30), pady=10, sticky= "ew", columnspan =2)

        self.lift()



    def select_file(self):
        global image_base64

        path = filedialog.askopenfilename(
                title="Selecciona una imagen",
                filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
            )
        
        if path:
            # Cargar la imagen seleccionada
            imagen = Image.open(path)
            # Convertir la imagen a un objeto BytesIO
            buffered = BytesIO()
            imagen.save(buffered, format="PNG")
            # Codificar la imagen a Base64
            image_base64 = base64.b64encode(buffered.getvalue()).decode()
            # Convertir Base64 a Image
            image_data = base64.b64decode(image_base64)
            image = Image.open(BytesIO(image_data))
            original_width, original_height = image.size
            # Calcular el nuevo ancho manteniendo la proporción
            aspect_ratio = original_width / original_height
            new_width = int(80 * aspect_ratio)
            # Convertir a PhotoImage
            self.lg_image = customtkinter.CTkImage(image,size=(new_width,80))
            self.lg_image_label.configure(image=self.lg_image)
            image.close()
        else:
            CTkMessagebox(title="Warning Message!", message="No se ha seleccionado ningún archivo",
                          icon="warning")
                          


    def cancel(self):
        self.destroy()


    def save(self, select_data):
        global image_base64
        password = select_data[1]
        user = select_data[0]
        select_customer = select_data[2]
        id_customer = get_id_item_bd(user, password, 'tbl_cliente', 'manager', 'nombre', select_customer)
        data = {
            "name": self.name_customer_entry.get(),
            "cif": self.cif_customer_entry.get(),
            "street": self.street_customer_entry.get(),
            "locality": self.locality_customer_entry.get(),
            "cp": self.cp_customer_entry.get(),
            "phone": self.phone_customer_entry.get(),
            "img": image_base64
        }
        mod_customer_item(user, password, data, id_customer)
        mssg="Se ha modificado en la base de datos el cliente: "+data["name"]
        self.destroy()
        CTkMessagebox(title="Successfull Message!", message=mssg,
                      icon="check")

