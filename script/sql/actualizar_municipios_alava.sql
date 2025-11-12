-- =====================================================================
-- ACTUALIZACIÓN DE MUNICIPIOS DE ÁLAVA
-- =====================================================================
-- Este script:
-- 1. Inserta o actualiza los 51 municipios oficiales de Álava según el INE
-- 2. Distribuye los municipios en sus comarcas correspondientes
-- 3. USA codigo_ine (clave única) para identificar municipios
-- 4. NO borra registros por ID (el ID es autoincrementado y puede cambiar)
-- =====================================================================

-- =====================================================================
-- PASO 1: NO SE BORRAN REGISTROS - Se usa INSERT ... ON DUPLICATE KEY UPDATE
-- =====================================================================
-- IMPORTANTE: NO usamos DELETE porque:
-- - Los IDs son autoincrementados y pueden no corresponder a municipios específicos
-- - Podríamos borrar municipios de otras provincias accidentalmente
-- - El campo codigo_ine es UNIQUE y nos permite hacer UPSERT de forma segura
-- =====================================================================

-- =====================================================================
-- PASO 2: Insertar o actualizar los 51 municipios de Álava con distribución por comarcas
-- =====================================================================
-- Los municipios se insertan según los códigos INE oficiales (enero 2025)
-- y se distribuyen en las 6 comarcas/cuadrillas de Álava

INSERT INTO dim_municipios (codigo_ine, municipio_nombre, provincia_id, comarca_id, activo, created_at) VALUES
-- =============================================================================
-- CUADRILLA DE VITORIA (comarca_id=3) - 19 municipios
-- =============================================================================
(1001, 'Alegría-Dulantzi', 1, 3, 1, NOW()),
(1008, 'Arratzua-Ubarrundia', 1, 3, 1, NOW()),
(1009, 'Asparrena', 1, 3, 1, NOW()),
(1013, 'Barrundia', 1, 3, 1, NOW()),
(1018, 'Zigoitia', 1, 3, 1, NOW()),
(1020, 'Kuartango', 1, 3, 1, NOW()),
(1021, 'Elburgo/Burgelu', 1, 3, 1, NOW()),
(1024, 'Erriberagoitia/Ribera Alta', 1, 3, 1, NOW()),
(1027, 'Iruraiz-Gauna', 1, 3, 1, NOW()),
(1036, 'Legutio', 1, 3, 1, NOW()),
(1047, 'Ribera Baja/Erribera Beitia', 1, 3, 1, NOW()),
(1051, 'Agurain/Salvatierra', 1, 3, 1, NOW()),
(1053, 'San Millán/Donemiliaga', 1, 3, 1, NOW()),
(1056, 'Harana/Valle de Arana', 1, 3, 1, NOW()),
(1058, 'Arraia-Maeztu', 1, 3, 1, NOW()),
(1059, 'Vitoria-Gasteiz', 1, 3, 1, NOW()),
(1061, 'Zalduondo', 1, 3, 1, NOW()),
(1063, 'Zuia', 1, 3, 1, NOW()),
(1901, 'Iruña Oka/Iruña de Oca', 1, 3, 1, NOW()),

-- =============================================================================
-- CUADRILLA DE AYALA (comarca_id=1) - 7 municipios
-- =============================================================================
(1002, 'Amurrio', 1, 1, 1, NOW()),
(1003, 'Aramaio', 1, 1, 1, NOW()),
(1004, 'Artziniega', 1, 1, 1, NOW()),
(1010, 'Ayala/Aiara', 1, 1, 1, NOW()),
(1042, 'Okondo', 1, 1, 1, NOW()),
(1054, 'Urkabustaiz', 1, 1, 1, NOW()),
(1055, 'Valdegovía/Gaubea', 1, 1, 1, NOW()),

-- =============================================================================
-- CUADRILLA DE LAGUARDIA-RIOJA ALAVESA (comarca_id=2) - 18 municipios
-- =============================================================================
(1011, 'Baños de Ebro/Mañueta', 1, 2, 1, NOW()),
(1014, 'Berantevilla', 1, 2, 1, NOW()),
(1019, 'Kripan', 1, 2, 1, NOW()),
(1022, 'Elciego', 1, 2, 1, NOW()),
(1025, 'Elvillar/Bilar', 1, 2, 1, NOW()),
(1028, 'Labastida/Bastida', 1, 2, 1, NOW()),
(1030, 'Lagrán', 1, 2, 1, NOW()),
(1031, 'Laguardia', 1, 2, 1, NOW()),
(1032, 'Lanciego/Lantziego', 1, 2, 1, NOW()),
(1033, 'Lapuebla de Labarca', 1, 2, 1, NOW()),
(1034, 'Leza', 1, 2, 1, NOW()),
(1039, 'Moreda de Álava/Moreda Araba', 1, 2, 1, NOW()),
(1041, 'Navaridas', 1, 2, 1, NOW()),
(1043, 'Oyón-Oion', 1, 2, 1, NOW()),
(1052, 'Samaniego', 1, 2, 1, NOW()),
(1057, 'Villabuena de Álava/Eskuernaga', 1, 2, 1, NOW()),
(1062, 'Zambrana', 1, 2, 1, NOW()),
(1902, 'Lantarón', 1, 2, 1, NOW()),

-- =============================================================================
-- CUADRILLA DE AÑANA (comarca_id=5) - 6 municipios
-- =============================================================================
(1006, 'Armiñón', 1, 5, 1, NOW()),
(1016, 'Bernedo', 1, 5, 1, NOW()),
(1037, 'Arraia-Maeztu', 1, 5, 1, NOW()),
(1044, 'Peñacerrada-Urizaharra', 1, 5, 1, NOW()),
(1049, 'Añana', 1, 5, 1, NOW()),
(1060, 'Yécora/Iekora', 1, 5, 1, NOW()),

-- =============================================================================
-- CUADRILLA DE CAMPEZO (comarca_id=6) - 1 municipio
-- =============================================================================
(1017, 'Campezo/Kanpezu', 1, 6, 1, NOW())

ON DUPLICATE KEY UPDATE
    municipio_nombre = VALUES(municipio_nombre),
    provincia_id = VALUES(provincia_id),
    comarca_id = VALUES(comarca_id),
    activo = 1,  -- Siempre restaurar a activo = 1
    created_at = IFNULL(created_at, NOW());  -- Mantener created_at original o NOW() si es NULL

-- =====================================================================
-- VERIFICACIÓN: Contar municipios por comarca
-- =====================================================================
SELECT
    c.comarca_nombre,
    COUNT(m.id) as total_municipios
FROM dim_comarcas c
LEFT JOIN dim_municipios m ON c.id = m.comarca_id
WHERE c.provincia_id = 1
GROUP BY c.id, c.comarca_nombre
ORDER BY c.id;

-- =====================================================================
-- VERIFICACIÓN: Listar todos los municipios de Álava
-- =====================================================================
SELECT
    m.codigo_ine,
    m.municipio_nombre,
    c.comarca_nombre,
    m.activo
FROM dim_municipios m
INNER JOIN dim_comarcas c ON m.comarca_id = c.id
WHERE m.provincia_id = 1
ORDER BY m.codigo_ine;

-- =====================================================================
-- VERIFICACIÓN: Total de municipios de Álava
-- =====================================================================
SELECT
    COUNT(*) as total_municipios_alava,
    '51 municipios esperados' as nota
FROM dim_municipios
WHERE provincia_id = 1;

-- =====================================================================
-- FIN DEL SCRIPT
-- =====================================================================
SELECT 'Script de actualización de municipios de Álava completado' AS Resultado;
