# Actualización de dim_codigo_trabajo

Este directorio contiene scripts para actualizar las descripciones de la tabla `dim_codigo_trabajo` con los 22 códigos de trabajo oficiales.

## Scripts disponibles

### 1. `actualizar_dim_codigo_trabajo.sql`
Script que **TRUNCA** la tabla y reinserta todos los registros.

**Ventajas:**
- Garantiza datos limpios
- Resetea el AUTO_INCREMENT

**Desventajas:**
- Fallará si hay claves foráneas activas que referencien esta tabla
- Elimina cualquier registro adicional que pueda existir

**Uso:**
```bash
mysql -u [usuario] -p [nombre_db] < script/sql/actualizar_dim_codigo_trabajo.sql
```

### 2. `actualizar_dim_codigo_trabajo_seguro.sql` (RECOMENDADO)
Script que **actualiza** las descripciones usando INSERT ... ON DUPLICATE KEY UPDATE.

**Ventajas:**
- Funciona incluso con claves foráneas activas
- No elimina registros, solo actualiza
- Desactiva automáticamente registros con id > 22

**Desventajas:**
- Mantiene registros antiguos (aunque desactivados)

**Uso:**
```bash
mysql -u [usuario] -p [nombre_db] < script/sql/actualizar_dim_codigo_trabajo_seguro.sql
```

## Códigos de Trabajo Actualizados

| ID | Código | Descripción |
|----|--------|-------------|
| 1  | 1      | Mantenimiento preventivo saneamiento |
| 2  | 2      | Limpieza captaciones |
| 3  | 3      | Mantenimiento fosas sépticas |
| 4  | 4      | Inventario y digitalización redes abastecimiento |
| 5  | 5      | Inventario y digitalización redes saneamiento |
| 6  | 6      | Inventario y digitalización aducción |
| 7  | 7      | Localización fugas abastecimiento |
| 8  | 8      | Instalación contadores |
| 9  | 9      | Desinstalación contadores |
| 10 | 10     | Sustitución contadores |
| 11 | 11     | Lectura contadores sectoriales |
| 12 | 12     | Cortes de agua |
| 13 | 13     | Asistencia técnica a URBIDE y organismos públicos |
| 14 | 14     | Maniobras válvulas |
| 15 | 15     | Gestión de la explotación |
| 16 | 16     | Limpieza colectores pluviales |
| 17 | 17     | Limpieza de red abastecimiento |
| 18 | 18     | Ejecución y conexión acometida |
| 19 | 19     | Revisión de sectores |
| 20 | 20     | Localización de fugas en Saneamiento |
| 21 | 21     | Realización de informes de Saneamiento |
| 22 | 22     | Realización de informes de Abastecimiento |

## Actualización en datos de prueba

El archivo `script/generar_datos_prueba.py` también ha sido actualizado para incluir estos 22 códigos de trabajo cuando se generan nuevas bases de datos de prueba.

## Recomendación

Se recomienda usar el script **seguro** (`actualizar_dim_codigo_trabajo_seguro.sql`) en bases de datos de producción o que ya tengan datos, ya que no elimina registros y funciona correctamente con claves foráneas activas.
