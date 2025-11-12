# Configuración de Decimales en el Software

## Descripción

Este conjunto de scripts y módulos implementa una solución integral para garantizar que todos los campos numéricos del software (presupuestos, precios unitarios, importes, certificaciones, pendientes, etc.) tengan exactamente **2 decimales**.

## Componentes

### 1. Script SQL: `fix_decimal_precision.sql`

Modifica la estructura de la base de datos para convertir todos los campos `DOUBLE` y `FLOAT` a `DECIMAL(10,2)`.

**Tablas modificadas:**
- `tbl_pres_precios` - Precios de partidas (campo `coste`)
- `tbl_pres_grupo_partidas` - Grupos de partidas (campo `coste`)
- `tbl_presupuesto` - Presupuestos (campo `cantidad`)
- `tbl_proy_presupuesto` - Presupuestos de proyectos (gastos_generales, beneficio_industrial, baja, presupuesto_licitacion, iva)
- `tbl_pres_certificacion` - Certificaciones (campo `cantidad_certificada`)

### 2. Script Python: `aplicar_decimales.py`

Aplica automáticamente el script SQL a la base de datos.

**Características:**
- Conexión segura a MySQL
- Validación de sentencias SQL
- Reporte detallado de cambios aplicados
- Verificación de la aplicación correcta

### 3. Generador de Script: `generar_script_decimales.py`

Genera automáticamente un script SQL basándose en la estructura actual de la base de datos.

**Ventajas:**
- Detecta automáticamente todas las columnas DOUBLE/FLOAT
- Genera sentencias ALTER TABLE específicas
- Útil para bases de datos con esquemas personalizados

### 4. Módulo de Formateo: `number_formatter.py`

Proporciona funciones para formatear números con exactamente 2 decimales en todo el código Python.

**Funciones principales:**
- `format_decimal(value, decimals=2)` - Formatea un número con decimales
- `format_currency(value, decimals=2, currency='€')` - Formatea como moneda
- `format_percentage(value, decimals=2)` - Formatea como porcentaje
- `to_decimal(value, decimals=2)` - Convierte a Decimal con precisión
- `safe_float(value, default=0.0)` - Conversión segura a float

## Uso

### Opción 1: Usar el script automático (Recomendado)

```bash
cd /home/user/v1.04_1812/script
python3 aplicar_decimales.py
```

Sigue las instrucciones en pantalla para:
1. Conectarte a la base de datos
2. Confirmar la aplicación de cambios
3. Verificar que los cambios se aplicaron correctamente

### Opción 2: Aplicar manualmente el script SQL

```bash
cd /home/user/v1.04_1812/script
mysql -h localhost -P 3307 -u root -p proyecto_tipo < sql/fix_decimal_precision.sql
```

### Opción 3: Generar script personalizado

Si tienes un esquema de base de datos diferente:

```bash
cd /home/user/v1.04_1812/script
python3 generar_script_decimales.py
```

Esto generará un script SQL personalizado basado en tu estructura actual.

## Uso del Módulo de Formateo

### En código Python existente

```python
from number_formatter import format_decimal, format_currency, format_percentage

# Formatear un precio
precio = 1234.567
print(format_decimal(precio))  # "1234.57"
print(format_currency(precio))  # "1234.57 €"

# Formatear un porcentaje
iva = 21.0
print(format_percentage(iva))  # "21.00%"

# Conversión segura
from number_formatter import to_decimal, safe_float

valor_decimal = to_decimal("1234.567")  # Decimal('1234.57')
valor_float = safe_float("1234.567")    # 1234.57
```

### Integración en informes

El código de informes (`informes_exportacion.py`) ya utiliza el formato correcto:

```python
# En exportación a Word/PDF
if isinstance(valor, (int, float)) and formato_campo == 'moneda':
    cell.text = f"{valor:,.2f} €"
```

## Verificación

Para verificar que los cambios se aplicaron correctamente:

```sql
-- Consulta para ver todas las columnas DECIMAL en la base de datos
SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, NUMERIC_PRECISION, NUMERIC_SCALE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'proyecto_tipo'
AND DATA_TYPE = 'decimal'
AND TABLE_NAME LIKE 'tbl_%'
ORDER BY TABLE_NAME, COLUMN_NAME;
```

Todas las columnas deberían mostrar `NUMERIC_PRECISION = 10` y `NUMERIC_SCALE = 2`.

## Backup de Seguridad

**IMPORTANTE:** Antes de aplicar cualquier cambio a la base de datos, se recomienda hacer un backup:

```bash
# Backup completo
mysqldump -h localhost -P 3307 -u root -p proyecto_tipo > backup_antes_decimales.sql

# O usar el script de backup del proyecto
cd /home/user/v1.04_1812
# [ejecutar script de backup según procedimiento del proyecto]
```

## Impacto de los Cambios

### A nivel de Base de Datos

- **ANTES:** `DOUBLE` - Precisión variable, puede tener más de 2 decimales
- **DESPUÉS:** `DECIMAL(10,2)` - Exactamente 2 decimales, hasta 10 dígitos totales

**Ejemplo:**
- Valor antiguo: `1234.5678901`
- Valor nuevo: `1234.57`

### A nivel de Aplicación

El código Python ya formatea correctamente los valores con 2 decimales usando:
- Formato `{valor:,.2f}` en strings
- Formato `#,##0.00 €` en Excel
- Funciones del módulo `number_formatter.py`

## Archivos Creados/Modificados

### Nuevos archivos:
- `script/sql/fix_decimal_precision.sql` - Script SQL de modificación
- `script/aplicar_decimales.py` - Script de aplicación automática
- `script/generar_script_decimales.py` - Generador de script SQL
- `script/number_formatter.py` - Módulo de formateo de números
- `script/README_DECIMALES.md` - Esta documentación

### Archivos existentes (sin cambios necesarios):
- `script/informes_exportacion.py` - Ya formatea correctamente con 2 decimales

## Soporte

Si encuentras algún problema:

1. Verifica que la base de datos esté accesible
2. Revisa que tienes permisos ALTER TABLE
3. Consulta los logs de error de MySQL
4. Verifica que todas las tablas mencionadas existen en tu base de datos

## Notas Técnicas

- **Tipo DECIMAL(10,2):**
  - 10 dígitos totales (precisión)
  - 2 dígitos después del punto decimal (escala)
  - Rango: -99999999.99 a 99999999.99

- **Ventajas sobre DOUBLE/FLOAT:**
  - Precisión exacta (no hay errores de redondeo)
  - Consistencia en cálculos monetarios
  - Cumplimiento con estándares contables

- **Consideraciones:**
  - Los valores existentes se redondearán a 2 decimales
  - Los cálculos futuros mantendrán exactamente 2 decimales
  - Compatible con todas las operaciones SQL estándar (SUM, AVG, etc.)
