import customtkinter
from PIL import Image
import tkinter as tk
from script.modulo_db import get_option_item_bd,get_id_item_bd,mod_catalog_regis_item,get_option_item_sub_bd,get_all_bd
from interface.item_aux_add_interfaz import AppItemAdd
from interface.base import BaseWindow
from interface.components import show_success, show_error
import os

# Obtener la ruta actual
current_path = os.path.dirname(os.path.realpath(__file__))

# Subir un nivel en la estructura de carpetas
parent_path = os.path.dirname(current_path)

customtkinter.set_appearance_mode("dark")

class AppCatalogRegisMod(BaseWindow):
    width = 800
    height = 700

    def __init__(self, select_data,item_select):
        super().__init__(title="Modificar catálogo")
        password = select_data[1]
        user = select_data[0]
        schema = select_data[2]


        self.title("Modificación pieza del catálogo")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        common_fg_color = "#171717"

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)


        #almacena tipo
        self.type_label = customtkinter.CTkLabel(self, text="TIPO DE ELEMENTO:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.type_label.grid(row=0, column=0, padx=(30,5), pady=(30,10), sticky= "e")
        type_value = get_option_item_bd(user, password, "tbl_cata_regis_tipo", schema, 'tipo')
        type_value.sort(key=str.lower)
        self.type_option = customtkinter.CTkOptionMenu(self,
                                                         dynamic_resizing=False,
                                                         values=type_value)
        self.type_option.grid(row=0, column=1, padx=(5,5), pady=(30,10), sticky= "ew")
        self.type_option.set(item_select[1])
        self.type_button = customtkinter.CTkButton(self, text="Añadir tipo",
                                                             command=lambda:self.add_type_data(select_data), width=50)
        self.type_button.grid(row=0, column=2, padx=(5,30), pady=(30,10), sticky= "ew")

        #almacena marca
        self.brand_label = customtkinter.CTkLabel(self, text="PROVEEDOR:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.brand_label.grid(row=1, column=0, padx=(30,5), pady=10, sticky= "e")
        brand_value=get_option_item_bd(user, password, "tbl_cata_regis_proveedor", schema, 'proveedor')
        brand_value.sort(key=str.lower)
        self.brand_option = customtkinter.CTkOptionMenu(self,
                                                         dynamic_resizing=False,
                                                         values=brand_value)
        self.brand_option.grid(row=1, column=1, padx=(5,5), pady=10, sticky= "ew")
        self.brand_option.set(item_select[2])
        self.brand_button = customtkinter.CTkButton(self, text="Añadir proveedor",
                                                             command=lambda:self.add_brand_data(select_data), width=50)
        self.brand_button.grid(row=1, column=2, padx=(5,30), pady=10, sticky= "ew")

        #almacena nombre modelo
        self.model_label = customtkinter.CTkLabel(self, text="MODELO:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.model_label.grid(row=2, column=0, padx=(30,5), pady=10, sticky= "e")
        default_model_value = tk.StringVar(value=item_select[3])
        self.model_entry = customtkinter.CTkEntry(self, textvariable=default_model_value,
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.model_entry.grid(row=2, column=1, padx=(5,30), pady=10, sticky= "ew", columnspan=2)

        #almacena referencia
        self.ref_label = customtkinter.CTkLabel(self, text="REFERENCIA:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.ref_label.grid(row=3, column=0, padx=(30,5), pady=10, sticky= "e")
        default_ref_value = tk.StringVar(value=item_select[4])
        self.ref_entry = customtkinter.CTkEntry(self, textvariable=default_ref_value,
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.ref_entry.grid(row=3, column=1, padx=(5,30), pady=10, sticky= "ew", columnspan=2)

        # almacena dimension A
        self.dimA_label = customtkinter.CTkLabel(self, text="DIMENSIÓN A:",
                                                 anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                 width=50)
        self.dimA_label.grid(row=4, column=0, padx=(30, 5), pady=10, sticky="e")
        default_dimA_value = tk.StringVar(value=item_select[5])
        self.dimA_entry = customtkinter.CTkEntry(self, textvariable=default_dimA_value,
                                                 fg_color=common_fg_color, text_color="#FFFFFF")
        self.dimA_entry.grid(row=4, column=1, padx=(5, 30), pady=10, sticky="ew", columnspan=2)

        # almacena dimension B
        self.dimB_label = customtkinter.CTkLabel(self, text="DIMENSIÓN B:",
                                                 anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                 width=50)
        self.dimB_label.grid(row=5, column=0, padx=(30, 5), pady=10, sticky="e")
        default_dimB_value = tk.StringVar(value=item_select[6])
        self.dimB_entry = customtkinter.CTkEntry(self,  textvariable=default_dimB_value,
                                                 fg_color=common_fg_color, text_color="#FFFFFF")
        self.dimB_entry.grid(row=5, column=1, padx=(5, 30), pady=10, sticky="ew", columnspan=2)

        # almacena dimension C
        self.dimC_label = customtkinter.CTkLabel(self, text="DIMENSIÓN C:",
                                                 anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                 width=50)
        self.dimC_label.grid(row=6, column=0, padx=(30, 5), pady=10, sticky="e")
        default_dimC_value = tk.StringVar(value=item_select[7])
        self.dimC_entry = customtkinter.CTkEntry(self,  textvariable=default_dimC_value,
                                                 fg_color=common_fg_color, text_color="#FFFFFF")
        self.dimC_entry.grid(row=6, column=1, padx=(5, 30), pady=10, sticky="ew", columnspan=2)


        #almacena descripción
        self.description_label = customtkinter.CTkLabel(self, text="DESCRIPCIÓN:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.description_label.grid(row=7, column=0, padx=(30,5), pady=(10,10), sticky= "e")
        self.description_entry = customtkinter.CTkTextbox(self, fg_color=common_fg_color,
                                                        border_width=2, border_color="#565B5E",text_color="#FFFFFF")
        self.description_entry.grid(row=7, column=1, padx=(5,30), pady=(10,10), sticky= "ew", columnspan=2)
        self.description_entry.insert("1.0",item_select[8])

        # relacion presupuesto
        self.rel_budget_label = customtkinter.CTkLabel(self, text="RELACIÓN PARTIDA DE PRESUPUESTO:",
                                                       anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                       width=50)
        self.rel_budget_label.grid(row=8, column=0, padx=(30, 5), pady=10, sticky="e")
        budget_values = get_all_bd(user, password, "tbl_pres_precios", schema)
        rel_budget_value = []
        for item in budget_values:
            rel_budget_value.append(str(item[1]) + " - " + item[4])
        self.rel_budget_option = customtkinter.CTkOptionMenu(self,
                                                             dynamic_resizing=False,
                                                             values=rel_budget_value)
        self.rel_budget_option.grid(row=8, column=1, padx=(5, 30), pady=10, sticky="ew", columnspan=2)
        if item_select[9] == '-':
            self.rel_budget_option.set("-")
        else:
            self.rel_budget_option.set(str(item_select[9]) + " - " +
                                       get_option_item_sub_bd(user, password, "tbl_pres_precios", schema, 'resumen',
                                                              str(item_select[9]), 'codigo')[0])

        # boton de guardar
        save_path = parent_path +"/resources/images/guardar.png"
        self.save_image = customtkinter.CTkImage(Image.open(save_path))
        self.save_button = customtkinter.CTkButton(self, text="Guardar",image=self.save_image, compound="left",fg_color="green",
                                                   font=("default", 14, "bold"),
                                                   command=lambda: self.save(select_data,item_select[0]),  height=40)
        self.save_button.grid(row=9, column=0, padx=(30,1), pady=10, sticky= "ew")


        # boton de cancelar
        cancel_path = parent_path +"/resources/images/cancelar.png"
        self.cancel_image = customtkinter.CTkImage(Image.open(cancel_path))
        self.cancel_button = customtkinter.CTkButton(self, text="Cancelar",image=self.cancel_image, compound="left",fg_color="red",
                                                   font=("default", 14, "bold"),
                                                   command=self.cancel,  height=40)
        self.cancel_button.grid(row=9, column=2, padx=(10,30), pady=10, sticky= "ew")

        self.lift()



    def add_type_data(self,select_data):
        appAux = AppItemAdd(select_data, 'tbl_cata_regis_tipo','tipo','Tipo elemento')
        appAux.grab_set()
        self.wait_window(appAux)
        type_value = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_regis_tipo", select_data[2], 'tipo')
        type_value.sort()
        self.type_option.configure(values=type_value)


    def add_brand_data(self,select_data):
        appAux = AppItemAdd(select_data, 'tbl_cata_regis_proveedor','proveedor','Proveedor')
        appAux.grab_set()
        self.wait_window(appAux)
        brand_value = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_regis_proveedor", select_data[2], 'proveedor')
        brand_value.sort()
        self.brand_option.configure(values=brand_value)

    def save(self, select_data,id_item):
        #recogida de datos de la interfaz
        id_type= get_id_item_bd(select_data[0], select_data[1], "tbl_cata_regis_tipo", select_data[2],
                                        "tipo", self.type_option.get())
        id_brand = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_regis_proveedor", select_data[2],
                                         "proveedor", self.brand_option.get())
        model = self.model_entry.get()
        ref = self.ref_entry.get()
        dimA = self.dimA_entry.get()
        dimB = self.dimB_entry.get()
        dimC = self.dimC_entry.get()
        description = self.description_entry.get("1.0", "end-1c")
        rel_budget_option_value = self.rel_budget_option.get()
        if isinstance(rel_budget_option_value, str):
            rel_budget_option_value = [rel_budget_option_value]
        cod_budget = rel_budget_option_value[0].split(" - ")[0]

        data = [id_type, id_brand, model, ref, dimA, dimB, dimC, description, cod_budget]
        result = mod_catalog_regis_item(select_data[0], select_data[1], select_data[2], data, id_item)
        #mensaje de avisos
        if result == 'ok':
            mssg="Se ha modificado la pieza en la base de datos"
            self.destroy()
            show_success(mssg)
        else:
            mssg="ERROR: "+str(result)
            self.destroy()
            show_error(mssg)
