# Importación de Mediciones de OTs

## Descripción

Script para importar las mediciones de trabajos realizados desde el archivo Excel `MEDICIONES OTS.xlsx` a la tabla `tbl_part_presupuesto`.

## Requisitos previos

### 1. Añadir campo fecha a la tabla

Antes de ejecutar la importación, debes ejecutar el script SQL para añadir el campo `fecha`:

```bash
# Si tienes MySQL en el PATH:
mysql -u root -p cert_dev < script/sql/add_fecha_tbl_part_presupuesto.sql

# O usando Python:
python3 -c "
import mysql.connector
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Lauburu1969',
    database='cert_dev'
)
cursor = conn.cursor()
cursor.execute(open('script/sql/add_fecha_tbl_part_presupuesto.sql').read())
conn.commit()
conn.close()
print('✅ Campo fecha añadido exitosamente')
"
```

### 2. Verificar el archivo Excel

El archivo `MEDICIONES OTS.xlsx` debe estar en la raíz del proyecto y tener estas columnas:
- `precio_id`: ID del precio en tbl_pres_precios
- `cantidad`: Cantidad de unidades
- `fecha_unidad`: Fecha de la medición (puede ser NULL)
- `parte_id`: Código del parte (ejemplo: OT/0121, TP/0278)

## Uso

### Modo simulación (dry-run)

Primero ejecuta en modo simulación para verificar que todo está correcto:

```bash
python3 script/importar_mediciones_ots.py --dry-run
```

Esto mostrará:
- Cuántos registros se procesarían
- Qué partes o precios no se encuentran
- Errores potenciales
- **NO insertará datos en la base de datos**

### Importación real

Una vez verificado que todo está correcto:

```bash
python3 script/importar_mediciones_ots.py
```

### Opciones adicionales

```bash
# Especificar esquema diferente
python3 script/importar_mediciones_ots.py --schema mi_esquema

# Especificar credenciales
python3 script/importar_mediciones_ots.py --user usuario --password clave

# Ver ayuda completa
python3 script/importar_mediciones_ots.py --help
```

## Estructura de la tabla tbl_part_presupuesto

Después de ejecutar el script SQL, la tabla tendrá esta estructura:

```sql
CREATE TABLE tbl_part_presupuesto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    parte_id INT NOT NULL,              -- FK a tbl_partes.id
    precio_id INT NOT NULL,             -- FK a tbl_pres_precios.id
    cantidad DECIMAL(10,2) NOT NULL,    -- Cantidad de unidades
    fecha DATE NULL,                    -- Fecha de medición ← NUEVO CAMPO
    precio_unit DECIMAL(10,2) NOT NULL, -- Precio unitario (snapshot)

    FOREIGN KEY (parte_id) REFERENCES tbl_partes(id),
    FOREIGN KEY (precio_id) REFERENCES tbl_pres_precios(id),
    INDEX idx_fecha (fecha)
);
```

## Proceso de importación

El script realiza los siguientes pasos:

1. **Validación del archivo Excel**
   - Verifica que existe
   - Comprueba que tiene las columnas requeridas

2. **Limpieza de datos**
   - Elimina registros con precio_id nulo
   - Convierte fechas al formato correcto de MySQL

3. **Para cada registro:**
   - Busca el ID interno del parte usando su código
   - Obtiene el precio unitario actual de `tbl_pres_precios`
   - Inserta el registro en `tbl_part_presupuesto`

4. **Manejo de errores**
   - Registra partes no encontrados
   - Registra precios no encontrados
   - Muestra resumen al final

## Resultados esperados

### Salida normal

```
================================================================================
IMPORTAR MEDICIONES DE OTS A TBL_PART_PRESUPUESTO
HydroFlow Manager v1.04
================================================================================
Esquema: cert_dev
Modo: IMPORTACIÓN REAL

✅ Archivo Excel válido: 2778 registros encontrados

📖 Leyendo archivo MEDICIONES OTS.xlsx...
   Total de registros a procesar: 2777
   Registros con fecha: 673
   Registros sin fecha: 2104

💾 IMPORTANDO mediciones...
--------------------------------------------------------------------------------
   Procesados: 100/2777 registros...
   Procesados: 200/2777 registros...
   ...

✅ Transacción confirmada (COMMIT)

================================================================================
📊 RESUMEN DE IMPORTACIÓN
================================================================================
Registros procesados:     2777
Registros insertados:     2650
Registros con errores:    127

⚠️  Partes no encontrados (15):
   - OT/9999
   - TP/8888
   ...
```

## Solución de problemas

### Error: "Partes no encontrados"

**Causa:** Los códigos de parte en el Excel no existen en `tbl_partes.codigo`

**Solución:**
1. Verifica los códigos en el Excel
2. Asegúrate de que los partes están creados en la base de datos
3. Revisa que el formato sea correcto (Ej: "OT/0121" no "OT-0121")

### Error: "Precios no encontrados"

**Causa:** Los IDs de precio en el Excel no existen en `tbl_pres_precios.id`

**Solución:**
1. Verifica que los precios estén importados
2. Comprueba los IDs en la tabla tbl_pres_precios
3. Asegúrate de que no haya errores de tipeo en el Excel

### Error: "Can't connect to MySQL server"

**Causa:** MySQL no está corriendo o las credenciales son incorrectas

**Solución:**
1. Verifica que MySQL está corriendo
2. Comprueba usuario y contraseña
3. Usa las opciones --user y --password si es necesario

## Notas importantes

### Sobre precio_unit

El campo `precio_unit` se llena automáticamente con el valor actual de `tbl_pres_precios.coste`. Esto es intencional y permite:

- Mantener histórico de precios
- No afectar presupuestos históricos cuando cambien los precios maestros
- Ver más detalles en: `docs/PRECIO_UNIT_EXPLICACION.md`

### Sobre el campo fecha

- La columna `fecha` es opcional (puede ser NULL)
- Si el Excel no tiene fecha para un registro, se insertará como NULL
- Puedes actualizar las fechas posteriormente si es necesario

### Duplicados

El script NO verifica duplicados. Si ejecutas el script varias veces, insertará los registros múltiples veces. Para evitar esto:

1. Usa siempre `--dry-run` primero
2. Verifica el estado actual de la tabla antes de importar
3. Si necesitas reimportar, limpia la tabla primero:
   ```sql
   TRUNCATE TABLE tbl_part_presupuesto;
   ```

## Ver también

- `docs/PRECIO_UNIT_EXPLICACION.md` - Explicación sobre el campo precio_unit
- `script/sql/add_fecha_tbl_part_presupuesto.sql` - Script para añadir campo fecha
- `script/importar_partes_access.py` - Importación de partes desde Access

---
*Documentación técnica - HydroFlow Manager v1.04*
*Fecha: 2025-11-11*
