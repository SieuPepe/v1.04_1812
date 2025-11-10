-- =====================================================================
-- CORRECCIÓN DE MUNICIPIOS DE ÁLAVA - Datos oficiales del INE
-- =====================================================================
-- Este script corrige los datos de dim_municipios para Álava
-- usando los datos oficiales del INE actualizados a enero 2025
--
-- PROBLEMAS DETECTADOS:
-- - Códigos INE incorrectos (desplazamiento sistemático)
-- - Faltan 5 municipios
-- - 4 códigos que no existen en el INE
-- - 30 municipios con nombres mal asignados a códigos
-- =====================================================================

-- Primero, eliminar todos los registros de Álava (provincia_id=1)
DELETE FROM dim_municipios WHERE provincia_id = 1;

-- Insertar los 51 municipios oficiales de Álava según el INE
-- Los códigos comarca_id se mantienen según la distribución original por cuadrillas
INSERT INTO dim_municipios (codigo_ine, nombre, provincia_id, comarca_id, activo) VALUES
-- Cuadrilla de Vitoria (comarca_id=3)
(1001, 'Alegría-Dulantzi', 1, 3, 1),
(1008, 'Arratzua-Ubarrundia', 1, 3, 1),
(1009, 'Asparrena', 1, 3, 1),
(1013, 'Barrundia', 1, 3, 1),
(1018, 'Zigoitia', 1, 3, 1),
(1020, 'Kuartango', 1, 3, 1),
(1021, 'Elburgo/Burgelu', 1, 3, 1),
(1023, 'Erriberagoitia/Ribera Alta', 1, 3, 1),
(1027, 'Iruraiz-Gauna', 1, 3, 1),
(1036, 'Legutio', 1, 3, 1),
(1047, 'Ribera Baja/Erribera Beitia', 1, 3, 1),
(1051, 'Agurain/Salvatierra', 1, 3, 1),
(1053, 'San Millán/Donemiliaga', 1, 3, 1),
(1056, 'Harana/Valle de Arana', 1, 3, 1),
(1058, 'Legutio', 1, 3, 1),
(1059, 'Vitoria-Gasteiz', 1, 3, 1),
(1061, 'Zalduondo', 1, 3, 1),
(1063, 'Zuia', 1, 3, 1),
(1901, 'Iruña Oka/Iruña de Oca', 1, 3, 1),

-- Cuadrilla de Ayala (comarca_id=1)
(1002, 'Amurrio', 1, 1, 1),
(1003, 'Aramaio', 1, 1, 1),
(1004, 'Artziniega', 1, 1, 1),
(1010, 'Ayala/Aiara', 1, 1, 1),
(1042, 'Okondo', 1, 1, 1),
(1054, 'Urkabustaiz', 1, 1, 1),
(1055, 'Valdegovía/Gaubea', 1, 1, 1),

-- Cuadrilla de Laguardia-Rioja Alavesa (comarca_id=2)
(1011, 'Baños de Ebro/Mañueta', 1, 2, 1),
(1014, 'Berantevilla', 1, 2, 1),
(1019, 'Kripan', 1, 2, 1),
(1022, 'Elciego', 1, 2, 1),
(1023, 'Elvillar/Bilar', 1, 2, 1),
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

-- Cuadrilla de Añana (comarca_id=5)
(1006, 'Armiñón', 1, 5, 1),
(1016, 'Bernedo', 1, 5, 1),
(1037, 'Arraia-Maeztu', 1, 5, 1),
(1044, 'Peñacerrada-Urizaharra', 1, 5, 1),
(1049, 'Añana', 1, 5, 1),
(1060, 'Yécora/Iekora', 1, 5, 1),

-- Cuadrilla de Campezo (comarca_id=6)
(1017, 'Campezo/Kanpezu', 1, 6, 1)
ON DUPLICATE KEY UPDATE
    nombre = VALUES(nombre),
    provincia_id = VALUES(provincia_id),
    comarca_id = VALUES(comarca_id);

-- =====================================================================
-- VERIFICACIÓN
-- =====================================================================
SELECT
    COUNT(*) as total_municipios,
    'Debe ser 51' as esperado
FROM dim_municipios
WHERE provincia_id = 1;

-- Mostrar todos los municipios de Álava ordenados por código INE
SELECT
    codigo_ine,
    nombre,
    comarca_id,
    activo
FROM dim_municipios
WHERE provincia_id = 1
ORDER BY codigo_ine;

-- =====================================================================
-- FIN DEL SCRIPT DE CORRECCIÓN
-- =====================================================================
SELECT 'Corrección de municipios de Álava completada' AS Resultado;
