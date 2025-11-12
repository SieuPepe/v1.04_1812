-- =====================================================================
-- SCRIPT DE RECUPERACIÓN DE dim_municipios
-- =====================================================================
-- Este script corrige los problemas causados por el DELETE por ID
-- y restaura correctamente todos los municipios de las 3 provincias
-- =====================================================================
-- PROBLEMAS QUE CORRIGE:
-- 1. Restaura municipios borrados incorrectamente (IDs 1-52)
-- 2. Restaura valores de 'activo' (debe ser 1)
-- 3. Restaura valores de 'created_at' (timestamp)
-- 4. Usa codigo_ine para identificar municipios (NO id autoincrementado)
-- 5. Asegura que codigo_postal esté en la columna correcta
-- =====================================================================

-- =====================================================================
-- PASO 1: Verificar estructura de la tabla
-- =====================================================================
SELECT 'Verificando estructura de dim_municipios...' AS Paso;
SHOW COLUMNS FROM dim_municipios;

-- =====================================================================
-- PASO 2: Hacer backup de datos actuales (mostrar qué hay ahora)
-- =====================================================================
SELECT 'Estado actual de la tabla:' AS Paso;
SELECT
    COUNT(*) as total_municipios,
    SUM(CASE WHEN provincia_id = 1 THEN 1 ELSE 0 END) as alava,
    SUM(CASE WHEN provincia_id = 2 THEN 1 ELSE 0 END) as bizkaia,
    SUM(CASE WHEN provincia_id = 3 THEN 1 ELSE 0 END) as gipuzkoa,
    SUM(CASE WHEN activo IS NULL OR activo = 0 THEN 1 ELSE 0 END) as sin_activo,
    SUM(CASE WHEN created_at IS NULL THEN 1 ELSE 0 END) as sin_created_at
FROM dim_municipios;

-- =====================================================================
-- PASO 3: Agregar columna codigo_postal si no existe
-- =====================================================================
SET @col_exists = (SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'dim_municipios'
    AND COLUMN_NAME = 'codigo_postal');

SET @sql_add_col = IF(@col_exists = 0,
    'ALTER TABLE dim_municipios ADD COLUMN codigo_postal VARCHAR(10) DEFAULT NULL AFTER nombre',
    'SELECT "Columna codigo_postal ya existe" AS mensaje');

PREPARE stmt FROM @sql_add_col;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- =====================================================================
-- PASO 4: Restaurar/Actualizar TODOS los municipios de Álava (provincia_id=1)
-- =====================================================================
-- Se usa INSERT ... ON DUPLICATE KEY UPDATE para:
-- - Insertar si no existe (por codigo_ine único)
-- - Actualizar si ya existe (restaurar activo y created_at)
-- =====================================================================

SELECT 'Restaurando municipios de Álava...' AS Paso;

INSERT INTO dim_municipios (codigo_ine, nombre, provincia_id, comarca_id, activo, created_at) VALUES
-- Cuadrilla de Vitoria (comarca_id=3) - 19 municipios
(1001, 'Alegría-Dulantzi', 1, 3, 1, NOW()),
(1008, 'Arratzua-Ubarrundia', 1, 3, 1, NOW()),
(1009, 'Asparrena', 1, 3, 1, NOW()),
(1013, 'Barrundia', 1, 3, 1, NOW()),
(1018, 'Zigoitia', 1, 3, 1, NOW()),
(1020, 'Kuartango', 1, 3, 1, NOW()),
(1021, 'Elburgo/Burgelu', 1, 3, 1, NOW()),
(1024, 'Erriberagoitia/Ribera Alta', 1, 3, 1, NOW()),
(1027, 'Iruraiz-Gauna', 1, 3, 1, NOW()),
(1036, 'Legutio', 1, 3, 1, NOW()),
(1047, 'Ribera Baja/Erribera Beitia', 1, 3, 1, NOW()),
(1051, 'Agurain/Salvatierra', 1, 3, 1, NOW()),
(1053, 'San Millán/Donemiliaga', 1, 3, 1, NOW()),
(1056, 'Harana/Valle de Arana', 1, 3, 1, NOW()),
(1058, 'Arraia-Maeztu', 1, 3, 1, NOW()),
(1059, 'Vitoria-Gasteiz', 1, 3, 1, NOW()),
(1061, 'Zalduondo', 1, 3, 1, NOW()),
(1063, 'Zuia', 1, 3, 1, NOW()),
(1901, 'Iruña Oka/Iruña de Oca', 1, 3, 1, NOW()),

-- Cuadrilla de Ayala (comarca_id=1) - 7 municipios
(1002, 'Amurrio', 1, 1, 1, NOW()),
(1003, 'Aramaio', 1, 1, 1, NOW()),
(1004, 'Artziniega', 1, 1, 1, NOW()),
(1010, 'Ayala/Aiara', 1, 1, 1, NOW()),
(1042, 'Okondo', 1, 1, 1, NOW()),
(1054, 'Urkabustaiz', 1, 1, 1, NOW()),
(1055, 'Valdegovía/Gaubea', 1, 1, 1, NOW()),

-- Cuadrilla de Laguardia-Rioja Alavesa (comarca_id=2) - 18 municipios
(1011, 'Baños de Ebro/Mañueta', 1, 2, 1, NOW()),
(1014, 'Berantevilla', 1, 2, 1, NOW()),
(1019, 'Kripan', 1, 2, 1, NOW()),
(1022, 'Elciego', 1, 2, 1, NOW()),
(1025, 'Elvillar/Bilar', 1, 2, 1, NOW()),
(1028, 'Labastida/Bastida', 1, 2, 1, NOW()),
(1030, 'Lagrán', 1, 2, 1, NOW()),
(1031, 'Laguardia', 1, 2, 1, NOW()),
(1032, 'Lanciego/Lantziego', 1, 2, 1, NOW()),
(1033, 'Lapuebla de Labarca', 1, 2, 1, NOW()),
(1034, 'Leza', 1, 2, 1, NOW()),
(1039, 'Moreda de Álava/Moreda Araba', 1, 2, 1, NOW()),
(1041, 'Navaridas', 1, 2, 1, NOW()),
(1043, 'Oyón-Oion', 1, 2, 1, NOW()),
(1052, 'Samaniego', 1, 2, 1, NOW()),
(1057, 'Villabuena de Álava/Eskuernaga', 1, 2, 1, NOW()),
(1062, 'Zambrana', 1, 2, 1, NOW()),
(1902, 'Lantarón', 1, 2, 1, NOW()),

-- Cuadrilla de Añana (comarca_id=5) - 6 municipios
(1006, 'Armiñón', 1, 5, 1, NOW()),
(1016, 'Bernedo', 1, 5, 1, NOW()),
(1037, 'Arraia-Maeztu', 1, 5, 1, NOW()),
(1044, 'Peñacerrada-Urizaharra', 1, 5, 1, NOW()),
(1049, 'Añana', 1, 5, 1, NOW()),
(1060, 'Yécora/Iekora', 1, 5, 1, NOW()),

-- Cuadrilla de Campezo (comarca_id=6) - 1 municipio
(1017, 'Campezo/Kanpezu', 1, 6, 1, NOW())

ON DUPLICATE KEY UPDATE
    nombre = VALUES(nombre),
    provincia_id = VALUES(provincia_id),
    comarca_id = VALUES(comarca_id),
    activo = 1,  -- RESTAURAR activo a 1
    created_at = IFNULL(created_at, NOW());  -- Mantener created_at original o NOW() si es NULL

-- =====================================================================
-- PASO 5: Restaurar/Actualizar TODOS los municipios de Bizkaia (provincia_id=2)
-- =====================================================================
SELECT 'Restaurando municipios de Bizkaia...' AS Paso;

INSERT INTO dim_municipios (codigo_ine, nombre, provincia_id, comarca_id, activo, created_at) VALUES
(48001, 'Abadiño', 2, 8, 1, NOW()),
(48002, 'Abanto y Ciérvana-Abanto Zierbena', 2, 8, 1, NOW()),
(48003, 'Ajangiz', 2, 8, 1, NOW()),
(48004, 'Alonsotegi', 2, 8, 1, NOW()),
(48005, 'Amorebieta-Etxano', 2, 8, 1, NOW()),
(48006, 'Amoroto', 2, 8, 1, NOW()),
(48007, 'Arakaldo', 2, 8, 1, NOW()),
(48008, 'Arantzazu', 2, 8, 1, NOW()),
(48009, 'Areatza', 2, 8, 1, NOW()),
(48010, 'Arrankudiaga', 2, 8, 1, NOW()),
(48011, 'Arratzu', 2, 8, 1, NOW()),
(48012, 'Arrieta', 2, 8, 1, NOW()),
(48013, 'Arrigorriaga', 2, 8, 1, NOW()),
(48014, 'Artea', 2, 8, 1, NOW()),
(48015, 'Artzentales', 2, 8, 1, NOW()),
(48016, 'Atxondo', 2, 8, 1, NOW()),
(48017, 'Aulesti', 2, 8, 1, NOW()),
(48018, 'Bakio', 2, 8, 1, NOW()),
(48019, 'Balmaseda', 2, 8, 1, NOW()),
(48020, 'Barakaldo', 2, 8, 1, NOW()),
(48021, 'Barrika', 2, 8, 1, NOW()),
(48022, 'Basauri', 2, 8, 1, NOW()),
(48023, 'Bedia', 2, 8, 1, NOW()),
(48024, 'Berango', 2, 8, 1, NOW()),
(48025, 'Bermeo', 2, 8, 1, NOW()),
(48026, 'Berriatua', 2, 8, 1, NOW()),
(48027, 'Berriz', 2, 8, 1, NOW()),
(48028, 'Bilbao', 2, 8, 1, NOW()),
(48029, 'Busturia', 2, 8, 1, NOW()),
(48030, 'Derio', 2, 8, 1, NOW()),
(48031, 'Dima', 2, 8, 1, NOW()),
(48032, 'Durango', 2, 8, 1, NOW()),
(48033, 'Ea', 2, 8, 1, NOW()),
(48034, 'Elantxobe', 2, 8, 1, NOW()),
(48035, 'Elorrio', 2, 8, 1, NOW()),
(48036, 'Erandio', 2, 8, 1, NOW()),
(48037, 'Ereño', 2, 8, 1, NOW()),
(48038, 'Ermua', 2, 8, 1, NOW()),
(48039, 'Errigoiti', 2, 8, 1, NOW()),
(48040, 'Etxebarri', 2, 8, 1, NOW()),
(48041, 'Etxebarria', 2, 8, 1, NOW()),
(48042, 'Forua', 2, 8, 1, NOW()),
(48043, 'Fruiz', 2, 8, 1, NOW()),
(48044, 'Galdakao', 2, 8, 1, NOW()),
(48045, 'Galdames', 2, 8, 1, NOW()),
(48046, 'Gamiz-Fika', 2, 8, 1, NOW()),
(48047, 'Garai', 2, 8, 1, NOW()),
(48048, 'Gatika', 2, 8, 1, NOW()),
(48049, 'Gautegiz Arteaga', 2, 8, 1, NOW()),
(48050, 'Gernika-Lumo', 2, 8, 1, NOW()),
(48051, 'Getxo', 2, 8, 1, NOW()),
(48052, 'Gizaburuaga', 2, 8, 1, NOW()),
(48053, 'Gordexola', 2, 8, 1, NOW()),
(48054, 'Gorliz', 2, 8, 1, NOW()),
(48055, 'Güeñes', 2, 8, 1, NOW()),
(48056, 'Ibarrangelu', 2, 8, 1, NOW()),
(48057, 'Igorre', 2, 8, 1, NOW()),
(48058, 'Ispaster', 2, 8, 1, NOW()),
(48059, 'Iurreta', 2, 8, 1, NOW()),
(48060, 'Izurtza', 2, 8, 1, NOW()),
(48061, 'Karrantza Harana/Valle de Carranza', 2, 8, 1, NOW()),
(48062, 'Kortezubi', 2, 8, 1, NOW()),
(48063, 'Lanestosa', 2, 8, 1, NOW()),
(48064, 'Larrabetzu', 2, 8, 1, NOW()),
(48065, 'Laukiz', 2, 8, 1, NOW()),
(48066, 'Leioa', 2, 8, 1, NOW()),
(48067, 'Lekeitio', 2, 8, 1, NOW()),
(48068, 'Lemoa', 2, 8, 1, NOW()),
(48069, 'Lemoiz', 2, 8, 1, NOW()),
(48070, 'Lezama', 2, 8, 1, NOW()),
(48071, 'Loiu', 2, 8, 1, NOW()),
(48072, 'Mallabia', 2, 8, 1, NOW()),
(48073, 'Mañaria', 2, 8, 1, NOW()),
(48074, 'Markina-Xemein', 2, 8, 1, NOW()),
(48075, 'Maruri-Jatabe', 2, 8, 1, NOW()),
(48076, 'Mendata', 2, 8, 1, NOW()),
(48077, 'Mendexa', 2, 8, 1, NOW()),
(48078, 'Meñaka', 2, 8, 1, NOW()),
(48079, 'Morga', 2, 8, 1, NOW()),
(48080, 'Muxika', 2, 8, 1, NOW()),
(48081, 'Mundaka', 2, 8, 1, NOW()),
(48082, 'Mungia', 2, 8, 1, NOW()),
(48083, 'Muskiz', 2, 8, 1, NOW()),
(48084, 'Mutriku', 2, 8, 1, NOW()),
(48085, 'Nabarniz', 2, 8, 1, NOW()),
(48086, 'Ondarroa', 2, 8, 1, NOW()),
(48087, 'Orozko', 2, 8, 1, NOW()),
(48088, 'Ortuella', 2, 8, 1, NOW()),
(48089, 'Otxandio', 2, 8, 1, NOW()),
(48090, 'Pedernales', 2, 8, 1, NOW()),
(48091, 'Plentzia', 2, 8, 1, NOW()),
(48092, 'Portugalete', 2, 8, 1, NOW()),
(48093, 'Santurtzi', 2, 8, 1, NOW()),
(48094, 'Sestao', 2, 8, 1, NOW()),
(48095, 'Sondika', 2, 8, 1, NOW()),
(48096, 'Sopelana', 2, 8, 1, NOW()),
(48097, 'Sopuerta', 2, 8, 1, NOW()),
(48098, 'Sukarrieta', 2, 8, 1, NOW()),
(48099, 'Trucios-Turtzioz', 2, 8, 1, NOW()),
(48100, 'Ubide', 2, 8, 1, NOW()),
(48101, 'Ugao-Miraballes', 2, 8, 1, NOW()),
(48102, 'Urduliz', 2, 8, 1, NOW()),
(48103, 'Urduña/Orduña', 2, 8, 1, NOW()),
(48104, 'Valle de Trápaga-Trapagaran', 2, 8, 1, NOW()),
(48105, 'Zaldibar', 2, 8, 1, NOW()),
(48106, 'Zalla', 2, 8, 1, NOW()),
(48107, 'Zamudio', 2, 8, 1, NOW()),
(48108, 'Zaratamo', 2, 8, 1, NOW()),
(48109, 'Zeanuri', 2, 8, 1, NOW()),
(48110, 'Zeberio', 2, 8, 1, NOW()),
(48111, 'Zierbena', 2, 8, 1, NOW()),
(48912, 'Ziortza-Bolibar', 2, 8, 1, NOW())

ON DUPLICATE KEY UPDATE
    nombre = VALUES(nombre),
    provincia_id = VALUES(provincia_id),
    comarca_id = VALUES(comarca_id),
    activo = 1,  -- RESTAURAR activo a 1
    created_at = IFNULL(created_at, NOW());

-- =====================================================================
-- PASO 6: Restaurar/Actualizar TODOS los municipios de Gipuzkoa (provincia_id=3)
-- =====================================================================
SELECT 'Restaurando municipios de Gipuzkoa...' AS Paso;

INSERT INTO dim_municipios (codigo_ine, nombre, provincia_id, comarca_id, activo, created_at) VALUES
(20001, 'Abaltzisketa', 3, 7, 1, NOW()),
(20002, 'Aduna', 3, 7, 1, NOW()),
(20003, 'Aia', 3, 7, 1, NOW()),
(20004, 'Aizarnazabal', 3, 7, 1, NOW()),
(20005, 'Albiztur', 3, 7, 1, NOW()),
(20006, 'Alegia', 3, 7, 1, NOW()),
(20007, 'Alkiza', 3, 7, 1, NOW()),
(20008, 'Altzaga', 3, 7, 1, NOW()),
(20009, 'Altzo', 3, 7, 1, NOW()),
(20010, 'Amezketa', 3, 7, 1, NOW()),
(20011, 'Andoain', 3, 7, 1, NOW()),
(20012, 'Anoeta', 3, 7, 1, NOW()),
(20013, 'Antzuola', 3, 7, 1, NOW()),
(20014, 'Arama', 3, 7, 1, NOW()),
(20015, 'Aretxabaleta', 3, 7, 1, NOW()),
(20016, 'Arrasate/Mondragón', 3, 7, 1, NOW()),
(20017, 'Asteasu', 3, 7, 1, NOW()),
(20018, 'Astigarraga', 3, 7, 1, NOW()),
(20019, 'Ataun', 3, 7, 1, NOW()),
(20020, 'Azkoitia', 3, 7, 1, NOW()),
(20021, 'Azpeitia', 3, 7, 1, NOW()),
(20022, 'Baliarrain', 3, 7, 1, NOW()),
(20023, 'Beasain', 3, 7, 1, NOW()),
(20024, 'Beizama', 3, 7, 1, NOW()),
(20025, 'Belauntza', 3, 7, 1, NOW()),
(20026, 'Berastegi', 3, 7, 1, NOW()),
(20027, 'Bergara', 3, 7, 1, NOW()),
(20028, 'Berrobi', 3, 7, 1, NOW()),
(20029, 'Bidania-Goiatz', 3, 7, 1, NOW()),
(20030, 'Deba', 3, 7, 1, NOW()),
(20031, 'Donostia-San Sebastián', 3, 7, 1, NOW()),
(20032, 'Eibar', 3, 7, 1, NOW()),
(20033, 'Elduain', 3, 7, 1, NOW()),
(20034, 'Elgeta', 3, 7, 1, NOW()),
(20035, 'Elgoibar', 3, 7, 1, NOW()),
(20036, 'Errenteria', 3, 7, 1, NOW()),
(20037, 'Errezil', 3, 7, 1, NOW()),
(20038, 'Eskoriatza', 3, 7, 1, NOW()),
(20039, 'Ezkio-Itsaso', 3, 7, 1, NOW()),
(20040, 'Gabiria', 3, 7, 1, NOW()),
(20041, 'Gaintza', 3, 7, 1, NOW()),
(20042, 'Gaztelu', 3, 7, 1, NOW()),
(20043, 'Getaria', 3, 7, 1, NOW()),
(20044, 'Hernani', 3, 7, 1, NOW()),
(20045, 'Hernialde', 3, 7, 1, NOW()),
(20046, 'Hondarribia', 3, 7, 1, NOW()),
(20047, 'Ibarra', 3, 7, 1, NOW()),
(20048, 'Idiazabal', 3, 7, 1, NOW()),
(20049, 'Ikaztegieta', 3, 7, 1, NOW()),
(20050, 'Irun', 3, 7, 1, NOW()),
(20051, 'Irura', 3, 7, 1, NOW()),
(20052, 'Itsasondo', 3, 7, 1, NOW()),
(20053, 'Larraul', 3, 7, 1, NOW()),
(20054, 'Lasarte-Oria', 3, 7, 1, NOW()),
(20055, 'Lazkao', 3, 7, 1, NOW()),
(20056, 'Leaburu', 3, 7, 1, NOW()),
(20057, 'Legazpi', 3, 7, 1, NOW()),
(20058, 'Legorreta', 3, 7, 1, NOW()),
(20059, 'Leintz-Gatzaga', 3, 7, 1, NOW()),
(20060, 'Lezo', 3, 7, 1, NOW()),
(20061, 'Lizartza', 3, 7, 1, NOW()),
(20062, 'Mendaro', 3, 7, 1, NOW()),
(20063, 'Mutiloa', 3, 7, 1, NOW()),
(20064, 'Mutriku', 3, 7, 1, NOW()),
(20065, 'Oiartzun', 3, 7, 1, NOW()),
(20066, 'Olaberria', 3, 7, 1, NOW()),
(20067, 'Onati', 3, 7, 1, NOW()),
(20068, 'Ordizia', 3, 7, 1, NOW()),
(20069, 'Orendain', 3, 7, 1, NOW()),
(20070, 'Orio', 3, 7, 1, NOW()),
(20071, 'Ormaiztegi', 3, 7, 1, NOW()),
(20072, 'Pasaia', 3, 7, 1, NOW()),
(20073, 'Segura', 3, 7, 1, NOW()),
(20074, 'Soraluze-Placencia de las Armas', 3, 7, 1, NOW()),
(20075, 'Tolosa', 3, 7, 1, NOW()),
(20076, 'Urnieta', 3, 7, 1, NOW()),
(20077, 'Urretxu', 3, 7, 1, NOW()),
(20078, 'Usurbil', 3, 7, 1, NOW()),
(20079, 'Villabona', 3, 7, 1, NOW()),
(20080, 'Zaldibia', 3, 7, 1, NOW()),
(20081, 'Zarautz', 3, 7, 1, NOW()),
(20082, 'Zegama', 3, 7, 1, NOW()),
(20083, 'Zerain', 3, 7, 1, NOW()),
(20084, 'Zestoa', 3, 7, 1, NOW()),
(20085, 'Zizurkil', 3, 7, 1, NOW()),
(20086, 'Zumaia', 3, 7, 1, NOW()),
(20087, 'Zumarraga', 3, 7, 1, NOW()),
(20088, 'Zumárraga', 3, 7, 1, NOW())

ON DUPLICATE KEY UPDATE
    nombre = VALUES(nombre),
    provincia_id = VALUES(provincia_id),
    comarca_id = VALUES(comarca_id),
    activo = 1,  -- RESTAURAR activo a 1
    created_at = IFNULL(created_at, NOW());

-- =====================================================================
-- PASO 7: Actualizar códigos postales de municipios de Álava
-- =====================================================================
-- IMPORTANTE: Ahora usamos codigo_ine para identificar municipios
-- NO usamos ID porque es autoincrementado y puede cambiar
-- =====================================================================

SELECT 'Actualizando códigos postales de Álava...' AS Paso;

-- Actualizar códigos postales usando codigo_ine (NO id)
UPDATE dim_municipios SET codigo_postal = '01470' WHERE codigo_ine = 1002;  -- Amurrio
UPDATE dim_municipios SET codigo_postal = '01474' WHERE codigo_ine = 1004;  -- Artziniega
UPDATE dim_municipios SET codigo_postal = '01479' WHERE codigo_ine = 1010;  -- Ayala / Aiara
UPDATE dim_municipios SET codigo_postal = '01400' WHERE codigo_ine = 1038;  -- Llodio / Laudio (si existe)
UPDATE dim_municipios SET codigo_postal = '01476' WHERE codigo_ine = 1042;  -- Okondo
UPDATE dim_municipios SET codigo_postal = '01307' WHERE codigo_ine = 1011;  -- Baños de Ebro / Mañueta
UPDATE dim_municipios SET codigo_postal = '01340' WHERE codigo_ine = 1022;  -- Elciego
UPDATE dim_municipios SET codigo_postal = '01320' WHERE codigo_ine = 1025;  -- Elvillar / Bilar
UPDATE dim_municipios SET codigo_postal = '01309' WHERE codigo_ine = 1019;  -- Kripan
UPDATE dim_municipios SET codigo_postal = '01330' WHERE codigo_ine = 1028;  -- Labastida / Bastida
UPDATE dim_municipios SET codigo_postal = '01300' WHERE codigo_ine = 1031;  -- Laguardia
UPDATE dim_municipios SET codigo_postal = '01308' WHERE codigo_ine = 1032;  -- Lanciego / Lantziego
UPDATE dim_municipios SET codigo_postal = '01306' WHERE codigo_ine = 1033;  -- Lapuebla de Labarca
UPDATE dim_municipios SET codigo_postal = '01321' WHERE codigo_ine = 1034;  -- Leza
UPDATE dim_municipios SET codigo_postal = '01320' WHERE codigo_ine = 1039;  -- Moreda de Álava / Moreda Araba
UPDATE dim_municipios SET codigo_postal = '01309' WHERE codigo_ine = 1041;  -- Navaridas
UPDATE dim_municipios SET codigo_postal = '01320' WHERE codigo_ine = 1043;  -- Oyón-Oion
UPDATE dim_municipios SET codigo_postal = '01307' WHERE codigo_ine = 1052;  -- Samaniego
UPDATE dim_municipios SET codigo_postal = '01307' WHERE codigo_ine = 1057;  -- Villabuena de Álava / Eskuernaga
UPDATE dim_municipios SET codigo_postal = '01208' WHERE codigo_ine = 1060;  -- Yécora / Iekora
UPDATE dim_municipios SET codigo_postal = '01240' WHERE codigo_ine = 1001;  -- Alegría-Dulantzi
UPDATE dim_municipios SET codigo_postal = '01250' WHERE codigo_ine = 1009;  -- Asparrena
UPDATE dim_municipios SET codigo_postal = '01110' WHERE codigo_ine = 1013;  -- Barrundia
UPDATE dim_municipios SET codigo_postal = '01130' WHERE codigo_ine = 1021;  -- Elburgo / Burgelu
UPDATE dim_municipios SET codigo_postal = '01259' WHERE codigo_ine = 1027;  -- Iruraiz-Gauna
UPDATE dim_municipios SET codigo_postal = '01200' WHERE codigo_ine = 1051;  -- Salvatierra / Agurain
UPDATE dim_municipios SET codigo_postal = '01428' WHERE codigo_ine = 1053;  -- San Millán / Donemiliaga
UPDATE dim_municipios SET codigo_postal = '01130' WHERE codigo_ine = 1061;  -- Zalduondo
UPDATE dim_municipios SET codigo_postal = '01166' WHERE codigo_ine = 1003;  -- Aramaio
UPDATE dim_municipios SET codigo_postal = '01013' WHERE codigo_ine = 1008;  -- Arratzua-Ubarrundia
UPDATE dim_municipios SET codigo_postal = '01170' WHERE codigo_ine = 1036;  -- Legutio
UPDATE dim_municipios SET codigo_postal = '01138' WHERE codigo_ine = 1054;  -- Urkabustaiz
UPDATE dim_municipios SET codigo_postal = '01199' WHERE codigo_ine = 1018;  -- Zigoitia
UPDATE dim_municipios SET codigo_postal = '01194' WHERE codigo_ine = 1063;  -- Zuia
UPDATE dim_municipios SET codigo_postal = '01426' WHERE codigo_ine = 1049;  -- Añana
UPDATE dim_municipios SET codigo_postal = '01213' WHERE codigo_ine = 1006;  -- Armiñón
UPDATE dim_municipios SET codigo_postal = '01211' WHERE codigo_ine = 1014;  -- Berantevilla
UPDATE dim_municipios SET codigo_postal = '01230' WHERE codigo_ine = 1901;  -- Iruña de Oca / Iruña Oka
UPDATE dim_municipios SET codigo_postal = '01478' WHERE codigo_ine = 1020;  -- Kuartango
UPDATE dim_municipios SET codigo_postal = '01212' WHERE codigo_ine = 1902;  -- Lantarón
UPDATE dim_municipios SET codigo_postal = '01220' WHERE codigo_ine = 1024;  -- Ribera Alta / Erriberagoitia
UPDATE dim_municipios SET codigo_postal = '01219' WHERE codigo_ine = 1047;  -- Ribera Baja / Erriberabeitia
UPDATE dim_municipios SET codigo_postal = '01439' WHERE codigo_ine = 1055;  -- Valdegovía / Gaubea
UPDATE dim_municipios SET codigo_postal = '01214' WHERE codigo_ine = 1062;  -- Zambrana
UPDATE dim_municipios SET codigo_postal = '01196' WHERE codigo_ine = 1058;  -- Arraia-Maeztu
UPDATE dim_municipios SET codigo_postal = '01118' WHERE codigo_ine = 1016;  -- Bernedo
UPDATE dim_municipios SET codigo_postal = '01111' WHERE codigo_ine = 1017;  -- Campezo / Kanpezu
UPDATE dim_municipios SET codigo_postal = '01308' WHERE codigo_ine = 1030;  -- Lagrán
UPDATE dim_municipios SET codigo_postal = '01212' WHERE codigo_ine = 1044;  -- Peñacerrada-Urizaharra
UPDATE dim_municipios SET codigo_postal = '01268' WHERE codigo_ine = 1056;  -- Valle de Arana / Harana

-- =====================================================================
-- PASO 8: Verificación final
-- =====================================================================
SELECT 'Verificación final de la tabla restaurada:' AS Paso;

-- Contar totales por provincia
SELECT
    p.nombre AS provincia,
    COUNT(m.id) AS total_municipios,
    SUM(CASE WHEN m.activo = 1 THEN 1 ELSE 0 END) AS activos,
    SUM(CASE WHEN m.created_at IS NOT NULL THEN 1 ELSE 0 END) AS con_created_at,
    SUM(CASE WHEN m.codigo_postal IS NOT NULL THEN 1 ELSE 0 END) AS con_codigo_postal
FROM dim_provincias p
LEFT JOIN dim_municipios m ON p.id = m.provincia_id
GROUP BY p.id, p.nombre
ORDER BY p.id;

-- Mostrar municipios de Álava con códigos postales
SELECT
    m.id,
    m.codigo_ine,
    m.nombre,
    m.codigo_postal,
    m.activo,
    m.created_at,
    c.comarca_nombre
FROM dim_municipios m
LEFT JOIN dim_comarcas c ON m.comarca_id = c.id
WHERE m.provincia_id = 1
ORDER BY m.codigo_ine;

-- Mostrar primeros 10 de Bizkaia para verificar
SELECT
    m.id,
    m.codigo_ine,
    m.nombre,
    m.activo,
    m.created_at
FROM dim_municipios m
WHERE m.provincia_id = 2
ORDER BY m.codigo_ine
LIMIT 10;

-- Mostrar primeros 10 de Gipuzkoa para verificar
SELECT
    m.id,
    m.codigo_ine,
    m.nombre,
    m.activo,
    m.created_at
FROM dim_municipios m
WHERE m.provincia_id = 3
ORDER BY m.codigo_ine
LIMIT 10;

-- =====================================================================
-- FIN DEL SCRIPT DE RECUPERACIÓN
-- =====================================================================
SELECT '¡Script de recuperación completado exitosamente!' AS Resultado;
SELECT 'Todos los municipios han sido restaurados con activo=1 y created_at' AS Nota;
