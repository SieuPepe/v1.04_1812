import customtkinter
from tkinter import ttk, filedialog
from CTkMessagebox import CTkMessagebox
from script.modulo_db import get_parts_list, get_dim_all, delete_parte
import pandas as pd
from datetime import datetime


class PartsTab(customtkinter.CTkFrame):
    def __init__(self, master, user, password, schema, **kwargs):
        super().__init__(master, **kwargs)
        self.user = user
        self.password = password
        self.schema = schema

        # Definir todas las columnas disponibles (codigo siempre primero)
        self.all_columns = {
            "codigo": {"label": "Código", "width": 120, "visible": True, "locked": True},
            "red": {"label": "Red", "width": 120, "visible": True, "locked": False},
            "tipo": {"label": "Tipo", "width": 100, "visible": True, "locked": False},
            "cod_trabajo": {"label": "Cód. Trabajo", "width": 120, "visible": True, "locked": False},
            "tipo_rep": {"label": "Tipo Reparación", "width": 130, "visible": True, "locked": False},
            "descripcion": {"label": "Descripción", "width": 300, "visible": True, "locked": False},
            "presupuesto": {"label": "Presupuesto (€)", "width": 120, "visible": True, "locked": False},
            "certificado": {"label": "Certificado (€)", "width": 120, "visible": True, "locked": False},
            "estado": {"label": "Estado", "width": 100, "visible": True, "locked": False},
            "created_at": {"label": "Fecha Creación", "width": 150, "visible": False, "locked": False},
        }

        self._build_ui()
        self._load_filters()
        self._load_data()

    def _build_ui(self):
        # Título
        lbl = customtkinter.CTkLabel(self, text="Listado de partes",
                                     font=("", 18, "bold"))
        lbl.pack(pady=(10, 5))

        # Frame de filtros
        filter_frame = customtkinter.CTkFrame(self, corner_radius=0)
        filter_frame.pack(fill="x", padx=10, pady=5)
        filter_frame.grid_columnconfigure(1, weight=1)
        filter_frame.grid_columnconfigure(3, weight=1)
        filter_frame.grid_columnconfigure(5, weight=1)

        # Filtro Red
        customtkinter.CTkLabel(filter_frame, text="Red:",
                               font=("", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.filter_red = customtkinter.CTkOptionMenu(filter_frame, values=["Todos"])
        self.filter_red.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.filter_red.set("Todos")

        # Filtro Tipo
        customtkinter.CTkLabel(filter_frame, text="Tipo:",
                               font=("", 12, "bold")).grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.filter_tipo = customtkinter.CTkOptionMenu(filter_frame, values=["Todos"])
        self.filter_tipo.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.filter_tipo.set("Todos")

        # Filtro Tipo de Reparación
        customtkinter.CTkLabel(filter_frame, text="Tipo Rep.:",
                               font=("", 12, "bold")).grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.filter_tipo_rep = customtkinter.CTkOptionMenu(filter_frame, values=["Todos"])
        self.filter_tipo_rep.grid(row=0, column=5, padx=5, pady=5, sticky="ew")
        self.filter_tipo_rep.set("Todos")

        # Filtro Código trabajo (con descripción)
        customtkinter.CTkLabel(filter_frame, text="Cód. Trabajo:",
                               font=("", 12, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.filter_cod = customtkinter.CTkOptionMenu(filter_frame, values=["Todos"])
        self.filter_cod.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.filter_cod.set("Todos")

        # Búsqueda por código/descripción
        customtkinter.CTkLabel(filter_frame, text="Buscar:",
                               font=("", 12, "bold")).grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.search_entry = customtkinter.CTkEntry(filter_frame,
                                                   placeholder_text="Código o descripción...")
        self.search_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        # Botón Aplicar Filtros
        self.btn_apply = customtkinter.CTkButton(filter_frame, text="Aplicar Filtros",
                                                 command=self._apply_filters, width=120)
        self.btn_apply.grid(row=1, column=4, padx=5, pady=5, sticky="ew")

        # Botón Columnas Visibles
        self.btn_columns = customtkinter.CTkButton(filter_frame, text="⚙ Columnas",
                                                   command=self._show_column_selector,
                                                   width=100, fg_color="#1f6aa5")
        self.btn_columns.grid(row=1, column=5, padx=5, pady=5, sticky="ew")

        # Frame para tabla
        self.table_frame = customtkinter.CTkFrame(self)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

        # Crear tabla con columnas visibles (se reconstruirá al cambiar columnas)
        self._rebuild_table()

        # Frame de botones
        btn_frame = customtkinter.CTkFrame(self)
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.btn_reload = customtkinter.CTkButton(btn_frame, text="Recargar",
                                                  command=self._load_data, width=120)
        self.btn_reload.pack(side="left", padx=5)

        self.btn_delete = customtkinter.CTkButton(btn_frame, text="Eliminar",
                                                  command=self._delete_selected,
                                                  fg_color="red", hover_color="#8B0000",
                                                  width=120)
        self.btn_delete.pack(side="left", padx=5)

        self.btn_export = customtkinter.CTkButton(btn_frame, text="Exportar a Excel",
                                                  command=self._export_excel,
                                                  fg_color="green", hover_color="#006400",
                                                  width=150)
        self.btn_export.pack(side="right", padx=5)

    def _rebuild_table(self):
        """Reconstruye la tabla con las columnas visibles seleccionadas"""
        # Eliminar tabla anterior si existe
        if hasattr(self, 'tree'):
            self.tree.destroy()
            self.yscroll.destroy()

        # Obtener columnas visibles (codigo siempre primero)
        visible_cols = ["id"]  # ID siempre incluido pero oculto
        visible_cols.append("codigo")  # Codigo siempre primero y visible

        # Agregar resto de columnas visibles
        for col_name, col_info in self.all_columns.items():
            if col_name != "codigo" and col_info["visible"]:
                visible_cols.append(col_name)

        # Crear nueva tabla
        self.tree = ttk.Treeview(self.table_frame, columns=visible_cols, show="headings", height=15)

        # Configurar columnas
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=0, stretch=False)  # ID oculto

        for col in visible_cols[1:]:  # Skip "id"
            col_info = self.all_columns.get(col, {"label": col, "width": 100})
            self.tree.heading(col, text=col_info["label"])
            self.tree.column(col, width=col_info["width"], anchor="w")

        # Scrollbar
        self.yscroll = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.yscroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.yscroll.grid(row=0, column=1, sticky="ns")

    def _show_column_selector(self):
        """Muestra ventana para seleccionar columnas visibles"""
        selector_window = customtkinter.CTkToplevel(self)
        selector_window.title("Seleccionar Columnas")
        selector_window.geometry("400x500")
        selector_window.grab_set()

        customtkinter.CTkLabel(
            selector_window,
            text="Seleccione las columnas a mostrar:",
            font=("", 14, "bold")
        ).pack(pady=10)

        customtkinter.CTkLabel(
            selector_window,
            text="(El campo 'Código' siempre es visible)",
            font=("", 10),
            text_color="gray"
        ).pack(pady=(0, 10))

        # Frame scrollable para checkboxes
        scroll_frame = customtkinter.CTkScrollableFrame(selector_window, width=350, height=300)
        scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Crear checkboxes
        checkboxes = {}
        for col_name, col_info in self.all_columns.items():
            if col_info["locked"]:
                continue  # Skip codigo (siempre visible)

            var = customtkinter.BooleanVar(value=col_info["visible"])
            cb = customtkinter.CTkCheckBox(
                scroll_frame,
                text=col_info["label"],
                variable=var,
                font=("", 12)
            )
            cb.pack(anchor="w", padx=10, pady=5)
            checkboxes[col_name] = var

        # Botones
        btn_frame = customtkinter.CTkFrame(selector_window)
        btn_frame.pack(pady=10)

        def apply_selection():
            # Actualizar visibilidad de columnas
            for col_name, var in checkboxes.items():
                self.all_columns[col_name]["visible"] = var.get()

            # Reconstruir tabla
            self._rebuild_table()
            # Recargar datos
            self._load_data()
            selector_window.destroy()

        customtkinter.CTkButton(
            btn_frame,
            text="Aplicar",
            command=apply_selection,
            fg_color="green",
            width=120
        ).pack(side="left", padx=5)

        customtkinter.CTkButton(
            btn_frame,
            text="Cancelar",
            command=selector_window.destroy,
            width=120
        ).pack(side="left", padx=5)

    def _load_filters(self):
        """Carga las opciones de filtros desde la base de datos"""
        try:
            dims = get_dim_all(self.user, self.password, self.schema)

            # Extraer solo los textos después del " - "
            red_values = ["Todos"] + [v.split(" - ")[1] if " - " in v else v for v in dims.get("RED", [])]
            tipo_values = ["Todos"] + [v.split(" - ")[1] if " - " in v else v for v in dims.get("TIPO_TRABAJO", [])]
            tipo_rep_values = ["Todos"] + [v.split(" - ")[1] if " - " in v else v for v in dims.get("TIPOS_REP", [])]

            # Para Código Trabajo, mostrar "codigo - descripcion"
            cod_raw = dims.get("COD_TRABAJO", [])
            cod_values = ["Todos"]
            for item in cod_raw:
                # item formato: "ID - CODIGO"
                # Necesitamos obtener la descripción de la DB
                cod_values.append(item)

            self.filter_red.configure(values=red_values)
            self.filter_tipo.configure(values=tipo_values)
            self.filter_tipo_rep.configure(values=tipo_rep_values)
            self.filter_cod.configure(values=cod_values)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error cargando filtros: {e}", icon="warning")

    def _load_data(self, filtered_rows=None):
        """Carga los datos en la tabla"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            if filtered_rows is None:
                rows = get_parts_list(self.user, self.password, self.schema, limit=1000)
            else:
                rows = filtered_rows

            # Mapeo de índices del resultado SQL
            # 0:id, 1:codigo, 2:red, 3:tipo, 4:cod_trabajo, 5:cod_trabajo_desc,
            # 6:tipo_rep, 7:descripcion, 8:presupuesto, 9:certificado, 10:estado, 11:creado_en
            field_map = {
                "id": 0,
                "codigo": 1,
                "red": 2,
                "tipo": 3,
                "cod_trabajo": 4,
                "cod_trabajo_desc": 5,
                "tipo_rep": 6,
                "descripcion": 7,
                "presupuesto": 8,
                "certificado": 9,
                "estado": 10,
                "created_at": 11
            }

            # Obtener columnas visibles actuales del tree
            visible_cols = self.tree["columns"]

            for row_data in rows:
                # Construir fila con solo las columnas visibles
                row_values = []
                for col in visible_cols:
                    idx = field_map.get(col)
                    if idx is not None and idx < len(row_data):
                        value = row_data[idx]
                        # Formatear valores especiales
                        if col in ["presupuesto", "certificado"] and value is not None:
                            row_values.append(f"{float(value):.2f}")
                        elif col == "created_at" and value is not None:
                            row_values.append(str(value))
                        else:
                            row_values.append(value if value is not None else "")
                    else:
                        row_values.append("")

                self.tree.insert("", "end", values=row_values)

        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error cargando datos: {e}", icon="cancel")

    def _apply_filters(self):
        """Aplica los filtros seleccionados"""
        try:
            # Cargar todos los datos
            all_rows = get_parts_list(self.user, self.password, self.schema, limit=1000)

            # Aplicar filtros
            # row = (id, codigo, red, tipo, cod_trabajo, cod_trabajo_desc, tipo_rep, descripcion,
            #        presupuesto, certificado, estado, created_at)
            filtered = []
            search_text = self.search_entry.get().lower()

            for row in all_rows:
                # Filtro Red
                if self.filter_red.get() != "Todos" and str(row[2]) != self.filter_red.get():
                    continue

                # Filtro Tipo
                if self.filter_tipo.get() != "Todos" and str(row[3]) != self.filter_tipo.get():
                    continue

                # Filtro Tipo Reparación
                if self.filter_tipo_rep.get() != "Todos" and str(row[6]) != self.filter_tipo_rep.get():
                    continue

                # Filtro Código Trabajo (comparar por código o descripción)
                if self.filter_cod.get() != "Todos":
                    filter_val = self.filter_cod.get()
                    # Extraer solo la parte después del " - " si existe
                    if " - " in filter_val:
                        filter_val = filter_val.split(" - ")[1]
                    if str(row[4]) != filter_val and str(row[5]) != filter_val:
                        continue

                # Búsqueda por código o descripción
                if search_text:
                    codigo_match = search_text in str(row[1]).lower()
                    desc_match = search_text in str(row[7]).lower()
                    if not (codigo_match or desc_match):
                        continue

                filtered.append(row)

            self._load_data(filtered)

        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error aplicando filtros: {e}", icon="cancel")

    def _delete_selected(self):
        """Elimina el parte seleccionado con confirmación"""
        selected = self.tree.selection()
        if not selected:
            CTkMessagebox(title="Aviso", message="Seleccione un parte para eliminar", icon="info")
            return

        # Obtener datos del registro seleccionado
        item = self.tree.item(selected[0])
        values = item['values']
        parte_id = values[0]
        codigo = values[1]

        # Confirmación
        msg = CTkMessagebox(
            title="Confirmar eliminación",
            message=f"¿Está seguro de eliminar el parte {codigo}?\n\nEsta acción no se puede deshacer.",
            icon="warning",
            option_1="Cancelar",
            option_2="Eliminar"
        )

        if msg.get() == "Eliminar":
            try:
                delete_parte(self.user, self.password, self.schema, parte_id)
                CTkMessagebox(title="Éxito",
                              message=f"Parte {codigo} eliminado correctamente",
                              icon="check")
                self._load_data()
            except Exception as e:
                CTkMessagebox(title="Error",
                              message=f"No se pudo eliminar el parte:\n{e}",
                              icon="cancel")

    def _export_excel(self):
        """Exporta los datos visibles a Excel"""
        try:
            # Obtener todos los elementos visibles en el tree
            data = []
            for item in self.tree.get_children():
                values = self.tree.item(item)['values']
                data.append(values)

            if not data:
                CTkMessagebox(title="Aviso", message="No hay datos para exportar", icon="info")
                return

            # Obtener nombres de columnas visibles actuales
            visible_cols = self.tree["columns"]
            col_labels = []
            for col in visible_cols:
                if col == "id":
                    col_labels.append("ID")
                else:
                    col_info = self.all_columns.get(col, {"label": col})
                    col_labels.append(col_info["label"])

            # Crear DataFrame
            df = pd.DataFrame(data, columns=col_labels)

            # Guardar en Excel
            filename = f"partes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            filepath = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=filename
            )

            if filepath:
                df.to_excel(filepath, index=False, engine='openpyxl')
                CTkMessagebox(title="Éxito",
                              message=f"Datos exportados a:\n{filepath}",
                              icon="check")
        except Exception as e:
            CTkMessagebox(title="Error",
                          message=f"Error al exportar:\n{e}",
                          icon="cancel")


class PartsListWindow(customtkinter.CTkToplevel):
    def __init__(self, master, user, password, schema):
        super().__init__(master)
        self.title("Listado de partes")
        self.geometry("1300x700")
        self.focus()
        tab = PartsTab(self, user, password, schema)
        tab.pack(fill="both", expand=True)


def open_parts_list(master, user, password, schema):
    """Función cómoda para abrir desde cualquier pantalla"""
    win = PartsListWindow(master, user, password, schema)
    return win


if __name__ == "__main__":
    app = customtkinter.CTk()
    app.title("Test ventana - Listado de partes")
    btn = customtkinter.CTkButton(app, text="Abrir lista",
                                  command=lambda: open_parts_list(app, "aperez", "WGueXNk9", "cert_dev"))
    btn.pack(padx=20, pady=20)
    app.mainloop()