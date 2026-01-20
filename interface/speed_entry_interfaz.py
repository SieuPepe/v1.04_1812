"""
Ventana de Entrada Rápida de Presupuestos (Speed Entry).
Permite introducir partidas de presupuesto de forma ágil usando solo el teclado.
"""

import customtkinter
from tkinter import ttk
from CTkMessagebox import CTkMessagebox


class SpeedEntryWindow(customtkinter.CTkToplevel):
    """Ventana de entrada rápida de presupuestos."""

    def __init__(self, parent, user: str, password: str, schema: str,
                 parte_id: int, parte_codigo: str, parte_titulo: str = "",
                 on_close_callback=None):
        super().__init__(parent)

        self.user = user
        self.password = password
        self.schema = schema
        self.parte_id = parte_id
        self.parte_codigo = parte_codigo
        self.parte_titulo = parte_titulo
        self.on_close_callback = on_close_callback

        # Lista de partidas añadidas en esta sesión
        self.items_added = []

        # Cache del catálogo para autocompletado
        self.catalogo_cache = {}
        self._load_catalogo_cache()

        # Configuración de ventana
        self.title(f"Entrada Rápida - {parte_codigo}")
        self.geometry("900x600")
        self.minsize(800, 500)

        # Hacer modal
        self.transient(parent)
        self.grab_set()

        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Crear interfaz
        self._create_header()
        self._create_entry_row()
        self._create_items_table()
        self._create_footer()

        # Centrar ventana
        self.update_idletasks()
        self._center_window()

        # Bindings de teclado
        self._setup_bindings()

        # Focus en el campo de código
        self.after(100, lambda: self.codigo_entry.focus_set())

    def _center_window(self):
        """Centra la ventana en la pantalla."""
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _load_catalogo_cache(self):
        """Carga el catálogo de partidas en cache para autocompletado."""
        try:
            from script.modulo_db import get_catalogo_partidas
            partidas = get_catalogo_partidas(self.user, self.password, self.schema)
            for row in partidas:
                # row: (id, codigo, resumen, coste, codigo_cap, capitulo, unidad)
                codigo = row[1].strip().upper() if row[1] else ""
                self.catalogo_cache[codigo] = {
                    'id': row[0],
                    'codigo': row[1],
                    'resumen': row[2] or "",
                    'precio': float(row[3]) if row[3] else 0.0,
                    'capitulo': row[5] or "",
                    'unidad': row[6] or ""
                }
        except Exception as e:
            print(f"Error cargando catálogo: {e}")

    def _create_header(self):
        """Crea el encabezado con información del parte."""
        header_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="#1a472a")
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(1, weight=1)

        # Icono y título
        title_label = customtkinter.CTkLabel(
            header_frame,
            text=f"⚡ ENTRADA RÁPIDA",
            font=customtkinter.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        title_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Info del parte
        parte_info = f"{self.parte_codigo}"
        if self.parte_titulo:
            parte_info += f" | {self.parte_titulo}"

        info_label = customtkinter.CTkLabel(
            header_frame,
            text=parte_info,
            font=customtkinter.CTkFont(size=14),
            text_color="#90EE90"
        )
        info_label.grid(row=0, column=1, padx=20, pady=10, sticky="w")

        # Ayuda rápida
        help_label = customtkinter.CTkLabel(
            header_frame,
            text="Tab: Siguiente | Enter: Añadir | Esc: Cerrar",
            font=customtkinter.CTkFont(size=11),
            text_color="#aaaaaa"
        )
        help_label.grid(row=0, column=2, padx=20, pady=10, sticky="e")

    def _create_entry_row(self):
        """Crea la fila de entrada de datos."""
        entry_frame = customtkinter.CTkFrame(self, corner_radius=10)
        entry_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=15)
        entry_frame.grid_columnconfigure(1, weight=1)

        # Campo: Código de partida
        customtkinter.CTkLabel(
            entry_frame, text="Código:", font=("", 12, "bold")
        ).grid(row=0, column=0, padx=(15, 5), pady=15, sticky="e")

        self.codigo_entry = customtkinter.CTkEntry(
            entry_frame, width=150,
            placeholder_text="Ej: 01.001"
        )
        self.codigo_entry.grid(row=0, column=1, padx=5, pady=15, sticky="w")

        # Campo: Descripción (autocompletada, solo lectura visual)
        customtkinter.CTkLabel(
            entry_frame, text="Descripción:", font=("", 12)
        ).grid(row=0, column=2, padx=(20, 5), pady=15, sticky="e")

        self.descripcion_label = customtkinter.CTkLabel(
            entry_frame,
            text="(introduce código)",
            font=("", 12),
            text_color="gray",
            width=300,
            anchor="w"
        )
        self.descripcion_label.grid(row=0, column=3, padx=5, pady=15, sticky="w")

        # Campo: Unidad
        customtkinter.CTkLabel(
            entry_frame, text="Ud:", font=("", 12)
        ).grid(row=0, column=4, padx=(20, 5), pady=15, sticky="e")

        self.unidad_label = customtkinter.CTkLabel(
            entry_frame, text="-", font=("", 12), width=40
        )
        self.unidad_label.grid(row=0, column=5, padx=5, pady=15, sticky="w")

        # Campo: Cantidad
        customtkinter.CTkLabel(
            entry_frame, text="Cantidad:", font=("", 12, "bold")
        ).grid(row=0, column=6, padx=(20, 5), pady=15, sticky="e")

        self.cantidad_entry = customtkinter.CTkEntry(
            entry_frame, width=100,
            placeholder_text="0.00"
        )
        self.cantidad_entry.grid(row=0, column=7, padx=5, pady=15, sticky="w")

        # Campo: Precio (autocompletado)
        customtkinter.CTkLabel(
            entry_frame, text="Precio:", font=("", 12)
        ).grid(row=0, column=8, padx=(20, 5), pady=15, sticky="e")

        self.precio_label = customtkinter.CTkLabel(
            entry_frame, text="0.00 €", font=("", 12), width=80
        )
        self.precio_label.grid(row=0, column=9, padx=5, pady=15, sticky="w")

        # Botón añadir
        self.add_btn = customtkinter.CTkButton(
            entry_frame, text="+ Añadir", width=90,
            fg_color="#2e7d32", hover_color="#1b5e20",
            command=self._add_item
        )
        self.add_btn.grid(row=0, column=10, padx=(20, 15), pady=15)

    def _create_items_table(self):
        """Crea la tabla de partidas añadidas."""
        table_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        table_frame.grid(row=2, column=0, sticky="nsew", padx=15, pady=(0, 10))
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        # Estilo del TreeView
        style = ttk.Style()
        style.configure(
            "SpeedEntry.Treeview",
            background="#2a2d2e",
            foreground="white",
            fieldbackground="#2a2d2e",
            rowheight=30,
            font=('Segoe UI', 11)
        )
        style.configure(
            "SpeedEntry.Treeview.Heading",
            background="#1f6aa5",
            foreground="white",
            font=('Segoe UI', 11, 'bold')
        )
        style.map("SpeedEntry.Treeview", background=[('selected', '#1f6aa5')])

        # Crear TreeView
        columns = ("codigo", "descripcion", "unidad", "cantidad", "precio", "importe")
        self.items_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="SpeedEntry.Treeview"
        )

        # Configurar columnas
        self.items_tree.heading("codigo", text="Código")
        self.items_tree.heading("descripcion", text="Descripción")
        self.items_tree.heading("unidad", text="Ud")
        self.items_tree.heading("cantidad", text="Cantidad")
        self.items_tree.heading("precio", text="Precio")
        self.items_tree.heading("importe", text="Importe")

        self.items_tree.column("codigo", width=100, anchor="w")
        self.items_tree.column("descripcion", width=350, anchor="w")
        self.items_tree.column("unidad", width=50, anchor="center")
        self.items_tree.column("cantidad", width=80, anchor="e")
        self.items_tree.column("precio", width=80, anchor="e")
        self.items_tree.column("importe", width=100, anchor="e")

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=scrollbar.set)

        self.items_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def _create_footer(self):
        """Crea el pie con total y botones."""
        footer_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="#1a1a2e")
        footer_frame.grid(row=3, column=0, sticky="ew")
        footer_frame.grid_columnconfigure(1, weight=1)

        # Total
        self.total_label = customtkinter.CTkLabel(
            footer_frame,
            text="TOTAL: 0.00 €",
            font=customtkinter.CTkFont(size=18, weight="bold"),
            text_color="#4CAF50"
        )
        self.total_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        # Contador de líneas
        self.count_label = customtkinter.CTkLabel(
            footer_frame,
            text="0 partidas añadidas",
            font=("", 12),
            text_color="gray"
        )
        self.count_label.grid(row=0, column=1, padx=20, pady=15)

        # Botones
        btn_frame = customtkinter.CTkFrame(footer_frame, fg_color="transparent")
        btn_frame.grid(row=0, column=2, padx=20, pady=15, sticky="e")

        customtkinter.CTkButton(
            btn_frame, text="Eliminar seleccionada", width=140,
            fg_color="#c62828", hover_color="#8e0000",
            command=self._delete_selected
        ).pack(side="left", padx=5)

        customtkinter.CTkButton(
            btn_frame, text="Cerrar (Esc)", width=120,
            fg_color="#455a64", hover_color="#37474f",
            command=self._close_window
        ).pack(side="left", padx=5)

    def _setup_bindings(self):
        """Configura los atajos de teclado."""
        # Escape para cerrar
        self.bind("<Escape>", lambda e: self._close_window())

        # Enter en código busca y pasa a cantidad
        self.codigo_entry.bind("<Return>", self._on_codigo_enter)
        self.codigo_entry.bind("<Tab>", self._on_codigo_tab)

        # Autocompletar al escribir código
        self.codigo_entry.bind("<KeyRelease>", self._on_codigo_change)

        # Enter en cantidad añade la línea
        self.cantidad_entry.bind("<Return>", lambda e: self._add_item())

        # Delete para eliminar línea seleccionada
        self.items_tree.bind("<Delete>", lambda e: self._delete_selected())

        # F2 para editar cantidad
        self.items_tree.bind("<F2>", self._edit_selected_cantidad)

    def _on_codigo_change(self, event):
        """Autocompletado al escribir código."""
        codigo = self.codigo_entry.get().strip().upper()

        if codigo in self.catalogo_cache:
            partida = self.catalogo_cache[codigo]
            self.descripcion_label.configure(
                text=partida['resumen'][:50] + "..." if len(partida['resumen']) > 50 else partida['resumen'],
                text_color="white"
            )
            self.unidad_label.configure(text=partida['unidad'])
            self.precio_label.configure(text=f"{partida['precio']:.2f} €")
            self.current_partida = partida
        else:
            self.descripcion_label.configure(text="(código no encontrado)", text_color="orange")
            self.unidad_label.configure(text="-")
            self.precio_label.configure(text="0.00 €")
            self.current_partida = None

    def _on_codigo_enter(self, event):
        """Al pulsar Enter en código, pasa a cantidad."""
        codigo = self.codigo_entry.get().strip().upper()
        if codigo in self.catalogo_cache:
            self.cantidad_entry.focus_set()
            self.cantidad_entry.select_range(0, 'end')
        else:
            # Mostrar sugerencias
            self._show_suggestions(codigo)

    def _on_codigo_tab(self, event):
        """Al pulsar Tab en código, pasa a cantidad."""
        self.cantidad_entry.focus_set()
        self.cantidad_entry.select_range(0, 'end')
        return "break"  # Evitar comportamiento por defecto

    def _show_suggestions(self, partial_code):
        """Muestra sugerencias de códigos similares."""
        if not partial_code:
            return

        suggestions = []
        for codigo, data in self.catalogo_cache.items():
            if partial_code in codigo:
                suggestions.append(f"{codigo} - {data['resumen'][:40]}")
            if len(suggestions) >= 5:
                break

        if suggestions:
            msg = "Sugerencias:\n\n" + "\n".join(suggestions)
            CTkMessagebox(title="Código no encontrado", message=msg, icon="info")

    def _add_item(self):
        """Añade una partida al presupuesto."""
        codigo = self.codigo_entry.get().strip().upper()

        if not hasattr(self, 'current_partida') or not self.current_partida:
            CTkMessagebox(title="Error", message="Código de partida no válido", icon="warning")
            self.codigo_entry.focus_set()
            return

        cantidad_str = self.cantidad_entry.get().strip()
        try:
            cantidad = float(cantidad_str.replace(',', '.'))
            if cantidad <= 0:
                raise ValueError("Cantidad debe ser mayor que 0")
        except:
            CTkMessagebox(title="Error", message="Cantidad no válida", icon="warning")
            self.cantidad_entry.focus_set()
            return

        partida = self.current_partida
        precio = partida['precio']
        importe = cantidad * precio

        # Añadir a la base de datos
        from script.modulo_db import add_part_presupuesto_item
        result = add_part_presupuesto_item(
            self.user, self.password, self.schema,
            self.parte_id, partida['id'], cantidad, precio
        )

        if result == "ok":
            # Añadir a la tabla visual
            self.items_tree.insert("", "end", values=(
                partida['codigo'],
                partida['resumen'][:50],
                partida['unidad'],
                f"{cantidad:.2f}",
                f"{precio:.2f}",
                f"{importe:.2f}"
            ))

            # Guardar en lista de añadidos
            self.items_added.append({
                'codigo': partida['codigo'],
                'cantidad': cantidad,
                'importe': importe
            })

            # Actualizar total
            self._update_total()

            # Limpiar campos y volver a código
            self.codigo_entry.delete(0, 'end')
            self.cantidad_entry.delete(0, 'end')
            self.descripcion_label.configure(text="(introduce código)", text_color="gray")
            self.unidad_label.configure(text="-")
            self.precio_label.configure(text="0.00 €")
            self.current_partida = None
            self.codigo_entry.focus_set()
        else:
            CTkMessagebox(title="Error", message=f"Error al guardar: {result}", icon="cancel")

    def _update_total(self):
        """Actualiza el total y contador."""
        total = sum(item['importe'] for item in self.items_added)
        count = len(self.items_added)

        self.total_label.configure(text=f"TOTAL: {total:,.2f} €")
        self.count_label.configure(text=f"{count} partida{'s' if count != 1 else ''} añadida{'s' if count != 1 else ''}")

    def _delete_selected(self):
        """Elimina la partida seleccionada."""
        selected = self.items_tree.selection()
        if not selected:
            CTkMessagebox(title="Aviso", message="Selecciona una partida para eliminar", icon="info")
            return

        # Por ahora solo eliminamos de la vista (no de BD)
        # Para eliminar de BD necesitaríamos el ID del registro
        item = self.items_tree.item(selected[0])
        codigo = item['values'][0]

        # Confirmar
        msg = CTkMessagebox(
            title="Confirmar",
            message=f"¿Eliminar partida '{codigo}'?",
            icon="question",
            option_1="Cancelar",
            option_2="Eliminar"
        )

        if msg.get() == "Eliminar":
            # Buscar y eliminar del registro local
            for i, added in enumerate(self.items_added):
                if added['codigo'] == codigo:
                    del self.items_added[i]
                    break

            self.items_tree.delete(selected[0])
            self._update_total()

            CTkMessagebox(
                title="Nota",
                message="Partida eliminada de la vista.\nPara eliminarla de la BD, use la ventana de Presupuesto.",
                icon="info"
            )

    def _edit_selected_cantidad(self, event):
        """Permite editar la cantidad de una partida seleccionada."""
        selected = self.items_tree.selection()
        if not selected:
            return

        item = self.items_tree.item(selected[0])
        codigo = item['values'][0]
        cantidad_actual = item['values'][3]

        # Crear ventana de edición simple
        dialog = customtkinter.CTkInputDialog(
            text=f"Nueva cantidad para {codigo}:",
            title="Editar cantidad"
        )
        nueva_cantidad = dialog.get_input()

        if nueva_cantidad:
            try:
                cantidad = float(nueva_cantidad.replace(',', '.'))
                if cantidad <= 0:
                    raise ValueError()

                # Actualizar en la vista
                precio = float(item['values'][4])
                importe = cantidad * precio

                self.items_tree.item(selected[0], values=(
                    item['values'][0],
                    item['values'][1],
                    item['values'][2],
                    f"{cantidad:.2f}",
                    f"{precio:.2f}",
                    f"{importe:.2f}"
                ))

                # Actualizar en lista local
                for added in self.items_added:
                    if added['codigo'] == codigo:
                        added['cantidad'] = cantidad
                        added['importe'] = importe
                        break

                self._update_total()
            except:
                CTkMessagebox(title="Error", message="Cantidad no válida", icon="warning")

    def _close_window(self):
        """Cierra la ventana y ejecuta callback si existe."""
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()
