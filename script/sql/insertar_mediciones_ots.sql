-- =============================================================================
-- Script de importación de mediciones desde Excel a tbl_part_presupuesto
-- Generado: 2025-11-12 00:30:34
-- Total de registros: 2777
-- =============================================================================

USE cert_dev;

-- IMPORTANTE:
-- Este script usa subconsultas para obtener el parte_id interno desde tbl_partes
-- basándose en el código del parte (OT/xxxx, TP/xxxx, GF/xxxx, etc.)
-- Si algún código no existe en tbl_partes, ese INSERT fallará

-- Descomentar la siguiente línea si quieres LIMPIAR la tabla antes de insertar:
-- TRUNCATE TABLE tbl_part_presupuesto;

-- Mostrar registros actuales antes de insertar
SELECT COUNT(*) AS 'Registros actuales en tbl_part_presupuesto' FROM tbl_part_presupuesto;

-- Insertar mediciones
-- Formato: (parte_id, precio_id, cantidad, fecha, precio_unit)
-- El parte_id se obtiene desde tbl_partes.codigo
-- El precio_unit se obtiene desde tbl_pres_precios.coste

-- Lote 1/28 (registros 1-100)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0121') AS parte_id,
        40587 AS precio_id,
        1.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40587) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0453') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0425') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0123') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0278') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0360') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0481') AS parte_id,
        20002 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0267') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0471') AS parte_id,
        41195 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41195) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0407') AS parte_id,
        40644 AS precio_id,
        2.0 AS cantidad,
        '2025-10-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40644) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        30001 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0109') AS parte_id,
        30010 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30010) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        20003 AS precio_id,
        10.0 AS cantidad,
        '2025-09-23' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0307') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0247') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0392') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0139') AS parte_id,
        41046 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0427') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0283') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0387') AS parte_id,
        40798 AS precio_id,
        6.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        40691 AS precio_id,
        1.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40691) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0375') AS parte_id,
        20002 AS precio_id,
        9.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0515') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-11-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0049') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0058') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0309') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0138') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0176') AS parte_id,
        40893 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40893) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0292') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0228') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'GF/0003') AS parte_id,
        10003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 10003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0493') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0315') AS parte_id,
        20002 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0430') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0199') AS parte_id,
        40565 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40565) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0405') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-27' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0345') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0103') AS parte_id,
        41048 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41048) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0241') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40751 AS precio_id,
        1.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40751) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0103') AS parte_id,
        40646 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40646) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0482') AS parte_id,
        41046 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0476') AS parte_id,
        20003 AS precio_id,
        11.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0128') AS parte_id,
        41046 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0215') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0105') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0474') AS parte_id,
        40561 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40561) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0311') AS parte_id,
        30011 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0250') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0239') AS parte_id,
        20002 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0445') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0125') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0265') AS parte_id,
        40344 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40344) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'GF/0004') AS parte_id,
        20001 AS precio_id,
        176.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0368') AS parte_id,
        20005 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0059') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0045') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0254') AS parte_id,
        20005 AS precio_id,
        8.0 AS cantidad,
        '2025-10-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        40831 AS precio_id,
        8.0 AS cantidad,
        '2025-10-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0308') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0231') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0221') AS parte_id,
        30008 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30008) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0394') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0341') AS parte_id,
        40754 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40754) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0389') AS parte_id,
        40717 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40350 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40350) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0208') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0218') AS parte_id,
        40752 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40752) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0485') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0329') AS parte_id,
        20004 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0166') AS parte_id,
        20003 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0148') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0165') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0025') AS parte_id,
        40755 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40755) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0504') AS parte_id,
        30011 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0435') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0176') AS parte_id,
        30009 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30009) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0150') AS parte_id,
        40105 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40105) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        41063 AS precio_id,
        12.0 AS cantidad,
        '2025-10-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41063) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0371') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0494') AS parte_id,
        20004 AS precio_id,
        24.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0172') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0351') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0431') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0380') AS parte_id,
        40028 AS precio_id,
        1.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40028) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0071') AS parte_id,
        20003 AS precio_id,
        11.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0290') AS parte_id,
        40839 AS precio_id,
        1.0 AS cantidad,
        '2025-10-16' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40839) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0498') AS parte_id,
        20004 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0397') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40629 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40629) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0178') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0415') AS parte_id,
        40643 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40643) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0102') AS parte_id,
        30003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0225') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0040') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0223') AS parte_id,
        30011 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0234') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0397') AS parte_id,
        20002 AS precio_id,
        6.0 AS cantidad,
        '2025-10-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 2/28 (registros 101-200)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0162') AS parte_id,
        30003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0269') AS parte_id,
        41187 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41187) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0152') AS parte_id,
        30003 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0203') AS parte_id,
        40941 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40941) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0203') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0236') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0361') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0403') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        30001 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0118') AS parte_id,
        30003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0463') AS parte_id,
        40027 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40027) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0004') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0214') AS parte_id,
        20004 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0066') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0122') AS parte_id,
        20002 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0221') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0007') AS parte_id,
        20004 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0397') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-10-13' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0282') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0199') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0474') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0345') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-23' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0520') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0244') AS parte_id,
        41114 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41114) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0438') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0336') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0266') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-11' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0265') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0489') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0057') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0033') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        40798 AS precio_id,
        3.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0066') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        20003 AS precio_id,
        21.0 AS cantidad,
        '2025-09-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40204 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40204) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0458') AS parte_id,
        41181 AS precio_id,
        1.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41181) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0244') AS parte_id,
        40831 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0280') AS parte_id,
        40028 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40028) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0448') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0488') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0002') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0345') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0484') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0198') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        30011 AS precio_id,
        11.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0220') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        '2025-10-24' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0003') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0437') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0397') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-10-14' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0418') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40556 AS precio_id,
        1.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40556) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0427') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0328') AS parte_id,
        40099 AS precio_id,
        0.5 AS cantidad,
        '2025-09-22' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40099) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0441') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-20' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0191') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0402') AS parte_id,
        40334 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40334) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0248') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0152') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        30001 AS precio_id,
        8.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0309') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40107 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40107) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0180') AS parte_id,
        40590 AS precio_id,
        1.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0290') AS parte_id,
        40798 AS precio_id,
        3.0 AS cantidad,
        '2025-10-16' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0061') AS parte_id,
        30011 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        41064 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41064) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0197') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0010') AS parte_id,
        40764 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40764) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0174') AS parte_id,
        41175 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41175) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0370') AS parte_id,
        30011 AS precio_id,
        9.0 AS cantidad,
        '2025-10-15' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0279') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0246') AS parte_id,
        40644 AS precio_id,
        2.0 AS cantidad,
        '2025-09-05' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40644) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0375') AS parte_id,
        20004 AS precio_id,
        24.0 AS cantidad,
        '2025-10-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0098') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0489') AS parte_id,
        40614 AS precio_id,
        1.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40614) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20002 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0094') AS parte_id,
        40590 AS precio_id,
        1.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0442') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0136') AS parte_id,
        20004 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0269') AS parte_id,
        40012 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0207') AS parte_id,
        40026 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40026) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0269') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0475') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0048') AS parte_id,
        41194 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41194) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40601 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40601) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0155') AS parte_id,
        40590 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0197') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0324') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0236') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0507') AS parte_id,
        40718 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40718) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0229') AS parte_id,
        40798 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0420') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0233') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0345') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40552 AS precio_id,
        1.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40552) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0124') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0312') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0202') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0237') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        20002 AS precio_id,
        7.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 3/28 (registros 201-300)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0439') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0387') AS parte_id,
        40059 AS precio_id,
        1.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0515') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        '2025-11-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0222') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40798 AS precio_id,
        2.0 AS cantidad,
        '2025-09-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0224') AS parte_id,
        30003 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0342') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0267') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0443') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0297') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0152') AS parte_id,
        41045 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41045) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0169') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0227') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0172') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0327') AS parte_id,
        20004 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0011') AS parte_id,
        40764 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40764) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0196') AS parte_id,
        20002 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0265') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        41016 AS precio_id,
        8.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41016) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0492') AS parte_id,
        40590 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0074') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0133') AS parte_id,
        40798 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0380') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0431') AS parte_id,
        40831 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0089') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0095') AS parte_id,
        20005 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0201') AS parte_id,
        30003 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0126') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0106') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0150') AS parte_id,
        41048 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41048) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0358') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0156') AS parte_id,
        40590 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0183') AS parte_id,
        30011 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0252') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0122') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'GF/0001') AS parte_id,
        10003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 10003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        40483 AS precio_id,
        1.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40483) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0130') AS parte_id,
        20003 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0303') AS parte_id,
        20004 AS precio_id,
        4.0 AS cantidad,
        '2025-10-16' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0502') AS parte_id,
        40020 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40020) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0244') AS parte_id,
        20003 AS precio_id,
        24.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0413') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0280') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0217') AS parte_id,
        40131 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40131) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0391') AS parte_id,
        30011 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0394') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0483') AS parte_id,
        41046 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0188') AS parte_id,
        40829 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40829) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0067') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0422') AS parte_id,
        40553 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40553) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0303') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0057') AS parte_id,
        40717 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0302') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0293') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0305') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0215') AS parte_id,
        40847 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40847) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        41064 AS precio_id,
        1.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41064) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0154') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20003 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0109') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0181') AS parte_id,
        41025 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41025) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0129') AS parte_id,
        30012 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0223') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0438') AS parte_id,
        40831 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0334') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        40107 AS precio_id,
        2.0 AS cantidad,
        '2025-10-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40107) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0168') AS parte_id,
        30003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0357') AS parte_id,
        40048 AS precio_id,
        1.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40048) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0257') AS parte_id,
        40014 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40014) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0494') AS parte_id,
        40018 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40018) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0079') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        30008 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30008) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0365') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0027') AS parte_id,
        30011 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0170') AS parte_id,
        41182 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41182) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        30008 AS precio_id,
        1.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30008) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0025') AS parte_id,
        40553 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40553) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0173') AS parte_id,
        30003 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0440') AS parte_id,
        40798 AS precio_id,
        2.0 AS cantidad,
        '2025-10-21' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0471') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0166') AS parte_id,
        20004 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0454') AS parte_id,
        41042 AS precio_id,
        1.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41042) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0500') AS parte_id,
        40882 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40882) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0185') AS parte_id,
        30011 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0235') AS parte_id,
        30003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0239') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0176') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0386') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0254') AS parte_id,
        20005 AS precio_id,
        7.5 AS cantidad,
        '2025-10-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0356') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0367') AS parte_id,
        20004 AS precio_id,
        24.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0094') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0345') AS parte_id,
        20003 AS precio_id,
        12.0 AS cantidad,
        '2025-09-22' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0172') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0106') AS parte_id,
        30003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0154') AS parte_id,
        20004 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 4/28 (registros 301-400)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        30001 AS precio_id,
        5.0 AS cantidad,
        '2025-09-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0345') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-23' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0295') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0255') AS parte_id,
        40798 AS precio_id,
        2.0 AS cantidad,
        '2025-09-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40820 AS precio_id,
        4.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40820) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        20004 AS precio_id,
        9.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0199') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0291') AS parte_id,
        30011 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0166') AS parte_id,
        40133 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40133) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0353') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0297') AS parte_id,
        30011 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0220') AS parte_id,
        30003 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0346') AS parte_id,
        40602 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40602) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0198') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0149') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0451') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0254') AS parte_id,
        20005 AS precio_id,
        7.5 AS cantidad,
        '2025-10-10' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0157') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0080') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0260') AS parte_id,
        40999 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40999) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0347') AS parte_id,
        41045 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41045) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        40830 AS precio_id,
        1.0 AS cantidad,
        '2025-10-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40830) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0377') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0356') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0287') AS parte_id,
        40059 AS precio_id,
        3.5 AS cantidad,
        '2025-09-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0451') AS parte_id,
        41047 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41047) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40798 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        30002 AS precio_id,
        1.0 AS cantidad,
        '2025-09-24' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0357') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0157') AS parte_id,
        40764 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40764) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0485') AS parte_id,
        20004 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0017') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0522') AS parte_id,
        20002 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0331') AS parte_id,
        40341 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40341) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0118') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0395') AS parte_id,
        40243 AS precio_id,
        4.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40243) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0316') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0186') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0389') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0331') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        40843 AS precio_id,
        1.0 AS cantidad,
        '2025-10-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40843) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        41076 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41076) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0406') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0053') AS parte_id,
        20004 AS precio_id,
        26.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0382') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0306') AS parte_id,
        40629 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40629) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0309') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0453') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0056') AS parte_id,
        30012 AS precio_id,
        15.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0275') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0062') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        40736 AS precio_id,
        1.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40736) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0061') AS parte_id,
        30012 AS precio_id,
        14.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0352') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0289') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0395') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-21' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0377') AS parte_id,
        40759 AS precio_id,
        2.0 AS cantidad,
        '2025-10-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40759) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0229') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        30001 AS precio_id,
        4.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0144') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0164') AS parte_id,
        30003 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0313') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0475') AS parte_id,
        40655 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40655) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0322') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0464') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        41016 AS precio_id,
        29.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41016) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0272') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0224') AS parte_id,
        40612 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40612) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0151') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0144') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        40589 AS precio_id,
        1.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40589) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0515') AS parte_id,
        40831 AS precio_id,
        5.0 AS cantidad,
        '2025-11-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0264') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0440') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-20' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0233') AS parte_id,
        41048 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41048) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0150') AS parte_id,
        40646 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40646) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0346') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0303') AS parte_id,
        40608 AS precio_id,
        1.0 AS cantidad,
        '2025-10-16' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40608) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0258') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0407') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        '2025-10-14' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0190') AS parte_id,
        40014 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40014) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        '2025-09-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        '2025-09-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0194') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0184') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0351') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0441') AS parte_id,
        40798 AS precio_id,
        2.0 AS cantidad,
        '2025-10-21' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0166') AS parte_id,
        30003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0454') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0191') AS parte_id,
        40764 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40764) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0336') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0149') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0130') AS parte_id,
        30012 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0397') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-10' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0198') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0249') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        40830 AS precio_id,
        1.0 AS cantidad,
        '2025-10-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40830) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 5/28 (registros 401-500)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0079') AS parte_id,
        30011 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0465') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0126') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0347') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0266') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        '2025-09-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0440') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        '2025-10-21' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        20003 AS precio_id,
        22.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0011') AS parte_id,
        40717 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0235') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0139') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0204') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0094') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0397') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0151') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0387') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0176') AS parte_id,
        40407 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40407) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0104') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0328') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0177') AS parte_id,
        30011 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0022') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0407') AS parte_id,
        41046 AS precio_id,
        1.0 AS cantidad,
        '2025-10-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0145') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0155') AS parte_id,
        40560 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40560) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0397') AS parte_id,
        41065 AS precio_id,
        5.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41065) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0020') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0354') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0371') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0426') AS parte_id,
        40798 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0154') AS parte_id,
        40560 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40560) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0099') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0271') AS parte_id,
        20002 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0154') AS parte_id,
        40764 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40764) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0498') AS parte_id,
        30011 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0432') AS parte_id,
        40717 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0189') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0296') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0393') AS parte_id,
        40643 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40643) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0303') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        '2025-10-16' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0468') AS parte_id,
        40634 AS precio_id,
        2.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40634) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        30001 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0337') AS parte_id,
        30011 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0246') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-05' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0113') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0213') AS parte_id,
        30003 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'GF/0006') AS parte_id,
        20001 AS precio_id,
        184.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0370') AS parte_id,
        20003 AS precio_id,
        9.0 AS cantidad,
        '2025-10-15' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0172') AS parte_id,
        40105 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40105) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0298') AS parte_id,
        20007 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0269') AS parte_id,
        40815 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40815) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0441') AS parte_id,
        40646 AS precio_id,
        2.0 AS cantidad,
        '2025-10-21' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40646) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0180') AS parte_id,
        40137 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40137) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0179') AS parte_id,
        30011 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0189') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0139') AS parte_id,
        40644 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40644) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0458') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0272') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0204') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        40470 AS precio_id,
        1.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40470) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0043') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0422') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0493') AS parte_id,
        40589 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40589) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0471') AS parte_id,
        41132 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41132) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0264') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0180') AS parte_id,
        40553 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40553) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0129') AS parte_id,
        30011 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0162') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0014') AS parte_id,
        40838 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40838) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0201') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0098') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40325 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40325) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0214') AS parte_id,
        30011 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0274') AS parte_id,
        20004 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0154') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0304') AS parte_id,
        20005 AS precio_id,
        8.0 AS cantidad,
        '2025-10-16' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0180') AS parte_id,
        40878 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40878) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0220') AS parte_id,
        40024 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40024) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0494') AS parte_id,
        40798 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0195') AS parte_id,
        20004 AS precio_id,
        10.0 AS cantidad,
        '2025-09-15' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0217') AS parte_id,
        20004 AS precio_id,
        24.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20007 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0163') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0153') AS parte_id,
        40830 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40830) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0425') AS parte_id,
        40059 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        20003 AS precio_id,
        10.0 AS cantidad,
        '2025-09-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0112') AS parte_id,
        40717 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0229') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0112') AS parte_id,
        40025 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40025) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        40798 AS precio_id,
        1.5 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0064') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0258') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        40798 AS precio_id,
        3.0 AS cantidad,
        '2025-10-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0172') AS parte_id,
        40717 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0465') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0255') AS parte_id,
        40027 AS precio_id,
        1.0 AS cantidad,
        '2025-09-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40027) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0146') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0322') AS parte_id,
        20002 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0157') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0386') AS parte_id,
        30011 AS precio_id,
        8.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0328') AS parte_id,
        40798 AS precio_id,
        2.0 AS cantidad,
        '2025-09-22' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0353') AS parte_id,
        20003 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 6/28 (registros 501-600)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0306') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0218') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0320') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-19' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0272') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0175') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0144') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0389') AS parte_id,
        40027 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40027) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0515') AS parte_id,
        40838 AS precio_id,
        1.0 AS cantidad,
        '2025-11-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40838) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0122') AS parte_id,
        30011 AS precio_id,
        3.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0105') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0136') AS parte_id,
        50004 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 50004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0155') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0150') AS parte_id,
        40590 AS precio_id,
        1.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40629 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40629) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0267') AS parte_id,
        40644 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40644) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0317') AS parte_id,
        50006 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 50006) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0323') AS parte_id,
        40754 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40754) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0290') AS parte_id,
        40798 AS precio_id,
        2.0 AS cantidad,
        '2025-09-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0123') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0346') AS parte_id,
        40562 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40562) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0507') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0449') AS parte_id,
        41016 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41016) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0380') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0325') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0441') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-21' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0238') AS parte_id,
        20007 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        41042 AS precio_id,
        3.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41042) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0393') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0243') AS parte_id,
        20003 AS precio_id,
        7.0 AS cantidad,
        '2025-09-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0417') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-14' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0325') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20002 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0387') AS parte_id,
        20002 AS precio_id,
        7.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0031') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0077') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        40831 AS precio_id,
        4.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0379') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-04' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0419') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0041') AS parte_id,
        40829 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40829) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0024') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0093') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0267') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0352') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0278') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0390') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0493') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0161') AS parte_id,
        30003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0181') AS parte_id,
        30008 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30008) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0155') AS parte_id,
        20004 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0173') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'GF/0003') AS parte_id,
        10002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 10002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0009') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        40840 AS precio_id,
        1.0 AS cantidad,
        '2025-10-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40840) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        20002 AS precio_id,
        7.0 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0387') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0161') AS parte_id,
        20003 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0462') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0274') AS parte_id,
        20003 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0346') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0281') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0332') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0327') AS parte_id,
        20003 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        40831 AS precio_id,
        10.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'GF/0001') AS parte_id,
        10004 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 10004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0315') AS parte_id,
        40646 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40646) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0442') AS parte_id,
        41047 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41047) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0305') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0278') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0227') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0236') AS parte_id,
        30001 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0096') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0270') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0415') AS parte_id,
        41046 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0488') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0268') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0190') AS parte_id,
        20004 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0250') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0218') AS parte_id,
        30003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0425') AS parte_id,
        40798 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0144') AS parte_id,
        40027 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40027) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0149') AS parte_id,
        40027 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40027) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0111') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0241') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0157') AS parte_id,
        40560 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40560) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0109') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0317') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0476') AS parte_id,
        40629 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40629) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0263') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0266') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        '2025-09-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0331') AS parte_id,
        20007 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0303') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0143') AS parte_id,
        40369 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40369) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0360') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0203') AS parte_id,
        30003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0344') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0259') AS parte_id,
        40483 AS precio_id,
        1.0 AS cantidad,
        '2025-09-10' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40483) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0116') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0172') AS parte_id,
        40644 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40644) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0014') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 7/28 (registros 601-700)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0028') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0242') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0415') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0141') AS parte_id,
        40588 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40588) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0268') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0190') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0098') AS parte_id,
        41032 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41032) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0019') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0127') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0266') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-09-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0342') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0202') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0005') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        30001 AS precio_id,
        5.0 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0156') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0182') AS parte_id,
        40027 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40027) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0328') AS parte_id,
        20003 AS precio_id,
        24.0 AS cantidad,
        '2025-09-21' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0360') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0441') AS parte_id,
        40059 AS precio_id,
        0.5 AS cantidad,
        '2025-10-21' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0253') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0312') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        40625 AS precio_id,
        2.0 AS cantidad,
        '2025-10-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40625) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0212') AS parte_id,
        20004 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0397') AS parte_id,
        30008 AS precio_id,
        2.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30008) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0382') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0295') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0376') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-04' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0240') AS parte_id,
        20002 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0442') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0118') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0380') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0176') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0234') AS parte_id,
        41131 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41131) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0006') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0418') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0254') AS parte_id,
        30011 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0490') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0269') AS parte_id,
        40357 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40357) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0132') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0360') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0154') AS parte_id,
        40551 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40551) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0096') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0417') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-15' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0310') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        '2025-10-19' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0364') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0156') AS parte_id,
        41149 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41149) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0310') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        '2025-10-18' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0094') AS parte_id,
        40644 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40644) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0342') AS parte_id,
        20007 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0162') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0277') AS parte_id,
        40798 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0308') AS parte_id,
        40608 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40608) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0369') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0467') AS parte_id,
        41046 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0104') AS parte_id,
        30011 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0370') AS parte_id,
        20004 AS precio_id,
        9.0 AS cantidad,
        '2025-10-16' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0214') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0417') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-15' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0431') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0025') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0228') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0397') AS parte_id,
        30008 AS precio_id,
        1.0 AS cantidad,
        '2025-10-14' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30008) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0236') AS parte_id,
        30008 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30008) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0350') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0405') AS parte_id,
        40798 AS precio_id,
        1.5 AS cantidad,
        '2025-10-28' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0159') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0410') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        40820 AS precio_id,
        2.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40820) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        20003 AS precio_id,
        20.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0026') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0300') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0192') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0306') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0014') AS parte_id,
        20002 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0095') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0378') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        20004 AS precio_id,
        4.0 AS cantidad,
        '2025-09-24' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0437') AS parte_id,
        40646 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40646) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0244') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0391') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0126') AS parte_id,
        40717 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0331') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        30011 AS precio_id,
        5.0 AS cantidad,
        '2025-09-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0164') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0308') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0416') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0265') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0316') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0220') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        '2025-10-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0152') AS parte_id,
        40764 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40764) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0265') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40366 AS precio_id,
        4.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40366) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0115') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0357') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0218') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0447') AS parte_id,
        41184 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41184) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        30002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0304') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0121') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 8/28 (registros 701-800)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0187') AS parte_id,
        40025 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40025) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        40107 AS precio_id,
        2.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40107) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0360') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        '2025-09-28' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0303') AS parte_id,
        40754 AS precio_id,
        2.0 AS cantidad,
        '2025-10-16' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40754) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0233') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40562 AS precio_id,
        7.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40562) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0049') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0441') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        '2025-10-21' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0384') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0246') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-04' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0360') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0082') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0133') AS parte_id,
        30004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0496') AS parte_id,
        40845 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40845) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0466') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0161') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0231') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0254') AS parte_id,
        20005 AS precio_id,
        8.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0389') AS parte_id,
        40764 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40764) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0238') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-09-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0314') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0143') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0221') AS parte_id,
        30011 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0207') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0476') AS parte_id,
        41185 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41185) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0470') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0454') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0301') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0511') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0491') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0330') AS parte_id,
        41046 AS precio_id,
        1.5 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0105') AS parte_id,
        41048 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41048) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0242') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0480') AS parte_id,
        40838 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40838) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0137') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        30011 AS precio_id,
        4.0 AS cantidad,
        '2025-09-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0411') AS parte_id,
        40014 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40014) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0265') AS parte_id,
        40475 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40475) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0069') AS parte_id,
        30011 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0186') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0182') AS parte_id,
        30003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0170') AS parte_id,
        20004 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        40798 AS precio_id,
        4.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0182') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0189') AS parte_id,
        20004 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0497') AS parte_id,
        40551 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40551) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40831 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0303') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0274') AS parte_id,
        30011 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0197') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0058') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0288') AS parte_id,
        40026 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40026) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0067') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0467') AS parte_id,
        40644 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40644) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0012') AS parte_id,
        40717 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0268') AS parte_id,
        41174 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41174) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40588 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40588) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0224') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0304') AS parte_id,
        40615 AS precio_id,
        1.0 AS cantidad,
        '2025-09-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40615) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0174') AS parte_id,
        41039 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41039) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0108') AS parte_id,
        40136 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40136) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0029') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0372') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        '2025-09-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0018') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0346') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0201') AS parte_id,
        40798 AS precio_id,
        1.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0269') AS parte_id,
        41007 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0178') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0308') AS parte_id,
        40562 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40562) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0349') AS parte_id,
        40059 AS precio_id,
        3.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0273') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0279') AS parte_id,
        20002 AS precio_id,
        3.0 AS cantidad,
        '2025-10-10' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0187') AS parte_id,
        20004 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0293') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0236') AS parte_id,
        20002 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0484') AS parte_id,
        40823 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40823) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0367') AS parte_id,
        41177 AS precio_id,
        1.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41177) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0476') AS parte_id,
        40614 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40614) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0180') AS parte_id,
        40798 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0302') AS parte_id,
        40829 AS precio_id,
        10.0 AS cantidad,
        '2025-09-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40829) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        30003 AS precio_id,
        5.0 AS cantidad,
        '2025-09-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0267') AS parte_id,
        40059 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0500') AS parte_id,
        40664 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40664) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0444') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0464') AS parte_id,
        41048 AS precio_id,
        1.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41048) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        20002 AS precio_id,
        4.0 AS cantidad,
        '2025-09-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0350') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0509') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0187') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0203') AS parte_id,
        41138 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41138) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0388') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0036') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0310') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-19' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0051') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        30008 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30008) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0196') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0440') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-21' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0449') AS parte_id,
        20003 AS precio_id,
        20.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 9/28 (registros 801-900)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0209') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0378') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0115') AS parte_id,
        30003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0272') AS parte_id,
        30011 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0199') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0052') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0496') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0240') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0469') AS parte_id,
        40798 AS precio_id,
        3.0 AS cantidad,
        '2025-10-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0026') AS parte_id,
        40802 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40802) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        30002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0104') AS parte_id,
        20003 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0023') AS parte_id,
        30011 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0235') AS parte_id,
        40057 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40057) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        40644 AS precio_id,
        6.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40644) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0219') AS parte_id,
        30011 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0438') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0387') AS parte_id,
        30001 AS precio_id,
        1.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0510') AS parte_id,
        40764 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40764) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0176') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0203') AS parte_id,
        40645 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40645) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0161') AS parte_id,
        20004 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0474') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0254') AS parte_id,
        20002 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        30003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0376') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0150') AS parte_id,
        20004 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0289') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0135') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0474') AS parte_id,
        40871 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40871) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0389') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0262') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0419') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0109') AS parte_id,
        30003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0500') AS parte_id,
        20004 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0387') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0229') AS parte_id,
        30003 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0148') AS parte_id,
        20003 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20003 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        40840 AS precio_id,
        1.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40840) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0204') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        40590 AS precio_id,
        12.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0248') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        '2025-09-04' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0152') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40831 AS precio_id,
        10.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0470') AS parte_id,
        40563 AS precio_id,
        1.0 AS cantidad,
        '2025-10-27' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40563) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0261') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0153') AS parte_id,
        40838 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40838) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0387') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0319') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0174') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0417') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-14' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0379') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-04' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0353') AS parte_id,
        30003 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0381') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0462') AS parte_id,
        40014 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40014) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        40839 AS precio_id,
        1.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40839) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0245') AS parte_id,
        40761 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40761) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0234') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0442') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0381') AS parte_id,
        20004 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0053') AS parte_id,
        40849 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40849) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0377') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0489') AS parte_id,
        40798 AS precio_id,
        2.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0471') AS parte_id,
        40692 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40692) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0409') AS parte_id,
        20004 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        40629 AS precio_id,
        3.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40629) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0519') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0353') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        '2025-11-05' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0070') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0202') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0222') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0257') AS parte_id,
        40798 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        30001 AS precio_id,
        1.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0176') AS parte_id,
        41140 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41140) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0129') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0045') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0333') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0328') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        '2025-09-22' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0262') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0377') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0213') AS parte_id,
        20003 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0130') AS parte_id,
        30011 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0190') AS parte_id,
        30003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0123') AS parte_id,
        30011 AS precio_id,
        3.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0494') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0441') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-20' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0403') AS parte_id,
        40646 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40646) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0437') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0469') AS parte_id,
        40001 AS precio_id,
        1.0 AS cantidad,
        '2025-10-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0278') AS parte_id,
        40026 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40026) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0105') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0388') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0285') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0429') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0180') AS parte_id,
        20004 AS precio_id,
        24.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0121') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0049') AS parte_id,
        30011 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 10/28 (registros 901-1000)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0381') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0208') AS parte_id,
        20007 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40798 AS precio_id,
        15.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0287') AS parte_id,
        41032 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41032) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0187') AS parte_id,
        20002 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0086') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0412') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0012') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0347') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0171') AS parte_id,
        41037 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41037) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0463') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        40107 AS precio_id,
        2.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40107) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0175') AS parte_id,
        40009 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40009) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0432') AS parte_id,
        40764 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40764) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0488') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0025') AS parte_id,
        40561 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40561) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0227') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0497') AS parte_id,
        40562 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40562) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0379') AS parte_id,
        20005 AS precio_id,
        8.0 AS cantidad,
        '2025-10-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        41032 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41032) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0309') AS parte_id,
        40611 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40611) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0258') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0449') AS parte_id,
        40598 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40598) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0432') AS parte_id,
        40611 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40611) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0469') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        '2025-10-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0424') AS parte_id,
        20002 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0468') AS parte_id,
        40363 AS precio_id,
        1.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40363) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0333') AS parte_id,
        20007 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0266') AS parte_id,
        40829 AS precio_id,
        10.0 AS cantidad,
        '2025-09-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40829) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0194') AS parte_id,
        20007 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0275') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0291') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        30001 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0425') AS parte_id,
        40014 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40014) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0157') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0215') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0474') AS parte_id,
        41184 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41184) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0196') AS parte_id,
        20004 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0255') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        '2025-09-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0408') AS parte_id,
        20004 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0056') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0470') AS parte_id,
        41043 AS precio_id,
        1.0 AS cantidad,
        '2025-10-27' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41043) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0345') AS parte_id,
        30011 AS precio_id,
        12.0 AS cantidad,
        '2025-09-22' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0387') AS parte_id,
        20002 AS precio_id,
        4.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40593 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40593) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0139') AS parte_id,
        20007 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0392') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        30002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0005') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0486') AS parte_id,
        40590 AS precio_id,
        1.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0492') AS parte_id,
        20004 AS precio_id,
        24.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0156') AS parte_id,
        40348 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40348) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0147') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0377') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-10-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0061') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0151') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0285') AS parte_id,
        20003 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0290') AS parte_id,
        40831 AS precio_id,
        2.0 AS cantidad,
        '2025-10-16' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0094') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0468') AS parte_id,
        41184 AS precio_id,
        1.0 AS cantidad,
        '2025-10-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41184) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0505') AS parte_id,
        20004 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0476') AS parte_id,
        41195 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41195) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        40099 AS precio_id,
        1.0 AS cantidad,
        '2025-09-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40099) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0336') AS parte_id,
        20003 AS precio_id,
        10.0 AS cantidad,
        '2025-09-24' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0310') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        41076 AS precio_id,
        24.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41076) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0213') AS parte_id,
        20007 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0310') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-18' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0218') AS parte_id,
        40611 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40611) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0508') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0507') AS parte_id,
        40717 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0009') AS parte_id,
        40764 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40764) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0393') AS parte_id,
        41045 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41045) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0505') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0069') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0374') AS parte_id,
        20005 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0218') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0178') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0175') AS parte_id,
        20004 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0266') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        '2025-09-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0224') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0330') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        '2025-09-19' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0402') AS parte_id,
        40643 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40643) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0256') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0269') AS parte_id,
        41042 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41042) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0320') AS parte_id,
        30011 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        20002 AS precio_id,
        7.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        30002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        20003 AS precio_id,
        10.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0099') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0120') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40755 AS precio_id,
        1.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40755) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0271') AS parte_id,
        40026 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40026) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0469') AS parte_id,
        40108 AS precio_id,
        1.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40108) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        41133 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41133) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        41057 AS precio_id,
        4.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41057) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0432') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0375') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 11/28 (registros 1001-1100)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0095') AS parte_id,
        20005 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        30002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0377') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0054') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0468') AS parte_id,
        41037 AS precio_id,
        40.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41037) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0170') AS parte_id,
        41114 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41114) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0503') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0238') AS parte_id,
        40028 AS precio_id,
        1.0 AS cantidad,
        '2025-09-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40028) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        20003 AS precio_id,
        24.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0115') AS parte_id,
        40598 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40598) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0155') AS parte_id,
        30003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0407') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0123') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0288') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0258') AS parte_id,
        40012 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0266') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0135') AS parte_id,
        20002 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0106') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0269') AS parte_id,
        40823 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40823) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0376') AS parte_id,
        30003 AS precio_id,
        15.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0346') AS parte_id,
        41181 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41181) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0468') AS parte_id,
        40831 AS precio_id,
        3.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0135') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0153') AS parte_id,
        20004 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0240') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0449') AS parte_id,
        41155 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41155) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0303') AS parte_id,
        40562 AS precio_id,
        3.0 AS cantidad,
        '2025-10-16' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40562) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0425') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0476') AS parte_id,
        41132 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41132) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0405') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-28' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0195') AS parte_id,
        40717 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0438') AS parte_id,
        40764 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40764) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0290') AS parte_id,
        40099 AS precio_id,
        0.5 AS cantidad,
        '2025-09-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40099) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0188') AS parte_id,
        20003 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        20002 AS precio_id,
        4.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0286') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0328') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-22' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0146') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0259') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        '2025-09-10' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0244') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0344') AS parte_id,
        20002 AS precio_id,
        17.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0201') AS parte_id,
        20007 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0236') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0369') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0123') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0025') AS parte_id,
        40754 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40754) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0395') AS parte_id,
        40846 AS precio_id,
        1.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40846) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0025') AS parte_id,
        41039 AS precio_id,
        30.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41039) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0303') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        '2025-10-16' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0077') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0318') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0458') AS parte_id,
        40831 AS precio_id,
        5.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        20004 AS precio_id,
        10.0 AS cantidad,
        '2025-09-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0293') AS parte_id,
        41048 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41048) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-09-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0305') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0310') AS parte_id,
        30009 AS precio_id,
        2.0 AS cantidad,
        '2025-10-18' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30009) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40931 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40931) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0149') AS parte_id,
        50016 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 50016) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0199') AS parte_id,
        30003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0220') AS parte_id,
        40798 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0303') AS parte_id,
        40830 AS precio_id,
        1.0 AS cantidad,
        '2025-10-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40830) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0375') AS parte_id,
        40629 AS precio_id,
        2.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40629) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0373') AS parte_id,
        20005 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        41016 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41016) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0164') AS parte_id,
        40025 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40025) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0101') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        20005 AS precio_id,
        20.0 AS cantidad,
        '2025-09-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0238') AS parte_id,
        40798 AS precio_id,
        0.5 AS cantidad,
        '2025-09-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0131') AS parte_id,
        20007 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0273') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0490') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0151') AS parte_id,
        30003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0492') AS parte_id,
        40798 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        41076 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41076) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0357') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0117') AS parte_id,
        30003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0171') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        41033 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41033) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0367') AS parte_id,
        41195 AS precio_id,
        1.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41195) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0408') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0142') AS parte_id,
        40798 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0470') AS parte_id,
        40479 AS precio_id,
        1.0 AS cantidad,
        '2025-10-27' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40479) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0255') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0469') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        '2025-10-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0315') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0009') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0382') AS parte_id,
        40615 AS precio_id,
        1.0 AS cantidad,
        '2025-10-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40615) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0497') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0035') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0143') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0123') AS parte_id,
        40798 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0197') AS parte_id,
        40552 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40552) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0301') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0320') AS parte_id,
        41004 AS precio_id,
        1.0 AS cantidad,
        '2025-09-19' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0257') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 12/28 (registros 1101-1200)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0376') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        '2025-09-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0252') AS parte_id,
        20003 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0153') AS parte_id,
        40831 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0188') AS parte_id,
        40590 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0105') AS parte_id,
        40646 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40646) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        40659 AS precio_id,
        2.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40659) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0048') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        40830 AS precio_id,
        10.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40830) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0260') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        30003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0468') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0268') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0302') AS parte_id,
        40829 AS precio_id,
        5.0 AS cantidad,
        '2025-09-18' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40829) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0373') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0178') AS parte_id,
        30003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0157') AS parte_id,
        41149 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41149) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0419') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0287') AS parte_id,
        20003 AS precio_id,
        36.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0168') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        41032 AS precio_id,
        25.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41032) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0321') AS parte_id,
        20003 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0341') AS parte_id,
        20005 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0227') AS parte_id,
        40028 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40028) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0195') AS parte_id,
        20002 AS precio_id,
        12.0 AS cantidad,
        '2025-09-18' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0290') AS parte_id,
        40831 AS precio_id,
        3.0 AS cantidad,
        '2025-09-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0516') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0269') AS parte_id,
        41181 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41181) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0321') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0086') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0468') AS parte_id,
        40551 AS precio_id,
        1.0 AS cantidad,
        '2025-10-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40551) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20001 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0350') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0137') AS parte_id,
        30004 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0080') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0214') AS parte_id,
        20003 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0128') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0323') AS parte_id,
        40764 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40764) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0248') AS parte_id,
        40553 AS precio_id,
        1.0 AS cantidad,
        '2025-09-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40553) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0304') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0440') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-21' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0141') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-10-28' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0191') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0287') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0259') AS parte_id,
        41181 AS precio_id,
        1.0 AS cantidad,
        '2025-09-10' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41181) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0141') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0253') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0284') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0259') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0500') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        20003 AS precio_id,
        20.0 AS cantidad,
        '2025-09-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0350') AS parte_id,
        40011 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        40930 AS precio_id,
        1.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40930) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0494') AS parte_id,
        40108 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40108) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0244') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0366') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0229') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0234') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0200') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        41016 AS precio_id,
        12.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41016) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0301') AS parte_id,
        20003 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0146') AS parte_id,
        30011 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0336') AS parte_id,
        30011 AS precio_id,
        11.0 AS cantidad,
        '2025-09-23' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0276') AS parte_id,
        20002 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0144') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0442') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0302') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-18' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0394') AS parte_id,
        40024 AS precio_id,
        1.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40024) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        40590 AS precio_id,
        1.5 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0466') AS parte_id,
        30011 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0217') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0443') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0445') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0432') AS parte_id,
        40831 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0276') AS parte_id,
        20002 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'GF/0005') AS parte_id,
        10002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 10002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0377') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0198') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0110') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0260') AS parte_id,
        40831 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0220') AS parte_id,
        20004 AS precio_id,
        24.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0426') AS parte_id,
        40843 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40843) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0355') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0248') AS parte_id,
        40873 AS precio_id,
        2.0 AS cantidad,
        '2025-09-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40873) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0316') AS parte_id,
        40798 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0127') AS parte_id,
        20003 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0357') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0075') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0340') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0152') AS parte_id,
        40611 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40611) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0365') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0182') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0330') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        '2025-09-24' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0318') AS parte_id,
        40629 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40629) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        40798 AS precio_id,
        12.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        40341 AS precio_id,
        1.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40341) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0328') AS parte_id,
        40829 AS precio_id,
        10.0 AS cantidad,
        '2025-09-23' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40829) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0291') AS parte_id,
        20005 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 13/28 (registros 1201-1300)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0133') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0074') AS parte_id,
        30012 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0239') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0081') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0114') AS parte_id,
        20007 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0384') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0122') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0112') AS parte_id,
        40709 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40709) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        41133 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41133) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0410') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0360') AS parte_id,
        40562 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40562) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0428') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0277') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0437') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0294') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0134') AS parte_id,
        30011 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0032') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        41084 AS precio_id,
        14.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41084) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        30001 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0382') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0193') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        30002 AS precio_id,
        1.0 AS cantidad,
        '2025-09-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0486') AS parte_id,
        20003 AS precio_id,
        24.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0468') AS parte_id,
        40845 AS precio_id,
        1.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40845) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        30001 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0404') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0111') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0495') AS parte_id,
        40140 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40140) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0153') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0295') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0262') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0354') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0314') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0296') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0492') AS parte_id,
        40059 AS precio_id,
        1.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0162') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        40350 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40350) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0078') AS parte_id,
        30011 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0251') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0103') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0121') AS parte_id,
        30003 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0155') AS parte_id,
        40764 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40764) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0342') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0326') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0345') AS parte_id,
        20002 AS precio_id,
        12.0 AS cantidad,
        '2025-09-22' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0492') AS parte_id,
        41061 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41061) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0518') AS parte_id,
        20005 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0015') AS parte_id,
        30011 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        41014 AS precio_id,
        12.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41014) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        30002 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0290') AS parte_id,
        41066 AS precio_id,
        2.5 AS cantidad,
        '2025-09-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41066) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0490') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40561 AS precio_id,
        2.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40561) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0181') AS parte_id,
        40587 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40587) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0172') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0173') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        40602 AS precio_id,
        30.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40602) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0272') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0379') AS parte_id,
        40006 AS precio_id,
        1.0 AS cantidad,
        '2025-10-04' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40006) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0299') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0363') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0146') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0113') AS parte_id,
        40709 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40709) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0155') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0258') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0244') AS parte_id,
        40798 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0119') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0387') AS parte_id,
        40586 AS precio_id,
        6.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40586) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0240') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0287') AS parte_id,
        41096 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41096) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0181') AS parte_id,
        20003 AS precio_id,
        40.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0346') AS parte_id,
        40553 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40553) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0170') AS parte_id,
        40059 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0184') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0116') AS parte_id,
        30003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0215') AS parte_id,
        40831 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0395') AS parte_id,
        20002 AS precio_id,
        6.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0129') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0499') AS parte_id,
        40831 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0194') AS parte_id,
        40012 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0044') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0464') AS parte_id,
        40646 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40646) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0039') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0309') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0150') AS parte_id,
        40717 AS precio_id,
        0.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0014') AS parte_id,
        40757 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40757) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0491') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0158') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0132') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0218') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0174') AS parte_id,
        30008 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30008) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0295') AS parte_id,
        41046 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0075') AS parte_id,
        30011 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0410') AS parte_id,
        40657 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40657) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0485') AS parte_id,
        40615 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40615) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0004') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0022') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0072') AS parte_id,
        20004 AS precio_id,
        8.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 14/28 (registros 1301-1400)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0288') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0110') AS parte_id,
        40014 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40014) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0304') AS parte_id,
        40561 AS precio_id,
        1.0 AS cantidad,
        '2025-09-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40561) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0053') AS parte_id,
        30011 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        41155 AS precio_id,
        1.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41155) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0181') AS parte_id,
        40099 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40099) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0411') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0010') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0316') AS parte_id,
        40841 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40841) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'GF/0005') AS parte_id,
        10003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 10003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        '2025-09-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0361') AS parte_id,
        40026 AS precio_id,
        2.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40026) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'GF/0001') AS parte_id,
        10002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 10002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0283') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0112') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0502') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0249') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0178') AS parte_id,
        40027 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40027) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0192') AS parte_id,
        20004 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0503') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0076') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0323') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0184') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0253') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0126') AS parte_id,
        20002 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0282') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0115') AS parte_id,
        41046 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0371') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0203') AS parte_id,
        20007 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0037') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0489') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0097') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0106') AS parte_id,
        41047 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41047) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0156') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0440') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-20' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        30003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0265') AS parte_id,
        40099 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40099) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0083') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0182') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0311') AS parte_id,
        40798 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0277') AS parte_id,
        20005 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        41187 AS precio_id,
        1.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41187) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0152') AS parte_id,
        20004 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0263') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0263') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0307') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0397') AS parte_id,
        40830 AS precio_id,
        5.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40830) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0250') AS parte_id,
        40016 AS precio_id,
        1.0 AS cantidad,
        '2025-09-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40016) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0483') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0520') AS parte_id,
        41046 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0013') AS parte_id,
        20003 AS precio_id,
        15.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0329') AS parte_id,
        40611 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40611) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0297') AS parte_id,
        30012 AS precio_id,
        20.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0255') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        '2025-09-12' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        40360 AS precio_id,
        1.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40360) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0328') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-23' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0421') AS parte_id,
        40656 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40656) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        40798 AS precio_id,
        3.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0434') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        '2025-10-21' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0380') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0269') AS parte_id,
        40640 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40640) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0330') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0341') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40351 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40351) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0345') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0255') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        40831 AS precio_id,
        10.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0246') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-04' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0296') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0115') AS parte_id,
        40133 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40133) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0236') AS parte_id,
        40014 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40014) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0336') AS parte_id,
        20002 AS precio_id,
        10.0 AS cantidad,
        '2025-09-24' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0211') AS parte_id,
        20007 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0216') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0385') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0351') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0469') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0496') AS parte_id,
        40831 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0188') AS parte_id,
        40009 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40009) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0387') AS parte_id,
        40480 AS precio_id,
        1.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40480) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0118') AS parte_id,
        20005 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0317') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0074') AS parte_id,
        30011 AS precio_id,
        3.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0367') AS parte_id,
        20003 AS precio_id,
        24.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0341') AS parte_id,
        40553 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40553) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0254') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0375') AS parte_id,
        41032 AS precio_id,
        1.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41032) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0055') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0358') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        30002 AS precio_id,
        1.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0170') AS parte_id,
        20003 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0518') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0220') AS parte_id,
        20003 AS precio_id,
        24.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0395') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0320') AS parte_id,
        40646 AS precio_id,
        2.0 AS cantidad,
        '2025-09-19' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40646) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0399') AS parte_id,
        30009 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30009) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0221') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0471') AS parte_id,
        41188 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41188) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 15/28 (registros 1401-1500)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0223') AS parte_id,
        20002 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40798 AS precio_id,
        3.0 AS cantidad,
        '2025-09-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0143') AS parte_id,
        40560 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40560) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0399') AS parte_id,
        30011 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        41020 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41020) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0075') AS parte_id,
        30012 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0186') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0050') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0377') AS parte_id,
        41042 AS precio_id,
        100.0 AS cantidad,
        '2025-10-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41042) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0003') AS parte_id,
        30012 AS precio_id,
        12.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0387') AS parte_id,
        40587 AS precio_id,
        5.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40587) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0258') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0248') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-04' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0399') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0246') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        '2025-09-05' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0094') AS parte_id,
        40587 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40587) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40650 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40650) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0305') AS parte_id,
        40712 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40712) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0400') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0489') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'GF/0002') AS parte_id,
        20001 AS precio_id,
        160.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        40184 AS precio_id,
        1.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40184) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0238') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        '2025-09-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0318') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40798 AS precio_id,
        4.0 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0472') AS parte_id,
        41046 AS precio_id,
        1.5 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0255') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        '2025-09-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0159') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0268') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40107 AS precio_id,
        3.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40107) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0397') AS parte_id,
        30003 AS precio_id,
        7.0 AS cantidad,
        '2025-10-10' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0307') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0109') AS parte_id,
        40136 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40136) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0247') AS parte_id,
        30011 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0181') AS parte_id,
        41116 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41116) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0331') AS parte_id,
        40754 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40754) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0314') AS parte_id,
        20002 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0498') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0290') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-16' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0252') AS parte_id,
        41149 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41149) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0321') AS parte_id,
        41046 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0276') AS parte_id,
        30011 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0079') AS parte_id,
        20004 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0106') AS parte_id,
        40645 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40645) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0167') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0158') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0405') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-28' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0361') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0508') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0215') AS parte_id,
        40603 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40603) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        41194 AS precio_id,
        1.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41194) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0063') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0324') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0161') AS parte_id,
        41046 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0136') AS parte_id,
        40753 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40753) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0388') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0387') AS parte_id,
        40760 AS precio_id,
        1.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40760) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40693 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40693) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0238') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        '2025-09-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40810 AS precio_id,
        1.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40810) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0173') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0231') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0490') AS parte_id,
        40019 AS precio_id,
        1.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40019) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0396') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40178 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40178) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0204') AS parte_id,
        41187 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41187) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0151') AS parte_id,
        20004 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0304') AS parte_id,
        20002 AS precio_id,
        4.0 AS cantidad,
        '2025-10-16' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0222') AS parte_id,
        30008 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30008) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0014') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0222') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        30008 AS precio_id,
        1.0 AS cantidad,
        '2025-09-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30008) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'GF/0005') AS parte_id,
        10004 AS precio_id,
        5.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 10004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0272') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0243') AS parte_id,
        20005 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0345') AS parte_id,
        41062 AS precio_id,
        6.0 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41062) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        30003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0281') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0361') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0475') AS parte_id,
        40107 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40107) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0268') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0320') AS parte_id,
        40708 AS precio_id,
        1.0 AS cantidad,
        '2025-09-19' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40708) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0357') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0348') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        30002 AS precio_id,
        1.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40107 AS precio_id,
        20.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40107) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        41181 AS precio_id,
        7.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41181) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0247') AS parte_id,
        30009 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30009) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0065') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0255') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        '2025-09-12' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        30008 AS precio_id,
        1.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30008) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0294') AS parte_id,
        40646 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40646) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0204') AS parte_id,
        41048 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41048) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0375') AS parte_id,
        20005 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0422') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0073') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0447') AS parte_id,
        40717 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0364') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40624 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40624) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 16/28 (registros 1501-1600)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0395') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0346') AS parte_id,
        40832 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40832) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0432') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0142') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0080') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0346') AS parte_id,
        40798 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0087') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0207') AS parte_id,
        30003 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0374') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0158') AS parte_id,
        30003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0325') AS parte_id,
        20002 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0295') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0095') AS parte_id,
        20002 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0266') AS parte_id,
        40551 AS precio_id,
        1.0 AS cantidad,
        '2025-09-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40551) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0285') AS parte_id,
        30011 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0172') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0256') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0397') AS parte_id,
        20003 AS precio_id,
        24.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0115') AS parte_id,
        41014 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41014) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        20003 AS precio_id,
        22.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0131') AS parte_id,
        30003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0254') AS parte_id,
        20005 AS precio_id,
        8.0 AS cantidad,
        '2025-10-28' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0183') AS parte_id,
        30012 AS precio_id,
        30.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0041') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0217') AS parte_id,
        20003 AS precio_id,
        48.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0315') AS parte_id,
        41048 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41048) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-04' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0320') AS parte_id,
        40165 AS precio_id,
        1.0 AS cantidad,
        '2025-09-19' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40165) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0397') AS parte_id,
        20002 AS precio_id,
        9.0 AS cantidad,
        '2025-10-13' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0248') AS parte_id,
        40840 AS precio_id,
        1.0 AS cantidad,
        '2025-09-04' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40840) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0115') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0030') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0455') AS parte_id,
        20005 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        20004 AS precio_id,
        10.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0279') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        '2025-10-23' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0294') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0413') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        41046 AS precio_id,
        13.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0181') AS parte_id,
        40831 AS precio_id,
        15.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0304') AS parte_id,
        20002 AS precio_id,
        5.0 AS cantidad,
        '2025-10-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0475') AS parte_id,
        40798 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0104') AS parte_id,
        20004 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        40588 AS precio_id,
        1.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40588) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0098') AS parte_id,
        30003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0290') AS parte_id,
        40841 AS precio_id,
        1.0 AS cantidad,
        '2025-09-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40841) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0190') AS parte_id,
        20003 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0479') AS parte_id,
        20002 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0518') AS parte_id,
        30011 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        '2025-09-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0370') AS parte_id,
        20003 AS precio_id,
        9.0 AS cantidad,
        '2025-10-16' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0382') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0053') AS parte_id,
        30012 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0201') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0368') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0029') AS parte_id,
        40556 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40556) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0125') AS parte_id,
        20005 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0353') AS parte_id,
        20004 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0385') AS parte_id,
        40717 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0144') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0496') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0407') AS parte_id,
        20004 AS precio_id,
        2.0 AS cantidad,
        '2025-10-14' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0210') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        40839 AS precio_id,
        1.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40839) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0248') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0174') AS parte_id,
        40561 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40561) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0061') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0265') AS parte_id,
        40551 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40551) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0320') AS parte_id,
        40362 AS precio_id,
        2.0 AS cantidad,
        '2025-09-19' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40362) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0461') AS parte_id,
        40059 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0174') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0128') AS parte_id,
        30011 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0341') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0510') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0195') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0063') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0377') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0164') AS parte_id,
        40798 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0155') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0244') AS parte_id,
        40798 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0094') AS parte_id,
        30003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0472') AS parte_id,
        20003 AS precio_id,
        20.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0115') AS parte_id,
        40644 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40644) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0087') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0480') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-23' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0332') AS parte_id,
        30011 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0269') AS parte_id,
        40754 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40754) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0114') AS parte_id,
        40014 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40014) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        40706 AS precio_id,
        2.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40706) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0001') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0130') AS parte_id,
        20004 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        30001 AS precio_id,
        1.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0352') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0273') AS parte_id,
        40025 AS precio_id,
        1.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40025) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0312') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0302') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        '2025-09-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0360') AS parte_id,
        40024 AS precio_id,
        1.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40024) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 17/28 (registros 1601-1700)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0471') AS parte_id,
        41181 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41181) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0493') AS parte_id,
        30001 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0328') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        '2025-09-24' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0321') AS parte_id,
        20004 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0115') AS parte_id,
        50018 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 50018) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0175') AS parte_id,
        20004 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0239') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0156') AS parte_id,
        40552 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40552) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0324') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0447') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0454') AS parte_id,
        40640 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40640) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0422') AS parte_id,
        40798 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        40598 AS precio_id,
        3.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40598) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0247') AS parte_id,
        20002 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0310') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-18' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0197') AS parte_id,
        40798 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0152') AS parte_id,
        40609 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40609) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0267') AS parte_id,
        41046 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0241') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        30001 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0328') AS parte_id,
        40831 AS precio_id,
        10.0 AS cantidad,
        '2025-09-23' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0347') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0180') AS parte_id,
        40371 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40371) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0203') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        30002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0495') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0251') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0370') AS parte_id,
        20004 AS precio_id,
        9.0 AS cantidad,
        '2025-10-15' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0418') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0338') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0462') AS parte_id,
        20004 AS precio_id,
        3.0 AS cantidad,
        '2025-10-27' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0101') AS parte_id,
        20003 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0247') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0289') AS parte_id,
        30011 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0168') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0469') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0328') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-22' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0319') AS parte_id,
        30012 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0376') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-04' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0513') AS parte_id,
        40659 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40659) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0180') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0387') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0089') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0003') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0320') AS parte_id,
        41015 AS precio_id,
        8.0 AS cantidad,
        '2025-09-19' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41015) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        40645 AS precio_id,
        1.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40645) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0521') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0458') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-27' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0463') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0026') AS parte_id,
        40610 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40610) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0476') AS parte_id,
        41152 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41152) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0425') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0475') AS parte_id,
        40830 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40830) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40827 AS precio_id,
        2.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40827) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0494') AS parte_id,
        20003 AS precio_id,
        24.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0421') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0391') AS parte_id,
        20002 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0190') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0252') AS parte_id,
        30011 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0113') AS parte_id,
        20002 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0152') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0378') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0464') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0295') AS parte_id,
        41125 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41125) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0283') AS parte_id,
        20002 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40595 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40595) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0431') AS parte_id,
        40611 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40611) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0104') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0260') AS parte_id,
        40108 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40108) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0394') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0093') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0169') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0396') AS parte_id,
        40611 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40611) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0060') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        40930 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40930) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0257') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        30003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0471') AS parte_id,
        41185 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41185) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0209') AS parte_id,
        20007 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0393') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0136') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0271') AS parte_id,
        20005 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0100') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0380') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0095') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0387') AS parte_id,
        30001 AS precio_id,
        1.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0304') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0245') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0310') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-19' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        20002 AS precio_id,
        5.0 AS cantidad,
        '2025-09-24' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0107') AS parte_id,
        40137 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40137) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0300') AS parte_id,
        40014 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40014) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0336') AS parte_id,
        40831 AS precio_id,
        5.0 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0311') AS parte_id,
        40059 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0191') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0381') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 18/28 (registros 1701-1800)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0431') AS parte_id,
        40344 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40344) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0407') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0224') AS parte_id,
        20002 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0361') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0108') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0006') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0198') AS parte_id,
        20004 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0361') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0136') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0389') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0467') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0082') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0045') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0497') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0228') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0004') AS parte_id,
        30011 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0154') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0218') AS parte_id,
        40553 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40553) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0470') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        30011 AS precio_id,
        3.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0461') AS parte_id,
        20003 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0419') AS parte_id,
        40473 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40473) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0339') AS parte_id,
        20007 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0302') AS parte_id,
        40831 AS precio_id,
        10.0 AS cantidad,
        '2025-09-18' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0465') AS parte_id,
        41048 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41048) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0119') AS parte_id,
        30003 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0199') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0112') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0522') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0269') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        20003 AS precio_id,
        15.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0227') AS parte_id,
        30003 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0265') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0362') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0301') AS parte_id,
        50004 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 50004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0158') AS parte_id,
        41045 AS precio_id,
        50.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41045) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0465') AS parte_id,
        40646 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40646) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0375') AS parte_id,
        40798 AS precio_id,
        2.0 AS cantidad,
        '2025-10-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40137 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40137) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0282') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0336') AS parte_id,
        20004 AS precio_id,
        10.0 AS cantidad,
        '2025-09-24' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0282') AS parte_id,
        41046 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40656 AS precio_id,
        1.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40656) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0422') AS parte_id,
        40831 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0376') AS parte_id,
        41042 AS precio_id,
        1.0 AS cantidad,
        '2025-10-04' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41042) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0422') AS parte_id,
        40838 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40838) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0329') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0147') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0319') AS parte_id,
        40027 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40027) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0489') AS parte_id,
        40059 AS precio_id,
        0.5 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0330') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0361') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0334') AS parte_id,
        30012 AS precio_id,
        20.0 AS cantidad,
        '2025-10-27' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0310') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0358') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0376') AS parte_id,
        40640 AS precio_id,
        2.0 AS cantidad,
        '2025-10-04' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40640) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0197') AS parte_id,
        20004 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        30003 AS precio_id,
        4.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0146') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0024') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0127') AS parte_id,
        30011 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0415') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0375') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        '2025-10-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0451') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0282') AS parte_id,
        40644 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40644) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0150') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0266') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-11' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0108') AS parte_id,
        41032 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41032) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0108') AS parte_id,
        40629 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40629) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0275') AS parte_id,
        40644 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40644) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0379') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        '2025-10-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        '2025-09-23' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0088') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0128') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0219') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0079') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0146') AS parte_id,
        30012 AS precio_id,
        30.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0188') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0368') AS parte_id,
        20003 AS precio_id,
        12.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0128') AS parte_id,
        40644 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40644) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0369') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0493') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0064') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        40603 AS precio_id,
        100.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40603) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0192') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0355') AS parte_id,
        30011 AS precio_id,
        12.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0347') AS parte_id,
        40643 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40643) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0041') AS parte_id,
        40838 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40838) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0153') AS parte_id,
        40605 AS precio_id,
        40.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40605) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0264') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        40588 AS precio_id,
        1.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40588) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0244') AS parte_id,
        20004 AS precio_id,
        24.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        20002 AS precio_id,
        5.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        40798 AS precio_id,
        12.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0164') AS parte_id,
        20003 AS precio_id,
        12.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0503') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0213') AS parte_id,
        20004 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0483') AS parte_id,
        40659 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40659) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0268') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        30003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 19/28 (registros 1801-1900)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0092') AS parte_id,
        20003 AS precio_id,
        1.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0366') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0106') AS parte_id,
        20002 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0370') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        40562 AS precio_id,
        2.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40562) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0420') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0439') AS parte_id,
        41047 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41047) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0142') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0120') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0477') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0245') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0189') AS parte_id,
        40798 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0149') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0107') AS parte_id,
        40028 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40028) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0400') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0416') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0336') AS parte_id,
        40031 AS precio_id,
        1.0 AS cantidad,
        '2025-09-23' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40031) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0156') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0303') AS parte_id,
        40059 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0312') AS parte_id,
        40764 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40764) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0165') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0327') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40855 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40855) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0319') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0257') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0098') AS parte_id,
        40645 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40645) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0103') AS parte_id,
        41048 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41048) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0517') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0039') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        40001 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0384') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-05' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0384') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0389') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0016') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        40629 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40629) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0158') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0330') AS parte_id,
        40644 AS precio_id,
        2.0 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40644) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0234') AS parte_id,
        40830 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40830) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0297') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0106') AS parte_id,
        40588 AS precio_id,
        1.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40588) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0353') AS parte_id,
        20004 AS precio_id,
        2.0 AS cantidad,
        '2025-11-05' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        41016 AS precio_id,
        24.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41016) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0261') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0349') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0171') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0127') AS parte_id,
        30003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0283') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40590 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0290') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-16' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0436') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        30011 AS precio_id,
        3.0 AS cantidad,
        '2025-09-04' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0078') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0084') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0276') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0084') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0391') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0298') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0482') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0309') AS parte_id,
        40764 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40764) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0137') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40829 AS precio_id,
        5.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40829) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0345') AS parte_id,
        40831 AS precio_id,
        10.0 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0234') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0277') AS parte_id,
        20002 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0236') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0168') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0013') AS parte_id,
        20002 AS precio_id,
        15.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        41076 AS precio_id,
        24.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41076) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0256') AS parte_id,
        40008 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40008) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0157') AS parte_id,
        20004 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0301') AS parte_id,
        40008 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40008) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0499') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0119') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0334') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        '2025-10-27' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0215') AS parte_id,
        20007 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0107') AS parte_id,
        40798 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0245') AS parte_id,
        20004 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0098') AS parte_id,
        20005 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0130') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0234') AS parte_id,
        40839 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40839) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0277') AS parte_id,
        40026 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40026) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        41039 AS precio_id,
        2.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41039) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0395') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0139') AS parte_id,
        30003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0285') AS parte_id,
        20002 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0380') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        40350 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40350) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0372') AS parte_id,
        20005 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0074') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        40692 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40692) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0470') AS parte_id,
        40469 AS precio_id,
        1.0 AS cantidad,
        '2025-10-27' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40469) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0368') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        '2025-09-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0266') AS parte_id,
        41037 AS precio_id,
        30.0 AS cantidad,
        '2025-09-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41037) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0521') AS parte_id,
        40026 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40026) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        40562 AS precio_id,
        1.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40562) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0257') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0461') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0238') AS parte_id,
        20002 AS precio_id,
        6.0 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 20/28 (registros 1901-2000)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0243') AS parte_id,
        30011 AS precio_id,
        7.0 AS cantidad,
        '2025-09-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0475') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0153') AS parte_id,
        30003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0387') AS parte_id,
        30002 AS precio_id,
        1.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0315') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0174') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0441') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-21' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0208') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0480') AS parte_id,
        40603 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40603) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0081') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0328') AS parte_id,
        40107 AS precio_id,
        5.0 AS cantidad,
        '2025-09-23' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40107) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0181') AS parte_id,
        30003 AS precio_id,
        11.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0356') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0397') AS parte_id,
        30003 AS precio_id,
        25.0 AS cantidad,
        '2025-10-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0095') AS parte_id,
        30011 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0443') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0472') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40773 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40773) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        40829 AS precio_id,
        20.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40829) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'GF/0003') AS parte_id,
        10004 AS precio_id,
        11.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 10004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0170') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        30002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20002 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0291') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0174') AS parte_id,
        40781 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40781) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0062') AS parte_id,
        30012 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0104') AS parte_id,
        30011 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0271') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0217') AS parte_id,
        30003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0216') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0168') AS parte_id,
        40023 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40023) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0487') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0302') AS parte_id,
        40830 AS precio_id,
        5.0 AS cantidad,
        '2025-09-18' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40830) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0107') AS parte_id,
        20002 AS precio_id,
        13.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0388') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0194') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0217') AS parte_id,
        40798 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0180') AS parte_id,
        20003 AS precio_id,
        24.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0377') AS parte_id,
        40659 AS precio_id,
        2.0 AS cantidad,
        '2025-10-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40659) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        20004 AS precio_id,
        11.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0242') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0320') AS parte_id,
        20002 AS precio_id,
        4.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0223') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0269') AS parte_id,
        40820 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40820) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        40830 AS precio_id,
        5.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40830) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0387') AS parte_id,
        20003 AS precio_id,
        24.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0373') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0128') AS parte_id,
        40025 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40025) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0303') AS parte_id,
        41181 AS precio_id,
        1.0 AS cantidad,
        '2025-10-16' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41181) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0472') AS parte_id,
        40659 AS precio_id,
        2.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40659) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0303') AS parte_id,
        40831 AS precio_id,
        1.0 AS cantidad,
        '2025-10-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0216') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0387') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        30011 AS precio_id,
        2.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0486') AS parte_id,
        40629 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40629) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0471') AS parte_id,
        41152 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41152) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0245') AS parte_id,
        40875 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40875) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0497') AS parte_id,
        41181 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41181) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0355') AS parte_id,
        20002 AS precio_id,
        12.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0343') AS parte_id,
        20003 AS precio_id,
        12.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0354') AS parte_id,
        40027 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40027) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0180') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0405') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-27' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0219') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0164') AS parte_id,
        41046 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0297') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0205') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0341') AS parte_id,
        40764 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40764) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0269') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0359') AS parte_id,
        30011 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40608 AS precio_id,
        1.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40608) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0506') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0233') AS parte_id,
        40028 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40028) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0103') AS parte_id,
        30003 AS precio_id,
        13.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0309') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0438') AS parte_id,
        41181 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41181) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        30003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0273') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0469') AS parte_id,
        20002 AS precio_id,
        4.0 AS cantidad,
        '2025-10-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0002') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0458') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-27' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0109') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0079') AS parte_id,
        30011 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0217') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0483') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        30001 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0037') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0476') AS parte_id,
        20002 AS precio_id,
        8.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0269') AS parte_id,
        40341 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40341) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0306') AS parte_id,
        40324 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40324) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0233') AS parte_id,
        40646 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40646) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0161') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0143') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0013') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0347') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0336') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        '2025-09-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 21/28 (registros 2001-2100)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0153') AS parte_id,
        40764 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40764) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0204') AS parte_id,
        30003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0056') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0161') AS parte_id,
        40694 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40694) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0062') AS parte_id,
        30011 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0327') AS parte_id,
        30011 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0380') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0437') AS parte_id,
        40798 AS precio_id,
        1.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0226') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0426') AS parte_id,
        40831 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0318') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0300') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-09-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0186') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0243') AS parte_id,
        20004 AS precio_id,
        7.0 AS cantidad,
        '2025-09-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0300') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0044') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0521') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0490') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0122') AS parte_id,
        30012 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0442') AS parte_id,
        40645 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40645) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0166') AS parte_id,
        20004 AS precio_id,
        1.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0207') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0344') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0231') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0397') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-10' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0332') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0155') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0484') AS parte_id,
        41184 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41184) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0248') AS parte_id,
        40798 AS precio_id,
        3.0 AS cantidad,
        '2025-09-04' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0239') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0405') AS parte_id,
        40014 AS precio_id,
        1.0 AS cantidad,
        '2025-10-28' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40014) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0220') AS parte_id,
        40588 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40588) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0183') AS parte_id,
        20004 AS precio_id,
        12.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0276') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0131') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0121') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0297') AS parte_id,
        30011 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0161') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0503') AS parte_id,
        40843 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40843) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0325') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0382') AS parte_id,
        20003 AS precio_id,
        10.0 AS cantidad,
        '2025-10-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0346') AS parte_id,
        30011 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        20004 AS precio_id,
        11.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0206') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0220') AS parte_id,
        40590 AS precio_id,
        1.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0166') AS parte_id,
        20003 AS precio_id,
        1.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0205') AS parte_id,
        20007 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0126') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0470') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-27' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0334') AS parte_id,
        30011 AS precio_id,
        3.0 AS cantidad,
        '2025-10-27' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0170') AS parte_id,
        40608 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40608) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0436') AS parte_id,
        41046 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0148') AS parte_id,
        30011 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0270') AS parte_id,
        20004 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0062') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0156') AS parte_id,
        40764 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40764) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0370') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0240') AS parte_id,
        40028 AS precio_id,
        1.0 AS cantidad,
        '2025-09-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40028) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0142') AS parte_id,
        20007 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0451') AS parte_id,
        40645 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40645) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0332') AS parte_id,
        20007 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        30001 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0515') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-11-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0138') AS parte_id,
        20005 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0127') AS parte_id,
        20004 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0186') AS parte_id,
        40587 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40587) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0405') AS parte_id,
        40059 AS precio_id,
        0.5 AS cantidad,
        '2025-10-28' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0362') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0158') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0267') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0486') AS parte_id,
        40099 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40099) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0344') AS parte_id,
        30002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0148') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0244') AS parte_id,
        40603 AS precio_id,
        30.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40603) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0232') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0114') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0213') AS parte_id,
        40646 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40646) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0052') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0206') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0344') AS parte_id,
        20003 AS precio_id,
        17.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0112') AS parte_id,
        30003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0391') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0403') AS parte_id,
        41048 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41048) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0287') AS parte_id,
        20002 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        41024 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41024) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0270') AS parte_id,
        40551 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40551) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0269') AS parte_id,
        40608 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40608) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0026') AS parte_id,
        40712 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40712) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0357') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0007') AS parte_id,
        40717 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0489') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0173') AS parte_id,
        40028 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40028) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0299') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0255') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-09-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 22/28 (registros 2101-2200)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0489') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0499') AS parte_id,
        40846 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40846) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0250') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0500') AS parte_id,
        40656 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40656) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0142') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0320') AS parte_id,
        41048 AS precio_id,
        2.0 AS cantidad,
        '2025-09-19' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41048) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0170') AS parte_id,
        30003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0287') AS parte_id,
        20004 AS precio_id,
        20.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0222') AS parte_id,
        40027 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40027) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0302') AS parte_id,
        40831 AS precio_id,
        15.0 AS cantidad,
        '2025-09-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40798 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0443') AS parte_id,
        40011 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0189') AS parte_id,
        20002 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0518') AS parte_id,
        30012 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        40592 AS precio_id,
        1.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40592) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0172') AS parte_id,
        41046 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0157') AS parte_id,
        40025 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40025) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0438') AS parte_id,
        40838 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40838) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0145') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0275') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0181') AS parte_id,
        40798 AS precio_id,
        12.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0382') AS parte_id,
        30001 AS precio_id,
        1.0 AS cantidad,
        '2025-10-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0460') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0149') AS parte_id,
        40601 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40601) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0381') AS parte_id,
        30011 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0312') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0357') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        '2025-09-27' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0039') AS parte_id,
        40754 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40754) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0041') AS parte_id,
        20003 AS precio_id,
        13.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0406') AS parte_id,
        20002 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0108') AS parte_id,
        30003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0176') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0502') AS parte_id,
        20004 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0471') AS parte_id,
        41076 AS precio_id,
        24.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41076) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0120') AS parte_id,
        40025 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40025) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0265') AS parte_id,
        40560 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40560) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0136') AS parte_id,
        40561 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40561) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0486') AS parte_id,
        40059 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0377') AS parte_id,
        40659 AS precio_id,
        1.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40659) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0357') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0306') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0280') AS parte_id,
        20002 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0129') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0520') AS parte_id,
        40644 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40644) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0313') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0274') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0303') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0334') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        '2025-10-27' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0344') AS parte_id,
        40025 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40025) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0441') AS parte_id,
        41048 AS precio_id,
        2.0 AS cantidad,
        '2025-10-21' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41048) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0319') AS parte_id,
        30011 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0454') AS parte_id,
        40059 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0381') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0266') AS parte_id,
        40831 AS precio_id,
        10.0 AS cantidad,
        '2025-09-11' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0180') AS parte_id,
        30003 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0360') AS parte_id,
        41181 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41181) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0106') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0075') AS parte_id,
        40846 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40846) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0484') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0497') AS parte_id,
        40754 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40754) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0179') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0397') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        '2025-10-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0053') AS parte_id,
        20003 AS precio_id,
        26.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0209') AS parte_id,
        30011 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0422') AS parte_id,
        41181 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41181) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0512') AS parte_id,
        41181 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41181) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        41042 AS precio_id,
        8.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41042) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0101') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0476') AS parte_id,
        41015 AS precio_id,
        32.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41015) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0183') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0343') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0153') AS parte_id,
        20003 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0255') AS parte_id,
        40059 AS precio_id,
        1.5 AS cantidad,
        '2025-09-12' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40324 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40324) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0201') AS parte_id,
        40492 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40492) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0439') AS parte_id,
        40059 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0361') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0181') AS parte_id,
        40107 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40107) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0320') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0269') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0172') AS parte_id,
        30003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0275') AS parte_id,
        41046 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0184') AS parte_id,
        40025 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40025) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0150') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0432') AS parte_id,
        40348 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40348) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40774 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40774) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0311') AS parte_id,
        40014 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40014) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0170') AS parte_id,
        41046 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0260') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0410') AS parte_id,
        40641 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40641) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-24' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0314') AS parte_id,
        40027 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40027) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0475') AS parte_id,
        41039 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41039) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0212') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0090') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0108') AS parte_id,
        30011 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0108') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0383') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0103') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0236') AS parte_id,
        40108 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40108) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 23/28 (registros 2201-2300)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0176') AS parte_id,
        40253 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40253) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0133') AS parte_id,
        20007 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0486') AS parte_id,
        20004 AS precio_id,
        24.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0470') AS parte_id,
        41181 AS precio_id,
        1.0 AS cantidad,
        '2025-10-27' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41181) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0222') AS parte_id,
        30003 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0343') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0367') AS parte_id,
        40480 AS precio_id,
        1.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40480) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0454') AS parte_id,
        40798 AS precio_id,
        1.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0120') AS parte_id,
        20005 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0140') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0046') AS parte_id,
        30011 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0013') AS parte_id,
        30004 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0254') AS parte_id,
        20005 AS precio_id,
        8.0 AS cantidad,
        '2025-10-16' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0373') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0472') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0401') AS parte_id,
        30011 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0381') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0011') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0287') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'GF/0001') AS parte_id,
        10001 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 10001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40191 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40191) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0163') AS parte_id,
        30003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0314') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0034') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0296') AS parte_id,
        20002 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0171') AS parte_id,
        40369 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40369) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0026') AS parte_id,
        40750 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40750) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0159') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        40590 AS precio_id,
        3.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0053') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0126') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0102') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0259') AS parte_id,
        20005 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0302') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-09-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0269') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0386') AS parte_id,
        30009 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30009) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        40593 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40593) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0380') AS parte_id,
        40798 AS precio_id,
        0.5 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0234') AS parte_id,
        40602 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40602) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0244') AS parte_id,
        41026 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41026) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0075') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0323') AS parte_id,
        20002 AS precio_id,
        12.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0312') AS parte_id,
        40009 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40009) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        41065 AS precio_id,
        12.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41065) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0478') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0230') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0397') AS parte_id,
        30008 AS precio_id,
        4.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30008) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0139') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0395') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0281') AS parte_id,
        20002 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0438') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0482') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0421') AS parte_id,
        20004 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0411') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0394') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0133') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0274') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0330') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0321') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0079') AS parte_id,
        30012 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40798 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0236') AS parte_id,
        30002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40601 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40601) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0233') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0151') AS parte_id,
        20004 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0126') AS parte_id,
        41181 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41181) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0390') AS parte_id,
        30001 AS precio_id,
        1.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0381') AS parte_id,
        40645 AS precio_id,
        2.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40645) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0276') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0500') AS parte_id,
        41039 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41039) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        41182 AS precio_id,
        1.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41182) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        30001 AS precio_id,
        8.0 AS cantidad,
        '2025-09-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0219') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0470') AS parte_id,
        20004 AS precio_id,
        4.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0416') AS parte_id,
        40027 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40027) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0164') AS parte_id,
        40644 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40644) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0140') AS parte_id,
        20007 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0302') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-18' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0153') AS parte_id,
        40560 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40560) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0266') AS parte_id,
        40107 AS precio_id,
        1.0 AS cantidad,
        '2025-09-11' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40107) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0188') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0217') AS parte_id,
        40838 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40838) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0177') AS parte_id,
        30011 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0269') AS parte_id,
        40999 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40999) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0238') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0377') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0415') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0306') AS parte_id,
        20002 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0308') AS parte_id,
        20007 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0436') AS parte_id,
        40644 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40644) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0434') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        '2025-10-22' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0193') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0445') AS parte_id,
        40027 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40027) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0207') AS parte_id,
        20007 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0123') AS parte_id,
        30003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0105') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0117') AS parte_id,
        20007 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0439') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 24/28 (registros 2301-2400)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0387') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        '2025-10-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0406') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0280') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0197') AS parte_id,
        30003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0246') AS parte_id,
        41046 AS precio_id,
        2.0 AS cantidad,
        '2025-09-05' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41046) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0318') AS parte_id,
        40059 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0258') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0407') AS parte_id,
        40644 AS precio_id,
        1.0 AS cantidad,
        '2025-10-14' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40644) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0438') AS parte_id,
        40608 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40608) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0405') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        '2025-10-28' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-04' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0274') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0514') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0175') AS parte_id,
        30011 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0348') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        '2025-09-05' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        20004 AS precio_id,
        20.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0470') AS parte_id,
        20002 AS precio_id,
        11.0 AS cantidad,
        '2025-10-27' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0260') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0121') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0259') AS parte_id,
        20002 AS precio_id,
        6.0 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0318') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0276') AS parte_id,
        40059 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0183') AS parte_id,
        20002 AS precio_id,
        12.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        41016 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41016) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0124') AS parte_id,
        40709 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40709) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0309') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0349') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0515') AS parte_id,
        40027 AS precio_id,
        1.0 AS cantidad,
        '2025-11-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40027) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0183') AS parte_id,
        20003 AS precio_id,
        12.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0470') AS parte_id,
        40798 AS precio_id,
        2.0 AS cantidad,
        '2025-10-27' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0409') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0277') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0288') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0381') AS parte_id,
        30012 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0500') AS parte_id,
        40986 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40986) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0119') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        41077 AS precio_id,
        12.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41077) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0160') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0328') AS parte_id,
        40613 AS precio_id,
        2.0 AS cantidad,
        '2025-09-21' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40613) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0083') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0311') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40588 AS precio_id,
        20.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40588) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0304') AS parte_id,
        20002 AS precio_id,
        4.0 AS cantidad,
        '2025-10-16' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0321') AS parte_id,
        40644 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40644) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0041') AS parte_id,
        40831 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0123') AS parte_id,
        41048 AS precio_id,
        2.7 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41048) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0269') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0119') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0107') AS parte_id,
        30008 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30008) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0482') AS parte_id,
        40644 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40644) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0188') AS parte_id,
        30011 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0278') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0253') AS parte_id,
        30011 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0270') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0071') AS parte_id,
        20004 AS precio_id,
        11.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40615 AS precio_id,
        1.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40615) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0486') AS parte_id,
        40798 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0340') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0239') AS parte_id,
        40024 AS precio_id,
        1.0 AS cantidad,
        '2025-09-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40024) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0513') AS parte_id,
        20004 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0317') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0148') AS parte_id,
        20004 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0071') AS parte_id,
        30012 AS precio_id,
        20.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0242') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0273') AS parte_id,
        20002 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0462') AS parte_id,
        40108 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40108) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0217') AS parte_id,
        40016 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40016) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0055') AS parte_id,
        30011 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0181') AS parte_id,
        40590 AS precio_id,
        1.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0328') AS parte_id,
        20004 AS precio_id,
        6.0 AS cantidad,
        '2025-09-24' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0469') AS parte_id,
        40099 AS precio_id,
        1.0 AS cantidad,
        '2025-10-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40099) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0157') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0102') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0293') AS parte_id,
        40646 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40646) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0181') AS parte_id,
        20004 AS precio_id,
        32.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0171') AS parte_id,
        40717 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0204') AS parte_id,
        40646 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40646) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0347') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0468') AS parte_id,
        20004 AS precio_id,
        4.0 AS cantidad,
        '2025-10-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0253') AS parte_id,
        20003 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0462') AS parte_id,
        40831 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        40059 AS precio_id,
        5.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0269') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0336') AS parte_id,
        20003 AS precio_id,
        24.0 AS cantidad,
        '2025-09-23' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0278') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0240') AS parte_id,
        20005 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0128') AS parte_id,
        30003 AS precio_id,
        14.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0378') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0198') AS parte_id,
        40798 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0297') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0145') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0361') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0149') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0397') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0107') AS parte_id,
        20003 AS precio_id,
        13.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0160') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0154') AS parte_id,
        20004 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 25/28 (registros 2401-2500)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        40629 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40629) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0254') AS parte_id,
        20005 AS precio_id,
        8.0 AS cantidad,
        '2025-10-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0336') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        40831 AS precio_id,
        20.0 AS cantidad,
        '2025-09-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0510') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0325') AS parte_id,
        40014 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40014) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0450') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40838 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40838) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0123') AS parte_id,
        30012 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0142') AS parte_id,
        30003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0319') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0141') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0122') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0326') AS parte_id,
        20002 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0101') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0107') AS parte_id,
        30003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0147') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0048') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0218') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0085') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0091') AS parte_id,
        20006 AS precio_id,
        48.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20006) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0238') AS parte_id,
        40059 AS precio_id,
        0.5 AS cantidad,
        '2025-09-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0232') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0217') AS parte_id,
        40831 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0092') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0100') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0095') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0095') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0102') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0101') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0101') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0095') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0095') AS parte_id,
        20005 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0103') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0107') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0237') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0235') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0115') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        30003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0155') AS parte_id,
        40137 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40137) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0513') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0253') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0134') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0143') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0462') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0266') AS parte_id,
        40798 AS precio_id,
        2.0 AS cantidad,
        '2025-09-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0255') AS parte_id,
        20002 AS precio_id,
        16.0 AS cantidad,
        '2025-09-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0158') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0275') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0176') AS parte_id,
        40177 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40177) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0303') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0311') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0181') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0328') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-23' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0335') AS parte_id,
        20002 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        30003 AS precio_id,
        6.0 AS cantidad,
        '2025-09-24' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        '2025-09-24' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0194') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0195') AS parte_id,
        20002 AS precio_id,
        10.0 AS cantidad,
        '2025-09-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0212') AS parte_id,
        20005 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0153') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0101') AS parte_id,
        30011 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'GF/0003') AS parte_id,
        10001 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 10001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0216') AS parte_id,
        20006 AS precio_id,
        176.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20006) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0217') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0336') AS parte_id,
        20002 AS precio_id,
        12.0 AS cantidad,
        '2025-09-23' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0220') AS parte_id,
        20007 AS precio_id,
        8.0 AS cantidad,
        '2025-09-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        30001 AS precio_id,
        3.0 AS cantidad,
        '2025-09-24' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0226') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0116') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0368') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0369') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0370') AS parte_id,
        30011 AS precio_id,
        9.0 AS cantidad,
        '2025-10-16' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0371') AS parte_id,
        30003 AS precio_id,
        5.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0290') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        '2025-09-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0304') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0249') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0241') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40059 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40059) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0384') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0261') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0423') AS parte_id,
        20002 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0334') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        '2025-10-21' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0454') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0343') AS parte_id,
        20006 AS precio_id,
        144.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20006) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0459') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0434') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        '2025-10-21' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0462') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0467') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0468') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        '2025-10-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0471') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0395') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        '2025-10-21' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0458') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0473') AS parte_id,
        30011 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0364') AS parte_id,
        20002 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0492') AS parte_id,
        20003 AS precio_id,
        24.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0379') AS parte_id,
        20005 AS precio_id,
        8.0 AS cantidad,
        '2025-10-28' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0353') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        '2025-11-04' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 26/28 (registros 2501-2600)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        30003 AS precio_id,
        16.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0504') AS parte_id,
        30009 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30009) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0353') AS parte_id,
        30011 AS precio_id,
        5.0 AS cantidad,
        '2025-11-05' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0505') AS parte_id,
        30011 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0515') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-11-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0246') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0262') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0184') AS parte_id,
        30003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0336') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        40592 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40592) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0008') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0420') AS parte_id,
        40013 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40013) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0127') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0257') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0504') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0110') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0025') AS parte_id,
        20002 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        30006 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30006) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0379') AS parte_id,
        20004 AS precio_id,
        16.0 AS cantidad,
        '2025-10-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0513') AS parte_id,
        40644 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40644) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0248') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-02' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0446') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0439') AS parte_id,
        40798 AS precio_id,
        1.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0387') AS parte_id,
        30008 AS precio_id,
        2.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30008) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20004 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'GF/0005') AS parte_id,
        10001 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 10001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0476') AS parte_id,
        40479 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40479) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0381') AS parte_id,
        41047 AS precio_id,
        2.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41047) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40899 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40899) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0438') AS parte_id,
        40754 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40754) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0012') AS parte_id,
        40764 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40764) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0021') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0103') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0275') AS parte_id,
        20002 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0408') AS parte_id,
        30011 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0354') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        30002 AS precio_id,
        1.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0360') AS parte_id,
        40608 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40608) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0174') AS parte_id,
        40485 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40485) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0208') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0352') AS parte_id,
        40012 AS precio_id,
        1.0 AS cantidad,
        '2025-09-26' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-24' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0202') AS parte_id,
        20007 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0160') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0221') AS parte_id,
        30003 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0323') AS parte_id,
        30011 AS precio_id,
        12.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0230') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0234') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0284') AS parte_id,
        20002 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0439') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0309') AS parte_id,
        20002 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0469') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0145') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0440') AS parte_id,
        40012 AS precio_id,
        1.0 AS cantidad,
        '2025-10-21' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0104') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0512') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0171') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0015') AS parte_id,
        20002 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0218') AS parte_id,
        40027 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40027) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0129') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0186') AS parte_id,
        40717 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0477') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0316') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0387') AS parte_id,
        40874 AS precio_id,
        1.0 AS cantidad,
        '2025-10-06' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40874) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0412') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0226') AS parte_id,
        20005 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0287') AS parte_id,
        40590 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0053') AS parte_id,
        40831 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0469') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0403') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0071') AS parte_id,
        30011 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0499') AS parte_id,
        20003 AS precio_id,
        13.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0256') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0452') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0010') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0259') AS parte_id,
        40553 AS precio_id,
        1.0 AS cantidad,
        '2025-09-10' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40553) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0211') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0162') AS parte_id,
        40014 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40014) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0388') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0150') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0269') AS parte_id,
        40366 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40366) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0106') AS parte_id,
        20005 AS precio_id,
        7.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0022') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0335') AS parte_id,
        20007 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0476') AS parte_id,
        40692 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40692) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-09' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0359') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0402') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0443') AS parte_id,
        20002 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0251') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0397') AS parte_id,
        30003 AS precio_id,
        6.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0242') AS parte_id,
        40006 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40006) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0110') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0449') AS parte_id,
        41076 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41076) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0472') AS parte_id,
        20004 AS precio_id,
        10.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0303') AS parte_id,
        40014 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40014) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0039') AS parte_id,
        40553 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40553) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 27/28 (registros 2601-2700)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0111') AS parte_id,
        40709 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40709) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0269') AS parte_id,
        40755 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40755) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0336') AS parte_id,
        20002 AS precio_id,
        3.0 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        30003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0121') AS parte_id,
        40798 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0239') AS parte_id,
        20005 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0236') AS parte_id,
        40588 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40588) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0221') AS parte_id,
        40025 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40025) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0245') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0144') AS parte_id,
        30003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0264') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0126') AS parte_id,
        30009 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30009) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0292') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0281') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0296') AS parte_id,
        40010 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40010) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0382') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        '2025-10-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0351') AS parte_id,
        30003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0303') AS parte_id,
        40838 AS precio_id,
        1.0 AS cantidad,
        '2025-10-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40838) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0290') AS parte_id,
        40830 AS precio_id,
        5.0 AS cantidad,
        '2025-10-16' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40830) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0436') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0372') AS parte_id,
        30003 AS precio_id,
        6.0 AS cantidad,
        '2025-09-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0446') AS parte_id,
        40745 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40745) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0195') AS parte_id,
        20002 AS precio_id,
        10.0 AS cantidad,
        '2025-09-15' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-10-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0164') AS parte_id,
        20004 AS precio_id,
        12.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0269') AS parte_id,
        20002 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0004') AS parte_id,
        30012 AS precio_id,
        12.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0255') AS parte_id,
        20004 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0426') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0281') AS parte_id,
        40027 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40027) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0137') AS parte_id,
        20005 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-23' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0379') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-10-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0426') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0149') AS parte_id,
        41014 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41014) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0254') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0110') AS parte_id,
        30003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0396') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0128') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0183') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0252') AS parte_id,
        20004 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0402') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0290') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0163') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0456') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0493') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0176') AS parte_id,
        20002 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0470') AS parte_id,
        30008 AS precio_id,
        1.0 AS cantidad,
        '2025-10-27' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30008) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0466') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0134') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0385') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0273') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-09-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0248') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-04' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0383') AS parte_id,
        30001 AS precio_id,
        2.0 AS cantidad,
        '2025-10-07' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30001) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0321') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0313') AS parte_id,
        30011 AS precio_id,
        30.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0343') AS parte_id,
        30009 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30009) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0213') AS parte_id,
        41048 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41048) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0156') AS parte_id,
        20004 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0068') AS parte_id,
        20003 AS precio_id,
        12.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0136') AS parte_id,
        40552 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40552) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0332') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0105') AS parte_id,
        30003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0174') AS parte_id,
        30003 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0288') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0079') AS parte_id,
        30012 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30012) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        20004 AS precio_id,
        10.0 AS cantidad,
        '2025-09-23' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0141') AS parte_id,
        40590 AS precio_id,
        1.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0389') AS parte_id,
        40590 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0025') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0170') AS parte_id,
        20003 AS precio_id,
        1.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        40553 AS precio_id,
        4.0 AS cantidad,
        '2025-10-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40553) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0330') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-09-24' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0182') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0225') AS parte_id,
        40189 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40189) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0289') AS parte_id,
        30011 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0400') AS parte_id,
        40025 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40025) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-09-24' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0029') AS parte_id,
        40759 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40759) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0079') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0221') AS parte_id,
        20003 AS precio_id,
        9.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-09-05' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0287') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0167') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0042') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0240') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-09-03' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0002') AS parte_id,
        40344 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40344) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0338') AS parte_id,
        30009 AS precio_id,
        2.0 AS cantidad,
        '2025-09-24' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30009) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0244') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0481') AS parte_id,
        30011 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0305') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40708 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40708) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0367') AS parte_id,
        40617 AS precio_id,
        1.0 AS cantidad,
        '2025-09-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40617) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0200') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0263') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0476') AS parte_id,
        41181 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41181) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0158') AS parte_id,
        40643 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40643) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0095') AS parte_id,
        20005 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Lote 28/28 (registros 2701-2777)
INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, fecha, precio_unit)
SELECT * FROM (
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0372') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        '2025-09-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0468') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        '2025-10-30' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0200') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0199') AS parte_id,
        40798 AS precio_id,
        0.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0503') AS parte_id,
        40831 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0377') AS parte_id,
        40655 AS precio_id,
        2.0 AS cantidad,
        '2025-10-29' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40655) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0357') AS parte_id,
        20003 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0286') AS parte_id,
        20002 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0117') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0241') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0360') AS parte_id,
        40485 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40485) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0178') AS parte_id,
        20004 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0201') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0229') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0472') AS parte_id,
        40830 AS precio_id,
        3.0 AS cantidad,
        '2025-10-31' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40830) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0320') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        '2025-09-19' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0439') AS parte_id,
        40645 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40645) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0245') AS parte_id,
        40565 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40565) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0290') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0520') AS parte_id,
        20003 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        40798 AS precio_id,
        4.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0349') AS parte_id,
        20004 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0003') AS parte_id,
        30011 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0337') AS parte_id,
        30002 AS precio_id,
        1.0 AS cantidad,
        '2025-09-25' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0433') AS parte_id,
        20002 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0318') AS parte_id,
        20003 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0281') AS parte_id,
        40798 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0072') AS parte_id,
        20003 AS precio_id,
        8.5 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0023') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0024') AS parte_id,
        50008 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 50008) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0175') AS parte_id,
        20005 AS precio_id,
        10.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0065') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0316') AS parte_id,
        40831 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0136') AS parte_id,
        40717 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0152') AS parte_id,
        40743 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40743) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0265') AS parte_id,
        41172 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41172) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0210') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0103') AS parte_id,
        30008 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30008) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0249') AS parte_id,
        30011 AS precio_id,
        5.0 AS cantidad,
        '2025-09-01' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0128') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0495') AS parte_id,
        20004 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0303') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        '2025-10-17' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0504') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0397') AS parte_id,
        30008 AS precio_id,
        2.0 AS cantidad,
        '2025-10-10' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30008) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0185') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0098') AS parte_id,
        20005 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0398') AS parte_id,
        40366 AS precio_id,
        1.0 AS cantidad,
        '2025-10-08' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40366) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0038') AS parte_id,
        30011 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0179') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0122') AS parte_id,
        30003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0311') AS parte_id,
        20002 AS precio_id,
        16.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0163') AS parte_id,
        20003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0486') AS parte_id,
        41032 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 41032) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0339') AS parte_id,
        20002 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0417') AS parte_id,
        40027 AS precio_id,
        1.0 AS cantidad,
        '2025-10-15' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40027) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0097') AS parte_id,
        20007 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20007) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        20002 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0124') AS parte_id,
        40180 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40180) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0236') AS parte_id,
        40829 AS precio_id,
        20.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40829) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0185') AS parte_id,
        20003 AS precio_id,
        4.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0107') AS parte_id,
        40590 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40590) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0270') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0029') AS parte_id,
        40717 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0336') AS parte_id,
        20004 AS precio_id,
        24.0 AS cantidad,
        '2025-09-23' AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20004) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0297') AS parte_id,
        20005 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0115') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0095') AS parte_id,
        20005 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20005) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0231') AS parte_id,
        30011 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30011) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0030') AS parte_id,
        40717 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40717) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0018') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0329') AS parte_id,
        20003 AS precio_id,
        3.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0131') AS parte_id,
        20002 AS precio_id,
        6.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20002) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0480') AS parte_id,
        40798 AS precio_id,
        1.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40798) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0236') AS parte_id,
        30003 AS precio_id,
        5.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 30003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'TP/0028') AS parte_id,
        20003 AS precio_id,
        8.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0480') AS parte_id,
        40831 AS precio_id,
        7.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 40831) AS precio_unit
    UNION ALL
    SELECT
        (SELECT id FROM tbl_partes WHERE codigo = 'OT/0414') AS parte_id,
        20003 AS precio_id,
        2.0 AS cantidad,
        NULL AS fecha,
        (SELECT coste FROM tbl_pres_precios WHERE id = 20003) AS precio_unit
) AS temp
WHERE temp.parte_id IS NOT NULL AND temp.precio_unit IS NOT NULL;

-- Verificación: contar registros después de insertar
SELECT COUNT(*) AS 'Registros totales después de insertar' FROM tbl_part_presupuesto;

-- Verificación: mostrar primeros 10 registros insertados
SELECT
    pp.id,
    p.codigo AS parte_codigo,
    pr.codigo AS precio_codigo,
    pp.cantidad,
    pp.fecha,
    pp.precio_unit
FROM tbl_part_presupuesto pp
LEFT JOIN tbl_partes p ON pp.parte_id = p.id
LEFT JOIN tbl_pres_precios pr ON pp.precio_id = pr.id
ORDER BY pp.id DESC
LIMIT 10;

-- FIN DEL SCRIPT
