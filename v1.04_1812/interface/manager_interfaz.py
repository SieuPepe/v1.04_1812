import shutil
import subprocess
import sys
import pyperclip
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
from script.catalog_import import catalog_import
from script.certification_export import export_monthly_certification
from script.modulo_db import (get_ccaa_bd, get_code_ccaa_bd, get_province_bd, get_option_item_bd, get_item_id_bd,
                              get_option_item_sub_bd, get_id_user_customer, get_id_user_company, get_user_db,
                              add_project_item,create_schemas_db, get_table_schemas_db,create_tables_schema_db,
                              get_id_province_bd, get_id_ccaa_bd, copy_tables_schema_db,update_reference,add_privileges,
                              create_locality_schema_db,get_filter_data_bd,add_economic_project_item, create_view_projects,
                              add_item_chapter,create_view_catalog,create_view_inventory,get_all_bd, revoke_privileges,
                              change_pass_user, sum_field_bd,sum_field_filter_bd, create_view_economic,mod_project_item)
from script.budget_import import budget_import
from interface.customer_add_interfaz import *
from interface.customer_mod_interfaz import *
from interface.user_customer_add_interfaz import *
from interface.user_customer_mod_interfaz import *
from interface.user_customer_add_new_interfaz import *
from interface.user_company_add_interfaz import *
from interface.user_company_mod_interfaz import *
from interface.user_company_add_new_interfaz import *
from interface.combox_interfaz import *
from interface.user_bd_add_new_interfaz import *
from interface.select_manager_project_interfaz import *


# Obtener la ruta actual
current_path = os.path.dirname(os.path.realpath(__file__))

# Subir un nivel en la estructura de carpetas
parent_path = os.path.dirname(current_path)

customtkinter.set_appearance_mode("dark")
data_user_bd=[]
user_privileges = {}

class AppManager(customtkinter.CTk):
    width = 1500
    height = 800

    def __init__(self, access):
        super().__init__()

        self.user = access[0]
        self.password =access[1]

        self.title("HydroFlow Manager")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)


        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # cargar imagenes de iconos
        image_logo_path = parent_path +"/source/logo artanda2.png"
        self.lg_image = customtkinter.CTkImage(Image.open(image_logo_path), size=(200, 44))
        new_project_path = parent_path +"/source/proyecto.png" #quitar punto cuando ya no este en pruebas
        self.new_project_image = customtkinter.CTkImage(Image.open(new_project_path),
                                                 size=(30, 30))
        project_path = parent_path +"/source/herramienta.png"#quitar punto cuando ya no este en pruebas
        self.project_image = customtkinter.CTkImage(Image.open(project_path),
                                                 size=(30, 30))
        user_path = parent_path +"/source/usuarios.png" #quitar punto cuando ya no este en pruebas
        self.user_image = customtkinter.CTkImage(Image.open(user_path),
                                                      size=(30, 30))
        cost_path = parent_path +"/source/certificaciones.png" #quitar punto cuando ya no este en pruebas
        self.cost_image = customtkinter.CTkImage(Image.open(cost_path),
                                                      size=(30, 30))


        # ----------------------FRAME MENU LATERAL-------------------------------------------------------------------
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0, width=200)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")

        #.......................elementos frame menu lateral............................................................
        self.lg_image_label = customtkinter.CTkLabel(self.navigation_frame, text=" ", image=self.lg_image)
        self.lg_image_label.grid(row=0, column=0, padx=30, pady=(15, 15))

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Gestión de proyectos",
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=18, weight="bold"))
        self.navigation_frame_label.grid(row=1, column=0, padx=20, pady=5)

        self.new_project_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                        border_spacing=10, text="Nuevo proyecto", fg_color="transparent",
                                                        text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray30"), image=self.new_project_image,
                                                        font=customtkinter.CTkFont(size=15, weight="bold"),
                                                        anchor="w", command=lambda :self.new_project_button_event(access))
        self.new_project_button.grid(row=2, column=0, sticky="ew")

        self.project_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                        border_spacing=10, text="Gestión de proyectos", fg_color="transparent",
                                                        text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray30"), image=self.project_image,
                                                        font=customtkinter.CTkFont(size=15, weight="bold"),
                                                        anchor="w", command=lambda :self.project_button_event(access))
        self.project_button.grid(row=3, column=0, sticky="ew")

        self.user_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                        border_spacing=10, text="Usuarios", fg_color="transparent",
                                                        text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray30"), image=self.user_image,
                                                        font=customtkinter.CTkFont(size=15, weight="bold"),
                                                        anchor="w", command=lambda :self.user_button_event(access))
        self.user_button.grid(row=4, column=0, sticky="ew")

        self.cost_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                        border_spacing=10, text="Certificaciones", fg_color="transparent",
                                                        text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray30"), image=self.cost_image,
                                                        font=customtkinter.CTkFont(size=15, weight="bold"),
                                                        anchor="w", command=lambda :self.cost_button_event(access))
        self.cost_button.grid(row=5, column=0, sticky="ew")

        # Espaciador vacío para empujar el botón hacia abajo
        self.navigation_frame.grid_rowconfigure(6, weight=1)
        self.view_project_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=5, height=40,
                                                        border_spacing=10, text="Ver proyectos",
                                                        text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray30"),
                                                        font=("default", 14, "bold"),
                                                        anchor="center", command=lambda:self.view_project_button_event(access))
        self.view_project_button.grid(row=7,padx=30, pady=(15, 15),sticky="nsew")

        #crea inicialmente los frame de las pestañas
        self.new_project_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.project_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.user_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.cost_frame = customtkinter.CTkFrame(self, corner_radius=0)

        #genera las vistas de las pestañas
        self.main_new_project(access)
        self.main_manager_project(access)
        self.main_manager_user(access)
        self.main_manager_cost(access)

        # select default frame
        self.select_frame_by_name("new_project")



    #------------------------------------FUNCIONES---------------------------------------------------------------

    # ----------------------ACCIONES VENTANA - VISUAL-------------------------------------------------------------------

    def main_new_project (self,access):

        # ----------------------FRAME NUEVO PROYECTO-------------------------------------------------------------------
        self.new_project_frame.grid_columnconfigure(0, weight=1)
        self.new_project_frame.grid_rowconfigure(0, weight=1)

        #.......................elementos frame nuevo proyecto............................................................
        #crear tabview para los distintos apartados
        self. tab_view= customtkinter.CTkTabview(self.new_project_frame)
        self.tab_view.grid(row=0,column=0, padx=30, pady=(15, 15), sticky="nsew", columnspan=4)
        custom_font = ("default", 16, "bold")
        self.tab_view.add("Datos Generales")
        self.tab_view.add("Datos Económicos")
        self.tab_view.add("Cliente")
        self.tab_view.add("Usuarios BD")
        self.tab_view.add("Referencias")
        # Aplicar la fuente personalizada a cada pestaña
        self.tab_view.tab("Datos Generales").grid_propagate(False)
        self.tab_view.tab("Datos Económicos").grid_propagate(False)
        self.tab_view.tab("Cliente").grid_propagate(False)
        self.tab_view.tab("Usuarios BD").grid_propagate(False)
        self.tab_view.tab("Referencias").grid_propagate(False)
        self.tab_view._segmented_button.configure(font=custom_font)

        #_____________________________añadir elementos por tab - Datos generales______________________________________
        self.tab_view.tab("Datos Generales").grid_columnconfigure(0, weight=1)
        self. tab_view.tab("Datos Generales").grid_columnconfigure(1, weight=10)

        #color predefinido para las letras
        common_fg_color = "#171717"

        #almacena código proyecto
        self.code_project_label = customtkinter.CTkLabel(self.tab_view.tab("Datos Generales"), text="CÓDIGO PROYECTO *:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.code_project_label.grid(row=0, column=0, padx=(30,10), pady=10, sticky= "e")
        self.code_project_entry = customtkinter.CTkEntry(self.tab_view.tab("Datos Generales"), placeholder_text="añada el código del proyecto",
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.code_project_entry.grid(row=0, column=1, padx=(5,30), pady=10, sticky= "ew", columnspan=2)

        #almacena  nombre proyecto
        self.name_project_label = customtkinter.CTkLabel(self.tab_view.tab("Datos Generales"), text="NOMBRE PROYECTO *:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.name_project_label.grid(row=1, column=0, padx=(30,10), pady=10, sticky= "e")
        self.name_project_entry = customtkinter.CTkEntry(self.tab_view.tab("Datos Generales"), placeholder_text="añada el nombre del proyecto",
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.name_project_entry.grid(row=1, column=1, padx=(5,30), pady=10, sticky= "ew", columnspan=2)

        #almacena descripción proyecto
        self.description_project_label = customtkinter.CTkLabel(self.tab_view.tab("Datos Generales"), text="DESCRIPCIÓN PROYECTO:",
                                                                anchor="e",font=customtkinter.CTkFont(size=15, weight="bold"),
                                                                width= 50)
        self.description_project_label.grid(row=2, column=0, padx=(30,10), pady=10, sticky= "e")
        self.description_project_entry = customtkinter.CTkTextbox(self.tab_view.tab("Datos Generales"), fg_color=common_fg_color,
                                                                  border_width=2, border_color="#565B5E",text_color="#FFFFFF")
        self.description_project_entry.grid(row=2, column=1, padx=(5,30), pady=10, sticky= "ew", columnspan=2)

        #almacena directorio de trabajo
        self.folder_project_label = customtkinter.CTkLabel(self.tab_view.tab("Datos Generales"), text="CARPETA DE LA APLICACIÓN  EN EL PROYECTO *:",
                                                           anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                           width= 50)
        self.folder_project_label.grid(row=3, column=0, padx=(30, 10), pady=10, sticky="e")
        # Crear un Entry para mostrar la ruta del directorio
        self.folder_project_entry = customtkinter.CTkEntry(self.tab_view.tab("Datos Generales"),fg_color=common_fg_color,
                                                           placeholder_text="Selecciona un directorio",text_color="#FFFFFF")
        self.folder_project_entry.grid(row=3, column=1, padx=(5,30), pady=10, sticky= "ew")
        # Crear un botón para abrir el diálogo de selección de directorio
        self.folder_project_button = customtkinter.CTkButton(self.tab_view.tab("Datos Generales"), text="Seleccionar Directorio",
                                                             command=self.select_directory, width=50)
        self.folder_project_button.grid(row=3, column=2, padx=(5,30), pady=10, sticky= "ew")

        # almacena CCAA del proyecto
        self.ccaa_project_label = customtkinter.CTkLabel(self.tab_view.tab("Datos Generales"), text="COMUNIDAD AUTÓNOMA:",
                                                           anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                           width= 50)
        self.ccaa_project_label.grid(row=4, column=0, padx=(30, 10), pady=10, sticky="e")
        ccaa_value=get_ccaa_bd(self.user, self.password)
        self.ccaa_option = customtkinter.CTkOptionMenu(self.tab_view.tab("Datos Generales"),
                                                         dynamic_resizing=False,
                                                         values=ccaa_value,
                                                         command= lambda event:self.update_province_options(access))
        self.ccaa_option.grid(row=4, column=1, padx=(5,30), pady=10, sticky= "ew", columnspan=2)

        select_ccaa = self.ccaa_option.get()
        code_ccaa = get_code_ccaa_bd(self.user, self.password, select_ccaa)

        #almacena provincia del proyect
        self.province_project_label = customtkinter.CTkLabel(self.tab_view.tab("Datos Generales"), text="PROVINCIA:",
                                                           anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                           width= 50)
        self.province_project_label.grid(row=5, column=0, padx=(30, 10), pady=10, sticky="e")
        province_value = get_province_bd(self.user, self.password, code_ccaa)
        self.province_option = customtkinter.CTkOptionMenu(self.tab_view.tab("Datos Generales"),
                                                           dynamic_resizing=False,
                                                           values=province_value)
        self.province_option.grid(row=5, column=1, padx=(5,30), pady=10, sticky= "ew", columnspan=2)
        self.ccaa_option.bind("<<ComboboxSelected>>", lambda event: self.update_province_options(access))
        self.province_option.set(province_value[0])


        self.tab_view.tab("Datos Generales").grid_rowconfigure(6,weight=1)
        self.note_label=customtkinter.CTkLabel(self.tab_view.tab("Datos Generales"), text="* Campos obligatorios para rellenar",
                                                           anchor="e", font=customtkinter.CTkFont(size=12),
                                                           width= 50)
        self.note_label.grid(row=7, column=0, padx=(30, 10), pady=10, sticky="nwes", columnspan=3)


        # almacenas las opciones de los responsables disponibles del adjudicatario en la bbdd
        id_users_company = get_option_item_bd(access[0], access[1], "tbl_empr_usuario", "manager", 'id')
        if len(id_users_company) == 0:
            self.user_company_frame = customtkinter.CTkFrame(self.tab_view.tab("Datos Generales"), corner_radius=0)
            self.user_company_frame.grid(row=6, padx=(10, 10), pady=(10, 10), sticky="nsew",columnspan=3)
            self.user_company_frame.grid_columnconfigure(0, weight=10)

            self.user_company_project_label = customtkinter.CTkLabel(self.user_company_frame,
                                                                     text="No se ha registrado ningún responsable, por favor añada un responsable para la compañia",
                                                                     anchor="center",
                                                                     font=customtkinter.CTkFont(size=15,
                                                                                                weight="bold"),
                                                                     width=50)
            self.user_company_project_label.grid(row=0, column=0, padx=(30, 10), pady=10, sticky="news",
                                                 columnspan=3)

            # Botón para añadir responsable del cliente
            self.add_user_company_button = customtkinter.CTkButton(self.user_company_frame,
                                                                   text="Añadir Responsable",
                                                                   command=lambda: self.add_user_company_first(access),
                                                                   width=100)
            self.add_user_company_button.grid(row=1, column=0, padx=(10, 30), pady=(10, 30), sticky="ew",
                                              columnspan=3)
        else:
            self.user_company_frame = customtkinter.CTkFrame(self.tab_view.tab("Datos Generales"), corner_radius=0)
            self.user_company_frame.grid(row=6, padx=(10, 10), pady=(10, 10), sticky="nsew",columnspan=3)
            self.user_company_frame.grid_columnconfigure(0, weight=10)
            self.user_company_frame.grid_columnconfigure(1, weight=1)
            self.user_company_frame.grid_columnconfigure(2, weight=1)

            self.user_company_project_label = customtkinter.CTkLabel(self.user_company_frame,
                                                                     text="RESPONSABLE PROYECTO",
                                                                     anchor="center",
                                                                     font=customtkinter.CTkFont(size=15,
                                                                                                weight="bold"))
            self.user_company_project_label.grid(row=0, column=0, padx=(30, 10), pady=10, sticky="news",
                                                 columnspan=3)
            users_value = []
            for item in id_users_company:
                user_surname_value = get_option_item_sub_bd(access[0], access[1], "tbl_empr_usuario", "manager",
                                                            'apellidos',
                                                            item, 'id')
                user_name_value = get_option_item_sub_bd(access[0], access[1], "tbl_empr_usuario", "manager",
                                                         'nombre',
                                                         item, 'id')
                value = user_surname_value[0] + ", " + user_name_value[0]
                users_value.append(value)
            users_value.sort(key=str.lower)
            self.user_company_option = customtkinter.CTkOptionMenu(self.user_company_frame,
                                                                   dynamic_resizing=False,
                                                                   values=users_value)
            self.user_company_option.grid(row=1, column=0, padx=(30, 30), pady=(10, 30), sticky="ew")

            # Botón para añadir responsable del cliente
            self.add_user_company_button = customtkinter.CTkButton(self.user_company_frame,
                                                                   text="Añadir Responsable",
                                                                   command=lambda: self.add_user_company(access),
                                                                   width=100)
            self.add_user_company_button.grid(row=1, column=1, padx=(10, 30), pady=(10, 30), sticky="ew")

            # Botón para modificar responsable del cliente
            self.update_company_button = customtkinter.CTkButton(self.user_company_frame,
                                                                 text="Modificar Responsable",
                                                                 command=lambda: self.mod_user_company(access),
                                                                 width=100)
            self.update_company_button.grid(row=1, column=2, padx=(10, 30), pady=(10, 30), sticky="ew")


        self.note_label = customtkinter.CTkLabel(self.tab_view.tab("Datos Generales"),
                                                 text="* Campos obligatorios para rellenar",
                                                 anchor="e", font=customtkinter.CTkFont(size=12),
                                                 width=50)
        self.note_label.grid(row=7, column=0, padx=(30, 10), pady=10, sticky="nwes", columnspan=3)

        #_____________________________añadir elementos por tab - Datos económicos______________________________________
        self.tab_view.tab("Datos Económicos").grid_columnconfigure(0, weight=1)
        self.tab_view.tab("Datos Económicos").grid_columnconfigure(1, weight=10)

        #color predefinido para las letras
        common_fg_color = "#171717"

        switch_var = customtkinter.StringVar(value="base")
        self.economic_switch = customtkinter.CTkSwitch(self.tab_view.tab("Datos Económicos"),
                                                       text="¿Desea definir los parámetros del presupuesto de licitación?",
                                                       switch_width=50, switch_height=20, command=self.switch_economic,
                                                       variable=switch_var, onvalue="pem", offvalue="base",
                                                       font=customtkinter.CTkFont(size=15, weight="bold"))
        self.economic_switch.grid(row=0, column=0, padx=(30, 10), pady=(30, 10), sticky="nwes", columnspan=2)

        # almacena presupuesto de licitación
        self.tender_project_label = customtkinter.CTkLabel(self.tab_view.tab("Datos Económicos"),
                                                           text="PRESUPUESTO DE LICITACIÓN (SIN IVA):",
                                                           anchor="e",
                                                           font=customtkinter.CTkFont(size=15, weight="bold"),
                                                           width=50)
        self.tender_project_label.grid(row=1, column=0, padx=(30, 10), pady=10, sticky="e")
        self.tender_project_entry = customtkinter.CTkEntry(self.tab_view.tab("Datos Económicos"),
                                                           placeholder_text="añada el presupuesto  de licitación del proyecto",
                                                           fg_color=common_fg_color, text_color="#FFFFFF")
        self.tender_project_entry.grid(row=1, column=1, padx=(5, 30), pady=10, sticky="ew")

        # almacena baja de licitación
        self.reduction_project_label = customtkinter.CTkLabel(self.tab_view.tab("Datos Económicos"),
                                                              text="% BAJA:",
                                                              anchor="e",
                                                              font=customtkinter.CTkFont(size=15, weight="bold"),
                                                              width=50)
        self.reduction_project_label.grid(row=2, column=0, padx=(30, 10), pady=10, sticky="e")
        self.reduction_project_entry = customtkinter.CTkEntry(self.tab_view.tab("Datos Económicos"),
                                                              placeholder_text="añada la baja del proyecto",
                                                              fg_color=common_fg_color, text_color="#FFFFFF")
        self.reduction_project_entry.grid(row=2, column=1, padx=(5, 30), pady=10, sticky="ew")

        self.economic_frame = customtkinter.CTkFrame(self.tab_view.tab("Datos Económicos"), corner_radius=0)
        self.economic_frame.grid(row=3, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew",columnspan=2)
        self.economic_frame.grid_columnconfigure(0, weight=1)
        self.economic_frame.grid_columnconfigure(1, weight=10)

        if self.economic_switch.get()=="pem":
            # almacena gasto generales
            self.gg_project_label = customtkinter.CTkLabel(self.economic_frame,
                                                             text="% GASTOS GENERALES:",
                                                             anchor="e",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"),
                                                             width=50)
            self.gg_project_label.grid(row=0, column=0, padx=(30, 10), pady=10, sticky="e")
            self.gg_project_entry = customtkinter.CTkEntry(self.economic_frame,
                                                             placeholder_text="añada los gastos generales del proyecto",
                                                             fg_color=common_fg_color, text_color="#FFFFFF")
            self.gg_project_entry.grid(row=0, column=1, padx=(5, 30), pady=10, sticky="ew")

            # almacena beneficio industrial
            self.bi_project_label = customtkinter.CTkLabel(self.economic_frame,
                                                             text="% BENEFICIO INDUSTRIAL:",
                                                             anchor="e",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"),
                                                             width=50)
            self.bi_project_label.grid(row=1, column=0, padx=(30, 10), pady=10, sticky="e")
            self.bi_project_entry = customtkinter.CTkEntry(self.economic_frame,
                                                             placeholder_text="añada el benedicio industrial del proyecto",
                                                             fg_color=common_fg_color, text_color="#FFFFFF")
            self.bi_project_entry.grid(row=1, column=1, padx=(5, 30), pady=10, sticky="ew")

            # almacena IVA
            self.iva_project_label = customtkinter.CTkLabel(self.economic_frame,
                                                           text="% IVA:",
                                                           anchor="e",
                                                           font=customtkinter.CTkFont(size=15, weight="bold"),
                                                           width=50)
            self.iva_project_label.grid(row=2, column=0, padx=(30, 10), pady=10, sticky="e")
            self.iva_project_entry = customtkinter.CTkEntry(self.economic_frame,
                                                           placeholder_text="añada el IVA del proyecto",
                                                           fg_color=common_fg_color, text_color="#FFFFFF")
            self.iva_project_entry.grid(row=2, column=1, padx=(5, 30), pady=10, sticky="ew")
        else:
            self.default1_project_label = customtkinter.CTkLabel(self.economic_frame,
                                                               text=f"Por defecto, se aplicará los siguientes gastos sobre el presupuesto de ejecución material:",
                                                               anchor="e",
                                                               font=customtkinter.CTkFont(size=15),
                                                               width=50)
            self.default1_project_label.grid(row=0, column=0, padx=(30, 10), pady=10, sticky="w")
            self.default2_project_label = customtkinter.CTkLabel(self.economic_frame,
                                                               text=f"- Gastos generales: 13%",
                                                               anchor="e",
                                                               font=customtkinter.CTkFont(size=15, weight="bold"),
                                                               width=50)
            self.default2_project_label.grid(row=1, column=0, padx=(30, 10), pady=10, sticky="w")
            self.default3_project_label = customtkinter.CTkLabel(self.economic_frame,
                                                               text=f"- Beneficio industrial: 6% ",
                                                               anchor="e",
                                                               font=customtkinter.CTkFont(size=15, weight="bold"),
                                                               width=50)
            self.default3_project_label.grid(row=2, column=0, padx=(30, 10), pady=10, sticky="w")
            self.default4_project_label = customtkinter.CTkLabel(self.economic_frame,
                                                                 text=f"- IVA: 21% ",
                                                                 anchor="e",
                                                                 font=customtkinter.CTkFont(size=15, weight="bold"),
                                                                 width=50)
            self.default4_project_label.grid(row=3, column=0, padx=(30, 10), pady=10, sticky="w")

        #_____________________________añadir elementos por tab - Cliente______________________________________
        self.tab_view.tab("Cliente").grid_columnconfigure(0, weight=1)
        self. tab_view.tab("Cliente").grid_columnconfigure(1, weight=10)
        self.tab_view.tab("Cliente").grid_columnconfigure(2, weight=1)
        self.tab_view.tab("Cliente").grid_columnconfigure(3, weight=1)

        # almacena cliente del proyecto
        self.customer_project_label = customtkinter.CTkLabel(self.tab_view.tab("Cliente"), text="SELECCIÓN DE CLIENTE:",
                                                           anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                           width= 50)
        self.customer_project_label.grid(row=1, column=0, padx=(30, 10), pady=10, sticky="e")
        customer_value=get_option_item_bd(self.user, self.password, "tbl_cliente", "manager", 'nombre')
        self.customer_option = customtkinter.CTkOptionMenu(self.tab_view.tab("Cliente"),
                                                         dynamic_resizing=False,
                                                         values=customer_value,
                                                         command= lambda event:self.update_customer_data(access))
        self.customer_option.grid(row=1, column=1, padx=(5,30), pady=10, sticky= "ew")
        self.customer_option.bind("<<ComboboxSelected>>", lambda event: self.update_customer_data(access))

        # Crear un botón para añadir cliente
        self.add_customer_button = customtkinter.CTkButton(self.tab_view.tab("Cliente"), text="Añadir Cliente",
                                                             command=lambda: self.add_customer(access), width=100)
        self.add_customer_button.grid(row=1, column=2, padx=(10,30), pady=10, sticky= "ew")

        # Crear un botón para modificar cliente
        self.update_customer_button = customtkinter.CTkButton(self.tab_view.tab("Cliente"), text="Modificar Cliente",
                                                             command=lambda: self.mod_customer(access), width=100)
        self.update_customer_button.grid(row=1, column=3, padx=(10,30), pady=10, sticky= "ew")

        #_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME DATOS CLIENTE_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.customer_frame = customtkinter.CTkFrame(self.tab_view.tab("Cliente"), corner_radius=0, width=200)
        self.customer_frame.grid(row=2, column=0, padx=(10,10), pady=(10,10),sticky="nsew", columnspan=4)
        self.customer_frame.grid_columnconfigure(0, weight=1)

        self.customer_data_label = customtkinter.CTkLabel(self.customer_frame, text="DATOS CLIENTE",
                                                             anchor="center",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"),
                                                             width=50)
        self.customer_data_label.grid(row=0, padx=(10, 10), pady=10, sticky="news")

        self.customer_data_frame = customtkinter.CTkFrame(self.customer_frame, corner_radius=0, width=200)
        self.customer_data_frame.grid(row=1, padx=(10,10), pady=(10,10),sticky="nsew")

        #Recopila los datos del cliente seleccionado de la bbdd para añadirlos en los entry
        customer_data=get_customer_data(self.user, self.password, self.customer_option.get())
        self.select_customer = [tk.StringVar(value=data) for data in customer_data]

        #devuelve nombre empresa
        self.name_customer_label = customtkinter.CTkLabel(self.customer_data_frame, text="NOMBRE EMPRESA:",
                                                         anchor="e", font=customtkinter.CTkFont(size=14),
                                                         width= 50)
        self.name_customer_label.grid(row=1, column=0, padx=(50,5), pady=(10,10), sticky= "e")
        self.name_customer_entry = customtkinter.CTkEntry(self.customer_data_frame, textvariable= self.select_customer[1],
                                                         fg_color=common_fg_color,text_color="#FFFFFF",state="disabled")
        self.name_customer_entry.grid(row=1, column=1, padx=(5,30), pady=(10,10), sticky= "ew", columnspan=3)

        #devuelve cif empresa
        self.cif_customer_label = customtkinter.CTkLabel(self.customer_data_frame, text="CIF:",
                                                         anchor="e", font=customtkinter.CTkFont(size=14),
                                                         width= 50)
        self.cif_customer_label.grid(row=2, column=0, padx=(50,5), pady=(10,10), sticky= "e")
        self.cif_customer_entry = customtkinter.CTkEntry(self.customer_data_frame, textvariable= self.select_customer[2],
                                                         fg_color=common_fg_color,text_color="#FFFFFF",state="disabled")
        self.cif_customer_entry.grid(row=2, column=1, padx=(5,30), pady=(10,10), sticky= "ew", columnspan=3)

        #devuelve direcciÓn empresa
        self.street_customer_label = customtkinter.CTkLabel(self.customer_data_frame, text="DIRECCIÓN:",
                                                         anchor="e", font=customtkinter.CTkFont(size=14),
                                                         width= 50)
        self.street_customer_label.grid(row=3, column=0, padx=(50,5), pady=(10,10), sticky= "e")
        self.street_customer_entry = customtkinter.CTkEntry(self.customer_data_frame, textvariable= self.select_customer[3],
                                                         fg_color=common_fg_color,text_color="#FFFFFF",state="disabled")
        self.street_customer_entry.grid(row=3, column=1, padx=(5,30), pady=(10,10), sticky= "ew", columnspan=3)

        #devuelve  municipio empresa
        self.locality_customer_label = customtkinter.CTkLabel(self.customer_data_frame, text="MUNICIPIO:",
                                                         anchor="e", font=customtkinter.CTkFont(size=14),
                                                         width= 50)
        self.locality_customer_label.grid(row=4, column=0, padx=(50,5), pady=(10,10), sticky= "e")
        self.locality_customer_entry = customtkinter.CTkEntry(self.customer_data_frame, textvariable= self.select_customer[4],
                                                         fg_color=common_fg_color,text_color="#FFFFFF",state="disabled")
        self.locality_customer_entry.grid(row=4, column=1, padx=(5,30), pady=(10,10), sticky= "ew", columnspan=4)

        #devuelve  c.postal empresa
        self.cp_customer_label = customtkinter.CTkLabel(self.customer_data_frame, text="C.POSTAL:",
                                                         anchor="e", font=customtkinter.CTkFont(size=14),
                                                         width= 50)
        self.cp_customer_label.grid(row=5, column=0, padx=(50,5), pady=(10,10), sticky= "e")
        self.cp_customer_entry = customtkinter.CTkEntry(self.customer_data_frame, textvariable= self.select_customer[5],
                                                        fg_color=common_fg_color,text_color="#FFFFFF", width=200,state="disabled")
        self.cp_customer_entry.grid(row=5, column=1, padx=(5,5), pady=(10,10), sticky= "ew")

        #devuelve  telefono empresa
        self.phone_customer_label = customtkinter.CTkLabel(self.customer_data_frame, text="TELÉFONO:",
                                                         anchor="e", font=customtkinter.CTkFont(size=14),
                                                         width= 50)
        self.phone_customer_label.grid(row=5, column=2, padx=(5,5), pady=(10,10), sticky= "e")
        self.phone_customer_entry = customtkinter.CTkEntry(self.customer_data_frame, textvariable= self.select_customer[6],
                                                         fg_color=common_fg_color,text_color="#FFFFFF", width=200,state="disabled")
        self.phone_customer_entry.grid(row=5, column=3, padx=(5,30), pady=(10,10), sticky= "ew")

        # devuelve  logo empresa
        self.lg_customer_label = customtkinter.CTkLabel(self.customer_data_frame, text="LOGO:",
                                                           anchor="e",
                                                           font=customtkinter.CTkFont(size=14),
                                                           width=50)
        self.lg_customer_label.grid(row=6, column=0, padx=(50, 5), pady=(10, 10), sticky="e")
        #formatea imagen base64 almacenada
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
        self.lg_image_label = customtkinter.CTkLabel(self.customer_data_frame, text=" ", image=self.lg_image, height=80)
        self.lg_image_label.grid(row=6, column=1, padx=30, pady=(15, 15), columnspan =2)

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME RESPONSABLE CLIENTE_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.user_customer_frame = customtkinter.CTkFrame(self.tab_view.tab("Cliente"), corner_radius=0, width=200)
        self.user_customer_frame.grid(row=3, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew", columnspan=4)
        self.user_customer_frame.grid_columnconfigure(0, weight=1)

        #almacenas las opciones de los responsables disponibles del contrato par ala empresa seleccionada
        id_customer = get_id_item_bd(access[0], access[1], "tbl_cliente", "manager", 'nombre',
                                     self.customer_option.get())
        id_users_customer= get_option_item_sub_bd(access[0], access[1], "tbl_clie_usuario", "manager", 'id', id_customer, 'id_cliente')
        if len(id_users_customer) == 0:
            self.user_customer_frame.forget()
            self.user_customer_frame = customtkinter.CTkFrame(self.tab_view.tab("Cliente"), corner_radius=0, width=200)
            self.user_customer_frame.grid(row=3, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew", columnspan=4)
            self.user_customer_frame.grid_columnconfigure(0, weight=1)
            self.user_customer_project_label = customtkinter.CTkLabel(self.user_customer_frame,
                                                                      text="No se ha registrado ningún responsable, por favor añada un responsable para la empresa seleccionada",
                                                                      anchor="center",
                                                                      font=customtkinter.CTkFont(size=15,
                                                                                                 weight="bold"),
                                                                      width=50)
            self.user_customer_project_label.grid(row=0, column=0, padx=(30, 10), pady=10, sticky="news", columnspan=3)

            # Botón para añadir responsable del cliente
            self.add_user_customer_button = customtkinter.CTkButton(self.user_customer_frame, text="Añadir Responsable",
                                                                    command=lambda: self.add_user_customer_first(access),
                                                                    width=100)
            self.add_user_customer_button.grid(row=1, column=0, padx=(10, 30), pady=(10, 30), sticky="ew", columnspan=3)
        else:
            self.user_customer_frame.forget()
            self.user_customer_frame = customtkinter.CTkFrame(self.tab_view.tab("Cliente"), corner_radius=0, width=200)
            self.user_customer_frame.grid(row=3, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew", columnspan=4)
            self.user_customer_frame.grid_columnconfigure(0, weight=1)

            self.user_customer_project_label = customtkinter.CTkLabel(self.user_customer_frame,
                                                                      text="RESPONSABLE CLIENTE",
                                                                      anchor="center",
                                                                      font=customtkinter.CTkFont(size=15,
                                                                                                 weight="bold"),
                                                                      width=50)
            self.user_customer_project_label.grid(row=0, column=0, padx=(30, 10), pady=10, sticky="news", columnspan=3)
            users_customer_value = []
            for item in id_users_customer:
                user_surname_value=get_option_item_sub_bd(access[0], access[1], "tbl_clie_usuario", "manager", 'apellidos',
                                                            item, 'id')
                user_name_value = get_option_item_sub_bd(access[0], access[1], "tbl_clie_usuario", "manager", 'nombre',
                                                            item, 'id')
                value=user_surname_value[0]+", "+user_name_value[0]
                users_customer_value.append(value)
            users_customer_value.sort()
            self.user_customer_option = customtkinter.CTkOptionMenu(self.user_customer_frame,
                                                               dynamic_resizing=False,
                                                               values=users_customer_value)
            self.user_customer_option.grid(row=1, column=0, padx=(30, 30), pady=(10,30), sticky="ew", columnspan=2)
            #self.user_customer_option.bind("<<ComboboxSelected>>", lambda event: self.update_customer_user(access))

            # Botón para añadir responsable del cliente
            self.add_user_customer_button = customtkinter.CTkButton(self.user_customer_frame, text="Añadir Responsable",
                                                               command=lambda: self.add_user_customer(access), width=100)
            self.add_user_customer_button.grid(row=1, column=2, padx=(10, 30), pady=(10,30), sticky="ew")

            # Botón para modificar responsable del cliente
            self.update_customer_button = customtkinter.CTkButton(self.user_customer_frame, text="Modificar Responsable",
                                                                  command=lambda: self.mod_user_customer(access), width=100)
            self.update_customer_button.grid(row=1, column=3, padx=(10, 30), pady=(10,30), sticky="ew")


        # _____________________________añadir elementos por tab - Usuarios BD______________________________________
        self.tab_view.tab("Usuarios BD").grid_columnconfigure(0, weight=1)
        self.tab_view.tab("Usuarios BD").grid_columnconfigure(1, weight=1)
        self.tab_view.tab("Usuarios BD").grid_columnconfigure(2, weight=1)
        self.tab_view.tab("Usuarios BD").grid_rowconfigure(1, weight=1)

        # Botón para seleccionar usuarios BD existentes
        self.select_user_bd_button = customtkinter.CTkButton(self.tab_view.tab("Usuarios BD"), text="Seleccionar usuario existente",
                                                           command=lambda: self.select_user_bd(access), width=100)
        self.select_user_bd_button.grid(row=0, column=0, padx=(30, 5), pady=(10,10), sticky="ew")

        # Botón para elimnar nuevo usuario BD
        self.delete_user_bd_button = customtkinter.CTkButton(self.tab_view.tab("Usuarios BD"), text="Eliminar usuario seleccionado",
                                                              command=lambda: self.delete_user_db(access), width=100)
        self.delete_user_bd_button.grid(row=0, column=1, padx=(5, 5), pady=(10,10), sticky="ew")

        # Botón para añadir nuevo usuario BD
        self.add_user_bd_button = customtkinter.CTkButton(self.tab_view.tab("Usuarios BD"), text="Crear nuevo usuario",
                                                              command=lambda: self.add_user_bd(access), width=100)
        self.add_user_bd_button.grid(row=0, column=2, padx=(5, 30), pady=(10,10), sticky="ew")


        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA TABLA DE USUARIO BD_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.user_bd_frame = customtkinter.CTkScrollableFrame(self.tab_view.tab("Usuarios BD"), corner_radius=0)
        self.user_bd_frame.grid(row=1, padx=(30, 30), pady=(30, 10), sticky="nsew", columnspan=3)
        self.user_bd_frame.grid_columnconfigure(0, weight=1)
        self.user_bd_frame.grid_columnconfigure(1, weight=1)
        self.user_bd_frame.grid_columnconfigure(2, weight=1)

        #cuerpo tabla de usuarios y permisos
        #botón estandar para seleccionar permisos
        privileges_bd_value = ['Seleccione permisos','Administrador', 'Escritura y lectura', 'Solo lectura']
        global data_user_bd
        if len(data_user_bd)==0:
            self.user_bd_label = customtkinter.CTkLabel(self.user_bd_frame, text="Por favor, añada como mínimo un usuario.",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=15, weight="bold"))
            self.user_bd_label.grid(row=0, column=0, padx=(30, 10), pady=50, sticky="nwes", columnspan=3)
        else:
            # encabezados tabla de usuarios y permisos
            self.user_bd_label = customtkinter.CTkLabel(self.user_bd_frame, text="USUARIOS",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=15, weight="bold"))
            self.user_bd_label.grid(row=0, column=0, padx=(30, 10), pady=10, sticky="nwes", columnspan=2)
            self.privileges_bd_label = customtkinter.CTkLabel(self.user_bd_frame, text="PERMISOS",
                                                              anchor="center",
                                                              font=customtkinter.CTkFont(size=15, weight="bold"))
            self.privileges_bd_label.grid(row=0, column=1, padx=(10, 30), pady=10, sticky="nwes")

            for i in range(len(data_user_bd)):
                # según los usuarios que estén almacenados en data_user_bd, añadirá tantas filas como usuarios
                n_row=i+1
                user_db=data_user_bd[i]
                self.user_bd = customtkinter.CTkLabel(self.user_bd_frame, text=user_db,
                                                            anchor="center",
                                                            font=customtkinter.CTkFont(size=14))
                self.user_bd.grid(row=n_row, column=0, padx=(30, 10), pady=10, sticky="nwes", columnspan=2)

                self.user_privilege_option = customtkinter.CTkOptionMenu(self.user_bd_frame,
                                                                         dynamic_resizing=False,
                                                                         values=privileges_bd_value,
                                                                         command=lambda value, user=user_db: self.update_privilege(user, value))
                self.user_privilege_option.grid(row=n_row, column=2, padx=(30, 30), pady=10, sticky="nwes")
                # Establecer el valor predeterminado
                default_value = 'Seleccione permisos'  # Cambia esto al valor predeterminado que quieras
                self.user_privilege_option.set(default_value)


        # _____________________________añadir elementos por tab - Referencias______________________________________

        self.tab_view.tab("Referencias").grid_columnconfigure(1, weight=1)

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA PRESUPUESTO_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.budget_frame = customtkinter.CTkFrame(self.tab_view.tab("Referencias"), corner_radius=0)
        self.budget_frame.grid(row=0, padx=(30, 30), pady=(10, 5), sticky="nsew", columnspan=2)
        self.budget_frame.grid_columnconfigure(0, weight=1)

        self.budget_label = customtkinter.CTkLabel(self.budget_frame, text="PRESUPUESTO BASE",
                                                    anchor="center",
                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
        self.budget_label.grid(row=0, column=0, padx=(30, 10), pady=10, sticky="nwes")

        self.budget_switch = customtkinter.CTkSwitch(self.budget_frame, text="¿Desea utilizar el presupuesto base predeterminado?",
                                                    switch_width=50,switch_height=20, command=self.switch_budget,
                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
        self.budget_switch.grid(row=1, column=0, padx=(30, 10), pady=10, sticky="nwes")

        self.upload_budget_button = customtkinter.CTkButton(self.budget_frame, corner_radius=5, height=40,
                                                        border_spacing=10, text="Añadir presupuesto base",
                                                        text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray30"),
                                                        font=("default", 14, "bold"),
                                                        anchor="center", command=self.add_budget)
        self.upload_budget_button.grid(row=2, column= 0, padx=(30,30), pady=(15, 15),sticky="nsew")

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA CATÁLOGO_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.catalog_frame = customtkinter.CTkFrame(self.tab_view.tab("Referencias"), corner_radius=0)
        self.catalog_frame.grid(row=1, padx=(30, 30), pady=(5, 10), sticky="nsew", columnspan=2)
        self.catalog_frame.grid_columnconfigure(0, weight=1)
        self.catalog_frame.grid_columnconfigure(1, weight=1)

        self.catalog_label = customtkinter.CTkLabel(self.catalog_frame, text="CATÁLOGO DE PIEZAS",
                                                    anchor="center",
                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
        self.catalog_label.grid(row=0, column=0, padx=(30, 10), pady=10, sticky="nwes",columnspan=2)

        self.catalog_switch = customtkinter.CTkSwitch(self.catalog_frame, text="¿Desea utilizar el catálogo predeterminado?",
                                                    switch_width=50,switch_height=20,command=self.switch_catalog,
                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
        self.catalog_switch.grid(row=1, column=0, padx=(30, 10), pady=10, sticky="nwes",columnspan=2)

        self.upload_catalog_button = customtkinter.CTkButton(self.catalog_frame, corner_radius=5, height=40,
                                                        border_spacing=10, text="Añadir catálogo de piezas",
                                                        text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray30"),
                                                        font=("default", 14, "bold"),
                                                        anchor="center", command=self.add_catalog)
        self.upload_catalog_button.grid(row=2, column= 0, padx=(10,30), pady=(15, 15),sticky="nsew")

        self.upload_cadReference_button = customtkinter.CTkButton(self.catalog_frame, corner_radius=5, height=40,
                                                        border_spacing=10, text="Añadir referencias CAD del catálogo",
                                                        text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray30"),
                                                        font=("default", 14, "bold"),
                                                        anchor="center", command=self.add_reference)
        self.upload_cadReference_button.grid(row=2, column= 1, padx=(10,30), pady=(15, 15),sticky="nsew")

        #muestra las rutas de lo elegido
        self.budget_path_label = customtkinter.CTkLabel(self.tab_view.tab("Referencias"), text="Ruta presupuesto base:",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=15, weight="bold"))
        self.budget_path_label.grid(row=2, column=0, padx=(30, 10), pady=10, sticky="w")

        path_budget = "No se ha seleccionado presupuesto"
        self.pathB_label = customtkinter.CTkLabel(self.tab_view.tab("Referencias"), text=path_budget,
                                                  font=customtkinter.CTkFont(size=15))
        self.pathB_label.grid(row=2, column=1, padx=(10, 30), pady=10, sticky="w")

        self.catalog_path_label = customtkinter.CTkLabel(self.tab_view.tab("Referencias"),
                                                         text="Ruta catálogo de piezas:",
                                                         anchor="center",
                                                         font=customtkinter.CTkFont(size=15, weight="bold"))
        self.catalog_path_label.grid(row=3, column=0, padx=(30, 10), pady=5, sticky="w")

        path_catalog = "No se ha seleccionado catálogo"
        self.pathC_label = customtkinter.CTkLabel(self.tab_view.tab("Referencias"), text=path_catalog,
                                                  font=customtkinter.CTkFont(size=15))
        self.pathC_label.grid(row=3, column=1, padx=(30, 10), pady=5, sticky="w")

        self.referenceCad_label = customtkinter.CTkLabel(self.tab_view.tab("Referencias"), text="Ruta referencias CAD:",
                                                         anchor="center",
                                                         font=customtkinter.CTkFont(size=15, weight="bold"))
        self.referenceCad_label.grid(row=4, column=0, padx=(30, 10), pady=10, sticky="w")

        path_referenceCad = "No se ha seleccionado referencias CAD"
        self.pathR_label = customtkinter.CTkLabel(self.tab_view.tab("Referencias"), text=path_referenceCad,
                                                  font=customtkinter.CTkFont(size=15))
        self.pathR_label.grid(row=4, column=1, padx=(10, 30), pady=10, sticky="w")

        self.download_example_button = customtkinter.CTkButton(self.tab_view.tab("Referencias"), corner_radius=5,
                                                               height=40,
                                                               border_spacing=10,
                                                               text="Descargar excel tipo presupuesto y catálogo",
                                                               text_color=("gray10", "gray90"),
                                                               hover_color=("gray70", "gray30"),
                                                               font=("default", 14, "bold"),
                                                               anchor="center", command=self.download_example)
        self.download_example_button.grid(row=5, column=1, padx=(10, 30), pady=10, sticky="nsew")

        self.update_template_dwg_button = customtkinter.CTkButton(self.tab_view.tab("Referencias"), corner_radius=5,
                                                                  height=40,
                                                                  border_spacing=10,
                                                                  text="Actualizar plantilla de Formato A3",
                                                                  text_color=("gray10", "gray90"),
                                                                  hover_color=("gray70", "gray30"),
                                                                  font=("default", 14, "bold"),
                                                                  anchor="center", command=self.update_template)
        self.update_template_dwg_button.grid(row=6, column=1, padx=(10, 30), pady=10, sticky="nsew")

        #bontones para desencadenar añadir los datos recopilados en la bbdd
        self.new_project_frame.grid_columnconfigure(0,weight=1)
        self.save_project_button = customtkinter.CTkButton(self.new_project_frame, corner_radius=5, height=40, width= 400 ,fg_color="green",
                                                        border_spacing=10, text="Crear proyecto",
                                                        text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray30"),
                                                        font=("default", 14, "bold"),
                                                        anchor="center", command=lambda:self.create_project_button_event(access))
        self.save_project_button.grid(row=1, column= 1, padx=(30,30), pady=(10, 15),sticky="w")


    def main_manager_project (self, access):
        self.project_frame.grid_columnconfigure(0, weight=1)
        self.project_frame.grid_columnconfigure(1, weight=1)
        self.project_frame.grid_rowconfigure(1, weight=1)

        n_project = len(get_all_bd(access[0],access[1],'tbl_proyectos','manager'))
        if n_project > 0:
            # filtro para elegir proyecto
            self.project_option_project_label = customtkinter.CTkLabel(self.project_frame,
                                                                    text="SELECCIONAR PROYECTO:",
                                                                    anchor="center",
                                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
            self.project_option_project_label.grid(row=0, column=0, padx=30, pady=(30, 10), sticky="nsew")
            project_data = get_all_bd(access[0], access[1], 'tbl_proyectos', 'manager')
            project_value = []
            for item in project_data:
                project_value.append(item[1] + " - " + item[2])
            self.project_option_project_filter = customtkinter.CTkOptionMenu(self.project_frame,
                                                                          dynamic_resizing=False,
                                                                          values=project_value,
                                                                          command=lambda
                                                                              event: self.project_filter_project_event(access))
            self.project_option_project_filter.grid(row=0, column=1, padx=30, pady=(30, 10), sticky="nsew", columnspan=2)
            self.project_option_project_filter.bind("<<ComboboxSelected>>",
                                                 lambda event: self.project_filter_project_event(access))

            self.data_project_frame = customtkinter.CTkScrollableFrame(self.project_frame, corner_radius=0)
            self.update_data_project_frame_manager(access)

            # boton de guardar
            save_path = parent_path + "/source/guardar.png"
            self.save_image = customtkinter.CTkImage(Image.open(save_path))
            self.save_project_button = customtkinter.CTkButton(self.project_frame, corner_radius=5, height=40, width= 400 ,
                                                            border_spacing=10, text="Guardar cambios", image=self.save_image,
                                                            text_color=("gray10", "gray90"),
                                                            hover_color=("gray70", "gray30"),
                                                            font=("default", 14, "bold"),fg_color="#005e08",
                                                            anchor="center", command=lambda:self.save_project_event(access))
            self.save_project_button.grid(row=2, column= 1, padx=30, pady=(10, 15),sticky="nsew")

        else:
            self.project_option_project_label = customtkinter.CTkLabel(self.project_frame,
                                                                       text="No se ha registrado ningún proyecto en la BBDD, puede acceder en la Pestaña Nuevo Proyecto para dar de alta un nuevo proyecto",
                                                                       anchor="center",
                                                                       font=customtkinter.CTkFont(size=15,
                                                                                                  weight="bold"))
            self.project_option_project_label.grid(row=0, column=0, padx=30, pady=(30, 10), sticky="nsew")


    def main_manager_user(self, access):
        self.user_frame.grid_columnconfigure(0, weight=1)
        self.user_frame.grid_columnconfigure(1, weight=1)
        self.user_frame.grid_columnconfigure(2, weight=1)
        self.user_frame.grid_rowconfigure(2, weight=1)

        n_project = len(get_all_bd(access[0],access[1],'tbl_proyectos','manager'))
        if n_project > 0:
            # filtro para elegir proyecto
            self.project_option_user_label = customtkinter.CTkLabel(self.user_frame,
                                                              text="SELECCIONAR PROYECTO:",
                                                              anchor="center",
                                                              font=customtkinter.CTkFont(size=15, weight="bold"))
            self.project_option_user_label.grid(row=0, column=0, padx=30, pady=(30,10), sticky="nsew")
            project_data = get_all_bd(access[0], access[1], 'tbl_proyectos', 'manager')
            project_value = []
            for item in project_data:
                project_value.append(item[1] + " - " + item[2])
            self.project_option_user_filter = customtkinter.CTkOptionMenu(self.user_frame,
                                                                                dynamic_resizing=False,
                                                                                values=project_value,
                                                                                command=lambda
                                                                                    event: self.project_filter_user_event(access))
            self.project_option_user_filter.grid(row=0, column=1, padx=30, pady=(30,10),  sticky="nsew", columnspan=2)
            self.project_option_user_filter.bind("<<ComboboxSelected>>",
                                                       lambda event: self.project_filter_user_event(access))

            self.user_label = customtkinter.CTkLabel(self.user_frame,
                                                                    text="USUARIOS",
                                                                    anchor="center",
                                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
            self.user_label.grid(row=1, column=0, padx=30, pady=10, sticky="nsew", columnspan=3)

            #recoge proyecto seleccionado
            project_select = self.project_option_user_filter.get()
            code_project_select = project_select .split(" - ")[0]
            code_project_select = str(code_project_select)
            #usuarios para proyecto seleccionado
            privileges_users_project= get_all_bd(access[0], access[1], 'vw_esquema_usuarios', 'manager')
            roles_project = defaultdict(list)
            for item in privileges_users_project:
                if str(item[2]).lower() == code_project_select.lower():
                    user_project=item[0]
                    privilege=item[3]
                    roles_project[user_project].append(privilege)

            # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA USUARIOS_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
            self.data_user_frame = customtkinter.CTkScrollableFrame(self.user_frame, corner_radius=0)
            self.update_data_user_frame_manager(access,roles_project)

            #bontones para desencadenar añadir y eliminar usuarios al proyecto
            self.add_user_button = customtkinter.CTkButton(self.user_frame, corner_radius=5, height=40, width= 400 ,fg_color="green",
                                                            border_spacing=10, text="Añadir usuario",
                                                            text_color=("gray10", "gray90"),
                                                            hover_color=("gray70", "gray30"),
                                                            font=("default", 14, "bold"),
                                                            anchor="center", command=lambda:self.add_user_manager(access))
            self.add_user_button.grid(row=3, column= 0, padx=30, pady=(10, 15),sticky="nsew")
            self.create_user_button = customtkinter.CTkButton(self.user_frame, corner_radius=5, height=40, width= 400 ,
                                                            border_spacing=10, text="Crear nuevo usuario",
                                                            text_color=("gray10", "gray90"),
                                                            hover_color=("gray70", "gray30"),
                                                            font=("default", 14, "bold"),
                                                            anchor="center", command=lambda:self.create_user_manager(access))
            self.create_user_button.grid(row=3, column= 1, padx=30, pady=(10, 15),sticky="nsew")

            self.delete_user_button = customtkinter.CTkButton(self.user_frame, corner_radius=5, height=40, width= 400 ,fg_color="red",
                                                            border_spacing=10, text="Eliminar usuario",
                                                            text_color=("gray10", "gray90"),
                                                            hover_color=("gray70", "gray30"),
                                                            font=("default", 14, "bold"),
                                                            anchor="center", command=lambda:self.delete_user_manager(access))
            self.delete_user_button.grid(row=3, column= 2, padx=30, pady=(10, 15),sticky="nsew")

        else:
            self.project_option_project_label = customtkinter.CTkLabel(self.user_frame,
                                                                       text="No se ha registrado ningún proyecto en la BBDD, puede acceder en la Pestaña Nuevo Proyecto para dar de alta un nuevo proyecto",
                                                                       anchor="center",
                                                                       font=customtkinter.CTkFont(size=15,
                                                                                                  weight="bold"))
            self.project_option_project_label.grid(row=0, column=0, padx=30, pady=(30, 10), sticky="nsew")


    def main_manager_cost(self, access):
        self.cost_frame.grid_columnconfigure(0, weight=1)
        self.cost_frame.grid_columnconfigure(1, weight=1)
        self.cost_frame.grid_columnconfigure(2, weight=1)
        self.cost_frame.grid_rowconfigure(2, weight=1)

        n_project = len(get_all_bd(access[0],access[1],'tbl_proyectos','manager'))
        if n_project > 0:
            # filtro para elegir proyecto
            self.project_option_cost_label = customtkinter.CTkLabel(self.cost_frame,
                                                                    text="SELECCIONAR PROYECTO:",
                                                                    anchor="center",
                                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
            self.project_option_cost_label.grid(row=0, column=0, padx=30, pady=(30,10), sticky="nsew")
            project_data = get_all_bd(access[0], access[1], 'tbl_proyectos', 'manager')
            project_value = []
            for item in project_data:
                project_value.append(item[1] + " - " + item[2])
            self.project_option_cost_filter = customtkinter.CTkOptionMenu(self.cost_frame,
                                                                          dynamic_resizing=False,
                                                                          values=project_value,
                                                                          command=lambda
                                                                              event: self.project_filter_cost_event(access))
            self.project_option_cost_filter.grid(row=0, column=1, padx=30, pady=(30,10), sticky="nsew", columnspan=2)
            self.project_option_cost_filter.bind("<<ComboboxSelected>>",
                                                 lambda event: self.project_filter_cost_event(access))

            self.cost_label = customtkinter.CTkLabel(self.cost_frame,
                                                     text="CONTROL ECONÓMICO - PRESUPUESTO Y CERTIFICAICONES",
                                                     anchor="center",
                                                     font=customtkinter.CTkFont(size=15, weight="bold"))
            self.cost_label.grid(row=1, column=0, padx=30, pady=5, sticky="nsew", columnspan=3)

            # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA USUARIOS_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
            self.data_cost_frame = customtkinter.CTkScrollableFrame(self.cost_frame, corner_radius=0)
            self.data_cost_monthly_frame = customtkinter.CTkScrollableFrame(self.cost_frame, corner_radius=0)
            self.update_data_cost_frame_manager(access)

        else:
            self.project_option_project_label = customtkinter.CTkLabel(self.cost_frame,
                                                                       text="No se ha registrado ningún proyecto en la BBDD, puede acceder en la Pestaña Nuevo Proyecto para dar de alta un nuevo proyecto",
                                                                       anchor="center",
                                                                       font=customtkinter.CTkFont(size=15,
                                                                                                  weight="bold"))
            self.project_option_project_label.grid(row=0, column=0, padx=30, pady=(30, 10), sticky="nsew")


    def select_frame_by_name(self, name):
        # set button color for selected button
        self.new_project_button.configure(fg_color=("gray75", "gray25") if name == "new_project" else "transparent")
        self.project_button.configure(fg_color=("gray75", "gray25") if name == "project" else "transparent")
        self.user_button.configure(fg_color=("gray75", "gray25") if name == "user" else "transparent")
        self.cost_button.configure(fg_color=("gray75", "gray25") if name == "cost" else "transparent")

        # show selected frame
        if name == "new_project":
            self.new_project_frame.grid(row=0, column=1,padx=30, pady=(15, 15),sticky="nsew")
        else:
            self.new_project_frame.grid_forget()

        if name == "project":
            self.project_frame.grid(row=0, column=1,padx=30, pady=(15, 15),sticky="nsew")
        else:
            self.project_frame.grid_forget()

        if name == "user":
            self.user_frame.grid(row=0, column=1, padx=30, pady=(15, 15), sticky="nsew")
        else:
            self.user_frame.grid_forget()

        if name == "cost":
            self.cost_frame.grid(row=0, column=1, padx=30, pady=(15, 15),sticky="nsew")
        else:
            self.cost_frame.grid_forget()


    # ----------------------FRAME CREAR NUEVO PROYECTO-------------------------------------------------------------------
    def new_project_button_event(self,access):
        self.new_project_frame.destroy()
        self.new_project_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.select_frame_by_name("new_project")
        self.main_new_project(access)


    def project_button_event(self,access):
        self.project_frame.destroy()
        self.project_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.select_frame_by_name("project")
        self.main_manager_project(access)


    def user_button_event(self,access):
        self.user_frame.destroy()
        self.user_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.select_frame_by_name("user")
        self.main_manager_user(access)


    def cost_button_event(self,access):
        self.cost_frame.destroy()
        self.cost_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.select_frame_by_name("cost")
        self.main_manager_cost(access)


    def view_project_button_event (self,access):

        schemas = get_schemas_db(access[0], access[1])
        schemas = [item for item in schemas if item not in ['proyecto_tipo','information_schema', 'performance_schema','manager', 'mysql', 'sys']]
        print(schemas)
        if len(schemas)==0:
            mssg = f"No se ha encontrado ningún proyecto registrado, registre un nuevo proyecto en la Pestaña Nuevo Proyecto"
            CTkMessagebox(title="Warning Message!", message=mssg,
                          icon="warning")
        else:
            self.withdraw()
            appAux12 = AppManagerSelectProject(self,access)
            appAux12.protocol("WM_DELETE_WINDOW", appAux12.on_closing)
            appAux12.mainloop()


    def create_progress_window(self):
        # Crear una nueva ventana para mostrar la barra de progreso
        self.progress_window = customtkinter.CTkToplevel(self.master)
        self.progress_window.title("Progreso")
        self.progress_window.geometry("300x100")

        # Etiqueta de progreso
        self.progress_label = customtkinter.CTkLabel(self.progress_window, text="Por favor, espere...")
        self.progress_label.pack(pady=10)

        # Barra de progreso
        self.progress_bar = customtkinter.CTkProgressBar(self.progress_window, mode="indeterminate")
        self.progress_bar.pack(pady=10, padx=20, fill="x")
        self.progress_bar.start()


    def destroy_progress_window(self):
        # Detener la barra de progreso y cerrar la ventana
        self.progress_bar.stop()
        self.progress_window.destroy()


    def create_project_button_event(self, access):
        # Mostrar la ventana de progreso
        self.create_progress_window()

        try:
            code_project = self.code_project_entry.get()
            name_project = self.name_project_entry.get()
            description_project = self.description_project_entry.get("1.0", "end-1c")
            path_project = self.folder_project_entry.get()
            ccaa_project = self.ccaa_option.get()
            province_project = self.province_option.get()
            customer_project = self.customer_option.get()
            user_customer_project = self.user_customer_option.get()
            user_client_project = self.user_company_option.get()
            users_db_project = user_privileges
            path_budget_project = self.pathB_label.cget("text")
            path_catalog_project = self.pathC_label.cget("text")
            path_reference_project = self.pathR_label.cget("text")
            tender_project = self.tender_project_entry.get()
            tender_project  = tender_project.replace("€", "").replace(",", ".").replace("E", "")
            reduction_project = self.reduction_project_entry.get()
            reduction_project =reduction_project.replace("%","").replace(",",".")
            type_tender_project = self.economic_switch.get()
            if self.economic_switch.get() == "pem":
                gg_project = self.gg_project_entry.get()
                gg_project = gg_project.replace("%", "").replace(",", ".")
                bi_project = self.bi_project_entry.get()
                bi_project = bi_project.replace("%", "").replace(",", ".")
                iva_project =self.iva_project_entry.get()
                iva_project = iva_project.replace("%", "").replace(",", ".")
            else:
                gg_project = 13
                bi_project = 6
                iva_project = 21

            none_value=[]

            if code_project == "":
                none_value.append("código de proyecto")
            if name_project == "":
                none_value.append("nombre de proyecto")
            if path_project == "":
                none_value.append("carpeta del proyecto")
            if tender_project == "":
                none_value.append("presupuesto")
            if reduction_project == "":
                none_value.append("baja")
            if len(users_db_project)==0:
                none_value.append("usuarios de la BBDD del proyecto")
            if path_reference_project=="No se ha seleccionado referencias CAD":
                none_value.append("referencias CAD")
            if path_catalog_project=="No se ha seleccionado catálogo":
                none_value.append("catálogo")
            if path_budget_project=="No se ha seleccionado presupuesto":
                none_value.append("presupuesto")

            if len(none_value)==0:
                #insertar registros en tbl_proyectos
                data = {
                    "code": code_project,
                    "name": name_project,
                    "description": description_project,
                    "folder": path_project,
                    "id_customer": get_id_item_bd(access[0], access[1], "tbl_cliente", "manager", "nombre", customer_project),
                    "id_user_customer":get_id_user_customer(access[0], access[1],  user_customer_project, get_id_item_bd(access[0], access[1], "tbl_cliente", "manager", "nombre", customer_project)),
                    "company":"OBRAS Y SERVICIOS ARTANDA",
                    "id_user_company":get_id_user_company(access[0], access[1],  user_client_project),
                    "id_state": 1,
                    "id_province":get_id_province_bd(access[0], access[1],  province_project),
                    "id_ccaa": get_id_ccaa_bd(access[0], access[1],  ccaa_project)
                }

                data_tender ={
                    "type": type_tender_project,
                    "tender": tender_project,
                    "reduction": reduction_project,
                    "gg": gg_project,
                    "bi": bi_project,
                    "iva": iva_project
                }

                if "-" in code_project:
                    mssg = f"ERROR: el código de proyecto no puede incluir ( @,#,$,%,&,*,-) modifique el código del proyecto y vuelva a pulser sobre Crear proyecto"
                    CTkMessagebox(title="Error", message=mssg, icon="cancel")
                else:
                    project=get_option_item_bd(access[0], access[1], 'tbl_proyectos', 'manager', 'codigo')

                    if code_project in project:
                        mssg=f"ERROR: el proyecto '{code_project}' ya existe, por favor acceda a la Pestaña de Gestión de Proyectos para cualquier modificación."
                        CTkMessagebox(title="Error", message=mssg, icon="cancel")
                    else:
                        result_op1=add_project_item(access[0], access[1], data)
                        if result_op1=="ok":
                            result_op2A=create_schemas_db(access[0], access[1], code_project)
                            result_op2B = create_view_projects(access[0], access[1], data['code'])
                            if result_op2A=="ok" and result_op2B=="ok":
                                tables_schema=get_table_schemas_db(access[0], access[1], 'proyecto_tipo')
                                new_tables = [code_project+"." + table for table in tables_schema]
                                example_tables = ["proyecto_tipo." + table for table in tables_schema]
                                result_op3 = create_tables_schema_db(access[0], access[1], new_tables,  example_tables)
                                province_select_data = get_filter_data_bd(access[0], access[1],  'list_provincias', 'manager', 'NAMEUNIT',province_project)
                                cod_province = province_select_data[0][8] #cambiar indice para bbdd final
                                result_op4 = create_locality_schema_db(access[0], access[1], code_project, cod_province)
                                list_tables =['tbl_inv_certificado', 'tbl_inv_estado', 'tbl_inv_foto_tipo', 'tbl_inv_material','tbl_inv_orientacion', 'tbl_inv_tipo']
                                for table in list_tables:
                                    result_op4 = copy_tables_schema_db(access[0], access[1], code_project, table)
                                if result_op3=="ok" and result_op4=="ok":
                                    if path_budget_project== "Presupuesto predeterminado":
                                        list_tables = ['tbl_pres_unidades', 'tbl_pres_precios', 'tbl_pres_naturaleza', 'tbl_pres_capitulos' ]
                                        for table in list_tables:
                                            result_op5=copy_tables_schema_db(access[0], access[1], code_project, table)
                                    else:
                                        result_op5=budget_import(access[0], access[1],  code_project ,path_budget_project)
                                        id_type = get_id_item_bd(access[0], access[1], 'tbl_pres_naturaleza', code_project,
                                                                 "tipo", "Capítulo")
                                        data = ("PA000", id_type, "PARTIDAS TIPO")
                                        result_op5= add_item_chapter(access[0], access[1], code_project, data)
                                    if result_op5=="ok":
                                        if path_catalog_project== "Catálogo predeterminado":
                                            list_tables = ['tbl_catalogo_registros', 'tbl_cata_regis_tipo', 'tbl_cata_regis_proveedor',
                                                           'tbl_catalogo_hidraulica','tbl_cata_hidra_tipo',  'tbl_cata_hidra_pn',
                                                           'tbl_cata_hidra_marcas', 'tbl_cata_hidra_dni','tbl_cata_hidra_dnf',
                                                           'tbl_cata_hidra_familia','tbl_cata_hidra_caracteristica','tbl_cata_hidra_angulo']
                                            for table in list_tables:
                                                result_op6=copy_tables_schema_db(access[0], access[1], code_project, table)
                                        else:
                                           result_op6=catalog_import(access[0], access[1],  code_project ,path_catalog_project)
                                        if path_reference_project=="Referencias predeterminadas":
                                            result_op7=copy_tables_schema_db(access[0], access[1], code_project, 'tbl_cata_hidra_referencias_cad')
                                        else:
                                            path_reference = path_reference_project
                                            result_op7 = update_reference(access[0], access[1], code_project, path_reference)
                                        create_view_catalog(access[0], access[1], code_project)
                                        create_view_inventory(access[0], access[1], code_project)
                                        create_view_economic(access[0], access[1], code_project)
                                        if result_op6=="ok" and result_op7=="ok":
                                            for key, value in users_db_project.items():
                                                user_bd= key
                                                type_privilege=value
                                                result_op8= add_privileges(access[0], access[1], code_project, user_bd, type_privilege)
                                            if result_op8=="ok":
                                                id_project=get_id_item_bd(access[0], access[1], "tbl_proyectos", "manager", "codigo", code_project)
                                                data_tender["id_project"]=id_project
                                                result_op9=add_economic_project_item(access[0], access[1],data_tender)
                                                if result_op9=="ok":
                                                    self.new_project_frame.destroy()
                                                    self.new_project_frame = customtkinter.CTkFrame(self,corner_radius=0)
                                                    self.reset_newporject_frame(access)
                                                    self.main_manager_project(access)
                                                    self.select_frame_by_name("project")
                                                    mssg = "Se ha creado el proyecto "+ code_project+" en la base de datos"
                                                    CTkMessagebox(title="Successfull Message!", message=mssg,
                                                                  icon="check")
                                                else:
                                                    mssg = f"ERROR: '{result_op9}'"
                                                    CTkMessagebox(title="Error", message=mssg, icon="warning")
                                            else:
                                                mssg = f"ERROR: '{result_op8}'"
                                                CTkMessagebox(title="Error", message=mssg, icon="warning")
                                        elif result_op6!="ok" :
                                            mssg = f"ERROR: '{result_op6}'"
                                            CTkMessagebox(title="Error", message=mssg, icon="cancel")
                                        elif result_op7!="ok" :
                                            mssg = f"ERROR: '{result_op7}'"
                                            CTkMessagebox(title="Error", message=mssg, icon="cancel")
                                        else:
                                            mssg = f"ERROR: No se ha podido crear el catálogo y las referencia, por favor revise que ambos tenga la ruta predeterminada."
                                            CTkMessagebox(title="Error", message=mssg, icon="warning")
                                    else:
                                        mssg = f"ERROR: '{result_op5}'"
                                        CTkMessagebox(title="Error", message=mssg, icon="cancel")
                                elif result_op3 != "ok":
                                    mssg = f"ERROR: '{result_op3}'"
                                    CTkMessagebox(title="Error", message=mssg, icon="cancel")
                                elif result_op4 != "ok":
                                    mssg = f"ERROR: '{result_op4}'"
                                    CTkMessagebox(title="Error", message=mssg, icon="cancel")
                            else:
                                mssg = f"ERROR: '{result_op2A}'\n '{result_op2B}'"
                                CTkMessagebox(title="Error", message=mssg, icon="cancel")
                        else:
                            mssg = f"ERROR: '{result_op1}' "
                            CTkMessagebox(title="Error", message=mssg, icon="cancel")
            else:
                mssg="Es necesario rellenar los siguiente campos obligatorios:\n\n"
                value=""
                for item in none_value:
                    value+="  -  "+item+"\n"
                mssg+=value + "\n Error: No se puede crear el proyecto sin los campos obligatorios"
                CTkMessagebox(title="Error", message=mssg, icon="cancel", width=500)

        finally:
            # Asegurarse de cerrar la ventana de progreso al final
            self.destroy_progress_window()


    def reset_newporject_frame(self,access):
        global data_user_bd
        global user_privileges
        data_user_bd = []
        user_privileges = {}
        self.main_new_project(access)


    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            folder_path_var=directory  # Mostrar la ruta en el Entry
            self.folder_project_entry.delete(0,"end")
            self.folder_project_entry.insert(0,directory)


    def update_province_options(self,access):

        select_ccaa = self.ccaa_option.get()
        code_ccaa = get_code_ccaa_bd(self.user, self.password, select_ccaa)

        province_values =get_province_bd(self.user, self.password , code_ccaa)
        self.province_option.configure(values=province_values)
        self.province_option.set(province_values[0])


    def update_customer_data(self, access):
        #color predefinido para las letras
        common_fg_color = "#171717"

        #eliminamos el customer_data_frame
        self.customer_data_frame.forget()

        #volvemos a iniciar el customer_data_frame
        self.customer_data_frame = customtkinter.CTkFrame(self.customer_frame, corner_radius=0, width=200)
        self.customer_data_frame.grid(row=1, padx=(10,10), pady=(10,10),sticky="nsew")

        #Recopila los datos del cliente seleccionado de la bbdd para añadirlos en los entry
        customer_data=get_customer_data(self.user, self.password , self.customer_option.get())
        self.select_customer = [tk.StringVar(value=data) for data in customer_data]

        #devuelve nombre empresa
        self.name_customer_label = customtkinter.CTkLabel(self.customer_data_frame, text="NOMBRE EMPRESA:",
                                                         anchor="e", font=customtkinter.CTkFont(size=14),
                                                         width= 50)
        self.name_customer_label.grid(row=1, column=0, padx=(50,5), pady=(10,10), sticky= "e")
        self.name_customer_entry = customtkinter.CTkEntry(self.customer_data_frame, textvariable= self.select_customer[1],
                                                         fg_color=common_fg_color,text_color="#FFFFFF",state="disabled")
        self.name_customer_entry.grid(row=1, column=1, padx=(5,30), pady=(10,10), sticky= "ew", columnspan=3)

        #devuelve cif empresa
        self.cif_customer_label = customtkinter.CTkLabel(self.customer_data_frame, text="CIF:",
                                                         anchor="e", font=customtkinter.CTkFont(size=14),
                                                         width= 50)
        self.cif_customer_label.grid(row=2, column=0, padx=(50,5), pady=(10,10), sticky= "e")
        self.cif_customer_entry = customtkinter.CTkEntry(self.customer_data_frame, textvariable= self.select_customer[2],
                                                         fg_color=common_fg_color,text_color="#FFFFFF",state="disabled")
        self.cif_customer_entry.grid(row=2, column=1, padx=(5,30), pady=(10,10), sticky= "ew", columnspan=3)

        #devuelve direcciÓn empresa
        self.street_customer_label = customtkinter.CTkLabel(self.customer_data_frame, text="DIRECCIÓN:",
                                                         anchor="e", font=customtkinter.CTkFont(size=14),
                                                         width= 50)
        self.street_customer_label.grid(row=3, column=0, padx=(50,5), pady=(10,10), sticky= "e")
        self.street_customer_entry = customtkinter.CTkEntry(self.customer_data_frame, textvariable= self.select_customer[3],
                                                         fg_color=common_fg_color,text_color="#FFFFFF",state="disabled")
        self.street_customer_entry.grid(row=3, column=1, padx=(5,30), pady=(10,10), sticky= "ew", columnspan=3)

        #devuelve  municipio empresa
        self.locality_customer_label = customtkinter.CTkLabel(self.customer_data_frame, text="MUNICIPIO:",
                                                         anchor="e", font=customtkinter.CTkFont(size=14),
                                                         width= 50)
        self.locality_customer_label.grid(row=4, column=0, padx=(50,5), pady=(10,10), sticky= "e")
        self.locality_customer_entry = customtkinter.CTkEntry(self.customer_data_frame, textvariable= self.select_customer[4],
                                                         fg_color=common_fg_color,text_color="#FFFFFF",state="disabled")
        self.locality_customer_entry.grid(row=4, column=1, padx=(5,30), pady=(10,10), sticky= "ew", columnspan=4)

        #devuelve  c.postal empresa
        self.cp_customer_label = customtkinter.CTkLabel(self.customer_data_frame, text="C.POSTAL:",
                                                         anchor="e", font=customtkinter.CTkFont(size=14),
                                                         width= 50)
        self.cp_customer_label.grid(row=5, column=0, padx=(50,5), pady=(10,10), sticky= "e")
        self.cp_customer_entry = customtkinter.CTkEntry(self.customer_data_frame, textvariable= self.select_customer[5],
                                                        fg_color=common_fg_color,text_color="#FFFFFF", width=200,state="disabled")
        self.cp_customer_entry.grid(row=5, column=1, padx=(5,5), pady=(10,10), sticky= "ew")

        #devuelve  telefono empresa
        self.phone_customer_label = customtkinter.CTkLabel(self.customer_data_frame, text="TELÉFONO:",
                                                         anchor="e", font=customtkinter.CTkFont(size=14),
                                                         width= 50)
        self.phone_customer_label.grid(row=5, column=2, padx=(5,5), pady=(10,10), sticky= "e")
        self.phone_customer_entry = customtkinter.CTkEntry(self.customer_data_frame, textvariable= self.select_customer[6],
                                                         fg_color=common_fg_color,text_color="#FFFFFF", width=200,state="disabled")
        self.phone_customer_entry.grid(row=5, column=3, padx=(5,30), pady=(10,10), sticky= "ew")

        # devuelve  logo empresa
        self.lg_customer_label = customtkinter.CTkLabel(self.customer_data_frame, text="LOGO:",
                                                           anchor="e",
                                                           font=customtkinter.CTkFont(size=14),
                                                           width=50)
        self.lg_customer_label.grid(row=6, column=0, padx=(50, 5), pady=(10, 10), sticky="e")
        #formatea imagen base64 almacenada
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
        self.lg_image_label = customtkinter.CTkLabel(self.customer_data_frame, text=" ", image=self.lg_image, height=80)
        self.lg_image_label.grid(row=6, column=1, padx=30, pady=(15, 15), columnspan =2)

        #modificamos las opciones de responsable de cliente
        id_customer = get_id_item_bd(access[0], access[1], "tbl_cliente", "manager", 'nombre',
                                     self.customer_option.get())
        id_users_customer = get_option_item_sub_bd(access[0], access[1], "tbl_clie_usuario", "manager", 'id',
                                                   id_customer, 'id_cliente')
        if len(id_users_customer) == 0:
            self.user_customer_frame.forget()
            self.user_customer_frame = customtkinter.CTkFrame(self.tab_view.tab("Cliente"), corner_radius=0, width=200)
            self.user_customer_frame.grid(row=3, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew", columnspan=4)
            self.user_customer_frame.grid_columnconfigure(0, weight=1)
            self.user_customer_project_label = customtkinter.CTkLabel(self.user_customer_frame,
                                                                      text="No se ha registrado ningún responsable, por favor añada un responsable para la empresa seleccionada",
                                                                      anchor="center",
                                                                      font=customtkinter.CTkFont(size=15,
                                                                                                 weight="bold"),
                                                                      width=50)
            self.user_customer_project_label.grid(row=0, column=0, padx=(30, 10), pady=10, sticky="news", columnspan=3)

            # Botón para añadir responsable del cliente
            self.add_user_customer_button = customtkinter.CTkButton(self.user_customer_frame, text="Añadir Responsable",
                                                                    command=lambda: self.add_user_customer_first(access),
                                                                    width=100)
            self.add_user_customer_button.grid(row=1, column=0, padx=(10, 30), pady=(10, 30), sticky="ew", columnspan=3)
        else:
            self.user_customer_frame.forget()
            self.user_customer_frame = customtkinter.CTkFrame(self.tab_view.tab("Cliente"), corner_radius=0, width=200)
            self.user_customer_frame.grid(row=3, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew", columnspan=4)
            self.user_customer_frame.grid_columnconfigure(0, weight=1)

            self.user_customer_project_label = customtkinter.CTkLabel(self.user_customer_frame,
                                                                      text="RESPONSABLE CLIENTE",
                                                                      anchor="center",
                                                                      font=customtkinter.CTkFont(size=15,
                                                                                                 weight="bold"),
                                                                      width=50)
            self.user_customer_project_label.grid(row=0, column=0, padx=(30, 10), pady=10, sticky="news", columnspan=3)
            users_value = []
            for item in id_users_customer:
                user_surname_value = get_option_item_sub_bd(access[0], access[1], "tbl_clie_usuario", "manager",
                                                            'apellidos',
                                                            item, 'id')
                user_name_value = get_option_item_sub_bd(access[0], access[1], "tbl_clie_usuario", "manager", 'nombre',
                                                         item, 'id')
                value = user_surname_value[0] + ", " + user_name_value[0]
                users_value.append(value)
            users_value.sort(key=str.lower)
            self.user_customer_option = customtkinter.CTkOptionMenu(self.user_customer_frame,
                                                                    dynamic_resizing=False,
                                                                    values=users_value)
            self.user_customer_option.grid(row=1, column=0, padx=(30, 30), pady=(10, 30), sticky="ew", columnspan=2)
            # self.user_customer_option.bind("<<ComboboxSelected>>", lambda event: self.update_customer_user(access))

            # Botón para añadir responsable del cliente
            self.add_user_customer_button = customtkinter.CTkButton(self.user_customer_frame, text="Añadir Responsable",
                                                                    command=lambda: self.add_user_customer(access),
                                                                    width=100)
            self.add_user_customer_button.grid(row=1, column=2, padx=(10, 30), pady=(10, 30), sticky="ew")

            # Botón para modificar responsable del cliente
            self.update_customer_button = customtkinter.CTkButton(self.user_customer_frame,
                                                                  text="Modificar Responsable",
                                                                  command=lambda: self.mod_user_customer(access),
                                                                  width=100)
            self.update_customer_button.grid(row=1, column=3, padx=(10, 30), pady=(10, 30), sticky="ew")


    def add_customer(self, access):
        appAux1 = AppCustomerAdd(access)
        appAux1.grab_set()
        self.wait_window(appAux1)
        customer_value=get_option_item_bd(access[0], access[1], "tbl_cliente", "manager", 'nombre')
        self.customer_option.configure(values=customer_value)


    def mod_customer(self, access):
        select_data=[access[0],access[1], self.customer_option.get()]
        id_customer=get_id_item_bd(access[0], access[1], "tbl_cliente", "manager", 'nombre', self.customer_option.get())
        appAux2 = AppCustomerMod(select_data)
        appAux2.grab_set()
        self.wait_window(appAux2)
        customer_value=get_option_item_bd(access[0], access[1], "tbl_cliente", "manager", 'nombre')
        modified_customer_name=get_item_id_bd(access[0], access[1], "tbl_cliente", "manager", 'nombre', id_customer)
        self.customer_option.configure(values=customer_value)
        self.customer_option.set(modified_customer_name)


    def add_user_customer(self, access):
        id_customer = get_id_item_bd(access[0], access[1], "tbl_cliente", "manager", 'nombre', self.customer_option.get())
        select_data = [access[0], access[1], id_customer]
        #abre ventana para introducir los datos del nuevo responsable
        appAux3 = AppUserCustomerAdd(select_data)
        appAux3.grab_set()
        self.wait_window(appAux3)
        #actualiza los datos que hay en las opciones del responsable del cliente
        users_value=[]
        user_name_value = get_option_item_sub_bd(access[0], access[1], "tbl_clie_usuario", "manager", 'nombre',
                                                 id_customer, 'id_cliente')
        user_surname_value = get_option_item_sub_bd(access[0], access[1], "tbl_clie_usuario", "manager", 'apellidos',
                                                    id_customer, 'id_cliente')
        for i in range(len(user_name_value)):
                value=user_surname_value[i]+", "+user_name_value[i]
                users_value.append(value)
        users_value.sort(key=str.lower)
        self.user_customer_option.configure(values=users_value)


    def add_user_customer_first(self, access):
        id_customer = get_id_item_bd(access[0], access[1], "tbl_cliente", "manager", 'nombre',
                                     self.customer_option.get())
        select_data = [access[0], access[1], id_customer]
        # abre ventana para introducir los datos del nuevo responsable
        appAux5 = AppUserCustomerAddNew(select_data, on_save_callback=lambda: self.update_user_customer_frame(access))
        appAux5.grab_set()


    def update_user_customer_frame(self, access):

        id_customer = get_id_item_bd(access[0], access[1], "tbl_cliente", "manager", 'nombre',
                                     self.customer_option.get())
        id_users_customer = get_option_item_sub_bd(access[0], access[1], "tbl_clie_usuario", "manager", 'id',
                                                   id_customer, 'id_cliente')
        # actualiza los datos que hay en las opciones del responsable del cliente
        self.user_customer_frame.forget()
        self.update_idletasks()
        self.user_customer_frame = customtkinter.CTkFrame(self.tab_view.tab("Cliente"), corner_radius=0, width=200)
        self.user_customer_frame.grid(row=3, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew", columnspan=4)
        self.user_customer_frame.grid_columnconfigure(0, weight=1)

        self.user_customer_project_label = customtkinter.CTkLabel(self.user_customer_frame,
                                                                  text="RESPONSABLE CLIENTE",
                                                                  anchor="center",
                                                                  font=customtkinter.CTkFont(size=15,
                                                                                             weight="bold"),
                                                                  width=50)
        self.user_customer_project_label.grid(row=0, column=0, padx=(30, 10), pady=10, sticky="news", columnspan=3)
        users_value = []
        for item in id_users_customer:
            user_surname_value = get_option_item_sub_bd(access[0], access[1], "tbl_clie_usuario", "manager",
                                                        'apellidos',
                                                        item, 'id')
            user_name_value = get_option_item_sub_bd(access[0], access[1], "tbl_clie_usuario", "manager", 'nombre',
                                                     item, 'id')
            value = user_surname_value[0] + ", " + user_name_value[0]
            users_value.append(value)
        users_value.sort(key=str.lower)
        self.user_customer_option = customtkinter.CTkOptionMenu(self.user_customer_frame,
                                                                dynamic_resizing=False,
                                                                values=users_value)
        self.user_customer_option.grid(row=1, column=0, padx=(30, 30), pady=(10, 30), sticky="ew", columnspan=2)
        # self.user_customer_option.bind("<<ComboboxSelected>>", lambda event: self.update_customer_user(access))

        # Botón para añadir responsable del cliente
        self.add_user_customer_button = customtkinter.CTkButton(self.user_customer_frame, text="Añadir Responsable",
                                                                command=lambda: self.add_user_customer(access),
                                                                width=100)
        self.add_user_customer_button.grid(row=1, column=2, padx=(10, 30), pady=(10, 30), sticky="ew")

        # Botón para modificar responsable del cliente
        self.update_customer_button = customtkinter.CTkButton(self.user_customer_frame,
                                                              text="Modificar Responsable",
                                                              command=lambda: self.mod_user_customer(access),
                                                              width=100)
        self.update_customer_button.grid(row=1, column=3, padx=(10, 30), pady=(10, 30), sticky="ew")


    def mod_user_customer(self, access):
        select_user_customer = self.user_customer_option.get()
        id_customer = get_id_item_bd(access[0], access[1], "tbl_cliente", "manager", 'nombre',
                                     self.customer_option.get())
        id_user_customer = get_id_user_customer(access[0], access[1], select_user_customer,id_customer)
        id_users_customer = get_option_item_sub_bd(access[0], access[1], "tbl_clie_usuario", "manager", 'id',
                                                   id_customer, 'id_cliente')
        select_data=[access[0],access[1],id_customer,id_user_customer]
        appAux4 = AppUserCustomerMod(select_data)
        appAux4.grab_set()
        self.wait_window(appAux4)
        users_value = []
        for item in id_users_customer:
            user_surname_value = get_option_item_sub_bd(access[0], access[1], "tbl_clie_usuario", "manager",
                                                        'apellidos',
                                                        item, 'id')
            user_name_value = get_option_item_sub_bd(access[0], access[1], "tbl_clie_usuario", "manager", 'nombre',
                                                     item, 'id')
            value = user_surname_value[0] + ", " + user_name_value[0]
            users_value.append(value)
        users_value.sort(key=str.lower)
        modified_user_customer_name = get_item_id_bd(access[0], access[1], "tbl_clie_usuario", "manager", 'nombre', id_user_customer)
        modified_user_customer_surname = get_item_id_bd(access[0], access[1], "tbl_clie_usuario", "manager", 'apellidos',
                                                     id_user_customer)
        modified_user_customer=modified_user_customer_surname+", "+modified_user_customer_name
        self.user_customer_option.configure(values=users_value)
        self.user_customer_option.set(modified_user_customer)


    def add_user_company(self, access):

        #abre ventana para introducir los datos del nuevo responsable
        appAux6 = AppUserCompanyAdd(access)
        appAux6.grab_set()
        self.wait_window(appAux6)
        #actualiza los datos que hay en las opciones del responsable del cliente
        id_users_company = get_option_item_bd(access[0], access[1], "tbl_empr_usuario", "manager", 'id')
        users_value=[]
        for item in id_users_company:
            user_surname_value = get_option_item_sub_bd(access[0], access[1], "tbl_empr_usuario", "manager",
                                                        'apellidos',
                                                        item, 'id')
            user_name_value = get_option_item_sub_bd(access[0], access[1], "tbl_empr_usuario", "manager", 'nombre',
                                                     item, 'id')
            value = user_surname_value[0] + ", " + user_name_value[0]
            users_value.append(value)
        users_value.sort(key=str.lower)
        self.user_company_option.configure(values=users_value)


    def add_user_company_first(self, access):
        # abre ventana para introducir los datos del nuevo responsable
        appAux7 = AppUserCompanyAddNew(access, on_save_callback=lambda: self.update_user_company_frame(access))
        appAux7.grab_set()


    def mod_user_company(self, access):
        select_user_company = self.user_company_option.get()
        id_user_company = get_id_user_company(access[0], access[1], select_user_company)
        select_data=[access[0],access[1],id_user_company]
        appAux8 = AppUserCompanyMod(select_data)
        appAux8.grab_set()
        self.wait_window(appAux8)
        id_users_company = get_option_item_bd(access[0], access[1], "tbl_empr_usuario", "manager", 'id')
        users_value = []
        for item in id_users_company:
            user_surname_value = get_option_item_sub_bd(access[0], access[1], "tbl_empr_usuario", "manager",
                                                        'apellidos',
                                                        item, 'id')
            user_name_value = get_option_item_sub_bd(access[0], access[1], "tbl_empr_usuario", "manager", 'nombre',
                                                     item, 'id')
            value = user_surname_value[0] + ", " + user_name_value[0]
            users_value.append(value)
        users_value.sort(key=str.lower)
        modified_user_company_name = get_item_id_bd(access[0], access[1], "tbl_empr_usuario", "manager", 'nombre', id_user_company)
        modified_user_company_surname = get_item_id_bd(access[0], access[1], "tbl_empr_usuario", "manager", 'apellidos',
                                                     id_user_company)
        modified_user_company=modified_user_company_surname+", "+modified_user_company_name
        self.user_customer_option.configure(values=users_value)
        self.user_customer_option.set(modified_user_company)


    def update_user_company_frame(self, access):

        id_users_company = get_option_item_bd(access[0], access[1], "tbl_empr_usuario", "manager", 'id')
        self.user_company_frame.forget()
        self.update_idletasks()
        self.user_company_frame = customtkinter.CTkFrame(self.tab_view.tab("Adjudicatario"), corner_radius=0)
        self.user_company_frame.grid(row=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.user_company_frame.grid_columnconfigure(0, weight=10)
        self.user_company_frame.grid_columnconfigure(1, weight=1)
        self.user_company_frame.grid_columnconfigure(2, weight=1)

        self.user_company_project_label = customtkinter.CTkLabel(self.user_company_frame,
                                                                 text="RESPONSABLE ADJUDICATARIO",
                                                                 anchor="center",
                                                                 font=customtkinter.CTkFont(size=15,
                                                                                            weight="bold"))
        self.user_company_project_label.grid(row=0, column=0, padx=(30, 10), pady=10, sticky="news",
                                             columnspan=3)
        users_value = []
        for item in id_users_company:
            user_surname_value = get_option_item_sub_bd(access[0], access[1], "tbl_empr_usuario", "manager",
                                                        'apellidos',
                                                        item, 'id')
            user_name_value = get_option_item_sub_bd(access[0], access[1], "tbl_empr_usuario", "manager",
                                                     'nombre',
                                                     item, 'id')
            value = user_surname_value[0] + ", " + user_name_value[0]
            users_value.append(value)
        users_value.sort(key=str.lower)
        self.user_company_option = customtkinter.CTkOptionMenu(self.user_company_frame,
                                                               dynamic_resizing=False,
                                                               values=users_value)
        self.user_company_option.grid(row=1, column=0, padx=(30, 30), pady=(10, 30), sticky="ew")

        # Botón para añadir responsable del cliente
        self.add_user_company_button = customtkinter.CTkButton(self.user_company_frame,
                                                               text="Añadir Responsable",
                                                               command=lambda: self.add_user_company(access),
                                                               width=100)
        self.add_user_company_button.grid(row=1, column=1, padx=(10, 30), pady=(10, 30), sticky="ew")

        # Botón para modificar responsable del cliente
        self.update_company_button = customtkinter.CTkButton(self.user_company_frame,
                                                             text="Modificar Responsable",
                                                             command=lambda: self.mod_user_company(access),
                                                             width=100)
        self.update_company_button.grid(row=1, column=2, padx=(10, 30), pady=(10, 30), sticky="ew")


    def update_privilege(self,user, selected_value):
        user_privileges[user] = selected_value
        print(f"Usuario: {user}, Privilegio seleccionado: {selected_value}")


    def add_user_bd(self,access):
        appAux10=AppUserBdAddNew(access)
        appAux10.grab_set()
        self.wait_window(appAux10)


    def delete_user_db(self,access):
        b=access
        appAux11 = AppCombox(data_user_bd, lambda selected_items: self.update_data_user_frame2(selected_items))
        appAux11.grab_set()
        self.wait_window(appAux11)


    def select_user_bd(self,access):
        users_value = get_user_db (self.user, self.password )
        appAux9 =  AppCombox(users_value, lambda selected_items: self.update_data_user_frame(selected_items))
        appAux9.grab_set()
        self.wait_window(appAux9)


    def update_data_user_frame(self, selected_items):
        for item in selected_items:
            data_user_bd.append(item)

        self.user_bd_frame.forget()
        self.user_bd_frame = customtkinter.CTkScrollableFrame(self.tab_view.tab("Usuarios BD"), corner_radius=0)
        self.user_bd_frame.grid(row=1, padx=(30, 30), pady=(30, 10), sticky="nsew", columnspan=3)
        self.user_bd_frame.grid_columnconfigure(0, weight=1)
        self.user_bd_frame.grid_columnconfigure(1, weight=1)
        self.user_bd_frame.grid_columnconfigure(2, weight=1)

         #encabezados tabla de usuarios y permisos
        self.user_bd_label = customtkinter.CTkLabel(self.user_bd_frame, text="USUARIOS",
                                                             anchor="center",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.user_bd_label.grid(row=0, column=0, padx=(30, 10), pady=10, sticky="nwes", columnspan=2)
        self.privileges_bd_label = customtkinter.CTkLabel(self.user_bd_frame, text="PERMISOS",
                                                             anchor="center",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.privileges_bd_label.grid(row=0, column=2, padx=(10, 30), pady=10, sticky="nwes")

        #cuerpo tabla de usuarios y permisos
        #botón estandar para seleccionar permisos
        privileges_bd_value = ['Administrador', 'Escritura y lectura', 'Solo lectura']

        # según los usuarios que estén almacenados en data_user_bd, añadirá tantas filas como usuarios
        for i in range(len(data_user_bd)):
            n_row = i + 1
            user_db = data_user_bd[i]
            self.user_bd = customtkinter.CTkLabel(self.user_bd_frame, text=user_db,
                                                  anchor="center",
                                                  font=customtkinter.CTkFont(size=14))
            self.user_bd.grid(row=n_row, column=0, padx=(30, 10), pady=10, sticky="nwes", columnspan=2)

            self.user_privilege_option = customtkinter.CTkOptionMenu(self.user_bd_frame,
                                                                     dynamic_resizing=False,
                                                                     values=privileges_bd_value,
                                                                     command=lambda value,
                                                                                    user=user_db: self.update_privilege(
                                                                         user, value))
            self.user_privilege_option.grid(row=n_row, column=2, padx=(30, 30), pady=10, sticky="nwes")
            # Establecer el valor predeterminado
            default_value = 'Seleccione permisos'  # Cambia esto al valor predeterminado que quieras
            self.user_privilege_option.set(default_value)


    def update_data_user_frame2(self, selected_items):
        for item in selected_items:
            data_user_bd.remove(item)

        self.user_bd_frame.forget()
        self.user_bd_frame = customtkinter.CTkScrollableFrame(self.tab_view.tab("Usuarios BD"), corner_radius=0)
        self.user_bd_frame.grid(row=1, padx=(30, 30), pady=(30, 10), sticky="nsew", columnspan=3)
        self.user_bd_frame.grid_columnconfigure(0, weight=1)
        self.user_bd_frame.grid_columnconfigure(1, weight=1)
        self.user_bd_frame.grid_columnconfigure(2, weight=1)

        # encabezados tabla de usuarios y permisos
        self.user_bd_label = customtkinter.CTkLabel(self.user_bd_frame, text="USUARIOS",
                                                    anchor="center",
                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
        self.user_bd_label.grid(row=0, column=0, padx=(30, 10), pady=10, sticky="nwes", columnspan=2)
        self.privileges_bd_label = customtkinter.CTkLabel(self.user_bd_frame, text="PERMISOS",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=15, weight="bold"))
        self.privileges_bd_label.grid(row=0, column=2, padx=(10, 30), pady=10, sticky="nwes")

        # cuerpo tabla de usuarios y permisos
        # botón estandar para seleccionar permisos
        privileges_bd_value = ['Administrador', 'Escritura y lectura', 'Solo lectura']

        # según los usuarios que estén almacenados en data_user_bd, añadirá tantas filas como usuarios
        for i in range(len(data_user_bd)):
            n_row = i + 1
            user_db = data_user_bd[i]
            self.user_bd = customtkinter.CTkLabel(self.user_bd_frame, text=user_db,
                                                  anchor="center",
                                                  font=customtkinter.CTkFont(size=14))
            self.user_bd.grid(row=n_row, column=0, padx=(30, 10), pady=10, sticky="nwes", columnspan=2)

            self.user_privilege_option = customtkinter.CTkOptionMenu(self.user_bd_frame,
                                                                     dynamic_resizing=False,
                                                                     values=privileges_bd_value,
                                                                     command=lambda value,
                                                                                    user=user_db: self.update_privilege(
                                                                         user, value))
            self.user_privilege_option.grid(row=n_row, column=2, padx=(30, 30), pady=10, sticky="nwes")


    def switch_budget(self):
        option=self.budget_switch.get()
        if option==1:
            self.pathB_label.destroy()
            self.pathB_label = customtkinter.CTkLabel(self.tab_view.tab("Referencias"), text="Presupuesto predeterminado",
                                                      font=customtkinter.CTkFont(size=15))
            self.pathB_label.grid(row=2, column=1, padx=(10, 30), pady=10, sticky="w")
        else:
            self.pathB_label.destroy()
            self.pathB_label = customtkinter.CTkLabel(self.tab_view.tab("Referencias"), text="No se ha seleccionado presupuesto",
                                                      font=customtkinter.CTkFont(size=15))
            self.pathB_label.grid(row=2, column=1, padx=(10, 30), pady=10, sticky="w")


    def switch_catalog(self):
        option=self.catalog_switch.get()
        if option==1:
            self.pathC_label.destroy()
            self.pathC_label = customtkinter.CTkLabel(self.tab_view.tab("Referencias"), text="Catálogo predeterminado",
                                                      font=customtkinter.CTkFont(size=15))
            self.pathC_label.grid(row=3, column=1, padx=(10, 30), pady=10, sticky="w")
            self.pathR_label.destroy()
            self.pathR_label = customtkinter.CTkLabel(self.tab_view.tab("Referencias"), text="Referencias predeterminadas",
                                                      font=customtkinter.CTkFont(size=15))
            self.pathR_label.grid(row=4, column=1, padx=(10, 30), pady=(10,15), sticky="w")
        else:
            self.pathC_label.destroy()
            self.pathC_label = customtkinter.CTkLabel(self.tab_view.tab("Referencias"),
                                                      text="No se ha seleccionado cátalogo",
                                                      font=customtkinter.CTkFont(size=15))
            self.pathC_label.grid(row=3, column=1, padx=(10, 30), pady=10, sticky="w")
            self.pathR_label.destroy()
            self.pathR_label = customtkinter.CTkLabel(self.tab_view.tab("Referencias"),
                                                      text="No se ha seleccionado referencias CAD",
                                                      font=customtkinter.CTkFont(size=15))
            self.pathR_label.grid(row=4, column=1, padx=(10, 30), pady=(10,15), sticky="w")


    def add_budget(self):
        pathB = filedialog.askopenfilename(
            title="Selecciona una imagen",
            filetypes=[("Archivos de excel", "*.xlsx")]
        )
        self.pathB_label.destroy()
        self.pathB_label = customtkinter.CTkLabel(self.tab_view.tab("Referencias"), text=pathB,
                                                  font=customtkinter.CTkFont(size=15))
        self.pathB_label.grid(row=2, column=1, padx=(10, 30), pady=10, sticky="w")
        self.budget_switch.deselect()


    def add_reference(self):
        pathR = filedialog.askdirectory(title='Seleccionar directorio de referencias')
        self.pathR_label.destroy()
        self.pathR_label = customtkinter.CTkLabel(self.tab_view.tab("Referencias"), text=pathR,
                                                  font=customtkinter.CTkFont(size=15))
        self.pathR_label.grid(row=4, column=1, padx=(10, 30), pady=(10,15), sticky="w")
        self.catalog_switch.deselect()


    def add_catalog(self):
        pathC = filedialog.askopenfilename(
            title="Selecciona una imagen",
            filetypes=[("Archivos de excel", "*.xlsx")]
        )
        self.pathC_label.destroy()
        self.pathC_label = customtkinter.CTkLabel(self.tab_view.tab("Referencias"), text=pathC,
                                                  font=customtkinter.CTkFont(size=15))
        self.pathC_label.grid(row=3, column=1, padx=(10, 30), pady=10, sticky="w")
        self.catalog_switch.deselect()


    def download_example(self):
        try:
            # Seleccionar la carpeta de destino
            destination_folder = filedialog.askdirectory(title="Selecciona la carpeta de destino")

            if not destination_folder:
                CTkMessagebox(title="Warning Message!", message="No se ha seleccionado ningún archivo",
                              icon="warning")

            list_files=["output/catalogo_piezas_tipo.xlsx","output/presupuesto_tipo.xlsx"]
            for file in list_files:
                # Seleccionar el archivo de origen
                source_file_path = os.path.join(parent_path,file)
                # Definir la ruta de destino del archivo
                destination_file_path = os.path.join(destination_folder, os.path.basename(source_file_path))
                # Copiar el archivo
                shutil.copy2(source_file_path, destination_file_path)
                # Abrir el archivo con la aplicación predeterminada
                if os.name == 'nt':  # Para Windows
                    os.startfile(destination_file_path)
                elif os.name == 'posix':  # Para macOS y Linux
                    subprocess.call(['open' if sys.platform == 'darwin' else 'xdg-open', destination_file_path])

        except Exception as e:
            mssg= f"Error al copiar o abrir el archivo: {e}"
            CTkMessagebox(title="Warning Message!", message=mssg,
                          icon="warning")


    def update_template(self):
        try:
            # Seleccionar la carpeta de destino
            source_file_path = filedialog.askopenfilename(title="Selecciona el cajetín formato A3 para los dwg",
                                                            filetypes=[("Archivos DWG", "*.dwg")])

            destination_folder = self.folder_project_entry.get()

            if not destination_folder:
                CTkMessagebox(title="Warning Message!", message="No se ha seleccionado ningún directorio que indique la carpeta del proyecto",
                              icon="warning")
            else:
                path_template = "DC_GRAFICA/CAD/01.refx"
                destination_folder = os.path.join(destination_folder, path_template)

                if not os.path.exists(destination_folder ):
                    os.makedirs(destination_folder)

                name_file_template = "Formato_A3.dwg"
                new_template = os.path.join(destination_folder, name_file_template)

                shutil.copy2(source_file_path, new_template)
                mssg = f"Se ha añadido el nuevo template a la carpeta {destination_folder}"
                CTkMessagebox(title="Successful!", message=mssg,
                              icon="check")

        except Exception as e:
            mssg = f"Error al copiar o abrir el archivo: {e}"
            CTkMessagebox(title="Warning Message!", message=mssg,
                          icon="warning")


    def switch_economic(self):
        #color predefinido para las letras
        common_fg_color = "#171717"

        if self.economic_switch.get() == "pem":
            self.economic_frame.destroy()

            self.economic_frame = customtkinter.CTkFrame(self.tab_view.tab("Datos Económicos"), corner_radius=0)
            self.economic_frame.grid(row=3, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew",columnspan=2)
            self.economic_frame.grid_columnconfigure(0, weight=1)
            self.economic_frame.grid_columnconfigure(1, weight=10)

            # almacena gasto generales
            self.gg_project_label = customtkinter.CTkLabel(self.economic_frame,
                                                           text="% GASTOS GENERALES:",
                                                           anchor="e",
                                                           font=customtkinter.CTkFont(size=15, weight="bold"),
                                                           width=50)
            self.gg_project_label.grid(row=0, column=0, padx=(30, 10), pady=10, sticky="e")
            self.gg_project_entry = customtkinter.CTkEntry(self.economic_frame,
                                                           placeholder_text="añada los gastos generales del proyecto",
                                                           fg_color=common_fg_color, text_color="#FFFFFF")
            self.gg_project_entry.grid(row=0, column=1, padx=(5, 30), pady=10, sticky="ew")

            # almacena beneficio industrial
            self.bi_project_label = customtkinter.CTkLabel(self.economic_frame,
                                                           text="% BENEFICIO INDUSTRIAL:",
                                                           anchor="e",
                                                           font=customtkinter.CTkFont(size=15, weight="bold"),
                                                           width=50)
            self.bi_project_label.grid(row=1, column=0, padx=(30, 10), pady=10, sticky="e")
            self.bi_project_entry = customtkinter.CTkEntry(self.economic_frame,
                                                           placeholder_text="añada el benedicio industrial del proyecto",
                                                           fg_color=common_fg_color, text_color="#FFFFFF")
            self.bi_project_entry.grid(row=1, column=1, padx=(5, 30), pady=10, sticky="ew")

            # almacena IVA
            self.iva_project_label = customtkinter.CTkLabel(self.economic_frame,
                                                           text="% IVA:",
                                                           anchor="e",
                                                           font=customtkinter.CTkFont(size=15, weight="bold"),
                                                           width=50)
            self.iva_project_label.grid(row=2, column=0, padx=(30, 10), pady=10, sticky="e")
            self.iva_project_entry = customtkinter.CTkEntry(self.economic_frame,
                                                           placeholder_text="añada el IVA del proyecto",
                                                           fg_color=common_fg_color, text_color="#FFFFFF")
            self.iva_project_entry.grid(row=2, column=1, padx=(5, 30), pady=10, sticky="ew")
        else:
            self.economic_frame.destroy()

            self.economic_frame = customtkinter.CTkFrame(self.tab_view.tab("Datos Económicos"), corner_radius=0)
            self.economic_frame.grid(row=3, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew",columnspan=2)
            self.economic_frame.grid_columnconfigure(0, weight=1)
            self.economic_frame.grid_columnconfigure(1, weight=10)

            self.default1_project_label = customtkinter.CTkLabel(self.economic_frame,
                                                                 text=f"Por defecto, se aplicará los siguientes gastos sobre el presupuesto de ejecución material:",
                                                                 anchor="e",
                                                                 font=customtkinter.CTkFont(size=15),
                                                                 width=50)
            self.default1_project_label.grid(row=0, column=0, padx=(30, 10), pady=10, sticky="w")
            self.default2_project_label = customtkinter.CTkLabel(self.economic_frame,
                                                                 text=f"- Gastos generales: 13%",
                                                                 anchor="e",
                                                                 font=customtkinter.CTkFont(size=15, weight="bold"),
                                                                 width=50)
            self.default2_project_label.grid(row=1, column=0, padx=(30, 10), pady=10, sticky="w")
            self.default3_project_label = customtkinter.CTkLabel(self.economic_frame,
                                                                 text=f"- Beneficio industrial: 6% ",
                                                                 anchor="e",
                                                                 font=customtkinter.CTkFont(size=15, weight="bold"),
                                                                 width=50)
            self.default3_project_label.grid(row=2, column=0, padx=(30, 10), pady=10, sticky="w")
            self.default4_project_label = customtkinter.CTkLabel(self.economic_frame,
                                                                 text=f"- IVA: 21% ",
                                                                 anchor="e",
                                                                 font=customtkinter.CTkFont(size=15, weight="bold"),
                                                                 width=50)
            self.default4_project_label.grid(row=3, column=0, padx=(30, 10), pady=10, sticky="w")


    # --------------------------------------FRAME GESTION PROYECTOS------------------------------------------------------------------

    def update_data_project_frame_manager(self, access):

        self.data_project_frame.grid(row=1, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=2)
        self.data_project_frame.grid_columnconfigure(0, weight=1)
        self.data_project_frame.grid_columnconfigure(1, weight=1)
        self.data_project_frame.grid_columnconfigure(2, weight=1)
        self.data_project_frame.grid_columnconfigure(3, weight=1)


        self.general_label = customtkinter.CTkLabel(self.data_project_frame,
                                                                text="DATOS GENERALES",
                                                                anchor="center",
                                                                font=customtkinter.CTkFont(size=15, weight="bold"))
        self.general_label.grid(row=0, column=0, padx=30, pady=10, sticky="nsew", columnspan=4)

        #color predefinido para las letras
        common_fg_color = "#171717"

        #recoge proyecto seleccionado
        project_select = self.project_option_project_filter.get()
        code_project_select = project_select .split(" - ")[0]
        code_project_select = str(code_project_select)
        project_data = get_filter_data_bd(access[0], access[1], 'tbl_proyectos', 'manager', 'codigo', code_project_select)[0]


        #almacena código proyecto
        self.code_project_label = customtkinter.CTkLabel(self.data_project_frame, text="CÓDIGO PROYECTO:",
                                                         anchor="e", font=customtkinter.CTkFont(size=12, weight="bold"),
                                                         width= 50)
        self.code_project_label.grid(row=1, column=0, padx=(30,5), pady=5, sticky= "e")
        code_project = tk.StringVar(value=project_data[1])
        self.code_project_manager_entry = customtkinter.CTkEntry(self.data_project_frame, textvariable=code_project,
                                                         fg_color=common_fg_color,text_color="#FFFFFF",
                                                         state="readonly")
        self.code_project_manager_entry.grid(row=1, column=1, padx=(5,30), pady=5, sticky= "ew")

        #almacena nombre proyecto
        self.name_project_label = customtkinter.CTkLabel(self.data_project_frame, text="NOMBRE PROYECTO:",
                                                         anchor="e", font=customtkinter.CTkFont(size=12, weight="bold"),
                                                         width= 50)
        self.name_project_label.grid(row=2, column=0, padx=(30,5), pady=5, sticky= "e")
        name_project = tk.StringVar(value=project_data[2])
        self.name_project_manager_entry = customtkinter.CTkEntry(self.data_project_frame,textvariable=name_project,
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.name_project_manager_entry.grid(row=2, column=1, padx=(5,30), pady=5, sticky= "ew")

        # almacena CCAA del proyecto
        self.ccaa_project_label = customtkinter.CTkLabel(self.data_project_frame, text="COMUNIDAD AUTÓNOMA:",
                                                           anchor="e", font=customtkinter.CTkFont(size=12, weight="bold"),
                                                           width= 50)
        self.ccaa_project_label.grid(row=3, column=0, padx=(30, 5), pady=5, sticky="e")
        select_ccaa = get_option_item_sub_bd(self.user, self.password, 'list_ccaa', 'manager', "NAMEUNIT", project_data[13],'id')
        code_ccaa = get_code_ccaa_bd(self.user, self.password, select_ccaa[0])
        ccaa_project = tk.StringVar(value=select_ccaa[0])
        self.ccaa_project_manager_entry = customtkinter.CTkEntry(self.data_project_frame, textvariable=ccaa_project,
                                                         fg_color=common_fg_color,text_color="#FFFFFF",
                                                         state="readonly")
        self.ccaa_project_manager_entry.grid(row=3, column=1, padx=(5,30), pady=5, sticky= "ew")

        #almacena provincia del proyectO
        self.province_project_label = customtkinter.CTkLabel(self.data_project_frame, text="PROVINCIA:",
                                                           anchor="e", font=customtkinter.CTkFont(size=12, weight="bold"),
                                                           width= 50)
        self.province_project_label.grid(row=4, column=0, padx=(30, 5), pady=5, sticky="e")
        select_province = get_option_item_sub_bd(self.user, self.password, 'list_provincias', 'manager',
                                                 "NAMEUNIT", project_data[12], 'id')
        province_project = tk.StringVar(value=select_province[0])
        self.province_project_manager_entry = customtkinter.CTkEntry(self.data_project_frame, textvariable=province_project,
                                                         fg_color=common_fg_color,text_color="#FFFFFF",
                                                         state="readonly")
        self.province_project_manager_entry .grid(row=4, column=1, padx=(5,30), pady=5, sticky= "ew")


        #almacena descripción proyecto
        self.description_project_label = customtkinter.CTkLabel(self.data_project_frame, text="DESCRIPCIÓN PROYECTO",
                                                                anchor="center",font=customtkinter.CTkFont(size=12, weight="bold"),
                                                                width= 50)
        self.description_project_label.grid(row=1, column=2, padx=30, pady=5, sticky= "news", columnspan=2)
        self.description_project_manager_entry = customtkinter.CTkTextbox(self.data_project_frame, fg_color=common_fg_color, height=100,
                                                                 border_width=2, border_color="#565B5E",text_color="#FFFFFF")
        self.description_project_manager_entry.grid(row=2, column=2, padx=30, pady=5, sticky= "ew",columnspan=2, rowspan=3)
        self.description_project_manager_entry.insert("0.0", project_data[9])

        #almacena directorio de trabajo
        self.folder_project_label = customtkinter.CTkLabel(self.data_project_frame, text="DIRECTORIO PROYECTO:",
                                                           anchor="e", font=customtkinter.CTkFont(size=12, weight="bold"),
                                                           width= 50)
        self.folder_project_label.grid(row=5, column=0, padx=(30, 5), pady=5, sticky="e")
        directory_project = tk.StringVar(value=project_data[14])
        # Crear un Entry para mostrar la ruta del directorio
        self.folder_project_manager_entry = customtkinter.CTkEntry(self.data_project_frame,fg_color=common_fg_color,
                                                           textvariable=directory_project,text_color="#FFFFFF")
        self.folder_project_manager_entry.grid(row=5, column=1, padx=5, pady=5, sticky= "ew",columnspan=2)
        # Crear un botón para abrir el diálogo de selección de directorio
        self.folder_project_button = customtkinter.CTkButton(self.data_project_frame, text="Seleccionar Directorio",
                                                             command=self.select_directory, width=50)
        self.folder_project_button.grid(row=5, column=3, padx=(5,30), pady=5, sticky= "ew")

        #Responsables y cliente
        self.responsibility_label = customtkinter.CTkLabel(self.data_project_frame,
                                                                text="RESPONSABLES Y CLIENTE",
                                                                anchor="center",
                                                                font=customtkinter.CTkFont(size=15, weight="bold"))
        self.responsibility_label.grid(row=6, column=0, padx=30, pady=10, sticky="nsew", columnspan=4)

        # almacena cliente del proyecto
        self.customer_project_label = customtkinter.CTkLabel(self.data_project_frame, text="SELECCIÓN DE CLIENTE:",
                                                           anchor="e", font=customtkinter.CTkFont(size=12, weight="bold"),
                                                           width= 50)
        self.customer_project_label.grid(row=7, column=0, padx=(30, 5), pady=5, sticky="e")
        customer_value=get_option_item_bd(self.user, self.password, "tbl_cliente", "manager", 'nombre')
        self.customer_manager_option = customtkinter.CTkOptionMenu(self.data_project_frame,
                                                         dynamic_resizing=False,
                                                         values=customer_value,
                                                         command= lambda event:self.update_customer_data(access))
        self.customer_manager_option.grid(row=7, column=1, padx=5, pady=5, sticky= "ew")
        self.customer_manager_option.bind("<<ComboboxSelected>>", lambda event: self.update_customer_data(access))
        select_customer = get_option_item_sub_bd(self.user, self.password, 'tbl_cliente', 'manager',
                                                 "nombre", project_data[3],'id')
        self.customer_manager_option.set(select_customer[0])

        # Crear un botón para añadir cliente
        self.add_customer_button = customtkinter.CTkButton(self.data_project_frame, text="Añadir Cliente",
                                                             command=lambda: self.add_customer(access), width=100)
        self.add_customer_button.grid(row=7, column=2, padx=5, pady=5, sticky= "ew")

        # Crear un botón para modificar cliente
        self.update_customer_button = customtkinter.CTkButton(self.data_project_frame, text="Modificar Cliente",
                                                             command=lambda: self.mod_customer(access), width=100)
        self.update_customer_button.grid(row=7, column=3, padx=(5,30), pady=5, sticky= "ew")

        #responsble ciente
        id_users_customer = get_option_item_sub_bd(access[0], access[1], "tbl_clie_usuario", "manager", 'id',
                                                   project_data[3], 'id_cliente')
        self.user_customer_project_label = customtkinter.CTkLabel(self.data_project_frame,
                                                                  text="RESPONSABLE CLIENTE:",
                                                                  anchor="center",
                                                                  font=customtkinter.CTkFont(size=12,
                                                                                             weight="bold"),
                                                                  width=50)
        self.user_customer_project_label.grid(row=8, column=0, padx=(30, 5), pady=5, sticky="e")
        users_customer_value = []
        for item in id_users_customer:
            user_surname_value = get_option_item_sub_bd(access[0], access[1], "tbl_clie_usuario", "manager",
                                                        'apellidos',
                                                        item, 'id')
            user_name_value = get_option_item_sub_bd(access[0], access[1], "tbl_clie_usuario", "manager", 'nombre',
                                                     item, 'id')
            value = user_surname_value[0] + ", " + user_name_value[0]
            users_customer_value.append(value)
        users_customer_value.sort(key=str.lower)
        self.user_customer_manager_option = customtkinter.CTkOptionMenu(self.data_project_frame,
                                                                dynamic_resizing=False,
                                                                values=users_customer_value)
        self.user_customer_manager_option.grid(row=8, column=1, padx=5, pady=5, sticky="ew")
        user_surname_customer_select = get_option_item_sub_bd(access[0], access[1], "tbl_clie_usuario", "manager",
                                                    'apellidos',
                                                    project_data[4], 'id')
        user_name_customer_select = get_option_item_sub_bd(access[0], access[1], "tbl_clie_usuario", "manager", 'nombre',
                                                 project_data[4], 'id')
        user_customer_select = user_surname_customer_select[0] + ", " + user_name_customer_select[0]
        self.user_customer_manager_option.set(user_customer_select)

        # Botón para añadir responsable del cliente
        self.add_user_customer_button = customtkinter.CTkButton(self.data_project_frame, text="Añadir Responsable",
                                                                command=lambda: self.add_user_customer(access),
                                                                width=100)
        self.add_user_customer_button.grid(row=8, column=2, padx=5, pady=5, sticky="ew")

        # Botón para modificar responsable del cliente
        self.update_customer_button = customtkinter.CTkButton(self.data_project_frame, text="Modificar Responsable",
                                                              command=lambda: self.mod_user_customer(access), width=100)
        self.update_customer_button.grid(row=8, column=3, padx=(5, 30), pady=5, sticky="ew")


        # Responsable proyecto
        self.user_company_project_label = customtkinter.CTkLabel(self.data_project_frame,
                                                                 text="RESPONSABLE PROYECTO:",
                                                                 anchor="center",
                                                                 font=customtkinter.CTkFont(size=12,
                                                                                            weight="bold"))
        self.user_company_project_label.grid(row=9, column=0, padx=(30, 5), pady=5, sticky="e")

        id_users_company = get_option_item_bd(access[0], access[1], "tbl_empr_usuario", "manager","id")
        users_company_value = []
        for item in id_users_company:
            user_surname_value = get_option_item_sub_bd(access[0], access[1], "tbl_empr_usuario", "manager",
                                                        'apellidos',
                                                        item, 'id')
            user_name_value = get_option_item_sub_bd(access[0], access[1], "tbl_empr_usuario", "manager",
                                                     'nombre',
                                                     item, 'id')
            value = user_surname_value[0] + ", " + user_name_value[0]
            users_company_value.append(value)
        users_company_value.sort(key=str.lower)
        self.user_company_manager_option = customtkinter.CTkOptionMenu(self.data_project_frame,
                                                               dynamic_resizing=False,
                                                               values=users_company_value)
        self.user_company_manager_option.grid(row=9, column=1, padx=5, pady=5, sticky="ew")
        user_surname_company_select = get_option_item_sub_bd(access[0], access[1], "tbl_empr_usuario", "manager",
                                                    'apellidos',project_data[6], 'id')
        user_name_company_select = get_option_item_sub_bd(access[0], access[1], "tbl_empr_usuario", "manager", 'nombre',
                                                 project_data[6], 'id')
        user_company_select = user_surname_company_select[0] + ", " + user_name_company_select[0]
        self.user_company_manager_option.set(user_company_select)

        # Botón para añadir responsable del cliente
        self.add_user_company_button = customtkinter.CTkButton(self.data_project_frame,
                                                               text="Añadir Responsable",
                                                               command=lambda: self.add_user_company(access),
                                                               width=100)
        self.add_user_company_button.grid(row=9, column=2, padx=5, pady=5, sticky="ew")

        # Botón para modificar responsable del cliente
        self.update_company_button = customtkinter.CTkButton(self.data_project_frame,
                                                             text="Modificar Responsable",
                                                             command=lambda: self.mod_user_company(access),
                                                             width=100)
        self.update_company_button.grid(row=9, column=3, padx=(5, 30), pady=5, sticky="ew")


        #Datos económicos
        self.economic_label = customtkinter.CTkLabel(self.data_project_frame,
                                                                text="DATOS ECONÓMICOS",
                                                                anchor="center",
                                                                font=customtkinter.CTkFont(size=15, weight="bold"))
        self.economic_label.grid(row=10, column=0, padx=30, pady=10, sticky="nsew", columnspan=4)

        economic_data_project = get_filter_data_bd(self.user, self.password, "tbl_proy_presupuesto", "manager",
                                                   "id_proyecto", str(project_data[0]))[0]

        # almacena presupuesto de licitación
        self.tender_project_label = customtkinter.CTkLabel(self.data_project_frame,
                                                           text="PRESUPUESTO DE LICITACIÓN (SIN IVA):",
                                                           anchor="e",
                                                           font=customtkinter.CTkFont(size=12, weight="bold"),
                                                           width=50)
        self.tender_project_label.grid(row=11, column=0, padx=(30, 5), pady=5, sticky="e")
        tender_project = tk.StringVar(value=economic_data_project[6])
        self.tender_project_manager_entry = customtkinter.CTkEntry(self.data_project_frame,
                                                           textvariable=tender_project,
                                                           fg_color=common_fg_color, text_color="#FFFFFF")
        self.tender_project_manager_entry.grid(row=11, column=1, padx=(5, 30), pady=5, sticky="ew")

        # almacena baja de licitación
        self.reduction_project_label = customtkinter.CTkLabel(self.data_project_frame,
                                                              text="% BAJA:",
                                                              anchor="e",
                                                              font=customtkinter.CTkFont(size=12, weight="bold"),
                                                              width=50)
        self.reduction_project_label.grid(row=12, column=0, padx=(30, 5), pady=5, sticky="e")
        reduction_project = tk.StringVar(value=economic_data_project[5])
        self.reduction_project_manager_entry = customtkinter.CTkEntry(self.data_project_frame,
                                                              textvariable=reduction_project,
                                                              fg_color=common_fg_color, text_color="#FFFFFF")
        self.reduction_project_manager_entry.grid(row=12, column=1, padx=(5, 30), pady=5, sticky="ew")

        # almacena gasto generales
        self.gg_project_label = customtkinter.CTkLabel(self.data_project_frame,
                                                       text="% GASTOS GENERALES:",
                                                       anchor="e",
                                                       font=customtkinter.CTkFont(size=12, weight="bold"),
                                                       width=50)
        self.gg_project_label.grid(row=11, column=2, padx=(30, 5), pady=5, sticky="e")
        gg_project = tk.StringVar(value=economic_data_project[3])
        self.gg_project_manager_entry = customtkinter.CTkEntry(self.data_project_frame,
                                                       textvariable=gg_project,
                                                       fg_color=common_fg_color, text_color="#FFFFFF")
        self.gg_project_manager_entry.grid(row=11, column=3, padx=(5, 30), pady=5, sticky="ew")

        # almacena beneficio industrial
        self.bi_project_label = customtkinter.CTkLabel(self.data_project_frame,
                                                       text="% BENEFICIO INDUSTRIAL:",
                                                       anchor="e",
                                                       font=customtkinter.CTkFont(size=12, weight="bold"),
                                                       width=50)
        self.bi_project_label.grid(row=12, column=2, padx=(30, 5), pady=5, sticky="e")
        bi_project = tk.StringVar(value=economic_data_project[4])
        self.bi_project_manager_entry = customtkinter.CTkEntry(self.data_project_frame,
                                                       textvariable=bi_project,
                                                       fg_color=common_fg_color, text_color="#FFFFFF")
        self.bi_project_manager_entry.grid(row=12, column=3, padx=(5, 30), pady=5, sticky="ew")

        # almacena IVA
        self.iva_project_label = customtkinter.CTkLabel(self.data_project_frame,
                                                        text="% IVA:",
                                                        anchor="e",
                                                        font=customtkinter.CTkFont(size=12, weight="bold"),
                                                        width=50)
        self.iva_project_label.grid(row=13, column=2, padx=(30, 5), pady=5, sticky="e")
        iva_project = tk.StringVar(value=economic_data_project[7])
        self.iva_project_manager_entry = customtkinter.CTkEntry(self.data_project_frame,
                                                        textvariable=iva_project,
                                                        fg_color=common_fg_color, text_color="#FFFFFF")
        self.iva_project_manager_entry.grid(row=13, column=3, padx=(5, 30), pady=5, sticky="ew")


        # filtro para estado proyecto
        self.state_option_project_label = customtkinter.CTkLabel(self.data_project_frame,
                                                                text="ESTADO PROYECTO:",
                                                                anchor="center",
                                                                font=customtkinter.CTkFont(size=15, weight="bold"))
        self.state_option_project_label.grid(row=14, column=0, padx=30, pady=10, sticky="nsew")
        state_values =  get_option_item_bd(self.user,self.password, "tbl_proy_estado","manager",'estado')
        self.state_option_manager_project = customtkinter.CTkOptionMenu(self.data_project_frame,
                                                                      dynamic_resizing=False,
                                                                      values=state_values)
        self.state_option_manager_project.grid(row=14, column=1, padx=30, pady=10, sticky="nsew", columnspan=3)
        self.state_option_manager_project.set(get_option_item_sub_bd(self.user,self.password, "tbl_proy_estado","manager", 'estado',str(project_data[11]),'id'))


    def project_filter_project_event(self,access):
        #actualizamos el frame de los datos de los usuarios del proyecto
        self.data_project_frame.destroy()
        self.data_project_frame = customtkinter.CTkScrollableFrame(self.project_frame, corner_radius=0)
        self.update_data_project_frame_manager(access)


    def save_project_event(self,access):

        code_project = self.code_project_manager_entry.get()
        name_project = self.name_project_manager_entry.get()
        description_project = self.description_project_manager_entry.get("1.0", "end-1c")
        path_project = self.folder_project_manager_entry.get()
        customer_project = self.customer_manager_option.get()
        user_customer_project = self.user_customer_manager_option.get()
        user_client_project = self.user_company_manager_option.get()
        tender_project = self.tender_project_manager_entry.get()
        tender_project = tender_project.replace("€", "").replace(",", ".").replace("E", "")
        reduction_project = self.reduction_project_manager_entry.get()
        reduction_project = reduction_project.replace("%", "").replace(",", ".")
        gg_project = self.gg_project_manager_entry.get()
        gg_project = gg_project.replace("%", "").replace(",", ".")
        bi_project = self.bi_project_manager_entry.get()
        bi_project = bi_project.replace("%", "").replace(",", ".")
        iva_project = self.iva_project_manager_entry.get()
        iva_project = iva_project.replace("%", "").replace(",", ".")
        state_project = self.state_option_manager_project.get()

        none_value = []


        if name_project == "":
            none_value.append("nombre de proyecto")
        if path_project == "":
            none_value.append("carpeta del proyecto")
        if tender_project == "":
            none_value.append("presupuesto")
        if reduction_project == "":
            none_value.append("baja")
        if gg_project == "":
            none_value.append("gastos generales")
        if bi_project == "":
            none_value.append("beneficio industrial")
        if iva_project == "":
            none_value.append("iva")


        if len(none_value) == 0:
            # insertar registros en tbl_proyectos
            data_project = {
                "name": name_project,
                "description": description_project,
                "folder": path_project,
                "id_customer": get_id_item_bd(access[0], access[1], "tbl_cliente", "manager", "nombre",
                                              customer_project),
                "id_user_customer": get_id_user_customer(access[0], access[1], user_customer_project,
                                                         get_id_item_bd(access[0], access[1], "tbl_cliente", "manager", "nombre", customer_project)),
                "company": "OBRAS Y SERVICIOS ARTANDA",
                "id_user_company": get_id_user_company(access[0], access[1], user_client_project),
                "id_state": get_id_item_bd(access[0], access[1], "tbl_proy_estado","manager",'estado',state_project)
            }

            data_tender = {
                "tender": tender_project,
                "reduction": reduction_project,
                "gg": gg_project,
                "bi": bi_project,
                "iva": iva_project
            }

            code_project_select = code_project.split(" - ")[0]
            code_project_select = str(code_project_select)
            id_project = get_filter_data_bd(access[0], access[1], 'tbl_proyectos', 'manager', 'codigo', code_project_select)[0][0]
            result = mod_project_item(access[0], access[1], data_project,data_tender,id_project)
            if result == "ok":
                mssg = "Se ha modificado el proyecto " + code_project + " en la base de datos"
                CTkMessagebox(title="Successfull Message!", message=mssg,
                              icon="check")
            else:
                mssg = f"ERROR: '{result}' "
                CTkMessagebox(title="Error", message=mssg, icon="cancel")
        else:
            mssg = "Es necesario rellenar los siguiente campos obligatorios:\n\n"
            value = ""
            for item in none_value:
                value += "  -  " + item + "\n"
            mssg += value + "\n Error: No se puede crear el proyecto sin los campos obligatorios"
            CTkMessagebox(title="Error", message=mssg, icon="cancel", width=500)


# --------------------------------------FRAME USUARIOS------------------------------------------------------------------

    def update_data_user_frame_manager (self,access,users_project):

        self.data_user_frame.grid(row=2, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=3)
        self.data_user_frame.grid_columnconfigure(0, weight=1)
        self.data_user_frame.grid_columnconfigure(1, weight=1)
        self.data_user_frame.grid_columnconfigure(2, weight=1)
        self.data_user_frame.grid_columnconfigure(3, weight=1)

        # cargar imagen de icono
        image_password_path = parent_path +"/source/contraseña.png"
        self.password_image = customtkinter.CTkImage(Image.open(image_password_path), size=(20,20))
        image_update_path = parent_path +"/source/permisos.png"
        self.update_image = customtkinter.CTkImage(Image.open(image_update_path), size=(20,20))

        # Listas para almacenar las variables por fila
        self.user_items_project = []
        self.role_items_project = []
        self.user_privilege_option = []

        #Encabezdos
        self.username_label = customtkinter.CTkLabel(self.data_user_frame, text="Usuario",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=13, weight="bold"))
        self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky="nwes")

        self.role_label = customtkinter.CTkLabel(self.data_user_frame, text="Rol asignado",
                                                      anchor="center",
                                                      font=customtkinter.CTkFont(size=13, weight="bold"))
        self.role_label.grid(row=0, column=1, padx=5, pady=5, sticky="nwes")

        #contenido de la tabla
        i=0
        for  i, (key, value) in enumerate(users_project.items()):
            i+=1
            user_db = key.split('@')[0].replace("'","")
            self.user_items_project.append(user_db)
            privileges_project= set(value)
            list_privileges_admin = set(['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'REFERENCES', 'INDEX', 'ALTER', 'CREATE TEMPORARY TABLES', 'LOCK TABLES', 'EXECUTE', 'CREATE VIEW', 'SHOW VIEW', 'CREATE ROUTINE', 'ALTER ROUTINE', 'EVENT', 'TRIGGER'])
            list_privileges_writer = set(['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'ALTER'])
            list_privileges_reader = set(['SELECT'])
            privileges_bd_value = ['Administrador', 'Escritura y lectura', 'Solo lectura']

            self.user_manager_label = customtkinter.CTkLabel(self.data_user_frame, text=user_db,
                                                  anchor="center",
                                                  font=customtkinter.CTkFont(size=14))
            self.user_manager_label.grid(row=i, column=0, padx=(30,10), pady=10, sticky="nwes")
            initial_option=""
            if privileges_project == list_privileges_admin:
                initial_option='Administrador'
            elif privileges_project==list_privileges_writer:
                initial_option='Escritura y lectura'
            elif privileges_project == list_privileges_reader:
                initial_option='Solo lectura'

            # almacena el tipo de rol asignado al usuarioa
            option_menu = customtkinter.CTkOptionMenu(
                self.data_user_frame,
                dynamic_resizing=False,
                values=privileges_bd_value,
                command=lambda value, i=i: self.update_privilege_option(i)
            )

            # Configurar el valor inicial
            option_menu.set(initial_option)

            # Posicionar el widget en la cuadrícula
            option_menu.grid(row=i, column=1, padx=10, pady=10, sticky="nwes")

            # Almacenar el widget en la lista
            self.user_privilege_option.append(option_menu)

            self.role_items_project.append(option_menu.get())
            
            #botones para cambiar contraseña y actualizar privilegios
            self.password_button_user = customtkinter.CTkButton(self.data_user_frame, image=self.password_image,
                                                                text="Cambiar contraseña",
                                                                command=lambda i=i: self.change_password(i, access),
                                                                width=30)
            self.password_button_user.grid(row=i, column=2, padx=10, pady=10, sticky="nwes")

            self.privileges_button_user = customtkinter.CTkButton(self.data_user_frame, image=self.update_image,
                                                                text="Cambiar privilegios",
                                                                command=lambda i=i: self.change_privileges(i, access),
                                                                width=30)
            self.privileges_button_user.grid(row=i, column=3, padx=(10,30), pady=10, sticky="nwes")


    def update_privilege_option(self, i):
        # Obtener el nuevo valor seleccionado
        new_privilege = self.user_privilege_option[i-1].get()
        # Actualizar el valor en role_items_project
        self.role_items_project[i - 1] = new_privilege


    def change_password(self, i,access):
        user_select = self.user_items_project[i - 1]
        newpassword = create_pass()
        change_pass_user(access[0], access[1],user_select, newpassword)

        # Copiar la contraseña al portapapeles
        pyperclip.copy(newpassword)

        mssg = f"La contraseña del usuario ({user_select}) se ha actualizado:\n {newpassword} \n\n\nADVERTENCIA: Se ha copiado la contraseña en su portapapeles, asegúrese de pegarla para poder compartirla"
        CTkMessagebox(title="Successful!", message=mssg,
                              icon="check")


    def change_privileges(self, i, access):
        user_select = self.user_items_project[i - 1]
        privileges_select = self.role_items_project[i - 1]
        project_select = self.project_option_user_filter.get()
        code_project_select = project_select.split(" - ")[0]
        code_project_select = str(code_project_select)
        revoke_privileges(access[0], access[1], user_select, code_project_select)
        add_privileges(access[0], access[1], code_project_select, user_select, privileges_select)

        mssg = f"Se han actualizado el rol del usuario : {user_select}"
        CTkMessagebox(title="Successful!", message=mssg,
                              icon="check")


    def project_filter_user_event(self,access):
        #recoge proyecto seleccionado
        project_select = self.project_option_user_filter.get()
        code_project_select = project_select .split(" - ")[0]
        code_project_select = str(code_project_select)
        #usuarios para proyecto seleccionado
        privileges_users_project= get_all_bd(access[0], access[1], 'vw_esquema_usuarios', 'manager')
        roles_project = defaultdict(list)
        for item in privileges_users_project:
            if str(item[2]).lower() == code_project_select.lower():
                user_project=item[0]
                privilege=item[3]
                roles_project[user_project].append(privilege)

        #actualizamos el frame de los datos de los usuarios del proyecto
        self.data_user_frame.destroy()
        self.data_user_frame = customtkinter.CTkScrollableFrame(self.user_frame, corner_radius=0)
        self.update_data_user_frame_manager(access,roles_project)


    def create_user_manager(self,access):
        appAux10=AppUserBdAddNew(access)
        appAux10.grab_set()
        self.wait_window(appAux10)


    def delete_user_manager(self,access):
        # recoge proyecto seleccionado
        project_select = self.project_option_user_filter.get()
        code_project_select = project_select.split(" - ")[0]
        code_project_select = str(code_project_select)

        # usuarios para proyecto seleccionado
        privileges_users_project = get_all_bd(access[0], access[1], 'vw_esquema_usuarios', 'manager')
        roles_project = defaultdict(list)
        for item in privileges_users_project:
            if str(item[2]).lower() == code_project_select.lower():
                user_project = item[0]
                privilege = item[3]
                roles_project[user_project].append(privilege)

        #revoca los permisos para el proyecto seleccionado para los usuario seleccionados en el combox
        users_project = list(roles_project.keys())
        users_project = [user.split("@")[0].replace("'","") for user in users_project]
        appAux11 = AppCombox(users_project, lambda selected_items: self.revoke_role_users(access,selected_items,code_project_select))
        appAux11.grab_set()
        self.wait_window(appAux11)

        # usuarios para proyecto seleccionado
        privileges_users_project = get_all_bd(access[0], access[1], 'vw_esquema_usuarios', 'manager')
        roles_project = defaultdict(list)
        for item in privileges_users_project:
            if str(item[2]).lower() == code_project_select.lower():
                user_project = item[0]
                privilege = item[3]
                roles_project[user_project].append(privilege)
        self.data_user_frame.destroy()
        self.data_user_frame = customtkinter.CTkScrollableFrame(self.user_frame, corner_radius=0)
        self.update_data_user_frame_manager(access,roles_project)


    def revoke_role_users(self, access,selected_items,select_project):
        for item in selected_items:
            revoke_privileges(access[0], access[1], item, select_project)


    def add_user_manager(self,access):
        project_select = self.project_option_user_filter.get()
        code_project_select = project_select.split(" - ")[0]
        #asigna por defecto rol de lectura y lo añade al proyecto
        users_value = get_user_db (access[0], access[1])
        appAux9 =  AppCombox(users_value, lambda selected_items: self.add_role_default_users(access,selected_items,code_project_select))
        appAux9.grab_set()
        self.wait_window(appAux9)

        # recoge proyecto seleccionado
        project_select = self.project_option_user_filter.get()
        code_project_select = project_select.split(" - ")[0]
        code_project_select = str(code_project_select)

        # usuarios para proyecto seleccionado
        privileges_users_project = get_all_bd(access[0], access[1], 'vw_esquema_usuarios', 'manager')
        roles_project = defaultdict(list)
        for item in privileges_users_project:
            if str(item[2]).lower() == code_project_select.lower():
                user_project = item[0]
                privilege = item[3]
                roles_project[user_project].append(privilege)
        self.data_user_frame.destroy()
        self.data_user_frame = customtkinter.CTkScrollableFrame(self.user_frame, corner_radius=0)
        self.update_data_user_frame_manager(access,roles_project)


    def add_role_default_users(self, access,selected_items,select_project):
        for item in selected_items:
            add_privileges(access[0], access[1], select_project, item, "Escritura y lectura")


    # --------------------------------------FRAME CERTIFICACIONES------------------------------------------------------------------

    def update_data_cost_frame_manager(self, access):

        self.data_cost_frame.grid(row=2, column=0, padx=30, pady=5, sticky="nsew", columnspan=3)
        self.data_cost_frame.grid_columnconfigure(0, weight=1)
        self.data_cost_frame.grid_columnconfigure(1, weight=1)
        self.data_cost_frame.grid_columnconfigure(2, weight=1)
        self.data_cost_frame.grid_columnconfigure(3, weight=1)

        # cargar imagen de icono
        image_password_path = parent_path + "/source/contraseña.png"
        self.password_image = customtkinter.CTkImage(Image.open(image_password_path), size=(20, 20))
        image_update_path = parent_path + "/source/permisos.png"
        self.update_image = customtkinter.CTkImage(Image.open(image_update_path), size=(20, 20))

        # Listas para almacenar las variables por fila
        self.user_items_project = []
        self.role_items_project = []
        self.user_privilege_option = []


        # recoge proyecto seleccionado
        project_select = self.project_option_cost_filter.get()
        code_project_select = project_select.split(" - ")[0]
        code_project_select = str(code_project_select)
        # presupuesto y certificaciones para proyecto seleccionado
        total_budget_project = sum_field_bd(access[0], access[1],'coste_total', 'cod_proyecto', code_project_select, 'vw_presupuesto')
        total_yescost_project = sum_field_filter_bd(access[0], access[1], 'coste_total', 'cod_proyecto', code_project_select, 'vw_certificaciones', 'certificada','1')
        total_nocost_project = sum_field_filter_bd(access[0], access[1], 'coste_total', 'cod_proyecto', code_project_select, 'vw_certificaciones', 'certificada','0')


        if total_budget_project:
            total_budget = total_budget_project[0][0]
        else:
            total_budget = 0

        if total_yescost_project:
            total_yescost = total_yescost_project[0][0]
        else:
            total_yescost = 0

        if total_nocost_project:
            total_nocost = total_nocost_project[0][0]
        else:
            total_nocost = 0

        total_cost = total_yescost + total_nocost

        print(total_cost)
        view_cost = get_all_bd(access[0], access[1],'vw_certificaciones', code_project_select)
        dict_cost = defaultdict(list)
        for item in view_cost:
            if item[14]==1:
                date_cost = str(item[13].year)+'-'+str(item[13].month)
                dict_cost[date_cost].append(item[10])


        # presupuesto total
        self.total_budget_manager_label = customtkinter.CTkLabel(self.data_cost_frame,
                                                                text="Presupuesto Total:",
                                                                anchor="center",
                                                                font=customtkinter.CTkFont(size=15, weight="bold"))
        self.total_budget_manager_label.grid(row=0, column=0, padx=(30,5), pady=10, sticky="nsew")
        self.total_budget_manager = customtkinter.CTkLabel(self.data_cost_frame,
                                                                text=f"{total_budget:.2f}€",
                                                                anchor="center",
                                                                font=customtkinter.CTkFont(size=15))
        self.total_budget_manager.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

        if total_budget- total_cost >= 0:
            color_font = "green4"
        else:
            color_font = "red3"
        # Diferencia
        self.dif_cost_manager_label = customtkinter.CTkLabel(self.data_cost_frame,
                                                             text="Diferencia:",
                                                             anchor="center",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.dif_cost_manager_label.grid(row=0, column=2, padx=5, pady=10, sticky="nsew")
        self.dif_cost_manager = customtkinter.CTkLabel(self.data_cost_frame,
                                                       text=f"{(total_budget - total_cost):.2f}€",
                                                       anchor="center",
                                                       font=customtkinter.CTkFont(size=15),
                                                       text_color=color_font )
        self.dif_cost_manager.grid(row=0, column=3, padx=(5, 30), pady=10, sticky="nsew")

        # total certificado
        self.total_yescost_manager_label = customtkinter.CTkLabel(self.data_cost_frame,
                                                                text="Certificación Acum.:",
                                                                anchor="center",
                                                                font=customtkinter.CTkFont(size=15, weight="bold"))
        self.total_yescost_manager_label.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        self.total_yescost_manager = customtkinter.CTkLabel(self.data_cost_frame,
                                                                text=f"{total_yescost:.2f}€",
                                                                anchor="center",
                                                                font=customtkinter.CTkFont(size=15))
        self.total_yescost_manager.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")

        #pendiente de certificar
        self.total_nocost_manager_label = customtkinter.CTkLabel(self.data_cost_frame,
                                                                text="Pte. Certificación:",
                                                                anchor="center",
                                                                font=customtkinter.CTkFont(size=15, weight="bold"))
        self.total_nocost_manager_label.grid(row=1, column=2, padx=5, pady=10, sticky="nsew")
        self.total_nocost_manager = customtkinter.CTkLabel(self.data_cost_frame,
                                                                text=f"{total_nocost:.2f}€",
                                                                anchor="center",
                                                                font=customtkinter.CTkFont(size=15))
        self.total_nocost_manager.grid(row=1, column=3, padx=5, pady=10, sticky="nsew")

        self.cost_label = customtkinter.CTkLabel(self.data_cost_frame,
                                                 text="CERTIFICACIÓN MENSUAL",
                                                 anchor="center",
                                                 font=customtkinter.CTkFont(size=15, weight="bold"))
        self.cost_label.grid(row=2, column=0, padx=30, pady=10, sticky="nsew", columnspan=4)

        self.data_cost_monthly_frame = customtkinter.CTkScrollableFrame(self.data_cost_frame, corner_radius=0)
        self.data_cost_monthly_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        self.data_cost_monthly_frame.grid_columnconfigure(0, weight=1)
        self.data_cost_monthly_frame.grid_columnconfigure(1, weight=1)


        # Encabezdos
        self.month_label = customtkinter.CTkLabel(self.data_cost_monthly_frame, text="Mes",
                                                     anchor="center",
                                                     font=customtkinter.CTkFont(size=13, weight="bold"))
        self.month_label.grid(row=0, column=0, padx=5, pady=5, sticky="nwes")

        self.cost_label = customtkinter.CTkLabel(self.data_cost_monthly_frame, text="Total (€)",
                                                 anchor="center",
                                                 font=customtkinter.CTkFont(size=13, weight="bold"))
        self.cost_label.grid(row=0, column=1, padx=5, pady=5, sticky="nwes")

        # contenido de la tabla
        i = 0
        for i, (key, value) in enumerate(dict_cost.items()):
            i += 1
            self.month_label = customtkinter.CTkLabel(self.data_cost_monthly_frame, text=key,
                                                             anchor="center",
                                                             font=customtkinter.CTkFont(size=14))
            self.month_label.grid(row=i, column=0, padx=5, pady=5, sticky="nwes")

            self.total_label = customtkinter.CTkLabel(self.data_cost_monthly_frame, text=f"{sum(value):.2f}",
                                                             anchor="center",
                                                             font=customtkinter.CTkFont(size=14))
            self.total_label.grid(row=i, column=1, padx=5, pady=5, sticky="nwes")

        df_cost=pd.DataFrame(view_cost, columns=['id', 'cod_proyecto', 'arqueta', 'cod_partida','naturaleza','unidad', 'resumen', 'descripcion', 'precio_unitario', 'cantidad_certificada', 'coste_total', 'cod_capitulo',' capitulo', 'fecha_certificacion', 'certificada'])
        if len(view_cost)!=0:
            df_cost = df_cost[df_cost['certificada']==1]
            # Extraer mes y año para agrupar
            df_cost['mes'] = df_cost['fecha_certificacion'].dt.month
            df_cost['año'] = df_cost['fecha_certificacion'].dt.year
            # Agrupar por año y mes y calcular la suma del coste total
            df_cost_agrupado = df_cost.groupby(['año', 'mes'])['coste_total'].sum().reset_index()
            # Calcular la suma acumulada del coste total
            df_cost_agrupado['coste_total_acumulado'] = df_cost_agrupado['coste_total'].cumsum()
            df_cost_agrupado=df_cost_agrupado.sort_values(by=['año', 'mes'])

            # Datos gráfico
            x_data = [f'{int(a)}-{int(m)}' for a, m in zip(df_cost_agrupado['año'], df_cost_agrupado['mes'])]
            y_data = df_cost_agrupado['coste_total_acumulado']
            y_limit = max(total_budget_project[0][0], max(df_cost_agrupado['coste_total_acumulado'])) * 1.2

            # Crear gráfico
            fig, ax = plt.subplots(facecolor='lightgray')
            fig.set_size_inches(400 / 100, 200/ 100)
            fig.tight_layout(pad=.7)
            bars = ax.bar(x_data, y_data, color='skyblue' )
            ax.axhline(y=total_budget_project[0][0], color='red', linestyle='--', label=f'Presupuesto = {total_budget_project[0][0]:.2f} €')
            # Añadir los valores encima de cada barra
            for bar in bars:
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, str(f"{yval:.2f} €"), ha='center', va='bottom', fontsize=5.5)
            ax.set_title('Certificación Mensual Acumulada')
            ax.set_ylim(0, y_limit)
            ax.legend()
            ax.tick_params(axis='x', labelsize=7,rotation=90)
            ax.tick_params(axis='y', labelsize=7)
            canvas1 = FigureCanvasTkAgg(fig, self.data_cost_frame)
            canvas1.draw()
            self.graph_cost=canvas1.get_tk_widget()
            self.graph_cost.grid(row=3, column=2, padx=30, pady=5, sticky="nwes", columnspan=2)
            self.graph_cost.config(width=400, height=400)



        # filtro para elegir fecha de certificado
        self.date_option_cost_label = customtkinter.CTkLabel(self.cost_frame,
                                                             text="SELECCIONAR FECHA CERTIFICACIÓN:",
                                                             anchor="center",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.date_option_cost_label.grid(row=4, column=0, padx=30, pady=10, sticky="nsew")
        cost_data = get_all_bd(access[0], access[1], 'vw_certificaciones', code_project_select)
        cost_date_value = []
        for item in cost_data:
            if item[13]:
                cost_date_value.append(str(item[13].year) + "-" + str(item[13].month))
        cost_date_value=list(set(cost_date_value))
        cost_date_value.sort()
        self.date_option_cost_filter = customtkinter.CTkOptionMenu(self.cost_frame,
                                                                   dynamic_resizing=False,
                                                                   values=cost_date_value)
        self.date_option_cost_filter.grid(row=4, column=1, padx=30, pady=10, sticky="nsew")

        # bontones para exportar certificacion
        self.export_cost_button = customtkinter.CTkButton(self.cost_frame, corner_radius=5, height=40, width=400,
                                                          border_spacing=10, text="Exportar Certificación",
                                                          text_color=("gray10", "gray90"),
                                                          hover_color=("gray70", "gray30"),
                                                          font=("default", 14, "bold"),
                                                          anchor="center",
                                                          command=lambda: self.export_cost_manager(access,self.project_option_cost_filter.get(),self.date_option_cost_filter.get()))
        self.export_cost_button.grid(row=4, column=2, padx=30, pady=10, sticky="e")


    def project_filter_cost_event(self, access):
        self.data_cost_frame.destroy()
        self.data_cost_monthly_frame.destroy()
        self.data_cost_frame = customtkinter.CTkScrollableFrame(self.cost_frame, corner_radius=0)
        self.data_cost_monthly_frame = customtkinter.CTkScrollableFrame(self.cost_frame, corner_radius=0)
        self.update_data_cost_frame_manager(access)


    def export_cost_manager(self,access,project_select, date_select):
        code_project_select = project_select.split(" - ")[0]
        code_project_select = str(code_project_select)
        # Abrir el cuadro de diálogo para seleccionar una carpeta
        folder_path = filedialog.askdirectory(title="Selecciona una carpeta")

        # Comprobar si se ha seleccionado una carpeta
        if folder_path:
            # Unir la ruta de la carpeta con el nombre del archivo
            output_path = os.path.join(folder_path, "certificacion_mensual.xlsx")

        result = export_monthly_certification(access[0], access[1], code_project_select, output_path, date_select)

        if result == "ok":
            mssg = "Se ha exportado a la carpeta seleccionada el informe de la certificación mensual"
            CTkMessagebox(title="Successfull Message!", message=mssg,
                          icon="check")
        else:
            mssg = f"ERROR: '{result}'"
            CTkMessagebox(title="Error", message=mssg, icon="warning")






