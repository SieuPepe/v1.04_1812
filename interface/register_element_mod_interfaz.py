import customtkinter
from PIL import Image
import tkinter as tk
from CTkMessagebox import CTkMessagebox
from interface.item_aux_add_interfaz import AppItemAdd
from script.modulo_db import get_option_item_sub_bd, get_option_item_bd, get_id_item_bd, get_filter_data_bd
import os

# Obtener la ruta actual
current_path = os.path.dirname(os.path.realpath(__file__))

# Subir un nivel en la estructura de carpetas
parent_path = os.path.dirname(current_path)

customtkinter.set_appearance_mode("dark")

class AppElementModEmpty(customtkinter.CTkToplevel):  # Toplevel
    width = 1400
    height = 950
    register_items = {}
    hidro_items = {}
    def __init__(self, select_data):
        super().__init__()

        password = select_data[1]
        user = select_data[0]
        schema = select_data[2]


        self.title("Modificar elementos de la arqueta")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        self.lift()
        self.attributes('-topmost', True)

        common_fg_color = "#171717"

        self.grid_columnconfigure(0, weight=10)
        self.grid_columnconfigure(1, weight=1)

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA FILTROS-REGISTROS_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.filter_register_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.filter_register_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        self.filter_register_frame.grid_columnconfigure(0, weight=1)
        self.filter_register_frame.grid_columnconfigure(1, weight=6)
        self.filter_register_frame.grid_columnconfigure(2, weight=1)

        # ///////////////////////////////////añadir filtos/////////////////////////////////////////////////////////////
        self.register_label = customtkinter.CTkLabel(self.filter_register_frame, text="AÑADIR ELEMENTO NO HIDRÁULICO",
                                                     anchor="center",
                                                     font=customtkinter.CTkFont(size=13, weight="bold"))
        self.register_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 0), sticky="nwes", columnspan=3)

        # tipo
        self.type_register_label = customtkinter.CTkLabel(self.filter_register_frame, text="Tipo",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13, weight="bold"))
        self.type_register_label.grid(row=1, column=0, padx=(10, 5), pady=(10, 0), sticky="nwes")
        type_register_value = get_option_item_bd(user, password, "tbl_cata_regis_tipo", schema, 'tipo')
        self.type_register_option = customtkinter.CTkOptionMenu(self.filter_register_frame,
                                                                dynamic_resizing=False,
                                                                values=type_register_value,
                                                                command=lambda
                                                                    event: self.update_register_model_options(
                                                                    select_data))
        self.type_register_option.grid(row=2, column=0, padx=(10, 5), pady=(0, 10), sticky="ew")

        # modelo
        self.model_register_label = customtkinter.CTkLabel(self.filter_register_frame, text="Modelo",
                                                           anchor="center",
                                                           font=customtkinter.CTkFont(size=13, weight="bold"))
        self.model_register_label.grid(row=1, column=1, padx=(5, 5), pady=(10, 0), sticky="nwes")
        id_type_register = get_id_item_bd(user, password, 'tbl_cata_regis_tipo', schema, 'tipo',
                                          self.type_register_option.get())
        register_model_value = get_option_item_sub_bd(user, password, 'tbl_catalogo_registros', schema, 'modelo',
                                                      id_type_register, 'id_tipo_registro')

        self.model_register_label2 = customtkinter.CTkLabel(self.filter_register_frame,
                                                            text="No existe elementos registrados en la BBDD de este tipo",
                                                            anchor="center",
                                                            font=customtkinter.CTkFont(size=13))
        self.model_register_option = customtkinter.CTkOptionMenu(self.filter_register_frame,
                                                                 dynamic_resizing=False,
                                                                 values=register_model_value)
        self.type_register_option.bind("<<ComboboxSelected>>",
                                       lambda event: self.update_register_model_options(select_data))

        if len(register_model_value) == 0:
            self.model_register_label2.grid(row=2, column=1, padx=(5, 5), pady=(0, 10), sticky="ew")

        else:
            self.model_register_option.grid(row=2, column=1, padx=(5, 5), pady=(0, 10), sticky="ew")


        # almacena número de elementos
        self.n_item_register_label = customtkinter.CTkLabel(self.filter_register_frame, text="Cantidad",
                                                            anchor="center",
                                                            font=customtkinter.CTkFont(size=13, weight="bold"),
                                                            width=50)
        self.n_item_register_label.grid(row=1, column=2, padx=(5, 10), pady=(10, 0), sticky="nwes")
        n_item_register = str(1)
        n_item_register_value = tk.StringVar(value=n_item_register)
        self.n_item_register_entry = customtkinter.CTkEntry(self.filter_register_frame,
                                                            textvariable=n_item_register_value,
                                                            fg_color=common_fg_color, text_color="#FFFFFF")
        self.n_item_register_entry.grid(row=2, column=2, padx=(5, 10), pady=(0, 10), sticky="nwes")

        # Botón para añadir elementos
        self.add_button_register = customtkinter.CTkButton(self.filter_register_frame, text="Añadir",
                                                           command=lambda: self.add_item_register(select_data),
                                                           fg_color="green")
        self.add_button_register.grid(row=3, column=2, padx=(5, 10), pady=(5, 10), sticky="ew")

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA LISTBOX-REGISTRO_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.listbox_register_frame = customtkinter.CTkFrame(self)
        self.listbox_register_frame.grid(row=1, column=0, rowspan=3, padx=10, pady=10, sticky="news")
        self.listbox_register_frame.grid_columnconfigure(0, weight=1)
        self.listbox_register_frame.grid_rowconfigure(0, weight=1)

        # Crear la lista (Listbox)
        self.listbox_register = tk.Listbox(self.listbox_register_frame, width=40, height=10)
        self.listbox_register.grid(row=0, column=0, sticky="news")

        # Botón para eliminar elementos seleccionados
        self.remove_button_register = customtkinter.CTkButton(self, text="Eliminar", command=self.remove_item_register,
                                                              fg_color="red")
        self.remove_button_register.grid(row=1, column=1, pady=15)
        # Flecha hacia arriba
        self.up_button_register = customtkinter.CTkButton(self, text="↑", command=self.move_up_register,
                                                          font=("default", 14, "bold"), )
        self.up_button_register.grid(row=2, column=1, pady=15)
        # Flecha hacia abajo
        self.down_button_register = customtkinter.CTkButton(self, text="↓", command=self.move_down_register,
                                                            font=("default", 14, "bold"))
        self.down_button_register.grid(row=3, column=1, pady=15)

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA FILTROS-HIDRÁULICA_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.filter_hidro_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.filter_hidro_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        self.filter_hidro_frame.grid_columnconfigure(0, weight=1)
        self.filter_hidro_frame.grid_columnconfigure(1, weight=6)
        self.filter_hidro_frame.grid_columnconfigure(2, weight=1)

        # ///////////////////////////////////añadir filtros/////////////////////////////////////////////////////////////
        self.hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="AÑADIR ELEMENTO HIDRÁULICO",
                                                  anchor="center",
                                                  font=customtkinter.CTkFont(size=13, weight="bold"))
        self.hidro_label.grid(row=0, column=0, padx=10, pady=10, sticky="nwes", columnspan=3)

        # Número de líneas
        self.n_lines_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Nº de lineas:",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13, weight="bold"))
        self.n_lines_hidro_label.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="nwes")
        n_lines_register = str(1)
        n_lines_register_value = tk.StringVar(value=n_lines_register)
        self.n_lines_register_entry = customtkinter.CTkEntry(self.filter_hidro_frame,
                                                             textvariable=n_lines_register_value,
                                                             fg_color=common_fg_color, text_color="#FFFFFF")
        self.n_lines_register_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nwes")

        # Botón para añadir elementos
        self.n_lines_button = customtkinter.CTkButton(self.filter_hidro_frame, text="Definir número de líneas",
                                                      command=lambda: self.add_hidro_filters(select_data,
                                                                                             self.n_lines_register_entry.get()))
        self.n_lines_button.grid(row=1, column=2, padx=(5, 10), pady=5, sticky="nwes")

        self.n_lines_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame,
                                                          text="Es necesario definir el número de lineas para añadir elementos",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13))
        self.n_lines_hidro_label.grid(row=2, column=0, padx=10, pady=10, sticky="nwes", columnspan=3)

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA LISTBOX-HIDRÁULICA_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.listbox_hidro_frame = customtkinter.CTkFrame(self)
        self.listbox_hidro_frame.grid(row=5, column=0, rowspan=3, padx=10, pady=10, sticky="news")
        self.listbox_hidro_frame.grid_columnconfigure(0, weight=1)
        self.listbox_hidro_frame.grid_rowconfigure(0, weight=1)

        # Crear la lista (Listbox)
        self.listbox_hidro = tk.Listbox(self.listbox_hidro_frame, width=40, height=10)
        self.listbox_hidro.grid(row=0, column=0, sticky="news")

        # Botón para eliminar elementos seleccionados
        self.remove_button_hidro = customtkinter.CTkButton(self, text="Eliminar", command=self.remove_item_hidro,
                                                           fg_color="red")
        self.remove_button_hidro.grid(row=5, column=1, pady=15)
        # Flecha hacia arriba
        self.up_button_hidro = customtkinter.CTkButton(self, text="↑", command=self.move_up_hidro,
                                                       font=("default", 14, "bold"), )
        self.up_button_hidro.grid(row=6, column=1, pady=15)
        # Flecha hacia abajo
        self.down_button_hidro = customtkinter.CTkButton(self, text="↓", command=self.move_down_hidro,
                                                         font=("default", 14, "bold"))
        self.down_button_hidro.grid(row=7, column=1, pady=15)

        self.grid_rowconfigure(8, weight=1)
        # boton de guardar
        save_path = parent_path + "/resources/images/guardar.png"
        self.save_image = customtkinter.CTkImage(Image.open(save_path))
        self.save_button = customtkinter.CTkButton(self, text="Guardar", image=self.save_image, compound="left",
                                                   fg_color="green",
                                                   font=("default", 14, "bold"),
                                                   command=self.save, height=40)
        self.save_button.grid(row=9, column=1, padx=10, pady=20, sticky="ew")

        self.lift()

    def update_register_model_options(self, select_data):
        id_type_register = get_id_item_bd(select_data[0], select_data[1], 'tbl_cata_regis_tipo', select_data[2], 'tipo',
                                          self.type_register_option.get())
        register_model_value = get_option_item_sub_bd(select_data[0], select_data[1], 'tbl_catalogo_registros',
                                                      select_data[2], 'modelo',
                                                      id_type_register, 'id_tipo_registro')

        self.model_register_option.grid_remove()
        self.model_register_label2.grid_remove()

        if len(register_model_value) == 0:
            self.model_register_label2.grid(row=2, column=1, padx=(5, 5), pady=(0, 10), sticky="nwes")
        else:
            self.model_register_option.configure(values=register_model_value)
            self.model_register_option.set(register_model_value[0])
            self.model_register_option.grid(row=2, column=1, padx=(5, 5), pady=(0, 10), sticky="ew")

    def add_item_register(self, select_data):
        if int(self.n_item_register_entry.get()) == 1:
            n_item_register = self.n_item_register_entry.get() + " ud"
        else:
            n_item_register = self.n_item_register_entry.get() + " uds"
        id_type_register = get_id_item_bd(select_data[0], select_data[1], 'tbl_cata_regis_tipo', select_data[2], 'tipo',
                                          self.type_register_option.get())
        register_model_value = get_option_item_sub_bd(select_data[0], select_data[1], 'tbl_catalogo_registros',
                                                      select_data[2], 'modelo',
                                                      id_type_register, 'id_tipo_registro')
        if len(register_model_value) > 0:
            item_register = self.model_register_option.get()
            item_type = self.type_register_option.get()
            item = (item_register, n_item_register, item_type)
            self.listbox_register.insert(customtkinter.END, str(item))
        else:
            mssg = "Por favor, introduce un elemento existente"
            CTkMessagebox(title="Error Message!", message=mssg,
                          icon="cancel")

    def remove_item_register(self):
        selected_register_index = self.listbox_register.curselection()
        if selected_register_index:
            self.listbox_register.delete(selected_register_index)
        else:
            mssg = "Selecciona un elemento para eliminar"
            CTkMessagebox(title="Error Message!", message=mssg,
                          icon="cancel")

    def move_up_register(self):
        selected_register_index = self.listbox_register.curselection()
        if selected_register_index and selected_register_index[0] > 0:
            current_index = selected_register_index[0]
            item = self.listbox_register.get(current_index)
            self.listbox_register.delete(current_index)
            self.listbox_register.insert(current_index - 1, item)
            self.listbox_register.select_set(current_index - 1)
        else:
            mssg = "No se puede mover el elemento más arriba"
            CTkMessagebox(title="Error Message!", message=mssg,
                          icon="cancel")

    def move_down_register(self):
        selected_register_index = self.listbox_register.curselection()
        if selected_register_index and selected_register_index[0] < self.listbox_register.size() - 1:
            current_index = selected_register_index[0]
            item = self.listbox_register.get(current_index)
            self.listbox_register.delete(current_index)
            self.listbox_register.insert(current_index + 1, item)
            self.listbox_register.select_set(current_index + 1)
        else:
            mssg = "No se puede mover el elemento más abajo"
            CTkMessagebox(title="Error Message!", message=mssg,
                          icon="cancel")

    def add_hidro_filters(self, select_data, n_lines):

        self.filter_hidro_frame.destroy()
        self.filter_hidro_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.filter_hidro_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        self.filter_hidro_frame.grid_columnconfigure(0, weight=3)
        self.filter_hidro_frame.grid_columnconfigure(1, weight=3)
        self.filter_hidro_frame.grid_columnconfigure(2, weight=1)
        self.filter_hidro_frame.grid_columnconfigure(3, weight=1)
        self.filter_hidro_frame.grid_columnconfigure(4, weight=1)
        self.filter_hidro_frame.grid_columnconfigure(5, weight=1)
        self.filter_hidro_frame.grid_columnconfigure(6, weight=3)

        common_fg_color = "#171717"

        # ///////////////////////////////////añadir filtros/////////////////////////////////////////////////////////////
        self.hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="AÑADIR ELEMENTO HIDRÁULICO",
                                                  anchor="center",
                                                  font=customtkinter.CTkFont(size=13, weight="bold"))
        self.hidro_label.grid(row=0, column=0, padx=(10, 10), pady=5, sticky="nwes", columnspan=7)

        # Número de líneas
        self.n_lines_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Nº de lineas:",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13, weight="bold"))
        self.n_lines_hidro_label.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="nwes", columnspan=2)

        n_lines_register_value = tk.StringVar(value=n_lines)
        self.n_lines_register_entry = customtkinter.CTkEntry(self.filter_hidro_frame,
                                                             textvariable=n_lines_register_value,
                                                             fg_color=common_fg_color, text_color="#FFFFFF")
        self.n_lines_register_entry.grid(row=1, column=2, padx=(5, 5), pady=5, sticky="nwes", columnspan=3)

        # Botón para añadir elementos
        self.n_lines_button = customtkinter.CTkButton(self.filter_hidro_frame, text="Definir número de líneas",
                                                      command=lambda: self.add_hidro_filters(select_data,
                                                                                             self.n_lines_register_entry.get()))
        self.n_lines_button.grid(row=1, column=5, padx=(5, 10), pady=5, sticky="nwes", columnspan=2)

        # seleccion de modelo
        self.select_model_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="SELECCIÓN DE MODELO",
                                                         anchor="center",
                                                         font=customtkinter.CTkFont(size=13, weight="bold"))
        self.select_model_label.grid(row=2, column=0, padx=(10, 10), pady=5, sticky="nwes", columnspan=7)

        # familia
        self.family_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Familia",
                                                         anchor="center",
                                                         font=customtkinter.CTkFont(size=13, weight="bold"))
        self.family_hidro_label.grid(row=3, column=0, padx=5, pady=(5, 0), sticky="nwes")
        family_value = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_familia", select_data[2],
                                          'familia')
        family_value.sort(key=str.lower)
        self.family_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                               dynamic_resizing=False,
                                                               values=family_value,
                                                               command=lambda
                                                                   event: self.update_type_hidro_options(select_data))
        self.family_hidro_option.grid(row=4, column=0, padx=5, pady=(0, 5), sticky="ew")
        self.family_hidro_option.set(family_value[0])
        self.family_hidro_option.bind("<<ComboboxSelected>>", lambda event: self.update_type_hidro_options(select_data))

        self.filter_hidro_options(select_data)

        # seleccion de posición
        self.select_position_label = customtkinter.CTkLabel(self.filter_hidro_frame,
                                                            text="INDICAR CARACTERÍSTICAS DE COLOCACIÓN DE LA PIEZA",
                                                            anchor="center",
                                                            font=customtkinter.CTkFont(size=13, weight="bold"))
        self.select_position_label.grid(row=5, column=0, padx=(10, 10), pady=5, sticky="nwes", columnspan=7)
        # línea
        list_lines = []
        for i in range(int(n_lines)):
            n_line = i + 1
            item = "L-" + str(n_line)
            list_lines.append(item)
        self.line_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Línea",
                                                       anchor="center",
                                                       font=customtkinter.CTkFont(size=13, weight="bold"),
                                                       width=40)
        self.line_hidro_label.grid(row=6, column=0, padx=(10, 5), pady=(5, 0), sticky="nwes")
        self.line_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                             dynamic_resizing=False,
                                                             values=list_lines,
                                                             width=70)
        self.line_hidro_option.grid(row=7, column=0, padx=(10, 5), pady=(0, 10), sticky="ew")

        # existente / nueva pieza
        self.state_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Estado pieza",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=13, weight="bold"),
                                                        width=40)
        self.state_hidro_label.grid(row=6, column=1, padx=5, pady=(5, 0), sticky="nwes")
        self.state_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                              dynamic_resizing=False,
                                                              values=['Nueva', 'Existente'],
                                                              width=70)
        self.state_hidro_option.grid(row=7, column=1, padx=5, pady=(0, 10), sticky="ew")
        self.state_hidro_option.set('Nueva')

        # orientacion
        orientation_value = get_option_item_bd(select_data[0], select_data[1], "tbl_inv_orientacion", select_data[2],
                                               'orientacion')
        self.orientation_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Orientación",
                                                              anchor="center",
                                                              font=customtkinter.CTkFont(size=13, weight="bold"),
                                                              width=40)
        self.orientation_hidro_label.grid(row=6, column=2, padx=5, pady=(5, 0), sticky="nwes")
        self.orientation_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                                    dynamic_resizing=False,
                                                                    values=orientation_value,
                                                                    width=70)
        self.orientation_hidro_option.grid(row=7, column=2, padx=5, pady=(0, 10), sticky="ew")
        self.orientation_hidro_option.set(orientation_value[0])

        # material de la pieza
        material_value = get_option_item_bd(select_data[0], select_data[1], "tbl_inv_material", select_data[2],
                                            'material')
        self.material_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Material",
                                                           anchor="center",
                                                           font=customtkinter.CTkFont(size=13, weight="bold"),
                                                           width=40)
        self.material_hidro_label.grid(row=6, column=3, padx=5, pady=(10, 0), sticky="nwes")
        self.material_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                                 dynamic_resizing=False,
                                                                 values=material_value,
                                                                 width=70)
        self.material_hidro_option.grid(row=7, column=3, padx=5, pady=(0, 10), sticky="ew")
        self.material_hidro_option.set(material_value[0])
        self.material_button_hidro = customtkinter.CTkButton(self.filter_hidro_frame, text="Añadir nuevo material",
                                                             command=lambda: self.add_material_data(select_data),
                                                             fg_color="gray21")
        self.material_button_hidro.grid(row=7, column=4, padx=5, pady=(0, 10), sticky="ew")

        self.update_connnection_hidro_options()

        # Botón para añadir elementos
        self.add_button_hidro = customtkinter.CTkButton(self.filter_hidro_frame, text="Añadir",
                                                        command=lambda: self.add_item_hidro(select_data),
                                                        fg_color="green")
        self.add_button_hidro.grid(row=7, column=6, padx=(5, 10), pady=(0, 10), sticky="ew")

    def filter_hidro_options(self, select_data):
        type_hidro_data = self.update_type_hidro_options(select_data)
        dni_hidro_data = self.update_dni_hidro_options(type_hidro_data)
        dnf_hidro_data = self.update_dnf_hidro_options(dni_hidro_data)
        pn_hidro_data = self.update_pn_hidro_options(dnf_hidro_data)
        angle_hidro_data = self.update_angle_hidro_options(pn_hidro_data)
        self.update_model_hidro_options(angle_hidro_data)

    def update_type_hidro_options(self, select_data):
        family_option_value = self.family_hidro_option.get()
        if isinstance(family_option_value, str):
            family_option_value = [family_option_value]
        hidro_data = get_filter_data_bd(select_data[0], select_data[1], "vw_catalogo_hidraulica",
                                        select_data[2], "familia", family_option_value[0])
        type_hidro_value = list(set([item[2] for item in hidro_data]))
        type_hidro_value.sort(key=str.lower)
        # tipo
        self.type_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Tipo",
                                                       anchor="center",
                                                       font=customtkinter.CTkFont(size=13, weight="bold"))
        self.type_hidro_label.grid(row=3, column=1, padx=5, pady=(5, 0), sticky="nwes")
        self.type_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                             dynamic_resizing=False,
                                                             values=type_hidro_value,
                                                             command=lambda event: self.update_dni_hidro_options(
                                                                 hidro_data))
        self.type_hidro_option.grid(row=4, column=1, padx=5, pady=(0, 5), sticky="ew")
        self.type_hidro_option.bind("<<ComboboxSelected>>", lambda event: self.update_dni_hidro_options(hidro_data))
        self.update_dni_hidro_options(hidro_data)
        return hidro_data

    def update_dni_hidro_options(self, hidro_data):
        type_option_value = self.type_hidro_option.get()
        if isinstance(type_option_value, str):
            type_option_value = [type_option_value]
        hidro_data = [sublist for sublist in hidro_data if type_option_value[0] in sublist]
        dni_hidro_value = list(set([item[7] for item in hidro_data]))
        dni_hidro_value.sort(key=str.lower)
        # dn inicial
        self.dni_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="DN incial",
                                                      anchor="center",
                                                      font=customtkinter.CTkFont(size=13, weight="bold"))
        self.dni_hidro_label.grid(row=3, column=2, padx=5, pady=(5, 0), sticky="nwes")
        self.dni_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                            dynamic_resizing=False,
                                                            values=dni_hidro_value,
                                                            command=lambda event: self.update_dnf_hidro_options(
                                                                hidro_data))
        self.dni_hidro_option.grid(row=4, column=2, padx=5, pady=(0, 5), sticky="ew")
        self.dni_hidro_option.bind("<<ComboboxSelected>>", lambda event: self.update_dnf_hidro_options(hidro_data))
        self.update_dnf_hidro_options(hidro_data)
        return hidro_data

    def update_dnf_hidro_options(self, hidro_data):
        dni_option_value = self.dni_hidro_option.get()
        if isinstance(dni_option_value, str):
            dni_option_value = [dni_option_value]
        hidro_data = [sublist for sublist in hidro_data if dni_option_value[0] in sublist]
        dnf_hidro_value = list(set([item[8] for item in hidro_data]))
        dnf_hidro_value.sort(key=str.lower)
        # dn final
        self.dnf_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="DN final",
                                                      anchor="center",
                                                      font=customtkinter.CTkFont(size=13, weight="bold"))
        self.dnf_hidro_label.grid(row=3, column=3, padx=5, pady=(5, 0), sticky="nwes")
        self.dnf_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                            dynamic_resizing=False,
                                                            values=dnf_hidro_value,
                                                            command=lambda event: self.update_pn_hidro_options(
                                                                hidro_data))
        self.dnf_hidro_option.grid(row=4, column=3, padx=5, pady=(0, 5), sticky="ew")
        self.dnf_hidro_option.bind("<<ComboboxSelected>>", lambda event: self.update_pn_hidro_options(hidro_data))
        self.update_pn_hidro_options(hidro_data)
        return hidro_data

    def update_pn_hidro_options(self, hidro_data):
        dnf_option_value = self.dnf_hidro_option.get()
        if isinstance(dnf_option_value, str):
            dnf_option_value = [dnf_option_value]
        hidro_data = [sublist for sublist in hidro_data if dnf_option_value[0] in sublist]
        pn_hidro_value = list(set([item[9] for item in hidro_data]))
        pn_hidro_value.sort(key=str.lower)
        # pn
        self.pn_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="PN",
                                                     anchor="center",
                                                     font=customtkinter.CTkFont(size=13, weight="bold"))
        self.pn_hidro_label.grid(row=3, column=4, padx=5, pady=(5, 0), sticky="nwes")
        self.pn_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                           dynamic_resizing=False,
                                                           values=pn_hidro_value,
                                                           command=lambda event: self.update_angle_hidro_options(
                                                               hidro_data))
        self.pn_hidro_option.grid(row=4, column=4, padx=5, pady=(0, 5), sticky="ew")
        self.pn_hidro_option.bind("<<ComboboxSelected>>", lambda event: self.update_angle_hidro_options(hidro_data))
        self.update_angle_hidro_options(hidro_data)
        return hidro_data

    def update_angle_hidro_options(self, hidro_data):
        pn_option_value = self.pn_hidro_option.get()
        if isinstance(pn_option_value, str):
            pn_option_value = [pn_option_value]
        hidro_data = [sublist for sublist in hidro_data if pn_option_value[0] in sublist]
        angle_hidro_value = list(set([item[10] for item in hidro_data]))
        angle_hidro_value.sort(key=str.lower)
        # angulo
        self.angle_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Ángulo",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=13, weight="bold"))
        self.angle_hidro_label.grid(row=3, column=5, padx=5, pady=(5, 0), sticky="nwes")
        self.angle_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                              dynamic_resizing=False,
                                                              values=angle_hidro_value,
                                                              command=lambda event: self.update_model_hidro_options(
                                                                  hidro_data))
        self.angle_hidro_option.grid(row=4, column=5, padx=5, pady=(0, 5), sticky="ew")
        self.angle_hidro_option.bind("<<ComboboxSelected>>", lambda event: self.update_model_hidro_options(hidro_data))
        self.update_model_hidro_options(hidro_data)
        return hidro_data

    def update_model_hidro_options(self, hidro_data):
        angle_option_value = self.angle_hidro_option.get()
        if isinstance(angle_option_value, str):
            angle_option_value = [angle_option_value]
        hidro_data = [sublist for sublist in hidro_data if angle_option_value[0] in sublist]
        model_hidro_value = [item[5] for item in hidro_data]
        model_hidro_value.sort(key=str.lower)
        # modelo
        self.model_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Modelo",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=13, weight="bold"))
        self.model_hidro_label.grid(row=3, column=6, padx=(5, 10), pady=(5, 0), sticky="nwes")
        self.model_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                              dynamic_resizing=False,
                                                              values=model_hidro_value)
        self.model_hidro_option.grid(row=4, column=6, padx=(5, 10), pady=(0, 5), sticky="ew")

    def update_connnection_hidro_options(self):
        # comprobar si hay elementos ya añadidos
        n_items_hidro = self.listbox_hidro.get(0, tk.END)
        self.connection_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame,
                                                             text="Pieza conexión (aguas arriba)",
                                                             anchor="center",
                                                             font=customtkinter.CTkFont(size=13, weight="bold"))
        self.connection_hidro_label.grid(row=6, column=5, padx=5, pady=(5, 0), sticky="nwes")
        if len(n_items_hidro) == 0:
            # conexion con pieza agua arriba
            self.connection_hidro_label2 = customtkinter.CTkLabel(self.filter_hidro_frame,
                                                                  text="Debe agregar un nuevo elemento",
                                                                  anchor="center",
                                                                  font=customtkinter.CTkFont(size=13))
            self.connection_hidro_label2.grid(row=7, column=5, padx=5, pady=(0, 5), sticky="nwes")
        else:
            hidro_connection_value = []
            for item in n_items_hidro:
                item = item.replace('"', '').replace("'", "").replace("(", "").replace(")", "")
                list = item.split(",")
                hidro_connection_value.append(list[0] + " " + list[2])
            hidro_connection_value.sort(reverse=True)
            self.connection_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                                       dynamic_resizing=False,
                                                                       values=hidro_connection_value)
            self.connection_hidro_option.grid(row=7, column=5, padx=5, pady=(0, 5), sticky="ew")
            self.connection_hidro_option.set(hidro_connection_value[0])

    def add_item_hidro(self, select_data):
        line = self.line_hidro_option.get()
        id_type_hidro = get_id_item_bd(select_data[0], select_data[1], 'tbl_cata_hidra_tipo', select_data[2],
                                       'tipo_elemento',
                                       self.type_hidro_option.get())
        hidro_model_value = get_option_item_sub_bd(select_data[0], select_data[1], 'tbl_catalogo_hidraulica',
                                                   select_data[2], 'modelo',
                                                   id_type_hidro, 'id_tipo_hidraulica')
        hidro_items = self.listbox_hidro.get(0, tk.END)
        if len(hidro_items) == 0:
            if len(hidro_model_value) > 0:
                position = "P" + str(len(hidro_items) + 1)
                type = self.type_hidro_option.get()
                status = self.state_hidro_option.get()
                orientation = self.orientation_hidro_option.get()
                material = self.material_hidro_option.get()
                model = self.model_hidro_option.get()
                line_model = line + "_" + model
                item = (position, line, line_model, "input", type, status, orientation, material)
                self.listbox_hidro.insert(customtkinter.END, str(item))
            else:
                mssg = "Por favor, introduce un elemento existente."
                CTkMessagebox(title="Error Message!", message=mssg,
                              icon="cancel")
        else:
            hidro_added = self.connection_hidro_option.get()
            if len(hidro_model_value) > 0 and len(hidro_added) > 0:
                position = "P" + str(len(hidro_items) + 1)
                type = self.type_hidro_option.get()
                status = self.state_hidro_option.get()
                orientation = self.orientation_hidro_option.get()
                material = self.material_hidro_option.get()
                model = self.model_hidro_option.get()
                line_model = line + "_" + model
                connection = self.connection_hidro_option.get()
                item = (position, line, line_model, connection, type, status, orientation, material)
                self.listbox_hidro.insert(customtkinter.END, str(item))
            else:
                mssg = "Por favor, introduce un elemento existente."
                CTkMessagebox(title="Error Message!", message=mssg,
                              icon="cancel")
        self.update_connnection_hidro_options()

    def remove_item_hidro(self):
        selected_index_hidro = self.listbox_hidro.curselection()
        if selected_index_hidro:
            self.listbox_hidro.delete(selected_index_hidro)
            self.update_connnection_hidro_options()
        else:
            mssg = "Selecciona un elemento para eliminar."
            CTkMessagebox(title="Error Message!", message=mssg,
                          icon="cancel")

    def move_up_hidro(self):
        selected_index_hidro = self.listbox_hidro.curselection()
        if selected_index_hidro and selected_index_hidro[0] > 0:
            current_index = selected_index_hidro[0]
            item = self.listbox_hidro.get(current_index)
            self.listbox_hidro.delete(current_index)
            self.listbox_hidro.insert(current_index - 1, item)
            self.listbox_hidro.select_set(current_index - 1)
        else:
            mssg = "No se puede mover el elemento más arriba"
            CTkMessagebox(title="Error Message!", message=mssg,
                          icon="cancel")

    def move_down_hidro(self):
        selected_index_hidro = self.listbox_hidro.curselection()
        if selected_index_hidro and selected_index_hidro[0] < self.listbox_hidro.size() - 1:
            current_index = selected_index_hidro[0]
            item = self.listbox_hidro.get(current_index)
            self.listbox_hidro.delete(current_index)
            self.listbox_hidro.insert(current_index + 1, item)
            self.listbox_hidro.select_set(current_index + 1)
        else:
            mssg = "No se puede mover el elemento más abajo"
            CTkMessagebox(title="Error Message!", message=mssg,
                          icon="cancel")

    def add_material_data(self, select_data):
        appAux = AppItemAdd(select_data, 'tbl_inv_material', 'material', 'Material')
        appAux.grab_set()
        self.wait_window(appAux)
        material_value = get_option_item_bd(select_data[0], select_data[1], "tbl_inv_material", select_data[2],
                                            'material')
        self.material_hidro_option.configure(values=material_value)

    def save(self):
        # Obtener todos los elementos del Listbox
        self.items_hidro = self.listbox_hidro.get(0, tk.END)
        self.items_register = self.listbox_register.get(0, tk.END)
        self.destroy()

    def get_items(self):
        return self.items_hidro, self.items_register


class AppElementModNoEmpty(customtkinter.CTkToplevel):  # Toplevel
    width = 1400
    height = 950
    register_items = {}
    hidro_items = {}

    def __init__(self, select_data,id_register_select,element_hidro_data, element_regis_data):
        super().__init__()

        password = select_data[1]
        user = select_data[0]
        schema = select_data[2]
        self.id_register=id_register_select

        self.title("Modificar elementos de la arqueta")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        self.lift()
        self.attributes('-topmost', True)

        common_fg_color = "#171717"

        self.grid_columnconfigure(0, weight=10)
        self.grid_columnconfigure(1, weight=1)

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA FILTROS-REGISTROS_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.filter_register_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.filter_register_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        self.filter_register_frame.grid_columnconfigure(0, weight=1)
        self.filter_register_frame.grid_columnconfigure(1, weight=6)
        self.filter_register_frame.grid_columnconfigure(2, weight=1)

        # ///////////////////////////////////añadir filtos/////////////////////////////////////////////////////////////
        self.register_label = customtkinter.CTkLabel(self.filter_register_frame, text="AÑADIR ELEMENTO NO HIDRÁULICO",
                                                     anchor="center",
                                                     font=customtkinter.CTkFont(size=13, weight="bold"))
        self.register_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 0), sticky="nwes", columnspan=3)
        # tipo
        self.type_register_label = customtkinter.CTkLabel(self.filter_register_frame, text="Tipo",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13, weight="bold"))
        self.type_register_label.grid(row=1, column=0, padx=(10, 5), pady=(10, 0), sticky="nwes")
        type_register_value = get_option_item_bd(user, password, "tbl_cata_regis_tipo", schema, 'tipo')
        self.type_register_option = customtkinter.CTkOptionMenu(self.filter_register_frame,
                                                                dynamic_resizing=False,
                                                                values=type_register_value,
                                                                command=lambda
                                                                    event: self.update_register_model_options(
                                                                    select_data))
        self.type_register_option.grid(row=2, column=0, padx=(10, 5), pady=(0, 10), sticky="ew")

        # modelo
        self.model_register_label = customtkinter.CTkLabel(self.filter_register_frame, text="Modelo",
                                                           anchor="center",
                                                           font=customtkinter.CTkFont(size=13, weight="bold"))
        self.model_register_label.grid(row=1, column=1, padx=(5, 5), pady=(10, 0), sticky="nwes")
        id_type_register = get_id_item_bd(user, password, 'tbl_cata_regis_tipo', schema, 'tipo',
                                          self.type_register_option.get())
        register_model_value = get_option_item_sub_bd(user, password, 'tbl_catalogo_registros', schema, 'modelo',
                                                      id_type_register, 'id_tipo_registro')
        self.model_register_label2 = customtkinter.CTkLabel(self.filter_register_frame,
                                                            text="No existe elementos registrados en la BBDD de este tipo",
                                                            anchor="center",
                                                            font=customtkinter.CTkFont(size=13))
        self.model_register_option = customtkinter.CTkOptionMenu(self.filter_register_frame,
                                                                 dynamic_resizing=False,
                                                                 values=register_model_value)
        self.type_register_option.bind("<<ComboboxSelected>>",
                                       lambda event: self.update_register_model_options(select_data))

        if len(register_model_value) == 0:
            self.model_register_label2.grid(row=2, column=1, padx=(5, 5), pady=(0, 10), sticky="ew")

        else:
            self.model_register_option.grid(row=2, column=1, padx=(5, 5), pady=(0, 10), sticky="ew")

        # almacena número de elementos
        self.n_item_register_label = customtkinter.CTkLabel(self.filter_register_frame, text="Cantidad",
                                                            anchor="center",
                                                            font=customtkinter.CTkFont(size=13, weight="bold"),
                                                            width=50)
        self.n_item_register_label.grid(row=1, column=2, padx=(5, 10), pady=(10, 0), sticky="nwes")
        n_item_register = str(1)
        n_item_register_value = tk.StringVar(value=n_item_register)
        self.n_item_register_entry = customtkinter.CTkEntry(self.filter_register_frame,
                                                            textvariable=n_item_register_value,
                                                            fg_color=common_fg_color, text_color="#FFFFFF")
        self.n_item_register_entry.grid(row=2, column=2, padx=(5, 10), pady=(0, 10), sticky="nwes")

        # Botón para añadir elementos
        self.add_button_register = customtkinter.CTkButton(self.filter_register_frame, text="Añadir",
                                                           command=lambda: self.add_item_register(select_data),
                                                           fg_color="green")
        self.add_button_register.grid(row=3, column=2, padx=(5, 10), pady=(5, 10), sticky="ew")

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA LISTBOX-REGISTRO_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.listbox_register_frame = customtkinter.CTkFrame(self)
        self.listbox_register_frame.grid(row=1, column=0, rowspan=3, padx=10, pady=10, sticky="news")
        self.listbox_register_frame.grid_columnconfigure(0, weight=1)
        self.listbox_register_frame.grid_rowconfigure(0, weight=1)

        # Crear la lista (Listbox)
        self.listbox_register = tk.Listbox(self.listbox_register_frame, width=40, height=10)
        self.listbox_register.grid(row=0, column=0, sticky="news")

        #añadimos elementos existentes
        for item in element_regis_data:
            self.listbox_register.insert(customtkinter.END, str(item))

        # Botón para eliminar elementos seleccionados
        self.remove_button_register = customtkinter.CTkButton(self, text="Eliminar", command=self.remove_item_register,
                                                              fg_color="red")
        self.remove_button_register.grid(row=1, column=1, pady=15)
        # Flecha hacia arriba
        self.up_button_register = customtkinter.CTkButton(self, text="↑", command=self.move_up_register,
                                                          font=("default", 14, "bold"), )
        self.up_button_register.grid(row=2, column=1, pady=15)
        # Flecha hacia abajo
        self.down_button_register = customtkinter.CTkButton(self, text="↓", command=self.move_down_register,
                                                            font=("default", 14, "bold"))
        self.down_button_register.grid(row=3, column=1, pady=15)

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA FILTROS-HIDRÁULICA_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.filter_hidro_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.filter_hidro_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        self.filter_hidro_frame.grid_columnconfigure(0, weight=3)
        self.filter_hidro_frame.grid_columnconfigure(1, weight=3)
        self.filter_hidro_frame.grid_columnconfigure(2, weight=1)
        self.filter_hidro_frame.grid_columnconfigure(3, weight=1)
        self.filter_hidro_frame.grid_columnconfigure(4, weight=1)
        self.filter_hidro_frame.grid_columnconfigure(5, weight=1)
        self.filter_hidro_frame.grid_columnconfigure(6, weight=3)

        # ///////////////////////////////////añadir filtros/////////////////////////////////////////////////////////////
        self.hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="AÑADIR ELEMENTO HIDRÁULICO",
                                                  anchor="center",
                                                  font=customtkinter.CTkFont(size=13, weight="bold"))
        self.hidro_label.grid(row=0, column=0, padx=(10, 10), pady=5, sticky="nwes", columnspan=7)

        # línea
        data_elements= get_filter_data_bd(user, password, "tbl_inv_elementos", schema, "id_inventario",  str(self.id_register))
        list_n_lines =[item[4] for item in data_elements if item[4] is not None]
        n_lines = max(list_n_lines)
        list_lines = []
        for i in range(n_lines):
            n_line = i + 1
            item = "L-" + str(n_line)
            list_lines.append(item)
        # Número de líneas
        self.n_lines_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Nº de lineas:",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13, weight="bold"))
        self.n_lines_hidro_label.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="nwes", columnspan=2)

        n_lines_register_value = tk.StringVar(value=n_lines)
        self.n_lines_register_entry = customtkinter.CTkEntry(self.filter_hidro_frame,
                                                             textvariable=n_lines_register_value,
                                                             fg_color=common_fg_color, text_color="#FFFFFF")
        self.n_lines_register_entry.grid(row=1, column=2, padx=(5, 5), pady=5, sticky="nwes", columnspan=3)

        # Botón para añadir elementos
        self.n_lines_button = customtkinter.CTkButton(self.filter_hidro_frame, text="Definir número de líneas",
                                                      command=lambda: self.add_hidro_filters(select_data,
                                                                                             self.n_lines_register_entry.get()))
        self.n_lines_button.grid(row=1, column=5, padx=(5, 10), pady=5, sticky="nwes", columnspan=2)

        # seleccion de modelo
        self.select_model_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="SELECCIÓN DE MODELO",
                                                         anchor="center",
                                                         font=customtkinter.CTkFont(size=13, weight="bold"))
        self.select_model_label.grid(row=2, column=0, padx=(10, 10), pady=5, sticky="nwes", columnspan=7)

        # familia
        self.family_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Familia",
                                                         anchor="center",
                                                         font=customtkinter.CTkFont(size=13, weight="bold"))
        self.family_hidro_label.grid(row=3, column=0, padx=5, pady=(5, 0), sticky="nwes")
        family_value = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_familia", select_data[2],
                                          'familia')
        family_value.sort(key=str.lower)
        self.family_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                               dynamic_resizing=False,
                                                               values=family_value,
                                                               command=lambda
                                                                   event: self.update_type_hidro_options(
                                                                   select_data))
        self.family_hidro_option.grid(row=4, column=0, padx=5, pady=(0, 5), sticky="ew")
        self.family_hidro_option.set(family_value[0])
        self.family_hidro_option.bind("<<ComboboxSelected>>",
                                      lambda event: self.update_type_hidro_options(select_data))

        self.filter_hidro_options(select_data)

        # seleccion de posición
        self.select_position_label = customtkinter.CTkLabel(self.filter_hidro_frame,
                                                            text="INDICAR CARACTERÍSTICAS DE COLOCACIÓN DE LA PIEZA",
                                                            anchor="center",
                                                            font=customtkinter.CTkFont(size=13, weight="bold"))
        self.select_position_label.grid(row=5, column=0, padx=(10, 10), pady=5, sticky="nwes", columnspan=7)

        self.line_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Línea",
                                                       anchor="center",
                                                       font=customtkinter.CTkFont(size=13, weight="bold"),
                                                       width=40)
        self.line_hidro_label.grid(row=6, column=0, padx=(10, 5), pady=(5, 0), sticky="nwes")
        self.line_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                             dynamic_resizing=False,
                                                             values=list_lines,
                                                             width=70)
        self.line_hidro_option.grid(row=7, column=0, padx=(10, 5), pady=(0, 10), sticky="ew")

        # existente / nueva pieza
        self.state_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Estado pieza",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=13, weight="bold"),
                                                        width=40)
        self.state_hidro_label.grid(row=6, column=1, padx=5, pady=(5, 0), sticky="nwes")
        self.state_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                              dynamic_resizing=False,
                                                              values=['Nueva', 'Existente'],
                                                              width=70)
        self.state_hidro_option.grid(row=7, column=1, padx=5, pady=(0, 10), sticky="ew")
        self.state_hidro_option.set('Nueva')

        # orientacion
        orientation_value = get_option_item_bd(select_data[0], select_data[1], "tbl_inv_orientacion",
                                               select_data[2],
                                               'orientacion')
        self.orientation_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Orientación",
                                                              anchor="center",
                                                              font=customtkinter.CTkFont(size=13, weight="bold"),
                                                              width=40)
        self.orientation_hidro_label.grid(row=6, column=2, padx=5, pady=(5, 0), sticky="nwes")
        self.orientation_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                                    dynamic_resizing=False,
                                                                    values=orientation_value,
                                                                    width=70)
        self.orientation_hidro_option.grid(row=7, column=2, padx=5, pady=(0, 10), sticky="ew")
        self.orientation_hidro_option.set(orientation_value[0])

        # material de la pieza
        material_value = get_option_item_bd(select_data[0], select_data[1], "tbl_inv_material", select_data[2],
                                            'material')
        self.material_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Material",
                                                           anchor="center",
                                                           font=customtkinter.CTkFont(size=13, weight="bold"),
                                                           width=40)
        self.material_hidro_label.grid(row=6, column=3, padx=5, pady=(10, 0), sticky="nwes")
        self.material_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                                 dynamic_resizing=False,
                                                                 values=material_value,
                                                                 width=70)
        self.material_hidro_option.grid(row=7, column=3, padx=5, pady=(0, 10), sticky="ew")
        self.material_hidro_option.set(material_value[0])
        self.material_button_hidro = customtkinter.CTkButton(self.filter_hidro_frame, text="Añadir nuevo material",
                                                             command=lambda: self.add_material_data(select_data),
                                                             fg_color="gray21")
        self.material_button_hidro.grid(row=7, column=4, padx=5, pady=(0, 10), sticky="ew")


        # Botón para añadir elementos
        self.add_button_hidro = customtkinter.CTkButton(self.filter_hidro_frame, text="Añadir",
                                                        command=lambda: self.add_item_hidro(select_data),
                                                        fg_color="green")
        self.add_button_hidro.grid(row=7, column=6, padx=(5, 10), pady=(0, 10), sticky="ew")

        # _-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_SUBFRAME PARA LISTBOX-HIDRÁULICA_-_-_-__-_-_-__-_-_-__-_-_-__-_-_-__-_-_-_
        self.listbox_hidro_frame = customtkinter.CTkFrame(self)
        self.listbox_hidro_frame.grid(row=5, column=0, rowspan=3, padx=10, pady=10, sticky="news")
        self.listbox_hidro_frame.grid_columnconfigure(0, weight=1)
        self.listbox_hidro_frame.grid_rowconfigure(0, weight=1)

        # Crear la lista (Listbox)
        self.listbox_hidro = tk.Listbox(self.listbox_hidro_frame, width=40, height=10)
        self.listbox_hidro.grid(row=0, column=0, sticky="news")

        # añadimos elementos existentes
        for item in element_hidro_data:
            self.listbox_hidro.insert(customtkinter.END, str(item))

        self.filter_hidro_options(select_data)
        self.update_connnection_hidro_options()

        # Botón para eliminar elementos seleccionados
        self.remove_button_hidro = customtkinter.CTkButton(self, text="Eliminar", command=self.remove_item_hidro,
                                                           fg_color="red")
        self.remove_button_hidro.grid(row=5, column=1, pady=15)
        # Flecha hacia arriba
        self.up_button_hidro = customtkinter.CTkButton(self, text="↑", command=self.move_up_hidro,
                                                       font=("default", 14, "bold"), )
        self.up_button_hidro.grid(row=6, column=1, pady=15)
        # Flecha hacia abajo
        self.down_button_hidro = customtkinter.CTkButton(self, text="↓", command=self.move_down_hidro,
                                                         font=("default", 14, "bold"))
        self.down_button_hidro.grid(row=7, column=1, pady=15)


        # boton de guardar
        save_path = parent_path +"/resources/images/guardar.png"
        self.save_image = customtkinter.CTkImage(Image.open(save_path))
        self.save_button = customtkinter.CTkButton(self, text="Guardar", image=self.save_image, compound="left",
                                                   fg_color="green",
                                                   font=("default", 14, "bold"),
                                                   command=self.save, height=40)
        self.save_button.grid(row=8, column=1, padx=10, pady=10, sticky="ew")


    def update_register_model_options(self, select_data):
        id_type_register = get_id_item_bd(select_data[0], select_data[1], 'tbl_cata_regis_tipo', select_data[2], 'tipo',
                                          self.type_register_option.get())
        register_model_value = get_option_item_sub_bd(select_data[0], select_data[1], 'tbl_catalogo_registros',
                                                      select_data[2], 'modelo',
                                                      id_type_register, 'id_tipo_registro')
        self.model_register_option.grid_remove()
        self.model_register_label2.grid_remove()

        if len(register_model_value) == 0:
            self.model_register_label2.grid(row=2, column=1, padx=(5, 5), pady=(0, 10), sticky="nwes")
        else:
            self.model_register_option.configure(values=register_model_value)
            self.model_register_option.set(register_model_value[0])
            self.model_register_option.grid(row=2, column=1, padx=(5, 5), pady=(0, 10), sticky="ew")


    def add_item_register(self, select_data):
        if int(self.n_item_register_entry.get()) == 1:
            n_item_register = self.n_item_register_entry.get() + " ud"
        else:
            n_item_register = self.n_item_register_entry.get() + " uds"
        id_type_register = get_id_item_bd(select_data[0], select_data[1], 'tbl_cata_regis_tipo', select_data[2], 'tipo',
                                          self.type_register_option.get())
        register_model_value = get_option_item_sub_bd(select_data[0], select_data[1], 'tbl_catalogo_registros',
                                                      select_data[2], 'modelo',
                                                      id_type_register, 'id_tipo_registro')
        if len(register_model_value) > 0:
            item_register = self.model_register_option.get()
            item_type = self.type_register_option.get()
            item = (item_register, n_item_register, item_type)
            self.listbox_register.insert(customtkinter.END, str(item))
        else:
            mssg = "Por favor, introduce un elemento existente"
            CTkMessagebox(title="Error Message!", message=mssg,
                          icon="cancel")


    def remove_item_register(self):
        selected_register_index = self.listbox_register.curselection()
        if selected_register_index:
            self.listbox_register.delete(selected_register_index)
        else:
            mssg = "Selecciona un elemento para eliminar"
            CTkMessagebox(title="Error Message!", message=mssg,
                          icon="cancel")


    def move_up_register(self):
        selected_register_index = self.listbox_register.curselection()
        if selected_register_index and selected_register_index[0] > 0:
            current_index = selected_register_index[0]
            item = self.listbox_register.get(current_index)
            self.listbox_register.delete(current_index)
            self.listbox_register.insert(current_index - 1, item)
            self.listbox_register.select_set(current_index - 1)
        else:
            mssg = "No se puede mover el elemento más arriba"
            CTkMessagebox(title="Error Message!", message=mssg,
                          icon="cancel")


    def move_down_register(self):
        selected_register_index = self.listbox_register.curselection()
        if selected_register_index and selected_register_index[0] < self.listbox_register.size() - 1:
            current_index = selected_register_index[0]
            item = self.listbox_register.get(current_index)
            self.listbox_register.delete(current_index)
            self.listbox_register.insert(current_index + 1, item)
            self.listbox_register.select_set(current_index + 1)
        else:
            mssg = "No se puede mover el elemento más abajo"
            CTkMessagebox(title="Error Message!", message=mssg,
                          icon="cancel")


    def add_hidro_filters (self,select_data, n_lines):

        self.filter_hidro_frame.destroy()
        self.filter_hidro_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.filter_hidro_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        self.filter_hidro_frame.grid_columnconfigure(0, weight=3)
        self.filter_hidro_frame.grid_columnconfigure(1, weight=3)
        self.filter_hidro_frame.grid_columnconfigure(2, weight=1)
        self.filter_hidro_frame.grid_columnconfigure(3, weight=1)
        self.filter_hidro_frame.grid_columnconfigure(4, weight=1)
        self.filter_hidro_frame.grid_columnconfigure(5, weight=1)
        self.filter_hidro_frame.grid_columnconfigure(6, weight=3)


        common_fg_color = "#171717"

        # ///////////////////////////////////añadir filtros/////////////////////////////////////////////////////////////
        self.hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="AÑADIR ELEMENTO HIDRÁULICO",
                                                  anchor="center",
                                                  font=customtkinter.CTkFont(size=13, weight="bold"))
        self.hidro_label.grid(row=0, column=0, padx=(10, 10), pady=5, sticky="nwes", columnspan=7)

        # Número de líneas
        self.n_lines_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Nº de lineas:",
                                                          anchor="center",
                                                          font=customtkinter.CTkFont(size=13, weight="bold"))
        self.n_lines_hidro_label.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="nwes", columnspan=2)

        n_lines_register_value = tk.StringVar(value=n_lines)
        self.n_lines_register_entry = customtkinter.CTkEntry(self.filter_hidro_frame,
                                                            textvariable=n_lines_register_value,
                                                            fg_color=common_fg_color, text_color="#FFFFFF")
        self.n_lines_register_entry.grid(row=1, column=2, padx=(5, 5), pady=5, sticky="nwes", columnspan =3)

        # Botón para añadir elementos
        self.n_lines_button = customtkinter.CTkButton(self.filter_hidro_frame, text="Definir número de líneas",
                                                      command=lambda :self.add_hidro_filters(select_data,self.n_lines_register_entry.get()))
        self.n_lines_button.grid(row=1, column=5, padx=(5, 10), pady=5, sticky="nwes", columnspan=2)

        #seleccion de modelo
        self.select_model_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="SELECCIÓN DE MODELO",
                                                  anchor="center",
                                                  font=customtkinter.CTkFont(size=13, weight="bold"))
        self.select_model_label.grid(row=2, column=0, padx=(10, 10), pady=5, sticky="nwes", columnspan=7)

        # familia
        self.family_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Familia",
                                                         anchor="center",
                                                         font=customtkinter.CTkFont(size=13, weight="bold"))
        self.family_hidro_label.grid(row=3, column=0, padx=5, pady=(5, 0), sticky="nwes")
        family_value = get_option_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_familia", select_data[2],
                                          'familia')
        family_value.sort(key=str.lower)
        self.family_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                               dynamic_resizing=False,
                                                               values=family_value,
                                                               command=lambda
                                                                   event: self.update_type_hidro_options(select_data))
        self.family_hidro_option.grid(row=4, column=0, padx=5, pady=(0, 5), sticky="ew")
        self.family_hidro_option.set(family_value[0])
        self.family_hidro_option.bind("<<ComboboxSelected>>", lambda event: self.update_type_hidro_options(select_data))

        self.filter_hidro_options(select_data)


        #seleccion de posición
        self.select_position_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="INDICAR CARACTERÍSTICAS DE COLOCACIÓN DE LA PIEZA",
                                                  anchor="center",
                                                  font=customtkinter.CTkFont(size=13, weight="bold"))
        self.select_position_label.grid(row=5, column=0, padx=(10, 10), pady=5, sticky="nwes", columnspan=7)
        # línea
        list_lines = []
        for i in range(int(n_lines)):
            n_line = i + 1
            item = "L-" + str(n_line)
            list_lines.append(item)
        self.line_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Línea",
                                                       anchor="center",
                                                       font=customtkinter.CTkFont(size=13, weight="bold"),
                                                       width=40)
        self.line_hidro_label.grid(row=6, column=0, padx=(10, 5), pady=(5, 0), sticky="nwes")
        self.line_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                             dynamic_resizing=False,
                                                             values=list_lines,
                                                             width=70)
        self.line_hidro_option.grid(row=7, column=0, padx=(10, 5), pady=(0, 10), sticky="ew")

        #existente / nueva pieza
        self.state_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Estado pieza",
                                                       anchor="center",
                                                       font=customtkinter.CTkFont(size=13, weight="bold"),
                                                       width=40)
        self.state_hidro_label.grid(row=6, column=1, padx=5, pady=(5, 0), sticky="nwes")
        self.state_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                             dynamic_resizing=False,
                                                             values=['Nueva', 'Existente'],
                                                             width=70)
        self.state_hidro_option.grid(row=7, column=1, padx=5, pady=(0, 10), sticky="ew")
        self.state_hidro_option.set('Nueva')

        #orientacion
        orientation_value = get_option_item_bd(select_data[0], select_data[1], "tbl_inv_orientacion", select_data[2],
                                          'orientacion')
        self.orientation_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Orientación",
                                                       anchor="center",
                                                       font=customtkinter.CTkFont(size=13, weight="bold"),
                                                       width=40)
        self.orientation_hidro_label.grid(row=6, column=2, padx=5, pady=(5, 0), sticky="nwes")
        self.orientation_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                             dynamic_resizing=False,
                                                             values=orientation_value,
                                                             width=70)
        self.orientation_hidro_option.grid(row=7, column=2, padx=5, pady=(0, 10), sticky="ew")
        self.orientation_hidro_option.set(orientation_value[0])

        #material de la pieza
        material_value = get_option_item_bd(select_data[0], select_data[1], "tbl_inv_material", select_data[2],
                                          'material')
        self.material_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Material",
                                                       anchor="center",
                                                       font=customtkinter.CTkFont(size=13, weight="bold"),
                                                       width=40)
        self.material_hidro_label.grid(row=6, column=3, padx=5, pady=(10, 0), sticky="nwes")
        self.material_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                             dynamic_resizing=False,
                                                             values=material_value,
                                                             width=70)
        self.material_hidro_option.grid(row=7, column=3, padx=5, pady=(0, 10), sticky="ew")
        self.material_hidro_option.set(material_value[0])
        self.material_button_hidro = customtkinter.CTkButton(self.filter_hidro_frame, text="Añadir nuevo material", command=lambda:self.add_material_data(select_data),
                                                  fg_color="gray21")
        self.material_button_hidro.grid(row=7, column=4, padx=5, pady=(0, 10), sticky="ew")

        self.update_connnection_hidro_options()

        # Botón para añadir elementos
        self.add_button_hidro = customtkinter.CTkButton(self.filter_hidro_frame, text="Añadir", command=lambda:self.add_item_hidro(select_data),
                                                  fg_color="green")
        self.add_button_hidro.grid(row=7, column=6, padx=(5, 10), pady=(0, 10), sticky="ew")


    def filter_hidro_options(self, select_data):
        type_hidro_data = self.update_type_hidro_options(select_data)
        dni_hidro_data = self.update_dni_hidro_options(type_hidro_data)
        dnf_hidro_data = self.update_dnf_hidro_options(dni_hidro_data)
        pn_hidro_data = self.update_pn_hidro_options(dnf_hidro_data)
        angle_hidro_data = self.update_angle_hidro_options(pn_hidro_data)
        self.update_model_hidro_options(angle_hidro_data)


    def update_type_hidro_options(self, select_data):
        family_option_value = self.family_hidro_option.get()
        if isinstance(family_option_value, str):
            family_option_value = [family_option_value]
        hidro_data = get_filter_data_bd(select_data[0], select_data[1], "vw_catalogo_hidraulica",
                                          select_data[2], "familia", family_option_value[0])
        type_hidro_value  = list(set([item[2] for item in hidro_data]))
        type_hidro_value.sort(key=str.lower)
        # tipo
        self.type_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Tipo",
                                                       anchor="center",
                                                       font=customtkinter.CTkFont(size=13, weight="bold"))
        self.type_hidro_label.grid(row=3, column=1, padx=5, pady=(5, 0), sticky="nwes")
        self.type_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                             dynamic_resizing=False,
                                                             values=type_hidro_value,
                                                             command=lambda event: self.update_dni_hidro_options(hidro_data))
        self.type_hidro_option.grid(row=4, column=1, padx=5, pady=(0, 5), sticky="ew")
        self.type_hidro_option.bind("<<ComboboxSelected>>", lambda event: self.update_dni_hidro_options(hidro_data))
        self.update_dni_hidro_options(hidro_data)
        return hidro_data


    def update_dni_hidro_options(self, hidro_data):
        type_option_value = self.type_hidro_option.get()
        if isinstance(type_option_value, str):
            type_option_value = [type_option_value]
        hidro_data = [sublist for sublist in hidro_data if type_option_value[0] in sublist]
        dni_hidro_value  = list(set([item[7] for item in hidro_data]))
        dni_hidro_value.sort(key=str.lower)
        # dn inicial
        self.dni_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="DN incial",
                                                      anchor="center",
                                                      font=customtkinter.CTkFont(size=13, weight="bold"))
        self.dni_hidro_label.grid(row=3, column=2, padx=5, pady=(5, 0), sticky="nwes")
        self.dni_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                            dynamic_resizing=False,
                                                            values=dni_hidro_value,
                                                            command=lambda event: self.update_dnf_hidro_options(hidro_data))
        self.dni_hidro_option.grid(row=4, column=2, padx=5, pady=(0, 5), sticky="ew")
        self.dni_hidro_option.bind("<<ComboboxSelected>>", lambda event: self.update_dnf_hidro_options(hidro_data))
        self.update_dnf_hidro_options(hidro_data)
        return hidro_data


    def update_dnf_hidro_options(self, hidro_data):
        dni_option_value = self.dni_hidro_option.get()
        if isinstance(dni_option_value, str):
            dni_option_value = [dni_option_value]
        hidro_data = [sublist for sublist in hidro_data if dni_option_value[0] in sublist]
        dnf_hidro_value  = list(set([item[8] for item in hidro_data]))
        dnf_hidro_value.sort(key=str.lower)
        # dn final
        self.dnf_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="DN final",
                                                      anchor="center",
                                                      font=customtkinter.CTkFont(size=13, weight="bold"))
        self.dnf_hidro_label.grid(row=3, column=3, padx=5, pady=(5, 0), sticky="nwes")
        self.dnf_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                            dynamic_resizing=False,
                                                            values=dnf_hidro_value,
                                                            command=lambda event: self.update_pn_hidro_options(hidro_data))
        self.dnf_hidro_option.grid(row=4, column=3, padx=5, pady=(0, 5), sticky="ew")
        self.dnf_hidro_option.bind("<<ComboboxSelected>>", lambda event: self.update_pn_hidro_options(hidro_data))
        self.update_pn_hidro_options(hidro_data)
        return hidro_data


    def update_pn_hidro_options(self, hidro_data):
        dnf_option_value = self.dnf_hidro_option.get()
        if isinstance(dnf_option_value, str):
            dnf_option_value = [dnf_option_value]
        hidro_data = [sublist for sublist in hidro_data if dnf_option_value[0] in sublist]
        pn_hidro_value = list(set([item[9] for item in hidro_data]))
        pn_hidro_value.sort(key=str.lower)
        # pn
        self.pn_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="PN",
                                                     anchor="center",
                                                     font=customtkinter.CTkFont(size=13, weight="bold"))
        self.pn_hidro_label.grid(row=3, column=4, padx=5, pady=(5, 0), sticky="nwes")
        self.pn_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                           dynamic_resizing=False,
                                                           values=pn_hidro_value,
                                                            command=lambda event: self.update_angle_hidro_options(hidro_data))
        self.pn_hidro_option.grid(row=4, column=4, padx=5, pady=(0, 5), sticky="ew")
        self.pn_hidro_option.bind("<<ComboboxSelected>>", lambda event: self.update_angle_hidro_options(hidro_data))
        self.update_angle_hidro_options(hidro_data)
        return hidro_data


    def update_angle_hidro_options(self, hidro_data):
        pn_option_value = self.pn_hidro_option.get()
        if isinstance(pn_option_value, str):
            pn_option_value = [pn_option_value]
        hidro_data = [sublist for sublist in hidro_data if pn_option_value[0] in sublist]
        angle_hidro_value = list(set([item[10] for item in hidro_data]))
        angle_hidro_value.sort(key=str.lower)
        # angulo
        self.angle_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Ángulo",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=13, weight="bold"))
        self.angle_hidro_label.grid(row=3, column=5, padx=5, pady=(5, 0), sticky="nwes")
        self.angle_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                              dynamic_resizing=False,
                                                              values=angle_hidro_value,
                                                            command=lambda event: self.update_model_hidro_options(hidro_data))
        self.angle_hidro_option.grid(row=4, column=5, padx=5, pady=(0, 5), sticky="ew")
        self.angle_hidro_option.bind("<<ComboboxSelected>>", lambda event: self.update_model_hidro_options(hidro_data))
        self.update_model_hidro_options(hidro_data)
        return hidro_data


    def update_model_hidro_options (self, hidro_data):
        angle_option_value = self.angle_hidro_option.get()
        if isinstance(angle_option_value, str):
            angle_option_value = [angle_option_value]
        hidro_data = [sublist for sublist in hidro_data if angle_option_value[0] in sublist]
        model_hidro_value = [item[5] for item in hidro_data]
        model_hidro_value.sort(key=str.lower)
        # modelo
        self.model_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame, text="Modelo",
                                                        anchor="center",
                                                        font=customtkinter.CTkFont(size=13, weight="bold"))
        self.model_hidro_label.grid(row=3, column=6, padx=(5,10), pady=(5, 0), sticky="nwes")
        self.model_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                              dynamic_resizing=False,
                                                              values=model_hidro_value)
        self.model_hidro_option.grid(row=4, column=6, padx=(5,10), pady=(0, 5), sticky="ew")


    def update_connnection_hidro_options(self):
        # comprobar si hay elementos ya añadidos
        n_items_hidro = self.listbox_hidro.get(0, tk.END)
        self.connection_hidro_label = customtkinter.CTkLabel(self.filter_hidro_frame,
                                                             text="Pieza conexión (aguas arriba)",
                                                             anchor="center",
                                                             font=customtkinter.CTkFont(size=13, weight="bold"))
        self.connection_hidro_label.grid(row=6, column=5, padx=5, pady=(5, 0), sticky="nwes")
        if len(n_items_hidro) == 0:
            # conexion con pieza agua arriba
            self.connection_hidro_label2 = customtkinter.CTkLabel(self.filter_hidro_frame,
                                                                 text="Debe agregar un nuevo elemento",
                                                                 anchor="center",
                                                                 font=customtkinter.CTkFont(size=13))
            self.connection_hidro_label2.grid(row=7, column=5, padx=5, pady=(0, 5), sticky="nwes")
        else:
            hidro_connection_value = []
            for item in n_items_hidro:
                item = item.replace('"', '').replace("'", "").replace("(", "").replace(")", "")
                list = item.split(",")
                hidro_connection_value.append(list[0] + " " + list[2])
            hidro_connection_value.sort(reverse=True)
            self.connection_hidro_option = customtkinter.CTkOptionMenu(self.filter_hidro_frame,
                                                                      dynamic_resizing=False,
                                                                      values=hidro_connection_value)
            self.connection_hidro_option.grid(row=7, column=5, padx=5, pady=(0, 5), sticky="ew")
            self.connection_hidro_option.set(hidro_connection_value[0])


    def add_item_hidro(self, select_data):
        line = self.line_hidro_option.get()
        id_type_hidro = get_id_item_bd(select_data[0], select_data[1], 'tbl_cata_hidra_tipo', select_data[2],
                                       'tipo_elemento',
                                       self.type_hidro_option.get())
        hidro_model_value = get_option_item_sub_bd(select_data[0], select_data[1], 'tbl_catalogo_hidraulica',
                                                   select_data[2], 'modelo',
                                                   id_type_hidro, 'id_tipo_hidraulica')
        hidro_items = self.listbox_hidro.get(0, tk.END)
        if len(hidro_items) == 0:
            if len(hidro_model_value) > 0:
                position = "P" + str(len(hidro_items) + 1)
                type = self.type_hidro_option.get()
                status = self.state_hidro_option.get()
                orientation = self.orientation_hidro_option.get()
                material = self.material_hidro_option.get()
                model = self.model_hidro_option.get()
                line_model = line + "_" + model
                item = (position, line, line_model, "input", type, status, orientation, material)
                self.listbox_hidro.insert(customtkinter.END, str(item))
            else:
                mssg = "Por favor, introduce un elemento existente."
                CTkMessagebox(title="Error Message!", message=mssg,
                              icon="cancel")
        else:
            hidro_added = self.connection_hidro_option.get()
            if len(hidro_model_value) > 0 and len(hidro_added) > 0:
                position = "P" + str(len(hidro_items) + 1)
                type = self.type_hidro_option.get()
                status = self.state_hidro_option.get()
                orientation = self.orientation_hidro_option.get()
                material = self.material_hidro_option.get()
                model = self.model_hidro_option.get()
                line_model = line + "_" + model
                connection = self.connection_hidro_option.get()
                item = (position, line, line_model, connection, type, status, orientation, material)
                self.listbox_hidro.insert(customtkinter.END, str(item))
            else:
                mssg = "Por favor, introduce un elemento existente."
                CTkMessagebox(title="Error Message!", message=mssg,
                              icon="cancel")

        self.update_connnection_hidro_options()


    def remove_item_hidro(self):
        selected_index_hidro = self.listbox_hidro.curselection()
        if selected_index_hidro:
            self.listbox_hidro.delete(selected_index_hidro)
            self.update_connnection_hidro_options()
        else:
            mssg = "Selecciona un elemento para eliminar."
            CTkMessagebox(title="Error Message!", message=mssg,
                          icon="cancel")


    def move_up_hidro(self):
        selected_index_hidro = self.listbox_hidro.curselection()
        if selected_index_hidro and selected_index_hidro[0] > 0:
            current_index = selected_index_hidro[0]
            item = self.listbox_hidro.get(current_index)
            self.listbox_hidro.delete(current_index)
            self.listbox_hidro.insert(current_index - 1, item)
            self.listbox_hidro.select_set(current_index - 1)
        else:
            mssg = "No se puede mover el elemento más arriba"
            CTkMessagebox(title="Error Message!", message=mssg,
                          icon="cancel")


    def move_down_hidro(self):
        selected_index_hidro = self.listbox_hidro.curselection()
        if selected_index_hidro and selected_index_hidro[0] < self.listbox_hidro.size() - 1:
            current_index = selected_index_hidro[0]
            item = self.listbox_hidro.get(current_index)
            self.listbox_hidro.delete(current_index)
            self.listbox_hidro.insert(current_index + 1, item)
            self.listbox_hidro.select_set(current_index + 1)
        else:
            mssg = "No se puede mover el elemento más abajo"
            CTkMessagebox(title="Error Message!", message=mssg,
                          icon="cancel")


    def add_material_data(self,select_data):
        appAux = AppItemAdd(select_data, 'tbl_inv_material','material','Material')
        appAux.grab_set()
        self.wait_window(appAux)
        material_value = get_option_item_bd(select_data[0], select_data[1], "tbl_inv_material", select_data[2], 'material')
        self.material_hidro_option.configure(values=material_value)



    def save(self):
        # Obtener todos los elementos del Listbox
        self.items_hidro = self.listbox_hidro.get(0, tk.END)
        self.items_register = self.listbox_register.get(0, tk.END)
        self.destroy()


    def get_items(self):
        return self.items_hidro, self.items_register





