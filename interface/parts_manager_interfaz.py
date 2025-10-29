# interface/parts_manager_interfaz.py
import customtkinter
from PIL import Image
from CTkMessagebox import CTkMessagebox
from tkinter import ttk, font as tkfont
from script.modulo_db import get_schemas_db, project_directory_db
import os

# Obtener rutas
current_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.dirname(current_path)

customtkinter.set_appearance_mode("dark")


# ✅ CONFIGURACIÓN GLOBAL DE TREEVIEW - Estilo mejorado
def configure_treeview_style():
    """Configura el estilo visual de todos los TreeView con mejor legibilidad"""
    style = ttk.Style()

    # Tema base
    style.theme_use('clam')

    # ========== ESTILO DE FILAS ==========
    style.configure("Treeview",
                    background="#2a2d2e",
                    foreground="white",
                    fieldbackground="#2a2d2e",
                    rowheight=35,  # ✅ Altura de fila aumentada
                    font=('Segoe UI', 11),  # ✅ Fuente más grande
                    borderwidth=0)

    # Colores alternos para filas (opcional)
    style.map('Treeview',
              background=[('selected', '#1f6aa5')],
              foreground=[('selected', 'white')])

    # ========== ESTILO DE HEADERS ==========
    style.configure("Treeview.Heading",
                    background="#1f6aa5",
                    foreground="white",
                    relief="flat",
                    font=('Segoe UI', 12, 'bold'),  # ✅ Headers más grandes y en negrita
                    borderwidth=1)

    style.map("Treeview.Heading",
              background=[('active', '#144870')],
              foreground=[('active', 'white')])

    # ========== BORDE DE CELDAS ==========
    # Para hacer las líneas divisorias más visibles
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])


customtkinter.set_appearance_mode("dark")

class AppPartsManager(customtkinter.CTk):
    width = 1600
    height = 900

    def __init__(self, access, schema):
        super().__init__()

        # ✅ CONFIGURAR ESTILO DE TREEVIEW PRIMERO
        configure_treeview_style()

        self.user = access[0]
        self.password = access[1]
        self.schema = schema

        self.title(f"HydroFlow Manager - Generador de Partes [{schema}]")

        self.user = access[0]
        self.password = access[1]
        self.schema = schema

        self.title(f"HydroFlow Manager - Generador de Partes [{schema}]")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        # Grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Cargar imágenes
        self._load_images()

        # Frame menú lateral
        self._create_sidebar()

        # Crear frames de pestañas
        self.resumen_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.partes_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.presupuesto_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.certificaciones_frame = customtkinter.CTkFrame(self, corner_radius=0)

        # Generar vistas
        self.main_resumen()
        self.main_partes()
        self.main_presupuesto()
        self.main_certificaciones()

        # Seleccionar frame por defecto
        self.select_frame_by_name("resumen")

    def _load_images(self):
        """Carga todas las imágenes necesarias"""
        logo_path = os.path.join(parent_path, "source/logo artanda2.png")
        self.lg_image = customtkinter.CTkImage(Image.open(logo_path), size=(200, 44))

        resumen_path = os.path.join(parent_path, "source/proyecto.png")
        self.resumen_image = customtkinter.CTkImage(Image.open(resumen_path), size=(30, 30))

        partes_path = os.path.join(parent_path, "source/herramienta.png")
        self.partes_image = customtkinter.CTkImage(Image.open(partes_path), size=(30, 30))

        budget_path = os.path.join(parent_path, "source/certificaciones.png")
        self.budget_image = customtkinter.CTkImage(Image.open(budget_path), size=(30, 30))

    def _create_sidebar(self):
        """Crea la barra lateral de navegación"""
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0, width=200)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")

        # Logo
        self.lg_image_label = customtkinter.CTkLabel(self.navigation_frame, text="", image=self.lg_image)
        self.lg_image_label.grid(row=0, column=0, padx=30, pady=(15, 15))

        # Título
        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame,
            text="Generador de Partes",
            compound="left",
            font=customtkinter.CTkFont(size=18, weight="bold")
        )
        self.navigation_frame_label.grid(row=1, column=0, padx=20, pady=5)

        # Botón Resumen
        self.resumen_button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=0, height=40,
            border_spacing=10, text="Resumen", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.resumen_image, font=customtkinter.CTkFont(size=15, weight="bold"),
            anchor="w", command=lambda: self.select_frame_by_name("resumen")
        )
        self.resumen_button.grid(row=2, column=0, sticky="ew")

        # Botón Partes
        self.partes_button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=0, height=40,
            border_spacing=10, text="Partes", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.partes_image, font=customtkinter.CTkFont(size=15, weight="bold"),
            anchor="w", command=lambda: self.select_frame_by_name("partes")
        )
        self.partes_button.grid(row=3, column=0, sticky="ew")

        # Botón Presupuesto
        self.presupuesto_button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=0, height=40,
            border_spacing=10, text="Presupuesto", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.budget_image, font=customtkinter.CTkFont(size=15, weight="bold"),
            anchor="w", command=lambda: self.select_frame_by_name("presupuesto")
        )
        self.presupuesto_button.grid(row=4, column=0, sticky="ew")

        # Botón Certificaciones
        self.certificaciones_button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=0, height=40,
            border_spacing=10, text="Certificaciones", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.budget_image, font=customtkinter.CTkFont(size=15, weight="bold"),
            anchor="w", command=lambda: self.select_frame_by_name("certificaciones")
        )
        self.certificaciones_button.grid(row=5, column=0, sticky="ew")

        # Espaciador
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        # Botón Volver
        self.back_button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=5, height=40,
            border_spacing=10, text="Volver",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            font=("default", 14, "bold"), anchor="center",
            command=self.back_to_selector
        )
        self.back_button.grid(row=8, padx=30, pady=(15, 15), sticky="nsew")

    def select_frame_by_name(self, name):
        """Cambia entre frames/pestañas"""
        # Actualizar colores de botones
        self.resumen_button.configure(fg_color=("gray75", "gray25") if name == "resumen" else "transparent")
        self.partes_button.configure(fg_color=("gray75", "gray25") if name == "partes" else "transparent")
        self.presupuesto_button.configure(fg_color=("gray75", "gray25") if name == "presupuesto" else "transparent")
        self.certificaciones_button.configure(
            fg_color=("gray75", "gray25") if name == "certificaciones" else "transparent")

        # Mostrar frame seleccionado
        if name == "resumen":
            self.resumen_frame.grid(row=0, column=1, padx=30, pady=(15, 15), sticky="nsew")
        else:
            self.resumen_frame.grid_forget()

        if name == "partes":
            self.partes_frame.grid(row=0, column=1, padx=30, pady=(15, 15), sticky="nsew")
        else:
            self.partes_frame.grid_forget()

        if name == "presupuesto":
            self.presupuesto_frame.grid(row=0, column=1, padx=30, pady=(15, 15), sticky="nsew")
        else:
            self.presupuesto_frame.grid_forget()

        if name == "certificaciones":
            self.certificaciones_frame.grid(row=0, column=1, padx=30, pady=(15, 15), sticky="nsew")
        else:
            self.certificaciones_frame.grid_forget()

    def main_resumen(self):
        """Pestaña Resumen - Lista de partes con KPIs"""
        from tkinter import ttk
        from script.modulo_db import get_partes_resumen
        from parts_list_window import open_parts_list

        self.resumen_frame.grid_columnconfigure(0, weight=1)
        self.resumen_frame.grid_rowconfigure(2, weight=1)

        # Título
        title = customtkinter.CTkLabel(
            self.resumen_frame,
            text="RESUMEN DE PARTES",
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=0, padx=30, pady=(20, 10), sticky="w", columnspan=3)

        # Botones superiores
        btn_frame = customtkinter.CTkFrame(self.resumen_frame, fg_color="transparent")
        btn_frame.grid(row=1, column=0, padx=30, pady=(0, 10), sticky="ew", columnspan=3)

        btn_add = customtkinter.CTkButton(
            btn_frame, text="➕ Añadir Parte",
            command=self._add_parte_resumen,
            fg_color="green", hover_color="#006400", width=150
        )
        btn_add.pack(side="left", padx=(0, 10))

        btn_refresh = customtkinter.CTkButton(
            btn_frame, text="🔄 Recargar",
            command=self._reload_resumen,
            width=120
        )
        btn_refresh.pack(side="left", padx=(0, 10))

        btn_list = customtkinter.CTkButton(
            btn_frame, text="📋 Ver Listado Completo",
            command=lambda: open_parts_list(self, self.user, self.password, self.schema),
            width=180
        )
        btn_list.pack(side="left")

        # Frame para tabla
        table_frame = customtkinter.CTkFrame(self.resumen_frame)
        table_frame.grid(row=2, column=0, padx=30, pady=(0, 20), sticky="nsew", columnspan=3)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Tabla de partes
        cols = ("id", "codigo", "descripcion", "estado", "ot", "red", "tipo", "cod_trabajo",
                "presupuesto", "certificado", "pendiente")
        self.tree_resumen = ttk.Treeview(table_frame, columns=cols, show="headings", height=20)

        # Configurar columnas
        col_widths = {
            "id": 40, "codigo": 80, "descripcion": 200, "estado": 80,
            "ot": 70, "red": 70, "tipo": 80, "cod_trabajo": 80,
            "presupuesto": 90, "certificado": 90, "pendiente": 90
        }

        for col in cols:
            header_text = {
                "id": "ID",
                "codigo": "Código",
                "descripcion": "Descripción",
                "estado": "Estado",
                "ot": "OT",
                "red": "Red",
                "tipo": "Tipo",
                "cod_trabajo": "Cód.Trabajo",
                "presupuesto": "Presup.",
                "certificado": "Certif.",
                "pendiente": "Pendiente"
            }
            self.tree_resumen.heading(col, text=header_text.get(col, col.title()))

        for col in cols:
            self.tree_resumen.heading(col, text=col.replace("_", " ").title())
            self.tree_resumen.column(col, width=col_widths.get(col, 100), anchor="center")  # ✅ center

                # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_resumen.yview)
        self.tree_resumen.configure(yscrollcommand=scrollbar.set)
        self.tree_resumen.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Botones inferiores
        bottom_frame = customtkinter.CTkFrame(self.resumen_frame, fg_color="transparent")
        bottom_frame.grid(row=3, column=0, padx=30, pady=(0, 20), sticky="ew", columnspan=3)

        btn_delete = customtkinter.CTkButton(
            bottom_frame, text="🗑️ Eliminar",
            command=self._delete_parte_resumen,
            fg_color="red", hover_color="#8B0000", width=120
        )
        btn_delete.pack(side="left", padx=(0, 10))

        btn_detail = customtkinter.CTkButton(
            bottom_frame, text="🔍 Ver Detalle",
            command=self._view_parte_detail,
            width=150
        )
        btn_detail.pack(side="left")

        # Cargar datos
        self._reload_resumen()

    def _reload_resumen(self):
        """Recarga los datos de la tabla de resumen"""
        from script.modulo_db import get_partes_resumen

        # Limpiar tabla
        for item in self.tree_resumen.get_children():
            self.tree_resumen.delete(item)

        try:
            rows = get_partes_resumen(self.user, self.password, self.schema)
            for row in rows:
                # row: id, codigo, descripcion, estado, ot, red, tipo, cod_trabajo,
                #      total_presupuesto, total_certificado, total_pendiente, creado_en, actualizado_en
                display_row = (
                    row[0],  # id
                    row[1],  # codigo
                    row[2] or "",  # descripcion
                    row[3] or "Pendiente",  # estado
                    row[4] or "",  # ot
                    row[5] or "",  # red
                    row[6] or "",  # tipo
                    row[7] or "",  # cod_trabajo
                    f"{float(row[8]):.2f}€" if row[8] else "0.00€",  # presupuesto
                    f"{float(row[9]):.2f}€" if row[9] else "0.00€",  # certificado
                    f"{float(row[10]):.2f}€" if row[10] else "0.00€",  # pendiente
                )
                self.tree_resumen.insert("", "end", values=display_row)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error cargando partes:\n{e}", icon="cancel")

    def _add_parte_resumen(self):
        """Abre ventana para añadir nuevo parte"""
        from interface.parts_interfaz import AppParts

        win = customtkinter.CTkToplevel(self)
        win.title("Añadir Nuevo Parte")
        win.geometry("820x420")
        win.lift()
        win.grab_set()
        win.focus()

        # Crear interfaz de añadir parte dentro de la ventana
        frame = customtkinter.CTkFrame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        from script.modulo_db import get_dim_all, add_parte_with_code

        # Cargar dimensiones
        dims = get_dim_all(self.user, self.password, self.schema)

        # OT
        customtkinter.CTkLabel(frame, text="OT:", font=("", 12, "bold")).grid(
            row=0, column=0, padx=10, pady=10, sticky="e")
        ot_values = dims.get("OT", ["Sin datos"])
        ot_menu = customtkinter.CTkOptionMenu(frame, values=ot_values)
        ot_menu.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ot_menu.set(ot_values[0])

        # Red
        customtkinter.CTkLabel(frame, text="Red:", font=("", 12, "bold")).grid(
            row=0, column=2, padx=10, pady=10, sticky="e")
        red_values = dims.get("RED", ["Sin datos"])
        red_menu = customtkinter.CTkOptionMenu(frame, values=red_values)
        red_menu.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
        red_menu.set(red_values[0])

        # Tipo
        customtkinter.CTkLabel(frame, text="Tipo:", font=("", 12, "bold")).grid(
            row=1, column=0, padx=10, pady=10, sticky="e")
        tipo_values = dims.get("TIPO_TRABAJO", ["Sin datos"])
        tipo_menu = customtkinter.CTkOptionMenu(frame, values=tipo_values)
        tipo_menu.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        tipo_menu.set(tipo_values[0])

        # Código
        customtkinter.CTkLabel(frame, text="Código:", font=("", 12, "bold")).grid(
            row=1, column=2, padx=10, pady=10, sticky="e")
        cod_values = dims.get("COD_TRABAJO", ["Sin datos"])
        cod_menu = customtkinter.CTkOptionMenu(frame, values=cod_values)
        cod_menu.grid(row=1, column=3, padx=10, pady=10, sticky="ew")
        cod_menu.set(cod_values[0])

        # Descripción
        customtkinter.CTkLabel(frame, text="Descripción:", font=("", 12, "bold")).grid(
            row=2, column=0, padx=10, pady=10, sticky="e")
        desc_entry = customtkinter.CTkEntry(frame, width=400)
        desc_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=10, sticky="ew")

        def guardar():
            try:
                # Validar que no sean valores "Sin datos"
                if "Sin datos" in ot_menu.get() or "Sin datos" in red_menu.get() or \
                   "Sin datos" in tipo_menu.get() or "Sin datos" in cod_menu.get():
                    CTkMessagebox(title="Error",
                                message="No se puede crear un parte sin configurar primero las dimensiones.\n\n"
                                        "Por favor, ve a 'Configuración' para añadir códigos de OT, Red, Tipo y Código de trabajo.",
                                icon="cancel")
                    return

                ot_id = int(ot_menu.get().split(" - ")[0])
                red_id = int(red_menu.get().split(" - ")[0])
                tipo_id = int(tipo_menu.get().split(" - ")[0])
                cod_id = int(cod_menu.get().split(" - ")[0])
                desc = desc_entry.get().strip() or None

                new_id, codigo = add_parte_with_code(
                    self.user, self.password, self.schema,
                    ot_id, red_id, tipo_id, cod_id, desc
                )

                CTkMessagebox(title="Éxito", message=f"Parte {codigo} creado", icon="check")
                win.destroy()
                self._reload_resumen()
            except Exception as e:
                CTkMessagebox(title="Error", message=f"Error:\n{e}", icon="cancel")

        btn_save = customtkinter.CTkButton(frame, text="Guardar", command=guardar,
                                           fg_color="green", hover_color="#006400")
        btn_save.grid(row=3, column=0, columnspan=4, padx=20, pady=20, sticky="ew")

    def _delete_parte_resumen(self):
        """Elimina el parte seleccionado"""
        from script.modulo_db import delete_parte

        selected = self.tree_resumen.selection()
        if not selected:
            CTkMessagebox(title="Aviso", message="Seleccione un parte", icon="info")
            return

        item = self.tree_resumen.item(selected[0])
        values = item['values']
        parte_id = values[0]
        codigo = values[1]

        msg = CTkMessagebox(
            title="Confirmar",
            message=f"¿Eliminar parte {codigo}?\n\nEsta acción no se puede deshacer.",
            icon="warning",
            option_1="Cancelar",
            option_2="Eliminar"
        )

        if msg.get() == "Eliminar":
            try:
                delete_parte(self.user, self.password, self.schema, parte_id)
                CTkMessagebox(title="Éxito", message=f"Parte {codigo} eliminado", icon="check")
                self._reload_resumen()
            except Exception as e:
                CTkMessagebox(title="Error", message=f"Error:\n{e}", icon="cancel")

    def _view_parte_detail(self):
        """Abre la pestaña Partes con el parte seleccionado"""
        selected = self.tree_resumen.selection()
        if not selected:
            CTkMessagebox(title="Aviso", message="Seleccione un parte", icon="info")
            return

        item = self.tree_resumen.item(selected[0])
        parte_id = item['values'][0]

        # Guardar el ID seleccionado y cambiar a pestaña Partes
        self.selected_parte_id = parte_id
        self.select_frame_by_name("partes")
        self._load_parte_selected()

    def main_partes(self):
        """Pestaña Partes - Con sub-tabs internas"""
        from script.modulo_db import get_partes_resumen

        self.partes_frame.grid_columnconfigure(0, weight=1)
        self.partes_frame.grid_rowconfigure(2, weight=1)

        # Título
        title = customtkinter.CTkLabel(
            self.partes_frame,
            text="GESTIÓN DE PARTES",
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=0, padx=30, pady=(20, 10), sticky="w", columnspan=2)

        # Selector de parte
        selector_frame = customtkinter.CTkFrame(self.partes_frame, fg_color="transparent")
        selector_frame.grid(row=1, column=0, padx=30, pady=(0, 10), sticky="ew", columnspan=2)
        selector_frame.grid_columnconfigure(1, weight=1)

        customtkinter.CTkLabel(selector_frame, text="Seleccionar Parte:",
                               font=("", 14, "bold")).grid(row=0, column=0, padx=(0, 10), sticky="e")

        # Cargar lista de partes
        try:
            partes_data = get_partes_resumen(self.user, self.password, self.schema)
            partes_list = [f"{row[0]} - {row[1]} | {row[4]} | {row[5]} | {row[2] or 'Sin desc.'}"
                           for row in partes_data]  # id - codigo | ot | red | descripcion
        except:
            partes_list = ["Sin partes"]

        self.partes_selector = customtkinter.CTkOptionMenu(
            selector_frame,
            values=partes_list if partes_list else ["Sin partes"],
            command=lambda x: self._load_parte_tabs()
        )
        self.partes_selector.grid(row=0, column=1, sticky="ew", padx=(0, 10))

        if partes_list and hasattr(self, 'selected_parte_id'):
            # Si viene desde Resumen con un parte seleccionado
            for item in partes_list:
                if item.startswith(f"{self.selected_parte_id} -"):
                    self.partes_selector.set(item)
                    break
        elif partes_list:
            self.partes_selector.set(partes_list[0])

        btn_reload = customtkinter.CTkButton(
            selector_frame, text="🔄", width=40,
            command=lambda: self._reload_partes_selector()
        )
        btn_reload.grid(row=0, column=2)

        # Frame principal que contendrá los sub-tabs
        self.partes_content_frame = customtkinter.CTkFrame(self.partes_frame)
        self.partes_content_frame.grid(row=2, column=0, padx=30, pady=(0, 20), sticky="nsew", columnspan=2)
        self.partes_content_frame.grid_columnconfigure(0, weight=1)
        self.partes_content_frame.grid_rowconfigure(1, weight=1)

        # Sub-tabs
        self.partes_subtabs = customtkinter.CTkTabview(self.partes_content_frame)
        self.partes_subtabs.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Crear las 3 pestañas
        self.partes_subtabs.add("📝 Datos Básicos")
        self.partes_subtabs.add("💰 Presupuesto")
        self.partes_subtabs.add("📅 Certificaciones")

        # Cargar datos si hay partes
        if partes_list and partes_list[0] != "Sin partes":
            self._load_parte_tabs()

    def _reload_partes_selector(self):
        """Recarga el selector de partes"""
        from script.modulo_db import get_partes_resumen

        try:
            partes_data = get_partes_resumen(self.user, self.password, self.schema)
            partes_list = [f"{row[0]} - {row[1]} | {row[4]} | {row[5]} | {row[2] or 'Sin desc.'}"
                           for row in partes_data]

            if partes_list:
                self.partes_selector.configure(values=partes_list)
                self.partes_selector.set(partes_list[0])
                self._load_parte_tabs()
            else:
                self.partes_selector.configure(values=["Sin partes"])
                self.partes_selector.set("Sin partes")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error recargando:\n{e}", icon="cancel")

    def _load_parte_tabs(self):
        """Carga el contenido de las 3 sub-pestañas"""
        selected = self.partes_selector.get()
        if selected == "Sin partes" or not selected:
            return

        try:
            parte_id = int(selected.split(" - ")[0])
            self.current_parte_id = parte_id

            # Cargar cada pestaña
            self._load_datos_basicos_tab(parte_id)
            self._load_presupuesto_tab(parte_id)
            self._load_certificaciones_tab(parte_id)

        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error cargando parte:\n{e}", icon="cancel")

    def _load_datos_basicos_tab(self, parte_id):
        """Carga la pestaña de Datos Básicos - Layout optimizado en 2 columnas"""
        from script.modulo_db import get_parte_detail, get_dim_all

        tab = self.partes_subtabs.tab("📝 Datos Básicos")

        # Limpiar
        for widget in tab.winfo_children():
            widget.destroy()

        # Frame principal SIN scroll
        main_frame = customtkinter.CTkFrame(tab, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        try:
            parte_data = get_parte_detail(self.user, self.password, self.schema, parte_id)
            if not parte_data:
                customtkinter.CTkLabel(main_frame, text="❌ No se encontró el parte").pack(pady=20)
                return

            dims = get_dim_all(self.user, self.password, self.schema)

            # ============ COLUMNA IZQUIERDA ============
            left_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
            left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
            left_frame.grid_columnconfigure(1, weight=1)

            row_left = 0

            # Header
            customtkinter.CTkLabel(
                left_frame, text="DATOS DEL PARTE", font=("", 16, "bold")
            ).grid(row=row_left, column=0, columnspan=2, pady=(0, 15), sticky="w")
            row_left += 1

            # ID
            customtkinter.CTkLabel(left_frame, text="ID:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")
            customtkinter.CTkLabel(left_frame, text=str(parte_data[0])).grid(
                row=row_left, column=1, padx=5, pady=8, sticky="w")
            row_left += 1

            # Código
            customtkinter.CTkLabel(left_frame, text="Código:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")
            customtkinter.CTkLabel(
                left_frame, text=parte_data[1], font=("", 14, "bold"), text_color="#4CAF50"
            ).grid(row=row_left, column=1, padx=5, pady=8, sticky="w")
            row_left += 1

            # Separador
            customtkinter.CTkFrame(left_frame, height=2, fg_color="gray40").grid(
                row=row_left, column=0, columnspan=2, pady=15, sticky="ew")
            row_left += 1

            # Estado
            customtkinter.CTkLabel(left_frame, text="Estado:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")
            self.estado_var = customtkinter.StringVar(value=parte_data[3] or "Pendiente")
            self.estado_menu = customtkinter.CTkOptionMenu(
                left_frame, variable=self.estado_var,
                values=["Pendiente", "En curso", "Finalizado", "Cerrado"]
            )
            self.estado_menu.grid(row=row_left, column=1, padx=5, pady=8, sticky="ew")
            row_left += 1

            # OT
            customtkinter.CTkLabel(left_frame, text="OT:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")
            self.ot_menu = customtkinter.CTkOptionMenu(left_frame, values=dims.get("OT", []))
            self.ot_menu.grid(row=row_left, column=1, padx=5, pady=8, sticky="ew")
            for item in dims.get("OT", []):
                if item.startswith(f"{parte_data[4]} -"):
                    self.ot_menu.set(item)
                    break
            row_left += 1

            # Red
            customtkinter.CTkLabel(left_frame, text="Red:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")
            self.red_menu = customtkinter.CTkOptionMenu(left_frame, values=dims.get("RED", []))
            self.red_menu.grid(row=row_left, column=1, padx=5, pady=8, sticky="ew")
            for item in dims.get("RED", []):
                if item.startswith(f"{parte_data[5]} -"):
                    self.red_menu.set(item)
                    break
            row_left += 1

            # Tipo
            customtkinter.CTkLabel(left_frame, text="Tipo Trabajo:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")
            self.tipo_menu = customtkinter.CTkOptionMenu(left_frame, values=dims.get("TIPO_TRABAJO", []))
            self.tipo_menu.grid(row=row_left, column=1, padx=5, pady=8, sticky="ew")
            for item in dims.get("TIPO_TRABAJO", []):
                if item.startswith(f"{parte_data[6]} -"):
                    self.tipo_menu.set(item)
                    break
            row_left += 1

            # Código trabajo
            customtkinter.CTkLabel(left_frame, text="Código Trabajo:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")
            self.cod_menu = customtkinter.CTkOptionMenu(left_frame, values=dims.get("COD_TRABAJO", []))
            self.cod_menu.grid(row=row_left, column=1, padx=5, pady=8, sticky="ew")
            for item in dims.get("COD_TRABAJO", []):
                if item.startswith(f"{parte_data[7]} -"):
                    self.cod_menu.set(item)
                    break
            row_left += 1

            # Fechas info
            customtkinter.CTkFrame(left_frame, height=2, fg_color="gray40").grid(
                row=row_left, column=0, columnspan=2, pady=15, sticky="ew")
            row_left += 1

            customtkinter.CTkLabel(
                left_frame, text=f"📅 Creado: {parte_data[10]}",
                font=("", 10), text_color="gray"
            ).grid(row=row_left, column=0, columnspan=2, padx=5, pady=3, sticky="w")
            row_left += 1

            if parte_data[11]:
                customtkinter.CTkLabel(
                    left_frame, text=f"🔄 Actualizado: {parte_data[11]}",
                    font=("", 10), text_color="gray"
                ).grid(row=row_left, column=0, columnspan=2, padx=5, pady=3, sticky="w")

            # ============ COLUMNA DERECHA ============
            right_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
            right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
            right_frame.grid_columnconfigure(0, weight=1)
            right_frame.grid_rowconfigure(1, weight=1)
            right_frame.grid_rowconfigure(3, weight=1)

            # Descripción
            customtkinter.CTkLabel(
                right_frame, text="Descripción:", font=("", 13, "bold")
            ).grid(row=0, column=0, padx=5, pady=(0, 5), sticky="w")

            self.desc_text = customtkinter.CTkTextbox(right_frame, height=200)
            self.desc_text.grid(row=1, column=0, padx=5, pady=(0, 15), sticky="nsew")
            if parte_data[2]:
                self.desc_text.insert("1.0", parte_data[2])

            # Observaciones
            customtkinter.CTkLabel(
                right_frame, text="Observaciones:", font=("", 13, "bold")
            ).grid(row=2, column=0, padx=5, pady=(0, 5), sticky="w")

            self.obs_text = customtkinter.CTkTextbox(right_frame, height=200)
            self.obs_text.grid(row=3, column=0, padx=5, pady=(0, 15), sticky="nsew")
            if parte_data[9]:
                self.obs_text.insert("1.0", parte_data[9])

            # Botón guardar (span completo)
            btn_save = customtkinter.CTkButton(
                right_frame, text="💾 GUARDAR CAMBIOS",
                command=lambda: self._confirm_and_save_parte(parte_id),
                fg_color="green", hover_color="#006400",
                height=50, font=("", 16, "bold")
            )
            btn_save.grid(row=4, column=0, padx=5, pady=15, sticky="ew")

        except Exception as e:
            import traceback
            print(f"ERROR:\n{traceback.format_exc()}")
            customtkinter.CTkLabel(main_frame, text=f"❌ Error: {e}").pack(pady=20)

    def _confirm_and_save_parte(self, parte_id):
        """Solicita confirmación antes de guardar"""
        msg = CTkMessagebox(
            title="Confirmar cambios",
            message="¿Desea guardar los cambios realizados en el parte?",
            icon="question",
            option_1="Cancelar",
            option_2="Guardar"
        )

        if msg.get() == "Guardar":
            self._save_parte_changes(parte_id)

    def _save_parte_changes(self, parte_id):
        """Guarda los cambios del parte"""
        from script.modulo_db import mod_parte_item

        try:
            # Validar que existan los widgets
            if not hasattr(self, 'ot_menu'):
                CTkMessagebox(title="Error", message="Error: Formulario no cargado correctamente", icon="cancel")
                return

            # Extraer IDs de los menús (formato: "id - nombre")
            ot_text = self.ot_menu.get()
            red_text = self.red_menu.get()
            tipo_text = self.tipo_menu.get()
            cod_text = self.cod_menu.get()

            print(f"DEBUG - Valores de menús:")
            print(f"  OT: {ot_text}")
            print(f"  Red: {red_text}")
            print(f"  Tipo: {tipo_text}")
            print(f"  Cod: {cod_text}")

            # Extraer IDs
            try:
                ot_id = int(ot_text.split(" - ")[0])
                red_id = int(red_text.split(" - ")[0])
                tipo_id = int(tipo_text.split(" - ")[0])
                cod_id = int(cod_text.split(" - ")[0])
            except Exception as e:
                CTkMessagebox(
                    title="Error",
                    message=f"Error extrayendo IDs de los menús:\n{e}",
                    icon="cancel"
                )
                return

            # Obtener textos
            descripcion = self.desc_text.get("1.0", "end-1c").strip() or None
            estado = self.estado_var.get()
            observaciones = self.obs_text.get("1.0", "end-1c").strip() or None

            print(f"DEBUG - Guardando parte {parte_id}:")
            print(f"  IDs: OT={ot_id}, Red={red_id}, Tipo={tipo_id}, Cod={cod_id}")
            print(f"  Estado: {estado}")
            print(f"  Descripción: {descripcion[:50] if descripcion else 'None'}")
            print(f"  Observaciones: {observaciones[:50] if observaciones else 'None'}")

            result = mod_parte_item(
                self.user, self.password, self.schema, parte_id,
                ot_id, red_id, tipo_id, cod_id, descripcion, estado, observaciones
            )

            print(f"DEBUG - Resultado: {result}")

            if result == "ok":
                CTkMessagebox(
                    title="Éxito",
                    message="✅ Parte actualizado correctamente",
                    icon="check"
                )
                # Recargar datos
                self._load_parte_tabs()
                if hasattr(self, 'tree_resumen'):
                    self._reload_resumen()
            else:
                CTkMessagebox(
                    title="Error",
                    message=f"❌ Error al guardar:\n\n{result}",
                    icon="cancel"
                )
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            print(f"ERROR completo en _save_parte_changes:\n{error_detail}")
            CTkMessagebox(
                title="Error",
                message=f"❌ Error guardando:\n\n{str(e)}\n\nVer consola para detalles",
                icon="cancel"
            )

    def _load_presupuesto_tab(self, parte_id):
        """Carga la pestaña de Presupuesto (solo lectura)"""
        from tkinter import ttk
        from script.modulo_db import get_part_presupuesto

        tab = self.partes_subtabs.tab("💰 Presupuesto")

        # Limpiar
        for widget in tab.winfo_children():
            widget.destroy()

        # Frame principal
        main_frame = customtkinter.CTkFrame(tab, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Info y botón
        top_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        customtkinter.CTkLabel(top_frame,
                               text="Vista de solo lectura. Para editar, usa la pestaña 'Presupuesto' principal.",
                               font=("", 11), text_color="gray").pack(side="left", padx=5)

        btn_ir = customtkinter.CTkButton(
            top_frame, text="➡️ Ir a Presupuesto",
            command=lambda: self._goto_presupuesto(parte_id),
            width=150
        )
        btn_ir.pack(side="right", padx=5)

        # Tabla
        table_frame = customtkinter.CTkFrame(main_frame)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        cols = ("id", "codigo", "resumen", "unidad", "cantidad", "precio_unit", "coste")
        tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)

        tree.heading("id", text="ID")
        tree.heading("codigo", text="Código")
        tree.heading("resumen", text="Resumen")
        tree.heading("unidad", text="Ud")
        tree.heading("cantidad", text="Cantidad")
        tree.heading("precio_unit", text="Precio Unit.")
        tree.heading("coste", text="Coste")

        tree.column("id", width=40, anchor="center")
        tree.column("codigo", width=90, anchor="center")
        tree.column("resumen", width=250, anchor="w")
        tree.column("unidad", width=40, anchor="center")
        tree.column("cantidad", width=70, anchor="e")
        tree.column("precio_unit", width=80, anchor="e")
        tree.column("coste", width=80, anchor="e")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Cargar datos
        try:
            rows = get_part_presupuesto(self.user, self.password, self.schema, parte_id)
            total = 0
            for row in rows:
                # row: id, parte_id, codigo_parte, codigo_partida, resumen, descripcion, unidad, cantidad, precio_unit, coste
                display = (
                    row[0], row[3], row[4] or "", row[6] or "",
                    f"{float(row[7]):.3f}", f"{float(row[8]):.2f}€", f"{float(row[9]):.2f}€"
                )
                tree.insert("", "end", values=display)
                total += float(row[9])

            # Total
            total_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
            total_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))

            customtkinter.CTkLabel(total_frame, text="TOTAL PRESUPUESTO:",
                                   font=("", 14, "bold")).pack(side="left", padx=10)
            customtkinter.CTkLabel(total_frame, text=f"{total:.2f}€",
                                   font=("", 16, "bold"), text_color="#4CAF50").pack(side="left")

        except Exception as e:
            customtkinter.CTkLabel(table_frame, text=f"❌ Error: {e}").pack(pady=20)

    def _load_certificaciones_tab(self, parte_id):
        """Carga la pestaña de Certificaciones (solo lectura)"""
        from tkinter import ttk
        from script.modulo_db import get_part_cert_certificadas

        tab = self.partes_subtabs.tab("📅 Certificaciones")

        # Limpiar
        for widget in tab.winfo_children():
            widget.destroy()

        # Frame principal
        main_frame = customtkinter.CTkFrame(tab, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Info y botón
        top_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        customtkinter.CTkLabel(top_frame,
                               text="Vista de solo lectura. Para certificar, usa la pestaña 'Certificaciones' principal.",
                               font=("", 11), text_color="gray").pack(side="left", padx=5)

        btn_ir = customtkinter.CTkButton(
            top_frame, text="➡️ Ir a Certificaciones",
            command=lambda: self._goto_certificaciones(parte_id),
            width=180
        )
        btn_ir.pack(side="right", padx=5)

        # Tabla
        table_frame = customtkinter.CTkFrame(main_frame)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        cols = ("id", "codigo", "resumen", "unidad", "cantidad", "precio", "coste", "fecha")
        tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)

        tree.heading("id", text="ID")
        tree.heading("codigo", text="Código")
        tree.heading("resumen", text="Resumen")
        tree.heading("unidad", text="Ud")
        tree.heading("cantidad", text="Cantidad")
        tree.heading("precio", text="Precio")
        tree.heading("coste", text="Coste")
        tree.heading("fecha", text="Fecha")

        tree.column("id", width=40, anchor="center")
        tree.column("codigo", width=90, anchor="center")
        tree.column("resumen", width=220, anchor="w")
        tree.column("unidad", width=40, anchor="center")
        tree.column("cantidad", width=70, anchor="e")
        tree.column("precio", width=80, anchor="e")
        tree.column("coste", width=80, anchor="e")
        tree.column("fecha", width=90, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Cargar datos
        try:
            rows = get_part_cert_certificadas(self.user, self.password, self.schema, parte_id)
            total = 0
            for row in rows:
                # row: id, parte_id, codigo_parte, codigo_partida, resumen, unidad, cantidad_cert, precio_unit, coste_cert, fecha_certificacion, ...
                display = (
                    row[0], row[3], row[4] or "", row[5] or "",
                    f"{float(row[6]):.3f}", f"{float(row[7]):.2f}€", f"{float(row[8]):.2f}€",
                    str(row[9])
                )
                tree.insert("", "end", values=display)
                total += float(row[8])

            # Total
            total_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
            total_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))

            customtkinter.CTkLabel(total_frame, text="TOTAL CERTIFICADO:",
                                   font=("", 14, "bold")).pack(side="left", padx=10)
            customtkinter.CTkLabel(total_frame, text=f"{total:.2f}€",
                                   font=("", 16, "bold"), text_color="#2196F3").pack(side="left")

        except Exception as e:
            customtkinter.CTkLabel(table_frame, text=f"❌ Error: {e}").pack(pady=20)

    def _save_parte_changes(self, parte_id):
        """Guarda los cambios del parte"""
        from script.modulo_db import mod_parte_item

        try:
            ot_id = int(self.ot_menu.get().split(" - ")[0])
            red_id = int(self.red_menu.get().split(" - ")[0])
            tipo_id = int(self.tipo_menu.get().split(" - ")[0])
            cod_id = int(self.cod_menu.get().split(" - ")[0])
            descripcion = self.desc_text.get("1.0", "end-1c").strip() or None
            estado = self.estado_var.get()
            observaciones = self.obs_text.get("1.0", "end-1c").strip() or None

            result = mod_parte_item(
                self.user, self.password, self.schema, parte_id,
                ot_id, red_id, tipo_id, cod_id, descripcion, estado, observaciones
            )

            if result == "ok":
                CTkMessagebox(title="Éxito", message="✅ Parte actualizado correctamente", icon="check")
                self._reload_partes_selector()
                # Recargar resumen si está visible
                if hasattr(self, 'tree_resumen'):
                    self._reload_resumen()
            else:
                CTkMessagebox(title="Error", message=f"Error:\n{result}", icon="cancel")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error guardando:\n{e}", icon="cancel")

    def _load_parte_selected(self):
        """Carga los datos del parte seleccionado"""
        from script.modulo_db import get_parte_detail, get_dim_all

        # Limpiar frame
        for widget in self.datos_parte_frame.winfo_children():
            widget.destroy()

        selected = self.partes_selector.get()
        if selected == "Sin partes" or not selected:
            return

        try:
            parte_id = int(selected.split(" - ")[0])
        except:
            return

        try:
            # Obtener datos del parte
            parte_data = get_parte_detail(self.user, self.password, self.schema, parte_id)
            if not parte_data:
                CTkMessagebox(title="Error", message="No se encontró el parte", icon="warning")
                return

            # parte_data: id, codigo, descripcion, estado, ot_id, red_id, tipo_trabajo_id,
            #             cod_trabajo_id, municipio_id, observaciones, creado_en, actualizado_en

            # Obtener dimensiones
            dims = get_dim_all(self.user, self.password, self.schema)

            # Título
            customtkinter.CTkLabel(
                self.datos_parte_frame,
                text=f"PARTE: {parte_data[1]}",
                font=("", 16, "bold")
            ).grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="w")

            row = 1

            # ID (solo lectura)
            customtkinter.CTkLabel(self.datos_parte_frame, text="ID:",
                                   font=("", 12, "bold")).grid(row=row, column=0, padx=10, pady=8, sticky="e")
            id_label = customtkinter.CTkLabel(self.datos_parte_frame, text=str(parte_data[0]))
            id_label.grid(row=row, column=1, padx=10, pady=8, sticky="w")
            row += 1

            # Código (solo lectura)
            customtkinter.CTkLabel(self.datos_parte_frame, text="Código:",
                                   font=("", 12, "bold")).grid(row=row, column=0, padx=10, pady=8, sticky="e")
            codigo_label = customtkinter.CTkLabel(self.datos_parte_frame, text=parte_data[1])
            codigo_label.grid(row=row, column=1, padx=10, pady=8, sticky="w")
            row += 1

            # Estado
            customtkinter.CTkLabel(self.datos_parte_frame, text="Estado:",
                                   font=("", 12, "bold")).grid(row=row, column=0, padx=10, pady=8, sticky="e")
            self.estado_var = customtkinter.StringVar(value=parte_data[3] or "Pendiente")
            estado_menu = customtkinter.CTkOptionMenu(
                self.datos_parte_frame,
                variable=self.estado_var,
                values=["Pendiente", "En curso", "Finalizado", "Cerrado"]
            )
            estado_menu.grid(row=row, column=1, padx=10, pady=8, sticky="ew")
            row += 1

            # OT
            customtkinter.CTkLabel(self.datos_parte_frame, text="OT:",
                                   font=("", 12, "bold")).grid(row=row, column=0, padx=10, pady=8, sticky="e")
            self.ot_menu = customtkinter.CTkOptionMenu(self.datos_parte_frame, values=dims.get("OT", []))
            self.ot_menu.grid(row=row, column=1, padx=10, pady=8, sticky="ew")
            # Preseleccionar valor actual
            for item in dims.get("OT", []):
                if item.startswith(f"{parte_data[4]} -"):
                    self.ot_menu.set(item)
                    break
            row += 1

            # Red
            customtkinter.CTkLabel(self.datos_parte_frame, text="Red:",
                                   font=("", 12, "bold")).grid(row=row, column=0, padx=10, pady=8, sticky="e")
            self.red_menu = customtkinter.CTkOptionMenu(self.datos_parte_frame, values=dims.get("RED", []))
            self.red_menu.grid(row=row, column=1, padx=10, pady=8, sticky="ew")
            for item in dims.get("RED", []):
                if item.startswith(f"{parte_data[5]} -"):
                    self.red_menu.set(item)
                    break
            row += 1

            # Tipo trabajo
            customtkinter.CTkLabel(self.datos_parte_frame, text="Tipo Trabajo:",
                                   font=("", 12, "bold")).grid(row=row, column=0, padx=10, pady=8, sticky="e")
            self.tipo_menu = customtkinter.CTkOptionMenu(self.datos_parte_frame, values=dims.get("TIPO_TRABAJO", []))
            self.tipo_menu.grid(row=row, column=1, padx=10, pady=8, sticky="ew")
            for item in dims.get("TIPO_TRABAJO", []):
                if item.startswith(f"{parte_data[6]} -"):
                    self.tipo_menu.set(item)
                    break
            row += 1

            # Código trabajo
            customtkinter.CTkLabel(self.datos_parte_frame, text="Código Trabajo:",
                                   font=("", 12, "bold")).grid(row=row, column=0, padx=10, pady=8, sticky="e")
            self.cod_menu = customtkinter.CTkOptionMenu(self.datos_parte_frame, values=dims.get("COD_TRABAJO", []))
            self.cod_menu.grid(row=row, column=1, padx=10, pady=8, sticky="ew")
            for item in dims.get("COD_TRABAJO", []):
                if item.startswith(f"{parte_data[7]} -"):
                    self.cod_menu.set(item)
                    break
            row += 1

            # Descripción
            customtkinter.CTkLabel(self.datos_parte_frame, text="Descripción:",
                                   font=("", 12, "bold")).grid(row=row, column=0, padx=10, pady=8, sticky="ne")
            self.desc_text = customtkinter.CTkTextbox(self.datos_parte_frame, height=100)
            self.desc_text.grid(row=row, column=1, padx=10, pady=8, sticky="ew")
            if parte_data[2]:
                self.desc_text.insert("1.0", parte_data[2])
            row += 1

            # Observaciones
            customtkinter.CTkLabel(self.datos_parte_frame, text="Observaciones:",
                                   font=("", 12, "bold")).grid(row=row, column=0, padx=10, pady=8, sticky="ne")
            self.obs_text = customtkinter.CTkTextbox(self.datos_parte_frame, height=100)
            self.obs_text.grid(row=row, column=1, padx=10, pady=8, sticky="ew")
            if parte_data[9]:
                self.obs_text.insert("1.0", parte_data[9])
            row += 1

            # Fechas (solo lectura)
            customtkinter.CTkLabel(self.datos_parte_frame, text="Creado:",
                                   font=("", 12, "bold")).grid(row=row, column=0, padx=10, pady=8, sticky="e")
            fecha_creado = customtkinter.CTkLabel(self.datos_parte_frame, text=str(parte_data[10]))
            fecha_creado.grid(row=row, column=1, padx=10, pady=8, sticky="w")
            row += 1

            if parte_data[11]:
                customtkinter.CTkLabel(self.datos_parte_frame, text="Actualizado:",
                                       font=("", 12, "bold")).grid(row=row, column=0, padx=10, pady=8, sticky="e")
                fecha_act = customtkinter.CTkLabel(self.datos_parte_frame, text=str(parte_data[11]))
                fecha_act.grid(row=row, column=1, padx=10, pady=8, sticky="w")
                row += 1

            # Botones
            btn_frame = customtkinter.CTkFrame(self.datos_parte_frame, fg_color="transparent")
            btn_frame.grid(row=row, column=0, columnspan=2, pady=20, sticky="ew")

            btn_save = customtkinter.CTkButton(
                btn_frame, text="💾 Guardar Cambios",
                command=lambda: self._save_parte_changes(parte_id),
                fg_color="green", hover_color="#006400", width=150
            )
            btn_save.pack(side="left", padx=(0, 10))

            btn_presupuesto = customtkinter.CTkButton(
                btn_frame, text="💰 Ver Presupuesto",
                command=lambda: self._goto_presupuesto(parte_id),
                width=150
            )
            btn_presupuesto.pack(side="left", padx=(0, 10))

            btn_certificaciones = customtkinter.CTkButton(
                btn_frame, text="📅 Ver Certificaciones",
                command=lambda: self._goto_certificaciones(parte_id),
                width=180
            )
            btn_certificaciones.pack(side="left")

        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error cargando parte:\n{e}", icon="cancel")

    def _save_parte_changes(self, parte_id):
        """Guarda los cambios del parte"""
        from script.modulo_db import mod_parte_item

        try:
            ot_id = int(self.ot_menu.get().split(" - ")[0])
            red_id = int(self.red_menu.get().split(" - ")[0])
            tipo_id = int(self.tipo_menu.get().split(" - ")[0])
            cod_id = int(self.cod_menu.get().split(" - ")[0])
            descripcion = self.desc_text.get("1.0", "end-1c").strip() or None
            estado = self.estado_var.get()

            # Observaciones solo si existe el widget
            observaciones = None
            if hasattr(self, 'obs_text'):
                observaciones = self.obs_text.get("1.0", "end-1c").strip() or None

            result = mod_parte_item(
                self.user, self.password, self.schema, parte_id,
                ot_id, red_id, tipo_id, cod_id, descripcion, estado, observaciones
            )

            if result == "ok":
                CTkMessagebox(title="Éxito", message="Parte actualizado correctamente", icon="check")
                self._load_parte_selected()
                # Recargar resumen si está visible
                if hasattr(self, 'tree_resumen'):
                    self._reload_resumen()
            else:
                CTkMessagebox(title="Error", message=f"Error:\n{result}", icon="cancel")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error guardando:\n{e}", icon="cancel")

    def _goto_presupuesto(self, parte_id):
        """Ir a pestaña Presupuesto con este parte"""
        self.selected_parte_id = parte_id
        self.select_frame_by_name("presupuesto")
        if hasattr(self, '_load_presupuesto_data'):
            self._load_presupuesto_data()

    def _goto_certificaciones(self, parte_id):
        """Ir a pestaña Certificaciones con este parte"""
        self.selected_parte_id = parte_id
        self.select_frame_by_name("certificaciones")
        if hasattr(self, '_load_certificaciones_data'):
            self._load_certificaciones_data()

    def main_presupuesto(self):
        """Pestaña Presupuesto - Gestión de presupuesto por parte (compatible con registros)"""
        from tkinter import ttk
        from script.modulo_db import get_partes_resumen, get_part_presupuesto

        self.presupuesto_frame.grid_columnconfigure(0, weight=1)
        self.presupuesto_frame.grid_rowconfigure(3, weight=1)

        # Título
        title = customtkinter.CTkLabel(
            self.presupuesto_frame,
            text="PRESUPUESTO POR PARTE",
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=0, padx=30, pady=(20, 10), sticky="w")

        # Selector de parte
        selector_frame = customtkinter.CTkFrame(self.presupuesto_frame, fg_color="transparent")
        selector_frame.grid(row=1, column=0, padx=30, pady=(0, 10), sticky="ew")
        selector_frame.grid_columnconfigure(1, weight=1)

        customtkinter.CTkLabel(selector_frame, text="Seleccionar Parte:",
                               font=("", 14, "bold")).grid(row=0, column=0, padx=(0, 10), sticky="e")

        # Cargar lista de partes
        try:
            partes_data = get_partes_resumen(self.user, self.password, self.schema)
            partes_list = [f"{row[0]} - {row[1]} | {row[4]} | {row[5]}" for row in partes_data]
        except:
            partes_list = ["Sin partes"]

        self.presupuesto_selector = customtkinter.CTkOptionMenu(
            selector_frame,
            values=partes_list if partes_list else ["Sin partes"],
            command=lambda x: self._load_presupuesto_data()
        )
        self.presupuesto_selector.grid(row=0, column=1, sticky="ew", padx=(0, 10))

        if partes_list and hasattr(self, 'selected_parte_id'):
            for item in partes_list:
                if item.startswith(f"{self.selected_parte_id} -"):
                    self.presupuesto_selector.set(item)
                    break
        elif partes_list:
            self.presupuesto_selector.set(partes_list[0])

        btn_reload = customtkinter.CTkButton(
            selector_frame, text="🔄", width=40,
            command=lambda: self._reload_presupuesto_selector()
        )
        btn_reload.grid(row=0, column=2)

        # Botones de acción
        buttons_frame = customtkinter.CTkFrame(self.presupuesto_frame, fg_color="transparent")
        buttons_frame.grid(row=2, column=0, padx=30, pady=(0, 10), sticky="ew")

        btn_add = customtkinter.CTkButton(
            buttons_frame, text="➕ Añadir Partida",
            command=self._add_partida_presupuesto,
            fg_color="green", hover_color="#006400", width=150
        )
        btn_add.pack(side="left", padx=(0, 10))

        btn_import = customtkinter.CTkButton(
            buttons_frame, text="📋 Importar Excel",
            command=self._import_excel_presupuesto,
            width=150
        )
        btn_import.pack(side="left", padx=(0, 10))

        btn_export = customtkinter.CTkButton(
            buttons_frame, text="💾 Exportar",
            command=self._export_presupuesto,
            width=120
        )
        btn_export.pack(side="left", padx=(0, 10))

        btn_update = customtkinter.CTkButton(
            buttons_frame, text="⚙️ Gestionar Catálogo",
            command=self._update_catalog_presupuesto,
            width=180
        )
        btn_update.pack(side="left")

        # Tabla de presupuesto
        table_frame = customtkinter.CTkFrame(self.presupuesto_frame)
        table_frame.grid(row=3, column=0, padx=30, pady=(0, 10), sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        cols = ("id", "codigo", "resumen", "unidad", "cantidad", "precio_unit", "coste")
        self.tree_presupuesto = ttk.Treeview(table_frame, columns=cols, show="headings", height=20)

        self.tree_presupuesto.heading("id", text="ID")
        self.tree_presupuesto.heading("codigo", text="Código")
        self.tree_presupuesto.heading("resumen", text="Resumen")
        self.tree_presupuesto.heading("unidad", text="Unidad")
        self.tree_presupuesto.heading("cantidad", text="Cantidad")
        self.tree_presupuesto.heading("precio_unit", text="Precio Unit.")
        self.tree_presupuesto.heading("coste", text="Coste")

        self.tree_presupuesto.column("id", width=40, anchor="center")
        self.tree_presupuesto.column("codigo", width=90, anchor="center")
        self.tree_presupuesto.column("resumen", width=280, anchor="w")
        self.tree_presupuesto.column("unidad", width=50, anchor="center")
        self.tree_presupuesto.column("cantidad", width=80, anchor="e")
        self.tree_presupuesto.column("precio_unit", width=90, anchor="e")
        self.tree_presupuesto.column("coste", width=90, anchor="e")

        headers_pres = {
            "id": "ID",
            "codigo": "Código",
            "resumen": "Resumen",
            "unidad": "Ud",
            "cantidad": "Cantidad",
            "precio_unit": "Precio Unit.",
            "coste": "Coste"
        }

        for col in cols:
            self.tree_presupuesto.heading(col, text=headers_pres[col])

        # Doble clic para editar cantidad
        self.tree_presupuesto.bind("<Double-1>", lambda e: self._edit_cantidad_presupuesto())

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_presupuesto.yview)
        self.tree_presupuesto.configure(yscrollcommand=scrollbar.set)
        self.tree_presupuesto.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Botones inferiores y total
        bottom_frame = customtkinter.CTkFrame(self.presupuesto_frame, fg_color="transparent")
        bottom_frame.grid(row=4, column=0, padx=30, pady=(0, 20), sticky="ew")
        bottom_frame.grid_columnconfigure(1, weight=1)

        btn_delete = customtkinter.CTkButton(
            bottom_frame, text="🗑️ Eliminar Seleccionada",
            command=self._delete_partida_presupuesto,
            fg_color="red", hover_color="#8B0000", width=180
        )
        btn_delete.grid(row=0, column=0, sticky="w")

        # Label de total
        self.total_presupuesto_label = customtkinter.CTkLabel(
            bottom_frame,
            text="TOTAL: 0.00€",
            font=customtkinter.CTkFont(size=18, weight="bold"),
            text_color="#4CAF50"
        )
        self.total_presupuesto_label.grid(row=0, column=1, sticky="e", padx=(0, 20))

        # Cargar datos
        if partes_list and partes_list[0] != "Sin partes":
            self._load_presupuesto_data()

    def _reload_presupuesto_selector(self):
        """Recarga el selector de partes en presupuesto"""
        from script.modulo_db import get_partes_resumen

        try:
            partes_data = get_partes_resumen(self.user, self.password, self.schema)
            partes_list = [f"{row[0]} - {row[1]} | {row[4]} | {row[5]}" for row in partes_data]

            if partes_list:
                self.presupuesto_selector.configure(values=partes_list)
                self.presupuesto_selector.set(partes_list[0])
                self._load_presupuesto_data()
            else:
                self.presupuesto_selector.configure(values=["Sin partes"])
                self.presupuesto_selector.set("Sin partes")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error recargando:\n{e}", icon="cancel")

    def _load_presupuesto_data(self):
        """Carga los datos del presupuesto del parte seleccionado"""
        from script.modulo_db import get_part_presupuesto

        # Limpiar tabla
        for item in self.tree_presupuesto.get_children():
            self.tree_presupuesto.delete(item)

        selected = self.presupuesto_selector.get()
        if selected == "Sin partes" or not selected:
            self.total_presupuesto_label.configure(text="TOTAL: 0.00€")
            return

        try:
            parte_id = int(selected.split(" - ")[0])
            self.current_presupuesto_parte_id = parte_id

            rows = get_part_presupuesto(self.user, self.password, self.schema, parte_id)
            total = 0

            for row in rows:
                # row: id, parte_id, codigo_parte, codigo_partida, resumen, descripcion, unidad, cantidad, precio_unit, coste
                display = (
                    row[0],  # id
                    row[3],  # codigo_partida
                    row[4] or "",  # resumen
                    row[6] or "",  # unidad
                    f"{float(row[7]):.3f}",  # cantidad
                    f"{float(row[8]):.2f}€",  # precio_unit
                    f"{float(row[9]):.2f}€"  # coste
                )
                self.tree_presupuesto.insert("", "end", values=display)
                total += float(row[9])

            self.total_presupuesto_label.configure(text=f"TOTAL: {total:.2f}€")

        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error cargando presupuesto:\n{e}", icon="cancel")

    def _add_partida_presupuesto(self):
        """Añade partida al presupuesto del parte (ventana similar a registros)"""
        selected = self.presupuesto_selector.get()
        if selected == "Sin partes" or not selected:
            CTkMessagebox(title="Aviso", message="Seleccione un parte primero", icon="info")
            return

        try:
            parte_id = int(selected.split(" - ")[0])

            # Abrir ventana de selección de partida
            from interface.parts_add_budget_item_interfaz import AppPartAddBudgetItem

            win = AppPartAddBudgetItem(
                self,
                [self.user, self.password, self.schema],
                parte_id
            )
            win.grab_set()
            self.wait_window(win)

            # Recargar datos
            self._load_presupuesto_data()

        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error:\n{e}", icon="cancel")

    def _edit_cantidad_presupuesto(self):
        """Edita la cantidad de la partida seleccionada"""
        from script.modulo_db import mod_amount_part_budget_item

        selected = self.tree_presupuesto.selection()
        if not selected:
            return

        item = self.tree_presupuesto.item(selected[0])
        values = item['values']
        item_id = values[0]
        cantidad_actual = values[4].replace(',', '.')

        # Ventana pequeña para editar cantidad
        win = customtkinter.CTkToplevel(self)
        win.title("Modificar Cantidad")
        win.geometry("400x150")
        win.resizable(False, False)
        win.attributes('-topmost', True)

        customtkinter.CTkLabel(
            win,
            text="Nueva Cantidad:",
            font=("", 14, "bold")
        ).pack(pady=(20, 10))

        cantidad_entry = customtkinter.CTkEntry(win, width=200)
        cantidad_entry.pack(pady=10)
        cantidad_entry.insert(0, cantidad_actual)
        cantidad_entry.select_range(0, 'end')
        cantidad_entry.focus()

        def guardar():
            try:
                nueva_cantidad = float(cantidad_entry.get().replace(',', '.'))
                result = mod_amount_part_budget_item(
                    self.user, self.password, self.schema, item_id, nueva_cantidad
                )

                if result == "ok":
                    win.destroy()
                    self._load_presupuesto_data()
                else:
                    CTkMessagebox(title="Error", message=f"Error:\n{result}", icon="cancel")
            except ValueError:
                CTkMessagebox(title="Error", message="Cantidad inválida", icon="cancel")

        btn_frame = customtkinter.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=10)

        customtkinter.CTkButton(
            btn_frame, text="Guardar", command=guardar,
            fg_color="green", width=100
        ).pack(side="left", padx=5)

        customtkinter.CTkButton(
            btn_frame, text="Cancelar", command=win.destroy,
            fg_color="red", width=100
        ).pack(side="left", padx=5)

        win.bind('<Return>', lambda e: guardar())
        win.lift()

    def _delete_partida_presupuesto(self):
        """Elimina la partida seleccionada del presupuesto"""
        from script.modulo_db import delete_part_presupuesto_item

        selected = self.tree_presupuesto.selection()
        if not selected:
            CTkMessagebox(title="Aviso", message="Seleccione una partida", icon="info")
            return

        item = self.tree_presupuesto.item(selected[0])
        values = item['values']
        item_id = values[0]
        codigo = values[1]

        msg = CTkMessagebox(
            title="Confirmar",
            message=f"¿Eliminar partida {codigo}?",
            icon="warning",
            option_1="Cancelar",
            option_2="Eliminar"
        )

        if msg.get() == "Eliminar":
            try:
                result = delete_part_presupuesto_item(self.user, self.password, self.schema, item_id)
                if result == "ok":
                    self._load_presupuesto_data()
                else:
                    CTkMessagebox(title="Error", message=f"Error:\n{result}", icon="cancel")
            except Exception as e:
                CTkMessagebox(title="Error", message=f"Error:\n{e}", icon="cancel")

    def _import_excel_presupuesto(self):
        """Importa presupuesto desde Excel al catálogo base (NO al parte)"""
        from tkinter import filedialog
        from script.budget_import import budget_import

        msg = CTkMessagebox(
            title="Importante",
            message="Esta función importa el Excel al CATÁLOGO BASE (tbl_pres_precios).\n\n"
                    "¿Desea continuar?",
            icon="question",
            option_1="Cancelar",
            option_2="Importar"
        )

        if msg.get() != "Importar":
            return

        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )

        if not file_path:
            return

        try:
            result = budget_import(self.user, self.password, self.schema, file_path)

            if result == "ok":
                CTkMessagebox(
                    title="Éxito",
                    message="✅ Presupuesto importado correctamente al catálogo base",
                    icon="check"
                )
            else:
                CTkMessagebox(
                    title="Error",
                    message=f"Error importando:\n{result}",
                    icon="cancel"
                )
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error:\n{e}", icon="cancel")

    def _export_presupuesto(self):
        """Exporta el presupuesto del parte a Excel"""
        from tkinter import filedialog
        import pandas as pd
        from script.modulo_db import get_part_presupuesto

        selected = self.presupuesto_selector.get()
        if selected == "Sin partes" or not selected:
            CTkMessagebox(title="Aviso", message="Seleccione un parte", icon="info")
            return

        try:
            parte_id = int(selected.split(" - ")[0])
            codigo_parte = selected.split(" - ")[1].split(" | ")[0]

            rows = get_part_presupuesto(self.user, self.password, self.schema, parte_id)

            if not rows:
                CTkMessagebox(title="Aviso", message="No hay partidas para exportar", icon="info")
                return

            # Crear DataFrame
            data = []
            for row in rows:
                data.append({
                    'Código': row[3],
                    'Resumen': row[4],
                    'Descripción': row[5],
                    'Unidad': row[6],
                    'Cantidad': float(row[7]),
                    'Precio Unit.': float(row[8]),
                    'Coste': float(row[9])
                })

            df = pd.DataFrame(data)

            # Guardar
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                initialfile=f"Presupuesto_{codigo_parte}.xlsx",
                filetypes=[("Excel files", "*.xlsx")]
            )

            if file_path:
                df.to_excel(file_path, index=False, sheet_name="Presupuesto")
                CTkMessagebox(title="Éxito", message="✅ Exportado correctamente", icon="check")

        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error exportando:\n{e}", icon="cancel")

    def _update_catalog_presupuesto(self):
        """Abre ventana de gestión del catálogo (igual que registros)"""
        from interface.update_budget_interfaz import AppBudgetUpdate

        win = AppBudgetUpdate([self.user, self.password, self.schema])
        win.grab_set()
        self.wait_window(win)

    def main_certificaciones(self):
        """Pestaña Certificaciones - Gestión de certificaciones por parte con fechas"""
        from tkinter import ttk
        from tkcalendar import DateEntry
        from datetime import datetime
        from script.modulo_db import get_partes_resumen

        self.certificaciones_frame.grid_columnconfigure(0, weight=1)
        self.certificaciones_frame.grid_rowconfigure(4, weight=1)
        self.certificaciones_frame.grid_rowconfigure(7, weight=1)

        # Título
        title = customtkinter.CTkLabel(
            self.certificaciones_frame,
            text="CERTIFICACIONES POR PARTE",
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=0, padx=30, pady=(20, 10), sticky="w")

        # Selector de parte
        selector_frame = customtkinter.CTkFrame(self.certificaciones_frame, fg_color="transparent")
        selector_frame.grid(row=1, column=0, padx=30, pady=(0, 10), sticky="ew")
        selector_frame.grid_columnconfigure(1, weight=1)

        customtkinter.CTkLabel(selector_frame, text="Seleccionar Parte:",
                               font=("", 14, "bold")).grid(row=0, column=0, padx=(0, 10), sticky="e")

        # Cargar lista de partes
        try:
            partes_data = get_partes_resumen(self.user, self.password, self.schema)
            partes_list = [f"{row[0]} - {row[1]} | {row[4]} | {row[5]}" for row in partes_data]
        except:
            partes_list = ["Sin partes"]

        self.cert_selector = customtkinter.CTkOptionMenu(
            selector_frame,
            values=partes_list if partes_list else ["Sin partes"],
            command=lambda x: self._load_certificaciones_data()
        )
        self.cert_selector.grid(row=0, column=1, sticky="ew", padx=(0, 10))

        if partes_list and hasattr(self, 'selected_parte_id'):
            for item in partes_list:
                if item.startswith(f"{self.selected_parte_id} -"):
                    self.cert_selector.set(item)
                    break
        elif partes_list:
            self.cert_selector.set(partes_list[0])

        btn_reload = customtkinter.CTkButton(
            selector_frame, text="🔄", width=40,
            command=lambda: self._reload_cert_selector()
        )
        btn_reload.grid(row=0, column=2)

        # ========== SECCIÓN PENDIENTES ==========
        pendientes_label = customtkinter.CTkLabel(
            self.certificaciones_frame,
            text="📋 PENDIENTES DE CERTIFICAR",
            font=customtkinter.CTkFont(size=16, weight="bold"),
            text_color="#FF9800"
        )
        pendientes_label.grid(row=2, column=0, padx=30, pady=(20, 5), sticky="w")

        # Selector de fecha global y botón certificar todas
        fecha_frame = customtkinter.CTkFrame(self.certificaciones_frame, fg_color="transparent")
        fecha_frame.grid(row=3, column=0, padx=30, pady=(0, 10), sticky="ew")

        customtkinter.CTkLabel(fecha_frame, text="Fecha para certificar:",
                               font=("", 13, "bold")).pack(side="left", padx=(0, 10))

        self.fecha_cert_global = DateEntry(
            fecha_frame,
            width=15,
            background='#1f6aa5',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd',
            locale='es_ES'
        )
        self.fecha_cert_global.set_date(datetime.now())
        self.fecha_cert_global.pack(side="left", padx=(0, 20))

        btn_cert_all = customtkinter.CTkButton(
            fecha_frame, text="✅ Certificar Todas",
            command=self._certificar_todas_pendientes,
            fg_color="#4CAF50", hover_color="#388E3C", width=150
        )
        btn_cert_all.pack(side="left")

        # Tabla pendientes
        table_pend_frame = customtkinter.CTkFrame(self.certificaciones_frame)
        table_pend_frame.grid(row=4, column=0, padx=30, pady=(0, 10), sticky="nsew")
        table_pend_frame.grid_rowconfigure(0, weight=1)
        table_pend_frame.grid_columnconfigure(0, weight=1)

        cols_pend = ("presupuesto_id", "precio_id", "codigo", "resumen", "unidad",
                     "presupuestado", "certificado", "pendiente", "precio", "fecha")
        self.tree_cert_pendientes = ttk.Treeview(table_pend_frame, columns=cols_pend, show="headings", height=10)

        # Configuración mejorada de columnas PENDIENTES
        cols_config = {
            "presupuesto_id": (50, "center"),
            "precio_id": (60, "center"),
            "codigo": (90, "center"),
            "resumen": (250, "w"),
            "unidad": (45, "center"),
            "presupuestado": (80, "e"),
            "certificado": (80, "e"),
            "pendiente": (80, "e"),
            "precio": (75, "e"),
            "fecha": (95, "center")
        }

        # Configurar headers con texto más legible
        headers = {
            "presupuesto_id": "Pres.ID",
            "precio_id": "Precio ID",
            "codigo": "Código",
            "resumen": "Resumen",
            "unidad": "Ud",
            "presupuestado": "Presup.",
            "certificado": "Certif.",
            "pendiente": "Pendiente",
            "precio": "Precio",
            "fecha": "Fecha Destino"
        }

        for col in cols_pend:
            self.tree_cert_pendientes.heading(col, text=headers[col])
            width, anchor = cols_config[col]
            self.tree_cert_pendientes.column(col, width=width, anchor=anchor, stretch=False)

        # Doble clic para editar fecha
        self.tree_cert_pendientes.bind("<Double-1>", lambda e: self._edit_fecha_destino())

        scrollbar_pend = ttk.Scrollbar(table_pend_frame, orient="vertical", command=self.tree_cert_pendientes.yview)
        self.tree_cert_pendientes.configure(yscrollcommand=scrollbar_pend.set)
        self.tree_cert_pendientes.grid(row=0, column=0, sticky="nsew")
        scrollbar_pend.grid(row=0, column=1, sticky="ns")

        # Botones para pendientes
        btn_pend_frame = customtkinter.CTkFrame(self.certificaciones_frame, fg_color="transparent")
        btn_pend_frame.grid(row=5, column=0, padx=30, pady=(0, 10), sticky="ew")

        btn_cert_selected = customtkinter.CTkButton(
            btn_pend_frame, text="💰 Certificar Seleccionada",
            command=self._certificar_seleccionada,
            fg_color="#2196F3", hover_color="#1976D2", width=180
        )
        btn_cert_selected.pack(side="left", padx=(0, 10))

        # ========== SECCIÓN CERTIFICADAS ==========
        certificadas_label = customtkinter.CTkLabel(
            self.certificaciones_frame,
            text="✅ CERTIFICADAS",
            font=customtkinter.CTkFont(size=16, weight="bold"),
            text_color="#4CAF50"
        )
        certificadas_label.grid(row=6, column=0, padx=30, pady=(20, 5), sticky="w")

        # Tabla certificadas
        table_cert_frame = customtkinter.CTkFrame(self.certificaciones_frame)
        table_cert_frame.grid(row=7, column=0, padx=30, pady=(0, 10), sticky="nsew")
        table_cert_frame.grid_rowconfigure(0, weight=1)
        table_cert_frame.grid_columnconfigure(0, weight=1)

        cols_cert = ("id", "codigo", "resumen", "unidad", "cantidad", "precio", "coste", "fecha")
        self.tree_cert_certificadas = ttk.Treeview(table_cert_frame, columns=cols_cert, show="headings", height=10)

        # Configuración mejorada de columnas CERTIFICADAS
        cols_config_cert = {
            "id": (45, "center"),
            "codigo": (95, "center"),
            "resumen": (270, "w"),
            "unidad": (45, "center"),
            "cantidad": (85, "e"),
            "precio": (85, "e"),
            "coste": (85, "e"),
            "fecha": (95, "center")
        }

        headers_cert = {
            "id": "ID",
            "codigo": "Código",
            "resumen": "Resumen",
            "unidad": "Ud",
            "cantidad": "Cantidad",
            "precio": "Precio",
            "coste": "Coste",
            "fecha": "Fecha Certif."
        }

        for col in cols_cert:
            self.tree_cert_certificadas.heading(col, text=headers_cert[col])
            width, anchor = cols_config_cert[col]
            self.tree_cert_certificadas.column(col, width=width, anchor=anchor, stretch=False)

        scrollbar_cert = ttk.Scrollbar(table_cert_frame, orient="vertical", command=self.tree_cert_certificadas.yview)
        self.tree_cert_certificadas.configure(yscrollcommand=scrollbar_cert.set)
        self.tree_cert_certificadas.grid(row=0, column=0, sticky="nsew")
        scrollbar_cert.grid(row=0, column=1, sticky="ns")

        # Botones para certificadas y total
        bottom_frame = customtkinter.CTkFrame(self.certificaciones_frame, fg_color="transparent")
        bottom_frame.grid(row=8, column=0, padx=30, pady=(0, 20), sticky="ew")
        bottom_frame.grid_columnconfigure(1, weight=1)

        btn_delete_cert = customtkinter.CTkButton(
            bottom_frame, text="🗑️ Eliminar Certificación",
            command=self._delete_certificacion,
            fg_color="red", hover_color="#8B0000", width=180
        )
        btn_delete_cert.grid(row=0, column=0, sticky="w")

        self.total_cert_label = customtkinter.CTkLabel(
            bottom_frame,
            text="TOTAL CERTIFICADO: 0.00€",
            font=customtkinter.CTkFont(size=18, weight="bold"),
            text_color="#4CAF50"
        )
        self.total_cert_label.grid(row=0, column=1, sticky="e", padx=(0, 20))

        # Cargar datos
        if partes_list and partes_list[0] != "Sin partes":
            self._load_certificaciones_data()

    def _reload_cert_selector(self):
        """Recarga el selector de partes en certificaciones"""
        from script.modulo_db import get_partes_resumen

        try:
            partes_data = get_partes_resumen(self.user, self.password, self.schema)
            partes_list = [f"{row[0]} - {row[1]} | {row[4]} | {row[5]}" for row in partes_data]

            if partes_list:
                self.cert_selector.configure(values=partes_list)
                self.cert_selector.set(partes_list[0])
                self._load_certificaciones_data()
            else:
                self.cert_selector.configure(values=["Sin partes"])
                self.cert_selector.set("Sin partes")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error recargando:\n{e}", icon="cancel")

    def _load_certificaciones_data(self):
        """Carga las certificaciones (pendientes y certificadas) del parte seleccionado"""
        from script.modulo_db import get_part_cert_pendientes, get_part_cert_certificadas

        # Limpiar tablas
        for item in self.tree_cert_pendientes.get_children():
            self.tree_cert_pendientes.delete(item)
        for item in self.tree_cert_certificadas.get_children():
            self.tree_cert_certificadas.delete(item)

        selected = self.cert_selector.get()
        if selected == "Sin partes" or not selected:
            self.total_cert_label.configure(text="TOTAL CERTIFICADO: 0.00€")
            return

        try:
            parte_id = int(selected.split(" - ")[0])
            self.current_cert_parte_id = parte_id

            # Cargar pendientes
            pendientes = get_part_cert_pendientes(self.user, self.password, self.schema, parte_id)
            for row in pendientes:
                # row: presupuesto_id, precio_id, codigo, resumen, unidad, cant_presup, cant_cert, cant_pend, precio_unit
                display = (
                    row[0],  # presupuesto_id
                    row[1],  # precio_id
                    row[2],  # codigo
                    row[3] or "",  # resumen
                    row[4] or "",  # unidad
                    f"{float(row[5]):.3f}",  # cantidad_presupuesto
                    f"{float(row[6]):.3f}",  # cantidad_certificada
                    f"{float(row[7]):.3f}",  # cantidad_pendiente
                    f"{float(row[8]):.2f}€",  # precio_unit
                    self.fecha_cert_global.get_date().strftime('%Y-%m-%d')  # fecha por defecto
                )
                self.tree_cert_pendientes.insert("", "end", values=display)

            # Cargar certificadas
            certificadas = get_part_cert_certificadas(self.user, self.password, self.schema, parte_id)
            total_cert = 0

            for row in certificadas:
                # row: id, parte_id, codigo_parte, codigo_partida, resumen, unidad, cantidad_cert, precio_unit, coste_cert, fecha_certificacion, ...
                display = (
                    row[0],  # id
                    row[3],  # codigo_partida
                    row[4] or "",  # resumen
                    row[5] or "",  # unidad
                    f"{float(row[6]):.3f}",  # cantidad_cert
                    f"{float(row[7]):.2f}€",  # precio_unit
                    f"{float(row[8]):.2f}€",  # coste_cert
                    str(row[9])  # fecha_certificacion
                )
                self.tree_cert_certificadas.insert("", "end", values=display)
                total_cert += float(row[8])

            self.total_cert_label.configure(text=f"TOTAL CERTIFICADO: {total_cert:.2f}€")

        except Exception as e:
            import traceback
            print(f"ERROR:\n{traceback.format_exc()}")
            CTkMessagebox(title="Error", message=f"Error cargando certificaciones:\n{e}", icon="cancel")

    def _edit_fecha_destino(self):
        """Edita la fecha destino de una partida pendiente"""
        from tkcalendar import DateEntry
        from datetime import datetime

        selected = self.tree_cert_pendientes.selection()
        if not selected:
            return

        item = self.tree_cert_pendientes.item(selected[0])
        values = list(item['values'])
        fecha_actual = values[9]

        # Ventana para editar fecha
        win = customtkinter.CTkToplevel(self)
        win.title("Modificar Fecha Destino")
        win.geometry("400x180")
        win.resizable(False, False)
        win.attributes('-topmost', True)

        customtkinter.CTkLabel(
            win,
            text="Nueva Fecha de Certificación:",
            font=("", 14, "bold")
        ).pack(pady=(20, 10))

        fecha_entry = DateEntry(
            win,
            width=20,
            background='#1f6aa5',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd',
            locale='es_ES'
        )

        try:
            fecha_entry.set_date(datetime.strptime(fecha_actual, '%Y-%m-%d'))
        except:
            fecha_entry.set_date(datetime.now())

        fecha_entry.pack(pady=10)

        def guardar():
            nueva_fecha = fecha_entry.get_date().strftime('%Y-%m-%d')
            values[9] = nueva_fecha
            self.tree_cert_pendientes.item(selected[0], values=values)
            win.destroy()

        btn_frame = customtkinter.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=15)

        customtkinter.CTkButton(
            btn_frame, text="Guardar", command=guardar,
            fg_color="green", width=100
        ).pack(side="left", padx=5)

        customtkinter.CTkButton(
            btn_frame, text="Cancelar", command=win.destroy,
            fg_color="red", width=100
        ).pack(side="left", padx=5)

        win.lift()

    def _certificar_seleccionada(self):
        """Certifica la partida pendiente seleccionada"""
        from script.modulo_db import add_part_cert_item

        selected = self.tree_cert_pendientes.selection()
        if not selected:
            CTkMessagebox(title="Aviso", message="Seleccione una partida", icon="info")
            return

        item = self.tree_cert_pendientes.item(selected[0])
        values = item['values']

        precio_id = values[1]
        cantidad_pendiente = float(values[7].replace(',', '.'))
        precio_unit = float(values[8].replace('€', '').replace(',', '.'))
        fecha = values[9]

        msg = CTkMessagebox(
            title="Confirmar",
            message=f"¿Certificar {cantidad_pendiente:.3f} unidades a fecha {fecha}?",
            icon="question",
            option_1="Cancelar",
            option_2="Certificar"
        )

        if msg.get() == "Certificar":
            try:
                result = add_part_cert_item(
                    self.user, self.password, self.schema,
                    self.current_cert_parte_id, precio_id, cantidad_pendiente,
                    precio_unit, fecha, certificada=1
                )

                if result == "ok":
                    CTkMessagebox(title="Éxito", message="✅ Partida certificada", icon="check")
                    self._load_certificaciones_data()
                else:
                    CTkMessagebox(title="Error", message=f"Error:\n{result}", icon="cancel")
            except Exception as e:
                CTkMessagebox(title="Error", message=f"Error:\n{e}", icon="cancel")

    def _certificar_todas_pendientes(self):
        """Certifica todas las partidas pendientes a la fecha global seleccionada"""
        from script.modulo_db import add_part_cert_item

        if not self.tree_cert_pendientes.get_children():
            CTkMessagebox(title="Aviso", message="No hay partidas pendientes", icon="info")
            return

        fecha = self.fecha_cert_global.get_date().strftime('%Y-%m-%d')
        count = len(self.tree_cert_pendientes.get_children())

        msg = CTkMessagebox(
            title="Confirmar",
            message=f"¿Certificar TODAS las {count} partidas pendientes a fecha {fecha}?",
            icon="warning",
            option_1="Cancelar",
            option_2="Certificar Todas"
        )

        if msg.get() != "Certificar Todas":
            return

        try:
            errores = []
            certificadas = 0

            for child in self.tree_cert_pendientes.get_children():
                item = self.tree_cert_pendientes.item(child)
                values = item['values']

                precio_id = values[1]
                cantidad_pendiente = float(values[7].replace(',', '.'))
                precio_unit = float(values[8].replace('€', '').replace(',', '.'))

                result = add_part_cert_item(
                    self.user, self.password, self.schema,
                    self.current_cert_parte_id, precio_id, cantidad_pendiente,
                    precio_unit, fecha, certificada=1
                )

                if result == "ok":
                    certificadas += 1
                else:
                    errores.append(f"Precio ID {precio_id}: {result}")

            if errores:
                CTkMessagebox(
                    title="Completado con errores",
                    message=f"✅ Certificadas: {certificadas}\n❌ Errores: {len(errores)}\n\n{errores[0]}",
                    icon="warning"
                )
            else:
                CTkMessagebox(
                    title="Éxito",
                    message=f"✅ {certificadas} partidas certificadas correctamente",
                    icon="check"
                )

            self._load_certificaciones_data()

        except Exception as e:
            import traceback
            print(f"ERROR:\n{traceback.format_exc()}")
            CTkMessagebox(title="Error", message=f"Error:\n{e}", icon="cancel")

    def _delete_certificacion(self):
        """Elimina una certificación"""
        from script.modulo_db import delete_part_cert_item

        selected = self.tree_cert_certificadas.selection()
        if not selected:
            CTkMessagebox(title="Aviso", message="Seleccione una certificación", icon="info")
            return

        item = self.tree_cert_certificadas.item(selected[0])
        values = item['values']
        cert_id = values[0]
        codigo = values[1]

        msg = CTkMessagebox(
            title="Confirmar",
            message=f"¿Eliminar certificación {codigo}?\n\nEsta acción no se puede deshacer.",
            icon="warning",
            option_1="Cancelar",
            option_2="Eliminar"
        )

        if msg.get() == "Eliminar":
            try:
                result = delete_part_cert_item(self.user, self.password, self.schema, cert_id)
                if result == "ok":
                    CTkMessagebox(title="Éxito", message="✅ Certificación eliminada", icon="check")
                    self._load_certificaciones_data()
                else:
                    CTkMessagebox(title="Error", message=f"Error:\n{result}", icon="cancel")
            except Exception as e:
                CTkMessagebox(title="Error", message=f"Error:\n{e}", icon="cancel")

    def back_to_selector(self):
        """Volver al selector de tipo de usuario"""
        self.destroy()
        from interface.typeUser_interfaz import AppTypeUser
        app = AppTypeUser([self.user, self.password])
        app.mainloop()


if __name__ == "__main__":
    # Test
    app = AppPartsManager(["aperez", "WGueXNk9"], "cert_dev")
    app.mainloop()