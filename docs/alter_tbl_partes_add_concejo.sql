-- ============================================================================
-- HydroFlow Manager - Añadir columna concejo_id a tbl_partes
-- Ejecutar DESPUÉS de crear la tabla dim_concejos
-- ============================================================================

-- Añadir columna concejo_id a tbl_partes (opcional, puede ser NULL)
ALTER TABLE tbl_partes
ADD COLUMN concejo_id INT DEFAULT NULL AFTER municipio_id;

-- Añadir Foreign Key a dim_concejos
ALTER TABLE tbl_partes
ADD CONSTRAINT fk_partes_concejo
FOREIGN KEY (concejo_id) REFERENCES dim_concejos(id) ON DELETE SET NULL;

-- Añadir índice para mejorar búsquedas por concejo
ALTER TABLE tbl_partes
ADD INDEX idx_concejo (concejo_id);

-- ============================================================================
-- Verificación (opcional)
-- ============================================================================
-- SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
-- FROM information_schema.COLUMNS
-- WHERE TABLE_NAME = 'tbl_partes' AND COLUMN_NAME = 'concejo_id';
