-- ============================================================================
-- LIMPIEZA DE DATOS DE PARTES
-- ============================================================================
-- Este script elimina TODOS los datos de las tablas de partes:
--   1. tbl_part_certificacion (certificaciones de partes)
--   2. tbl_part_presupuesto (presupuestos de partes)
--   3. tbl_partes (partes/órdenes de trabajo)
--
-- NO elimina:
--   - tbl_presupuesto (presupuestos de inventario/registros)
--   - tbl_pres_certificacion (certificaciones de inventario/registros)
--   - Tablas de dimensiones (dim_*, tbl_parte_estados, etc.)
--   - Catálogos de precios (tbl_pres_precios, tbl_pres_capitulos, etc.)
--
-- IMPORTANTE: Este script es DESTRUCTIVO. Los datos NO se pueden recuperar.
-- Asegúrate de tener un backup antes de ejecutar.
-- ============================================================================

-- Mostrar esquema actual
SELECT DATABASE() AS esquema_actual;

-- ============================================================================
-- PASO 1: VERIFICACIÓN PREVIA - Contar registros ANTES de borrar
-- ============================================================================

SELECT '=== ESTADÍSTICAS ANTES DE BORRAR ===' AS info;

SELECT
    'tbl_partes' AS tabla,
    COUNT(*) AS registros_totales
FROM tbl_partes
UNION ALL
SELECT
    'tbl_part_presupuesto' AS tabla,
    COUNT(*) AS registros_totales
FROM tbl_part_presupuesto
UNION ALL
SELECT
    'tbl_part_certificacion' AS tabla,
    COUNT(*) AS registros_totales
FROM tbl_part_certificacion;

-- Mostrar rangos de datos
SELECT
    'tbl_partes' AS tabla,
    MIN(creado_en) AS fecha_mas_antigua,
    MAX(creado_en) AS fecha_mas_reciente
FROM tbl_partes
WHERE creado_en IS NOT NULL;

-- ============================================================================
-- PASO 2: DESACTIVAR VERIFICACIÓN DE CLAVES FORÁNEAS (temporalmente)
-- ============================================================================
-- Esto permite eliminar en cualquier orden sin problemas de FK

SET FOREIGN_KEY_CHECKS = 0;

-- ============================================================================
-- PASO 3: ELIMINAR DATOS DE LAS 3 TABLAS
-- ============================================================================

-- 3.1: Eliminar certificaciones de partes
DELETE FROM tbl_part_certificacion;

SELECT 'tbl_part_certificacion eliminada' AS info, ROW_COUNT() AS registros_eliminados;

-- 3.2: Eliminar presupuestos de partes
DELETE FROM tbl_part_presupuesto;

SELECT 'tbl_part_presupuesto eliminada' AS info, ROW_COUNT() AS registros_eliminados;

-- 3.3: Eliminar partes
DELETE FROM tbl_partes;

SELECT 'tbl_partes eliminada' AS info, ROW_COUNT() AS registros_eliminados;

-- ============================================================================
-- PASO 4: REACTIVAR VERIFICACIÓN DE CLAVES FORÁNEAS
-- ============================================================================

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================================
-- PASO 5: REINICIAR AUTO_INCREMENT (opcional)
-- ============================================================================
-- Esto resetea los contadores de ID a 1 para empezar desde cero

ALTER TABLE tbl_part_certificacion AUTO_INCREMENT = 1;
ALTER TABLE tbl_part_presupuesto AUTO_INCREMENT = 1;
ALTER TABLE tbl_partes AUTO_INCREMENT = 1;

SELECT 'Auto-increment reseteado' AS info;

-- ============================================================================
-- PASO 6: VERIFICACIÓN POSTERIOR - Confirmar que las tablas están vacías
-- ============================================================================

SELECT '=== ESTADÍSTICAS DESPUÉS DE BORRAR ===' AS info;

SELECT
    'tbl_partes' AS tabla,
    COUNT(*) AS registros_restantes,
    CASE WHEN COUNT(*) = 0 THEN '✓ LIMPIA' ELSE '⚠ TIENE DATOS' END AS estado
FROM tbl_partes
UNION ALL
SELECT
    'tbl_part_presupuesto' AS tabla,
    COUNT(*) AS registros_restantes,
    CASE WHEN COUNT(*) = 0 THEN '✓ LIMPIA' ELSE '⚠ TIENE DATOS' END AS estado
FROM tbl_part_presupuesto
UNION ALL
SELECT
    'tbl_part_certificacion' AS tabla,
    COUNT(*) AS registros_restantes,
    CASE WHEN COUNT(*) = 0 THEN '✓ LIMPIA' ELSE '⚠ TIENE DATOS' END AS estado
FROM tbl_part_certificacion;

-- ============================================================================
-- PASO 7: VERIFICAR QUE NO SE TOCARON OTRAS TABLAS
-- ============================================================================

SELECT '=== VERIFICACIÓN DE TABLAS NO AFECTADAS ===' AS info;

SELECT
    'tbl_presupuesto' AS tabla,
    COUNT(*) AS registros,
    'NO debe haberse modificado' AS nota
FROM tbl_presupuesto
UNION ALL
SELECT
    'tbl_pres_certificacion' AS tabla,
    COUNT(*) AS registros,
    'NO debe haberse modificado' AS nota
FROM tbl_pres_certificacion
UNION ALL
SELECT
    'tbl_parte_estados' AS tabla,
    COUNT(*) AS registros,
    'NO debe haberse modificado' AS nota
FROM tbl_parte_estados
UNION ALL
SELECT
    'dim_red' AS tabla,
    COUNT(*) AS registros,
    'NO debe haberse modificado' AS nota
FROM dim_red
UNION ALL
SELECT
    'dim_tipo_trabajo' AS tabla,
    COUNT(*) AS registros,
    'NO debe haberse modificado' AS nota
FROM dim_tipo_trabajo
UNION ALL
SELECT
    'dim_codigo_trabajo' AS tabla,
    COUNT(*) AS registros,
    'NO debe haberse modificado' AS nota
FROM dim_codigo_trabajo;

-- ============================================================================
-- FIN DEL SCRIPT
-- ============================================================================

SELECT '✓ LIMPIEZA COMPLETADA - Las 3 tablas de partes están vacías' AS resultado_final;

-- ============================================================================
-- NOTAS DE USO:
-- ============================================================================
/*
1. CÓMO EJECUTAR ESTE SCRIPT:

   Opción A - Desde MySQL Workbench:
   - Conectar al servidor MySQL
   - Seleccionar el esquema: USE nombre_esquema;
   - Abrir este archivo y ejecutar (Ctrl+Shift+Enter)

   Opción B - Desde línea de comandos:
   mysql -u usuario -p nombre_esquema < limpiar_datos_partes.sql

2. ANTES DE EJECUTAR:
   - IMPORTANTE: Crear un backup del esquema
   - Verificar que estás en el esquema correcto (SELECT DATABASE();)
   - Confirmar que quieres eliminar TODOS los datos de partes

3. DESPUÉS DE EJECUTAR:
   - Verificar las estadísticas finales
   - Confirmar que las 3 tablas están vacías (COUNT = 0)
   - Verificar que las otras tablas no se modificaron

4. REVERSIÓN:
   - Si tienes un backup, puedes restaurar los datos
   - No hay forma de deshacer esta operación sin backup

5. QUÉ SE ELIMINA:
   ✓ Todos los partes (tbl_partes)
   ✓ Todos los presupuestos de partes (tbl_part_presupuesto)
   ✓ Todas las certificaciones de partes (tbl_part_certificacion)

6. QUÉ SE CONSERVA:
   ✓ Estados de partes (tbl_parte_estados)
   ✓ Dimensiones (dim_red, dim_tipo_trabajo, dim_codigo_trabajo, etc.)
   ✓ Catálogo de precios (tbl_pres_precios, tbl_pres_capitulos)
   ✓ Presupuestos de inventario (tbl_presupuesto)
   ✓ Certificaciones de inventario (tbl_pres_certificacion)
   ✓ Inventario/registros (tbl_inventario, tbl_inv_*)
*/
