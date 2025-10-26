import customtkinter
from PIL import Image
from script.modulo_db import login_db
from interface.typeUser_interfaz import AppTypeUser
from CTkMessagebox import CTkMessagebox
import os

# Obtener la ruta actual
current_path = os.path.dirname(os.path.realpath(__file__))

# Subir un nivel en la estructura de carpetas
parent_path = os.path.dirname(current_path)

customtkinter.set_appearance_mode("dark")

class AppLogin(customtkinter.CTk):
    width = 1200
    height = 700


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("HydroFlow Manager")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        # load and create background image
        image_path = parent_path +"/source/fondo.jpeg"
        self.bg_image = customtkinter.CTkImage(Image.open(image_path),
                                               size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # create login frame
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.login_frame.grid(row=0, column=0, sticky="ns")
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="Inicio Sesión",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=30, pady=(150, 15))
        self.username_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="usuario")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        self.password_entry = customtkinter.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="contraseña")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", command=self.login_event, width=200)
        self.login_button.grid(row=3, column=0, padx=30, pady=(15, 15))

        self.login_frame.grid_rowconfigure(4, weight=1)

        image_logo_path = parent_path +"/source/logo artanda2.png"
        self.lg_image = customtkinter.CTkImage(Image.open(image_logo_path), size=(200,44))
        self.lg_image_label = customtkinter.CTkLabel(self.login_frame, text=" ",image=self.lg_image)
        self.lg_image_label.grid(row=5, column=0, padx=30, pady=(15, 15))


    def login_event(self):
        user = self.username_entry.get()
        password = self.password_entry.get()
        access = [user, password]
        db, error = login_db(user, password)

        # check connection
        if db:
            self.destroy()
            app = AppTypeUser(access)
            app.mainloop()

            return access

        else:
            mssg = f"Error al conectar a la base de datos:\n{str(error)} "
            CTkMessagebox(title="Warning Message!", message=mssg,
                          icon="warning")
