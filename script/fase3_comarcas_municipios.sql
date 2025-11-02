-- Fase 3: Relacionar comarcas con provincias y completar municipios
-- ===================================================================
-- Este script adapta la tabla dim_comarcas existente para relacionarla con
-- dim_provincias, añade Gipuzkoa y Bizkaia, y completa los municipios

-- IMPORTANTE: La tabla dim_comarcas ya existe con estructura:
--   id, comarca_codigo, comarca_nombre, created_at
-- Contiene 6 comarcas de Álava (ids 1-6)

-- 1. Añadir columna provincia_id a dim_comarcas
-- ==============================================
SET @col_exists = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'dim_comarcas'
    AND COLUMN_NAME = 'provincia_id'
);

SET @sql_add_col = IF(@col_exists = 0,
    'ALTER TABLE dim_comarcas ADD COLUMN provincia_id INT DEFAULT NULL COMMENT ''ID de la provincia'' AFTER id',
    'SELECT "Columna provincia_id ya existe en dim_comarcas" AS mensaje'
);

PREPARE stmt FROM @sql_add_col;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Crear índice para provincia_id (solo si no existe)
SET @idx_exists = (
    SELECT COUNT(*)
    FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'dim_comarcas'
    AND INDEX_NAME = 'idx_provincia_id'
);

SET @sql_add_idx = IF(@idx_exists = 0,
    'ALTER TABLE dim_comarcas ADD INDEX idx_provincia_id (provincia_id)',
    'SELECT "Índice idx_provincia_id ya existe en dim_comarcas" AS mensaje'
);

PREPARE stmt FROM @sql_add_idx;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Crear FK solo si no existe
SET @fk_exists = (
    SELECT COUNT(*)
    FROM information_schema.TABLE_CONSTRAINTS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'dim_comarcas'
    AND CONSTRAINT_NAME = 'fk_comarcas_provincia'
);

SET @sql_fk = IF(@fk_exists = 0,
    'ALTER TABLE dim_comarcas ADD CONSTRAINT fk_comarcas_provincia FOREIGN KEY (provincia_id) REFERENCES dim_provincias(id)',
    'SELECT "FK fk_comarcas_provincia ya existe" AS mensaje'
);

PREPARE stmt FROM @sql_fk;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 2. Actualizar comarcas existentes de Álava con provincia_id=1
-- ==============================================================
UPDATE dim_comarcas SET provincia_id = 1 WHERE id BETWEEN 1 AND 6 AND provincia_id IS NULL;

-- 3. Insertar nuevas comarcas para Gipuzkoa y Bizkaia
-- ====================================================
INSERT INTO dim_comarcas (id, provincia_id, comarca_codigo, comarca_nombre, created_at) VALUES
(7, 3, 'GIPUZ', 'Gipuzkoa', NOW()),
(8, 2, 'BIZKA', 'Bizkaia', NOW())
ON DUPLICATE KEY UPDATE
    comarca_codigo = VALUES(comarca_codigo),
    comarca_nombre = VALUES(comarca_nombre),
    provincia_id = VALUES(provincia_id);

-- 4. Añadir columna comarca_id a tbl_municipios
-- ==============================================
SET @col_exists = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'tbl_municipios'
    AND COLUMN_NAME = 'comarca_id'
);

SET @sql_add_col = IF(@col_exists = 0,
    'ALTER TABLE tbl_municipios ADD COLUMN comarca_id INT DEFAULT NULL COMMENT ''ID de la comarca/cuadrilla'' AFTER provincia_id',
    'SELECT "Columna comarca_id ya existe" AS mensaje'
);

PREPARE stmt FROM @sql_add_col;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Crear índice para comarca_id (solo si no existe)
SET @idx_exists = (
    SELECT COUNT(*)
    FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'tbl_municipios'
    AND INDEX_NAME = 'idx_comarca_id'
);

SET @sql_add_idx = IF(@idx_exists = 0,
    'ALTER TABLE tbl_municipios ADD INDEX idx_comarca_id (comarca_id)',
    'SELECT "Índice idx_comarca_id ya existe" AS mensaje'
);

PREPARE stmt FROM @sql_add_idx;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Crear FK solo si no existe
SET @fk_exists = (
    SELECT COUNT(*)
    FROM information_schema.TABLE_CONSTRAINTS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'tbl_municipios'
    AND CONSTRAINT_NAME = 'fk_municipios_comarca'
);

SET @sql_fk = IF(@fk_exists = 0,
    'ALTER TABLE tbl_municipios ADD CONSTRAINT fk_municipios_comarca FOREIGN KEY (comarca_id) REFERENCES dim_comarcas(id)',
    'SELECT "FK fk_municipios_comarca ya existe" AS mensaje'
);

PREPARE stmt FROM @sql_fk;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 5. Actualizar comarca_id para municipios existentes
-- ====================================================

-- Actualizar municipios de Bizkaia (provincia_id=2) con comarca_id=8
UPDATE tbl_municipios SET comarca_id = 8 WHERE provincia_id = 2 AND comarca_id IS NULL;

-- Actualizar municipios de Araba (provincia_id=1)
-- Por ahora asignar todos a la comarca correspondiente (se puede refinar después)
-- Comarca 3 (LLANA - Llanada Alavesa) como valor por defecto para municipios de Álava
UPDATE tbl_municipios SET comarca_id = 3 WHERE provincia_id = 1 AND comarca_id IS NULL;

-- 6. Insertar municipios de Gipuzkoa (88 municipios)
-- ===================================================
INSERT INTO tbl_municipios (provincia_id, comarca_id, NAMEUNIT, CODIGOINE) VALUES
-- Provincia de Gipuzkoa (código 20) - Comarca Gipuzkoa (comarca_id=7)
(3, 7, 'Abaltzisketa', 20001),
(3, 7, 'Aduna', 20002),
(3, 7, 'Aia', 20003),
(3, 7, 'Aizarnazabal', 20004),
(3, 7, 'Alegia', 20005),
(3, 7, 'Alkiza', 20006),
(3, 7, 'Altzaga', 20007),
(3, 7, 'Altzo', 20008),
(3, 7, 'Amezketa', 20009),
(3, 7, 'Andoain', 20010),
(3, 7, 'Anoeta', 20011),
(3, 7, 'Antzuola', 20012),
(3, 7, 'Arama', 20013),
(3, 7, 'Aretxabaleta', 20014),
(3, 7, 'Asteasu', 20015),
(3, 7, 'Astigarraga', 20016),
(3, 7, 'Ataun', 20017),
(3, 7, 'Azkoitia', 20018),
(3, 7, 'Azpeitia', 20019),
(3, 7, 'Baliarrain', 20020),
(3, 7, 'Beasain', 20021),
(3, 7, 'Beizama', 20022),
(3, 7, 'Belauntza', 20023),
(3, 7, 'Berastegi', 20024),
(3, 7, 'Bergara', 20025),
(3, 7, 'Berrobi', 20026),
(3, 7, 'Bidania-Goiatz', 20027),
(3, 7, 'Deba', 20028),
(3, 7, 'Donostia-San Sebastián', 20069),
(3, 7, 'Eibar', 20030),
(3, 7, 'Elduain', 20031),
(3, 7, 'Elgeta', 20032),
(3, 7, 'Elgoibar', 20033),
(3, 7, 'Errenteria', 20034),
(3, 7, 'Errezil', 20035),
(3, 7, 'Eskoriatza', 20036),
(3, 7, 'Ezkio-Itsaso', 20037),
(3, 7, 'Gabiria', 20038),
(3, 7, 'Gaintza', 20039),
(3, 7, 'Gaztelu', 20040),
(3, 7, 'Getaria', 20041),
(3, 7, 'Hernani', 20042),
(3, 7, 'Hernialde', 20043),
(3, 7, 'Hondarribia', 20044),
(3, 7, 'Ibarra', 20045),
(3, 7, 'Idiazabal', 20046),
(3, 7, 'Ikaztegieta', 20047),
(3, 7, 'Irun', 20048),
(3, 7, 'Irura', 20049),
(3, 7, 'Itsasondo', 20050),
(3, 7, 'Larraul', 20051),
(3, 7, 'Lasarte-Oria', 20052),
(3, 7, 'Lazkao', 20053),
(3, 7, 'Leaburu', 20054),
(3, 7, 'Legazpi', 20055),
(3, 7, 'Legorreta', 20056),
(3, 7, 'Leintz-Gatzaga', 20057),
(3, 7, 'Lezo', 20058),
(3, 7, 'Lizartza', 20059),
(3, 7, 'Mendaro', 20060),
(3, 7, 'Mutiloa', 20061),
(3, 7, 'Mutriku', 20062),
(3, 7, 'Oiartzun', 20063),
(3, 7, 'Olaberria', 20064),
(3, 7, 'Arrasate/Mondragón', 20065),
(3, 7, 'Onati', 20066),
(3, 7, 'Ordizia', 20067),
(3, 7, 'Orendain', 20068),
(3, 7, 'Orexa', 20070),
(3, 7, 'Orio', 20071),
(3, 7, 'Ormaiztegi', 20072),
(3, 7, 'Pasaia', 20073),
(3, 7, 'Segura', 20074),
(3, 7, 'Soraluze-Placencia de las Armas', 20075),
(3, 7, 'Tolosa', 20076),
(3, 7, 'Urnieta', 20077),
(3, 7, 'Urretxu', 20078),
(3, 7, 'Usurbil', 20079),
(3, 7, 'Villabona', 20080),
(3, 7, 'Zaldibia', 20081),
(3, 7, 'Zarautz', 20082),
(3, 7, 'Zegama', 20083),
(3, 7, 'Zerain', 20084),
(3, 7, 'Zestoa', 20085),
(3, 7, 'Zizurkil', 20086),
(3, 7, 'Zumaia', 20087),
(3, 7, 'Zumarraga', 20088)
ON DUPLICATE KEY UPDATE
    NAMEUNIT = VALUES(NAMEUNIT),
    provincia_id = VALUES(provincia_id),
    comarca_id = VALUES(comarca_id);

-- 7. Verificación
-- ===============
SELECT 'Resumen de comarcas por provincia:' AS resultado;
SELECT
    p.nombre AS provincia,
    c.comarca_nombre AS comarca,
    COUNT(m.id) AS total_municipios
FROM dim_provincias p
LEFT JOIN dim_comarcas c ON c.provincia_id = p.id
LEFT JOIN tbl_municipios m ON m.comarca_id = c.id
GROUP BY p.id, p.nombre, c.id, c.comarca_nombre
ORDER BY p.codigo, c.id;

SELECT 'Resumen total por provincia:' AS resultado;
SELECT
    p.nombre AS provincia,
    COUNT(m.id) AS total_municipios
FROM dim_provincias p
LEFT JOIN tbl_municipios m ON m.provincia_id = p.id
GROUP BY p.id, p.nombre
ORDER BY p.codigo;

SELECT 'Detalle de comarcas:' AS resultado;
SELECT
    c.id,
    c.comarca_codigo,
    c.comarca_nombre,
    p.nombre AS provincia
FROM dim_comarcas c
LEFT JOIN dim_provincias p ON p.id = c.provincia_id
ORDER BY c.id;
