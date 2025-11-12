-- =====================================================================
-- Script para insertar comarcas y municipios adicionales
-- =====================================================================
-- Este script:
-- 1. Inserta 2 nuevas comarcas en dim_comarcas (VITO y ALAV)
-- 2. Inserta 8 nuevos municipios "Varios" en dim_municipios
-- =====================================================================

-- =====================================================================
-- PASO 1: Insertar nuevas comarcas en dim_comarcas
-- =====================================================================
INSERT INTO dim_comarcas (id, provincia_id, comarca_codigo, comarca_nombre, created_at)
VALUES
    (9, 1, 'VITO', 'Vitoria', NOW()),
    (10, 1, 'ALAV', 'Alava completa', NOW())
ON DUPLICATE KEY UPDATE
    provincia_id = VALUES(provincia_id),
    comarca_codigo = VALUES(comarca_codigo),
    comarca_nombre = VALUES(comarca_nombre);

-- =====================================================================
-- PASO 2: Insertar nuevos municipios "Varios" en dim_municipios
-- =====================================================================
INSERT INTO dim_municipios (id, codigo_ine, nombre, provincia_id, comarca_id, activo)
VALUES
    (304, 0, 'Varios AIARA', 1, 1, 1),
    (305, 0, 'Varios LAGUA', 1, 2, 1),
    (306, 0, 'Varios LLANA', 1, 3, 1),
    (307, 0, 'Varios GORBE', 1, 4, 1),
    (308, 0, 'Varios AANA', 1, 5, 1),
    (309, 0, 'Varios CAMPE', 1, 6, 1),
    (310, 0, 'Vitoria', 1, 9, 1),
    (311, 0, 'Varios ALAV', 1, 10, 1)
ON DUPLICATE KEY UPDATE
    nombre = VALUES(nombre),
    provincia_id = VALUES(provincia_id),
    comarca_id = VALUES(comarca_id),
    activo = VALUES(activo);

-- =====================================================================
-- Verificación de los datos insertados
-- =====================================================================
SELECT 'Nuevas comarcas insertadas:' AS mensaje;
SELECT id, provincia_id, comarca_codigo, comarca_nombre
FROM dim_comarcas
WHERE id IN (9, 10);

SELECT 'Nuevos municipios insertados:' AS mensaje;
SELECT id, codigo_ine, nombre, provincia_id, comarca_id, activo
FROM dim_municipios
WHERE id BETWEEN 304 AND 311;
