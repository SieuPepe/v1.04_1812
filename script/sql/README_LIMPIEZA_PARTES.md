# Limpieza de Datos de Partes

## Descripción

Este directorio contiene scripts para eliminar TODOS los datos de las tablas de partes (órdenes de trabajo):

### Tablas que se ELIMINARÁN:
- ✓ `tbl_partes` - Tabla principal de partes/órdenes de trabajo
- ✓ `tbl_part_presupuesto` - Presupuestos asociados a partes
- ✓ `tbl_part_certificacion` - Certificaciones de partes

### Tablas que se CONSERVARÁN:
- ✓ `tbl_presupuesto` - Presupuestos de inventario/registros
- ✓ `tbl_pres_certificacion` - Certificaciones de inventario/registros
- ✓ `tbl_parte_estados` - Catálogo de estados
- ✓ `tbl_pres_precios` - Catálogo de precios
- ✓ `dim_*` - Todas las tablas de dimensiones
- ✓ `tbl_inventario` y `tbl_inv_*` - Inventario y registros

---

## Opción 1: Script Python Interactivo (RECOMENDADO)

### Uso:
```bash
cd /home/user/v1.04_1812
python3 script/limpiar_partes.py
```

### Características:
- ✓ Interactivo y seguro
- ✓ Muestra estadísticas ANTES y DESPUÉS
- ✓ Solicita confirmación doble
- ✓ Verifica que otras tablas no se modificaron
- ✓ Lista esquemas disponibles
- ✓ Manejo automático de transacciones

### Flujo:
1. Solicita credenciales de MySQL
2. Lista esquemas/bases de datos disponibles
3. Solicita el nombre del esquema a limpiar
4. Muestra estadísticas de datos actuales
5. Solicita confirmación (debes escribir "SI")
6. Elimina los datos
7. Muestra estadísticas finales
8. Verifica integridad de otras tablas

---

## Opción 2: Script SQL Directo

### Uso desde MySQL Workbench:
```sql
USE nombre_esquema;
SOURCE /home/user/v1.04_1812/script/sql/limpiar_datos_partes.sql;
```

### Uso desde línea de comandos:
```bash
mysql -u root -p nombre_esquema < /home/user/v1.04_1812/script/sql/limpiar_datos_partes.sql
```

### Características:
- ✓ Ejecución directa en MySQL
- ✓ Muestra estadísticas ANTES y DESPUÉS
- ✓ Resetea AUTO_INCREMENT
- ✓ Manejo de claves foráneas
- ✓ Verificación final

---

## ⚠️ IMPORTANTE - ANTES DE EJECUTAR

### 1. CREAR BACKUP
```bash
# Backup completo del esquema
mysqldump -u root -p --port=3307 nombre_esquema > backup_antes_limpieza.sql

# O backup solo de las 3 tablas
mysqldump -u root -p --port=3307 nombre_esquema \
  tbl_partes tbl_part_presupuesto tbl_part_certificacion \
  > backup_tablas_partes.sql
```

### 2. VERIFICAR ESQUEMA
```sql
-- Asegúrate de estar en el esquema correcto
SELECT DATABASE();

-- Ver cuántos registros hay
SELECT COUNT(*) FROM tbl_partes;
SELECT COUNT(*) FROM tbl_part_presupuesto;
SELECT COUNT(*) FROM tbl_part_certificacion;
```

### 3. CONFIRMAR INTENCIÓN
Esta operación es **IRREVERSIBLE**. Los datos NO se pueden recuperar sin un backup.

---

## Ejemplo de Ejecución

```bash
$ python3 script/limpiar_partes.py

======================================================================
SCRIPT DE LIMPIEZA DE DATOS DE PARTES
======================================================================

Usuario de MySQL (default: root): root
Contraseña: ********

======================================================================
ESQUEMAS/BASES DE DATOS DISPONIBLES
======================================================================
  1. manager
  2. proyecto_tipo
  3. PR001
  4. test_db

======================================================================
Introduce el nombre del esquema a limpiar: proyecto_tipo

======================================================================
LIMPIEZA DE DATOS DE PARTES - Esquema: proyecto_tipo
======================================================================

======================================================================
ESTADÍSTICAS ANTES DE BORRAR
======================================================================
  Partes/Órdenes de Trabajo                        150 registros
  Presupuestos de Partes                           320 registros
  Certificaciones de Partes                        180 registros

  Rango de fechas: 2024-01-15 a 2025-11-08

⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠
⚠  ADVERTENCIA: Esta operación es IRREVERSIBLE
⚠  Se eliminarán TODOS los datos de las 3 tablas de partes
⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠

¿Estás seguro de que quieres continuar? (escribe 'SI' para confirmar): SI

======================================================================
ELIMINANDO DATOS...
======================================================================
  ✓ tbl_part_certificacion: 180 registros eliminados
  ✓ tbl_part_presupuesto: 320 registros eliminados
  ✓ tbl_partes: 150 registros eliminados

  ✓ Cambios confirmados (COMMIT)

======================================================================
ESTADÍSTICAS DESPUÉS DE BORRAR
======================================================================
  Partes/Órdenes de Trabajo                          0 registros  ✓ LIMPIA
  Presupuestos de Partes                              0 registros  ✓ LIMPIA
  Certificaciones de Partes                           0 registros  ✓ LIMPIA

======================================================================
VERIFICACIÓN DE TABLAS NO AFECTADAS
======================================================================
  Presupuestos de Inventario                        450 registros  (OK)
  Certificaciones de Inventario                     280 registros  (OK)
  Estados de Partes                                   5 registros  (OK)
  Catálogo de Redes                                  10 registros  (OK)
  Catálogo de Tipos de Trabajo                       3 registros  (OK)
  Catálogo de Códigos de Trabajo                    22 registros  (OK)

======================================================================
✓ LIMPIEZA COMPLETADA EXITOSAMENTE
======================================================================
```

---

## Restaurar desde Backup (si es necesario)

Si necesitas restaurar los datos eliminados:

```bash
# Restaurar backup completo
mysql -u root -p nombre_esquema < backup_antes_limpieza.sql

# O restaurar solo las 3 tablas
mysql -u root -p nombre_esquema < backup_tablas_partes.sql
```

---

## Preguntas Frecuentes

### ¿Se eliminan las tablas o solo los datos?
Solo se eliminan los **DATOS**. Las tablas, estructura, índices y claves foráneas se conservan intactos.

### ¿Se resetean los contadores AUTO_INCREMENT?
Sí, los contadores se resetean a 1. El próximo registro insertado tendrá ID = 1.

### ¿Qué pasa con las claves foráneas?
El script desactiva temporalmente la verificación de FK durante la eliminación y la reactiva al final.

### ¿Puedo cancelar la operación?
Sí, cuando el script Python solicita confirmación, escribe cualquier cosa diferente a "SI" para cancelar.

### ¿Qué pasa si hay un error durante la ejecución?
El script Python usa transacciones. Si hay un error, se hace ROLLBACK automáticamente.

---

## Soporte

Si tienes problemas:
1. Verifica que tienes permisos en la base de datos
2. Verifica que las tablas existen en el esquema
3. Revisa los logs de error
4. Contacta al administrador del sistema
