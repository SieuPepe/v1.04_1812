-- ============================================================================
-- Script para recrear la vista vw_partes_resumen sin campos obsoletos
-- Elimina referencias a codigo_ot, fecha_prevista_fin y campo ot redundante
--
-- USO:
-- mysql -u root -phydroflow cert_dev < recrear_vw_partes_resumen.sql
-- mysql -u root -phydroflow proyecto_tipo < recrear_vw_partes_resumen.sql
-- ============================================================================

SET @schema_name = DATABASE();

SELECT CONCAT('Recreando vista vw_partes_resumen en esquema: ', @schema_name) AS Info;

-- Eliminar vista anterior si existe
DROP VIEW IF EXISTS vw_partes_resumen;

-- Crear vista sin campos obsoletos (sin ot, sin codigo_ot, sin fecha_prevista_fin)
CREATE OR REPLACE VIEW vw_partes_resumen AS
SELECT
    p.id,
    p.codigo,
    p.descripcion,
    p.estado,
    COALESCE(rd.red_codigo, '') AS red,
    COALESCE(tt.tipo_codigo, '') AS tipo,
    COALESCE(ct.cod_trabajo, '') AS cod_trabajo,
    COALESCE(SUM(pp.cantidad * pp.precio_unit), 0) AS total_presupuesto,
    COALESCE(SUM(CASE WHEN pc.certificada = 1 THEN pc.cantidad_cert * pc.precio_unit ELSE 0 END), 0) AS total_certificado,
    COALESCE(SUM(pp.cantidad * pp.precio_unit), 0) - COALESCE(SUM(CASE WHEN pc.certificada = 1 THEN pc.cantidad_cert * pc.precio_unit ELSE 0 END), 0) AS total_pendiente,
    p.creado_en,
    p.actualizado_en
FROM tbl_partes p
LEFT JOIN dim_red rd ON rd.id = p.red_id
LEFT JOIN dim_tipo_trabajo tt ON tt.id = p.tipo_trabajo_id
LEFT JOIN dim_codigo_trabajo ct ON ct.id = p.cod_trabajo_id
LEFT JOIN tbl_part_presupuesto pp ON pp.parte_id = p.id
LEFT JOIN tbl_part_certificacion pc ON pc.parte_id = p.id
GROUP BY p.id, p.codigo, p.descripcion, p.estado, rd.red_codigo, tt.tipo_codigo, ct.cod_trabajo, p.creado_en, p.actualizado_en;

SELECT '✓ Vista vw_partes_resumen recreada correctamente' AS Resultado;
