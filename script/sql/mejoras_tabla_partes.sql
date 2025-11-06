-- ============================================================================
-- MEJORA DE ÓRDENES DE TRABAJO (PARTES) - FASE 1
-- Script SQL para añadir campos mejorados a tbl_partes
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

-- Insertar estados predefinidos
INSERT INTO tbl_parte_estados (nombre, descripcion, orden) VALUES
('Pendiente', 'Parte pendiente de iniciar', 1),
('En curso', 'Parte en ejecución', 2),
('Finalizada', 'Parte completada con éxito', 3),
('Cancelada', 'Parte cancelada', 4),
('Suspendida', 'Parte temporalmente suspendida', 5)
ON DUPLICATE KEY UPDATE descripcion=VALUES(descripcion), orden=VALUES(orden);

-- ============================================================================
-- PARTE 2: AÑADIR CAMPOS A tbl_partes
-- ============================================================================

-- Verificar si la tabla existe antes de alterarla
-- Este script está diseñado para ejecutarse de forma segura en cualquier esquema

-- Añadir columna TITULO (obligatorio para describir el parte)
ALTER TABLE tbl_partes
ADD COLUMN IF NOT EXISTS titulo VARCHAR(255) COMMENT 'Título descriptivo del parte';

-- Añadir columna DESCRIPCION_LARGA (detalles completos)
ALTER TABLE tbl_partes
ADD COLUMN IF NOT EXISTS descripcion_larga TEXT COMMENT 'Descripción detallada del trabajo realizado';

-- Añadir columna DESCRIPCION_CORTA (resumen para listados)
ALTER TABLE tbl_partes
ADD COLUMN IF NOT EXISTS descripcion_corta VARCHAR(100) COMMENT 'Descripción breve para listados';

-- Añadir columnas de FECHAS
ALTER TABLE tbl_partes
ADD COLUMN IF NOT EXISTS fecha_inicio DATE COMMENT 'Fecha de inicio del trabajo';

ALTER TABLE tbl_partes
ADD COLUMN IF NOT EXISTS fecha_fin DATE COMMENT 'Fecha de finalización del trabajo';

ALTER TABLE tbl_partes
ADD COLUMN IF NOT EXISTS fecha_prevista_fin DATE COMMENT 'Fecha prevista de finalización';

-- Añadir columna de ESTADO
ALTER TABLE tbl_partes
ADD COLUMN IF NOT EXISTS id_estado INT DEFAULT 1 COMMENT 'Estado del parte (FK a tbl_parte_estados)';

-- Añadir columna FINALIZADA (booleano para compatibilidad con Access)
ALTER TABLE tbl_partes
ADD COLUMN IF NOT EXISTS finalizada BOOLEAN DEFAULT FALSE COMMENT 'Indica si el parte está finalizado';

-- Añadir columna LOCALIZACION (ubicación textual)
ALTER TABLE tbl_partes
ADD COLUMN IF NOT EXISTS localizacion VARCHAR(255) COMMENT 'Localización textual del trabajo';

-- Añadir columna ID_MUNICIPIO (si no existe)
ALTER TABLE tbl_partes
ADD COLUMN IF NOT EXISTS id_municipio INT COMMENT 'Municipio donde se realizó el trabajo';

-- ============================================================================
-- PARTE 3: AÑADIR CLAVES FORÁNEAS
-- ============================================================================

-- Añadir FK a tabla de estados
ALTER TABLE tbl_partes
ADD CONSTRAINT IF NOT EXISTS fk_partes_estado
FOREIGN KEY (id_estado) REFERENCES tbl_parte_estados(id)
ON DELETE RESTRICT
ON UPDATE CASCADE;

-- Añadir FK a municipios (si la tabla existe)
-- Nota: Esta FK solo se añadirá si existe la tabla tbl_municipios
SET @table_exists = (
    SELECT COUNT(*)
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'tbl_municipios'
);

-- Solo ejecutar si la tabla existe
SET @sql = IF(@table_exists > 0,
    'ALTER TABLE tbl_partes
     ADD CONSTRAINT IF NOT EXISTS fk_partes_municipio
     FOREIGN KEY (id_municipio) REFERENCES tbl_municipios(id)
     ON DELETE SET NULL
     ON UPDATE CASCADE',
    'SELECT "Tabla tbl_municipios no existe, FK no creada" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ============================================================================
-- PARTE 4: CREAR ÍNDICES PARA OPTIMIZAR CONSULTAS
-- ============================================================================

-- Índice en estado para filtrar partes por estado
CREATE INDEX IF NOT EXISTS idx_partes_estado ON tbl_partes(id_estado);

-- Índice en finalizada para consultas frecuentes
CREATE INDEX IF NOT EXISTS idx_partes_finalizada ON tbl_partes(finalizada);

-- Índice en fecha_inicio para ordenar cronológicamente
CREATE INDEX IF NOT EXISTS idx_partes_fecha_inicio ON tbl_partes(fecha_inicio);

-- Índice en fecha_fin para ordenar cronológicamente
CREATE INDEX IF NOT EXISTS idx_partes_fecha_fin ON tbl_partes(fecha_fin);

-- Índice en municipio para agrupar por localidad
CREATE INDEX IF NOT EXISTS idx_partes_municipio ON tbl_partes(id_municipio);

-- Índice compuesto para consultas de partes pendientes
CREATE INDEX IF NOT EXISTS idx_partes_estado_fecha ON tbl_partes(id_estado, fecha_inicio);

-- ============================================================================
-- PARTE 5: CREAR TRIGGER PARA SINCRONIZAR FINALIZADA CON ESTADO
-- ============================================================================

-- Trigger para mantener sincronizados 'finalizada' y 'id_estado'
-- Cuando id_estado = 3 (Finalizada), finalizada = TRUE
-- Cuando id_estado != 3, finalizada = FALSE

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
        SET NEW.finalizada = FALSE;
    END IF;

    -- Si finalizada=TRUE, poner estado en Finalizada (id=3)
    IF NEW.finalizada = TRUE AND NEW.id_estado != 3 THEN
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

-- Vista que incluye todos los nuevos campos con información legible
CREATE OR REPLACE VIEW vw_partes_completo AS
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

-- Poner valores por defecto en registros existentes que no tienen los nuevos campos

-- Establecer estado 'Pendiente' a partes sin estado
UPDATE tbl_partes
SET id_estado = 1
WHERE id_estado IS NULL;

-- Generar descripción_corta desde descripcion si está vacía
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

-- Consulta de verificación: mostrar estructura de la tabla
DESCRIBE tbl_partes;

-- Consulta de verificación: contar registros por estado
SELECT
    pe.nombre AS estado,
    COUNT(*) AS cantidad
FROM tbl_partes p
LEFT JOIN tbl_parte_estados pe ON p.id_estado = pe.id
GROUP BY pe.nombre
ORDER BY pe.orden;

-- Consulta de verificación: listar partes con nuevos campos
SELECT
    codigo,
    titulo,
    descripcion_corta,
    fecha_inicio,
    fecha_fin,
    estado,
    finalizada,
    localizacion
FROM vw_partes_completo
LIMIT 10;

-- ============================================================================
-- FIN DEL SCRIPT
-- ============================================================================

-- NOTAS DE USO:
-- 1. Este script es IDEMPOTENTE: se puede ejecutar múltiples veces sin problemas
-- 2. Usa IF NOT EXISTS para evitar errores si los campos ya existen
-- 3. Los triggers mantienen sincronizados 'finalizada' y 'id_estado'
-- 4. La vista vw_partes_completo facilita consultas con información legible
-- 5. Se crean índices para optimizar consultas frecuentes

-- MIGRACIÓN A PROYECTOS EXISTENTES:
-- Para aplicar estos cambios a un proyecto existente, ejecutar:
--   USE nombre_proyecto;
--   SOURCE mejoras_tabla_partes.sql;

-- VERIFICAR APLICACIÓN:
-- SELECT * FROM tbl_parte_estados;
-- DESCRIBE tbl_partes;
-- SELECT * FROM vw_partes_completo LIMIT 5;
