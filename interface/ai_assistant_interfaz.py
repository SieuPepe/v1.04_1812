"""
Interfaz de chat para el Asistente de IA de HydroFlow Manager.

Ventana de chat interactivo que permite consultar dudas,
analizar codigo y realizar consultas a la base de datos.
"""

import customtkinter
from tkinter import messagebox
import threading
from typing import Optional


class AIAssistantWindow(customtkinter.CTkToplevel):
    """Ventana de chat del asistente de IA."""

    def __init__(self, parent, user: str, password: str, schema: str):
        super().__init__(parent)

        self.user = user
        self.password = password
        self.schema = schema
        self.parent = parent
        self.assistant = None
        self.is_processing = False

        # Configuracion de ventana
        self.title("Asistente IA - HydroFlow Manager")
        self.geometry("700x600")
        self.minsize(600, 500)

        # Hacer modal (pero no bloquear eventos)
        self.transient(parent)
        # self.grab_set()  # Desactivado temporalmente para debug

        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Crear interfaz
        self._create_header()
        self._create_chat_area()
        self._create_input_area()
        self._create_status_bar()

        # Verificar requisitos despues de mostrar ventana
        self.after(500, self._check_requirements)

        # Forzar actualizacion de ventana
        self.update()

    def _create_header(self):
        """Crea el encabezado con titulo y selector de modelo."""
        header = customtkinter.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        # Titulo
        title = customtkinter.CTkLabel(
            header,
            text="Asistente IA",
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w")

        # Frame para selector de modelo
        model_frame = customtkinter.CTkFrame(header, fg_color="transparent")
        model_frame.grid(row=0, column=1, sticky="e")

        customtkinter.CTkLabel(
            model_frame,
            text="Modelo:",
            font=customtkinter.CTkFont(size=12)
        ).pack(side="left", padx=(0, 5))

        self.model_selector = customtkinter.CTkOptionMenu(
            model_frame,
            values=["Cargando..."],
            width=180,
            command=self._on_model_change
        )
        self.model_selector.pack(side="left")

        # Boton actualizar modelos
        self.btn_refresh = customtkinter.CTkButton(
            model_frame,
            text="↻",
            width=30,
            command=self._refresh_models
        )
        self.btn_refresh.pack(side="left", padx=(5, 0))

    def _create_chat_area(self):
        """Crea el area de historial de chat."""
        # Frame contenedor
        chat_frame = customtkinter.CTkFrame(self)
        chat_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="nsew")
        chat_frame.grid_columnconfigure(0, weight=1)
        chat_frame.grid_rowconfigure(0, weight=1)

        # Area de texto scrollable para el historial
        self.chat_display = customtkinter.CTkTextbox(
            chat_frame,
            wrap="word",
            font=customtkinter.CTkFont(size=13),
            state="disabled"
        )
        self.chat_display.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Configurar tags para estilos
        self.chat_display._textbox.tag_configure("user", foreground="#4da6ff")
        self.chat_display._textbox.tag_configure("assistant", foreground="#90EE90")
        self.chat_display._textbox.tag_configure("system", foreground="#FFD700")
        self.chat_display._textbox.tag_configure("error", foreground="#FF6B6B")

        # Mensaje inicial
        self._add_system_message(
            "Bienvenido al Asistente IA de HydroFlow Manager.\n"
            "Puedo ayudarte con:\n"
            "  - Dudas sobre el uso de la aplicacion\n"
            "  - Consultas sobre la base de datos\n"
            "  - Explicaciones del codigo fuente\n\n"
            "Escribe tu pregunta abajo para comenzar."
        )

    def _create_input_area(self):
        """Crea el area de entrada de texto."""
        input_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        input_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)

        # Campo de entrada
        self.input_entry = customtkinter.CTkEntry(
            input_frame,
            placeholder_text="Escribe tu pregunta aqui...",
            height=40,
            font=customtkinter.CTkFont(size=13)
        )
        self.input_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.input_entry.bind("<Return>", lambda e: self._send_message())

        # Boton enviar
        self.btn_send = customtkinter.CTkButton(
            input_frame,
            text="Enviar",
            width=100,
            height=40,
            command=self._send_message
        )
        self.btn_send.grid(row=0, column=1)

        # Botones adicionales
        btn_frame = customtkinter.CTkFrame(input_frame, fg_color="transparent")
        btn_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        # Boton limpiar historial
        customtkinter.CTkButton(
            btn_frame,
            text="Limpiar chat",
            width=100,
            fg_color="transparent",
            border_width=1,
            command=self._clear_chat
        ).pack(side="left")

        # Botones de consultas rapidas
        customtkinter.CTkButton(
            btn_frame,
            text="Estadisticas BD",
            width=120,
            fg_color="#2d5a27",
            command=lambda: self._quick_query("Dame las estadisticas actuales de la base de datos")
        ).pack(side="left", padx=(10, 0))

        customtkinter.CTkButton(
            btn_frame,
            text="Ver esquema",
            width=100,
            fg_color="#5a4227",
            command=lambda: self._quick_query("Muestrame la estructura de las tablas principales")
        ).pack(side="left", padx=(10, 0))

    def _create_status_bar(self):
        """Crea la barra de estado inferior."""
        status_frame = customtkinter.CTkFrame(self, height=30, fg_color=("gray85", "gray20"))
        status_frame.grid(row=3, column=0, sticky="ew")
        status_frame.grid_columnconfigure(0, weight=1)

        self.status_label = customtkinter.CTkLabel(
            status_frame,
            text="Verificando conexion con Ollama...",
            font=customtkinter.CTkFont(size=11),
            anchor="w"
        )
        self.status_label.grid(row=0, column=0, padx=15, pady=5, sticky="w")

        # Indicador de procesamiento
        self.processing_label = customtkinter.CTkLabel(
            status_frame,
            text="",
            font=customtkinter.CTkFont(size=11),
            text_color="#FFD700"
        )
        self.processing_label.grid(row=0, column=1, padx=15, pady=5, sticky="e")

    def _check_requirements(self):
        """Verifica los requisitos del asistente en un hilo separado."""
        print("[DEBUG] _check_requirements() llamado")  # DEBUG
        self._set_status("Conectando con Ollama...")
        self.update()  # Forzar actualizacion UI

        # Ejecutar verificacion en hilo separado para no bloquear UI
        thread = threading.Thread(target=self._do_check_requirements)
        thread.daemon = True
        thread.start()
        print("[DEBUG] Thread iniciado")  # DEBUG

    def _do_check_requirements(self):
        """Ejecuta la verificacion de requisitos (en hilo separado)."""
        print("[DEBUG] _do_check_requirements() iniciado")  # DEBUG
        from script.ai_assistant import check_requirements, AIAssistant

        try:
            reqs = check_requirements()
            print(f"[DEBUG] check_requirements() retorno: {reqs}")  # DEBUG
            # Actualizar UI desde el hilo principal
            self.after(0, lambda: self._apply_requirements(reqs))
        except Exception as e:
            print(f"[DEBUG] Error en check_requirements: {e}")  # DEBUG
            self.after(0, lambda: self._set_status(f"Error: {str(e)}", error=True))
            self.after(0, lambda: self._add_error_message(f"Error: {str(e)}"))

    def _apply_requirements(self, reqs):
        """Aplica los resultados de la verificacion a la UI."""
        print(f"[DEBUG] _apply_requirements() llamado con: {reqs}")  # DEBUG
        from script.ai_assistant import AIAssistant

        if not reqs['ollama_installed']:
            self._set_status(reqs.get('message', 'Ollama no instalado'), error=True)
            self._add_system_message(
                "AVISO: Ollama no detectado.\n\n"
                "Para usar el asistente IA:\n"
                "1. Descarga Ollama desde https://ollama.ai\n"
                "2. Abre la aplicacion Ollama\n"
                "3. Descarga un modelo: ollama pull mistral:7b\n\n"
                "Luego haz clic en el boton de actualizar (↻)"
            )
            self.model_selector.configure(values=["No disponible"])
            self.model_selector.set("No disponible")
            self.btn_send.configure(state="disabled")
            return

        if not reqs['ollama_running']:
            self._set_status(reqs.get('message', 'Ollama no ejecutandose'), error=True)
            self._add_system_message(
                f"AVISO: {reqs.get('message', 'Ollama no esta ejecutandose')}\n\n"
                "Abre la aplicacion Ollama y haz clic en actualizar (↻)"
            )
            self.model_selector.configure(values=["No disponible"])
            self.model_selector.set("No disponible")
            self.btn_send.configure(state="disabled")
            return

        if not reqs['models_available']:
            self._set_status("Sin modelos instalados", error=True)
            self._add_system_message(
                "AVISO: No hay modelos de IA instalados.\n\n"
                "Ejecuta en terminal:\n"
                "  ollama pull mistral:7b\n\n"
                "Luego haz clic en actualizar (↻)"
            )
            self.model_selector.configure(values=["Sin modelos"])
            self.model_selector.set("Sin modelos")
            self.btn_send.configure(state="disabled")
            return

        # Todo OK - configurar modelos
        self.model_selector.configure(values=reqs['models_available'])

        # Seleccionar modelo recomendado o el primero
        if reqs['recommended_model']:
            self.model_selector.set(reqs['recommended_model'])
        else:
            self.model_selector.set(reqs['models_available'][0])

        # Crear instancia del asistente
        self.assistant = AIAssistant(self.user, self.password, self.schema)
        self.assistant.set_model(self.model_selector.get())

        self._set_status(f"Listo. Modelo: {self.model_selector.get()}")
        self.btn_send.configure(state="normal")
        self._add_system_message(f"Asistente listo con modelo: {self.model_selector.get()}")

    def _refresh_models(self):
        """Actualiza la lista de modelos disponibles."""
        from script.ai_assistant import AIAssistant

        self._set_status("Actualizando modelos...")
        models = AIAssistant.get_available_models()

        if models:
            self.model_selector.configure(values=models)
            self._set_status(f"Modelos disponibles: {len(models)}")
        else:
            self._set_status("No se encontraron modelos", error=True)

    def _on_model_change(self, model_name: str):
        """Callback cuando cambia el modelo seleccionado."""
        if self.assistant:
            self.assistant.set_model(model_name)
            self._set_status(f"Modelo cambiado a: {model_name}")

    def _send_message(self):
        """Envia el mensaje al asistente."""
        if self.is_processing:
            return

        message = self.input_entry.get().strip()
        if not message:
            return

        if not self.assistant:
            self._add_error_message("El asistente no esta disponible. Verifica la conexion con Ollama.")
            return

        # Limpiar entrada
        self.input_entry.delete(0, "end")

        # Mostrar mensaje del usuario
        self._add_user_message(message)

        # Procesar en hilo separado
        self.is_processing = True
        self.btn_send.configure(state="disabled")
        self.processing_label.configure(text="Procesando...")

        thread = threading.Thread(target=self._process_message, args=(message,))
        thread.daemon = True
        thread.start()

    def _process_message(self, message: str):
        """Procesa el mensaje en un hilo separado."""
        try:
            # Verificar si es una consulta SQL directa
            if message.upper().startswith("SELECT") or message.upper().startswith("SHOW"):
                result = self.assistant.execute_query_from_prompt(message)
                if result:
                    self.after(0, lambda: self._add_assistant_message(result))
                    self.after(0, self._finish_processing)
                    return

            # Usar streaming para mejor UX
            response_parts = []
            for chunk in self.assistant.chat_stream(message):
                response_parts.append(chunk)

            full_response = "".join(response_parts)
            self.after(0, lambda: self._add_assistant_message(full_response))

        except Exception as e:
            self.after(0, lambda: self._add_error_message(f"Error: {str(e)}"))

        finally:
            self.after(0, self._finish_processing)

    def _finish_processing(self):
        """Finaliza el procesamiento."""
        self.is_processing = False
        self.btn_send.configure(state="normal")
        self.processing_label.configure(text="")

    def _quick_query(self, query: str):
        """Ejecuta una consulta rapida predefinida."""
        self.input_entry.delete(0, "end")
        self.input_entry.insert(0, query)
        self._send_message()

    def _add_message(self, text: str, tag: str, prefix: str = ""):
        """Agrega un mensaje al area de chat."""
        self.chat_display.configure(state="normal")

        if prefix:
            self.chat_display.insert("end", f"\n{prefix}\n", tag)
        self.chat_display.insert("end", f"{text}\n\n")

        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def _add_user_message(self, text: str):
        """Agrega un mensaje del usuario."""
        self._add_message(text, "user", "Tu:")

    def _add_assistant_message(self, text: str):
        """Agrega un mensaje del asistente."""
        self._add_message(text, "assistant", "Asistente:")

    def _add_system_message(self, text: str):
        """Agrega un mensaje del sistema."""
        self._add_message(text, "system", "Sistema:")

    def _add_error_message(self, text: str):
        """Agrega un mensaje de error."""
        self._add_message(text, "error", "Error:")

    def _clear_chat(self):
        """Limpia el historial de chat."""
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")

        if self.assistant:
            self.assistant.clear_history()

        self._add_system_message("Historial limpiado. Puedes comenzar una nueva conversacion.")

    def _set_status(self, text: str, error: bool = False):
        """Actualiza el texto de la barra de estado."""
        color = "#FF6B6B" if error else None
        self.status_label.configure(text=text, text_color=color)


def open_ai_assistant(parent, user: str, password: str, schema: str):
    """
    Abre la ventana del asistente de IA.

    Args:
        parent: Ventana padre
        user: Usuario de BD
        password: Password de BD
        schema: Esquema activo
    """
    window = AIAssistantWindow(parent, user, password, schema)
    return window


# Para pruebas independientes
if __name__ == "__main__":
    import os
    import getpass

    app = customtkinter.CTk()
    app.withdraw()

    USER = os.getenv('DB_USER') or input("Usuario BD: ")
    PASSWORD = os.getenv('DB_PASSWORD') or getpass.getpass("Password: ")
    SCHEMA = os.getenv('DB_SCHEMA', 'cert_dev')

    window = AIAssistantWindow(app, USER, PASSWORD, SCHEMA)
    app.mainloop()
