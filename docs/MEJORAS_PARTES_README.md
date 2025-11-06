# MEJORAS DE ÓRDENES DE TRABAJO (PARTES) - FASE 1

## 📋 RESUMEN

Implementación de la **Opción A** del plan de mejoras: campos adicionales en órdenes de trabajo (partes) basados en las funcionalidades de la Base de Datos Access de Certificaciones UTE.

**Estado**: ✅ Base de datos COMPLETA | ⏳ Interfaces PENDIENTE

---

## 🎯 OBJETIVO

Mejorar la gestión de partes/órdenes de trabajo añadiendo:
- Título descriptivo
- Descripciones larga y corta
- Fechas de inicio, fin y prevista
- Estados (Pendiente, En curso, Finalizada, Cancelada, Suspendida)
- Localización textual
- Referencia a municipio

---

## 📦 ARCHIVOS INCLUIDOS

### 1. `script/mejoras_tabla_partes.sql`
Script SQL completo para migración de base de datos.

**Características:**
- ✅ Idempotente (se puede ejecutar múltiples veces sin errores)
- ✅ Crea tabla `tbl_parte_estados`
- ✅ Añade 11 campos nuevos a `tbl_partes`
- ✅ Crea triggers para sincronización automática
- ✅ Crea vista `vw_partes_completo`
- ✅ Crea índices optimizados
- ✅ Incluye script de verificación

**Tabla tbl_parte_estados:**
```sql
+----+-------------+--------------------------------+-------+--------+
| id | nombre      | descripcion                    | orden | activo |
+----+-------------+--------------------------------+-------+--------+
|  1 | Pendiente   | Parte pendiente de iniciar     |     1 | TRUE   |
|  2 | En curso    | Parte en ejecución             |     2 | TRUE   |
|  3 | Finalizada  | Parte completada con éxito     |     3 | TRUE   |
|  4 | Cancelada   | Parte cancelada                |     4 | TRUE   |
|  5 | Suspendida  | Parte temporalmente suspendida |     5 | TRUE   |
+----+-------------+--------------------------------+-------+--------+
```

**Nuevos campos en tbl_partes:**
```sql
-- Campos descriptivos
titulo                VARCHAR(255)   -- Título descriptivo obligatorio
descripcion_larga     TEXT           -- Descripción detallada
descripcion_corta     VARCHAR(100)   -- Resumen para listados

-- Campos de fechas
fecha_inicio          DATE           -- Fecha de inicio del trabajo
fecha_fin             DATE           -- Fecha real de finalización
fecha_prevista_fin    DATE           -- Fecha prevista de finalización

-- Campos de estado
id_estado             INT            -- FK a tbl_parte_estados
finalizada            BOOLEAN        -- Indicador booleano (sincronizado con estado)

-- Campos de ubicación
localizacion          VARCHAR(255)   -- Ubicación textual
id_municipio          INT            -- FK a tbl_municipios
```

---

### 2. `script/migrate_partes_mejoras.py`
Script Python para aplicar la migración a todos los proyectos automáticamente.

**Características:**
- ✅ Detecta automáticamente todos los esquemas de proyecto
- ✅ Excluye esquemas de sistema (mysql, information_schema, manager)
- ✅ Ejecución idempotente
- ✅ Modo dry-run para simulación
- ✅ Reporte detallado de éxito/errores por esquema
- ✅ Sin valores hardcodeados (usa db_config)

**Uso:**

```bash
# Aplicar a todos los proyectos
python script/migrate_partes_mejoras.py --user admin --password tu_password

# Aplicar a un proyecto específico
python script/migrate_partes_mejoras.py --user admin --password tu_password --schema proyecto_especifico

# Simular sin ejecutar (dry-run)
python script/migrate_partes_mejoras.py --user admin --password tu_password --dry-run
```

**Ejemplo de salida:**
```
================================================================================
  MIGRACIÓN: Mejoras de Órdenes de Trabajo (tbl_partes)
================================================================================

📄 Leyendo script SQL: script/mejoras_tabla_partes.sql
   ✅ Script cargado (28456 caracteres)

🔍 Detectando esquemas de proyectos...
   ✅ Encontrados 5 esquemas

🚀 Iniciando migración...

[1/5] cert_dev... ✅ Completado exitosamente
[2/5] proyecto_agua... ✅ Completado exitosamente
[3/5] proyecto_saneamiento... ✅ Completado exitosamente
[4/5] plantilla_proyecto... ⏭️  OMITIDO: Tabla tbl_partes no existe
[5/5] test_schema... ✅ Completado exitosamente

================================================================================
  RESUMEN DE MIGRACIÓN
================================================================================
  ✅ Exitosos:  4
  ⏭️  Omitidos:  1
  ❌ Errores:   0
  📊 Total:     5
================================================================================

🎉 ¡Migración completada exitosamente!
```

---

### 3. `script/db_partes.py` (MODIFICADO)
Añadidas 4 funciones nuevas con soporte completo para los nuevos campos.

#### **Función: `add_parte_mejorado()`**

Crea un parte con todos los campos mejorados.

**Firma:**
```python
def add_parte_mejorado(
    user: str, password: str, schema: str,
    ot_id: int, red_id: int, tipo_trabajo_id: int, cod_trabajo_id: int,
    titulo: str = None,
    descripcion: str = None,
    descripcion_larga: str = None,
    descripcion_corta: str = None,
    fecha_inicio: str = None,
    fecha_fin: str = None,
    fecha_prevista_fin: str = None,
    id_estado: int = 1,
    finalizada: bool = False,
    localizacion: str = None,
    id_municipio: int = None
) -> tuple[int, str]:
    """Retorna: (id, codigo)"""
```

**Ejemplo de uso:**
```python
from script.modulo_db import add_parte_mejorado

new_id, codigo = add_parte_mejorado(
    user='admin',
    password='pass',
    schema='cert_dev',
    ot_id=1,
    red_id=2,
    tipo_trabajo_id=3,
    cod_trabajo_id=4,
    titulo='Reparación de fuga en Llodio',
    descripcion_corta='Fuga en tubería principal',
    descripcion_larga='Se detectó fuga importante en tubería principal de DN 300mm...',
    fecha_inicio='2025-10-29',
    fecha_prevista_fin='2025-10-30',
    id_estado=2,  # En curso
    localizacion='Calle Mayor, 45, Llodio',
    id_municipio=123
)

print(f"Parte creado: {codigo}")  # PT-00042
```

#### **Función: `mod_parte_mejorado()`**

Modifica un parte existente. Solo actualiza los campos que se pasan (no-None).

**Firma:**
```python
def mod_parte_mejorado(
    user: str, password: str, schema: str,
    parte_id: int,
    # ... mismos parámetros que add_parte_mejorado (todos opcionales)
) -> str:
    """Retorna: "ok" si exitoso, mensaje de error si falla"""
```

**Ejemplo de uso:**
```python
from script.modulo_db import mod_parte_mejorado

result = mod_parte_mejorado(
    user='admin',
    password='pass',
    schema='cert_dev',
    parte_id=42,
    id_estado=3,  # Cambiar a Finalizada
    fecha_fin='2025-10-29'
)

if result == "ok":
    print("Parte actualizado correctamente")
```

#### **Función: `get_estados_parte()`**

Obtiene la lista de estados disponibles.

**Ejemplo de uso:**
```python
from script.modulo_db import get_estados_parte

estados = get_estados_parte('admin', 'pass', 'cert_dev')
for id, nombre, descripcion, orden in estados:
    print(f"{id}: {nombre} - {descripcion}")

# Output:
# 1: Pendiente - Parte pendiente de iniciar
# 2: En curso - Parte en ejecución
# 3: Finalizada - Parte completada con éxito
# 4: Cancelada - Parte cancelada
```

#### **Función: `list_partes_mejorado()`**

Lista partes con todos los campos nuevos.

**Ejemplo de uso:**
```python
from script.modulo_db import list_partes_mejorado

partes = list_partes_mejorado('admin', 'pass', 'cert_dev', limit=10)
for parte in partes:
    print(f"{parte['codigo']}: {parte['titulo']}")
    print(f"  Estado: {parte['estado']}")
    print(f"  Fechas: {parte['fecha_inicio']} → {parte['fecha_fin']}")
    print(f"  Localización: {parte['localizacion']}")
    print(f"  Duración: {parte['dias_duracion']} días")
```

---

### 4. `script/modulo_db.py` (MODIFICADO)
Exporta las 4 nuevas funciones para uso en toda la aplicación.

---

## 🔧 INSTALACIÓN Y USO

### Paso 1: Aplicar Migración a Proyectos Existentes

```bash
# Navegar al directorio del proyecto
cd /ruta/a/v1.04_1812

# Ejecutar migración (reemplazar credenciales)
python script/migrate_partes_mejoras.py --user TU_USUARIO --password TU_PASSWORD
```

⚠️ **IMPORTANTE**: Hacer backup de la base de datos antes de ejecutar la migración.

```bash
# Backup de todos los esquemas
mysqldump -u usuario -p --all-databases > backup_antes_migracion.sql

# Backup de un esquema específico
mysqldump -u usuario -p nombre_esquema > backup_esquema.sql
```

### Paso 2: Verificar Migración

```bash
# Conectar a MySQL
mysql -u usuario -p

# Usar esquema del proyecto
USE cert_dev;

# Verificar nueva tabla
DESCRIBE tbl_parte_estados;
SELECT * FROM tbl_parte_estados;

# Verificar nuevos campos
DESCRIBE tbl_partes;

# Verificar vista
SELECT * FROM vw_partes_completo LIMIT 5;
```

### Paso 3: Usar Nuevas Funciones en Código

```python
# Importar funciones
from script.modulo_db import (
    add_parte_mejorado,
    mod_parte_mejorado,
    get_estados_parte,
    list_partes_mejorado
)

# O mantener compatibilidad con código antiguo
from script.modulo_db import add_parte_with_code  # Función antigua sigue funcionando
```

---

## 🧪 PRUEBAS

### Test Manual en Python

```python
#!/usr/bin/env python3
"""Test de funciones mejoradas de partes"""

from script.modulo_db import (
    add_parte_mejorado,
    mod_parte_mejorado,
    get_estados_parte,
    list_partes_mejorado
)

USER = 'admin'
PASSWORD = 'tu_password'
SCHEMA = 'cert_dev'

# Test 1: Obtener estados
print("Test 1: Obtener estados")
estados = get_estados_parte(USER, PASSWORD, SCHEMA)
print(f"✅ {len(estados)} estados encontrados")
for e in estados:
    print(f"   - {e[1]}")

# Test 2: Crear parte mejorado
print("\nTest 2: Crear parte con campos mejorados")
new_id, codigo = add_parte_mejorado(
    USER, PASSWORD, SCHEMA,
    ot_id=1, red_id=1, tipo_trabajo_id=1, cod_trabajo_id=1,
    titulo='Test de parte mejorado',
    descripcion_corta='Test corto',
    descripcion_larga='Este es un test detallado de la funcionalidad mejorada',
    fecha_inicio='2025-10-29',
    id_estado=1,
    localizacion='Oficina central'
)
print(f"✅ Parte creado: {codigo} (ID: {new_id})")

# Test 3: Modificar parte
print("\nTest 3: Modificar parte")
result = mod_parte_mejorado(
    USER, PASSWORD, SCHEMA,
    parte_id=new_id,
    id_estado=2,  # Cambiar a "En curso"
    fecha_prevista_fin='2025-10-30'
)
print(f"✅ Resultado: {result}")

# Test 4: Listar partes
print("\nTest 4: Listar partes mejorados")
partes = list_partes_mejorado(USER, PASSWORD, SCHEMA, limit=5)
print(f"✅ {len(partes)} partes encontrados")
for p in partes[:3]:
    print(f"   - {p.get('codigo')}: {p.get('titulo', 'Sin título')}")

print("\n🎉 Todos los tests completados exitosamente")
```

Guardar como `test_partes_mejorados.py` y ejecutar:
```bash
python test_partes_mejorados.py
```

---

## ⚙️ DETALLES TÉCNICOS

### Sincronización Estado/Finalizada

Los triggers automáticos mantienen sincronizados los campos `id_estado` y `finalizada`:

| Acción | Resultado |
|--------|-----------|
| `id_estado = 3` | `finalizada = TRUE` automáticamente |
| `id_estado != 3` | `finalizada = FALSE` automáticamente |
| `finalizada = TRUE` | `id_estado = 3` automáticamente |
| `finalizada = FALSE` desde TRUE | `id_estado = 2` (En curso) automáticamente |
| Estado cambia a Finalizada | `fecha_fin = HOY` si es NULL |

Esto garantiza coherencia sin intervención manual.

### Vista vw_partes_completo

Vista que une toda la información legible:
- Datos del parte
- Nombre del estado (en vez de ID)
- Nombre del municipio (en vez de ID)
- Códigos de OT, Red, Tipo, etc. (en vez de IDs)
- Campos calculados: `dias_duracion`, `dias_retraso`

**Uso:**
```sql
SELECT * FROM vw_partes_completo
WHERE estado = 'Pendiente'
ORDER BY fecha_prevista_fin;
```

### Índices Creados

Para optimizar consultas frecuentes:
- `idx_partes_estado`: Filtrar por estado
- `idx_partes_finalizada`: Filtrar finalizadas/pendientes
- `idx_partes_fecha_inicio`: Ordenar cronológicamente
- `idx_partes_fecha_fin`: Ordenar por finalización
- `idx_partes_municipio`: Agrupar por municipio
- `idx_partes_estado_fecha`: Consultas combinadas

### Compatibilidad Hacia Atrás

Todas las funciones antiguas siguen funcionando:
- `add_parte_with_code()` → Crea parte con campos mínimos
- `mod_parte_item()` → Modifica parte con campos antiguos
- `list_partes()` → Lista partes con campos antiguos

Las **nuevas funciones** detectan dinámicamente qué columnas existen:
- Si la migración NO se ha aplicado → Solo usan campos antiguos
- Si la migración SÍ se ha aplicado → Usan todos los campos

---

## 📚 PRÓXIMOS PASOS

### Interfaces (Pendiente)

1. **Modificar `interface/parts_interfaz.py`**:
   - Añadir campos para título, descripciones
   - Añadir DatePicker para fechas
   - Añadir ComboBox para estado
   - Añadir Entry para localización
   - Usar `add_parte_mejorado()` en vez de `add_parte_with_code()`

2. **Modificar `parts_list_window.py`**:
   - Mostrar nuevos campos en tabla
   - Filtrar por estado
   - Ordenar por fechas
   - Usar `list_partes_mejorado()`

3. **Modificar `parts_tab_embed.py`**:
   - Actualizar visualización

### Documentación (Pendiente)

4. **Crear manual de usuario**:
   - Cómo usar los nuevos campos
   - Qué significa cada estado
   - Flujo de trabajo recomendado

### Testing (Pendiente)

5. **Pruebas de integración**:
   - Probar creación de partes desde interfaz
   - Probar modificación
   - Probar filtros y ordenación
   - Validar triggers

---

## ❓ PREGUNTAS FRECUENTES

### ¿Tengo que migrar todos los proyectos a la vez?

No. La migración se puede aplicar proyecto por proyecto usando el parámetro `--schema`.

### ¿Qué pasa si ejecuto la migración dos veces?

Nada. El script es idempotente: detecta si los cambios ya están aplicados y no los repite.

### ¿Puedo deshacer la migración?

Sí, con las siguientes queries:
```sql
DROP VIEW IF EXISTS vw_partes_completo;
DROP TRIGGER IF EXISTS trg_partes_sync_finalizada_insert;
DROP TRIGGER IF EXISTS trg_partes_sync_finalizada_update;
ALTER TABLE tbl_partes
    DROP COLUMN titulo,
    DROP COLUMN descripcion_larga,
    DROP COLUMN descripcion_corta,
    DROP COLUMN fecha_inicio,
    DROP COLUMN fecha_fin,
    DROP COLUMN fecha_prevista_fin,
    DROP COLUMN id_estado,
    DROP COLUMN finalizada,
    DROP COLUMN localizacion,
    DROP COLUMN id_municipio;
DROP TABLE IF EXISTS tbl_parte_estados;
```

Pero **mejor hacer backup antes**.

### ¿Las funciones antiguas siguen funcionando?

Sí, al 100%. Todas las funciones antiguas (`add_parte_with_code`, etc.) siguen disponibles y funcionando.

---

## 📞 SOPORTE

Para problemas o preguntas:
1. Revisar este README
2. Ejecutar script de verificación en `mejoras_tabla_partes.sql`
3. Comprobar logs de migración
4. Contactar con el equipo de desarrollo

---

## 📝 CHANGELOG

### v1.0.0 (2025-10-29)
- ✅ Script SQL de migración completo
- ✅ Script Python de migración automática
- ✅ 4 funciones nuevas en db_partes.py
- ✅ Exportación en modulo_db.py
- ✅ Documentación completa
- ⏳ Interfaces pendientes

---

**Autor**: Claude Code
**Fecha**: 29 de octubre de 2025
**Versión**: 1.0.0
**Estado**: Base de datos COMPLETA | Interfaces PENDIENTE
