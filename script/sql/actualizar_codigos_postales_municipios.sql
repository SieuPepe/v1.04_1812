-- =====================================================================
-- Script para actualizar códigos postales en dim_municipios
-- Generado: 2025-11-12 07:28:23
-- Total de municipios: 52
-- =====================================================================

-- =====================================================================
-- PASO 1: Agregar columna codigo_postal a dim_municipios
-- =====================================================================
SET @col_exists = (SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'dim_municipios'
    AND COLUMN_NAME = 'codigo_postal');

SET @sql_add_col = IF(@col_exists = 0,
    'ALTER TABLE dim_municipios ADD COLUMN codigo_postal VARCHAR(10) DEFAULT NULL AFTER municipio_nombre',
    'SELECT "Columna codigo_postal ya existe en dim_municipios" AS mensaje');

PREPARE stmt FROM @sql_add_col;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Verificar duplicados en los códigos postales
-- ADVERTENCIA: Códigos postales duplicados encontrados:
-- 01320: Moreda de Álava / Moreda Araba
-- 01309: Navaridas
-- 01320: Oyón-Oion
-- 01307: Samaniego
-- 01307: Villabuena de Álava / Eskuernaga
-- 01130: Zalduondo
-- 01308: Lagrán
-- 01212: Peñacerrada-Urizaharra

-- =====================================================================
-- PASO 2: NO NECESITAMOS actualizar provincia_id porque se gestiona por codigo_ine
-- =====================================================================
-- IMPORTANTE: Los municipios ya tienen provincia_id correcto basado en su codigo_ine
-- NO usamos UPDATE por ID porque los IDs pueden cambiar

-- =====================================================================
-- PASO 3: Actualizar códigos postales de municipios de Álava
-- =====================================================================
-- IMPORTANTE: Usamos codigo_ine (NO id) para identificar municipios de forma segura

-- Amurrio (codigo_ine: 1002)
UPDATE dim_municipios SET codigo_postal = '01470' WHERE codigo_ine = 1002;

-- Artziniega (codigo_ine: 1004)
UPDATE dim_municipios SET codigo_postal = '01474' WHERE codigo_ine = 1004;

-- Ayala / Aiara (codigo_ine: 1010)
UPDATE dim_municipios SET codigo_postal = '01479' WHERE codigo_ine = 1010;

-- Llodio / Laudio (codigo_ine: 1038) - Si existe
UPDATE dim_municipios SET codigo_postal = '01400' WHERE codigo_ine = 1038;

-- Okondo (codigo_ine: 1042)
UPDATE dim_municipios SET codigo_postal = '01476' WHERE codigo_ine = 1042;

-- Baños de Ebro / Mañueta (codigo_ine: 1011)
UPDATE dim_municipios SET codigo_postal = '01307' WHERE codigo_ine = 1011;

-- Elciego (codigo_ine: 1022)
UPDATE dim_municipios SET codigo_postal = '01340' WHERE codigo_ine = 1022;

-- Elvillar / Bilar (codigo_ine: 1025)
UPDATE dim_municipios SET codigo_postal = '01320' WHERE codigo_ine = 1025;

-- Kripan (codigo_ine: 1019)
UPDATE dim_municipios SET codigo_postal = '01309' WHERE codigo_ine = 1019;

-- Labastida / Bastida (codigo_ine: 1028)
UPDATE dim_municipios SET codigo_postal = '01330' WHERE codigo_ine = 1028;

-- Laguardia (codigo_ine: 1031)
UPDATE dim_municipios SET codigo_postal = '01300' WHERE codigo_ine = 1031;

-- Lanciego / Lantziego (codigo_ine: 1032)
UPDATE dim_municipios SET codigo_postal = '01308' WHERE codigo_ine = 1032;

-- Lapuebla de Labarca (codigo_ine: 1033)
UPDATE dim_municipios SET codigo_postal = '01306' WHERE codigo_ine = 1033;

-- Leza (codigo_ine: 1034)
UPDATE dim_municipios SET codigo_postal = '01321' WHERE codigo_ine = 1034;

-- Moreda de Álava / Moreda Araba (codigo_ine: 1039)
UPDATE dim_municipios SET codigo_postal = '01320' WHERE codigo_ine = 1039;

-- Navaridas (codigo_ine: 1041)
UPDATE dim_municipios SET codigo_postal = '01309' WHERE codigo_ine = 1041;

-- Oyón-Oion (codigo_ine: 1043)
UPDATE dim_municipios SET codigo_postal = '01320' WHERE codigo_ine = 1043;

-- Samaniego (codigo_ine: 1052)
UPDATE dim_municipios SET codigo_postal = '01307' WHERE codigo_ine = 1052;

-- Villabuena de Álava / Eskuernaga (codigo_ine: 1057)
UPDATE dim_municipios SET codigo_postal = '01307' WHERE codigo_ine = 1057;

-- Yécora / Iekora (codigo_ine: 1060)
UPDATE dim_municipios SET codigo_postal = '01208' WHERE codigo_ine = 1060;

-- Alegría-Dulantzi (codigo_ine: 1001)
UPDATE dim_municipios SET codigo_postal = '01240' WHERE codigo_ine = 1001;

-- Asparrena (codigo_ine: 1009)
UPDATE dim_municipios SET codigo_postal = '01250' WHERE codigo_ine = 1009;

-- Barrundia (codigo_ine: 1013)
UPDATE dim_municipios SET codigo_postal = '01110' WHERE codigo_ine = 1013;

-- Elburgo / Burgelu (codigo_ine: 1021)
UPDATE dim_municipios SET codigo_postal = '01130' WHERE codigo_ine = 1021;

-- Iruraiz-Gauna (codigo_ine: 1027)
UPDATE dim_municipios SET codigo_postal = '01259' WHERE codigo_ine = 1027;

-- Salvatierra / Agurain (codigo_ine: 1051)
UPDATE dim_municipios SET codigo_postal = '01200' WHERE codigo_ine = 1051;

-- San Millán / Donemiliaga (codigo_ine: 1053)
UPDATE dim_municipios SET codigo_postal = '01428' WHERE codigo_ine = 1053;

-- Zalduondo (codigo_ine: 1061)
UPDATE dim_municipios SET codigo_postal = '01130' WHERE codigo_ine = 1061;

-- Aramaio (codigo_ine: 1003)
UPDATE dim_municipios SET codigo_postal = '01166' WHERE codigo_ine = 1003;

-- Arratzua-Ubarrundia (codigo_ine: 1008)
UPDATE dim_municipios SET codigo_postal = '01013' WHERE codigo_ine = 1008;

-- Legutio (codigo_ine: 1036)
UPDATE dim_municipios SET codigo_postal = '01170' WHERE codigo_ine = 1036;

-- Urkabustaiz (codigo_ine: 1054)
UPDATE dim_municipios SET codigo_postal = '01138' WHERE codigo_ine = 1054;

-- Zigoitia (codigo_ine: 1018)
UPDATE dim_municipios SET codigo_postal = '01199' WHERE codigo_ine = 1018;

-- Zuia (codigo_ine: 1063)
UPDATE dim_municipios SET codigo_postal = '01194' WHERE codigo_ine = 1063;

-- Añana (codigo_ine: 1049)
UPDATE dim_municipios SET codigo_postal = '01426' WHERE codigo_ine = 1049;

-- Armiñón (codigo_ine: 1006)
UPDATE dim_municipios SET codigo_postal = '01213' WHERE codigo_ine = 1006;

-- Berantevilla (codigo_ine: 1014)
UPDATE dim_municipios SET codigo_postal = '01211' WHERE codigo_ine = 1014;

-- Iruña de Oca / Iruña Oka (codigo_ine: 1901)
UPDATE dim_municipios SET codigo_postal = '01230' WHERE codigo_ine = 1901;

-- Kuartango (codigo_ine: 1020)
UPDATE dim_municipios SET codigo_postal = '01478' WHERE codigo_ine = 1020;

-- Lantarón (codigo_ine: 1902)
UPDATE dim_municipios SET codigo_postal = '01212' WHERE codigo_ine = 1902;

-- Ribera Alta / Erriberagoitia (codigo_ine: 1024)
UPDATE dim_municipios SET codigo_postal = '01220' WHERE codigo_ine = 1024;

-- Ribera Baja / Erriberabeitia (codigo_ine: 1047)
UPDATE dim_municipios SET codigo_postal = '01219' WHERE codigo_ine = 1047;

-- Valdegovía / Gaubea (codigo_ine: 1055)
UPDATE dim_municipios SET codigo_postal = '01439' WHERE codigo_ine = 1055;

-- Zambrana (codigo_ine: 1062)
UPDATE dim_municipios SET codigo_postal = '01214' WHERE codigo_ine = 1062;

-- Arraia-Maeztu (codigo_ine: 1058)
UPDATE dim_municipios SET codigo_postal = '01196' WHERE codigo_ine = 1058;

-- Bernedo (codigo_ine: 1016)
UPDATE dim_municipios SET codigo_postal = '01118' WHERE codigo_ine = 1016;

-- Campezo / Kanpezu (codigo_ine: 1017)
UPDATE dim_municipios SET codigo_postal = '01111' WHERE codigo_ine = 1017;

-- Lagrán (codigo_ine: 1030)
UPDATE dim_municipios SET codigo_postal = '01308' WHERE codigo_ine = 1030;

-- Peñacerrada-Urizaharra (codigo_ine: 1044)
UPDATE dim_municipios SET codigo_postal = '01212' WHERE codigo_ine = 1044;

-- Valle de Arana / Harana (codigo_ine: 1056)
UPDATE dim_municipios SET codigo_postal = '01268' WHERE codigo_ine = 1056;

-- =====================================================================
-- Verificación: Mostrar municipios con códigos postales
-- =====================================================================
SELECT 
    m.id,
    m.municipio_nombre,
    m.codigo_postal,
    m.provincia_id,
    c.nombre AS comarca,
    p.nombre AS provincia
FROM dim_municipios m
LEFT JOIN dim_comarcas c ON m.comarca_id = c.id
LEFT JOIN dim_provincias p ON m.provincia_id = p.id
WHERE m.id >= 1 AND m.id <= 52
ORDER BY m.comarca_id, m.id;

-- Contar municipios sin código postal
SELECT COUNT(*) AS municipios_sin_cp
FROM dim_municipios
WHERE provincia_id = 1 AND (codigo_postal IS NULL OR codigo_postal = '');
