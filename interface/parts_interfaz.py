# interface/parts_interfaz.py
"""
⚠️ ARCHIVO OBSOLETO - LEGACY CODE ⚠️

Esta es la versión original y simplificada del formulario de partes.
Solo permite crear partes básicos con campos mínimos (RED, TIPO, CÓDIGO, DESCRIPCIÓN).

NO INCLUYE:
- Campos FASE 1 (título, descripciones largas/cortas, fechas, estado, localización, municipio)
- Campos adicionales (trabajadores, GPS)

USO RECOMENDADO:
Para crear partes completos con todos los campos, usa:
- interface/parts_interfaz_v2_fixed.py (AppPartsV2)

Este archivo se mantiene solo para compatibilidad con código legacy.
Considerar eliminarlo en futuras versiones.
"""
import customtkinter
from CTkMessagebox import CTkMessagebox
from script.modulo_db import add_parte_with_code, get_dim_all
import mysql.connector as m

class AppParts(customtkinter.CTk):
    """
    Ventana mínima para crear partes en cert_dev.
    Selecciona RED, TIPO_TRABAJO y COD_TRABAJO y hace INSERT en tbl_partes.
    El código de OT/Parte se genera automáticamente (PT-00001).

    ⚠️ OBSOLETO: Usa AppPartsV2 de parts_interfaz_v2_fixed.py en su lugar.
    """
    def __init__(self, user: str, password: str, default_schema: str = "cert_dev"):
        super().__init__()
        self.title("Generador de partes")
        self.geometry("820x380")
        self.resizable(False, False)

        self.user = user
        self.password = password
        self.schema = default_schema  # de momento fijo, editable en un Entry

        # Cabecera
        customtkinter.CTkLabel(self, text="Generador de partes (schema) →").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.schema_entry = customtkinter.CTkEntry(self, width=180)
        self.schema_entry.insert(0, self.schema)
        self.schema_entry.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        self.reload_btn = customtkinter.CTkButton(self, text="Recargar listas", command=self._reload_dims)
        self.reload_btn.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        # Código OT (solo lectura, se actualiza dinámicamente)
        customtkinter.CTkLabel(self, text="Código OT:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.codigo_ot_entry = customtkinter.CTkEntry(self, width=200, state="readonly",
                                                       fg_color="gray90", text_color="gray30")
        self.codigo_ot_entry.grid(row=1, column=1, padx=5, pady=10, sticky="w")

        # Fila 2: RED / TIPO
        customtkinter.CTkLabel(self, text="Red:").grid(row=2, column=0, padx=10, pady=15, sticky="e")
        self.red_menu = customtkinter.CTkOptionMenu(self, values=["(cargando...)"])
        self.red_menu.grid(row=2, column=1, padx=5, pady=15, sticky="w")

        customtkinter.CTkLabel(self, text="Tipo trabajo:").grid(row=2, column=2, padx=10, pady=15, sticky="e")
        self.tipo_menu = customtkinter.CTkOptionMenu(self, values=["(cargando...)"], command=self._update_codigo_ot)
        self.tipo_menu.grid(row=2, column=3, padx=5, pady=15, sticky="w")

        # Fila 3: Código trabajo
        customtkinter.CTkLabel(self, text="Código trabajo:").grid(row=3, column=0, padx=10, pady=15, sticky="e")
        self.cod_menu = customtkinter.CTkOptionMenu(self, values=["(cargando...)"])
        self.cod_menu.grid(row=3, column=1, padx=5, pady=15, sticky="w")

        # Descripción opcional
        customtkinter.CTkLabel(self, text="Descripción (opcional):").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.desc_entry = customtkinter.CTkEntry(self, width=540)
        self.desc_entry.grid(row=4, column=1, columnspan=3, padx=5, pady=10, sticky="w")

        # Botón guardar
        self.save_btn = customtkinter.CTkButton(self, text="Guardar parte", command=self._save_part)
        self.save_btn.grid(row=5, column=0, columnspan=4, padx=20, pady=25, sticky="nsew")

        # Cargar por primera vez
        self._reload_dims()

        # Actualizar código OT inicial
        self._update_codigo_ot()

    def _reload_dims(self):
        try:
            self.schema = self.schema_entry.get().strip() or "cert_dev"
            dims = get_dim_all(self.user, self.password, self.schema)
            # Esperamos claves: 'RED', 'TIPO_TRABAJO', 'COD_TRABAJO' devolviendo textos "id - nombre"
            self.red_menu.configure(values=dims.get("RED", ["(sin datos)"]))
            self.tipo_menu.configure(values=dims.get("TIPO_TRABAJO", ["(sin datos)"]))
            self.cod_menu.configure(values=dims.get("COD_TRABAJO", ["(sin datos)"]))

            # Preseleccionar primer elemento
            for w in (self.red_menu, self.tipo_menu, self.cod_menu):
                vals = w.cget("values")
                if vals and len(vals) > 0:
                    w.set(vals[0])
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error cargando listas: {e}", icon="warning")

    @staticmethod
    def _take_id(v: str) -> int|None:
        # Menús muestran "id - texto". Tomamos la parte izquierda.
        if not v:
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
                # Más robusto: maneja NULLs y códigos vacíos
                cur.execute("""
                    SELECT COALESCE(
                        MAX(
                            CAST(
                                REPLACE(codigo, %s, '') AS UNSIGNED
                            )
                        ),
                        0
                    ) + 1
                    FROM tbl_partes
                    WHERE codigo IS NOT NULL
                      AND codigo LIKE %s
                """, (prefix + '-', prefix + '-%'))
                next_id = int(cur.fetchone()[0])  # Convertir a int para evitar ValueError con Decimal
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
        red_id = self._take_id(self.red_menu.get())
        tipo_id = self._take_id(self.tipo_menu.get())
        cod_id = self._take_id(self.cod_menu.get())
        descripcion = self.desc_entry.get().strip() or None

        if not all([red_id, tipo_id, cod_id]):
            CTkMessagebox(title="Aviso", message="Selecciona Red, Tipo y Código de trabajo.", icon="info")
            return

        try:
            new_id, codigo = add_parte_with_code(self.user, self.password, self.schema,
                                                 red_id, tipo_id, cod_id, descripcion)

            CTkMessagebox(title="Parte guardado",
                          message=f"Parte creado con código {codigo}",
                          icon="check")
        except Exception as e:
            CTkMessagebox(title="Error",
                          message=f"No se pudo guardar el parte:\n{e}",
                          icon="cancel")
