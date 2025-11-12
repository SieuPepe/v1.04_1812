-- Script para actualizar la columna finalizada en tbl_partes
-- Corrige los valores booleanos True/False a 1/0

-- Registros con finalizada = True: 825
-- Registros con finalizada = False: 3

-- IDs de registros con finalizada = False: [424, 427, 744]

-- Actualizar registros con finalizada = False (0)
UPDATE tbl_partes SET finalizada = 0 WHERE id IN (424,427,744);

-- Actualizar todos los demás registros a finalizada = True (1)
UPDATE tbl_partes SET finalizada = 1 WHERE id NOT IN (424,427,744);
