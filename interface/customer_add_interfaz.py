import customtkinter
from PIL import Image, ImageTk
import base64
from io import BytesIO
from tkinter import filedialog
from script.modulo_db  import add_customer_item
from interface.base import BaseWindow
from interface.components import show_success, show_warning
import os

# Obtener la ruta actual
current_path = os.path.dirname(os.path.realpath(__file__))

# Subir un nivel en la estructura de carpetas
parent_path = os.path.dirname(current_path)

customtkinter.set_appearance_mode("dark")

image_base64=None

class AppCustomerAdd(BaseWindow):
    width = 800
    height = 450

    def __init__(self, access):
        super().__init__(title="Registro de empresas")
        global image_base64
        password = access[1]
        user = access[0]

        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        common_fg_color = "#171717"

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        #almacena nombre empresa
        self.name_customer_label = customtkinter.CTkLabel(self, text="NOMBRE EMPRESA:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.name_customer_label.grid(row=0, column=0, padx=(30,5), pady=(30,10), sticky= "e")
        self.name_customer_entry = customtkinter.CTkEntry(self, placeholder_text="añada nombre de la empresa",
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.name_customer_entry.grid(row=0, column=1, padx=(5,30), pady=(30,10), sticky= "ew", columnspan=3)

        #almacena cif empresa
        self.cif_customer_label = customtkinter.CTkLabel(self, text="CIF:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.cif_customer_label.grid(row=1, column=0, padx=(30,5), pady=(10,10), sticky= "e")
        self.cif_customer_entry = customtkinter.CTkEntry(self, placeholder_text="añada CIF de la empresa",
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.cif_customer_entry.grid(row=1, column=1, padx=(5,30), pady=(10,10), sticky= "ew", columnspan=3)

        #almacena direccion empresa
        self.street_customer_label = customtkinter.CTkLabel(self, text="DIRECCIÓN:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.street_customer_label.grid(row=2, column=0, padx=(30,5), pady=(10,10), sticky= "e")
        self.street_customer_entry = customtkinter.CTkEntry(self, placeholder_text="añada la dirección de la empresa",
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.street_customer_entry.grid(row=2, column=1, padx=(5,30), pady=(10,10), sticky= "ew", columnspan=3)

        #almacena municipio empresa
        self.locality_customer_label = customtkinter.CTkLabel(self, text="MUNICIPIO:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.locality_customer_label.grid(row=3, column=0, padx=(30,5), pady=(10,10), sticky= "e")
        self.locality_customer_entry = customtkinter.CTkEntry(self, placeholder_text="añada el municipio  de la empresa",
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.locality_customer_entry.grid(row=3, column=1, padx=(5,30), pady=(10,10), sticky= "ew", columnspan=3)

        #almacena c.postal empresa
        self.cp_customer_label = customtkinter.CTkLabel(self, text="C.POSTAL:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.cp_customer_label.grid(row=4, column=0, padx=(30,5), pady=(10,10), sticky= "e")
        self.cp_customer_entry = customtkinter.CTkEntry(self, placeholder_text="añada el código postal de la empresa",
                                                         fg_color=common_fg_color,text_color="#FFFFFF", width=200)
        self.cp_customer_entry.grid(row=4, column=1, padx=(5,5), pady=(10,10), sticky= "ew")

        #almacena telefono empresa
        self.phone_customer_label = customtkinter.CTkLabel(self, text="TELÉFONO:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.phone_customer_label.grid(row=4, column=2, padx=(5,5), pady=(10,10), sticky= "e")
        self.phone_customer_entry = customtkinter.CTkEntry(self, placeholder_text="telefono de la empresa",
                                                         fg_color=common_fg_color,text_color="#FFFFFF", width=200)
        self.phone_customer_entry.grid(row=4, column=3, padx=(5,30), pady=(10,10), sticky= "ew")

        # almacena logo empresa
        self.lg_customer_label = customtkinter.CTkLabel(self, text="LOGO:", anchor="e",
                                                           font=customtkinter.CTkFont(size=15, weight="bold"),
                                                           width=50)
        self.lg_customer_label.grid(row=5, column=0, padx=(30, 5), pady=(10, 10), sticky="e")

        #Insertamos imagen base
        image_base64 = """
                iVBORw0KGgoAAAANSUhEUgAAAFAAAABQCAYAAACOEfKtAAAACXBIWXMAAAsTAAALEwEAmpwYAAADY0lEQVR4nO2c/U9SURzG/fuyF7dWzim63PKXFtbMpmkuFTdSW2uufhFflmkupTcyCWWDtCkZ6ogU5nZxGmpZ4BtZrXzauVgjQEEOl3v1fp/t2YV77s493w/PefmJrCwSiUQikUgkkqpV0WQA2ZA0AwLYJBFA0v4igJwigJwigJwigJwigJwigJwigHIDHBCOthOJAAoEEJRAQf6pSlNYIICQO220iQgEEHInjo4xAgGEkkwHaYEAghIoREHwAa+Xgak14MMW4A2Fr1PB8H3Wrog+lTCFzfOAfQkYXQ5frYvA+w3A+21vs/ahheSLZM8m0yd7d+RY2NgUC/ClD3B8ATyh/QvbyzNbgCUJiOwZ9mwq72Bjc6yGxyorQOtHYDIAuDbCV/F7MLWiIj0dBAbngdGVcH8sRczsM7vH2qbX+N/D+otXQ0YA2vz8BXj38WwotbZ0mNUmOcBEa4/3EJvVJjlAqVPgldGsNskBOgPyF+qVyO8CGQDIM8DJ1e9otc5B22LHQ8ei7MDiWZEARxY2cPuZG+f0Fmh05n+u7XZi4tO27NAUC3B4LoC6HicKI6BF+3zjsJhGTwrFekI7GJxZQX3XKPKv96LV4hbvHWqAntAOTO7PqGwb3xNaPFd1OjDmDyVVpM0XwJ3nThTU9OLYRcN/vnDLBJsQOHwA3eu/xCSV3h05ELhIF98cQoddwGycFE2shMSEleifxkCL9vHSduh7x+AK/lQ+wKmvP8SNoaTZmjK4aLP0vlncEn+UR+MCyu9ZRCiJwEU7r6oHD0bmlAlwfCmEloFZFOuH0gYu0oUNZuRW9x8YWjyzH2DMv6kMgHbfOhofu1DU8EoScNHOu2HCycv3uSHmlHWK6+bM5m95AWYCmibGgzhT2YdsbRs3yKK6PphcfrUBNKc1jdlaA2o6bHCubqsLoGbXZ6v6ka09+KYS7dNXu2LOjqoAqNGZkV/7AqfKutKyyUSeHVUDUMNc/zeN/GvjiUvtaDa+VRlA3W4a6waQc6U7LWlUJUDNrnOrn3CvjaoGqNGZUcDSWN6tXIDXjGtH2olEAI0EEJRAo/xTlaawkQBC7rTRJmIkgFDdMUbtqiCAfCKAnCKAnCKAnCKAnCKAnCKAUgMkG+jf2yoyEISYBJJIJBKJRCKRstSkPxan6ndmzY4HAAAAAElFTkSuQmCC
                """
        image = Image.open(BytesIO(base64.b64decode(image_base64)))
        self.lg_image = customtkinter.CTkImage(image, size=(80,80))
        self.lg_image_label = customtkinter.CTkLabel(self, text=" ", image=self.lg_image, height=80)
        self.lg_image_label.grid(row=5, column=1, padx=30, pady=(15, 15), columnspan =2)
        # Crear un botón para añadir logo
        self.lg_button = customtkinter.CTkButton(self, text="Añadir Logo",
                                                 font=("default", 14, "bold"), command=self.select_logo, width=50)
        self.lg_button.grid(row=5, column=3, padx=(10,30), pady=10, sticky= "ew")

        # Espaciamos botones de guardar y cancelar
        self.grid_rowconfigure(6, weight=1)

        # boton de guardar
        save_path = parent_path +"/source/guardar.png"
        self.save_image = customtkinter.CTkImage(Image.open(save_path))
        self.save_button = customtkinter.CTkButton(self, text="Guardar",image=self.save_image, compound="left",fg_color="green",
                                                   font=("default", 14, "bold"),
                                                   command=lambda: self.save(access),  height=40)
        self.save_button.grid(row=7, column=0, padx=(30,1), pady=10, sticky= "ew", columnspan =2)

        # boton de cancelar
        cancel_path = parent_path +"/source/cancelar.png"
        self.cancel_image = customtkinter.CTkImage(Image.open(cancel_path))
        self.cancel_button = customtkinter.CTkButton(self, text="Cancelar",image=self.cancel_image, compound="left",fg_color="red",
                                                   font=("default", 14, "bold"),
                                                   command=self.cancel,  height=40)
        self.cancel_button.grid(row=7, column=2, padx=(10,30), pady=10, sticky= "ew", columnspan =2)

        self.lift()



    def select_logo(self):
        global image_base64
        #abrir cuadro de dialogo para seleccionar la imagen
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
            # Acutalizar imagen en la ventana
            self.lg_image = customtkinter.CTkImage(image,size=(new_width,80))
            self.lg_image_label.configure(image=self.lg_image)
            image.close()

        else:
            show_warning("No se ha seleccionado ningún archivo")
                          
    def save(self, access):
        global image_base64
        password = access[1]
        user = access[0]
        #recolecatamos los datos
        data = {
            "name": self.name_customer_entry.get(),
            "cif": self.cif_customer_entry.get(),
            "street": self.street_customer_entry.get(),
            "locality": self.locality_customer_entry.get(),
            "cp": self.cp_customer_entry.get(),
            "phone": self.phone_customer_entry.get(),
            "img": image_base64
        }
        #insertamos los datos en la bbdd
        add_customer_item(user, password, data)
        #mostramos mensage de confirmacion y cerramos ventana
        mssg="Se ha añadido a la base de datos "+data["name"]
        self.destroy()
        show_success(mssg)

