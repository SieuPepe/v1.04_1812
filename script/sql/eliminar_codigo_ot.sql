-- ============================================================================
-- Script para eliminar la columna codigo_ot de tbl_partes
-- Esta columna es obsoleta, ya no se usa dim_ot
--
-- USO:
-- mysql -u root -phydroflow cert_dev < elimin ar_codigo_ot.sql
-- mysql -u root -phydroflow proyecto_tipo < eliminar_codigo_ot.sql
-- ============================================================================

SET @schema_name = DATABASE();

-- Verificar si la columna existe antes de intentar eliminarla
SET @column_exists = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = @schema_name
      AND TABLE_NAME = 'tbl_partes'
      AND COLUMN_NAME = 'codigo_ot'
);

-- Si existe, eliminarla
SET @sql = IF(
    @column_exists > 0,
    'ALTER TABLE tbl_partes DROP COLUMN codigo_ot',
    'SELECT "La columna codigo_ot no existe en tbl_partes" AS Info'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SELECT '✓ Columna codigo_ot eliminada correctamente' AS Resultado;
