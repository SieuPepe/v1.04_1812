-- Script para corregir nombres de municipios de Gipuzkoa y Bizkaia
-- ====================================================================
-- Este script actualiza los nombres de los municipios que se insertaron
-- sin nombre debido a problemas con la estructura de la tabla

-- IMPORTANTE: Ejecutar primero verificar_municipios_gipuzkoa.sql para
-- confirmar que los municipios están sin nombre

-- 1. Actualizar nombres de municipios de Gipuzkoa
-- ================================================
UPDATE tbl_municipios SET NAMEUNIT = 'Abaltzisketa' WHERE CODIGOINE = 20001;
UPDATE tbl_municipios SET NAMEUNIT = 'Aduna' WHERE CODIGOINE = 20002;
UPDATE tbl_municipios SET NAMEUNIT = 'Aia' WHERE CODIGOINE = 20003;
UPDATE tbl_municipios SET NAMEUNIT = 'Aizarnazabal' WHERE CODIGOINE = 20004;
UPDATE tbl_municipios SET NAMEUNIT = 'Alegia' WHERE CODIGOINE = 20005;
UPDATE tbl_municipios SET NAMEUNIT = 'Alkiza' WHERE CODIGOINE = 20006;
UPDATE tbl_municipios SET NAMEUNIT = 'Altzaga' WHERE CODIGOINE = 20007;
UPDATE tbl_municipios SET NAMEUNIT = 'Altzo' WHERE CODIGOINE = 20008;
UPDATE tbl_municipios SET NAMEUNIT = 'Amezketa' WHERE CODIGOINE = 20009;
UPDATE tbl_municipios SET NAMEUNIT = 'Andoain' WHERE CODIGOINE = 20010;
UPDATE tbl_municipios SET NAMEUNIT = 'Anoeta' WHERE CODIGOINE = 20011;
UPDATE tbl_municipios SET NAMEUNIT = 'Antzuola' WHERE CODIGOINE = 20012;
UPDATE tbl_municipios SET NAMEUNIT = 'Arama' WHERE CODIGOINE = 20013;
UPDATE tbl_municipios SET NAMEUNIT = 'Aretxabaleta' WHERE CODIGOINE = 20014;
UPDATE tbl_municipios SET NAMEUNIT = 'Asteasu' WHERE CODIGOINE = 20015;
UPDATE tbl_municipios SET NAMEUNIT = 'Astigarraga' WHERE CODIGOINE = 20016;
UPDATE tbl_municipios SET NAMEUNIT = 'Ataun' WHERE CODIGOINE = 20017;
UPDATE tbl_municipios SET NAMEUNIT = 'Azkoitia' WHERE CODIGOINE = 20018;
UPDATE tbl_municipios SET NAMEUNIT = 'Azpeitia' WHERE CODIGOINE = 20019;
UPDATE tbl_municipios SET NAMEUNIT = 'Baliarrain' WHERE CODIGOINE = 20020;
UPDATE tbl_municipios SET NAMEUNIT = 'Beasain' WHERE CODIGOINE = 20021;
UPDATE tbl_municipios SET NAMEUNIT = 'Beizama' WHERE CODIGOINE = 20022;
UPDATE tbl_municipios SET NAMEUNIT = 'Belauntza' WHERE CODIGOINE = 20023;
UPDATE tbl_municipios SET NAMEUNIT = 'Berastegi' WHERE CODIGOINE = 20024;
UPDATE tbl_municipios SET NAMEUNIT = 'Bergara' WHERE CODIGOINE = 20025;
UPDATE tbl_municipios SET NAMEUNIT = 'Berrobi' WHERE CODIGOINE = 20026;
UPDATE tbl_municipios SET NAMEUNIT = 'Bidania-Goiatz' WHERE CODIGOINE = 20027;
UPDATE tbl_municipios SET NAMEUNIT = 'Deba' WHERE CODIGOINE = 20028;
UPDATE tbl_municipios SET NAMEUNIT = 'Donostia-San Sebastián' WHERE CODIGOINE = 20069;
UPDATE tbl_municipios SET NAMEUNIT = 'Eibar' WHERE CODIGOINE = 20030;
UPDATE tbl_municipios SET NAMEUNIT = 'Elduain' WHERE CODIGOINE = 20031;
UPDATE tbl_municipios SET NAMEUNIT = 'Elgeta' WHERE CODIGOINE = 20032;
UPDATE tbl_municipios SET NAMEUNIT = 'Elgoibar' WHERE CODIGOINE = 20033;
UPDATE tbl_municipios SET NAMEUNIT = 'Errenteria' WHERE CODIGOINE = 20034;
UPDATE tbl_municipios SET NAMEUNIT = 'Errezil' WHERE CODIGOINE = 20035;
UPDATE tbl_municipios SET NAMEUNIT = 'Eskoriatza' WHERE CODIGOINE = 20036;
UPDATE tbl_municipios SET NAMEUNIT = 'Ezkio-Itsaso' WHERE CODIGOINE = 20037;
UPDATE tbl_municipios SET NAMEUNIT = 'Gabiria' WHERE CODIGOINE = 20038;
UPDATE tbl_municipios SET NAMEUNIT = 'Gaintza' WHERE CODIGOINE = 20039;
UPDATE tbl_municipios SET NAMEUNIT = 'Gaztelu' WHERE CODIGOINE = 20040;
UPDATE tbl_municipios SET NAMEUNIT = 'Getaria' WHERE CODIGOINE = 20041;
UPDATE tbl_municipios SET NAMEUNIT = 'Hernani' WHERE CODIGOINE = 20042;
UPDATE tbl_municipios SET NAMEUNIT = 'Hernialde' WHERE CODIGOINE = 20043;
UPDATE tbl_municipios SET NAMEUNIT = 'Hondarribia' WHERE CODIGOINE = 20044;
UPDATE tbl_municipios SET NAMEUNIT = 'Ibarra' WHERE CODIGOINE = 20045;
UPDATE tbl_municipios SET NAMEUNIT = 'Idiazabal' WHERE CODIGOINE = 20046;
UPDATE tbl_municipios SET NAMEUNIT = 'Ikaztegieta' WHERE CODIGOINE = 20047;
UPDATE tbl_municipios SET NAMEUNIT = 'Irun' WHERE CODIGOINE = 20048;
UPDATE tbl_municipios SET NAMEUNIT = 'Irura' WHERE CODIGOINE = 20049;
UPDATE tbl_municipios SET NAMEUNIT = 'Itsasondo' WHERE CODIGOINE = 20050;
UPDATE tbl_municipios SET NAMEUNIT = 'Larraul' WHERE CODIGOINE = 20051;
UPDATE tbl_municipios SET NAMEUNIT = 'Lasarte-Oria' WHERE CODIGOINE = 20052;
UPDATE tbl_municipios SET NAMEUNIT = 'Lazkao' WHERE CODIGOINE = 20053;
UPDATE tbl_municipios SET NAMEUNIT = 'Leaburu' WHERE CODIGOINE = 20054;
UPDATE tbl_municipios SET NAMEUNIT = 'Legazpi' WHERE CODIGOINE = 20055;
UPDATE tbl_municipios SET NAMEUNIT = 'Legorreta' WHERE CODIGOINE = 20056;
UPDATE tbl_municipios SET NAMEUNIT = 'Leintz-Gatzaga' WHERE CODIGOINE = 20057;
UPDATE tbl_municipios SET NAMEUNIT = 'Lezo' WHERE CODIGOINE = 20058;
UPDATE tbl_municipios SET NAMEUNIT = 'Lizartza' WHERE CODIGOINE = 20059;
UPDATE tbl_municipios SET NAMEUNIT = 'Mendaro' WHERE CODIGOINE = 20060;
UPDATE tbl_municipios SET NAMEUNIT = 'Mutiloa' WHERE CODIGOINE = 20061;
UPDATE tbl_municipios SET NAMEUNIT = 'Mutriku' WHERE CODIGOINE = 20062;
UPDATE tbl_municipios SET NAMEUNIT = 'Oiartzun' WHERE CODIGOINE = 20063;
UPDATE tbl_municipios SET NAMEUNIT = 'Olaberria' WHERE CODIGOINE = 20064;
UPDATE tbl_municipios SET NAMEUNIT = 'Arrasate/Mondragón' WHERE CODIGOINE = 20065;
UPDATE tbl_municipios SET NAMEUNIT = 'Onati' WHERE CODIGOINE = 20066;
UPDATE tbl_municipios SET NAMEUNIT = 'Ordizia' WHERE CODIGOINE = 20067;
UPDATE tbl_municipios SET NAMEUNIT = 'Orendain' WHERE CODIGOINE = 20068;
UPDATE tbl_municipios SET NAMEUNIT = 'Orexa' WHERE CODIGOINE = 20070;
UPDATE tbl_municipios SET NAMEUNIT = 'Orio' WHERE CODIGOINE = 20071;
UPDATE tbl_municipios SET NAMEUNIT = 'Ormaiztegi' WHERE CODIGOINE = 20072;
UPDATE tbl_municipios SET NAMEUNIT = 'Pasaia' WHERE CODIGOINE = 20073;
UPDATE tbl_municipios SET NAMEUNIT = 'Segura' WHERE CODIGOINE = 20074;
UPDATE tbl_municipios SET NAMEUNIT = 'Soraluze-Placencia de las Armas' WHERE CODIGOINE = 20075;
UPDATE tbl_municipios SET NAMEUNIT = 'Tolosa' WHERE CODIGOINE = 20076;
UPDATE tbl_municipios SET NAMEUNIT = 'Urnieta' WHERE CODIGOINE = 20077;
UPDATE tbl_municipios SET NAMEUNIT = 'Urretxu' WHERE CODIGOINE = 20078;
UPDATE tbl_municipios SET NAMEUNIT = 'Usurbil' WHERE CODIGOINE = 20079;
UPDATE tbl_municipios SET NAMEUNIT = 'Villabona' WHERE CODIGOINE = 20080;
UPDATE tbl_municipios SET NAMEUNIT = 'Zaldibia' WHERE CODIGOINE = 20081;
UPDATE tbl_municipios SET NAMEUNIT = 'Zarautz' WHERE CODIGOINE = 20082;
UPDATE tbl_municipios SET NAMEUNIT = 'Zegama' WHERE CODIGOINE = 20083;
UPDATE tbl_municipios SET NAMEUNIT = 'Zerain' WHERE CODIGOINE = 20084;
UPDATE tbl_municipios SET NAMEUNIT = 'Zestoa' WHERE CODIGOINE = 20085;
UPDATE tbl_municipios SET NAMEUNIT = 'Zizurkil' WHERE CODIGOINE = 20086;
UPDATE tbl_municipios SET NAMEUNIT = 'Zumaia' WHERE CODIGOINE = 20087;
UPDATE tbl_municipios SET NAMEUNIT = 'Zumarraga' WHERE CODIGOINE = 20088;

-- 2. Verificación
-- ===============
SELECT 'Municipios actualizados de Gipuzkoa:' AS resultado;
SELECT COUNT(*) as total,
       SUM(CASE WHEN NAMEUNIT IS NOT NULL AND NAMEUNIT != '' THEN 1 ELSE 0 END) as con_nombre
FROM tbl_municipios
WHERE provincia_id = 3;

SELECT 'Muestra de municipios de Gipuzkoa:' AS resultado;
SELECT id, NAMEUNIT, CODIGOINE, comarca_id
FROM tbl_municipios
WHERE provincia_id = 3
ORDER BY NAMEUNIT
LIMIT 10;
