# Fase 2: Provincias y Municipios

## Objetivo
Añadir soporte para provincias (Álava, Bizkaia, Gipuzkoa) y municipios de Álava a la base de datos, con selectores separados en la interfaz.

## Paso 1: Ejecutar el script SQL

El script `fase2_provincias_municipios.sql` realiza las siguientes operaciones:

1. **Crear tabla `dim_provincias`** con las 3 provincias del País Vasco
2. **Añadir columna `provincia_id`** a `tbl_municipios`
3. **Actualizar municipios existentes** (Bizkaia) con provincia_id = 2
4. **Insertar 51 municipios de Álava**

### Ejecución en PowerShell:

```powershell
# Navegar al directorio del proyecto
cd C:\Users\...\v1.04_1812

# Ejecutar el script
Get-Content script\fase2_provincias_municipios.sql | mysql -u root -pNuevaPass!2025 cert_dev
```

### Verificación:

Después de ejecutar el script, deberías ver un resumen como este:

```
+------------+----------------+-------------------+
| provincia  | nombre_euskera | total_municipios  |
+------------+----------------+-------------------+
| Álava      | Araba          | 51                |
| Bizkaia    | Bizkaia        | 115               |
| Gipuzkoa   | Gipuzkoa       | 0                 |
+------------+----------------+-------------------+
```

## Paso 2: Actualizar la interfaz (Pendiente)

Una vez ejecutado el script SQL, se actualizarán los formularios para:

1. Añadir selector de **Provincia** (Álava, Bizkaia, Gipuzkoa)
2. Actualizar selector de **Municipio** para filtrar por provincia seleccionada
3. Implementar funcionalidad de búsqueda en ambos selectores

## Funciones Python disponibles

Ya están implementadas en `script/db_partes.py`:

- `get_provincias(user, password, schema)` - Obtiene lista de provincias
- `get_municipios_by_provincia(user, password, schema, provincia_id)` - Obtiene municipios filtrados por provincia

## Estructura de la tabla dim_provincias

| id | codigo | nombre    | nombre_euskera |
|----|--------|-----------|----------------|
| 1  | 01     | Álava     | Araba          |
| 2  | 48     | Bizkaia   | Bizkaia        |
| 3  | 20     | Gipuzkoa  | Gipuzkoa       |

## Estructura actualizada de tbl_municipios

```sql
CREATE TABLE tbl_municipios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    provincia_id INT,  -- NUEVA COLUMNA
    INSPIREID TEXT,
    NATCODE BIGINT,
    NAMEUNIT TEXT,     -- Nombre del municipio
    CODIGOINE BIGINT,  -- Código INE
    ...
    FOREIGN KEY (provincia_id) REFERENCES dim_provincias(id)
);
```

## Notas importantes

- Los municipios de Gipuzkoa no están incluidos en este script (se pueden añadir más adelante si es necesario)
- La numeración de códigos OT (GF/OT/TP) sigue siendo independiente por prefijo
- El campo "Código OT" ahora usa una consulta SQL más robusta que maneja valores NULL correctamente
