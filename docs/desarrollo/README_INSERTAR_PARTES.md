# Guía para Insertar Datos en tbl_partes

## Resumen

Este documento explica cómo insertar los 828 registros del archivo Excel "Para exportar.xlsx" en la tabla `tbl_partes`.

## Problema Identificado

Los datos en el Excel referencian municipios (campo `id_municipio`) que deben existir en la tabla `dim_municipios` debido a una restricción de clave foránea (`fk_partes_municipio`).

Los IDs de municipios referenciados en el Excel son:
- **[1, 2, 3, 4, 5, 6, 9, 10, 21, 26, 41, 44, 45, 46, 48]**

## Scripts Creados

### 1. Scripts de Análisis y Verificación

#### `script/analizar_municipios_excel.py`
Analiza el archivo Excel para identificar qué municipios se referencian.

```bash
python3 script/analizar_municipios_excel.py
```

**Salida:**
- Lista de IDs de municipios únicos
- Distribución de registros por municipio
- Análisis de columnas relacionadas con municipios

#### `script/sql/verificar_e_insertar_municipios_faltantes.sql`
Verifica qué municipios existen en `dim_municipios` y cuáles faltan.

**Resultado esperado:**
- Lista de municipios existentes
- Conteo de municipios faltantes
- IDs específicos de municipios faltantes

### 2. Scripts de Inserción de Municipios

#### `script/sql/insertar_municipios_faltantes_1_48.sql`
Inserta municipios faltantes con datos placeholder.

**Características:**
- Usa `INSERT IGNORE` para evitar duplicados
- Asigna códigos INE genéricos (90000001-90000048)
- Puede actualizarse más tarde con datos reales

**IMPORTANTE:** Este script solo inserta los municipios que NO existen.

### 3. Scripts de Generación e Inserción de Partes

#### `script/generar_insert_partes.py`
Genera el archivo SQL con los INSERT para tbl_partes.

**Mejoras incluidas:**
- ✅ Corrige mapeo de campo: `descripion` → `descripcion`
- ✅ Maneja valores NULL correctamente
- ✅ Escapa caracteres especiales en strings
- ✅ Usa `ON DUPLICATE KEY UPDATE` para evitar duplicados

```bash
python3 script/generar_insert_partes.py
```

**Salida:** `script/sql/insertar_partes_desde_excel.sql`

#### `script/insertar_partes_por_lotes.py`
Inserta registros en tbl_partes por lotes de 50 registros.

**Ventajas:**
- ✅ Verifica existencia de municipios antes de insertar
- ✅ Inserta en lotes pequeños para identificar errores
- ✅ Muestra progreso durante la inserción
- ✅ Guarda query fallida en `error_query.sql` si hay error

**IMPORTANTE:** Debes configurar las credenciales de base de datos en el script antes de ejecutar.

```python
conn = mysql.connector.connect(
    host='localhost',
    user='root',      # ← Ajustar
    password='',      # ← Ajustar
    database='cert_dev'  # ← Ajustar
)
```

## Proceso de Inserción Recomendado

### Paso 1: Verificar Municipios Existentes

Ejecuta el script de verificación en tu base de datos:

```sql
SOURCE script/sql/verificar_e_insertar_municipios_faltantes.sql;
```

Este script mostrará:
- Qué municipios YA existen
- Cuántos municipios faltan
- Cuáles son los IDs faltantes

### Paso 2: Insertar Municipios Faltantes (si es necesario)

Si hay municipios faltantes, ejecuta:

```sql
SOURCE script/sql/insertar_municipios_faltantes_1_48.sql;
```

**NOTA:** Este script inserta municipios con nombres genéricos (ej: "Municipio 1", "Municipio 2"). Puedes actualizarlos más tarde con los nombres reales si lo deseas.

### Paso 3: Insertar Datos en tbl_partes

Tienes dos opciones:

#### Opción A: Usando el script Python (Recomendado)

```bash
python3 script/insertar_partes_por_lotes.py
```

**Ventajas:**
- Muestra progreso en tiempo real
- Identifica exactamente dónde falla si hay error
- Inserta en lotes de 50 registros

#### Opción B: Usando el archivo SQL generado

```sql
SOURCE script/sql/insertar_partes_desde_excel.sql;
```

**ADVERTENCIA:** Este archivo contiene 828 registros en un solo INSERT. Si hay un error, será más difícil identificar la causa.

### Paso 4: Verificar Inserción

Después de insertar, verifica los datos:

```sql
-- Contar registros totales
SELECT COUNT(*) AS total_registros FROM tbl_partes;

-- Ver primeros registros
SELECT * FROM tbl_partes ORDER BY id LIMIT 5;

-- Ver últimos registros
SELECT * FROM tbl_partes ORDER BY id DESC LIMIT 5;

-- Verificar distribución por municipio
SELECT id_municipio, COUNT(*) as total
FROM tbl_partes
GROUP BY id_municipio
ORDER BY id_municipio;
```

## Notas Importantes

### Correcciones Aplicadas

1. **Campo descripcion:** Se corrigió el mapeo de `descripion` (Excel) a `descripcion` (base de datos)
2. **Tabla de municipios:** Se usa `dim_municipios` en lugar de `tbl_municipios`
3. **Tabla de comarcas:** Se usa `dim_comarcas` en lugar de otras variantes

### Estructura de dim_municipios

```sql
CREATE TABLE dim_municipios (
    id INT NOT NULL AUTO_INCREMENT,
    codigo_ine BIGINT NOT NULL,
    municipio_nombre VARCHAR(255) NOT NULL,
    provincia_id INT NOT NULL,
    comarca_id INT DEFAULT NULL,
    activo TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_codigo_ine (codigo_ine)
);
```

### IDs de Provincias

- **1** = Álava / Araba
- **2** = Bizkaia
- **3** = Gipuzkoa

### IDs de Comarcas (ejemplos)

- **1** = Ayala (Álava)
- **2** = Laguardia (Álava)
- **3** = Vitoria / Llanada Alavesa (Álava)
- **8** = Bizkaia
- **7** = Gipuzkoa

## Troubleshooting

### Error: Foreign Key Constraint Fails

Si obtienes un error de restricción de clave foránea:

```
Error Code: 1452. Cannot add or update a child row: a foreign key constraint fails
```

**Solución:**
1. Ejecuta el script de verificación de municipios
2. Identifica los IDs faltantes
3. Inserta los municipios faltantes
4. Vuelve a intentar la inserción de partes

### Error: Duplicate Entry

Si obtienes un error de entrada duplicada:

```
Error Code: 1062. Duplicate entry '...' for key '...'
```

**Solución:**
- El script usa `ON DUPLICATE KEY UPDATE`, por lo que debería actualizar registros existentes
- Verifica que la clave primaria (`id`) o claves únicas no tengan conflictos

### Script Python No Conecta a BD

**Solución:**
1. Verifica las credenciales en el script
2. Asegúrate de que MySQL esté corriendo
3. Verifica que el usuario tenga permisos de escritura

## Archivos Generados

- `script/sql/insertar_partes_desde_excel.sql` - SQL generado con 828 registros
- `error_query.sql` - Query que causó error (si hay fallo en script Python)

## Resumen de Distribución de Datos

Según el análisis del Excel:

| id_municipio | Cantidad de Registros |
|-------------|-----------------------|
| 1           | 448                   |
| 2           | 13                    |
| 3           | 118                   |
| 4           | 26                    |
| 5           | 145                   |
| 6           | 27                    |
| 9           | 4                     |
| 10          | 9                     |
| 21          | 7                     |
| 26          | 10                    |
| 41          | 12                    |
| 44          | 3                     |
| 45          | 1                     |
| 46          | 4                     |
| 48          | 1                     |
| **TOTAL**   | **828**               |

---

**Autor:** Claude Code
**Fecha:** 2025-11-12
**Rama:** claude/add-groupby-reports-011CUsQyJRsqr6bWy6iiR69c
