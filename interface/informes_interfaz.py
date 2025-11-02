# interface/informes_interfaz.py
"""
Interfaz del Módulo de Informes
Generación de informes personalizados con filtros multicriterio
"""

import customtkinter
from tkinter import ttk, filedialog
from PIL import Image
import os
import sys

# Agregar el directorio padre al path para imports
current_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.dirname(current_path)
sys.path.append(parent_path)

from script.informes_config import (
    CATEGORIAS_INFORMES,
    CAMPOS_PARTES,
    CAMPOS_RECURSOS,
    CAMPOS_PRESUPUESTOS,
    CAMPOS_CERTIFICACIONES,
    CAMPOS_PLANIFICACION,
    OPERADORES,
    TIPOS_CAMPO,
    FORMATOS_SALIDA,
    ORDEN_OPCIONES,
    LOGICA_FILTROS,
    CONFIG_CABECERA_DEFAULT
)


class InformesFrame(customtkinter.CTkFrame):
    """Frame principal del módulo de Informes"""

    def __init__(self, master, user, password, schema, **kwargs):
        super().__init__(master, **kwargs)

        self.user = user
        self.password = password
        self.schema = schema

        # Variables de estado
        self.informe_seleccionado = None
        self.categoria_seleccionada = None
        self.clasificaciones = []
        self.filtros = []
        self.campos_seleccionados = {}

        # Configurar grid
        self.grid_columnconfigure(0, weight=0)  # Panel izquierdo fijo
        self.grid_columnconfigure(1, weight=1)  # Panel derecho expandible
        self.grid_rowconfigure(0, weight=1)

        # Crear componentes
        self._create_header()
        self._create_left_panel()
        self._create_right_panel()
        self._create_action_bar()

    def _create_header(self):
        """Crea el encabezado con título y botón de configuración"""
        header_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=15, pady=(5, 0))
        header_frame.grid_columnconfigure(0, weight=1)

        # Título
        title = customtkinter.CTkLabel(
            header_frame,
            text="GENERACIÓN DE INFORMES",
            font=customtkinter.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w")

        # Botón configuración
        config_button = customtkinter.CTkButton(
            header_frame,
            text="⚙️ Configuración",
            width=140,
            height=32,
            command=self._open_config_dialog
        )
        config_button.grid(row=0, column=1, sticky="e")

    def _create_left_panel(self):
        """Crea el panel izquierdo con el árbol de informes"""
        left_frame = customtkinter.CTkFrame(self, width=300)  # Aumentado de 280 a 300
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(15, 8), pady=5)
        left_frame.grid_propagate(False)
        left_frame.grid_rowconfigure(1, weight=1)

        # Título
        title = customtkinter.CTkLabel(
            left_frame,
            text="TIPO DE INFORME",
            font=customtkinter.CTkFont(size=13, weight="bold")
        )
        title.grid(row=0, column=0, padx=10, pady=(8, 5), sticky="w")

        # Frame para el TreeView
        tree_frame = customtkinter.CTkFrame(left_frame)
        tree_frame.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")

        # TreeView con scroll
        self.tree_scroll = customtkinter.CTkScrollbar(tree_frame)
        self.tree_scroll.pack(side="right", fill="y")

        # Crear TreeView
        self.tree = ttk.Treeview(
            tree_frame,
            yscrollcommand=self.tree_scroll.set,
            show="tree"
        )
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree_scroll.configure(command=self.tree.yview)

        # IMPORTANTE: Configurar el estilo DESPUÉS de crear el widget y empaquetarlo
        # Esto asegura que sobrescribe cualquier configuración global previa
        self._configure_tree_style()

        # Poblar el árbol
        self._populate_tree()

        # Bind para selección
        self.tree.bind('<<TreeviewSelect>>', self._on_tree_select)

    def _configure_tree_style(self):
        """Configura el estilo del TreeView DESPUÉS de crearlo para asegurar que se aplique"""
        import tkinter.font as tkfont

        # Crear estilo único DESPUÉS de que el TreeView existe
        style = ttk.Style()

        # Nombre único para evitar conflictos
        style_name = "InformesCustom.Treeview"

        # Configurar con fuente grande
        style.configure(style_name,
                        background="#2a2d2e",
                        foreground="white",
                        fieldbackground="#2a2d2e",
                        borderwidth=0,
                        rowheight=32,  # Fila más alta
                        font=('Segoe UI', 14, 'bold'))  # Fuente AÚN MÁS GRANDE para que sea VISIBLE

        style.configure(f"{style_name}.Heading",
                        background="#1f538d",
                        foreground="white",
                        font=('Segoe UI', 14, 'bold'))

        style.map(style_name,
                  background=[('selected', '#1f538d')],
                  foreground=[('selected', 'white')])

        # Aplicar el estilo al TreeView
        self.tree.configure(style=style_name)

        # ENFOQUE ALTERNATIVO: Configurar fuente directamente usando tags
        # Esto es más robusto que depender solo de Style
        custom_font = tkfont.Font(family='Segoe UI', size=14, weight='bold')

        # Crear un tag con la fuente personalizada
        self.tree.tag_configure('custom_font', font=custom_font)

    def _populate_tree(self):
        """Puebla el TreeView con categorías e informes"""
        for categoria, informes in CATEGORIAS_INFORMES.items():
            # Insertar categoría con tag personalizado
            cat_id = self.tree.insert("", "end", text=categoria, open=False, tags=('custom_font',))

            # Insertar informes de la categoría con tag personalizado
            for informe in informes:
                self.tree.insert(cat_id, "end", text=f"  {informe}", tags=('custom_font',))

    def _on_tree_select(self, event):
        """Maneja la selección en el TreeView"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            text = self.tree.item(item, "text")

            # Verificar si es categoría o informe
            parent = self.tree.parent(item)

            if parent:  # Es un informe
                # Obtener categoría padre
                parent_text = self.tree.item(parent, "text")
                self.categoria_seleccionada = parent_text
                self.informe_seleccionado = text.strip()

                # Actualizar título del informe
                self.informe_title_label.configure(
                    text=f"Informe seleccionado: {self.informe_seleccionado}"
                )

                # Actualizar campos disponibles según categoría
                self._update_campos_disponibles()

    def _create_right_panel(self):
        """Crea el panel derecho con la configuración del informe"""
        right_frame = customtkinter.CTkScrollableFrame(self)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(8, 15), pady=5)
        right_frame.grid_columnconfigure(0, weight=1)

        # Título del informe seleccionado
        self.informe_title_label = customtkinter.CTkLabel(
            right_frame,
            text="Informe seleccionado: Ninguno",
            font=customtkinter.CTkFont(size=13, weight="bold"),
            text_color="gray"
        )
        self.informe_title_label.grid(row=0, column=0, padx=15, pady=(5, 10), sticky="w")

        # Separador
        separator1 = customtkinter.CTkFrame(right_frame, height=2, fg_color="gray30")
        separator1.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 8))

        # Sección CLASIFICACIÓN
        self._create_clasificacion_section(right_frame, row=2)

        # Separador
        separator2 = customtkinter.CTkFrame(right_frame, height=2, fg_color="gray30")
        separator2.grid(row=3, column=0, sticky="ew", padx=15, pady=10)

        # Sección FILTROS
        self._create_filtros_section(right_frame, row=4)

        # Separador
        separator3 = customtkinter.CTkFrame(right_frame, height=2, fg_color="gray30")
        separator3.grid(row=5, column=0, sticky="ew", padx=15, pady=10)

        # Sección CAMPOS A MOSTRAR
        self._create_campos_section(right_frame, row=6)

        # Separador
        separator4 = customtkinter.CTkFrame(right_frame, height=2, fg_color="gray30")
        separator4.grid(row=7, column=0, sticky="ew", padx=15, pady=10)

        # Sección OPCIONES DE PRESENTACIÓN
        self._create_opciones_section(right_frame, row=8)

    def _create_clasificacion_section(self, parent, row):
        """Crea la sección de clasificación"""
        # Frame contenedor con altura mínima
        clasif_frame = customtkinter.CTkFrame(parent, fg_color="transparent", height=150)
        clasif_frame.grid(row=row, column=0, sticky="ew", padx=15, pady=3)
        clasif_frame.grid_columnconfigure(0, weight=1)

        # Título
        title = customtkinter.CTkLabel(
            clasif_frame,
            text="📋 CLASIFICACIÓN (Agrupar por)",
            font=customtkinter.CTkFont(size=12, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w", pady=(0, 8))

        # Botón añadir
        add_button = customtkinter.CTkButton(
            clasif_frame,
            text="+ Añadir clasificación",
            width=150,
            height=28,
            command=self._add_clasificacion
        )
        add_button.grid(row=1, column=0, sticky="w", pady=(0, 8))

        # Frame para clasificaciones con scroll
        self.clasificaciones_container = customtkinter.CTkScrollableFrame(
            clasif_frame,
            height=100,
            fg_color="transparent"
        )
        self.clasificaciones_container.grid(row=2, column=0, sticky="ew")

        self.clasificaciones_frame = customtkinter.CTkFrame(self.clasificaciones_container, fg_color="transparent")
        self.clasificaciones_frame.pack(fill="both", expand=True)
        self.clasificaciones_frame.grid_columnconfigure(0, weight=1)

    def _create_filtros_section(self, parent, row):
        """Crea la sección de filtros"""
        # Frame contenedor con altura mínima
        filtros_frame = customtkinter.CTkFrame(parent, fg_color="transparent", height=150)
        filtros_frame.grid(row=row, column=0, sticky="ew", padx=15, pady=3)
        filtros_frame.grid_columnconfigure(0, weight=1)

        # Título
        title = customtkinter.CTkLabel(
            filtros_frame,
            text="🔍 FILTROS (Mostrar solo si...)",
            font=customtkinter.CTkFont(size=12, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w", pady=(0, 8))

        # Botón añadir
        add_button = customtkinter.CTkButton(
            filtros_frame,
            text="+ Añadir filtro",
            width=150,
            height=28,
            command=self._add_filtro
        )
        add_button.grid(row=1, column=0, sticky="w", pady=(0, 8))

        # Frame para filtros con scroll
        self.filtros_container = customtkinter.CTkScrollableFrame(
            filtros_frame,
            height=120,
            fg_color="transparent"
        )
        self.filtros_container.grid(row=2, column=0, sticky="ew")

        self.filtros_frame = customtkinter.CTkFrame(self.filtros_container, fg_color="transparent")
        self.filtros_frame.pack(fill="both", expand=True)
        self.filtros_frame.grid_columnconfigure(0, weight=1)

    def _create_campos_section(self, parent, row):
        """Crea la sección de campos a mostrar"""
        # Frame contenedor
        campos_frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        campos_frame.grid(row=row, column=0, sticky="ew", padx=15, pady=3)
        campos_frame.grid_columnconfigure(0, weight=1)

        # Título
        title = customtkinter.CTkLabel(
            campos_frame,
            text="📄 CAMPOS A MOSTRAR",
            font=customtkinter.CTkFont(size=12, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w", pady=(0, 8))

        # Frame scrollable para checkboxes
        self.campos_scrollable = customtkinter.CTkScrollableFrame(campos_frame, height=180)
        self.campos_scrollable.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        self.campos_scrollable.grid_columnconfigure(0, weight=1)
        self.campos_scrollable.grid_columnconfigure(1, weight=1)
        self.campos_scrollable.grid_columnconfigure(2, weight=1)

        # Mensaje inicial
        self.campos_message = customtkinter.CTkLabel(
            self.campos_scrollable,
            text="Seleccione un informe para ver los campos disponibles",
            text_color="gray"
        )
        self.campos_message.grid(row=0, column=0, columnspan=3, pady=20)

        # Botones de selección
        buttons_frame = customtkinter.CTkFrame(campos_frame, fg_color="transparent")
        buttons_frame.grid(row=2, column=0, sticky="w")

        select_all = customtkinter.CTkButton(
            buttons_frame,
            text="☑ Seleccionar todo",
            width=140,
            height=28,
            command=self._select_all_campos
        )
        select_all.grid(row=0, column=0, padx=(0, 10))

        deselect_all = customtkinter.CTkButton(
            buttons_frame,
            text="☐ Deseleccionar todo",
            width=140,
            height=28,
            command=self._deselect_all_campos
        )
        deselect_all.grid(row=0, column=1)

    def _create_opciones_section(self, parent, row):
        """Crea la sección de opciones de presentación"""
        # Frame contenedor
        opciones_frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        opciones_frame.grid(row=row, column=0, sticky="ew", padx=15, pady=3)
        opciones_frame.grid_columnconfigure(0, weight=1)

        # Título
        title = customtkinter.CTkLabel(
            opciones_frame,
            text="🎨 OPCIONES DE PRESENTACIÓN",
            font=customtkinter.CTkFont(size=12, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w", pady=(0, 8))

        # Formato de salida
        formato_label = customtkinter.CTkLabel(
            opciones_frame,
            text="Formato de salida:",
            font=customtkinter.CTkFont(size=12)
        )
        formato_label.grid(row=1, column=0, sticky="w", pady=(5, 5))

        self.formato_var = customtkinter.StringVar(value="Tabla")
        formato_frame = customtkinter.CTkFrame(opciones_frame, fg_color="transparent")
        formato_frame.grid(row=2, column=0, sticky="w", padx=(20, 0))

        for i, formato in enumerate(FORMATOS_SALIDA):
            radio = customtkinter.CTkRadioButton(
                formato_frame,
                text=formato,
                variable=self.formato_var,
                value=formato
            )
            radio.grid(row=0, column=i, padx=(0, 20))

        # Opciones de totales
        totales_label = customtkinter.CTkLabel(
            opciones_frame,
            text="Opciones de totales:",
            font=customtkinter.CTkFont(size=12)
        )
        totales_label.grid(row=3, column=0, sticky="w", pady=(15, 5))

        self.subtotales_var = customtkinter.BooleanVar(value=True)
        self.subtotales_check = customtkinter.CTkCheckBox(
            opciones_frame,
            text="Mostrar subtotales por grupo",
            variable=self.subtotales_var
        )
        self.subtotales_check.grid(row=4, column=0, sticky="w", padx=(20, 0), pady=2)

        self.totales_var = customtkinter.BooleanVar(value=True)
        self.totales_check = customtkinter.CTkCheckBox(
            opciones_frame,
            text="Mostrar totales generales",
            variable=self.totales_var
        )
        self.totales_check.grid(row=5, column=0, sticky="w", padx=(20, 0), pady=2)

        self.graficos_var = customtkinter.BooleanVar(value=False)
        self.graficos_check = customtkinter.CTkCheckBox(
            opciones_frame,
            text="Incluir gráficos resumen",
            variable=self.graficos_var
        )
        self.graficos_check.grid(row=6, column=0, sticky="w", padx=(20, 0), pady=2)

        # Opciones adicionales
        adicionales_label = customtkinter.CTkLabel(
            opciones_frame,
            text="Opciones adicionales:",
            font=customtkinter.CTkFont(size=12)
        )
        adicionales_label.grid(row=7, column=0, sticky="w", pady=(15, 5))

        self.logo_var = customtkinter.BooleanVar(value=True)
        logo_check = customtkinter.CTkCheckBox(
            opciones_frame,
            text="Incluir logo de empresa",
            variable=self.logo_var
        )
        logo_check.grid(row=8, column=0, sticky="w", padx=(20, 0), pady=2)

        self.fecha_var = customtkinter.BooleanVar(value=True)
        fecha_check = customtkinter.CTkCheckBox(
            opciones_frame,
            text="Incluir fecha de generación",
            variable=self.fecha_var
        )
        fecha_check.grid(row=9, column=0, sticky="w", padx=(20, 0), pady=2)

        self.compacto_var = customtkinter.BooleanVar(value=False)
        compacto_check = customtkinter.CTkCheckBox(
            opciones_frame,
            text="Modo compacto (menos espaciado)",
            variable=self.compacto_var
        )
        compacto_check.grid(row=10, column=0, sticky="w", padx=(20, 0), pady=2)

    def _create_action_bar(self):
        """Crea la barra de acciones inferior"""
        action_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=15, pady=(5, 10))
        action_frame.grid_columnconfigure(0, weight=1)

        # Frame para centrar botones
        buttons_frame = customtkinter.CTkFrame(action_frame, fg_color="transparent")
        buttons_frame.grid(row=0, column=0)

        # Botones
        preview_btn = customtkinter.CTkButton(
            buttons_frame,
            text="👁️ Previsualizar",
            width=140,
            height=35,
            command=self._preview_report
        )
        preview_btn.grid(row=0, column=0, padx=5)

        word_btn = customtkinter.CTkButton(
            buttons_frame,
            text="📄 Word",
            width=120,
            height=35,
            command=self._export_word
        )
        word_btn.grid(row=0, column=1, padx=5)

        excel_btn = customtkinter.CTkButton(
            buttons_frame,
            text="📊 Excel",
            width=120,
            height=35,
            command=self._export_excel
        )
        excel_btn.grid(row=0, column=2, padx=5)

        pdf_btn = customtkinter.CTkButton(
            buttons_frame,
            text="📕 PDF",
            width=120,
            height=35,
            command=self._export_pdf
        )
        pdf_btn.grid(row=0, column=3, padx=5)

        print_btn = customtkinter.CTkButton(
            buttons_frame,
            text="🖨️ Imprimir",
            width=120,
            height=35,
            command=self._print_report
        )
        print_btn.grid(row=0, column=4, padx=5)

    def _add_clasificacion(self):
        """Añade un nuevo selector de clasificación"""
        row = len(self.clasificaciones)

        clasif_container = customtkinter.CTkFrame(self.clasificaciones_frame)
        clasif_container.grid(row=row, column=0, sticky="ew", pady=5)
        clasif_container.grid_columnconfigure(1, weight=1)
        clasif_container.grid_columnconfigure(3, weight=1)

        # Label
        label = customtkinter.CTkLabel(
            clasif_container,
            text=f"Clasificación {row + 1}:",
            font=customtkinter.CTkFont(size=11)
        )
        label.grid(row=0, column=0, padx=(0, 10), sticky="w")

        # Variable
        var_label = customtkinter.CTkLabel(clasif_container, text="Variable:")
        var_label.grid(row=0, column=1, sticky="w", padx=(0, 5))

        var_combo = customtkinter.CTkComboBox(
            clasif_container,
            values=["Seleccionar..."],
            width=200
        )
        var_combo.grid(row=0, column=2, sticky="w", padx=(0, 20))

        # Orden
        orden_label = customtkinter.CTkLabel(clasif_container, text="Orden:")
        orden_label.grid(row=0, column=3, sticky="w", padx=(0, 5))

        orden_combo = customtkinter.CTkComboBox(
            clasif_container,
            values=ORDEN_OPCIONES,
            width=150
        )
        orden_combo.grid(row=0, column=4, sticky="w", padx=(0, 10))

        # Botón eliminar
        del_btn = customtkinter.CTkButton(
            clasif_container,
            text="🗑️",
            width=40,
            fg_color="darkred",
            hover_color="red",
            command=lambda: self._remove_clasificacion(clasif_container)
        )
        del_btn.grid(row=0, column=5, padx=(0, 5))

        self.clasificaciones.append({
            'container': clasif_container,
            'var_combo': var_combo,
            'orden_combo': orden_combo
        })

    def _remove_clasificacion(self, container):
        """Elimina un selector de clasificación"""
        container.destroy()
        # Actualizar lista
        self.clasificaciones = [c for c in self.clasificaciones if c['container'].winfo_exists()]

    def _add_filtro(self):
        """Añade un nuevo selector de filtro"""
        row = len(self.filtros)

        filtro_container = customtkinter.CTkFrame(self.filtros_frame)
        filtro_container.grid(row=row, column=0, sticky="ew", pady=5)
        filtro_container.grid_columnconfigure(2, weight=1)

        # Lógica (Y/O) - solo si no es el primero
        if row > 0:
            logica_combo = customtkinter.CTkComboBox(
                filtro_container,
                values=LOGICA_FILTROS,
                width=60
            )
            logica_combo.grid(row=0, column=0, padx=(0, 10), sticky="w")
        else:
            logica_combo = None

        # Label
        label = customtkinter.CTkLabel(
            filtro_container,
            text=f"Filtro {row + 1}:",
            font=customtkinter.CTkFont(size=11)
        )
        label.grid(row=0, column=1, padx=(0, 10), sticky="w")

        # Campo
        campo_label = customtkinter.CTkLabel(filtro_container, text="Campo:")
        campo_label.grid(row=0, column=2, sticky="w", padx=(0, 5))

        campo_combo = customtkinter.CTkComboBox(
            filtro_container,
            values=["Seleccionar..."],
            width=150
        )
        campo_combo.grid(row=0, column=3, sticky="w", padx=(0, 15))

        # Operador
        operador_label = customtkinter.CTkLabel(filtro_container, text="Operador:")
        operador_label.grid(row=0, column=4, sticky="w", padx=(0, 5))

        operador_combo = customtkinter.CTkComboBox(
            filtro_container,
            values=["Seleccionar..."],
            width=130
        )
        operador_combo.grid(row=0, column=5, sticky="w", padx=(0, 15))

        # Valor
        valor_label = customtkinter.CTkLabel(filtro_container, text="Valor:")
        valor_label.grid(row=0, column=6, sticky="w", padx=(0, 5))

        valor_entry = customtkinter.CTkEntry(filtro_container, width=150)
        valor_entry.grid(row=0, column=7, sticky="w", padx=(0, 10))

        # Botón eliminar
        del_btn = customtkinter.CTkButton(
            filtro_container,
            text="🗑️",
            width=40,
            fg_color="darkred",
            hover_color="red",
            command=lambda: self._remove_filtro(filtro_container)
        )
        del_btn.grid(row=0, column=8, padx=(0, 5))

        self.filtros.append({
            'container': filtro_container,
            'logica_combo': logica_combo,
            'campo_combo': campo_combo,
            'operador_combo': operador_combo,
            'valor_entry': valor_entry
        })

    def _remove_filtro(self, container):
        """Elimina un selector de filtro"""
        container.destroy()
        # Actualizar lista
        self.filtros = [f for f in self.filtros if f['container'].winfo_exists()]

    def _update_campos_disponibles(self):
        """Actualiza los campos disponibles según la categoría seleccionada"""
        # Limpiar campos actuales
        for widget in self.campos_scrollable.winfo_children():
            widget.destroy()

        self.campos_seleccionados = {}

        # Determinar qué campos mostrar
        campos_dict = None
        if "Partes" in self.categoria_seleccionada:
            campos_dict = CAMPOS_PARTES
        elif "Recursos" in self.categoria_seleccionada:
            campos_dict = CAMPOS_RECURSOS
        elif "Presupuestos" in self.categoria_seleccionada:
            campos_dict = CAMPOS_PRESUPUESTOS
        elif "Certificaciones" in self.categoria_seleccionada:
            campos_dict = CAMPOS_CERTIFICACIONES
        elif "Planificación" in self.categoria_seleccionada:
            campos_dict = CAMPOS_PLANIFICACION

        if not campos_dict:
            return

        # Crear checkboxes por grupos
        row = 0
        for grupo, campos in campos_dict.items():
            # Título del grupo
            grupo_label = customtkinter.CTkLabel(
                self.campos_scrollable,
                text=f"{grupo}:",
                font=customtkinter.CTkFont(size=12, weight="bold")
            )
            grupo_label.grid(row=row, column=0, columnspan=3, sticky="w", pady=(10, 5))
            row += 1

            # Checkboxes en 3 columnas
            col = 0
            for campo in campos:
                var = customtkinter.BooleanVar(value=True)
                check = customtkinter.CTkCheckBox(
                    self.campos_scrollable,
                    text=campo,
                    variable=var
                )
                check.grid(row=row, column=col, sticky="w", padx=5, pady=2)

                self.campos_seleccionados[campo] = var

                col += 1
                if col >= 3:
                    col = 0
                    row += 1

            if col > 0:
                row += 1

    def _select_all_campos(self):
        """Selecciona todos los campos"""
        for var in self.campos_seleccionados.values():
            var.set(True)

    def _deselect_all_campos(self):
        """Deselecciona todos los campos"""
        for var in self.campos_seleccionados.values():
            var.set(False)

    def _open_config_dialog(self):
        """Abre el diálogo de configuración de cabecera"""
        from CTkMessagebox import CTkMessagebox

        CTkMessagebox(
            title="Configuración",
            message="Funcionalidad de configuración de cabecera en desarrollo.\n\n"
                    "Próximamente podrás configurar:\n"
                    "• Datos de la empresa\n"
                    "• Logo corporativo\n"
                    "• Datos del proyecto\n"
                    "• Pie de página personalizado",
            icon="info"
        )

    def _preview_report(self):
        """Previsualiza el informe"""
        from CTkMessagebox import CTkMessagebox

        if not self.informe_seleccionado:
            CTkMessagebox(
                title="Aviso",
                message="Por favor, seleccione un informe del menú izquierdo.",
                icon="warning"
            )
            return

        CTkMessagebox(
            title="Previsualización",
            message=f"Vista previa del informe:\n{self.informe_seleccionado}\n\n"
                    "Funcionalidad en desarrollo.",
            icon="info"
        )

    def _export_word(self):
        """Exporta a Word"""
        self._export_message("Word (.docx)")

    def _export_excel(self):
        """Exporta a Excel"""
        self._export_message("Excel (.xlsx)")

    def _export_pdf(self):
        """Exporta a PDF"""
        self._export_message("PDF (.pdf)")

    def _print_report(self):
        """Imprime el informe"""
        from CTkMessagebox import CTkMessagebox

        if not self.informe_seleccionado:
            CTkMessagebox(
                title="Aviso",
                message="Por favor, seleccione un informe del menú izquierdo.",
                icon="warning"
            )
            return

        CTkMessagebox(
            title="Imprimir",
            message="Funcionalidad de impresión en desarrollo.",
            icon="info"
        )

    def _export_message(self, format_name):
        """Muestra mensaje de exportación"""
        from CTkMessagebox import CTkMessagebox

        if not self.informe_seleccionado:
            CTkMessagebox(
                title="Aviso",
                message="Por favor, seleccione un informe del menú izquierdo.",
                icon="warning"
            )
            return

        CTkMessagebox(
            title=f"Exportar a {format_name}",
            message=f"Exportación a {format_name} en desarrollo.\n\n"
                    f"Informe seleccionado: {self.informe_seleccionado}",
            icon="info"
        )
