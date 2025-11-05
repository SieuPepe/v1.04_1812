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

        # Cargar datos iniciales
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
        """Crea la barra de filtros y calendario"""
        filter_frame = customtkinter.CTkFrame(self)
        filter_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

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

        # Botón de búsqueda
        customtkinter.CTkLabel(
            filter_frame,
            text="Buscar:",
            font=customtkinter.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=2, padx=(20, 5), pady=10, sticky="w")

        self.search_entry = customtkinter.CTkEntry(filter_frame, width=300, placeholder_text="Buscar por código, red, descripción...")
        self.search_entry.grid(row=0, column=3, padx=(0, 10), pady=10, sticky="w")
        self.search_entry.bind("<KeyRelease>", lambda e: self._apply_search())

        # Botón selector de columnas
        btn_columns = customtkinter.CTkButton(
            filter_frame,
            text="📋 Columnas",
            width=120,
            command=self._open_column_selector
        )
        btn_columns.grid(row=0, column=4, padx=(20, 10), pady=10)

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
                    'pendiente': float(row[10]) if row[10] else 0.0
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
        """Aplica búsqueda de texto a los datos"""
        filtered = data

        # Búsqueda por texto (código, red, descripción)
        search_text = self.search_entry.get().lower()
        if search_text:
            filtered = [
                p for p in filtered
                if search_text in p['codigo'].lower()
                or search_text in p['red'].lower()
                or search_text in p['descripcion'].lower()
            ]

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
    # Test standalone
    app = customtkinter.CTk()
    app.withdraw()

    USER = "root"
    PASSWORD = "NuevaPass!2025"
    SCHEMA = "cert_dev"

    win = CertLotesWindow(app, USER, PASSWORD, SCHEMA)
    app.mainloop()
