-- =====================================================================
-- Script para verificar e insertar municipios faltantes en tbl_municipios
-- =====================================================================
-- Los IDs de municipios requeridos por el Excel son:
-- [1, 2, 3, 4, 5, 6, 9, 10, 21, 26, 41, 44, 45, 46, 48]
-- =====================================================================

-- Paso 1: Verificar cuáles de estos municipios YA existen
SELECT '=== MUNICIPIOS QUE YA EXISTEN ===' AS mensaje;
SELECT id, municipio_nombre, provincia_id, comarca_id, activo
FROM dim_municipios
WHERE id IN (1, 2, 3, 4, 5, 6, 9, 10, 21, 26, 41, 44, 45, 46, 48)
ORDER BY id;

-- Paso 2: Contar cuántos existen vs cuántos se necesitan
SELECT '=== RESUMEN ===' AS mensaje;
SELECT
    COUNT(*) AS municipios_existentes,
    15 AS municipios_requeridos,
    (15 - COUNT(*)) AS municipios_faltantes
FROM dim_municipios
WHERE id IN (1, 2, 3, 4, 5, 6, 9, 10, 21, 26, 41, 44, 45, 46, 48);

-- Paso 3: Identificar cuáles faltan (si alguno)
SELECT '=== MUNICIPIOS FALTANTES ===' AS mensaje;
SELECT t.id_faltante
FROM (
    SELECT 1 AS id_faltante UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL
    SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 9 UNION ALL
    SELECT 10 UNION ALL SELECT 21 UNION ALL SELECT 26 UNION ALL SELECT 41 UNION ALL
    SELECT 44 UNION ALL SELECT 45 UNION ALL SELECT 46 UNION ALL SELECT 48
) AS t
WHERE t.id_faltante NOT IN (SELECT id FROM dim_municipios)
ORDER BY t.id_faltante;

-- =====================================================================
-- NOTA: Si hay municipios faltantes, necesitamos insertarlos antes de
-- poder insertar los datos en tbl_partes.
--
-- Para cada municipio faltante, necesitamos conocer:
-- - municipio_nombre: Nombre del municipio
-- - codigo_ine: Código INE del municipio
-- - provincia_id: ID de la provincia (1=Álava, 2=Bizkaia, 3=Gipuzkoa)
-- - comarca_id: ID de la comarca
-- - activo: 1 para activo, 0 para inactivo
-- =====================================================================
