# interface/parts_interfaz_v2.py
"""
Formulario mejorado para crear partes de trabajo.
Incluye campos de la Fase 1: título, estado, descripciones, fechas, localización, municipio.
"""
import customtkinter
from CTkMessagebox import CTkMessagebox
from tkcalendar import DateEntry
from datetime import date
from script.modulo_db import add_parte_mejorado, get_estados_parte, get_dim_all
from parts_list_window import open_parts_list
import mysql.connector as m

class AppPartsV2(customtkinter.CTk):
    """
    Ventana mejorada para crear partes con todos los campos de Fase 1.
    Layout vertical optimizado para mejor legibilidad.
    """
    def __init__(self, user: str, password: str, default_schema: str = "cert_dev"):
        super().__init__()
        self.title("Generador de Partes - Versión Mejorada")
        self.geometry("620x750")
        self.resizable(False, False)

        self.user = user
        self.password = password
        self.schema = default_schema

        # Variables para guardar los datos de dimensiones
        self.dim_data = {}

        # ====================================================================
        # SECCIÓN: SCHEMA
        # ====================================================================
        frame_schema = customtkinter.CTkFrame(self)
        frame_schema.pack(fill="x", padx=10, pady=5)

        customtkinter.CTkLabel(frame_schema, text="Schema:").pack(side="left", padx=5)
        self.schema_entry = customtkinter.CTkEntry(frame_schema, width=200)
        self.schema_entry.insert(0, self.schema)
        self.schema_entry.pack(side="left", padx=5)

        self.reload_btn = customtkinter.CTkButton(frame_schema, text="Recargar", command=self._reload_dims, width=100)
        self.reload_btn.pack(side="left", padx=5)

        # ====================================================================
        # SECCIÓN: INFORMACIÓN BÁSICA (OBLIGATORIO)
        # ====================================================================
        frame_basic = customtkinter.CTkFrame(self)
        frame_basic.pack(fill="x", padx=10, pady=5)

        customtkinter.CTkLabel(frame_basic, text="** INFORMACIÓN BÁSICA **", font=("Arial", 12, "bold")).pack(pady=5)

        # Título *
        frame_titulo = customtkinter.CTkFrame(frame_basic, fg_color="transparent")
        frame_titulo.pack(fill="x", padx=10, pady=3)
        customtkinter.CTkLabel(frame_titulo, text="Título*:", width=120, anchor="e").pack(side="left")
        self.titulo_entry = customtkinter.CTkEntry(frame_titulo, width=420)
        self.titulo_entry.pack(side="left", padx=5)

        # Estado *
        frame_estado = customtkinter.CTkFrame(frame_basic, fg_color="transparent")
        frame_estado.pack(fill="x", padx=10, pady=3)
        customtkinter.CTkLabel(frame_estado, text="Estado*:", width=120, anchor="e").pack(side="left")
        self.estado_menu = customtkinter.CTkOptionMenu(frame_estado, values=["Cargando..."], width=420)
        self.estado_menu.pack(side="left", padx=5)

        # ====================================================================
        # SECCIÓN: DIMENSIONES (OBLIGATORIO)
        # ====================================================================
        frame_dims = customtkinter.CTkFrame(self)
        frame_dims.pack(fill="x", padx=10, pady=5)

        customtkinter.CTkLabel(frame_dims, text="** DIMENSIONES **", font=("Arial", 12, "bold")).pack(pady=5)

        # Red *
        frame_red = customtkinter.CTkFrame(frame_dims, fg_color="transparent")
        frame_red.pack(fill="x", padx=10, pady=3)
        customtkinter.CTkLabel(frame_red, text="Red*:", width=120, anchor="e").pack(side="left")
        self.red_menu = customtkinter.CTkOptionMenu(frame_red, values=["Cargando..."], width=420)
        self.red_menu.pack(side="left", padx=5)

        # Tipo Trabajo *
        frame_tipo = customtkinter.CTkFrame(frame_dims, fg_color="transparent")
        frame_tipo.pack(fill="x", padx=10, pady=3)
        customtkinter.CTkLabel(frame_tipo, text="Tipo Trabajo*:", width=120, anchor="e").pack(side="left")
        self.tipo_menu = customtkinter.CTkOptionMenu(frame_tipo, values=["Cargando..."], width=420)
        self.tipo_menu.pack(side="left", padx=5)

        # Código Trabajo *
        frame_cod = customtkinter.CTkFrame(frame_dims, fg_color="transparent")
        frame_cod.pack(fill="x", padx=10, pady=3)
        customtkinter.CTkLabel(frame_cod, text="Código Trabajo*:", width=120, anchor="e").pack(side="left")
        self.cod_menu = customtkinter.CTkOptionMenu(frame_cod, values=["Cargando..."], width=420)
        self.cod_menu.pack(side="left", padx=5)

        # Tipo de Reparación (opcional)
        frame_tipo_rep = customtkinter.CTkFrame(frame_dims, fg_color="transparent")
        frame_tipo_rep.pack(fill="x", padx=10, pady=3)
        customtkinter.CTkLabel(frame_tipo_rep, text="Tipo Reparación:", width=120, anchor="e").pack(side="left")
        self.tipo_rep_menu = customtkinter.CTkOptionMenu(frame_tipo_rep, values=["Sin especificar"], width=420)
        self.tipo_rep_menu.pack(side="left", padx=5)

        # ====================================================================
        # SECCIÓN: DESCRIPCIONES (OBLIGATORIO)
        # ====================================================================
        frame_desc = customtkinter.CTkFrame(self)
        frame_desc.pack(fill="x", padx=10, pady=5)

        customtkinter.CTkLabel(frame_desc, text="** DESCRIPCIONES **", font=("Arial", 12, "bold")).pack(pady=5)

        # Descripción *
        frame_descripcion = customtkinter.CTkFrame(frame_desc, fg_color="transparent")
        frame_descripcion.pack(fill="x", padx=10, pady=3)
        customtkinter.CTkLabel(frame_descripcion, text="Descripción*:", width=120, anchor="e").pack(side="left")
        self.descripcion_entry = customtkinter.CTkEntry(frame_descripcion, width=420)
        self.descripcion_entry.pack(side="left", padx=5)

        # Descripción Corta *
        frame_desc_corta = customtkinter.CTkFrame(frame_desc, fg_color="transparent")
        frame_desc_corta.pack(fill="x", padx=10, pady=3)
        customtkinter.CTkLabel(frame_desc_corta, text="Desc. Corta*:", width=120, anchor="e").pack(side="left")
        self.desc_corta_entry = customtkinter.CTkEntry(frame_desc_corta, width=420, placeholder_text="Máx 100 caracteres")
        self.desc_corta_entry.pack(side="left", padx=5)

        # Descripción Larga * (TextBox 3 líneas)
        customtkinter.CTkLabel(frame_desc, text="Descripción Larga*:", anchor="w").pack(fill="x", padx=10, pady=(10,2))
        self.desc_larga_text = customtkinter.CTkTextbox(frame_desc, height=60, width=560)
        self.desc_larga_text.pack(padx=10, pady=2)

        # ====================================================================
        # SECCIÓN: FECHAS (OBLIGATORIO INICIO Y PREVISTA)
        # ====================================================================
        frame_fechas = customtkinter.CTkFrame(self)
        frame_fechas.pack(fill="x", padx=10, pady=5)

        customtkinter.CTkLabel(frame_fechas, text="** FECHAS **", font=("Arial", 12, "bold")).pack(pady=5)

        # Fecha Inicio * (default = hoy)
        frame_inicio = customtkinter.CTkFrame(frame_fechas, fg_color="transparent")
        frame_inicio.pack(fill="x", padx=10, pady=3)
        customtkinter.CTkLabel(frame_inicio, text="Fecha Inicio*:", width=120, anchor="e").pack(side="left")
        self.fecha_inicio_entry = DateEntry(frame_inicio, width=30, date_pattern='dd/mm/yyyy', locale='es_ES')
        self.fecha_inicio_entry.set_date(date.today())
        self.fecha_inicio_entry.pack(side="left", padx=5)

        # Fecha Fin (opcional)
        frame_fin = customtkinter.CTkFrame(frame_fechas, fg_color="transparent")
        frame_fin.pack(fill="x", padx=10, pady=3)
        customtkinter.CTkLabel(frame_fin, text="Fecha Fin:", width=120, anchor="e").pack(side="left")
        self.fecha_fin_entry = DateEntry(frame_fin, width=30, date_pattern='dd/mm/yyyy', locale='es_ES')
        self.fecha_fin_entry.pack(side="left", padx=5)
        # Dejar vacía por defecto
        self.fecha_fin_entry.delete(0, "end")

        # Fecha Prevista Fin *
        frame_prevista = customtkinter.CTkFrame(frame_fechas, fg_color="transparent")
        frame_prevista.pack(fill="x", padx=10, pady=3)
        customtkinter.CTkLabel(frame_prevista, text="Fecha Prevista*:", width=120, anchor="e").pack(side="left")
        self.fecha_prevista_entry = DateEntry(frame_prevista, width=30, date_pattern='dd/mm/yyyy', locale='es_ES')
        self.fecha_prevista_entry.pack(side="left", padx=5)
        # Usuario dijo NO poner valor por defecto
        self.fecha_prevista_entry.delete(0, "end")

        # ====================================================================
        # SECCIÓN: UBICACIÓN (OBLIGATORIO)
        # ====================================================================
        frame_ubicacion = customtkinter.CTkFrame(self)
        frame_ubicacion.pack(fill="x", padx=10, pady=5)

        customtkinter.CTkLabel(frame_ubicacion, text="** UBICACIÓN **", font=("Arial", 12, "bold")).pack(pady=5)

        # Localización *
        customtkinter.CTkLabel(frame_ubicacion, text="Localización*:", anchor="w").pack(fill="x", padx=10, pady=(5,2))
        self.localizacion_entry = customtkinter.CTkEntry(frame_ubicacion, width=560, placeholder_text="Ej: Calle Mayor 123, Edificio A")
        self.localizacion_entry.pack(padx=10, pady=2)

        # Municipio *
        frame_municipio = customtkinter.CTkFrame(frame_ubicacion, fg_color="transparent")
        frame_municipio.pack(fill="x", padx=10, pady=5)
        customtkinter.CTkLabel(frame_municipio, text="Municipio*:", width=120, anchor="e").pack(side="left")
        self.municipio_menu = customtkinter.CTkOptionMenu(frame_municipio, values=["Cargando..."], width=420)
        self.municipio_menu.pack(side="left", padx=5)

        # ====================================================================
        # BOTONES
        # ====================================================================
        self.save_btn = customtkinter.CTkButton(self, text="GUARDAR PARTE", command=self._save_part, height=40, font=("Arial", 14, "bold"))
        self.save_btn.pack(fill="x", padx=20, pady=10)

        self.btn_ver_partes = customtkinter.CTkButton(self, text="Ver listado de partes", command=self._open_parts_list, height=35)
        self.btn_ver_partes.pack(fill="x", padx=20, pady=5)

        # Cargar datos iniciales
        self._reload_dims()

    def _reload_dims(self):
        """Recarga estados, dimensiones y municipios"""
        try:
            self.schema = self.schema_entry.get().strip() or "cert_dev"

            # 1. Cargar estados
            estados = get_estados_parte(self.user, self.password, self.schema)
            if estados:
                estado_values = [f"{e['id']} - {e['nombre']}" for e in estados]
                self.estado_menu.configure(values=estado_values)
                self.estado_menu.set(estado_values[0] if estado_values else "1 - Pendiente")
            else:
                self.estado_menu.configure(values=["1 - Pendiente"])
                self.estado_menu.set("1 - Pendiente")

            # 2. Cargar dimensiones (RED, TIPO, COD, TIPO_REP)
            dims = get_dim_all(self.user, self.password, self.schema)
            self.red_menu.configure(values=dims.get("RED", ["Sin datos"]))
            self.tipo_menu.configure(values=dims.get("TIPO_TRABAJO", ["Sin datos"]))
            self.cod_menu.configure(values=dims.get("COD_TRABAJO", ["Sin datos"]))

            # Tipo de Reparación (opcional, agregar "Sin especificar" como primera opción)
            tipos_rep = dims.get("TIPOS_REP", [])
            tipo_rep_values = ["Sin especificar"] + tipos_rep
            self.tipo_rep_menu.configure(values=tipo_rep_values)
            self.tipo_rep_menu.set("Sin especificar")

            # Preseleccionar primer elemento
            for menu in (self.red_menu, self.tipo_menu, self.cod_menu):
                vals = menu.cget("values")
                if vals and len(vals) > 0:
                    menu.set(vals[0])

            # 3. Cargar municipios
            municipios = self._get_municipios()
            if municipios:
                self.municipio_menu.configure(values=municipios)
                self.municipio_menu.set(municipios[0] if municipios else "Sin datos")
            else:
                self.municipio_menu.configure(values=["Sin municipios"])
                self.municipio_menu.set("Sin municipios")

        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error cargando datos: {e}", icon="warning")

    def _get_municipios(self):
        """Obtiene lista de municipios de tbl_municipios"""
        try:
            from script.db_connection import get_project_connection
            with get_project_connection(self.user, self.password, self.schema) as cn:
                cur = cn.cursor()

                # Detectar qué columna usar para mostrar el municipio
                cur.execute(f"""
                    SELECT COLUMN_NAME
                    FROM information_schema.COLUMNS
                    WHERE TABLE_SCHEMA = '{self.schema}'
                    AND TABLE_NAME = 'tbl_municipios'
                    AND COLUMN_NAME IN ('nombre', 'municipio', 'descripcion', 'NAMEUNIT')
                    ORDER BY FIELD(COLUMN_NAME, 'nombre', 'municipio', 'descripcion', 'NAMEUNIT')
                    LIMIT 1
                """)
                col_result = cur.fetchone()
                col_name = col_result[0] if col_result else 'id'

                # Obtener municipios
                cur.execute(f"SELECT id, {col_name} FROM tbl_municipios ORDER BY {col_name}")
                rows = cur.fetchall()
                cur.close()

                return [f"{row[0]} - {row[1]}" for row in rows]
        except Exception:
            return []

    @staticmethod
    def _take_id(v: str) -> int|None:
        """Extrae ID de string formato 'id - texto'"""
        if not v:
            return None
        try:
            return int(str(v).split(" - ")[0].strip())
        except Exception:
            return None

    def _save_part(self):
        """Guarda el parte con todos los campos nuevos"""
        # Validar campos obligatorios
        titulo = self.titulo_entry.get().strip()
        if not titulo:
            CTkMessagebox(title="Campo obligatorio", message="El Título es obligatorio", icon="warning")
            return

        estado_id = self._take_id(self.estado_menu.get())
        if not estado_id:
            CTkMessagebox(title="Campo obligatorio", message="El Estado es obligatorio", icon="warning")
            return

        red_id = self._take_id(self.red_menu.get())
        tipo_id = self._take_id(self.tipo_menu.get())
        cod_id = self._take_id(self.cod_menu.get())

        if not all([red_id, tipo_id, cod_id]):
            CTkMessagebox(title="Campos obligatorios", message="Debes seleccionar Red, Tipo y Código de Trabajo", icon="warning")
            return

        # Tipo de Reparación es opcional
        tipo_rep_id = None
        tipo_rep_val = self.tipo_rep_menu.get()
        if tipo_rep_val and tipo_rep_val != "Sin especificar":
            tipo_rep_id = self._take_id(tipo_rep_val)

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

        # Fecha fin es opcional
        fecha_fin_str = self.fecha_fin_entry.get() or None

        # Convertir fechas a formato MySQL (YYYY-MM-DD)
        def convert_date(date_str):
            if not date_str:
                return None
            try:
                # Si viene en formato dd/mm/yyyy, convertir
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
            # Usar función mejorada
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
                estado_id=estado_id,
                tipo_rep_id=tipo_rep_id,
                localizacion=localizacion,
                municipio_id=municipio_id
            )

            CTkMessagebox(
                title="Parte guardado",
                message=f"Parte creado exitosamente\n\nCódigo: {codigo}\nID: {new_id}",
                icon="check"
            )

            # Limpiar formulario
            self._clear_form()

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"No se pudo guardar el parte:\n\n{e}",
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

    def _open_parts_list(self):
        """Abre ventana de lista de partes"""
        open_parts_list(self, self.user, self.password, self.schema)
