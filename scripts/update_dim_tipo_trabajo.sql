-- Script para actualizar la tabla dim_tipo_trabajo
-- Fecha: 2025-11-10
-- Descripción: Actualización de códigos y descripciones de tipos de trabajo

-- Iniciar transacción para seguridad
START TRANSACTION;

-- Actualizar registros existentes
UPDATE dim_tipo_trabajo SET tipo_codigo = 'OT', descripcion = 'Orden de Trabajo' WHERE id = 1;
UPDATE dim_tipo_trabajo SET tipo_codigo = 'TP', descripcion = 'Trabajos Programados' WHERE id = 2;
UPDATE dim_tipo_trabajo SET tipo_codigo = 'GF', descripcion = 'Gastos Fijos' WHERE id = 3;

-- Insertar nuevos registros si no existen (por si acaso faltan)
INSERT INTO dim_tipo_trabajo (id, tipo_codigo, descripcion)
VALUES
(1, 'OT', 'Orden de Trabajo'),
(2, 'TP', 'Trabajos Programados'),
(3, 'GF', 'Gastos Fijos')
ON DUPLICATE KEY UPDATE tipo_codigo = VALUES(tipo_codigo), descripcion = VALUES(descripcion);

-- Confirmar transacción
COMMIT;

-- Verificar los cambios
SELECT * FROM dim_tipo_trabajo ORDER BY id;
