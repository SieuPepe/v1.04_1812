-- Corrección de municipios de Bizkaia
-- ====================================
-- Este script elimina los municipios incorrectos de Bizkaia
-- e inserta la lista correcta de 112 municipios

USE cert_dev;

-- 1. Eliminar municipios incorrectos de Bizkaia
-- ==============================================
DELETE FROM tbl_municipios WHERE provincia_id = 2;

-- 2. Insertar municipios correctos de Bizkaia (112 municipios)
-- =============================================================
INSERT INTO tbl_municipios (provincia_id, NAMEUNIT, CODIGOINE) VALUES
-- Provincia de Bizkaia (código 48)
(2, 'Abadiño', 48001),
(2, 'Abanto y Ciérvana-Abanto Zierbena', 48002),
(2, 'Ajangiz', 48911),
(2, 'Alonsotegi', 48912),
(2, 'Amorebieta-Etxano', 48003),
(2, 'Amoroto', 48004),
(2, 'Arakaldo', 48005),
(2, 'Arantzazu', 48006),
(2, 'Areatza', 48093),
(2, 'Arrankudiaga-Zollo', 48009),
(2, 'Arratzu', 48914),
(2, 'Arrieta', 48010),
(2, 'Arrigorriaga', 48011),
(2, 'Artea', 48023),
(2, 'Artzentales', 48008),
(2, 'Atxondo', 48091),
(2, 'Aulesti', 48070),
(2, 'Bakio', 48012),
(2, 'Balmaseda', 48090),
(2, 'Barakaldo', 48013),
(2, 'Barrika', 48014),
(2, 'Basauri', 48015),
(2, 'Bedia', 48092),
(2, 'Berango', 48016),
(2, 'Bermeo', 48017),
(2, 'Berriatua', 48018),
(2, 'Berriz', 48019),
(2, 'Bilbao', 48020),
(2, 'Busturia', 48021),
(2, 'Derio', 48901),
(2, 'Dima', 48026),
(2, 'Durango', 48027),
(2, 'Ea', 48028),
(2, 'Elantxobe', 48031),
(2, 'Elorrio', 48032),
(2, 'Erandio', 48902),
(2, 'Ereño', 48033),
(2, 'Ermua', 48034),
(2, 'Errigoiti', 48079),
(2, 'Etxebarri', 48029),
(2, 'Etxebarria', 48030),
(2, 'Forua', 48906),
(2, 'Fruiz', 48035),
(2, 'Galdakao', 48036),
(2, 'Galdames', 48037),
(2, 'Gamiz-Fika', 48038),
(2, 'Garai', 48039),
(2, 'Gatika', 48040),
(2, 'Gautegiz Arteaga', 48041),
(2, 'Gernika-Lumo', 48046),
(2, 'Getxo', 48044),
(2, 'Gizaburuaga', 48047),
(2, 'Gordexola', 48042),
(2, 'Gorliz', 48043),
(2, 'Güeñes', 48045),
(2, 'Ibarrangelu', 48048),
(2, 'Igorre', 48094),
(2, 'Ispaster', 48049),
(2, 'Iurreta', 48910),
(2, 'Izurtza', 48050),
(2, 'Karrantza Harana/Valle de Carranza', 48022),
(2, 'Kortezubi', 48907),
(2, 'Lanestosa', 48051),
(2, 'Larrabetzu', 48052),
(2, 'Laukiz', 48053),
(2, 'Leioa', 48054),
(2, 'Lekeitio', 48057),
(2, 'Lemoa', 48055),
(2, 'Lemoiz', 48056),
(2, 'Lezama', 48081),
(2, 'Loiu', 48903),
(2, 'Mallabia', 48058),
(2, 'Mañaria', 48059),
(2, 'Markina-Xemein', 48060),
(2, 'Maruri-Jatabe', 48061),
(2, 'Mendata', 48062),
(2, 'Mendexa', 48063),
(2, 'Meñaka', 48064),
(2, 'Morga', 48066),
(2, 'Mundaka', 48068),
(2, 'Mungia', 48069),
(2, 'Munitibar-Arbatzegi Gerrikaitz', 48007),
(2, 'Murueta', 48908),
(2, 'Muskiz', 48071),
(2, 'Muxika', 48067),
(2, 'Nabarniz', 48909),
(2, 'Ondarroa', 48073),
(2, 'Orozko', 48075),
(2, 'Ortuella', 48083),
(2, 'Otxandio', 48072),
(2, 'Plentzia', 48077),
(2, 'Portugalete', 48078),
(2, 'Santurtzi', 48082),
(2, 'Sestao', 48084),
(2, 'Sondika', 48904),
(2, 'Sopela', 48085),
(2, 'Sopuerta', 48086),
(2, 'Sukarrieta', 48076),
(2, 'Trucios-Turtzioz', 48087),
(2, 'Ubide', 48088),
(2, 'Ugao-Miraballes', 48065),
(2, 'Urduliz', 48089),
(2, 'Urduña/Orduña', 48074),
(2, 'Valle de Trápaga-Trapagaran', 48080),
(2, 'Zaldibar', 48095),
(2, 'Zalla', 48096),
(2, 'Zamudio', 48905),
(2, 'Zaratamo', 48097),
(2, 'Zeanuri', 48024),
(2, 'Zeberio', 48025),
(2, 'Zierbena', 48913),
(2, 'Ziortza-Bolibar', 48915);

-- 3. Verificación
-- ===============
SELECT 'Municipios actualizados:' AS resultado;
SELECT
    p.nombre AS provincia,
    COUNT(m.id) AS total_municipios
FROM dim_provincias p
LEFT JOIN tbl_municipios m ON m.provincia_id = p.id
GROUP BY p.id, p.nombre
ORDER BY p.codigo;

-- Mostrar algunos municipios de Bizkaia para verificar
SELECT 'Muestra de municipios de Bizkaia:' AS resultado;
SELECT NAMEUNIT, CODIGOINE
FROM tbl_municipios
WHERE provincia_id = 2
ORDER BY NAMEUNIT
LIMIT 10;
