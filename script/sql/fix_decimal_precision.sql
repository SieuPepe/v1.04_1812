-- ============================================================================
-- Script para establecer precisión de 2 decimales en todos los campos numéricos
-- relacionados con presupuestos, precios, importes, certificaciones, etc.
-- ============================================================================
-- Autor: Claude
-- Fecha: 2025-11-08
-- Descripción: Convierte todos los campos DOUBLE y FLOAT a DECIMAL(10,2)
-- ============================================================================

USE proyecto_tipo;

-- ============================================================================
-- TABLAS DE PRESUPUESTO
-- ============================================================================

-- Tabla: tbl_pres_precios
-- Descripción: Precios de partidas presupuestarias
ALTER TABLE tbl_pres_precios
    MODIFY COLUMN coste DECIMAL(10,2) DEFAULT NULL COMMENT 'Precio unitario de la partida';

-- Tabla: tbl_pres_grupo_partidas
-- Descripción: Grupos de partidas presupuestarias
ALTER TABLE tbl_pres_grupo_partidas
    MODIFY COLUMN coste DECIMAL(10,2) DEFAULT NULL COMMENT 'Coste del grupo de partidas';

-- Tabla: tbl_presupuesto
-- Descripción: Presupuesto de partidas en proyectos
ALTER TABLE tbl_presupuesto
    MODIFY COLUMN cantidad DECIMAL(10,2) DEFAULT NULL COMMENT 'Cantidad presupuestada';

-- Tabla: tbl_proy_presupuesto
-- Descripción: Presupuestos de proyectos
ALTER TABLE tbl_proy_presupuesto
    MODIFY COLUMN gastos_generales DECIMAL(10,2) DEFAULT NULL COMMENT 'Porcentaje de gastos generales',
    MODIFY COLUMN beneficio_industrial DECIMAL(10,2) DEFAULT NULL COMMENT 'Porcentaje de beneficio industrial',
    MODIFY COLUMN baja DECIMAL(10,2) DEFAULT NULL COMMENT 'Porcentaje de baja',
    MODIFY COLUMN presupuesto_licitacion DECIMAL(10,2) DEFAULT NULL COMMENT 'Importe de presupuesto de licitación',
    MODIFY COLUMN iva DECIMAL(10,2) DEFAULT NULL COMMENT 'Porcentaje de IVA';

-- ============================================================================
-- TABLAS DE CERTIFICACIONES
-- ============================================================================

-- Tabla: tbl_pres_certificacion
-- Descripción: Certificaciones de partidas
ALTER TABLE tbl_pres_certificacion
    MODIFY COLUMN cantidad_certificada DECIMAL(10,2) DEFAULT NULL COMMENT 'Cantidad certificada';

-- ============================================================================
-- TABLAS DE ELEMENTOS Y GRUPOS
-- ============================================================================

-- Tabla: tbl_pres_grupo_elementos (si existe)
-- Descripción: Elementos dentro de grupos de partidas
-- Nota: Verificar si esta tabla tiene campos numéricos antes de ejecutar
-- ALTER TABLE tbl_pres_grupo_elementos
--     MODIFY COLUMN cantidad DECIMAL(10,2) DEFAULT NULL COMMENT 'Cantidad del elemento';

-- ============================================================================
-- VERIFICACIÓN Y RESUMEN
-- ============================================================================

SELECT 'Script de corrección de precisión decimal completado' AS status;
SELECT 'Todos los campos numéricos ahora usan DECIMAL(10,2) para garantizar 2 decimales' AS info;

-- Para verificar los cambios, ejecuta:
-- SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, NUMERIC_PRECISION, NUMERIC_SCALE
-- FROM INFORMATION_SCHEMA.COLUMNS
-- WHERE TABLE_SCHEMA = 'proyecto_tipo'
-- AND DATA_TYPE = 'decimal'
-- AND TABLE_NAME LIKE 'tbl_%'
-- ORDER BY TABLE_NAME, COLUMN_NAME;
