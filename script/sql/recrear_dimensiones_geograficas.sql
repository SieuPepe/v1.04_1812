-- ============================================================================
-- RECREAR DIMENSIONES GEOGRÁFICAS - ÁLAVA COMPLETA
-- ============================================================================
-- Basado en la lista oficial de concejos de Álava
-- https://es.wikipedia.org/wiki/Anexo:Concejos_de_Álava
--
-- USO:
--   mysql -h localhost -P 3307 -u root -p [esquema] < recrear_dimensiones_geograficas.sql
-- ============================================================================

SELECT DATABASE() AS esquema_actual;
SELECT '=== INICIO: Recrear dimensiones geográficas ===' AS info;
SELECT NOW() AS fecha_ejecucion;

-- ============================================================================
-- FASE 0: DESACTIVAR RESTRICCIONES Y LIMPIAR
-- ============================================================================

SELECT '>>> FASE 0: Preparando...' AS paso;

SET SQL_SAFE_UPDATES = 0;
SET FOREIGN_KEY_CHECKS = 0;

-- Limpiar referencias en tablas de hechos
UPDATE tbl_partes SET municipio_id = NULL, concejo_id = NULL
WHERE municipio_id IS NOT NULL OR concejo_id IS NOT NULL;
SELECT CONCAT('  ✓ tbl_partes limpiada: ', ROW_COUNT(), ' registros') AS resultado;

-- ============================================================================
-- FASE 1: VACIAR TABLAS
-- ============================================================================

SELECT '>>> FASE 1: Vaciando tablas...' AS paso;

TRUNCATE TABLE dim_concejos;
TRUNCATE TABLE dim_municipios;
TRUNCATE TABLE dim_comarcas;

SELECT '  ✓ Tablas vaciadas' AS resultado;

-- ============================================================================
-- FASE 2: CREAR COMARCAS
-- ============================================================================

SELECT '>>> FASE 2: Creando comarcas...' AS paso;

INSERT INTO dim_comarcas (id, provincia_id, comarca_codigo, comarca_nombre) VALUES
(1, 1, 'TODO', 'Todo Álava'),
(2, 1, 'AIAR', 'Ayala / Aiaraldea'),
(3, 1, 'LLAN', 'Llanada Alavesa'),
(4, 1, 'RIOJ', 'Rioja Alavesa'),
(5, 1, 'AÑAN', 'Añana'),
(6, 1, 'MONT', 'Montaña Alavesa'),
(7, 1, 'GORB', 'Estribaciones del Gorbea');

SELECT CONCAT('  ✓ Comarcas: ', ROW_COUNT()) AS resultado;

-- ============================================================================
-- FASE 3: CREAR MUNICIPIOS
-- ============================================================================

SELECT '>>> FASE 3: Creando municipios...' AS paso;

-- 3.1 MUNICIPIOS "TODO" (IDs 1-7)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(1, '00001', 'Todo Álava', 1, 1, 1),
(2, '00002', 'Todo Aiaraldea', 1, 2, 1),
(3, '00003', 'Todo Llanada Alavesa', 1, 3, 1),
(4, '00004', 'Todo Rioja Alavesa', 1, 4, 1),
(5, '00005', 'Todo Añana', 1, 5, 1),
(6, '00006', 'Todo Montaña Alavesa', 1, 6, 1),
(7, '00007', 'Todo Estribaciones Gorbea', 1, 7, 1);

-- 3.2 MUNICIPIOS REALES

-- COMARCA: Ayala / Aiaraldea (comarca_id = 2)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(101, '01002', 'Amurrio', 1, 2, 1),
(102, '01010', 'Ayala/Aiara', 1, 2, 1),
(103, '01003', 'Aramaio', 1, 2, 1),
(104, '01004', 'Artziniega', 1, 2, 1),
(105, '01036', 'Laudio/Llodio', 1, 2, 1),
(106, '01042', 'Okondo', 1, 2, 1);

-- COMARCA: Llanada Alavesa (comarca_id = 3)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(201, '01001', 'Alegría-Dulantzi', 1, 3, 1),
(202, '01008', 'Arrazua-Ubarrundia', 1, 3, 1),
(203, '01009', 'Asparrena', 1, 3, 1),
(204, '01013', 'Barrundia', 1, 3, 1),
(205, '01021', 'Elburgo/Burgelu', 1, 3, 1),
(206, '01027', 'Iruraiz-Gauna', 1, 3, 1),
(207, '01053', 'San Millán/Donemiliaga', 1, 3, 1),
(208, '01059', 'Vitoria-Gasteiz', 1, 3, 1),
(209, '01051', 'Agurain/Salvatierra', 1, 3, 1),
(210, '01061', 'Zalduondo', 1, 3, 1);

-- COMARCA: Rioja Alavesa (comarca_id = 4)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(301, '01028', 'Labastida/Bastida', 1, 4, 1),
(302, '01031', 'Laguardia', 1, 4, 1),
(303, '01043', 'Oyón-Oion', 1, 4, 1),
(304, '01011', 'Baños de Ebro/Mañueta', 1, 4, 1),
(305, '01019', 'Kripan', 1, 4, 1),
(306, '01022', 'Elciego', 1, 4, 1),
(307, '01032', 'Lanciego/Lantziego', 1, 4, 1),
(308, '01033', 'Lapuebla de Labarca', 1, 4, 1),
(309, '01034', 'Leza', 1, 4, 1),
(310, '01039', 'Moreda de Álava', 1, 4, 1),
(311, '01041', 'Navaridas', 1, 4, 1),
(312, '01052', 'Samaniego', 1, 4, 1),
(313, '01057', 'Villabuena de Álava', 1, 4, 1),
(314, '01060', 'Yécora/Iekora', 1, 4, 1);

-- COMARCA: Añana (comarca_id = 5)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(401, '01049', 'Añana', 1, 5, 1),
(402, '01006', 'Armiñón', 1, 5, 1),
(403, '01014', 'Berantevilla', 1, 5, 1),
(404, '01020', 'Kuartango', 1, 5, 1),
(405, '01901', 'Iruña Oka', 1, 5, 1),
(406, '01902', 'Lantarón', 1, 5, 1),
(407, '01023', 'Ribera Alta', 1, 5, 1),
(408, '01047', 'Ribera Baja', 1, 5, 1),
(409, '01055', 'Valdegovía/Gaubea', 1, 5, 1),
(410, '01062', 'Zambrana', 1, 5, 1);

-- COMARCA: Montaña Alavesa (comarca_id = 6)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(501, '01037', 'Arraia-Maeztu', 1, 6, 1),
(502, '01016', 'Bernedo', 1, 6, 1),
(503, '01017', 'Campezo/Kanpezu', 1, 6, 1),
(504, '01030', 'Lagrán', 1, 6, 1),
(505, '01044', 'Peñacerrada-Urizaharra', 1, 6, 1),
(506, '01056', 'Harana/Valle de Arana', 1, 6, 1);

-- COMARCA: Estribaciones del Gorbea (comarca_id = 7)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(601, '01018', 'Zigoitia', 1, 7, 1),
(602, '01063', 'Zuia', 1, 7, 1),
(603, '01058', 'Legutio', 1, 7, 1),
(604, '01054', 'Urkabustaiz', 1, 7, 1);

SELECT CONCAT('  ✓ Municipios: ', (SELECT COUNT(*) FROM dim_municipios)) AS resultado;

-- ============================================================================
-- FASE 4: CREAR CONCEJOS
-- ============================================================================

SELECT '>>> FASE 4: Creando concejos...' AS paso;

-- 4.1 CONCEJOS "TODO" para municipios especiales (IDs 1-7)
INSERT INTO dim_concejos (id, municipio_id, nombre, activo) VALUES
(1, 1, 'Todo Álava', 1),
(2, 2, 'Todo Aiaraldea', 1),
(3, 3, 'Todo Llanada Alavesa', 1),
(4, 4, 'Todo Rioja Alavesa', 1),
(5, 5, 'Todo Añana', 1),
(6, 6, 'Todo Montaña Alavesa', 1),
(7, 7, 'Todo Estribaciones Gorbea', 1);

-- 4.2 CONCEJOS "TODO" para cada municipio real
INSERT INTO dim_concejos (municipio_id, nombre, activo)
SELECT id, CONCAT('Todo ', municipio_nombre), 1
FROM dim_municipios WHERE id > 7;

-- ============================================================================
-- 4.3 CONCEJOS REALES POR MUNICIPIO
-- ============================================================================

-- AMURRIO (101)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(101, 'Aloria', 1),
(101, 'Amurrio', 1),
(101, 'Artomaña', 1),
(101, 'Baranbio', 1),
(101, 'Delika', 1),
(101, 'Larrinbe', 1),
(101, 'Lekamaña', 1),
(101, 'Lezama', 1),
(101, 'Saratxo', 1),
(101, 'Tertanga', 1);

-- AYALA/AIARA (102)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(102, 'Agiñaga', 1),
(102, 'Añes', 1),
(102, 'Arespalditza/Respaldiza', 1),
(102, 'Costera/Opellora', 1),
(102, 'Etxegoien', 1),
(102, 'Erbi', 1),
(102, 'Izoria', 1),
(102, 'Lejarzo/Lexartzu', 1),
(102, 'Llanteno', 1),
(102, 'Luxo/Lujo', 1),
(102, 'Luiaondo', 1),
(102, 'Madaria', 1),
(102, 'Maroño', 1),
(102, 'Menagarai-Beotegi', 1),
(102, 'Menoio', 1),
(102, 'Murga', 1),
(102, 'Olabezar', 1),
(102, 'Ozeka', 1),
(102, 'Quejana/Kexaa', 1),
(102, 'Retes de Llanteno', 1),
(102, 'Salmantón', 1),
(102, 'Soxo/Sojo', 1),
(102, 'Zuaza/Zuhatza', 1);

-- ARAMAIO (103)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(103, 'Oleta', 1);

-- ALEGRÍA-DULANTZI (201)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(201, 'Alegría-Dulantzi', 1),
(201, 'Egileta', 1);

-- ARRAZUA-UBARRUNDIA (202)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(202, 'Arroiabe', 1),
(202, 'Arzubiaga', 1),
(202, 'Betolaza', 1),
(202, 'Ziriano', 1),
(202, 'Durana', 1),
(202, 'Landa', 1),
(202, 'Luko', 1),
(202, 'Mendibil', 1),
(202, 'Ullíbarri-Gamboa', 1),
(202, 'Zurbano/Zurbao', 1);

-- ASPARRENA (203)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(203, 'Albeiz/Albéniz', 1),
(203, 'Ametzaga Asparrena', 1),
(203, 'Andoin', 1),
(203, 'Arriola', 1),
(203, 'Egino', 1),
(203, 'Gordoa', 1),
(203, 'Ibarguren', 1),
(203, 'Ilarduia', 1),
(203, 'Urabain', 1);

-- BARRUNDIA (204)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(204, 'Audikana', 1),
(204, 'Dallo', 1),
(204, 'Elgea', 1),
(204, 'Etura', 1),
(204, 'Etxabarri Urtupiña', 1),
(204, 'Gebara', 1),
(204, 'Heredia', 1),
(204, 'Hermua', 1),
(204, 'Larrea', 1),
(204, 'Marieta-Larrintzar', 1),
(204, 'Maturana', 1),
(204, 'Mendixur/Mendíjur', 1),
(204, 'Ozaeta', 1);

-- ELBURGO/BURGELU (205)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(205, 'Añua', 1),
(205, 'Arbulu', 1),
(205, 'Argomaniz', 1),
(205, 'Elburgo/Burgelu', 1),
(205, 'Gazeta', 1),
(205, 'Hijona/Ixona', 1);

-- IRURAIZ-GAUNA (206)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(206, 'Alaitza', 1),
(206, 'Arrieta', 1),
(206, 'Azilu', 1),
(206, 'Erentxun', 1),
(206, 'Ezkerekotxa', 1),
(206, 'Gazeo', 1),
(206, 'Gauna', 1),
(206, 'Gereñu', 1),
(206, 'Jauregi', 1),
(206, 'Langarika', 1),
(206, 'Trokoniz', 1);

-- SAN MILLÁN/DONEMILIAGA (207)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(207, 'Adana', 1),
(207, 'Axpuru', 1),
(207, 'Bikuña/Vicuña', 1),
(207, 'Eguílaz/Egilatz', 1),
(207, 'Galarreta', 1),
(207, 'Luzuriaga', 1),
(207, 'Mezkia', 1),
(207, 'Munain', 1),
(207, 'Narbaiza', 1),
(207, 'Okariz', 1),
(207, 'Ordoñana/Erdoñana', 1),
(207, 'Durruma/San Román de San Millán', 1),
(207, 'Txintxetru', 1),
(207, 'Ullibarri-Jauregi/Uribarri-Jauregi', 1),
(207, 'Zuazo de San Millán/Zuhatzu Donemiliaga', 1);

-- VITORIA-GASTEIZ (208) - 60+ concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(208, 'Abetxuko', 1),
(208, 'Aberasturi', 1),
(208, 'Ehari/Ali', 1),
(208, 'Amarita', 1),
(208, 'Andollu', 1),
(208, 'Antezana/Andetxa', 1),
(208, 'Arangiz', 1),
(208, 'Arkauti/Arcaute', 1),
(208, 'Arkaia', 1),
(208, 'Aretxabaleta', 1),
(208, 'Argandoña', 1),
(208, 'Ariñiz/Aríñez', 1),
(208, 'Armentia', 1),
(208, 'Askartza', 1),
(208, 'Astegieta', 1),
(208, 'Berrostegieta', 1),
(208, 'Betoño', 1),
(208, 'Bolívar', 1),
(208, 'Castillo/Gaztelu', 1),
(208, 'Zerio', 1),
(208, 'Krispiña/Crispijana', 1),
(208, 'Elorriaga', 1),
(208, 'Eskibel', 1),
(208, 'Estarrona', 1),
(208, 'Foronda', 1),
(208, 'Gamarra Mayor/Gamarra Nagusia', 1),
(208, 'Gamarra Menor', 1),
(208, 'Gamiz', 1),
(208, 'Gardelegi', 1),
(208, 'Gobeo', 1),
(208, 'Gometxa', 1),
(208, 'Gereña', 1),
(208, 'Hueto Abajo/Otobarren', 1),
(208, 'Otogoien/Hueto Arriba', 1),
(208, 'Ilarratza', 1),
(208, 'Jungitu', 1),
(208, 'Lasarte', 1),
(208, 'Legarda', 1),
(208, 'Lermanda', 1),
(208, 'Lopidana', 1),
(208, 'Lubiano', 1),
(208, 'Margarita', 1),
(208, 'Martioda', 1),
(208, 'Matauko', 1),
(208, 'Mendiguren', 1),
(208, 'Mendiola', 1),
(208, 'Mendoza', 1),
(208, 'Miñao/Miñano Mayor', 1),
(208, 'Miñano Menor/Miñano Gutxia', 1),
(208, 'Monasterioguren', 1),
(208, 'Oreitia', 1),
(208, 'Otazu', 1),
(208, 'Retana', 1),
(208, 'Subijana de Álava/Subillana-Gasteiz', 1),
(208, 'Ullíbarri de los Olleros/Uribarri Nagusia', 1),
(208, 'Ullíbarri-Arrazua', 1),
(208, 'Ullíbarri-Viña/Uribarri-Dibiña', 1),
(208, 'Villafranca', 1),
(208, 'Yurre/Ihurre', 1),
(208, 'Zuazo de Vitoria/Zuhatzu', 1),
(208, 'Zumeltzu', 1);

-- LABASTIDA (301)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(301, 'Salinillas de Buradón/Gatzaga Buradon', 1);

-- LAGUARDIA (302)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(302, 'Páganos', 1);

-- OYÓN-OION (303)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(303, 'Barriobusto/Gorrebusto', 1),
(303, 'Labraza', 1);

-- AÑANA (401)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(401, 'Atiega', 1);

-- ARMIÑÓN (402)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(402, 'Armiñón', 1),
(402, 'Estavillo', 1);

-- BERANTEVILLA (403)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(403, 'Berantevilla', 1),
(403, 'Lacervilla', 1),
(403, 'Mijancas', 1),
(403, 'Santa Cruz del Fierro', 1),
(403, 'Santurde', 1),
(403, 'Tobera', 1);

-- KUARTANGO (404)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(404, 'Anda', 1),
(404, 'Aprikano', 1),
(404, 'Etxabarri Kuartango', 1),
(404, 'Jokano', 1),
(404, 'Luna', 1),
(404, 'Marinda', 1),
(404, 'Sendadiano', 1),
(404, 'Uribarri Kuartango', 1),
(404, 'Urbina Eza', 1),
(404, 'Zuhatzu Kuartango', 1);

-- IRUÑA OKA (405)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(405, 'Montevite/Mandaita', 1),
(405, 'Nanclares de la Oca/Langraiz Oka', 1),
(405, 'Ollávarre/Olabarri', 1),
(405, 'Trespuentes', 1),
(405, 'Víllodas/Billoda', 1);

-- LANTARÓN (406)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(406, 'Alcedo', 1),
(406, 'Bergonda/Bergüenda', 1),
(406, 'Caicedo de Yuso', 1),
(406, 'Comunión/Komunioi', 1),
(406, 'Fontecha', 1),
(406, 'Leciñana del Camino/Leziñana', 1),
(406, 'Molinilla', 1),
(406, 'Puentelarrá/Larrazubi', 1),
(406, 'Salcedo', 1),
(406, 'Sobrón', 1),
(406, 'Turiso', 1),
(406, 'Zubillaga', 1);

-- RIBERA ALTA (407)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(407, 'Antezana de la Ribera', 1),
(407, 'Anuntzeta/Anúcita', 1),
(407, 'Arreo', 1),
(407, 'Artaza-Escota/Artatza-Axkoeta', 1),
(407, 'Barrón', 1),
(407, 'Basquiñuelas', 1),
(407, 'Caicedo-Sopeña', 1),
(407, 'Hereña', 1),
(407, 'Lasierra', 1),
(407, 'Leciñana de la Oca', 1),
(407, 'Morillas', 1),
(407, 'Ormijana', 1),
(407, 'Paúl', 1),
(407, 'Pobes', 1),
(407, 'Subijana-Morillas', 1),
(407, 'Tuyo', 1),
(407, 'Villabezana', 1),
(407, 'Villaluenga', 1),
(407, 'Villambrosa', 1),
(407, 'Viloria', 1);

-- RIBERA BAJA (408)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(408, 'Igay', 1),
(408, 'Manzanos', 1),
(408, 'Melledes', 1),
(408, 'Quintanilla de la Ribera', 1),
(408, 'Rivabellosa', 1),
(408, 'Rivaguda', 1);

-- VALDEGOVÍA (409)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(409, 'Acebedo', 1),
(409, 'Bachicabo', 1),
(409, 'Barrio', 1),
(409, 'Basabe', 1),
(409, 'Bóveda', 1),
(409, 'Caranca y Mioma', 1),
(409, 'Karkamu', 1),
(409, 'Corro', 1),
(409, 'Espejo', 1),
(409, 'Fresneda', 1),
(409, 'Gurendes-Quejo', 1),
(409, 'Nograro', 1),
(409, 'Osma', 1),
(409, 'Pinedo', 1),
(409, 'Quintanilla', 1),
(409, 'Tobillas', 1),
(409, 'Tuesta', 1),
(409, 'Valderejo', 1),
(409, 'Valluerca', 1),
(409, 'Villamaderne-Bellojín', 1),
(409, 'Villanañe', 1),
(409, 'Villanueva de Valdegovía', 1);

-- ZAMBRANA (410)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(410, 'Berganzo', 1),
(410, 'Ocio', 1),
(410, 'Portilla/Zabalate', 1),
(410, 'Zambrana', 1);

-- ARRAIA-MAEZTU (501)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(501, 'Apellániz/Apinaiz', 1),
(501, 'Atauri', 1),
(501, 'Azazeta', 1),
(501, 'Korres', 1),
(501, 'Maeztu/Maestu', 1),
(501, 'Onraita/Erroeta', 1),
(501, 'Real Valle de Laminoria/Laminoriako Erret Harana', 1),
(501, 'Róitegui/Erroitegi', 1),
(501, 'Sabando', 1),
(501, 'Vírgala Mayor/Birgara Goien', 1);

-- BERNEDO (502)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(502, 'Angostina', 1),
(502, 'Arluzea', 1),
(502, 'Bernedo', 1),
(502, 'Markinez', 1),
(502, 'Navarrete', 1),
(502, 'Okina', 1),
(502, 'Quintana', 1),
(502, 'San Román de Campezo/Durruma Kanpezu', 1),
(502, 'Urarte', 1),
(502, 'Urturi', 1),
(502, 'Villafría', 1);

-- CAMPEZO (503)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(503, 'Antoñana', 1),
(503, 'Bujanda', 1),
(503, 'Orbiso', 1),
(503, 'Oteo', 1),
(503, 'Santa Cruz de Campezo/Santikurutze Kanpezu', 1);

-- LAGRÁN (504)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(504, 'Lagran', 1),
(504, 'Pipaon', 1),
(504, 'Villaverde', 1);

-- PEÑACERRADA (505)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(505, 'Baroja-Zumentu', 1),
(505, 'Faido/Faidu', 1),
(505, 'Loza', 1),
(505, 'Montoria', 1),
(505, 'Payueta/Pagoeta', 1),
(505, 'Peñacerrada-Urizaharra', 1);

-- HARANA/VALLE DE ARANA (506)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(506, 'Alda', 1),
(506, 'Kontrasta', 1),
(506, 'San Vicente de Arana/Done Bikendi Harana', 1),
(506, 'Ullíbarri-Arana/Uribarri Harana', 1);

-- ZIGOITIA (601)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(601, 'Acosta/Okoizta', 1),
(601, 'Apodaka', 1),
(601, 'Berrikano', 1),
(601, 'Buruaga', 1),
(601, 'Zestafe', 1),
(601, 'Etxaguen', 1),
(601, 'Etxabarri Ibiña', 1),
(601, 'Eribe', 1),
(601, 'Gopegi', 1),
(601, 'Letona', 1),
(601, 'Manurga', 1),
(601, 'Mendarozketa', 1),
(601, 'Murua', 1),
(601, 'Olano', 1),
(601, 'Ondategi', 1),
(601, 'Zaitegi', 1);

-- ZUIA (602)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(602, 'Ametzaga Zuia', 1),
(602, 'Aperregi', 1),
(602, 'Domaikia', 1),
(602, 'Gillerna', 1),
(602, 'Jugo', 1),
(602, 'Lukiano', 1),
(602, 'Markina', 1),
(602, 'Murgia', 1),
(602, 'Sarria', 1),
(602, 'Bitoriano', 1),
(602, 'Zarate', 1);

-- LEGUTIO (603)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(603, 'Elosu', 1),
(603, 'Goiain', 1),
(603, 'Legutio', 1),
(603, 'Urbina', 1),
(603, 'Urrunaga', 1);

-- URKABUSTAIZ (604)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(604, 'Abezia', 1),
(604, 'Abornikano', 1),
(604, 'Beluntza', 1),
(604, 'Goiuri-Ondona', 1),
(604, 'Inoso', 1),
(604, 'Izarra', 1),
(604, 'Larrazkueta', 1),
(604, 'Oiardo', 1),
(604, 'Untza-Apregindana', 1),
(604, 'Uzkiano', 1);

SELECT CONCAT('  ✓ Concejos: ', (SELECT COUNT(*) FROM dim_concejos)) AS resultado;

-- ============================================================================
-- FASE 5: REACTIVAR RESTRICCIONES
-- ============================================================================

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================================
-- FASE 6: VERIFICACIÓN
-- ============================================================================

SELECT '>>> FASE 6: Verificación...' AS paso;

SELECT '--- TOTALES ---' AS seccion;
SELECT
    (SELECT COUNT(*) FROM dim_comarcas) AS comarcas,
    (SELECT COUNT(*) FROM dim_municipios) AS municipios,
    (SELECT COUNT(*) FROM dim_concejos) AS concejos,
    (SELECT COUNT(*) FROM dim_municipios WHERE municipio_nombre LIKE 'Todo %') AS municipios_todo,
    (SELECT COUNT(*) FROM dim_concejos WHERE nombre LIKE 'Todo %') AS concejos_todo;

SELECT '--- Municipios SIN concejos (no debería haber) ---' AS seccion;
SELECT m.id, m.municipio_nombre, 'SIN CONCEJOS!' AS problema
FROM dim_municipios m
LEFT JOIN dim_concejos c ON c.municipio_id = m.id
WHERE c.id IS NULL;

SELECT '=== FIN ===' AS resultado;

-- ============================================================================
-- FASE 7: TABLA DE COMBINACIONES
-- ============================================================================

SELECT '>>> FASE 7: Todas las combinaciones...' AS paso;

SELECT
    c.id AS comarca_id,
    c.comarca_nombre AS comarca,
    m.id AS municipio_id,
    m.municipio_nombre AS municipio,
    co.id AS concejo_id,
    co.nombre AS concejo
FROM dim_comarcas c
LEFT JOIN dim_municipios m ON m.comarca_id = c.id OR (c.id = 1 AND m.id = 1)
LEFT JOIN dim_concejos co ON co.municipio_id = m.id
ORDER BY
    c.id,
    CASE WHEN m.municipio_nombre LIKE 'Todo %' THEN 0 ELSE 1 END,
    m.id,
    CASE WHEN co.nombre LIKE 'Todo %' THEN 0 ELSE 1 END,
    co.id;

SET SQL_SAFE_UPDATES = 1;
