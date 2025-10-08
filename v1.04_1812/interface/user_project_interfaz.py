import tkinter.ttk
import tkinter as tk
from PIL import Image
import base64
from io import BytesIO
import ast
from collections import Counter
from interface.confirm_photo_interfaz import AppPhotoUpload
from script.modulo_db import (get_all_bd, get_item_id_bd, get_option_item_bd, get_id_item_bd, get_filter_data_bd,
                              get_id_item_sub_bd,get_option_item_sub_bd,mod_amount_budget_item,add_budget_item,
                              delete_budget_item,mod_amount_cost_item,delete_cost_item,add_cost_item,cert_cost_item,
                              import_budget_items,add_register_elements, delete_register_item,close_register_data,
                              mod_register_data,mod_photo_site_register,get_multifilter_data_bd,delete_register_budget_items)
from interface.combox_interfaz import *
from interface.reg_catalog_hidro_add_interfaz import AppCatalogHidroAdd
from interface.reg_catalog_hidro_mod_interfaz import AppCatalogHidroMod
from interface.reg_catalog_regis_add_interfaz import AppCatalogRegisAdd
from interface.reg_catalog_regis_mod_interfaz import AppCatalogRegisMod
from interface.register_add_interfaz import AppRegisterAdd
from interface.register_element_mod_interfaz import AppElementModEmpty, AppElementModNoEmpty
from interface.amount_interfaz import AppAmountAdd
from interface.update_budget_interfaz import AppBudgetUpdate
from interface.view_photo_interfaz import AppViewPhoto
from interface.operation_interfaz import AppOperation
from CTkMessagebox import CTkMessagebox
import os

# Obtener la ruta actual
current_path = os.path.dirname(os.path.realpath(__file__))

# Subir un nivel en la estructura de carpetas
parent_path = os.path.dirname(current_path)

customtkinter.set_appearance_mode("dark")


class AppUserProject(customtkinter.CTkToplevel):
    width = 1500
    height = 800


    def __init__(self,main_view, select_data):
        super().__init__()
        password = select_data[1]
        user = select_data[0]
        schema = select_data[2]

        self.ventana_principal = main_view
        self.select_register = None

        self.title("HydroFlow Manager")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)


        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # cargar imagenes de iconos
        image_logo_path = parent_path +"/source/logo artanda2.png"
        self.lg_image = customtkinter.CTkImage(Image.open(image_logo_path), size=(200, 44))
        resume_path = parent_path +"/source/resumen.png"  # quitar punto cuando ya no este en pruebas
        self.resume_image = customtkinter.CTkImage(Image.open(resume_path),
                                                      size=(30, 30))
        inventory_path = parent_path +"/source/registro.png" #quitar punto cuando ya no este en pruebas
        self.inventory_image = customtkinter.CTkImage(Image.open(inventory_path),
                                                 size=(30, 30))
        catalog_path = parent_path +"/source/valvula.png"#quitar punto cuando ya no este en pruebas
        self.catalog_image = customtkinter.CTkImage(Image.open(catalog_path),
                                                 size=(30, 30))
        budget_path = parent_path +"/source/presupuesto.png" #quitar punto cuando ya no este en pruebas
        self.budget_image = customtkinter.CTkImage(Image.open(budget_path),
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

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=select_data[2],
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=18, weight="bold"))
        self.navigation_frame_label.grid(row=1, column=0, padx=20, pady=5)

        self.resume_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                        border_spacing=10, text="Resumen proyecto", fg_color="transparent",
                                                        text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray30"), image=self.resume_image,
                                                        font=customtkinter.CTkFont(size=15, weight="bold"),
                                                        anchor="w", command=lambda: self.resume_button_event(select_data))
        self.resume_button.grid(row=2, column=0, sticky="ew")

        self.inventory_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                        border_spacing=10, text="Inventario", fg_color="transparent",
                                                        text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray30"), image=self.inventory_image,
                                                        font=customtkinter.CTkFont(size=15, weight="bold"),
                                                        anchor="w", command=lambda:self.inventory_button_event(select_data))
        self.inventory_button.grid(row=3, column=0, sticky="ew")

        self.catalog_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                        border_spacing=10, text="Catálogo de piezas", fg_color="transparent",
                                                        text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray30"), image=self.catalog_image,
                                                        font=customtkinter.CTkFont(size=15, weight="bold"),
                                                        anchor="w", command=self.catalog_button_event)
        self.catalog_button.grid(row=4, column=0, sticky="ew")

        self.budget_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                        border_spacing=10, text="Presupuesto", fg_color="transparent",
                                                        text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray30"), image=self.budget_image,
                                                        font=customtkinter.CTkFont(size=15, weight="bold"),
                                                        anchor="w", command=lambda:self.budget_button_event(select_data))
        self.budget_button.grid(row=5, column=0, sticky="ew")

        self.cost_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                        border_spacing=10, text="Certificaciones", fg_color="transparent",
                                                        text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray30"), image=self.cost_image,
                                                        font=customtkinter.CTkFont(size=15, weight="bold"),
                                                        anchor="w", command=lambda :self.cost_button_event(select_data))
        self.cost_button.grid(row=6, column=0, sticky="ew")

        # Espaciador vacío para empujar el botón hacia abajo
        self.navigation_frame.grid_rowconfigure(7, weight=1)
        self.view_project_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=5, height=40,
                                                        border_spacing=10, text="Acceder a otro proyecto",
                                                        text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray30"),
                                                        font=("default", 14, "bold"),
                                                        anchor="center", command=lambda:self.view_project_button_event(select_data))
        self.view_project_button.grid(row=8,padx=30, pady=(15, 15),sticky="nsew")


        # ----------------------FRAME RESUMEN -------------------------------------------------------------------
        self.resume_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.resume_frame.grid_columnconfigure(0, weight=1)
        self.resume_frame.grid_columnconfigure(1, weight=2)
        self.resume_frame.grid_columnconfigure(2, weight=1)
        self.resume_frame.grid_rowconfigure(2, weight=2)

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA RESUMEN PROYECTO_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.total_frame = customtkinter.CTkFrame(self.resume_frame, corner_radius=0)
        self.total_frame.grid(row=0, padx=30, pady=(15, 10),sticky="nsew", columnspan=3)
        self.total_frame.grid_columnconfigure(0,weight=1)
        self.total_frame.grid_columnconfigure(1, weight=1)
        self.total_frame.grid_columnconfigure(2, weight=2)

        #resumen de los resgistros del proyecto
        #consigue lso datos de la tabla inventario y los trata
        data_register = get_all_bd(user, password, 'tbl_inventario', schema)
        count_total = len(data_register)
        count_pending = 0
        count_wip = 0
        count_finish = 0
        count_completed = 0
        for i in range(len(data_register)):
            status = data_register[i][6]
            if status == 1:
                count_wip += 1
            elif status == 2:
                count_finish += 1
            elif status == 3:
                count_pending += 1
            elif status == 4:
                count_completed += 1

        # totales
        self.total_resumen_label = customtkinter.CTkLabel(self.total_frame, text="RESUMEN GENERAL",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13, weight="bold"))
        self.total_resumen_label.grid(row=0, column=0, padx=10, pady=5, sticky="nwes", columnspan=3)

        self.total_resumen_label = customtkinter.CTkLabel(self.total_frame, text="Nº total de resgitros",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13, weight="bold"))
        self.total_resumen_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.total_resumen = customtkinter.CTkLabel(self.total_frame, text=count_total,
                                                    font=customtkinter.CTkFont(size=13))
        self.total_resumen.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.completed_resumen_label = customtkinter.CTkLabel(self.total_frame, text="Registros completos:",
                                                              anchor="center",
                                                              font=customtkinter.CTkFont(size=13, weight="bold"))
        self.completed_resumen_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.completed_resumen = customtkinter.CTkLabel(self.total_frame, text=count_completed,
                                                        font=customtkinter.CTkFont(size=13))
        self.completed_resumen.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.wip_resumen_label = customtkinter.CTkLabel(self.total_frame, text="Registros en ejecución:",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=13, weight="bold"))
        self.wip_resumen_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.wip_resumen = customtkinter.CTkLabel(self.total_frame, text=count_wip,
                                                  font=customtkinter.CTkFont(size=13))
        self.wip_resumen.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.pending_resumen_label = customtkinter.CTkLabel(self.total_frame, text="Registros pendientes:",
                                                            anchor="center",
                                                            font=customtkinter.CTkFont(size=13, weight="bold"))
        self.pending_resumen_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.pending_resumen = customtkinter.CTkLabel(self.total_frame, text=count_pending,
                                                      font=customtkinter.CTkFont(size=13))
        self.pending_resumen.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        self.finish_resumen_label = customtkinter.CTkLabel(self.total_frame, text="Registros finalizados:",
                                                           anchor="center",
                                                           font=customtkinter.CTkFont(size=13, weight="bold"))
        self.finish_resumen_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.finish_resumen = customtkinter.CTkLabel(self.total_frame, text=count_finish,
                                                     font=customtkinter.CTkFont(size=13))
        self.finish_resumen.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        # consigue los datos de los totales de las certificaciones y presupuesto del proyecto
        total_cost,total_budget= self.total_budget_cost_project(select_data)
        #totales presupuesto
        self.budget_resumen_label = customtkinter.CTkLabel(self.total_frame, text="PRESUPUESTO TOTAL ESTIMADO",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13, weight="bold"))
        self.budget_resumen_label.grid(row=1, column=2, padx=5, pady=5, sticky="nwes")

        self.budget_resumen = customtkinter.CTkLabel(self.total_frame, text=f"{total_budget:.2f} €",
                                                    anchor="center",
                                                    font=customtkinter.CTkFont(size=13))
        self.budget_resumen.grid(row=2, column=2, padx=5, pady=5, sticky="nwes")

        #totales certificaciones
        self.certification_resumen_label = customtkinter.CTkLabel(self.total_frame, text="CERTIFICACIÓN TOTAL",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13, weight="bold"))
        self.certification_resumen_label.grid(row=3, column=2, padx=5, pady=5, sticky="nwes")

        self.certification_resumen = customtkinter.CTkLabel(self.total_frame, text= f"{total_cost:.2f} €",
                                                    anchor="center",
                                                    font=customtkinter.CTkFont(size=13))
        self.certification_resumen.grid(row=4, column=2, padx=5, pady=5, sticky="nwes")

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA FILTROS_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.filter_resume_frame = customtkinter.CTkFrame(self.resume_frame, corner_radius=0)
        self.filter_resume_frame.grid(row=1, padx=30, pady=(5, 10), sticky="nsew", columnspan=3)
        self.filter_resume_frame.grid_columnconfigure(0, weight=1)
        self.filter_resume_frame.grid_columnconfigure(1, weight=1)
        self.filter_resume_frame.grid_columnconfigure(2, weight=1)

        #añadir filtos
        default_value = 'Todos'  # Cambia esto al valor predeterminado que quieras
        #municipio
        self.locality_filter_label = customtkinter.CTkLabel(self.filter_resume_frame, text="Municipio",
                                                    anchor="center",
                                                    font=customtkinter.CTkFont(size=13, weight="bold"))
        self.locality_filter_label.grid(row=0, column=0, padx=(10, 5), pady=(10,5), sticky="nwes")
        locality_value=get_option_item_bd(user, password, "tbl_municipios", schema, 'NAMEUNIT')
        self.locality_filter_option = customtkinter.CTkOptionMenu(self.filter_resume_frame,
                                                         dynamic_resizing=False,
                                                         values=locality_value)
        self.locality_filter_option.grid(row=1, column=0, padx=(10,5), pady=(0,10), sticky= "ew")
        self.locality_filter_option.set(default_value)
        #estado
        self.state_filter_label = customtkinter.CTkLabel(self.filter_resume_frame, text="Estado",
                                                    anchor="center",
                                                    font=customtkinter.CTkFont(size=13, weight="bold"))
        self.state_filter_label.grid(row=0, column=1, padx=(5, 5), pady=(10,5), sticky="nwes")
        state_value=get_option_item_bd(user, password, "tbl_inv_estado", schema, 'estado')
        self.state_filter_option = customtkinter.CTkOptionMenu(self.filter_resume_frame,
                                                         dynamic_resizing=False,
                                                         values=state_value)
        self.state_filter_option.grid(row=1, column=1, padx=(5,5), pady=(0,10), sticky= "ew")
        self.state_filter_option.set(default_value)
        #certificacion
        self.cost_filter_label = customtkinter.CTkLabel(self.filter_resume_frame, text="Certificación",
                                                    anchor="center",
                                                    font=customtkinter.CTkFont(size=13, weight="bold"))
        self.cost_filter_label.grid(row=0, column=2, padx=(5, 10), pady=(10,5), sticky="nwes")
        cost_value=get_option_item_bd(user, password, "tbl_inv_certificado", schema, 'tipo_certificacion')
        self.cost_filter_option = customtkinter.CTkOptionMenu(self.filter_resume_frame,
                                                         dynamic_resizing=False,
                                                         values=cost_value)
        self.cost_filter_option.grid(row=1, column=2, padx=(5,10), pady=(0,10), sticky= "ew")
        self.cost_filter_option.set(default_value)
        #botón para filtrar
        self.filter_items_resume_button = customtkinter.CTkButton(self.filter_resume_frame, text="Filtrar datos",
                                                             command=lambda:self.filter_data_resume(select_data), width=50)
        self.filter_items_resume_button.grid(row=2, column=1, padx=(5,10), pady=10, sticky= "ew")

        # botón para limpiar filtrar
        self.clean_filter_resume_button = customtkinter.CTkButton(self.filter_resume_frame, text="Limpiar filtro",
                                                             command=lambda:self.clean_filter_resume(select_data), width=50)
        self.clean_filter_resume_button.grid(row=2, column=2, padx=(5,10), pady=10, sticky= "ew")

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA DATOS_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.data_resume_frame = customtkinter.CTkScrollableFrame(self.resume_frame,
                                                           label_text='Registros del proyecto',
                                                           corner_radius=0)
        self.data_resume_frame.grid(row=2, padx=30, pady=(5, 15), sticky="nsew", columnspan=3)
        self.data_resume_frame.grid_columnconfigure(0,weight=1)
        self.data_resume_frame.grid_rowconfigure(0,weight=1)

        # Crear el tabla dentro del Frame
        self.tree_data_resume = tkinter.ttk.Treeview(self.data_resume_frame, selectmode="browse", height=14)
        # Definir las columnas
        self.tree_data_resume['columns'] = (
        "ID", "Código", "Coordenada X", "Coordenada Y", "Municipio", "Descripción", "Estado", "Certificación")
        # Formatear las columnas
        self.tree_data_resume.column("#0", width=0, stretch=customtkinter.NO)
        self.tree_data_resume.column("ID", anchor=customtkinter.CENTER, width=10)
        self.tree_data_resume.column("Código", anchor=customtkinter.CENTER, width=40)
        self.tree_data_resume.column("Coordenada X", anchor=customtkinter.CENTER, width=30)
        self.tree_data_resume.column("Coordenada Y", anchor=customtkinter.CENTER, width=30)
        self.tree_data_resume.column("Municipio", anchor=customtkinter.CENTER, width=80)
        self.tree_data_resume.column("Descripción", anchor=customtkinter.CENTER, width=200)
        self.tree_data_resume.column("Estado", anchor=customtkinter.CENTER, width=30)
        self.tree_data_resume.column("Certificación", anchor=customtkinter.CENTER, width=30)
        # Definir encabezados
        self.tree_data_resume.heading("#0", text="", anchor=customtkinter.CENTER)
        self.tree_data_resume.heading("ID", text="ID", anchor=customtkinter.CENTER)
        self.tree_data_resume.heading("Código", text="Código", anchor=customtkinter.CENTER)
        self.tree_data_resume.heading("Coordenada X", text="Coordenada X", anchor=customtkinter.CENTER)
        self.tree_data_resume.heading("Coordenada Y", text="Coordenada Y", anchor=customtkinter.CENTER)
        self.tree_data_resume.heading("Municipio", text="Municipio", anchor=customtkinter.CENTER)
        self.tree_data_resume.heading("Descripción", text="Descripción", anchor=customtkinter.CENTER)
        self.tree_data_resume.heading("Estado", text="Estado", anchor=customtkinter.CENTER)
        self.tree_data_resume.heading("Certificación", text="Certificación", anchor=customtkinter.CENTER)
        # devuelve todos los item que hay en el catálogo y los inserta en la tabala
        resume_data = get_all_bd(user, password, "tbl_inventario", schema)
        for i, item in enumerate(resume_data):
            sub_data = []
            items = item
            id = items[0]
            code = items[1]
            coord_X = items[3]
            coord_Y = items[4]
            locality = get_item_id_bd(user, password, "tbl_municipios", schema, "NAMEUNIT", items[5])
            state = get_item_id_bd(user, password, "tbl_inv_estado", schema, "estado", items[6])
            description = items[7]
            state_certification = get_item_id_bd(user, password, "tbl_inv_certificado", schema, "tipo_certificacion", items[8])
            sub_data.append(id)
            sub_data.append(code)
            sub_data.append(coord_X)
            sub_data.append(coord_Y)
            sub_data.append(locality)
            sub_data.append(description)
            sub_data.append(state)
            sub_data.append(state_certification)
            self.tree_data_resume.insert("", "end", values=sub_data)
        self.tree_data_resume.grid(row=0, column=0, sticky="nsew")

        #botón para actualizar y añadir elementos a catálogo
        self.add_item_resume_button = customtkinter.CTkButton(self.resume_frame, text="Añadir registro",
                                                                fg_color="#005e08",
                                                                command=lambda:self.add_item_register_event(select_data),
                                                                width=50,
                                                                font=("default", 13, "bold"))
        self.add_item_resume_button.grid(row=3, column=0, padx=10, pady=10, sticky= "ew")

        self.update_item_resume_button = customtkinter.CTkButton(self.resume_frame, text="Modificar registro",
                                                                command=lambda :self.mod_item_register_event(select_data),
                                                                width=50,
                                                                font=("default", 13, "bold"))
        self.update_item_resume_button.grid(row=3, column=2, padx=10, pady=10, sticky= "ew")


        # ----------------------FRAME inventario-------------------------------------------------------------------
        self.inventory_frame = customtkinter.CTkFrame(self, corner_radius=0)

        registers_data = get_all_bd(user, password, 'tbl_inventario', schema)
        if len(registers_data) == 0:
            self.main_inventory(select_data)
        else:
            register_value = []
            for item in registers_data:
                locality_value = get_item_id_bd(user, password, "tbl_municipios", schema, "NAMEUNIT", item[5])
                register_value.append(item[1] + " - " + locality_value)

            self.select_register = register_value[0]
            self.main_inventory(select_data)
        self.main_inventory(select_data)


        # ----------------------FRAME CATÁLOGO-------------------------------------------------------------------
        self.catalog_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.catalog_frame.grid_columnconfigure(0,weight=1)
        self.catalog_frame.grid_rowconfigure(0, weight=1)

        # crear tabview para los distintos apartados
        self.tab_view = customtkinter.CTkTabview(self.catalog_frame)
        self.tab_view.grid(row=0, column=0, padx=30, pady=(15, 30), sticky="nsew", columnspan=4)
        custom_font = ("default", 16, "bold")
        self.tab_view.add("Hidráulica")
        self.tab_view.add("Registros")
        # Aplicar la fuente personalizada a cada pestaña
        self.tab_view.tab("Hidráulica").grid_propagate(False)
        self.tab_view.tab("Registros").grid_propagate(False)
        self.tab_view._segmented_button.configure(font=custom_font)


        #_____________________________añadir elementos por tab - Hidráulica______________________________________
        self.tab_view.tab("Hidráulica").grid_columnconfigure(0, weight=1)
        self.tab_view.tab("Hidráulica").grid_columnconfigure(1, weight=2)
        self.tab_view.tab("Hidráulica").grid_columnconfigure(2, weight=1)

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA FILTROS_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.filter_hidro_frame = customtkinter.CTkFrame(self.tab_view.tab("Hidráulica"), corner_radius=0)
        self.filter_hidro_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 10), sticky="nsew",columnspan=3)
        self.filter_hidro_frame.grid_columnconfigure(0,weight=1)
        self.filter_hidro_frame.grid_columnconfigure(1, weight=1)
        self.filter_hidro_frame.grid_columnconfigure(2, weight=1)

        #construye los filtros para el catálogo hidráulico
        self.update_filter_hidro(select_data)


        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA DATA-CATÁLOGO_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.tab_view.tab("Hidráulica").grid_rowconfigure(1, weight=1)
        self.data_hidro_frame = customtkinter.CTkScrollableFrame(self.tab_view.tab("Hidráulica"), label_text='Catálogo de elementos hidráulicos',
                                                           corner_radius=0)
        self.data_hidro_frame.grid(row=1, column=0, padx=(10, 5), pady=(10, 10), sticky="nsew",columnspan=3)
        self.data_hidro_frame.grid_columnconfigure(0,weight=1)
        self.data_hidro_frame.grid_rowconfigure(0,weight=1)

        # Crear el tabla dentro del Frame
        self.tree_data_hidro = tkinter.ttk.Treeview(self.data_hidro_frame, selectmode="browse",height=19)
        # Definir las columnas
        self.tree_data_hidro['columns'] = ("ID","Familia","Tipo","Marca","Modelo","Referencia","DNi","DNf","PN","Angulo","Bloque CAD","Descripción","Partida")
        # Formatear las columnas
        self.tree_data_hidro.column("#0", width=0,stretch=customtkinter.NO)
        self.tree_data_hidro.column("ID", anchor=customtkinter.CENTER, width=10)
        self.tree_data_hidro.column("Familia", anchor=customtkinter.CENTER, width=70)
        self.tree_data_hidro.column("Tipo", anchor=customtkinter.CENTER, width=90)
        self.tree_data_hidro.column("Marca", anchor=customtkinter.CENTER, width=30)
        self.tree_data_hidro.column("Modelo", anchor=customtkinter.CENTER, width=150)
        self.tree_data_hidro.column("Referencia", anchor=customtkinter.CENTER, width=70)
        self.tree_data_hidro.column("DNi", anchor=customtkinter.CENTER, width=10)
        self.tree_data_hidro.column("DNf", anchor=customtkinter.CENTER, width=10)
        self.tree_data_hidro.column("PN", anchor=customtkinter.CENTER, width=20)
        self.tree_data_hidro.column("Angulo", anchor=customtkinter.CENTER, width=20)
        self.tree_data_hidro.column("Bloque CAD", anchor=customtkinter.CENTER, width=100)
        self.tree_data_hidro.column("Descripción", anchor=customtkinter.CENTER, width=70)
        self.tree_data_hidro.column("Partida", anchor=customtkinter.CENTER, width=60)
        # Definir encabezados
        self.tree_data_hidro.heading("#0", text="", anchor=customtkinter.CENTER)
        self.tree_data_hidro.heading("ID", text="ID", anchor=customtkinter.CENTER)
        self.tree_data_hidro.heading("Familia", text="Familia", anchor=customtkinter.CENTER)
        self.tree_data_hidro.heading("Tipo", text="Tipo", anchor=customtkinter.CENTER)
        self.tree_data_hidro.heading("Marca", text="Marca", anchor=customtkinter.CENTER)
        self.tree_data_hidro.heading("Modelo", text="Modelo", anchor=customtkinter.CENTER)
        self.tree_data_hidro.heading("Referencia", text="Referencia", anchor=customtkinter.CENTER)
        self.tree_data_hidro.heading("DNi", text="DNi", anchor=customtkinter.CENTER)
        self.tree_data_hidro.heading("DNf", text="DNf", anchor=customtkinter.CENTER)
        self.tree_data_hidro.heading("PN", text="PN", anchor=customtkinter.CENTER)
        self.tree_data_hidro.heading("Angulo", text="Ángulo", anchor=customtkinter.CENTER)
        self.tree_data_hidro.heading("Bloque CAD", text="Bloque CAD", anchor=customtkinter.CENTER)
        self.tree_data_hidro.heading("Descripción", text="Descripción", anchor=customtkinter.CENTER)
        self.tree_data_hidro.heading("Partida", text="Partida", anchor=customtkinter.CENTER)
        #devuelve todos los item que hay en el catálogo y los inserta en la tabala
        hidro_data=get_all_bd(user, password, "vw_catalogo_hidraulica", schema)
        for i, item in enumerate(hidro_data):
            sub_data = []
            items = item
            id = items[0]
            family = items[1]
            type = items[2]
            brand = items[3]
            model = items[5]
            reference = items[6]
            dni = items[7]
            dnf = items[8]
            pn = items[9]
            angle = items[10]
            cad_ref = items[16]
            description = items[17]
            cod_partida = items[18]
            sub_data.append(id)
            sub_data.append(family)
            sub_data.append(type)
            sub_data.append(brand)
            sub_data.append(model)
            sub_data.append(reference)
            sub_data.append(dni)
            sub_data.append(dnf)
            sub_data.append(pn)
            sub_data.append(angle)
            sub_data.append(cad_ref)
            sub_data.append(description)
            sub_data.append(cod_partida )
            self.tree_data_hidro.insert("", "end", values=sub_data)
        self.tree_data_hidro.grid(row=0, column=0, sticky="nsew")


        #botón para actualizar y añadir elementos a catálogo
        self.add_item_catalog_button = customtkinter.CTkButton(self.tab_view.tab("Hidráulica"), text="Añadir pieza",
                                                               font=customtkinter.CTkFont(size=13, weight="bold"),
                                                               fg_color="#005e08",
                                                                command=lambda:self.add_item_hidro_event(select_data), width=50)
        self.add_item_catalog_button.grid(row=2, column=0, padx=(5,10), pady=10, sticky= "ew")

        self.update_item_catalog_button = customtkinter.CTkButton(self.tab_view.tab("Hidráulica"), text="Modificar pieza",
                                                                font=customtkinter.CTkFont(size=13, weight="bold"),
                                                                command=lambda:self.mod_item_hidro_event(select_data), width=50)
        self.update_item_catalog_button.grid(row=2, column=2, padx=(5,10), pady=10, sticky= "ew")

        # _____________________________añadir elementos por tab - Registros______________________________________
        self.tab_view.tab("Registros").grid_columnconfigure(0, weight=1)
        self.tab_view.tab("Registros").grid_columnconfigure(1, weight=2)
        self.tab_view.tab("Registros").grid_columnconfigure(2, weight=1)

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA FILTROS_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.filter_register_frame = customtkinter.CTkFrame(self.tab_view.tab("Registros"), corner_radius=0)
        self.filter_register_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 10), sticky="nsew", columnspan=3)
        self.filter_register_frame.grid_columnconfigure(0, weight=1)
        self.filter_register_frame.grid_columnconfigure(1, weight=1)

        self.update_filter_regis(select_data)

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA DATA-REGISTRO_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.tab_view.tab("Registros").grid_rowconfigure(1, weight=1)
        self.data_register_frame = customtkinter.CTkScrollableFrame(self.tab_view.tab("Registros"),
                                                           label_text='Catálogo de elementos de los registros',
                                                           corner_radius=0)
        self.data_register_frame.grid(row=1, column=0, padx=(10, 5), pady=(10, 10), sticky="nsew", columnspan=3)
        self.data_register_frame.grid_columnconfigure(0, weight=1)
        self.data_register_frame.grid_rowconfigure(0, weight=10)


        # Crear el tabla dentro del Frame
        self.tree_data_regis = tkinter.ttk.Treeview(self.data_register_frame, selectmode="browse",height=19)
        # Definir las columnas
        self.tree_data_regis['columns'] = (
            "ID", "Tipo", "Proveedor", "Modelo", "Referencia", "Dimension A", "Dimension B", "Dimension C",  "Descripción", "Partida")
        # Formatear las columnas
        self.tree_data_regis.column("#0", width=0, stretch=customtkinter.NO)
        self.tree_data_regis.column("ID", anchor=customtkinter.CENTER, width=10)
        self.tree_data_regis.column("Tipo", anchor=customtkinter.CENTER, width=40)
        self.tree_data_regis.column("Proveedor", anchor=customtkinter.CENTER, width=30)
        self.tree_data_regis.column("Modelo", anchor=customtkinter.CENTER, width=150)
        self.tree_data_regis.column("Referencia", anchor=customtkinter.CENTER, width=80)
        self.tree_data_regis.column("Dimension A", anchor=customtkinter.CENTER, width=30)
        self.tree_data_regis.column("Dimension B", anchor=customtkinter.CENTER, width=30)
        self.tree_data_regis.column("Dimension C", anchor=customtkinter.CENTER, width=80)
        self.tree_data_regis.column("Descripción", anchor=customtkinter.CENTER, width=150)
        self.tree_data_regis.column("Partida", anchor=customtkinter.CENTER, width=60)
        # Definir encabezados
        self.tree_data_regis.heading("#0", text="", anchor=customtkinter.CENTER)
        self.tree_data_regis.heading("ID", text="ID", anchor=customtkinter.CENTER)
        self.tree_data_regis.heading("Tipo", text="Tipo", anchor=customtkinter.CENTER)
        self.tree_data_regis.heading("Proveedor", text="Marca", anchor=customtkinter.CENTER)
        self.tree_data_regis.heading("Modelo", text="Modelo", anchor=customtkinter.CENTER)
        self.tree_data_regis.heading("Referencia", text="Referencia", anchor=customtkinter.CENTER)
        self.tree_data_regis.heading("Dimension A", text="Dimension A", anchor=customtkinter.CENTER)
        self.tree_data_regis.heading("Dimension B", text="Dimension B", anchor=customtkinter.CENTER)
        self.tree_data_regis.heading("Dimension C", text="Dimension C", anchor=customtkinter.CENTER)
        self.tree_data_regis.heading("Descripción", text="Descripción", anchor=customtkinter.CENTER)
        self.tree_data_regis.heading("Partida", text="Partida", anchor=customtkinter.CENTER)
        # devuelve todos los item que hay en el catálogo y los inserta en la tabla
        register_data = get_all_bd(user, password, "vw_catalogo_registros", schema)
        for i, item in enumerate(register_data):
            sub_data = []
            items = item
            id = items[0]
            type = items[1]
            brand = items[2]
            model = items[3]
            reference = items[4]
            dimA = items[5]
            dimB = items[6]
            dimC = items[7]
            description = items[8]
            cod_partida = items[9]
            sub_data.append(id)
            sub_data.append(type)
            sub_data.append(brand)
            sub_data.append(model)
            sub_data.append(reference)
            sub_data.append(dimA)
            sub_data.append(dimB)
            sub_data.append(dimC)
            sub_data.append(description)
            sub_data.append(cod_partida)
            self.tree_data_regis.insert("", "end", values=sub_data)
        self.tree_data_regis.grid(row=0, column=0, sticky="nsew")

        # botón para actualizar y añadir elementos a catálogo
        self.add_item_register_button = customtkinter.CTkButton(self.tab_view.tab("Registros"), text="Añadir pieza",
                                                               command=lambda: self.add_item_regis_event(select_data),
                                                               fg_color="#005e08",
                                                               font=customtkinter.CTkFont(size=13, weight="bold"),
                                                               width=50)
        self.add_item_register_button.grid(row=2, column=0, padx=(5, 10), pady=10, sticky="ew")

        self.update_item_register_button = customtkinter.CTkButton(self.tab_view.tab("Registros"),
                                                                  text="Modificar pieza",
                                                                  font=customtkinter.CTkFont(size=13, weight="bold"),
                                                                  command=lambda: self.mod_item_regis_event(select_data), width=50)
        self.update_item_register_button.grid(row=2, column=2, padx=(5, 10), pady=10, sticky="ew")


        # -----------------------------------FRAME PRESUPUESTO -------------------------------------------------------------------
        self.budget_frame = customtkinter.CTkFrame(self, corner_radius=0)


        self.main_budget(select_data)


        # ----------------------FRAME CERTIFICACIONES -------------------------------------------------------------------
        self.cost_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.cost_frame.grid_columnconfigure(0, weight=1)
        self.cost_frame.grid_rowconfigure(3, weight=1)
        self.cost_frame.grid_rowconfigure(5, weight=1)

        self.main_cost(select_data)


        # select default frame
        self.select_frame_by_name("resume")



    # """"""""""""""""""""""""""""""""""""""""""""""""""FUNCIONES MENU""""""""""""""""""""""""""""""""""""""""""""""""
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.resume_button.configure(fg_color=("gray75", "gray25") if name == "resume" else "transparent")
        self.inventory_button.configure(fg_color=("gray75", "gray25") if name == "inventory" else "transparent")
        self.catalog_button.configure(fg_color=("gray75", "gray25") if name == "catalog" else "transparent")
        self.budget_button.configure(fg_color=("gray75", "gray25") if name == "budget" else "transparent")
        self.cost_button.configure(fg_color=("gray75", "gray25") if name == "cost" else "transparent")

        # show selected frame
        if name == "resume":
            self.resume_frame.grid(row=0, column=1,padx=30, pady=(15, 15),sticky="nsew")
        else:
            self.resume_frame.grid_forget()
        # show selected frame
        if name == "inventory":
            self.inventory_frame.grid(row=0, column=1,padx=30, pady=(15, 15),sticky="nsew")
        else:
            self.inventory_frame.grid_forget()

        if name == "catalog":
            self.catalog_frame.grid(row=0, column=1,padx=30, pady=(15, 15),sticky="nsew")
        else:
            self.catalog_frame.grid_forget()

        if name == "budget":
            self.budget_frame.grid(row=0, column=1, padx=30, pady=(15, 15), sticky="nsew")
        else:
            self.budget_frame.grid_forget()

        if name == "cost":
            self.cost_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 20),sticky="nsew")
        else:
            self.cost_frame.grid_forget()


    def resume_button_event(self,select_data):
        self.select_frame_by_name("resume")
        # consigue los datos de los totales de las certificaciones y presupuesto del proyecto
        total_cost, total_budget = self.total_budget_cost_project(select_data)

        self.budget_resumen.destroy()
        self.budget_resumen = customtkinter.CTkLabel(self.total_frame, text=f"{total_budget:.2f} €",
                                                     anchor="center",
                                                     font=customtkinter.CTkFont(size=13))
        self.budget_resumen.grid(row=2, column=2, padx=5, pady=5, sticky="nwes")

        self.certification_resumen.destroy()
        self.certification_resumen = customtkinter.CTkLabel(self.total_frame, text=f"{total_cost:.2f} €",
                                                            anchor="center",
                                                            font=customtkinter.CTkFont(size=13))
        self.certification_resumen.grid(row=4, column=2, padx=5, pady=5, sticky="nwes")


    def inventory_button_event(self,select_data):
        self.inventory_frame.destroy()
        self.inventory_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.select_frame_by_name("inventory")
        self.main_inventory(select_data)


    def catalog_button_event(self):
        self.select_frame_by_name("catalog")


    def budget_button_event(self,select_data):
        self.budget_frame.destroy()
        self.budget_frame = customtkinter.CTkFrame(self, corner_radius=0)
        #seleciona el frame del presupuesto como determinado
        self.select_frame_by_name("budget")
        self.main_budget(select_data)


    def cost_button_event(self,select_data):
        self.cost_frame.destroy()
        self.cost_frame = customtkinter.CTkFrame(self, corner_radius=0)
        # selecciona el frame de certificaciones como determinado
        self.select_frame_by_name("cost")
        self.main_cost(select_data)


    def view_project_button_event (self,access):
        self.destroy()
        self.ventana_principal.deiconify()

        pass


    def main_inventory(self,select_data):
        password = select_data[1]
        user = select_data[0]
        schema = select_data[2]

        registers_data = get_all_bd(user, password, 'tbl_inventario', schema)

        if len(registers_data) == 0:
            self.inventory_frame.grid_columnconfigure(0, weight=1)
            self.inventory_frame.grid_rowconfigure(0, weight=1)

            self.no_register_data_label = customtkinter.CTkLabel(self.inventory_frame,
                                                                 text="No hay ningún registro para seleccionar. Por favor, añada algún registro en la Pestaña Resumen",
                                                                 anchor="center",
                                                                 font=customtkinter.CTkFont(size=15, weight="bold"))
            self.no_register_data_label.grid(row=0, padx=30, pady=30, sticky="nwes")
        else:
            self.register_data_label = customtkinter.CTkLabel(self.inventory_frame,
                                                              text="SELECCIONAR REGISTRO:",
                                                              anchor="center",
                                                              font=customtkinter.CTkFont(size=15, weight="bold"))
            self.register_data_label.grid(row=0, column=0, padx=30, pady=5, sticky="nsew", columnspan=2)
            # filtro de registros
            register_value = []
            for item in registers_data:
                locality_value = get_item_id_bd(user, password, "tbl_municipios", schema, "NAMEUNIT", item[5])
                register_value.append(item[1] + " - " + locality_value)
            self.register_filter_option_inventary = customtkinter.CTkOptionMenu(self.inventory_frame,
                                                                                dynamic_resizing=False,
                                                                                values=register_value,
                                                                                command=lambda
                                                                                    event: self.register_filter_event(
                                                                                    select_data))
            self.register_filter_option_inventary.grid(row=1, column=0, padx=30, pady=5, sticky="nsew", columnspan=2)
            self.register_filter_option_inventary.bind("<<ComboboxSelected>>",
                                                       lambda event: self.register_filter_event(select_data))

            self.register_filter_option_inventary.set(self.select_register)
            register_select = self.register_filter_option_inventary.get()
            code_register_select = register_select.split(" - ")[0]
            id_register_select = get_id_item_bd(user, password, "tbl_inventario", schema, "codigo",
                                                str(code_register_select))

            self.site_photo_label = customtkinter.CTkLabel(self.inventory_frame, text="EMPLAZAMIENTO",
                                                           anchor="s",
                                                           font=customtkinter.CTkFont(size=12, weight="bold"),
                                                           width=50)
            self.site_photo_label.grid(row=2, column=1, padx=30, pady=5, sticky="s")

            # botón para añadir foto de emplazamiento
            self.site_photo_button = customtkinter.CTkButton(self.inventory_frame,
                                                             text="Añadir foto de emplazamiento",
                                                             command=lambda: self.add_photo_site_event(
                                                                 select_data, str(id_register_select)),
                                                             width=50)
            self.site_photo_button.grid(row=3, column=1, padx=30, pady=10, sticky="nsew")
            self.update_photo_site(select_data, id_register_select)

            self.inventory_frame.grid_columnconfigure(0, weight=1)
            self.inventory_frame.grid_columnconfigure(1, weight=1)

            # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA DATOS REGISTRO_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
            self.general_data_frame = customtkinter.CTkFrame(self.inventory_frame, corner_radius=0)
            self.general_data_frame.grid(row=2, column=0, padx=30, pady=10, sticky="nsew", rowspan=2)
            self.general_data_frame.grid_columnconfigure(0, weight=1)
            self.general_data_frame.grid_columnconfigure(1, weight=1)
            self.general_data_frame.grid_columnconfigure(2, weight=1)
            self.general_data_frame.grid_columnconfigure(3, weight=1)

            register_select = self.register_filter_option_inventary.get()
            code_register_select = register_select.split(" - ")[0]
            id_register_select = get_id_item_bd(user, password, "tbl_inventario", schema, "codigo",
                                                str(code_register_select))
            register_data_select = get_filter_data_bd(user, password, "tbl_inventario", schema, "id", str(id_register_select))[0]
            self.update_general_data(select_data, register_data_select)

            # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA ELEMENTOS_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
            self.element_data_frame = customtkinter.CTkFrame(self.inventory_frame, corner_radius=0)
            self.element_data_frame.grid(row=4, column=0, padx=30, pady=5, sticky="nsew", columnspan=2)
            self.element_data_frame.grid_columnconfigure(0, weight=1)
            self.element_data_frame.grid_columnconfigure(1, weight=1)
            self.element_data_frame.grid_rowconfigure(0, weight=1)

            # almacena coordenadas
            self.element_label = customtkinter.CTkLabel(self.element_data_frame, text="ELEMENTOS DEL REGISTRO",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=15, weight="bold"))
            self.element_label.grid(row=0, column=0, padx=30, pady=1, sticky="nsew", columnspan=2)

            element_data = get_filter_data_bd(user, password, "tbl_inv_elementos", schema, "id_inventario",
                                              str(id_register_select))
            element_hidro_data = []
            element_regis_data = []
            for element in element_data:
                if element[1] == 1:
                    element_regis_data.append(element)
                else:
                    element_hidro_data.append(element)

            self.update_element_data(select_data, element_hidro_data, element_regis_data)

            # botón para añadir modidicar los elementos del registros
            self.mod_element_button = customtkinter.CTkButton(self.element_data_frame,
                                                              text="Modificar elementos del registro",
                                                              command=lambda: self.mod_element_event(select_data,
                                                                                                     self.register_filter_option_inventary.get()),
                                                              font=customtkinter.CTkFont(size=13, weight="bold"),
                                                              width=50)
            self.mod_element_button.grid(row=2, column=1, padx=30, pady=5, sticky="nsew")

            # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA OTROS FRAME AUXILIARES_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
            self.auxiliary_frame = customtkinter.CTkFrame(self.inventory_frame, corner_radius=0)
            self.auxiliary_frame.grid(row=5, column=0, padx=30, pady=5, sticky="nsew", columnspan=2)
            self.auxiliary_frame.grid_columnconfigure(0, weight=1)
            self.auxiliary_frame.grid_columnconfigure(1, weight=1)

            self.status_frame = customtkinter.CTkFrame(self.auxiliary_frame, corner_radius=0)
            self.status_frame.grid(row=0, column=0, padx=30, pady=5, sticky="nsew")
            self.status_frame.grid_columnconfigure(0, weight=1)
            self.status_frame.grid_columnconfigure(1, weight=1)

            self.update_other_data(select_data, register_data_select)

            self.closed_register_button = customtkinter.CTkButton(self.status_frame,
                                                                  text="Cierre de operaciones", fg_color="#ab6503",
                                                                  command=lambda: self.close_event(select_data,
                                                                                                   self.register_filter_option_inventary.get()),
                                                                  font=customtkinter.CTkFont(size=15, weight="bold"),
                                                                  width=50)
            self.closed_register_button.grid(row=2, column=0, padx=30, pady=10, sticky="nsew", columnspan=2)
            self.inventory_frame.grid_rowconfigure(6, weight=1)

            self.document_frame = customtkinter.CTkFrame(self.auxiliary_frame, corner_radius=0)
            self.document_frame.grid(row=0, column=1, padx=30, pady=5, sticky="nsew")
            self.document_frame.grid_columnconfigure(0, weight=1)

            self.document_label = customtkinter.CTkLabel(self.document_frame, text="DOCUMENTOS REGISTRO",
                                                         anchor="center",
                                                         font=customtkinter.CTkFont(size=13, weight="bold"))
            self.document_label.grid(row=0, padx=30, pady=5, sticky="nsew")

            self.document_button = customtkinter.CTkButton(self.document_frame,
                                                           text="Ver documentos",
                                                           command=lambda: self.document_event(select_data,
                                                                                               self.register_filter_option_inventary.get()),
                                                           font=customtkinter.CTkFont(size=13),
                                                           width=50)
            self.document_button.grid(row=1, padx=30, pady=5, sticky="nsew")

            self.photos_label = customtkinter.CTkLabel(self.document_frame, text="FOTOS REGISTRO",
                                                       anchor="center",
                                                       font=customtkinter.CTkFont(size=13, weight="bold"))
            self.photos_label.grid(row=2, padx=30, pady=5, sticky="nsew")

            self.photos_button = customtkinter.CTkButton(self.document_frame,
                                                         text="Ver Fotos",
                                                         command=lambda: self.photo_event(select_data,
                                                                                          self.register_filter_option_inventary.get()),
                                                         font=customtkinter.CTkFont(size=13),
                                                         width=50)
            self.photos_button.grid(row=3, padx=30, pady=5, sticky="nsew")

            # boton de guardar
            save_path = parent_path +"/source/guardar.png"
            self.save_image = customtkinter.CTkImage(Image.open(save_path))
            self.save_change_button = customtkinter.CTkButton(self.inventory_frame, fg_color="#005e08", height=40,
                                                              text="Guardar cambios", image=self.save_image,
                                                              compound="left",
                                                              command=lambda: self.save_change_event(select_data,
                                                                                                     self.register_filter_option_inventary.get()),
                                                              font=customtkinter.CTkFont(size=15, weight="bold"),
                                                              width=50)
            self.save_change_button.grid(row=6, column=1, padx=30, pady=10, sticky="nsew")


    def main_budget(self, select_data):
        password = select_data[1]
        user = select_data[0]
        schema = select_data[2]

        registers_data = get_all_bd(user, password, 'tbl_inventario', schema)


        if len(registers_data) == 0:
            self.budget_frame.grid_columnconfigure(0, weight=1)
            self.budget_frame.grid_rowconfigure(0, weight=1)

            self.no_register_data_label = customtkinter.CTkLabel(self.budget_frame,
                                                                 text="No hay ningún registro para seleccionar. Por favor, añada algún registro en la Pestaña Resumen",
                                                                 anchor="center",
                                                                 font=customtkinter.CTkFont(size=15, weight="bold"))
            self.no_register_data_label.grid(row=0, padx=30, pady=30, sticky="nwes")
        else:
            self.budget_frame.grid_columnconfigure(0, weight=0)
            self.budget_frame.grid_columnconfigure(1, weight=2)
            self.budget_frame.grid_rowconfigure(2, weight=1)

            self.register_data_label = customtkinter.CTkLabel(self.budget_frame,
                                                              text="SELECCIONAR REGISTRO:",
                                                              anchor="center",
                                                              font=customtkinter.CTkFont(size=15, weight="bold"))
            self.register_data_label.grid(row=0, column=0, padx=30, pady=5, sticky="nsew")
            # filtro de registros
            register_value = []
            for item in registers_data:
                locality_value = get_item_id_bd(user, password, "tbl_municipios", schema, "NAMEUNIT", item[5])
                register_value.append(item[1] + " - " + locality_value)
            self.register_filter_option_budget = customtkinter.CTkOptionMenu(self.budget_frame,
                                                                             dynamic_resizing=False,
                                                                             values=register_value,
                                                                             command=lambda
                                                                                 event: self.register_filter_budget_event(
                                                                                 select_data))
            self.register_filter_option_budget.grid(row=0, column=1, padx=30, pady=5, sticky="nsew", columnspan=2)
            self.register_filter_option_budget.bind("<<ComboboxSelected>>",
                                                    lambda event: self.register_filter_budget_event(select_data))

            self.register_filter_option_budget.set(self.select_register)

            # recoger id de elemento seleccionado para hacer el frame de datos
            register_select = self.register_filter_option_budget.get()
            code_register_select = register_select.split(" - ")[0]
            id_register_select = get_id_item_bd(user, password, "tbl_inventario", schema, "codigo",
                                                str(code_register_select))

            # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_FILTROS_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
            self.filter_budget_frame = customtkinter.CTkFrame(self.budget_frame, corner_radius=0)
            self.filter_budget_frame.grid(row=1, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=3)
            self.filter_budget_frame.grid_columnconfigure(0, weight=1)
            self.filter_budget_frame.grid_columnconfigure(1, weight=1)

            # capítulo
            self.chapter_budget_label = customtkinter.CTkLabel(self.filter_budget_frame, text="Capítulo",
                                                               anchor="center",
                                                               font=customtkinter.CTkFont(size=13, weight="bold"))
            self.chapter_budget_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="nwes")
            chapter_budget_items = get_all_bd(user, password, "tbl_pres_capitulos", schema)
            chapter_values = []
            for item in chapter_budget_items:
                code = item[1]
                name = item[3]
                chapter_values.append(str(code) + " - " + name)
            self.chapter_budget_option = customtkinter.CTkOptionMenu(self.filter_budget_frame,
                                                                     dynamic_resizing=False,
                                                                     values=chapter_values,
                                                                     command=lambda event: self.update_budget_option(
                                                                         select_data))
            self.chapter_budget_option.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky="ew")

            # partida de presupuesto
            self.item_budget_label = customtkinter.CTkLabel(self.filter_budget_frame, text="Partidas",
                                                            anchor="center",
                                                            font=customtkinter.CTkFont(size=13, weight="bold"))
            self.item_budget_label.grid(row=0, column=1, padx=(10, 5), pady=(10, 5), sticky="nwes")

            chapter_select = self.chapter_budget_option.get()
            if chapter_select == "PA000 - PARTIDAS TIPO":
                item_budget_values = get_all_bd(user, password, "tbl_pres_grupo_partidas", schema)
                if len(item_budget_values) == 0:
                    # partida de presupuesto
                    self.item_budget_option = customtkinter.CTkLabel(self.filter_budget_frame,
                                                                     text="No hay grupos de partidas, modifica el presupuesto",
                                                                     anchor="center",
                                                                     font=customtkinter.CTkFont(size=13, weight="bold"))
                    self.item_budget_option.grid(row=1, column=1, padx=(10, 5), pady=(5, 10), sticky="ew")
                else:
                    item_values = []
                    for item in item_budget_values:
                        code = item[1]
                        name = item[4]
                        item_values.append(str(code) + " - " + name)
                    self.item_budget_option = customtkinter.CTkOptionMenu(self.filter_budget_frame,
                                                                          dynamic_resizing=False, values=item_values)
                    self.item_budget_option.grid(row=1, column=1, padx=(10, 5), pady=(5, 10), sticky="ew")

            else:
                code_chapter_select = chapter_select.split(" - ")[0]
                name_chapter_select = chapter_select.split(" - ")[1]
                id_chapter_select = get_id_item_sub_bd(user, password, "tbl_pres_capitulos", schema, "codigo_capitulo",
                                                       code_chapter_select, "capitulo", name_chapter_select)
                item_budget_values = get_filter_data_bd(user, password, "tbl_pres_precios", schema, "id_capitulo",
                                                        str(id_chapter_select))
                item_values = []
                for item in item_budget_values:
                    code = item[1]
                    name = item[4]
                    item_values.append(str(code) + " - " + name)
                self.item_budget_option = customtkinter.CTkOptionMenu(self.filter_budget_frame, dynamic_resizing=False,
                                                                      values=item_values)
                self.item_budget_option.grid(row=1, column=1, padx=(10, 5), pady=(5, 10), sticky="ew")

            self.chapter_budget_option.bind("<<ComboboxSelected>>",
                                            lambda event: self.update_budget_option(select_data))

            # botón para actualizar elementos del presupuesto
            self.update_budget_button = customtkinter.CTkButton(self.filter_budget_frame,
                                                                text="Modificar presupuesto base",
                                                                font=customtkinter.CTkFont(size=13, weight="bold"),
                                                                command=lambda: self.mod_budget_event(select_data),
                                                                width=400)
            self.update_budget_button.grid(row=2, column=0, padx=30, pady=10, sticky="w")

            # botón para añadir elementos del presupuesto
            self.add_item_budget_button = customtkinter.CTkButton(self.filter_budget_frame, text="Añadir partida",
                                                                  fg_color="#005e08",
                                                                  command=lambda: self.add_item_budget_event(
                                                                      select_data),
                                                                  font=customtkinter.CTkFont(size=13, weight="bold"),
                                                                  width=400)
            self.add_item_budget_button.grid(row=2, column=1, padx=30, pady=10, sticky="e")

            # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA PRESUPUESTO_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
            self.data_budget_frame = customtkinter.CTkScrollableFrame(self.budget_frame, corner_radius=0)
            self.data_budget_frame.grid(row=2, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=3)
            self.data_budget_frame.grid_columnconfigure(2, weight=5)

            items_budget = get_filter_data_bd(user, password, "tbl_presupuesto", schema, "id_arqueta",
                                              str(id_register_select))
            if len(items_budget) == 0:
                # Encabezdos
                self.code_budget_label = customtkinter.CTkLabel(self.data_budget_frame, text="Codigo",
                                                                anchor="center",
                                                                font=customtkinter.CTkFont(size=13, weight="bold"))
                self.code_budget_label.grid(row=0, column=0, padx=5, pady=5, sticky="nwes")

                self.ud_budget_label = customtkinter.CTkLabel(self.data_budget_frame, text="Ud",
                                                              anchor="center",
                                                              font=customtkinter.CTkFont(size=13, weight="bold"))
                self.ud_budget_label.grid(row=0, column=1, padx=5, pady=5, sticky="nwes")

                self.resume_budget_label = customtkinter.CTkLabel(self.data_budget_frame, text="Resumen",
                                                                  anchor="center",
                                                                  font=customtkinter.CTkFont(size=13, weight="bold"))
                self.resume_budget_label.grid(row=0, column=2, padx=5, pady=5, sticky="nwes")

                self.amount_budget_label = customtkinter.CTkLabel(self.data_budget_frame, text="Cantidad",
                                                                  anchor="center",
                                                                  font=customtkinter.CTkFont(size=13, weight="bold"))
                self.amount_budget_label.grid(row=0, column=4, padx=5, pady=5, sticky="nwes")

                self.price_budget_label = customtkinter.CTkLabel(self.data_budget_frame, text="Precio",
                                                                 anchor="center",
                                                                 font=customtkinter.CTkFont(size=13, weight="bold"))
                self.price_budget_label.grid(row=0, column=6, padx=5, pady=5, sticky="nwes")

                self.cost_budget_label = customtkinter.CTkLabel(self.data_budget_frame, text="Coste",
                                                                anchor="center",
                                                                font=customtkinter.CTkFont(size=13, weight="bold"))
                self.cost_budget_label.grid(row=0, column=7, padx=5, pady=5, sticky="nwes")
            else:
                self.update_data_budget(select_data, items_budget)

            # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_TOTAL PRESUPUESTO_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
            # botón para importar las partidas de la tabla de presupuesto a certificación en la base de datos
            self.update_total_budget_button = customtkinter.CTkButton(self.budget_frame,
                                                                      text="Exportar presupuesto a certificaciones",
                                                                      command=lambda: self.import_budget_event(
                                                                          select_data),
                                                                      width=30)
            self.update_total_budget_button.grid(row=3, column=0, padx=(30, 5), pady=15, sticky="w")

            # actualizar totales
            self.update_total_budget_event()

            image_update_path = parent_path +"/source/actualizar.png"
            self.update_image = customtkinter.CTkImage(Image.open(image_update_path), size=(20, 20))
            self.update_total_budget_button = customtkinter.CTkButton(self.budget_frame, text="Actualizar total",
                                                                      image=self.update_image,
                                                                      command=lambda: self.update_total_budget_event(),
                                                                      font=customtkinter.CTkFont(size=13,
                                                                                                 weight="bold"),
                                                                      width=30)
            self.update_total_budget_button.grid(row=3, column=2, padx=(10, 5), pady=15, sticky="w")


    def main_cost(self, select_data):
        password = select_data[1]
        user = select_data[0]
        schema = select_data[2]

        registers_data = get_all_bd(user, password, 'tbl_inventario', schema)

        if len(registers_data) == 0:
            self.cost_frame.grid_columnconfigure(0, weight=1)
            self.cost_frame.grid_rowconfigure(0, weight=1)

            self.no_register_data_label = customtkinter.CTkLabel(self.cost_frame,
                                                                 text="No hay ningún registro para seleccionar. Por favor, añada algún registro en la Pestaña Resumen",
                                                                 anchor="center",
                                                                 font=customtkinter.CTkFont(size=15, weight="bold"))
            self.no_register_data_label.grid(row=0, padx=30, pady=30, sticky="nwes")
        else:
            self.cost_frame.grid_columnconfigure(0, weight=0)
            self.cost_frame.grid_columnconfigure(1, weight=2)
            self.register_data_label = customtkinter.CTkLabel(self.cost_frame,
                                                              text="SELECCIONAR REGISTRO:",
                                                              anchor="center",
                                                              font=customtkinter.CTkFont(size=15, weight="bold"))
            self.register_data_label.grid(row=0, column=0, padx=30, pady=5, sticky="nsew")
            # filtro de registros
            register_value_cost = []
            for item in registers_data:
                locality_value = get_item_id_bd(user, password, "tbl_municipios", schema, "NAMEUNIT", item[5])
                register_value_cost.append(item[1] + " - " + locality_value)
            self.register_filter_option_cost = customtkinter.CTkOptionMenu(self.cost_frame,
                                                                           dynamic_resizing=False,
                                                                           values=register_value_cost,
                                                                           command=lambda
                                                                               event: self.register_filter_cost_event(
                                                                               select_data))
            self.register_filter_option_cost.grid(row=0, column=1, padx=30, pady=5, sticky="nsew", columnspan=2)
            self.register_filter_option_cost.bind("<<ComboboxSelected>>",
                                                  lambda event: self.register_filter_cost_event(select_data))
            self.register_filter_option_cost.set(self.select_register)

            register_select = self.register_filter_option_cost.get()
            code_register_select = register_select.split(" - ")[0]
            id_register_select = get_id_item_bd(user, password, "tbl_inventario", schema, "codigo",
                                                str(code_register_select))

            # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA FILTROS_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
            self.filter_cost_frame = customtkinter.CTkFrame(self.cost_frame, corner_radius=0)
            self.filter_cost_frame.grid(row=1, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=2)
            self.filter_cost_frame.grid_columnconfigure(0, weight=1)
            self.filter_cost_frame.grid_columnconfigure(1, weight=1)

            # capítulo
            self.chapter_cost_label = customtkinter.CTkLabel(self.filter_cost_frame, text="Capítulo",
                                                             anchor="center",
                                                             font=customtkinter.CTkFont(size=13, weight="bold"))
            self.chapter_cost_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="nwes")
            chapter_cost_items = get_all_bd(user, password, "tbl_pres_capitulos", schema)
            chapter_values = []
            for item in chapter_cost_items:
                code = item[1]
                name = item[3]
                chapter_values.append(str(code) + " - " + name)
            self.chapter_cost_option = customtkinter.CTkOptionMenu(self.filter_cost_frame,
                                                                   dynamic_resizing=False,
                                                                   values=chapter_values,
                                                                   command=lambda
                                                                       event: self.update_item_cost_option(
                                                                       select_data))
            self.chapter_cost_option.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky="ew")

            # partida de presupuesto
            self.item_cost_label = customtkinter.CTkLabel(self.filter_cost_frame, text="Partidas",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13, weight="bold"))
            self.item_cost_label.grid(row=0, column=1, padx=(10, 5), pady=(10, 5), sticky="nwes")
            chapter_select = self.chapter_cost_option.get()
            item_values = []
            if chapter_select == "PA000 - PARTIDAS TIPO":
                item_cost_values = get_all_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2])
                if len(item_cost_values) == 0:
                    # partida de presupuesto
                    self.item_cost_option = customtkinter.CTkLabel(self.filter_cost_frame,
                                                                   text="No hay grupos de partidas, modifica el presupuesto",
                                                                   anchor="center",
                                                                   font=customtkinter.CTkFont(size=13, weight="bold"))
                    self.item_budget_option.grid(row=1, column=1, padx=(10, 5), pady=(5, 10), sticky="ew")
                else:
                    for item in item_cost_values:
                        code = item[1]
                        name = item[4]
                        item_values.append(str(code) + " - " + name)
                    self.item_cost_option = customtkinter.CTkOptionMenu(self.filter_cost_frame, dynamic_resizing=False,
                                                                        values=item_values)
                    self.item_cost_option.grid(row=1, column=1, padx=(10, 5), pady=(5, 10), sticky="ew")
                    self.item_cost_option.set(item_values[0])
            else:
                code_chapter_select = chapter_select.split(" - ")[0]
                name_chapter_select = chapter_select.split(" - ")[1]
                id_chapter_select = get_id_item_sub_bd(select_data[0], select_data[1], "tbl_pres_capitulos",
                                                       select_data[2], "codigo_capitulo",
                                                       code_chapter_select, "capitulo", name_chapter_select)
                item_cost_values = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_precios",
                                                      select_data[2], "id_capitulo",
                                                      str(id_chapter_select))
                for item in item_cost_values:
                    code = item[1]
                    name = item[4]
                    item_values.append(str(code) + " - " + name)
            self.item_cost_option = customtkinter.CTkOptionMenu(self.filter_cost_frame,
                                                                dynamic_resizing=False,
                                                                values=item_values)
            self.item_cost_option.grid(row=1, column=1, padx=(10, 5), pady=(5, 10), sticky="ew")
            self.chapter_cost_option.bind("<<ComboboxSelected>>",
                                          lambda event: self.update_item_cost_option(select_data))

            # botón para actualizar y añadir elementos del presupuesto
            self.update_cost_button = customtkinter.CTkButton(self.filter_cost_frame,
                                                              text="Modificar presupuesto base",
                                                              font=customtkinter.CTkFont(size=13, weight="bold"),
                                                              command=lambda: self.mod_budget_event(select_data),
                                                              width=400)
            self.update_cost_button.grid(row=2, column=0, padx=30, pady=10, sticky="w")

            self.add_item_cost_button = customtkinter.CTkButton(self.filter_cost_frame, text="Añadir partida",
                                                                fg_color="#005e08",
                                                                command=lambda: self.add_item_cost_event(
                                                                    select_data),
                                                                font=customtkinter.CTkFont(size=13, weight="bold"),
                                                                width=400)
            self.add_item_cost_button.grid(row=2, column=1, padx=30, pady=10, sticky="e")

            # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA CERTIFICACIONES_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
            self.no_cert_label = customtkinter.CTkLabel(self.cost_frame,
                                                        text=f"PARTIDAS NO CERTIFICADAS",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=15, weight="bold"))
            self.no_cert_label.grid(row=2, padx=30, pady=5, sticky="nwes", columnspan=2)

            self.data_cost_frame1 = customtkinter.CTkScrollableFrame(self.cost_frame, corner_radius=0)
            self.data_cost_frame1.grid(row=3, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=2)
            self.data_cost_frame1.grid_columnconfigure(2, weight=5)

            self.cert_label = customtkinter.CTkLabel(self.cost_frame,
                                                     text=f"PARTIDAS CERTIFICADAS",
                                                     anchor="center",
                                                     font=customtkinter.CTkFont(size=15, weight="bold"))
            self.cert_label.grid(row=4, padx=30, pady=5, sticky="nwes", columnspan=2)

            self.data_cost_frame2 = customtkinter.CTkScrollableFrame(self.cost_frame, corner_radius=0)
            self.data_cost_frame2.grid(row=5, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=2)
            self.data_cost_frame2.grid_columnconfigure(2, weight=5)

            items_cost = get_filter_data_bd(user, password, "tbl_pres_certificacion", schema, "id_arqueta",
                                            str(id_register_select))
            items_cert = []
            items_no_cert = []
            for sublist in items_cost:
                if sublist[-2] == 0:
                    items_no_cert.append(sublist)
                else:
                    items_cert.append(sublist)
            self.update_data_cost(select_data, items_no_cert, items_cert)

            # Actualizamos el total de las certificaciones
            self.update_total_cost_event()



    # """"""""""""""""""""""""""""""FUNCIONES PESTAÑA CATÁLOGO """"""""""""""""""""""""""""""""""""""""""""""""""""""""


    def clean_filter_hidro(self,select_data):
        default_value = 'Todos'
        self.family_hidro_option.set(default_value)
        self.type_hidro_option.set(default_value)
        self.brand_hidro_option.set(default_value)
        self.dni_hidro_option.set(default_value)
        self.dnf_hidro_option.set(default_value)
        self.pn_hidro_option.set(default_value)
        self.angle_hidro_option.set(default_value)
        # Limpiar la tabla
        self.tree_data_hidro.delete(*self.tree_data_hidro.get_children())
        #obtener todos los datos
        hidro_data = get_all_bd(select_data[0], select_data[1], "vw_catalogo_hidraulica", select_data[2])
        for i, item in enumerate(hidro_data):
            sub_data = []
            items = item
            id = items[0]
            family = items[1]
            type = items[2]
            brand = items[3]
            model = items[5]
            reference = items[6]
            dni = items[7]
            dnf = items[8]
            pn = items[9]
            angle = items[10]
            cad_ref = items[16]
            description = items[17]
            cod_partida = items[18]
            sub_data.append(id)
            sub_data.append(family)
            sub_data.append(type)
            sub_data.append(brand)
            sub_data.append(model)
            sub_data.append(reference)
            sub_data.append(dni)
            sub_data.append(dnf)
            sub_data.append(pn)
            sub_data.append(angle)
            sub_data.append(cad_ref)
            sub_data.append(description)
            sub_data.append(cod_partida)
            self.tree_data_hidro.insert("", "end", values=sub_data)


    def filter_data_hidro(self, select_data):

        hidro_data = get_all_bd(select_data[0], select_data[1], "vw_catalogo_hidraulica", select_data[2])

        # Normalizar los valores de las opciones, asegurando que siempre sean listas
        family_option_value = self.family_hidro_option.get()
        if isinstance(family_option_value, str):
            family_option_value = [family_option_value]

        type_option_value = self.type_hidro_option.get()
        if isinstance(type_option_value, str):
            type_option_value = [type_option_value]

        brand_option_value = self.brand_hidro_option.get()
        if isinstance(brand_option_value, str):
            brand_option_value = [brand_option_value]

        dni_option_value = self.dni_hidro_option.get()
        if isinstance(dni_option_value, str):
            dni_option_value = [dni_option_value]

        dnf_option_value = self.dnf_hidro_option.get()
        if isinstance(dnf_option_value, str):
            dnf_option_value = [dnf_option_value]

        pn_option_value = self.pn_hidro_option.get()
        if isinstance(pn_option_value, str):
            pn_option_value = [pn_option_value]

        angle_option_value = self.angle_hidro_option.get()
        if isinstance(angle_option_value, str):
            angle_option_value = [angle_option_value]

        if self.family_hidro_option.get() == 'Todos':
            hidro_option1 = hidro_data
        else:
            hidro_option1 = get_filter_data_bd(select_data[0], select_data[1], "vw_catalogo_hidraulica",
                                                 select_data[2], "familia", family_option_value[0] )
        if self.type_hidro_option.get() == 'Todos':
            hidro_option2 = hidro_data
        else:
            hidro_option2 = get_filter_data_bd(select_data[0], select_data[1], "vw_catalogo_hidraulica",
                                                 select_data[2], "tipo_elemento", type_option_value[0])
        if self.brand_hidro_option.get() == 'Todos':
            hidro_option3 = hidro_data
        else:
            hidro_option3 = get_filter_data_bd(select_data[0], select_data[1], "vw_catalogo_hidraulica",
                                                 select_data[2], "marca", brand_option_value[0])
        if self.dni_hidro_option.get() == 'Todos':
            hidro_option4 = hidro_data
        else:
            hidro_option4 = get_filter_data_bd(select_data[0], select_data[1], "vw_catalogo_hidraulica",
                                                 select_data[2], "dni", dni_option_value[0])
        if self.dnf_hidro_option.get() == 'Todos':
            hidro_option5= hidro_data
        else:
            hidro_option5 = get_filter_data_bd(select_data[0], select_data[1], "vw_catalogo_hidraulica",
                                                 select_data[2], "dnf", dnf_option_value[0])
        if self.pn_hidro_option.get() == 'Todos':
            hidro_option6 = hidro_data
        else:
            hidro_option6 = get_filter_data_bd(select_data[0], select_data[1], "vw_catalogo_hidraulica",
                                                 select_data[2], "pn", pn_option_value[0])
        if self.angle_hidro_option.get() == 'Todos':
            hidro_option7 = hidro_data
        else:
            hidro_option7 = get_filter_data_bd(select_data[0], select_data[1], "vw_catalogo_hidraulica",
                                                 select_data[2], "angulo", angle_option_value[0])

        #filtrar datos
        hidro_option1_set = set(hidro_option1)
        hidro_option2_set = set(hidro_option2)
        hidro_option3_set = set(hidro_option3)
        hidro_option4_set = set(hidro_option4)
        hidro_option5_set = set(hidro_option5)
        hidro_option6_set = set(hidro_option6)
        hidro_option7_set = set(hidro_option7)
        hidro_data=hidro_option1_set & hidro_option2_set & hidro_option3_set & hidro_option4_set & hidro_option5_set & hidro_option6_set & hidro_option7_set
        hidro_data = list(hidro_data)
        hidro_data.sort(key=lambda x: x[0])
        # Limpiar la tabla
        self.tree_data_hidro.delete(*self.tree_data_hidro.get_children())  # Limpiar la tabla
        # Volver a crear la tabla
        for i, item in enumerate(hidro_data):
            sub_data = []
            items = item
            id = items[0]
            family = items[1]
            type = items[2]
            brand = items[3]
            model = items[5]
            reference = items[6]
            dni = items[7]
            dnf = items[8]
            pn = items[9]
            angle = items[10]
            cad_ref = items[16]
            description = items[17]
            cod_partida = items[18]
            sub_data.append(id)
            sub_data.append(family)
            sub_data.append(type)
            sub_data.append(brand)
            sub_data.append(model)
            sub_data.append(reference)
            sub_data.append(dni)
            sub_data.append(dnf)
            sub_data.append(pn)
            sub_data.append(angle)
            sub_data.append(cad_ref)
            sub_data.append(description)
            sub_data.append(cod_partida)
            self.tree_data_hidro.insert("", "end", values=sub_data)


    def update_filter_hidro(self,select_data):

        #añadir filtos
        default_value = 'Todos'  # Cambia esto al valor predeterminado que quieras
        # familia
        self.family_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Familia",
                                                       anchor="center",
                                                       font=customtkinter.CTkFont(size=13, weight="bold"))
        self.family_hidro_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="nwes")
        family_value = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_familia", select_data[2], 'familia')
        self.family_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                             dynamic_resizing=False,
                                                             values=family_value,
                                                             command=lambda
                                                                event: self.update_type_options(
                                                                select_data))
        self.family_hidro_option.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky="ew")
        self.family_hidro_option.set(default_value)

        #tipo
        self.type_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Tipo",
                                                    anchor="center",
                                                    font=customtkinter.CTkFont(size=13, weight="bold"))
        self.type_hidro_label.grid(row=0, column=1, padx=(10, 5), pady=(10,5), sticky="nwes")
        select_family = self.family_hidro_option.get()
        if select_family == "Todos":
            type_values = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_tipo", select_data[2],
                                             "tipo_elemento")
        else:
            id_family = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_familia", select_data[2],
                                       "familia", select_family)

            type_values = get_option_item_sub_bd(select_data[0], select_data[1], "tbl_cata_hidra_tipo", select_data[2],
                                                 "tipo_elemento", str(id_family), "id_familia")
        self.type_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                         dynamic_resizing=False,
                                                         values=type_values)
        self.type_hidro_option.grid(row=1, column=1, padx=5, pady=(5,10), sticky= "ew")
        self.family_hidro_option.bind("<<ComboboxSelected>>",
                                                   lambda event: self.update_type_options(select_data))
        self.type_hidro_option.set(default_value)
        # brand
        self.brand_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Marca",
                                                    anchor="center",
                                                    font=customtkinter.CTkFont(size=13, weight="bold"))
        self.brand_hidro_label.grid(row=0, column=2, padx=5, pady=(10,5), sticky="nwes")
        brand_value=get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_marcas", select_data[2], 'marca')
        self.brand_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                         dynamic_resizing=False,
                                                         values=brand_value)
        self.brand_hidro_option.grid(row=1, column=2, padx=5, pady=(5,10), sticky= "ew")
        self.brand_hidro_option.set(default_value)
        # dn inicial
        self.dni_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="DN incial",
                                                    anchor="center",
                                                    font=customtkinter.CTkFont(size=13, weight="bold"))
        self.dni_hidro_label.grid(row=0, column=3, padx=5, pady=(10,5), sticky="nwes")
        dni_value=get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_dni", select_data[2], 'dni')
        self.dni_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                         dynamic_resizing=False,
                                                         values=dni_value)
        self.dni_hidro_option.grid(row=1, column=3, padx=5, pady=(5,10), sticky= "ew")
        self.dni_hidro_option.set(default_value)
        # dn final
        self.dnf_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="DN final",
                                                    anchor="center",
                                                    font=customtkinter.CTkFont(size=13, weight="bold"))
        self.dnf_hidro_label.grid(row=0, column=4, padx=5, pady=(10,5), sticky="nwes")
        dnf_value=get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_dnf", select_data[2], 'dnf')
        self.dnf_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                         dynamic_resizing=False,
                                                         values=dnf_value)
        self.dnf_hidro_option.grid(row=1, column=4, padx=5, pady=(5,10), sticky= "ew")
        self.dnf_hidro_option.set(default_value)
        # pn
        self.pn_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="PN",
                                                    anchor="center",
                                                    font=customtkinter.CTkFont(size=13, weight="bold"))
        self.pn_hidro_label.grid(row=0, column=5, padx=5, pady=(10,5), sticky="nwes")
        pn_value=get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_pn", select_data[2], 'pn')
        self.pn_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                         dynamic_resizing=False,
                                                         values=pn_value)
        self.pn_hidro_option.grid(row=1, column=5, padx=5, pady=(5,10), sticky= "ew")
        self.pn_hidro_option.set(default_value)
        # angulo
        self.angle_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Ángulo",
                                                    anchor="center",
                                                    font=customtkinter.CTkFont(size=13, weight="bold"))
        self.angle_hidro_label.grid(row=0, column=6, padx=(5, 10), pady=(10,5), sticky="nwes")
        angle_value=get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_angulo", select_data[2], 'angulo')
        self.angle_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                         dynamic_resizing=False,
                                                         values=angle_value)
        self.angle_hidro_option.grid(row=1, column=6, padx=(5,10), pady=(5,10), sticky= "ew")
        self.angle_hidro_option.set(default_value)

        #botón para filtrar
        self.filter_items_hidro_button = customtkinter.CTkButton(self.filter_hidro_frame, text="Filtrar datos",
                                                             command=lambda:self.filter_data_hidro(select_data), width=50)
        self.filter_items_hidro_button.grid(row=2, column=5, padx=(5,10), pady=10, sticky= "ew")

        # botón para limpiar filtrar
        self.clean_filter_hidro_button = customtkinter.CTkButton(self.filter_hidro_frame, text="Limpiar filtro",
                                                             command=lambda:self.clean_filter_hidro(select_data), width=50)
        self.clean_filter_hidro_button.grid(row=2, column=6, padx=(5,10), pady=10, sticky= "ew")


    def update_type_options(self, select_data):
        select_family = self.family_hidro_option.get()
        if select_family == "Todos":
            type_values = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_tipo", select_data[2],
                                                 "tipo_elemento")
            self.type_hidro_option.configure(values=type_values)
        else:
            id_family = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_familia",select_data[2],"familia",select_family)

            type_values = get_option_item_sub_bd(select_data[0], select_data[1], "tbl_cata_hidra_tipo",select_data[2],"tipo_elemento",str(id_family),"id_familia")
            self.type_hidro_option.configure(values=(type_values if len(type_values) > 0 else "-"))
            self.type_hidro_option.set(type_values[0] if len(type_values) > 0 else "-")


    def add_item_hidro_event(self,select_data):
        self.withdraw()
        #inicia la interfaz para añadir un elemento del catalogo
        appAux1=AppCatalogHidroAdd(select_data)
        self.wait_window(appAux1)
        self.deiconify()
        #actualiza filtros por si se han añadido alguna caracteristica nueva
        self.filter_hidro_frame.destroy()
        self.filter_hidro_frame = customtkinter.CTkFrame(self.tab_view.tab("Hidráulica"), corner_radius=0)
        self.filter_hidro_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 10), sticky="nsew",columnspan=3)
        self.filter_hidro_frame.grid_columnconfigure(0,weight=1)
        self.filter_hidro_frame.grid_columnconfigure(1, weight=1)
        self.filter_hidro_frame.grid_columnconfigure(2, weight=1)
        self.update_filter_hidro(select_data)
        #actauliza los datos de la tabla
        self.update_data_frame_hidro(select_data)


    def mod_item_hidro_event(self,select_data):
        # selecciona el item a modificar
        item_select = self.tree_data_hidro.selection()
        if item_select:
            item_data = self.tree_data_hidro.item(item_select)
            data_item=item_data['values']
            id_item_select=data_item[0]
            items_hidro=get_filter_data_bd(select_data[0], select_data[1], "tbl_catalogo_hidraulica", select_data[2], 'id', str(id_item_select))[0]
            self.withdraw()
            # inicia la interfaz para modificar el elemento seleccionado
            appAux2 = AppCatalogHidroMod(select_data,items_hidro)
            self.wait_window(appAux2)
            self.deiconify()
            # actualiza filtros por si se han añadido alguna caracteristica nueva
            self.filter_hidro_frame.destroy()
            self.filter_hidro_frame = customtkinter.CTkFrame(self.tab_view.tab("Hidráulica"), corner_radius=0)
            self.filter_hidro_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 10), sticky="nsew", columnspan=3)
            self.filter_hidro_frame.grid_columnconfigure(0, weight=1)
            self.filter_hidro_frame.grid_columnconfigure(1, weight=1)
            self.filter_hidro_frame.grid_columnconfigure(2, weight=1)
            self.update_filter_hidro(select_data)
            # actauliza los datos de la tabla
            self.update_data_frame_hidro(select_data)
        else:
            CTkMessagebox(title="Error Message!", message='Por favor, seleccione un item de la tabla para modificar',
                          icon="warning")


    def update_data_frame_hidro(self,select_data):
        default_value = 'Todos'
        self.family_hidro_option.set(default_value)
        self.type_hidro_option.set(default_value)
        self.brand_hidro_option.set(default_value)
        self.dni_hidro_option.set(default_value)
        self.dnf_hidro_option.set(default_value)
        self.pn_hidro_option.set(default_value)
        self.angle_hidro_option.set(default_value)
        # Limpiar la tabla
        self.tree_data_hidro.delete(*self.tree_data_hidro.get_children())
        # obtener todos los datos
        hidro_data = get_all_bd(select_data[0], select_data[1], "vw_catalogo_hidraulica", select_data[2])
        for i, item in enumerate(hidro_data):
            sub_data = []
            items = item
            id = items[0]
            family = items[1]
            type = items[2]
            brand = items[3]
            model = items[5]
            reference = items[6]
            dni = items[7]
            dnf = items[8]
            pn = items[9]
            angle = items[10]
            cad_ref = items[16]
            description = items[17]
            cod_partida = items[18]
            sub_data.append(id)
            sub_data.append(family)
            sub_data.append(type)
            sub_data.append(brand)
            sub_data.append(model)
            sub_data.append(reference)
            sub_data.append(dni)
            sub_data.append(dnf)
            sub_data.append(pn)
            sub_data.append(angle)
            sub_data.append(cad_ref)
            sub_data.append(description)
            sub_data.append(cod_partida)
            self.tree_data_hidro.insert("", "end", values=sub_data)


    def clean_filter_regis(self,select_data):
        default_value = 'Todos'
        self.type_register_option.set(default_value)
        self.brand_register_option.set(default_value)
        # Limpiar la tabla
        self.tree_data_regis.delete(*self.tree_data_regis.get_children())
        #obtener todos los datos
        register_data = get_all_bd(select_data[0], select_data[1], "vw_catalogo_registros", select_data[2])
        for i, item in enumerate(register_data):
            sub_data = []
            items = item
            id = items[0]
            type = items[1]
            brand = items[2]
            model = items[3]
            reference = items[4]
            dimA = items[5]
            dimB = items[6]
            dimC = items[7]
            description = items[8]
            cod_partida = items[9]
            sub_data.append(id)
            sub_data.append(type)
            sub_data.append(brand)
            sub_data.append(model)
            sub_data.append(reference)
            sub_data.append(dimA)
            sub_data.append(dimB)
            sub_data.append(dimC)
            sub_data.append(description)
            sub_data.append(cod_partida)
            self.tree_data_regis.insert("", "end", values=sub_data)


    def filter_data_regis(self, select_data):

        register_data = get_all_bd(select_data[0], select_data[1], "vw_catalogo_registros", select_data[2])
        # Normalizar los valores de las opciones, asegurando que siempre sean lista
        type_option_value = self.type_register_option.get()
        if isinstance(type_option_value, str):
            type_option_value = [type_option_value]

        brand_option_value = self.brand_register_option.get()
        if isinstance(brand_option_value, str):
            brand_option_value = [brand_option_value]

        if self.type_register_option.get() == 'Todos':
            register_option1 = register_data
        else:
            register_option1 = get_filter_data_bd(select_data[0], select_data[1], "vw_catalogo_registros",
                                                 select_data[2], "tipo", type_option_value[0])
        if self.brand_register_option.get() == 'Todos':
            register_option2 = register_data
        else:
            register_option2 = get_filter_data_bd(select_data[0], select_data[1], "vw_catalogo_registros",
                                                 select_data[2], "proveedor", brand_option_value[0])

        #filtrar datos
        register_option1_set = set(register_option1)
        register_option2_set = set(register_option2)
        register_data = register_option1_set & register_option2_set
        register_data = list(register_data)
        register_data.sort(key=lambda x: x[0])
        # Limpiar la tabla
        self.tree_data_regis.delete(*self.tree_data_regis.get_children())  # Limpiar la tabla
        # Volver a crear la tabla
        for i, item in enumerate(register_data):
            sub_data = []
            items = item
            id = items[0]
            type = items[1]
            brand = items[2]
            model = items[3]
            reference = items[4]
            dimA = items[5]
            dimB = items[6]
            dimC = items[7]
            description = items[8]
            cod_partida = items[9]
            sub_data.append(id)
            sub_data.append(type)
            sub_data.append(brand)
            sub_data.append(model)
            sub_data.append(reference)
            sub_data.append(dimA)
            sub_data.append(dimB)
            sub_data.append(dimC)
            sub_data.append(description)
            sub_data.append(cod_partida)
            self.tree_data_regis.insert("", "end", values=sub_data)


    def update_filter_regis(self,select_data):

        # añadir filtos
        default_value = 'Todos'  # Cambia esto al valor predeterminado que quieras
        # tipo
        self.type_register_label = customtkinter.CTkLabel(self.filter_register_frame, text="Tipo",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13, weight="bold"))
        self.type_register_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="nwes")
        type_value = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_regis_tipo", select_data[2], 'tipo')
        self.type_register_option = customtkinter.CTkOptionMenu(self.filter_register_frame,
                                                                dynamic_resizing=False,
                                                                values=type_value)
        self.type_register_option.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky="ew")
        self.type_register_option.set(default_value)
        # brand
        self.brand_register_label = customtkinter.CTkLabel(self.filter_register_frame, text="Proveedor",
                                                           anchor="center",
                                                           font=customtkinter.CTkFont(size=13, weight="bold"))
        self.brand_register_label.grid(row=0, column=1, padx=(5, 5), pady=(10, 5), sticky="nwes")
        brand_value = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_regis_proveedor", select_data[2], 'proveedor')
        self.brand_register_option = customtkinter.CTkOptionMenu(self.filter_register_frame,
                                                                 dynamic_resizing=False,
                                                                 values=brand_value)
        self.brand_register_option.grid(row=1, column=1, padx=(5, 5), pady=(5, 10), sticky="ew")
        self.brand_register_option.set(default_value)

        # botón para filtrar
        self.filter_items_register_button = customtkinter.CTkButton(self.filter_register_frame, text="Filtrar datos",
                                                                    command=lambda: self.filter_data_regis(select_data),
                                                                    width=50)
        self.filter_items_register_button.grid(row=2, column=0, padx=(5, 10), pady=10, sticky="ew")

        # botón para limpiar filtrar
        self.clean_filter_register_button = customtkinter.CTkButton(self.filter_register_frame, text="Limpiar filtro",
                                                                    command=lambda: self.clean_filter_regis(
                                                                        select_data),
                                                                    width=50)
        self.clean_filter_register_button.grid(row=2, column=1, padx=(5, 10), pady=10, sticky="ew")


    def add_item_regis_event(self, select_data):
        self.withdraw()
        appAux1 = AppCatalogRegisAdd(select_data)
        self.wait_window(appAux1)
        self.deiconify()
        # actualiza filtros por si se han añadido un elemento nuevo
        self.filter_register_frame.destroy()
        self.filter_register_frame = customtkinter.CTkFrame(self.tab_view.tab("Registros"), corner_radius=0)
        self.filter_register_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 10), sticky="nsew", columnspan=3)
        self.filter_register_frame.grid_columnconfigure(0, weight=1)
        self.filter_register_frame.grid_columnconfigure(1, weight=1)
        self.update_filter_regis(select_data)
        #actualiza datos de tabla de registros
        self.update_data_frame_regis(select_data)


    def mod_item_regis_event(self, select_data):
        item_select = self.tree_data_regis.selection()
        if item_select:
            item_data = self.tree_data_regis.item(item_select)
            self.withdraw()
            appAux2 = AppCatalogRegisMod(select_data, item_data['values'])
            self.wait_window(appAux2)
            self.deiconify()
            # actualiza filtros por si se han añadido alguna caracteristica nueva
            self.filter_register_frame.destroy()
            self.filter_register_frame = customtkinter.CTkFrame(self.tab_view.tab("Registros"), corner_radius=0)
            self.filter_register_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 10), sticky="nsew", columnspan=3)
            self.filter_register_frame.grid_columnconfigure(0, weight=1)
            self.filter_register_frame.grid_columnconfigure(1, weight=1)
            self.update_filter_regis(select_data)
            # actualiza datos de tabla de registros
            self.update_data_frame_regis(select_data)
        else:
            CTkMessagebox(title="Error Message!", message='Por favor, seleccione un item de la tabla para modificar',
                          icon="warning")


    def update_data_frame_regis(self, select_data):
        default_value = 'Todos'
        self.type_register_option.set(default_value)
        self.brand_register_option.set(default_value)
        # Limpiar la tabla
        self.tree_data_regis.delete(*self.tree_data_regis.get_children())
        # obtener todos los datos
        register_data = get_all_bd(select_data[0], select_data[1], "vw_catalogo_registros", select_data[2])
        for i, item in enumerate(register_data):
            sub_data = []
            items = item
            id = items[0]
            type = items[1]
            brand = items[2]
            model = items[3]
            reference = items[4]
            dimA = items[5]
            dimB = items[6]
            dimC = items[7]
            description = items[8]
            cod_partida = items[9]
            sub_data.append(id)
            sub_data.append(type)
            sub_data.append(brand)
            sub_data.append(model)
            sub_data.append(reference)
            sub_data.append(dimA)
            sub_data.append(dimB)
            sub_data.append(dimC)
            sub_data.append(description)
            sub_data.append(cod_partida)
            self.tree_data_regis.insert("", "end", values=sub_data)

    # """"""""""""""""""""""""""""""FUNCIONES PESTAÑA RESUMEN  """"""""""""""""""""""""""""""""""""""""""""""""""""""""
    def clean_filter_resume(self,select_data):
        default_value = 'Todos'
        self.locality_filter_option.set(default_value)
        self.state_filter_option.set(default_value)
        self.cost_filter_option.set(default_value)
        # Limpiar la tabla
        self.tree_data_resume.delete(*self.tree_data_resume.get_children())
        #obtener todos los datos
        resume_data = get_all_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2])
        for i, item in enumerate(resume_data):
            sub_data = []
            items = item
            id = items[0]
            code = items[1]
            coord_X = items[3]
            coord_Y = items[4]
            locality = get_item_id_bd(select_data[0], select_data[1], "tbl_municipios", select_data[2], "NAMEUNIT", items[5])
            state = get_item_id_bd(select_data[0], select_data[1], "tbl_inv_estado", select_data[2], "estado", items[6])
            description = items[7]
            state_certification = get_item_id_bd(select_data[0], select_data[1], "tbl_inv_certificado", select_data[2], "tipo_certificacion",
                                                 items[8])
            sub_data.append(id)
            sub_data.append(code)
            sub_data.append(coord_X)
            sub_data.append(coord_Y)
            sub_data.append(locality)
            sub_data.append(description)
            sub_data.append(state)
            sub_data.append(state_certification)
            self.tree_data_resume.insert("", "end", values=sub_data)


    def filter_data_resume(self, select_data):
        resume_data = get_all_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2])
        if self.locality_filter_option.get() == 'Todos':
            resume_option1 = resume_data
        else:
            id_locality_option = get_id_item_bd(select_data[0], select_data[1], "tbl_municipios", select_data[2],
                                            "NAMEUNIT", self.locality_filter_option.get())
            resume_option1 = get_filter_data_bd(select_data[0], select_data[1], "tbl_inventario",
                                                 select_data[2], "id_municipio", str(id_locality_option))
        if self.state_filter_option.get() == 'Todos':
            resume_option2 = resume_data
        else:
            id_state_option = get_id_item_bd(select_data[0], select_data[1], "tbl_inv_estado", select_data[2],
                                            "estado", self.state_filter_option.get())
            resume_option2 = get_filter_data_bd(select_data[0], select_data[1], "tbl_inventario",
                                                 select_data[2], "id_estado", str(id_state_option))
        if self.cost_filter_option.get() == 'Todos':
            resume_option3 = resume_data
        else:
            id_cost_option = get_id_item_bd(select_data[0], select_data[1], "tbl_inv_certificado", select_data[2],
                                          "tipo_certificacion", self.cost_filter_option.get())
            resume_option3 = get_filter_data_bd(select_data[0], select_data[1], "tbl_inventario",
                                                 select_data[2], "id_certificacion", str(id_cost_option))


        #filtrar datos
        resume_option1_set = set(resume_option1)
        resume_option2_set = set(resume_option2)
        resume_option3_set = set(resume_option3)
        resume_data=resume_option1_set & resume_option2_set & resume_option3_set
        resume_data = list(resume_data)
        resume_data.sort(key=lambda x: x[0])
        # Limpiar la tabla
        self.tree_data_resume.delete(*self.tree_data_resume.get_children())  # Limpiar la tabla
        # Volver a crear la tabla
        for i, item in enumerate(resume_data):
            sub_data = []
            items = item
            id = items[0]
            code = items[1]
            coord_X = items[3]
            coord_Y = items[4]
            locality = get_item_id_bd(select_data[0], select_data[1], "tbl_municipios", select_data[2], "NAMEUNIT",
                                      items[5])
            state = get_item_id_bd(select_data[0], select_data[1], "tbl_inv_estado", select_data[2], "estado", items[6])
            description = items[7]
            state_certification = get_item_id_bd(select_data[0], select_data[1], "tbl_inv_certificado", select_data[2],
                                                 "tipo_certificacion",
                                                 items[8])
            sub_data.append(id)
            sub_data.append(code)
            sub_data.append(coord_X)
            sub_data.append(coord_Y)
            sub_data.append(locality)
            sub_data.append(description)
            sub_data.append(state)
            sub_data.append(state_certification)
            self.tree_data_resume.insert("", "end", values=sub_data)


    def add_item_register_event(self,select_data):
        self.withdraw()
        appAux2=AppRegisterAdd(select_data)
        self.wait_window(appAux2)
        self.deiconify()
        self.update_data_frame_resume(select_data)

        self.main_inventory(select_data)
        self.main_budget(select_data)
        self.main_cost(select_data)

        registers_data = get_all_bd(select_data[0], select_data[1], 'tbl_inventario', select_data[2])
        register_value = []
        for item in registers_data:
            locality_value = get_item_id_bd(select_data[0], select_data[1], "tbl_municipios", select_data[2], "NAMEUNIT", item[5])
            register_value.append(item[1] + " - " + locality_value)

        self.register_filter_option_cost.configure(values=register_value)
        self.register_filter_option_budget.configure(values=register_value)
        self.register_filter_option_inventary.configure(values=register_value)


    def mod_item_register_event(self,select_data):
        item_select = self.tree_data_resume.selection()
        if item_select:
            item_data = self.tree_data_resume.item(item_select)
            values = item_data["values"]
            #reinicia el frame de inventario
            self.inventory_frame.destroy()
            self.inventory_frame = customtkinter.CTkFrame(self, corner_radius=0)
            self.select_frame_by_name("inventory")
            self.main_inventory(select_data)

            self.select_register = values[1]+" - "+values[4]
            self.register_filter_option_inventary.set(self.select_register)
            self.register_filter_option_cost.set(self.select_register)
            self.register_filter_option_budget.set(self.select_register)
            register_select = self.register_filter_option_inventary.get()
            code_register_select = register_select.split(" - ")[0]
            id_register_select = get_id_item_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2], "codigo",
                                                str(code_register_select))
            register_data_select = \
            get_filter_data_bd(select_data[0], select_data[1], "tbl_inventario",select_data[2], "id", str(id_register_select))[0]
            self.update_general_data(select_data, register_data_select)

            element_data = get_filter_data_bd(select_data[0], select_data[1], "tbl_inv_elementos", select_data[2], "id_inventario",
                                              str(id_register_select))
            element_hidro_data = []
            element_regis_data = []
            for element in element_data:
                if element[1] == 1:
                    element_regis_data.append(element)
                else:
                    element_hidro_data.append(element)
            self.element_data_frame.forget()
            self.update_element_data(select_data, element_hidro_data, element_regis_data)
            self.status_frame.forget()
            self.update_other_data(select_data, register_data_select)
            self.update_photo_site(select_data, id_register_select)

        else:
            CTkMessagebox(title="Error Message!", message='Por favor, seleccione un item de la tabla para modificar',
                          icon="warning")


    def update_data_frame_resume(self,select_data):
        # actualizamos resumen de los registros del proyecto
        data_register = get_all_bd(select_data[0], select_data[1], 'tbl_inventario', select_data[2])
        count_total = len(data_register)
        count_pending = 0
        count_wip = 0
        count_finish = 0
        count_completed = 0
        for i in range(len(data_register)):
            status = data_register[i][6]
            if status == 1:
                count_wip += 1
            elif status == 2:
                count_finish += 1
            elif status == 3:
                count_pending += 1
            elif status == 4:
                count_completed += 1

        self.total_resumen.configure(text=count_total)
        self.completed_resumen.configure(text=count_completed)
        self.wip_resumen.configure(text=count_wip)
        self.pending_resumen.configure(text=count_pending)
        self.finish_resumen.configure(text=count_finish)

        total_cost, total_budget = self.total_budget_cost_project(select_data)
        self.budget_resumen.configure(text=f"{total_budget:.2f} €")
        self.certification_resumen.configure(text=f"{total_cost:.2f} €")

        default_value = 'Todos'
        self.locality_filter_option.set(default_value)
        self.state_filter_option.set(default_value)
        self.cost_filter_option.set(default_value)
        # Limpiar la tabla
        self.tree_data_resume.delete(*self.tree_data_resume.get_children())
        # obtener todos los datos
        resume_data = get_all_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2])
        for i, item in enumerate(resume_data):
            sub_data = []
            items = item
            id = items[0]
            code = items[1]
            coord_X = items[3]
            coord_Y = items[4]
            locality = get_item_id_bd(select_data[0], select_data[1], "tbl_municipios", select_data[2], "NAMEUNIT",
                                      items[5])
            state = get_item_id_bd(select_data[0], select_data[1], "tbl_inv_estado", select_data[2], "estado", items[6])
            description = items[7]
            state_certification = get_item_id_bd(select_data[0], select_data[1], "tbl_inv_certificado", select_data[2],
                                                 "tipo_certificacion", items[8])
            sub_data.append(id)
            sub_data.append(code)
            sub_data.append(coord_X)
            sub_data.append(coord_Y)
            sub_data.append(locality)
            sub_data.append(description)
            sub_data.append(state)
            sub_data.append(state_certification)
            self.tree_data_resume.insert("", "end", values=sub_data)


    def total_budget_cost_project(self, select_data):
        # calcula el total de las certificaciones del proyecto
        cost_items = []
        items_cost = get_all_bd(select_data[0], select_data[1], "tbl_pres_certificacion", select_data[2])
        for item in items_cost:
            id_item = item[1]
            if item[7] == 0:
                data_item = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_precios", select_data[2], "id",
                                               str(id_item))[0]
                if len(data_item) != 0:
                    cost = item[2] * data_item[6]
                    cost_items.append(cost)
            else:
                data_item = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas",
                                               select_data[2], "id", str(id_item))[0]
                if len(data_item) != 0:
                    cost = item[2] * data_item[6]
                    cost_items.append(cost)
        total_cost = round(sum(cost_items), 2)

        # calcula el total del presupuesto del proyecto
        budget_items = []
        items_budget = get_all_bd(select_data[0], select_data[1], "tbl_presupuesto", select_data[2])
        for item in items_budget:
            id_item = item[1]
            if item[5] == 0:
                data_item = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_precios",
                                               select_data[2], "id", str(id_item))[0]
                if len(data_item) != 0:
                    budget = item[2] * data_item[6]
                    budget_items.append(budget)
            else:
                data_item = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas",
                                               select_data[2], "id", str(id_item))[0]
                if len(data_item) != 0:
                    budget = item[2] * data_item[6]
                    budget_items.append(budget)

        total_budget = round(sum(budget_items), 2)

        return total_cost, total_budget


    # """"""""""""""""""""""""""""""FUNCIONES PESTAÑA INVENTARIO""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def add_photo_site_event(self,select_data,id_register):
        self.withdraw()
        appAux3=AppPhotoUpload(select_data,id_register)
        self.wait_window(appAux3)
        self.img_base64 = appAux3.get_result()
        type_photo = 'emplazamiento'
        id_type_photo = get_id_item_bd(select_data[0], select_data[1], "tbl_inv_foto_tipo", select_data[2],
                                       "tipo_foto", type_photo)
        photo=self.img_base64
        mod_photo_site_register(select_data[0], select_data[1], select_data[2], photo, id_type_photo, id_register)
        self.deiconify()
        self.update_photo(self.img_base64)


    def update_photo(self,image_base64):
        image_site = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_site))
        original_width, original_height = image.size
        # Calcular el nuevo ancho manteniendo la proporción
        aspect_ratio = original_width / original_height
        new_width = int(180* aspect_ratio)
        # Acutalizar imagen en la ventana
        self.site_photo_label = customtkinter.CTkLabel(self.inventory_frame, text="",
                                                       anchor="center", font=customtkinter.CTkFont(size=12, weight="bold"),
                                                       width=8)
        self.site_image = customtkinter.CTkImage(image, size=(new_width, 180))
        self.site_photo_label.configure(image=self.site_image)
        self.site_photo_button.destroy()
        image.close()
        self.site_photo_label.grid(row=2, column=1, padx=(5, 30), pady=5, sticky="nsew")


    def register_filter_event(self,select_data):
        self.select_register = self.register_filter_option_inventary.get()

        register_select = self.register_filter_option_inventary.get()
        code_register_select = register_select.split(" - ")[0]
        id_register_select = get_id_item_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2],  "codigo",
                                            str(code_register_select))
        register_data_select = get_filter_data_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2], "id", str(id_register_select))[0]
        self.update_general_data(select_data, register_data_select)

        element_data = get_filter_data_bd(select_data[0], select_data[1], "tbl_inv_elementos", select_data[2], "id_inventario",
                                          str(id_register_select))
        element_hidro_data = []
        element_regis_data = []
        for element in element_data:
            if element[1] == 1:
                element_regis_data.append(element)
            else:
                element_hidro_data.append(element)
        self.element_data_frame.forget()
        self.update_element_data(select_data, element_hidro_data, element_regis_data)
        self.status_frame.forget()
        self.update_other_data( select_data, register_data_select)
        self.update_photo_site(select_data, id_register_select)


    def update_general_data(self, select_data, register_general_data):
        common_fg_color = "#171717"

        # almacena codigo arqueta
        self.code_label = customtkinter.CTkLabel(self.general_data_frame, text="CÓDIGO:",
                                                 anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                 width=50)
        self.code_label.grid(row=0, column=0, padx=(30, 5), pady=5, sticky="e")
        code_select = register_general_data[1]
        code_value = tk.StringVar(value=code_select)
        self.code_entry = customtkinter.CTkEntry(self.general_data_frame, textvariable=code_value,
                                                 fg_color=common_fg_color, text_color="#FFFFFF", state="disabled")
        self.code_entry.grid(row=0, column=1, padx=(5, 30), pady=5, sticky="ew", columnspan=3)

        # almacena municipio
        self.locality_label = customtkinter.CTkLabel(self.general_data_frame, text="MUNICIPIO:",
                                                     anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                     width=50)
        self.locality_label.grid(row=1, column=0, padx=(30, 5), pady=5, sticky="e")
        locality_value = get_option_item_bd(select_data[0], select_data[1], "tbl_municipios", select_data[2], 'NAMEUNIT')
        locality_value.sort(key=str.lower)
        locality_select = get_item_id_bd(select_data[0], select_data[1], "tbl_municipios", select_data[2], "NAMEUNIT", register_general_data[5])
        self.locality_option = customtkinter.CTkOptionMenu(self.general_data_frame,
                                                           dynamic_resizing=False,
                                                           values=locality_value)
        self.locality_option.grid(row=1, column=1, padx=(5, 30), pady=5, sticky="ew", columnspan=3)
        self.locality_option.set(locality_select)

        # almacena descripción
        self.description_label = customtkinter.CTkLabel(self.general_data_frame, text="DESCRIPCIÓN:",
                                                        anchor="e",
                                                        font=customtkinter.CTkFont(size=15, weight="bold"),
                                                        width=50)
        self.description_label.grid(row=2, column=0, padx=(30, 5), pady=5, sticky="e")
        description_select = register_general_data[7]
        self.description_entry = customtkinter.CTkTextbox(self.general_data_frame, fg_color=common_fg_color,
                                                          border_width=2, border_color="#565B5E",
                                                          text_color="#FFFFFF", height=40)
        self.description_entry.grid(row=2, column=1, padx=(5, 30), pady=5, sticky="ew", columnspan=3)
        self.description_entry.insert("0.0", description_select)

        # almacena coordenadas
        self.coord_X_label = customtkinter.CTkLabel(self.general_data_frame, text="COORDENADA X:",
                                                    anchor="e",
                                                    font=customtkinter.CTkFont(size=15, weight="bold"),
                                                    width=50)
        self.coord_X_label.grid(row=3, column=0, padx=(30, 5), pady=5, sticky="e")
        coord_X_select = register_general_data[3]
        coord_X_value = tk.StringVar(value=coord_X_select)
        self.coord_X_entry = customtkinter.CTkEntry(self.general_data_frame, textvariable=coord_X_value,
                                                    fg_color=common_fg_color, text_color="#FFFFFF", state="disabled")
        self.coord_X_entry.grid(row=3, column=1, padx=(5, 5), pady=5, sticky="ew")
        self.coord_Y_label = customtkinter.CTkLabel(self.general_data_frame, text="COORDENADA Y:",
                                                    anchor="e",
                                                    font=customtkinter.CTkFont(size=15, weight="bold"),
                                                    width=50)
        self.coord_Y_label.grid(row=3, column=2, padx=(5, 5), pady=5, sticky="e")
        coord_Y_select = register_general_data[4]
        coord_Y_value = tk.StringVar(value=coord_Y_select)
        self.coord_X_entry = customtkinter.CTkEntry(self.general_data_frame, textvariable=coord_Y_value,
                                                    fg_color=common_fg_color, text_color="#FFFFFF", state="disabled")
        self.coord_X_entry.grid(row=3, column=3, padx=(5, 30), pady=5, sticky="ew")


    def update_element_data(self, select_data, element_hidro_data, element_regis_data):
        register_select = self.register_filter_option_inventary.get()
        code_register_select = register_select.split(" - ")[0]
        id_register_select = get_id_item_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2], "codigo",
                                            str(code_register_select))
        # listado de elementos hidráulicos añadidos
        self.element_hidro_frame = customtkinter.CTkScrollableFrame(self.element_data_frame, corner_radius=0)
        self.element_hidro_frame.grid(row=1, column=0, padx=1, pady=1, sticky="nsew")
        # Crear la lista (Listbox)
        self.listbox_hidro = tk.Listbox(self.element_hidro_frame, height=20, width=85)
        self.listbox_hidro.grid(row=0, column=0, sticky="news")

        # listado de elementos registro añadidos
        self.element_regis_frame = customtkinter.CTkScrollableFrame(self.element_data_frame, corner_radius=0)
        self.element_regis_frame.grid(row=1, column=1, padx=1, pady=1, sticky="nsew")
        # Crear la lista (Listbox)
        self.listbox_regis = tk.Listbox(self.element_regis_frame, height=20, width=95)
        self.listbox_regis.grid(row=0, column=1, sticky="news")

        if len(element_hidro_data)!=0:
            for item in element_hidro_data:
                n_order = item[9]
                n_line = item[4]
                id_element_catalog = item[8]
                id_type_catalog = item[7]
                model = get_item_id_bd(select_data[0], select_data[1], "tbl_catalogo_hidraulica", select_data[2], "modelo", str(id_element_catalog))
                type = get_item_id_bd(select_data[0], select_data[1], "tbl_cata_hidra_tipo", select_data[2], "tipo_elemento", str(id_type_catalog))
                n_order_connection = item[5]
                if item[10] == 0:
                    status = 'Nueva'
                else:
                    status = 'Existente'
                id_orientation = item[11]
                orientation  = get_item_id_bd(select_data[0], select_data[1], "tbl_inv_orientacion", select_data[2],
                                       "orientacion", str(id_orientation))
                id_material = item[12]
                material  = get_item_id_bd(select_data[0], select_data[1], "tbl_inv_material", select_data[2],
                                       "material", str(id_material))
                element_connection=self.conect_element(select_data,n_order_connection,id_register_select)
                element_list=('P'+str(n_order),'L-'+str(n_line), 'L-'+str(n_line)+'_'+model, element_connection,type, status, orientation, material)
                self.listbox_hidro.insert(customtkinter.END, str(element_list))

        if len(element_regis_data)!=0:
            for item in element_regis_data:
                amount = item[6]
                if amount >1:
                    amount_value=str(amount)+' ud'
                else:
                    amount_value=str(amount)+' uds'
                id_element_catalog = item[8]
                id_type_catalog = item[7]
                model = get_item_id_bd(select_data[0], select_data[1], "tbl_catalogo_registros", select_data[2], "modelo", str(id_element_catalog))
                type = get_item_id_bd(select_data[0], select_data[1], "tbl_cata_regis_tipo", select_data[2], "tipo",
                                      str(id_type_catalog))
                element_list = (model, amount_value, type)
                self.listbox_regis.insert(customtkinter.END, str(element_list))


    def conect_element(self,select_data, n_order_connection,id_register):
        if n_order_connection==0:
            return 'input'
        else:
            element_connection = get_multifilter_data_bd(select_data[0], select_data[1],  "tbl_inv_elementos", select_data[2], "n_orden",
                                          str(n_order_connection),'id_inventario',str(id_register))[0]
            n_order = element_connection[9]
            n_line = element_connection[4]
            id_element_catalog = element_connection[8]
            model = get_item_id_bd(select_data[0], select_data[1], "tbl_catalogo_hidraulica", select_data[2], "modelo",
                                   str(id_element_catalog))
            value_element_connection = 'P'+str(n_order)+' L-'+str(n_line)+'_'+model
            return value_element_connection


    def mod_element_event(self,select_data, register_select):
        #recoge los datos existentes
        code_register_select = register_select.split(" - ")[0]
        id_register_select = get_id_item_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2], "codigo",
                                            str(code_register_select))
        element_data = get_filter_data_bd(select_data[0], select_data[1], "tbl_inv_elementos", select_data[2], "id_inventario",
                                          str(id_register_select))
        #divide los datos entre los hidráulicos y no hidráulicos
        element_hidro_data = []
        element_regis_data = []
        for element in element_data:
            if element[1] == 1:
                element_regis_data.append(element)
            else:
                element_hidro_data.append(element)

        #formatea los datos para añadirlos a los listbox
        elements_list_hidro= []
        if len(element_hidro_data)!=0:
            for item in element_hidro_data:
                n_order = item[9]
                n_line = item[4]
                id_element_catalog = item[8]
                id_type_catalog = item[7]
                model = get_item_id_bd(select_data[0], select_data[1], "tbl_catalogo_hidraulica", select_data[2], "modelo", str(id_element_catalog))
                type = get_item_id_bd(select_data[0], select_data[1], "tbl_cata_hidra_tipo", select_data[2], "tipo_elemento", str(id_type_catalog))
                n_order_connection = item[5]
                if item[10] == 0:
                    status = 'Nueva'
                else:
                    status = 'Existente'
                id_orientation = item[11]
                orientation = get_item_id_bd(select_data[0], select_data[1], "tbl_inv_orientacion", select_data[2],
                                             "orientacion", str(id_orientation))
                id_material = item[12]
                material = get_item_id_bd(select_data[0], select_data[1], "tbl_inv_material", select_data[2],
                                          "material", str(id_material))
                element_connection = self.conect_element(select_data, n_order_connection,id_register_select)
                elements_list_hidro.append(('P'+str(n_order),'L-'+str(n_line), 'L-'+str(n_line)+'_'+model, element_connection,type, status, orientation, material))

        element_list_regis=[]
        if len(element_regis_data)!=0:
            for item in element_regis_data:
                amount = item[6]
                if amount >1:
                    amount_value=str(amount)+' ud'
                else:
                    amount_value=str(amount)+' uds'
                id_element_catalog = item[8]
                id_type_catalog = item[7]
                model = get_item_id_bd(select_data[0], select_data[1], "tbl_catalogo_registros", select_data[2], "modelo", str(id_element_catalog))
                type = get_item_id_bd(select_data[0], select_data[1], "tbl_cata_regis_tipo", select_data[2], "tipo",
                                      str(id_type_catalog))
                element_list_regis.append((model, amount_value, type))

        #comprueba si hay registros existentes o se añaden nuevos
        if len(element_list_regis)==0 and len(elements_list_hidro)==0:
            appAux6 = AppElementModEmpty(select_data)
            self.wait_window(appAux6)
            items_hidro, items_register = appAux6.get_items()
        else:
            appAux6 = AppElementModNoEmpty(select_data,id_register_select,elements_list_hidro,element_list_regis)
            self.wait_window(appAux6)
            items_hidro, items_register = appAux6.get_items()

        id_project = get_id_item_bd(select_data[0], select_data[1], "tbl_proyectos", select_data[2],
                                        "codigo", select_data[2])

        #se vuelven a formatear los datos para añadirlos a la bbdd
        data_element_hidro = []
        rel_budget_hidro = []
        data_element_budget_hidro = []
        data_no_budget_hidro=[]
        if len(items_hidro) != 0:
            list_items = [ast.literal_eval(item) for item in items_hidro]
            for item in list_items:
                sub_data = []
                id_type = 2
                id_project_item = id_project
                id_inventory = id_register_select
                n_line = int(item[1].replace("L-", ""))
                if item[3] == 'input':
                    connection = 0
                else:
                    position = str(item[3])
                    position = position[0:2]
                    connection = next((i + 1 for i, item in enumerate(list_items) if position in item), None)
                n_order = int(item[0].replace("P", ""))
                id_type_element = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_tipo",
                                                 select_data[2],
                                                 "tipo_elemento", item[4])
                model = item[2].replace(item[1] + "_", "")
                id_catalog_element = get_id_item_sub_bd(select_data[0], select_data[1], "tbl_catalogo_hidraulica",
                                                        select_data[2], "id_tipo_hidraulica", str(id_type_element),
                                                        "modelo", model)
                if item[5] == 'Nueva':
                    status_element = 0
                else:
                    status_element = 1
                id_orientation = get_id_item_bd(select_data[0], select_data[1], "tbl_inv_orientacion", select_data[2],
                                                 "orientacion", item[6])
                id_material = get_id_item_bd(select_data[0], select_data[1], "tbl_inv_material", select_data[2],
                                                 "material", item[7])
                sub_data.append(id_type)
                sub_data.append(id_project_item)
                sub_data.append(id_inventory)
                sub_data.append(n_line)
                sub_data.append(connection)
                sub_data.append(id_type_element)
                sub_data.append(id_catalog_element)
                sub_data.append(n_order)
                sub_data.append(status_element)
                sub_data.append(id_orientation)
                sub_data.append(id_material)
                data_element_hidro.append(sub_data)
                cod_budget = get_option_item_sub_bd(select_data[0], select_data[1], "tbl_catalogo_hidraulica",
                                                    select_data[2],
                                                    "cod_partida", id_catalog_element, "id")

                if status_element == 0:
                    if cod_budget[0] == '-':
                        data_no_budget_hidro.append(model)
                    else:
                        rel_budget_hidro.append(id_catalog_element)

            sum_budget_hidro = Counter(rel_budget_hidro)
            for key, value in sum_budget_hidro.items():
                cod_budget = get_option_item_sub_bd(select_data[0], select_data[1], "tbl_catalogo_hidraulica",
                                                    select_data[2], "cod_partida", key, "id")
                id_budget = get_id_item_bd(select_data[0], select_data[1], "tbl_pres_precios", select_data[2], "codigo",
                                           cod_budget[0])
                data_element_budget_hidro.append([id_budget, value, id_project, id_register_select, 0])

        sum_budget_regis = {}
        data_element_register = []
        data_element_budget_regis = []
        data_no_budget_regis = []
        if len(items_register) != 0:
            list_items = [ast.literal_eval(item) for item in items_register]
            for item in list_items:
                sub_data = []
                id_type = 1
                id_project_item = id_project
                id_inventory = id_register_select
                id_type_element = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_regis_tipo",
                                                 select_data[2],
                                                 "tipo", item[2])
                model = item[0]
                id_catalog_element = get_id_item_sub_bd(select_data[0], select_data[1], "tbl_catalogo_registros",
                                                        select_data[2], "id_tipo_registro", str(id_type_element),
                                                        "modelo", model)
                n_element = int(item[1].replace(" ud", "").replace("s", ""))
                sub_data.append(id_type)
                sub_data.append(id_project_item)
                sub_data.append(id_inventory)
                sub_data.append(n_element)
                sub_data.append(id_type_element)
                sub_data.append(id_catalog_element)
                data_element_register.append(sub_data)
                cod_budget = get_option_item_sub_bd(select_data[0], select_data[1], "tbl_catalogo_registros",
                                                    select_data[2], "cod_partida", id_catalog_element, "id")
                if cod_budget[0] == '-':
                    data_no_budget_regis.append(model)
                else:
                    sum_budget_regis[id_catalog_element] = n_element

            for key, value in sum_budget_regis.items():
                cod_budget = get_option_item_sub_bd(select_data[0], select_data[1], "tbl_catalogo_registros",
                                                    select_data[2], "cod_partida", key, "id")
                id_budget = get_id_item_bd(select_data[0], select_data[1], "tbl_pres_precios", select_data[2], "codigo",
                                           cod_budget[0])
                data_element_budget_regis.append([id_budget, value, id_project, id_register_select, 0])

            data_no_budget = data_no_budget_hidro + data_no_budget_regis
            #se eliminan de los existentes y se añaden modificados
            delete_register_budget_items(select_data[0], select_data[1],  select_data[2], id_register_select)
            delete_register_item(select_data[0], select_data[1],  select_data[2], id_register_select)
            result=add_register_elements(select_data[0], select_data[1],  select_data[2], data_element_hidro, data_element_register,data_element_budget_hidro, data_element_budget_regis)

            if len(data_no_budget) != 0:
                mssg = "Los siguientes elementos no tienen asociado una partrida y no se pueden asignar al presupuesto: \n"  + "\n".join(data_no_budget)
                CTkMessagebox(title="Error Message!", message=mssg,
                              icon="cancel")

            if result=="ok":
                element_data = get_filter_data_bd(select_data[0], select_data[1], "tbl_inv_elementos", select_data[2], "id_inventario", str(id_register_select))
                element_hidro_data = []
                element_regis_data = []
                for element in element_data:
                    if element[1] == 1:
                        element_regis_data.append(element)
                    else:
                        element_hidro_data.append(element)
                self.element_hidro_frame.forget()
                self.element_regis_frame.forget()
                self.update_element_data(select_data, element_hidro_data, element_regis_data)
            else:
                CTkMessagebox(title="Warning Message!", message=f"Error: {result}",
                              icon="warning")


    def update_other_data(self, select_data, register_data_select):
        # almacena coordenadas
        self.status_label = customtkinter.CTkLabel(self.status_frame, text="ESTADO DEL REGISTRO:",
                                                    anchor="center",
                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
        self.status_label.grid(row=0, column=0, padx=(30,5), pady=10, sticky="e")

        status_value=get_option_item_bd(select_data[0], select_data[1],  "tbl_inv_estado", select_data[2], "estado")
        id_status=register_data_select[6]
        status_default=get_item_id_bd(select_data[0], select_data[1],  "tbl_inv_estado", select_data[2], "estado",str(id_status))
        self.status_option = customtkinter.CTkOptionMenu(self.status_frame,dynamic_resizing=False,
                                                                            values=status_value)
        self.status_option.grid(row=0, column=1, padx=(5,30), pady=10, sticky="nsew")
        self.status_option.set(status_default)

        # almacena coordenadas
        self.cert_label = customtkinter.CTkLabel(self.status_frame, text="CERTIFICACIÓN:",
                                                    anchor="center",
                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
        self.cert_label.grid(row=1, column=0, padx=(30,5), pady=10, sticky="e")

        cert_value=get_option_item_bd(select_data[0], select_data[1],  "tbl_inv_certificado", select_data[2], "tipo_certificacion")
        id_cert=register_data_select[8]
        cert_default = get_item_id_bd(select_data[0], select_data[1], "tbl_inv_certificado", select_data[2], "tipo_certificacion", str(id_cert))
        self.cert_option = customtkinter.CTkOptionMenu(self.status_frame,dynamic_resizing=False,
                                                                            values=cert_value)
        self.cert_option.grid(row=1, column=1, padx=(5,30), pady=10, sticky="nsew")
        self.cert_option.set(cert_default)


    def photo_event(self,select_data, register_select):
        code_register_select = register_select.split(" - ")[0]
        id_register_select = get_id_item_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2], "codigo",
                                            str(code_register_select))
        appAux7 = AppViewPhoto(select_data, id_register_select)
        self.wait_window(appAux7)


    def document_event(self,select_data, register_select):
        """        code_register_select = register_select.split(" - ")[0]
            id_register_select = get_id_item_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2], "codigo",
                                                str(code_register_select))
            appAux8 = AppViewPhoto(select_data, id_register_select)
            self.wait_window(appAux8)"""
        pass


    def save_change_event(self,select_data, register_select):
        code_register_select = register_select.split(" - ")[0]
        id_register_select = get_id_item_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2], "codigo",
                                            str(code_register_select))
        status = self.status_option.get()
        id_status = get_id_item_bd(select_data[0], select_data[1], "tbl_inv_estado", select_data[2], "estado",
                                   status)
        status_cert = self.cert_option.get()
        id_status_cert = get_id_item_bd(select_data[0], select_data[1], "tbl_inv_certificado", select_data[2],
                                        "tipo_certificacion",
                                        status_cert)
        code = self.code_entry.get()
        locality = self.locality_option.get()
        id_locality = get_id_item_bd(select_data[0], select_data[1], "tbl_municipios", select_data[2], "NAMEUNIT",
                                     locality)
        description = self.description_entry.get("0.0", tk.END)

        data = (code, id_locality, id_status, description, id_status_cert)

        if status=="Cerrada" and status_cert=="Completa":
            self.close_event(select_data, register_select)

        else:
            result = close_register_data(select_data[0], select_data[1], select_data[2], data, id_register_select)
            if result == "ok":
                CTkMessagebox(title="Successfull Message!",
                              message="Se ha modificado el registro de la base de datos",
                              icon="check")

            else:
                CTkMessagebox(title="Warning Message!", message=f"Error: {result}",
                              icon="warning")

        #actualizar tabla de resumen
        self.update_data_frame_resume(select_data)



    def close_event(self,select_data, register_select):
        code_register_select = register_select.split(" - ")[0]
        id_register_select = get_id_item_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2], "codigo",
                                            str(code_register_select))
        self.status_option.set("Cerrada")
        status=self.status_option.get()
        id_status=get_id_item_bd(select_data[0], select_data[1], "tbl_inv_estado", select_data[2], "estado",
                                 status)
        self.cert_option.set("Completa")
        status_cert=self.cert_option.get()
        id_status_cert=get_id_item_bd(select_data[0], select_data[1], "tbl_inv_certificado", select_data[2], "tipo_certificacion",
                       status_cert)
        code=self.code_entry.get()
        locality=self.locality_option.get()
        id_locality = get_id_item_bd(select_data[0], select_data[1], "tbl_municipios", select_data[2], "NAMEUNIT",
                                   locality)
        description= self.description_entry.get("0.0",tk.END)

        data=(code,id_locality,id_status,description,id_status_cert)

        if status=="Cerrada" and status_cert=="Completa":
            appAux8 = AppOperation("¿Desea cerrar las operaciones del registro?")
            self.wait_window(appAux8)
            result = appAux8.get_result()
            if result=="Yes":
                result_1=close_register_data(select_data[0], select_data[1], select_data[2],  data, id_register_select)
                if result_1 == "ok":
                    CTkMessagebox(title="Successfull Message!",
                                  message="Se ha cerrado el registro y se han certificado todas las partidas de la base de datos",
                                  icon="check")
                else:
                    CTkMessagebox(title="Warning Message!", message=f"Error: {result}",
                                  icon="warning")
            else:
                status = self.status_option.set("Finalizada")
                id_status = get_id_item_bd(select_data[0], select_data[1], "tbl_inv_estado", select_data[2], "estado",
                                           status)
                data = (code, id_locality, id_status, description, id_status_cert)
                result_1=mod_register_data(select_data[0], select_data[1], select_data[2],  data, id_register_select)
                if result_1 == "ok":

                    CTkMessagebox(title="Warning Message!", message=f"No se ha dado por cerrado el registro, se ha finalizado las operaciones",
                              icon="warning")
                else:
                    CTkMessagebox(title="Warning Message!", message=f"Error: {result}",
                                  icon="warning")

        items_cost = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_certificacion", select_data[2],
                                        "id_arqueta", str(id_register_select))
        items_cert = []
        items_no_cert = []
        for sublist in items_cost:
            if sublist[-2] == 0:
                items_no_cert.append(sublist)
            else:
                items_cert.append(sublist)
        self.update_data_cost(select_data, items_no_cert, items_cert)
        self.update_data_frame_resume(select_data)


    def update_photo_site (self,select_data, id_register_select):
        # almacena foto emplazamiento
        exist_site_photo = get_option_item_sub_bd(select_data[0], select_data[1], "tbl_inv_fotografias", select_data[2], "id_tipo_foto",
                                                  str(id_register_select), "id_inventario")
        self.site_photo_label.destroy()
        self.site_photo_button.destroy()

        if len(exist_site_photo) == 0:
            self.site_photo_label = customtkinter.CTkLabel(self.inventory_frame, text="EMPLAZAMIENTO",
                                                           anchor="s",
                                                           font=customtkinter.CTkFont(size=12, weight="bold"),
                                                           width=50)
            self.site_photo_label.grid(row=2, column=1, padx=30, pady=5, sticky="s")

            # botón para añadir foto de emplazamiento
            self.site_photo_button = customtkinter.CTkButton(self.inventory_frame,
                                                             text="Añadir foto de emplazamiento",
                                                             command=lambda: self.add_photo_site_event(
                                                                 select_data, str(id_register_select)),
                                                             width=50)
            self.site_photo_button.grid(row=3, column=1, padx=30, pady=10, sticky="nsew")
        else:

            if 1 in exist_site_photo:
                id_site_photo = get_id_item_sub_bd(select_data[0], select_data[1], "tbl_inv_fotografias", select_data[2], "id_inventario",
                                                   str(id_register_select), "id_tipo_foto", str(1))
                image_base64 = get_item_id_bd(select_data[0], select_data[1], "tbl_inv_fotografias", select_data[2],"base64",
                                              str(id_site_photo))
                self.update_photo(image_base64)
            else:
                self.site_photo_label = customtkinter.CTkLabel(self.inventory_frame, text="EMPLAZAMIENTO",
                                                               anchor="s",
                                                               font=customtkinter.CTkFont(size=12,
                                                                                          weight="bold"),
                                                               width=50)
                self.site_photo_label.grid(row=2, column=1, padx=30, pady=5, sticky="s")

                # botón para añadir foto de emplazamiento
                self.site_photo_button = customtkinter.CTkButton(self.inventory_frame,
                                                                 text="Añadir foto de emplazamiento",
                                                                 command=lambda: self.add_photo_site_event(
                                                                     select_data, str(id_register_select)),
                                                                 width=50)
                self.site_photo_button.grid(row=3, column=1, padx=30, pady=10, sticky="nsew")


    #""""""""""""""""""""""""""""""FUNCIONES PESTAÑA PRESUPUESTO"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def update_budget_option (self, select_data):
        chapter_select = self.chapter_budget_option.get()
        if chapter_select == "PA000 - PARTIDAS TIPO":
            item_budget_values = get_all_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2])
            if len(item_budget_values) == 0:
                # partida de presupuesto
                self.item_budget_option.destroy()
                self.item_budget_option = customtkinter.CTkLabel(self.filter_budget_frame,
                                                                 text="No hay grupos de partidas, modifica el presupuesto",
                                                                 anchor="center",
                                                                 font=customtkinter.CTkFont(size=13, weight="bold"))
                self.item_budget_option.grid(row=1, column=1, padx=(10, 5), pady=(5, 10), sticky="ew")
            else:
                item_values = []
                for item in item_budget_values:
                    code = item[1]
                    name = item[4]
                    item_values.append(str(code) + " - " + name)
                self.item_budget_option.destroy()
                self.item_budget_option = customtkinter.CTkOptionMenu(self.filter_budget_frame, dynamic_resizing=False,
                                                                      values=item_values)
                self.item_budget_option.grid(row=1, column=1, padx=(10, 5), pady=(5, 10), sticky="ew")
                self.item_budget_option.set(item_values[0])
        else:
            code_chapter_select = chapter_select.split(" - ")[0]
            name_chapter_select = chapter_select.split(" - ")[1]
            id_chapter_select = get_id_item_sub_bd(select_data[0], select_data[1], "tbl_pres_capitulos", select_data[2], "codigo_capitulo",
                                                   code_chapter_select, "capitulo", name_chapter_select)
            item_budget_values = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_precios", select_data[2],"id_capitulo",
                                                    str(id_chapter_select))
            item_values = []
            for item in item_budget_values:
                code = item[1]
                name = item[4]
                item_values.append(str(code) + " - " + name)
            self.item_budget_option.configure(values=item_values)
            self.item_budget_option.set(item_values[0])


    def update_data_budget (self, select_data, item_budget):
        # cargar imagen de icono
        image_info_path = parent_path +"/source/info.png"
        self.info_image = customtkinter.CTkImage(Image.open(image_info_path), size=(20,20))
        image_update_path = parent_path +"/source/actualizar.png"
        self.update_image = customtkinter.CTkImage(Image.open(image_update_path), size=(20,20))
        image_delete_path = parent_path +"/source/papelera.png"
        self.delete_image = customtkinter.CTkImage(Image.open(image_delete_path), size=(20,20))

        # Listas para almacenar las variables por fila
        self.id_bd_items_budget = []
        self.amount_items_budget = []
        self.price_items_budget = []
        self.cost_items_budget = []
        self.describe_items_budget = []

        #Encabezdos
        self.code_budget_label = customtkinter.CTkLabel(self.data_budget_frame, text="Codigo",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=13, weight="bold"))
        self.code_budget_label.grid(row=0, column=0, padx=5, pady=5, sticky="nwes")

        self.ud_budget_label = customtkinter.CTkLabel(self.data_budget_frame, text="Ud",
                                                      anchor="center",
                                                      font=customtkinter.CTkFont(size=13, weight="bold"))
        self.ud_budget_label.grid(row=0, column=1, padx=5, pady=5, sticky="nwes")

        self.resume_budget_label = customtkinter.CTkLabel(self.data_budget_frame, text="Resumen",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13, weight="bold"))
        self.resume_budget_label.grid(row=0, column=2, padx=5, pady=5, sticky="nwes")

        self.amount_budget_label = customtkinter.CTkLabel(self.data_budget_frame, text="Cantidad",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13, weight="bold"))
        self.amount_budget_label.grid(row=0, column=4, padx=5, pady=5, sticky="nwes")

        self.price_budget_label = customtkinter.CTkLabel(self.data_budget_frame, text="Precio",
                                                         anchor="center",
                                                         font=customtkinter.CTkFont(size=13, weight="bold"))
        self.price_budget_label.grid(row=0, column=6, padx=5, pady=5, sticky="nwes")

        self.cost_budget_label = customtkinter.CTkLabel(self.data_budget_frame, text="Coste",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=13, weight="bold"))
        self.cost_budget_label.grid(row=0, column=7, padx=5, pady=5, sticky="nwes")

        #contenido de la tabla
        i=0
        for i,item in enumerate(item_budget):
            i+=1
            id_bd = item[0]
            self.id_bd_items_budget.append(id_bd)

            id_item = item[1]
            if item[5]==0:
                data_item = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_precios", select_data[2], "id", str(id_item))[0]
            else:
                data_item = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2], "id", str(id_item))[0]


            self.code_item_budget= customtkinter.CTkLabel(self.data_budget_frame, text=data_item[1],
                                                            anchor="center")
            self.code_item_budget.grid(row=i, column=0, padx=5, pady=5, sticky="nwes")

            ud_value=get_item_id_bd(select_data[0], select_data[1], "tbl_pres_unidades", select_data[2],"unidad",str(data_item[3]))
            self.ud_item_budget= customtkinter.CTkLabel(self.data_budget_frame, text=ud_value,
                                                            anchor="center")
            self.ud_item_budget.grid(row=i, column=1, padx=5, pady=5, sticky="nwes")

            self.resume_item_budget= customtkinter.CTkLabel(self.data_budget_frame, text=data_item[4],
                                                            anchor="center")
            self.resume_item_budget.grid(row=i, column=2, padx=5, pady=5, sticky="nwes")

            self.describe_items_budget.append(data_item[5])
            self.description_button_budget= customtkinter.CTkButton(self.data_budget_frame, image=self.info_image, text="",
                                                                    command=lambda i=i:  self.info_event(self.describe_items_budget,i),width=30)
            self.description_button_budget.grid(row=i, column=3, padx=5, pady=5, sticky="nwes")

            amount_value_budget = tk.StringVar(value=f"{str(item[2])}")
            self.amount_items_budget.append(amount_value_budget)
            self.amount_entry_budget = customtkinter.CTkEntry(self.data_budget_frame, textvariable=amount_value_budget, text_color="#FFFFFF")
            self.amount_entry_budget.grid(row=i, column=4, padx=5, pady=5, sticky="nwes")

            self.update_button_budget= customtkinter.CTkButton(self.data_budget_frame, image=self.update_image, text="",
                                                                    command=lambda i=i: self.update_budget(i,select_data),width=30)
            self.update_button_budget.grid(row=i, column=5, padx=5, pady=5, sticky="nwes")

            price_value_budget = round(float(data_item[6]), 2)
            self.price_items_budget.append(price_value_budget)
            self.price_item_budget = customtkinter.CTkLabel(self.data_budget_frame, text=f"{price_value_budget} €", anchor="center")
            self.price_item_budget.grid(row=i, column=6, padx=5, pady=5, sticky="nwes")

            cost_value=round(price_value_budget * float(amount_value_budget.get() or 0), 2)
            cost_value_budget= tk.StringVar(value=f"{cost_value} €")
            self.cost_items_budget.append(cost_value_budget.get())
            self.cost_item_budget = customtkinter.CTkLabel(self.data_budget_frame, textvariable=cost_value_budget, anchor="center")
            self.cost_item_budget.grid(row=i, column=7, padx=5, pady=5, sticky="nwes")

            self.delete_button_budget= customtkinter.CTkButton(self.data_budget_frame, image=self.delete_image, text="",
                                                                    command=lambda i=i: self.delete_budget_event(i,select_data),width=30)
            self.delete_button_budget.grid(row=i, column=8, padx=5, pady=5, sticky="nwes")


    def update_budget(self, i,select_data):
        value = self.amount_items_budget[i - 1].get()
        if  isinstance(value,str):
            amount_budget=value.replace(",",".")
            amount_budget = float(amount_budget) if amount_budget else 0
        else:
            amount_budget = float(self.amount_items_budget[i - 1].get()) if self.amount_items_budget[i - 1].get() else 0
        id_bd = self.id_bd_items_budget[i - 1]
        # Obtener el valor actual del amount_entry y el precio por ítem en la fila 'i'
        mod_amount_budget_item(select_data[0], select_data[1], select_data[2], amount_budget, str(id_bd))

        # reiniciamos el frame
        self.data_budget_frame.destroy()
        self.data_budget_frame = customtkinter.CTkScrollableFrame(self.budget_frame, corner_radius=0)
        self.data_budget_frame.grid(row=2, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=3)
        self.data_budget_frame.grid_columnconfigure(2, weight=5)

        #actaulizamos los valores
        register_select = self.register_filter_option_budget.get()
        code_register_select = register_select.split(" - ")[0]
        id_register_select = get_id_item_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2],
                                            "codigo",
                                            str(code_register_select))
        items_budget = get_filter_data_bd(select_data[0], select_data[1], "tbl_presupuesto", select_data[2],
                                          "id_arqueta", str(id_register_select))
        self.update_data_budget(select_data, items_budget)

        # Actualizamos el total del presupuesto
        self.total_budget_label.destroy()
        self.update_total_budget_event()


    def delete_budget_event(self, i, select_data):
        id_bd = self.id_bd_items_budget[i - 1]
        # borrar el item de la base de datos
        result=delete_budget_item(select_data[0], select_data[1], select_data[2], str(id_bd))
        #reiniciamos el frame
        self.data_budget_frame.destroy()
        self.data_budget_frame = customtkinter.CTkScrollableFrame(self.budget_frame, corner_radius=0)
        self.data_budget_frame.grid(row=2, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=3)
        self.data_budget_frame.grid_columnconfigure(2, weight=5)

        register_select = self.register_filter_option_budget.get()
        code_register_select = register_select.split(" - ")[0]
        id_register_select = get_id_item_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2], "codigo",
                                            str(code_register_select))
        items_budget = get_filter_data_bd(select_data[0], select_data[1], "tbl_presupuesto", select_data[2],
                                          "id_arqueta",str(id_register_select))
        self.update_data_budget(select_data,items_budget)
        if result =="ok":
            CTkMessagebox(title="Successfull Message!",
                          message="Se ha eliminado el item de la base de datos",
                          icon="check")

        else:
            CTkMessagebox(title="Warning Message!", message=f"Error: {result}",
                          icon="warning")

        #Actualizamos el total del presupuesto
        self.total_budget_label.destroy()
        self.update_total_budget_event()


    def info_event(self, list_info,i):
        info = list_info[i-1]
        if info=="":
            info="no descripción"
        CTkMessagebox(title="Descripción partida",width=500, message=info, icon="info")


    def add_item_budget_event(self,select_data):
        #recogemos los datos para añadirlos en la función de añadir el item
        data = []

        register_select = self.register_filter_option_budget.get()
        code_register_select = register_select.split(" - ")[0]
        id_register_select = get_id_item_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2], "codigo",
                                            str(code_register_select))

        id_project=get_id_item_bd(select_data[0], select_data[1], "tbl_proyectos", select_data[2],
                                        "codigo", select_data[2])

        item_budget_select = self.item_budget_option.get()
        code_select = item_budget_select.split(" - ")[0]
        name_select = item_budget_select.split(" - ")[1]
        if self.chapter_budget_option.get()=="PA000 - PARTIDAS TIPO":
            id_item = get_id_item_sub_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2], "codigo",
                                         code_select, "resumen", name_select)
            id_ud_item = get_item_id_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2],
                                        "id_unidades", id_item)
            ud_item = get_item_id_bd(select_data[0], select_data[1], "tbl_pres_unidades", select_data[2], "unidad",
                                     id_ud_item)
        else:
            id_item = get_id_item_sub_bd(select_data[0], select_data[1],  "tbl_pres_precios", select_data[2], "codigo",
                                                   code_select, "resumen", name_select)
            id_ud_item = get_item_id_bd(select_data[0], select_data[1], "tbl_pres_precios", select_data[2],  "id_unidades", id_item)
            ud_item = get_item_id_bd(select_data[0], select_data[1], "tbl_pres_unidades", select_data[2], "unidad",id_ud_item)

        # desplegamos la ventana para recoger la cantidad
        appAux4=AppAmountAdd(item_budget_select,ud_item)
        appAux4.grab_set()
        self.wait_window(appAux4)
        amount_value = appAux4.get_items()
        if isinstance(amount_value, str):
            amount = amount_value.replace(",", ".")
        else:
            amount = amount_value

        data.append(id_item)
        data.append(amount)
        data.append(id_project)
        data.append(id_register_select)
        if self.chapter_budget_option.get() == "PA000 - PARTIDAS TIPO":
            data.append(1)
        else:
            data.append(0)
        #añadimos el registro a la base de datos
        add_budget_item(select_data[0], select_data[1], select_data[2], data)
        #actaulizamos la ventana
        items_budget = get_filter_data_bd(select_data[0], select_data[1], "tbl_presupuesto", select_data[2], "id_arqueta",
                                          str(id_register_select))
        self.update_data_budget(select_data, items_budget)

        #Actualizamos el total del presupuesto
        self.total_budget_label.destroy()
        self.update_total_budget_event()


    def register_filter_budget_event(self,select_data):
        self.select_register = self.register_filter_option_budget.get()

        #se elimina y vuelve a crear el frame del presupuesto
        self.data_budget_frame.destroy()
        self.data_budget_frame = customtkinter.CTkScrollableFrame(self.budget_frame, corner_radius=0)
        self.data_budget_frame.grid(row=2, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=3)
        self.data_budget_frame.grid_columnconfigure(2, weight=5)

        # Actualiza el frame de los datos del presupuesto para el item seleccionado
        register_select = self.register_filter_option_budget.get()
        code_register_select = register_select.split(" - ")[0]
        id_register_select = get_id_item_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2], "codigo",
                                            str(code_register_select))
        items_budget = get_filter_data_bd(select_data[0], select_data[1], "tbl_presupuesto", select_data[2],
                                          "id_arqueta",
                                          str(id_register_select))
        self.update_data_budget(select_data, items_budget)

        #actualizamos el total del presupuesto
        self.total_budget_label.destroy()
        self.update_total_budget_event()


    def update_total_budget_event(self):
        if not hasattr(self, 'cost_items_budget') or not self.cost_items_budget:
            total_budget = "0"
        else:
            total_budget = f'{round(sum([float(item.replace(" €", "")) for item in self.cost_items_budget]),2)}'

        self.total_budget_label = customtkinter.CTkLabel(self.budget_frame,
                                                       text=f"Prespuesto de ejecución material: {total_budget} €",
                                                       anchor="e",
                                                       font=customtkinter.CTkFont(size=15, weight="bold"))
        self.total_budget_label.grid(row=3,column=1, padx=(30,10), pady=15, sticky="e")


    def import_budget_event(self,select_data):
        register_select = self.register_filter_option_budget.get()
        code_register_select = register_select.split(" - ")[0]
        id_register_select = get_id_item_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2], "codigo",
                                            str(code_register_select))
        items_budget = get_filter_data_bd(select_data[0], select_data[1], "tbl_presupuesto", select_data[2],
                                          "id_arqueta",
                                          str(id_register_select))
        import_budget_items(select_data[0], select_data[1], select_data[2], items_budget)
        self.cost_button_event(select_data)


    #""""""""""""""""""""""""""""""FUNCIONES PESTAÑA CERTIFICACIONES"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    def update_item_cost_option (self, select_data):
        chapter_select = self.chapter_cost_option.get()
        if chapter_select == "PA000 - PARTIDAS TIPO":
            item_cost_values = get_all_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2])
            if len(item_cost_values) == 0:
                # partida de presupuesto
                self.item_cost_option.destroy()
                self.item_cost_option = customtkinter.CTkLabel(self.filter_cost_frame,
                                                                 text="No hay grupos de partidas, modifica el presupuesto",
                                                                 anchor="center",
                                                                 font=customtkinter.CTkFont(size=13, weight="bold"))
                self.item_budget_option.grid(row=1, column=1, padx=(10, 5), pady=(5, 10), sticky="ew")
            else:
                item_values = []
                for item in item_cost_values:
                    code = item[1]
                    name = item[4]
                    item_values.append(str(code) + " - " + name)
                self.item_cost_option.destroy()
                self.item_cost_option = customtkinter.CTkOptionMenu(self.filter_cost_frame, dynamic_resizing=False,
                                                                      values=item_values)
                self.item_cost_option.grid(row=1, column=1, padx=(10, 5), pady=(5, 10), sticky="ew")
                self.item_cost_option.set(item_values[0])
        else:
            code_chapter_select = chapter_select.split(" - ")[0]
            name_chapter_select = chapter_select.split(" - ")[1]
            id_chapter_select = get_id_item_sub_bd(select_data[0], select_data[1], "tbl_pres_capitulos", select_data[2], "codigo_capitulo",
                                                   code_chapter_select, "capitulo", name_chapter_select)
            item_cost_values = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_precios", select_data[2],"id_capitulo",
                                                    str(id_chapter_select))
            item_values = []
            for item in item_cost_values:
                code = item[1]
                name = item[4]
                item_values.append(str(code) + " - " + name)
            self.item_cost_option.configure(values=item_values)
            self.item_cost_option.set(item_values[0])


    def update_data_cost (self, select_data, item_no_cert, item_cert):
        # cargar imagen de icono
        image_info_path = parent_path +"/source/info.png"
        self.info_image = customtkinter.CTkImage(Image.open(image_info_path), size=(20,20))
        image_update_path = parent_path +"/source/actualizar.png"
        self.update_image = customtkinter.CTkImage(Image.open(image_update_path), size=(20,20))
        image_delete_path = parent_path +"/source/papelera.png"
        self.delete_image = customtkinter.CTkImage(Image.open(image_delete_path), size=(20,20))
        image_cert_path = parent_path +"/source/monedas.png"
        self.cert_image = customtkinter.CTkImage(Image.open(image_cert_path), size=(20,20))

        # /////////////////////NO CERTIFICADAS//////////////////////////
        # Listas para almacenar las variables por fila
        self.id_bd_items_no_cert = []
        self.amount_values_no_cert = []
        self.price_items_no_cert = []
        self.cost_items_no_cert = []
        self.describe_items_no_cert = []


        #encabezados de la tabla
        self.code_cost_label_no_cert = customtkinter.CTkLabel(self.data_cost_frame1, text="Codigo",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=13, weight="bold"))
        self.code_cost_label_no_cert.grid(row=0, column=0, padx=5, pady=5, sticky="nwes")

        self.ud_cost_label_no_cert = customtkinter.CTkLabel(self.data_cost_frame1, text="Ud",
                                                      anchor="center",
                                                      font=customtkinter.CTkFont(size=13, weight="bold"))
        self.ud_cost_label_no_cert.grid(row=0, column=1, padx=5, pady=5, sticky="nwes")

        self.resume_cost_label_no_cert = customtkinter.CTkLabel(self.data_cost_frame1, text="Resumen",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13, weight="bold"))
        self.resume_cost_label_no_cert.grid(row=0, column=2, padx=5, pady=5, sticky="nwes")

        self.amount_cost_label_no_cert = customtkinter.CTkLabel(self.data_cost_frame1, text="Cantidad",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13, weight="bold"))
        self.amount_cost_label_no_cert.grid(row=0, column=4, padx=5, pady=5, sticky="nwes")

        self.price_cost_label_no_cert = customtkinter.CTkLabel(self.data_cost_frame1, text="Precio",
                                                         anchor="center",
                                                         font=customtkinter.CTkFont(size=13, weight="bold"))
        self.price_cost_label_no_cert.grid(row=0, column=6, padx=5, pady=5, sticky="nwes")

        self.cost_cost_label_no_cert = customtkinter.CTkLabel(self.data_cost_frame1, text="Coste",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=13, weight="bold"))
        self.cost_cost_label_no_cert.grid(row=0, column=7, padx=5, pady=5, sticky="nwes")

        i=0
        if len(item_no_cert) != 0:
            for i,item in enumerate(item_no_cert):
                i+=1
                id_bd = item[0]
                self.id_bd_items_no_cert.append(id_bd)
                id_item = item[1]
                if item[7] == 0:
                    data_item = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_precios", select_data[2], "id", str(id_item))
                    if len(data_item) != 0:
                        data_item=data_item[0]
                else:
                    data_item = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2], "id", str(id_item))
                    if len(data_item) != 0:
                        data_item=data_item[0]


                self.code_item_no_cert= customtkinter.CTkLabel(self.data_cost_frame1, text=data_item[1],
                                                                anchor="center")
                self.code_item_no_cert.grid(row=i, column=0, padx=5, pady=5, sticky="nwes")

                ud_value=get_item_id_bd(select_data[0], select_data[1], "tbl_pres_unidades", select_data[2],"unidad",str(data_item[3]))
                self.ud_item_no_cert= customtkinter.CTkLabel(self.data_cost_frame1, text=ud_value, anchor="center")
                self.ud_item_no_cert.grid(row=i, column=1, padx=5, pady=5, sticky="nwes")

                self.code_item_no_cert= customtkinter.CTkLabel(self.data_cost_frame1, text=data_item[4], anchor="center")
                self.code_item_no_cert.grid(row=i, column=2, padx=5, pady=5, sticky="nwes")

                self.describe_items_no_cert.append(data_item[5])
                self.description_button_no_cert= customtkinter.CTkButton(self.data_cost_frame1, image=self.info_image, text="",
                                                                        command=lambda i=i:  self.info_event(self.describe_items_no_cert,i),width=30)
                self.description_button_no_cert.grid(row=i, column=3, padx=5, pady=5, sticky="nwes")

                amount_value = tk.StringVar(value=f"{str(item[2])}")
                self.amount_values_no_cert.append(amount_value)
                self.amount_entry_no_cert = customtkinter.CTkEntry(self.data_cost_frame1, textvariable=amount_value,
                                                           text_color="#FFFFFF")
                self.amount_entry_no_cert.grid(row=i, column=4, padx=5, pady=5, sticky="nwes")

                self.update_button_no_cert= customtkinter.CTkButton(self.data_cost_frame1, image=self.update_image, text="",
                                                                        command=lambda i=i: self.update_cost_no_cert(i,select_data,self.register_filter_option_cost.get()),width=30)
                self.update_button_no_cert.grid(row=i, column=5, padx=5, pady=5, sticky="nwes")

                price = round(float(data_item[6]), 2)
                self.price_item_no_cert = customtkinter.CTkLabel(self.data_cost_frame1, text=f"{price} €", anchor="center")
                self.price_item_no_cert.grid(row=i, column=6, padx=5, pady=5, sticky="nwes")
                self.price_items_no_cert.append(price)

                cost = round(price * float(amount_value.get() or 0), 2)
                self.cost_item_no_cert = customtkinter.CTkLabel(self.data_cost_frame1, text=f"{cost} €", anchor="center")
                self.cost_item_no_cert.grid(row=i, column=7, padx=5, pady=5, sticky="nwes")
                self.cost_items_no_cert.append(cost)

                self.delete_button_no_cert= customtkinter.CTkButton(self.data_cost_frame1, image=self.delete_image, text="",
                                                                        command=lambda i=i: self.delete_cost_event_no_cert(i,select_data),width=30)
                self.delete_button_no_cert.grid(row=i, column=8, padx=5, pady=5, sticky="nwes")

                self.cert_button_no_cert= customtkinter.CTkButton(self.data_cost_frame1, image=self.cert_image, text="",
                                                                        command=lambda i=i: self.cert_cost_event(i,select_data),width=30)
                self.cert_button_no_cert.grid(row=i, column=9, padx=5, pady=5, sticky="nwes")

        # /////////////////////CERTIFICADAS//////////////////////////
        # Listas para almacenar las variables por fila
        self.id_bd_items_cert = []
        self.amount_values_cert = []
        self.price_items_cert = []
        self.cost_items_cert  = []
        self.describe_items_cert = []

        # encabezados de la tabla
        self.code_cost_label_cert = customtkinter.CTkLabel(self.data_cost_frame2, text="Codigo",
                                                              anchor="center",
                                                              font=customtkinter.CTkFont(size=13, weight="bold"))
        self.code_cost_label_cert.grid(row=0, column=0, padx=5, pady=5, sticky="nwes")

        self.ud_cost_label_cert = customtkinter.CTkLabel(self.data_cost_frame2, text="Ud",
                                                            anchor="center",
                                                            font=customtkinter.CTkFont(size=13, weight="bold"))
        self.ud_cost_label_cert.grid(row=0, column=1, padx=5, pady=5, sticky="nwes")

        self.resume_cost_label_cert = customtkinter.CTkLabel(self.data_cost_frame2, text="Resumen",
                                                                anchor="center",
                                                                font=customtkinter.CTkFont(size=13, weight="bold"))
        self.resume_cost_label_cert.grid(row=0, column=2, padx=5, pady=5, sticky="nwes")

        self.amount_cost_label_cert = customtkinter.CTkLabel(self.data_cost_frame2, text="Cantidad",
                                                                anchor="center",
                                                                font=customtkinter.CTkFont(size=13, weight="bold"))
        self.amount_cost_label_cert.grid(row=0, column=4, padx=5, pady=5, sticky="nwes")

        self.price_cost_label_cert = customtkinter.CTkLabel(self.data_cost_frame2, text="Precio",
                                                               anchor="center",
                                                               font=customtkinter.CTkFont(size=13, weight="bold"))
        self.price_cost_label_cert.grid(row=0, column=5, padx=5, pady=5, sticky="nwes")

        self.cost_cost_label_cert = customtkinter.CTkLabel(self.data_cost_frame2, text="Coste",
                                                              anchor="center",
                                                              font=customtkinter.CTkFont(size=13, weight="bold"))
        self.cost_cost_label_cert.grid(row=0, column=6, padx=5, pady=5, sticky="nwes")

        i = 0
        if len(item_cert)!=0:
            for i, item in enumerate(item_cert):
                i += 1
                id_bd = item[0]
                self.id_bd_items_cert.append(id_bd)
                id_item = item[1]
                if item[7] == 0:
                    data_item = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_precios", select_data[2], "id", str(id_item))
                    if len(data_item) != 0:
                        data_item=data_item[0]
                else:
                    data_item = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2], "id", str(id_item))
                    if len(data_item) != 0:
                        data_item=data_item[0]

                self.code_item_cert = customtkinter.CTkLabel(self.data_cost_frame2, text=data_item[1],
                                                                anchor="center")
                self.code_item_cert.grid(row=i, column=0, padx=5, pady=5, sticky="nwes")

                ud_value = get_item_id_bd(select_data[0], select_data[1], "tbl_pres_unidades", select_data[2], "unidad",
                                          str(data_item[3]))
                self.ud_item_cert = customtkinter.CTkLabel(self.data_cost_frame2, text=ud_value,
                                                              anchor="center")
                self.ud_item_cert.grid(row=i, column=1, padx=5, pady=5, sticky="nwes")

                self.code_item_cert = customtkinter.CTkLabel(self.data_cost_frame2, text=data_item[4],
                                                                anchor="center")
                self.code_item_cert.grid(row=i, column=2, padx=5, pady=5, sticky="nwes")

                self.describe_items_cert.append(data_item[5])
                self.description_button_cert = customtkinter.CTkButton(self.data_cost_frame2, image=self.info_image,
                                                                       text="",
                                                                       command=lambda i=i: self.info_event(
                                                                              self.describe_items_cert, i),
                                                                       width=30)
                self.description_button_cert .grid(row=i, column=3, padx=5, pady=5, sticky="nwes")

                amount_value = tk.StringVar(value=f"{str(item[2])}")
                self.amount_values_cert.append(amount_value)
                self.amount_entry_cert  = customtkinter.CTkEntry(self.data_cost_frame2, textvariable=amount_value,
                                                                text_color="#FFFFFF", state='disable')
                self.amount_entry_cert.grid(row=i, column=4, padx=5, pady=5, sticky="nwes")

                price = round(float(data_item[6]), 2)
                self.price_item_cert = customtkinter.CTkLabel(self.data_cost_frame2, text=f"{price} €",
                                                                 anchor="center")
                self.price_item_cert.grid(row=i, column=5, padx=5, pady=5, sticky="nwes")
                self.price_items_cert.append(price)

                cost = round(price * float(amount_value.get() or 0), 2)
                self.cost_item_cert = customtkinter.CTkLabel(self.data_cost_frame2, text=f"{cost} €",
                                                                anchor="center")
                self.cost_item_cert.grid(row=i, column=6, padx=5, pady=5, sticky="nwes")
                self.cost_items_cert.append(cost)

                self.delete_button_cert = customtkinter.CTkButton(self.data_cost_frame2, image=self.delete_image,
                                                                  text="",
                                                                  command=lambda i=i: self.delete_cost_event_cert(i,
                                                                                                             select_data),
                                                                  width=30)
                self.delete_button_cert.grid(row=i, column=7, padx=5, pady=5, sticky="nwes")


    def update_cost_no_cert(self, i,select_data,register_select):
        value = self.amount_values_no_cert[i - 1].get()
        if  isinstance(value,str):
            amount=value.replace(",",".")
            amount_cost = float(amount) if amount else 0
        else:
            amount_cost = float(self.amount_values_no_cert[i - 1].get()) if self.amount_values_no_cert[i - 1].get() else 0
        id_bd = self.id_bd_items_no_cert[i - 1]
        # Obtener el valor actual del amount_entry y el precio por ítem en la fila 'i'
        mod_amount_cost_item(select_data[0], select_data[1], select_data[2], amount_cost, str(id_bd))

        # reiniciamos el frame
        self.data_cost_frame1.destroy()
        self.data_cost_frame1 = customtkinter.CTkScrollableFrame(self.cost_frame, corner_radius=0)
        self.data_cost_frame1.grid(row=3, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=2)
        self.data_cost_frame1.grid_columnconfigure(2, weight=5)

        self.data_cost_frame2.destroy()
        self.data_cost_frame2 = customtkinter.CTkScrollableFrame(self.cost_frame, corner_radius=0)
        self.data_cost_frame2.grid(row=5, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=2)
        self.data_cost_frame2.grid_columnconfigure(2, weight=5)

        code_register_select = register_select.split(" - ")[0]
        id_register_select = get_id_item_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2], "codigo",
                                            str(code_register_select))

        items_cost = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_certificacion", select_data[2],
                                        "id_arqueta", str(id_register_select))
        items_cert = []
        items_no_cert = []
        for sublist in items_cost:
            if sublist[-2] == 0:
                items_no_cert.append(sublist)
            else:
                items_cert.append(sublist)
        self.update_data_cost(select_data, items_no_cert, items_cert)

        # actualizamos el total de las certificaciones
        self.total_cost_label.destroy()
        self.update_total_cost_event()


    def delete_cost_event_no_cert(self, i, select_data):
        id_bd = self.id_bd_items_no_cert[i - 1]
        # borrar el item de la base de datos
        result=delete_cost_item(select_data[0], select_data[1], select_data[2], str(id_bd))
        #reiniciamos el frame
        self.data_cost_frame1.destroy()
        self.data_cost_frame1 = customtkinter.CTkScrollableFrame(self.cost_frame, corner_radius=0)
        self.data_cost_frame1.grid(row=3, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=2)
        self.data_cost_frame1.grid_columnconfigure(2, weight=5)

        self.data_cost_frame2.destroy()
        self.data_cost_frame2 = customtkinter.CTkScrollableFrame(self.cost_frame, corner_radius=0)
        self.data_cost_frame2.grid(row=5, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=2)
        self.data_cost_frame2.grid_columnconfigure(2, weight=5)

        register_select = self.register_filter_option_cost.get()
        code_register_select = register_select.split(" - ")[0]
        id_register_select = get_id_item_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2], "codigo",
                                            str(code_register_select))
        items_cost = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_certificacion", select_data[2], "id_arqueta",
                                        str(id_register_select))
        items_cert = []
        items_no_cert = []
        for sublist in items_cost:
            if sublist[-2] == 0:
                items_no_cert.append(sublist)
            else:
                items_cert.append(sublist)
        self.update_data_cost(select_data, items_no_cert, items_cert)
        if result =="ok":
            CTkMessagebox(title="Successfull Message!",
                          message="Se ha eliminado el item de la base de datos",
                          icon="check")

        else:
            CTkMessagebox(title="Warning Message!", message=f"Error: {result}",
                          icon="warning")

        # actualizamos el total de las certificaciones
        self.total_cost_label.destroy()
        self.update_total_cost_event()


    def cert_cost_event(self, i, select_data):
        id_bd = self.id_bd_items_no_cert[i - 1]
        # certificar el item de la base de datos
        cert_cost_item(select_data[0], select_data[1], select_data[2], str(id_bd))

        #reiniciamos el frame
        self.data_cost_frame1.destroy()
        self.data_cost_frame1 = customtkinter.CTkScrollableFrame(self.cost_frame, corner_radius=0)
        self.data_cost_frame1.grid(row=3, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=2)
        self.data_cost_frame1.grid_columnconfigure(2, weight=5)

        self.data_cost_frame2.destroy()
        self.data_cost_frame2 = customtkinter.CTkScrollableFrame(self.cost_frame, corner_radius=0)
        self.data_cost_frame2.grid(row=5, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=2)
        self.data_cost_frame2.grid_columnconfigure(2, weight=5)

        register_select = self.register_filter_option_cost.get()
        code_register_select = register_select.split(" - ")[0]
        id_register_select = get_id_item_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2], "codigo",
                                            str(code_register_select))
        items_cost = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_certificacion", select_data[2], "id_arqueta",
                                        str(id_register_select))
        items_cert = []
        items_no_cert = []
        for sublist in items_cost:
            if sublist[-2] == 0:
                items_no_cert.append(sublist)
            else:
                items_cert.append(sublist)
        self.update_data_cost(select_data, items_no_cert, items_cert)

        # actualizamos el total de las certificaciones
        self.total_cost_label.destroy()
        self.update_total_cost_event()


    def delete_cost_event_cert(self, i, select_data):
        id_bd = self.id_bd_items_cert[i - 1]
        # borrar el item de la base de datos
        result=delete_cost_item(select_data[0], select_data[1], select_data[2], str(id_bd))
        #reiniciamos el frame
        self.data_cost_frame1.destroy()
        self.data_cost_frame1 = customtkinter.CTkScrollableFrame(self.cost_frame, corner_radius=0)
        self.data_cost_frame1.grid(row=3, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=2)
        self.data_cost_frame1.grid_columnconfigure(2, weight=5)

        self.data_cost_frame2.destroy()
        self.data_cost_frame2 = customtkinter.CTkScrollableFrame(self.cost_frame, corner_radius=0)
        self.data_cost_frame2.grid(row=5, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=2)
        self.data_cost_frame2.grid_columnconfigure(2, weight=5)

        register_select = self.register_filter_option_cost.get()
        code_register_select = register_select.split(" - ")[0]
        id_register_select = get_id_item_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2], "codigo",
                                            str(code_register_select))
        items_cost = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_certificacion", select_data[2], "id_arqueta",
                                        str(id_register_select))
        items_cert = []
        items_no_cert = []
        for sublist in items_cost:
            if sublist[-2] == 0:
                items_no_cert.append(sublist)
            else:
                items_cert.append(sublist)
        self.update_data_cost(select_data, items_no_cert, items_cert)
        if result =="ok":
            CTkMessagebox(title="Successfull Message!",
                          message="Se ha eliminado el item de la base de datos",
                          icon="check")

        else:
            CTkMessagebox(title="Warning Message!", message=f"Error: {result}",
                          icon="warning")

        # actualizamos el total de las certificaciones
        self.total_cost_label.destroy()
        self.update_total_cost_event()


    def add_item_cost_event(self,select_data):
        #recogemos los datos para añadirlos en la función de añadir el item
        data = []

        register_select = self.register_filter_option_cost.get()
        code_register_select = register_select.split(" - ")[0]
        id_register_select = get_id_item_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2], "codigo",
                                            str(code_register_select))

        id_project=get_id_item_bd(select_data[0], select_data[1], "tbl_proyectos", select_data[2],
                                        "codigo", select_data[2])

        item_cost_select = self.item_cost_option.get()
        code_select = item_cost_select.split(" - ")[0]
        name_select = item_cost_select.split(" - ")[1]
        if self.chapter_cost_option.get() == "PA000 - PARTIDAS TIPO":
            id_item = get_id_item_sub_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2], "codigo",
                                         code_select, "resumen", name_select)
            id_ud_item = get_item_id_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2],
                                        "id_unidades", id_item)
            ud_item = get_item_id_bd(select_data[0], select_data[1], "tbl_pres_unidades", select_data[2], "unidad",
                                     id_ud_item)
        else:
            id_item = get_id_item_sub_bd(select_data[0], select_data[1],  "tbl_pres_precios", select_data[2], "codigo",
                                                   code_select, "resumen", name_select)
            id_ud_item = get_item_id_bd(select_data[0], select_data[1], "tbl_pres_precios", select_data[2],  "id_unidades", id_item)
            ud_item = get_item_id_bd(select_data[0], select_data[1], "tbl_pres_unidades", select_data[2], "unidad",id_ud_item)

        # desplegamos la ventana para recoger la cantidad
        appAux5=AppAmountAdd(item_cost_select,ud_item)
        appAux5.grab_set()
        self.wait_window(appAux5)
        amount_value_cost = appAux5.get_items()
        if isinstance(amount_value_cost, str):
            amount_cost = amount_value_cost.replace(",", ".")
        else:
            amount_cost = amount_value_cost

        data.append(id_item)
        data.append(amount_cost)
        data.append(id_project)
        data.append(id_register_select)
        if self.chapter_cost_option.get() == "PA000 - PARTIDAS TIPO":
            data.append(1)
        else:
            data.append(0)
        #añadimos el registro a la base de datos
        add_cost_item(select_data[0], select_data[1], select_data[2], data)
        #actualizamos la ventana
        items_cost = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_certificacion", select_data[2],
                                        "id_arqueta",
                                        str(id_register_select))
        items_cert = []
        items_no_cert = []
        for sublist in items_cost:
            if sublist[-2] == 0:
                items_no_cert.append(sublist)
            else:
                items_cert.append(sublist)
        self.update_data_cost(select_data, items_no_cert, items_cert)

        #Actualizamos el total de las certificaciones
        self.total_cost_label.destroy()
        self.update_total_cost_event()


    def register_filter_cost_event(self,select_data):
        self.select_register= self.register_filter_option_cost.get()

        self.data_cost_frame1.destroy()
        self.data_cost_frame1 = customtkinter.CTkScrollableFrame(self.cost_frame, corner_radius=0)
        self.data_cost_frame1.grid(row=3, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=2)
        self.data_cost_frame1.grid_columnconfigure(2, weight=5)

        self.data_cost_frame2.destroy()
        self.data_cost_frame2 = customtkinter.CTkScrollableFrame(self.cost_frame, corner_radius=0)
        self.data_cost_frame2.grid(row=5, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=2)
        self.data_cost_frame2.grid_columnconfigure(2, weight=5)

        register_select=self.register_filter_option_cost.get()
        code_register_select = register_select.split(" - ")[0]
        id_register_select = get_id_item_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2], "codigo",
                                            str(code_register_select))
        items_cost = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_certificacion", select_data[2],
                                        "id_arqueta",
                                        str(id_register_select))
        items_cert = []
        items_no_cert = []
        for sublist in items_cost:
            if sublist[-2] == 0:
                items_no_cert.append(sublist)
            else:
                items_cert.append(sublist)
        self.update_data_cost(select_data, items_no_cert, items_cert)

        # actualizamos el total de las certificaciones
        self.total_cost_label.destroy()
        self.update_total_cost_event()


    def update_total_cost_event(self):
        total_no_cert= sum([float(str(item).replace(" €", "")) for item in self.cost_items_no_cert])
        total_cert = sum([float(str(item).replace(" €", "")) for item in self.cost_items_cert])
        total_cert  =round(total_cert, 2)
        total_no_cert = round(total_no_cert, 2)
        total_cost = total_cert+total_no_cert
        total_cost = round(total_cost,2)

        self.total_cost_label = customtkinter.CTkLabel(self.cost_frame,
                                                         text=f"Presupuesto no certificado: {total_no_cert} € | Presupuesto certificado: {total_cert} €  |  Presupuesto total {total_cost} € ",
                                                         anchor="e",
                                                         font=customtkinter.CTkFont(size=15, weight="bold"))
        self.total_cost_label.grid(row=6, padx=30, pady=15, sticky="nwes", columnspan=2)


    def mod_budget_event(self,select_data):
        appAux=AppBudgetUpdate(select_data)
        appAux.grab_set()
        self.wait_window(appAux)
        # reiniciamos el frame
        self.data_budget_frame.destroy()
        self.data_budget_frame = customtkinter.CTkScrollableFrame(self.budget_frame, corner_radius=0)
        self.data_budget_frame.grid(row=2, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=3)
        self.data_budget_frame.grid_columnconfigure(2, weight=5)

        #actaulizamos los valores
        register_select = self.register_filter_option_budget.get()
        code_register_select = register_select.split(" - ")[0]
        id_register_select = get_id_item_bd(select_data[0], select_data[1], "tbl_inventario", select_data[2],
                                            "codigo",
                                            str(code_register_select))
        items_budget = get_filter_data_bd(select_data[0], select_data[1], "tbl_presupuesto", select_data[2],
                                          "id_arqueta", str(id_register_select))
        self.update_data_budget(select_data, items_budget)

