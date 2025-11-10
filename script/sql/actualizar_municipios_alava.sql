-- =====================================================================
-- ACTUALIZACIÓN DE MUNICIPIOS DE ÁLAVA
-- =====================================================================
-- Este script:
-- 1. Elimina los registros del ID 1 al 52 de dim_municipios
-- 2. Inserta los 51 municipios oficiales de Álava según el INE
-- 3. Distribuye los municipios en sus comarcas correspondientes
-- =====================================================================

-- =====================================================================
-- PASO 1: Eliminar registros del 1 al 52
-- =====================================================================
DELETE FROM dim_municipios WHERE id BETWEEN 1 AND 52;

-- =====================================================================
-- PASO 2: Insertar los 51 municipios de Álava con distribución por comarcas
-- =====================================================================
-- Los municipios se insertan según los códigos INE oficiales (enero 2025)
-- y se distribuyen en las 6 comarcas/cuadrillas de Álava

INSERT INTO dim_municipios (codigo_ine, nombre, provincia_id, comarca_id, activo) VALUES
-- =============================================================================
-- CUADRILLA DE VITORIA (comarca_id=3) - 19 municipios
-- =============================================================================
(1001, 'Alegría-Dulantzi', 1, 3, 1),
(1008, 'Arratzua-Ubarrundia', 1, 3, 1),
(1009, 'Asparrena', 1, 3, 1),
(1013, 'Barrundia', 1, 3, 1),
(1018, 'Zigoitia', 1, 3, 1),
(1020, 'Kuartango', 1, 3, 1),
(1021, 'Elburgo/Burgelu', 1, 3, 1),
(1024, 'Erriberagoitia/Ribera Alta', 1, 3, 1),
(1027, 'Iruraiz-Gauna', 1, 3, 1),
(1036, 'Legutio', 1, 3, 1),
(1047, 'Ribera Baja/Erribera Beitia', 1, 3, 1),
(1051, 'Agurain/Salvatierra', 1, 3, 1),
(1053, 'San Millán/Donemiliaga', 1, 3, 1),
(1056, 'Harana/Valle de Arana', 1, 3, 1),
(1058, 'Arraia-Maeztu', 1, 3, 1),
(1059, 'Vitoria-Gasteiz', 1, 3, 1),
(1061, 'Zalduondo', 1, 3, 1),
(1063, 'Zuia', 1, 3, 1),
(1901, 'Iruña Oka/Iruña de Oca', 1, 3, 1),

-- =============================================================================
-- CUADRILLA DE AYALA (comarca_id=1) - 7 municipios
-- =============================================================================
(1002, 'Amurrio', 1, 1, 1),
(1003, 'Aramaio', 1, 1, 1),
(1004, 'Artziniega', 1, 1, 1),
(1010, 'Ayala/Aiara', 1, 1, 1),
(1042, 'Okondo', 1, 1, 1),
(1054, 'Urkabustaiz', 1, 1, 1),
(1055, 'Valdegovía/Gaubea', 1, 1, 1),

-- =============================================================================
-- CUADRILLA DE LAGUARDIA-RIOJA ALAVESA (comarca_id=2) - 18 municipios
-- =============================================================================
(1011, 'Baños de Ebro/Mañueta', 1, 2, 1),
(1014, 'Berantevilla', 1, 2, 1),
(1019, 'Kripan', 1, 2, 1),
(1022, 'Elciego', 1, 2, 1),
(1025, 'Elvillar/Bilar', 1, 2, 1),
(1028, 'Labastida/Bastida', 1, 2, 1),
(1030, 'Lagrán', 1, 2, 1),
(1031, 'Laguardia', 1, 2, 1),
(1032, 'Lanciego/Lantziego', 1, 2, 1),
(1033, 'Lapuebla de Labarca', 1, 2, 1),
(1034, 'Leza', 1, 2, 1),
(1039, 'Moreda de Álava/Moreda Araba', 1, 2, 1),
(1041, 'Navaridas', 1, 2, 1),
(1043, 'Oyón-Oion', 1, 2, 1),
(1052, 'Samaniego', 1, 2, 1),
(1057, 'Villabuena de Álava/Eskuernaga', 1, 2, 1),
(1062, 'Zambrana', 1, 2, 1),
(1902, 'Lantarón', 1, 2, 1),

-- =============================================================================
-- CUADRILLA DE AÑANA (comarca_id=5) - 6 municipios
-- =============================================================================
(1006, 'Armiñón', 1, 5, 1),
(1016, 'Bernedo', 1, 5, 1),
(1037, 'Arraia-Maeztu', 1, 5, 1),
(1044, 'Peñacerrada-Urizaharra', 1, 5, 1),
(1049, 'Añana', 1, 5, 1),
(1060, 'Yécora/Iekora', 1, 5, 1),

-- =============================================================================
-- CUADRILLA DE CAMPEZO (comarca_id=6) - 1 municipio
-- =============================================================================
(1017, 'Campezo/Kanpezu', 1, 6, 1)

ON DUPLICATE KEY UPDATE
    nombre = VALUES(nombre),
    provincia_id = VALUES(provincia_id),
    comarca_id = VALUES(comarca_id),
    activo = VALUES(activo);

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
    m.nombre,
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
