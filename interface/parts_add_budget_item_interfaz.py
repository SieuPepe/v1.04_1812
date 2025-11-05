# interface/parts_add_budget_item_interfaz.py
import customtkinter
from CTkMessagebox import CTkMessagebox
from script.modulo_db import get_all_bd, get_filter_data_bd, get_id_item_sub_bd, get_id_item_bd, \
    add_part_presupuesto_item
import os

current_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.dirname(current_path)

customtkinter.set_appearance_mode("dark")


class AppPartAddBudgetItem(customtkinter.CTkToplevel):
    def __init__(self, parent, select_data, parte_id):
        super().__init__(parent)

        self.user = select_data[0]
        self.password = select_data[1]
        self.schema = select_data[2]
        self.parte_id = parte_id
        self._after_ids = []  # Lista para guardar IDs de callbacks .after()
        self.current_items = []  # Almacenar datos de partidas actuales

        self.title("Añadir Partida al Presupuesto del Parte")
        self.geometry("900x500")
        self.resizable(False, False)
        self.attributes('-topmost', True)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Frame filtros
        filter_frame = customtkinter.CTkFrame(self, corner_radius=0)
        filter_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
        filter_frame.grid_columnconfigure(1, weight=1)
        filter_frame.grid_columnconfigure(3, weight=1)

        # Capítulo
        customtkinter.CTkLabel(filter_frame, text="Capítulo:",
                               font=("", 13, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="e")

        chapter_items = get_all_bd(self.user, self.password, "tbl_pres_capitulos", self.schema)
        self.chapter_values = [f"{item[1]} - {item[3]}" for item in chapter_items if item[1] != "PA000"]

        self.chapter_option = customtkinter.CTkOptionMenu(
            filter_frame,
            values=self.chapter_values
        )
        self.chapter_option.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Partida
        customtkinter.CTkLabel(filter_frame, text="Partida:",
                               font=("", 13, "bold")).grid(row=0, column=2, padx=10, pady=10, sticky="e")

        self.item_option = customtkinter.CTkOptionMenu(
            filter_frame,
            values=["Seleccione capítulo y presione Filtrar"],
            command=self._on_item_changed
        )
        self.item_option.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        # Botón filtrar
        btn_filter = customtkinter.CTkButton(
            filter_frame, text="🔍 Filtrar",
            command=self._update_items,
            width=100,
            fg_color="#1f6aa5",
            hover_color="#144870"
        )
        btn_filter.grid(row=0, column=4, padx=10, pady=10)

        # Cantidad
        customtkinter.CTkLabel(self, text="Cantidad:",
                               font=("", 14, "bold")).grid(row=1, column=0, padx=20, pady=15, sticky="e")

        self.cantidad_entry = customtkinter.CTkEntry(self, placeholder_text="0.000", width=250)
        self.cantidad_entry.grid(row=1, column=1, padx=20, pady=15, sticky="w")

        # Precio unitario (readonly)
        customtkinter.CTkLabel(self, text="Precio Unitario (€):",
                               font=("", 14, "bold")).grid(row=2, column=0, padx=20, pady=15, sticky="e")

        self.precio_entry = customtkinter.CTkEntry(
            self,
            placeholder_text="0.00",
            width=250,
            state="readonly",
            fg_color="gray20",
            text_color="gray60"
        )
        self.precio_entry.grid(row=2, column=1, padx=20, pady=15, sticky="w")

        # Info sobre precio del catálogo
        self.precio_catalogo_label = customtkinter.CTkLabel(
            self,
            text="",
            font=("", 11),
            text_color="gray"
        )
        self.precio_catalogo_label.grid(row=3, column=0, columnspan=2, pady=5)

        # Info general
        self.info_label = customtkinter.CTkLabel(
            self,
            text="💡 Precio obtenido de la Base de Precios y no puede modificarse",
            font=("", 11),
            text_color="#4CAF50"
        )
        self.info_label.grid(row=4, column=0, columnspan=2, pady=5)

        # Botones
        btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=5, column=0, columnspan=2, pady=30)

        customtkinter.CTkButton(
            btn_frame, text="💾 Guardar", command=self._save,
            fg_color="green", hover_color="#006400", width=180, height=40,
            font=("", 14, "bold")
        ).pack(side="left", padx=10)

        customtkinter.CTkButton(
            btn_frame, text="❌ Cerrar ventana", command=self.destroy,
            fg_color="red", hover_color="#8B0000", width=180, height=40,
            font=("", 14, "bold")
        ).pack(side="left", padx=10)

        self.lift()

    def _update_items(self):
        """Actualiza lista de partidas según capítulo seleccionado"""
        try:
            # Obtener capítulo seleccionado
            chapter = self.chapter_option.get()

            if not chapter or chapter == "Seleccione capítulo":
                CTkMessagebox(title="Aviso", message="Seleccione un capítulo", icon="info")
                return

            print(f"DEBUG - Capítulo seleccionado: {chapter}")

            # Separar código y nombre
            parts = chapter.split(" - ", 1)
            if len(parts) != 2:
                CTkMessagebox(title="Error", message="Formato de capítulo inválido", icon="cancel")
                return

            code_chapter = parts[0].strip()
            name_chapter = parts[1].strip()

            print(f"DEBUG - Código: {code_chapter}, Nombre: {name_chapter}")

            # Obtener ID del capítulo
            id_chapter = get_id_item_sub_bd(
                self.user, self.password, "tbl_pres_capitulos", self.schema,
                "codigo_capitulo", code_chapter, "capitulo", name_chapter
            )

            print(f"DEBUG - ID Capítulo: {id_chapter}")

            # Obtener partidas del capítulo
            items = get_filter_data_bd(
                self.user, self.password, "tbl_pres_precios", self.schema,
                "id_capitulo", str(id_chapter)
            )

            print(f"DEBUG - Partidas encontradas: {len(items)}")

            if items:
                # Guardar datos completos de partidas para uso posterior
                self.current_items = items

                # Crear lista de partidas: "codigo - resumen"
                item_values = []
                for item in items:
                    codigo = item[1]  # codigo
                    resumen = item[4]  # resumen
                    item_values.append(f"{codigo} - {resumen}")

                print(f"DEBUG - Primera partida: {item_values[0] if item_values else 'ninguna'}")

                # Actualizar dropdown
                self.item_option.configure(values=item_values)
                self.item_option.set(item_values[0])

                # Autocompletar precio del catálogo de la primera partida
                precio_catalogo = float(items[0][6])  # coste
                self.precio_entry.configure(state="normal")
                self.precio_entry.delete(0, 'end')
                self.precio_entry.insert(0, f"{precio_catalogo:.2f}")
                self.precio_entry.configure(state="readonly", fg_color="gray20", text_color="gray60")

                self.precio_catalogo_label.configure(
                    text=f"📋 Precio catálogo: {precio_catalogo:.2f}€",
                    text_color="gray"
                )

                CTkMessagebox(
                    title="Éxito",
                    message=f"✅ Se cargaron {len(items)} partidas del capítulo",
                    icon="check"
                )
            else:
                self.item_option.configure(values=["Sin partidas en este capítulo"])
                self.item_option.set("Sin partidas en este capítulo")
                self.precio_entry.configure(state="normal")
                self.precio_entry.delete(0, 'end')
                self.precio_entry.configure(state="readonly", fg_color="gray20", text_color="gray60")
                self.precio_catalogo_label.configure(text="")

                CTkMessagebox(
                    title="Aviso",
                    message=f"No hay partidas en el capítulo seleccionado",
                    icon="info"
                )

        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            print(f"ERROR en _update_items:\n{error_detail}")

            self.item_option.configure(values=["Error cargando partidas"])
            self.item_option.set("Error cargando partidas")

            CTkMessagebox(
                title="Error",
                message=f"Error cargando partidas:\n\n{str(e)}",
                icon="cancel"
            )

    def _on_item_changed(self, selected_item):
        """Actualiza el precio unitario cuando cambia la selección de partida"""
        try:
            if not self.current_items:
                return

            # Extraer código de la partida seleccionada
            codigo_seleccionado = selected_item.split(" - ")[0].strip()

            # Buscar la partida en los datos actuales
            for item in self.current_items:
                codigo = item[1]  # codigo
                if codigo == codigo_seleccionado:
                    precio_catalogo = float(item[6])  # coste

                    # Actualizar precio en el entry (readonly)
                    self.precio_entry.configure(state="normal")
                    self.precio_entry.delete(0, 'end')
                    self.precio_entry.insert(0, f"{precio_catalogo:.2f}")
                    self.precio_entry.configure(state="readonly", fg_color="gray20", text_color="gray60")

                    # Actualizar label informativo
                    self.precio_catalogo_label.configure(
                        text=f"📋 Precio catálogo: {precio_catalogo:.2f}€",
                        text_color="gray"
                    )
                    break

        except Exception as e:
            print(f"Error al actualizar precio: {e}")

    def _save(self):
        """Guarda la partida en el presupuesto del parte"""
        try:
            # Validar campos vacíos
            if not self.cantidad_entry.get().strip():
                CTkMessagebox(title="Error", message="Ingrese la cantidad", icon="warning")
                return

            if not self.precio_entry.get().strip():
                CTkMessagebox(title="Error", message="Ingrese el precio unitario", icon="warning")
                return

            # Obtener partida seleccionada
            item_select = self.item_option.get()

            if item_select in ["Sin partidas en este capítulo", "Error cargando partidas",
                               "Seleccione capítulo y presione Filtrar"]:
                CTkMessagebox(title="Error", message="Seleccione una partida válida", icon="warning")
                return

            # Extraer código de partida
            code_item = item_select.split(" - ")[0].strip()

            print(f"DEBUG - Guardando partida: {code_item}")

            # Obtener ID de la partida usando el código
            precio_id = get_id_item_bd(
                self.user, self.password, "tbl_pres_precios", self.schema,
                "codigo", code_item
            )

            print(f"DEBUG - ID precio: {precio_id}")

            cantidad = float(self.cantidad_entry.get().strip().replace(',', '.'))
            precio_unit = float(self.precio_entry.get().strip().replace(',', '.'))

            # Validar valores positivos
            if cantidad <= 0:
                CTkMessagebox(title="Error", message="La cantidad debe ser mayor a 0", icon="warning")
                return

            if precio_unit <= 0:
                CTkMessagebox(title="Error", message="El precio debe ser mayor a 0", icon="warning")
                return

            print(f"DEBUG - Cantidad: {cantidad}, Precio: {precio_unit}")

            # Guardar
            result = add_part_presupuesto_item(
                self.user, self.password, self.schema,
                self.parte_id, precio_id, cantidad, precio_unit
            )

            print(f"DEBUG - Resultado: {result}")

            if result == "ok":
                total = cantidad * precio_unit
                CTkMessagebox(
                    title="Éxito",
                    message=f"✅ Partida añadida correctamente\n\n"
                            f"Código: {code_item}\n"
                            f"Cantidad: {cantidad:.3f}\n"
                            f"Precio: {precio_unit:.2f}€\n"
                            f"Total: {total:.2f}€",
                    icon="check"
                )
                # Limpiar campo de cantidad para permitir añadir más partidas sin cerrar ventana
                self.cantidad_entry.delete(0, 'end')
                self.cantidad_entry.focus()
            else:
                CTkMessagebox(title="Error", message=f"Error guardando:\n\n{result}", icon="cancel")

        except ValueError as e:
            CTkMessagebox(title="Error", message=f"Cantidad o precio inválido:\n\n{str(e)}", icon="cancel")
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            print(f"ERROR completo en _save:\n{error_detail}")
            CTkMessagebox(title="Error", message=f"Error inesperado:\n\n{str(e)}", icon="cancel")

    def destroy(self):
        """Sobrescribe destroy para cancelar callbacks pendientes antes de destruir"""
        try:
            # Cancelar todos los callbacks pendientes registrados con .after()
            for after_id in getattr(self, '_after_ids', []):
                try:
                    self.after_cancel(after_id)
                except:
                    pass

            # Liberar grab si está activo
            if self.grab_current() == self:
                self.grab_release()

            # Llamar al destroy original
            super().destroy()
        except Exception as e:
            # Si hay error, forzar destrucción
            try:
                super().destroy()
            except:
                pass