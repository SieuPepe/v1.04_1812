import customtkinter
from PIL import Image
from CTkMessagebox import CTkMessagebox
from script.modulo_db  import (get_all_bd, get_id_item_sub_bd, get_id_item_bd,get_option_item_bd, add_item_budget)
from interface.item_aux_add_interfaz import AppItemAdd
from interface.item_chapter_add_interfaz import AppItemChapterAdd
import os

# Obtener la ruta actual
current_path = os.path.dirname(os.path.realpath(__file__))

# Subir un nivel en la estructura de carpetas
parent_path = os.path.dirname(current_path)

customtkinter.set_appearance_mode("dark")


class AppItemBudgetAdd(customtkinter.CTkToplevel):
    width = 800
    height = 575
    def __init__(self, select_data):
        super().__init__()

        password = select_data[1]
        user = select_data[0]
        schema =select_data[2]

        self.title("Añadir partida del presupuesto base")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_FRAME DATA_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.data_budget_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.data_budget_frame.grid(row=1, column=0, padx=30, pady=(10, 10), sticky="nsew", columnspan=2)
        self.data_budget_frame.grid_columnconfigure(0, weight=1)
        self.data_budget_frame.grid_columnconfigure(1, weight=1)

        # almacena código partida
        self.chapter_label = customtkinter.CTkLabel(self.data_budget_frame, text="CAPÍTULO:",
                                                 anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                 width=50)
        self.chapter_label.grid(row=0, column=0, padx=(30, 5), pady=10, sticky="e")
        chapter_budget_items = get_all_bd(user, password, "tbl_pres_capitulos", schema)
        chapter_values = []
        for item in chapter_budget_items:
            code = item[1]
            name = item[3]
            chapter_values.append(str(code) + " - " + name)
        chapter_values.remove("PA000 - PARTIDAS TIPO")
        self.chapter_option = customtkinter.CTkOptionMenu(self.data_budget_frame,
                                                                 dynamic_resizing=False,
                                                                 values=chapter_values)
        self.chapter_option.grid(row=0, column=1, padx=(5, 5), pady=10, sticky="ew")
        self.chapter_button = customtkinter.CTkButton(self.data_budget_frame, text="Añada nuevo capítulo",
                                                   command=lambda: self.add_chapter_data(select_data), width=50)
        self.chapter_button.grid(row=0, column=2, padx=(5, 30), pady=10, sticky="ew")

        common_fg_color = "#171717"

        # almacena código partida
        self.code_label = customtkinter.CTkLabel(self.data_budget_frame, text="CÓDIGO PARTIDA:",
                                                 anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                 width=50)
        self.code_label.grid(row=1, column=0, padx=(30, 5), pady=10, sticky="e")
        self.code_entry = customtkinter.CTkEntry(self.data_budget_frame, placeholder_text="añada código de partida",
                                                 fg_color=common_fg_color, text_color="#FFFFFF")
        self.code_entry.grid(row=1, column=1, padx=(5, 30), pady=10, sticky="ew", columnspan=2)

        # almacena la naturaleza
        self.type_label = customtkinter.CTkLabel(self.data_budget_frame, text="NATURALEZA:",
                                                 anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                 width=50)
        self.type_label.grid(row=2, column=0, padx=(30, 5), pady=10, sticky="e")
        type_value = get_option_item_bd(select_data[0], select_data[1], "tbl_pres_naturaleza", select_data[2], 'tipo')
        type_value.sort(key=str.lower)
        self.type_option = customtkinter.CTkOptionMenu(self.data_budget_frame,
                                                       dynamic_resizing=False,
                                                       values=type_value)
        self.type_option.grid(row=2, column=1, padx=(5, 5), pady=10, sticky="ew")
        self.type_button = customtkinter.CTkButton(self.data_budget_frame, text="Añada nueva naturaleza",
                                                   command=lambda: self.add_type_data(select_data), width=50)
        self.type_button.grid(row=2, column=2, padx=(5, 30), pady=10, sticky="ew")

        # almacena las unidades
        self.ud_label = customtkinter.CTkLabel(self.data_budget_frame, text="UNIDADES:",
                                               anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                               width=50)
        self.ud_label.grid(row=3, column=0, padx=(30, 5), pady=10, sticky="e")
        ud_value = get_option_item_bd(select_data[0], select_data[1], "tbl_pres_unidades", select_data[2], 'unidad')
        ud_value.sort(key=str.lower)
        self.ud_option = customtkinter.CTkOptionMenu(self.data_budget_frame,
                                                     dynamic_resizing=False,
                                                     values=ud_value)
        self.ud_option.grid(row=3, column=1, padx=(5, 5), pady=10, sticky="ew")
        self.ud_button = customtkinter.CTkButton(self.data_budget_frame, text="Añada nueva unidad",
                                                 command=lambda: self.add_ud_data(select_data), width=50)
        self.ud_button.grid(row=3, column=2, padx=(5, 30), pady=10, sticky="ew")

        # almacena resumen
        self.resume_label = customtkinter.CTkLabel(self.data_budget_frame, text="RESUMEN:",
                                                   anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                   width=50)
        self.resume_label.grid(row=4, column=0, padx=(30, 5), pady=(10, 10), sticky="e")
        self.resume_entry = customtkinter.CTkTextbox(self.data_budget_frame, fg_color=common_fg_color, height=100,
                                                     border_width=2, border_color="#565B5E", text_color="#FFFFFF")
        self.resume_entry.grid(row=4, column=1, padx=(5, 30), pady=(10, 10), sticky="ew", columnspan=2)

        # almacena descripción
        self.description_label = customtkinter.CTkLabel(self.data_budget_frame, text="DESCRIPCIÓN:",
                                                        anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                        width=50)
        self.description_label.grid(row=5, column=0, padx=(30, 5), pady=(10, 10), sticky="e")
        self.description_entry = customtkinter.CTkTextbox(self.data_budget_frame, fg_color=common_fg_color, height=100,
                                                          border_width=2, border_color="#565B5E", text_color="#FFFFFF")
        self.description_entry.grid(row=5, column=1, padx=(5, 30), pady=(10, 10), sticky="ew", columnspan=2)

        # almacena precio
        self.price_label = customtkinter.CTkLabel(self.data_budget_frame, text="PRECIO (€):",
                                                  anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                  width=50)
        self.price_label.grid(row=6, column=0, padx=(30, 5), pady=10, sticky="e")
        self.price_entry = customtkinter.CTkEntry(self.data_budget_frame, placeholder_text="añada precio de la partida",
                                                  fg_color=common_fg_color, text_color="#FFFFFF")
        self.price_entry.grid(row=6, column=1, padx=(5, 30), pady=10, sticky="ew", columnspan=2)


        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_BOTONES_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        # boton de guardar
        save_path = parent_path +"/source/guardar.png"
        self.save_image = customtkinter.CTkImage(Image.open(save_path))
        self.save_button = customtkinter.CTkButton(self, text="Guardar",image=self.save_image, compound="left",fg_color="green",
                                                   font=("default", 14, "bold"),
                                                   command=lambda: self.save(select_data),  height=40)
        self.save_button.grid(row=3, column=0, padx=(30,1), pady=10, sticky= "ew")

        # boton de cancelar
        cancel_path = parent_path +"/source/cancelar.png"
        self.cancel_image = customtkinter.CTkImage(Image.open(cancel_path))
        self.cancel_button = customtkinter.CTkButton(self, text="Cancelar",image=self.cancel_image, compound="left",fg_color="red",
                                                   font=("default", 14, "bold"),
                                                   command=self.cancel,  height=40)
        self.cancel_button.grid(row=3, column=1, padx=(10,30), pady=10, sticky= "ew")

        self.lift()


    def add_ud_data(self,select_data):
        appAux = AppItemAdd(select_data, 'tbl_pres_unidades', 'unidad', 'Unidades')
        appAux.grab_set()
        self.wait_window(appAux)
        ud_value = get_option_item_bd(select_data[0], select_data[1], 'tbl_pres_unidades', select_data[2],
                                         'unidad')
        ud_value.sort(key=str.lower)
        self.ud_option.configure(values=ud_value)


    def add_type_data(self,select_data):
        appAux = AppItemAdd(select_data, 'tbl_pres_naturaleza', 'tipo', 'Naturaleza')
        appAux.grab_set()
        self.wait_window(appAux)
        type_value = get_option_item_bd(select_data[0], select_data[1], 'tbl_pres_naturaleza', select_data[2],
                                         'tipo')
        type_value.sort(key=str.lower)
        self.type_option.configure(values=type_value)


    def add_chapter_data(self,select_data):
        appAux = AppItemChapterAdd(select_data)
        appAux.grab_set()
        self.wait_window(appAux)
        chapter_budget_items = get_all_bd(select_data[0], select_data[1], "tbl_pres_capitulos", select_data[2])
        chapter_values = []
        for item in chapter_budget_items:
            code = item[1]
            name = item[3]
            chapter_values.append(str(code) + " - " + name)
        chapter_values.remove("PA000 - PARTIDAS TIPO")
        self.chapter_option.configure(values=chapter_values)


    def cancel(self):
        self.destroy()


    def save(self, select_data):
        # recogida de datos de la interfaz
        chapter_select = self.chapter_option.get()
        code_chapter_select = chapter_select.split(" - ")[0]
        name_chapter_select = chapter_select.split(" - ")[1]
        id_chapter= get_id_item_sub_bd(select_data[0], select_data[1],  "tbl_pres_capitulos", select_data[2], "codigo_capitulo",
                                               code_chapter_select, "capitulo", name_chapter_select)
        code = self.code_entry.get()
        id_type = get_id_item_bd(select_data[0], select_data[1], 'tbl_pres_naturaleza', select_data[2],
                                 'tipo', self.type_option.get())
        id_ud = get_id_item_bd(select_data[0], select_data[1], 'tbl_pres_unidades', select_data[2],
                                  'unidad', self.ud_option.get())
        resume = self.resume_entry.get("1.0", "end-1c")
        description = self.description_entry.get("1.0", "end-1c")
        price = self.price_entry.get()
        if isinstance(price, str):
            price = price.replace(",", ".")

        data = [code, id_type, id_ud, resume, description,price, id_chapter]

        # modifica elementos de la bbdd
        result = add_item_budget(select_data[0], select_data[1], select_data[2], data)

        # mensaje de avisos
        if result == 'ok':
            mssg = "Se ha añadido la partida en la base de datos "
            self.destroy()
            CTkMessagebox(title="Successfull Message!", message=mssg,
                          icon="check")
        else:
            mssg = "ERROR: " + str(result)
            self.destroy()
            CTkMessagebox(title="Error Message!", message=mssg,
                          icon="cancel")

