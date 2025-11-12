-- =====================================================================
-- Script para insertar municipios faltantes (IDs 1-48) en dim_municipios
-- =====================================================================
-- Este script inserta los municipios con IDs 1-48 que no existan
-- usando INSERT IGNORE para evitar duplicados
-- =====================================================================

-- Insertar municipios con IDs específicos (1-48)
-- NOTA: Solo se insertarán si no existen (INSERT IGNORE)
-- Usamos códigos INE genéricos (90000001-90000015) para evitar conflictos
-- Estos pueden actualizarse más tarde con los datos reales
INSERT IGNORE INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo)
VALUES
    (1, 90000001, 'Municipio 1', 1, 1, 1),
    (2, 90000002, 'Municipio 2', 1, 1, 1),
    (3, 90000003, 'Municipio 3', 1, 1, 1),
    (4, 90000004, 'Municipio 4', 1, 1, 1),
    (5, 90000005, 'Municipio 5', 1, 1, 1),
    (6, 90000006, 'Municipio 6', 1, 1, 1),
    (9, 90000009, 'Municipio 9', 1, 1, 1),
    (10, 90000010, 'Municipio 10', 1, 1, 1),
    (21, 90000021, 'Municipio 21', 1, 3, 1),
    (26, 90000026, 'Municipio 26', 1, 3, 1),
    (41, 90000041, 'Municipio 41', 1, 3, 1),
    (44, 90000044, 'Municipio 44', 2, 8, 1),
    (45, 90000045, 'Municipio 45', 2, 8, 1),
    (46, 90000046, 'Municipio 46', 2, 8, 1),
    (48, 90000048, 'Municipio 48', 2, 8, 1);

-- Verificar los municipios insertados
SELECT 'Municipios que ahora existen (IDs 1-48):' AS mensaje;
SELECT id, municipio_nombre, provincia_id, comarca_id, activo
FROM dim_municipios
WHERE id IN (1, 2, 3, 4, 5, 6, 9, 10, 21, 26, 41, 44, 45, 46, 48)
ORDER BY id;
