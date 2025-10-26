import customtkinter
from PIL import Image
from tkinter import filedialog
import tkinter as tk
from script.modulo_db import (get_option_item_bd, update_reference, get_id_item_bd, mod_catalog_hidro_item,
                                get_option_item_sub_bd, get_id_item_sub_bd,get_all_bd)
from interface.item_aux_add_interfaz import AppItemAdd
from interface.item_aux_type_add_interfaz import AppItemTypeAdd
from interface.base import BaseWindow
from interface.components import show_success, show_error
import os

# Obtener la ruta actual
current_path = os.path.dirname(os.path.realpath(__file__))

# Subir un nivel en la estructura de carpetas
parent_path = os.path.dirname(current_path)

customtkinter.set_appearance_mode("dark")

class AppCatalogHidroMod(BaseWindow):
    width = 800
    height = 700

    def __init__(self, select_data,item_select):
        super().__init__(title="Modificar catálogo hidráulico")
        password = select_data[1]
        user = select_data[0]
        schema = select_data[2]

        self.title("Modificación pieza del catálogo")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        common_fg_color = "#171717"

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.data_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0)
        self.data_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        self.data_frame.grid_columnconfigure(0, weight=1)
        self.data_frame.grid_columnconfigure(1, weight=2)
        self.data_frame.grid_columnconfigure(2, weight=1)

        # almacena Familia
        self.family_label = customtkinter.CTkLabel(self.data_frame, text="FAMILIA DE ELEMENTO:",
                                                   anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                   width=50)
        self.family_label.grid(row=0, column=0, padx=(30, 5), pady=(30, 10), sticky="e")
        family_value = get_option_item_bd(user, password, "tbl_cata_hidra_familia", schema, 'familia')
        family_value.sort(key=str.lower)
        self.family_option = customtkinter.CTkOptionMenu(self.data_frame,
                                                         dynamic_resizing=False,
                                                         values=family_value,
                                                         command=lambda
                                                             event: self.update_type_options(
                                                             select_data))
        self.family_option.grid(row=0, column=1, padx=(5, 5), pady=(30, 10), sticky="ew")
        self.family_option.set(get_option_item_sub_bd(user, password, "tbl_cata_hidra_familia", schema, "familia", item_select[1],"id"))
        self.family_button = customtkinter.CTkButton(self.data_frame, text="Añadir familia",
                                                     command=lambda: self.add_family_data(select_data), width=50)
        self.family_button.grid(row=0, column=2, padx=(5, 30), pady=(30, 10), sticky="ew")

        #almacena tipo
        self.type_label = customtkinter.CTkLabel(self.data_frame, text="TIPO DE ELEMENTO:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.type_label.grid(row=1, column=0, padx=(30,5), pady=10, sticky= "e")
        select_family = self.family_option.get()
        id_family = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_familia", select_data[2], "familia",
                                   select_family[0])
        type_values = get_option_item_sub_bd(select_data[0], select_data[1], "tbl_cata_hidra_tipo", select_data[2],
                                             "tipo_elemento", str(id_family), "id_familia")
        type_values.sort(key=str.lower)
        self.type_option = customtkinter.CTkOptionMenu(self.data_frame,
                                                         dynamic_resizing=False,
                                                         values=type_values)
        self.type_option.grid(row=1, column=1, padx=(5,5), pady=10, sticky= "ew")
        self.type_option.set(get_option_item_sub_bd(user, password,"tbl_cata_hidra_tipo",schema,"tipo_elemento",item_select[2],"id"))
        self.type_button = customtkinter.CTkButton(self.data_frame, text="Añadir tipo",
                                                             command=lambda:self.add_type_data(select_data), width=50)
        self.type_button.grid(row=1, column=2, padx=(5,30), pady=10, sticky= "ew")
        self.family_option.bind("<<ComboboxSelected>>", lambda event: self.update_type_options(select_data))

        #almacena marca
        self.brand_label = customtkinter.CTkLabel(self.data_frame, text="MARCA:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.brand_label.grid(row=2, column=0, padx=(30,5), pady=10, sticky= "e")
        brand_value=get_option_item_bd(user, password, "tbl_cata_hidra_marcas", schema, 'marca')
        brand_value.sort(key=str.lower)
        self.brand_option = customtkinter.CTkOptionMenu(self.data_frame,
                                                         dynamic_resizing=False,
                                                         values=brand_value)
        self.brand_option.grid(row=2, column=1, padx=(5,5), pady=10, sticky= "ew")
        self.brand_option.set(get_option_item_sub_bd(user, password, "tbl_cata_hidra_marcas", schema, "marca", item_select[3],"id"))
        self.brand_button = customtkinter.CTkButton(self.data_frame, text="Añadir marca",
                                                             command=lambda:self.add_brand_data(select_data), width=50)
        self.brand_button.grid(row=2, column=2, padx=(5,30), pady=10, sticky= "ew")

        # almacena caracteristica
        self.feature_label = customtkinter.CTkLabel(self.data_frame, text="CARACTERÍSTICA:",
                                                    anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                    width=50)
        self.feature_label.grid(row=3, column=0, padx=(30, 5), pady=10, sticky="e")
        feature_value = get_option_item_bd(user, password, "tbl_cata_hidra_caracteristica", schema, 'caracteristica')
        feature_value.sort(key=str.lower)
        self.feature_option = customtkinter.CTkOptionMenu(self.data_frame,
                                                          dynamic_resizing=False,
                                                          values=feature_value)
        self.feature_option.grid(row=3, column=1, padx=(5, 5), pady=10, sticky="ew")
        self.feature_option.set(get_option_item_sub_bd(user, password, "tbl_cata_hidra_caracteristica", schema, "caracteristica", item_select[4], "id"))
        self.feature_button = customtkinter.CTkButton(self.data_frame, text="Añadir característica",
                                                      command=lambda: self.add_feature_data(select_data), width=50)
        self.feature_button.grid(row=3, column=2, padx=(5, 30), pady=10, sticky="ew")

        #almacena nombre modelo
        self.model_label = customtkinter.CTkLabel(self.data_frame, text="MODELO:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.model_label.grid(row=4, column=0, padx=(30,5), pady=10, sticky= "e")
        default_model_value = tk.StringVar(value=item_select[5])
        self.model_entry = customtkinter.CTkEntry(self.data_frame, textvariable=default_model_value,
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.model_entry.grid(row=4, column=1, padx=(5,30), pady=10, sticky= "ew", columnspan=2)

        #almacena referencia
        self.ref_label = customtkinter.CTkLabel(self.data_frame, text="REFERENCIA:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.ref_label.grid(row=5, column=0, padx=(30,5), pady=10, sticky= "e")
        default_ref_value = tk.StringVar(value=item_select[6])
        self.ref_entry = customtkinter.CTkEntry(self.data_frame, textvariable=default_ref_value,
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.ref_entry.grid(row=5, column=1, padx=(5,30), pady=10, sticky= "ew", columnspan=2)

        #almacena DN inicial
        self.dni_label = customtkinter.CTkLabel(self.data_frame, text="DN inicial:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.dni_label.grid(row=6, column=0, padx=(30,5), pady=10, sticky= "e")
        dni_value = get_option_item_bd(user, password, "tbl_cata_hidra_dni", schema, 'dni')
        dni_value.sort(key=str.lower)
        self.dni_option = customtkinter.CTkOptionMenu(self.data_frame,
                                                         dynamic_resizing=False,
                                                         values=dni_value)
        self.dni_option.grid(row=6, column=1, padx=(5,5), pady=10, sticky= "ew")
        self.dni_option.set(get_option_item_sub_bd(user, password, "tbl_cata_hidra_dni", schema, "dni", item_select[7],"id"))
        self.dni_button = customtkinter.CTkButton(self.data_frame, text="Añadir DNi",
                                                             command=lambda:self.add_dni_data(select_data), width=50)
        self.dni_button.grid(row=6, column=2, padx=(5,30), pady=10, sticky= "ew")

        #almacena DN final
        self.dnf_label = customtkinter.CTkLabel(self.data_frame, text="DN final:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.dnf_label.grid(row=7, column=0, padx=(30,5), pady=10, sticky= "e")
        dnf_value = get_option_item_bd(user, password, "tbl_cata_hidra_dnf", schema, 'dnf')
        dnf_value.sort(key=str.lower)
        self.dnf_option = customtkinter.CTkOptionMenu(self.data_frame,
                                                         dynamic_resizing=False,
                                                         values=dnf_value)
        self.dnf_option.grid(row=7, column=1, padx=(5,5), pady=10, sticky= "ew")
        self.dnf_option.set(get_option_item_sub_bd(user, password, "tbl_cata_hidra_dnf", schema, "dnf", item_select[8],"id"))
        self.dnf_button = customtkinter.CTkButton(self.data_frame, text="Añadir DNf",
                                                             command=lambda:self.add_dnf_data(select_data), width=50)
        self.dnf_button.grid(row=7, column=2, padx=(5,30), pady=10, sticky= "ew")

        # almacena PN
        self.pn_label = customtkinter.CTkLabel(self.data_frame, text="PN:",
                                               anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                               width=50)
        self.pn_label.grid(row=8, column=0, padx=(30, 5), pady=10, sticky="e")
        pn_value = get_option_item_bd(user, password, "tbl_cata_hidra_pn", schema, 'pn')
        pn_value.sort(key=str.lower)
        self.pn_option = customtkinter.CTkOptionMenu(self.data_frame,
                                                     dynamic_resizing=False,
                                                     values=pn_value)
        self.pn_option.grid(row=8, column=1, padx=(5, 5), pady=10, sticky="ew")
        self.pn_option.set(get_option_item_sub_bd(user, password, "tbl_cata_hidra_pn", schema, "pn", item_select[9],"id"))
        self.pn_button = customtkinter.CTkButton(self.data_frame, text="Añadir PN",
                                                 command=lambda: self.add_pn_data(select_data), width=50)
        self.pn_button.grid(row=8, column=2, padx=(5, 30), pady=10, sticky="ew")

        # almacena ANGULO
        self.angle_label = customtkinter.CTkLabel(self.data_frame, text="ÁNGULO:",
                                               anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                               width=50)
        self.angle_label.grid(row=9, column=0, padx=(30, 5), pady=10, sticky="e")
        angle_value = get_option_item_bd(user, password, "tbl_cata_hidra_angulo", schema, 'angulo')
        angle_value.sort(key=str.lower)
        self.angle_option = customtkinter.CTkOptionMenu(self.data_frame,
                                                     dynamic_resizing=False,
                                                     values=angle_value)
        self.angle_option.grid(row=9, column=1, padx=(5, 5), pady=10, sticky="ew")
        self.angle_option.set(get_option_item_sub_bd(user, password, "tbl_cata_hidra_angulo", schema, "angulo", item_select[10], "id"))
        self.angle_button = customtkinter.CTkButton(self.data_frame, text="Añadir ángulo",
                                                 command=lambda: self.add_angle_data(select_data), width=50)
        self.angle_button.grid(row=9, column=2, padx=(5, 30), pady=10, sticky="ew")

        # almacena referencias cad
        self.ref_cad_label = customtkinter.CTkLabel(self.data_frame, text="REFERNCIA CAD:",
                                               anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                               width=50)
        self.ref_cad_label.grid(row=10, column=0, padx=(30, 5), pady=10, sticky="e")
        ref_cad_value = get_option_item_bd(user, password, "tbl_cata_hidra_referencias_cad", schema, 'ruta')
        ref_cad_value.sort(key=str.lower)
        self.ref_cad_option = customtkinter.CTkOptionMenu(self.data_frame,
                                                     dynamic_resizing=False,
                                                     values=ref_cad_value)
        self.ref_cad_option.grid(row=10, column=1, padx=(5, 5), pady=10, sticky="ew")
        self.ref_cad_option.set(item_select[16])
        self.ref_cad_button = customtkinter.CTkButton(self.data_frame, text="Actualizar referencias CAD",
                                                 command=lambda: self.update_ref_cad_data(select_data), width=50)
        self.ref_cad_button.grid(row=10, column=2, padx=(5, 30), pady=10, sticky="ew")

        #almacena descripción
        self.description_label = customtkinter.CTkLabel(self.data_frame, text="DESCRIPCIÓN:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.description_label.grid(row=11, column=0, padx=(30,5), pady=(10,10), sticky= "e")
        self.description_entry = customtkinter.CTkTextbox(self.data_frame, fg_color=common_fg_color,
                                                        border_width=2, border_color="#565B5E",text_color="#FFFFFF")
        self.description_entry.grid(row=11, column=1, padx=(5,30), pady=(10,10), sticky= "ew", columnspan=2)
        self.description_entry.insert("1.0",item_select[17])

        # almacena longitud
        self.len_label = customtkinter.CTkLabel(self.data_frame, text="LONGITUD:",
                                                anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                width=50)
        self.len_label.grid(row=12, column=0, padx=(30, 5), pady=10, sticky="e")
        default_len_value = tk.StringVar(value=item_select[11])
        self.len_entry = customtkinter.CTkEntry(self.data_frame, textvariable=default_len_value,
                                                fg_color=common_fg_color, text_color="#FFFFFF")
        self.len_entry.grid(row=12, column=1, padx=(5, 30), pady=10, sticky="ew", columnspan=2)

        # almacena longitud extremos
        self.len_ext_label = customtkinter.CTkLabel(self.data_frame, text="LONGITUD EXTREMOS:",
                                                    anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                    width=50)
        self.len_ext_label.grid(row=13, column=0, padx=(30, 5), pady=10, sticky="e")
        default_len_ext_value = tk.StringVar(value=item_select[12])
        self.len_ext_entry = customtkinter.CTkEntry(self.data_frame,
                                                    textvariable=default_len_ext_value,
                                                    fg_color=common_fg_color, text_color="#FFFFFF")
        self.len_ext_entry.grid(row=13, column=1, padx=(5, 30), pady=10, sticky="ew", columnspan=2)

        # almacena altura eje de la pieza
        self.h_axis_label = customtkinter.CTkLabel(self.data_frame, text="ALTURA EJE:",
                                                   anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                   width=50)
        self.h_axis_label.grid(row=14, column=0, padx=(30, 5), pady=10, sticky="e")
        default_h_axis_value = tk.StringVar(value=item_select[13])
        self.h_axis_entry = customtkinter.CTkEntry(self.data_frame, textvariable=default_h_axis_value,
                                                   fg_color=common_fg_color, text_color="#FFFFFF")
        self.h_axis_entry.grid(row=14, column=1, padx=(5, 30), pady=10, sticky="ew", columnspan=2)

        # altura total de la pieza
        self.h_total_label = customtkinter.CTkLabel(self.data_frame, text="ALTURA TOTAL:",
                                                    anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                    width=50)
        self.h_total_label.grid(row=15, column=0, padx=(30, 5), pady=10, sticky="e")
        default_h_total_value = tk.StringVar(value=item_select[14])
        self.h_total_entry = customtkinter.CTkEntry(self.data_frame, textvariable=default_h_total_value,
                                                    fg_color=common_fg_color, text_color="#FFFFFF")
        self.h_total_entry.grid(row=15, column=1, padx=(5, 30), pady=10, sticky="ew", columnspan=2)

        # almacena lpeso
        self.weight_label = customtkinter.CTkLabel(self.data_frame, text="PESO:",
                                                   anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                   width=50)
        self.weight_label.grid(row=16, column=0, padx=(30, 5), pady=10, sticky="e")
        default_weight_value = tk.StringVar(value=item_select[15])
        self.weight_entry = customtkinter.CTkEntry(self.data_frame, textvariable=default_weight_value,
                                                   fg_color=common_fg_color, text_color="#FFFFFF")
        self.weight_entry.grid(row=16, column=1, padx=(5, 30), pady=10, sticky="ew", columnspan=2)

        #relacion presupuesto
        self.rel_budget_label = customtkinter.CTkLabel(self.data_frame, text="PARTIDA DE PRESUPUESTO:",
                                                anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                width=50)
        self.rel_budget_label.grid(row=17, column=0, padx=(30, 5), pady=10, sticky="e")
        budget_values = get_all_bd(user, password, "tbl_pres_precios", schema)
        rel_budget_value = []
        for item in budget_values:
            rel_budget_value.append(str(item[1])+" - "+item[4])
        self.rel_budget_option = customtkinter.CTkOptionMenu(self.data_frame,
                                                     dynamic_resizing=False,
                                                     values=rel_budget_value)
        self.rel_budget_option.grid(row=17, column=1, padx=(5, 30), pady=10, sticky="ew", columnspan=2)
        if item_select[18] == '-':
            self.rel_budget_option.set("-")
        else:
            self.rel_budget_option.set(str(item_select[18])+" - "+get_option_item_sub_bd(user, password, "tbl_pres_precios", schema, 'resumen',str(item_select[18]),'codigo')[0])


        # boton de guardar
        save_path = parent_path +"/source/guardar.png"
        self.save_image = customtkinter.CTkImage(Image.open(save_path))
        self.save_button = customtkinter.CTkButton(self, text="Guardar",image=self.save_image, compound="left",fg_color="green",
                                                   font=("default", 14, "bold"),
                                                   command=lambda: self.save(select_data,str(item_select[0])),  height=40)
        self.save_button.grid(row=1, column=0, padx=(30,1), pady=10, sticky= "ew")


        # boton de cancelar
        cancel_path = parent_path +"/source/cancelar.png"
        self.cancel_image = customtkinter.CTkImage(Image.open(cancel_path))
        self.cancel_button = customtkinter.CTkButton(self, text="Cancelar",image=self.cancel_image, compound="left",fg_color="red",
                                                   font=("default", 14, "bold"),
                                                   command=self.cancel,  height=40)
        self.cancel_button.grid(row=1, column=1, padx=(10,30), pady=10, sticky= "ew")

        self.lift()


    def update_type_options(self, select_data):
        select_family = self.family_option.get()
        id_family = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_familia", select_data[2], "familia",
                                   select_family)
        type_values = get_option_item_sub_bd(select_data[0], select_data[1], "tbl_cata_hidra_tipo", select_data[2],
                                             "tipo_elemento", str(id_family), "id_familia")

        self.type_option.configure(values=(type_values if len(type_values) > 0 else "-"))
        self.type_option.set(type_values[0] if len(type_values) > 0 else "-")


    def add_family_data(self,select_data):
        appAux = AppItemAdd(select_data, 'tbl_cata_hidra_familia','familia','Familia')
        appAux.grab_set()
        self.wait_window(appAux)
        family_value = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_familia", select_data[2], 'familia')
        family_value.sort(key=str.lower)
        self.family_option.configure(values=family_value)


    def add_type_data(self,select_data):
        family_option_value = self.family_option.get()
        if isinstance(family_option_value, str):
            family_option_value = [family_option_value]
        id_family = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_familia", select_data[2], "familia",
                                   family_option_value[0])
        appAux = AppItemTypeAdd(select_data, 'tbl_cata_hidra_tipo', 'tipo_elemento', 'Tipo elemento', 'id_familia',
                                id_family)
        appAux.grab_set()
        self.wait_window(appAux)
        self.update_type_options(select_data)


    def add_brand_data(self,select_data):
        appAux = AppItemAdd(select_data, 'tbl_cata_hidra_marcas','marca','Marca')
        appAux.grab_set()
        self.wait_window(appAux)
        brand_value = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_marcas", select_data[2], 'marca')
        brand_value.sort()
        self.brand_option.configure(values=brand_value)


    def add_feature_data(self,select_data):
        appAux = AppItemAdd(select_data, 'tbl_cata_hidra_caracteristica','caracteristica','Caracteristica')
        appAux.grab_set()
        self.wait_window(appAux)
        feature_value = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_caracteristica", select_data[2], 'caracteristica')
        feature_value.sort(key=str.lower)
        self.feature_option.configure(values=feature_value)


    def add_dni_data(self,select_data):
        appAux = AppItemAdd(select_data, 'tbl_cata_hidra_dni','dni','DN inicial(Diametro Nominal)')
        appAux.grab_set()
        self.wait_window(appAux)
        dni_value = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_dni", select_data[2], 'dni')
        dni_value.sort(key=str.lower)
        self.dni_option.configure(values=dni_value)


    def add_dnf_data(self,select_data):
        appAux = AppItemAdd(select_data, 'tbl_cata_hidra_dnf','dnf','DN final (Diametro Nominal)')
        appAux.grab_set()
        self.wait_window(appAux)
        dnf_value = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_dnf", select_data[2], 'dnf')
        dnf_value.sort(key=str.lower)
        self.dnf_option.configure(values=dnf_value)


    def add_pn_data(self,select_data):
        appAux = AppItemAdd(select_data, 'tbl_cata_hidra_pn','pn','PN (Presión nominal')
        appAux.grab_set()
        self.wait_window(appAux)
        pn_value = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_pn", select_data[2], 'pn')
        pn_value.sort(key=str.lower)
        self.pn_option.configure(values=pn_value)


    def add_angle_data(self, select_data):
        appAux = AppItemAdd(select_data, 'tbl_cata_hidra_angulo', 'angulo', 'ÁNGULO')
        appAux.grab_set()
        self.wait_window(appAux)
        angle_value = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_angulo", select_data[2],
                                         'angulo')
        angle_value.sort(key=str.lower)
        self.angle_option.configure(values=angle_value)


    def update_ref_cad_data(self,select_data):
        path_reference = filedialog.askdirectory(title="Selecciona directorio de referencias CAD")
        result = update_reference(select_data[0], select_data[1],  select_data[2], path_reference)
        if result=='ok':
            mssg="Se ha actualizado las referencias en la base de datos."
            show_success(mssg)
            ref_cad_value = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_referencias_cad", select_data[2], 'ruta')
            ref_cad_value.sort(key=str.lower)
            self.ref_cad_option.configure(values=ref_cad_value)

        else:
            mssg="ERROR: "+str(result)
            self.destroy()
            show_error(mssg)

    def save(self, select_data,id_item):
        # Normalizar los valores de las opciones, asegurando que siempre sean listas
        family_option_value = self.family_option.get()
        if isinstance(family_option_value, str):
            family_option_value = [family_option_value]

        type_option_value = self.type_option.get()
        if isinstance(type_option_value, str):
            type_option_value = [type_option_value]

        brand_option_value = self.brand_option.get()
        if isinstance(brand_option_value, str):
            brand_option_value = [brand_option_value]

        feature_option_value = self.feature_option.get()
        if isinstance(feature_option_value, str):
            feature_option_value = [feature_option_value]

        dni_option_value = self.dni_option.get()
        if isinstance(dni_option_value, str):
            dni_option_value = [dni_option_value]

        dnf_option_value = self.dnf_option.get()
        if isinstance(dnf_option_value, str):
            dnf_option_value = [dnf_option_value]

        pn_option_value = self.pn_option.get()
        if isinstance(pn_option_value, str):
            pn_option_value = [pn_option_value]

        angle_option_value = self.angle_option.get()
        if isinstance(angle_option_value, str):
            angle_option_value = [angle_option_value]

        rel_budget_option_value = self.rel_budget_option.get()
        if isinstance(rel_budget_option_value, str):
            rel_budget_option_value = [rel_budget_option_value]

        # conseguimos opciones para guardar en la base de datos
        id_family = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_familia", select_data[2],
                                   "familia", family_option_value[0])

        id_type = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_tipo", select_data[2],
                                 "tipo_elemento", type_option_value[0])

        id_brand = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_marcas", select_data[2],
                                  "marca", brand_option_value[0])

        id_feature = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_caracteristica", select_data[2],
                                    "caracteristica", feature_option_value[0])

        model = self.model_entry.get()
        ref = self.ref_entry.get()

        id_dni = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_dni", select_data[2],
                                "dni", dni_option_value[0])

        id_dnf = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_dnf", select_data[2],
                                "dnf", dnf_option_value[0])

        id_pn = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_pn", select_data[2],
                               "pn", pn_option_value[0])

        id_angle = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_angulo", select_data[2],
                                  "angulo", angle_option_value[0])
        ref_cad = self.ref_cad_option.get()
        description = self.description_entry.get("1.0", "end-1c")
        len_value = self.len_entry.get()
        len_ext_value  = self.len_ext_entry.get()
        h_axis_value  = self.h_axis_entry.get()
        h_total_value  = self.h_total_entry.get()
        weight_value  = self.weight_entry.get()
        cod_budget = rel_budget_option_value[0].split(" - ")[0]

        data=[id_family,id_type,id_brand,id_feature,model,ref,id_dni,id_dnf,id_pn,id_angle,len_value,len_ext_value,h_axis_value,h_total_value,weight_value,ref_cad,description,cod_budget]
        #modifica elementos de la bbdd
        result = mod_catalog_hidro_item(select_data[0], select_data[1],select_data[2], data,str(id_item))



        #mensaje de avisos
        if result == 'ok':
            mssg="Se ha modificado la pieza en la base de datos "
            self.destroy()
            show_success(mssg)
        else:
            mssg="ERROR: "+str(result)
            self.destroy()
            show_error(mssg)


