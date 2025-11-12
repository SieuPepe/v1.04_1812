-- =====================================================================================
-- Script de Verificación de Conexión y Datos
-- Para ejecutar en MySQL Workbench
-- =====================================================================================

-- 1. Información de la conexión actual
SELECT
    '=== INFORMACIÓN DE CONEXIÓN ===' AS '';

SELECT
    DATABASE() AS 'Esquema Actual',
    USER() AS 'Usuario Conectado',
    VERSION() AS 'Versión MySQL',
    @@hostname AS 'Hostname',
    @@port AS 'Puerto';

-- 2. Listar todos los esquemas disponibles
SELECT
    '=== ESQUEMAS DISPONIBLES ===' AS '';

SELECT
    SCHEMA_NAME AS 'Nombre del Esquema'
FROM information_schema.SCHEMATA
WHERE SCHEMA_NAME NOT IN ('information_schema', 'mysql', 'performance_schema', 'sys')
ORDER BY SCHEMA_NAME;

-- 3. Buscar tbl_partes en todos los esquemas
SELECT
    '=== UBICACIÓN DE tbl_partes ===' AS '';

SELECT
    TABLE_SCHEMA AS 'Esquema',
    TABLE_NAME AS 'Tabla',
    TABLE_ROWS AS 'Registros Aproximados',
    CREATE_TIME AS 'Fecha Creación',
    UPDATE_TIME AS 'Última Actualización'
FROM information_schema.TABLES
WHERE TABLE_NAME = 'tbl_partes'
ORDER BY TABLE_SCHEMA;

-- 4. Contar registros EXACTOS en cert_dev.tbl_partes
SELECT
    '=== REGISTROS EN cert_dev.tbl_partes ===' AS '';

SELECT COUNT(*) AS 'Total de Registros'
FROM cert_dev.tbl_partes;

-- 5. Mostrar primeros 10 registros
SELECT
    '=== PRIMEROS 10 REGISTROS ===' AS '';

SELECT
    id,
    codigo,
    titulo,
    fecha_inicio
FROM cert_dev.tbl_partes
ORDER BY id
LIMIT 10;

-- 6. Buscar códigos específicos del Excel
SELECT
    '=== BUSCAR CÓDIGOS DEL EXCEL ===' AS '';

SELECT
    codigo,
    id,
    titulo
FROM cert_dev.tbl_partes
WHERE codigo IN ('OT/0121', 'OT/0453', 'OT/0425', 'GF/0001', 'GF/0002', 'TP/0278')
ORDER BY codigo;

-- 7. Contar códigos por prefijo
SELECT
    '=== ESTADÍSTICAS POR PREFIJO ===' AS '';

SELECT
    SUBSTRING_INDEX(codigo, '/', 1) AS 'Prefijo',
    COUNT(*) AS 'Cantidad'
FROM cert_dev.tbl_partes
WHERE codigo IS NOT NULL
GROUP BY SUBSTRING_INDEX(codigo, '/', 1)
ORDER BY COUNT(*) DESC;

-- 8. Verificar estructura de la tabla
SELECT
    '=== ESTRUCTURA DE tbl_partes ===' AS '';

DESCRIBE cert_dev.tbl_partes;

-- FIN DEL SCRIPT
SELECT
    '=== VERIFICACIÓN COMPLETADA ===' AS '';
