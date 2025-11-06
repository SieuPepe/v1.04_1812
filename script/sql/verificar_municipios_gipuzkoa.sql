-- Script de verificación de municipios de Gipuzkoa
-- ===================================================

-- 1. Ver municipios de Gipuzkoa insertados
SELECT 'Municipios de Gipuzkoa (primeros 20):' AS resultado;
SELECT id, provincia_id, comarca_id, NAMEUNIT, CODIGOINE
FROM tbl_municipios
WHERE provincia_id = 3
ORDER BY CODIGOINE
LIMIT 20;

-- 2. Contar municipios por provincia
SELECT 'Conteo por provincia:' AS resultado;
SELECT
    p.nombre AS provincia,
    COUNT(m.id) AS total_municipios,
    SUM(CASE WHEN m.NAMEUNIT IS NULL OR m.NAMEUNIT = '' THEN 1 ELSE 0 END) AS sin_nombre,
    SUM(CASE WHEN m.NAMEUNIT IS NOT NULL AND m.NAMEUNIT != '' THEN 1 ELSE 0 END) AS con_nombre
FROM dim_provincias p
LEFT JOIN tbl_municipios m ON m.provincia_id = p.id
GROUP BY p.id, p.nombre
ORDER BY p.codigo;

-- 3. Ver todos los municipios sin nombre
SELECT 'Municipios sin nombre:' AS resultado;
SELECT id, provincia_id, comarca_id, CODIGOINE
FROM tbl_municipios
WHERE NAMEUNIT IS NULL OR NAMEUNIT = ''
ORDER BY provincia_id, CODIGOINE;

-- 4. Ver estructura de la tabla
SELECT 'Estructura de tbl_municipios:' AS resultado;
DESCRIBE tbl_municipios;
