-- ============================================================================
-- Script MAESTRO para recrear TODAS las vistas afectadas
-- Ejecuta la recreación de vw_partes_resumen y vw_part_certificaciones
-- Elimina campos obsoletos: codigo_ot, fecha_prevista_fin, campo "ot"
--
-- USO:
-- mysql -u root -phydroflow cert_dev < recrear_todas_vistas.sql
-- mysql -u root -phydroflow proyecto_tipo < recrear_todas_vistas.sql
-- ============================================================================

SET @schema_name = DATABASE();

SELECT '============================================================' AS '';
SELECT CONCAT('Recreando TODAS las vistas en esquema: ', @schema_name) AS '';
SELECT '============================================================' AS '';

-- ============================================================================
-- 1. Vista vw_partes_resumen
-- ============================================================================
SELECT '' AS '';
SELECT '1. Recreando vw_partes_resumen...' AS '';

-- Detectar si existen las columnas timestamp en tbl_partes
SET @has_partes_creado = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'tbl_partes'
    AND COLUMN_NAME = 'creado_en'
);

SET @has_partes_actualizado = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'tbl_partes'
    AND COLUMN_NAME = 'actualizado_en'
);

-- Construir columnas y GROUP BY dinámicamente
SET @partes_creado_col = IF(@has_partes_creado > 0, 'p.creado_en', 'NULL as creado_en');
SET @partes_actualizado_col = IF(@has_partes_actualizado > 0, 'p.actualizado_en', 'NULL as actualizado_en');
SET @group_by_cols = 'p.id, p.codigo, p.descripcion, p.estado, rd.red_codigo, tt.tipo_codigo, ct.cod_trabajo';
SET @group_by_cols = IF(@has_partes_creado > 0, CONCAT(@group_by_cols, ', p.creado_en'), @group_by_cols);
SET @group_by_cols = IF(@has_partes_actualizado > 0, CONCAT(@group_by_cols, ', p.actualizado_en'), @group_by_cols);

SET @sql_view_resumen = CONCAT('
CREATE OR REPLACE VIEW vw_partes_resumen AS
SELECT
    p.id,
    p.codigo,
    p.descripcion,
    p.estado,
    COALESCE(rd.red_codigo, '''') AS red,
    COALESCE(tt.tipo_codigo, '''') AS tipo,
    COALESCE(ct.cod_trabajo, '''') AS cod_trabajo,
    COALESCE(SUM(pp.cantidad * pp.precio_unit), 0) AS total_presupuesto,
    COALESCE(SUM(CASE WHEN pc.certificada = 1 THEN pc.cantidad_cert * pc.precio_unit ELSE 0 END), 0) AS total_certificado,
    COALESCE(SUM(pp.cantidad * pp.precio_unit), 0) - COALESCE(SUM(CASE WHEN pc.certificada = 1 THEN pc.cantidad_cert * pc.precio_unit ELSE 0 END), 0) AS total_pendiente,
    ', @partes_creado_col, ',
    ', @partes_actualizado_col, '
FROM tbl_partes p
LEFT JOIN dim_red rd ON rd.id = p.red_id
LEFT JOIN dim_tipo_trabajo tt ON tt.id = p.tipo_trabajo_id
LEFT JOIN dim_codigo_trabajo ct ON ct.id = p.cod_trabajo_id
LEFT JOIN tbl_part_presupuesto pp ON pp.parte_id = p.id
LEFT JOIN tbl_part_certificacion pc ON pc.parte_id = p.id
GROUP BY ', @group_by_cols
);

DROP VIEW IF EXISTS vw_partes_resumen;

PREPARE stmt FROM @sql_view_resumen;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SELECT '   ✓ vw_partes_resumen recreada' AS '';

-- ============================================================================
-- 2. Vista vw_part_certificaciones
-- ============================================================================
SELECT '' AS '';
SELECT '2. Recreando vw_part_certificaciones...' AS '';

-- Detectar si existe la columna creado_en en tbl_part_certificacion
SET @has_cert_creado = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'tbl_part_certificacion'
    AND COLUMN_NAME = 'creado_en'
);

-- Construir la vista según si existe o no la columna creado_en
SET @cert_creado_col = IF(@has_cert_creado > 0, 'pc.creado_en', 'NULL as creado_en');

SET @sql_view_cert = CONCAT('
CREATE OR REPLACE VIEW vw_part_certificaciones AS
SELECT
    pc.id,
    pc.parte_id,
    p.codigo AS codigo_parte,
    pr.codigo AS codigo_partida,
    pr.resumen,
    u.unidad,
    pc.cantidad_cert,
    pc.precio_unit,
    (pc.cantidad_cert * pc.precio_unit) AS coste_cert,
    pc.fecha_certificacion,
    pc.certificada,
    COALESCE(rd.red_codigo, '''') AS red,
    COALESCE(tt.tipo_codigo, '''') AS tipo,
    COALESCE(ct.cod_trabajo, '''') AS cod_trabajo,
    ', @cert_creado_col, '
FROM tbl_part_certificacion pc
INNER JOIN tbl_partes p ON p.id = pc.parte_id
INNER JOIN tbl_pres_precios pr ON pr.id = pc.precio_id
LEFT JOIN tbl_pres_unidades u ON u.id = pr.id_unidades
LEFT JOIN dim_red rd ON rd.id = p.red_id
LEFT JOIN dim_tipo_trabajo tt ON tt.id = p.tipo_trabajo_id
LEFT JOIN dim_codigo_trabajo ct ON ct.id = p.cod_trabajo_id
');

DROP VIEW IF EXISTS vw_part_certificaciones;

PREPARE stmt FROM @sql_view_cert;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SELECT '   ✓ vw_part_certificaciones recreada' AS '';

-- ============================================================================
-- Resumen final
-- ============================================================================
SELECT '' AS '';
SELECT '============================================================' AS '';
SELECT '✓✓✓ TODAS LAS VISTAS RECREADAS CORRECTAMENTE ✓✓✓' AS '';
SELECT '============================================================' AS '';
SELECT '' AS '';
SELECT 'Vistas recreadas:' AS '';
SELECT '  - vw_partes_resumen' AS '';
SELECT '  - vw_part_certificaciones' AS '';
SELECT '' AS '';
SELECT 'Campos eliminados de las vistas:' AS '';
SELECT '  - codigo_ot (obsoleto)' AS '';
SELECT '  - ot (campo redundante)' AS '';
SELECT '  - fecha_prevista_fin (obsoleto)' AS '';
SELECT '' AS '';
