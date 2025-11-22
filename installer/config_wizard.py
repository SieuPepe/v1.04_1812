#!/usr/bin/env python3
"""
HydroFlow Manager v1.04 - Configuration Wizard
===============================================

Asistente de configuración post-instalación para HydroFlow Manager.
Este wizard configura la conexión a la base de datos MySQL existente.

IMPORTANTE: Este wizard NO instala dependencias ni crea esquemas.
           Solo configura la conexión a una base de datos ya existente.

Uso:
    python config_wizard.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
from pathlib import Path
import subprocess

class ConfigWizard:
    """Wizard de configuración de HydroFlow Manager"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HydroFlow Manager - Configuración")
        self.root.geometry("700x550")
        self.root.resizable(False, False)

        # Configuración por defecto
        self.install_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
        self.config = {
            'db_host': tk.StringVar(value='localhost'),
            'db_port': tk.StringVar(value='3307'),  # Puerto por defecto 3307
            'db_user': tk.StringVar(value='root'),
            'db_password': tk.StringVar(value=''),
            'db_manager_schema': tk.StringVar(value='manager'),
            'db_example_schema': tk.StringVar(value='proyecto_tipo'),
            'db_schema': tk.StringVar(value='cert_dev')
        }

        # Estado
        self.current_step = 0
        self.connection_ok = False

        # Crear UI
        self.create_ui()
        self.show_step(0)

    def create_ui(self):
        """Crear interfaz de usuario"""
        # Contenedor principal
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título
        self.title_label = ttk.Label(
            self.main_frame,
            text="",
            font=('Segoe UI', 16, 'bold')
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Contenedor de pasos
        self.step_frame = ttk.Frame(self.main_frame)
        self.step_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Botones
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))

        self.back_btn = ttk.Button(button_frame, text="< Anterior", command=self.prev_step)
        self.back_btn.grid(row=0, column=0, padx=5)

        self.next_btn = ttk.Button(button_frame, text="Siguiente >", command=self.next_step)
        self.next_btn.grid(row=0, column=1, padx=5)

        self.finish_btn = ttk.Button(button_frame, text="Finalizar", command=self.finish)
        self.finish_btn.grid(row=0, column=2, padx=5)
        self.finish_btn.grid_remove()

    def clear_step_frame(self):
        """Limpiar frame de paso actual"""
        for widget in self.step_frame.winfo_children():
            widget.destroy()

    def show_step(self, step):
        """Mostrar paso específico"""
        self.current_step = step
        self.clear_step_frame()

        if step == 0:
            self.step_welcome()
        elif step == 1:
            self.step_configure_database()
        elif step == 2:
            self.step_test_connection()
        elif step == 3:
            self.step_finish()

        # Actualizar botones
        self.back_btn.config(state='normal' if step > 0 else 'disabled')

        if step == 3:
            self.next_btn.grid_remove()
            self.finish_btn.grid()
        else:
            self.finish_btn.grid_remove()
            self.next_btn.grid()

    def step_welcome(self):
        """Paso 1: Bienvenida"""
        self.title_label.config(text="Bienvenido a HydroFlow Manager v1.04")

        welcome_text = """
Este asistente le ayudará a configurar la conexión a la base de datos MySQL.

REQUISITOS PREVIOS:
  ✓ MySQL/MariaDB instalado y funcionando
  ✓ Base de datos HydroFlow ya creada e importada
  ✓ Credenciales de acceso a MySQL disponibles

IMPORTANTE:
  Este asistente NO crea esquemas ni importa datos.
  La base de datos debe estar lista y configurada previamente.

El proceso de configuración incluye:
  1. Configurar conexión a MySQL
  2. Probar la conexión
  3. Generar archivo de configuración (.env)

Presione 'Siguiente' para comenzar.
        """

        text_widget = tk.Text(
            self.step_frame,
            wrap=tk.WORD,
            height=18,
            width=70,
            font=('Consolas', 10),
            relief=tk.FLAT,
            bg='#f0f0f0'
        )
        text_widget.insert('1.0', welcome_text)
        text_widget.config(state='disabled')
        text_widget.grid(row=0, column=0, pady=10)

    def step_configure_database(self):
        """Paso 2: Configurar base de datos"""
        self.title_label.config(text="Configuración de Base de Datos")

        # Instrucciones
        ttk.Label(
            self.step_frame,
            text="Ingrese los datos de conexión a MySQL:",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky=tk.W)

        # Campos de configuración
        fields = [
            ("Host:", 'db_host', "Generalmente 'localhost'"),
            ("Puerto:", 'db_port', "3307 por defecto"),
            ("Usuario:", 'db_user', "Usuario con permisos"),
            ("Contraseña:", 'db_password', "Contraseña de MySQL"),
            ("", "", ""),  # Separador
            ("Esquema Manager:", 'db_manager_schema', "Esquema maestro"),
            ("Esquema Proyecto Tipo:", 'db_example_schema', "Plantilla de proyecto"),
            ("Esquema Desarrollo:", 'db_schema', "Esquema de trabajo")
        ]

        row = 1
        for label_text, config_key, hint in fields:
            if not label_text:  # Separador
                ttk.Separator(self.step_frame, orient='horizontal').grid(
                    row=row, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E)
                )
                row += 1
                continue

            ttk.Label(self.step_frame, text=label_text).grid(
                row=row, column=0, sticky=tk.W, pady=5, padx=(0, 10)
            )

            if config_key == 'db_password':
                entry = ttk.Entry(
                    self.step_frame,
                    textvariable=self.config[config_key],
                    width=30,
                    show='*'
                )
            else:
                entry = ttk.Entry(
                    self.step_frame,
                    textvariable=self.config[config_key],
                    width=30
                )
            entry.grid(row=row, column=1, sticky=tk.W, pady=5)

            ttk.Label(
                self.step_frame,
                text=hint,
                font=('Segoe UI', 8),
                foreground='gray'
            ).grid(row=row, column=2, sticky=tk.W, pady=5, padx=(10, 0))

            row += 1

    def step_test_connection(self):
        """Paso 3: Probar conexión"""
        self.title_label.config(text="Probar Conexión a Base de Datos")

        ttk.Label(
            self.step_frame,
            text="Presione 'Probar Conexión' para verificar la configuración:",
            font=('Segoe UI', 10)
        ).grid(row=0, column=0, pady=(0, 15), sticky=tk.W)

        # Botón de prueba
        test_btn = ttk.Button(
            self.step_frame,
            text="Probar Conexión",
            command=self.test_connection
        )
        test_btn.grid(row=1, column=0, pady=10)

        # Área de resultados
        self.test_result_frame = ttk.LabelFrame(
            self.step_frame,
            text="Resultado",
            padding="10"
        )
        self.test_result_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)

        self.test_result_label = ttk.Label(
            self.test_result_frame,
            text="Presione el botón para probar la conexión...",
            font=('Segoe UI', 9)
        )
        self.test_result_label.pack()

    def test_connection(self):
        """Probar conexión a MySQL"""
        self.test_result_label.config(text="Probando conexión...", foreground='blue')
        self.root.update()

        try:
            # Instalar mysql-connector-python si no está disponible
            try:
                import mysql.connector
            except ImportError:
                self.test_result_label.config(
                    text="Instalando mysql-connector-python...",
                    foreground='orange'
                )
                self.root.update()
                subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', 'mysql-connector-python'],
                    check=True,
                    capture_output=True
                )
                import mysql.connector

            # Intentar conexión
            connection = mysql.connector.connect(
                host=self.config['db_host'].get(),
                port=int(self.config['db_port'].get()),
                user=self.config['db_user'].get(),
                password=self.config['db_password'].get()
            )

            # Obtener versión de MySQL
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]

            # Verificar que los esquemas existen
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]

            missing_schemas = []
            for schema_key in ['db_manager_schema', 'db_example_schema', 'db_schema']:
                schema_name = self.config[schema_key].get()
                if schema_name not in databases:
                    missing_schemas.append(schema_name)

            cursor.close()
            connection.close()

            if missing_schemas:
                self.test_result_label.config(
                    text=f"⚠ Conexión exitosa (MySQL {version})\n"
                         f"ADVERTENCIA: Los siguientes esquemas no existen:\n"
                         f"{', '.join(missing_schemas)}\n"
                         f"Asegúrese de que la base de datos esté correctamente configurada.",
                    foreground='orange'
                )
                self.connection_ok = False
            else:
                self.test_result_label.config(
                    text=f"✓ Conexión exitosa!\n"
                         f"MySQL versión: {version}\n"
                         f"Todos los esquemas encontrados correctamente.",
                    foreground='green'
                )
                self.connection_ok = True

        except Exception as e:
            self.test_result_label.config(
                text=f"✗ Error de conexión:\n{str(e)}\n\n"
                     f"Verifique los datos de conexión e inténtelo nuevamente.",
                foreground='red'
            )
            self.connection_ok = False

    def step_finish(self):
        """Paso 4: Finalización"""
        self.title_label.config(text="Configuración Completa")

        if not self.connection_ok:
            finish_text = """
⚠ ADVERTENCIA:
No se pudo verificar la conexión a la base de datos.

Puede continuar con la configuración, pero es posible que
la aplicación no funcione correctamente.

Se recomienda:
  1. Verificar que MySQL esté corriendo
  2. Verificar las credenciales de acceso
  3. Verificar que los esquemas existan
  4. Volver atrás y probar la conexión nuevamente

¿Desea continuar de todos modos?
            """
        else:
            finish_text = """
✓ Configuración completada exitosamente!

Se generará el archivo .env con la configuración proporcionada.

Configuración:
  Host: {host}
  Puerto: {port}
  Usuario: {user}
  Esquema Manager: {manager}
  Esquema Proyecto Tipo: {example}
  Esquema Desarrollo: {dev}

Presione 'Finalizar' para guardar la configuración y cerrar el asistente.

Una vez finalizado, puede ejecutar HydroFlow Manager desde:
  {install_dir}\\HydroFlowManager.exe
            """.format(
                host=self.config['db_host'].get(),
                port=self.config['db_port'].get(),
                user=self.config['db_user'].get(),
                manager=self.config['db_manager_schema'].get(),
                example=self.config['db_example_schema'].get(),
                dev=self.config['db_schema'].get(),
                install_dir=self.install_dir
            )

        text_widget = tk.Text(
            self.step_frame,
            wrap=tk.WORD,
            height=20,
            width=70,
            font=('Consolas', 9),
            relief=tk.FLAT,
            bg='#f0f0f0'
        )
        text_widget.insert('1.0', finish_text)
        text_widget.config(state='disabled')
        text_widget.grid(row=0, column=0, pady=10)

    def next_step(self):
        """Ir al siguiente paso"""
        # Validaciones antes de avanzar
        if self.current_step == 1:
            # Validar que todos los campos estén llenos
            if not all([
                self.config['db_host'].get(),
                self.config['db_port'].get(),
                self.config['db_user'].get(),
                self.config['db_password'].get()
            ]):
                messagebox.showwarning(
                    "Campos Incompletos",
                    "Por favor complete todos los campos obligatorios:\n"
                    "Host, Puerto, Usuario y Contraseña"
                )
                return

        if self.current_step == 2:
            # Advertir si no se probó la conexión
            if not self.connection_ok:
                result = messagebox.askyesno(
                    "Conexión No Verificada",
                    "No se ha probado la conexión a la base de datos.\n\n"
                    "¿Desea continuar de todos modos?"
                )
                if not result:
                    return

        self.show_step(self.current_step + 1)

    def prev_step(self):
        """Ir al paso anterior"""
        if self.current_step > 0:
            self.show_step(self.current_step - 1)

    def finish(self):
        """Finalizar configuración"""
        try:
            # Generar archivo .env
            env_path = self.install_dir / '.env'

            env_content = f"""# HydroFlow Manager v1.04 - Configuración
# Generado automáticamente por el asistente de configuración

# Servidor MySQL
DB_HOST={self.config['db_host'].get()}
DB_PORT={self.config['db_port'].get()}

# Credenciales (MANTENER SEGURO)
DB_USER={self.config['db_user'].get()}
DB_PASSWORD={self.config['db_password'].get()}

# Esquemas
DB_MANAGER_SCHEMA={self.config['db_manager_schema'].get()}
DB_EXAMPLE_SCHEMA={self.config['db_example_schema'].get()}
DB_SCHEMA={self.config['db_schema'].get()}

# Rendimiento
DB_USE_POOLING=true
"""

            with open(env_path, 'w', encoding='utf-8') as f:
                f.write(env_content)

            messagebox.showinfo(
                "Configuración Guardada",
                f"La configuración se ha guardado correctamente en:\n{env_path}\n\n"
                f"Puede ejecutar HydroFlow Manager desde:\n{self.install_dir}\\HydroFlowManager.exe"
            )

            self.root.quit()

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al guardar la configuración:\n{str(e)}"
            )

    def run(self):
        """Ejecutar wizard"""
        self.root.mainloop()


if __name__ == "__main__":
    wizard = ConfigWizard()
    wizard.run()
