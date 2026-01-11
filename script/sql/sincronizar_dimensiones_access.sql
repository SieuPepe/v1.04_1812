-- ============================================================================
-- SINCRONIZACIÓN DE DIMENSIONES CON BD ACCESS
-- ============================================================================
-- Este script actualiza las tablas de dimensiones MySQL para que coincidan
-- con la base de datos Access: APLICACION CERTIFICACIONES UTE REDES URBIDE.accdb
--
-- Tablas afectadas:
--   1. dim_tipo_trabajo (TIPO DE TRABAJOS)
--   2. dim_red (valores únicos de RED)
--   3. tbl_pres_unidades (UNIDADES únicas de PRECIOS UNITARIOS)
--   4. tbl_pres_capitulos (CAPITULOS únicos de PRECIOS UNITARIOS)
--
-- Tablas NO afectadas (ya correctas):
--   - dim_codigo_trabajo (los 22 registros coinciden)
--
-- USO:
--   mysql -u [usuario] -p [esquema] < sincronizar_dimensiones_access.sql
-- ============================================================================

-- Mostrar esquema actual
SELECT DATABASE() AS esquema_actual;
SELECT '=== INICIO SINCRONIZACIÓN DIMENSIONES ===' AS info;

-- ============================================================================
-- 1. CORREGIR dim_tipo_trabajo
-- ============================================================================
-- Access tiene:
--   ID 1 = ORDEN DE TRABAJO (OT/)
--   ID 2 = TRABAJOS PROGRAMADOS (TP/)
--   ID 3 = GASTOS FIJOS DE LA EXPLOTACIÓN (GF/)
-- ============================================================================

SELECT '>>> Actualizando dim_tipo_trabajo...' AS paso;

-- Verificar si la columna tipo_codigo existe
SET @tiene_tipo_codigo = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'dim_tipo_trabajo'
    AND COLUMN_NAME = 'tipo_codigo'
);

-- Agregar columna tipo_codigo si no existe
SET @sql = IF(@tiene_tipo_codigo = 0,
    'ALTER TABLE dim_tipo_trabajo ADD COLUMN tipo_codigo VARCHAR(10) AFTER codigo',
    'SELECT "Columna tipo_codigo ya existe" AS info'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Limpiar tabla y reinsertar con IDs correctos del Access
SET FOREIGN_KEY_CHECKS = 0;

DELETE FROM dim_tipo_trabajo;

INSERT INTO dim_tipo_trabajo (id, codigo, tipo_codigo, descripcion, activo) VALUES
(1, '1', 'OT', 'ORDEN DE TRABAJO', 1),
(2, '2', 'TP', 'TRABAJOS PROGRAMADOS', 1),
(3, '3', 'GF', 'GASTOS FIJOS DE LA EXPLOTACIÓN', 1);

SET FOREIGN_KEY_CHECKS = 1;

SELECT 'dim_tipo_trabajo actualizada:' AS resultado;
SELECT * FROM dim_tipo_trabajo ORDER BY id;

-- ============================================================================
-- 2. ACTUALIZAR dim_red
-- ============================================================================
-- Access tiene estos valores únicos en el campo RED:
--   DISTRIBUCIÓN, SANEAMIENTO, ADUCCIÓN, DEPURACIÓN, OTROS
-- ============================================================================

SELECT '>>> Actualizando dim_red...' AS paso;

SET FOREIGN_KEY_CHECKS = 0;

DELETE FROM dim_red;
ALTER TABLE dim_red AUTO_INCREMENT = 1;

INSERT INTO dim_red (id, codigo, descripcion, activo) VALUES
(1, 'DIST', 'DISTRIBUCIÓN', 1),
(2, 'SAN', 'SANEAMIENTO', 1),
(3, 'ADUC', 'ADUCCIÓN', 1),
(4, 'DEP', 'DEPURACIÓN', 1),
(5, 'OTROS', 'OTROS', 1);

SET FOREIGN_KEY_CHECKS = 1;

SELECT 'dim_red actualizada:' AS resultado;
SELECT * FROM dim_red ORDER BY id;

-- ============================================================================
-- 3. ACTUALIZAR tbl_pres_unidades
-- ============================================================================
-- Access tiene estas unidades: día, h, kg, l, m2, m3, mes, ml, tn, ud
-- ============================================================================

SELECT '>>> Actualizando tbl_pres_unidades...' AS paso;

-- Verificar si la tabla existe
SET @tabla_existe = (
    SELECT COUNT(*)
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'tbl_pres_unidades'
);

-- Crear tabla si no existe
SET @sql = IF(@tabla_existe = 0,
    'CREATE TABLE tbl_pres_unidades (
        id INT AUTO_INCREMENT PRIMARY KEY,
        unidad VARCHAR(20) NOT NULL UNIQUE,
        descripcion VARCHAR(100),
        activo TINYINT DEFAULT 1
    )',
    'SELECT "Tabla tbl_pres_unidades ya existe" AS info'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Insertar unidades (ON DUPLICATE KEY para evitar errores si ya existen)
INSERT INTO tbl_pres_unidades (unidad, descripcion, activo) VALUES
('ud', 'Unidad', 1),
('h', 'Hora', 1),
('día', 'Día', 1),
('mes', 'Mes', 1),
('m2', 'Metro cuadrado', 1),
('m3', 'Metro cúbico', 1),
('ml', 'Metro lineal', 1),
('kg', 'Kilogramo', 1),
('tn', 'Tonelada', 1),
('l', 'Litro', 1)
ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion), activo = 1;

SELECT 'tbl_pres_unidades actualizada:' AS resultado;
SELECT * FROM tbl_pres_unidades ORDER BY id;

-- ============================================================================
-- 4. ACTUALIZAR tbl_pres_capitulos
-- ============================================================================
-- Access tiene estos capítulos: Contador, Gastos Fijos, Maquinaria,
--                               Material, Personal, Precio contradictorio
-- ============================================================================

SELECT '>>> Actualizando tbl_pres_capitulos...' AS paso;

-- Verificar si la tabla existe
SET @tabla_existe = (
    SELECT COUNT(*)
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'tbl_pres_capitulos'
);

-- Si existe, verificar columnas necesarias
SET @tiene_codigo = 0;
SET @tiene_capitulo = 0;

SET @sql = IF(@tabla_existe > 0,
    CONCAT(
        'SELECT ',
        '(SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = ''tbl_pres_capitulos'' AND COLUMN_NAME = ''codigo_capitulo'') INTO @tiene_codigo'
    ),
    'SELECT 0 INTO @tiene_codigo'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Insertar capítulos basados en Access
-- Primero asegurarnos de que existen los capítulos necesarios
INSERT INTO tbl_pres_capitulos (codigo_capitulo, capitulo, id_naturaleza)
SELECT '01', 'Personal', 1
WHERE NOT EXISTS (SELECT 1 FROM tbl_pres_capitulos WHERE capitulo = 'Personal');

INSERT INTO tbl_pres_capitulos (codigo_capitulo, capitulo, id_naturaleza)
SELECT '02', 'Material', 1
WHERE NOT EXISTS (SELECT 1 FROM tbl_pres_capitulos WHERE capitulo = 'Material');

INSERT INTO tbl_pres_capitulos (codigo_capitulo, capitulo, id_naturaleza)
SELECT '03', 'Maquinaria', 1
WHERE NOT EXISTS (SELECT 1 FROM tbl_pres_capitulos WHERE capitulo = 'Maquinaria');

INSERT INTO tbl_pres_capitulos (codigo_capitulo, capitulo, id_naturaleza)
SELECT '04', 'Contador', 1
WHERE NOT EXISTS (SELECT 1 FROM tbl_pres_capitulos WHERE capitulo = 'Contador');

INSERT INTO tbl_pres_capitulos (codigo_capitulo, capitulo, id_naturaleza)
SELECT '05', 'Gastos Fijos', 1
WHERE NOT EXISTS (SELECT 1 FROM tbl_pres_capitulos WHERE capitulo = 'Gastos Fijos');

INSERT INTO tbl_pres_capitulos (codigo_capitulo, capitulo, id_naturaleza)
SELECT '06', 'Precio contradictorio', 1
WHERE NOT EXISTS (SELECT 1 FROM tbl_pres_capitulos WHERE capitulo = 'Precio contradictorio');

SELECT 'tbl_pres_capitulos actualizada:' AS resultado;
SELECT id, codigo_capitulo, capitulo FROM tbl_pres_capitulos ORDER BY id;

-- ============================================================================
-- 5. VERIFICACIÓN FINAL
-- ============================================================================

SELECT '=== VERIFICACIÓN FINAL ===' AS info;

SELECT 'dim_tipo_trabajo' AS tabla, COUNT(*) AS registros FROM dim_tipo_trabajo
UNION ALL
SELECT 'dim_red', COUNT(*) FROM dim_red
UNION ALL
SELECT 'dim_codigo_trabajo', COUNT(*) FROM dim_codigo_trabajo
UNION ALL
SELECT 'tbl_pres_unidades', COUNT(*) FROM tbl_pres_unidades
UNION ALL
SELECT 'tbl_pres_capitulos', COUNT(*) FROM tbl_pres_capitulos;

SELECT '=== SINCRONIZACIÓN COMPLETADA ===' AS resultado;

-- ============================================================================
-- NOTAS IMPORTANTES PARA LA IMPORTACIÓN DE DATOS
-- ============================================================================
/*
MAPEO DE TIPO DE TRABAJOS (LISTADO OTS.TIPO DE TRABAJOS → tbl_partes.tipo_trabajo_id):
  Access ID 1 (OT/) → MySQL ID 1
  Access ID 2 (TP/) → MySQL ID 2
  Access ID 3 (GF/) → MySQL ID 3

MAPEO DE RED (LISTADO OTS.RED → tbl_partes.red_id):
  'DISTRIBUCIÓN' → 1
  'SANEAMIENTO'  → 2
  'ADUCCIÓN'     → 3
  'DEPURACIÓN'   → 4
  'OTROS'        → 5

MAPEO DE TRABAJOS PROGRAMADOS (LISTADO OTS.TRABAJOS PROGRAMADOS → tbl_partes.cod_trabajo_id):
  Los IDs coinciden directamente (1-22)

MAPEO DE UNIDADES (PRECIOS UNITARIOS.UNIDAD → tbl_pres_precios.id_unidades):
  Usar: SELECT id FROM tbl_pres_unidades WHERE unidad = '[valor]'

MAPEO DE CAPITULOS (PRECIOS UNITARIOS.CAPITULO → tbl_pres_precios.id_capitulo):
  Usar: SELECT id FROM tbl_pres_capitulos WHERE capitulo = '[valor]'
*/
