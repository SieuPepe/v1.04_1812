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

        # Filtro OT
        customtkinter.CTkLabel(filter_frame, text="OT:",
                               font=("", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.filter_ot = customtkinter.CTkOptionMenu(filter_frame, values=["Todos"])
        self.filter_ot.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.filter_ot.set("Todos")

        # Filtro Red
        customtkinter.CTkLabel(filter_frame, text="Red:",
                               font=("", 12, "bold")).grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.filter_red = customtkinter.CTkOptionMenu(filter_frame, values=["Todos"])
        self.filter_red.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.filter_red.set("Todos")

        # Filtro Tipo
        customtkinter.CTkLabel(filter_frame, text="Tipo:",
                               font=("", 12, "bold")).grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.filter_tipo = customtkinter.CTkOptionMenu(filter_frame, values=["Todos"])
        self.filter_tipo.grid(row=0, column=5, padx=5, pady=5, sticky="ew")
        self.filter_tipo.set("Todos")

        # Filtro Código trabajo
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
        self.btn_apply.grid(row=1, column=4, columnspan=2, padx=5, pady=5, sticky="ew")

        # Frame para tabla
        frame = customtkinter.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Tabla
        cols = ("id", "codigo", "ot", "red", "tipo", "cod_trabajo", "descripcion", "created_at")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=15)
        for c, w in zip(cols, (60, 110, 120, 120, 120, 140, 300, 180)):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor="w")

        yscroll = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")

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

    def _load_filters(self):
        """Carga las opciones de filtros desde la base de datos"""
        try:
            dims = get_dim_all(self.user, self.password, self.schema)

            # Extraer solo los textos después del " - "
            ot_values = ["Todos"] + [v.split(" - ")[1] if " - " in v else v for v in dims.get("OT", [])]
            red_values = ["Todos"] + [v.split(" - ")[1] if " - " in v else v for v in dims.get("RED", [])]
            tipo_values = ["Todos"] + [v.split(" - ")[1] if " - " in v else v for v in dims.get("TIPO_TRABAJO", [])]
            cod_values = ["Todos"] + [v.split(" - ")[1] if " - " in v else v for v in dims.get("COD_TRABAJO", [])]

            self.filter_ot.configure(values=ot_values)
            self.filter_red.configure(values=red_values)
            self.filter_tipo.configure(values=tipo_values)
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

            for r in rows:
                r2 = list(r)
                if len(r2) > 7 and r2[7] is not None:
                    r2[7] = str(r2[7])
                self.tree.insert("", "end", values=r2)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error cargando datos: {e}", icon="cancel")

    def _apply_filters(self):
        """Aplica los filtros seleccionados"""
        try:
            # Cargar todos los datos
            all_rows = get_parts_list(self.user, self.password, self.schema, limit=1000)

            # Aplicar filtros
            filtered = []
            search_text = self.search_entry.get().lower()

            for row in all_rows:
                # row = (id, codigo, ot, red, tipo, cod_trabajo, descripcion, created_at)
                if self.filter_ot.get() != "Todos" and row[2] != self.filter_ot.get():
                    continue
                if self.filter_red.get() != "Todos" and row[3] != self.filter_red.get():
                    continue
                if self.filter_tipo.get() != "Todos" and row[4] != self.filter_tipo.get():
                    continue
                if self.filter_cod.get() != "Todos" and row[5] != self.filter_cod.get():
                    continue
                if search_text and search_text not in str(row[1]).lower() and search_text not in str(row[6]).lower():
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

            # Crear DataFrame
            cols = ["ID", "Código", "OT", "Red", "Tipo", "Cód. Trabajo", "Descripción", "Fecha Creación"]
            df = pd.DataFrame(data, columns=cols)

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