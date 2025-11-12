-- =====================================================================
-- Script para verificar municipios requeridos por tbl_partes
-- =====================================================================
-- Los IDs de municipios que aparecen en el Excel son:
-- [1, 2, 3, 4, 5, 6, 9, 10, 21, 26, 41, 44, 45, 46, 48]
-- =====================================================================

-- Verificar cuáles de estos municipios existen en tbl_municipios
SELECT 'Municipios que SÍ existen en la base de datos:' AS mensaje;
SELECT id, NAMEUNIT, CODIGOINE, provincia_id
FROM tbl_municipios
WHERE id IN (1, 2, 3, 4, 5, 6, 9, 10, 21, 26, 41, 44, 45, 46, 48)
ORDER BY id;

-- Contar cuántos existen
SELECT 'Total de municipios existentes vs requeridos:' AS mensaje;
SELECT
    COUNT(*) AS municipios_existentes,
    15 AS municipios_requeridos,
    (15 - COUNT(*)) AS municipios_faltantes
FROM tbl_municipios
WHERE id IN (1, 2, 3, 4, 5, 6, 9, 10, 21, 26, 41, 44, 45, 46, 48);

-- Identificar cuáles faltan (si alguno)
SELECT 'Municipios que FALTAN (si alguno):' AS mensaje;
SELECT id_faltante
FROM (
    SELECT 1 AS id_faltante UNION ALL
    SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL
    SELECT 6 UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 21 UNION ALL
    SELECT 26 UNION ALL SELECT 41 UNION ALL SELECT 44 UNION ALL SELECT 45 UNION ALL
    SELECT 46 UNION ALL SELECT 48
) AS requeridos
WHERE id_faltante NOT IN (SELECT id FROM tbl_municipios)
ORDER BY id_faltante;
