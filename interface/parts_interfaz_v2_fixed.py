# interface/parts_interfaz_v2.py
"""
Formulario mejorado para crear partes de trabajo.
Mantiene el estilo visual del formulario original.
"""
import customtkinter
from CTkMessagebox import CTkMessagebox
from tkcalendar import DateEntry
from datetime import date
from script.modulo_db import add_parte_mejorado, get_estados_parte, get_dim_all
from parts_list_window import open_parts_list

class AppPartsV2(customtkinter.CTk):
    """
    Ventana mejorada para crear partes con todos los campos de Fase 1.
    Estilo original mantenido.
    """
    def __init__(self, user: str, password: str, default_schema: str = "cert_dev"):
        super().__init__()
        self.title("Generador de partes")
        self.geometry("900x700")
        self.resizable(False, False)

        self.user = user
        self.password = password
        self.schema = default_schema

        row = 0

        # ====================================================================
        # INFORMACIÓN BÁSICA
        # ====================================================================
        customtkinter.CTkLabel(self, text="Título:").grid(row=row, column=0, padx=10, pady=10, sticky="e")
        self.titulo_entry = customtkinter.CTkEntry(self, width=720)
        self.titulo_entry.grid(row=row, column=1, columnspan=3, padx=5, pady=10, sticky="w")
        row += 1

        customtkinter.CTkLabel(self, text="Estado:").grid(row=row, column=0, padx=10, pady=10, sticky="e")
        self.estado_menu = customtkinter.CTkOptionMenu(self, values=["Cargando..."], width=300)
        self.estado_menu.grid(row=row, column=1, padx=5, pady=10, sticky="w")
        row += 1

        # Código OT (solo lectura, se actualiza dinámicamente)
        customtkinter.CTkLabel(self, text="Código OT:").grid(row=row, column=0, padx=10, pady=10, sticky="e")
        self.codigo_ot_entry = customtkinter.CTkEntry(self, width=200, state="readonly",
                                                       fg_color="gray90", text_color="gray30")
        self.codigo_ot_entry.grid(row=row, column=1, padx=5, pady=10, sticky="w")
        row += 1

        # ====================================================================
        # CARACTERÍSTICAS DEL TRABAJO
        # ====================================================================
        # Fila 1: Red / Tipo trabajo
        customtkinter.CTkLabel(self, text="Red:").grid(row=row, column=0, padx=10, pady=10, sticky="e")
        self.red_menu = customtkinter.CTkOptionMenu(self, values=["(cargando...)"], width=300)
        self.red_menu.grid(row=row, column=1, padx=5, pady=10, sticky="w")

        customtkinter.CTkLabel(self, text="Tipo trabajo:").grid(row=row, column=2, padx=10, pady=10, sticky="e")
        self.tipo_menu = customtkinter.CTkOptionMenu(self, values=["(cargando...)"], width=300,
                                                       command=self._update_codigo_ot)
        self.tipo_menu.grid(row=row, column=3, padx=5, pady=10, sticky="w")
        row += 1

        # Fila 2: Código trabajo
        customtkinter.CTkLabel(self, text="Código trabajo:").grid(row=row, column=0, padx=10, pady=10, sticky="e")
        self.cod_menu = customtkinter.CTkOptionMenu(self, values=["(cargando...)"], width=300)
        self.cod_menu.grid(row=row, column=1, padx=5, pady=10, sticky="w")
        row += 1

        # ====================================================================
        # DESCRIPCIONES
        # ====================================================================
        customtkinter.CTkLabel(self, text="Descripción:").grid(row=row, column=0, padx=10, pady=10, sticky="e")
        self.descripcion_entry = customtkinter.CTkEntry(self, width=720)
        self.descripcion_entry.grid(row=row, column=1, columnspan=3, padx=5, pady=10, sticky="w")
        row += 1

        customtkinter.CTkLabel(self, text="Descripción corta:").grid(row=row, column=0, padx=10, pady=10, sticky="e")
        self.desc_corta_entry = customtkinter.CTkEntry(self, width=720, placeholder_text="Máx 100 caracteres")
        self.desc_corta_entry.grid(row=row, column=1, columnspan=3, padx=5, pady=10, sticky="w")
        row += 1

        customtkinter.CTkLabel(self, text="Descripción larga:").grid(row=row, column=0, padx=10, pady=5, sticky="ne")
        self.desc_larga_text = customtkinter.CTkTextbox(self, height=60, width=720)
        self.desc_larga_text.grid(row=row, column=1, columnspan=3, padx=5, pady=5, sticky="w")
        row += 1

        # ====================================================================
        # FECHAS
        # ====================================================================
        customtkinter.CTkLabel(self, text="Fecha inicio:").grid(row=row, column=0, padx=10, pady=10, sticky="e")
        self.fecha_inicio_entry = DateEntry(self, width=28, date_pattern='dd/mm/yyyy', locale='es_ES')
        self.fecha_inicio_entry.set_date(date.today())
        self.fecha_inicio_entry.grid(row=row, column=1, padx=5, pady=10, sticky="w")

        customtkinter.CTkLabel(self, text="Fecha fin:").grid(row=row, column=2, padx=10, pady=10, sticky="e")
        self.fecha_fin_entry = DateEntry(self, width=28, date_pattern='dd/mm/yyyy', locale='es_ES')
        self.fecha_fin_entry.grid(row=row, column=3, padx=5, pady=10, sticky="w")
        self.fecha_fin_entry.delete(0, "end")  # Vacío por defecto
        row += 1

        customtkinter.CTkLabel(self, text="Fecha prevista:").grid(row=row, column=0, padx=10, pady=10, sticky="e")
        self.fecha_prevista_entry = DateEntry(self, width=28, date_pattern='dd/mm/yyyy', locale='es_ES')
        self.fecha_prevista_entry.grid(row=row, column=1, padx=5, pady=10, sticky="w")
        self.fecha_prevista_entry.delete(0, "end")  # Vacío por defecto
        row += 1

        # ====================================================================
        # UBICACIÓN
        # ====================================================================
        customtkinter.CTkLabel(self, text="Localización:").grid(row=row, column=0, padx=10, pady=10, sticky="e")
        self.localizacion_entry = customtkinter.CTkEntry(self, width=720, placeholder_text="Ej: Calle Mayor 123")
        self.localizacion_entry.grid(row=row, column=1, columnspan=3, padx=5, pady=10, sticky="w")
        row += 1

        customtkinter.CTkLabel(self, text="Municipio:").grid(row=row, column=0, padx=10, pady=10, sticky="e")
        self.municipio_menu = customtkinter.CTkComboBox(self, values=["Cargando..."], width=400, state="normal")
        self.municipio_menu.grid(row=row, column=1, columnspan=2, padx=5, pady=10, sticky="w")
        row += 1

        # ====================================================================
        # BOTONES
        # ====================================================================
        self.save_btn = customtkinter.CTkButton(self, text="Guardar parte", command=self._save_part)
        self.save_btn.grid(row=row, column=0, columnspan=4, padx=20, pady=15, sticky="nsew")

        # Cargar datos iniciales
        self._reload_dims()

        # Actualizar código OT inicial
        self._update_codigo_ot()

    def _reload_dims(self):
        """Recarga estados, dimensiones y municipios."""
        try:
            # 1. Cargar estados
            estados = get_estados_parte(self.user, self.password, self.schema)
            if estados:
                estado_values = [f"{e['id']} - {e['nombre']}" for e in estados]
                self.estado_menu.configure(values=estado_values)
                self.estado_menu.set(estado_values[0] if estado_values else "1 - Pendiente")
            else:
                self.estado_menu.configure(values=["1 - Pendiente"])
                self.estado_menu.set("1 - Pendiente")

            # 2. Cargar dimensiones (RED, TIPO, COD)
            dims = get_dim_all(self.user, self.password, self.schema)
            self.red_menu.configure(values=dims.get("RED", ["(sin datos)"]))
            self.tipo_menu.configure(values=dims.get("TIPO_TRABAJO", ["(sin datos)"]))
            self.cod_menu.configure(values=dims.get("COD_TRABAJO", ["(sin datos)"]))

            # Preseleccionar primer elemento
            for menu in (self.red_menu, self.tipo_menu, self.cod_menu):
                vals = menu.cget("values")
                if vals and len(vals) > 0:
                    menu.set(vals[0])

            # 3. Cargar municipios
            municipios = self._get_municipios()
            if municipios:
                self.municipio_menu.configure(values=municipios)
                self.municipio_menu.set(municipios[0] if municipios else "(sin datos)")
            else:
                self.municipio_menu.configure(values=["(sin datos)"])
                self.municipio_menu.set("(sin datos)")

        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error cargando datos: {e}", icon="warning")

    def _get_municipios(self):
        """Obtiene lista de municipios ordenados alfabéticamente"""
        try:
            from script.db_connection import get_project_connection
            with get_project_connection(self.user, self.password, self.schema) as cn:
                cur = cn.cursor()

                # Detectar columna para mostrar
                cur.execute(f"""
                    SELECT COLUMN_NAME
                    FROM information_schema.COLUMNS
                    WHERE TABLE_SCHEMA = '{self.schema}'
                    AND TABLE_NAME = 'tbl_municipios'
                    AND COLUMN_NAME IN ('nombre', 'municipio', 'descripcion', 'NAMEUNIT', 'CODIGOINE')
                    ORDER BY FIELD(COLUMN_NAME, 'nombre', 'municipio', 'descripcion', 'NAMEUNIT', 'CODIGOINE')
                    LIMIT 1
                """)
                col_result = cur.fetchone()
                col_name = col_result[0] if col_result else 'id'

                cur.execute(f"SELECT id, {col_name} FROM tbl_municipios ORDER BY {col_name}")
                rows = cur.fetchall()
                cur.close()

                return [f"{row[0]} - {row[1]}" for row in rows]
        except Exception as e:
            print(f"Error loading municipios: {e}")
            return []

    @staticmethod
    def _take_id(v: str) -> int|None:
        """Extrae ID de string formato 'id - texto'"""
        if not v or v == "(sin datos)":
            return None
        try:
            return int(str(v).split(" - ")[0].strip())
        except Exception:
            return None

    def _update_codigo_ot(self, *args):
        """Actualiza el código OT preview según el tipo de trabajo seleccionado"""
        try:
            from script.db_partes import _get_tipo_trabajo_prefix
            from script.db_connection import get_project_connection

            tipo_id = self._take_id(self.tipo_menu.get())
            if not tipo_id:
                self.codigo_ot_entry.configure(state="normal")
                self.codigo_ot_entry.delete(0, "end")
                self.codigo_ot_entry.insert(0, "PT-?????")
                self.codigo_ot_entry.configure(state="readonly")
                return

            # Get prefix based on tipo_trabajo
            prefix = _get_tipo_trabajo_prefix(self.user, self.password, self.schema, tipo_id)

            # Get next number for this specific prefix (independent numbering per prefix)
            with get_project_connection(self.user, self.password, self.schema) as cn:
                cur = cn.cursor()
                # Extract the numeric part from existing codes with this prefix
                cur.execute("""
                    SELECT COALESCE(MAX(CAST(SUBSTRING(codigo, LENGTH(%s) + 2) AS UNSIGNED)), 0) + 1
                    FROM tbl_partes
                    WHERE codigo LIKE CONCAT(%s, '-%%')
                """, (prefix, prefix))
                next_id = cur.fetchone()[0]
                cur.close()

            codigo = f"{prefix}-{next_id:05d}"

            # Update readonly entry
            self.codigo_ot_entry.configure(state="normal")
            self.codigo_ot_entry.delete(0, "end")
            self.codigo_ot_entry.insert(0, codigo)
            self.codigo_ot_entry.configure(state="readonly")

        except Exception as e:
            print(f"Error updating código OT: {e}")
            self.codigo_ot_entry.configure(state="normal")
            self.codigo_ot_entry.delete(0, "end")
            self.codigo_ot_entry.insert(0, "Error")
            self.codigo_ot_entry.configure(state="readonly")

    def _save_part(self):
        """Guarda el parte con validación completa"""
        # Validar campos obligatorios
        titulo = self.titulo_entry.get().strip()
        if not titulo:
            CTkMessagebox(title="Campo obligatorio", message="El Título es obligatorio", icon="warning")
            return

        estado_id = self._take_id(self.estado_menu.get())
        estado_nombre = self.estado_menu.get().split(" - ")[1] if " - " in self.estado_menu.get() else ""

        if not estado_id:
            CTkMessagebox(title="Campo obligatorio", message="El Estado es obligatorio", icon="warning")
            return

        red_id = self._take_id(self.red_menu.get())
        tipo_id = self._take_id(self.tipo_menu.get())
        cod_id = self._take_id(self.cod_menu.get())

        if not all([red_id, tipo_id, cod_id]):
            CTkMessagebox(title="Campos obligatorios", message="Selecciona Red, Tipo y Código de Trabajo", icon="warning")
            return

        descripcion = self.descripcion_entry.get().strip()
        if not descripcion:
            CTkMessagebox(title="Campo obligatorio", message="La Descripción es obligatoria", icon="warning")
            return

        desc_corta = self.desc_corta_entry.get().strip()
        if not desc_corta:
            CTkMessagebox(title="Campo obligatorio", message="La Descripción Corta es obligatoria", icon="warning")
            return

        desc_larga = self.desc_larga_text.get("1.0", "end-1c").strip()
        if not desc_larga:
            CTkMessagebox(title="Campo obligatorio", message="La Descripción Larga es obligatoria", icon="warning")
            return

        fecha_inicio_str = self.fecha_inicio_entry.get()
        if not fecha_inicio_str:
            CTkMessagebox(title="Campo obligatorio", message="La Fecha de Inicio es obligatoria", icon="warning")
            return

        fecha_prevista_str = self.fecha_prevista_entry.get()
        if not fecha_prevista_str:
            CTkMessagebox(title="Campo obligatorio", message="La Fecha Prevista es obligatoria", icon="warning")
            return

        localizacion = self.localizacion_entry.get().strip()
        if not localizacion:
            CTkMessagebox(title="Campo obligatorio", message="La Localización es obligatoria", icon="warning")
            return

        municipio_id = self._take_id(self.municipio_menu.get())
        if not municipio_id:
            CTkMessagebox(title="Campo obligatorio", message="El Municipio es obligatorio", icon="warning")
            return

        # VALIDACIÓN ESPECIAL: Si estado es "Finalizada", Fecha Fin es obligatoria
        fecha_fin_str = self.fecha_fin_entry.get()
        if estado_nombre.lower() == "finalizada" and not fecha_fin_str:
            CTkMessagebox(
                title="Campo obligatorio",
                message="Si el estado es 'Finalizada', debes indicar la Fecha de Fin",
                icon="warning"
            )
            return

        # Convertir fechas a formato MySQL
        def convert_date(date_str):
            if not date_str:
                return None
            try:
                parts = date_str.split('/')
                if len(parts) == 3:
                    return f"{parts[2]}-{parts[1]}-{parts[0]}"
                return date_str
            except:
                return date_str

        fecha_inicio = convert_date(fecha_inicio_str)
        fecha_fin = convert_date(fecha_fin_str) if fecha_fin_str else None
        fecha_prevista = convert_date(fecha_prevista_str)

        try:
            new_id, codigo = add_parte_mejorado(
                self.user, self.password, self.schema,
                red_id, tipo_id, cod_id,
                titulo=titulo,
                descripcion=descripcion,
                descripcion_larga=desc_larga,
                descripcion_corta=desc_corta,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                fecha_prevista_fin=fecha_prevista,
                id_estado=estado_id,
                localizacion=localizacion,
                id_municipio=municipio_id
            )

            CTkMessagebox(
                title="Parte guardado",
                message=f"Parte creado con código {codigo}",
                icon="check"
            )

            # Limpiar formulario
            self._clear_form()

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"No se pudo guardar el parte:\n{e}",
                icon="cancel"
            )

    def _clear_form(self):
        """Limpia el formulario después de guardar"""
        self.titulo_entry.delete(0, "end")
        self.descripcion_entry.delete(0, "end")
        self.desc_corta_entry.delete(0, "end")
        self.desc_larga_text.delete("1.0", "end")
        self.fecha_inicio_entry.set_date(date.today())
        self.fecha_fin_entry.delete(0, "end")
        self.fecha_prevista_entry.delete(0, "end")
        self.localizacion_entry.delete(0, "end")
        # Recargar mantiene OT preseleccionada
        self._reload_dims()

    def _open_parts_list(self):
        """Abre ventana de lista de partes"""
        open_parts_list(self, self.user, self.password, self.schema)
