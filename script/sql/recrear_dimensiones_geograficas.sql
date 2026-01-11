-- ============================================================================
-- RECREAR DIMENSIONES GEOGRÁFICAS CON ESTRUCTURA "VARIOS"
-- ============================================================================
-- Este script recrea las tablas de dimensiones geográficas con la estructura
-- correcta para soportar selecciones de "Varios {nombre}".
--
-- JERARQUÍA: Provincia → Comarca → Municipio → Concejo
--
-- ESTRUCTURA DE IDs:
--   Comarcas:   ID 1 = "Varios Álava", IDs 2+ = comarcas reales
--   Municipios: ID 1 = "Varios Álava", IDs 2-100 = "Varios {Comarca}", IDs 1000+ = municipios reales
--   Concejos:   IDs bajos = "Varios {X}", IDs altos = concejos reales
--
-- ⚠️ ADVERTENCIA: Este script ELIMINA todos los datos geográficos existentes
--
-- USO:
--   mysql -h localhost -P 3307 -u root -p cert_dev < recrear_dimensiones_geograficas.sql
-- ============================================================================

SELECT DATABASE() AS esquema_actual;
SELECT '=== INICIO: Recrear dimensiones geográficas ===' AS info;
SELECT NOW() AS fecha_ejecucion;

-- ============================================================================
-- FASE 0: VERIFICAR Y LIMPIAR TABLAS DE HECHOS
-- ============================================================================

SELECT '>>> FASE 0: Verificando tablas de hechos...' AS paso;

-- Mostrar registros que se verán afectados
SELECT
    'tbl_partes' AS tabla,
    COUNT(*) AS registros,
    COUNT(municipio_id) AS con_municipio,
    COUNT(concejo_id) AS con_concejo
FROM tbl_partes;

-- Si hay registros, advertir
SELECT
    CASE
        WHEN COUNT(*) > 0 THEN '⚠️ ADVERTENCIA: Hay partes con referencias geográficas que se perderán'
        ELSE '✓ No hay partes con referencias geográficas'
    END AS estado
FROM tbl_partes
WHERE municipio_id IS NOT NULL OR concejo_id IS NOT NULL;

-- Desactivar FK
SET FOREIGN_KEY_CHECKS = 0;

-- Limpiar referencias geográficas en tbl_partes (no eliminar, solo quitar FK)
UPDATE tbl_partes SET municipio_id = NULL, concejo_id = NULL;
SELECT CONCAT('  ✓ Referencias geográficas limpiadas en tbl_partes: ', ROW_COUNT(), ' registros') AS resultado;

-- ============================================================================
-- FASE 1: LIMPIAR TABLAS DE DIMENSIONES GEOGRÁFICAS
-- ============================================================================

SELECT '>>> FASE 1: Limpiando tablas de dimensiones...' AS paso;

-- Orden: de más dependiente a menos
DELETE FROM dim_concejos;
SELECT CONCAT('  ✓ dim_concejos limpiada: ', ROW_COUNT(), ' registros eliminados') AS resultado;

DELETE FROM dim_municipios;
SELECT CONCAT('  ✓ dim_municipios limpiada: ', ROW_COUNT(), ' registros eliminados') AS resultado;

DELETE FROM dim_comarcas;
SELECT CONCAT('  ✓ dim_comarcas limpiada: ', ROW_COUNT(), ' registros eliminados') AS resultado;

-- Resetear AUTO_INCREMENT
ALTER TABLE dim_concejos AUTO_INCREMENT = 1;
ALTER TABLE dim_municipios AUTO_INCREMENT = 1;
ALTER TABLE dim_comarcas AUTO_INCREMENT = 1;

-- ============================================================================
-- FASE 2: CREAR COMARCAS (Cuadrillas de Álava)
-- ============================================================================

SELECT '>>> FASE 2: Creando comarcas...' AS paso;

-- ID 1 = Varios Álava (representa todas las comarcas)
-- IDs 2-7 = Comarcas reales (Cuadrillas de Álava)
INSERT INTO dim_comarcas (id, comarca_nombre, provincia_id, activo) VALUES
(1, 'Varios Álava', 1, 1),
(2, 'Ayala / Aiaraldea', 1, 1),
(3, 'Vitoria-Gasteiz / Llanada Alavesa', 1, 1),
(4, 'Rioja Alavesa', 1, 1),
(5, 'Añana', 1, 1),
(6, 'Montaña Alavesa', 1, 1),
(7, 'Estribaciones del Gorbea', 1, 1);

SELECT CONCAT('  ✓ Comarcas creadas: ', ROW_COUNT()) AS resultado;

-- ============================================================================
-- FASE 3: CREAR MUNICIPIOS
-- ============================================================================

SELECT '>>> FASE 3: Creando municipios...' AS paso;

-- ============================================================================
-- 3.1 REGISTROS "VARIOS" (IDs 1-100)
-- ============================================================================

-- ID 1 = Varios Álava (todos los municipios de Álava)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(1, '0000', 'Varios Álava', 1, NULL, 1);

-- IDs 2-7 = Varios por comarca
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(2, '0000', 'Varios Aiaraldea', 1, 2, 1),
(3, '0000', 'Varios Llanada Alavesa', 1, 3, 1),
(4, '0000', 'Varios Rioja Alavesa', 1, 4, 1),
(5, '0000', 'Varios Añana', 1, 5, 1),
(6, '0000', 'Varios Montaña Alavesa', 1, 6, 1),
(7, '0000', 'Varios Estribaciones Gorbea', 1, 7, 1);

-- ============================================================================
-- 3.2 MUNICIPIOS REALES (IDs 1001+)
-- ============================================================================

-- Comarca Ayala/Aiaraldea (comarca_id = 2)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(1001, '01002', 'Amurrio', 1, 2, 1),
(1002, '01010', 'Ayala/Aiara', 1, 2, 1),
(1003, '01004', 'Artziniega', 1, 2, 1),
(1004, '01036', 'Laudio/Llodio', 1, 2, 1),
(1005, '01042', 'Okondo', 1, 2, 1),
(1006, '01003', 'Aramaio', 1, 2, 1);

-- Comarca Llanada Alavesa / Vitoria (comarca_id = 3)
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

-- Comarca Añana (comarca_id = 5)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(1030, '01049', 'Añana', 1, 5, 1),
(1031, '01006', 'Armiñón', 1, 5, 1),
(1032, '01014', 'Berantevilla', 1, 5, 1),
(1033, '01020', 'Kuartango', 1, 5, 1),
(1034, '01901', 'Iruña Oka/Iruña de Oca', 1, 5, 1),
(1035, '01902', 'Lantarón', 1, 5, 1),
(1036, '01023', 'Erriberagoitia/Ribera Alta', 1, 5, 1),
(1037, '01047', 'Ribera Baja/Erribera Beitia', 1, 5, 1),
(1038, '01055', 'Valdegovía/Gaubea', 1, 5, 1),
(1039, '01062', 'Zambrana', 1, 5, 1);

-- Comarca Montaña Alavesa (comarca_id = 6)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(1050, '01037', 'Arraia-Maeztu', 1, 6, 1),
(1051, '01016', 'Bernedo', 1, 6, 1),
(1052, '01017', 'Campezo/Kanpezu', 1, 6, 1),
(1053, '01030', 'Lagrán', 1, 6, 1),
(1054, '01044', 'Peñacerrada-Urizaharra', 1, 6, 1),
(1055, '01056', 'Harana/Valle de Arana', 1, 6, 1);

-- Comarca Rioja Alavesa (comarca_id = 4)
INSERT INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo) VALUES
(1060, '01011', 'Baños de Ebro/Mañueta', 1, 4, 1),
(1061, '01019', 'Kripan', 1, 4, 1),
(1062, '01022', 'Elciego', 1, 4, 1),
(1063, '01028', 'Labastida/Bastida', 1, 4, 1),
(1064, '01031', 'Laguardia', 1, 4, 1),
(1065, '01032', 'Lanciego/Lantziego', 1, 4, 1),
(1066, '01033', 'Lapuebla de Labarca', 1, 4, 1),
(1067, '01034', 'Leza', 1, 4, 1),
(1068, '01039', 'Moreda de Álava/Moreda Araba', 1, 4, 1),
(1069, '01041', 'Navaridas', 1, 4, 1),
(1070, '01043', 'Oyón-Oion', 1, 4, 1),
(1071, '01052', 'Samaniego', 1, 4, 1),
(1072, '01057', 'Villabuena de Álava/Eskuernaga', 1, 4, 1),
(1073, '01060', 'Yécora/Iekora', 1, 4, 1);

SELECT CONCAT('  ✓ Municipios creados: ', (SELECT COUNT(*) FROM dim_municipios)) AS resultado;

-- ============================================================================
-- FASE 4: CREAR CONCEJOS
-- ============================================================================

SELECT '>>> FASE 4: Creando concejos...' AS paso;

-- ============================================================================
-- 4.1 REGISTROS "VARIOS" - Uno por cada municipio (incluidos los "Varios")
-- ============================================================================

-- Varios globales y por comarca (corresponden a municipios IDs 1-7)
INSERT INTO dim_concejos (id, municipio_id, nombre, activo) VALUES
(1, 1, 'Varios Álava', 1),
(2, 2, 'Varios Aiaraldea', 1),
(3, 3, 'Varios Llanada Alavesa', 1),
(4, 4, 'Varios Rioja Alavesa', 1),
(5, 5, 'Varios Añana', 1),
(6, 6, 'Varios Montaña Alavesa', 1),
(7, 7, 'Varios Estribaciones Gorbea', 1);

-- Varios por municipio real (IDs 1001+, concejos IDs 1001+)
INSERT INTO dim_concejos (id, municipio_id, nombre, activo)
SELECT id, id, CONCAT('Varios ', municipio_nombre), 1
FROM dim_municipios
WHERE id >= 1001;

-- ============================================================================
-- 4.2 CONCEJOS REALES
-- ============================================================================

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

-- Valdegovía/Gaubea (municipio_id = 1038)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1038, 'Acebedo', 1),
(1038, 'Bachicabo', 1),
(1038, 'Barrio', 1),
(1038, 'Basabe', 1),
(1038, 'Bóveda', 1),
(1038, 'Caranca y Mioma', 1),
(1038, 'Karkamu', 1),
(1038, 'Corro', 1),
(1038, 'Espejo', 1),
(1038, 'Fresneda', 1),
(1038, 'Gurendes-Quejo', 1),
(1038, 'Nograro', 1),
(1038, 'Osma', 1),
(1038, 'Pinedo', 1),
(1038, 'Quintanilla', 1),
(1038, 'Tobillas', 1),
(1038, 'Tuesta', 1),
(1038, 'Valderejo', 1),
(1038, 'Valluerca', 1),
(1038, 'Villamaderne-Bellojín', 1),
(1038, 'Villanañe', 1),
(1038, 'Villanueva de Valdegovía', 1);

-- Zambrana (municipio_id = 1039)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1039, 'Berganzo', 1),
(1039, 'Ocio', 1),
(1039, 'Portilla/Zabalate', 1),
(1039, 'Zambrana', 1);

-- Arraia-Maeztu (municipio_id = 1050)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1050, 'Apellániz/Apinaiz', 1),
(1050, 'Atauri', 1),
(1050, 'Azazeta', 1),
(1050, 'Korres', 1),
(1050, 'Maeztu/Maestu', 1),
(1050, 'Onraita/Erroeta', 1),
(1050, 'Róitegui/Erroitegi', 1),
(1050, 'Sabando', 1),
(1050, 'Vírgala Mayor/Birgara Goien', 1);

-- Bernedo (municipio_id = 1051)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1051, 'Angostina', 1),
(1051, 'Arluzea', 1),
(1051, 'Bernedo', 1),
(1051, 'Markinez', 1),
(1051, 'Navarrete', 1),
(1051, 'Okina', 1),
(1051, 'Quintana', 1),
(1051, 'San Román de Campezo', 1),
(1051, 'Urarte', 1),
(1051, 'Urturi', 1),
(1051, 'Villafría', 1);

-- Campezo/Kanpezu (municipio_id = 1052)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1052, 'Antoñana', 1),
(1052, 'Bujanda', 1),
(1052, 'Orbiso', 1),
(1052, 'Oteo', 1),
(1052, 'Santa Cruz de Campezo', 1);

-- Ribera Alta (municipio_id = 1036)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1036, 'Antezana de la Ribera', 1),
(1036, 'Anuntzeta/Anúcita', 1),
(1036, 'Arreo', 1),
(1036, 'Artaza-Escota', 1),
(1036, 'Barrón', 1),
(1036, 'Basquiñuelas', 1),
(1036, 'Caicedo-Sopeña', 1),
(1036, 'Hereña', 1),
(1036, 'Lasierra', 1),
(1036, 'Leciñana de la Oca', 1),
(1036, 'Morillas', 1),
(1036, 'Ormijana', 1),
(1036, 'Paúl', 1),
(1036, 'Pobes', 1),
(1036, 'Subijana-Morillas', 1),
(1036, 'Tuyo', 1),
(1036, 'Villabezana', 1),
(1036, 'Villaluenga', 1),
(1036, 'Villambrosa', 1),
(1036, 'Viloria', 1);

-- Lantarón (municipio_id = 1035)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1035, 'Alcedo', 1),
(1035, 'Bergüenda', 1),
(1035, 'Caicedo de Yuso', 1),
(1035, 'Comunión', 1),
(1035, 'Fontecha', 1),
(1035, 'Leciñana del Camino', 1),
(1035, 'Molinilla', 1),
(1035, 'Puentelarrá', 1),
(1035, 'Salcedo', 1),
(1035, 'Sobrón', 1),
(1035, 'Turiso', 1),
(1035, 'Zubillaga', 1);

-- Berantevilla (municipio_id = 1032)
INSERT INTO dim_concejos (municipio_id, nombre, activo) VALUES
(1032, 'Berantevilla', 1),
(1032, 'Lacervilla', 1),
(1032, 'Mijancas', 1),
(1032, 'Santa Cruz del Fierro', 1),
(1032, 'Santurde', 1),
(1032, 'Tobera', 1);

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

SELECT CONCAT('  ✓ Concejos creados: ', (SELECT COUNT(*) FROM dim_concejos)) AS resultado;

-- Reactivar FK
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================================
-- FASE 5: VERIFICACIÓN FINAL
-- ============================================================================

SELECT '>>> FASE 5: Verificación final...' AS paso;

SELECT '--- COMARCAS ---' AS '';
SELECT id, comarca_nombre, provincia_id FROM dim_comarcas ORDER BY id;

SELECT '--- MUNICIPIOS "Varios" (primeros) ---' AS '';
SELECT id, municipio_nombre, comarca_id FROM dim_municipios WHERE id < 100 ORDER BY id;

SELECT '--- MUNICIPIOS reales (muestra) ---' AS '';
SELECT id, municipio_nombre, comarca_id FROM dim_municipios WHERE id >= 1001 ORDER BY id LIMIT 10;

SELECT '--- CONCEJOS "Varios" (primeros) ---' AS '';
SELECT id, nombre, municipio_id FROM dim_concejos WHERE id < 100 ORDER BY id;

SELECT '--- TOTALES ---' AS '';
SELECT
    (SELECT COUNT(*) FROM dim_comarcas) AS comarcas,
    (SELECT COUNT(*) FROM dim_municipios) AS municipios,
    (SELECT COUNT(*) FROM dim_concejos) AS concejos,
    (SELECT COUNT(*) FROM dim_municipios WHERE municipio_nombre LIKE 'Varios %') AS municipios_varios,
    (SELECT COUNT(*) FROM dim_concejos WHERE nombre LIKE 'Varios %') AS concejos_varios;

SELECT '=== FIN: Dimensiones geográficas recreadas correctamente ===' AS resultado;

-- ============================================================================
-- REGLAS DE USO EN DROPDOWNS:
-- ============================================================================
--
-- 1. Al cargar COMARCAS para una provincia:
--    SELECT * FROM dim_comarcas WHERE provincia_id = 1 ORDER BY id
--    → "Varios Álava" aparece primero (id=1)
--
-- 2. Al cargar MUNICIPIOS para una comarca:
--    - Si comarca_id = 1 (Varios Álava):
--        Solo mostrar municipio id=1 (Varios Álava)
--    - Si comarca_id > 1 (comarca específica):
--        SELECT * FROM dim_municipios
--        WHERE comarca_id = ? OR id = ?  -- incluir "Varios {comarca}"
--        ORDER BY id
--
-- 3. Al cargar CONCEJOS para un municipio:
--    SELECT * FROM dim_concejos WHERE municipio_id = ? ORDER BY id
--    → Si municipio_id < 100 (es "Varios"), solo devuelve su "Varios" correspondiente
--    → Si municipio_id >= 1001, devuelve "Varios {municipio}" + concejos reales
-- ============================================================================
