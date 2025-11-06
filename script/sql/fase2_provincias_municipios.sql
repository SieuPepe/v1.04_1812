-- Fase 2: Añadir provincias y municipios de Álava
-- ===================================================

-- 1. Crear tabla de provincias
-- =============================
CREATE TABLE IF NOT EXISTS dim_provincias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(2) NOT NULL COMMENT 'Código provincial (01=Álava, 20=Gipuzkoa, 48=Bizkaia)',
    nombre VARCHAR(100) NOT NULL COMMENT 'Nombre de la provincia',
    nombre_euskera VARCHAR(100) COMMENT 'Nombre en euskera',
    UNIQUE KEY uk_codigo (codigo),
    UNIQUE KEY uk_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Catálogo de provincias del País Vasco';

-- 2. Insertar las tres provincias
-- ================================
INSERT INTO dim_provincias (id, codigo, nombre, nombre_euskera) VALUES
(1, '01', 'Álava', 'Araba'),
(2, '48', 'Bizkaia', 'Bizkaia'),
(3, '20', 'Gipuzkoa', 'Gipuzkoa')
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nombre_euskera = VALUES(nombre_euskera);

-- 3. Añadir columna provincia_id a tbl_municipios
-- ================================================
-- Verificar si la columna ya existe antes de añadirla
SET @col_exists = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'tbl_municipios'
    AND COLUMN_NAME = 'provincia_id'
);

SET @sql_add_col = IF(@col_exists = 0,
    'ALTER TABLE tbl_municipios ADD COLUMN provincia_id INT DEFAULT NULL COMMENT ''ID de la provincia'' AFTER id',
    'SELECT "Columna provincia_id ya existe" AS mensaje'
);

PREPARE stmt FROM @sql_add_col;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Crear índice para provincia_id (solo si no existe)
SET @idx_exists = (
    SELECT COUNT(*)
    FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'tbl_municipios'
    AND INDEX_NAME = 'idx_provincia_id'
);

SET @sql_add_idx = IF(@idx_exists = 0,
    'ALTER TABLE tbl_municipios ADD INDEX idx_provincia_id (provincia_id)',
    'SELECT "Índice idx_provincia_id ya existe" AS mensaje'
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
    AND CONSTRAINT_NAME = 'fk_municipios_provincia'
);

SET @sql_fk = IF(@fk_exists = 0,
    'ALTER TABLE tbl_municipios ADD CONSTRAINT fk_municipios_provincia FOREIGN KEY (provincia_id) REFERENCES dim_provincias(id)',
    'SELECT "FK fk_municipios_provincia ya existe" AS mensaje'
);

PREPARE stmt FROM @sql_fk;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 4. Actualizar municipios existentes (Bizkaia)
-- ===============================================
-- Los municipios existentes tienen CODIGOINE que empieza por 48
UPDATE tbl_municipios SET provincia_id = 2 WHERE provincia_id IS NULL;

-- 5. Insertar municipios de Álava
-- ================================
-- Lista de 51 municipios de Álava/Araba

INSERT INTO tbl_municipios (provincia_id, NAMEUNIT, CODIGOINE) VALUES
-- Cuadrilla de Vitoria (21 municipios)
(1, 'Vitoria-Gasteiz', 1059),
(1, 'Alegría-Dulantzi', 1001),
(1, 'Armiñón', 1006),
(1, 'Asparrena', 1008),
(1, 'Barrundia', 1011),
(1, 'Berantevilla', 1013),
(1, 'Elburgo', 1021),
(1, 'Harana', 1901),
(1, 'Iruraiz-Gauna', 1027),
(1, 'Legutio', 1029),
(1, 'Salvatierra', 1051),
(1, 'San Millán', 1052),
(1, 'Urkabustaiz', 1058),
(1, 'Vitoria-Gasteiz (Arrazua-Ubarrundia)', 1007),
(1, 'Vitoria-Gasteiz (Foronda)', 1902),
(1, 'Vitoria-Gasteiz (Gamarra Mayor)', 1903),
(1, 'Vitoria-Gasteiz (Mendoza)', 1904),
(1, 'Vitoria-Gasteiz (Arcaya)', 1905),
(1, 'Zalduondo', 1060),
(1, 'Zigoitia', 1061),
(1, 'Zuia', 1062),

-- Cuadrilla de Laguardia (9 municipios)
(1, 'Laguardia', 1028),
(1, 'Baños de Ebro', 1010),
(1, 'Elciego', 1020),
(1, 'Kripan', 1026),
(1, 'Labastida', 1031),
(1, 'Lanciego', 1032),
(1, 'Lapuebla de Labarca', 1033),
(1, 'Moreda de Álava', 1039),
(1, 'Navaridas', 1042),
(1, 'Oyón-Oion', 1043),
(1, 'Samaniego', 1049),
(1, 'Villabuena de Álava', 1057),
(1, 'Yécora', 1063),

-- Cuadrilla de Añana (11 municipios)
(1, 'Añana', 1002),
(1, 'Arraia-Maeztu', 1003),
(1, 'Bernedo', 1014),
(1, 'Campezo', 1016),
(1, 'Iruña Oka', 1901),
(1, 'Kuartango', 1022),
(1, 'Lantarón', 1036),
(1, 'Peñacerrada', 1044),
(1, 'Ribera Alta', 1046),
(1, 'Ribera Baja', 1047),
(1, 'Valdegovía', 1053),

-- Cuadrilla de Ayala (3 municipios)
(1, 'Ayala', 1009),
(1, 'Artziniega', 1004),
(1, 'Okondo', 1041)

ON DUPLICATE KEY UPDATE
    NAMEUNIT = VALUES(NAMEUNIT),
    provincia_id = VALUES(provincia_id);

-- 6. Verificación
-- ===============
SELECT 'Resumen de municipios por provincia:' AS resultado;
SELECT
    p.nombre AS provincia,
    p.nombre_euskera,
    COUNT(m.id) AS total_municipios
FROM dim_provincias p
LEFT JOIN tbl_municipios m ON m.provincia_id = p.id
GROUP BY p.id, p.nombre, p.nombre_euskera
ORDER BY p.codigo;
