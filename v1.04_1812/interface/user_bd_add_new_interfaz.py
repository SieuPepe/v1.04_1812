import customtkinter
from PIL import Image
from tkinter import StringVar
from script.modulo_db  import create_user_bd, create_pass
from interface.base import BaseWindow
from interface.components import show_success, show_info
import os

# Obtener la ruta actual
current_path = os.path.dirname(os.path.realpath(__file__))

# Subir un nivel en la estructura de carpetas
parent_path = os.path.dirname(current_path)

customtkinter.set_appearance_mode("dark")

class AppUserBdAddNew(BaseWindow):
    width = 400
    height = 350

    def __init__(self, access):
        super().__init__(title="Añadir nuevo usuario de la base de datos")

        self.user_value = StringVar()
        self.pass_value = StringVar()

        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        common_fg_color = "#171717"

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #almacena nombre del usuario
        self.name_label = customtkinter.CTkLabel(self, text="NOMBRE:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.name_label.grid(row=0, column=0, padx=(30,5), pady=(30,10), sticky= "nwes")
        self.name_entry = customtkinter.CTkEntry(self, placeholder_text="añada nombre del usuario",
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.name_entry.grid(row=0, column=1, padx=(5,30), pady=(30,10), sticky= "nwes")

        #almacena apellidos del usuario
        self.surname_label = customtkinter.CTkLabel(self, text="APELIIDOS:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.surname_label.grid(row=1, column=0, padx=(30,5), pady=(10,10), sticky= "e")
        self.surname_entry = customtkinter.CTkEntry(self, placeholder_text="añada apellidos del usuario",
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.surname_entry.grid(row=1, column=1, padx=(5,30), pady=(10,10), sticky= "ew")

        #boton para que te genere la contraseña y el usuario con la misma metodología
        self.generate_button = customtkinter.CTkButton(self, text="Generar usuario y contraseña",  compound="left",
                                                   font=("default", 14, "bold"),
                                                   command=lambda: self.generate(), height=40)
        self.generate_button.grid(row=2, column=0, padx=(30, 30), pady=10, sticky="ew", columnspan=2)

        # almacena usuario de la bbbdd
        self.user_label = customtkinter.CTkLabel(self, text="USUARIO:",
                                                             anchor="e",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"),
                                                             width=50)
        self.user_label.grid(row=3, column=0, padx=(30, 5), pady=(10, 10), sticky="e")
        self.user_entry = customtkinter.CTkEntry(self, textvariable=self.user_value,placeholder_text="añada apellidos del usuario",
                                                             fg_color=common_fg_color, text_color="#FFFFFF",
                                                             state="readonly")
        self.user_entry.grid(row=3, column=1, padx=(5, 30), pady=(10, 10), sticky="ew")

        # almacena la constraseña de la bbdd
        self.password_label = customtkinter.CTkLabel(self, text="CONTRASEÑA:",
                                                             anchor="e",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"),
                                                             width=50)
        self.password_label.grid(row=4, column=0, padx=(30, 5), pady=(10, 10), sticky="e")
        self.password_entry = customtkinter.CTkEntry(self, textvariable=self.pass_value,placeholder_text="añada apellidos del usuario",
                                                             fg_color=common_fg_color, text_color="#FFFFFF",
                                                             state="readonly")
        self.password_entry.grid(row=4, column=1, padx=(5, 30), pady=(10, 10), sticky="ew")


        # Espaciamos botones de guardar y cancelar
        self.grid_rowconfigure(5, weight=1)

        # boton de guardar
        save_path = parent_path +"/source/ok.png"
        self.save_image = customtkinter.CTkImage(Image.open(save_path))
        self.save_button = customtkinter.CTkButton(self, text="Aceptar",image=self.save_image, compound="left",fg_color="green",
                                                   font=("default", 14, "bold"),
                                                   command=lambda: self.save(access),  height=40)
        self.save_button.grid(row=6, column=0, padx=(30,1), pady=10, sticky= "ew")

        # boton de cancelar
        cancel_path = parent_path +"/source/cancelar.png"
        self.cancel_image = customtkinter.CTkImage(Image.open(cancel_path))
        self.cancel_button = customtkinter.CTkButton(self, text="Cancelar",image=self.cancel_image, compound="left",fg_color="red",
                                                   font=("default", 14, "bold"),
                                                   command=self.cancel,  height=40)
        self.cancel_button.grid(row=6, column=1, padx=(10,30), pady=10, sticky= "ew")

        self.lift()


    def generate (self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()

        name_split = name.split(" ")
        name_clean=[elemento for elemento in name_split if elemento.strip()]
        surname_split = surname.split(" ")
        surname_clean = [elemento for elemento in surname_split if elemento.strip()]

        user=""
        if len(name_clean)>1:
            for i in range(len(name_clean)):
                user+=name_clean[i][0]
        else:
            user += name_clean[0][0]

        for i in range(len(surname_clean)):
            if i == 0:
                user += surname_clean[0]
            elif i >= 1:
                user += surname_clean[i][0]

        #inserta el valor del usario y la contraseña creados
        self.user_value.set(user.lower())
        self.pass_value.set(create_pass())

        # mostramos mensage de confirmacion y cerramos ventana
        mssg = f"¡¡¡IMPORTANTE!!!! Recuerde copiar el usuario y la contraseña en un bloc de notas, antes de Aceptar"
        show_info(mssg)

    def save(self, access):
        password = access[1]
        user = access[0]
        user_db=self.user_entry.get()
        password_db=self.password_entry.get()

        #crea el usuario en la bbdd
        create_user_bd(user,password,user_db,password_db)

        #mostramos mensage de confirmacion y cerramos ventana
        mssg=f"Se ha añadido a la base de datos el usuario: "+user_db+ " . Lo tiene disponible para seleccionar y añadir al proyecto."
        self.destroy()
        show_success(mssg)








