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

        # Cargar filtros y datos iniciales
        self._load_filters()
        self._load_data()

    def _create_header(self):
        """Crea el encabezado con título y advertencia"""
        header_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        title = customtkinter.CTkLabel(
            header_frame,
            text="📦 CERTIFICACIÓN POR LOTES",
            font=customtkinter.CTkFont(size=24, weight="bold")
        )
        title.pack(side="left")

        # Advertencia
        warning_frame = customtkinter.CTkFrame(self, fg_color="#8B4513", corner_radius=10)
        warning_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

        warning = customtkinter.CTkLabel(
            warning_frame,
            text="⚠️ ADVERTENCIA: Esta función certifica el parte completo. Solo usar con partes sin certificaciones previas.",
            font=customtkinter.CTkFont(size=13, weight="bold"),
            text_color="white"
        )
        warning.pack(padx=15, pady=12)

    def _create_filters(self):
        """Crea la barra de filtros completa (como Listado de Partes)"""
        # Frame principal de filtros
        filter_frame = customtkinter.CTkFrame(self)
        filter_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        filter_frame.grid_columnconfigure(1, weight=1)
        filter_frame.grid_columnconfigure(3, weight=1)
        filter_frame.grid_columnconfigure(5, weight=1)

        # Fila 1: Red, Tipo, Tipo Reparación
        customtkinter.CTkLabel(filter_frame, text="Red:",
                               font=("", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.filter_red = customtkinter.CTkOptionMenu(filter_frame, values=["Todos"], width=150)
        self.filter_red.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.filter_red.set("Todos")

        customtkinter.CTkLabel(filter_frame, text="Tipo:",
                               font=("", 12, "bold")).grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.filter_tipo = customtkinter.CTkOptionMenu(filter_frame, values=["Todos"], width=150)
        self.filter_tipo.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.filter_tipo.set("Todos")

        customtkinter.CTkLabel(filter_frame, text="Tipo Rep.:",
                               font=("", 12, "bold")).grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.filter_tipo_rep = customtkinter.CTkOptionMenu(filter_frame, values=["Todos"], width=150)
        self.filter_tipo_rep.grid(row=0, column=5, padx=5, pady=5, sticky="w")
        self.filter_tipo_rep.set("Todos")

        # Fila 2: Código trabajo, Búsqueda
        customtkinter.CTkLabel(filter_frame, text="Cód. Trabajo:",
                               font=("", 12, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.filter_cod = customtkinter.CTkOptionMenu(filter_frame, values=["Todos"], width=150)
        self.filter_cod.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.filter_cod.set("Todos")

        # Búsqueda por campo
        customtkinter.CTkLabel(filter_frame, text="Buscar en:",
                               font=("", 12, "bold")).grid(row=1, column=2, padx=5, pady=5, sticky="e")

        search_fields = ["Código", "Descripción", "Red", "Municipio", "Localización"]
        self.search_field_map = {
            "Código": "codigo", "Descripción": "descripcion", "Red": "red",
            "Municipio": "municipio", "Localización": "localizacion"
        }
        self.search_field_selector = customtkinter.CTkOptionMenu(filter_frame, values=search_fields, width=120)
        self.search_field_selector.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.search_field_selector.set("Código")

        self.search_entry = customtkinter.CTkEntry(filter_frame, width=200, placeholder_text="Escriba el valor...")
        self.search_entry.grid(row=1, column=4, padx=5, pady=5, sticky="w")
        self.search_entry.bind("<KeyRelease>", lambda e: self._apply_search())

        # Botón Aplicar Filtros
        btn_apply = customtkinter.CTkButton(filter_frame, text="🔍 Aplicar", width=100, command=self._apply_filters)
        btn_apply.grid(row=1, column=5, padx=5, pady=5, sticky="w")

        # Fila 3: Fecha de certificación y opciones
        customtkinter.CTkLabel(filter_frame, text="Fecha Cert.:",
                               font=("", 12, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.fecha_cert = DateEntry(
            filter_frame, width=15, background='#1f6aa5', foreground='white',
            borderwidth=2, date_pattern='yyyy-mm-dd', locale='es_ES'
        )
        self.fecha_cert.set_date(date.today())
        self.fecha_cert.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Checkbox: Solo sin certificar
        self.solo_sin_cert_var = customtkinter.BooleanVar(value=True)
        self.solo_sin_cert_cb = customtkinter.CTkCheckBox(
            filter_frame, text="Solo partes SIN certificar",
            variable=self.solo_sin_cert_var, command=self._apply_filters,
            font=("", 12, "bold"), text_color="#FFD700"
        )
        self.solo_sin_cert_cb.grid(row=2, column=2, columnspan=2, padx=10, pady=5, sticky="w")

        # Botón selector de columnas
        btn_columns = customtkinter.CTkButton(
            filter_frame, text="📋 Columnas", width=100, command=self._open_column_selector
        )
        btn_columns.grid(row=2, column=5, padx=5, pady=5, sticky="w")

    def _create_table(self):
        """Crea la tabla con los partes (selección por filas)"""
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
            show="headings",  # Solo columnas, sin tree column
            selectmode="extended",  # Selección múltiple de filas
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

    def _create_buttons(self):
        """Crea los botones de acción"""
        btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")
        btn_frame.grid_columnconfigure(0, weight=1)

        # Estadísticas (ahora solo total de partes mostrados)
        self.stats_label = customtkinter.CTkLabel(
            btn_frame,
            text="Total de partes: 0",
            font=customtkinter.CTkFont(size=13, weight="bold")
        )
        self.stats_label.pack(side="left", padx=(0, 20))

        # Botón Certificar Seleccionados
        btn_cert_selected = customtkinter.CTkButton(
            btn_frame,
            text="✅ Certificar Partes Seleccionados",
            command=self._cert_selected,
            width=250,
            height=40,
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=customtkinter.CTkFont(size=14, weight="bold")
        )
        btn_cert_selected.pack(side="right", padx=5)

        # Botón Cerrar
        btn_close = customtkinter.CTkButton(
            btn_frame,
            text="❌ Cerrar",
            command=self.destroy,
            width=120,
            height=40,
            fg_color="gray"
        )
        btn_close.pack(side="right", padx=5)

    def _load_filters(self):
        """Carga los valores para los filtros desde la base de datos"""
        from script.modulo_db import get_dim_all

        try:
            # Cargar Redes
            redes = get_dim_all(self.user, self.password, self.schema, "dim_red")
            red_values = ["Todos"] + [r[1] if r[1] else r[2] for r in redes]  # codigo o descripcion
            self.filter_red.configure(values=red_values)

            # Cargar Tipos
            tipos = get_dim_all(self.user, self.password, self.schema, "dim_tipo_trabajo")
            tipo_values = ["Todos"] + [t[1] if t[1] else t[2] for t in tipos]
            self.filter_tipo.configure(values=tipo_values)

            # Cargar Tipos de Reparación
            tipos_rep = get_dim_all(self.user, self.password, self.schema, "dim_tipos_rep")
            rep_values = ["Todos"] + [t[1] if t[1] else t[2] for t in tipos_rep]
            self.filter_tipo_rep.configure(values=rep_values)

            # Cargar Códigos de Trabajo
            cod_trabajo = get_dim_all(self.user, self.password, self.schema, "dim_codigo_trabajo")
            cod_values = ["Todos"] + [f"{c[1]} - {c[2]}" for c in cod_trabajo if c[1] and c[2]]
            self.filter_cod.configure(values=cod_values)

        except Exception as e:
            print(f"Error cargando filtros: {e}")

    def _apply_filters(self):
        """Aplica todos los filtros y actualiza la tabla"""
        self._update_table()

    def _load_data(self):
        """Carga los datos de partes desde la base de datos"""
        from script.modulo_db import get_partes_resumen

        try:
            # Obtener todos los partes
            data = get_partes_resumen(self.user, self.password, self.schema)

            # Procesar datos
            # row: id, codigo, descripcion, estado, red, tipo, cod_trabajo, tipo_rep,
            #      presupuesto, certificado, pendiente, titulo, desc_corta, desc_larga,
            #      fecha_inicio, fecha_fin, created_at, updated_at, localizacion, municipio, ...
            self.partes_data = []
            for row in data:
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
                    'localizacion': row[18] if len(row) > 18 and row[18] else '',
                    'municipio': row[19] if len(row) > 19 and row[19] else '',
                }
                self.partes_data.append(parte)

            # Definir todas las columnas disponibles
            self.all_columns = list(self.partes_data[0].keys()) if self.partes_data else []

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

            # Insertar fila (tags con ID del parte para referencia)
            self.tree.insert("", "end", values=formatted_values, tags=(parte['id'],))

        # Actualizar estadísticas
        self.stats_label.configure(text=f"Total de partes: {len(filtered_data)}")

    def _filter_data(self, data):
        """Aplica todos los filtros a los datos"""
        filtered = data

        # Filtro: Solo sin certificar (por defecto activado)
        if self.solo_sin_cert_var.get():
            filtered = [p for p in filtered if p['certificado'] == 0]

        # Filtro Red
        red_filter = self.filter_red.get()
        if red_filter != "Todos":
            filtered = [p for p in filtered if red_filter.lower() in p['red'].lower()]

        # Filtro Tipo
        tipo_filter = self.filter_tipo.get()
        if tipo_filter != "Todos":
            filtered = [p for p in filtered if tipo_filter.lower() in p['tipo'].lower()]

        # Filtro Tipo Reparación
        tipo_rep_filter = self.filter_tipo_rep.get()
        if tipo_rep_filter != "Todos":
            filtered = [p for p in filtered if tipo_rep_filter.lower() in p['tipo_rep'].lower()]

        # Filtro Código Trabajo
        cod_filter = self.filter_cod.get()
        if cod_filter != "Todos":
            # El formato es "codigo - descripcion", extraemos el código
            cod_value = cod_filter.split(" - ")[0] if " - " in cod_filter else cod_filter
            filtered = [p for p in filtered if cod_value.lower() in p['cod_trabajo'].lower()]

        # Búsqueda por campo específico
        search_text = self.search_entry.get().strip().lower()
        if search_text:
            field_name = self.search_field_selector.get()
            field_key = self.search_field_map.get(field_name, "codigo")
            filtered = [p for p in filtered if search_text in str(p.get(field_key, '')).lower()]

        return filtered

    def _apply_search(self):
        """Aplica el filtro de búsqueda"""
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
        """Certifica los partes seleccionados (basado en selección de filas del TreeView)"""
        # Obtener filas seleccionadas del TreeView
        selected_items = self.tree.selection()

        if not selected_items:
            CTkMessagebox(
                title="Advertencia",
                message="No has seleccionado ningún parte.\n\nSelecciona filas de la tabla haciendo click.",
                icon="warning"
            )
            return

        fecha = self.fecha_cert.get_date().strftime('%Y-%m-%d')

        # Obtener datos de partes seleccionados
        selected_partes = []
        for item in selected_items:
            tags = self.tree.item(item, 'tags')
            if tags:
                parte_id = int(tags[0])
                # Buscar el parte en partes_data
                parte = next((p for p in self.partes_data if p['id'] == parte_id), None)
                if parte:
                    selected_partes.append(parte)

        msg = CTkMessagebox(
            title="Confirmar",
            message=f"¿Certificar {len(selected_partes)} parte(s) completo(s) con fecha {fecha}?\n\n" +
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

        for parte in selected_partes:
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
    # Test standalone - requiere credenciales desde variables de entorno
    import getpass

    app = customtkinter.CTk()
    app.withdraw()

    # Leer desde variables de entorno o solicitar
    USER = os.getenv('DB_USER') or input("Usuario de BD: ")
    PASSWORD = os.getenv('DB_PASSWORD') or getpass.getpass("Contraseña de BD: ")
    SCHEMA = os.getenv('DB_SCHEMA', 'cert_dev')

    win = CertLotesWindow(app, USER, PASSWORD, SCHEMA)
    app.mainloop()
