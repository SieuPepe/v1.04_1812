import customtkinter
from PIL import Image
import tkinter as tk
from script.modulo_db  import (get_all_bd, get_filter_data_bd, get_id_item_sub_bd, get_id_item_bd,get_option_item_bd,
                               get_item_id_bd, add_group_budget, add_item_group_budget,mod_amount_group_item, delete_group_item,
                               mod_item_aux)
from interface.item_aux_add_interfaz import AppItemAdd
from interface.amount_interfaz import AppAmountAdd
from interface.base import BaseWindow
from interface.components import show_success, show_warning, show_error, show_info
import os

# Obtener la ruta actual
current_path = os.path.dirname(os.path.realpath(__file__))

# Subir un nivel en la estructura de carpetas
parent_path = os.path.dirname(current_path)


customtkinter.set_appearance_mode("dark")


class AppGroupBudgetAdd(BaseWindow):
    width = 800
    height = 350
    def __init__(self, select_data):
        super().__init__()

        password = select_data[1]
        user = select_data[0]
        schema =select_data[2]

        self.title("Crear grupos de partidas")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        common_fg_color = "#171717"
        
        #genera código de grupo de partidas
        group_data = get_all_bd(user, password, "tbl_pres_grupo_partidas", schema)
        if len(group_data)!=0:
            id_last = max(sublist[0] for sublist in group_data)
            self.id_next = id_last + 1
            code = f"PA000{self.id_next}"
            code_value = tk.StringVar(value=code)
        else:
            code_value = tk.StringVar(value="PA0001")
        self.code_label = customtkinter.CTkLabel(self, text="CÓDIGO GRUPO DE PARTIDAS:",
                                                 anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                 width=50)
        self.code_label.grid(row=0, column=0, padx=(30, 5), pady=10, sticky="e")
        self.code_entry = customtkinter.CTkEntry(self, textvariable=code_value,
                                                 fg_color=common_fg_color, text_color="#FFFFFF", state='disable')
        self.code_entry.grid(row=0, column=1, padx=(5, 30), pady=10, sticky="ew", columnspan=2)

        # almacena código partida
        self.resume_label = customtkinter.CTkLabel(self, text="NOMBRE GRUPO DE PARTIDAS:",
                                                 anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                 width=50)
        self.resume_label.grid(row=1, column=0, padx=(30, 5), pady=10, sticky="e")
        self.resume_entry = customtkinter.CTkEntry(self,  placeholder_text="añada nombre del grupo de partidas",
                                                 fg_color=common_fg_color, text_color="#FFFFFF")
        self.resume_entry.grid(row=1, column=1, padx=(5, 30), pady=10, sticky="ew", columnspan=2)

        #almacena descripción
        self.description_label = customtkinter.CTkLabel(self, text="DESCRIPCIÓN:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.description_label.grid(row=2, column=0, padx=(30,5), pady=(10,10), sticky= "e")
        self.description_entry = customtkinter.CTkTextbox(self, fg_color=common_fg_color, height= 50,
                                                        border_width=2, border_color="#565B5E",text_color="#FFFFFF")
        self.description_entry.grid(row=2, column=1, padx=(5,30), pady=(10,10), sticky= "ew", columnspan=2)

        # almacena la naturaleza
        self.type_label = customtkinter.CTkLabel(self, text="NATURALEZA:",
                                                 anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                 width=50)
        self.type_label.grid(row=3, column=0, padx=(30, 5), pady=10, sticky="e")
        type_value = get_option_item_bd(select_data[0], select_data[1], "tbl_pres_naturaleza", select_data[2], 'tipo')
        type_value.sort(key=str.lower)
        self.type_option = customtkinter.CTkOptionMenu(self,
                                                       dynamic_resizing=False,
                                                       values=type_value)
        self.type_option.grid(row=3, column=1, padx=(5, 5), pady=10, sticky="ew")
        self.type_button = customtkinter.CTkButton(self, text="Añada nueva naturaleza",
                                                   command=lambda: self.add_type_data(select_data), width=50)
        self.type_button.grid(row=3, column=2, padx=(5, 30), pady=10, sticky="ew")

        # almacena las unidades
        self.ud_label = customtkinter.CTkLabel(self, text="UNIDADES:",
                                               anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                               width=50)
        self.ud_label.grid(row=4, column=0, padx=(30, 5), pady=10, sticky="e")
        ud_value = get_option_item_bd(select_data[0], select_data[1], "tbl_pres_unidades", select_data[2], 'unidad')
        ud_value.sort(key=str.lower)
        self.ud_option = customtkinter.CTkOptionMenu(self,
                                                     dynamic_resizing=False,
                                                     values=ud_value)
        self.ud_option.grid(row=4, column=1, padx=(5, 5), pady=10, sticky="ew")
        self.ud_button = customtkinter.CTkButton(self, text="Añada nueva unidad",
                                                 command=lambda: self.add_ud_data(select_data), width=50)
        self.ud_button.grid(row=4, column=2, padx=(5, 30), pady=10, sticky="ew")

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_BOTONES_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        # boton de guardar
        save_path = parent_path +"/resources/images/guardar.png"
        self.save_image = customtkinter.CTkImage(Image.open(save_path))
        self.save_button = customtkinter.CTkButton(self, text="Guardar",image=self.save_image, compound="left",fg_color="green",
                                                   font=("default", 14, "bold"),
                                                   command=lambda: self.save(select_data),  height=40)
        self.save_button.grid(row=8, column=1, padx=(30,1), pady=10, sticky= "ew")

        # boton de cancelar
        cancel_path = parent_path +"/resources/images/cancelar.png"
        self.cancel_image = customtkinter.CTkImage(Image.open(cancel_path))
        self.cancel_button = customtkinter.CTkButton(self, text="Cancelar",image=self.cancel_image, compound="left",fg_color="red",
                                                   font=("default", 14, "bold"),
                                                   command=self.cancel,  height=40)
        self.cancel_button.grid(row=8, column=2, padx=(10,30), pady=10, sticky= "ew")

        self.lift()


    def add_ud_data(self,select_data):
        appAux = AppItemAdd(select_data, 'tbl_pres_unidades', 'unidad', 'Unidades')
        appAux.grab_set()
        self.wait_window(appAux)
        type_value = get_option_item_bd(select_data[0], select_data[1], 'tbl_pres_unidades', select_data[2],
                                         'unidad')
        type_value.sort(key=str.lower)
        self.type_option.configure(values=type_value)


    def add_type_data(self,select_data):
        appAux = AppItemAdd(select_data, 'tbl_pres_naturaleza', 'tipo', 'Naturaleza')
        appAux.grab_set()
        self.wait_window(appAux)
        type_value = get_option_item_bd(select_data[0], select_data[1], 'tbl_pres_naturaleza', select_data[2],
                                         'tipo')
        type_value.sort(key=str.lower)
        self.type_option.configure(values=type_value)


    def save(self, select_data):
        # recogida de datos de la interfaz
        code = self.code_entry.get()
        id_type = get_id_item_bd(select_data[0], select_data[1], 'tbl_pres_naturaleza', select_data[2],
                                 'tipo', self.type_option.get())
        id_ud = get_id_item_bd(select_data[0], select_data[1], 'tbl_pres_unidades', select_data[2],
                                  'unidad', self.ud_option.get())
        resume = self.resume_entry.get()
        description = self.description_entry.get("1.0", "end-1c")
        id_chapter = get_id_item_bd(select_data[0], select_data[1], 'tbl_pres_capitulos', select_data[2],
                                  'codigo_capitulo', 'PA000')

        data = [code, id_type, id_ud, resume, description,id_chapter]

        # modifica elementos de la bbdd
        result = add_group_budget(select_data[0], select_data[1], select_data[2], data)
        # mensaje de avisos
        if result == 'ok':
            self.withdraw()
            # desplegamos la ventana para recoger los elemntos añadidos a la partida
            appAux2 = AppItemGroupBudgetAdd(select_data,code)
            appAux2.grab_set()
            self.wait_window(appAux2)
            self.destroy()

        else:
            mssg = "ERROR: " + str(result)
            self.destroy()
            show_error(mssg)


class AppItemGroupBudgetAdd(BaseWindow):
    width = 950
    height = 600

    def __init__(self, select_data, code_group):
        super().__init__()

        password = select_data[1]
        user = select_data[0]
        schema = select_data[2]

        self.title("Añadir partidas a grupo")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(2, weight=1)

        common_fg_color = "#171717"

        self.code_label = customtkinter.CTkLabel(self, text="CÓDIGO GRUPO DE PARTIDAS:",
                                                 anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                 width=50)
        self.code_label.grid(row=0, column=0, padx=(30, 5), pady=10, sticky="e")
        code_value = tk.StringVar(value=code_group)
        self.code_entry = customtkinter.CTkEntry(self, textvariable=code_value,
                                                 fg_color=common_fg_color, text_color="#FFFFFF", state='disable')
        self.code_entry.grid(row=0, column=1, padx=(5, 30), pady=10, sticky="ew", columnspan=2)

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_FRAME FILTROS_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.filter_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.filter_frame.grid(row=1, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=3)
        self.filter_frame.grid_columnconfigure(0, weight=1)
        self.filter_frame.grid_columnconfigure(1, weight=1)

        # capítulo
        self.chapter_budget_label = customtkinter.CTkLabel(self.filter_frame, text="Capítulo",
                                                           anchor="center",
                                                           font=customtkinter.CTkFont(size=13, weight="bold"))
        self.chapter_budget_label.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="nwes")
        chapter_budget_items = get_all_bd(user, password, "tbl_pres_capitulos", schema)
        chapter_values = []
        for item in chapter_budget_items:
            code = item[1]
            name = item[3]
            chapter_values.append(str(code) + " - " + name)
        chapter_values.remove("PA000 - PARTIDAS TIPO")
        self.chapter_budget_option = customtkinter.CTkOptionMenu(self.filter_frame,
                                                                 dynamic_resizing=False,
                                                                 values=chapter_values,
                                                                 command=lambda event: self.update_budget_option(
                                                                     select_data))
        self.chapter_budget_option.grid(row=1, column=0, padx=(10, 5), pady=10, sticky="ew")

        # partida de presupuesto
        self.item_budget_label = customtkinter.CTkLabel(self.filter_frame, text="Partidas",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=13, weight="bold"))
        self.item_budget_label.grid(row=0, column=1, padx=(10, 5), pady=5, sticky="nwes")
        chapter_select = self.chapter_budget_option.get()
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
        self.item_budget_option = customtkinter.CTkOptionMenu(self.filter_frame,
                                                              dynamic_resizing=False,
                                                              values=item_values)
        self.item_budget_option.grid(row=1, column=1, padx=(5, 15), pady=10, sticky="ew")

        self.chapter_budget_option.bind("<<ComboboxSelected>>", lambda event: self.update_budget_option(select_data))

        # botón para añadir partida
        self.add_button = customtkinter.CTkButton(self.filter_frame, text="Añadir partida a grupo",
                                                  command=lambda: self.add_item(select_data,
                                                                                self.item_budget_option.get()),
                                                  width=50)
        self.add_button.grid(row=2, column=1, padx=(5, 10), pady=10, sticky="ew")

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_FRAME DATA_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.data_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0)
        self.data_frame.grid(row=2, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=3)
        self.data_frame.grid_columnconfigure(2, weight=5)

        # Encabezados
        self.code_budget_label = customtkinter.CTkLabel(self.data_frame, text="Codigo",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=13, weight="bold"))
        self.code_budget_label.grid(row=0, column=0, padx=5, pady=5, sticky="nwes")

        self.ud_budget_label = customtkinter.CTkLabel(self.data_frame, text="Ud",
                                                      anchor="center",
                                                      font=customtkinter.CTkFont(size=13, weight="bold"))
        self.ud_budget_label.grid(row=0, column=1, padx=5, pady=5, sticky="nwes")

        self.resume_budget_label = customtkinter.CTkLabel(self.data_frame, text="Resumen",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13, weight="bold"))
        self.resume_budget_label.grid(row=0, column=2, padx=5, pady=5, sticky="nwes")

        self.amount_budget_label = customtkinter.CTkLabel(self.data_frame, text="Cantidad",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13, weight="bold"))
        self.amount_budget_label.grid(row=0, column=4, padx=5, pady=5, sticky="nwes")

        self.price_budget_label = customtkinter.CTkLabel(self.data_frame, text="Precio",
                                                         anchor="center",
                                                         font=customtkinter.CTkFont(size=13, weight="bold"))
        self.price_budget_label.grid(row=0, column=6, padx=5, pady=5, sticky="nwes")

        self.cost_budget_label = customtkinter.CTkLabel(self.data_frame, text="Coste",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=13, weight="bold"))
        self.cost_budget_label.grid(row=0, column=7, padx=5, pady=5, sticky="nwes")

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_BOTONES_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        # boton de guardar
        self.save_button = customtkinter.CTkButton(self, text="Ok", compound="left",
                                                   fg_color="green",
                                                   font=("default", 14, "bold"),
                                                   command=lambda :self.save(select_data), height=40)
        self.save_button.grid(row=3, column=1, padx=(30, 1), pady=10, sticky="ew")

        # boton de cancelar
        cancel_path = parent_path +"/resources/images/cancelar.png"
        self.cancel_image = customtkinter.CTkImage(Image.open(cancel_path))
        self.cancel_button = customtkinter.CTkButton(self, text="Cancelar", image=self.cancel_image, compound="left",
                                                     fg_color="red",
                                                     font=("default", 14, "bold"),
                                                     command=self.cancel, height=40)
        self.cancel_button.grid(row=3, column=2, padx=(10, 30), pady=10, sticky="ew")

        self.lift()


    def update_budget_option (self, select_data):
        chapter_select = self.chapter_budget_option.get()
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


    def add_item(self, select_data, item_select):
        data = []

        #ventana para añadir la cantidad
        code_item_select = item_select.split(" - ")[0]
        id_item_select = get_id_item_bd(select_data[0], select_data[1], "tbl_pres_precios", select_data[2],
                                        "codigo",
                                        str(code_item_select))
        id_ud_item = get_item_id_bd(select_data[0], select_data[1], "tbl_pres_precios", select_data[2],  "id_unidades", id_item_select)
        ud_item = get_item_id_bd(select_data[0], select_data[1], "tbl_pres_unidades", select_data[2], "unidad",id_ud_item)
        group_select=self.code_entry.get()
        id_group_select = get_id_item_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2],
                                        "codigo",
                                        str(group_select))

        appAux1 = AppAmountAdd(item_select, ud_item)
        appAux1.grab_set()
        self.wait_window(appAux1)
        amount_value = appAux1.get_items()
        if isinstance(amount_value, str):
            amount = amount_value.replace(",", ".")
        else:
            amount = amount_value

        # añadimos el registro a la base de datos
        data.append(id_group_select)
        data.append(id_item_select)
        data.append(amount)
        add_item_group_budget(select_data[0], select_data[1], select_data[2], data)

        # actualizamos los datos agregados
        self.data_frame.destroy()
        self.data_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0)
        self.data_frame.grid(row=2, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=3)
        self.data_frame.grid_columnconfigure(2, weight=5)
        items_group =get_filter_data_bd(select_data[0], select_data[1],"tbl_pres_grupo_elementos",select_data[2],"id_grupo",str(id_group_select))
        self.update_data_frame(select_data, items_group)
        
    
    def update_data_frame (self, select_data, items_group):
        # cargar imagen de icono
        image_info_path = parent_path +"/resources/images/info.png"
        self.info_image = customtkinter.CTkImage(Image.open(image_info_path), size=(20,20))
        image_update_path = parent_path +"/resources/images/actualizar.png"
        self.update_image = customtkinter.CTkImage(Image.open(image_update_path), size=(20,20))
        image_delete_path = parent_path +"/resources/images/papelera.png"
        self.delete_image = customtkinter.CTkImage(Image.open(image_delete_path), size=(20,20))

        # Listas para almacenar las variables por fila
        self.id_bd_items = []
        self.amount_items = []
        self.price_items = []
        self.cost_items = []

        #Encabezdos
        self.code_label = customtkinter.CTkLabel(self.data_frame, text="Codigo",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=13, weight="bold"))
        self.code_label.grid(row=0, column=0, padx=5, pady=5, sticky="nwes")

        self.ud_label = customtkinter.CTkLabel(self.data_frame, text="Ud",
                                                      anchor="center",
                                                      font=customtkinter.CTkFont(size=13, weight="bold"))
        self.ud_label.grid(row=0, column=1, padx=5, pady=5, sticky="nwes")

        self.resume_label = customtkinter.CTkLabel(self.data_frame, text="Resumen",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13, weight="bold"))
        self.resume_label.grid(row=0, column=2, padx=5, pady=5, sticky="nwes")

        self.amount_label = customtkinter.CTkLabel(self.data_frame, text="Cantidad",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13, weight="bold"))
        self.amount_label.grid(row=0, column=4, padx=5, pady=5, sticky="nwes")

        self.price_label = customtkinter.CTkLabel(self.data_frame, text="Precio",
                                                         anchor="center",
                                                         font=customtkinter.CTkFont(size=13, weight="bold"))
        self.price_label.grid(row=0, column=6, padx=5, pady=5, sticky="nwes")

        self.cost_label = customtkinter.CTkLabel(self.data_frame, text="Coste",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=13, weight="bold"))
        self.cost_label.grid(row=0, column=7, padx=5, pady=5, sticky="nwes")

        #contenido de la tabla
        for i,item in enumerate(items_group):
            i+=1
            id_bd = item[0]
            self.id_bd_items.append(id_bd)
            id_item = item[2]
            data_item = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_precios", select_data[2], "id", str(id_item))[0]
            self.code_item= customtkinter.CTkLabel(self.data_frame, text=data_item[1],
                                                            anchor="center")
            self.code_item.grid(row=i, column=0, padx=5, pady=5, sticky="nwes")

            ud_value=get_item_id_bd(select_data[0], select_data[1], "tbl_pres_unidades", select_data[2],"unidad",str(data_item[3]))
            self.ud_item= customtkinter.CTkLabel(self.data_frame, text=ud_value,
                                                            anchor="center")
            self.ud_item.grid(row=i, column=1, padx=5, pady=5, sticky="nwes")

            self.resume_item= customtkinter.CTkLabel(self.data_frame, text=data_item[4],
                                                            anchor="center")
            self.resume_item.grid(row=i, column=2, padx=5, pady=5, sticky="nwes")

            self.description_button= customtkinter.CTkButton(self.data_frame, image=self.info_image, text="",
                                                                    command=lambda: self.info_event(data_item[5]),width=30)
            self.description_button.grid(row=i, column=3, padx=5, pady=5, sticky="nwes")

            amount_value = tk.StringVar(value=f"{str(item[3])}")
            self.amount_items.append(amount_value)
            self.amount_entry = customtkinter.CTkEntry(self.data_frame, textvariable=amount_value, text_color="#FFFFFF")
            self.amount_entry.grid(row=i, column=4, padx=5, pady=5, sticky="nwes")

            self.update_button= customtkinter.CTkButton(self.data_frame, image=self.update_image, text="",
                                                                    command=lambda i=i: self.update_event(i,select_data),width=30)
            self.update_button.grid(row=i, column=5, padx=5, pady=5, sticky="nwes")

            price_value = round(float(data_item[6]), 2)
            self.price_items.append(price_value)
            self.price_item = customtkinter.CTkLabel(self.data_frame, text=f"{price_value} €", anchor="center")
            self.price_item.grid(row=i, column=6, padx=5, pady=5, sticky="nwes")

            cost_value=round(price_value * float(amount_value.get() or 0), 2)
            cost_value= tk.StringVar(value=f"{cost_value} €")
            self.cost_items.append(cost_value.get())
            self.cost_item = customtkinter.CTkLabel(self.data_frame, textvariable=cost_value, anchor="center")
            self.cost_item.grid(row=i, column=7, padx=5, pady=5, sticky="nwes")

            self.delete_button= customtkinter.CTkButton(self.data_frame, image=self.delete_image, text="",
                                                                    command=lambda i=i: self.delete_event(i,select_data),width=30)
            self.delete_button.grid(row=i, column=8, padx=5, pady=5, sticky="nwes")


    def info_event(self, info):
        show_info(info)


    def update_event(self, i,select_data):
        value = self.amount_items[i - 1].get()
        if  isinstance(value,str):
            amount=value.replace(",",".")
            amount = float(amount) if amount else 0
        else:
            amount = float(self.amount_items[i - 1].get()) if self.amount_items[i - 1].get() else 0
        id_bd = self.id_bd_items[i - 1]
        # Obtener el valor actual del amount_entry y el precio por ítem en la fila 'i'
        mod_amount_group_item(select_data[0], select_data[1], select_data[2], amount, str(id_bd))

        # actualizamos los datos agregados
        self.data_frame.destroy()
        self.data_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0)
        self.data_frame.grid(row=2, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=3)
        self.data_frame.grid_columnconfigure(2, weight=5)
        group_select=self.code_entry.get()
        id_group_select = get_id_item_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2],
                                        "codigo",
                                        str(group_select))
        items_group = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_grupo_elementos", select_data[2],
                                         "id_grupo", str(id_group_select))
        self.update_data_frame(select_data, items_group)


    def delete_event(self, i, select_data):
        id_bd = self.id_bd_items[i - 1]
        # borrar el item de la base de datos
        result=delete_group_item(select_data[0], select_data[1], select_data[2], str(id_bd))

        # actualizamos los datos agregados
        self.data_frame.destroy()
        self.data_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0)
        self.data_frame.grid(row=2, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=3)
        self.data_frame.grid_columnconfigure(2, weight=5)
        group_select=self.code_entry.get()
        id_group_select = get_id_item_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2],
                                        "codigo",
                                        str(group_select))
        items_group = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_grupo_elementos", select_data[2],
                                         "id_grupo", str(id_group_select))
        self.update_data_frame(select_data, items_group)

        if result =="ok":
            show_success("Se ha eliminado el item de la base de datos")

        else:
            show_warning(f"Error: {result}")

    def save(self,select_data):
        #Actualizamos el coste con el sumatorio del coste de todas las partidas
        group_select = self.code_entry.get()
        id_group_select = get_id_item_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2],
                                         "codigo",
                                         str(group_select))
        cost_group=0
        for item in self.cost_items:
            cost=float(item.replace(" €",""))
            cost_group+=cost
        result=mod_item_aux(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2],"coste",cost_group, id_group_select)

        self.destroy()

        if result =="ok":
            show_success("Se ha añadido el grupo a la base de datos")
        else:
            show_warning(f"Error: {result}")


class AppItemGroupBudgetMod(BaseWindow):
    width = 950
    height = 600

    def __init__(self, select_data, code_group):
        super().__init__()

        password = select_data[1]
        user = select_data[0]
        schema = select_data[2]

        self.title("Modificar partidas a grupo")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(2, weight=1)

        common_fg_color = "#171717"

        self.code_label = customtkinter.CTkLabel(self, text="CÓDIGO GRUPO DE PARTIDAS:",
                                                 anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                 width=50)
        self.code_label.grid(row=0, column=0, padx=(30, 5), pady=10, sticky="e")
        code_value = tk.StringVar(value=code_group)
        self.code_entry = customtkinter.CTkEntry(self, textvariable=code_value,
                                                 fg_color=common_fg_color, text_color="#FFFFFF", state='disable')
        self.code_entry.grid(row=0, column=1, padx=(5, 30), pady=10, sticky="ew", columnspan=2)

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_FRAME FILTROS_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.filter_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.filter_frame.grid(row=1, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=3)
        self.filter_frame.grid_columnconfigure(0, weight=1)
        self.filter_frame.grid_columnconfigure(1, weight=1)

        # capítulo
        self.chapter_budget_label = customtkinter.CTkLabel(self.filter_frame, text="Capítulo",
                                                           anchor="center",
                                                           font=customtkinter.CTkFont(size=13, weight="bold"))
        self.chapter_budget_label.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="nwes")
        chapter_budget_items = get_all_bd(user, password, "tbl_pres_capitulos", schema)
        chapter_values = []
        for item in chapter_budget_items:
            code = item[1]
            name = item[3]
            chapter_values.append(str(code) + " - " + name)
        chapter_values.remove("PA000 - PARTIDAS TIPO")
        self.chapter_budget_option = customtkinter.CTkOptionMenu(self.filter_frame,
                                                                 dynamic_resizing=False,
                                                                 values=chapter_values,
                                                                 command=lambda event: self.update_budget_option(
                                                                     select_data))
        self.chapter_budget_option.grid(row=1, column=0, padx=(10, 5), pady=10, sticky="ew")

        # partida de presupuesto
        self.item_budget_label = customtkinter.CTkLabel(self.filter_frame, text="Partidas",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=13, weight="bold"))
        self.item_budget_label.grid(row=0, column=1, padx=(10, 5), pady=5, sticky="nwes")
        chapter_select = self.chapter_budget_option.get()
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
        self.item_budget_option = customtkinter.CTkOptionMenu(self.filter_frame,
                                                              dynamic_resizing=False,
                                                              values=item_values)
        self.item_budget_option.grid(row=1, column=1, padx=(5, 15), pady=10, sticky="ew")

        self.chapter_budget_option.bind("<<ComboboxSelected>>", lambda event: self.update_budget_option(select_data))

        # botón para filtrar
        self.add_button = customtkinter.CTkButton(self.filter_frame, text="Añadir partida a grupo",
                                                  command=lambda: self.add_item(select_data,
                                                                                self.item_budget_option.get()),
                                                  width=50)
        self.add_button.grid(row=2, column=1, padx=(5, 10), pady=10, sticky="ew")

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_FRAME DATa_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.data_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0)
        self.data_frame.grid(row=2, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=3)
        self.data_frame.grid_columnconfigure(2, weight=5)
        item_group=[]
        id_group_select = get_id_item_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2],
                                         "codigo",
                                         str(code_group))
        items_group =get_filter_data_bd(select_data[0], select_data[1],"tbl_pres_grupo_elementos",select_data[2],"id_grupo",str(id_group_select))
        if len(items_group)==0:
            # Encabezdos
            self.code_budget_label = customtkinter.CTkLabel(self.data_frame, text="Codigo",
                                                            anchor="center",
                                                            font=customtkinter.CTkFont(size=13, weight="bold"))
            self.code_budget_label.grid(row=0, column=0, padx=5, pady=5, sticky="nwes")

            self.ud_budget_label = customtkinter.CTkLabel(self.data_frame, text="Ud",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13, weight="bold"))
            self.ud_budget_label.grid(row=0, column=1, padx=5, pady=5, sticky="nwes")

            self.resume_budget_label = customtkinter.CTkLabel(self.data_frame, text="Resumen",
                                                              anchor="center",
                                                              font=customtkinter.CTkFont(size=13, weight="bold"))
            self.resume_budget_label.grid(row=0, column=2, padx=5, pady=5, sticky="nwes")

            self.amount_budget_label = customtkinter.CTkLabel(self.data_frame, text="Cantidad",
                                                              anchor="center",
                                                              font=customtkinter.CTkFont(size=13, weight="bold"))
            self.amount_budget_label.grid(row=0, column=4, padx=5, pady=5, sticky="nwes")

            self.price_budget_label = customtkinter.CTkLabel(self.data_frame, text="Precio",
                                                             anchor="center",
                                                             font=customtkinter.CTkFont(size=13, weight="bold"))
            self.price_budget_label.grid(row=0, column=6, padx=5, pady=5, sticky="nwes")

            self.cost_budget_label = customtkinter.CTkLabel(self.data_frame, text="Coste",
                                                            anchor="center",
                                                            font=customtkinter.CTkFont(size=13, weight="bold"))
            self.cost_budget_label.grid(row=0, column=7, padx=5, pady=5, sticky="nwes")

        else:
            self.update_data_frame( select_data, items_group)

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_BOTONES_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        # boton de guardar
        self.save_button = customtkinter.CTkButton(self, text="Ok", compound="left",
                                                   fg_color="green",
                                                   font=("default", 14, "bold"),
                                                   command=lambda: self.save(select_data), height=40)
        self.save_button.grid(row=3, column=1, padx=(30, 1), pady=10, sticky="ew")

        # boton de cancelar
        cancel_path = parent_path +"/resources/images/cancelar.png"
        self.cancel_image = customtkinter.CTkImage(Image.open(cancel_path))
        self.cancel_button = customtkinter.CTkButton(self, text="Cancelar", image=self.cancel_image, compound="left",
                                                     fg_color="red",
                                                     font=("default", 14, "bold"),
                                                     command=self.cancel, height=40)
        self.cancel_button.grid(row=3, column=2, padx=(10, 30), pady=10, sticky="ew")

        self.lift()

    def update_budget_option(self, select_data):
        chapter_select = self.chapter_budget_option.get()
        code_chapter_select = chapter_select.split(" - ")[0]
        name_chapter_select = chapter_select.split(" - ")[1]
        id_chapter_select = get_id_item_sub_bd(select_data[0], select_data[1], "tbl_pres_capitulos", select_data[2],
                                               "codigo_capitulo",
                                               code_chapter_select, "capitulo", name_chapter_select)
        item_budget_values = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_precios", select_data[2],
                                                "id_capitulo",
                                                str(id_chapter_select))
        item_values = []
        for item in item_budget_values:
            code = item[1]
            name = item[4]
            item_values.append(str(code) + " - " + name)
        self.item_budget_option.configure(values=item_values)
        self.item_budget_option.set(item_values[0])


    def add_item(self, select_data, item_select):
        data = []
        code_item_select = item_select.split(" - ")[0]
        id_item_select = get_id_item_bd(select_data[0], select_data[1], "tbl_pres_precios", select_data[2],
                                        "codigo",
                                        str(code_item_select))
        id_ud_item = get_item_id_bd(select_data[0], select_data[1], "tbl_pres_precios", select_data[2], "id_unidades",
                                    id_item_select)
        ud_item = get_item_id_bd(select_data[0], select_data[1], "tbl_pres_unidades", select_data[2], "unidad",
                                 id_ud_item)

        group_select = self.code_entry.get()
        id_group_select = get_id_item_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2],
                                         "codigo",
                                         str(group_select))

        appAux1 = AppAmountAdd(item_select, ud_item)
        appAux1.grab_set()
        self.wait_window(appAux1)
        amount_value = appAux1.get_items()
        if isinstance(amount_value, str):
            amount = amount_value.replace(",", ".")
        else:
            amount = amount_value

        data.append(id_group_select)
        data.append(id_item_select)
        data.append(amount)
        # añadimos el registro a la base de datos
        add_item_group_budget(select_data[0], select_data[1], select_data[2], data)

        # actualizamos los datos agregados
        self.data_frame.destroy()
        self.data_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0)
        self.data_frame.grid(row=2, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=3)
        self.data_frame.grid_columnconfigure(2, weight=5)
        items_group = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_grupo_elementos", select_data[2],
                                         "id_grupo", str(id_group_select))
        self.update_data_frame(select_data, items_group)


    def update_data_frame(self, select_data, items_group):
        # cargar imagen de icono
        image_info_path = parent_path +"/resources/images/info.png"
        self.info_image = customtkinter.CTkImage(Image.open(image_info_path), size=(20, 20))
        image_update_path = parent_path +"/resources/images/actualizar.png"
        self.update_image = customtkinter.CTkImage(Image.open(image_update_path), size=(20, 20))
        image_delete_path = parent_path +"/resources/images/papelera.png"
        self.delete_image = customtkinter.CTkImage(Image.open(image_delete_path), size=(20, 20))

        # Listas para almacenar las variables por fila
        self.id_bd_items = []
        self.amount_items = []
        self.price_items = []
        self.cost_items = []

        # Encabezdos
        self.code_label = customtkinter.CTkLabel(self.data_frame, text="Codigo",
                                                 anchor="center",
                                                 font=customtkinter.CTkFont(size=13, weight="bold"))
        self.code_label.grid(row=0, column=0, padx=5, pady=5, sticky="nwes")

        self.ud_label = customtkinter.CTkLabel(self.data_frame, text="Ud",
                                               anchor="center",
                                               font=customtkinter.CTkFont(size=13, weight="bold"))
        self.ud_label.grid(row=0, column=1, padx=5, pady=5, sticky="nwes")

        self.resume_label = customtkinter.CTkLabel(self.data_frame, text="Resumen",
                                                   anchor="center",
                                                   font=customtkinter.CTkFont(size=13, weight="bold"))
        self.resume_label.grid(row=0, column=2, padx=5, pady=5, sticky="nwes")

        self.amount_label = customtkinter.CTkLabel(self.data_frame, text="Cantidad",
                                                   anchor="center",
                                                   font=customtkinter.CTkFont(size=13, weight="bold"))
        self.amount_label.grid(row=0, column=4, padx=5, pady=5, sticky="nwes")

        self.price_label = customtkinter.CTkLabel(self.data_frame, text="Precio",
                                                  anchor="center",
                                                  font=customtkinter.CTkFont(size=13, weight="bold"))
        self.price_label.grid(row=0, column=6, padx=5, pady=5, sticky="nwes")

        self.cost_label = customtkinter.CTkLabel(self.data_frame, text="Coste",
                                                 anchor="center",
                                                 font=customtkinter.CTkFont(size=13, weight="bold"))
        self.cost_label.grid(row=0, column=7, padx=5, pady=5, sticky="nwes")

        # contenido de la tabla
        for i, item in enumerate(items_group):
            i += 1
            id_bd = item[0]
            self.id_bd_items.append(id_bd)
            id_item = item[2]
            data_item = \
            get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_precios", select_data[2], "id", str(id_item))[
                0]
            self.code_item = customtkinter.CTkLabel(self.data_frame, text=data_item[1],
                                                    anchor="center")
            self.code_item.grid(row=i, column=0, padx=5, pady=5, sticky="nwes")

            ud_value = get_item_id_bd(select_data[0], select_data[1], "tbl_pres_unidades", select_data[2], "unidad",
                                      str(data_item[3]))
            self.ud_item = customtkinter.CTkLabel(self.data_frame, text=ud_value,
                                                  anchor="center")
            self.ud_item.grid(row=i, column=1, padx=5, pady=5, sticky="nwes")

            self.resume_item = customtkinter.CTkLabel(self.data_frame, text=data_item[4],
                                                      anchor="center")
            self.resume_item.grid(row=i, column=2, padx=5, pady=5, sticky="nwes")

            self.description_button = customtkinter.CTkButton(self.data_frame, image=self.info_image, text="",
                                                              command=lambda: self.info_event(data_item[5]), width=30)
            self.description_button.grid(row=i, column=3, padx=5, pady=5, sticky="nwes")

            amount_value = tk.StringVar(value=f"{str(item[3])}")
            self.amount_items.append(amount_value)
            self.amount_entry = customtkinter.CTkEntry(self.data_frame, textvariable=amount_value, text_color="#FFFFFF")
            self.amount_entry.grid(row=i, column=4, padx=5, pady=5, sticky="nwes")

            self.update_button = customtkinter.CTkButton(self.data_frame, image=self.update_image, text="",
                                                         command=lambda i=i: self.update_event(i, select_data),
                                                         width=30)
            self.update_button.grid(row=i, column=5, padx=5, pady=5, sticky="nwes")

            price_value = round(float(data_item[6]), 2)
            self.price_items.append(price_value)
            self.price_item = customtkinter.CTkLabel(self.data_frame, text=f"{price_value} €", anchor="center")
            self.price_item.grid(row=i, column=6, padx=5, pady=5, sticky="nwes")

            cost_value = round(price_value * float(amount_value.get() or 0), 2)
            cost_value = tk.StringVar(value=f"{cost_value} €")
            self.cost_items.append(cost_value.get())
            self.cost_item = customtkinter.CTkLabel(self.data_frame, textvariable=cost_value, anchor="center")
            self.cost_item.grid(row=i, column=7, padx=5, pady=5, sticky="nwes")

            self.delete_button = customtkinter.CTkButton(self.data_frame, image=self.delete_image, text="",
                                                         command=lambda i=i: self.delete_event(i, select_data),
                                                         width=30)
            self.delete_button.grid(row=i, column=8, padx=5, pady=5, sticky="nwes")


    def info_event(self, info):
        show_info(info)


    def update_event(self, i, select_data):
        value = self.amount_items[i - 1].get()
        if isinstance(value, str):
            amount = value.replace(",", ".")
            amount = float(amount) if amount else 0
        else:
            amount = float(self.amount_items[i - 1].get()) if self.amount_items[i - 1].get() else 0
        id_bd = self.id_bd_items[i - 1]
        # Obtener el valor actual del amount_entry y el precio por ítem en la fila 'i'
        mod_amount_group_item(select_data[0], select_data[1], select_data[2], amount, str(id_bd))

        # actualizamos los datos agregados
        self.data_frame.destroy()
        self.data_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0)
        self.data_frame.grid(row=2, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=3)
        self.data_frame.grid_columnconfigure(2, weight=5)
        group_select = self.code_entry.get()
        id_group_select = get_id_item_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2],
                                         "codigo",
                                         str(group_select))
        items_group = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_grupo_elementos", select_data[2],
                                         "id_grupo", str(id_group_select))
        self.update_data_frame(select_data, items_group)


    def delete_event(self, i, select_data):
        id_bd = self.id_bd_items[i - 1]
        # borrar el item de la base de datos
        result = delete_group_item(select_data[0], select_data[1], select_data[2], str(id_bd))

        # actualizamos los datos agregados
        self.data_frame.destroy()
        self.data_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0)
        self.data_frame.grid(row=2, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=3)
        self.data_frame.grid_columnconfigure(2, weight=5)
        group_select = self.code_entry.get()
        id_group_select = get_id_item_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2],
                                         "codigo",
                                         str(group_select))
        items_group = get_filter_data_bd(select_data[0], select_data[1], "tbl_pres_grupo_elementos", select_data[2],
                                         "id_grupo", str(id_group_select))
        self.update_data_frame(select_data, items_group)

        if result == "ok":
            show_success("Se ha eliminado el item de la base de datos")

        else:
            show_warning(f"Error: {result}")

    def save(self, select_data):
        #actualizamos el coste del grupo con el sumatorio del coste de las partidas agregadas
        group_select = self.code_entry.get()
        id_group_select = get_id_item_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2],
                                         "codigo",
                                         str(group_select))
        cost_group = 0
        for item in self.cost_items:
            cost = float(item.replace(" €", ""))
            cost_group += cost
        result = mod_item_aux(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2], "coste",
                              cost_group, id_group_select)

        self.destroy()

        if result == "ok":
            show_success("Se ha modificado el grupo en la base de datos")
        else:
            show_warning(f"Error: {result}")



