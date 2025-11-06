# interface/parts_manager_interfaz.py
import customtkinter
from PIL import Image
from CTkMessagebox import CTkMessagebox
from tkinter import ttk, font as tkfont
from script.modulo_db import get_schemas_db, project_directory_db
from script.db_connection import get_project_connection
import os
import json

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
    height = 1000

    def __init__(self, access, schema):
        super().__init__()

        # ✅ CONFIGURAR ESTILO DE TREEVIEW PRIMERO
        configure_treeview_style()

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
        self.informes_frame = customtkinter.CTkFrame(self, corner_radius=0)

        # Generar vistas
        self.main_resumen()
        self.main_partes()
        self.main_presupuesto()
        self.main_certificaciones()
        self.main_informes()

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

        informes_path = os.path.join(parent_path, "source/informes.png")
        self.informes_image = customtkinter.CTkImage(Image.open(informes_path), size=(30, 30))

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

        # Botón Añadir Parte (destacado en verde)
        add_parte_path = os.path.join(parent_path, "source/guardar.png")
        self.add_parte_image = customtkinter.CTkImage(Image.open(add_parte_path), size=(25, 25))

        self.add_parte_button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=5, height=50,
            border_spacing=10, text="➕ Añadir Parte",
            fg_color="green", hover_color="#006400",
            text_color="white",
            image=self.add_parte_image,
            font=customtkinter.CTkFont(size=16, weight="bold"),
            anchor="center", command=self._add_parte_resumen
        )
        self.add_parte_button.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 15))

        # Botón Resumen
        self.resumen_button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=0, height=40,
            border_spacing=10, text="Resumen", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.resumen_image, font=customtkinter.CTkFont(size=15, weight="bold"),
            anchor="w", command=lambda: self.select_frame_by_name("resumen")
        )
        self.resumen_button.grid(row=3, column=0, sticky="ew")

        # Botón Partes
        self.partes_button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=0, height=40,
            border_spacing=10, text="Partes", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.partes_image, font=customtkinter.CTkFont(size=15, weight="bold"),
            anchor="w", command=lambda: self.select_frame_by_name("partes")
        )
        self.partes_button.grid(row=4, column=0, sticky="ew")

        # Botón Presupuesto
        self.presupuesto_button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=0, height=40,
            border_spacing=10, text="Presupuesto", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.budget_image, font=customtkinter.CTkFont(size=15, weight="bold"),
            anchor="w", command=lambda: self.select_frame_by_name("presupuesto")
        )
        self.presupuesto_button.grid(row=5, column=0, sticky="ew")

        # Botón Certificaciones
        self.certificaciones_button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=0, height=40,
            border_spacing=10, text="Certificaciones", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.budget_image, font=customtkinter.CTkFont(size=15, weight="bold"),
            anchor="w", command=lambda: self.select_frame_by_name("certificaciones")
        )
        self.certificaciones_button.grid(row=6, column=0, sticky="ew")

        # Botón Informes
        self.informes_button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=0, height=40,
            border_spacing=10, text="Informes", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.informes_image, font=customtkinter.CTkFont(size=15, weight="bold"),
            anchor="w", command=lambda: self.select_frame_by_name("informes")
        )
        self.informes_button.grid(row=7, column=0, sticky="ew")

        # Espaciador
        self.navigation_frame.grid_rowconfigure(8, weight=1)

        # Botón Volver
        self.back_button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=5, height=40,
            border_spacing=10, text="Volver",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            font=("default", 14, "bold"), anchor="center",
            command=self.back_to_selector
        )
        self.back_button.grid(row=9, padx=30, pady=(15, 15), sticky="nsew")

    def _get_config_path(self):
        """Retorna la ruta del archivo de configuración de columnas"""
        config_dir = os.path.join(parent_path, ".config")
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        return os.path.join(config_dir, f"columns_config_{self.schema}.json")

    def _save_column_config(self, section, columns_dict):
        """
        Guarda la configuración de columnas visibles
        section: 'resumen' o 'listado'
        columns_dict: diccionario con la configuración de columnas
        """
        try:
            config_path = self._get_config_path()

            # Leer configuración existente o crear nueva
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {}

            # Guardar solo el estado de visibilidad de cada columna
            config[section] = {
                col_name: col_info["visible"]
                for col_name, col_info in columns_dict.items()
            }

            # Escribir archivo
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)

        except Exception as e:
            print(f"Error guardando configuración de columnas: {e}")

    def _load_column_config(self, section, columns_dict):
        """
        Carga la configuración de columnas visibles
        section: 'resumen' o 'listado'
        columns_dict: diccionario con la configuración de columnas (se modifica in-place)
        """
        try:
            config_path = self._get_config_path()

            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                if section in config:
                    # Aplicar configuración guardada
                    for col_name, visible in config[section].items():
                        if col_name in columns_dict:
                            columns_dict[col_name]["visible"] = visible

        except Exception as e:
            print(f"Error cargando configuración de columnas: {e}")

    def select_frame_by_name(self, name):
        """Cambia entre frames/pestañas"""
        # Actualizar colores de botones
        self.resumen_button.configure(fg_color=("gray75", "gray25") if name == "resumen" else "transparent")
        self.partes_button.configure(fg_color=("gray75", "gray25") if name == "partes" else "transparent")
        self.presupuesto_button.configure(fg_color=("gray75", "gray25") if name == "presupuesto" else "transparent")
        self.certificaciones_button.configure(
            fg_color=("gray75", "gray25") if name == "certificaciones" else "transparent")
        self.informes_button.configure(
            fg_color=("gray75", "gray25") if name == "informes" else "transparent")

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

        if name == "informes":
            self.informes_frame.grid(row=0, column=1, padx=30, pady=(15, 15), sticky="nsew")
        else:
            self.informes_frame.grid_forget()

    def main_resumen(self):
        """Pestaña Resumen - Lista de partes con KPIs"""
        from tkinter import ttk
        from script.modulo_db import get_partes_resumen
        # from parts_list_window import open_parts_list  # OBSOLETO: Módulo eliminado

        self.resumen_frame.grid_columnconfigure(0, weight=1)
        self.resumen_frame.grid_rowconfigure(2, weight=1)

        # Definir TODAS las columnas disponibles para tbl_partes + presupuesto/certificado/pendiente
        self.resumen_columns = {
            # Columnas principales (visibles por defecto)
            "codigo": {"label": "Código", "width": 80, "visible": True, "locked": True},
            "descripcion": {"label": "Descripción", "width": 200, "visible": True, "locked": False},
            "estado": {"label": "Estado", "width": 80, "visible": True, "locked": False},
            "red": {"label": "Red", "width": 120, "visible": True, "locked": False},
            "tipo": {"label": "Tipo Trabajo", "width": 120, "visible": True, "locked": False},
            "cod_trabajo": {"label": "Cód.Trabajo", "width": 120, "visible": True, "locked": False},
            "tipo_rep": {"label": "Tipo Reparación", "width": 130, "visible": True, "locked": False},
            "presupuesto": {"label": "Presup.", "width": 90, "visible": True, "locked": False},
            "certificado": {"label": "Certif.", "width": 90, "visible": True, "locked": False},
            "pendiente": {"label": "Pendiente", "width": 90, "visible": True, "locked": False},

            # Campos de descripción ampliada (ocultos por defecto)
            "titulo": {"label": "Título", "width": 200, "visible": False, "locked": False},
            "descripcion_corta": {"label": "Desc. Corta", "width": 150, "visible": False, "locked": False},
            "descripcion_larga": {"label": "Desc. Larga", "width": 300, "visible": False, "locked": False},

            # Fechas (ocultas por defecto excepto created_at)
            "fecha_inicio": {"label": "Fecha Inicio", "width": 110, "visible": False, "locked": False},
            "fecha_fin": {"label": "Fecha Fin", "width": 110, "visible": False, "locked": False},
            "created_at": {"label": "Fecha Creación", "width": 150, "visible": False, "locked": False},
            "updated_at": {"label": "Última Actualiz.", "width": 150, "visible": False, "locked": False},

            # Localización (ocultos por defecto)
            "localizacion": {"label": "Localización", "width": 200, "visible": False, "locked": False},
            "municipio": {"label": "Municipio", "width": 150, "visible": False, "locked": False},
            "comarca": {"label": "Comarca", "width": 150, "visible": False, "locked": False},
            "provincia": {"label": "Provincia", "width": 120, "visible": False, "locked": False},
            "latitud": {"label": "Latitud", "width": 100, "visible": False, "locked": False},
            "longitud": {"label": "Longitud", "width": 100, "visible": False, "locked": False},

            # Otros campos (ocultos por defecto)
            "trabajadores": {"label": "Trabajadores", "width": 200, "visible": False, "locked": False},
            "observaciones": {"label": "Observaciones", "width": 250, "visible": False, "locked": False},
        }

        # Cargar configuración guardada de columnas visibles
        self._load_column_config("resumen", self.resumen_columns)

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

        # OBSOLETO: Botón deshabilitado - módulo parts_list_window eliminado
        # btn_list = customtkinter.CTkButton(
        #     btn_frame, text="📋 Ver Listado Completo",
        #     command=lambda: open_parts_list(self, self.user, self.password, self.schema),
        #     width=180
        # )
        # btn_list.pack(side="left", padx=(0, 10))

        btn_columns = customtkinter.CTkButton(
            btn_frame, text="⚙ Columnas",
            command=self._show_resumen_column_selector,
            width=100, fg_color="#1f6aa5"
        )
        btn_columns.pack(side="left")

        # Frame para tabla
        self.resumen_table_frame = customtkinter.CTkFrame(self.resumen_frame)
        self.resumen_table_frame.grid(row=2, column=0, padx=30, pady=(0, 20), sticky="nsew", columnspan=3)
        self.resumen_table_frame.grid_rowconfigure(0, weight=1)
        self.resumen_table_frame.grid_columnconfigure(0, weight=1)

        # Crear tabla con columnas seleccionadas
        self._rebuild_resumen_tree()

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

            # Mapeo de índices del resultado SQL - TODAS las columnas
            # row: id, codigo, descripcion, estado, red, tipo, cod_trabajo, tipo_rep,
            #      presupuesto, certificado, pendiente, titulo, descripcion_corta, descripcion_larga,
            #      fecha_inicio, fecha_fin, created_at, updated_at, localizacion, municipio, comarca,
            #      provincia, latitud, longitud, trabajadores, observaciones
            field_map = {
                "id": 0,
                "codigo": 1,
                "descripcion": 2,
                "estado": 3,
                "red": 4,
                "tipo": 5,
                "cod_trabajo": 6,
                "tipo_rep": 7,
                "presupuesto": 8,
                "certificado": 9,
                "pendiente": 10,
                "titulo": 11,
                "descripcion_corta": 12,
                "descripcion_larga": 13,
                "fecha_inicio": 14,
                "fecha_fin": 15,
                "created_at": 16,
                "updated_at": 17,
                "localizacion": 18,
                "municipio": 19,
                "comarca": 20,
                "provincia": 21,
                "latitud": 22,
                "longitud": 23,
                "trabajadores": 24,
                "observaciones": 25,
            }

            # Obtener columnas visibles actuales del tree
            visible_cols = self.tree_resumen["columns"]

            for row_data in rows:
                # Construir fila con solo las columnas visibles
                row_values = []
                for col in visible_cols:
                    idx = field_map.get(col)
                    if idx is not None and idx < len(row_data):
                        value = row_data[idx]
                        # Formatear valores especiales
                        if col in ["presupuesto", "certificado", "pendiente"] and value is not None:
                            row_values.append(f"{float(value):.2f}€")
                        elif col in ["created_at", "updated_at", "fecha_inicio", "fecha_fin"] and value is not None:
                            row_values.append(str(value))
                        elif col in ["latitud", "longitud"] and value is not None:
                            row_values.append(f"{float(value):.6f}")
                        elif col == "estado":
                            row_values.append(value if value else "Pendiente")
                        else:
                            row_values.append(value if value is not None else "")
                    else:
                        row_values.append("")

                self.tree_resumen.insert("", "end", values=row_values)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error cargando partes:\n{e}", icon="cancel")

    def _rebuild_resumen_tree(self):
        """Reconstruye la tabla del resumen con las columnas visibles seleccionadas"""
        from tkinter import ttk

        # Eliminar tabla anterior si existe
        if hasattr(self, 'tree_resumen'):
            self.tree_resumen.destroy()
            self.resumen_scrollbar.destroy()

        # Obtener columnas visibles (codigo siempre primero)
        visible_cols = ["id"]  # ID siempre incluido pero oculto
        visible_cols.append("codigo")  # Codigo siempre primero y visible

        # Agregar resto de columnas visibles
        for col_name, col_info in self.resumen_columns.items():
            if col_name != "codigo" and col_info["visible"]:
                visible_cols.append(col_name)

        # Crear nueva tabla
        self.tree_resumen = ttk.Treeview(self.resumen_table_frame, columns=visible_cols, show="headings", height=20)

        # Configurar columnas
        self.tree_resumen.heading("id", text="ID")
        self.tree_resumen.column("id", width=0, stretch=False)  # ID oculto

        for col in visible_cols[1:]:  # Skip "id"
            col_info = self.resumen_columns.get(col, {"label": col, "width": 100})
            self.tree_resumen.heading(col, text=col_info["label"])
            self.tree_resumen.column(col, width=col_info["width"], anchor="center")

        # Scrollbar
        self.resumen_scrollbar = ttk.Scrollbar(self.resumen_table_frame, orient="vertical", command=self.tree_resumen.yview)
        self.tree_resumen.configure(yscrollcommand=self.resumen_scrollbar.set)
        self.tree_resumen.grid(row=0, column=0, sticky="nsew")
        self.resumen_scrollbar.grid(row=0, column=1, sticky="ns")

        # Doble clic para ver detalles
        self.tree_resumen.bind("<Double-1>", lambda e: self._view_parte_detail())

        # Recargar datos
        self._reload_resumen()

    def _show_resumen_column_selector(self):
        """Muestra ventana para seleccionar columnas visibles del resumen"""
        selector_window = customtkinter.CTkToplevel(self)
        selector_window.title("Seleccionar Columnas - Resumen")
        selector_window.geometry("400x500")
        selector_window.transient(self)
        selector_window.grab_set()

        # Título
        title_label = customtkinter.CTkLabel(
            selector_window,
            text="Seleccionar Columnas Visibles",
            font=("", 16, "bold")
        )
        title_label.pack(pady=(20, 10))

        # Scroll frame para checkboxes
        scroll_frame = customtkinter.CTkScrollableFrame(selector_window, width=350, height=350)
        scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Checkboxes
        checkboxes = {}
        for col_name, col_info in self.resumen_columns.items():
            if col_info["locked"]:
                # Columnas bloqueadas (siempre visibles)
                label = customtkinter.CTkLabel(
                    scroll_frame,
                    text=f"✓ {col_info['label']} (siempre visible)",
                    font=("", 12)
                )
                label.pack(anchor="w", pady=5, padx=10)
            else:
                # Columnas opcionales
                var = customtkinter.BooleanVar(value=col_info["visible"])
                cb = customtkinter.CTkCheckBox(
                    scroll_frame,
                    text=col_info["label"],
                    variable=var,
                    font=("", 12)
                )
                cb.pack(anchor="w", pady=5, padx=10)
                checkboxes[col_name] = var

        # Botones
        btn_frame = customtkinter.CTkFrame(selector_window, fg_color="transparent")
        btn_frame.pack(pady=20)

        def aplicar():
            # Actualizar visibilidad
            for col_name, var in checkboxes.items():
                self.resumen_columns[col_name]["visible"] = var.get()

            # Guardar configuración
            self._save_column_config("resumen", self.resumen_columns)

            # Reconstruir tabla
            self._rebuild_resumen_tree()
            selector_window.destroy()

        def cancelar():
            selector_window.destroy()

        btn_aplicar = customtkinter.CTkButton(btn_frame, text="Aplicar", command=aplicar, width=120)
        btn_aplicar.pack(side="left", padx=5)

        btn_cancelar = customtkinter.CTkButton(btn_frame, text="Cancelar", command=cancelar, width=120)
        btn_cancelar.pack(side="left", padx=5)

    def _add_parte_resumen(self):
        """
        Abre ventana mejorada para añadir nuevo parte con todos los campos.
        Incluye: título, estado, descripciones, fechas, localización, municipio, GPS, trabajadores.
        """
        try:
            from interface.parts_interfaz_v2_fixed import AppPartsV2

            # Callback para cuando se crea un parte nuevo
            def on_parte_created(parte_id):
                # Guardar el ID del parte seleccionado para Presupuesto
                self.selected_parte_id = parte_id

                # Recargar el resumen
                self._reload_resumen()

                # Cambiar a la pestaña de "Partes" (que contiene los subtabs)
                self.select_frame_by_name("partes")

                # Recargar el selector de partes
                self._reload_partes_selector()

                # Seleccionar el nuevo parte
                from script.modulo_db import get_partes_resumen
                partes_data = get_partes_resumen(self.user, self.password, self.schema)
                for row in partes_data:
                    if row[0] == parte_id:  # row[0] es el ID
                        parte_text = f"{row[0]} - {row[1]} | {row[4]} | {row[5]} | {row[2] or 'Sin desc.'}"
                        self._set_selected_parte(parte_text)
                        break

                # Ir directamente a la función de Presupuesto del sidebar
                # (no a la pestaña interna de presupuesto)
                self.select_frame_by_name("presupuesto")

                # Recargar el selector de presupuesto para que seleccione el parte nuevo
                if hasattr(self, 'presupuesto_selector'):
                    self._reload_presupuesto_selector()

            # Crear ventana independiente con el formulario mejorado
            parts_window = AppPartsV2(
                user=self.user,
                password=self.password,
                default_schema=self.schema,
                on_parte_created=on_parte_created
            )

            # Hacer que la ventana aparezca al frente
            parts_window.lift()
            parts_window.focus()

        except Exception as e:
            import traceback
            traceback.print_exc()
            CTkMessagebox(title="Error",
                        message=f"No se pudo abrir el formulario de partes:\n{e}",
                        icon="cancel")

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

        # Actualizar el selector para mostrar el parte seleccionado
        if hasattr(self, 'partes_selector'):
            # Buscar el item en el selector que corresponde a este parte_id
            values = self.partes_selector.cget("values")
            for item in values:
                if item.startswith(f"{parte_id} -"):
                    self.partes_selector.set(item)
                    # Cargar las tabs del parte
                    self._load_parte_tabs()
                    break

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

        customtkinter.CTkLabel(selector_frame, text="Buscar Parte:",
                               font=("", 14, "bold")).grid(row=0, column=0, padx=(0, 10), sticky="e")

        # Cargar lista de partes
        try:
            partes_data = get_partes_resumen(self.user, self.password, self.schema)
            self.partes_list = [f"{row[0]} - {row[1]} | {row[4]} | {row[5]} | {row[2] or 'Sin desc.'}"
                           for row in partes_data]  # id - codigo | ot | red | descripcion
            self.partes_list_full = self.partes_list.copy()  # Guardar lista completa
        except:
            self.partes_list = ["Sin partes"]
            self.partes_list_full = ["Sin partes"]

        # Frame contenedor para entry + dropdown
        search_container = customtkinter.CTkFrame(selector_frame, fg_color="transparent")
        search_container.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        search_container.grid_columnconfigure(0, weight=1)

        # Entry de búsqueda
        self.partes_search_entry = customtkinter.CTkEntry(
            search_container,
            placeholder_text="Escriba para buscar parte..."
        )
        self.partes_search_entry.grid(row=0, column=0, sticky="ew")
        self.partes_search_entry.bind('<KeyRelease>', self._filter_partes_list)
        self.partes_search_entry.bind('<Return>', lambda e: self._select_first_match())

        # Frame flotante para dropdown (inicialmente oculto)
        self.partes_dropdown_frame = customtkinter.CTkFrame(
            search_container,
            fg_color="#2b2b2b",
            border_width=1,
            border_color="gray"
        )
        self.partes_dropdown_frame.grid_remove()  # Oculto inicialmente

        # Scrollable frame para lista de partes
        self.partes_listbox_frame = customtkinter.CTkScrollableFrame(
            self.partes_dropdown_frame,
            height=200,
            fg_color="transparent"
        )
        self.partes_listbox_frame.pack(fill="both", expand=True)

        # Variable para almacenar el parte seleccionado
        self.selected_parte_text = None

        # Seleccionar primer parte por defecto
        if self.partes_list and self.partes_list[0] != "Sin partes":
            self._set_selected_parte(self.partes_list[0])
            if hasattr(self, 'selected_parte_id'):
                # Si viene desde Resumen con un parte seleccionado
                for item in self.partes_list:
                    if item.startswith(f"{self.selected_parte_id} -"):
                        self._set_selected_parte(item)
                        break

        btn_reload = customtkinter.CTkButton(
            selector_frame, text="🔄", width=40,
            command=lambda: self._reload_partes_selector()
        )
        btn_reload.grid(row=0, column=2)

        # Frame principal que contendrá los sub-tabs
        self.partes_content_frame = customtkinter.CTkFrame(self.partes_frame)
        self.partes_content_frame.grid(row=2, column=0, padx=30, pady=(0, 20), sticky="nsew", columnspan=2)
        self.partes_content_frame.grid_columnconfigure(0, weight=1)
        self.partes_content_frame.grid_rowconfigure(0, weight=1)  # FIX: era 1, debe ser 0 para que el tabview se expanda

        # Sub-tabs
        self.partes_subtabs = customtkinter.CTkTabview(self.partes_content_frame)
        self.partes_subtabs.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        # CTkTabview gestiona su propio layout interno, no necesita configuración de grid

        # Crear las 3 pestañas
        self.partes_subtabs.add("📝 Datos Básicos")
        self.partes_subtabs.add("💰 Presupuesto")
        self.partes_subtabs.add("📅 Certificaciones")

        # NOTA: No configurar grid para los tabs individuales porque usan pack() para el contenido

        # Cargar datos si hay partes
        if self.partes_list and self.partes_list[0] != "Sin partes":
            self._load_parte_tabs()

    def _filter_partes_list(self, event=None):
        """Filtra la lista de partes según el texto de búsqueda"""
        search_text = self.partes_search_entry.get().lower()

        if not search_text:
            # Si está vacío, ocultar dropdown
            self.partes_dropdown_frame.grid_remove()
            return

        # Filtrar partes que contengan el texto de búsqueda
        filtered = [p for p in self.partes_list_full if search_text in p.lower()]

        # Limpiar listbox
        for widget in self.partes_listbox_frame.winfo_children():
            widget.destroy()

        if filtered:
            # Mostrar dropdown
            self.partes_dropdown_frame.grid(row=1, column=0, sticky="ew", pady=(2, 0))

            # Crear botones para cada resultado (máximo 10)
            for parte in filtered[:10]:
                btn = customtkinter.CTkButton(
                    self.partes_listbox_frame,
                    text=parte,
                    anchor="w",
                    fg_color="transparent",
                    hover_color="#1f6aa5",
                    command=lambda p=parte: self._select_parte_from_dropdown(p)
                )
                btn.pack(fill="x", padx=2, pady=1)

            # Mostrar contador si hay más resultados
            if len(filtered) > 10:
                info_label = customtkinter.CTkLabel(
                    self.partes_listbox_frame,
                    text=f"... y {len(filtered) - 10} más. Refine su búsqueda.",
                    text_color="gray",
                    font=("", 10)
                )
                info_label.pack(pady=5)
        else:
            # Ocultar si no hay resultados
            self.partes_dropdown_frame.grid_remove()

    def _select_parte_from_dropdown(self, parte_text):
        """Selecciona un parte del dropdown"""
        self._set_selected_parte(parte_text)
        self.partes_dropdown_frame.grid_remove()
        self._load_parte_tabs()

    def _select_first_match(self):
        """Selecciona el primer resultado cuando se presiona Enter"""
        search_text = self.partes_search_entry.get().lower()
        if search_text:
            filtered = [p for p in self.partes_list_full if search_text in p.lower()]
            if filtered:
                self._set_selected_parte(filtered[0])
                self.partes_dropdown_frame.grid_remove()
                self._load_parte_tabs()

    def _set_selected_parte(self, parte_text):
        """Establece el parte seleccionado"""
        self.selected_parte_text = parte_text
        self.partes_search_entry.delete(0, 'end')
        self.partes_search_entry.insert(0, parte_text)

    def _reload_partes_selector(self):
        """Recarga el selector de partes"""
        from script.modulo_db import get_partes_resumen

        try:
            partes_data = get_partes_resumen(self.user, self.password, self.schema)
            self.partes_list = [f"{row[0]} - {row[1]} | {row[4]} | {row[5]} | {row[2] or 'Sin desc.'}"
                           for row in partes_data]
            self.partes_list_full = self.partes_list.copy()

            if self.partes_list:
                self._set_selected_parte(self.partes_list[0])
                self._load_parte_tabs()
            else:
                self.partes_list = ["Sin partes"]
                self.partes_list_full = ["Sin partes"]
                self.partes_search_entry.delete(0, 'end')
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error recargando:\n{e}", icon="cancel")

    def _load_parte_tabs(self):
        """Carga el contenido de las 3 sub-pestañas"""
        selected = self.selected_parte_text if hasattr(self, 'selected_parte_text') else None
        if not selected or selected == "Sin partes":
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
        from script.modulo_db import get_parte_detail, get_dim_all, get_provincias, get_municipios_by_provincia
        from tkcalendar import DateEntry

        # Bandera para evitar marcar como cambiado durante la carga inicial
        self._loading_initial_data = True

        tab = self.partes_subtabs.tab("📝 Datos Básicos")

        # Limpiar
        for widget in tab.winfo_children():
            widget.destroy()

        # Frame scrollable para contener todo el contenido - usar pack para CTkScrollableFrame
        scroll_frame = customtkinter.CTkScrollableFrame(tab, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Frame principal dentro del scroll
        main_frame = customtkinter.CTkFrame(scroll_frame, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        try:
            parte_data = get_parte_detail(self.user, self.password, self.schema, parte_id)
            if not parte_data:
                customtkinter.CTkLabel(main_frame, text="❌ No se encontró el parte").grid(row=0, column=0, pady=20)
                return

            dims = get_dim_all(self.user, self.password, self.schema)

            # Variable para rastrear si hay cambios
            self.has_changes = False

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

            # ID (solo lectura)
            customtkinter.CTkLabel(left_frame, text="ID:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")
            customtkinter.CTkLabel(left_frame, text=str(parte_data[0])).grid(
                row=row_left, column=1, padx=5, pady=8, sticky="w")
            row_left += 1

            # Código (solo lectura)
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

            # NUEVO: Título
            customtkinter.CTkLabel(left_frame, text="Título:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")
            self.titulo_entry = customtkinter.CTkEntry(left_frame)
            self.titulo_entry.grid(row=row_left, column=1, padx=5, pady=8, sticky="ew")
            if parte_data[12]:
                self.titulo_entry.insert(0, parte_data[12])
            row_left += 1

            # Estado - ComboBox con mapeo a IDs
            customtkinter.CTkLabel(left_frame, text="Estado:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")

            # Mapeo de estados: texto → ID (según tbl_parte_estados)
            self.estados_map = {
                "Pendiente": 1,
                "En curso": 2,
                "Finalizado": 3,
                "Cancelado": 4
            }
            self.estados_reverse_map = {v: k for k, v in self.estados_map.items()}

            # Obtener estado actual (puede ser ID o texto por compatibilidad)
            estado_actual = parte_data[3] or 1  # Por defecto ID 1 (Pendiente)
            if isinstance(estado_actual, int):
                # Es un ID, convertir a texto
                estado_texto = self.estados_reverse_map.get(estado_actual, "Pendiente")
            else:
                # Es texto, usar directamente
                estado_texto = estado_actual if estado_actual in self.estados_map else "Pendiente"

            self.estado_var = customtkinter.StringVar(value=estado_texto)
            self.estado_menu = customtkinter.CTkOptionMenu(
                left_frame, variable=self.estado_var,
                values=["Pendiente", "En curso", "Finalizado", "Cancelado"]
            )
            self.estado_menu.grid(row=row_left, column=1, padx=5, pady=8, sticky="ew")
            row_left += 1

            # Red
            customtkinter.CTkLabel(left_frame, text="Red:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")
            self.red_menu = customtkinter.CTkOptionMenu(left_frame, values=dims.get("RED", []))
            self.red_menu.grid(row=row_left, column=1, padx=5, pady=8, sticky="ew")
            for item in dims.get("RED", []):
                if item.startswith(f"{parte_data[4]} -"):  # Actualizado: era 5, ahora 4
                    self.red_menu.set(item)
                    break
            row_left += 1

            # Tipo Trabajo
            customtkinter.CTkLabel(left_frame, text="Tipo Trabajo:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")
            self.tipo_menu = customtkinter.CTkOptionMenu(left_frame, values=dims.get("TIPO_TRABAJO", []))
            self.tipo_menu.grid(row=row_left, column=1, padx=5, pady=8, sticky="ew")
            for item in dims.get("TIPO_TRABAJO", []):
                if item.startswith(f"{parte_data[5]} -"):  # Actualizado: era 6, ahora 5
                    self.tipo_menu.set(item)
                    break
            row_left += 1

            # Código trabajo
            customtkinter.CTkLabel(left_frame, text="Código Trabajo:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")
            self.cod_menu = customtkinter.CTkOptionMenu(left_frame, values=dims.get("COD_TRABAJO", []))
            self.cod_menu.grid(row=row_left, column=1, padx=5, pady=8, sticky="ew")
            for item in dims.get("COD_TRABAJO", []):
                if item.startswith(f"{parte_data[6]} -"):  # Actualizado: era 7, ahora 6
                    self.cod_menu.set(item)
                    break
            row_left += 1

            # Tipo de Reparación
            customtkinter.CTkLabel(left_frame, text="Tipo Reparación:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")
            self.tipo_rep_menu = customtkinter.CTkOptionMenu(left_frame, values=dims.get("TIPOS_REP", []))
            self.tipo_rep_menu.grid(row=row_left, column=1, padx=5, pady=8, sticky="ew")
            for item in dims.get("TIPOS_REP", []):
                if parte_data[7] and item.startswith(f"{parte_data[7]} -"):  # Actualizado: era 8, ahora 7
                    self.tipo_rep_menu.set(item)
                    break
            row_left += 1

            # Provincia
            customtkinter.CTkLabel(left_frame, text="Provincia:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")
            provincias_list = get_provincias(self.user, self.password, self.schema)
            self.provincia_menu = customtkinter.CTkOptionMenu(
                left_frame,
                values=provincias_list,
                command=self._on_provincia_change
            )
            self.provincia_menu.grid(row=row_left, column=1, padx=5, pady=8, sticky="ew")
            row_left += 1

            # Municipio - CREAR ANTES de establecer la provincia
            customtkinter.CTkLabel(left_frame, text="Municipio:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")
            self.municipio_menu = customtkinter.CTkOptionMenu(left_frame, values=["Seleccione provincia primero"])
            self.municipio_menu.grid(row=row_left, column=1, padx=5, pady=8, sticky="ew")
            row_left += 1

            # AHORA establecer provincia y municipio
            current_municipio_id = parte_data[8]  # Actualizado: era 9, ahora 8
            if current_municipio_id:
                # Obtener provincia del municipio actual
                try:
                    with get_project_connection(self.user, self.password, self.schema) as cn:
                        cur = cn.cursor()
                        # FIX: Tabla correcta es dim_municipios (con 's'), no dim_municipio
                        cur.execute(f"SELECT provincia_id FROM {self.schema}.dim_municipios WHERE id = %s", (current_municipio_id,))
                        result = cur.fetchone()
                        if result:
                            provincia_id = result[0]

                            # Cargar municipios de esta provincia ANTES de establecer provincia
                            municipios_list = get_municipios_by_provincia(self.user, self.password, self.schema, provincia_id)
                            self.municipio_menu.configure(values=municipios_list)

                            # Establecer provincia (esto dispara _on_provincia_change que actualiza lista de municipios)
                            for item in provincias_list:
                                if item.startswith(f"{provincia_id} -"):
                                    self.provincia_menu.set(item)
                                    break

                            # Establecer municipio DESPUES de establecer provincia
                            # La lista ya fue actualizada por _on_provincia_change
                            for item in municipios_list:
                                if item.startswith(f"{current_municipio_id} -"):
                                    self.municipio_menu.set(item)
                                    break
                        cur.close()
                except Exception as e:
                    print(f"Error al cargar provincia/municipio: {e}")
                    import traceback
                    traceback.print_exc()

            # Separador
            customtkinter.CTkFrame(left_frame, height=2, fg_color="gray40").grid(
                row=row_left, column=0, columnspan=2, pady=15, sticky="ew")
            row_left += 1

            # NUEVO: Fecha Inicio
            customtkinter.CTkLabel(left_frame, text="Fecha Inicio:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")
            self.fecha_inicio_entry = DateEntry(left_frame, width=20, background='darkblue',
                                             foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            self.fecha_inicio_entry.grid(row=row_left, column=1, padx=5, pady=8, sticky="w")
            if parte_data[13]:
                try:
                    self.fecha_inicio_entry.set_date(parte_data[13])
                except:
                    pass
            row_left += 1

            # NUEVO: Fecha Fin
            customtkinter.CTkLabel(left_frame, text="Fecha Fin:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")
            self.fecha_fin_entry = DateEntry(left_frame, width=20, background='darkblue',
                                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            self.fecha_fin_entry.grid(row=row_left, column=1, padx=5, pady=8, sticky="w")
            if parte_data[14]:
                try:
                    self.fecha_fin_entry.set_date(parte_data[14])
                except:
                    pass
            row_left += 1

            # NUEVO: Trabajadores
            customtkinter.CTkLabel(left_frame, text="Trabajadores:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")
            self.trabajadores_entry = customtkinter.CTkEntry(left_frame)
            self.trabajadores_entry.grid(row=row_left, column=1, padx=5, pady=8, sticky="ew")
            if parte_data[18]:
                self.trabajadores_entry.insert(0, parte_data[18])
            row_left += 1

            # NUEVO: Localización
            customtkinter.CTkLabel(left_frame, text="Localización:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")
            self.localizacion_entry = customtkinter.CTkEntry(left_frame)
            self.localizacion_entry.grid(row=row_left, column=1, padx=5, pady=8, sticky="ew")
            if parte_data[15]:
                self.localizacion_entry.insert(0, parte_data[15])
            row_left += 1

            # NUEVO: Coordenadas GPS
            customtkinter.CTkLabel(left_frame, text="Latitud:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")
            self.latitud_entry = customtkinter.CTkEntry(left_frame, placeholder_text="41.123456")
            self.latitud_entry.grid(row=row_left, column=1, padx=5, pady=8, sticky="ew")
            if parte_data[16]:
                self.latitud_entry.insert(0, str(parte_data[16]))
            row_left += 1

            customtkinter.CTkLabel(left_frame, text="Longitud:", font=("", 12, "bold")).grid(
                row=row_left, column=0, padx=5, pady=8, sticky="e")
            self.longitud_entry = customtkinter.CTkEntry(left_frame, placeholder_text="2.123456")
            self.longitud_entry.grid(row=row_left, column=1, padx=5, pady=8, sticky="ew")
            if parte_data[17]:
                self.longitud_entry.insert(0, str(parte_data[17]))
            row_left += 1

            # Separador
            customtkinter.CTkFrame(left_frame, height=2, fg_color="gray40").grid(
                row=row_left, column=0, columnspan=2, pady=15, sticky="ew")
            row_left += 1

            # Fechas de auditoría (info solo lectura)
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
            # No dar weight a las filas para que no se expandan y empujen el botón fuera de pantalla

            # Descripción
            customtkinter.CTkLabel(
                right_frame, text="Descripción:", font=("", 13, "bold")
            ).grid(row=0, column=0, padx=5, pady=(0, 5), sticky="w")

            self.desc_text = customtkinter.CTkTextbox(right_frame, height=120)
            self.desc_text.grid(row=1, column=0, padx=5, pady=(0, 15), sticky="ew")
            if parte_data[2]:
                self.desc_text.insert("1.0", parte_data[2])

            # Observaciones
            customtkinter.CTkLabel(
                right_frame, text="Observaciones:", font=("", 13, "bold")
            ).grid(row=2, column=0, padx=5, pady=(0, 5), sticky="w")

            self.obs_text = customtkinter.CTkTextbox(right_frame, height=120)
            self.obs_text.grid(row=3, column=0, padx=5, pady=(0, 15), sticky="ew")
            if parte_data[9]:
                self.obs_text.insert("1.0", parte_data[9])

            # Botón guardar (span completo) - inicialmente deshabilitado
            self.btn_save_parte = customtkinter.CTkButton(
                right_frame, text="💾 GUARDAR CAMBIOS",
                command=lambda: self._confirm_and_save_parte(parte_id),
                fg_color="gray", hover_color="gray",
                height=50, font=("", 16, "bold"),
                state="disabled"
            )
            self.btn_save_parte.grid(row=4, column=0, padx=5, pady=15, sticky="ew")

            # Conectar eventos de cambio a todos los widgets
            self._connect_change_events()

            # Desactivar bandera de carga inicial
            self._loading_initial_data = False

        except Exception as e:
            import traceback
            print(f"ERROR:\n{traceback.format_exc()}")
            customtkinter.CTkLabel(main_frame, text=f"❌ Error: {e}").grid(row=0, column=0, pady=20)

    def _mark_as_changed(self, *args):
        """Marca que hay cambios pendientes y habilita el botón guardar"""
        # No marcar como cambiado si estamos cargando datos iniciales
        if hasattr(self, '_loading_initial_data') and self._loading_initial_data:
            return

        if not self.has_changes:
            self.has_changes = True
            if hasattr(self, 'btn_save_parte'):
                self.btn_save_parte.configure(
                    state="normal",
                    fg_color="green",
                    hover_color="#006400"
                )

    def _connect_change_events(self):
        """Conecta eventos de cambio a todos los widgets editables"""
        # Entry widgets
        if hasattr(self, 'titulo_entry'):
            self.titulo_entry.bind('<KeyRelease>', self._mark_as_changed)
        if hasattr(self, 'trabajadores_entry'):
            self.trabajadores_entry.bind('<KeyRelease>', self._mark_as_changed)
        if hasattr(self, 'localizacion_entry'):
            self.localizacion_entry.bind('<KeyRelease>', self._mark_as_changed)
        if hasattr(self, 'latitud_entry'):
            self.latitud_entry.bind('<KeyRelease>', self._mark_as_changed)
        if hasattr(self, 'longitud_entry'):
            self.longitud_entry.bind('<KeyRelease>', self._mark_as_changed)

        # OptionMenu widgets (usan command en lugar de bind)
        if hasattr(self, 'estado_menu'):
            self.estado_menu.configure(command=lambda _: self._mark_as_changed())
        if hasattr(self, 'red_menu'):
            self.red_menu.configure(command=lambda _: self._mark_as_changed())
        if hasattr(self, 'tipo_menu'):
            self.tipo_menu.configure(command=lambda _: self._mark_as_changed())
        if hasattr(self, 'cod_menu'):
            self.cod_menu.configure(command=lambda _: self._mark_as_changed())
        if hasattr(self, 'tipo_rep_menu'):
            self.tipo_rep_menu.configure(command=lambda _: self._mark_as_changed())
        if hasattr(self, 'municipio_menu'):
            self.municipio_menu.configure(command=lambda _: self._mark_as_changed())
        # Nota: provincia_menu ya tiene command=self._on_provincia_change que marca cambios

        # Textbox widgets
        if hasattr(self, 'desc_text'):
            self.desc_text.bind('<KeyRelease>', self._mark_as_changed)
        if hasattr(self, 'obs_text'):
            self.obs_text.bind('<KeyRelease>', self._mark_as_changed)

        # DateEntry widgets (se activan cuando se selecciona una fecha)
        if hasattr(self, 'fecha_inicio_entry'):
            self.fecha_inicio_entry.bind('<<DateEntrySelected>>', self._mark_as_changed)
        if hasattr(self, 'fecha_fin_entry'):
            self.fecha_fin_entry.bind('<<DateEntrySelected>>', self._mark_as_changed)

    def _on_provincia_change(self, selected_provincia):
        """Actualiza lista de municipios cuando cambia la provincia"""
        from script.modulo_db import get_municipios_by_provincia

        # Si estamos cargando datos iniciales, NO hacer nada
        # La carga inicial se encarga de configurar todo correctamente
        if hasattr(self, '_loading_initial_data') and self._loading_initial_data:
            return

        try:
            provincia_id = int(selected_provincia.split(" - ")[0])
            municipios_list = get_municipios_by_provincia(self.user, self.password, self.schema, provincia_id)

            if hasattr(self, 'municipio_menu'):
                # Actualizar la lista de municipios disponibles para esta provincia
                if municipios_list:
                    self.municipio_menu.configure(values=municipios_list)

                    # Es un cambio manual del usuario
                    current_municipio = self.municipio_menu.get()

                    # Solo mantener el municipio actual si está en la nueva lista
                    if current_municipio not in municipios_list:
                        # El municipio actual no pertenece a la nueva provincia seleccionada
                        # No seleccionar automáticamente ninguno, dejar vacío
                        self.municipio_menu.set("")

            # Marcar como cambiado
            self._mark_as_changed()
        except Exception as e:
            print(f"Error al cambiar provincia: {e}")

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
            # Extraer IDs de dimensiones
            red_id = int(self.red_menu.get().split(" - ")[0])
            tipo_id = int(self.tipo_menu.get().split(" - ")[0])
            cod_id = int(self.cod_menu.get().split(" - ")[0])

            # Tipo de reparación
            tipo_rep_id = None
            try:
                tipo_rep_text = self.tipo_rep_menu.get()
                if tipo_rep_text and not tipo_rep_text.startswith("Seleccione") and " - " in tipo_rep_text:
                    tipo_rep_id = int(tipo_rep_text.split(" - ")[0])
            except:
                pass

            # Municipio
            municipio_id = None
            try:
                municipio_text = self.municipio_menu.get()
                if municipio_text and not municipio_text.startswith("Seleccione"):
                    municipio_id = int(municipio_text.split(" - ")[0])
            except:
                pass

            # Campos de texto
            titulo = self.titulo_entry.get().strip() or None
            descripcion = self.desc_text.get("1.0", "end-1c").strip() or None
            estado_texto = self.estado_var.get()
            # Convertir texto a ID numérico (según tbl_parte_estados)
            estado_id = self.estados_map.get(estado_texto, 1)  # Por defecto 1 (Pendiente)
            observaciones = self.obs_text.get("1.0", "end-1c").strip() or None
            trabajadores = self.trabajadores_entry.get().strip() or None
            localizacion = self.localizacion_entry.get().strip() or None

            # Fechas
            fecha_inicio = self.fecha_inicio_entry.get_date() if hasattr(self.fecha_inicio_entry, 'get_date') else None
            fecha_fin = self.fecha_fin_entry.get_date() if hasattr(self.fecha_fin_entry, 'get_date') else None

            # Coordenadas GPS
            latitud = None
            longitud = None
            try:
                lat_text = self.latitud_entry.get().strip()
                if lat_text:
                    latitud = float(lat_text)
            except ValueError:
                pass

            try:
                lon_text = self.longitud_entry.get().strip()
                if lon_text:
                    longitud = float(lon_text)
            except ValueError:
                pass

            # VALIDACIÓN: Fecha fin obligatoria si estado es "Finalizado"
            if estado_texto == "Finalizado" and not fecha_fin:
                CTkMessagebox(
                    title="Campo obligatorio",
                    message="⚠️ El campo 'Fecha Fin' es obligatorio cuando el estado es 'Finalizado'",
                    icon="warning"
                )
                return

            print(f"DEBUG - Guardando parte {parte_id}:")
            print(f"  IDs: Red={red_id}, Tipo={tipo_id}, Cod={cod_id}, TipoRep={tipo_rep_id}, Municipio={municipio_id}")
            print(f"  Título: {titulo}")
            print(f"  Estado: {estado_texto} (ID: {estado_id})")
            print(f"  Fechas: inicio={fecha_inicio}, fin={fecha_fin}")
            print(f"  Trabajadores: {trabajadores}")
            print(f"  Localización: {localizacion}")
            print(f"  GPS: {latitud}, {longitud}")

            result = mod_parte_item(
                self.user, self.password, self.schema, parte_id,
                red_id, tipo_id, cod_id,
                descripcion=descripcion,
                estado=estado_id,
                observaciones=observaciones,
                municipio_id=municipio_id,
                tipo_rep_id=tipo_rep_id,
                titulo=titulo,
                fecha_fin=fecha_fin,
                trabajadores=trabajadores,
                localizacion=localizacion,
                latitud=latitud,
                longitud=longitud
            )

            print(f"DEBUG - Resultado: {result}")

            if result == "ok":
                # Resetear estado de cambios
                self.has_changes = False
                if hasattr(self, 'btn_save_parte'):
                    self.btn_save_parte.configure(
                        state="disabled",
                        fg_color="gray",
                        hover_color="gray"
                    )

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

        # Frame principal - usar pack para mejor expansión
        main_frame = customtkinter.CTkFrame(tab, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
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
            customtkinter.CTkLabel(table_frame, text=f"❌ Error: {e}").grid(row=0, column=0, pady=20)

    def _load_certificaciones_tab(self, parte_id):
        """Carga la pestaña de Certificaciones (solo lectura)"""
        from tkinter import ttk
        from script.modulo_db import get_part_cert_certificadas

        tab = self.partes_subtabs.tab("📅 Certificaciones")

        # Limpiar
        for widget in tab.winfo_children():
            widget.destroy()

        # Frame principal - usar pack para mejor expansión
        main_frame = customtkinter.CTkFrame(tab, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
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
            customtkinter.CTkLabel(table_frame, text=f"❌ Error: {e}").grid(row=0, column=0, pady=20)

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

        # Título y botón de certificación por lotes
        title_frame = customtkinter.CTkFrame(self.certificaciones_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=30, pady=(20, 10), sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)

        title = customtkinter.CTkLabel(
            title_frame,
            text="CERTIFICACIONES POR PARTE",
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        title.pack(side="left")

        btn_cert_lotes = customtkinter.CTkButton(
            title_frame,
            text="📦 Certificación por Lotes",
            command=self._open_cert_lotes,
            font=customtkinter.CTkFont(size=14, weight="bold"),
            fg_color="#FF9800",
            hover_color="#F57C00",
            height=35,
            width=220
        )
        btn_cert_lotes.pack(side="right", padx=(10, 0))

        # Selector de parte
        selector_frame = customtkinter.CTkFrame(self.certificaciones_frame, fg_color="transparent")
        selector_frame.grid(row=1, column=0, padx=30, pady=(0, 10), sticky="ew")
        selector_frame.grid_columnconfigure(1, weight=1)

        customtkinter.CTkLabel(selector_frame, text="Buscar Parte:",
                               font=("", 14, "bold")).grid(row=0, column=0, padx=(0, 10), sticky="e")

        # Cargar lista de partes completa para búsqueda
        try:
            partes_data = get_partes_resumen(self.user, self.password, self.schema)
            self.cert_list = [f"{row[0]} - {row[1]} | {row[4]} | {row[5]}" for row in partes_data]
            self.cert_list_full = self.cert_list.copy()
        except:
            self.cert_list = ["Sin partes"]
            self.cert_list_full = self.cert_list.copy()

        # Frame contenedor para Entry + Dropdown
        search_container_cert = customtkinter.CTkFrame(selector_frame, fg_color="transparent")
        search_container_cert.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        search_container_cert.grid_rowconfigure(0, weight=1)
        search_container_cert.grid_columnconfigure(0, weight=1)

        # Entry para búsqueda con dropdown
        self.cert_search_entry = customtkinter.CTkEntry(
            search_container_cert,
            placeholder_text="Escriba para buscar parte..."
        )
        self.cert_search_entry.grid(row=0, column=0, sticky="ew")
        self.cert_search_entry.bind('<KeyRelease>', self._filter_cert_list)
        self.cert_search_entry.bind('<Return>', lambda e: self._select_first_cert_match())

        # Frame flotante para dropdown (inicialmente oculto)
        self.cert_dropdown_frame = customtkinter.CTkFrame(
            search_container_cert,
            fg_color="#2b2b2b",
            border_width=1,
            border_color="gray"
        )
        self.cert_dropdown_frame.grid_remove()  # Oculto inicialmente

        # Listbox para mostrar resultados filtrados
        self.cert_listbox = ttk.Treeview(
            self.cert_dropdown_frame,
            columns=("partes",),
            show="tree",
            selectmode="browse",
            height=10
        )
        self.cert_listbox.pack(fill="both", expand=True)
        self.cert_listbox.bind("<ButtonRelease-1>", self._on_cert_select)
        self.cert_listbox.bind("<Return>", self._on_cert_select)

        # Seleccionar primer parte si hay selected_parte_id
        if self.cert_list and self.cert_list[0] != "Sin partes":
            if hasattr(self, 'selected_parte_id'):
                for item in self.cert_list:
                    if item.startswith(f"{self.selected_parte_id} -"):
                        self._set_selected_cert(item)
                        break
            else:
                self._set_selected_cert(self.cert_list[0])

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
        if self.cert_list and self.cert_list[0] != "Sin partes":
            self._load_certificaciones_data()

    def _filter_cert_list(self, event=None):
        """Filtra la lista de partes en certificaciones según el texto de búsqueda"""
        search_text = self.cert_search_entry.get().lower()

        if not search_text:
            # Si está vacío, ocultar dropdown
            self.cert_dropdown_frame.grid_remove()
            return

        # Filtrar partes que contengan el texto de búsqueda
        filtered = [p for p in self.cert_list_full if search_text in p.lower()]

        # Limpiar listbox
        for item in self.cert_listbox.get_children():
            self.cert_listbox.delete(item)

        # Mostrar dropdown solo si hay resultados
        if filtered:
            # Limitar a 10 resultados para no sobrecargar
            for parte in filtered[:10]:
                self.cert_listbox.insert("", "end", text=parte, values=(parte,))

            # Mostrar dropdown debajo del entry
            self.cert_dropdown_frame.grid(row=1, column=0, sticky="ew", pady=(2, 0))
        else:
            self.cert_dropdown_frame.grid_remove()

    def _on_cert_select(self, event=None):
        """Maneja la selección de un parte del dropdown en certificaciones"""
        selection = self.cert_listbox.selection()
        if selection:
            item = selection[0]
            parte_text = self.cert_listbox.item(item, "text")
            self._set_selected_cert(parte_text)
            self.cert_dropdown_frame.grid_remove()
            self._load_certificaciones_data()

    def _select_first_cert_match(self):
        """Selecciona el primer resultado del filtro en certificaciones"""
        search_text = self.cert_search_entry.get().lower()
        if search_text:
            filtered = [p for p in self.cert_list_full if search_text in p.lower()]
            if filtered:
                self._set_selected_cert(filtered[0])
                self.cert_dropdown_frame.grid_remove()
                self._load_certificaciones_data()

    def _set_selected_cert(self, parte_text):
        """Establece el parte seleccionado en certificaciones"""
        self.selected_cert_text = parte_text
        self.cert_search_entry.delete(0, 'end')
        self.cert_search_entry.insert(0, parte_text)

    def _reload_cert_selector(self):
        """Recarga el selector de partes en certificaciones"""
        from script.modulo_db import get_partes_resumen

        try:
            partes_data = get_partes_resumen(self.user, self.password, self.schema)
            self.cert_list = [f"{row[0]} - {row[1]} | {row[4]} | {row[5]}" for row in partes_data]
            self.cert_list_full = self.cert_list.copy()

            if self.cert_list:
                self._set_selected_cert(self.cert_list[0])
                self._load_certificaciones_data()
            else:
                self.cert_search_entry.delete(0, 'end')
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

        # Usar el texto seleccionado del sistema de búsqueda incremental
        selected = getattr(self, 'selected_cert_text', '')
        if not selected or selected == "Sin partes":
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

    def _open_cert_lotes(self):
        """Abre la ventana de Certificación por Lotes"""
        try:
            from interface.cert_lotes_interfaz import CertLotesWindow

            # Crear ventana de certificación por lotes
            cert_window = CertLotesWindow(
                parent=self,
                user=self.user,
                password=self.password,
                schema=self.schema
            )

            # Hacer que la ventana aparezca al frente
            cert_window.lift()
            cert_window.focus()

        except Exception as e:
            import traceback
            traceback.print_exc()
            CTkMessagebox(
                title="Error",
                message=f"No se pudo abrir Certificación por Lotes:\n{e}",
                icon="cancel"
            )

    def main_informes(self):
        """Pestaña Informes - Generación de informes personalizados"""
        from interface.informes_interfaz import InformesFrame

        self.informes_frame.grid_columnconfigure(0, weight=1)
        self.informes_frame.grid_rowconfigure(0, weight=1)

        # Crear el frame de informes completo
        informes_app = InformesFrame(
            self.informes_frame,
            user=self.user,
            password=self.password,
            schema=self.schema
        )
        informes_app.grid(row=0, column=0, sticky="nsew")

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