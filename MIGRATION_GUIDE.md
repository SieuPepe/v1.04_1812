# Guía de Migración - Refactorización de Módulos de Base de Datos

## 📋 Resumen

Esta guía explica cómo migrar las funciones existentes en `db_core.py`, `db_projects.py` y `db_partes.py` al nuevo sistema sin valores hardcodeados.

---

## 🎯 Objetivos de la Refactorización

1. ✅ **Eliminar valores hardcodeados** (`host='localhost'`, `port=3307`, `database='manager'`)
2. ✅ **Centralizar configuración** en `db_config.py`
3. ✅ **Reducir código duplicado** usando `db_connection.py`
4. ✅ **Mejorar mantenibilidad** con context managers
5. ✅ **Facilitar testing** con configuración inyectable

---

## 📁 Nuevos Archivos Creados

### 1. `db_config.py`
Configuración centralizada de la base de datos.

**Variables configurables:**
- `DB_HOST` (por defecto: `localhost`)
- `DB_PORT` (por defecto: `3307`)
- `DB_MANAGER_SCHEMA` (por defecto: `manager`)
- `DB_EXAMPLE_SCHEMA` (por defecto: `proyecto_tipo`)

**Uso:**
```python
from script.db_config import get_config

config = get_config()
print(config.host)            # 'localhost'
print(config.port)            # 3307
print(config.manager_schema)  # 'manager'
```

### 2. `db_connection.py`
Clases y funciones para manejar conexiones con context managers.

**Funciones principales:**
- `get_connection(user, password, database=None)` - Conexión genérica
- `get_manager_connection(user, password)` - Conexión al esquema manager
- `get_project_connection(user, password, project_code)` - Conexión a proyecto
- `execute_query(...)` - Ejecutar SELECT
- `execute_update(...)` - Ejecutar UPDATE/DELETE
- `execute_insert(...)` - Ejecutar INSERT y retornar ID
- `execute_transaction(...)` - Ejecutar múltiples queries en transacción

### 3. `.env.example`
Plantilla para configurar variables de entorno.

### 4. `.gitignore`
Protege el archivo `.env` para no subirlo al repositorio.

---

## 🔄 Patrones de Migración

### Patrón 1: Conexión Simple

**❌ ANTES:**
```python
def mi_funcion(user, password):
    conexion = mysql.connector.connect(
        host='localhost',      # ❌ Hardcodeado
        port=3307,             # ❌ Hardcodeado
        user=user,
        password=password
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT ...")
    results = cursor.fetchall()
    conexion.close()
    return results
```

**✅ DESPUÉS:**
```python
from script.db_connection import get_connection

def mi_funcion(user, password):
    with get_connection(user, password) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ...")
        results = cursor.fetchall()
        cursor.close()
        return results
```

---

### Patrón 2: Conexión al Esquema Manager

**❌ ANTES:**
```python
def get_clientes(user, password):
    conexion = mysql.connector.connect(
        host='localhost',      # ❌ Hardcodeado
        port=3307,             # ❌ Hardcodeado
        database='manager',    # ❌ Hardcodeado
        user=user,
        password=password
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM tbl_cliente")
    results = cursor.fetchall()
    conexion.close()
    return results
```

**✅ DESPUÉS:**
```python
from script.db_connection import get_manager_connection

def get_clientes(user, password):
    with get_manager_connection(user, password) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbl_cliente")
        results = cursor.fetchall()
        cursor.close()
        return results
```

---

### Patrón 3: Conexión a Proyecto Específico

**❌ ANTES:**
```python
def get_partes(user, password, schema):
    conexion = mysql.connector.connect(
        host='localhost',      # ❌ Hardcodeado
        port=3307,             # ❌ Hardcodeado
        database=schema,
        user=user,
        password=password
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM tbl_partes")
    results = cursor.fetchall()
    conexion.close()
    return results
```

**✅ DESPUÉS:**
```python
from script.db_connection import get_project_connection

def get_partes(user, password, project_code):
    with get_project_connection(user, password, project_code) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbl_partes")
        results = cursor.fetchall()
        cursor.close()
        return results
```

---

### Patrón 4: Usar Helpers para Consultas Simples

**✅ OPCIÓN SIMPLIFICADA:**
```python
from script.db_connection import execute_query
from script.db_config import get_config

def get_clientes(user, password):
    config = get_config()
    query = "SELECT * FROM tbl_cliente"
    return execute_query(user, password, query, database=config.manager_schema)
```

---

### Patrón 5: INSERT con Transacción

**❌ ANTES:**
```python
def add_item(user, password, data):
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        database='manager',
        user=user,
        password=password
    )
    conexion.start_transaction()
    cursor = conexion.cursor()

    sql_query = "INSERT INTO table (col1, col2) VALUES (%s, %s)"
    cursor.execute(sql_query, (data['col1'], data['col2']))

    conexion.commit()
    conexion.close()
```

**✅ DESPUÉS:**
```python
from script.db_connection import get_manager_connection
from mysql.connector import Error

def add_item(user, password, data):
    with get_manager_connection(user, password) as conn:
        cursor = conn.cursor()
        try:
            conn.start_transaction()

            sql_query = "INSERT INTO table (col1, col2) VALUES (%s, %s)"
            cursor.execute(sql_query, (data['col1'], data['col2']))
            new_id = cursor.lastrowid

            conn.commit()
            cursor.close()
            return new_id

        except Error as e:
            conn.rollback()
            cursor.close()
            raise e
```

---

### Patrón 6: Referenciar Esquemas Dinámicamente

**❌ ANTES:**
```python
cursor.execute("SELECT * FROM manager.tbl_cliente")
```

**✅ DESPUÉS:**
```python
from script.db_config import get_config

config = get_config()
cursor.execute(f"SELECT * FROM {config.manager_schema}.tbl_cliente")
```

---

## 📝 Checklist de Migración por Función

Para cada función en `db_core.py`, `db_projects.py`, `db_partes.py`:

- [ ] **Paso 1:** Importar helpers necesarios
  ```python
  from script.db_connection import get_connection, get_manager_connection, get_project_connection
  from script.db_config import get_config
  from mysql.connector import Error
  ```

- [ ] **Paso 2:** Reemplazar creación de conexión por context manager apropiado

- [ ] **Paso 3:** Reemplazar referencias hardcodeadas:
  - `'localhost'` → `config.host`
  - `3307` → `config.port`
  - `'manager'` → `config.manager_schema`
  - `'proyecto_tipo'` → `config.example_schema`

- [ ] **Paso 4:** Eliminar `conexion.close()` (se hace automático con `with`)

- [ ] **Paso 5:** Añadir manejo de errores con try/except si hay transacciones

- [ ] **Paso 6:** Probar la función migrada

---

## ⚙️ Configuración del Entorno

### Opción 1: Valores por defecto
No hacer nada. El sistema usará:
- Host: `localhost`
- Port: `3307`
- Manager schema: `manager`
- Example schema: `proyecto_tipo`

### Opción 2: Variables de entorno
1. Copiar `.env.example` a `.env`:
   ```bash
   cp .env.example .env
   ```

2. Editar `.env` con tus valores:
   ```bash
   DB_HOST=mi-servidor.com
   DB_PORT=3306
   DB_MANAGER_SCHEMA=gestion
   DB_EXAMPLE_SCHEMA=plantilla
   ```

3. Las variables se cargarán automáticamente

---

## 🧪 Testing

### Probar configuración:
```python
from script.db_config import get_config

config = get_config()
print(f"Host: {config.host}")
print(f"Port: {config.port}")
print(f"Manager: {config.manager_schema}")
```

### Probar conexión:
```python
from script.db_connection import get_connection

try:
    with get_connection('user', 'password') as conn:
        print("✅ Conexión exitosa")
except Exception as e:
    print(f"❌ Error: {e}")
```

---

## 📚 Orden Recomendado de Migración

1. **Primero:** Funciones simples de consulta (SELECT)
2. **Segundo:** Funciones de inserción (INSERT)
3. **Tercero:** Funciones de actualización (UPDATE/DELETE)
4. **Cuarto:** Funciones complejas con múltiples transacciones
5. **Quinto:** Funciones que crean esquemas y vistas

---

## 🔍 Ejemplos Completos

Ver archivo: `script/db_core_refactored_example.py` para ejemplos detallados de:
- `login_db` - Autenticación
- `get_ccaa_bd` - Consulta al esquema manager
- `get_table_schemas_db` - Consulta a esquema dinámico
- `add_customer_item` - INSERT con transacción
- `create_view_catalog` - Creación de vistas en proyecto

---

## ⚠️ Importante

1. **NO subir el archivo `.env` al repositorio** (ya está en `.gitignore`)
2. **Probar cada función migrada** antes de usarla en producción
3. **Mantener compatibilidad** durante la transición (ambos sistemas pueden coexistir)
4. **Documentar cambios** en las funciones migradas

---

## 🎯 Próximos Pasos

1. ✅ Configurar tu archivo `.env` con tus credenciales
2. ✅ Probar las funciones ejemplo en `db_core_refactored_example.py`
3. ✅ Migrar funciones una por una siguiendo los patrones
4. ✅ Actualizar tests si los tienes
5. ✅ Eliminar código antiguo cuando todo esté migrado

---

## 📞 Soporte

Si tienes dudas sobre cómo migrar una función específica, consulta los ejemplos en:
- `script/db_core_refactored_example.py`
- Esta guía en la sección de patrones
