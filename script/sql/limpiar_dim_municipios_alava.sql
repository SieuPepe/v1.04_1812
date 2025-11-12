-- =====================================================================
-- Script para limpiar y actualizar dim_municipios
-- Generado: 2025-11-12
-- =====================================================================
-- Este script:
-- 1. Elimina registros del 312 al 362
-- 2. Elimina la columna codigo_postal
-- 3. Actualiza registros 1 al 52 con datos correctos de Álava
-- =====================================================================

-- =====================================================================
-- PASO 1: Eliminar registros del 312 al 362
-- =====================================================================
DELETE FROM dim_municipios
WHERE id BETWEEN 312 AND 362;

SELECT CONCAT('Registros eliminados: ', ROW_COUNT()) AS Resultado;

-- =====================================================================
-- PASO 2: Eliminar la columna codigo_postal
-- =====================================================================
SET @col_exists = (SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'dim_municipios'
    AND COLUMN_NAME = 'codigo_postal');

SET @sql_drop_col = IF(@col_exists > 0,
    'ALTER TABLE dim_municipios DROP COLUMN codigo_postal',
    'SELECT "Columna codigo_postal no existe" AS mensaje');

PREPARE stmt FROM @sql_drop_col;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- =====================================================================
-- PASO 3: Actualizar registros 1 al 52 con datos correctos
-- =====================================================================
-- Usar INSERT ... ON DUPLICATE KEY UPDATE para actualizar por ID

-- Primero, desactivar temporalmente las foreign keys si es necesario
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;

-- Actualizar los 52 municipios de Álava
-- Cuadrilla de Ayala (comarca_id=1)
UPDATE dim_municipios SET codigo_ine = '01002', provincia_id = 1, comarca_id = 1, municipio_nombre = 'Amurrio', activo = 1 WHERE id = 1;
UPDATE dim_municipios SET codigo_ine = '01004', provincia_id = 1, comarca_id = 1, municipio_nombre = 'Artziniega', activo = 1 WHERE id = 2;
UPDATE dim_municipios SET codigo_ine = '01010', provincia_id = 1, comarca_id = 1, municipio_nombre = 'Ayala / Aiara', activo = 1 WHERE id = 3;
UPDATE dim_municipios SET codigo_ine = '01036', provincia_id = 1, comarca_id = 1, municipio_nombre = 'Llodio / Laudio', activo = 1 WHERE id = 4;
UPDATE dim_municipios SET codigo_ine = '01042', provincia_id = 1, comarca_id = 1, municipio_nombre = 'Okondo', activo = 1 WHERE id = 5;

-- Cuadrilla de Laguardia (comarca_id=2)
UPDATE dim_municipios SET codigo_ine = '01011', provincia_id = 1, comarca_id = 2, municipio_nombre = 'Baños de Ebro / Mañueta', activo = 1 WHERE id = 6;
UPDATE dim_municipios SET codigo_ine = '01022', provincia_id = 1, comarca_id = 2, municipio_nombre = 'Elciego', activo = 1 WHERE id = 7;
UPDATE dim_municipios SET codigo_ine = '01023', provincia_id = 1, comarca_id = 2, municipio_nombre = 'Elvillar / Bilar', activo = 1 WHERE id = 8;
UPDATE dim_municipios SET codigo_ine = '01019', provincia_id = 1, comarca_id = 2, municipio_nombre = 'Kripan', activo = 1 WHERE id = 9;
UPDATE dim_municipios SET codigo_ine = '01028', provincia_id = 1, comarca_id = 2, municipio_nombre = 'Labastida / Bastida', activo = 1 WHERE id = 10;
UPDATE dim_municipios SET codigo_ine = '01031', provincia_id = 1, comarca_id = 2, municipio_nombre = 'Laguardia', activo = 1 WHERE id = 11;
UPDATE dim_municipios SET codigo_ine = '01032', provincia_id = 1, comarca_id = 2, municipio_nombre = 'Lanciego / Lantziego', activo = 1 WHERE id = 12;
UPDATE dim_municipios SET codigo_ine = '01033', provincia_id = 1, comarca_id = 2, municipio_nombre = 'Lapuebla de Labarca', activo = 1 WHERE id = 13;
UPDATE dim_municipios SET codigo_ine = '01034', provincia_id = 1, comarca_id = 2, municipio_nombre = 'Leza', activo = 1 WHERE id = 14;
UPDATE dim_municipios SET codigo_ine = '01039', provincia_id = 1, comarca_id = 2, municipio_nombre = 'Moreda de Álava / Moreda Araba', activo = 1 WHERE id = 15;
UPDATE dim_municipios SET codigo_ine = '01041', provincia_id = 1, comarca_id = 2, municipio_nombre = 'Navaridas', activo = 1 WHERE id = 16;
UPDATE dim_municipios SET codigo_ine = '01043', provincia_id = 1, comarca_id = 2, municipio_nombre = 'Oyón-Oion', activo = 1 WHERE id = 17;
UPDATE dim_municipios SET codigo_ine = '01052', provincia_id = 1, comarca_id = 2, municipio_nombre = 'Samaniego', activo = 1 WHERE id = 18;
UPDATE dim_municipios SET codigo_ine = '01057', provincia_id = 1, comarca_id = 2, municipio_nombre = 'Villabuena de Álava / Eskuernaga', activo = 1 WHERE id = 19;
UPDATE dim_municipios SET codigo_ine = '01060', provincia_id = 1, comarca_id = 2, municipio_nombre = 'Yécora / Iekora', activo = 1 WHERE id = 20;

-- Cuadrilla de Vitoria (comarca_id=3)
UPDATE dim_municipios SET codigo_ine = '01001', provincia_id = 1, comarca_id = 3, municipio_nombre = 'Alegría-Dulantzi', activo = 1 WHERE id = 21;
UPDATE dim_municipios SET codigo_ine = '01009', provincia_id = 1, comarca_id = 3, municipio_nombre = 'Asparrena', activo = 1 WHERE id = 22;
UPDATE dim_municipios SET codigo_ine = '01013', provincia_id = 1, comarca_id = 3, municipio_nombre = 'Barrundia', activo = 1 WHERE id = 23;
UPDATE dim_municipios SET codigo_ine = '01021', provincia_id = 1, comarca_id = 3, municipio_nombre = 'Elburgo / Burgelu', activo = 1 WHERE id = 24;
UPDATE dim_municipios SET codigo_ine = '01027', provincia_id = 1, comarca_id = 3, municipio_nombre = 'Iruraiz-Gauna', activo = 1 WHERE id = 25;
UPDATE dim_municipios SET codigo_ine = '01051', provincia_id = 1, comarca_id = 3, municipio_nombre = 'Salvatierra / Agurain', activo = 1 WHERE id = 26;
UPDATE dim_municipios SET codigo_ine = '01053', provincia_id = 1, comarca_id = 3, municipio_nombre = 'San Millán / Donemiliaga', activo = 1 WHERE id = 27;
UPDATE dim_municipios SET codigo_ine = '01061', provincia_id = 1, comarca_id = 3, municipio_nombre = 'Zalduondo', activo = 1 WHERE id = 28;

-- Cuadrilla mixta entre Vitoria y Ayala (comarca_id=4)
UPDATE dim_municipios SET codigo_ine = '01003', provincia_id = 1, comarca_id = 4, municipio_nombre = 'Aramaio', activo = 1 WHERE id = 29;
UPDATE dim_municipios SET codigo_ine = '01008', provincia_id = 1, comarca_id = 4, municipio_nombre = 'Arratzua-Ubarrundia', activo = 1 WHERE id = 30;
UPDATE dim_municipios SET codigo_ine = '01058', provincia_id = 1, comarca_id = 4, municipio_nombre = 'Legutio', activo = 1 WHERE id = 31;
UPDATE dim_municipios SET codigo_ine = '01054', provincia_id = 1, comarca_id = 4, municipio_nombre = 'Urkabustaiz', activo = 1 WHERE id = 32;
UPDATE dim_municipios SET codigo_ine = '01018', provincia_id = 1, comarca_id = 4, municipio_nombre = 'Zigoitia', activo = 1 WHERE id = 33;
UPDATE dim_municipios SET codigo_ine = '01063', provincia_id = 1, comarca_id = 4, municipio_nombre = 'Zuia', activo = 1 WHERE id = 34;

-- Cuadrilla de Añana (comarca_id=5)
UPDATE dim_municipios SET codigo_ine = '01049', provincia_id = 1, comarca_id = 5, municipio_nombre = 'Añana', activo = 1 WHERE id = 35;
UPDATE dim_municipios SET codigo_ine = '01006', provincia_id = 1, comarca_id = 5, municipio_nombre = 'Armiñón', activo = 1 WHERE id = 36;
UPDATE dim_municipios SET codigo_ine = '01014', provincia_id = 1, comarca_id = 5, municipio_nombre = 'Berantevilla', activo = 1 WHERE id = 37;
UPDATE dim_municipios SET codigo_ine = '01901', provincia_id = 1, comarca_id = 5, municipio_nombre = 'Iruña de Oca / Iruña Oka', activo = 1 WHERE id = 38;
UPDATE dim_municipios SET codigo_ine = '01020', provincia_id = 1, comarca_id = 5, municipio_nombre = 'Kuartango', activo = 1 WHERE id = 39;
UPDATE dim_municipios SET codigo_ine = '01902', provincia_id = 1, comarca_id = 5, municipio_nombre = 'Lantarón', activo = 1 WHERE id = 40;
UPDATE dim_municipios SET codigo_ine = '01046', provincia_id = 1, comarca_id = 5, municipio_nombre = 'Ribera Alta / Erriberagoitia', activo = 1 WHERE id = 41;
UPDATE dim_municipios SET codigo_ine = '01047', provincia_id = 1, comarca_id = 5, municipio_nombre = 'Ribera Baja / Erriberabeitia', activo = 1 WHERE id = 42;
UPDATE dim_municipios SET codigo_ine = '99801', provincia_id = 1, comarca_id = 5, municipio_nombre = 'Sierra Brava de Badaia', activo = 1 WHERE id = 43;
UPDATE dim_municipios SET codigo_ine = '01055', provincia_id = 1, comarca_id = 5, municipio_nombre = 'Valdegovía / Gaubea', activo = 1 WHERE id = 44;
UPDATE dim_municipios SET codigo_ine = '01062', provincia_id = 1, comarca_id = 5, municipio_nombre = 'Zambrana', activo = 1 WHERE id = 45;

-- Cuadrilla de Campezo (comarca_id=6)
UPDATE dim_municipios SET codigo_ine = '01037', provincia_id = 1, comarca_id = 6, municipio_nombre = 'Arraia-Maeztu', activo = 1 WHERE id = 46;
UPDATE dim_municipios SET codigo_ine = '01016', provincia_id = 1, comarca_id = 6, municipio_nombre = 'Bernedo', activo = 1 WHERE id = 47;
UPDATE dim_municipios SET codigo_ine = '01017', provincia_id = 1, comarca_id = 6, municipio_nombre = 'Campezo / Kanpezu', activo = 1 WHERE id = 48;
UPDATE dim_municipios SET codigo_ine = '01030', provincia_id = 1, comarca_id = 6, municipio_nombre = 'Lagrán', activo = 1 WHERE id = 49;
UPDATE dim_municipios SET codigo_ine = '99802', provincia_id = 1, comarca_id = 6, municipio_nombre = 'Parzoneria de Entzia', activo = 1 WHERE id = 50;
UPDATE dim_municipios SET codigo_ine = '01044', provincia_id = 1, comarca_id = 6, municipio_nombre = 'Peñacerrada-Urizaharra', activo = 1 WHERE id = 51;
UPDATE dim_municipios SET codigo_ine = '01056', provincia_id = 1, comarca_id = 6, municipio_nombre = 'Valle de Arana / Harana', activo = 1 WHERE id = 52;

-- Restaurar foreign key checks
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;

-- =====================================================================
-- PASO 4: Verificación
-- =====================================================================
SELECT '¡Script completado exitosamente!' AS Resultado;

SELECT
    'Verificación de municipios de Álava actualizados:' AS Paso,
    COUNT(*) AS total_municipios
FROM dim_municipios
WHERE id BETWEEN 1 AND 52;

-- Mostrar los 52 municipios actualizados
SELECT
    id,
    codigo_ine,
    provincia_id,
    comarca_id,
    municipio_nombre,
    activo
FROM dim_municipios
WHERE id BETWEEN 1 AND 52
ORDER BY id;
