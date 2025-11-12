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
-- PASO 2: Actualizar provincia_id para municipios de Álava (1-52)
-- =====================================================================
UPDATE dim_municipios SET provincia_id = 1 WHERE id >= 1 AND id <= 52;

-- =====================================================================
-- PASO 3: Actualizar códigos postales de municipios de Álava
-- =====================================================================

-- Amurrio
UPDATE dim_municipios SET codigo_postal = '01470' WHERE id = 1;

-- Artziniega
UPDATE dim_municipios SET codigo_postal = '01474' WHERE id = 2;

-- Ayala / Aiara
UPDATE dim_municipios SET codigo_postal = '01479' WHERE id = 3;

-- Llodio / Laudio
UPDATE dim_municipios SET codigo_postal = '01400' WHERE id = 4;

-- Okondo
UPDATE dim_municipios SET codigo_postal = '01476' WHERE id = 5;

-- Baños de Ebro / Mañueta
UPDATE dim_municipios SET codigo_postal = '01307' WHERE id = 6;

-- Elciego
UPDATE dim_municipios SET codigo_postal = '01340' WHERE id = 7;

-- Elvillar / Bilar
UPDATE dim_municipios SET codigo_postal = '01320' WHERE id = 8;

-- Kripan
UPDATE dim_municipios SET codigo_postal = '01309' WHERE id = 9;

-- Labastida / Bastida
UPDATE dim_municipios SET codigo_postal = '01330' WHERE id = 10;

-- Laguardia
UPDATE dim_municipios SET codigo_postal = '01300' WHERE id = 11;

-- Lanciego / Lantziego
UPDATE dim_municipios SET codigo_postal = '01308' WHERE id = 12;

-- Lapuebla de Labarca
UPDATE dim_municipios SET codigo_postal = '01306' WHERE id = 13;

-- Leza
UPDATE dim_municipios SET codigo_postal = '01321' WHERE id = 14;

-- Moreda de Álava / Moreda Araba
UPDATE dim_municipios SET codigo_postal = '01320' WHERE id = 15;

-- Navaridas
UPDATE dim_municipios SET codigo_postal = '01309' WHERE id = 16;

-- Oyón-Oion
UPDATE dim_municipios SET codigo_postal = '01320' WHERE id = 17;

-- Samaniego
UPDATE dim_municipios SET codigo_postal = '01307' WHERE id = 18;

-- Villabuena de Álava / Eskuernaga
UPDATE dim_municipios SET codigo_postal = '01307' WHERE id = 19;

-- Yécora / Iekora
UPDATE dim_municipios SET codigo_postal = '01208' WHERE id = 20;

-- Alegría-Dulantzi
UPDATE dim_municipios SET codigo_postal = '01240' WHERE id = 21;

-- Asparrena
UPDATE dim_municipios SET codigo_postal = '01250' WHERE id = 22;

-- Barrundia
UPDATE dim_municipios SET codigo_postal = '01110' WHERE id = 23;

-- Elburgo / Burgelu
UPDATE dim_municipios SET codigo_postal = '01130' WHERE id = 24;

-- Iruraiz-Gauna
UPDATE dim_municipios SET codigo_postal = '01259' WHERE id = 25;

-- Salvatierra / Agurain
UPDATE dim_municipios SET codigo_postal = '01200' WHERE id = 26;

-- San Millán / Donemiliaga
UPDATE dim_municipios SET codigo_postal = '01428' WHERE id = 27;

-- Zalduondo
UPDATE dim_municipios SET codigo_postal = '01130' WHERE id = 28;

-- Aramaio
UPDATE dim_municipios SET codigo_postal = '01166' WHERE id = 29;

-- Arratzua-Ubarrundia
UPDATE dim_municipios SET codigo_postal = '01013' WHERE id = 30;

-- Legutio
UPDATE dim_municipios SET codigo_postal = '01170' WHERE id = 31;

-- Urkabustaiz
UPDATE dim_municipios SET codigo_postal = '01138' WHERE id = 32;

-- Zigoitia
UPDATE dim_municipios SET codigo_postal = '01199' WHERE id = 33;

-- Zuia
UPDATE dim_municipios SET codigo_postal = '01194' WHERE id = 34;

-- Añana
UPDATE dim_municipios SET codigo_postal = '01426' WHERE id = 35;

-- Armiñón
UPDATE dim_municipios SET codigo_postal = '01213' WHERE id = 36;

-- Berantevilla
UPDATE dim_municipios SET codigo_postal = '01211' WHERE id = 37;

-- Iruña de Oca / Iruña Oka
UPDATE dim_municipios SET codigo_postal = '01230' WHERE id = 38;

-- Kuartango
UPDATE dim_municipios SET codigo_postal = '01478' WHERE id = 39;

-- Lantarón
UPDATE dim_municipios SET codigo_postal = '01212' WHERE id = 40;

-- Ribera Alta / Erriberagoitia
UPDATE dim_municipios SET codigo_postal = '01220' WHERE id = 41;

-- Ribera Baja / Erriberabeitia
UPDATE dim_municipios SET codigo_postal = '01219' WHERE id = 42;

-- Sierra Brava de Badaia
UPDATE dim_municipios SET codigo_postal = '99801' WHERE id = 43;

-- Valdegovía / Gaubea
UPDATE dim_municipios SET codigo_postal = '01439' WHERE id = 44;

-- Zambrana
UPDATE dim_municipios SET codigo_postal = '01214' WHERE id = 45;

-- Arraia-Maeztu
UPDATE dim_municipios SET codigo_postal = '01196' WHERE id = 46;

-- Bernedo
UPDATE dim_municipios SET codigo_postal = '01118' WHERE id = 47;

-- Campezo / Kanpezu
UPDATE dim_municipios SET codigo_postal = '01111' WHERE id = 48;

-- Lagrán
UPDATE dim_municipios SET codigo_postal = '01308' WHERE id = 49;

-- Parzoneria de Entzia
UPDATE dim_municipios SET codigo_postal = '99802' WHERE id = 50;

-- Peñacerrada-Urizaharra
UPDATE dim_municipios SET codigo_postal = '01212' WHERE id = 51;

-- Valle de Arana / Harana
UPDATE dim_municipios SET codigo_postal = '01268' WHERE id = 52;

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
