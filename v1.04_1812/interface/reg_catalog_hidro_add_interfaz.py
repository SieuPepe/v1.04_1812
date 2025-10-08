import customtkinter
from PIL import Image
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox
from script.modulo_db import (get_option_item_bd, update_reference,get_id_item_bd,add_catalog_hidro_item,get_option_item_sub_bd,
                                get_all_bd)
from interface.item_aux_add_interfaz import AppItemAdd
from interface.item_aux_type_add_interfaz import AppItemTypeAdd
import os

# Obtener la ruta actual
current_path = os.path.dirname(os.path.realpath(__file__))

# Subir un nivel en la estructura de carpetas
parent_path = os.path.dirname(current_path)

customtkinter.set_appearance_mode("dark")

class AppCatalogHidroAdd(customtkinter.CTkToplevel):#Toplevel
    width = 800
    height = 700

    def __init__(self, select_data):
        super().__init__()
        password = select_data[1]
        user = select_data[0]
        schema = select_data[2]


        self.title("Añadir pieza del catálogo")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        common_fg_color = "#171717"

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.data_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0)
        self.data_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew",columnspan=2)
        self.data_frame.grid_columnconfigure(0, weight=1)
        self.data_frame.grid_columnconfigure(1, weight=2)
        self.data_frame.grid_columnconfigure(2, weight=1)

        #almacena Familia
        self.family_label = customtkinter.CTkLabel(self.data_frame, text="FAMILIA DE ELEMENTO:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.family_label.grid(row=0, column=0, padx=(30,5), pady=(30,10), sticky= "e")
        family_value = get_option_item_bd(user, password, "tbl_cata_hidra_familia", schema, 'familia')
        family_value.sort(key=str.lower)
        self.family_option = customtkinter.CTkOptionMenu(self.data_frame,
                                                         dynamic_resizing=False,
                                                         values=family_value,
                                                         command=lambda
                                                            event: self.update_type_options(
                                                            select_data))
        self.family_option.grid(row=0, column=1, padx=(5,5), pady=(30,10), sticky= "ew")
        self.family_button = customtkinter.CTkButton(self.data_frame, text="Añadir familia",
                                                             command=lambda:self.add_family_data(select_data), width=50)
        self.family_button.grid(row=0, column=2, padx=(5,30), pady=(30,10), sticky= "ew")


        #almacena tipo
        self.type_label = customtkinter.CTkLabel(self.data_frame, text="TIPO DE ELEMENTO:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.type_label.grid(row=1, column=0, padx=(30,5), pady=10, sticky= "e")
        select_family = self.family_option.get()
        id_family = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_familia", select_data[2], "familia",
                                   select_family)
        type_values = get_option_item_sub_bd(select_data[0], select_data[1], "tbl_cata_hidra_tipo", select_data[2],
                                             "tipo_elemento", str(id_family), "id_familia")
        type_values.sort(key=str.lower)
        self.type_option = customtkinter.CTkOptionMenu(self.data_frame,
                                                         dynamic_resizing=False,
                                                         values=type_values)
        self.type_option.grid(row=1, column=1, padx=(5,5), pady=10, sticky= "ew")
        self.type_option.set(type_values[0] if len(type_values) > 0 else "-" )
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
        self.brand_button = customtkinter.CTkButton(self.data_frame, text="Añadir marca",
                                                             command=lambda:self.add_brand_data(select_data), width=50)
        self.brand_button.grid(row=2, column=2, padx=(5,30), pady=10, sticky= "ew")

        #almacena caracteristica
        self.feature_label = customtkinter.CTkLabel(self.data_frame, text="CARACTERÍSTICA:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.feature_label.grid(row=3, column=0, padx=(30,5), pady=10, sticky= "e")
        feature_value=get_option_item_bd(user, password, "tbl_cata_hidra_caracteristica" , schema, 'caracteristica')
        feature_value.sort(key=str.lower)
        self.feature_option = customtkinter.CTkOptionMenu(self.data_frame,
                                                         dynamic_resizing=False,
                                                         values=feature_value)
        self.feature_option.grid(row=3, column=1, padx=(5,5), pady=10, sticky= "ew")
        self.feature_button = customtkinter.CTkButton(self.data_frame, text="Añadir característica",
                                                             command=lambda:self.add_feature_data(select_data), width=50)
        self.feature_button.grid(row=3, column=2, padx=(5,30), pady=10, sticky= "ew")

        #almacena nombre modelo
        self.model_label = customtkinter.CTkLabel(self.data_frame, text="MODELO:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.model_label.grid(row=4, column=0, padx=(30,5), pady=10, sticky= "e")
        self.model_entry = customtkinter.CTkEntry(self.data_frame, placeholder_text="añada modelo",
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.model_entry.grid(row=4, column=1, padx=(5,30), pady=10, sticky= "ew", columnspan=2)

        #almacena referencia
        self.ref_label = customtkinter.CTkLabel(self.data_frame, text="REFERENCIA:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.ref_label.grid(row=5, column=0, padx=(30,5), pady=10, sticky= "e")
        self.ref_entry = customtkinter.CTkEntry(self.data_frame, placeholder_text="añada referencia modelo",
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.ref_entry.grid(row=5, column=1, padx=(5,30), pady=10, sticky= "ew", columnspan=2)

        #almacena DN inicial
        self.dni_label = customtkinter.CTkLabel(self.data_frame, text="DN inical:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.dni_label.grid(row=6, column=0, padx=(30,5), pady=10, sticky= "e")
        dni_value = get_option_item_bd(user, password, "tbl_cata_hidra_dni", schema, 'dni')
        dni_value.sort(key=str.lower)
        self.dni_option = customtkinter.CTkOptionMenu(self.data_frame,
                                                         dynamic_resizing=False,
                                                         values=dni_value)
        self.dni_option.grid(row=6, column=1, padx=(5,5), pady=10, sticky= "ew")
        self.dni_button = customtkinter.CTkButton(self.data_frame, text="Añadir DNi",
                                                             command=lambda:self.add_dni_data(select_data), width=50)
        self.dni_button.grid(row=6, column=2, padx=(5,30), pady=10, sticky= "ew")

        # almacena DN final
        self.dnf_label = customtkinter.CTkLabel(self.data_frame, text="DN final:",
                                               anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                               width=50)
        self.dnf_label.grid(row=7, column=0, padx=(30, 5), pady=10, sticky="e")
        dnf_value = get_option_item_bd(user, password, "tbl_cata_hidra_dnf", schema, 'dnf')
        dnf_value.sort(key=str.lower)
        self.dnf_option = customtkinter.CTkOptionMenu(self.data_frame,
                                                     dynamic_resizing=False,
                                                     values=dnf_value)
        self.dnf_option.grid(row=7, column=1, padx=(5, 5), pady=10, sticky="ew")
        self.dnf_button = customtkinter.CTkButton(self.data_frame, text="Añadir DNf",
                                                 command=lambda: self.add_dnf_data(select_data), width=50)
        self.dnf_button.grid(row=7, column=2, padx=(5, 30), pady=10, sticky="ew")

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

        #almacena longitud
        self.len_label = customtkinter.CTkLabel(self.data_frame, text="LONGITUD:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.len_label.grid(row=12, column=0, padx=(30,5), pady=10, sticky= "e")
        self.len_entry = customtkinter.CTkEntry(self.data_frame, placeholder_text="añada longitud de la pieza",
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.len_entry.grid(row=12, column=1, padx=(5,30), pady=10, sticky= "ew", columnspan=2)

        #almacena longitud extremos
        self.len_ext_label = customtkinter.CTkLabel(self.data_frame, text="LONGITUD EXTREMOS:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.len_ext_label.grid(row=13, column=0, padx=(30,5), pady=10, sticky= "e")
        self.len_ext_entry = customtkinter.CTkEntry(self.data_frame, placeholder_text="añada longitud extremos de la pieza",
                                                         fg_color=common_fg_color,text_color="#FFFFFF")
        self.len_ext_entry.grid(row=13, column=1, padx=(5,30), pady=10, sticky= "ew", columnspan=2)

        # almacena altura eje de la pieza
        self.h_axis_label = customtkinter.CTkLabel(self.data_frame, text="ALTURA EJE:",
                                                anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                width=50)
        self.h_axis_label.grid(row=14, column=0, padx=(30, 5), pady=10, sticky="e")
        self.h_axis_entry = customtkinter.CTkEntry(self.data_frame, placeholder_text="añada altura eje de la pieza",
                                                fg_color=common_fg_color, text_color="#FFFFFF")
        self.h_axis_entry.grid(row=14, column=1, padx=(5, 30), pady=10, sticky="ew", columnspan=2)

        # altura total de la pieza
        self.h_total_label = customtkinter.CTkLabel(self.data_frame, text="ALTURA TOTAL:",
                                                    anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                    width=50)
        self.h_total_label.grid(row=15, column=0, padx=(30, 5), pady=10, sticky="e")
        self.h_total_entry = customtkinter.CTkEntry(self.data_frame, placeholder_text="añada altura total de la pieza",
                                                    fg_color=common_fg_color, text_color="#FFFFFF")
        self.h_total_entry.grid(row=15, column=1, padx=(5, 30), pady=10, sticky="ew", columnspan=2)

        # almacena lpeso
        self.weight_label = customtkinter.CTkLabel(self.data_frame, text="PESO:",
                                                anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                width=50)
        self.weight_label.grid(row=16, column=0, padx=(30, 5), pady=10, sticky="e")
        self.weight_entry = customtkinter.CTkEntry(self.data_frame, placeholder_text="añada peso de la pieza",
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

        # boton de guardar
        save_path = parent_path +"/source/guardar.png"
        self.save_image = customtkinter.CTkImage(Image.open(save_path))
        self.save_button = customtkinter.CTkButton(self, text="Guardar",image=self.save_image, compound="left",fg_color="green",
                                                   font=("default", 14, "bold"),
                                                   command=lambda: self.save(select_data),  height=40)
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
        appAux = AppItemTypeAdd(select_data, 'tbl_cata_hidra_tipo','tipo_elemento','Tipo elemento','id_familia',id_family)
        appAux.grab_set()
        self.wait_window(appAux)
        self.update_type_options(select_data)


    def add_feature_data(self,select_data):
        appAux = AppItemAdd(select_data, 'tbl_cata_hidra_caracteristica','caracteristica','Caracteristica')
        appAux.grab_set()
        self.wait_window(appAux)
        feature_value = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_caracteristica", select_data[2], 'caracteristica')
        feature_value.sort(key=str.lower)
        self.feature_option.configure(values=feature_value)


    def add_brand_data(self,select_data):
        appAux = AppItemAdd(select_data, 'tbl_cata_hidra_marcas','marca','Marca')
        appAux.grab_set()
        self.wait_window(appAux)
        brand_value = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_marcas", select_data[2], 'marca')
        brand_value.sort(key=str.lower)
        self.brand_option.configure(values=brand_value)


    def add_dni_data(self,select_data):
        appAux = AppItemAdd(select_data, 'tbl_cata_hidra_dni','dni','DN incial (Diametro Nominal)')
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


    def add_angle_data(self,select_data):
        appAux = AppItemAdd(select_data, 'tbl_cata_hidra_angulo','angulo','ÁNGULO')
        appAux.grab_set()
        self.wait_window(appAux)
        angle_value = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_angulo", select_data[2], 'angulo')
        angle_value.sort(key=str.lower)
        self.angle_option.configure(values=angle_value)


    def update_ref_cad_data(self,select_data):
        path_reference = filedialog.askdirectory(title="Selecciona directorio de referencias CAD")
        result = update_reference(select_data[0], select_data[1],  select_data[2], path_reference)
        if result=='ok':
            mssg="Se ha actualizado las referencias en la base de datos."
            CTkMessagebox(title="Successfull Message!", message=mssg,
                          icon="check")
            ref_cad_value = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_referencias_cad", select_data[2], 'ruta')
            ref_cad_value.sort(key=str.lower)
            self.ref_cad_option.configure(values=ref_cad_value)

        else:
            mssg="ERROR: "+str(result)
            self.destroy()
            CTkMessagebox(title="Error Message!", message=mssg,
                          icon="cancel")


    def cancel(self):
        self.destroy()


    def save(self, select_data):
        id_family= get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_familia", select_data[2],
                                        "familia", self.family_option.get())
        id_type= get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_tipo", select_data[2],
                                        "tipo_elemento", self.type_option.get())
        id_brand = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_marcas", select_data[2],
                                         "marca", self.brand_option.get())
        id_feature = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_caracteristica", select_data[2],
                                         "caracteristica", self.feature_option.get())
        model = self.model_entry.get()
        ref = self.ref_entry.get()
        id_dni = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_dni", select_data[2],
                                      "dni", self.dni_option.get())
        id_dnf = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_dnf", select_data[2],
                                      "dnf", self.dnf_option.get())
        id_pn = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_pn", select_data[2],
                                      "pn", self.pn_option.get())
        id_angle = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_angulo", select_data[2],
                               "angulo", self.angle_option.get())
        ref_cad = self.ref_cad_option.get()
        description = self.description_entry.get("1.0", "end-1c")
        len_value = self.len_entry.get()
        len_ext_value  = self.len_ext_entry.get()
        h_axis_value  = self.h_axis_entry.get()
        h_total_value  = self.h_total_entry.get()
        weight_value  = self.weight_entry.get()
        cod_budget = self.rel_budget_option.get().split(" - ")[0]

        data=[id_family,id_type,id_brand,id_feature,model,ref,id_dni,id_dnf,id_pn,id_angle,len_value,len_ext_value,h_axis_value,h_total_value,weight_value,ref_cad,description,cod_budget]
        result = add_catalog_hidro_item(select_data[0], select_data[1],select_data[2], data)

        if result == 'ok':
            mssg="Se ha añadido a la base de datos "
            self.destroy()
            CTkMessagebox(title="Successfull Message!", message=mssg,
                          icon="check")
        else:
            mssg="ERROR: "+str(result)
            self.destroy()
            CTkMessagebox(title="Error Message!", message=mssg,
                          icon="cancel")

