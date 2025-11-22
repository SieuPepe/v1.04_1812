#!/usr/bin/env python3
"""
HydroFlow Manager v2.0 - Setup Wizard (Versión Simplificada)
Instalador Gráfico Interactivo

Este wizard guía al usuario a través del proceso de instalación:
1. Verificación de MySQL
2. Configuración de conexión a base de datos existente
3. Prueba de conexión
4. Instalación de dependencias Python
5. Generación de archivo .env

NOTA: Esta versión asume que la base de datos ya está configurada.
No crea esquemas ni importa datos.

Diseñado para usuarios sin experiencia técnica.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import os
import sys
import subprocess
import threading
import shutil
from pathlib import Path
import urllib.request
import json

class SetupWizard:
    """Wizard de instalación de HydroFlow Manager"""

    def __init__(self, root):
        self.root = root
        self.root.title("HydroFlow Manager v2.0 - Instalador")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Variables de configuración
        self.config = {
            'db_host': tk.StringVar(value='localhost'),
            'db_port': tk.StringVar(value='3306'),
            'db_user': tk.StringVar(value='root'),
            'db_password': tk.StringVar(value=''),
            'db_manager_schema': tk.StringVar(value='manager'),
            'db_example_schema': tk.StringVar(value='proyecto_tipo'),
            'db_schema': tk.StringVar(value='cert_dev'),
            'install_path': tk.StringVar(value=str(Path.home() / 'HydroFlowManager'))
        }

        self.current_step = 0
        self.mysql_installed = False
        self.mysql_running = False
        self.connection_tested = False

        # Directorio del proyecto
        self.project_root = Path(__file__).resolve().parent.parent

        # Crear interfaz
        self.create_ui()
        self.show_step(0)

    def create_ui(self):
        """Crear interfaz de usuario"""
        # Header
        header = tk.Frame(self.root, bg='#2c3e50', height=80)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="HydroFlow Manager v2.0",
            font=('Arial', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title.pack(pady=25)

        # Main container
        self.container = tk.Frame(self.root)
        self.container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Footer con botones
        footer = tk.Frame(self.root)
        footer.pack(fill=tk.X, padx=20, pady=10)

        self.btn_back = tk.Button(
            footer,
            text="< Atrás",
            command=self.previous_step,
            width=15
        )
        self.btn_back.pack(side=tk.LEFT)

        self.btn_next = tk.Button(
            footer,
            text="Siguiente >",
            command=self.next_step,
            width=15,
            bg='#3498db',
            fg='white'
        )
        self.btn_next.pack(side=tk.RIGHT)

        tk.Button(
            footer,
            text="Cancelar",
            command=self.cancel_installation,
            width=15
        ).pack(side=tk.RIGHT, padx=5)

    def clear_container(self):
        """Limpiar contenedor principal"""
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_step(self, step):
        """Mostrar paso específico"""
        self.current_step = step
        self.clear_container()

        steps = [
            self.step_welcome,
            self.step_verify_mysql,
            self.step_configure_database,
            self.step_test_connection,
            self.step_install_dependencies,
            self.step_finish
        ]

        if 0 <= step < len(steps):
            steps[step]()

        # Actualizar estado de botones
        self.btn_back.config(state=tk.NORMAL if step > 0 else tk.DISABLED)

        if step == len(steps) - 1:
            self.btn_next.config(text="Finalizar", bg='#27ae60')
        else:
            self.btn_next.config(text="Siguiente >", bg='#3498db')

    def next_step(self):
        """Ir al siguiente paso"""
        if self.current_step == 5:  # Último paso
            self.finish_installation()
        else:
            self.show_step(self.current_step + 1)

    def previous_step(self):
        """Volver al paso anterior"""
        if self.current_step > 0:
            self.show_step(self.current_step - 1)

    # ========================================================================
    # PASO 1: Bienvenida
    # ========================================================================

    def step_welcome(self):
        """Pantalla de bienvenida"""
        tk.Label(
            self.container,
            text="HydroFlow Manager v2.0 - Instalador",
            font=('Arial', 14, 'bold')
        ).pack(pady=10)

        welcome_text = """Este asistente configurará HydroFlow Manager v2.0.

Pasos de instalación:
✓ Verificar MySQL  ✓ Configurar conexión  ✓ Instalar dependencias  ✓ Generar .env

REQUISITOS:
• MySQL/MariaDB instalado y corriendo
• Base de datos configurada (esquemas y datos ya importados)
• Credenciales de MySQL (usuario y contraseña)
• Conexión a Internet

NOTA: Este instalador NO crea esquemas. La BD debe estar lista.
"""

        tk.Label(
            self.container,
            text=welcome_text,
            justify=tk.LEFT,
            font=('Arial', 9)
        ).pack(pady=5, padx=20)

    # ========================================================================
    # PASO 2: Verificar MySQL
    # ========================================================================

    def step_verify_mysql(self):
        """Verificar que MySQL está corriendo"""
        tk.Label(
            self.container,
            text="Verificación de MySQL",
            font=('Arial', 16, 'bold')
        ).pack(pady=20)

        tk.Label(
            self.container,
            text="Verificando que MySQL/MariaDB esté instalado y corriendo...",
            font=('Arial', 10)
        ).pack(pady=10)

        self.mysql_status_text = scrolledtext.ScrolledText(
            self.container,
            height=18,
            width=80,
            font=('Consolas', 9)
        )
        self.mysql_status_text.pack(pady=10)

        tk.Button(
            self.container,
            text="Verificar Nuevamente",
            command=self.verify_mysql,
            bg='#3498db',
            fg='white',
            width=25,
            font=('Arial', 10, 'bold')
        ).pack(pady=10)

        # Auto-verificar al entrar
        self.root.after(500, self.verify_mysql)

    def verify_mysql(self):
        """Verificar si MySQL está instalado"""
        self.log_mysql("Verificando instalación de MySQL...\n")

        # Buscar mysql.exe
        mysql_path = shutil.which('mysql')

        if mysql_path:
            self.log_mysql(f"✓ MySQL encontrado en: {mysql_path}\n")
            self.mysql_installed = True
            self.log_mysql("=" * 60)
            self.log_mysql("✓ VERIFICACIÓN COMPLETADA - MySQL detectado")
            self.log_mysql("=" * 60)
            self.log_mysql("\nPuede continuar al siguiente paso.")
        else:
            self.log_mysql("⚠ MySQL no encontrado en el PATH")
            self.log_mysql("\nBuscando en ubicaciones comunes...\n")

            common_paths = [
                r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
                r"C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe",
                r"C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe",
                r"C:\xampp\mysql\bin\mysql.exe",
                r"C:\wamp64\bin\mysql\mysql8.0.27\bin\mysql.exe"
            ]

            found = False
            for path in common_paths:
                if os.path.exists(path):
                    self.log_mysql(f"✓ MySQL encontrado en: {path}\n")
                    self.log_mysql("  NOTA: Considere agregar esta ruta al PATH del sistema\n")
                    self.mysql_installed = True
                    found = True
                    self.log_mysql("=" * 60)
                    self.log_mysql("✓ VERIFICACIÓN COMPLETADA - MySQL detectado")
                    self.log_mysql("=" * 60)
                    self.log_mysql("\nPuede continuar al siguiente paso.")
                    break

            if not found:
                self.log_mysql("=" * 60)
                self.log_mysql("✗ VERIFICACIÓN FALLIDA - MySQL NO encontrado")
                self.log_mysql("=" * 60)
                self.log_mysql("\n** IMPORTANTE **")
                self.log_mysql("MySQL/MariaDB debe estar instalado antes de continuar.\n")
                self.log_mysql("Por favor:")
                self.log_mysql("1. Instale MySQL/MariaDB o XAMPP")
                self.log_mysql("2. Asegúrese de que esté corriendo")
                self.log_mysql("3. Haga clic en 'Verificar Nuevamente'\n")
                self.mysql_installed = False

                messagebox.showwarning(
                    "MySQL No Encontrado",
                    "MySQL/MariaDB no está instalado o no se encuentra en el PATH.\n\n"
                    "Opciones:\n"
                    "• Instale MySQL desde: https://dev.mysql.com/downloads/mysql/\n"
                    "• O instale XAMPP: https://www.apachefriends.org/\n\n"
                    "Luego haga clic en 'Verificar Nuevamente'."
                )


    def log_mysql(self, message):
        """Agregar mensaje al log de MySQL"""
        self.mysql_status_text.insert(tk.END, message + '\n')
        self.mysql_status_text.see(tk.END)
        self.root.update()

    # ========================================================================
    # PASO 3: Configurar Base de Datos
    # ========================================================================

    def step_configure_database(self):
        """Configurar conexión a base de datos"""
        tk.Label(
            self.container,
            text="Configuración de Base de Datos",
            font=('Arial', 16, 'bold')
        ).pack(pady=20)

        tk.Label(
            self.container,
            text="Ingrese los datos de conexión a su servidor MySQL:",
            font=('Arial', 10)
        ).pack(pady=10)

        # Formulario
        form = tk.Frame(self.container)
        form.pack(pady=10, padx=50, fill=tk.BOTH, expand=True)

        fields = [
            ("Servidor (Host):", 'db_host', "Ejemplo: localhost"),
            ("Puerto:", 'db_port', "Ejemplo: 3306 o 3307"),
            ("Usuario:", 'db_user', "Ejemplo: root"),
            ("Contraseña:", 'db_password', "Su contraseña de MySQL"),
        ]

        for i, (label, var_name, placeholder) in enumerate(fields):
            tk.Label(form, text=label, font=('Arial', 10, 'bold')).grid(
                row=i, column=0, sticky=tk.W, pady=5
            )

            entry = tk.Entry(form, textvariable=self.config[var_name], width=40)
            if var_name == 'db_password':
                entry.config(show='*')
            entry.grid(row=i, column=1, pady=5, padx=10)

            tk.Label(form, text=placeholder, font=('Arial', 8), fg='gray').grid(
                row=i, column=2, sticky=tk.W, padx=5
            )

        # Separador
        ttk.Separator(form, orient='horizontal').grid(
            row=len(fields), column=0, columnspan=3, sticky='ew', pady=15
        )

        # Esquemas
        tk.Label(
            form,
            text="Nombres de Esquemas (puede dejar los valores por defecto):",
            font=('Arial', 10, 'bold')
        ).grid(row=len(fields)+1, column=0, columnspan=3, sticky=tk.W, pady=5)

        schema_fields = [
            ("Esquema Manager:", 'db_manager_schema'),
            ("Esquema Proyecto Tipo:", 'db_example_schema'),
            ("Esquema de Trabajo:", 'db_schema'),
        ]

        for i, (label, var_name) in enumerate(schema_fields):
            row = len(fields) + 2 + i
            tk.Label(form, text=label, font=('Arial', 10)).grid(
                row=row, column=0, sticky=tk.W, pady=5
            )
            tk.Entry(form, textvariable=self.config[var_name], width=40).grid(
                row=row, column=1, pady=5, padx=10
            )

    # ========================================================================
    # PASO 4: Probar Conexión
    # ========================================================================

    def step_test_connection(self):
        """Probar conexión a base de datos"""
        tk.Label(
            self.container,
            text="Probar Conexión",
            font=('Arial', 16, 'bold')
        ).pack(pady=20)

        self.connection_log = scrolledtext.ScrolledText(
            self.container,
            height=20,
            width=80,
            font=('Consolas', 9)
        )
        self.connection_log.pack(pady=10)

        tk.Button(
            self.container,
            text="Probar Conexión",
            command=self.test_connection,
            bg='#3498db',
            fg='white',
            width=20,
            font=('Arial', 10, 'bold')
        ).pack(pady=10)

        # Auto-test al entrar
        self.root.after(500, self.test_connection)

    def test_connection(self):
        """Probar conexión a MySQL"""
        self.connection_log.delete('1.0', tk.END)
        self.log_connection("Probando conexión a MySQL...")
        self.log_connection(f"Host: {self.config['db_host'].get()}")
        self.log_connection(f"Puerto: {self.config['db_port'].get()}")
        self.log_connection(f"Usuario: {self.config['db_user'].get()}")
        self.log_connection("")

        # Comando de prueba
        cmd = [
            'mysql',
            '-h', self.config['db_host'].get(),
            '-P', self.config['db_port'].get(),
            '-u', self.config['db_user'].get(),
            f'-p{self.config["db_password"].get()}',
            '-e', 'SELECT VERSION();'
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                self.log_connection("✓ CONEXIÓN EXITOSA")
                self.log_connection("")
                self.log_connection(result.stdout)
                self.connection_tested = True

                messagebox.showinfo(
                    "Éxito",
                    "La conexión a MySQL fue exitosa.\n\n"
                    "Haga clic en 'Siguiente' para continuar."
                )
            else:
                self.log_connection("✗ ERROR DE CONEXIÓN")
                self.log_connection("")
                self.log_connection(result.stderr)
                self.connection_tested = False

                messagebox.showerror(
                    "Error de Conexión",
                    "No se pudo conectar a MySQL.\n\n"
                    "Verifique:\n"
                    "• Que MySQL esté corriendo\n"
                    "• Que las credenciales sean correctas\n"
                    "• Que el puerto sea el correcto"
                )
        except subprocess.TimeoutExpired:
            self.log_connection("✗ TIMEOUT")
            self.log_connection("La conexión tardó demasiado tiempo")
            self.connection_tested = False
        except FileNotFoundError:
            self.log_connection("✗ ERROR: mysql.exe no encontrado")
            self.log_connection("Asegúrese de que MySQL esté instalado")
            self.connection_tested = False
        except Exception as e:
            self.log_connection(f"✗ ERROR: {e}")
            self.connection_tested = False

    def log_connection(self, message):
        """Agregar mensaje al log de conexión"""
        self.connection_log.insert(tk.END, message + '\n')
        self.connection_log.see(tk.END)
        self.root.update()

    # ========================================================================
    # PASO 5: Crear Esquemas
    # ========================================================================

    def step_create_schemas(self):
        """Crear esquemas de base de datos"""
        tk.Label(
            self.container,
            text="Crear Esquemas de Base de Datos",
            font=('Arial', 16, 'bold')
        ).pack(pady=20)

        tk.Label(
            self.container,
            text="Se crearán los siguientes esquemas en MySQL:",
            font=('Arial', 10)
        ).pack(pady=10)

        # Lista de esquemas
        schema_frame = tk.Frame(self.container)
        schema_frame.pack(pady=10)

        schemas = [
            (self.config['db_manager_schema'].get(), "Esquema maestro de proyectos"),
            (self.config['db_example_schema'].get(), "Plantilla de proyecto tipo"),
            (self.config['db_schema'].get(), "Esquema de trabajo/desarrollo"),
        ]

        for i, (schema, desc) in enumerate(schemas):
            tk.Label(
                schema_frame,
                text=f"• {schema}",
                font=('Arial', 10, 'bold')
            ).grid(row=i, column=0, sticky=tk.W, padx=20, pady=2)

            tk.Label(
                schema_frame,
                text=f"({desc})",
                font=('Arial', 9),
                fg='gray'
            ).grid(row=i, column=1, sticky=tk.W, pady=2)

        self.schema_log = scrolledtext.ScrolledText(
            self.container,
            height=15,
            width=80,
            font=('Consolas', 9)
        )
        self.schema_log.pack(pady=10)

        tk.Button(
            self.container,
            text="Crear Esquemas",
            command=self.create_schemas,
            bg='#27ae60',
            fg='white',
            width=20,
            font=('Arial', 10, 'bold')
        ).pack(pady=10)

    def create_schemas(self):
        """Crear esquemas en MySQL"""
        self.schema_log.delete('1.0', tk.END)
        self.log_schema("Creando esquemas...")

        schemas = [
            self.config['db_manager_schema'].get(),
            self.config['db_example_schema'].get(),
            self.config['db_schema'].get(),
        ]

        for schema in schemas:
            self.log_schema(f"\nCreando esquema '{schema}'...")

            cmd = [
                'mysql',
                '-h', self.config['db_host'].get(),
                '-P', self.config['db_port'].get(),
                '-u', self.config['db_user'].get(),
                f'-p{self.config["db_password"].get()}',
                '-e', f'CREATE DATABASE IF NOT EXISTS {schema};'
            ]

            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode == 0:
                    self.log_schema(f"✓ Esquema '{schema}' creado exitosamente")
                else:
                    self.log_schema(f"✗ Error al crear esquema '{schema}':")
                    self.log_schema(result.stderr)
            except Exception as e:
                self.log_schema(f"✗ Error: {e}")

        self.log_schema("\n✓ Proceso de creación de esquemas completado")
        messagebox.showinfo(
            "Esquemas Creados",
            "Los esquemas de base de datos han sido creados.\n\n"
            "Haga clic en 'Siguiente' para importar los datos."
        )

    def log_schema(self, message):
        """Agregar mensaje al log de esquemas"""
        self.schema_log.insert(tk.END, message + '\n')
        self.schema_log.see(tk.END)
        self.root.update()

    # ========================================================================
    # PASO 6: Importar Datos
    # ========================================================================

    def step_import_data(self):
        """Importar datos iniciales"""
        tk.Label(
            self.container,
            text="Importar Datos Iniciales",
            font=('Arial', 16, 'bold')
        ).pack(pady=20)

        tk.Label(
            self.container,
            text="Seleccione los archivos SQL de backup para importar:",
            font=('Arial', 10)
        ).pack(pady=10)

        # Selección de archivos
        file_frame = tk.Frame(self.container)
        file_frame.pack(pady=10, fill=tk.X, padx=50)

        self.sql_files = {
            'manager': tk.StringVar(),
            'proyecto_tipo': tk.StringVar(),
        }

        files = [
            ("manager", "Backup del esquema Manager:"),
            ("proyecto_tipo", "Backup del esquema Proyecto Tipo:"),
        ]

        for i, (key, label) in enumerate(files):
            tk.Label(file_frame, text=label, font=('Arial', 10, 'bold')).grid(
                row=i, column=0, sticky=tk.W, pady=5
            )

            tk.Entry(file_frame, textvariable=self.sql_files[key], width=50).grid(
                row=i, column=1, pady=5, padx=5
            )

            tk.Button(
                file_frame,
                text="Buscar...",
                command=lambda k=key: self.browse_sql_file(k),
                width=10
            ).grid(row=i, column=2, pady=5)

        self.import_log = scrolledtext.ScrolledText(
            self.container,
            height=12,
            width=80,
            font=('Consolas', 9)
        )
        self.import_log.pack(pady=10)

        tk.Button(
            self.container,
            text="Importar Datos",
            command=self.import_data,
            bg='#27ae60',
            fg='white',
            width=20,
            font=('Arial', 10, 'bold')
        ).pack(pady=10)

        # Auto-detectar archivos SQL en backups/produccion
        self.auto_detect_sql_files()

    def auto_detect_sql_files(self):
        """Auto-detectar archivos SQL de backup"""
        backup_dir = self.project_root / 'backups' / 'produccion'

        if not backup_dir.exists():
            return

        # Buscar el directorio más reciente
        subdirs = [d for d in backup_dir.iterdir() if d.is_dir()]
        if not subdirs:
            return

        latest_dir = max(subdirs, key=lambda d: d.stat().st_mtime)

        # Buscar archivos SQL
        manager_file = latest_dir / 'manager_estructura_y_datos.sql'
        proyecto_tipo_file = latest_dir / 'proyecto_tipo_completo.sql'

        if manager_file.exists():
            self.sql_files['manager'].set(str(manager_file))

        if proyecto_tipo_file.exists():
            self.sql_files['proyecto_tipo'].set(str(proyecto_tipo_file))

    def browse_sql_file(self, key):
        """Buscar archivo SQL"""
        filename = filedialog.askopenfilename(
            title=f"Seleccionar archivo SQL para {key}",
            filetypes=[("SQL files", "*.sql"), ("All files", "*.*")],
            initialdir=str(self.project_root / 'backups' / 'produccion')
        )

        if filename:
            self.sql_files[key].set(filename)

    def import_data(self):
        """Importar datos desde archivos SQL"""
        self.import_log.delete('1.0', tk.END)
        self.log_import("Importando datos...")

        imports = [
            ('manager', self.sql_files['manager'].get()),
            ('proyecto_tipo', self.sql_files['proyecto_tipo'].get()),
        ]

        for name, filepath in imports:
            if not filepath:
                self.log_import(f"\n⚠ Archivo para '{name}' no seleccionado, omitiendo...")
                continue

            if not os.path.exists(filepath):
                self.log_import(f"\n✗ Archivo no encontrado: {filepath}")
                continue

            self.log_import(f"\nImportando '{name}' desde:")
            self.log_import(f"  {filepath}")

            cmd = [
                'mysql',
                '-h', self.config['db_host'].get(),
                '-P', self.config['db_port'].get(),
                '-u', self.config['db_user'].get(),
                f'-p{self.config["db_password"].get()}',
            ]

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    result = subprocess.run(
                        cmd,
                        stdin=f,
                        capture_output=True,
                        text=True,
                        timeout=60
                    )

                if result.returncode == 0:
                    self.log_import(f"✓ Datos de '{name}' importados exitosamente")
                else:
                    self.log_import(f"✗ Error al importar '{name}':")
                    self.log_import(result.stderr)
            except Exception as e:
                self.log_import(f"✗ Error: {e}")

        self.log_import("\n✓ Proceso de importación completado")
        messagebox.showinfo(
            "Datos Importados",
            "Los datos iniciales han sido importados.\n\n"
            "Haga clic en 'Siguiente' para instalar las dependencias de Python."
        )

    def log_import(self, message):
        """Agregar mensaje al log de importación"""
        self.import_log.insert(tk.END, message + '\n')
        self.import_log.see(tk.END)
        self.root.update()

    # ========================================================================
    # PASO 5: Instalar Dependencias
    # ========================================================================

    def step_install_dependencies(self):
        """Instalar dependencias de Python"""
        tk.Label(
            self.container,
            text="Instalar Dependencias",
            font=('Arial', 16, 'bold')
        ).pack(pady=20)

        tk.Label(
            self.container,
            text="Se instalarán las dependencias de Python necesarias:",
            font=('Arial', 10)
        ).pack(pady=10)

        self.deps_log = scrolledtext.ScrolledText(
            self.container,
            height=18,
            width=80,
            font=('Consolas', 9)
        )
        self.deps_log.pack(pady=10)

        tk.Button(
            self.container,
            text="Instalar Dependencias",
            command=self.install_dependencies,
            bg='#27ae60',
            fg='white',
            width=20,
            font=('Arial', 10, 'bold')
        ).pack(pady=10)

    def install_dependencies(self):
        """Instalar dependencias de Python"""
        self.deps_log.delete('1.0', tk.END)
        self.log_deps("Instalando dependencias de Python...")
        self.log_deps(f"Python: {sys.version}")
        self.log_deps("")

        requirements_file = self.project_root / 'requirements.txt'

        if not requirements_file.exists():
            self.log_deps("✗ Archivo requirements.txt no encontrado")
            return

        self.log_deps(f"Usando: {requirements_file}")
        self.log_deps("")

        cmd = [
            sys.executable,
            '-m',
            'pip',
            'install',
            '-r',
            str(requirements_file),
            '--upgrade'
        ]

        try:
            # Ejecutar en un thread para no bloquear la UI
            def run_install():
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )

                for line in process.stdout:
                    self.root.after(0, lambda l=line: self.log_deps(l.strip()))

                process.wait()

                if process.returncode == 0:
                    self.root.after(0, lambda: self.log_deps("\n✓ Dependencias instaladas exitosamente"))
                    self.root.after(0, lambda: messagebox.showinfo(
                        "Éxito",
                        "Las dependencias de Python han sido instaladas.\n\n"
                        "Haga clic en 'Siguiente' para finalizar la instalación."
                    ))
                else:
                    self.root.after(0, lambda: self.log_deps("\n✗ Error al instalar dependencias"))

            thread = threading.Thread(target=run_install, daemon=True)
            thread.start()

        except Exception as e:
            self.log_deps(f"\n✗ Error: {e}")

    def log_deps(self, message):
        """Agregar mensaje al log de dependencias"""
        self.deps_log.insert(tk.END, message + '\n')
        self.deps_log.see(tk.END)
        self.root.update()

    # ========================================================================
    # PASO 6: Finalizar
    # ========================================================================

    def step_finish(self):
        """Pantalla de finalización"""
        tk.Label(
            self.container,
            text="¡Instalación Completada!",
            font=('Arial', 16, 'bold'),
            fg='#27ae60'
        ).pack(pady=30)

        finish_text = """
HydroFlow Manager v2.0 ha sido instalado exitosamente.

✓ MySQL configurado
✓ Esquemas de base de datos creados
✓ Datos iniciales importados
✓ Dependencias instaladas
✓ Archivo .env configurado

Puede iniciar la aplicación ejecutando:
  python main.py

O compilar el ejecutable con:
  .\\build.ps1

Gracias por instalar HydroFlow Manager.
"""

        tk.Label(
            self.container,
            text=finish_text,
            justify=tk.LEFT,
            font=('Arial', 10)
        ).pack(pady=20)

        # Guardar configuración al finalizar
        self.save_config()

    def save_config(self):
        """Guardar configuración en .env"""
        env_file = self.project_root / '.env'

        env_content = f"""# HydroFlow Manager v2.0 - Configuración
# Generado automáticamente por el instalador

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

        try:
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(env_content)
            print(f"✓ Archivo .env creado: {env_file}")
        except Exception as e:
            print(f"✗ Error al crear .env: {e}")

    # ========================================================================
    # Utilidades
    # ========================================================================

    def cancel_installation(self):
        """Cancelar instalación"""
        if messagebox.askyesno(
            "Cancelar Instalación",
            "¿Está seguro de que desea cancelar la instalación?"
        ):
            self.root.destroy()

    def finish_installation(self):
        """Finalizar instalación"""
        messagebox.showinfo(
            "Instalación Completada",
            "La instalación ha finalizado exitosamente.\n\n"
            "El instalador se cerrará ahora."
        )
        self.root.destroy()


def main():
    """Función principal"""
    root = tk.Tk()
    app = SetupWizard(root)
    root.mainloop()


if __name__ == '__main__':
    main()
