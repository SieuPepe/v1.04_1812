-- ============================================================================
-- SCRIPT DE VERIFICACIÓN MANUAL POST-MIGRACIÓN
-- Ejecutar en MySQL Workbench después de la migración
-- ============================================================================

-- INSTRUCCIONES:
-- 1. Conecta a tu esquema: USE cert_dev; (o el esquema que estés probando)
-- 2. Ejecuta cada sección por separado
-- 3. Revisa los resultados de cada consulta

-- ============================================================================
-- 1. VERIFICAR NUEVAS COLUMNAS EN tbl_partes
-- ============================================================================

SELECT
    COLUMN_NAME AS columna,
    COLUMN_TYPE AS tipo,
    IS_NULLABLE AS permite_nulos,
    COLUMN_DEFAULT AS valor_defecto,
    COLUMN_COMMENT AS comentario
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
AND TABLE_NAME = 'tbl_partes'
AND COLUMN_NAME IN (
    'titulo', 'descripcion_larga', 'descripcion_corta',
    'fecha_inicio', 'fecha_fin', 'fecha_prevista_fin',
    'id_estado', 'finalizada', 'localizacion', 'id_municipio'
)
ORDER BY ORDINAL_POSITION;

-- Resultado esperado: 10 filas (una por cada columna nueva)

-- ============================================================================
-- 2. VERIFICAR TABLA DE ESTADOS
-- ============================================================================

-- Verificar que existe la tabla
SELECT COUNT(*) AS tabla_existe
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = DATABASE()
AND TABLE_NAME = 'tbl_parte_estados';

-- Resultado esperado: 1

-- Ver los estados insertados
SELECT
    id,
    nombre,
    descripcion,
    orden,
    activo
FROM tbl_parte_estados
ORDER BY orden;

-- Resultado esperado: 5 estados
-- 1. Pendiente
-- 2. En curso
-- 3. Finalizada
-- 4. Cancelada
-- 5. Suspendida

-- ============================================================================
-- 3. VERIFICAR VISTA vw_partes_completo
-- ============================================================================

-- Verificar que existe la vista
SELECT COUNT(*) AS vista_existe
FROM information_schema.VIEWS
WHERE TABLE_SCHEMA = DATABASE()
AND TABLE_NAME = 'vw_partes_completo';

-- Resultado esperado: 1

-- Ver primeros registros de la vista
SELECT
    id,
    codigo,
    titulo,
    descripcion_corta,
    fecha_inicio,
    fecha_fin,
    estado,
    finalizada,
    localizacion,
    municipio
FROM vw_partes_completo
LIMIT 10;

-- ============================================================================
-- 4. VERIFICAR TRIGGERS
-- ============================================================================

SELECT
    TRIGGER_NAME AS nombre_trigger,
    EVENT_MANIPULATION AS evento,
    ACTION_TIMING AS momento
FROM information_schema.TRIGGERS
WHERE TRIGGER_SCHEMA = DATABASE()
AND EVENT_OBJECT_TABLE = 'tbl_partes'
AND TRIGGER_NAME LIKE '%sync_finalizada%'
ORDER BY TRIGGER_NAME;

-- Resultado esperado: 2 triggers
-- - trg_partes_sync_finalizada_insert (INSERT, BEFORE)
-- - trg_partes_sync_finalizada_update (UPDATE, BEFORE)

-- ============================================================================
-- 5. VERIFICAR ÍNDICES
-- ============================================================================

SELECT
    INDEX_NAME AS nombre_indice,
    GROUP_CONCAT(COLUMN_NAME ORDER BY SEQ_IN_INDEX) AS columnas,
    NON_UNIQUE AS no_unico,
    INDEX_TYPE AS tipo
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = DATABASE()
AND TABLE_NAME = 'tbl_partes'
AND INDEX_NAME LIKE 'idx_partes_%'
GROUP BY INDEX_NAME, NON_UNIQUE, INDEX_TYPE
ORDER BY INDEX_NAME;

-- Resultado esperado: Al menos 6 índices nuevos
-- - idx_partes_estado
-- - idx_partes_finalizada
-- - idx_partes_fecha_inicio
-- - idx_partes_fecha_fin
-- - idx_partes_municipio
-- - idx_partes_estado_fecha

-- ============================================================================
-- 6. VERIFICAR CLAVES FORÁNEAS
-- ============================================================================

SELECT
    CONSTRAINT_NAME AS nombre_fk,
    COLUMN_NAME AS columna,
    REFERENCED_TABLE_NAME AS tabla_referenciada,
    REFERENCED_COLUMN_NAME AS columna_referenciada
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = DATABASE()
AND TABLE_NAME = 'tbl_partes'
AND CONSTRAINT_NAME LIKE 'fk_partes_%'
ORDER BY CONSTRAINT_NAME;

-- Resultado esperado: Al menos 1 FK
-- - fk_partes_estado (id_estado -> tbl_parte_estados.id)
-- - fk_partes_municipio (id_municipio -> tbl_municipios.id) - solo si existe tbl_municipios

-- ============================================================================
-- 7. VERIFICAR INTEGRIDAD DE DATOS
-- ============================================================================

-- Contar registros totales
SELECT COUNT(*) AS total_partes
FROM tbl_partes;

-- Ver distribución por estado
SELECT
    COALESCE(pe.nombre, 'Sin estado') AS estado,
    COUNT(*) AS cantidad,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM tbl_partes), 2) AS porcentaje
FROM tbl_partes p
LEFT JOIN tbl_parte_estados pe ON p.id_estado = pe.id
GROUP BY pe.nombre, pe.orden
ORDER BY pe.orden;

-- Ver registros con nuevos campos poblados
SELECT
    COUNT(*) AS total,
    COUNT(titulo) AS con_titulo,
    COUNT(descripcion_larga) AS con_desc_larga,
    COUNT(descripcion_corta) AS con_desc_corta,
    COUNT(fecha_inicio) AS con_fecha_inicio,
    COUNT(fecha_fin) AS con_fecha_fin,
    COUNT(localizacion) AS con_localizacion
FROM tbl_partes;

-- ============================================================================
-- 8. PRUEBA DE TRIGGER (OPCIONAL)
-- ============================================================================

-- IMPORTANTE: Esta sección MODIFICA DATOS. Solo ejecutar si quieres probar.
-- Comenta o descomenta según necesites.

/*
-- Insertar un parte de prueba
INSERT INTO tbl_partes (
    codigo,
    id_ot,
    id_red,
    id_tipo_trabajo,
    id_cod_trabajo,
    titulo,
    descripcion_corta,
    id_estado,
    fecha_inicio
) VALUES (
    'TEST-001',
    1,  -- Ajustar con un ID válido
    1,  -- Ajustar con un ID válido
    1,  -- Ajustar con un ID válido
    1,  -- Ajustar con un ID válido
    'Prueba de migración',
    'Parte de prueba para verificar triggers',
    1,  -- Pendiente
    CURDATE()
);

-- Verificar que finalizada = FALSE (porque id_estado = 1)
SELECT id, codigo, titulo, id_estado, finalizada
FROM tbl_partes
WHERE codigo = 'TEST-001';

-- Cambiar estado a Finalizada (id = 3)
UPDATE tbl_partes
SET id_estado = 3
WHERE codigo = 'TEST-001';

-- Verificar que finalizada cambió a TRUE automáticamente
SELECT id, codigo, titulo, id_estado, finalizada, fecha_fin
FROM tbl_partes
WHERE codigo = 'TEST-001';

-- LIMPIAR: Eliminar parte de prueba
DELETE FROM tbl_partes WHERE codigo = 'TEST-001';
*/

-- ============================================================================
-- FIN DE VERIFICACIONES
-- ============================================================================

-- Si todas las consultas anteriores devolvieron los resultados esperados,
-- la migración se completó exitosamente.

-- Próximo paso: Probar las funciones Python con el script test_migration_complete.py
