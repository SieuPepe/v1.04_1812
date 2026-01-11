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
--
-- MySQL actual tiene (INCORRECTO):
--   ID 1 = GF (Gastos Fijos)
--   ID 2 = OT (Orden de Trabajo)
--   ID 3 = TP (Trabajos Programados)
--
-- CORRECCIÓN: Actualizar para que coincidan los IDs con Access
-- ============================================================================

SELECT '>>> Actualizando dim_tipo_trabajo...' AS paso;

-- Mostrar estado ANTES
SELECT 'ANTES de actualizar:' AS info;
SELECT * FROM dim_tipo_trabajo ORDER BY id;

SET FOREIGN_KEY_CHECKS = 0;

-- Actualizar cada registro para que coincida con Access
-- ID 1: Debe ser OT (Orden de Trabajo) - Access ID 1
UPDATE dim_tipo_trabajo SET tipo_codigo = 'OT', descripcion = 'ORDEN DE TRABAJO' WHERE id = 1;

-- ID 2: Debe ser TP (Trabajos Programados) - Access ID 2
UPDATE dim_tipo_trabajo SET tipo_codigo = 'TP', descripcion = 'TRABAJOS PROGRAMADOS' WHERE id = 2;

-- ID 3: Debe ser GF (Gastos Fijos) - Access ID 3
UPDATE dim_tipo_trabajo SET tipo_codigo = 'GF', descripcion = 'GASTOS FIJOS DE LA EXPLOTACIÓN' WHERE id = 3;

SET FOREIGN_KEY_CHECKS = 1;

SELECT 'dim_tipo_trabajo actualizada:' AS resultado;
SELECT * FROM dim_tipo_trabajo ORDER BY id;

-- ============================================================================
-- 2. VERIFICAR dim_red
-- ============================================================================
-- Access tiene estos valores únicos en el campo RED:
--   DISTRIBUCIÓN, SANEAMIENTO, ADUCCIÓN, DEPURACIÓN, OTROS
--
-- MySQL actual (YA CORRECTO):
--   ID 1 = ADU (Aducción)
--   ID 2 = DEP (Depuración)
--   ID 3 = DIS (Distribución)
--   ID 4 = OTR (Otros)
--   ID 5 = SAN (Saneamiento)
--
-- MAPEO Access texto → MySQL ID:
--   'ADUCCIÓN'     → 1
--   'DEPURACIÓN'   → 2
--   'DISTRIBUCIÓN' → 3
--   'OTROS'        → 4
--   'SANEAMIENTO'  → 5
-- ============================================================================

SELECT '>>> Verificando dim_red...' AS paso;
SELECT 'dim_red ya tiene los valores correctos:' AS resultado;
SELECT * FROM dim_red ORDER BY id;

-- ============================================================================
-- 2b. LIMPIAR dim_codigo_trabajo (eliminar registros de prueba)
-- ============================================================================
-- Eliminar registros de prueba (id > 22)

SELECT '>>> Limpiando dim_codigo_trabajo (registros de prueba)...' AS paso;

DELETE FROM dim_codigo_trabajo WHERE id > 22;

SELECT 'dim_codigo_trabajo limpiada (eliminados registros id > 22):' AS resultado;
SELECT COUNT(*) AS total_registros FROM dim_codigo_trabajo;

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
  ┌─────────────┬─────────────────────────────────┬───────────┐
  │ Access ID   │ Access Valor                    │ MySQL ID  │
  ├─────────────┼─────────────────────────────────┼───────────┤
  │ 1           │ ORDEN DE TRABAJO (OT/)          │ 1         │
  │ 2           │ TRABAJOS PROGRAMADOS (TP/)      │ 2         │
  │ 3           │ GASTOS FIJOS DE LA EXPLOT. (GF/)│ 3         │
  └─────────────┴─────────────────────────────────┴───────────┘
  Los IDs coinciden directamente tras ejecutar este script.

MAPEO DE RED (LISTADO OTS.RED → tbl_partes.red_id):
  ┌─────────────────┬───────────┐
  │ Access Texto    │ MySQL ID  │
  ├─────────────────┼───────────┤
  │ 'ADUCCIÓN'      │ 1         │
  │ 'DEPURACIÓN'    │ 2         │
  │ 'DISTRIBUCIÓN'  │ 3         │
  │ 'OTROS'         │ 4         │
  │ 'SANEAMIENTO'   │ 5         │
  └─────────────────┴───────────┘
  Usar CASE o tabla de lookup para convertir texto a ID.

MAPEO DE TRABAJOS PROGRAMADOS (LISTADO OTS.TRABAJOS PROGRAMADOS → tbl_partes.cod_trabajo_id):
  Los IDs coinciden directamente (1-22).
  NULL en Access = NULL en MySQL (solo aplica a OT y GF, no a TP).

MAPEO DE UNIDADES (PRECIOS UNITARIOS.UNIDAD → tbl_pres_precios.id_unidades):
  Usar: SELECT id FROM tbl_pres_unidades WHERE unidad = '[valor]'

MAPEO DE CAPITULOS (PRECIOS UNITARIOS.CAPITULO → tbl_pres_precios.id_capitulo):
  Usar: SELECT id FROM tbl_pres_capitulos WHERE capitulo = '[valor]'

EJEMPLO DE IMPORTACIÓN DE LISTADO OTS:
  INSERT INTO tbl_partes (codigo, tipo_trabajo_id, cod_trabajo_id, red_id, ...)
  SELECT
    COD_TRABAJO,
    `TIPO DE TRABAJOS`,  -- ID coincide directamente
    `TRABAJOS PROGRAMADOS`,  -- ID coincide directamente (puede ser NULL)
    CASE RED
      WHEN 'ADUCCIÓN' THEN 1
      WHEN 'DEPURACIÓN' THEN 2
      WHEN 'DISTRIBUCIÓN' THEN 3
      WHEN 'OTROS' THEN 4
      WHEN 'SANEAMIENTO' THEN 5
    END,
    ...
  FROM access_listado_ots;
*/
