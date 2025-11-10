-- Script para actualizar la tabla dim_red
-- Fecha: 2025-11-10
-- Descripción: Actualización de códigos y descripciones de redes, añadiendo registro de Saneamiento

-- Iniciar transacción para seguridad
START TRANSACTION;

-- Actualizar registros existentes
UPDATE dim_red SET red_codigo = 'ADU', descripcion = 'Aducción' WHERE id = 1;
UPDATE dim_red SET red_codigo = 'DEP', descripcion = 'Depuración' WHERE id = 2;
UPDATE dim_red SET red_codigo = 'DIS', descripcion = 'Distribución' WHERE id = 3;
UPDATE dim_red SET red_codigo = 'OTR', descripcion = 'Otros' WHERE id = 4;

-- Insertar nuevo registro de Saneamiento
INSERT INTO dim_red (id, red_codigo, descripcion)
VALUES (5, 'SAN', 'Saneamiento')
ON DUPLICATE KEY UPDATE red_codigo = 'SAN', descripcion = 'Saneamiento';

-- Confirmar transacción
COMMIT;

-- Verificar los cambios
SELECT * FROM dim_red ORDER BY id;
