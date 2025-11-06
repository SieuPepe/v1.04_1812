-- ==============================================================================
-- SCRIPT: Eliminar dim_ot y ot_id de tbl_partes
-- ==============================================================================
-- Fecha: 2025-10-29
-- Propósito: Eliminar tabla dim_ot y campo ot_id de tbl_partes
-- Razón: dim_ot no representa ningún concepto del negocio.
--        El código de OT/Parte se autogenera en el campo tbl_partes.codigo
-- ==============================================================================

-- Paso 1: Eliminar Foreign Key de tbl_partes hacia dim_ot
ALTER TABLE tbl_partes DROP FOREIGN KEY IF EXISTS fk_partes_ot;

-- Paso 2: Eliminar columna ot_id de tbl_partes
ALTER TABLE tbl_partes DROP COLUMN IF EXISTS ot_id;

-- Paso 3: Eliminar tabla dim_ot
DROP TABLE IF EXISTS dim_ot;

-- ==============================================================================
-- VERIFICACIÓN
-- ==============================================================================
-- Verificar que la columna ot_id no existe en tbl_partes:
-- DESCRIBE tbl_partes;

-- Verificar que dim_ot no existe:
-- SHOW TABLES LIKE 'dim_ot';
-- ==============================================================================
