-- ============================================================================
-- RECREAR DIMENSIONES GEOGRÁFICAS - ÁLAVA COMPLETA
-- ============================================================================
-- Fuente: Lista oficial de concejos de Álava (Wikipedia)
--
-- TOTALES ESPERADOS:
--   - dim_comarcas:   7 comarcas + 1 "Todo Álava" = 8 registros
--   - dim_municipios: 51 reales + 14 (Todo/Varios comarca) + 2 (Álava) = 67 registros
--   - dim_concejos:   335 reales + 102 (Todo/Varios municipio) + 14 (comarca) + 4 (Álava) = 455 registros
--
-- CORRECCIONES v1.1:
--   - Añadido Elvillar/Bilar (01023) que faltaba
--   - Corregido código INE de Ribera Alta (01023 → 01046)
--   - Corregido concejos Álava: ahora cada municipio especial tiene Todo+Varios
--
-- USO:
--   mysql -h localhost -P 3307 -u root -p [esquema] < recrear_dimensiones_geograficas.sql
-- ============================================================================

SELECT DATABASE() AS esquema_actual;
SELECT '=== INICIO ===' AS info;
SELECT NOW() AS fecha_ejecucion;

-- ============================================================================
-- FASE 0: PREPARACIÓN
-- ============================================================================

SET SQL_SAFE_UPDATES = 0;
SET FOREIGN_KEY_CHECKS = 0;

UPDATE tbl_partes SET municipio_id = NULL, concejo_id = NULL
WHERE municipio_id IS NOT NULL OR concejo_id IS NOT NULL;

TRUNCATE TABLE dim_concejos;
TRUNCATE TABLE dim_municipios;
TRUNCATE TABLE dim_comarcas;

-- ============================================================================
-- FASE 1: COMARCAS (8 registros)
-- ============================================================================

INSERT INTO dim_comarcas (id, provincia_id, comarca_codigo, comarca_nombre) VALUES
(1, 1, 'TODO', 'Todo Álava'),
(2, 1, 'AIAR', 'Ayala/Aiaraldea'),
(3, 1, 'LLAN', 'Llanada Alavesa'),
(4, 1, 'RIOJ', 'Rioja Alavesa'),
(5, 1, 'AÑAN', 'Añana'),
(6, 1, 'MONT', 'Montaña Alavesa'),
(7, 1, 'GORB', 'Estribaciones del Gorbea'),
(8, 1, 'CANT', 'Cantábrica Alavesa');

-- ============================================================================
-- FASE 2: MUNICIPIOS (67 registros)
-- ============================================================================

-- 2.1 TODO Y VARIOS ÁLAVA (IDs 1-2)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(1, '00001', 'Todo Álava', 1, 1, 1),
(2, '00002', 'Varios Álava', 1, 1, 1);

-- 2.2 TODO Y VARIOS POR COMARCA (IDs 3-16)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(3, '00003', 'Todo Ayala/Aiaraldea', 1, 2, 1),
(4, '00004', 'Varios Ayala/Aiaraldea', 1, 2, 1),
(5, '00005', 'Todo Llanada Alavesa', 1, 3, 1),
(6, '00006', 'Varios Llanada Alavesa', 1, 3, 1),
(7, '00007', 'Todo Rioja Alavesa', 1, 4, 1),
(8, '00008', 'Varios Rioja Alavesa', 1, 4, 1),
(9, '00009', 'Todo Añana', 1, 5, 1),
(10, '00010', 'Varios Añana', 1, 5, 1),
(11, '00011', 'Todo Montaña Alavesa', 1, 6, 1),
(12, '00012', 'Varios Montaña Alavesa', 1, 6, 1),
(13, '00013', 'Todo Estribaciones Gorbea', 1, 7, 1),
(14, '00014', 'Varios Estribaciones Gorbea', 1, 7, 1),
(15, '00015', 'Todo Cantábrica Alavesa', 1, 8, 1),
(16, '00016', 'Varios Cantábrica Alavesa', 1, 8, 1);

-- 2.3 MUNICIPIOS REALES (51 municipios, IDs 101-151)
-- Nota: Elvillar/Bilar tiene ID 151 (añadido en corrección)

-- AYALA/AIARALDEA (comarca_id = 2)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(101, '01002', 'Amurrio', 1, 2, 1),
(102, '01010', 'Ayala/Aiara', 1, 2, 1),
(103, '01003', 'Aramaio', 1, 2, 1),
(104, '01004', 'Artziniega', 1, 2, 1),
(105, '01036', 'Laudio/Llodio', 1, 2, 1),
(106, '01042', 'Okondo', 1, 2, 1);

-- LLANADA ALAVESA (comarca_id = 3)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(107, '01001', 'Alegría-Dulantzi', 1, 3, 1),
(108, '01008', 'Arrazua-Ubarrundia', 1, 3, 1),
(109, '01009', 'Asparrena', 1, 3, 1),
(110, '01013', 'Barrundia', 1, 3, 1),
(111, '01021', 'Elburgo/Burgelu', 1, 3, 1),
(112, '01027', 'Iruraiz-Gauna', 1, 3, 1),
(113, '01053', 'San Millán/Donemiliaga', 1, 3, 1),
(114, '01059', 'Vitoria-Gasteiz', 1, 3, 1),
(115, '01051', 'Agurain/Salvatierra', 1, 3, 1),
(116, '01061', 'Zalduondo', 1, 3, 1);

-- RIOJA ALAVESA (comarca_id = 4)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(117, '01028', 'Labastida/Bastida', 1, 4, 1),
(118, '01031', 'Laguardia', 1, 4, 1),
(119, '01043', 'Oyón-Oion', 1, 4, 1),
(120, '01011', 'Baños de Ebro/Mañueta', 1, 4, 1),
(121, '01019', 'Kripan', 1, 4, 1),
(122, '01022', 'Elciego', 1, 4, 1),
(123, '01032', 'Lanciego/Lantziego', 1, 4, 1),
(124, '01033', 'Lapuebla de Labarca', 1, 4, 1),
(125, '01034', 'Leza', 1, 4, 1),
(126, '01039', 'Moreda de Álava', 1, 4, 1),
(127, '01041', 'Navaridas', 1, 4, 1),
(128, '01052', 'Samaniego', 1, 4, 1),
(129, '01057', 'Villabuena de Álava', 1, 4, 1),
(130, '01060', 'Yécora/Iekora', 1, 4, 1),
(151, '01023', 'Elvillar/Bilar', 1, 4, 1);

-- AÑANA (comarca_id = 5)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(131, '01049', 'Añana', 1, 5, 1),
(132, '01006', 'Armiñón', 1, 5, 1),
(133, '01014', 'Berantevilla', 1, 5, 1),
(134, '01020', 'Kuartango', 1, 5, 1),
(135, '01901', 'Iruña Oka', 1, 5, 1),
(136, '01902', 'Lantarón', 1, 5, 1),
(137, '01046', 'Ribera Alta', 1, 5, 1),
(138, '01047', 'Ribera Baja', 1, 5, 1),
(139, '01055', 'Valdegovía/Gaubea', 1, 5, 1),
(140, '01062', 'Zambrana', 1, 5, 1);

-- MONTAÑA ALAVESA (comarca_id = 6)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(141, '01037', 'Arraia-Maeztu', 1, 6, 1),
(142, '01016', 'Bernedo', 1, 6, 1),
(143, '01017', 'Campezo/Kanpezu', 1, 6, 1),
(144, '01030', 'Lagrán', 1, 6, 1),
(145, '01044', 'Peñacerrada-Urizaharra', 1, 6, 1),
(146, '01056', 'Harana/Valle de Arana', 1, 6, 1);

-- ESTRIBACIONES DEL GORBEA (comarca_id = 7)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(147, '01018', 'Zigoitia', 1, 7, 1),
(148, '01063', 'Zuia', 1, 7, 1),
(149, '01058', 'Legutio', 1, 7, 1),
(150, '01054', 'Urkabustaiz', 1, 7, 1);

-- CANTÁBRICA ALAVESA (comarca_id = 8) - si aplica
-- (Si no hay municipios adicionales, esta comarca solo tiene Todo/Varios)

SELECT CONCAT('Municipios insertados: ', (SELECT COUNT(*) FROM dim_municipios)) AS resultado;

-- ============================================================================
-- FASE 3: CONCEJOS (437 registros)
-- ============================================================================

-- 3.1 TODO Y VARIOS ÁLAVA (IDs 1-4)
-- Cada municipio especial de Álava tiene ambos concejos: Todo y Varios
INSERT INTO dim_concejos (id, municipio_id, nombre, activo) VALUES
(1, 1, 'Todo Álava', 1),
(2, 1, 'Varios Álava', 1),
(3, 2, 'Todo Álava', 1),
(4, 2, 'Varios Álava', 1);

-- 3.2 TODO Y VARIOS POR MUNICIPIO (102 registros)
-- Para los municipios especiales de comarca (IDs 3-16)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(3, 'Todo Ayala/Aiaraldea', 1),
(4, 'Varios Ayala/Aiaraldea', 1),
(5, 'Todo Llanada Alavesa', 1),
(6, 'Varios Llanada Alavesa', 1),
(7, 'Todo Rioja Alavesa', 1),
(8, 'Varios Rioja Alavesa', 1),
(9, 'Todo Añana', 1),
(10, 'Varios Añana', 1),
(11, 'Todo Montaña Alavesa', 1),
(12, 'Varios Montaña Alavesa', 1),
(13, 'Todo Estribaciones Gorbea', 1),
(14, 'Varios Estribaciones Gorbea', 1),
(15, 'Todo Cantábrica Alavesa', 1),
(16, 'Varios Cantábrica Alavesa', 1);

-- Para todos los municipios reales (51 municipios * 2 = 102 registros)
INSERT INTO dim_concejos (municipio_id, nombre, activo)
SELECT id, CONCAT('Todo ', municipio_nombre), 1 FROM dim_municipios WHERE id >= 101;

INSERT INTO dim_concejos (municipio_id, nombre, activo)
SELECT id, CONCAT('Varios ', municipio_nombre), 1 FROM dim_municipios WHERE id >= 101;

-- ============================================================================
-- 3.3 CONCEJOS REALES (335 registros)
-- ============================================================================

-- ALEGRÍA-DULANTZI (107) - 2 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(107, 'Alegría-Dulantzi', 1),
(107, 'Egileta', 1);

-- AMURRIO (101) - 10 concejos
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

-- AÑANA (131) - 1 concejo
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(131, 'Atiega', 1);

-- ARAMAIO (103) - 1 concejo
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(103, 'Oleta', 1);

-- ARMIÑÓN (132) - 2 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(132, 'Armiñón', 1),
(132, 'Estavillo', 1);

-- ARRAIA-MAEZTU (141) - 10 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(141, 'Apellániz/Apinaiz', 1),
(141, 'Atauri', 1),
(141, 'Azazeta', 1),
(141, 'Korres', 1),
(141, 'Maeztu/Maestu', 1),
(141, 'Onraita/Erroeta', 1),
(141, 'Real Valle de Laminoria/Laminoriako Erret Harana', 1),
(141, 'Róitegui/Erroitegi', 1),
(141, 'Sabando', 1),
(141, 'Vírgala Mayor/Birgara Goien', 1);

-- ARRAZUA-UBARRUNDIA (108) - 10 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(108, 'Arroiabe', 1),
(108, 'Arzubiaga', 1),
(108, 'Betolaza', 1),
(108, 'Durana', 1),
(108, 'Landa', 1),
(108, 'Luko', 1),
(108, 'Mendibil', 1),
(108, 'Ullíbarri-Gamboa', 1),
(108, 'Ziriano', 1),
(108, 'Zurbano/Zurbao', 1);

-- ASPARRENA (109) - 9 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(109, 'Albeiz/Albéniz', 1),
(109, 'Ametzaga Asparrena', 1),
(109, 'Andoin', 1),
(109, 'Arriola', 1),
(109, 'Egino', 1),
(109, 'Gordoa', 1),
(109, 'Ibarguren', 1),
(109, 'Ilarduia', 1),
(109, 'Urabain', 1);

-- AYALA/AIARA (102) - 23 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(102, 'Agiñaga', 1),
(102, 'Añes', 1),
(102, 'Arespalditza/Respaldiza', 1),
(102, 'Costera/Opellora', 1),
(102, 'Erbi', 1),
(102, 'Etxegoien', 1),
(102, 'Izoria', 1),
(102, 'Lejarzo/Lexartzu', 1),
(102, 'Llanteno', 1),
(102, 'Luiaondo', 1),
(102, 'Luxo/Lujo', 1),
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

-- BARRUNDIA (110) - 13 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(110, 'Audikana', 1),
(110, 'Dallo', 1),
(110, 'Elgea', 1),
(110, 'Etura', 1),
(110, 'Etxabarri Urtupiña', 1),
(110, 'Gebara', 1),
(110, 'Heredia', 1),
(110, 'Hermua', 1),
(110, 'Larrea', 1),
(110, 'Marieta-Larrintzar', 1),
(110, 'Maturana', 1),
(110, 'Mendixur/Mendíjur', 1),
(110, 'Ozaeta', 1);

-- BERANTEVILLA (133) - 6 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(133, 'Berantevilla', 1),
(133, 'Lacervilla', 1),
(133, 'Mijancas', 1),
(133, 'Santa Cruz del Fierro', 1),
(133, 'Santurde', 1),
(133, 'Tobera', 1);

-- BERNEDO (142) - 11 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(142, 'Angostina', 1),
(142, 'Arluzea', 1),
(142, 'Bernedo', 1),
(142, 'Markinez', 1),
(142, 'Navarrete', 1),
(142, 'Okina', 1),
(142, 'Quintana', 1),
(142, 'San Román de Campezo/Durruma Kanpezu', 1),
(142, 'Urarte', 1),
(142, 'Urturi', 1),
(142, 'Villafría', 1);

-- CAMPEZO (143) - 5 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(143, 'Antoñana', 1),
(143, 'Bujanda', 1),
(143, 'Orbiso', 1),
(143, 'Oteo', 1),
(143, 'Santa Cruz de Campezo/Santikurutze Kanpezu', 1);

-- ZIGOITIA (147) - 16 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(147, 'Acosta/Okoizta', 1),
(147, 'Apodaka', 1),
(147, 'Berrikano', 1),
(147, 'Buruaga', 1),
(147, 'Eribe', 1),
(147, 'Etxabarri Ibiña', 1),
(147, 'Etxaguen', 1),
(147, 'Gopegi', 1),
(147, 'Letona', 1),
(147, 'Manurga', 1),
(147, 'Mendarozketa', 1),
(147, 'Murua', 1),
(147, 'Olano', 1),
(147, 'Ondategi', 1),
(147, 'Zaitegi', 1),
(147, 'Zestafe', 1);

-- KUARTANGO (134) - 10 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(134, 'Anda', 1),
(134, 'Aprikano', 1),
(134, 'Etxabarri Kuartango', 1),
(134, 'Jokano', 1),
(134, 'Luna', 1),
(134, 'Marinda', 1),
(134, 'Sendadiano', 1),
(134, 'Urbina Eza', 1),
(134, 'Uribarri Kuartango', 1),
(134, 'Zuhatzu Kuartango', 1);

-- ELBURGO (111) - 6 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(111, 'Añua', 1),
(111, 'Arbulu', 1),
(111, 'Argomaniz', 1),
(111, 'Elburgo/Burgelu', 1),
(111, 'Gazeta', 1),
(111, 'Hijona/Ixona', 1);

-- IRUÑA OKA (135) - 5 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(135, 'Montevite/Mandaita', 1),
(135, 'Nanclares de la Oca/Langraiz Oka', 1),
(135, 'Ollávarre/Olabarri', 1),
(135, 'Trespuentes', 1),
(135, 'Víllodas/Billoda', 1);

-- IRURAIZ-GAUNA (112) - 11 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(112, 'Alaitza', 1),
(112, 'Arrieta', 1),
(112, 'Azilu', 1),
(112, 'Erentxun', 1),
(112, 'Ezkerekotxa', 1),
(112, 'Gauna', 1),
(112, 'Gazeo', 1),
(112, 'Gereñu', 1),
(112, 'Jauregi', 1),
(112, 'Langarika', 1),
(112, 'Trokoniz', 1);

-- LABASTIDA (117) - 1 concejo
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(117, 'Salinillas de Buradón/Gatzaga Buradon', 1);

-- LAGRÁN (144) - 3 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(144, 'Lagran', 1),
(144, 'Pipaon', 1),
(144, 'Villaverde', 1);

-- LAGUARDIA (118) - 1 concejo
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(118, 'Páganos', 1);

-- ELVILLAR/BILAR (151) - 1 concejo (el propio municipio)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(151, 'Elvillar/Bilar', 1);

-- LANTARÓN (136) - 12 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(136, 'Alcedo', 1),
(136, 'Bergonda/Bergüenda', 1),
(136, 'Caicedo de Yuso', 1),
(136, 'Comunión/Komunioi', 1),
(136, 'Fontecha', 1),
(136, 'Leciñana del Camino/Leziñana', 1),
(136, 'Molinilla', 1),
(136, 'Puentelarrá/Larrazubi', 1),
(136, 'Salcedo', 1),
(136, 'Sobrón', 1),
(136, 'Turiso', 1),
(136, 'Zubillaga', 1);

-- OYÓN-OION (119) - 2 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(119, 'Barriobusto/Gorrebusto', 1),
(119, 'Labraza', 1);

-- PEÑACERRADA (145) - 6 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(145, 'Baroja-Zumentu', 1),
(145, 'Faido/Faidu', 1),
(145, 'Loza', 1),
(145, 'Montoria', 1),
(145, 'Payueta/Pagoeta', 1),
(145, 'Peñacerrada-Urizaharra', 1);

-- RIBERA ALTA (137) - 20 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(137, 'Antezana de la Ribera', 1),
(137, 'Anuntzeta/Anúcita', 1),
(137, 'Arreo', 1),
(137, 'Artaza-Escota/Artatza-Axkoeta', 1),
(137, 'Barrón', 1),
(137, 'Basquiñuelas', 1),
(137, 'Caicedo-Sopeña', 1),
(137, 'Hereña', 1),
(137, 'Lasierra', 1),
(137, 'Leciñana de la Oca', 1),
(137, 'Morillas', 1),
(137, 'Ormijana', 1),
(137, 'Paúl', 1),
(137, 'Pobes', 1),
(137, 'Subijana-Morillas', 1),
(137, 'Tuyo', 1),
(137, 'Villabezana', 1),
(137, 'Villaluenga', 1),
(137, 'Villambrosa', 1),
(137, 'Viloria', 1);

-- RIBERA BAJA (138) - 6 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(138, 'Igay', 1),
(138, 'Manzanos', 1),
(138, 'Melledes', 1),
(138, 'Quintanilla de la Ribera', 1),
(138, 'Rivabellosa', 1),
(138, 'Rivaguda', 1);

-- SAN MILLÁN (113) - 15 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(113, 'Adana', 1),
(113, 'Axpuru', 1),
(113, 'Bikuña/Vicuña', 1),
(113, 'Durruma/San Román de San Millán', 1),
(113, 'Eguílaz/Egilatz', 1),
(113, 'Galarreta', 1),
(113, 'Luzuriaga', 1),
(113, 'Mezkia', 1),
(113, 'Munain', 1),
(113, 'Narbaiza', 1),
(113, 'Okariz', 1),
(113, 'Ordoñana/Erdoñana', 1),
(113, 'Txintxetru', 1),
(113, 'Ullibarri-Jauregi/Uribarri-Jauregi', 1),
(113, 'Zuazo de San Millán/Zuhatzu Donemiliaga', 1);

-- URKABUSTAIZ (150) - 10 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(150, 'Abezia', 1),
(150, 'Abornikano', 1),
(150, 'Beluntza', 1),
(150, 'Goiuri-Ondona', 1),
(150, 'Inoso', 1),
(150, 'Izarra', 1),
(150, 'Larrazkueta', 1),
(150, 'Oiardo', 1),
(150, 'Untza-Apregindana', 1),
(150, 'Uzkiano', 1);

-- VALDEGOVÍA (139) - 22 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(139, 'Acebedo', 1),
(139, 'Bachicabo', 1),
(139, 'Barrio', 1),
(139, 'Basabe', 1),
(139, 'Bóveda', 1),
(139, 'Caranca y Mioma', 1),
(139, 'Corro', 1),
(139, 'Espejo', 1),
(139, 'Fresneda', 1),
(139, 'Gurendes-Quejo', 1),
(139, 'Karkamu', 1),
(139, 'Nograro', 1),
(139, 'Osma', 1),
(139, 'Pinedo', 1),
(139, 'Quintanilla', 1),
(139, 'Tobillas', 1),
(139, 'Tuesta', 1),
(139, 'Valderejo', 1),
(139, 'Valluerca', 1),
(139, 'Villamaderne-Bellojín', 1),
(139, 'Villanañe', 1),
(139, 'Villanueva de Valdegovía', 1);

-- HARANA/VALLE DE ARANA (146) - 4 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(146, 'Alda', 1),
(146, 'Kontrasta', 1),
(146, 'San Vicente de Arana/Done Bikendi Harana', 1),
(146, 'Ullíbarri-Arana/Uribarri Harana', 1);

-- LEGUTIO/VILLARREAL DE ÁLAVA (149) - 5 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(149, 'Elosu', 1),
(149, 'Goiain', 1),
(149, 'Legutio', 1),
(149, 'Urbina', 1),
(149, 'Urrunaga', 1);

-- VITORIA-GASTEIZ (114) - 63 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(114, 'Aberasturi', 1),
(114, 'Abetxuko', 1),
(114, 'Amarita', 1),
(114, 'Andollu', 1),
(114, 'Antezana/Andetxa', 1),
(114, 'Arangiz', 1),
(114, 'Aretxabaleta', 1),
(114, 'Argandoña', 1),
(114, 'Ariñiz/Aríñez', 1),
(114, 'Arkaia', 1),
(114, 'Arkauti/Arcaute', 1),
(114, 'Armentia', 1),
(114, 'Askartza', 1),
(114, 'Astegieta', 1),
(114, 'Berrostegieta', 1),
(114, 'Betoño', 1),
(114, 'Bolívar', 1),
(114, 'Castillo/Gaztelu', 1),
(114, 'Ehari/Ali', 1),
(114, 'Elorriaga', 1),
(114, 'Eskibel', 1),
(114, 'Estarrona', 1),
(114, 'Foronda', 1),
(114, 'Gamarra Mayor/Gamarra Nagusia', 1),
(114, 'Gamarra Menor', 1),
(114, 'Gamiz', 1),
(114, 'Gardelegi', 1),
(114, 'Gereña', 1),
(114, 'Gobeo', 1),
(114, 'Gometxa', 1),
(114, 'Hueto Abajo/Otobarren', 1),
(114, 'Ilarratza', 1),
(114, 'Jungitu', 1),
(114, 'Krispiña/Crispijana', 1),
(114, 'Lasarte', 1),
(114, 'Legarda', 1),
(114, 'Lermanda', 1),
(114, 'Lopidana', 1),
(114, 'Lubiano', 1),
(114, 'Margarita', 1),
(114, 'Martioda', 1),
(114, 'Matauko', 1),
(114, 'Mendiguren', 1),
(114, 'Mendiola', 1),
(114, 'Mendoza', 1),
(114, 'Miñano Menor/Miñano Gutxia', 1),
(114, 'Miñao/Miñano Mayor', 1),
(114, 'Monasterioguren', 1),
(114, 'Oreitia', 1),
(114, 'Otazu', 1),
(114, 'Otogoien/Hueto Arriba', 1),
(114, 'Retana', 1),
(114, 'Subijana de Álava/Subillana-Gasteiz', 1),
(114, 'Ullíbarri de los Olleros/Uribarri Nagusia', 1),
(114, 'Ullíbarri-Arrazua', 1),
(114, 'Ullíbarri-Viña/Uribarri-Dibiña', 1),
(114, 'Villafranca', 1),
(114, 'Yurre/Ihurre', 1),
(114, 'Zerio', 1),
(114, 'Zuazo de Vitoria/Zuhatzu', 1),
(114, 'Zumeltzu', 1);

-- ZAMBRANA (140) - 4 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(140, 'Berganzo', 1),
(140, 'Ocio', 1),
(140, 'Portilla/Zabalate', 1),
(140, 'Zambrana', 1);

-- ZUIA (148) - 11 concejos
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(148, 'Ametzaga Zuia', 1),
(148, 'Aperregi', 1),
(148, 'Bitoriano', 1),
(148, 'Domaikia', 1),
(148, 'Gillerna', 1),
(148, 'Jugo', 1),
(148, 'Lukiano', 1),
(148, 'Markina', 1),
(148, 'Murgia', 1),
(148, 'Sarria', 1),
(148, 'Zarate', 1);

-- ============================================================================
-- FASE 4: REACTIVAR RESTRICCIONES
-- ============================================================================

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================================
-- FASE 5: VERIFICACIÓN
-- ============================================================================

SELECT '=== VERIFICACIÓN ===' AS seccion;

SELECT
    (SELECT COUNT(*) FROM dim_comarcas) AS comarcas,
    (SELECT COUNT(*) FROM dim_municipios) AS municipios,
    (SELECT COUNT(*) FROM dim_concejos) AS concejos;

SELECT '--- Municipios sin concejos (no debería haber) ---' AS seccion;
SELECT m.id, m.municipio_nombre
FROM dim_municipios m
LEFT JOIN dim_concejos c ON c.municipio_id = m.id
WHERE c.id IS NULL;

SELECT '--- Conteo de concejos por tipo ---' AS seccion;
SELECT
    SUM(CASE WHEN nombre LIKE 'Todo %' THEN 1 ELSE 0 END) AS concejos_todo,
    SUM(CASE WHEN nombre LIKE 'Varios %' THEN 1 ELSE 0 END) AS concejos_varios,
    SUM(CASE WHEN nombre NOT LIKE 'Todo %' AND nombre NOT LIKE 'Varios %' THEN 1 ELSE 0 END) AS concejos_reales
FROM dim_concejos;

SELECT '=== FIN ===' AS resultado;

-- ============================================================================
-- FASE 6: TODAS LAS COMBINACIONES
-- ============================================================================

SELECT
    c.id AS comarca_id,
    c.comarca_nombre AS comarca,
    m.id AS municipio_id,
    m.municipio_nombre AS municipio,
    co.id AS concejo_id,
    co.nombre AS concejo
FROM dim_comarcas c
LEFT JOIN dim_municipios m ON m.comarca_id = c.id
LEFT JOIN dim_concejos co ON co.municipio_id = m.id
ORDER BY c.id, m.id, co.id;

SET SQL_SAFE_UPDATES = 1;
