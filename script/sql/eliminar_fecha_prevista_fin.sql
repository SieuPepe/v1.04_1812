-- ============================================================================
-- Script para eliminar la columna fecha_prevista_fin de tbl_partes
--
-- USO:
-- mysql -u root -phydroflow cert_dev < eliminar_fecha_prevista_fin.sql
-- mysql -u root -phydroflow proyecto_tipo < eliminar_fecha_prevista_fin.sql
-- ============================================================================

SET @schema_name = DATABASE();

-- Verificar si la columna existe antes de intentar eliminarla
SET @column_exists = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = @schema_name
      AND TABLE_NAME = 'tbl_partes'
      AND COLUMN_NAME = 'fecha_prevista_fin'
);

-- Si existe, eliminarla
SET @sql = IF(
    @column_exists > 0,
    'ALTER TABLE tbl_partes DROP COLUMN fecha_prevista_fin',
    'SELECT "La columna fecha_prevista_fin no existe en tbl_partes" AS Info'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SELECT '✓ Columna fecha_prevista_fin eliminada correctamente' AS Resultado;
