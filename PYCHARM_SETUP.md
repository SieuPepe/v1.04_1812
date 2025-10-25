# Guía de Configuración en PyCharm

Esta guía te ayudará a configurar el proyecto refactorizado en PyCharm para trabajar correctamente con los nuevos módulos de base de datos.

---

## 📁 1. Abrir el Proyecto en PyCharm

### Opción A: Abrir proyecto existente
1. Abre PyCharm
2. `File` → `Open`
3. Navega a `/home/user/v1.04_1812` (o tu ruta local)
4. Selecciona la carpeta `v1.04_1812` (la interna, donde está `script/`)
5. Click en `OK`

### Opción B: Clonar desde Git (si usas repositorio remoto)
1. `File` → `New` → `Project from Version Control`
2. Ingresa la URL del repositorio
3. Selecciona la rama `claude/refactor-db-module-011CUTX3NSwphiJqMH4a8vW3`

---

## 🐍 2. Configurar el Intérprete de Python

### Paso 1: Verificar versión de Python
El proyecto requiere **Python 3.7+**

1. `File` → `Settings` (Windows/Linux) o `PyCharm` → `Preferences` (Mac)
2. `Project: v1.04_1812` → `Python Interpreter`
3. Verifica que tienes Python 3.7 o superior

### Paso 2: Crear entorno virtual (recomendado)
```bash
# Desde la terminal de PyCharm o terminal externa
cd /home/user/v1.04_1812/v1.04_1812
python3 -m venv venv

# Activar el entorno virtual
# En Linux/Mac:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### Paso 3: Seleccionar el intérprete en PyCharm
1. `File` → `Settings` → `Project` → `Python Interpreter`
2. Click en el ⚙️ → `Add`
3. Selecciona `Virtualenv Environment` → `Existing environment`
4. Navega a `v1.04_1812/venv/bin/python` (o `venv\Scripts\python.exe` en Windows)
5. Click `OK`

---

## 📦 3. Instalar Dependencias

### Dependencias requeridas:

```bash
# Con el entorno virtual activado:
pip install mysql-connector-python
pip install python-dotenv  # Opcional pero recomendado para .env
```

### Crear requirements.txt (opcional):
```bash
# Generar archivo de dependencias
pip freeze > requirements.txt
```

Contenido típico de `requirements.txt`:
```
mysql-connector-python==8.2.0
python-dotenv==1.0.0
```

---

## ⚙️ 4. Configurar Variables de Entorno

### Opción A: Usar archivo .env (Recomendado)

1. **Crear archivo .env en el directorio raíz del proyecto:**
   ```
   v1.04_1812/
   ├── .env          ← Crear aquí
   ├── .env.example
   └── script/
   ```

2. **Copiar contenido de .env.example:**
   ```bash
   cp .env.example .env
   ```

3. **Editar .env con tus valores:**
   ```bash
   # Configuración de Base de Datos
   DB_HOST=localhost
   DB_PORT=3307
   DB_MANAGER_SCHEMA=manager
   DB_EXAMPLE_SCHEMA=proyecto_tipo
   ```

4. **Instalar python-dotenv:**
   ```bash
   pip install python-dotenv
   ```

5. **Modificar db_config.py para cargar .env automáticamente:**

   Abre `v1.04_1812/script/db_config.py` y añade al principio:
   ```python
   import os
   from dotenv import load_dotenv
   from pathlib import Path

   # Cargar .env desde la raíz del proyecto
   env_path = Path(__file__).parent.parent / '.env'
   load_dotenv(dotenv_path=env_path)
   ```

### Opción B: Configurar en PyCharm (Run Configurations)

1. `Run` → `Edit Configurations`
2. Selecciona tu configuración de ejecución (o crea una nueva)
3. En `Environment variables`, click en el icono de carpeta
4. Añade las variables:
   ```
   DB_HOST=localhost
   DB_PORT=3307
   DB_MANAGER_SCHEMA=manager
   DB_EXAMPLE_SCHEMA=proyecto_tipo
   ```
5. Click `OK`

---

## 🔧 5. Marcar Directorio como Sources Root

Para que los imports funcionen correctamente:

1. En el explorador de proyectos, click derecho en la carpeta `v1.04_1812/script`
2. `Mark Directory as` → `Sources Root`

Esto permite que los imports relativos funcionen:
```python
from .db_config import get_config
from .db_connection import get_connection
```

---

## 🎨 6. Configurar Code Style (Opcional)

Para mantener el estilo del código:

1. `File` → `Settings` → `Editor` → `Code Style` → `Python`
2. Configuración recomendada:
   - Tab size: 4
   - Indent: 4
   - Continuation indent: 8
   - Use tab character: ❌ (usar espacios)

---

## 🔍 7. Verificar Configuración

### Crear archivo de prueba: `test_imports.py`

```python
"""
Archivo de prueba para verificar que los imports funcionan correctamente
"""

# Prueba 1: Importar módulos base
print("Prueba 1: Importando módulos base...")
try:
    from script.db_config import get_config
    from script.db_connection import get_connection, get_manager_connection, get_project_connection
    print("✅ Módulos base importados correctamente")
except ImportError as e:
    print(f"❌ Error importando módulos base: {e}")

# Prueba 2: Verificar configuración
print("\nPrueba 2: Verificando configuración...")
try:
    config = get_config()
    print(f"✅ Host: {config.host}")
    print(f"✅ Puerto: {config.port}")
    print(f"✅ Schema Manager: {config.manager_schema}")
except Exception as e:
    print(f"❌ Error en configuración: {e}")

# Prueba 3: Importar desde modulo_db (compatibilidad)
print("\nPrueba 3: Importando desde modulo_db...")
try:
    from script.modulo_db import login_db, add_project_item, add_parte_with_code
    print("✅ Funciones importadas desde modulo_db correctamente")
except ImportError as e:
    print(f"❌ Error importando desde modulo_db: {e}")

# Prueba 4: Verificar que mysql.connector está disponible
print("\nPrueba 4: Verificando mysql.connector...")
try:
    import mysql.connector
    print(f"✅ mysql.connector versión: {mysql.connector.__version__}")
except ImportError:
    print("❌ mysql.connector no está instalado")
    print("   Instalar con: pip install mysql-connector-python")

print("\n" + "="*60)
print("Verificación completada")
print("="*60)
```

**Ejecutar el test:**
1. Click derecho en `test_imports.py`
2. `Run 'test_imports'`
3. Verificar que todas las pruebas pasan ✅

---

## 📝 8. Uso en tu Código

### Ejemplo de uso desde tu aplicación principal:

```python
# Opción 1: Importar directamente desde módulos especializados
from script.db_core import login_db, get_schemas_db, create_schemas_db
from script.db_projects import add_project_item, mod_project_item
from script.db_partes import add_parte_with_code

# Opción 2: Importar desde modulo_db (mantiene compatibilidad)
from script.modulo_db import (
    login_db,
    get_schemas_db,
    add_project_item,
    add_parte_with_code
)

# Uso normal
user = "admin"
password = "mi_password"

# Login
conexion, error = login_db(user, password)
if error:
    print(f"Error de conexión: {error}")
else:
    print("Conexión exitosa")

# Obtener schemas
schemas = get_schemas_db(user, password)
print(f"Schemas disponibles: {schemas}")
```

---

## 🐛 9. Solución de Problemas Comunes

### Problema 1: "ModuleNotFoundError: No module named 'script'"

**Solución:**
- Asegúrate de marcar `v1.04_1812/script` como Sources Root
- Verifica que estés ejecutando desde el directorio correcto
- En PyCharm: `Mark Directory as` → `Sources Root`

### Problema 2: "No module named 'mysql'"

**Solución:**
```bash
pip install mysql-connector-python
```

### Problema 3: Los imports relativos no funcionan

**Solución:**
- Verifica que el directorio `script` tenga un archivo `__init__.py`
- Si no existe, créalo vacío:
  ```bash
  touch v1.04_1812/script/__init__.py
  ```

### Problema 4: Variables de entorno no se cargan

**Solución:**
- Verifica que `.env` esté en el directorio correcto
- Asegúrate de tener `python-dotenv` instalado
- Modifica `db_config.py` para cargar `.env` explícitamente

### Problema 5: PyCharm no reconoce las funciones

**Solución:**
- `File` → `Invalidate Caches / Restart`
- Espera a que PyCharm reindexe el proyecto

---

## 🔐 10. Seguridad y Mejores Prácticas

### ✅ Hacer:
- ✅ Usar archivo `.env` para credenciales
- ✅ Añadir `.env` a `.gitignore`
- ✅ Usar entorno virtual para dependencias
- ✅ Mantener `requirements.txt` actualizado

### ❌ NO Hacer:
- ❌ Commitear archivo `.env` al repositorio
- ❌ Hardcodear contraseñas en el código
- ❌ Compartir credenciales de producción

---

## 📚 11. Recursos Adicionales

- **Documentación del proyecto:**
  - `DATABASE_README.md` - Guía completa del sistema
  - `MIGRATION_GUIDE.md` - Patrones de refactorización
  - `VERIFICATION_REPORT.md` - Reporte de verificación

- **Archivos de configuración:**
  - `.env.example` - Plantilla de variables de entorno
  - `requirements.txt` - Dependencias del proyecto

---

## 🚀 12. Próximos Pasos

1. ✅ Configurar PyCharm según esta guía
2. ✅ Crear archivo `.env` con tus credenciales
3. ✅ Ejecutar `test_imports.py` para verificar
4. ✅ Revisar `DATABASE_README.md` para entender la arquitectura
5. 🔄 Comenzar a usar los nuevos módulos en tu código

---

## 💡 Tips de PyCharm

### Autocompletado
PyCharm ahora autocompletará las funciones correctamente. Escribe:
```python
from script.modulo_db import log
```
Y PyCharm sugerirá `login_db`

### Navegación rápida
- `Ctrl+Click` (o `Cmd+Click` en Mac) en una función para ir a su definición
- `Ctrl+B` para ir a la declaración
- `Ctrl+Alt+B` para ir a la implementación

### Refactoring seguro
- Si renombras una función, PyCharm actualizará todas las referencias automáticamente
- `Shift+F6` para renombrar de forma segura

---

**¿Necesitas ayuda?**
Consulta `DATABASE_README.md` o `MIGRATION_GUIDE.md` para más información.
