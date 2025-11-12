# Problema con dim_municipios - Análisis y Solución

## ❌ Problema Identificado

### Scripts problemáticos ejecutados:
1. **`actualizar_municipios_alava.sql`** (línea 13):
   ```sql
   DELETE FROM dim_municipios WHERE id BETWEEN 1 AND 52;
   ```

2. **`actualizar_codigos_postales_municipios.sql`** (líneas 38, 45-198):
   ```sql
   UPDATE dim_municipios SET provincia_id = 1 WHERE id >= 1 AND id <= 52;
   UPDATE dim_municipios SET codigo_postal = '01470' WHERE id = 1;
   UPDATE dim_municipios SET codigo_postal = '01474' WHERE id = 2;
   -- ... etc
   ```

### Daños causados:

1. **DELETE por ID autoincrementado**:
   - Borró los registros con `id` 1-52, sin importar su `codigo_ine`
   - Estos IDs podían corresponder a **cualquier municipio**, no solo a Álava
   - Probablemente incluyó municipios de **Bizkaia y Gipuzkoa**

2. **Pérdida de datos**:
   - ❌ Campo `activo` se perdió (debería ser `1`)
   - ❌ Campo `created_at` se perdió (timestamp)
   - ❌ El script de códigos postales actualizó registros incorrectos por ID

3. **Confusión de campos**:
   - Los scripts usaban `nombre` vs `municipio_nombre` inconsistentemente
   - El campo correcto de la tabla es `municipio_nombre`

4. **Error conceptual grave**:
   - Usar `id` (campo autoincrementado) en lugar de `codigo_ine` (clave única del INE)
   - El `id` puede cambiar con inserts/deletes, el `codigo_ine` es estable y oficial

## ✅ Solución Implementada

### 1. Script de Recuperación Completo

**Archivo**: `script/sql/RECUPERAR_dim_municipios.sql`

Este script:
- ✅ Restaura **todos los municipios** de las 3 provincias
- ✅ Usa `codigo_ine` como identificador (NO `id`)
- ✅ Restaura valores de `activo = 1`
- ✅ Restaura valores de `created_at`
- ✅ Usa `INSERT ... ON DUPLICATE KEY UPDATE` (UPSERT seguro)
- ✅ Actualiza códigos postales por `codigo_ine`
- ✅ Incluye verificaciones detalladas

**Cómo ejecutarlo**:
```bash
# Ejecutar en MySQL Workbench o línea de comandos
mysql -u usuario -p nombre_bd < script/sql/RECUPERAR_dim_municipios.sql
```

### 2. Scripts Corregidos

#### A) `actualizar_municipios_alava.sql`

**Cambios realizados**:
- ❌ **ELIMINADO**: `DELETE FROM dim_municipios WHERE id BETWEEN 1 AND 52;`
- ✅ **AÑADIDO**: Comentarios explicando por qué NO usar DELETE por ID
- ✅ **MODIFICADO**: INSERT ahora incluye `created_at`
- ✅ **MEJORADO**: ON DUPLICATE KEY UPDATE preserva `activo` y `created_at`

```sql
-- ANTES (INCORRECTO):
DELETE FROM dim_municipios WHERE id BETWEEN 1 AND 52;
INSERT INTO dim_municipios (codigo_ine, nombre, provincia_id, comarca_id, activo) VALUES ...

-- DESPUÉS (CORRECTO):
INSERT INTO dim_municipios (codigo_ine, nombre, provincia_id, comarca_id, activo, created_at) VALUES ...
ON DUPLICATE KEY UPDATE
    nombre = VALUES(nombre),
    provincia_id = VALUES(provincia_id),
    comarca_id = VALUES(comarca_id),
    activo = 1,  -- Siempre restaurar a 1
    created_at = IFNULL(created_at, NOW());  -- Preservar original
```

#### B) `actualizar_codigos_postales_municipios.sql`

**Cambios realizados**:
- ❌ **ELIMINADO**: `UPDATE ... WHERE id = 1;` (y todos los UPDATEs por ID)
- ✅ **AÑADIDO**: `UPDATE ... WHERE codigo_ine = 1002;` (usando codigo_ine)
- ✅ **MEJORADO**: Comentarios con codigo_ine en cada UPDATE

```sql
-- ANTES (INCORRECTO):
UPDATE dim_municipios SET codigo_postal = '01470' WHERE id = 1;
UPDATE dim_municipios SET codigo_postal = '01474' WHERE id = 2;

-- DESPUÉS (CORRECTO):
UPDATE dim_municipios SET codigo_postal = '01470' WHERE codigo_ine = 1002;  -- Amurrio
UPDATE dim_municipios SET codigo_postal = '01474' WHERE codigo_ine = 1004;  -- Artziniega
```

## 📋 Pasos para Recuperar la Base de Datos

### Opción 1: Recuperación Completa (RECOMENDADO)

1. **Ejecutar script de recuperación**:
   ```bash
   mysql -u usuario -p cert_dev < script/sql/RECUPERAR_dim_municipios.sql
   ```

2. **Verificar resultados**:
   - El script muestra verificaciones automáticas al final
   - Revisar que todos los municipios tienen `activo = 1`
   - Revisar que todos tienen `created_at`
   - Revisar que los códigos postales están correctos

### Opción 2: Ejecutar Scripts Corregidos (solo si la tabla está vacía)

1. **Ejecutar fase3_dim_municipios.sql** (crea tabla y municipios base)
2. **Ejecutar actualizar_municipios_alava.sql** (versión corregida)
3. **Ejecutar actualizar_codigos_postales_municipios.sql** (versión corregida)

## 🔍 Verificaciones Recomendadas

### 1. Verificar totales por provincia

```sql
SELECT
    p.nombre AS provincia,
    COUNT(m.id) AS total_municipios,
    SUM(CASE WHEN m.activo = 1 THEN 1 ELSE 0 END) AS activos,
    SUM(CASE WHEN m.created_at IS NOT NULL THEN 1 ELSE 0 END) AS con_created_at
FROM dim_provincias p
LEFT JOIN dim_municipios m ON p.id = m.provincia_id
GROUP BY p.id, p.nombre
ORDER BY p.id;
```

**Resultados esperados**:
- Álava: 51 municipios (todos activos, todos con created_at)
- Bizkaia: 112 municipios (todos activos, todos con created_at)
- Gipuzkoa: 88 municipios (todos activos, todos con created_at)

### 2. Verificar códigos postales de Álava

```sql
SELECT
    codigo_ine,
    nombre,
    codigo_postal,
    activo,
    created_at
FROM dim_municipios
WHERE provincia_id = 1
ORDER BY codigo_ine;
```

**Verificar que**:
- Todos tienen `activo = 1`
- Todos tienen `created_at` con fecha válida
- Los códigos postales son de formato `01XXX`

### 3. Verificar que no hay registros huérfanos

```sql
SELECT * FROM dim_municipios
WHERE activo IS NULL OR activo = 0 OR created_at IS NULL;
```

**Resultado esperado**: 0 registros

## 📚 Lecciones Aprendidas

### ❌ Nunca hacer:

1. **DELETE por ID en tablas con claves naturales**:
   ```sql
   -- ❌ MAL: Los IDs son autoincrementados y pueden cambiar
   DELETE FROM tabla WHERE id BETWEEN 1 AND 100;
   ```

2. **UPDATE por ID cuando existe codigo_ine**:
   ```sql
   -- ❌ MAL: El ID no identifica al municipio de forma estable
   UPDATE dim_municipios SET codigo_postal = '01470' WHERE id = 1;
   ```

### ✅ Siempre hacer:

1. **Usar la clave natural (codigo_ine)**:
   ```sql
   -- ✅ BIEN: codigo_ine es único y estable (código INE oficial)
   UPDATE dim_municipios SET codigo_postal = '01470' WHERE codigo_ine = 1002;
   ```

2. **Usar UPSERT en lugar de DELETE + INSERT**:
   ```sql
   -- ✅ BIEN: Inserta si no existe, actualiza si existe
   INSERT INTO dim_municipios (codigo_ine, nombre, ...) VALUES (...)
   ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), ...;
   ```

3. **Preservar campos de auditoría**:
   ```sql
   -- ✅ BIEN: Mantener created_at original
   created_at = IFNULL(created_at, NOW())
   ```

## 🎯 Estructura Correcta de dim_municipios

```sql
CREATE TABLE dim_municipios (
    id INT AUTO_INCREMENT PRIMARY KEY,           -- ID técnico (autoincrementado)
    codigo_ine BIGINT NOT NULL UNIQUE,           -- Clave natural (INE oficial) ⭐
    nombre VARCHAR(255) NOT NULL,                 -- o municipio_nombre
    provincia_id INT NOT NULL,
    comarca_id INT DEFAULT NULL,
    activo TINYINT(1) DEFAULT 1,                 -- Debe ser 1 siempre
    codigo_postal VARCHAR(10) DEFAULT NULL,       -- Añadido después
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Auditoría
);
```

### Claves:
- `id`: Campo técnico, **NO usar para identificar municipios**
- `codigo_ine`: **Clave única oficial del INE**, usar para todas las operaciones
- `activo`: Indica si el municipio está activo (1) o no (0)
- `created_at`: Timestamp de creación, **nunca sobrescribir**

## 📞 Contacto

Si hay más problemas o dudas, revisar:
- Script de recuperación: `script/sql/RECUPERAR_dim_municipios.sql`
- Scripts corregidos: `script/sql/actualizar_municipios_alava.sql`
- Scripts corregidos: `script/sql/actualizar_codigos_postales_municipios.sql`
