-- ============================================================================
-- AGREGAR REGISTROS "TODO X" A TABLAS GEOGRÁFICAS
-- ============================================================================
-- Este script añade registros especiales "Todo {Nombre}" a las tablas de
-- dimensiones geográficas para permitir seleccionar "todos" los elementos
-- de un nivel jerárquico.
--
-- JERARQUÍA: Provincia → Comarca → Municipio → Concejo
--
-- CONVENCIÓN DE IDs:
--   - ID = 1 para "Todo Álava" en municipios
--   - ID = municipio_id para "Todo {Municipio}" en concejos (ordenación natural)
--
-- USO:
--   mysql -u [usuario] -p [esquema] < agregar_registros_todo_geograficos.sql
-- ============================================================================

SELECT DATABASE() AS esquema_actual;
SELECT '=== INICIO: Agregar registros Todo X ===' AS info;

-- Desactivar FK temporalmente
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================================================
-- 1. AGREGAR "Todo Álava" a dim_municipios (ID = 1)
-- ============================================================================

SELECT '>>> Paso 1: Agregando Todo Álava a dim_municipios...' AS paso;

-- Si existe ID=1 y NO es "Todo Álava", moverlo
UPDATE dim_municipios
SET id = id + 10000
WHERE id = 1
  AND municipio_nombre NOT LIKE 'Todo %';

-- Actualizar FK en dim_concejos si se movió algún municipio
UPDATE dim_concejos
SET municipio_id = municipio_id + 10000
WHERE municipio_id = 1;

-- Insertar "Todo Álava" con ID = 1
INSERT IGNORE INTO dim_municipios (id, codigo_ine, municipio_nombre, provincia_id, comarca_id, activo)
VALUES (1, '0000', 'Todo Álava', 1, NULL, 1);

SELECT '  ✓ Todo Álava agregado/verificado en dim_municipios (ID=1)' AS resultado;

-- ============================================================================
-- 2. AGREGAR "Todo {Municipio}" a dim_concejos
-- ============================================================================

SELECT '>>> Paso 2: Agregando Todo {Municipio} a dim_concejos...' AS paso;

-- Para cada municipio, insertar un concejo "Todo {Municipio}"
-- El ID será igual al municipio_id para mantener ordenación natural
INSERT IGNORE INTO dim_concejos (id, municipio_id, nombre, activo)
SELECT
    m.id,           -- ID = municipio_id
    m.id,           -- municipio_id
    CONCAT('Todo ', m.municipio_nombre),
    1
FROM dim_municipios m
WHERE m.activo = 1 OR m.id = 1;

SELECT CONCAT('  ✓ Concejos "Todo" agregados: ', ROW_COUNT()) AS resultado;

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================================
-- 3. VERIFICACIÓN
-- ============================================================================

SELECT '>>> Verificación final...' AS paso;

SELECT '--- Municipios "Todo" ---' AS '';
SELECT id, municipio_nombre, provincia_id
FROM dim_municipios
WHERE municipio_nombre LIKE 'Todo %'
ORDER BY id;

SELECT '--- Concejos "Todo" (primeros 15) ---' AS '';
SELECT c.id, c.nombre, c.municipio_id
FROM dim_concejos c
WHERE c.nombre LIKE 'Todo %'
ORDER BY c.id
LIMIT 15;

SELECT '--- Totales ---' AS '';
SELECT
    (SELECT COUNT(*) FROM dim_municipios WHERE municipio_nombre LIKE 'Todo %') AS municipios_todo,
    (SELECT COUNT(*) FROM dim_concejos WHERE nombre LIKE 'Todo %') AS concejos_todo,
    (SELECT COUNT(*) FROM dim_municipios WHERE activo = 1) AS municipios_total,
    (SELECT COUNT(*) FROM dim_concejos WHERE activo = 1) AS concejos_total;

SELECT '=== FIN: Registros Todo X agregados correctamente ===' AS resultado;

-- ============================================================================
-- EJEMPLO DE USO EN DROPDOWNS:
-- ============================================================================
--
-- Al cargar municipios para una provincia:
--   SELECT * FROM dim_municipios
--   WHERE provincia_id = 1 AND activo = 1
--   ORDER BY id ASC;  -- "Todo Álava" (id=1) aparece primero
--
-- Al cargar concejos para un municipio:
--   SELECT * FROM dim_concejos
--   WHERE municipio_id = ? AND activo = 1
--   ORDER BY id ASC;  -- "Todo {Municipio}" aparece primero
--
-- Si municipio_id = 1 (Todo Álava):
--   Solo devuelve "Todo Álava" como concejo
-- ============================================================================
