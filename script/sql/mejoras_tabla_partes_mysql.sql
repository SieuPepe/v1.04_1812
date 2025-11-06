-- ============================================================================
-- MEJORA DE ÓRDENES DE TRABAJO (PARTES) - FASE 1
-- Script SQL COMPATIBLE CON MySQL 5.7+ (sin MariaDB features)
-- Basado en funcionalidades de BD Access Certificaciones UTE
-- ============================================================================

-- ============================================================================
-- PARTE 1: CREAR TABLA DE ESTADOS
-- ============================================================================

-- Tabla de estados para las órdenes de trabajo
CREATE TABLE IF NOT EXISTS tbl_parte_estados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion VARCHAR(200),
    orden INT NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_orden (orden),
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Catálogo de estados de partes/órdenes de trabajo';

-- Insertar estados predefinidos (idempotente)
INSERT INTO tbl_parte_estados (nombre, descripcion, orden) VALUES
('Pendiente', 'Parte pendiente de iniciar', 1),
('En curso', 'Parte en ejecución', 2),
('Finalizada', 'Parte completada con éxito', 3),
('Cancelada', 'Parte cancelada', 4),
('Suspendida', 'Parte temporalmente suspendida', 5)
ON DUPLICATE KEY UPDATE descripcion=VALUES(descripcion), orden=VALUES(orden);

-- ============================================================================
-- PARTE 2: AÑADIR CAMPOS A tbl_partes (COMPATIBLE MySQL)
-- ============================================================================

-- Procedimiento para añadir columna solo si no existe
DELIMITER //

DROP PROCEDURE IF EXISTS add_column_if_not_exists//
CREATE PROCEDURE add_column_if_not_exists(
    IN p_table_name VARCHAR(64),
    IN p_column_name VARCHAR(64),
    IN p_column_definition TEXT
)
BEGIN
    DECLARE column_count INT;

    SELECT COUNT(*) INTO column_count
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = p_table_name
    AND COLUMN_NAME = p_column_name;

    IF column_count = 0 THEN
        SET @sql = CONCAT('ALTER TABLE ', p_table_name,
                         ' ADD COLUMN ', p_column_name, ' ', p_column_definition);
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        SELECT CONCAT('✓ Columna ', p_column_name, ' añadida') AS resultado;
    ELSE
        SELECT CONCAT('⚠ Columna ', p_column_name, ' ya existe') AS resultado;
    END IF;
END//

DELIMITER ;

-- Añadir columnas usando el procedimiento
CALL add_column_if_not_exists('tbl_partes', 'titulo',
    "VARCHAR(255) COMMENT 'Título descriptivo del parte'");

CALL add_column_if_not_exists('tbl_partes', 'descripcion_larga',
    "TEXT COMMENT 'Descripción detallada del trabajo realizado'");

CALL add_column_if_not_exists('tbl_partes', 'descripcion_corta',
    "VARCHAR(100) COMMENT 'Descripción breve para listados'");

CALL add_column_if_not_exists('tbl_partes', 'fecha_inicio',
    "DATE COMMENT 'Fecha de inicio del trabajo'");

CALL add_column_if_not_exists('tbl_partes', 'fecha_fin',
    "DATE COMMENT 'Fecha de finalización del trabajo'");

CALL add_column_if_not_exists('tbl_partes', 'fecha_prevista_fin',
    "DATE COMMENT 'Fecha prevista de finalización'");

CALL add_column_if_not_exists('tbl_partes', 'id_estado',
    "INT DEFAULT 1 COMMENT 'Estado del parte (FK a tbl_parte_estados)'");

CALL add_column_if_not_exists('tbl_partes', 'finalizada',
    "BOOLEAN DEFAULT FALSE COMMENT 'Indica si el parte está finalizado'");

CALL add_column_if_not_exists('tbl_partes', 'localizacion',
    "VARCHAR(255) COMMENT 'Localización textual del trabajo'");

CALL add_column_if_not_exists('tbl_partes', 'id_municipio',
    "INT COMMENT 'Municipio donde se realizó el trabajo'");

-- Limpiar procedimiento temporal
DROP PROCEDURE IF EXISTS add_column_if_not_exists;

-- ============================================================================
-- PARTE 3: AÑADIR CLAVES FORÁNEAS (con verificación)
-- ============================================================================

DELIMITER //

DROP PROCEDURE IF EXISTS add_fk_if_not_exists//
CREATE PROCEDURE add_fk_if_not_exists(
    IN p_table_name VARCHAR(64),
    IN p_constraint_name VARCHAR(64),
    IN p_fk_definition TEXT
)
BEGIN
    DECLARE fk_count INT;

    SELECT COUNT(*) INTO fk_count
    FROM information_schema.TABLE_CONSTRAINTS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = p_table_name
    AND CONSTRAINT_NAME = p_constraint_name
    AND CONSTRAINT_TYPE = 'FOREIGN KEY';

    IF fk_count = 0 THEN
        SET @sql = CONCAT('ALTER TABLE ', p_table_name,
                         ' ADD CONSTRAINT ', p_constraint_name,
                         ' ', p_fk_definition);
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        SELECT CONCAT('✓ FK ', p_constraint_name, ' añadida') AS resultado;
    ELSE
        SELECT CONCAT('⚠ FK ', p_constraint_name, ' ya existe') AS resultado;
    END IF;
END//

DELIMITER ;

-- Añadir FK a tabla de estados
CALL add_fk_if_not_exists('tbl_partes', 'fk_partes_estado',
    'FOREIGN KEY (id_estado) REFERENCES tbl_parte_estados(id) ON DELETE RESTRICT ON UPDATE CASCADE');

-- Añadir FK a municipios solo si la tabla existe
DELIMITER //

DROP PROCEDURE IF EXISTS add_fk_municipio_if_table_exists//
CREATE PROCEDURE add_fk_municipio_if_table_exists()
BEGIN
    DECLARE table_count INT;
    DECLARE fk_count INT;

    -- Verificar si existe la tabla tbl_municipios
    SELECT COUNT(*) INTO table_count
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'tbl_municipios';

    IF table_count > 0 THEN
        -- Verificar si ya existe la FK
        SELECT COUNT(*) INTO fk_count
        FROM information_schema.TABLE_CONSTRAINTS
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = 'tbl_partes'
        AND CONSTRAINT_NAME = 'fk_partes_municipio'
        AND CONSTRAINT_TYPE = 'FOREIGN KEY';

        IF fk_count = 0 THEN
            ALTER TABLE tbl_partes
            ADD CONSTRAINT fk_partes_municipio
            FOREIGN KEY (id_municipio) REFERENCES tbl_municipios(id)
            ON DELETE SET NULL
            ON UPDATE CASCADE;
            SELECT '✓ FK fk_partes_municipio añadida' AS resultado;
        ELSE
            SELECT '⚠ FK fk_partes_municipio ya existe' AS resultado;
        END IF;
    ELSE
        SELECT 'ℹ Tabla tbl_municipios no existe, FK no creada' AS resultado;
    END IF;
END//

DELIMITER ;

CALL add_fk_municipio_if_table_exists();

-- Limpiar procedimientos temporales
DROP PROCEDURE IF EXISTS add_fk_if_not_exists;
DROP PROCEDURE IF EXISTS add_fk_municipio_if_table_exists;

-- ============================================================================
-- PARTE 4: CREAR ÍNDICES PARA OPTIMIZAR CONSULTAS
-- ============================================================================

-- Índices con IF NOT EXISTS (soportado desde MySQL 5.7)
CREATE INDEX IF NOT EXISTS idx_partes_estado ON tbl_partes(id_estado);
CREATE INDEX IF NOT EXISTS idx_partes_finalizada ON tbl_partes(finalizada);
CREATE INDEX IF NOT EXISTS idx_partes_fecha_inicio ON tbl_partes(fecha_inicio);
CREATE INDEX IF NOT EXISTS idx_partes_fecha_fin ON tbl_partes(fecha_fin);
CREATE INDEX IF NOT EXISTS idx_partes_municipio ON tbl_partes(id_municipio);
CREATE INDEX IF NOT EXISTS idx_partes_estado_fecha ON tbl_partes(id_estado, fecha_inicio);

-- ============================================================================
-- PARTE 5: CREAR TRIGGER PARA SINCRONIZAR FINALIZADA CON ESTADO
-- ============================================================================

DELIMITER //

DROP TRIGGER IF EXISTS trg_partes_sync_finalizada_insert//
CREATE TRIGGER trg_partes_sync_finalizada_insert
BEFORE INSERT ON tbl_partes
FOR EACH ROW
BEGIN
    -- Si el estado es Finalizada (id=3), marcar finalizada=TRUE
    IF NEW.id_estado = 3 THEN
        SET NEW.finalizada = TRUE;
    ELSE
        SET NEW.finalizada = COALESCE(NEW.finalizada, FALSE);
    END IF;

    -- Si finalizada=TRUE, poner estado en Finalizada (id=3)
    IF NEW.finalizada = TRUE AND COALESCE(NEW.id_estado, 1) != 3 THEN
        SET NEW.id_estado = 3;
    END IF;
END//

DROP TRIGGER IF EXISTS trg_partes_sync_finalizada_update//
CREATE TRIGGER trg_partes_sync_finalizada_update
BEFORE UPDATE ON tbl_partes
FOR EACH ROW
BEGIN
    -- Si el estado cambia a Finalizada (id=3), marcar finalizada=TRUE
    IF NEW.id_estado = 3 AND OLD.id_estado != 3 THEN
        SET NEW.finalizada = TRUE;
        -- Si fecha_fin es NULL, poner fecha actual
        IF NEW.fecha_fin IS NULL THEN
            SET NEW.fecha_fin = CURDATE();
        END IF;
    END IF;

    -- Si el estado cambia desde Finalizada a otro, marcar finalizada=FALSE
    IF NEW.id_estado != 3 AND OLD.id_estado = 3 THEN
        SET NEW.finalizada = FALSE;
    END IF;

    -- Si finalizada cambia a TRUE, poner estado en Finalizada (id=3)
    IF NEW.finalizada = TRUE AND NEW.id_estado != 3 THEN
        SET NEW.id_estado = 3;
        -- Si fecha_fin es NULL, poner fecha actual
        IF NEW.fecha_fin IS NULL THEN
            SET NEW.fecha_fin = CURDATE();
        END IF;
    END IF;

    -- Si finalizada cambia a FALSE desde TRUE, cambiar estado a En curso (id=2)
    IF NEW.finalizada = FALSE AND OLD.finalizada = TRUE THEN
        SET NEW.id_estado = 2;
    END IF;
END//

DELIMITER ;

-- ============================================================================
-- PARTE 6: CREAR VISTA MEJORADA DE PARTES
-- ============================================================================

DROP VIEW IF EXISTS vw_partes_completo;

CREATE VIEW vw_partes_completo AS
SELECT
    p.id,
    p.codigo,
    p.titulo,
    p.descripcion AS descripcion_original,
    p.descripcion_larga,
    p.descripcion_corta,
    p.fecha_inicio,
    p.fecha_fin,
    p.fecha_prevista_fin,
    CASE
        WHEN p.fecha_fin IS NOT NULL AND p.fecha_inicio IS NOT NULL
        THEN DATEDIFF(p.fecha_fin, p.fecha_inicio)
        ELSE NULL
    END AS dias_duracion,
    CASE
        WHEN p.fecha_fin IS NULL AND p.fecha_prevista_fin IS NOT NULL
        THEN DATEDIFF(CURDATE(), p.fecha_prevista_fin)
        ELSE NULL
    END AS dias_retraso,
    pe.nombre AS estado,
    pe.descripcion AS estado_descripcion,
    p.finalizada,
    p.localizacion,
    m.nombre AS municipio,
    ot.nombre AS ot,
    r.nombre AS red,
    tt.nombre AS tipo_trabajo,
    ct.nombre AS cod_trabajo,
    p.fecha_creacion,
    p.fecha_modificacion
FROM tbl_partes p
LEFT JOIN tbl_parte_estados pe ON p.id_estado = pe.id
LEFT JOIN tbl_municipios m ON p.id_municipio = m.id
LEFT JOIN dim_ot ot ON p.id_ot = ot.id
LEFT JOIN dim_red r ON p.id_red = r.id
LEFT JOIN dim_tipo_trabajo tt ON p.id_tipo_trabajo = tt.id
LEFT JOIN dim_cod_trabajo ct ON p.id_cod_trabajo = ct.id
ORDER BY p.fecha_inicio DESC, p.id DESC;

-- ============================================================================
-- PARTE 7: ACTUALIZAR DATOS EXISTENTES (OPCIONAL)
-- ============================================================================

-- Establecer estado 'Pendiente' a partes sin estado
UPDATE tbl_partes
SET id_estado = 1
WHERE id_estado IS NULL;

-- Generar descripcion_corta desde descripcion si está vacía
UPDATE tbl_partes
SET descripcion_corta = LEFT(COALESCE(descripcion, 'Sin descripción'), 100)
WHERE descripcion_corta IS NULL OR descripcion_corta = '';

-- Generar titulo desde descripcion_corta si está vacío
UPDATE tbl_partes
SET titulo = COALESCE(descripcion_corta, LEFT(descripcion, 100), CONCAT('Parte ', codigo))
WHERE titulo IS NULL OR titulo = '';

-- Si no hay descripcion_larga, copiar desde descripcion
UPDATE tbl_partes
SET descripcion_larga = descripcion
WHERE descripcion_larga IS NULL AND descripcion IS NOT NULL;

-- ============================================================================
-- PARTE 8: VERIFICACIÓN
-- ============================================================================

-- Mostrar estructura de la tabla
SELECT 'Verificando estructura de tbl_partes...' AS info;
SHOW COLUMNS FROM tbl_partes LIKE '%estado%';
SHOW COLUMNS FROM tbl_partes LIKE '%descripcion%';
SHOW COLUMNS FROM tbl_partes LIKE '%fecha%';

-- Contar estados
SELECT 'Verificando estados...' AS info;
SELECT COUNT(*) AS total_estados FROM tbl_parte_estados;

-- Mostrar distribución de partes por estado
SELECT
    COALESCE(pe.nombre, 'Sin estado') AS estado,
    COUNT(*) AS cantidad
FROM tbl_partes p
LEFT JOIN tbl_parte_estados pe ON p.id_estado = pe.id
GROUP BY pe.nombre
ORDER BY pe.orden;

-- ============================================================================
-- FIN DEL SCRIPT
-- ============================================================================

SELECT '✅ MIGRACIÓN COMPLETADA' AS resultado;
