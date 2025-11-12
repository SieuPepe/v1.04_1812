import customtkinter
from PIL import Image
from script.modulo_db  import add_user_company_item
from interface.base import BaseWindow
from interface.components import show_success
import os

# Obtener la ruta actual
current_path = os.path.dirname(os.path.realpath(__file__))

# Subir un nivel en la estructura de carpetas
parent_path = os.path.dirname(current_path)

customtkinter.set_appearance_mode("dark")

class AppUserCompanyAddNew(BaseWindow):
    width = 600
    height = 300

    def __init__(self, access, on_save_callback=None):
        super().__init__(title="Registro de responsable")

        self.on_save_callback = on_save_callback

        self.title("Registro de responsable")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        common_fg_color = "#171717"

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        #almacena nombre responable
        self.name_customer_label = customtkinter.CTkLabel(self, text="NOMBRE:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.name_customer_label.grid(row=0, column=0, padx=(30,5), pady=(30,10), sticky= "e")
        self.name_customer_entry = customtkinter.CTkEntry(self, placeholder_text="añada nombre del responsable",
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.name_customer_entry.grid(row=0, column=1, padx=(5,30), pady=(30,10), sticky= "ew", columnspan=3)

        #almacena apellidos
        self.surname_customer_label = customtkinter.CTkLabel(self, text="APELLIDOS:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.surname_customer_label.grid(row=1, column=0, padx=(30,5), pady=(10,10), sticky= "e")
        self.surname_customer_entry = customtkinter.CTkEntry(self, placeholder_text="añada apellidos del responsable",
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.surname_customer_entry.grid(row=1, column=1, padx=(5,30), pady=(10,10), sticky= "ew", columnspan=3)

        #almacena dirección email
        self.email_customer_label = customtkinter.CTkLabel(self, text="EMAIL:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.email_customer_label.grid(row=2, column=0, padx=(30,5), pady=(10,10), sticky= "e")
        self.email_customer_entry = customtkinter.CTkEntry(self, placeholder_text="añada email de contacto",
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.email_customer_entry.grid(row=2, column=1, padx=(5,30), pady=(10,10), sticky= "ew", columnspan=3)

        #almacena teléfono de contacto
        self.phone_customer_label = customtkinter.CTkLabel(self, text="CONTACTO:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.phone_customer_label.grid(row=3, column=0, padx=(30,5), pady=(10,10), sticky= "e")
        self.phone_customer_entry = customtkinter.CTkEntry(self, placeholder_text="añada teléfono de contacto",
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.phone_customer_entry.grid(row=3, column=1, padx=(5,30), pady=(10,10), sticky= "ew", columnspan=3)

        # Espaciamos botones de guardar y cancelar
        self.grid_rowconfigure(4, weight=1)

        # boton de guardar
        save_path = parent_path +"/resources/images/guardar.png"
        self.save_image = customtkinter.CTkImage(Image.open(save_path))
        self.save_button = customtkinter.CTkButton(self, text="Guardar",image=self.save_image, compound="left",fg_color="green",
                                                   font=("default", 14, "bold"),
                                                   command=lambda: self.save(access),  height=40)
        self.save_button.grid(row=7, column=0, padx=(30,1), pady=10, sticky= "ew", columnspan =2)

        # boton de cancelar
        cancel_path = parent_path +"/resources/images/cancelar.png"
        self.cancel_image = customtkinter.CTkImage(Image.open(cancel_path))
        self.cancel_button = customtkinter.CTkButton(self, text="Cancelar",image=self.cancel_image, compound="left",fg_color="red",
                                                   font=("default", 14, "bold"),
                                                   command=self.cancel,  height=40)
        self.cancel_button.grid(row=7, column=2, padx=(10,30), pady=10, sticky= "ew", columnspan =2)

        self.lift()


    def save(self, access):
        password = access[1]
        user = access[0]

        #recolecatamos los datos
        data = {
            "name": self.name_customer_entry.get(),
            "surname": self.surname_customer_entry.get(),
            "email": self.email_customer_entry.get(),
            "phone": self.phone_customer_entry.get(),
        }
        #insertamos los datos en la bbdd
        add_user_company_item(user, password, data)
        #mostramos mensage de confirmacion y cerramos ventana
        mssg="Se ha añadido un NUEVO RESPONSABLE a la base de datos: "+data["name"]+' '+data["surname"]
        self.destroy()
        show_success(mssg)
        # Llamamos al callback para actualizar la ventana principal
        if self.on_save_callback:
            self.on_save_callback()

