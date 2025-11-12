# Fase 3: Relacionar Comarcas con Provincias y Completar Municipios

## Objetivo
Relacionar la tabla `dim_comarcas` existente con `dim_provincias`, añadir las comarcas de Gipuzkoa y Bizkaia, y completar los municipios de estas provincias.

## Cambios implementados

### 1. Tabla dim_comarcas (existente)
La tabla `dim_comarcas` ya existe con la siguiente estructura:
- `id` - ID único de la comarca
- `comarca_codigo` - Código corto de la comarca (5 caracteres)
- `comarca_nombre` - Nombre de la comarca
- `created_at` - Fecha de creación

**NUEVO**: Se añade el campo `provincia_id` para relacionarla con `dim_provincias`:

```sql
ALTER TABLE dim_comarcas
ADD COLUMN provincia_id INT DEFAULT NULL,
ADD CONSTRAINT fk_comarcas_provincia FOREIGN KEY (provincia_id) REFERENCES dim_provincias(id)
```

### 2. Comarcas existentes y nuevas

#### Araba/Álava (ids 1-6) - YA EXISTENTES
Estas comarcas ya existían, solo se les asigna `provincia_id=1`:
1. AIARA - Aiaraldea
2. LAGUA - Laguardia-Rioja Alavesa
3. LLANA - Llanada Alavesa
4. GORBE - Gorbeialdea
5. AANA - Añana
6. CAMPE - Campezo-Montaña Alavesa

#### Gipuzkoa (id=7) - NUEVA
Comarca única para toda la provincia de Gipuzkoa:
- Código: GIPUZ
- Nombre: Gipuzkoa
- provincia_id: 3

#### Bizkaia (id=8) - NUEVA
Comarca única para toda la provincia de Bizkaia:
- Código: BIZKA
- Nombre: Bizkaia
- provincia_id: 2

### 3. Tabla tbl_municipios actualizada
Se añade el campo `comarca_id` a la tabla `tbl_municipios`:

```sql
ALTER TABLE tbl_municipios
ADD COLUMN comarca_id INT DEFAULT NULL AFTER provincia_id,
ADD CONSTRAINT fk_municipios_comarca FOREIGN KEY (comarca_id) REFERENCES dim_comarcas(id)
```

### 4. Municipios completados

- **Gipuzkoa**: 88 municipios insertados con comarca_id=7
- **Bizkaia**: Municipios existentes (112) actualizados con comarca_id=8
- **Álava**: Municipios existentes (51) actualizados con comarca_id=3 (LLANA - Llanada Alavesa por defecto)

## Ejecución del script

### En PowerShell (Windows):

```powershell
# Navegar al directorio del proyecto
cd C:\Users\...\v1.04_1812

# Ejecutar el script
Get-Content script\fase3_comarcas_municipios.sql | mysql -u root -pNuevaPass!2025 cert_dev
```

### En Bash (Linux/Mac):

```bash
# Navegar al directorio del proyecto
cd ~/v1.04_1812

# Ejecutar el script
mysql -u root -p cert_dev < script/fase3_comarcas_municipios.sql
```

## Verificación

Después de ejecutar el script, deberías ver un resumen como este:

### Por comarca:
```
+------------+---------------------------+-------------------+
| provincia  | comarca                   | total_municipios  |
+------------+---------------------------+-------------------+
| Álava      | Aiaraldea                 | 0                 |
| Álava      | Laguardia-Rioja Alavesa   | 0                 |
| Álava      | Llanada Alavesa           | 51                |
| Álava      | Gorbeialdea               | 0                 |
| Álava      | Añana                     | 0                 |
| Álava      | Campezo-Montaña Alavesa   | 0                 |
| Bizkaia    | Bizkaia                   | 112               |
| Gipuzkoa   | Gipuzkoa                  | 88                |
+------------+---------------------------+-------------------+
```

### Por provincia:
```
+------------+-------------------+
| provincia  | total_municipios  |
+------------+-------------------+
| Álava      | 51                |
| Bizkaia    | 112               |
| Gipuzkoa   | 88                |
+------------+-------------------+
```

**Total: 251 municipios**

## Notas importantes

- Los municipios de Álava se han asignado por defecto a la comarca LLANA (Llanada Alavesa, comarca_id=3)
- Si se necesita asignar los municipios de Álava a sus comarcas específicas, se puede hacer con UPDATE posteriores
- Las comarcas de Gipuzkoa y Bizkaia son únicas para toda la provincia (no hay subdivisión comarcal como en Álava)
- Los códigos INE de Gipuzkoa van del 20001 al 20088
- La tabla dim_comarcas ya existía con 6 comarcas de Álava, este script añade el campo provincia_id y las comarcas 7 y 8

## Estructura de datos final

### dim_provincias
| id | codigo | nombre    | nombre_euskera |
|----|--------|-----------|----------------|
| 1  | 01     | Álava     | Araba          |
| 2  | 48     | Bizkaia   | Bizkaia        |
| 3  | 20     | Gipuzkoa  | Gipuzkoa       |

### dim_comarcas
| id | provincia_id | comarca_codigo | comarca_nombre            |
|----|--------------|----------------|---------------------------|
| 1  | 1            | AIARA          | Aiaraldea                 |
| 2  | 1            | LAGUA          | Laguardia-Rioja Alavesa   |
| 3  | 1            | LLANA          | Llanada Alavesa           |
| 4  | 1            | GORBE          | Gorbeialdea               |
| 5  | 1            | AANA           | Añana                     |
| 6  | 1            | CAMPE          | Campezo-Montaña Alavesa   |
| 7  | 3            | GIPUZ          | Gipuzkoa                  |
| 8  | 2            | BIZKA          | Bizkaia                   |

### tbl_municipios (estructura)
- `id` - ID único del municipio
- `provincia_id` - Referencia a dim_provincias (1=Álava, 2=Bizkaia, 3=Gipuzkoa)
- `comarca_id` - Referencia a dim_comarcas (1-6=Comarcas Álava, 7=Gipuzkoa, 8=Bizkaia)
- `NAMEUNIT` - Nombre del municipio
- `CODIGOINE` - Código INE del municipio
- (otros campos...)

### dim_comarcas (estructura actualizada)
- `id` - ID único de la comarca
- `provincia_id` - **NUEVO** Referencia a dim_provincias
- `comarca_codigo` - Código corto de la comarca (AIARA, LAGUA, LLANA, GORBE, AANA, CAMPE, GIPUZ, BIZKA)
- `comarca_nombre` - Nombre completo de la comarca
- `created_at` - Fecha de creación

## Funciones Python disponibles

Para utilizar estas tablas en la aplicación, se pueden crear funciones adicionales en `script/db_partes.py`:

- `get_comarcas(user, password, schema, provincia_id=None)` - Obtiene lista de comarcas (opcionalmente filtradas por provincia)
- `get_municipios_by_comarca(user, password, schema, comarca_id)` - Obtiene municipios filtrados por comarca
- `get_comarcas_by_provincia(user, password, schema, provincia_id)` - Obtiene comarcas de una provincia específica
