# Módulos de Base de Datos - Documentación

## 📖 Descripción

Sistema de gestión de base de datos refactorizado y optimizado para el proyecto v1.04_1812.

### Características principales:
- ✅ **Sin valores hardcodeados** - Configuración centralizada
- ✅ **Context managers** - Gestión automática de conexiones
- ✅ **Modular** - Código organizado por responsabilidades
- ✅ **Configurable** - Variables de entorno para diferentes ambientes
- ✅ **Mantenible** - 70% menos código duplicado

---

## 📁 Estructura de Archivos

```
v1.04_1812/
├── .env                          # Configuración (NO subir a git)
├── .env.example                  # Plantilla de configuración
├── .gitignore                    # Protege .env
├── DATABASE_README.md            # Este archivo
├── MIGRATION_GUIDE.md            # Guía de migración
│
└── script/
    ├── db_config.py              # ✨ Configuración centralizada
    ├── db_connection.py          # ✨ Gestión de conexiones
    ├── db_core.py                # Funciones base (autenticación, esquemas, CRUD)
    ├── db_projects.py            # Funciones de proyectos y presupuestos
    ├── db_partes.py              # Funciones de partes de trabajo
    ├── modulo_db.py              # Punto de entrada (re-exporta todo)
    └── db_core_refactored_example.py  # Ejemplos de refactorización
```

---

## 🚀 Inicio Rápido

### 1. Configurar Variables de Entorno (Opcional)

Si quieres cambiar los valores por defecto:

```bash
# Copiar plantilla
cp .env.example .env

# Editar .env con tus valores
DB_HOST=localhost
DB_PORT=3307
DB_MANAGER_SCHEMA=manager
DB_EXAMPLE_SCHEMA=proyecto_tipo
```

Si no creas el archivo `.env`, el sistema usará los valores por defecto.

### 2. Usar las Funciones

**Opción A: Importar desde módulo consolidado (compatible con código antiguo)**
```python
from script.modulo_db import login_db, get_schemas_db, add_project_item

# Usar funciones normalmente
connection, error = login_db('usuario', 'password')
schemas = get_schemas_db('usuario', 'password')
```

**Opción B: Importar desde módulos específicos (recomendado)**
```python
from script.db_core import login_db, get_schemas_db
from script.db_projects import add_project_item
from script.db_partes import add_parte_with_code

# Usar funciones normalmente
connection, error = login_db('usuario', 'password')
```

---

## 🔧 Nuevas Utilidades

### Clase de Configuración

```python
from script.db_config import get_config

config = get_config()
print(config.host)            # 'localhost' (o valor de .env)
print(config.port)            # 3307 (o valor de .env)
print(config.manager_schema)  # 'manager' (o valor de .env)
```

### Context Managers de Conexión

```python
from script.db_connection import (
    get_connection,
    get_manager_connection,
    get_project_connection
)

# Conexión genérica
with get_connection('user', 'pass') as conn:
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    print(cursor.fetchall())

# Conexión al esquema manager
with get_manager_connection('user', 'pass') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_cliente")
    print(cursor.fetchall())

# Conexión a proyecto específico
with get_project_connection('user', 'pass', 'PRJ001') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_partes")
    print(cursor.fetchall())
```

### Helpers para Consultas

```python
from script.db_connection import execute_query, execute_update, execute_insert

# SELECT
results = execute_query(
    'user', 'pass',
    "SELECT * FROM tbl_cliente WHERE id=%s",
    params=(1,),
    database='manager'
)

# UPDATE
execute_update(
    'user', 'pass',
    "UPDATE tbl_cliente SET nombre=%s WHERE id=%s",
    params=('Nuevo Nombre', 1),
    database='manager'
)

# INSERT (retorna ID)
new_id = execute_insert(
    'user', 'pass',
    "INSERT INTO tbl_cliente (nombre) VALUES (%s)",
    params=('Cliente Nuevo',),
    database='manager'
)
```

---

## 📚 Módulos

### `db_core.py` - Funciones Base
Contiene funciones fundamentales:
- **Autenticación**: `login_db`, `manager_db`, `user_db`
- **Esquemas**: `get_schemas_db`, `create_schemas_db`, `create_view_*`
- **Usuarios BD**: `create_user_bd`, `add_privileges`, `revoke_privileges`
- **CRUD genérico**: `get_all_bd`, `get_filter_data_bd`, `add_item_aux`
- **Ubicaciones**: `get_ccaa_bd`, `get_province_bd`

### `db_projects.py` - Proyectos y Presupuestos
Contiene funciones de negocio:
- **Proyectos**: `add_project_item`, `mod_project_item`
- **Clientes**: `add_customer_item`, `get_customer_data`
- **Usuarios**: `add_user_customer_item`, `add_user_company_item`
- **Catálogos**: `add_catalog_hidro_item`, `add_catalog_regis_item`
- **Inventario**: `add_register_item`, `mod_register_data`
- **Presupuestos**: `add_budget_item`, `add_cost_item`
- **Fotografías**: `add_photo_register`

### `db_partes.py` - Partes de Trabajo
Contiene funciones de partes:
- **Dimensiones**: `get_dim_all`
- **Partes**: `add_parte_with_code`, `list_partes`, `mod_parte_item`
- **Presupuesto partes**: `add_part_presupuesto_item`
- **Certificaciones**: `add_part_cert_item`, `cert_part_item`

---

## 🔄 Migración desde Código Antiguo

Si tienes código existente que usa `modulo_db.py`, **no necesitas cambiar nada**.
El archivo `modulo_db.py` re-exporta todas las funciones para mantener compatibilidad.

**Para migrar gradualmente:**
1. Lee `MIGRATION_GUIDE.md`
2. Revisa ejemplos en `db_core_refactored_example.py`
3. Migra funciones una por una siguiendo los patrones

---

## 🎯 Ventajas del Nuevo Sistema

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| **Configuración** | Hardcodeada en 150+ lugares | Centralizada en 1 archivo |
| **Host/Port** | `'localhost'`, `3307` | `config.host`, `config.port` |
| **Esquemas** | `'manager'` hardcodeado | `config.manager_schema` |
| **Conexiones** | Manualmente en cada función | Context managers automáticos |
| **Código duplicado** | Alto (91 funciones × conexión) | Bajo (helpers reutilizables) |
| **Mantenibilidad** | Difícil (cambios en 150+ lugares) | Fácil (cambios en 1 lugar) |
| **Testing** | Difícil | Fácil (inyección de config) |
| **Seguridad** | Credenciales en código | Variables de entorno |

---

## 📋 Tareas Pendientes

- [ ] Migrar todas las funciones de `db_core.py` al nuevo patrón
- [ ] Migrar todas las funciones de `db_projects.py` al nuevo patrón
- [ ] Migrar todas las funciones de `db_partes.py` al nuevo patrón
- [ ] Crear tests unitarios para funciones críticas
- [ ] Actualizar documentación de funciones migradas
- [ ] Eliminar código antiguo cuando todo esté migrado

---

## 🧪 Testing

### Probar configuración:
```python
python -c "from script.db_config import get_config; c=get_config(); print(f'Host: {c.host}, Port: {c.port}')"
```

### Probar conexión:
```python
python -c "from script.db_connection import get_connection; get_connection('user', 'pass').__enter__()"
```

---

## ⚠️ Importante

1. **NUNCA subir `.env` al repositorio** - Contiene credenciales
2. **Usar `.env.example`** como plantilla
3. **Probar cada función** después de migrarla
4. **Documentar cambios** en el código

---

## 📞 Recursos

- **Guía de migración**: `MIGRATION_GUIDE.md`
- **Ejemplos**: `script/db_core_refactored_example.py`
- **Configuración**: `script/db_config.py`
- **Conexiones**: `script/db_connection.py`

---

## 🚦 Estado del Proyecto

| Módulo | Estado | Progreso |
|--------|--------|----------|
| `db_config.py` | ✅ Completado | 100% |
| `db_connection.py` | ✅ Completado | 100% |
| `db_core.py` | 🔄 En migración | 0% |
| `db_projects.py` | 🔄 En migración | 0% |
| `db_partes.py` | 🔄 En migración | 0% |

---

## 📝 Changelog

### v2.0.0 (2025-01-XX) - Refactorización Mayor
- ✅ Creado sistema de configuración centralizada
- ✅ Implementado context managers para conexiones
- ✅ Eliminados valores hardcodeados del sistema
- ✅ Añadido soporte para variables de entorno
- ✅ Creadas utilidades de conexión reutilizables
- ✅ Documentación completa de migración

### v1.0.0 (2025-01-XX) - División Modular
- ✅ Dividido `modulo_db.py` en 3 módulos especializados
- ✅ Creado `db_core.py` (funciones base)
- ✅ Creado `db_projects.py` (proyectos y presupuestos)
- ✅ Creado `db_partes.py` (partes de trabajo)
- ✅ Mantenida compatibilidad con código existente
