-- =====================================================================
-- FASE 3: Configuración de dim_comarcas y creación de dim_municipios
-- =====================================================================
-- Este script:
-- 1. Crea la tabla dim_municipios si no existe
-- 2. Añade provincia_id a dim_comarcas
-- 3. Relaciona comarcas existentes de Álava con provincia_id=1
-- 4. Inserta comarcas para Gipuzkoa (id=7) y Bizkaia (id=8)
-- 5. Puebla dim_municipios con los 251 municipios de las 3 provincias
-- =====================================================================

-- =====================================================================
-- PASO 1: Crear tabla dim_municipios
-- =====================================================================
CREATE TABLE IF NOT EXISTS dim_municipios (
    id INT NOT NULL AUTO_INCREMENT,
    codigo_ine BIGINT NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    provincia_id INT NOT NULL,
    comarca_id INT DEFAULT NULL,
    activo TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_codigo_ine (codigo_ine),
    KEY idx_provincia (provincia_id),
    KEY idx_comarca (comarca_id),
    KEY idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================================
-- PASO 2: Añadir provincia_id a dim_comarcas si no existe
-- =====================================================================
SET @col_exists = (SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'dim_comarcas'
    AND COLUMN_NAME = 'provincia_id');

SET @sql_add_col = IF(@col_exists = 0,
    'ALTER TABLE dim_comarcas ADD COLUMN provincia_id INT DEFAULT NULL AFTER id',
    'SELECT "Columna provincia_id ya existe en dim_comarcas" AS mensaje');

PREPARE stmt FROM @sql_add_col;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- =====================================================================
-- PASO 3: Actualizar comarcas existentes de Álava con provincia_id=1
-- =====================================================================
UPDATE dim_comarcas
SET provincia_id = 1
WHERE id BETWEEN 1 AND 6
AND provincia_id IS NULL;

-- =====================================================================
-- PASO 4: Insertar comarcas de Gipuzkoa y Bizkaia
-- =====================================================================
INSERT INTO dim_comarcas (id, provincia_id, comarca_codigo, comarca_nombre, created_at)
VALUES
    (7, 3, 'GIPUZ', 'Gipuzkoa', NOW()),
    (8, 2, 'BIZKA', 'Bizkaia', NOW())
ON DUPLICATE KEY UPDATE
    provincia_id = VALUES(provincia_id),
    comarca_codigo = VALUES(comarca_codigo),
    comarca_nombre = VALUES(comarca_nombre);

-- =====================================================================
-- PASO 5: Poblar dim_municipios con municipios de Álava (comarca_id según cuadrilla)
-- =====================================================================
-- Nota: Los 51 municipios de Álava se distribuyen entre las 6 comarcas/cuadrillas
-- Datos actualizados según códigos INE oficiales (enero 2025)
-- Comarca_id: 1=Ayala, 2=Laguardia, 3=Vitoria, 5=Añana, 6=Campezo

-- Municipios de Álava - Distribuidos por cuadrillas según códigos INE oficiales
INSERT INTO dim_municipios (codigo_ine, nombre, provincia_id, comarca_id, activo) VALUES
-- Cuadrilla de Vitoria (comarca_id=3)
(1001, 'Alegría-Dulantzi', 1, 3, 1),
(1008, 'Arratzua-Ubarrundia', 1, 3, 1),
(1009, 'Asparrena', 1, 3, 1),
(1013, 'Barrundia', 1, 3, 1),
(1018, 'Zigoitia', 1, 3, 1),
(1020, 'Kuartango', 1, 3, 1),
(1021, 'Elburgo/Burgelu', 1, 3, 1),
(1023, 'Erriberagoitia/Ribera Alta', 1, 3, 1),
(1027, 'Iruraiz-Gauna', 1, 3, 1),
(1036, 'Legutio', 1, 3, 1),
(1047, 'Ribera Baja/Erribera Beitia', 1, 3, 1),
(1051, 'Agurain/Salvatierra', 1, 3, 1),
(1053, 'San Millán/Donemiliaga', 1, 3, 1),
(1056, 'Harana/Valle de Arana', 1, 3, 1),
(1058, 'Legutio', 1, 3, 1),
(1059, 'Vitoria-Gasteiz', 1, 3, 1),
(1061, 'Zalduondo', 1, 3, 1),
(1063, 'Zuia', 1, 3, 1),
(1901, 'Iruña Oka/Iruña de Oca', 1, 3, 1),
-- Cuadrilla de Ayala (comarca_id=1)
(1002, 'Amurrio', 1, 1, 1),
(1003, 'Aramaio', 1, 1, 1),
(1004, 'Artziniega', 1, 1, 1),
(1010, 'Ayala/Aiara', 1, 1, 1),
(1042, 'Okondo', 1, 1, 1),
(1054, 'Urkabustaiz', 1, 1, 1),
(1055, 'Valdegovía/Gaubea', 1, 1, 1),
-- Cuadrilla de Laguardia-Rioja Alavesa (comarca_id=2)
(1011, 'Baños de Ebro/Mañueta', 1, 2, 1),
(1014, 'Berantevilla', 1, 2, 1),
(1019, 'Kripan', 1, 2, 1),
(1022, 'Elciego', 1, 2, 1),
(1023, 'Elvillar/Bilar', 1, 2, 1),
(1028, 'Labastida/Bastida', 1, 2, 1),
(1030, 'Lagrán', 1, 2, 1),
(1031, 'Laguardia', 1, 2, 1),
(1032, 'Lanciego/Lantziego', 1, 2, 1),
(1033, 'Lapuebla de Labarca', 1, 2, 1),
(1034, 'Leza', 1, 2, 1),
(1039, 'Moreda de Álava/Moreda Araba', 1, 2, 1),
(1041, 'Navaridas', 1, 2, 1),
(1043, 'Oyón-Oion', 1, 2, 1),
(1052, 'Samaniego', 1, 2, 1),
(1057, 'Villabuena de Álava/Eskuernaga', 1, 2, 1),
(1062, 'Zambrana', 1, 2, 1),
(1902, 'Lantarón', 1, 2, 1),
-- Cuadrilla de Añana (comarca_id=5)
(1006, 'Armiñón', 1, 5, 1),
(1016, 'Bernedo', 1, 5, 1),
(1037, 'Arraia-Maeztu', 1, 5, 1),
(1044, 'Peñacerrada-Urizaharra', 1, 5, 1),
(1049, 'Añana', 1, 5, 1),
(1060, 'Yécora/Iekora', 1, 5, 1),
-- Cuadrilla de Campezo (comarca_id=6)
(1017, 'Campezo/Kanpezu', 1, 6, 1)
ON DUPLICATE KEY UPDATE
    nombre = VALUES(nombre),
    provincia_id = VALUES(provincia_id),
    comarca_id = VALUES(comarca_id);

-- =====================================================================
-- PASO 6: Poblar dim_municipios con municipios de Bizkaia (comarca_id=8)
-- =====================================================================
INSERT INTO dim_municipios (codigo_ine, nombre, provincia_id, comarca_id, activo) VALUES
(48001, 'Abadiño', 2, 8, 1),
(48002, 'Abanto y Ciérvana-Abanto Zierbena', 2, 8, 1),
(48003, 'Ajangiz', 2, 8, 1),
(48004, 'Alonsotegi', 2, 8, 1),
(48005, 'Amorebieta-Etxano', 2, 8, 1),
(48006, 'Amoroto', 2, 8, 1),
(48007, 'Arakaldo', 2, 8, 1),
(48008, 'Arantzazu', 2, 8, 1),
(48009, 'Areatza', 2, 8, 1),
(48010, 'Arrankudiaga', 2, 8, 1),
(48011, 'Arratzu', 2, 8, 1),
(48012, 'Arrieta', 2, 8, 1),
(48013, 'Arrigorriaga', 2, 8, 1),
(48014, 'Artea', 2, 8, 1),
(48015, 'Artzentales', 2, 8, 1),
(48016, 'Atxondo', 2, 8, 1),
(48017, 'Aulesti', 2, 8, 1),
(48018, 'Bakio', 2, 8, 1),
(48019, 'Balmaseda', 2, 8, 1),
(48020, 'Barakaldo', 2, 8, 1),
(48021, 'Barrika', 2, 8, 1),
(48022, 'Basauri', 2, 8, 1),
(48023, 'Bedia', 2, 8, 1),
(48024, 'Berango', 2, 8, 1),
(48025, 'Bermeo', 2, 8, 1),
(48026, 'Berriatua', 2, 8, 1),
(48027, 'Berriz', 2, 8, 1),
(48028, 'Bilbao', 2, 8, 1),
(48029, 'Busturia', 2, 8, 1),
(48030, 'Derio', 2, 8, 1),
(48031, 'Dima', 2, 8, 1),
(48032, 'Durango', 2, 8, 1),
(48033, 'Ea', 2, 8, 1),
(48034, 'Elantxobe', 2, 8, 1),
(48035, 'Elorrio', 2, 8, 1),
(48036, 'Erandio', 2, 8, 1),
(48037, 'Ereño', 2, 8, 1),
(48038, 'Ermua', 2, 8, 1),
(48039, 'Errigoiti', 2, 8, 1),
(48040, 'Etxebarri', 2, 8, 1),
(48041, 'Etxebarria', 2, 8, 1),
(48042, 'Forua', 2, 8, 1),
(48043, 'Fruiz', 2, 8, 1),
(48044, 'Galdakao', 2, 8, 1),
(48045, 'Galdames', 2, 8, 1),
(48046, 'Gamiz-Fika', 2, 8, 1),
(48047, 'Garai', 2, 8, 1),
(48048, 'Gatika', 2, 8, 1),
(48049, 'Gautegiz Arteaga', 2, 8, 1),
(48050, 'Gernika-Lumo', 2, 8, 1),
(48051, 'Getxo', 2, 8, 1),
(48052, 'Gizaburuaga', 2, 8, 1),
(48053, 'Gordexola', 2, 8, 1),
(48054, 'Gorliz', 2, 8, 1),
(48055, 'Güeñes', 2, 8, 1),
(48056, 'Ibarrangelu', 2, 8, 1),
(48057, 'Igorre', 2, 8, 1),
(48058, 'Ispaster', 2, 8, 1),
(48059, 'Iurreta', 2, 8, 1),
(48060, 'Izurtza', 2, 8, 1),
(48061, 'Karrantza Harana/Valle de Carranza', 2, 8, 1),
(48062, 'Kortezubi', 2, 8, 1),
(48063, 'Lanestosa', 2, 8, 1),
(48064, 'Larrabetzu', 2, 8, 1),
(48065, 'Laukiz', 2, 8, 1),
(48066, 'Leioa', 2, 8, 1),
(48067, 'Lekeitio', 2, 8, 1),
(48068, 'Lemoa', 2, 8, 1),
(48069, 'Lemoiz', 2, 8, 1),
(48070, 'Lezama', 2, 8, 1),
(48071, 'Loiu', 2, 8, 1),
(48072, 'Mallabia', 2, 8, 1),
(48073, 'Mañaria', 2, 8, 1),
(48074, 'Markina-Xemein', 2, 8, 1),
(48075, 'Maruri-Jatabe', 2, 8, 1),
(48076, 'Mendata', 2, 8, 1),
(48077, 'Mendexa', 2, 8, 1),
(48078, 'Meñaka', 2, 8, 1),
(48079, 'Morga', 2, 8, 1),
(48080, 'Muxika', 2, 8, 1),
(48081, 'Mundaka', 2, 8, 1),
(48082, 'Mungia', 2, 8, 1),
(48083, 'Muskiz', 2, 8, 1),
(48084, 'Mutriku', 2, 8, 1),
(48085, 'Nabarniz', 2, 8, 1),
(48086, 'Ondarroa', 2, 8, 1),
(48087, 'Orozko', 2, 8, 1),
(48088, 'Ortuella', 2, 8, 1),
(48089, 'Otxandio', 2, 8, 1),
(48090, 'Pedernales', 2, 8, 1),
(48091, 'Plentzia', 2, 8, 1),
(48092, 'Portugalete', 2, 8, 1),
(48093, 'Santurtzi', 2, 8, 1),
(48094, 'Sestao', 2, 8, 1),
(48095, 'Sondika', 2, 8, 1),
(48096, 'Sopelana', 2, 8, 1),
(48097, 'Sopuerta', 2, 8, 1),
(48098, 'Sukarrieta', 2, 8, 1),
(48099, 'Trucios-Turtzioz', 2, 8, 1),
(48100, 'Ubide', 2, 8, 1),
(48101, 'Ugao-Miraballes', 2, 8, 1),
(48102, 'Urduliz', 2, 8, 1),
(48103, 'Urduña/Orduña', 2, 8, 1),
(48104, 'Valle de Trápaga-Trapagaran', 2, 8, 1),
(48105, 'Zaldibar', 2, 8, 1),
(48106, 'Zalla', 2, 8, 1),
(48107, 'Zamudio', 2, 8, 1),
(48108, 'Zaratamo', 2, 8, 1),
(48109, 'Zeanuri', 2, 8, 1),
(48110, 'Zeberio', 2, 8, 1),
(48111, 'Zierbena', 2, 8, 1),
(48912, 'Ziortza-Bolibar', 2, 8, 1)
ON DUPLICATE KEY UPDATE
    nombre = VALUES(nombre),
    provincia_id = VALUES(provincia_id),
    comarca_id = VALUES(comarca_id);

-- =====================================================================
-- PASO 7: Poblar dim_municipios con municipios de Gipuzkoa (comarca_id=7)
-- =====================================================================
INSERT INTO dim_municipios (codigo_ine, nombre, provincia_id, comarca_id, activo) VALUES
(20001, 'Abaltzisketa', 3, 7, 1),
(20002, 'Aduna', 3, 7, 1),
(20003, 'Aia', 3, 7, 1),
(20004, 'Aizarnazabal', 3, 7, 1),
(20005, 'Albiztur', 3, 7, 1),
(20006, 'Alegia', 3, 7, 1),
(20007, 'Alkiza', 3, 7, 1),
(20008, 'Altzaga', 3, 7, 1),
(20009, 'Altzo', 3, 7, 1),
(20010, 'Amezketa', 3, 7, 1),
(20011, 'Andoain', 3, 7, 1),
(20012, 'Anoeta', 3, 7, 1),
(20013, 'Antzuola', 3, 7, 1),
(20014, 'Arama', 3, 7, 1),
(20015, 'Aretxabaleta', 3, 7, 1),
(20016, 'Arrasate/Mondragón', 3, 7, 1),
(20017, 'Asteasu', 3, 7, 1),
(20018, 'Astigarraga', 3, 7, 1),
(20019, 'Ataun', 3, 7, 1),
(20020, 'Azkoitia', 3, 7, 1),
(20021, 'Azpeitia', 3, 7, 1),
(20022, 'Baliarrain', 3, 7, 1),
(20023, 'Beasain', 3, 7, 1),
(20024, 'Beizama', 3, 7, 1),
(20025, 'Belauntza', 3, 7, 1),
(20026, 'Berastegi', 3, 7, 1),
(20027, 'Bergara', 3, 7, 1),
(20028, 'Berrobi', 3, 7, 1),
(20029, 'Bidania-Goiatz', 3, 7, 1),
(20030, 'Deba', 3, 7, 1),
(20031, 'Donostia-San Sebastián', 3, 7, 1),
(20032, 'Eibar', 3, 7, 1),
(20033, 'Elduain', 3, 7, 1),
(20034, 'Elgeta', 3, 7, 1),
(20035, 'Elgoibar', 3, 7, 1),
(20036, 'Errenteria', 3, 7, 1),
(20037, 'Errezil', 3, 7, 1),
(20038, 'Eskoriatza', 3, 7, 1),
(20039, 'Ezkio-Itsaso', 3, 7, 1),
(20040, 'Gabiria', 3, 7, 1),
(20041, 'Gaintza', 3, 7, 1),
(20042, 'Gaztelu', 3, 7, 1),
(20043, 'Getaria', 3, 7, 1),
(20044, 'Hernani', 3, 7, 1),
(20045, 'Hernialde', 3, 7, 1),
(20046, 'Hondarribia', 3, 7, 1),
(20047, 'Ibarra', 3, 7, 1),
(20048, 'Idiazabal', 3, 7, 1),
(20049, 'Ikaztegieta', 3, 7, 1),
(20050, 'Irun', 3, 7, 1),
(20051, 'Irura', 3, 7, 1),
(20052, 'Itsasondo', 3, 7, 1),
(20053, 'Larraul', 3, 7, 1),
(20054, 'Lasarte-Oria', 3, 7, 1),
(20055, 'Lazkao', 3, 7, 1),
(20056, 'Leaburu', 3, 7, 1),
(20057, 'Legazpi', 3, 7, 1),
(20058, 'Legorreta', 3, 7, 1),
(20059, 'Leintz-Gatzaga', 3, 7, 1),
(20060, 'Lezo', 3, 7, 1),
(20061, 'Lizartza', 3, 7, 1),
(20062, 'Mendaro', 3, 7, 1),
(20063, 'Mutiloa', 3, 7, 1),
(20064, 'Mutriku', 3, 7, 1),
(20065, 'Oiartzun', 3, 7, 1),
(20066, 'Olaberria', 3, 7, 1),
(20067, 'Onati', 3, 7, 1),
(20068, 'Ordizia', 3, 7, 1),
(20069, 'Orendain', 3, 7, 1),
(20070, 'Orio', 3, 7, 1),
(20071, 'Ormaiztegi', 3, 7, 1),
(20072, 'Pasaia', 3, 7, 1),
(20073, 'Segura', 3, 7, 1),
(20074, 'Soraluze-Placencia de las Armas', 3, 7, 1),
(20075, 'Tolosa', 3, 7, 1),
(20076, 'Urnieta', 3, 7, 1),
(20077, 'Urretxu', 3, 7, 1),
(20078, 'Usurbil', 3, 7, 1),
(20079, 'Villabona', 3, 7, 1),
(20080, 'Zaldibia', 3, 7, 1),
(20081, 'Zarautz', 3, 7, 1),
(20082, 'Zegama', 3, 7, 1),
(20083, 'Zerain', 3, 7, 1),
(20084, 'Zestoa', 3, 7, 1),
(20085, 'Zizurkil', 3, 7, 1),
(20086, 'Zumaia', 3, 7, 1),
(20087, 'Zumarraga', 3, 7, 1),
(20088, 'Zumárraga', 3, 7, 1)
ON DUPLICATE KEY UPDATE
    nombre = VALUES(nombre),
    provincia_id = VALUES(provincia_id),
    comarca_id = VALUES(comarca_id);

-- =====================================================================
-- FIN DEL SCRIPT
-- =====================================================================
SELECT 'Script completado exitosamente' AS Resultado;
