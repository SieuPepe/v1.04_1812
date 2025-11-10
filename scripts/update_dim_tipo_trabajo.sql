-- Script para actualizar la tabla dim_tipo_trabajo
-- Fecha: 2025-11-10
-- Descripción: Actualización completa de tipos de trabajo con nuevos códigos

-- Iniciar transacción para seguridad
START TRANSACTION;

-- Limpiar la tabla para evitar registros antiguos
DELETE FROM dim_tipo_trabajo;

-- Insertar los nuevos registros
INSERT INTO dim_tipo_trabajo (id, tipo_codigo, descripcion) VALUES
(1, 'OT', 'Orden de Trabajo'),
(2, 'TP', 'Trabajos Programados'),
(3, 'GF', 'Gastos Fijos');

-- Confirmar transacción
COMMIT;

-- Verificar los cambios
SELECT * FROM dim_tipo_trabajo ORDER BY id;
