#!/usr/bin/env python3
"""
Ventana de prueba para comparar opciones de dropdown con filtrado.
Ejecutar: python test_dropdown_options.py
"""
import customtkinter

customtkinter.set_appearance_mode("dark")


class TestDropdownOptions(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Comparación de Opciones de Dropdown con Filtrado")
        self.geometry("1200x700")

        # Datos de prueba
        self.test_data = [
            "001 - Tubería PVC 110mm presión",
            "002 - Tubería PVC 160mm presión",
            "003 - Tubería PVC 200mm presión",
            "004 - Tubería polietileno 32mm",
            "005 - Tubería polietileno 50mm",
            "006 - Válvula compuerta DN100",
            "007 - Válvula compuerta DN150",
            "008 - Válvula mariposa DN200",
            "009 - Codo 90° PVC 110mm",
            "010 - Codo 45° PVC 110mm",
            "011 - Te PVC 110mm",
            "012 - Reducción PVC 160-110mm",
            "013 - Hidrante DN80",
            "014 - Hidrante DN100",
            "015 - Arqueta de registro 40x40",
            "016 - Arqueta de registro 60x60",
            "017 - Tapa fundición D400",
            "018 - Contador DN20",
            "019 - Contador DN25",
            "020 - Acometida domiciliaria completa",
        ]

        # Título
        title = customtkinter.CTkLabel(
            self,
            text="Comparación de Opciones de Dropdown con Filtrado",
            font=("", 20, "bold")
        )
        title.pack(pady=20)

        # Frame principal con 3 columnas
        main_frame = customtkinter.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        main_frame.grid_columnconfigure((0, 1, 2), weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        # ========== OPCIÓN A: Entry + Botón ▼ + Toplevel ==========
        self._create_option_a(main_frame, 0)

        # ========== OPCIÓN B: Entry que despliega al clic ==========
        self._create_option_b(main_frame, 1)

        # ========== OPCIÓN C: CTkComboBox nativo ==========
        self._create_option_c(main_frame, 2)

        # Resultado seleccionado
        result_frame = customtkinter.CTkFrame(self)
        result_frame.pack(fill="x", padx=20, pady=20)

        customtkinter.CTkLabel(
            result_frame,
            text="Selección actual:",
            font=("", 14, "bold")
        ).pack(side="left", padx=10)

        self.result_label = customtkinter.CTkLabel(
            result_frame,
            text="(ninguna)",
            font=("", 14)
        )
        self.result_label.pack(side="left", padx=10)

    def _create_option_a(self, parent, col):
        """OPCIÓN A: Entry + Botón ▼ + Toplevel flotante"""
        frame = customtkinter.CTkFrame(parent)
        frame.grid(row=0, column=col, padx=10, pady=10, sticky="nsew", rowspan=2)
        frame.grid_columnconfigure(0, weight=1)

        # Título
        customtkinter.CTkLabel(
            frame,
            text="OPCIÓN A",
            font=("", 16, "bold"),
            text_color="#4CAF50"
        ).pack(pady=(10, 5))

        customtkinter.CTkLabel(
            frame,
            text="Entry + Botón ▼ + Toplevel",
            font=("", 12)
        ).pack(pady=(0, 10))

        # Descripción
        desc = customtkinter.CTkLabel(
            frame,
            text="• Escribir filtra opciones\n• Botón ▼ muestra todas\n• Dropdown flota (Toplevel)",
            font=("", 11),
            justify="left"
        )
        desc.pack(pady=5)

        # Widget
        widget_frame = customtkinter.CTkFrame(frame, fg_color="transparent")
        widget_frame.pack(fill="x", padx=20, pady=20)
        widget_frame.grid_columnconfigure(0, weight=1)

        # Entry + Botón en la misma fila
        entry_frame = customtkinter.CTkFrame(widget_frame, fg_color="transparent")
        entry_frame.pack(fill="x")
        entry_frame.grid_columnconfigure(0, weight=1)

        self.entry_a = customtkinter.CTkEntry(
            entry_frame,
            placeholder_text="Escriba para buscar..."
        )
        self.entry_a.grid(row=0, column=0, sticky="ew")
        self.entry_a.bind('<KeyRelease>', self._filter_option_a)
        self.entry_a.bind('<Return>', lambda e: self._select_first_a())

        self.btn_dropdown_a = customtkinter.CTkButton(
            entry_frame,
            text="▼",
            width=40,
            command=self._toggle_dropdown_a
        )
        self.btn_dropdown_a.grid(row=0, column=1, padx=(5, 0))

        # Variables
        self.selected_a = None
        self.dropdown_a = None  # Toplevel
        self.dropdown_a_visible = False

    def _toggle_dropdown_a(self):
        """Muestra/oculta el dropdown de la opción A"""
        if self.dropdown_a_visible:
            self._hide_dropdown_a()
        else:
            self._show_dropdown_a()

    def _show_dropdown_a(self, filtered=None):
        """Muestra el dropdown como Toplevel"""
        if self.dropdown_a:
            self.dropdown_a.destroy()

        # Obtener posición del entry
        x = self.entry_a.winfo_rootx()
        y = self.entry_a.winfo_rooty() + self.entry_a.winfo_height()
        width = self.entry_a.winfo_width() + 45

        # Crear Toplevel
        self.dropdown_a = customtkinter.CTkToplevel(self)
        self.dropdown_a.withdraw()  # Ocultar mientras se configura
        self.dropdown_a.overrideredirect(True)  # Sin bordes de ventana
        self.dropdown_a.geometry(f"{width}x250+{x}+{y}")

        # Frame con scroll
        scroll_frame = customtkinter.CTkScrollableFrame(
            self.dropdown_a,
            fg_color="#2b2b2b"
        )
        scroll_frame.pack(fill="both", expand=True)

        # Opciones a mostrar
        items = filtered if filtered else self.test_data

        for item in items[:15]:  # Máximo 15
            btn = customtkinter.CTkButton(
                scroll_frame,
                text=item,
                anchor="w",
                fg_color="transparent",
                hover_color="#1f6aa5",
                command=lambda i=item: self._select_option_a(i)
            )
            btn.pack(fill="x", padx=2, pady=1)

        if len(items) > 15:
            customtkinter.CTkLabel(
                scroll_frame,
                text=f"... y {len(items) - 15} más",
                text_color="gray"
            ).pack(pady=5)

        self.dropdown_a.deiconify()  # Mostrar
        self.dropdown_a_visible = True

        # Cerrar al hacer clic fuera
        self.dropdown_a.bind('<FocusOut>', lambda e: self._hide_dropdown_a())

    def _hide_dropdown_a(self):
        """Oculta el dropdown"""
        if self.dropdown_a:
            self.dropdown_a.destroy()
            self.dropdown_a = None
        self.dropdown_a_visible = False

    def _filter_option_a(self, event=None):
        """Filtra opciones mientras se escribe"""
        text = self.entry_a.get().lower()
        if text:
            filtered = [i for i in self.test_data if text in i.lower()]
            if filtered:
                self._show_dropdown_a(filtered)
            else:
                self._hide_dropdown_a()
        else:
            self._hide_dropdown_a()

    def _select_first_a(self):
        """Selecciona el primer resultado con Enter"""
        text = self.entry_a.get().lower()
        if text:
            filtered = [i for i in self.test_data if text in i.lower()]
            if filtered:
                self._select_option_a(filtered[0])

    def _select_option_a(self, item):
        """Selecciona una opción"""
        self.selected_a = item
        self.entry_a.delete(0, 'end')
        self.entry_a.insert(0, item)
        self._hide_dropdown_a()
        self.result_label.configure(text=f"Opción A: {item}")

    def _create_option_b(self, parent, col):
        """OPCIÓN B: Entry que despliega al hacer clic"""
        frame = customtkinter.CTkFrame(parent)
        frame.grid(row=0, column=col, padx=10, pady=10, sticky="nsew", rowspan=2)
        frame.grid_columnconfigure(0, weight=1)

        # Título
        customtkinter.CTkLabel(
            frame,
            text="OPCIÓN B",
            font=("", 16, "bold"),
            text_color="#2196F3"
        ).pack(pady=(10, 5))

        customtkinter.CTkLabel(
            frame,
            text="Entry con clic + Toplevel",
            font=("", 12)
        ).pack(pady=(0, 10))

        # Descripción
        desc = customtkinter.CTkLabel(
            frame,
            text="• Clic en entry despliega\n• Escribir filtra opciones\n• Icono ▼ decorativo",
            font=("", 11),
            justify="left"
        )
        desc.pack(pady=5)

        # Widget
        widget_frame = customtkinter.CTkFrame(frame, fg_color="transparent")
        widget_frame.pack(fill="x", padx=20, pady=20)

        # Entry con icono integrado (simulado con frame)
        entry_container = customtkinter.CTkFrame(widget_frame, fg_color="#343638", corner_radius=6)
        entry_container.pack(fill="x")
        entry_container.grid_columnconfigure(0, weight=1)

        self.entry_b = customtkinter.CTkEntry(
            entry_container,
            placeholder_text="Clic o escriba para buscar...",
            border_width=0,
            fg_color="transparent"
        )
        self.entry_b.grid(row=0, column=0, sticky="ew", padx=(5, 0))
        self.entry_b.bind('<KeyRelease>', self._filter_option_b)
        self.entry_b.bind('<Button-1>', lambda e: self._show_dropdown_b())
        self.entry_b.bind('<Return>', lambda e: self._select_first_b())

        # Icono ▼ (label clickeable)
        self.icon_b = customtkinter.CTkLabel(
            entry_container,
            text="▼",
            width=30,
            cursor="hand2"
        )
        self.icon_b.grid(row=0, column=1, padx=(0, 5))
        self.icon_b.bind('<Button-1>', lambda e: self._show_dropdown_b())

        # Variables
        self.selected_b = None
        self.dropdown_b = None
        self.dropdown_b_visible = False

    def _show_dropdown_b(self, filtered=None):
        """Muestra dropdown para opción B"""
        if self.dropdown_b:
            self.dropdown_b.destroy()

        x = self.entry_b.winfo_rootx()
        y = self.entry_b.winfo_rooty() + self.entry_b.winfo_height() + 5
        width = self.entry_b.winfo_width() + 35

        self.dropdown_b = customtkinter.CTkToplevel(self)
        self.dropdown_b.withdraw()
        self.dropdown_b.overrideredirect(True)
        self.dropdown_b.geometry(f"{width}x250+{x}+{y}")

        scroll_frame = customtkinter.CTkScrollableFrame(
            self.dropdown_b,
            fg_color="#2b2b2b"
        )
        scroll_frame.pack(fill="both", expand=True)

        items = filtered if filtered else self.test_data

        for item in items[:15]:
            btn = customtkinter.CTkButton(
                scroll_frame,
                text=item,
                anchor="w",
                fg_color="transparent",
                hover_color="#1f6aa5",
                command=lambda i=item: self._select_option_b(i)
            )
            btn.pack(fill="x", padx=2, pady=1)

        if len(items) > 15:
            customtkinter.CTkLabel(
                scroll_frame,
                text=f"... y {len(items) - 15} más",
                text_color="gray"
            ).pack(pady=5)

        self.dropdown_b.deiconify()
        self.dropdown_b_visible = True

    def _hide_dropdown_b(self):
        if self.dropdown_b:
            self.dropdown_b.destroy()
            self.dropdown_b = None
        self.dropdown_b_visible = False

    def _filter_option_b(self, event=None):
        text = self.entry_b.get().lower()
        if text:
            filtered = [i for i in self.test_data if text in i.lower()]
            if filtered:
                self._show_dropdown_b(filtered)
            else:
                self._hide_dropdown_b()
        else:
            self._show_dropdown_b()  # Mostrar todas si está vacío

    def _select_first_b(self):
        text = self.entry_b.get().lower()
        if text:
            filtered = [i for i in self.test_data if text in i.lower()]
            if filtered:
                self._select_option_b(filtered[0])
        elif self.test_data:
            self._select_option_b(self.test_data[0])

    def _select_option_b(self, item):
        self.selected_b = item
        self.entry_b.delete(0, 'end')
        self.entry_b.insert(0, item)
        self._hide_dropdown_b()
        self.result_label.configure(text=f"Opción B: {item}")

    def _create_option_c(self, parent, col):
        """OPCIÓN C: CTkComboBox nativo (limitado)"""
        frame = customtkinter.CTkFrame(parent)
        frame.grid(row=0, column=col, padx=10, pady=10, sticky="nsew", rowspan=2)
        frame.grid_columnconfigure(0, weight=1)

        # Título
        customtkinter.CTkLabel(
            frame,
            text="OPCIÓN C",
            font=("", 16, "bold"),
            text_color="#FF9800"
        ).pack(pady=(10, 5))

        customtkinter.CTkLabel(
            frame,
            text="CTkComboBox nativo",
            font=("", 12)
        ).pack(pady=(0, 10))

        # Descripción
        desc = customtkinter.CTkLabel(
            frame,
            text="• Comportamiento nativo\n• Sin filtrado al escribir\n• Dropdown estándar",
            font=("", 11),
            justify="left"
        )
        desc.pack(pady=5)

        # Widget
        widget_frame = customtkinter.CTkFrame(frame, fg_color="transparent")
        widget_frame.pack(fill="x", padx=20, pady=20)

        self.combo_c = customtkinter.CTkComboBox(
            widget_frame,
            values=self.test_data,
            command=self._on_combo_c_select
        )
        self.combo_c.pack(fill="x")
        self.combo_c.set("Seleccione una opción...")

        # Nota
        customtkinter.CTkLabel(
            frame,
            text="⚠️ No permite filtrar\nmientras escribes",
            font=("", 10),
            text_color="orange"
        ).pack(pady=10)

    def _on_combo_c_select(self, item):
        self.result_label.configure(text=f"Opción C: {item}")


if __name__ == "__main__":
    app = TestDropdownOptions()
    app.mainloop()
