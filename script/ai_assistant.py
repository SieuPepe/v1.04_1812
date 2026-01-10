"""
Asistente de IA local para HydroFlow Manager.

Utiliza Ollama para ejecutar modelos de lenguaje localmente.
Puede consultar manuales, codigo fuente y la base de datos.
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

# Intentar importar requests
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    requests = None

# Ruta base del proyecto
PROJECT_ROOT = Path(__file__).resolve().parent.parent


class AIAssistant:
    """Asistente de IA local usando Ollama."""

    # Modelos recomendados (ordenados por calidad/tamanio)
    RECOMMENDED_MODELS = [
        "llama3.2:3b",      # Rapido, buena calidad
        "mistral:7b",       # Equilibrado
        "llama3.1:8b",      # Mejor calidad
        "codellama:7b",     # Especializado en codigo
    ]

    OLLAMA_API_URL = "http://localhost:11434"

    def __init__(self, user: str, password: str, schema: str):
        """
        Inicializa el asistente.

        Args:
            user: Usuario de BD para consultas
            password: Password de BD
            schema: Esquema de BD activo
        """
        self.user = user
        self.password = password
        self.schema = schema
        self.model = None
        self.conversation_history: List[Dict] = []
        self._system_context = self._build_system_context()

    def _build_system_context(self) -> str:
        """Construye el contexto del sistema para el asistente."""
        return """Eres un asistente experto en HydroFlow Manager, una aplicacion de gestion de proyectos hidroelectricos.

Tu rol es ayudar a los usuarios con:
1. Dudas sobre el uso de la aplicacion
2. Consultas sobre la base de datos del proyecto
3. Explicaciones sobre el codigo fuente
4. Resolucion de problemas tecnicos

Informacion del sistema:
- Aplicacion: HydroFlow Manager v2.0
- Base de datos: MySQL/MariaDB
- Lenguaje: Python con CustomTkinter
- Esquema activo: """ + self.schema + """

Cuando el usuario pregunte sobre datos, puedes usar la funcion query_database.
Cuando pregunte sobre codigo, puedes usar la funcion read_code.
Cuando pregunte sobre manuales, puedes usar la funcion read_manual.

Responde siempre en espanol y de forma concisa pero completa."""

    @staticmethod
    def check_ollama_available() -> tuple[bool, str]:
        """
        Verifica si Ollama esta disponible.

        Returns:
            tuple: (disponible, mensaje)
        """
        try:
            response = requests.get(
                f"http://localhost:11434/api/tags",
                timeout=5
            )
            if response.status_code == 200:
                return True, "Ollama disponible"
            return False, f"Ollama responde con error: {response.status_code}"
        except requests.exceptions.ConnectionError:
            return False, "Ollama no esta ejecutandose. Ejecuta 'ollama serve' en terminal."
        except Exception as e:
            return False, f"Error verificando Ollama: {str(e)}"

    @staticmethod
    def get_available_models() -> List[str]:
        """Obtiene la lista de modelos disponibles en Ollama."""
        try:
            response = requests.get(
                "http://localhost:11434/api/tags",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except:
            return []

    @staticmethod
    def pull_model(model_name: str, progress_callback=None) -> bool:
        """
        Descarga un modelo de Ollama.

        Args:
            model_name: Nombre del modelo a descargar
            progress_callback: Funcion para reportar progreso

        Returns:
            bool: True si la descarga fue exitosa
        """
        try:
            response = requests.post(
                "http://localhost:11434/api/pull",
                json={"name": model_name},
                stream=True,
                timeout=600
            )

            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if progress_callback and 'status' in data:
                        progress_callback(data.get('status', ''))
                    if data.get('status') == 'success':
                        return True
            return True
        except Exception as e:
            print(f"Error descargando modelo: {e}")
            return False

    def set_model(self, model_name: str):
        """Establece el modelo a usar."""
        self.model = model_name

    def query_database(self, query: str) -> Dict[str, Any]:
        """
        Ejecuta una consulta SQL en la base de datos.

        Args:
            query: Consulta SQL (solo SELECT permitido)

        Returns:
            dict: Resultado con columns, data, error
        """
        # Solo permitir SELECT por seguridad
        query_upper = query.strip().upper()
        if not query_upper.startswith('SELECT'):
            return {
                'success': False,
                'error': 'Solo se permiten consultas SELECT',
                'data': []
            }

        try:
            from script.db_connection import get_project_connection

            with get_project_connection(self.user, self.password, self.schema) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                data = cursor.fetchall()
                cursor.close()

                return {
                    'success': True,
                    'columns': columns,
                    'data': data,
                    'row_count': len(data)
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'data': []
            }

    def get_database_schema(self) -> str:
        """Obtiene informacion del esquema de la base de datos."""
        result = self.query_database(f"""
            SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, IS_NULLABLE
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = '{self.schema}'
            ORDER BY TABLE_NAME, ORDINAL_POSITION
        """)

        if not result['success']:
            return f"Error obteniendo esquema: {result['error']}"

        # Formatear como texto
        tables = {}
        for row in result['data']:
            table, column, dtype, nullable = row
            if table not in tables:
                tables[table] = []
            tables[table].append(f"  - {column} ({dtype})")

        schema_text = "Estructura de la base de datos:\n\n"
        for table, columns in tables.items():
            schema_text += f"{table}:\n" + "\n".join(columns) + "\n\n"

        return schema_text

    def get_database_stats(self) -> str:
        """Obtiene estadisticas basicas de la base de datos."""
        stats = []

        # Contar partes
        result = self.query_database("SELECT COUNT(*) FROM tbl_partes")
        if result['success'] and result['data']:
            stats.append(f"Total de partes: {result['data'][0][0]}")

        # Partes por estado
        result = self.query_database("""
            SELECT estado, COUNT(*) as total
            FROM tbl_partes
            GROUP BY estado
        """)
        if result['success'] and result['data']:
            estados = ", ".join([f"{row[0]}: {row[1]}" for row in result['data']])
            stats.append(f"Partes por estado: {estados}")

        # Totales economicos
        result = self.query_database("""
            SELECT
                SUM(presupuesto) as presupuesto_total,
                SUM(certificado) as certificado_total,
                SUM(pendiente) as pendiente_total
            FROM tbl_partes
        """)
        if result['success'] and result['data']:
            row = result['data'][0]
            if row[0]:
                stats.append(f"Presupuesto total: {row[0]:,.2f} EUR")
            if row[1]:
                stats.append(f"Certificado total: {row[1]:,.2f} EUR")
            if row[2]:
                stats.append(f"Pendiente total: {row[2]:,.2f} EUR")

        return "\n".join(stats) if stats else "No se pudieron obtener estadisticas"

    def read_manual(self, manual_type: str = "usuario") -> str:
        """
        Lee el contenido de un manual.

        Args:
            manual_type: usuario, informes, o tecnico

        Returns:
            str: Contenido del manual
        """
        manual_files = {
            "usuario": "docs/manual/Manual_Usuario_v2.0.md",
            "informes": "docs/manual/Manual_Informes_v2.0.md",
            "tecnico": "docs/manual/Manual_Tecnico_v2.0.md"
        }

        file_path = PROJECT_ROOT / manual_files.get(manual_type, manual_files["usuario"])

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return f"Manual '{manual_type}' no encontrado"
        except Exception as e:
            return f"Error leyendo manual: {str(e)}"

    def read_code(self, file_pattern: str) -> str:
        """
        Lee archivos de codigo fuente.

        Args:
            file_pattern: Patron de archivo (ej: "parts_manager", "modulo_db")

        Returns:
            str: Contenido del archivo o lista de archivos encontrados
        """
        import glob

        # Buscar en directorios principales
        search_paths = [
            str(PROJECT_ROOT / "script" / f"*{file_pattern}*.py"),
            str(PROJECT_ROOT / "interface" / f"*{file_pattern}*.py"),
        ]

        found_files = []
        for pattern in search_paths:
            found_files.extend(glob.glob(pattern))

        if not found_files:
            return f"No se encontraron archivos con patron '{file_pattern}'"

        if len(found_files) == 1:
            try:
                with open(found_files[0], 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Limitar tamano para no sobrecargar el contexto
                    if len(content) > 10000:
                        content = content[:10000] + "\n\n... (archivo truncado)"
                    return f"Archivo: {found_files[0]}\n\n{content}"
            except Exception as e:
                return f"Error leyendo archivo: {str(e)}"
        else:
            return "Archivos encontrados:\n" + "\n".join(found_files)

    def chat(self, user_message: str) -> str:
        """
        Envia un mensaje al asistente y obtiene respuesta.

        Args:
            user_message: Mensaje del usuario

        Returns:
            str: Respuesta del asistente
        """
        if not self.model:
            return "Error: No hay modelo seleccionado. Selecciona un modelo primero."

        # Detectar si necesita informacion adicional
        context_additions = []

        lower_msg = user_message.lower()

        # Si pregunta sobre datos/estadisticas
        if any(word in lower_msg for word in ['cuantos', 'total', 'estadisticas', 'datos', 'partes']):
            stats = self.get_database_stats()
            context_additions.append(f"Estadisticas actuales:\n{stats}")

        # Si pregunta sobre esquema/tablas
        if any(word in lower_msg for word in ['tabla', 'columna', 'esquema', 'estructura']):
            schema = self.get_database_schema()
            # Limitar tamano
            if len(schema) > 3000:
                schema = schema[:3000] + "\n... (truncado)"
            context_additions.append(f"Esquema de BD:\n{schema}")

        # Construir mensajes para Ollama
        messages = [
            {"role": "system", "content": self._system_context}
        ]

        # Agregar contexto adicional si existe
        if context_additions:
            context_msg = "\n\n".join(context_additions)
            messages.append({
                "role": "system",
                "content": f"Informacion adicional para responder:\n{context_msg}"
            })

        # Agregar historial (ultimos 10 mensajes)
        for msg in self.conversation_history[-10:]:
            messages.append(msg)

        # Agregar mensaje actual
        messages.append({"role": "user", "content": user_message})

        try:
            response = requests.post(
                f"{self.OLLAMA_API_URL}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False
                },
                timeout=120
            )

            if response.status_code == 200:
                data = response.json()
                assistant_message = data.get('message', {}).get('content', '')

                # Guardar en historial
                self.conversation_history.append({"role": "user", "content": user_message})
                self.conversation_history.append({"role": "assistant", "content": assistant_message})

                return assistant_message
            else:
                return f"Error de Ollama: {response.status_code} - {response.text}"

        except requests.exceptions.Timeout:
            return "Error: La respuesta tardo demasiado. Intenta con una pregunta mas corta."
        except requests.exceptions.ConnectionError:
            return "Error: No se puede conectar con Ollama. Asegurate de que esta ejecutandose."
        except Exception as e:
            return f"Error: {str(e)}"

    def chat_stream(self, user_message: str):
        """
        Envia mensaje y obtiene respuesta en streaming.

        Args:
            user_message: Mensaje del usuario

        Yields:
            str: Fragmentos de la respuesta
        """
        if not self.model:
            yield "Error: No hay modelo seleccionado."
            return

        # Detectar contexto necesario
        context_additions = []
        lower_msg = user_message.lower()

        if any(word in lower_msg for word in ['cuantos', 'total', 'estadisticas', 'datos']):
            stats = self.get_database_stats()
            context_additions.append(f"Estadisticas:\n{stats}")

        # Construir mensajes
        messages = [{"role": "system", "content": self._system_context}]

        if context_additions:
            messages.append({
                "role": "system",
                "content": "\n\n".join(context_additions)
            })

        for msg in self.conversation_history[-10:]:
            messages.append(msg)

        messages.append({"role": "user", "content": user_message})

        try:
            response = requests.post(
                f"{self.OLLAMA_API_URL}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": True
                },
                stream=True,
                timeout=120
            )

            full_response = ""
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if 'message' in data and 'content' in data['message']:
                        chunk = data['message']['content']
                        full_response += chunk
                        yield chunk

            # Guardar en historial
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": full_response})

        except Exception as e:
            yield f"\nError: {str(e)}"

    def clear_history(self):
        """Limpia el historial de conversacion."""
        self.conversation_history.clear()

    def execute_query_from_prompt(self, prompt: str) -> str:
        """
        Intenta extraer y ejecutar una consulta SQL del prompt.

        Args:
            prompt: Texto que puede contener una consulta SQL

        Returns:
            str: Resultado de la consulta formateado
        """
        # Buscar patron de consulta SQL
        import re

        # Patrones comunes de consulta
        patterns = [
            r'SELECT\s+.+\s+FROM\s+.+',
            r'SHOW\s+.+',
        ]

        for pattern in patterns:
            match = re.search(pattern, prompt, re.IGNORECASE | re.DOTALL)
            if match:
                query = match.group(0)
                # Limpiar query
                query = query.split(';')[0].strip()

                result = self.query_database(query)

                if result['success']:
                    if not result['data']:
                        return "La consulta no devolvio resultados."

                    # Formatear resultado como tabla
                    output = f"Resultado ({result['row_count']} filas):\n\n"
                    output += " | ".join(result['columns']) + "\n"
                    output += "-" * 50 + "\n"

                    for row in result['data'][:20]:  # Limitar a 20 filas
                        output += " | ".join(str(v) for v in row) + "\n"

                    if result['row_count'] > 20:
                        output += f"\n... y {result['row_count'] - 20} filas mas"

                    return output
                else:
                    return f"Error en consulta: {result['error']}"

        return None  # No se encontro consulta SQL


# Funcion alternativa usando urllib (no requiere requests)
def _check_ollama_urllib() -> Dict[str, Any]:
    """Verifica Ollama usando urllib (stdlib)."""
    import urllib.request
    import urllib.error

    requirements = {
        'ollama_installed': False,
        'ollama_running': False,
        'models_available': [],
        'recommended_model': None,
        'message': ''
    }

    try:
        req = urllib.request.Request(
            "http://localhost:11434/api/tags",
            headers={'Accept': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                requirements['ollama_installed'] = True
                requirements['ollama_running'] = True
                requirements['models_available'] = [m['name'] for m in data.get('models', [])]

                # Recomendar modelo
                for rec in ['mistral', 'llama3.2', 'llama3.1', 'codellama', 'llama2']:
                    for available in requirements['models_available']:
                        if available.startswith(rec):
                            requirements['recommended_model'] = available
                            break
                    if requirements['recommended_model']:
                        break

                if requirements['models_available']:
                    requirements['message'] = f"Ollama listo. Modelos: {', '.join(requirements['models_available'])}"
                else:
                    requirements['message'] = "Ollama listo pero sin modelos."

    except urllib.error.URLError as e:
        requirements['message'] = f"No se puede conectar con Ollama: {str(e.reason)}"
    except Exception as e:
        requirements['message'] = f"Error: {str(e)}"

    return requirements


# Funcion de utilidad para verificar requisitos
def check_requirements() -> Dict[str, Any]:
    """
    Verifica los requisitos del asistente IA.

    Returns:
        dict: Estado de cada requisito
    """
    # Si requests no esta disponible, usar urllib
    if not REQUESTS_AVAILABLE:
        return _check_ollama_urllib()

    requirements = {
        'ollama_installed': False,
        'ollama_running': False,
        'models_available': [],
        'recommended_model': None,
        'message': ''
    }

    # En Windows con la app de escritorio, el comando puede no estar en PATH
    # Verificamos directamente la API HTTP que es mas confiable
    try:
        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=5
        )
        if response.status_code == 200:
            # Si la API responde, Ollama esta instalado y corriendo
            requirements['ollama_installed'] = True
            requirements['ollama_running'] = True

            # Obtener modelos
            data = response.json()
            requirements['models_available'] = [model['name'] for model in data.get('models', [])]

            # Recomendar modelo
            recommended_models = ['mistral', 'llama3.2', 'llama3.1', 'codellama', 'llama2']
            for rec in recommended_models:
                for available in requirements['models_available']:
                    if available.startswith(rec):
                        requirements['recommended_model'] = available
                        break
                if requirements['recommended_model']:
                    break

            if not requirements['models_available']:
                requirements['message'] = "Ollama listo pero sin modelos. Ejecuta: ollama pull mistral:7b"
            else:
                requirements['message'] = f"Ollama listo. Modelos: {', '.join(requirements['models_available'])}"
        else:
            requirements['message'] = f"Ollama responde con error: {response.status_code}"

    except requests.exceptions.ConnectionError as e:
        requirements['message'] = f"No se puede conectar con Ollama (ConnectionError)"
        # La API no responde - verificar si el comando existe
        try:
            result = subprocess.run(['ollama', '--version'], capture_output=True, text=True, timeout=5)
            requirements['ollama_installed'] = result.returncode == 0
            if requirements['ollama_installed']:
                requirements['message'] = "Ollama instalado pero no ejecutandose. Abre la aplicacion Ollama."
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

    except requests.exceptions.Timeout:
        requirements['message'] = "Ollama no responde (timeout). Reinicia la aplicacion Ollama."

    except Exception as e:
        requirements['message'] = f"Error verificando Ollama: {str(e)}"

    return requirements
