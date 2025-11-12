import customtkinter
from PIL import Image
from interface.manager_interfaz import AppManager
from interface.select_project_interfaz import AppSelectProject
from script.modulo_db import manager_db, user_db, get_schemas_db
from CTkMessagebox import CTkMessagebox
from interface.parts_interfaz import AppParts
import os

# Obtener la ruta actual
current_path = os.path.dirname(os.path.realpath(__file__))

# Subir un nivel en la estructura de carpetas
parent_path = os.path.dirname(current_path)


customtkinter.set_appearance_mode("dark")

class AppTypeUser(customtkinter.CTk):
    width = 1200
    height = 700

    def __init__(self, access):
        super().__init__()

        self.title("HydroFlow Manager")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        # load and create background image
        image_path = parent_path +"/resources/images/fondo.jpeg"
        self.bg_image = customtkinter.CTkImage(Image.open(image_path),
                                               size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, text='', image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # create frame
        self.select_frame = customtkinter.CTkFrame(self, corner_radius=0, height= 500)
        self.select_frame.place(relx=0.5, rely=0.5, anchor="center")

        image_logo_path = parent_path +"/resources/images/logo artanda2.png"
        self.lg_image = customtkinter.CTkImage(Image.open(image_logo_path), size=(200,44))
        self.lg_image_label = customtkinter.CTkLabel(self.select_frame, text=" ",image=self.lg_image)
        self.lg_image_label.grid(row=0, column=0, padx=30, pady=(15, 15), columnspan=2)

        user_path = parent_path +"/resources/images/tecnico.png"
        self.user_image = customtkinter.CTkImage(Image.open(user_path),
                                               size=(100, 100))
        self.user_image_label = customtkinter.CTkLabel(self.select_frame, text='', image=self.user_image)
        self.user_image_label.grid(row=1, column=0, padx=30, pady=(15, 5))
        self.user_button = customtkinter.CTkButton(self.select_frame, text="Técnico", command=lambda:self.user_event(access), width=200)
        self.user_button.grid(row=2, column=0, padx=30, pady=(15, 15))

        manager_path = parent_path +"/resources/images/manager.png"
        self.admin_image = customtkinter.CTkImage(Image.open(manager_path),
                                               size=(100, 100))
        self.admin_label = customtkinter.CTkLabel(self.select_frame,  text='',image=self.admin_image)
        self.admin_label.grid(row=1, column=1, padx=30, pady=(15, 5))
        self.admin_button = customtkinter.CTkButton(self.select_frame, text="Administrador de proyecto", command=lambda:self.manager_event(access), width=200)
        self.admin_button.grid(row=2, column=1, padx=30, pady=(15, 15))
        # --- NUEVO: botón Generador de partes ---
        self.parts_button = customtkinter.CTkButton(
            self.select_frame,
            text="Generador de partes",
            command=lambda: self.parts_event(access),
            width=200
        )
        self.parts_button.grid(row=2, column=2, padx=30, pady=(15, 15))

    def manager_event(self, access):
        password = access[1]
        user = access[0]
        db, error = manager_db(user, password)

        if db:
            self.destroy()
            app = AppManager(access)
            app.mainloop()
        else:
            mssg = f"Acceso denegado al módulo de gestión de proyectos, ponte en contacto con un administrador"
            CTkMessagebox(title="Warning Message!", message=mssg,
                          icon="warning")

    def parts_event(self, access):
        """Abrir selector de proyecto para Generador de Partes"""
        try:
            from script.db_config import DatabaseConfig
            user, password = access[0], access[1]
            schemas = get_schemas_db(user, password)
            # Solo permitir esquemas válidos para el generador de partes
            schemas = [s for s in schemas if s in DatabaseConfig.VALID_PARTS_GENERATOR_SCHEMAS]

            if not schemas:
                CTkMessagebox(
                    title="Aviso",
                    message="No tienes acceso a ningún proyecto.\nContacta con un administrador.",
                    icon="warning"
                )
                return

            # Si solo hay 1 esquema, abrir directamente
            if len(schemas) == 1:
                from interface.parts_manager_interfaz import AppPartsManager
                self.destroy()
                app = AppPartsManager(access, schemas[0])
                app.mainloop()
            else:
                # Si hay múltiples proyectos, usar el primero por ahora
                # TODO: Implementar selector de proyectos
                from interface.parts_manager_interfaz import AppPartsManager
                self.destroy()
                app = AppPartsManager(access, schemas[0])
                app.mainloop()

        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo abrir Generador de partes:\n{e}", icon="warning")
    def user_event(self, access):
        password = access[1]
        user = access[0]
        db, error = user_db(user, password)
        schemas = get_schemas_db(user, password)
        schemas = [item for item in schemas if item not in ['information_schema', 'performance_schema']]
        if db:
            if len(schemas)==0:
                mssg = f"No se ha encontrado ningún proyecto al que tenga acceso, contacte con algún administrador"
                CTkMessagebox(title="Warning Message!", message=mssg,
                              icon="warning")
            else:
                self.destroy()
                app = AppSelectProject(access)
                app.mainloop()
        else:
            mssg = f"Error al conectar a la base de datos:\n{str(error)} "
            CTkMessagebox(title="Warning Message!", message=mssg,
                          icon="warning")