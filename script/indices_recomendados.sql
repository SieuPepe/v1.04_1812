-- =======================================================================================
-- ÍNDICES RECOMENDADOS PARA OPTIMIZACIÓN DE RENDIMIENTO
-- =======================================================================================
-- Este archivo contiene índices recomendados basados en el análisis de queries frecuentes
-- Ejecutar estos índices puede mejorar significativamente el rendimiento de la aplicación
-- =======================================================================================

-- NOTA: Verificar que los índices no existan antes de crearlos
-- Para verificar: SHOW INDEX FROM tabla_nombre;

-- =======================================================================================
-- ÍNDICES PARA tbl_partes (tabla principal de partes)
-- =======================================================================================

-- Índice compuesto para búsquedas por tipo de trabajo y código
-- Usado en: generación de códigos automáticos, listados filtrados
CREATE INDEX IF NOT EXISTS idx_partes_tipo_codigo ON tbl_partes(tipo_trabajo_id, codigo);

-- Índice para búsquedas por municipio (usado frecuentemente en listados)
-- Ya debe existir: idx_partes_municipio
CREATE INDEX IF NOT EXISTS idx_partes_municipio ON tbl_partes(municipio_id);

-- Índice compuesto para listados ordenados por fecha y estado
-- Usado en: vistas de resumen, listados cronológicos
CREATE INDEX IF NOT EXISTS idx_partes_fecha_estado ON tbl_partes(fecha_inicio DESC, id_estado);

-- Índice para búsqueda por código (consultas frecuentes)
CREATE INDEX IF NOT EXISTS idx_partes_codigo ON tbl_partes(codigo);

-- =======================================================================================
-- ÍNDICES PARA tbl_part_presupuesto (presupuestos de partes)
-- =======================================================================================

-- Índice compuesto para agregaciones de presupuesto por parte
-- Usado en: get_parts_list(), get_partes_resumen() - queries con SUM y GROUP BY
CREATE INDEX IF NOT EXISTS idx_part_presupuesto_parte_precio ON tbl_part_presupuesto(parte_id, precio_id, cantidad, precio_unit);

-- Índice simple por parte_id (ya debe existir como FK)
CREATE INDEX IF NOT EXISTS idx_part_presupuesto_parte ON tbl_part_presupuesto(parte_id);

-- =======================================================================================
-- ÍNDICES PARA tbl_part_certificacion (certificaciones)
-- =======================================================================================

-- Índice compuesto para agregaciones de certificaciones
-- Usado en: get_parts_list(), get_partes_resumen() - queries con SUM CASE
CREATE INDEX IF NOT EXISTS idx_part_cert_parte_certificada ON tbl_part_certificacion(parte_id, certificada, cantidad_cert, precio_unit);

-- Índice para búsqueda de certificaciones pendientes
CREATE INDEX IF NOT EXISTS idx_part_cert_pendientes ON tbl_part_certificacion(certificada, parte_id);

-- =======================================================================================
-- ÍNDICES PARA dim_municipios (municipios)
-- =======================================================================================

-- Índice para JOINs con comarcas y provincias
-- Usado en: get_parts_list(), get_partes_resumen() - JOINs frecuentes
CREATE INDEX IF NOT EXISTS idx_municipios_comarca ON dim_municipios(comarca_id);
CREATE INDEX IF NOT EXISTS idx_municipios_provincia ON dim_municipios(provincia_id);

-- =======================================================================================
-- ÍNDICES PARA tablas dimensionales
-- =======================================================================================

-- Índices en tablas de dimensiones para JOINs rápidos
-- Estas tablas son pequeñas pero se usan en JOINs constantemente

-- dim_red
CREATE INDEX IF NOT EXISTS idx_red_descripcion ON dim_red(descripcion);

-- dim_tipo_trabajo
CREATE INDEX IF NOT EXISTS idx_tipo_trabajo_descripcion ON dim_tipo_trabajo(descripcion);

-- dim_codigo_trabajo
CREATE INDEX IF NOT EXISTS idx_codigo_trabajo_descripcion ON dim_codigo_trabajo(descripcion);

-- dim_tipos_rep
CREATE INDEX IF NOT EXISTS idx_tipos_rep_descripcion ON dim_tipos_rep(descripcion);

-- =======================================================================================
-- ÍNDICES PARA tbl_parte_estados
-- =======================================================================================

-- Índice por nombre para búsquedas de estado
CREATE INDEX IF NOT EXISTS idx_parte_estados_nombre ON tbl_parte_estados(nombre);

-- =======================================================================================
-- ANÁLISIS Y MANTENIMIENTO RECOMENDADO
-- =======================================================================================

-- Después de crear los índices, analizar las tablas para actualizar estadísticas
-- Esto ayuda al optimizador de MySQL a elegir los mejores planes de ejecución

ANALYZE TABLE tbl_partes;
ANALYZE TABLE tbl_part_presupuesto;
ANALYZE TABLE tbl_part_certificacion;
ANALYZE TABLE dim_municipios;

-- =======================================================================================
-- VERIFICACIÓN DE ÍNDICES CREADOS
-- =======================================================================================

-- Verificar índices en tbl_partes
SELECT
    INDEX_NAME,
    COLUMN_NAME,
    SEQ_IN_INDEX,
    CARDINALITY,
    INDEX_TYPE
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'tbl_partes'
ORDER BY INDEX_NAME, SEQ_IN_INDEX;

-- =======================================================================================
-- NOTAS ADICIONALES
-- =======================================================================================

/*
1. IMPACTO EN ESCRITURA:
   - Los índices mejoran la velocidad de lectura pero pueden ralentizar ligeramente las inserciones
   - En esta aplicación, las lecturas son mucho más frecuentes que las escrituras
   - El impacto en inserciones es mínimo comparado con la mejora en consultas

2. MANTENIMIENTO:
   - MySQL mantiene los índices automáticamente
   - Ejecutar ANALYZE TABLE periódicamente (mensual) para actualizar estadísticas
   - Monitorear el tamaño de los índices: SELECT * FROM information_schema.TABLES WHERE TABLE_SCHEMA = DATABASE();

3. ÍNDICES COMPUESTOS:
   - El orden de las columnas en un índice compuesto es importante
   - La primera columna debe ser la más selectiva o la más usada en WHERE/JOIN
   - Estos índices pueden usarse para consultas que filtren solo por la primera columna

4. COVERING INDEXES:
   - Algunos índices incluyen columnas adicionales para "cubrir" la consulta completa
   - Esto elimina la necesidad de acceder a la tabla principal (index-only scan)
   - Ejemplo: idx_part_presupuesto_parte_precio incluye cantidad y precio_unit

5. CUÁNDO RECREAR ÍNDICES:
   - Si las tablas crecen significativamente (>100K filas)
   - Si el rendimiento se degrada con el tiempo
   - Comando: ALTER TABLE tabla_nombre DROP INDEX idx_nombre, ADD INDEX idx_nombre(...);
*/
