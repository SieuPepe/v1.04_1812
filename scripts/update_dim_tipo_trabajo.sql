-- Script para actualizar la tabla dim_tipo_trabajo
-- Fecha: 2025-11-10
-- Descripción: Actualización de códigos y descripciones de tipos de trabajo

-- Iniciar transacción para seguridad
START TRANSACTION;

-- Actualizar registros existentes
UPDATE dim_tipo_trabajo SET tipo_codigo = 'OT', descripcion = 'Orden de Trabajo' WHERE id = 1;
UPDATE dim_tipo_trabajo SET tipo_codigo = 'TP', descripcion = 'Trabajos Programados' WHERE id = 2;
UPDATE dim_tipo_trabajo SET tipo_codigo = 'GF', descripcion = 'Gastos Fijos' WHERE id = 3;

-- Confirmar transacción
COMMIT;

-- Verificar los cambios
SELECT * FROM dim_tipo_trabajo ORDER BY id;
