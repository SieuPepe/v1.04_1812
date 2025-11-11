-- Script para actualizar columna finalizada a 1 (compatible con safe update mode)
-- Actualiza todos los registros usando la columna id (KEY)
UPDATE tbl_partes SET finalizada = 1 WHERE id > 0;
