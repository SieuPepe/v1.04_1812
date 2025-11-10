import customtkinter
from interface.user_project_interfaz import AppUserProject
from script.modulo_db import get_schemas_db

customtkinter.set_appearance_mode("dark")

class AppSelectProject(customtkinter.CTk):
    width = 400
    height = 200

    def __init__(self, access):
        super().__init__()

        self.title("HydroFlow Manager")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)



        self.grid_columnconfigure(0,weight=1)
        self.select_label = customtkinter.CTkLabel(self,
                                                         text="SELECCIONAR CÓDIGO DE PROYECTO",
                                                         anchor="center", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width=50)
        self.select_label.grid(row=0, padx=(30, 30), pady=(30,10), sticky="news")

        #crea seleccionable para elegir proyecto
        schemas = get_schemas_db(access[0], access[1])
        schema_filter = [elemento for elemento in schemas if all(exclude not in elemento for exclude in ["power_bi","cert_dev","_schema", "manager", "mysql", "sys"])]
        self.project_option = customtkinter.CTkOptionMenu(self,
                                                           dynamic_resizing=False,
                                                           values=schema_filter)
        self.project_option.grid(row=1,  padx=(30,30), pady=(10,30), sticky= "news")

        self.ok_button = customtkinter.CTkButton(self, text="Abrir proyecto", command=lambda:self.project_event(access), width=200)
        self.ok_button.grid(row=2, padx=(30,30), pady=(10,30), sticky= "news")
      

    def project_event(self, access):
        password = access[1]
        user = access[0]
        select_project = self.project_option.get()
        select_data = [user, password, select_project]

        self.withdraw()
        app = AppUserProject(self, select_data)
        app.mainloop()

