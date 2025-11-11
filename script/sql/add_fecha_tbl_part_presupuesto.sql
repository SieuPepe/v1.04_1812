-- =====================================================================================
-- Script: Añadir campo fecha a tbl_part_presupuesto
-- Descripción: Añade columna fecha para registrar la fecha de medición/ejecución
-- Autor: HydroFlow Manager v1.04
-- Fecha: 2025-11-11
-- =====================================================================================

USE cert_dev;

-- Añadir columna fecha si no existe
ALTER TABLE tbl_part_presupuesto
ADD COLUMN IF NOT EXISTS fecha DATE NULL COMMENT 'Fecha de medición o ejecución de la partida'
AFTER cantidad;

-- Crear índice para mejorar consultas por fecha
CREATE INDEX IF NOT EXISTS idx_fecha ON tbl_part_presupuesto(fecha);

-- Mostrar la estructura actualizada
DESCRIBE tbl_part_presupuesto;

-- Verificación
SELECT 'Campo fecha añadido exitosamente a tbl_part_presupuesto' AS resultado;
