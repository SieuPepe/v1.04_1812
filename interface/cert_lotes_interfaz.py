# interface/cert_lotes_interfaz.py
"""
Ventana de Certificación por Lotes.

Permite certificar partes completos de forma masiva con filtros y selección múltiple.
Similar a la ventana de listado de partes, pero enfocada en certificación.
"""

import sys
import os
from pathlib import Path

# Añadir directorio raíz al path
root_dir = Path(__file__).parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import customtkinter
from CTkMessagebox import CTkMessagebox
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date


class CertLotesWindow(customtkinter.CTkToplevel):
    """Ventana para certificación masiva de partes completos"""

    def __init__(self, parent, user: str, password: str, schema: str):
        super().__init__(parent)

        self.title("Certificación por Lotes")
        self.geometry("1400x800")
        self.user = user
        self.password = password
        self.schema = schema

        # Asegurar que la ventana aparezca al frente
        self.lift()
        self.focus_force()

        # Variables
        self.current_filter = "sin_certificar"  # Filtro por defecto
        self.selected_columns = ["codigo", "red", "presupuesto", "certificado"]
        self.all_columns = []
        self.partes_data = []

        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Crear interfaz
        self._create_header()
        self._create_filters()
        self._create_table()
        self._create_buttons()

        # Cargar datos iniciales
        self._load_data()

    def _create_header(self):
        """Crea el encabezado con título"""
        header_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        title = customtkinter.CTkLabel(
            header_frame,
            text="📦 CERTIFICACIÓN POR LOTES",
            font=customtkinter.CTkFont(size=24, weight="bold")
        )
        title.pack(side="left")

        # Info
        info = customtkinter.CTkLabel(
            header_frame,
            text="Selecciona partes completos para certificar",
            font=customtkinter.CTkFont(size=12),
            text_color="gray"
        )
        info.pack(side="left", padx=(20, 0))

    def _create_filters(self):
        """Crea la barra de filtros y calendario"""
        filter_frame = customtkinter.CTkFrame(self)
        filter_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Fecha de certificación
        customtkinter.CTkLabel(
            filter_frame,
            text="Fecha de Certificación:",
            font=customtkinter.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")

        self.fecha_cert = DateEntry(
            filter_frame,
            width=20,
            background='#1f6aa5',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd',
            locale='es_ES'
        )
        self.fecha_cert.set_date(date.today())
        self.fecha_cert.grid(row=0, column=1, padx=(0, 20), pady=10, sticky="w")

        # Filtro
        customtkinter.CTkLabel(
            filter_frame,
            text="Filtro:",
            font=customtkinter.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=2, padx=(10, 5), pady=10, sticky="w")

        self.filter_menu = customtkinter.CTkOptionMenu(
            filter_frame,
            values=[
                "Sin certificar",
                "Parcialmente certificados",
                "Completamente certificados",
                "Todos"
            ],
            command=self._apply_filter,
            width=220
        )
        self.filter_menu.set("Sin certificar")
        self.filter_menu.grid(row=0, column=3, padx=(0, 20), pady=10, sticky="w")

        # Botón de búsqueda
        customtkinter.CTkLabel(
            filter_frame,
            text="Buscar:",
            font=customtkinter.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=4, padx=(10, 5), pady=10, sticky="w")

        self.search_entry = customtkinter.CTkEntry(filter_frame, width=250, placeholder_text="Buscar por código, red...")
        self.search_entry.grid(row=0, column=5, padx=(0, 10), pady=10, sticky="w")
        self.search_entry.bind("<KeyRelease>", lambda e: self._apply_search())

        # Botón selector de columnas
        btn_columns = customtkinter.CTkButton(
            filter_frame,
            text="Columnas",
            width=100,
            command=self._open_column_selector
        )
        btn_columns.grid(row=0, column=6, padx=(10, 10), pady=10)

    def _create_table(self):
        """Crea la tabla con los partes"""
        table_frame = customtkinter.CTkFrame(self)
        table_frame.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Crear Treeview con scrollbar
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")

        self.tree = ttk.Treeview(
            table_frame,
            columns=(),  # Se definirán dinámicamente
            show="tree headings",
            selectmode="extended",  # Selección múltiple
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        # Estilo
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background="#2b2b2b",
                       foreground="white",
                       fieldbackground="#2b2b2b",
                       rowheight=30)
        style.configure("Treeview.Heading",
                       background="#1f538d",
                       foreground="white",
                       font=('', 11, 'bold'))
        style.map("Treeview",
                 background=[('selected', '#1f6aa5')])

        # Checkbox en primera columna
        self.tree.heading("#0", text="☐", anchor="center")
        self.tree.column("#0", width=40, stretch=False)
        self.tree.bind("<ButtonRelease-1>", self._on_tree_click)

    def _create_buttons(self):
        """Crea los botones de acción"""
        btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")
        btn_frame.grid_columnconfigure(0, weight=1)

        # Estadísticas
        self.stats_label = customtkinter.CTkLabel(
            btn_frame,
            text="Seleccionados: 0 | Total: 0",
            font=customtkinter.CTkFont(size=13, weight="bold")
        )
        self.stats_label.pack(side="left", padx=(0, 20))

        # Botón Seleccionar Todos
        btn_select_all = customtkinter.CTkButton(
            btn_frame,
            text="Seleccionar Todos Visibles",
            command=self._select_all_visible,
            width=200,
            height=35
        )
        btn_select_all.pack(side="left", padx=5)

        # Botón Deseleccionar Todos
        btn_deselect_all = customtkinter.CTkButton(
            btn_frame,
            text="Deseleccionar Todos",
            command=self._deselect_all,
            width=180,
            height=35,
            fg_color="gray"
        )
        btn_deselect_all.pack(side="left", padx=5)

        # Botón Certificar Seleccionados
        btn_cert_selected = customtkinter.CTkButton(
            btn_frame,
            text="✅ Certificar Seleccionados",
            command=self._cert_selected,
            width=220,
            height=35,
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=customtkinter.CTkFont(size=14, weight="bold")
        )
        btn_cert_selected.pack(side="right", padx=5)

        # Botón Cerrar
        btn_close = customtkinter.CTkButton(
            btn_frame,
            text="Cerrar",
            command=self.destroy,
            width=100,
            height=35,
            fg_color="gray"
        )
        btn_close.pack(side="right", padx=5)

    def _load_data(self):
        """Carga los datos de partes desde la base de datos"""
        from script.modulo_db import get_partes_resumen

        try:
            # Obtener todos los partes
            data = get_partes_resumen(self.user, self.password, self.schema)

            # Procesar datos
            self.partes_data = []
            for row in data:
                # row: id, codigo, descripcion, estado, red, tipo, cod_trabajo, tipo_rep,
                #      presupuesto, certificado, pendiente, + otros campos
                parte = {
                    'id': row[0],
                    'codigo': row[1] or '',
                    'descripcion': row[2] or '',
                    'estado': row[3] or '',
                    'red': row[4] or '',
                    'tipo': row[5] or '',
                    'cod_trabajo': row[6] or '',
                    'tipo_rep': row[7] or '',
                    'presupuesto': float(row[8]) if row[8] else 0.0,
                    'certificado': float(row[9]) if row[9] else 0.0,
                    'pendiente': float(row[10]) if row[10] else 0.0,
                    'selected': False
                }
                self.partes_data.append(parte)

            # Definir todas las columnas disponibles
            self.all_columns = list(self.partes_data[0].keys()) if self.partes_data else []
            if 'selected' in self.all_columns:
                self.all_columns.remove('selected')

            # Actualizar tabla
            self._update_table()

        except Exception as e:
            import traceback
            traceback.print_exc()
            CTkMessagebox(
                title="Error",
                message=f"Error cargando datos:\n{e}",
                icon="cancel"
            )

    def _update_table(self):
        """Actualiza la tabla con los datos filtrados"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Configurar columnas
        display_cols = [col for col in self.selected_columns if col in self.all_columns]
        self.tree.config(columns=display_cols)

        # Configurar encabezados
        for col in display_cols:
            self.tree.heading(col, text=col.upper().replace('_', ' '), anchor="w")
            width = 150 if col in ['descripcion', 'cod_trabajo'] else 120
            self.tree.column(col, width=width, anchor="w")

        # Aplicar filtro y búsqueda
        filtered_data = self._filter_data(self.partes_data)

        # Insertar datos
        for parte in filtered_data:
            values = [parte.get(col, '') for col in display_cols]

            # Formatear valores numéricos
            formatted_values = []
            for i, val in enumerate(values):
                col_name = display_cols[i]
                if col_name in ['presupuesto', 'certificado', 'pendiente']:
                    formatted_values.append(f"{float(val):.2f}€" if val else "0.00€")
                else:
                    formatted_values.append(str(val))

            # Icono de checkbox
            check_icon = "☑" if parte['selected'] else "☐"
            self.tree.insert("", "end", text=check_icon, values=formatted_values, tags=(parte['id'],))

        # Actualizar estadísticas
        selected_count = sum(1 for p in filtered_data if p['selected'])
        self.stats_label.configure(text=f"Seleccionados: {selected_count} | Total: {len(filtered_data)}")

    def _filter_data(self, data):
        """Aplica filtros a los datos"""
        filtered = data

        # Filtro por estado de certificación
        filter_value = self.filter_menu.get()
        if filter_value == "Sin certificar":
            filtered = [p for p in filtered if p['certificado'] == 0]
        elif filter_value == "Parcialmente certificados":
            filtered = [p for p in filtered if 0 < p['certificado'] < p['presupuesto']]
        elif filter_value == "Completamente certificados":
            filtered = [p for p in filtered if p['certificado'] >= p['presupuesto'] and p['presupuesto'] > 0]
        # "Todos" no filtra nada

        # Filtro de búsqueda
        search_text = self.search_entry.get().lower()
        if search_text:
            filtered = [
                p for p in filtered
                if search_text in p['codigo'].lower()
                or search_text in p['red'].lower()
                or search_text in p['descripcion'].lower()
            ]

        return filtered

    def _apply_filter(self, choice):
        """Aplica el filtro seleccionado"""
        self._update_table()

    def _apply_search(self):
        """Aplica el filtro de búsqueda"""
        self._update_table()

    def _on_tree_click(self, event):
        """Maneja clics en la tabla para selección"""
        region = self.tree.identify_region(event.x, event.y)
        if region == "tree":
            # Click en checkbox
            item = self.tree.identify_row(event.y)
            if item:
                tags = self.tree.item(item, 'tags')
                if tags:
                    parte_id = int(tags[0])
                    # Toggle selección
                    for parte in self.partes_data:
                        if parte['id'] == parte_id:
                            parte['selected'] = not parte['selected']
                            break
                    self._update_table()

    def _select_all_visible(self):
        """Selecciona todos los partes visibles"""
        filtered = self._filter_data(self.partes_data)
        for parte in filtered:
            parte['selected'] = True
        self._update_table()

    def _deselect_all(self):
        """Deselecciona todos los partes"""
        for parte in self.partes_data:
            parte['selected'] = False
        self._update_table()

    def _open_column_selector(self):
        """Abre ventana para seleccionar columnas visibles"""
        win = customtkinter.CTkToplevel(self)
        win.title("Seleccionar Columnas")
        win.geometry("400x500")
        win.resizable(False, False)
        win.attributes('-topmost', True)

        customtkinter.CTkLabel(
            win,
            text="Selecciona las columnas a mostrar:",
            font=customtkinter.CTkFont(size=14, weight="bold")
        ).pack(pady=(20, 10))

        # Frame con scroll para checkboxes
        scroll_frame = customtkinter.CTkScrollableFrame(win, width=360, height=350)
        scroll_frame.pack(padx=20, pady=10)

        checkboxes = {}
        for col in self.all_columns:
            var = customtkinter.BooleanVar(value=(col in self.selected_columns))
            cb = customtkinter.CTkCheckBox(
                scroll_frame,
                text=col.upper().replace('_', ' '),
                variable=var
            )
            cb.pack(anchor="w", pady=5)
            checkboxes[col] = var

        def apply_selection():
            self.selected_columns = [col for col, var in checkboxes.items() if var.get()]
            if not self.selected_columns:
                CTkMessagebox(title="Error", message="Debes seleccionar al menos una columna", icon="warning")
                return
            self._update_table()
            win.destroy()

        btn_apply = customtkinter.CTkButton(win, text="Aplicar", command=apply_selection, width=150)
        btn_apply.pack(pady=(10, 20))

    def _cert_selected(self):
        """Certifica los partes seleccionados"""
        selected = [p for p in self.partes_data if p['selected']]

        if not selected:
            CTkMessagebox(
                title="Advertencia",
                message="No has seleccionado ningún parte",
                icon="warning"
            )
            return

        fecha = self.fecha_cert.get_date().strftime('%Y-%m-%d')

        msg = CTkMessagebox(
            title="Confirmar",
            message=f"¿Certificar {len(selected)} parte(s) completo(s) con fecha {fecha}?\n\n" +
                    "Esto certificará TODAS las partidas presupuestadas de cada parte.",
            icon="question",
            option_1="Cancelar",
            option_2="Certificar"
        )

        if msg.get() != "Certificar":
            return

        # Realizar certificación
        from script.modulo_db import cert_parte_completo

        success_count = 0
        error_count = 0
        errors = []

        for parte in selected:
            try:
                result = cert_parte_completo(
                    self.user,
                    self.password,
                    self.schema,
                    parte['id'],
                    fecha
                )
                if result == "ok":
                    success_count += 1
                    parte['selected'] = False  # Deseleccionar
                else:
                    error_count += 1
                    errors.append(f"Parte {parte['codigo']}: {result}")
            except Exception as e:
                error_count += 1
                errors.append(f"Parte {parte['codigo']}: {str(e)}")

        # Mostrar resultado
        if error_count == 0:
            CTkMessagebox(
                title="Éxito",
                message=f"✅ {success_count} parte(s) certificado(s) correctamente",
                icon="check"
            )
        else:
            error_msg = "\n".join(errors[:5])  # Mostrar solo los primeros 5 errores
            if len(errors) > 5:
                error_msg += f"\n... y {len(errors) - 5} errores más"

            CTkMessagebox(
                title="Resultado Parcial",
                message=f"✅ Exitosos: {success_count}\n❌ Fallidos: {error_count}\n\nErrores:\n{error_msg}",
                icon="warning"
            )

        # Recargar datos
        self._load_data()


if __name__ == "__main__":
    # Test standalone
    app = customtkinter.CTk()
    app.withdraw()

    USER = "root"
    PASSWORD = "NuevaPass!2025"
    SCHEMA = "cert_dev"

    win = CertLotesWindow(app, USER, PASSWORD, SCHEMA)
    app.mainloop()
