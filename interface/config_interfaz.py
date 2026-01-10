"""
Ventana de Configuración del Sistema.
Permite gestionar variables del sistema y catálogo de partidas.
"""

import os
import customtkinter
from tkinter import ttk
from CTkMessagebox import CTkMessagebox

# Ruta del proyecto
parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppConfiguracion(customtkinter.CTkToplevel):
    """Ventana principal de configuración del sistema."""

    def __init__(self, parent, user: str, password: str, schema: str):
        super().__init__(parent)

        self.user = user
        self.password = password
        self.schema = schema
        self.parent = parent

        # Configuración de ventana
        self.title("Configuración del Sistema")
        self.geometry("1000x700")
        self.minsize(900, 600)

        # Hacer modal
        self.transient(parent)
        self.grab_set()

        # Configurar grid principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Crear interfaz
        self._create_header()
        self._create_tabs()

        # Centrar ventana
        self.update_idletasks()
        self._center_window()

        # Focus
        self.lift()
        self.focus_force()

    def _center_window(self):
        """Centra la ventana en la pantalla."""
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _create_header(self):
        """Crea el encabezado de la ventana."""
        header_frame = customtkinter.CTkFrame(self, corner_radius=0, height=60)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_columnconfigure(0, weight=1)

        # Título
        title_label = customtkinter.CTkLabel(
            header_frame,
            text="⚙️ Configuración del Sistema",
            font=customtkinter.CTkFont(size=22, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        # Botón cerrar
        close_btn = customtkinter.CTkButton(
            header_frame,
            text="✕ Cerrar",
            width=100,
            fg_color="transparent",
            hover_color=("gray70", "gray30"),
            command=self.destroy
        )
        close_btn.grid(row=0, column=1, padx=20, pady=15, sticky="e")

    def _create_tabs(self):
        """Crea las pestañas principales."""
        self.tabview = customtkinter.CTkTabview(self, corner_radius=10)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))

        # Crear pestañas
        self.tabview.add("📊 Gestión de Variables")
        self.tabview.add("📦 Catálogo de Partidas")

        # Configurar contenido de cada pestaña
        self._setup_variables_tab()
        self._setup_catalogo_tab()

    # =========================================================================
    # PESTAÑA: GESTIÓN DE VARIABLES
    # =========================================================================

    def _setup_variables_tab(self):
        """Configura la pestaña de gestión de variables."""
        tab = self.tabview.tab("📊 Gestión de Variables")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        # Frame scrollable para las secciones
        scroll_frame = customtkinter.CTkScrollableFrame(tab, fg_color="transparent")
        scroll_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        scroll_frame.grid_columnconfigure(0, weight=1)

        # Secciones de dimensiones
        self.dim_sections = {}

        # Sección: Redes
        self._create_dimension_section(
            scroll_frame, row=0,
            title="🌐 Redes",
            table_name="dim_red",
            description="Gestiona los tipos de red disponibles (Abastecimiento, Saneamiento, etc.)"
        )

        # Sección: Tipos de Reparación
        self._create_dimension_section(
            scroll_frame, row=1,
            title="🔧 Tipos de Reparación",
            table_name="dim_tipos_rep",
            description="Gestiona los tipos de reparación (Fuga, Atasco, etc.)"
        )

        # Sección: Códigos de Trabajo
        self._create_dimension_section(
            scroll_frame, row=2,
            title="📝 Códigos de Trabajo",
            table_name="dim_codigo_trabajo",
            description="Gestiona los códigos de trabajo programado"
        )

    def _create_dimension_section(self, parent, row: int, title: str,
                                   table_name: str, description: str):
        """Crea una sección colapsable para una tabla de dimensiones."""
        # Frame contenedor de la sección
        section_frame = customtkinter.CTkFrame(parent, corner_radius=10)
        section_frame.grid(row=row, column=0, sticky="ew", padx=5, pady=10)
        section_frame.grid_columnconfigure(0, weight=1)

        # Header de la sección (clickeable para expandir/colapsar)
        header_frame = customtkinter.CTkFrame(section_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header_frame.grid_columnconfigure(1, weight=1)

        # Botón expandir/colapsar
        expand_btn = customtkinter.CTkButton(
            header_frame,
            text="▼",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=("gray70", "gray30"),
            font=customtkinter.CTkFont(size=14)
        )
        expand_btn.grid(row=0, column=0, padx=(0, 10))

        # Título
        title_label = customtkinter.CTkLabel(
            header_frame,
            text=title,
            font=customtkinter.CTkFont(size=16, weight="bold")
        )
        title_label.grid(row=0, column=1, sticky="w")

        # Descripción
        desc_label = customtkinter.CTkLabel(
            header_frame,
            text=description,
            font=customtkinter.CTkFont(size=11),
            text_color="gray"
        )
        desc_label.grid(row=1, column=1, sticky="w", pady=(5, 0))

        # Contenido (inicialmente visible)
        content_frame = customtkinter.CTkFrame(section_frame, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        content_frame.grid_columnconfigure(0, weight=1)

        # Guardar referencia
        self.dim_sections[table_name] = {
            'frame': content_frame,
            'expanded': True,
            'expand_btn': expand_btn
        }

        # Configurar toggle
        expand_btn.configure(command=lambda t=table_name: self._toggle_section(t))

        # Crear contenido de la sección
        self._create_dimension_content(content_frame, table_name)

    def _toggle_section(self, table_name: str):
        """Expande o colapsa una sección."""
        section = self.dim_sections[table_name]
        if section['expanded']:
            section['frame'].grid_remove()
            section['expand_btn'].configure(text="▶")
            section['expanded'] = False
        else:
            section['frame'].grid()
            section['expand_btn'].configure(text="▼")
            section['expanded'] = True

    def _create_dimension_content(self, parent, table_name: str):
        """Crea el contenido de una sección de dimensiones."""
        # TreeView para mostrar registros
        tree_frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        tree_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        tree_frame.grid_columnconfigure(0, weight=1)

        # Configurar estilo del TreeView
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            f"Dim_{table_name}.Treeview",
            background="#2a2d2e",
            foreground="white",
            fieldbackground="#2a2d2e",
            rowheight=30,
            font=('Segoe UI', 11)
        )
        style.configure(
            f"Dim_{table_name}.Treeview.Heading",
            background="#1f6aa5",
            foreground="white",
            font=('Segoe UI', 11, 'bold')
        )
        style.map(
            f"Dim_{table_name}.Treeview",
            background=[('selected', '#1f6aa5')]
        )

        # Crear TreeView
        columns = ("id", "codigo", "descripcion", "activo")
        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=5,
            style=f"Dim_{table_name}.Treeview"
        )

        # Configurar columnas
        tree.heading("id", text="ID")
        tree.heading("codigo", text="Código")
        tree.heading("descripcion", text="Descripción")
        tree.heading("activo", text="Activo")

        tree.column("id", width=50, anchor="center")
        tree.column("codigo", width=100, anchor="w")
        tree.column("descripcion", width=300, anchor="w")
        tree.column("activo", width=70, anchor="center")

        tree.grid(row=0, column=0, sticky="ew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        tree.configure(yscrollcommand=scrollbar.set)

        # Guardar referencia al tree
        self.dim_sections[table_name]['tree'] = tree

        # Frame para añadir nuevo registro
        add_frame = customtkinter.CTkFrame(parent, fg_color=("#e0e0e0", "#333333"))
        add_frame.grid(row=1, column=0, sticky="ew", pady=5)
        add_frame.grid_columnconfigure(2, weight=1)

        # Label
        customtkinter.CTkLabel(
            add_frame,
            text="Añadir nuevo:",
            font=customtkinter.CTkFont(size=12, weight="bold")
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Entry Código
        customtkinter.CTkLabel(add_frame, text="Código:").grid(row=0, column=1, padx=(10, 5), pady=10)
        codigo_entry = customtkinter.CTkEntry(
            add_frame,
            width=100,
            fg_color="#171717",
            text_color="#FFFFFF",
            placeholder_text="Ej: AB"
        )
        codigo_entry.grid(row=0, column=2, padx=5, pady=10, sticky="w")

        # Entry Descripción
        customtkinter.CTkLabel(add_frame, text="Descripción:").grid(row=0, column=3, padx=(20, 5), pady=10)
        desc_entry = customtkinter.CTkEntry(
            add_frame,
            width=250,
            fg_color="#171717",
            text_color="#FFFFFF",
            placeholder_text="Ej: Abastecimiento"
        )
        desc_entry.grid(row=0, column=4, padx=5, pady=10, sticky="ew")

        # Botón Añadir
        add_btn = customtkinter.CTkButton(
            add_frame,
            text="➕ Añadir",
            width=100,
            fg_color="green",
            hover_color="#006400",
            command=lambda: self._add_dimension_record(table_name, codigo_entry, desc_entry)
        )
        add_btn.grid(row=0, column=5, padx=10, pady=10)

        # Guardar referencias
        self.dim_sections[table_name]['codigo_entry'] = codigo_entry
        self.dim_sections[table_name]['desc_entry'] = desc_entry

        # Frame de acciones
        actions_frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        actions_frame.grid(row=2, column=0, sticky="ew")

        # Botón Editar
        edit_btn = customtkinter.CTkButton(
            actions_frame,
            text="✏️ Editar",
            width=100,
            fg_color="#1f6aa5",
            hover_color="#144870",
            command=lambda: self._edit_dimension_record(table_name)
        )
        edit_btn.grid(row=0, column=0, padx=(0, 10), pady=5)

        # Botón Eliminar
        delete_btn = customtkinter.CTkButton(
            actions_frame,
            text="🗑️ Eliminar",
            width=100,
            fg_color="#8B0000",
            hover_color="#5C0000",
            command=lambda: self._delete_dimension_record(table_name)
        )
        delete_btn.grid(row=0, column=1, padx=10, pady=5)

        # Botón Activar/Desactivar
        toggle_btn = customtkinter.CTkButton(
            actions_frame,
            text="🔄 Activar/Desactivar",
            width=140,
            fg_color="#8B4513",
            hover_color="#5D2E0C",
            command=lambda: self._toggle_dimension_record(table_name)
        )
        toggle_btn.grid(row=0, column=2, padx=10, pady=5)

        # Botón Actualizar
        refresh_btn = customtkinter.CTkButton(
            actions_frame,
            text="🔄 Actualizar",
            width=100,
            fg_color="transparent",
            hover_color=("gray70", "gray30"),
            command=lambda: self._load_dimension_data(table_name)
        )
        refresh_btn.grid(row=0, column=3, padx=10, pady=5)

        # Cargar datos iniciales
        self._load_dimension_data(table_name)

    def _load_dimension_data(self, table_name: str):
        """Carga los datos de una tabla de dimensiones."""
        from script.db_config_admin import get_dimension_records

        tree = self.dim_sections[table_name]['tree']

        # Limpiar datos existentes
        for item in tree.get_children():
            tree.delete(item)

        # Obtener datos
        records = get_dimension_records(self.user, self.password, self.schema, table_name)

        # Insertar en el TreeView
        for record in records:
            activo_text = "✓" if record[3] == 1 else "✗"
            tree.insert("", "end", values=(record[0], record[1], record[2], activo_text))

    def _add_dimension_record(self, table_name: str, codigo_entry, desc_entry):
        """Añade un nuevo registro a una tabla de dimensiones."""
        from script.db_config_admin import add_dimension_record, validar_codigo_dimension, validar_descripcion

        codigo = codigo_entry.get().strip()
        descripcion = desc_entry.get().strip()

        # Validaciones
        if not codigo:
            CTkMessagebox(title="Error", message="El código es obligatorio", icon="cancel")
            return

        if not descripcion:
            CTkMessagebox(title="Error", message="La descripción es obligatoria", icon="cancel")
            return

        # Formatear valores
        codigo = validar_codigo_dimension(codigo, table_name)
        descripcion = validar_descripcion(descripcion)

        # Añadir registro
        result = add_dimension_record(self.user, self.password, self.schema, table_name, codigo, descripcion)

        if result['success']:
            CTkMessagebox(title="Éxito", message=result['message'], icon="check")
            codigo_entry.delete(0, 'end')
            desc_entry.delete(0, 'end')
            self._load_dimension_data(table_name)
        else:
            CTkMessagebox(title="Error", message=result['message'], icon="cancel")

    def _edit_dimension_record(self, table_name: str):
        """Edita un registro seleccionado."""
        tree = self.dim_sections[table_name]['tree']
        selected = tree.selection()

        if not selected:
            CTkMessagebox(title="Aviso", message="Seleccione un registro para editar", icon="warning")
            return

        # Obtener datos del registro seleccionado
        item = tree.item(selected[0])
        values = item['values']
        record_id = values[0]
        current_codigo = values[1]
        current_desc = values[2]

        # Crear ventana de edición
        self._show_edit_dialog(table_name, record_id, current_codigo, current_desc)

    def _show_edit_dialog(self, table_name: str, record_id: int, current_codigo: str, current_desc: str):
        """Muestra el diálogo de edición."""
        dialog = customtkinter.CTkToplevel(self)
        dialog.title("Editar Registro")
        dialog.geometry("400x200")
        dialog.transient(self)
        dialog.grab_set()

        dialog.grid_columnconfigure(1, weight=1)

        # Código
        customtkinter.CTkLabel(dialog, text="Código:", font=("", 12, "bold")).grid(
            row=0, column=0, padx=20, pady=(20, 10), sticky="e")
        codigo_entry = customtkinter.CTkEntry(dialog, fg_color="#171717", text_color="#FFFFFF")
        codigo_entry.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="ew")
        codigo_entry.insert(0, current_codigo)

        # Descripción
        customtkinter.CTkLabel(dialog, text="Descripción:", font=("", 12, "bold")).grid(
            row=1, column=0, padx=20, pady=10, sticky="e")
        desc_entry = customtkinter.CTkEntry(dialog, fg_color="#171717", text_color="#FFFFFF")
        desc_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        desc_entry.insert(0, current_desc)

        # Botones
        btn_frame = customtkinter.CTkFrame(dialog, fg_color="transparent")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)

        def save_changes():
            from script.db_config_admin import update_dimension_record, validar_codigo_dimension, validar_descripcion

            codigo = validar_codigo_dimension(codigo_entry.get(), table_name)
            descripcion = validar_descripcion(desc_entry.get())

            if not codigo or not descripcion:
                CTkMessagebox(title="Error", message="Código y descripción son obligatorios", icon="cancel")
                return

            result = update_dimension_record(
                self.user, self.password, self.schema, table_name,
                record_id, codigo, descripcion, 1
            )

            if result['success']:
                CTkMessagebox(title="Éxito", message=result['message'], icon="check")
                dialog.destroy()
                self._load_dimension_data(table_name)
            else:
                CTkMessagebox(title="Error", message=result['message'], icon="cancel")

        customtkinter.CTkButton(
            btn_frame, text="Guardar", fg_color="green", hover_color="#006400",
            command=save_changes
        ).grid(row=0, column=0, padx=10)

        customtkinter.CTkButton(
            btn_frame, text="Cancelar", fg_color="red", hover_color="#8B0000",
            command=dialog.destroy
        ).grid(row=0, column=1, padx=10)

    def _delete_dimension_record(self, table_name: str):
        """Elimina un registro seleccionado."""
        from script.db_config_admin import delete_dimension_record

        tree = self.dim_sections[table_name]['tree']
        selected = tree.selection()

        if not selected:
            CTkMessagebox(title="Aviso", message="Seleccione un registro para eliminar", icon="warning")
            return

        item = tree.item(selected[0])
        record_id = item['values'][0]
        descripcion = item['values'][2]

        # Confirmar eliminación
        msg = CTkMessagebox(
            title="Confirmar eliminación",
            message=f"¿Está seguro de eliminar '{descripcion}'?\n\nEsta acción no se puede deshacer.",
            icon="warning",
            option_1="Cancelar",
            option_2="Eliminar"
        )

        if msg.get() == "Eliminar":
            result = delete_dimension_record(self.user, self.password, self.schema, table_name, record_id)

            if result['success']:
                CTkMessagebox(title="Éxito", message=result['message'], icon="check")
                self._load_dimension_data(table_name)
            else:
                CTkMessagebox(title="Error", message=result['message'], icon="cancel")

    def _toggle_dimension_record(self, table_name: str):
        """Activa/desactiva un registro seleccionado."""
        from script.db_config_admin import toggle_dimension_active

        tree = self.dim_sections[table_name]['tree']
        selected = tree.selection()

        if not selected:
            CTkMessagebox(title="Aviso", message="Seleccione un registro", icon="warning")
            return

        item = tree.item(selected[0])
        record_id = item['values'][0]

        result = toggle_dimension_active(self.user, self.password, self.schema, table_name, record_id)

        if result['success']:
            CTkMessagebox(title="Éxito", message=result['message'], icon="check")
            self._load_dimension_data(table_name)
        else:
            CTkMessagebox(title="Error", message=result['message'], icon="cancel")

    # =========================================================================
    # PESTAÑA: CATÁLOGO DE PARTIDAS
    # =========================================================================

    def _setup_catalogo_tab(self):
        """Configura la pestaña del catálogo de partidas."""
        tab = self.tabview.tab("📦 Catálogo de Partidas")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        # Frame de filtros
        filter_frame = customtkinter.CTkFrame(tab, fg_color="transparent")
        filter_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        filter_frame.grid_columnconfigure(2, weight=1)

        # Filtro por familia
        customtkinter.CTkLabel(filter_frame, text="Familia:", font=("", 12, "bold")).grid(
            row=0, column=0, padx=(0, 10), pady=5, sticky="e")

        self.familia_var = customtkinter.StringVar(value="Todas")
        self.familia_menu = customtkinter.CTkOptionMenu(
            filter_frame,
            variable=self.familia_var,
            values=["Todas"],
            width=200,
            command=self._on_familia_change
        )
        self.familia_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Búsqueda
        customtkinter.CTkLabel(filter_frame, text="Buscar:", font=("", 12, "bold")).grid(
            row=0, column=2, padx=(20, 10), pady=5, sticky="e")

        self.search_entry = customtkinter.CTkEntry(
            filter_frame,
            width=250,
            fg_color="#171717",
            text_color="#FFFFFF",
            placeholder_text="Código o descripción..."
        )
        self.search_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.search_entry.bind('<KeyRelease>', self._on_search_change)

        # Botón buscar
        customtkinter.CTkButton(
            filter_frame,
            text="🔍",
            width=40,
            fg_color="#1f6aa5",
            hover_color="#144870",
            command=self._load_catalogo_data
        ).grid(row=0, column=4, padx=5, pady=5)

        # Frame del TreeView
        tree_frame = customtkinter.CTkFrame(tab, fg_color="transparent")
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        # Configurar estilo
        style = ttk.Style()
        style.configure(
            "Catalogo.Treeview",
            background="#2a2d2e",
            foreground="white",
            fieldbackground="#2a2d2e",
            rowheight=30,
            font=('Segoe UI', 11)
        )
        style.configure(
            "Catalogo.Treeview.Heading",
            background="#1f6aa5",
            foreground="white",
            font=('Segoe UI', 11, 'bold')
        )
        style.map("Catalogo.Treeview", background=[('selected', '#1f6aa5')])

        # Crear TreeView
        columns = ("id", "codigo", "descripcion", "precio", "familia", "activo")
        self.catalogo_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            style="Catalogo.Treeview"
        )

        # Configurar columnas
        self.catalogo_tree.heading("id", text="ID")
        self.catalogo_tree.heading("codigo", text="Código")
        self.catalogo_tree.heading("descripcion", text="Descripción")
        self.catalogo_tree.heading("precio", text="Precio")
        self.catalogo_tree.heading("familia", text="Familia")
        self.catalogo_tree.heading("activo", text="Activo")

        self.catalogo_tree.column("id", width=50, anchor="center")
        self.catalogo_tree.column("codigo", width=100, anchor="w")
        self.catalogo_tree.column("descripcion", width=350, anchor="w")
        self.catalogo_tree.column("precio", width=80, anchor="e")
        self.catalogo_tree.column("familia", width=150, anchor="w")
        self.catalogo_tree.column("activo", width=60, anchor="center")

        self.catalogo_tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.catalogo_tree.yview)
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.catalogo_tree.configure(yscrollcommand=scrollbar_y.set)

        # Frame para añadir partida
        add_frame = customtkinter.CTkFrame(tab, fg_color=("#e0e0e0", "#333333"))
        add_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        add_frame.grid_columnconfigure(4, weight=1)

        customtkinter.CTkLabel(add_frame, text="Nueva partida:", font=("", 12, "bold")).grid(
            row=0, column=0, padx=10, pady=10, sticky="w")

        # Código
        customtkinter.CTkLabel(add_frame, text="Código:").grid(row=0, column=1, padx=5, pady=10)
        self.partida_codigo_entry = customtkinter.CTkEntry(
            add_frame, width=100, fg_color="#171717", text_color="#FFFFFF"
        )
        self.partida_codigo_entry.grid(row=0, column=2, padx=5, pady=10)

        # Descripción
        customtkinter.CTkLabel(add_frame, text="Descripción:").grid(row=0, column=3, padx=5, pady=10)
        self.partida_desc_entry = customtkinter.CTkEntry(
            add_frame, width=300, fg_color="#171717", text_color="#FFFFFF"
        )
        self.partida_desc_entry.grid(row=0, column=4, padx=5, pady=10, sticky="ew")

        # Precio
        customtkinter.CTkLabel(add_frame, text="Precio:").grid(row=0, column=5, padx=5, pady=10)
        self.partida_precio_entry = customtkinter.CTkEntry(
            add_frame, width=80, fg_color="#171717", text_color="#FFFFFF", placeholder_text="0.00"
        )
        self.partida_precio_entry.grid(row=0, column=6, padx=5, pady=10)

        # Botón Añadir
        customtkinter.CTkButton(
            add_frame,
            text="➕ Añadir",
            width=100,
            fg_color="green",
            hover_color="#006400",
            command=self._add_catalogo_partida
        ).grid(row=0, column=7, padx=10, pady=10)

        # Frame de acciones
        actions_frame = customtkinter.CTkFrame(tab, fg_color="transparent")
        actions_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))

        customtkinter.CTkButton(
            actions_frame, text="✏️ Editar", width=100,
            fg_color="#1f6aa5", hover_color="#144870",
            command=self._edit_catalogo_partida
        ).grid(row=0, column=0, padx=(0, 10), pady=5)

        customtkinter.CTkButton(
            actions_frame, text="🗑️ Eliminar", width=100,
            fg_color="#8B0000", hover_color="#5C0000",
            command=self._delete_catalogo_partida
        ).grid(row=0, column=1, padx=10, pady=5)

        customtkinter.CTkButton(
            actions_frame, text="📋 Duplicar", width=100,
            fg_color="#8B4513", hover_color="#5D2E0C",
            command=self._duplicate_catalogo_partida
        ).grid(row=0, column=2, padx=10, pady=5)

        customtkinter.CTkButton(
            actions_frame, text="🔄 Actualizar", width=100,
            fg_color="transparent", hover_color=("gray70", "gray30"),
            command=self._load_catalogo_data
        ).grid(row=0, column=3, padx=10, pady=5)

        # Cargar familias y datos
        self._load_catalogo_familias()
        self._load_catalogo_data()

    def _load_catalogo_familias(self):
        """Carga las familias disponibles."""
        from script.db_config_admin import get_catalogo_familias

        familias = get_catalogo_familias(self.user, self.password, self.schema)
        valores = ["Todas"] + [f"{f[0]} - {f[1]}" for f in familias]
        self.familia_menu.configure(values=valores)

    def _on_familia_change(self, value):
        """Callback cuando cambia la familia seleccionada."""
        self._load_catalogo_data()

    def _on_search_change(self, event):
        """Callback cuando cambia el texto de búsqueda."""
        # Debounce: solo buscar si han pasado 300ms sin teclear
        if hasattr(self, '_search_after_id'):
            self.after_cancel(self._search_after_id)
        self._search_after_id = self.after(300, self._load_catalogo_data)

    def _load_catalogo_data(self):
        """Carga los datos del catálogo."""
        from script.db_config_admin import get_catalogo_partidas

        # Limpiar TreeView
        for item in self.catalogo_tree.get_children():
            self.catalogo_tree.delete(item)

        # Obtener filtros
        familia_value = self.familia_var.get()
        familia_id = None
        if familia_value != "Todas" and " - " in familia_value:
            try:
                familia_id = int(familia_value.split(" - ")[0])
            except ValueError:
                pass

        search_text = self.search_entry.get().strip() or None

        # Obtener datos
        partidas = get_catalogo_partidas(
            self.user, self.password, self.schema,
            familia_id=familia_id,
            search_text=search_text
        )

        # Insertar en TreeView
        for partida in partidas:
            activo_text = "✓" if partida[5] == 1 else "✗"
            precio_text = f"{partida[3]:.2f}" if partida[3] else "0.00"
            self.catalogo_tree.insert("", "end", values=(
                partida[0], partida[1], partida[2], precio_text, partida[4] or "", activo_text
            ))

    def _add_catalogo_partida(self):
        """Añade una nueva partida al catálogo."""
        from script.db_config_admin import add_catalogo_partida, validar_precio

        codigo = self.partida_codigo_entry.get().strip().upper()
        descripcion = self.partida_desc_entry.get().strip()
        precio_str = self.partida_precio_entry.get().strip() or "0"

        if not codigo:
            CTkMessagebox(title="Error", message="El código es obligatorio", icon="cancel")
            return

        if not descripcion:
            CTkMessagebox(title="Error", message="La descripción es obligatoria", icon="cancel")
            return

        # Validar precio
        success, precio, error_msg = validar_precio(precio_str)
        if not success:
            CTkMessagebox(title="Error", message=error_msg, icon="cancel")
            return

        # Capitalizar descripción
        if descripcion:
            descripcion = descripcion[0].upper() + descripcion[1:] if len(descripcion) > 1 else descripcion.upper()

        result = add_catalogo_partida(self.user, self.password, self.schema, codigo, descripcion, precio)

        if result['success']:
            CTkMessagebox(title="Éxito", message=result['message'], icon="check")
            self.partida_codigo_entry.delete(0, 'end')
            self.partida_desc_entry.delete(0, 'end')
            self.partida_precio_entry.delete(0, 'end')
            self._load_catalogo_data()
        else:
            CTkMessagebox(title="Error", message=result['message'], icon="cancel")

    def _edit_catalogo_partida(self):
        """Edita una partida seleccionada."""
        selected = self.catalogo_tree.selection()
        if not selected:
            CTkMessagebox(title="Aviso", message="Seleccione una partida para editar", icon="warning")
            return

        item = self.catalogo_tree.item(selected[0])
        values = item['values']
        record_id = values[0]
        current_codigo = values[1]
        current_desc = values[2]
        current_precio = values[3]

        # Crear diálogo de edición
        dialog = customtkinter.CTkToplevel(self)
        dialog.title("Editar Partida")
        dialog.geometry("450x250")
        dialog.transient(self)
        dialog.grab_set()

        dialog.grid_columnconfigure(1, weight=1)

        # Código
        customtkinter.CTkLabel(dialog, text="Código:", font=("", 12, "bold")).grid(
            row=0, column=0, padx=20, pady=(20, 10), sticky="e")
        codigo_entry = customtkinter.CTkEntry(dialog, fg_color="#171717", text_color="#FFFFFF")
        codigo_entry.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="ew")
        codigo_entry.insert(0, current_codigo)

        # Descripción
        customtkinter.CTkLabel(dialog, text="Descripción:", font=("", 12, "bold")).grid(
            row=1, column=0, padx=20, pady=10, sticky="e")
        desc_entry = customtkinter.CTkEntry(dialog, fg_color="#171717", text_color="#FFFFFF")
        desc_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        desc_entry.insert(0, current_desc)

        # Precio
        customtkinter.CTkLabel(dialog, text="Precio:", font=("", 12, "bold")).grid(
            row=2, column=0, padx=20, pady=10, sticky="e")
        precio_entry = customtkinter.CTkEntry(dialog, fg_color="#171717", text_color="#FFFFFF")
        precio_entry.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        precio_entry.insert(0, current_precio)

        # Botones
        btn_frame = customtkinter.CTkFrame(dialog, fg_color="transparent")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

        def save_changes():
            from script.db_config_admin import update_catalogo_partida, validar_precio

            codigo = codigo_entry.get().strip().upper()
            descripcion = desc_entry.get().strip()

            if descripcion:
                descripcion = descripcion[0].upper() + descripcion[1:] if len(descripcion) > 1 else descripcion.upper()

            success, precio, error_msg = validar_precio(precio_entry.get())
            if not success:
                CTkMessagebox(title="Error", message=error_msg, icon="cancel")
                return

            result = update_catalogo_partida(
                self.user, self.password, self.schema, record_id, codigo, descripcion, precio
            )

            if result['success']:
                CTkMessagebox(title="Éxito", message=result['message'], icon="check")
                dialog.destroy()
                self._load_catalogo_data()
            else:
                CTkMessagebox(title="Error", message=result['message'], icon="cancel")

        customtkinter.CTkButton(
            btn_frame, text="Guardar", fg_color="green", hover_color="#006400",
            command=save_changes
        ).grid(row=0, column=0, padx=10)

        customtkinter.CTkButton(
            btn_frame, text="Cancelar", fg_color="red", hover_color="#8B0000",
            command=dialog.destroy
        ).grid(row=0, column=1, padx=10)

    def _delete_catalogo_partida(self):
        """Elimina una partida seleccionada."""
        from script.db_config_admin import delete_catalogo_partida

        selected = self.catalogo_tree.selection()
        if not selected:
            CTkMessagebox(title="Aviso", message="Seleccione una partida para eliminar", icon="warning")
            return

        item = self.catalogo_tree.item(selected[0])
        record_id = item['values'][0]
        descripcion = item['values'][2]

        msg = CTkMessagebox(
            title="Confirmar eliminación",
            message=f"¿Está seguro de eliminar '{descripcion}'?\n\nEsta acción no se puede deshacer.",
            icon="warning",
            option_1="Cancelar",
            option_2="Eliminar"
        )

        if msg.get() == "Eliminar":
            result = delete_catalogo_partida(self.user, self.password, self.schema, record_id)

            if result['success']:
                CTkMessagebox(title="Éxito", message=result['message'], icon="check")
                self._load_catalogo_data()
            else:
                CTkMessagebox(title="Error", message=result['message'], icon="cancel")

    def _duplicate_catalogo_partida(self):
        """Duplica una partida seleccionada."""
        selected = self.catalogo_tree.selection()
        if not selected:
            CTkMessagebox(title="Aviso", message="Seleccione una partida para duplicar", icon="warning")
            return

        item = self.catalogo_tree.item(selected[0])
        values = item['values']

        # Rellenar los campos de nueva partida con los valores duplicados
        self.partida_codigo_entry.delete(0, 'end')
        self.partida_codigo_entry.insert(0, f"{values[1]}_COPIA")

        self.partida_desc_entry.delete(0, 'end')
        self.partida_desc_entry.insert(0, values[2])

        self.partida_precio_entry.delete(0, 'end')
        self.partida_precio_entry.insert(0, values[3])

        CTkMessagebox(
            title="Duplicar",
            message="Los datos se han copiado al formulario.\nModifique el código y pulse 'Añadir'.",
            icon="info"
        )
