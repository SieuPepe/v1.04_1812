# interface/parts_interfaz.py
import customtkinter
from CTkMessagebox import CTkMessagebox
from script.modulo_db import add_parte_with_code
from parts_list_window import open_parts_list
import mysql.connector as m

# Usamos la utilidad que ya probaste para traer las tres dimensiones
from script.modulo_db import get_dim_all

class AppParts(customtkinter.CTk):
    """
    Ventana mínima para crear partes en cert_dev.
    Selecciona RED, TIPO_TRABAJO y COD_TRABAJO y hace INSERT en tbl_partes.
    El código de OT/Parte se genera automáticamente (PT-00001).
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

        # Fila 1: RED / TIPO
        customtkinter.CTkLabel(self, text="Red:").grid(row=1, column=0, padx=10, pady=15, sticky="e")
        self.red_menu = customtkinter.CTkOptionMenu(self, values=["(cargando...)"])
        self.red_menu.grid(row=1, column=1, padx=5, pady=15, sticky="w")

        customtkinter.CTkLabel(self, text="Tipo trabajo:").grid(row=1, column=2, padx=10, pady=15, sticky="e")
        self.tipo_menu = customtkinter.CTkOptionMenu(self, values=["(cargando...)"])
        self.tipo_menu.grid(row=1, column=3, padx=5, pady=15, sticky="w")

        # Fila 2: Código trabajo
        customtkinter.CTkLabel(self, text="Código trabajo:").grid(row=2, column=0, padx=10, pady=15, sticky="e")
        self.cod_menu = customtkinter.CTkOptionMenu(self, values=["(cargando...)"])
        self.cod_menu.grid(row=2, column=1, padx=5, pady=15, sticky="w")

        # Descripción opcional
        customtkinter.CTkLabel(self, text="Descripción (opcional):").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.desc_entry = customtkinter.CTkEntry(self, width=540)
        self.desc_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=10, sticky="w")

        # Botón guardar
        self.save_btn = customtkinter.CTkButton(self, text="Guardar parte", command=self._save_part)
        self.save_btn.grid(row=4, column=0, columnspan=4, padx=20, pady=25, sticky="nsew")

        # Botón para ver listado de partes
        self.btn_ver_partes = customtkinter.CTkButton(
            self,
            text="Ver listado de partes",
            command=self._open_parts_list
        )
        self.btn_ver_partes.grid(row=5, column=0, columnspan=4, padx=20, pady=10, sticky="ew")

        # Cargar por primera vez
        self._reload_dims()



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

    def _open_parts_list(self):
        # Asumo que la clase ya guarda estas credenciales en self.user, self.password, self.schema
        open_parts_list(self, self.user, self.password, self.schema)
