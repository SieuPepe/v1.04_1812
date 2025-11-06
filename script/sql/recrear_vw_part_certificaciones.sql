-- ============================================================================
-- Script para recrear la vista vw_part_certificaciones sin campo ot obsoleto
-- Elimina campo "ot" redundante (era p.codigo AS ot)
--
-- USO:
-- mysql -u root -phydroflow cert_dev < recrear_vw_part_certificaciones.sql
-- mysql -u root -phydroflow proyecto_tipo < recrear_vw_part_certificaciones.sql
-- ============================================================================

SET @schema_name = DATABASE();

SELECT CONCAT('Recreando vista vw_part_certificaciones en esquema: ', @schema_name) AS Info;

-- Detectar si existe la columna creado_en en tbl_part_certificacion
SET @has_creado_en = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'tbl_part_certificacion'
    AND COLUMN_NAME = 'creado_en'
);

-- Construir la vista según si existe o no la columna creado_en
SET @sql_view = CONCAT('
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
    COALESCE(rd.descripcion, '''') AS red,
    COALESCE(tt.descripcion, '''') AS tipo,
    COALESCE(ct.descripcion, '''') AS cod_trabajo,
    ', IF(@has_creado_en > 0, 'pc.creado_en', 'NULL as creado_en'), '
FROM tbl_part_certificacion pc
INNER JOIN tbl_partes p ON p.id = pc.parte_id
INNER JOIN tbl_pres_precios pr ON pr.id = pc.precio_id
LEFT JOIN tbl_pres_unidades u ON u.id = pr.id_unidades
LEFT JOIN dim_red rd ON rd.id = p.red_id
LEFT JOIN dim_tipo_trabajo tt ON tt.id = p.tipo_trabajo_id
LEFT JOIN dim_codigo_trabajo ct ON ct.id = p.cod_trabajo_id
');

-- Eliminar vista anterior si existe
DROP VIEW IF EXISTS vw_part_certificaciones;

-- Ejecutar el SQL dinámico
PREPARE stmt FROM @sql_view;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SELECT '✓ Vista vw_part_certificaciones recreada correctamente' AS Resultado;
