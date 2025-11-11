# Instrucciones para Importar Datos de Excel a tbl_partes

## Archivos Generados

- **Para exportar.xlsx**: Archivo Excel con 828 registros de partes para importar
- **importar_partes_desde_excel.sql**: Script SQL listo para ejecutar en MySQL Workbench
- **script/generar_script_importacion.py**: Script Python generador (por si necesitas regenerar)

## Pasos para Importar en MySQL Workbench

### 1. Abrir MySQL Workbench
Conecta a tu servidor MySQL con las credenciales apropiadas.

### 2. Abrir el Script SQL
- Ve a: `File > Open SQL Script...`
- Selecciona el archivo: `importar_partes_desde_excel.sql`

### 3. Ejecutar el Script
- Presiona `Ctrl + Shift + Enter` (o haz clic en el icono de rayo con documentos)
- El script se ejecutará completamente y mostrará el progreso

## Qué Hace el Script

1. **Desactiva temporalmente las restricciones de claves foráneas** para evitar errores
2. **Añade automáticamente los campos necesarios** si no existen en tbl_partes:
   - titulo
   - descripcion_larga, descripcion_corta
   - id_estado, finalizada
   - localizacion, id_municipio
   - latitud, longitud
   - observaciones, trabajadores
   - estado

3. **Inserta los 828 registros** del archivo Excel
4. **Reactiva las restricciones** de claves foráneas
5. **Muestra estadísticas** de verificación al final

## Características del Script

- ✅ **Seguro**: Usa transacciones (COMMIT al final, puedes hacer ROLLBACK si algo falla)
- ✅ **Idempotente**: Añade campos solo si no existen
- ✅ **Completo**: Mapea todos los campos del Excel correctamente
- ✅ **Corregido**: Convierte valores booleanos y corrige typos (descripion → descripcion)

## Si Algo Sale Mal

Si hay un error durante la ejecución:

```sql
-- Deshacer todos los cambios
ROLLBACK;
```

## Verificación Post-Importación

Al final del script se ejecutan automáticamente:

```sql
-- Ver total de registros
SELECT COUNT(*) as 'Total registros en tbl_partes' FROM cert_dev.tbl_partes;

-- Ver últimos 10 registros insertados
SELECT * FROM cert_dev.tbl_partes ORDER BY id DESC LIMIT 10;
```

## Regenerar el Script (Opcional)

Si necesitas modificar el script o regenerarlo:

```bash
python3 script/generar_script_importacion.py
```

El script te preguntará el nombre del schema (por defecto: cert_dev).

## Estructura de Datos

El Excel contiene estos campos (828 registros):
- Información básica: codigo, titulo, descripcion
- Fechas: fecha_inicio, fecha_fin
- Clasificación: red_id, tipo_trabajo_id, cod_trabajo_id, tipo_rep_id
- Geografía: provincia_id, comarca_id, municipio_id, localizacion
- Coordenadas: latitud, longitud
- Estado: estado, id_estado, finalizada
- Otros: trabajadores, observaciones

---

**Fecha de generación**: 2025-11-11
**Total de registros**: 828
**Schema destino**: cert_dev
