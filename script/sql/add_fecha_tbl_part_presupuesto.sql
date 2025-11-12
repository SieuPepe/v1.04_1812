-- =====================================================================================
-- Script: Añadir campo fecha a tbl_part_presupuesto
-- Descripción: Añade columna fecha para registrar la fecha de medición/ejecución
-- Autor: HydroFlow Manager v1.04
-- Fecha: 2025-11-11
-- =====================================================================================

USE cert_dev;

-- Añadir columna fecha si no existe (compatible con MySQL 5.x)
SET @col_exists = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'tbl_part_presupuesto'
    AND COLUMN_NAME = 'fecha'
);

SET @sql = IF(@col_exists = 0,
    'ALTER TABLE tbl_part_presupuesto ADD COLUMN fecha DATE NULL COMMENT ''Fecha de medición o ejecución de la partida'' AFTER cantidad',
    'SELECT ''La columna fecha ya existe'' AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Crear índice para mejorar consultas por fecha (compatible con MySQL 5.x)
SET @idx_exists = (
    SELECT COUNT(*)
    FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'tbl_part_presupuesto'
    AND INDEX_NAME = 'idx_fecha'
);

SET @sql = IF(@idx_exists = 0,
    'CREATE INDEX idx_fecha ON tbl_part_presupuesto(fecha)',
    'SELECT ''El índice idx_fecha ya existe'' AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Mostrar la estructura actualizada
DESCRIBE tbl_part_presupuesto;

-- Verificación
SELECT 'Campo fecha añadido exitosamente a tbl_part_presupuesto' AS resultado;
