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
        self.geometry("1100x750")
        self.minsize(1000, 650)

        # Hacer modal
        self.transient(parent)
        self.grab_set()

        # Configurar grid principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Diccionario para guardar referencias
        self.dim_sections = {}

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
        """Configura la pestaña de gestión de variables con sub-pestañas."""
        tab = self.tabview.tab("📊 Gestión de Variables")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        # Sub-pestañas para cada tabla de dimensiones
        self.var_subtabs = customtkinter.CTkTabview(tab, corner_radius=5)
        self.var_subtabs.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Crear sub-pestañas
        self.var_subtabs.add("🌐 Redes")
        self.var_subtabs.add("🔧 Tipos Reparación")
        self.var_subtabs.add("📝 Códigos Trabajo")

        # Configurar cada sub-pestaña
        self._setup_dimension_subtab(
            self.var_subtabs.tab("🌐 Redes"),
            "dim_red",
            "Gestiona los tipos de red (Abastecimiento, Saneamiento, etc.)"
        )
        self._setup_dimension_subtab(
            self.var_subtabs.tab("🔧 Tipos Reparación"),
            "dim_tipos_rep",
            "Gestiona los tipos de reparación (Fuga, Atasco, etc.)"
        )
        self._setup_dimension_subtab(
            self.var_subtabs.tab("📝 Códigos Trabajo"),
            "dim_codigo_trabajo",
            "Gestiona los códigos de trabajo programado"
        )

    def _setup_dimension_subtab(self, tab, table_name: str, description: str):
        """Configura una sub-pestaña para una tabla de dimensiones."""
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        # Descripción
        desc_label = customtkinter.CTkLabel(
            tab,
            text=description,
            font=customtkinter.CTkFont(size=12),
            text_color="gray"
        )
        desc_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        # Frame para el TreeView
        tree_frame = customtkinter.CTkFrame(tab, fg_color="transparent")
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        # Configurar estilo del TreeView
        style = ttk.Style()
        style.theme_use('clam')
        style_name = f"Dim_{table_name}.Treeview"
        style.configure(
            style_name,
            background="#2a2d2e",
            foreground="white",
            fieldbackground="#2a2d2e",
            rowheight=28,
            font=('Segoe UI', 11)
        )
        style.configure(
            f"{style_name}.Heading",
            background="#1f6aa5",
            foreground="white",
            font=('Segoe UI', 11, 'bold')
        )
        style.map(style_name, background=[('selected', '#1f6aa5')])

        # Crear TreeView
        columns = ("id", "codigo", "descripcion", "activo")
        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=10,
            style=style_name
        )

        # Configurar columnas
        tree.heading("id", text="ID")
        tree.heading("codigo", text="Código")
        tree.heading("descripcion", text="Descripción")
        tree.heading("activo", text="Activo")

        tree.column("id", width=60, anchor="center")
        tree.column("codigo", width=120, anchor="w")
        tree.column("descripcion", width=400, anchor="w")
        tree.column("activo", width=80, anchor="center")

        tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        tree.configure(yscrollcommand=scrollbar.set)

        # Guardar referencia al tree
        self.dim_sections[table_name] = {'tree': tree}

        # Frame para añadir nuevo registro
        add_frame = customtkinter.CTkFrame(tab, fg_color=("#e0e0e0", "#333333"), corner_radius=10)
        add_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        add_frame.grid_columnconfigure(3, weight=1)

        # Label
        customtkinter.CTkLabel(
            add_frame,
            text="Añadir nuevo:",
            font=customtkinter.CTkFont(size=12, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=12, sticky="w")

        # Entry Código
        customtkinter.CTkLabel(add_frame, text="Código:").grid(row=0, column=1, padx=(10, 5), pady=12)
        codigo_entry = customtkinter.CTkEntry(
            add_frame,
            width=120,
            fg_color="#171717",
            text_color="#FFFFFF",
            placeholder_text="Ej: AB"
        )
        codigo_entry.grid(row=0, column=2, padx=5, pady=12)

        # Entry Descripción
        customtkinter.CTkLabel(add_frame, text="Descripción:").grid(row=0, column=3, padx=(20, 5), pady=12, sticky="e")
        desc_entry = customtkinter.CTkEntry(
            add_frame,
            width=300,
            fg_color="#171717",
            text_color="#FFFFFF",
            placeholder_text="Ej: Abastecimiento"
        )
        desc_entry.grid(row=0, column=4, padx=5, pady=12, sticky="ew")

        # Botón Añadir
        add_btn = customtkinter.CTkButton(
            add_frame,
            text="➕ Añadir",
            width=100,
            fg_color="green",
            hover_color="#006400",
            command=lambda: self._add_dimension_record(table_name, codigo_entry, desc_entry)
        )
        add_btn.grid(row=0, column=5, padx=15, pady=12)

        # Guardar referencias a los entries
        self.dim_sections[table_name]['codigo_entry'] = codigo_entry
        self.dim_sections[table_name]['desc_entry'] = desc_entry

        # Frame de acciones
        actions_frame = customtkinter.CTkFrame(tab, fg_color="transparent")
        actions_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Botón Editar
        customtkinter.CTkButton(
            actions_frame,
            text="✏️ Editar",
            width=110,
            fg_color="#1f6aa5",
            hover_color="#144870",
            command=lambda: self._edit_dimension_record(table_name)
        ).grid(row=0, column=0, padx=(0, 10), pady=5)

        # Botón Eliminar
        customtkinter.CTkButton(
            actions_frame,
            text="🗑️ Eliminar",
            width=110,
            fg_color="#8B0000",
            hover_color="#5C0000",
            command=lambda: self._delete_dimension_record(table_name)
        ).grid(row=0, column=1, padx=10, pady=5)

        # Botón Activar/Desactivar
        customtkinter.CTkButton(
            actions_frame,
            text="🔄 Activar/Desact.",
            width=130,
            fg_color="#8B4513",
            hover_color="#5D2E0C",
            command=lambda: self._toggle_dimension_record(table_name)
        ).grid(row=0, column=2, padx=10, pady=5)

        # Botón Actualizar
        customtkinter.CTkButton(
            actions_frame,
            text="🔄 Actualizar",
            width=110,
            fg_color="transparent",
            hover_color=("gray70", "gray30"),
            border_width=1,
            command=lambda: self._load_dimension_data(table_name)
        ).grid(row=0, column=3, padx=10, pady=5)

        # Cargar datos iniciales
        self.after(100, lambda: self._load_dimension_data(table_name))

    def _load_dimension_data(self, table_name: str):
        """Carga los datos de una tabla de dimensiones."""
        from script.db_config_admin import get_dimension_records

        if table_name not in self.dim_sections:
            print(f"Error: {table_name} no encontrado en dim_sections")
            return

        tree = self.dim_sections[table_name]['tree']

        # Limpiar datos existentes
        for item in tree.get_children():
            tree.delete(item)

        try:
            # Obtener datos
            records = get_dimension_records(self.user, self.password, self.schema, table_name)

            # Insertar en el TreeView
            for record in records:
                activo_text = "✓ Sí" if record[3] == 1 else "✗ No"
                tree.insert("", "end", values=(record[0], record[1], record[2], activo_text))

            if not records:
                print(f"No se encontraron registros en {table_name}")

        except Exception as e:
            print(f"Error al cargar datos de {table_name}: {e}")
            CTkMessagebox(title="Error", message=f"Error al cargar {table_name}:\n{e}", icon="cancel")

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
        dialog.geometry("450x220")
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)

        dialog.grid_columnconfigure(1, weight=1)

        # Título
        customtkinter.CTkLabel(
            dialog,
            text="Editar Registro",
            font=customtkinter.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, padx=20, pady=(15, 10))

        # Código
        customtkinter.CTkLabel(dialog, text="Código:", font=("", 12, "bold")).grid(
            row=1, column=0, padx=20, pady=10, sticky="e")
        codigo_entry = customtkinter.CTkEntry(dialog, fg_color="#171717", text_color="#FFFFFF", width=250)
        codigo_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        codigo_entry.insert(0, current_codigo)

        # Descripción
        customtkinter.CTkLabel(dialog, text="Descripción:", font=("", 12, "bold")).grid(
            row=2, column=0, padx=20, pady=10, sticky="e")
        desc_entry = customtkinter.CTkEntry(dialog, fg_color="#171717", text_color="#FFFFFF", width=250)
        desc_entry.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        desc_entry.insert(0, current_desc)

        # Botones
        btn_frame = customtkinter.CTkFrame(dialog, fg_color="transparent")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

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
            btn_frame, text="💾 Guardar", fg_color="green", hover_color="#006400",
            width=100, command=save_changes
        ).grid(row=0, column=0, padx=10)

        customtkinter.CTkButton(
            btn_frame, text="❌ Cancelar", fg_color="red", hover_color="#8B0000",
            width=100, command=dialog.destroy
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
        filter_frame.grid_columnconfigure(3, weight=1)

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
            rowheight=28,
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
        self.catalogo_tree.column("activo", width=70, anchor="center")

        self.catalogo_tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.catalogo_tree.yview)
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.catalogo_tree.configure(yscrollcommand=scrollbar_y.set)

        # Frame para añadir partida
        add_frame = customtkinter.CTkFrame(tab, fg_color=("#e0e0e0", "#333333"), corner_radius=10)
        add_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        add_frame.grid_columnconfigure(4, weight=1)

        customtkinter.CTkLabel(add_frame, text="Nueva partida:", font=("", 12, "bold")).grid(
            row=0, column=0, padx=15, pady=12, sticky="w")

        # Código
        customtkinter.CTkLabel(add_frame, text="Código:").grid(row=0, column=1, padx=5, pady=12)
        self.partida_codigo_entry = customtkinter.CTkEntry(
            add_frame, width=100, fg_color="#171717", text_color="#FFFFFF"
        )
        self.partida_codigo_entry.grid(row=0, column=2, padx=5, pady=12)

        # Descripción
        customtkinter.CTkLabel(add_frame, text="Descripción:").grid(row=0, column=3, padx=5, pady=12)
        self.partida_desc_entry = customtkinter.CTkEntry(
            add_frame, width=300, fg_color="#171717", text_color="#FFFFFF"
        )
        self.partida_desc_entry.grid(row=0, column=4, padx=5, pady=12, sticky="ew")

        # Precio
        customtkinter.CTkLabel(add_frame, text="Precio:").grid(row=0, column=5, padx=5, pady=12)
        self.partida_precio_entry = customtkinter.CTkEntry(
            add_frame, width=80, fg_color="#171717", text_color="#FFFFFF", placeholder_text="0.00"
        )
        self.partida_precio_entry.grid(row=0, column=6, padx=5, pady=12)

        # Botón Añadir
        customtkinter.CTkButton(
            add_frame,
            text="➕ Añadir",
            width=100,
            fg_color="green",
            hover_color="#006400",
            command=self._add_catalogo_partida
        ).grid(row=0, column=7, padx=15, pady=12)

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
            border_width=1,
            command=self._load_catalogo_data
        ).grid(row=0, column=3, padx=10, pady=5)

        # Cargar familias y datos después de que la ventana esté lista
        self.after(100, self._load_catalogo_familias)
        self.after(200, self._load_catalogo_data)

    def _load_catalogo_familias(self):
        """Carga las familias disponibles."""
        from script.db_config_admin import get_catalogo_familias

        try:
            familias = get_catalogo_familias(self.user, self.password, self.schema)
            valores = ["Todas"] + [f"{f[0]} - {f[1]}" for f in familias]
            self.familia_menu.configure(values=valores)
        except Exception as e:
            print(f"Error al cargar familias: {e}")

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

        try:
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
                activo_text = "✓ Sí" if partida[5] == 1 else "✗ No"
                precio_text = f"{partida[3]:.2f}" if partida[3] else "0.00"
                self.catalogo_tree.insert("", "end", values=(
                    partida[0], partida[1], partida[2], precio_text, partida[4] or "", activo_text
                ))

            if not partidas:
                print("No se encontraron partidas en el catálogo")

        except Exception as e:
            print(f"Error al cargar catálogo: {e}")

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
        dialog.geometry("500x280")
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)

        dialog.grid_columnconfigure(1, weight=1)

        # Título
        customtkinter.CTkLabel(
            dialog,
            text="Editar Partida",
            font=customtkinter.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, padx=20, pady=(15, 10))

        # Código
        customtkinter.CTkLabel(dialog, text="Código:", font=("", 12, "bold")).grid(
            row=1, column=0, padx=20, pady=10, sticky="e")
        codigo_entry = customtkinter.CTkEntry(dialog, fg_color="#171717", text_color="#FFFFFF", width=300)
        codigo_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        codigo_entry.insert(0, current_codigo)

        # Descripción
        customtkinter.CTkLabel(dialog, text="Descripción:", font=("", 12, "bold")).grid(
            row=2, column=0, padx=20, pady=10, sticky="e")
        desc_entry = customtkinter.CTkEntry(dialog, fg_color="#171717", text_color="#FFFFFF", width=300)
        desc_entry.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        desc_entry.insert(0, current_desc)

        # Precio
        customtkinter.CTkLabel(dialog, text="Precio:", font=("", 12, "bold")).grid(
            row=3, column=0, padx=20, pady=10, sticky="e")
        precio_entry = customtkinter.CTkEntry(dialog, fg_color="#171717", text_color="#FFFFFF", width=300)
        precio_entry.grid(row=3, column=1, padx=20, pady=10, sticky="ew")
        precio_entry.insert(0, current_precio)

        # Botones
        btn_frame = customtkinter.CTkFrame(dialog, fg_color="transparent")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

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
            btn_frame, text="💾 Guardar", fg_color="green", hover_color="#006400",
            width=100, command=save_changes
        ).grid(row=0, column=0, padx=10)

        customtkinter.CTkButton(
            btn_frame, text="❌ Cancelar", fg_color="red", hover_color="#8B0000",
            width=100, command=dialog.destroy
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
