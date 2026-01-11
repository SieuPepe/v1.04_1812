-- ============================================================================
-- RECREAR DIMENSIONES GEOGRÁFICAS - VERSIÓN CORREGIDA
-- ============================================================================
-- Este script ELIMINA y RECREA todas las tablas de dimensiones geográficas
-- con la estructura correcta para dropdowns en cascada.
--
-- JERARQUÍA: Provincia → Comarca → Municipio → Concejo
--
-- REGLA FUNDAMENTAL:
--   - CADA nivel tiene opción "Todo {nombre}" para seleccionar toda la zona
--   - NINGÚN dropdown debe quedar vacío
--   - Si un municipio no tiene concejos reales, tendrá "Todo {Municipio}"
--
-- USO:
--   mysql -h localhost -P 3307 -u root -p [esquema] < recrear_dimensiones_geograficas.sql
-- ============================================================================

-- Mostrar esquema actual
SELECT DATABASE() AS esquema_actual;
SELECT '=== INICIO: Recrear dimensiones geográficas ===' AS info;
SELECT NOW() AS fecha_ejecucion;

-- ============================================================================
-- FASE 0: DESACTIVAR FK Y MODO SEGURO, LIMPIAR REFERENCIAS
-- ============================================================================

SELECT '>>> FASE 0: Desactivando FK, modo seguro y limpiando referencias...' AS paso;

-- Desactivar modo seguro de MySQL Workbench
SET SQL_SAFE_UPDATES = 0;
SET FOREIGN_KEY_CHECKS = 0;

-- Limpiar TODAS las referencias geográficas en tablas de hechos
UPDATE tbl_partes SET municipio_id = NULL, concejo_id = NULL WHERE municipio_id IS NOT NULL OR concejo_id IS NOT NULL;
SELECT CONCAT('  ✓ tbl_partes: ', ROW_COUNT(), ' registros limpiados') AS resultado;

-- Si hay otras tablas con FK a estas dimensiones, limpiarlas aquí también
-- UPDATE tbl_certificaciones SET municipio_id = NULL WHERE municipio_id IS NOT NULL;

-- ============================================================================
-- FASE 1: VACIAR TABLAS DE DIMENSIONES
-- ============================================================================

SELECT '>>> FASE 1: Vaciando tablas de dimensiones...' AS paso;

-- Eliminar en orden de dependencia
TRUNCATE TABLE dim_concejos;
SELECT '  ✓ dim_concejos vaciada' AS resultado;

TRUNCATE TABLE dim_municipios;
SELECT '  ✓ dim_municipios vaciada' AS resultado;

TRUNCATE TABLE dim_comarcas;
SELECT '  ✓ dim_comarcas vaciada' AS resultado;

-- ============================================================================
-- FASE 2: CREAR COMARCAS
-- ============================================================================
-- Estructura:
--   ID 1 = "Todo Álava" (representa TODAS las comarcas)
--   IDs 2-7 = Comarcas reales (Cuadrillas de Álava)
-- ============================================================================

SELECT '>>> FASE 2: Creando comarcas...' AS paso;

INSERT INTO dim_comarcas (id, provincia_id, comarca_codigo, comarca_nombre) VALUES
-- Opción para seleccionar TODA la provincia
(1, 1, 'TODO', 'Todo Álava'),
-- Comarcas reales
(2, 1, 'AIAR', 'Ayala / Aiaraldea'),
(3, 1, 'LLAN', 'Llanada Alavesa'),
(4, 1, 'RIOJ', 'Rioja Alavesa'),
(5, 1, 'AÑAN', 'Añana'),
(6, 1, 'MONT', 'Montaña Alavesa'),
(7, 1, 'GORB', 'Estribaciones del Gorbea');

SELECT CONCAT('  ✓ Comarcas creadas: ', ROW_COUNT()) AS resultado;

-- ============================================================================
-- FASE 3: CREAR MUNICIPIOS
-- ============================================================================
-- Estructura de IDs:
--   ID 1 = "Todo Álava" (para comarca "Todo Álava")
--   IDs 2-7 = "Todo {Comarca}" (uno por cada comarca real)
--   IDs 1001+ = Municipios reales
-- ============================================================================

SELECT '>>> FASE 3: Creando municipios...' AS paso;

-- -----------------------------------------------------------------------------
-- 3.1 MUNICIPIOS "TODO" (para seleccionar todos los municipios de una zona)
-- -----------------------------------------------------------------------------

INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
-- Para comarca "Todo Álava" → solo puede elegir "Todo Álava" como municipio
(1, '00000', 'Todo Álava', 1, 1, 1),
-- Para cada comarca real → puede elegir "Todo {Comarca}" + municipios reales
(2, '00000', 'Todo Aiaraldea', 1, 2, 1),
(3, '00000', 'Todo Llanada Alavesa', 1, 3, 1),
(4, '00000', 'Todo Rioja Alavesa', 1, 4, 1),
(5, '00000', 'Todo Añana', 1, 5, 1),
(6, '00000', 'Todo Montaña Alavesa', 1, 6, 1),
(7, '00000', 'Todo Estribaciones Gorbea', 1, 7, 1);

-- -----------------------------------------------------------------------------
-- 3.2 MUNICIPIOS REALES
-- -----------------------------------------------------------------------------

-- Comarca: Ayala / Aiaraldea (comarca_id = 2)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(1001, '01002', 'Amurrio', 1, 2, 1),
(1002, '01010', 'Ayala/Aiara', 1, 2, 1),
(1003, '01004', 'Artziniega', 1, 2, 1),
(1004, '01036', 'Laudio/Llodio', 1, 2, 1),
(1005, '01042', 'Okondo', 1, 2, 1),
(1006, '01003', 'Aramaio', 1, 2, 1);

-- Comarca: Llanada Alavesa (comarca_id = 3)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(1010, '01059', 'Vitoria-Gasteiz', 1, 3, 1),
(1011, '01001', 'Alegría-Dulantzi', 1, 3, 1),
(1012, '01051', 'Agurain/Salvatierra', 1, 3, 1),
(1013, '01008', 'Arratzua-Ubarrundia', 1, 3, 1),
(1014, '01009', 'Asparrena', 1, 3, 1),
(1015, '01013', 'Barrundia', 1, 3, 1),
(1016, '01021', 'Elburgo/Burgelu', 1, 3, 1),
(1017, '01027', 'Iruraiz-Gauna', 1, 3, 1),
(1018, '01053', 'San Millán/Donemiliaga', 1, 3, 1),
(1019, '01061', 'Zalduondo', 1, 3, 1),
(1020, '01018', 'Zigoitia', 1, 3, 1),
(1021, '01063', 'Zuia', 1, 3, 1),
(1022, '01058', 'Legutio', 1, 3, 1),
(1023, '01054', 'Urkabustaiz', 1, 3, 1);

-- Comarca: Rioja Alavesa (comarca_id = 4)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(1030, '01011', 'Baños de Ebro/Mañueta', 1, 4, 1),
(1031, '01019', 'Kripan', 1, 4, 1),
(1032, '01022', 'Elciego', 1, 4, 1),
(1033, '01028', 'Labastida/Bastida', 1, 4, 1),
(1034, '01031', 'Laguardia', 1, 4, 1),
(1035, '01032', 'Lanciego/Lantziego', 1, 4, 1),
(1036, '01033', 'Lapuebla de Labarca', 1, 4, 1),
(1037, '01034', 'Leza', 1, 4, 1),
(1038, '01039', 'Moreda de Álava/Moreda Araba', 1, 4, 1),
(1039, '01041', 'Navaridas', 1, 4, 1),
(1040, '01043', 'Oyón-Oion', 1, 4, 1),
(1041, '01052', 'Samaniego', 1, 4, 1),
(1042, '01057', 'Villabuena de Álava/Eskuernaga', 1, 4, 1),
(1043, '01060', 'Yécora/Iekora', 1, 4, 1);

-- Comarca: Añana (comarca_id = 5)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(1050, '01049', 'Añana', 1, 5, 1),
(1051, '01006', 'Armiñón', 1, 5, 1),
(1052, '01014', 'Berantevilla', 1, 5, 1),
(1053, '01020', 'Kuartango', 1, 5, 1),
(1054, '01901', 'Iruña Oka/Iruña de Oca', 1, 5, 1),
(1055, '01902', 'Lantarón', 1, 5, 1),
(1056, '01023', 'Erriberagoitia/Ribera Alta', 1, 5, 1),
(1057, '01047', 'Ribera Baja/Erribera Beitia', 1, 5, 1),
(1058, '01055', 'Valdegovía/Gaubea', 1, 5, 1),
(1059, '01062', 'Zambrana', 1, 5, 1);

-- Comarca: Montaña Alavesa (comarca_id = 6)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(1060, '01037', 'Arraia-Maeztu', 1, 6, 1),
(1061, '01016', 'Bernedo', 1, 6, 1),
(1062, '01017', 'Campezo/Kanpezu', 1, 6, 1),
(1063, '01030', 'Lagrán', 1, 6, 1),
(1064, '01044', 'Peñacerrada-Urizaharra', 1, 6, 1),
(1065, '01056', 'Harana/Valle de Arana', 1, 6, 1);

-- Comarca: Estribaciones del Gorbea (comarca_id = 7)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(1070, '01018', 'Zigoitia', 1, 7, 1),
(1071, '01063', 'Zuia', 1, 7, 1),
(1072, '01058', 'Legutio', 1, 7, 1),
(1073, '01054', 'Urkabustaiz', 1, 7, 1);

SELECT CONCAT('  ✓ Municipios creados: ', (SELECT COUNT(*) FROM dim_municipios)) AS resultado;

-- ============================================================================
-- FASE 4: CREAR CONCEJOS
-- ============================================================================
-- REGLA: CADA municipio DEBE tener al menos un concejo "Todo {Municipio}"
-- ============================================================================

SELECT '>>> FASE 4: Creando concejos...' AS paso;

-- -----------------------------------------------------------------------------
-- 4.1 CONCEJOS "TODO" - Uno por CADA municipio (incluyendo los "Todo X")
-- -----------------------------------------------------------------------------

-- Concejos "Todo" para municipios especiales (IDs 1-7)
INSERT INTO dim_concejos (id, municipio_id, nombre, activo) VALUES
(1, 1, 'Todo Álava', 1),
(2, 2, 'Todo Aiaraldea', 1),
(3, 3, 'Todo Llanada Alavesa', 1),
(4, 4, 'Todo Rioja Alavesa', 1),
(5, 5, 'Todo Añana', 1),
(6, 6, 'Todo Montaña Alavesa', 1),
(7, 7, 'Todo Estribaciones Gorbea', 1);

-- Concejos "Todo" para TODOS los municipios reales
-- Usamos IDs que coinciden con el municipio_id para facilitar la relación
INSERT INTO dim_concejos (id, municipio_id, nombre, activo)
SELECT
    m.id AS id,  -- mismo ID que el municipio
    m.id AS municipio_id,
    CONCAT('Todo ', m.municipio_nombre) AS nombre,
    1 AS activo
FROM dim_municipios m
WHERE m.id >= 1001;

SELECT CONCAT('  ✓ Concejos "Todo" creados: ', (SELECT COUNT(*) FROM dim_concejos)) AS resultado;

-- -----------------------------------------------------------------------------
-- 4.2 CONCEJOS REALES (IDs 10000+)
-- -----------------------------------------------------------------------------

-- Amurrio (municipio_id = 1001)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1001, 'Aloria', 1),
(1001, 'Amurrio', 1),
(1001, 'Artomaña', 1),
(1001, 'Baranbio', 1),
(1001, 'Delika', 1),
(1001, 'Larrinbe', 1),
(1001, 'Lekamaña', 1),
(1001, 'Lezama', 1),
(1001, 'Saratxo', 1),
(1001, 'Tertanga', 1);

-- Ayala/Aiara (municipio_id = 1002)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1002, 'Agiñaga', 1),
(1002, 'Añes', 1),
(1002, 'Arespalditza/Respaldiza', 1),
(1002, 'Costera/Opellora', 1),
(1002, 'Erbi', 1),
(1002, 'Etxegoien', 1),
(1002, 'Izoria', 1),
(1002, 'Lejarzo/Lexartzu', 1),
(1002, 'Llanteno', 1),
(1002, 'Luxo/Lujo', 1),
(1002, 'Luiaondo', 1),
(1002, 'Madaria', 1),
(1002, 'Maroño', 1),
(1002, 'Menagarai-Beotegi', 1),
(1002, 'Menoio', 1),
(1002, 'Murga', 1),
(1002, 'Olabezar', 1),
(1002, 'Ozeka', 1),
(1002, 'Quejana/Kexaa', 1),
(1002, 'Retes de Llanteno', 1),
(1002, 'Salmantón', 1),
(1002, 'Soxo/Sojo', 1),
(1002, 'Zuaza/Zuhatza', 1);

-- Artziniega (municipio_id = 1003)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1003, 'Artziniega', 1);

-- Laudio/Llodio (municipio_id = 1004)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1004, 'Laudio/Llodio', 1);

-- Okondo (municipio_id = 1005)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1005, 'Okondo', 1);

-- Aramaio (municipio_id = 1006)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1006, 'Aramaio', 1),
(1006, 'Arexola', 1),
(1006, 'Azkoaga', 1),
(1006, 'Barajuen', 1),
(1006, 'Etura', 1),
(1006, 'Gantzaga', 1),
(1006, 'Ibarra', 1),
(1006, 'Olaeta', 1),
(1006, 'Uribarri', 1),
(1006, 'Untzilla', 1);

-- Vitoria-Gasteiz (municipio_id = 1010)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1010, 'Vitoria-Gasteiz', 1);

-- Alegría-Dulantzi (municipio_id = 1011)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1011, 'Alegría-Dulantzi', 1);

-- Agurain/Salvatierra (municipio_id = 1012)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1012, 'Agurain/Salvatierra', 1);

-- Arratzua-Ubarrundia (municipio_id = 1013)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1013, 'Arzubiaga', 1),
(1013, 'Betolaza', 1),
(1013, 'Durana', 1),
(1013, 'Elosu', 1),
(1013, 'Garayo/Garaio', 1),
(1013, 'Gopegi', 1),
(1013, 'Luko', 1),
(1013, 'Marieta', 1),
(1013, 'Mendixur', 1),
(1013, 'Ullibarri-Ganboa', 1);

-- Asparrena (municipio_id = 1014)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1014, 'Albeniz', 1),
(1014, 'Ametzaga', 1),
(1014, 'Andoin', 1),
(1014, 'Araia', 1),
(1014, 'Arriola', 1),
(1014, 'Egino', 1),
(1014, 'Gordoa', 1),
(1014, 'Ilarduia', 1),
(1014, 'Luzuriaga', 1),
(1014, 'Narvaja', 1),
(1014, 'Okariz', 1),
(1014, 'San Vicente de Arana', 1),
(1014, 'Urabain', 1);

-- Barrundia (municipio_id = 1015)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1015, 'Audikana', 1),
(1015, 'Dallo', 1),
(1015, 'Etura', 1),
(1015, 'Gebara', 1),
(1015, 'Hermua', 1),
(1015, 'Larrea', 1),
(1015, 'Maturana', 1),
(1015, 'Ozaeta', 1);

-- Elburgo/Burgelu (municipio_id = 1016)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1016, 'Añua', 1),
(1016, 'Arbulu', 1),
(1016, 'Argomaniz', 1),
(1016, 'Elburgo/Burgelu', 1),
(1016, 'Gazeta', 1),
(1016, 'Hijona/Ixona', 1);

-- Iruraiz-Gauna (municipio_id = 1017)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1017, 'Alaitza', 1),
(1017, 'Arrieta', 1),
(1017, 'Azilu', 1),
(1017, 'Erentxun', 1),
(1017, 'Ezkerekotxa', 1),
(1017, 'Gazeo', 1),
(1017, 'Gauna', 1),
(1017, 'Gereñu', 1),
(1017, 'Jauregi', 1),
(1017, 'Langarika', 1),
(1017, 'Trokoniz', 1);

-- San Millán/Donemiliaga (municipio_id = 1018)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1018, 'Adana', 1),
(1018, 'Aspuru', 1),
(1018, 'Chinchetru', 1),
(1018, 'Eguilaz', 1),
(1018, 'Galarreta', 1),
(1018, 'Mezquía', 1),
(1018, 'Munain', 1),
(1018, 'Narbaiza', 1),
(1018, 'Ordoñana', 1);

-- Zalduondo (municipio_id = 1019)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1019, 'Zalduondo', 1);

-- Zigoitia (municipio_id = 1020) - este está en Llanada Alavesa
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1020, 'Acosta', 1),
(1020, 'Berrikano', 1),
(1020, 'Buruaga', 1),
(1020, 'Eribe', 1),
(1020, 'Etxabarri-Ibiña', 1),
(1020, 'Gopegui', 1),
(1020, 'Larrinoa', 1),
(1020, 'Letona', 1),
(1020, 'Manurga', 1),
(1020, 'Murua', 1),
(1020, 'Olano', 1),
(1020, 'Ondategi', 1),
(1020, 'Zaitegi', 1);

-- Zuia (municipio_id = 1021)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1021, 'Altube', 1),
(1021, 'Ametzaga de Zuia', 1),
(1021, 'Aperregi', 1),
(1021, 'Domaikia', 1),
(1021, 'Guillerna', 1),
(1021, 'Jugo', 1),
(1021, 'Lukiano', 1),
(1021, 'Markina de Zuia', 1),
(1021, 'Murgia', 1),
(1021, 'Sarria', 1),
(1021, 'Vitoriano', 1),
(1021, 'Zarate', 1);

-- Legutio (municipio_id = 1022)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1022, 'Elosu', 1),
(1022, 'Legutio/Villarreal de Álava', 1),
(1022, 'Nafarrate', 1),
(1022, 'Urbina', 1),
(1022, 'Urrunaga', 1);

-- Urkabustaiz (municipio_id = 1023)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1023, 'Abecia', 1),
(1023, 'Abornikano', 1),
(1023, 'Belunza', 1),
(1023, 'Goiuri-Ondona', 1),
(1023, 'Izarra', 1),
(1023, 'Oiardo', 1),
(1023, 'Unzá', 1);

-- Rioja Alavesa - Municipios con concejos simples (un solo núcleo)
-- Baños de Ebro (1030), Kripan (1031), Elciego (1032), etc.
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1030, 'Baños de Ebro/Mañueta', 1),
(1031, 'Kripan', 1),
(1032, 'Elciego', 1),
(1033, 'Labastida/Bastida', 1),
(1034, 'Laguardia', 1),
(1035, 'Lanciego/Lantziego', 1),
(1036, 'Lapuebla de Labarca', 1),
(1037, 'Leza', 1),
(1038, 'Moreda de Álava', 1),
(1039, 'Navaridas', 1),
(1040, 'Oyón-Oion', 1),
(1041, 'Samaniego', 1),
(1042, 'Villabuena de Álava', 1),
(1043, 'Yécora/Iekora', 1);

-- Comarca Añana - Municipios
-- Añana (1050)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1050, 'Salinas de Añana', 1);

-- Armiñón (1051)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1051, 'Armiñón', 1),
(1051, 'Estavillo', 1);

-- Berantevilla (1052)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1052, 'Berantevilla', 1),
(1052, 'Lacervilla', 1),
(1052, 'Mijancas', 1),
(1052, 'Santa Cruz del Fierro', 1),
(1052, 'Santurde', 1),
(1052, 'Tobera', 1);

-- Kuartango (1053)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1053, 'Anda', 1),
(1053, 'Andagoia', 1),
(1053, 'Apodaka', 1),
(1053, 'Archua', 1),
(1053, 'Catadiano', 1),
(1053, 'Guinea', 1),
(1053, 'Jócano', 1),
(1053, 'Luna', 1),
(1053, 'Marinda', 1),
(1053, 'Sendadiano', 1),
(1053, 'Tortura', 1),
(1053, 'Urbina de Eza', 1),
(1053, 'Zuazo de Cuartango', 1);

-- Iruña Oka (1054)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1054, 'Iruña Oka', 1),
(1054, 'Nanclares de Oca/Langara', 1),
(1054, 'Ollávarre/Olabarri', 1),
(1054, 'Trespuentes', 1),
(1054, 'Víllodas', 1);

-- Lantarón (1055)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1055, 'Alcedo', 1),
(1055, 'Bergüenda', 1),
(1055, 'Caicedo de Yuso', 1),
(1055, 'Comunión', 1),
(1055, 'Fontecha', 1),
(1055, 'Leciñana del Camino', 1),
(1055, 'Molinilla', 1),
(1055, 'Puentelarrá', 1),
(1055, 'Salcedo', 1),
(1055, 'Sobrón', 1),
(1055, 'Turiso', 1),
(1055, 'Zubillaga', 1);

-- Ribera Alta (1056)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1056, 'Antezana de la Ribera', 1),
(1056, 'Anuntzeta/Anúcita', 1),
(1056, 'Arreo', 1),
(1056, 'Artaza-Escota', 1),
(1056, 'Barrón', 1),
(1056, 'Basquiñuelas', 1),
(1056, 'Caicedo-Sopeña', 1),
(1056, 'Hereña', 1),
(1056, 'Lasierra', 1),
(1056, 'Leciñana de la Oca', 1),
(1056, 'Morillas', 1),
(1056, 'Ormijana', 1),
(1056, 'Paúl', 1),
(1056, 'Pobes', 1),
(1056, 'Subijana-Morillas', 1),
(1056, 'Tuyo', 1),
(1056, 'Villabezana', 1),
(1056, 'Villaluenga', 1),
(1056, 'Villambrosa', 1),
(1056, 'Viloria', 1);

-- Ribera Baja (1057)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1057, 'Igay', 1),
(1057, 'Manzanos', 1),
(1057, 'Melledes', 1),
(1057, 'Quintanilla de la Ribera', 1),
(1057, 'Rivabellosa', 1);

-- Valdegovía/Gaubea (1058)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1058, 'Acebedo', 1),
(1058, 'Bachicabo', 1),
(1058, 'Barrio', 1),
(1058, 'Basabe', 1),
(1058, 'Bóveda', 1),
(1058, 'Caranca y Mioma', 1),
(1058, 'Karkamu', 1),
(1058, 'Corro', 1),
(1058, 'Espejo', 1),
(1058, 'Fresneda', 1),
(1058, 'Gurendes-Quejo', 1),
(1058, 'Nograro', 1),
(1058, 'Osma', 1),
(1058, 'Pinedo', 1),
(1058, 'Quintanilla', 1),
(1058, 'Tobillas', 1),
(1058, 'Tuesta', 1),
(1058, 'Valderejo', 1),
(1058, 'Valluerca', 1),
(1058, 'Villamaderne-Bellojín', 1),
(1058, 'Villanañe', 1),
(1058, 'Villanueva de Valdegovía', 1);

-- Zambrana (1059)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1059, 'Berganzo', 1),
(1059, 'Ocio', 1),
(1059, 'Portilla/Zabalate', 1),
(1059, 'Zambrana', 1);

-- Montaña Alavesa
-- Arraia-Maeztu (1060)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1060, 'Apellániz/Apinaiz', 1),
(1060, 'Atauri', 1),
(1060, 'Azazeta', 1),
(1060, 'Korres', 1),
(1060, 'Maeztu/Maestu', 1),
(1060, 'Onraita/Erroeta', 1),
(1060, 'Róitegui/Erroitegi', 1),
(1060, 'Sabando', 1),
(1060, 'Vírgala Mayor/Birgara Goien', 1);

-- Bernedo (1061)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1061, 'Angostina', 1),
(1061, 'Arluzea', 1),
(1061, 'Bernedo', 1),
(1061, 'Markinez', 1),
(1061, 'Navarrete', 1),
(1061, 'Okina', 1),
(1061, 'Quintana', 1),
(1061, 'San Román de Campezo', 1),
(1061, 'Urarte', 1),
(1061, 'Urturi', 1),
(1061, 'Villafría', 1);

-- Campezo/Kanpezu (1062)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1062, 'Antoñana', 1),
(1062, 'Bujanda', 1),
(1062, 'Orbiso', 1),
(1062, 'Oteo', 1),
(1062, 'Santa Cruz de Campezo', 1);

-- Lagrán (1063)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1063, 'Lagrán', 1),
(1063, 'Pipaón', 1),
(1063, 'Villaverde', 1);

-- Peñacerrada-Urizaharra (1064)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1064, 'Baroja', 1),
(1064, 'Faido', 1),
(1064, 'Loza', 1),
(1064, 'Montoria', 1),
(1064, 'Payueta', 1),
(1064, 'Peñacerrada-Urizaharra', 1);

-- Harana/Valle de Arana (1065)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1065, 'Alda', 1),
(1065, 'Arenaza', 1),
(1065, 'Kontrasta', 1),
(1065, 'San Vicente de Arana', 1),
(1065, 'Ullibarri Arana', 1);

-- Estribaciones del Gorbea
-- Zigoitia (1070)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1070, 'Acosta', 1),
(1070, 'Berrikano', 1),
(1070, 'Buruaga', 1),
(1070, 'Eribe', 1),
(1070, 'Etxabarri-Ibiña', 1),
(1070, 'Gopegui', 1),
(1070, 'Larrinoa', 1),
(1070, 'Letona', 1),
(1070, 'Manurga', 1),
(1070, 'Murua', 1),
(1070, 'Olano', 1),
(1070, 'Ondategi', 1),
(1070, 'Zaitegi', 1);

-- Zuia (1071)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1071, 'Altube', 1),
(1071, 'Ametzaga de Zuia', 1),
(1071, 'Aperregi', 1),
(1071, 'Domaikia', 1),
(1071, 'Guillerna', 1),
(1071, 'Jugo', 1),
(1071, 'Lukiano', 1),
(1071, 'Markina de Zuia', 1),
(1071, 'Murgia', 1),
(1071, 'Sarria', 1),
(1071, 'Vitoriano', 1),
(1071, 'Zarate', 1);

-- Legutio (1072)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1072, 'Elosu', 1),
(1072, 'Legutio/Villarreal de Álava', 1),
(1072, 'Nafarrate', 1),
(1072, 'Urbina', 1),
(1072, 'Urrunaga', 1);

-- Urkabustaiz (1073)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1073, 'Abecia', 1),
(1073, 'Abornikano', 1),
(1073, 'Belunza', 1),
(1073, 'Goiuri-Ondona', 1),
(1073, 'Izarra', 1),
(1073, 'Oiardo', 1),
(1073, 'Unzá', 1);

SELECT CONCAT('  ✓ Concejos creados (total): ', (SELECT COUNT(*) FROM dim_concejos)) AS resultado;

-- ============================================================================
-- FASE 5: REACTIVAR FK
-- ============================================================================

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================================
-- FASE 6: VERIFICACIÓN FINAL
-- ============================================================================

SELECT '>>> FASE 6: Verificación final...' AS paso;

SELECT '--- COMARCAS ---' AS seccion;
SELECT id, comarca_nombre FROM dim_comarcas ORDER BY id;

SELECT '--- MUNICIPIOS "Todo" ---' AS seccion;
SELECT id, municipio_nombre, comarca_id FROM dim_municipios WHERE id <= 7 ORDER BY id;

SELECT '--- MUNICIPIOS por comarca (muestra) ---' AS seccion;
SELECT id, municipio_nombre, comarca_id FROM dim_municipios WHERE id >= 1001 ORDER BY comarca_id, id LIMIT 20;

SELECT '--- CONCEJOS "Todo" ---' AS seccion;
SELECT id, nombre, municipio_id FROM dim_concejos WHERE nombre LIKE 'Todo %' ORDER BY id LIMIT 15;

SELECT '--- VERIFICAR: Municipios SIN concejos (NO debe haber ninguno) ---' AS seccion;
SELECT m.id, m.municipio_nombre, 'SIN CONCEJOS!' AS problema
FROM dim_municipios m
LEFT JOIN dim_concejos c ON c.municipio_id = m.id
WHERE c.id IS NULL;

SELECT '--- TOTALES ---' AS seccion;
SELECT
    (SELECT COUNT(*) FROM dim_comarcas) AS total_comarcas,
    (SELECT COUNT(*) FROM dim_municipios) AS total_municipios,
    (SELECT COUNT(*) FROM dim_concejos) AS total_concejos,
    (SELECT COUNT(*) FROM dim_municipios WHERE municipio_nombre LIKE 'Todo %') AS municipios_todo,
    (SELECT COUNT(*) FROM dim_concejos WHERE nombre LIKE 'Todo %') AS concejos_todo;

SELECT '=== FIN: Dimensiones geográficas recreadas ===' AS resultado;

-- ============================================================================
-- FASE 7: TABLA DE TODAS LAS COMBINACIONES PARA REVISIÓN
-- ============================================================================

SELECT '>>> FASE 7: Mostrando todas las combinaciones posibles...' AS paso;

SELECT '--- TODAS LAS COMBINACIONES: Comarca → Municipio → Concejo ---' AS seccion;

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

-- Restaurar modo seguro
SET SQL_SAFE_UPDATES = 1;

-- ============================================================================
-- LÓGICA PARA DROPDOWNS EN LA APLICACIÓN
-- ============================================================================
--
-- 1. CARGAR COMARCAS:
--    SELECT id, comarca_nombre FROM dim_comarcas
--    WHERE provincia_id = 1 ORDER BY id
--    → Muestra: "Todo Álava" + comarcas reales
--
-- 2. CARGAR MUNICIPIOS según comarca seleccionada:
--    - Si comarca_id = 1 (Todo Álava):
--        SELECT * FROM dim_municipios WHERE id = 1
--        → Solo "Todo Álava"
--    - Si comarca_id > 1:
--        SELECT * FROM dim_municipios
--        WHERE id = {comarca_id} OR comarca_id = {comarca_id}
--        ORDER BY id
--        → "Todo {Comarca}" + municipios de esa comarca
--
-- 3. CARGAR CONCEJOS según municipio seleccionado:
--    SELECT * FROM dim_concejos WHERE municipio_id = {municipio_id} ORDER BY id
--    → Siempre devuelve al menos "Todo {Municipio}"
--    → Si hay concejos reales, también los incluye
--
-- ============================================================================
