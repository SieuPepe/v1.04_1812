# Fase 3: Configuración de dim_comarcas y creación de dim_municipios

## Resumen

Este script implementa la estructura completa de tablas dimensionales para provincias, comarcas y municipios del País Vasco, preparando la base de datos para su uso en el programa de partes.

## Cambios Implementados

### 1. Creación de dim_municipios
Se crea la tabla `dim_municipios` con la siguiente estructura:

```sql
CREATE TABLE dim_municipios (
    id INT NOT NULL AUTO_INCREMENT,
    codigo_ine BIGINT NOT NULL,              -- Código INE del municipio
    nombre VARCHAR(255) NOT NULL,            -- Nombre del municipio
    provincia_id INT NOT NULL,               -- FK a dim_provincias
    comarca_id INT DEFAULT NULL,             -- FK a dim_comarcas
    activo TINYINT(1) DEFAULT 1,            -- Para filtrado activo/inactivo
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_codigo_ine (codigo_ine)
);
```

**Nota importante**: El campo `nombre` coincide con el nombre esperado por el código en `db_partes.py` (líneas 757-767), que busca en orden: 'nombre', 'municipio', 'descripcion'.

### 2. Relación dim_comarcas con dim_provincias
Se añade el campo `provincia_id` a la tabla `dim_comarcas` existente para relacionarla con `dim_provincias`.

### 3. Estructura de Comarcas

#### Comarcas Existentes (Álava)
Las 6 comarcas/cuadrillas de Álava ya existían:
- id=1: AIARA - Cuadrilla de Ayala (provincia_id=1)
- id=2: LAGUA - Cuadrilla de Laguardia (provincia_id=1)
- id=3: LLANA - Cuadrilla de Vitoria (provincia_id=1)
- id=4: GORBE - Cuadrilla de Gorbeialdea (provincia_id=1)
- id=5: AANA - Cuadrilla de Añana (provincia_id=1)
- id=6: CAMPE - Cuadrilla de Campezo (provincia_id=1)

#### Comarcas Nuevas
- id=7: GIPUZ - Gipuzkoa (provincia_id=3)
- id=8: BIZKA - Bizkaia (provincia_id=2)

### 4. Datos de Municipios

Total de municipios insertados: **251**

#### Distribución por provincia:
- **Álava**: 51 municipios (distribuidos entre las 6 cuadrillas)
- **Bizkaia**: 112 municipios (comarca_id=8)
- **Gipuzkoa**: 88 municipios (comarca_id=7)

#### Códigos INE por provincia:
- Álava: 01xxx (ej: 01001, 01018)
- Bizkaia: 48xxx (ej: 48020 para Barakaldo, 48028 para Bilbao)
- Gipuzkoa: 20xxx (ej: 20001 para Abaltzisketa, 20031 para Donostia)

## Ejecución del Script

### Opción 1: PowerShell (Windows)
```powershell
.\script\ejecutar_fase3_dim_municipios.ps1
```

### Opción 2: MySQL CLI (Linux/Mac)
```bash
mysql -u root -p cert_dev < script/fase3_dim_municipios.sql
```

### Opción 3: MySQL CLI con verificación
```bash
mysql -u root -p cert_dev < script/fase3_dim_municipios.sql && \
mysql -u root -p cert_dev -e "
SELECT p.nombre as Provincia, COUNT(DISTINCT c.id) as Comarcas, COUNT(m.id) as Municipios
FROM dim_provincias p
LEFT JOIN dim_comarcas c ON c.provincia_id = p.id
LEFT JOIN dim_municipios m ON m.provincia_id = p.id
GROUP BY p.id, p.nombre
ORDER BY p.id;
"
```

## Verificación de Resultados

### 1. Verificar estructura de dim_municipios
```sql
DESCRIBE dim_municipios;
```

Debe mostrar las columnas: id, codigo_ine, nombre, provincia_id, comarca_id, activo, created_at

### 2. Contar comarcas por provincia
```sql
SELECT
    p.nombre AS Provincia,
    COUNT(c.id) AS Total_Comarcas
FROM dim_provincias p
LEFT JOIN dim_comarcas c ON c.provincia_id = p.id
GROUP BY p.id, p.nombre
ORDER BY p.id;
```

**Resultado esperado:**
```
+------------------+----------------+
| Provincia        | Total_Comarcas |
+------------------+----------------+
| Araba/Álava      |              6 |
| Bizkaia          |              1 |
| Gipuzkoa         |              1 |
+------------------+----------------+
```

### 3. Contar municipios por provincia
```sql
SELECT
    p.nombre AS Provincia,
    COUNT(m.id) AS Total_Municipios
FROM dim_provincias p
LEFT JOIN dim_municipios m ON m.provincia_id = p.id
GROUP BY p.id, p.nombre
ORDER BY p.id;
```

**Resultado esperado:**
```
+------------------+------------------+
| Provincia        | Total_Municipios |
+------------------+------------------+
| Araba/Álava      |               51 |
| Bizkaia          |              112 |
| Gipuzkoa         |               88 |
+------------------+------------------+
Total: 251 municipios
```

### 4. Contar municipios por comarca
```sql
SELECT
    c.comarca_nombre AS Comarca,
    p.nombre AS Provincia,
    COUNT(m.id) AS Total_Municipios
FROM dim_comarcas c
LEFT JOIN dim_provincias p ON c.provincia_id = p.id
LEFT JOIN dim_municipios m ON m.comarca_id = c.id
GROUP BY c.id, c.comarca_nombre, p.nombre
ORDER BY p.id, c.id;
```

### 5. Verificar nombres de municipios de Gipuzkoa
```sql
SELECT codigo_ine, nombre
FROM dim_municipios
WHERE provincia_id = 3
ORDER BY codigo_ine
LIMIT 10;
```

**Resultado esperado (primeros 10):**
```
+------------+-----------------+
| codigo_ine | nombre          |
+------------+-----------------+
|      20001 | Abaltzisketa    |
|      20002 | Aduna           |
|      20003 | Aia             |
|      20004 | Aizarnazabal    |
|      20005 | Albiztur        |
|      20006 | Alegia          |
|      20007 | Alkiza          |
|      20008 | Altzaga         |
|      20009 | Altzo           |
|      20010 | Amezketa        |
+------------+-----------------+
```

### 6. Verificar municipios activos
```sql
SELECT
    provincia_id,
    COUNT(*) as Total,
    SUM(activo) as Activos,
    COUNT(*) - SUM(activo) as Inactivos
FROM dim_municipios
GROUP BY provincia_id;
```

Todos los municipios deben estar activos (activo=1).

## Compatibilidad con el Programa de Partes

El script garantiza compatibilidad con `db_partes.py`:

1. **Nombre de tabla**: Usa `dim_municipios` (requerido por db_partes.py:761)
2. **Campo nombre**: Usa `nombre` como nombre de columna (primera opción en db_partes.py:762)
3. **Campo provincia_id**: Incluido para filtrado por provincia (db_partes.py:785)
4. **Campo activo**: Incluido para filtrado de municipios activos (db_partes.py:781)
5. **Campo id**: Clave primaria usada para referencias (db_partes.py:783)

## Notas Importantes

### Asignación de Comarcas en Álava
Los municipios de Álava se han asignado a sus cuadrillas correspondientes según la división administrativa tradicional:
- **Cuadrilla de Ayala (AIARA)**: Municipios del noroeste (Amurrio, Laudio, Okondo, etc.)
- **Cuadrilla de Laguardia (LAGUA)**: Municipios de la Rioja Alavesa
- **Cuadrilla de Vitoria (LLANA)**: Municipios de la zona central (incluye Vitoria-Gasteiz)
- **Cuadrilla de Gorbeialdea (GORBE)**: Sin municipios en esta asignación simplificada
- **Cuadrilla de Añana (AANA)**: Municipios del este (Arraia-Maeztu, Bernedo, etc.)
- **Cuadrilla de Campezo (CAMPE)**: Municipio de Campezo/Kanpezu

**Nota**: En una implementación de producción, se recomienda verificar las asignaciones específicas con las fuentes oficiales de la Diputación Foral de Álava.

### Idempotencia
El script es **idempotente** - puede ejecutarse múltiples veces sin causar errores:
- Usa `CREATE TABLE IF NOT EXISTS`
- Verifica existencia de columnas antes de añadirlas
- Usa `ON DUPLICATE KEY UPDATE` en los INSERT de datos
- La clave única en `codigo_ine` previene duplicados

### Códigos INE
Los códigos INE (Instituto Nacional de Estadística) son únicos y oficiales. La constraint `UNIQUE KEY uk_codigo_ine` garantiza que no haya duplicados.

## Resolución de Problemas

### Error: "Table 'dim_comarcas' doesn't exist"
Primero debe existir la tabla `dim_comarcas`. Verificar con:
```sql
SHOW TABLES LIKE 'dim_comarcas';
```

### Error: "Duplicate entry for key 'uk_codigo_ine'"
Indica que ya existen municipios con esos códigos INE. Para limpiar y reinsertar:
```sql
DELETE FROM dim_municipios;
-- Luego ejecutar el script nuevamente
```

### Error: "Cannot add foreign key constraint"
Verificar que existan las tablas `dim_provincias` y `dim_comarcas` con sus claves primarias.

## Archivos Relacionados

- `fase3_dim_municipios.sql` - Script SQL principal
- `ejecutar_fase3_dim_municipios.ps1` - Script PowerShell de ejecución
- `README_FASE3_dim_municipios.md` - Este archivo (documentación)

## Siguientes Pasos

1. Ejecutar el script en entorno de desarrollo
2. Verificar los resultados con las queries de verificación
3. Probar el programa de partes con los nuevos datos
4. Si todo funciona correctamente, ejecutar en producción
5. Crear backup antes de ejecutar en producción

## Referencias

- Fuente de datos: Instituto Nacional de Estadística (INE)
- Códigos municipales: https://www.ine.es/
- Estructura administrativa: Diputaciones Forales del País Vasco
