-- ============================================================================
-- Script de importación de datos para tbl_partes
-- Generado automáticamente desde: Para exportar.xlsx
-- Fecha de generación: 2025-11-11 22:58:44
-- Total de registros: 828
-- ============================================================================

-- Configuración inicial
SET FOREIGN_KEY_CHECKS = 0;
SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';
SET AUTOCOMMIT = 0;
START TRANSACTION;

-- Usar el schema correcto
USE cert_dev;

-- ============================================================================
-- AÑADIR CAMPOS ADICIONALES SI NO EXISTEN
-- ============================================================================

-- Procedimiento auxiliar para añadir columnas
DELIMITER //

DROP PROCEDURE IF EXISTS add_column_if_not_exists//
CREATE PROCEDURE add_column_if_not_exists(
    IN p_table_name VARCHAR(64),
    IN p_column_name VARCHAR(64),
    IN p_column_definition TEXT
)
BEGIN
    DECLARE column_count INT;

    SELECT COUNT(*) INTO column_count
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = p_table_name
    AND COLUMN_NAME = p_column_name;

    IF column_count = 0 THEN
        SET @sql = CONCAT('ALTER TABLE ', p_table_name,
                         ' ADD COLUMN ', p_column_name, ' ', p_column_definition);
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END IF;
END//

DELIMITER ;

-- Añadir campos que podrían no existir
CALL add_column_if_not_exists('tbl_partes', 'titulo', 'VARCHAR(255)');
CALL add_column_if_not_exists('tbl_partes', 'descripcion_larga', 'TEXT');
CALL add_column_if_not_exists('tbl_partes', 'descripcion_corta', 'VARCHAR(100)');
CALL add_column_if_not_exists('tbl_partes', 'id_estado', 'INT');
CALL add_column_if_not_exists('tbl_partes', 'finalizada', 'BOOLEAN DEFAULT 0');
CALL add_column_if_not_exists('tbl_partes', 'localizacion', 'VARCHAR(255)');
CALL add_column_if_not_exists('tbl_partes', 'id_municipio', 'INT');
CALL add_column_if_not_exists('tbl_partes', 'latitud', 'DECIMAL(10,8)');
CALL add_column_if_not_exists('tbl_partes', 'longitud', 'DECIMAL(11,8)');
CALL add_column_if_not_exists('tbl_partes', 'observaciones', 'TEXT');
CALL add_column_if_not_exists('tbl_partes', 'trabajadores', 'INT DEFAULT 0');
CALL add_column_if_not_exists('tbl_partes', 'estado', 'VARCHAR(50)');

-- Limpiar procedimiento
DROP PROCEDURE IF EXISTS add_column_if_not_exists;

-- ============================================================================
-- INSERCIÓN DE DATOS EN tbl_partes
-- ============================================================================

-- Registro 1/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0001', 5.0, 2, 1, 1, 3, 'Limpieza tamices en Lejarzo', 'Limpieza de las tamices de 7:00 a 12:00 en Lejarzo', '2025-08-01', '2025-08-01', 43.060111111111105, -3.12325, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Lejarzo', 3, 0, 1, 0);

-- Registro 2/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0092', 3.0, 1, 0, 1, 1, 'Abrir válvula en Erbi', 'Se ha abierto una válvula en Erbi de 14:50 - 15:25', '2025-08-01', '2025-08-01', 43.07491666666667, -3.1068611111111113, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Erbi', 1, 0, 1, 3);

-- Registro 3/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0093', 3.0, 1, 0, 1, 1, 'Revisión falta de presión en Amurrio', 'Se ha revisado la falta de presión, debido a un contador sucio', '2025-08-01', '2025-08-01', 43.05433333333333, -3.007138888888889, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 2);

-- Registro 4/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0096', 3.0, 1, 0, 1, 1, 'Aviso por contador fugando en Amurrio', 'Aviso por contador fugando', '2025-08-01', '2025-08-01', 43.05433333333333, -3.007416666666667, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 1);

-- Registro 5/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0003', 2.0, 2, 3, 1, 1, 'Limpieza fosa en Respaldiza', 'Limpieza fosa séptica en Respaldiza', '2025-08-01', '2025-08-01', 43.07777777777778, -3.0410277777777774, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Respaldiza', 1, 0, 1, 0);

-- Registro 6/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0004', 2.0, 2, 3, 1, 1, 'Limpieza fosa séptica en Menoio', 'Limpieza fosa séptica en Menoio', '2025-08-01', '2025-08-01', 43.07013888888889, -3.074638888888889, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Menoio', 1, 0, 1, 0);

-- Registro 7/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0005', 1.0, 2, 2, 3, 3, 'Limpieza captaciones', 'Limpieza captaciones', '2025-08-01', '2025-08-01', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 0, 1, 0);

-- Registro 8/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0094', 3.0, 1, 0, 1, 1, 'Fuga en Cacerías Artziniega', 'Fuga en Artziniega - Cacerías', '2025-08-01', '2025-08-01', 43.12269444444445, -3.1251944444444444, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 0, 1, 1);

-- Registro 9/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0006', 5.0, 2, 1, 1, 1, 'Limpieza fosa en Tamices Onsoño (Amurrio)', 'Limpieza de fosa séptica Tamices Onsoño', '2025-08-01', '2025-08-01', 43.0605, -2.942138888888889, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Onsoño-Amurrio', 1, 0, 1, 0);

-- Registro 10/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0095', 5.0, 1, 0, 5, 44, 'Desatasco colector saneamiento en Espejo', 'Desatascar en Espejo', '2025-08-01', '2025-08-01', 42.80891666666666, -3.0424166666666665, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Espejo', 44, 0, 1, 2);

-- Registro 11/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0002', 3.0, 2, 8, 3, 3, 'Contadores Polígonos los Fueros en Agurain', 'Alta de contadores en Polígono los fueros en Agurain', '2025-08-01', '2025-08-01', 42.849944444444446, -2.3926944444444445, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 0, 1, 0);

-- Registro 12/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0007', 3.0, 2, 8, 3, 3, 'Alta contador en Agurain', 'Instalación del contador - Alta contador en Agurain', '2025-08-01', '2025-08-01', 42.849944444444446, -2.3929722222222223, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 0, 1, 0);

-- Registro 13/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0097', 3.0, 1, 0, 5, 5, 'Fuga en Ribabellosa', 'Fuga en ribabellosa, visita montaña alavesa', '2025-08-01', '2025-08-01', 42.71027777777778, -2.9265833333333333, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa', 5, 0, 1, 1);

-- Registro 14/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0098', 3.0, 1, 0, 1, 1, 'Fuga en Larrinbe', 'Reparación de una fuga en Larrinbe', '2025-08-02', '2025-08-02', 43.04558333333333, -2.9768611111111114, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Larrinbe-Amurrio', 1, 0, 1, 1);

-- Registro 15/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0099', 3.0, 1, 0, 1, 1, 'Fuga en Larrinbe', 'Falso aviso de posible fuga en Larrinbe', '2025-08-02', '2025-08-02', 43.04408333333333, -2.9771388888888892, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Larrinbe-Amurrio', 1, 0, 1, 1);

-- Registro 16/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0100', 3.0, 1, 0, 1, 1, 'Aviso de fuga de acometida en Llodio', 'Aviso de fuga en acometida en edificios en construcción', '2025-08-03', '2025-08-03', 43.14025, -2.96075, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 17/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0101', 5.0, 1, 0, 5, 41, 'Atasco en Anucita', 'Atasco en Anucita en dos días 03/08-04/08', '2025-08-03', '2025-08-03', 42.80144444444444, -2.894361111111111, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Anucita', 41, 0, 1, 2);

-- Registro 18/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0102', 3.0, 1, 0, 3, 3, 'Búsqueda de fuga en Agurain', 'Búsqueda de fuga en Agurain', '2025-08-04', '2025-08-04', 42.85163888888889, -2.3946388888888888, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 0, 1, 1);

-- Registro 19/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0103', 1.0, 1, 0, 1, 1, 'Reparación fuga en Sojoguti', 'Reparación fuga en Sojoguti', '2025-08-04', '2025-08-04', 43.11186111111111, -3.12825, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Sojoguti/Artzeniaga', 1, 0, 1, 1);

-- Registro 20/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0104', 5.0, 1, 0, 5, 41, 'Desatasco en Anuncita', 'Desatasco', '2025-08-04', '2025-08-04', 42.80130555555555, -2.8951944444444444, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Anucita', 41, 0, 1, 2);

-- Registro 21/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0105', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Respaldiza', 'Reparación de una fuga en Respaldiza,esquina abajo desde el 04/08/2025 hasta el 13/08/2025', '2025-08-04', '2025-08-04', 43.087583333333335, -3.045472222222222, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Esquina Abajo/Respaldiza', 1, 0, 1, 1);

-- Registro 22/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0008', 5.0, 2, 1, 1, 1, 'Ejecución de arqueta en Amurrio', 'Ejecución de arqueta en Amurrio, en el barrio San Roque', '2025-08-01', '2025-08-01', 43.06894444444445, -2.99575, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Barrio San Roque', 1, 0, 1, 0);

-- Registro 23/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0106', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Larrinbe', 'Reparación de fuga en Larrinbe', '2025-08-04', '2025-08-04', 43.03783333333333, -2.9793611111111113, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Larrinbe-Amurrio', 1, 0, 1, 1);

-- Registro 24/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0009', 3.0, 2, 8, 3, 3, 'Instalación de contador - Alta contador en Argomaniz', 'Instalación de contador - Alta contador en Argomaniz', '2025-08-04', '2025-08-04', 42.867583333333336, -2.5463055555555556, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Argomaniz', 3, 0, 1, 0);

-- Registro 25/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0010', 3.0, 2, 10, 6, 6, 'Cambio de contador en Sabanto', 'Instalacion de contador, cambio de contador', '2025-08-04', '2025-08-04', 42.749138888888886, -2.41325, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Sabando', 6, 0, 1, 0);

-- Registro 26/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0011', 3.0, 2, 8, 1, 1, 'Alta contador en Amurrio', 'Alta del contador, instalación de contadores', '2025-08-04', '2025-08-04', 43.05330555555555, -3.0135277777777776, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 0);

-- Registro 27/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0012', 3.0, 2, 8, 1, 1, 'Instalación de contadores en Amurrio', 'Colocar contador en Caravanas - Barracas (Amurrio)', '2025-08-04', '2025-08-04', 43.049527777777776, -3.0138055555555554, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 0);

-- Registro 28/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0107', 3.0, 1, 0, 5, 5, 'Reparación de fuga Calle Iturbide en Ribabellosa', 'Localización, reparación de fuga. Creación de avisos. Asfaltado.', '2025-08-04', '2025-08-04', 42.711000000000006, -2.9307499999999997, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa', 5, 0, 1, 1);

-- Registro 29/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0108', 3.0, 1, 0, 5, 5, 'Búsqueda y reparación de fuga Calle Gazarriza en Ribabellosa', 'Búsqueda y reparación de fuga en Ribabellosa', '2025-08-05', '2025-08-05', 42.71038888888889, -2.9310277777777776, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa', 5, 0, 1, 1);

-- Registro 30/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0109', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Erbi', 'Reparación de fuga en Erbi', '2025-08-05', '2025-08-05', 43.07505555555556, -3.114638888888889, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Erbi', 1, 0, 1, 1);

-- Registro 31/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0013', 5.0, 2, 1, 6, 46, 'Búsqueda tubo de saneamiento en Maeztu', 'Se ha abierto una cata en busca del tubo de saneamiento', '2025-08-05', '2025-08-05', 42.739000000000004, -2.4482500000000003, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maeztu', 46, 0, 1, 0);

-- Registro 32/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0110', 3.0, 1, 0, 5, 5, 'Reparación de fuga en Puentelarra', 'Se ha tenido que picar bajo el armario del contador en busca de una fuga', '2025-08-05', '2025-08-05', 42.75083333333333, -3.0485277777777777, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Puentelarra', 5, 0, 1, 1);

-- Registro 33/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0111', 3.0, 1, 0, 1, 1, 'Revisión de la zona por aviso municipal en Llodio', 'Revisión de la zona por aviso municipal en Avenida Zumalacarregui', '2025-08-05', '2025-08-05', 43.14241666666667, -2.9654722222222225, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 3);

-- Registro 34/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0014', 3.0, 2, 10, 5, 5, 'Instalación contadores - Cambio de contador en Villanañe', 'Picar arqueta, cambio de contador y acerar arqueta.', '2025-08-05', '2025-08-05', 42.83627777777778, -3.082416666666667, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Villanañe', 5, 0, 1, 0);

-- Registro 35/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0015', 5.0, 2, 1, 1, 4, 'Asistencia a camión saneamiento en Llodio', 'Asistencia a camión de saneamiento', '2025-08-05', '2025-08-05', 43.135305555555554, -2.9826944444444448, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 4, 0, 1, 0);

-- Registro 36/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0016', 3.0, 2, 9, 1, 1, 'Baja de contador domiciliario en Llodio', 'Bajade contador domiciliario en Doctor Fleming 1, Llodio', '2025-08-05', '2025-08-05', 43.14461111111111, -2.9663055555555555, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 37/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0112', 3.0, 1, 0, 3, 3, 'Búsqueda y arreglo de fuga en Agurain', 'Búsqueda y arreglo de fuga en Agurain', '2025-08-05', '2025-08-05', 42.851, -2.3999166666666665, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 0, 1, 1);

-- Registro 38/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0113', 3.0, 1, 0, 1, 1, 'Localización de fuga en Bañoteibar en Amurrio', 'Localización de fuga en Amurrio', '2025-08-06', '2025-08-06', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 1);

-- Registro 39/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0114', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Amurrio', 'Reparación de fuga en Amurrio', '2025-08-06', '2025-08-06', 43.05013888888889, -3.000472222222222, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 1);

-- Registro 40/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0115', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Olabezar', 'Reparación de fuga en Olabezar', '2025-08-06', '2025-08-06', 43.068333333333335, -3.0174166666666666, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Olabezar', 1, 0, 1, 1);

-- Registro 41/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0116', 3.0, 1, 0, 1, 1, 'Búsqueda de fuga en Amurrio', 'Búsqueda de fuga en Amurrio', '2025-08-06', '2025-08-06', 43.05141666666666, -3.001027777777778, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 1);

-- Registro 42/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0117', 3.0, 1, 0, 1, 1, 'Excavación de fuga en Lekamaña', 'Excavación de fuga en Lekamaña', '2025-08-06', '2025-08-06', 43.02161111111111, -3.0013055555555557, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Lekamaña-Amurrio', 1, 0, 1, 1);

-- Registro 43/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0017', 3.0, 2, 12, 1, 1, 'Corte de agua en Llodio', 'Corte y reposición de servicio a fontanero particular', '2025-08-05', '2025-08-05', 43.152138888888885, -2.984916666666667, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 44/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0118', 5.0, 1, 0, 6, 46, 'Reparación fuga de saneamiento en Maeztu', 'Reparación fuga de saneamiento en Maeztu', '2025-08-05', '2025-08-05', 42.73927777777778, -2.4518611111111115, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maeztu', 46, 0, 1, 1);

-- Registro 45/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0119', 3.0, 1, 0, 3, 3, 'Reparación de fuga en Opakua', 'Reparación de fuga en Opakua', '2025-08-05', '2025-08-05', 42.82752777777778, -2.368805555555556, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Opacua', 3, 0, 1, 1);

-- Registro 46/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0120', 3.0, 1, 0, 5, 5, 'Reparación de fuga en Villanañe', 'Reparación de fuga en Villañane', '2025-08-05', '2025-08-05', 42.83641666666667, -3.08575, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Villanañe', 5, 0, 1, 1);

-- Registro 47/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0121', 3.0, 1, 0, 5, 5, 'Reparación de fuga en Puentelarra', 'Reparación de fuga en Puentelarra', '2025-08-06', '2025-08-06', 42.75127777777778, -3.052694444444444, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Puentelarra', 5, 0, 1, 1);

-- Registro 48/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0122', 5.0, 1, 0, 1, 3, 'Atasco en tubería en Zuaza', 'Atasco en tubería en Zuaza', '2025-08-06', '2025-08-06', 43.099805555555555, -3.052972222222222, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Zuaza', 3, 0, 1, 2);

-- Registro 49/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0123', 3.0, 1, 0, 3, 3, 'Fuga de agua en Opakua', 'Fuga de agua en Opakua', '2025-08-06', '2025-08-06', 42.82766666666667, -2.3699166666666667, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Opacua', 3, 0, 1, 1);

-- Registro 50/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0124', 3.0, 1, 0, 1, 1, 'Reparación fuga en Bañoteibar en Amurrio', 'Reparación de fuga en Amurrio', '2025-08-14', '2025-09-05', 43.05416, -2.99752, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 1);

-- Registro 51/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0125', 3.0, 1, 0, 1, 1, 'Aviso falta de suministro en Luiando', 'Aviso falta de suministro en Barrena Kalea en Luiando', '2025-08-06', '2025-08-06', 43.10516666666667, -2.9966944444444445, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Luiando', 1, 0, 1, 1);

-- Registro 52/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0126', 3.0, 1, 0, 1, 1, 'Vertido calle Landaluze (Llodio)', 'Vertido en calle Landaluze', '2025-08-08', '2025-08-08', 43.14063888888889, -2.9803055555555558, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 53/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0127', 3.0, 1, 0, 6, 6, 'Excavación y colocación de anillo de arqueta en Maeztu', 'Excavación y colocación de anillo de arqueta en Maeztu', '2025-08-07', '2025-08-07', 42.73986111111111, -2.4472500000000004, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maeztu', 6, 0, 1, 3);

-- Registro 54/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0128', 3.0, 1, 0, 1, 1, 'Reparación fuga en Lekamaña', 'Reparación fuga: Búsqueda de fuga, descubrirla, repararla, tapar caata y fuga.', '2025-08-07', '2025-08-07', 43.02163888888889, -2.997527777777778, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Lekamaña', 1, 0, 1, 1);

-- Registro 55/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0129', 3.0, 1, 0, 1, 1, 'Localización de fuga en Delika', 'Localización de fuga en tubería de abastecimiento a depósito', '2025-08-07', '2025-08-07', 42.96988888888889, -2.997805555555556, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Delika', 1, 0, 1, 1);

-- Registro 56/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0130', 3.0, 1, 0, 5, 5, 'Localización de fuga en Zambrana', 'Localización de fuga por aviso de fuga', '2025-08-07', '2025-08-07', 42.662388888888884, -2.8814166666666665, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Zambrana', 5, 0, 1, 1);

-- Registro 57/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0138', 3.0, 1, 0, 5, 5, 'Incidencia en Ribabellosa', 'Incidencia en Ribabellosa', '2025-08-07', '2025-08-07', 42.70991666666667, -2.931694444444444, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa', 5, 0, 1, 3);

-- Registro 58/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0131', 5.0, 1, 0, 1, 3, 'Atasco en Calle Padura (Luiando)', 'Atasco en Calle Padura', '2025-08-07', '2025-08-07', 43.093111111111114, -3.0153055555555555, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Luiando', 3, 0, 1, 2);

-- Registro 59/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0132', 3.0, 1, 0, 1, 1, 'Reparación de fuga y corte de agua', 'Corte de agua en Mendiko Kalea', '2025-08-07', '2025-08-07', 43.05933333333333, -3.0155833333333333, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 1);

-- Registro 60/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0133', 3.0, 1, 0, 1, 1, 'Fuga en Barretaguren, Artziniega', 'Fuga en Barretaguren, Artziniega', '2025-08-07', '2025-08-07', 43.126444444444445, -3.132527777777778, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 0, 1, 1);

-- Registro 61/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0134', 5.0, 1, 0, 6, 46, 'Saneamiento ayuda a camión en Maeztu', 'Saneamiento Maeztu', '2025-08-07', '2025-08-07', 42.73863888888889, -2.4494722222222225, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maeztu', 46, 0, 1, 3);

-- Registro 62/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0135', 3.0, 1, 0, 3, 3, 'Revisión y análisis de trabajos pendientes en Agurain y Alegría', 'Revisión y análisis de trabajos pendientes', '2025-08-07', '2025-08-07', 42.847972222222225, -2.39975, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain y Alegría', 3, 0, 1, 3);

-- Registro 63/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0136', 3.0, 1, 0, 1, 1, 'Aviso usuario en agua en Luiando', 'Aviso usuario', '2025-08-07', '2025-08-07', 43.09986111111111, -3.000027777777778, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Luiando', 1, 0, 1, 1);

-- Registro 64/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0137', 3.0, 1, 0, 1, 1, 'Fuga de agua en Santa Coloma Artzeniaga', 'Fuga de agua en Santa Coloma, Artziniega', '2025-08-07', '2025-08-07', 43.13847222222222, -3.1669722222222223, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 0, 1, 1);

-- Registro 65/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0018', 1.0, 2, 2, 1, 1, 'Limpieza de captaciones', 'Limpieza de captaciones en Aiaraldea', '2025-08-08', '2025-08-08', 43.13472222222222, -2.983916666666667, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'AIARALDEA', 1, 0, 1, 0);

-- Registro 66/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0019', 2.0, 2, 3, 1, 1, 'Mantenimiento fosas sépticas en Oceca', 'Mantenimiento fosas sépticas: Limpieza, vaciado y desbrozado de acceso de fosas', '2025-08-08', '2025-08-08', 43.07127777777778, -3.100861111111111, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ozeka', 1, 0, 1, 0);

-- Registro 67/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0020', 2.0, 2, 3, 1, 1, 'Mantenimiento fosas sépticas en Llanteno', 'Mantenimiento fosas sépticas: Limpieza, vaciado y desbrozado de acceso de fosas', '2025-08-08', '2025-08-08', 43.084138888888894, -3.1178055555555555, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llanteno-Ayala', 1, 0, 1, 0);

-- Registro 68/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0139', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Santa Coloma Atzeniaga', 'Fuga en Santa Coloma, reparación de fuga', '2025-08-08', '2025-08-08', 43.13825, -3.168083333333333, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 0, 1, 1);

-- Registro 69/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0140', 3.0, 1, 0, 5, 5, 'Aviso de fuga en Ribabellosa', 'Aviso de urgencia con fuga estrangular', '2025-08-08', '2025-08-08', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa', 5, 0, 1, 1);

-- Registro 70/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0141', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Artzeniaga', 'Reparación de fuga en Torre Barretaguren en Artziniega', '2025-08-09', '2025-08-09', 43.13291666666667, -3.118638888888889, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 0, 1, 1);

-- Registro 71/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0142', 1.0, 1, 0, 1, 1, 'Tapado de catas en Delika', 'Tapado de catas en Delika', '2025-08-09', '2025-08-09', 42.97027777777778, -3.00225, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Delika', 1, 0, 1, 3);

-- Registro 72/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0143', 5.0, 1, 0, 1, 1, 'Desatasco en Calle Aiara en Amurrio', 'Desatasco en Calle Aiara, Amurrio', '2025-08-09', '2025-08-09', 43.05594444444444, -3.0191944444444445, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 2);

-- Registro 73/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0144', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Respaldiza', 'Reparación de fuga en Respaldiza', '2025-08-09', '2025-08-09', 43.07658333333334, -3.0528055555555556, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Respaldiza', 1, 0, 1, 1);

-- Registro 74/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0145', 3.0, 1, 0, 1, 1, 'Reparación de fuga  en Artzeniaga', 'Reparación de fuga en Artzeniaga', '2025-08-10', '2025-08-10', 43.1225, -3.136416666666667, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 0, 1, 1);

-- Registro 75/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0146', 5.0, 1, 0, 1, 3, 'Desatasco Bikandi, Respaldiza', 'Desatasco Bikandi, Respaldiza', '2025-08-10', '2025-08-10', 43.07822222222222, -3.053361111111111, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Respaldiza', 3, 0, 1, 2);

-- Registro 76/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0147', 3.0, 1, 0, 1, 1, 'Búqueda de fuga en Okendo Llodio', 'Búqueda de fuga con el geófono en Okendo, Llodio', '2025-08-11', '2025-08-11', 43.155722222222224, -3.036972222222222, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 77/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0148', 3.0, 1, 0, 3, 3, 'Revisión contador por aviso en Alegria/Dulantzi', 'Aviso de poca presion. Se revisa un contador.', '2025-08-11', '2025-08-11', 42.84188888888889, -2.520583333333333, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 3, 0, 1, 3);

-- Registro 78/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0149', 3.0, 1, 0, 5, 5, 'Búsqueda y reparación de fuga en Zambrana', 'Búsqueda y reparación de fuga', '2025-08-11', '2025-08-11', 42.661055555555556, -2.8875277777777777, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Zambrana', 5, 0, 1, 1);

-- Registro 79/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0021', 2.0, 2, 3, 5, 5, 'Búsqueda y desbroce de fosa séptica en Portilla', 'Búsqueda y desbroce de fosa séptica', '2025-08-11', '2025-08-11', 42.67252777777777, -2.8544722222222223, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Portilla', 5, 0, 1, 0);

-- Registro 80/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0150', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Respaldiza', 'Reparación de fuga en Respaldiza', '2025-08-11', '2025-08-11', 43.07658333333334, -3.05475, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Respaldiza', 1, 0, 1, 1);

-- Registro 81/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0022', 5.0, 2, 1, 1, 3, 'Mantenimiento preventivo de saneamiento Mendico en Amurrio', 'Mantenimiento preventivo de saneamiento en Mendiko, Amurrio', '2025-08-11', '2025-08-11', 43.05933333333333, -3.0216944444444445, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Mendiko, Amurrio', 3, 0, 1, 0);

-- Registro 82/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0151', 3.0, 1, 0, 5, 5, 'Búsqueda de fuga en Espejo', 'Búsqueda de fuga', '2025-08-11', '2025-08-11', 42.80994444444444, -3.0553055555555555, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Espejo', 5, 0, 1, 1);

-- Registro 83/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0152', 3.0, 1, 0, 5, 5, 'Excavación de tubería, trabajos de zanjeo y reinstalación de la tubería en Barrio', 'Se descubre la tubería, se zanja para bajar de profundidad y se vuelve a tapar.', '2025-08-11', '2025-08-11', 42.809305555555554, -3.1055833333333336, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Barrio', 5, 0, 1, 1);

-- Registro 84/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0153', 3.0, 1, 0, 1, 1, 'Realizar nueva arqueta en San Roque (Amurrio)', 'Llevar el material, excavación para realizar la arqueta y taparla.', '2025-08-12', '2025-08-12', 43.06866666666667, -3.0058611111111113, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 3);

-- Registro 85/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0154', 3.0, 1, 0, 1, 1, 'Reparación de fuente en Respaldiza', 'Reparación de fuente', '2025-08-12', '2025-08-12', 43.07766666666667, -3.056138888888889, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Respaldiza', 1, 0, 1, 1);

-- Registro 86/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0155', 3.0, 1, 0, 5, 5, 'Tapado catas varias en Ribabellosa y Zambrana', 'Hormigonar, retirar y tirar escombro', '2025-08-12', '2025-08-12', 42.71088888888889, -2.9397499999999996, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa y Zambrana', 5, 0, 1, 3);

-- Registro 87/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0023', 5.0, 2, 1, 1, 3, 'Mantenimiento preventivo saneamiento en Luiando', 'Mantenimiento preventivo saneamiento, limpiea de saneamiento', '2025-08-12', '2025-08-12', 43.09875, -3.0066944444444443, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Luiando', 3, 0, 1, 0);

-- Registro 88/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0156', 3.0, 1, 0, 1, 1, 'Tapado de catas en Delika', 'Tapado de catas', '2025-08-12', '2025-08-12', 42.968611111111116, -3.006972222222222, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Delika', 1, 0, 1, 3);

-- Registro 89/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0157', 3.0, 1, 0, 5, 5, 'Reparación de fuga en Zambrana', 'Reparación de fuga', '2025-08-12', '2025-08-12', 42.66458333333333, -2.8905833333333333, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Zambrana', 5, 0, 1, 1);

-- Registro 90/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0158', 3.0, 1, 0, 5, 5, 'Tapado de tubería en Barrio', 'Tapado de tubería', '2025-08-12', '2025-08-12', 42.8095, -3.107527777777778, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Barrio', 5, 0, 1, 3);

-- Registro 91/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0159', 1.0, 1, 0, 5, 5, 'Aviso por fuga en Espejo', 'Aviso por fuga', '2025-08-12', '2025-08-12', 42.80997222222222, -3.0578055555555554, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Espejo', 5, 0, 1, 1);

-- Registro 92/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0160', 3.0, 1, 0, 4, 4, 'Sacar aires en Elosu', 'Sacar aires', '2025-08-12', '2025-08-12', 42.97602777777778, -2.6914166666666666, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Elosu', 4, 0, 1, 3);

-- Registro 93/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0161', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Atzeniaga', 'Reparación de fuga en San Antonio Auzoa', '2025-08-12', '2025-08-12', 43.11672222222222, -3.158361111111111, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 0, 1, 1);

-- Registro 94/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0162', 3.0, 1, 0, 3, 3, 'Reparación de fuga en Alegría/Dulantzi', 'Reparación de fuga', '2025-08-13', '2025-08-13', 42.842194444444445, -2.5253055555555557, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 3, 0, 1, 1);

-- Registro 95/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0024', 3.0, 2, 8, 1, 1, 'Alta contador en Kartuja-Ibarra', 'Alta contador - Alta contador', '2025-08-12', '2025-08-12', 43.13341666666667, -2.9922500000000003, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Katuja-Ibarra, Llodio', 1, 0, 1, 0);

-- Registro 96/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0025', 3.0, 2, 18, 1, 1, 'Conexión de acometida de agua potable Kartuja-Ibarra', 'Conexión de acometida de agua potable a barraqueros', '2025-08-12', '2025-08-12', 43.13341666666667, -2.9925277777777777, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Katuja-Ibarra, Llodio', 1, 0, 1, 0);

-- Registro 97/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0026', 3.0, 2, 8, 1, 1, 'Alta contador de fiestas de Herriko Plaza en Llodio', 'Alta contador de fiestas de Llodio', '2025-08-13', '2025-08-13', 43.14297222222222, -2.976138888888889, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Herriko Palaza, Llodio', 1, 0, 1, 0);

-- Registro 98/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0027', 5.0, 2, 1, 1, 1, 'Limpieza mantenimiento saneamiento Amurrio', 'Limpieza mantenimiento saneamiento en el barrio San Jose, Amurrio', '2025-08-13', '2025-08-13', 43.059888888888885, -3.00975, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 0);

-- Registro 99/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0028', 1.0, 2, 2, 1, 1, 'Limpieza captaciones Katxabazo e Intxutaspe', 'Limpieza captaciones Katxabazo e Intxutaspe', '2025-08-13', '2025-08-13', 43.04602777777777, -2.9100277777777777, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Katxabazo e Intxutaspe-Baranbio', 1, 0, 1, 0);

-- Registro 100/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0163', 3.0, 1, 0, 1, 1, 'Tapado de cata y reparación de la puerta de cierre en Delika (Amurrio)', 'Tapado de cata y reparación de la puerta de cierre', '2025-08-06', '2025-08-06', 42.97013888888889, -3.0103055555555556, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Delika', 1, 0, 1, 3);

-- Registro 101/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0164', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Delika (Amurrio)', 'Búsqueda y reparación de fuga. Hormigonado.', '2025-08-07', '2025-08-07', 42.97013888888889, -3.0105833333333334, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Delika', 1, 0, 1, 1);

-- Registro 102/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0165', 3.0, 1, 0, 1, 1, 'Cierre de llave Delika (Amurrio)', 'Cierre de llave', '2025-08-08', '2025-08-08', 42.97013888888889, -3.010861111111111, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Delika', 1, 0, 1, 3);

-- Registro 103/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0166', 3.0, 1, 0, 1, 1, 'Búsqueda y reparación de fuga en Artzeniaga', 'Búsqueda y reparación de fuga', '2025-08-08', '2025-08-08', 43.122083333333336, -3.1444722222222223, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 0, 1, 1);

-- Registro 104/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0167', 3.0, 1, 0, 3, 3, 'Búsqueda de arquetas en Agurain/Salvatierra', 'Búsqueda de arquetas en el Polígono fFueros, 2, Agurain', '2025-08-12', '2025-08-12', 42.84991666666667, -2.4114166666666668, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 0, 1, 3);

-- Registro 105/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0029', 3.0, 2, 8, 1, 1, 'Alta contador en Amurrio', 'Instalación contadores, alta contador', '2025-08-06', '2025-08-06', 43.05244444444444, -3.0283611111111113, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 0);

-- Registro 106/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0030', 3.0, 2, 8, 1, 1, 'Alta contador en Amurrio', 'Instalación contadores, alta contador', '2025-08-07', '2025-08-07', 43.05013888888889, -3.028638888888889, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 0);

-- Registro 107/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0031', 3.0, 2, 9, 1, 1, 'Baja contador en Amurrio', 'Desinstalación contadores, baja contador', '2025-08-08', '2025-08-08', 43.04841666666667, -3.0289166666666665, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 0);

-- Registro 108/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0032', 3.0, 2, 9, 1, 1, 'Baja contador en Llodio', 'Desinstalación contadores, baja contador', '2025-08-11', '2025-08-11', 43.14308333333333, -2.9791944444444445, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 109/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0033', 3.0, 2, 8, 1, 1, 'Alta contadores Llodio', 'Instalación contadores, alta contador', '2025-08-11', '2025-08-11', 43.14391666666667, -2.9794722222222223, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 110/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0034', 3.0, 2, 10, 1, 1, 'Cambio de contador en Amurrio', 'Sustitución contadores, cambio de contador', '2025-08-12', '2025-08-12', 43.056555555555555, -3.02975, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 0);

-- Registro 111/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0035', 3.0, 2, 10, 3, 3, 'Cambio de contador en Agurain', 'Sustitución contadores, cambio de contador', '2025-08-12', '2025-08-12', 42.85347222222222, -2.413361111111111, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 0, 1, 0);

-- Registro 112/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0036', 3.0, 2, 10, 5, 5, 'Cambio de contador en Rivabellosa', 'Sustitución contadores, cambio de contador', '2025-08-12', '2025-08-12', 42.71002777777778, -2.946972222222222, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa-Rivera Alta', 5, 0, 1, 0);

-- Registro 113/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0168', 3.0, 1, 0, 1, 1, 'Fuga Añes alta', 'Fuga Añes alta', '2025-08-14', '2025-08-14', 43.058, -3.14725, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Añes-Ayala', 1, 0, 1, 1);

-- Registro 114/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0169', 5.0, 1, 0, 1, 3, 'Limpieza de saneamiento con camión en Esquina Abajo/Respaldiza', 'Limpieza de saneamiento con camión', '2025-08-14', '2025-08-14', 43.08763888888889, -3.0641944444444444, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Esquina Abajo/Respaldiza', 3, 0, 1, 3);

-- Registro 115/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0037', 1.0, 2, 2, 1, 1, 'Limpieza captaciones Aiaraldea', 'Limpieza captaciones Aiaraldea', '2025-08-14', '2025-08-14', 43.13472222222222, -2.997805555555556, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'AIARA', 1, 0, 1, 0);

-- Registro 116/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0038', 5.0, 2, 1, 1, 4, 'Mantenimiento de saneamiento con camión en Llodio', 'Mantenimiento de saneamiento con camión', '2025-08-14', '2025-08-14', 43.14147222222222, -2.981416666666667, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 4, 0, 1, 0);

-- Registro 117/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0170', 3.0, 1, 0, 1, 1, 'Preparación de fuga en Artziniaga', 'Preparación de fuga en el campo de fútbol de Artziniega', '2025-08-14', '2025-08-14', 43.117555555555555, -3.148361111111111, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 0, 1, 1);

-- Registro 118/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0171', 3.0, 1, 0, 3, 3, 'Instalación de acometida opakua en Agurain/Salvatierra', 'Instalación de acometida opakua', '2025-08-14', '2025-08-14', 42.84963888888889, -2.4153055555555554, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Opacua', 3, 0, 1, 3);

-- Registro 119/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0172', 1.0, 1, 0, 1, 1, 'Búsqueda de fuga Añes', 'Búsqueda de fuga', '2025-08-13', '2025-08-13', 43.05855555555555, -3.1489166666666666, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Añes', 1, 0, 1, 1);

-- Registro 120/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0039', 3.0, 2, 10, 5, 5, 'Sustitución contador Urbina Eza', 'Sustitución contador', '2025-08-13', '2025-08-13', 42.87788888888889, -2.915861111111111, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Urbina Eza-Kuartango', 5, 0, 1, 0);

-- Registro 121/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0040', 3.0, 2, 10, 4, 4, 'Sustitución contador en Landa', 'Búsqueda arqueta del contador y sustitución contador', '2025-08-13', '2025-08-13', 42.960055555555556, -2.616138888888889, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Landa', 4, 0, 1, 0);

-- Registro 122/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0041', 3.0, 2, 10, 3, 3, 'Sustitución contadores en Fueros, Agurain', 'Búsqueda de contador. Picar arqueta, cambiar contador y hacer arqueta.', '2025-08-13', '2025-08-13', 42.84986111111111, -2.4164166666666667, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Fueros, Agurain', 3, 0, 1, 0);

-- Registro 123/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0042', 3.0, 2, 10, 6, 6, 'Sustitución contador en Sabando', 'Sustitución contador', '2025-08-13', '2025-08-13', 42.74922222222222, -2.433361111111111, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Sabando', 6, 0, 1, 0);

-- Registro 124/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0043', 3.0, 2, 10, 6, 6, 'Sustitución contador en Antoñana', 'Sustitución contador', '2025-08-13', '2025-08-13', 42.69325, -2.4169722222222223, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Antoñana', 6, 0, 1, 0);

-- Registro 125/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0044', 3.0, 2, 10, 9, 9, 'Sustitución contador en Oreitia', 'Sustitución contador', '2025-08-13', '2025-08-13', 42.85702777777778, -2.5839166666666666, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Oreitia', 9, 0, 1, 0);

-- Registro 126/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0045', 5.0, 2, 1, 1, 2, 'Mantenimiento preventivo de saneamiento en Artzeniaga', 'Mantenimiento preventivo de saneamiento', '2025-08-13', '2025-08-13', 43.12136111111111, -3.1508611111111113, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 2, 0, 1, 0);

-- Registro 127/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0173', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Larraño( Llodio)', 'Reparación de fuga en Larraño, Llodio', '2025-08-14', '2025-08-14', 43.14769444444445, -3.001138888888889, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 128/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0174', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Llodio', 'Reparación de fuga. Acometida.', '2025-08-14', '2025-08-14', 43.14383333333333, -2.98475, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 129/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0046', 5.0, 2, 1, 1, 2, 'Limpieza de mantenimiento preventivo saneamiento en Artzeniaga', 'Limpieza de mantenimiento preventivo saneamiento', '2025-08-14', '2025-08-14', 43.12275, -3.1516944444444444, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 2, 0, 1, 0);

-- Registro 130/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0175', 3.0, 1, 0, 5, 5, 'Reparacion de fuga por aviso en Jokano', 'Reparacion de fuga por aviso', '2025-08-14', '2025-08-14', 42.87188888888889, -2.951972222222222, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Jokano', 5, 0, 1, 1);

-- Registro 131/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0047', 3.0, 2, 14, 4, 4, 'Maniobras de válvulas en Landa', 'Maniobras de válvulas', '2025-08-14', '2025-08-14', 42.958194444444445, -2.618916666666667, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Landa', 4, 0, 1, 0);

-- Registro 132/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0048', 3.0, 2, 14, 4, 4, 'Sustitución y limpieza de ventosas en Elosu', 'Sustitución y limpieza de ventosas en Elosu', '2025-08-14', '2025-08-14', 42.976083333333335, -2.7025277777777776, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Elosu', 4, 0, 1, 0);

-- Registro 133/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0176', 3.0, 1, 0, 1, 1, 'Inspección de tuberías con cámara en Colegio La Milagrosa (Llodio)', 'Inspección de tuberías con cámara', '2025-08-14', '2025-08-14', 43.147194444444445, -3.0028055555555557, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 3);

-- Registro 134/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0049', 5.0, 2, 1, 1, 1, 'Mantenimiento preventivo de saneamiento de las fosas de Tamices en Onsoño', 'Mantenimiento preventivo de saneamiento de las fosas de Tamices', '2025-08-14', '2025-08-14', 43.0605, -2.9697500000000003, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Onsoño-Amurrio', 1, 0, 1, 0);

-- Registro 135/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0177', 5.0, 1, 0, 1, 1, 'Atasco en Amurrio', 'Atasco en Amurrio', '2025-08-15', '2025-08-15', 43.05294444444444, -3.0366944444444446, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 2);

-- Registro 136/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0178', 3.0, 1, 0, 1, 1, 'Fuga de agua en Sojoguti (Concejo municipio Artzeniaga)', 'Fuga de agua en Sojoguti', '2025-08-15', '2025-08-15', 43.11227777777778, -3.153638888888889, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Sojoguti/Artzeniaga', 1, 0, 1, 1);

-- Registro 137/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0179', 5.0, 1, 0, 1, 1, 'Atasco de saneamiento en Amurrio', 'Atasco de saneamiento', '2025-08-15', '2025-08-15', 43.05283333333333, -3.03725, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 2);

-- Registro 138/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0180', 3.0, 1, 0, 1, 1, 'Reparación de fuga en acometida  en Retes de Llanteno', 'Reparación de fuga en acometida. Hormigonado y asfaltado.', '2025-08-15', '2025-08-15', 43.09144444444445, -3.1375277777777777, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Retes de Llanteno', 1, 0, 1, 1);

-- Registro 139/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0181', 3.0, 1, 0, 1, 1, 'Reparación avería en Llodio', 'Picado y reparación de reventón. Preparación para hormigonado. Desescombrar. Hormigonado y recorte de baldosa. Embaldosado.', '2025-08-16', '2025-08-16', 43.14227777777778, -2.9878055555555556, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 3);

-- Registro 140/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0182', 3.0, 1, 0, 1, 1, 'Fuga de agua en Berganza', 'Fuga de agua en Berganza', '2025-08-16', '2025-08-16', 43.12130555555556, -3.15475, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Berganza-Baranbio', 1, 0, 1, 1);

-- Registro 141/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0183', 5.0, 1, 0, 1, 4, 'Atasco en Landaluce, Llodio', 'Atasco en Landaluce, Llodio', '2025-08-16', '2025-08-16', 43.14047222222222, -3.005027777777778, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 4, 0, 1, 2);

-- Registro 142/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0184', 3.0, 1, 0, 1, 1, 'Fuga de agua en Erbi', 'Fuga de agua en Erbi', '2025-08-17', '2025-08-17', 43.07505555555556, -3.138638888888889, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Erbi', 1, 0, 1, 1);

-- Registro 143/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0185', 5.0, 1, 0, 1, 1, 'Atasco de saneamiento en Amurrio', 'Atasco de saneamiento', '2025-08-17', '2025-08-17', 43.05394444444444, -3.0389166666666667, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 2);

-- Registro 144/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0186', 3.0, 1, 0, 1, 1, 'Fuga de agua en Erbi', 'Fuga de agua en Erbi', '2025-08-18', '2025-08-18', 43.07519444444445, -3.1391944444444446, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Erbi-Ayala', 1, 0, 1, 1);

-- Registro 145/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0187', 3.0, 1, 0, 1, 1, 'Fuga de agua en Berganza', 'Fuga de agua', '2025-08-18', '2025-08-18', 43.12130555555556, -3.156138888888889, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Berganza-Baranbio', 1, 0, 1, 1);

-- Registro 146/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0050', 5.0, 2, 1, 1, 4, 'Mantenimiento preventivo con camión de saneamiento en Llodio', 'Mantenimiento preventivo con camión de saneamient en Llodio: Goikoplaza, Tubacex, Zumalakarregi.', '2025-08-18', '2025-08-18', 43.13822222222222, -2.9897500000000004, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 4, 0, 1, 0);

-- Registro 147/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0188', 3.0, 1, 0, 5, 5, 'Reparación de fuga y tapado de cata en Zambrana', 'Reparación de fuga y tapado de cata', '2025-08-18', '2025-08-18', 42.66152777777778, -2.9066944444444447, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Zambrana', 5, 0, 1, 1);

-- Registro 148/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0051', 3.0, 2, 8, 1, 1, 'Retirada de contadores en Amurrio', 'Retirada de contadores de txonas, etc.', '2025-08-18', '2025-08-18', 43.04991666666667, -3.0236388888888888, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 0);

-- Registro 149/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0189', 3.0, 1, 0, 5, 5, 'Fuga de agua en Zambrana', 'Fuga de agua en Zambrana', '2025-08-19', '2025-08-19', 42.66405555555556, -2.90725, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Zambrana', 5, 0, 1, 1);

-- Registro 150/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0190', 3.0, 1, 0, 1, 1, 'Fuga de agua en Lujatea (Erbi)', 'Fuga de agua en Lujatea', '2025-08-19', '2025-08-19', 43.0775, -3.140861111111111, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Lujatea-Erbi', 1, 0, 1, 1);

-- Registro 151/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0052', 3.0, 2, 1, 5, 5, 'Limpieza de red de saneamiento en Pinedo', 'Limpieza de red de saneamiento', '2025-08-19', '2025-08-19', 42.8755, -3.174472222222222, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Pinedo', 5, 0, 1, 0);

-- Registro 152/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0053', 2.0, 2, 3, 4, 4, 'Limpieza fosa séptica en Durana', 'Limpieza fosa séptica. Picar arquetas, preparar y colocar tapas de arquetas. Hormigonar. Recoger escombros.', '2025-08-19', '2025-08-19', 42.890166666666666, -2.67475, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Durana', 4, 0, 1, 0);

-- Registro 153/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0054', 3.0, 2, 8, 1, 1, 'Instalación de contador en Llodio', 'Instalación de contador en el rocódromo de Llodio', '2025-08-19', '2025-08-19', 43.13713888888889, -2.9916944444444447, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 154/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0055', 2.0, 2, 3, 1, 1, 'Limpieza de la Fosa de Izoria', 'Mantenimiento de la Fosa de Izoria', '2025-08-19', '2025-08-19', 43.06111111111111, -3.0753055555555555, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Izoria', 1, 0, 1, 0);

-- Registro 155/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0056', 2.0, 2, 3, 1, 1, 'Limpieza de la fosa Artomaña', 'Limpieza de la fosa Artomaña', '2025-08-19', '2025-08-19', 42.98419444444445, -3.008916666666667, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artomaña-Amurrio', 1, 0, 1, 0);

-- Registro 156/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0191', 3.0, 1, 0, 3, 3, 'Fuga de agua en Opacua', 'Fugade agua en Opakua', '2025-08-20', '2025-08-20', 42.82866666666667, -2.392527777777778, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Opacua', 3, 0, 1, 1);

-- Registro 157/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0192', 3.0, 1, 0, 5, 5, 'Aviso de usuario por presión en Ribabellosa', 'Aviso de usuario por presión', '2025-08-20', '2025-08-20', 42.708555555555556, -2.9594722222222223, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa', 5, 0, 1, 3);

-- Registro 158/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0193', 3.0, 1, 0, 1, 1, 'Cambio de contador y reductora en mal estado en Amurrio', 'Cambio de contador y reductora en mal estado', '2025-08-20', '2025-08-20', 43.05305555555555, -3.043083333333333, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 3);

-- Registro 159/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0057', 3.0, 2, 8, 1, 1, 'Alta contador en Llodio', 'Alta contador', '2025-08-20', '2025-08-20', 43.13719444444445, -2.993361111111111, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 160/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0058', 3.0, 2, 8, 1, 1, 'Alta contador en Llodio', 'Alta contador', '2025-08-20', '2025-08-20', 43.141888888888886, -2.993638888888889, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 161/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0059', 2.0, 2, 3, 3, 3, 'Mantenimiento fosa séptica Elburgo', 'Mantenimiento fosa séptica, desbrozar fosa séptica', '2025-08-20', '2025-08-20', 42.84952777777778, -2.57725, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Elburgo', 3, 0, 1, 0);

-- Registro 162/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0060', 2.0, 2, 3, 5, 5, 'Mantenimiento fosa séptica Lahoz', 'Mantenimiento fosa séptica, desbrozar fosa séptica', '2025-08-20', '2025-08-20', 42.88447222222222, -3.277527777777778, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Lahoz', 5, 0, 1, 0);

-- Registro 163/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0061', 2.0, 2, 3, 1, 1, 'Mantenimiento fosa séptica en Delika', 'Mantenimiento fosa séptica', '2025-08-20', '2025-08-20', 42.969972222222225, -3.0278055555555556, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Delika', 1, 0, 1, 0);

-- Registro 164/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0194', 3.0, 1, 0, 5, 5, 'Reparación de fuga en Jokano', 'Reparación de fuga', '2025-08-20', '2025-08-20', 42.87188888888889, -2.9614166666666666, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Jokano', 5, 0, 1, 1);

-- Registro 165/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0195', 3.0, 1, 0, 6, 6, 'Reparación de fuga del contador en Maeztu', 'Reparación de fuga', '2025-08-21', '2025-08-21', 42.739111111111114, -2.4783611111111115, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maeztu', 6, 0, 1, 1);

-- Registro 166/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0196', 3.0, 1, 0, 5, 5, 'Aviso de falta de agua en Salinas de Añana', 'Reductora en mal estado.', '2025-08-21', '2025-08-21', 42.80255555555555, -3.028638888888889, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Salinas de Añana-AÑANA', 5, 0, 1, 3);

-- Registro 167/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0062', 2.0, 2, 3, 5, 5, 'Mantenimiento fosa séptica de San Miguel', 'Limpieza de la fosa de San Miguel con camión succionador y descarga en la depuradora.', '2025-08-21', '2025-08-21', 42.756972222222224, -2.96225, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'San Miguel', 5, 0, 1, 0);

-- Registro 168/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0063', 2.0, 2, 3, 1, 1, 'Mantenimiento fosa séptica en Artzeniaga', 'Limpieza de la fosa de Artziniega', '2025-08-21', '2025-08-21', 43.12275, -3.1625277777777776, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 0, 1, 0);

-- Registro 169/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0197', 3.0, 1, 0, 1, 1, 'Recoger escombro en Amurrio', 'Recoger escombro', '2025-08-21', '2025-08-21', 43.14147222222222, -2.996138888888889, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 3);

-- Registro 170/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0198', 3.0, 1, 0, 1, 1, 'Tapado de catas en Menagarai', 'Tapado de catas', '2025-08-21', '2025-08-21', 43.096444444444444, -3.1130833333333334, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Menagaray', 1, 0, 1, 3);

-- Registro 171/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0199', 3.0, 1, 0, 3, 3, 'Reparación de fuga en la EDAR Agurain/Salvatierra', 'Reparación de fuga en la EDAR Agurain', '2025-08-21', '2025-08-22', 42.85602777777778, -2.4466944444444443, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 0, 1, 1);

-- Registro 172/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0200', 3.0, 1, 0, 5, 5, 'Aviso de fuga de agua en Puentelarrá', 'Aviso de fuga de agua en Puentelarrá por filtro roto', '2025-08-22', '2025-08-22', 42.75138888888889, -3.0803055555555554, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Puentelarra', 5, 0, 1, 1);

-- Registro 173/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0064', 3.0, 2, 8, 5, 5, 'Alta contador en Antezana de la Ribera', 'Alta contador', '2025-08-22', '2025-08-22', 42.771277777777776, -2.9139166666666667, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Antezana de la Ribera', 5, 0, 1, 0);

-- Registro 174/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0065', 3.0, 2, 8, 5, 5, 'Alta contador en Anuntzeta', 'Alta contador', '2025-08-22', '2025-08-22', 42.80122222222222, -2.930861111111111, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Anuntzeta', 5, 0, 1, 0);

-- Registro 175/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0066', 2.0, 2, 3, 5, 5, 'Desbrozado de fosa Arbígano', 'Desbrozado de fosa. Desatascar y quitar raíces.', '2025-08-22', '2025-08-22', 42.805, -2.964472222222222, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Arbígano', 5, 0, 1, 0);

-- Registro 176/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0067', 1.0, 2, 2, 1, 1, 'Limpieza de captaciones Katzabazo, Intxutaspe, Delika, Artomaña', 'Limpieza de captaciones Katzabazo, Intxutaspe, Delika, Artomaña', '2025-08-22', '2025-08-22', 42.984027777777776, -3.0147500000000003, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Katxabazo, Intxutaspe, Delika, Artomaña-Aiaraldea', 1, 0, 1, 0);

-- Registro 177/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0201', 3.0, 1, 0, 1, 1, 'Fuga de agua en Delika', 'Fuga de agua en Delika', '2025-08-22', '2025-08-22', 42.96955555555556, -3.0316944444444447, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Delika', 1, 0, 1, 1);

-- Registro 178/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0202', 5.0, 1, 0, 1, 3, 'Atasco en Luiando', 'Atasco en Luiando', '2025-08-22', '2025-08-22', 43.09963888888889, -3.031972222222222, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Luiando', 3, 0, 1, 2);

-- Registro 179/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0203', 3.0, 1, 0, 3, 3, 'Fuga de agua en Depuradora Agurain', 'Fuga de agua en Depuradora Agurain', '2025-08-22', '2025-08-22', 42.85611111111111, -2.4489166666666664, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 0, 1, 1);

-- Registro 180/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0204', 3.0, 1, 0, 3, 3, 'Fuga en Opakua', 'Fuga en Opakua', '2025-08-19', '2025-08-19', 42.82805555555556, -2.3991944444444444, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Opacua', 3, 0, 1, 1);

-- Registro 181/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0205', 3.0, 1, 0, 3, 3, 'Aviso de fuga en Eguileor', 'Aviso de fuga en Eguileor', '2025-08-19', '2025-08-19', 42.82027777777778, -2.4328055555555554, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Eguileor', 3, 0, 1, 1);

-- Registro 182/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0206', 3.0, 1, 0, 3, 3, 'Fuga de contador en Agurain/Salvatierra', 'Arreglo de fuga de un contador', '2025-08-19', '2025-08-19', 42.848555555555556, -2.4330833333333333, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain/Salvatierra', 3, 0, 1, 1);

-- Registro 183/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0207', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Maroño', 'Reparación de fuga en Maroño', '2025-08-20', '2025-08-20', 43.0515, -3.1000277777777776, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maroño', 1, 0, 1, 1);

-- Registro 184/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0208', 5.0, 1, 0, 1, 2, 'Atasco de Retes de Tudela (Artzeniaga)', 'Atasco de Retes de Tudela', '2025-08-21', '2025-08-21', 43.114555555555555, -3.216972222222222, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Retes de Tudela', 2, 0, 1, 2);

-- Registro 185/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0068', 2.0, 2, 3, 5, 5, 'Desbroce de fosas sépticas en Lahoz', 'Mantenimiento fosas sépticas, desbroce de fosas sépticas', '2025-08-21', '2025-08-21', 42.8845, -3.283916666666667, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Lahoz', 5, 0, 1, 0);

-- Registro 186/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0069', 5.0, 2, 1, 1, 4, 'Limpieza purgador y revisión de camión de saneamiento en Llodio', 'Limpieza purgador y revisión de camión de saneamiento', '2025-08-21', '2025-08-21', 43.147194444444445, -3.017527777777778, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Colegio La Milagrosa', 4, 0, 1, 0);

-- Registro 187/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0209', 5.0, 1, 0, 5, 45, 'Desatasco de saneamiento en Zambrana', 'Desatasco de saneamiento en Zambrana', '2025-08-21', '2025-08-21', 42.66116666666667, -2.9178055555555558, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Zambrana', 45, 0, 1, 2);

-- Registro 188/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0070', 5.0, 2, 13, 5, 41, 'Asistencia técnica a Urbide', 'Asistencia técnica a Urbide', '2025-08-21', '2025-08-21', 42.70569444444445, -2.9680833333333334, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa', 41, 0, 1, 0);

-- Registro 189/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0212', 3.0, 1, 0, 5, 5, 'Búsqueda de fuga en Salinas de Añana', 'Búsqueda de fuga en Salinas de Añana', '2025-08-18', '2025-08-18', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Salinas de Añana', 5, 0, 1, 1);

-- Registro 190/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0211', 3.0, 1, 0, 4, 4, 'Búsqueda de fuga en Landa', 'Búsqueda de fuga', '2025-08-18', '2025-08-18', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Landa', 4, 0, 1, 1);

-- Registro 191/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0210', 3.0, 1, 0, 3, 3, 'Búsqueda de fuga en Opakua-Agurain', 'Búsqueda de fuga en Opakua', '2025-08-18', '2025-08-18', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Opacua', 3, 0, 1, 1);

-- Registro 192/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0071', 2.0, 2, 3, 5, 5, 'Limpieza fosa de Jokano', 'Limpieza fosa de Jokano', '2025-08-22', '2025-08-22', 42.871916666666664, -2.9691944444444442, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Jokano-Kuartango', 5, 0, 1, 0);

-- Registro 193/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0213', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Olabezar', 'Reparación de fuga en Olabezar', '2025-08-23', '2025-08-23', 43.06841666666667, -3.0528055555555556, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Olabezar', 1, 0, 1, 1);

-- Registro 194/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0214', 5.0, 1, 0, 1, 3, 'Desatasco de red de saneamiento en Murga', 'Desatasco de red de saneamiento', '2025-08-24', '2025-08-24', 43.07630555555556, -3.06975, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Murga', 3, 0, 1, 2);

-- Registro 195/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0217', 3.0, 1, 0, 3, 3, 'Reparación de fuga en Agurain', 'Reparación de fuga en Agurain', '2025-08-26', '2025-08-26', 42.85344444444445, -2.4366944444444445, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 0, 1, 1);

-- Registro 196/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0216', 5.0, 1, 0, 1, 1, 'Desatasco en Amurrio', 'Desatasco en Amurrio Landaburu 37', '2025-08-27', '2025-08-27', 43.10552777777778, -3.703638888888889, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 2);

-- Registro 197/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0215', 5.0, 1, 0, 3, 26, 'Reparación arqueta de saneamiento en Opacua', 'Reparación arqueta de saneamiento', '2025-08-26', '2025-08-26', 42.82736111111112, -2.403916666666667, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Opacua', 26, 0, 1, 3);

-- Registro 198/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0072', 2.0, 2, 3, 1, 1, 'Revisión y desbroce para limpieza de fosas en Artziniega', 'Revisión y desbroce para limpieza de fosas en Artziniega', '2025-08-25', '2025-08-25', 43.11911111111111, -3.1708611111111114, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 0, 1, 0);

-- Registro 199/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0073', 3.0, 2, 8, 1, 1, 'Instalación de contador en Murga', 'Instalación de contador', '2025-08-25', '2025-08-25', 43.07566666666667, -3.0711388888888886, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Murga', 1, 0, 1, 0);

-- Registro 200/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0074', 2.0, 2, 3, 3, 3, 'Limpieza de fosa Gazeta', 'Limpieza de fosa Gazeta', '2025-08-26', '2025-08-26', 42.843444444444444, -2.588083333333333, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Gazeta', 3, 0, 1, 0);

-- Registro 201/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0075', 2.0, 2, 3, 5, 5, 'Limpieza de fosa de Portilla', 'Limpieza de fosa de Portilla', '2025-08-27', '2025-08-27', 42.67225, -2.888361111111111, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Portilla-Zambrana', 5, 0, 1, 0);

-- Registro 202/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0076', 3.0, 2, 8, 3, 3, 'Instalación de contador en Agurain', 'Instalación de contador, estaba mal puesto', '2025-08-26', '2025-08-26', 42.849944444444446, -2.438638888888889, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 0, 1, 0);

-- Registro 203/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0218', 3.0, 1, 0, 1, 1, 'Fuga de agua en Olabezar', 'Fuga de agua en Olabezar', '2025-08-25', '2025-08-25', 43.068361111111116, -3.0555833333333333, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Olabezar', 1, 0, 1, 1);

-- Registro 204/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0077', 2.0, 2, 3, 1, 1, 'Mantenimiento fosas sépticas de Artziniega y Llanteno', 'Mantenimiento fosas sépticas de Artziniega y Llanteno', '2025-08-26', '2025-08-26', 43.12105555555556, -3.172527777777778, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega y Llanteno', 1, 0, 1, 0);

-- Registro 205/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0219', 5.0, 1, 0, 1, 3, 'Atasco en Llanteno Ureta', 'Atasco en Llanteno Ureta', '2025-08-26', '2025-08-26', 43.10919444444445, -3.1394722222222224, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llanteno', 3, 0, 1, 2);

-- Registro 206/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0220', 3.0, 1, 0, 1, 1, 'Fuga de agua en Barretaguren, Artziniega', 'Reparación de la fuga de agua en Barretaguren, Artziniega', '2025-08-26', '2025-08-26', 43.12636111111111, -3.1730833333333335, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 0, 1, 1);

-- Registro 207/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0078', 2.0, 2, 3, 1, 1, 'Limpieza de fosa séptica Larrinbe', 'Limpieza de fosa séptica Larrinbe', '2025-08-27', '2025-08-27', 43.03808333333333, -3.0233611111111114, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Larrinbe', 1, 0, 1, 0);

-- Registro 208/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0221', 1.0, 1, 0, 1, 1, 'Fuga de agua en Erbi', 'Reparación fuga de agua en Erbi', '2025-08-27', '2025-08-27', 43.07505555555556, -3.1569722222222225, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Erbi', 1, 0, 1, 1);

-- Registro 209/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0222', 1.0, 1, 0, 1, 1, 'Fuga de agua en Berganza', 'Fuga de agua en Berganza', '2025-08-27', '2025-08-27', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Berganza-Baranbio', 1, 0, 1, 1);

-- Registro 210/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0079', 2.0, 2, 3, 1, 1, 'Mantenimiento de la fosa séptica Larrimbe', 'Limpieza de mantenimiento de la fosa séptica Larrinbe', '2025-08-28', '2025-08-28', 43.03736111111111, -3.0241944444444444, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Larrinbe', 1, 0, 1, 0);

-- Registro 211/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0223', 5.0, 1, 0, 1, 1, 'Desatasco en Amurrio', 'Desatasco en Amurrio Landaburu 30', '2025-08-28', '2025-08-28', 43.06119444444444, -3.041138888888889, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 2);

-- Registro 212/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0080', 3.0, 2, 11, 1, 1, 'Lectura de contadores en Aiala, Llodio y Agurain', 'Lectura de contadores en Aiala, Llodio y Agurain', '2025-08-28', '2025-08-28', 43.14, -3.0080833333333334, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Aiala,Llodio y Agurain', 1, 0, 1, 0);

-- Registro 213/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0081', 5.0, 2, 1, 1, 1, 'Mantenimiento preventivo saneamiento en San Jose en Amurrio', 'Limpieza del conector de mantenimiento preventivo de saneamiento de conector de San José kalea', '2025-08-28', '2025-08-28', 43.06033333333333, -3.0416944444444445, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'San José Kalea', 1, 0, 1, 0);

-- Registro 214/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0224', 3.0, 1, 0, 4, 4, 'Fuga de agua en Luko', 'Reparación de fuga de agua en Luko', '2025-08-28', '2025-08-28', 42.934555555555555, -2.691972222222222, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Luko', 4, 0, 1, 1);

-- Registro 215/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0082', 1.0, 2, 2, 1, 1, 'Limpieza de captaciones en  Artomaña, Delika, Katzabazo, Intxutaspe, Lejarzo y Añes', 'Limpieza de las captaciones Artomaña, Delika, Katzabazo, Intxutaspe, Lejarzo y Añes', '2025-08-29', '2025-08-29', 42.984027777777776, -3.0255833333333335, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'AIARALDEA', 1, 0, 1, 0);

-- Registro 216/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0083', 5.0, 2, 1, 1, 1, 'Mantenimiento preventivo saneamiento en Artomaña', 'Mantenimiento preventivo saneamiento en Artomaña', '2025-08-29', '2025-08-29', 42.98302777777778, -3.0258611111111113, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artomaña', 1, 0, 1, 0);

-- Registro 217/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0084', 2.0, 2, 3, 1, 1, 'Desbroce de fosas para limpieza en Zuaza, Respaldiza e Izoria', 'Desbroce de fosas para limpieza', '2025-08-29', '2025-08-29', 43.099611111111116, -3.0928055555555556, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Zuaza, Respaldiza e Izoria', 1, 0, 1, 0);

-- Registro 218/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0225', 3.0, 1, 0, 5, 5, 'Reparación de fuga de agua en Sobrón', 'Fuga de agua en Sobrón', '2025-08-29', '2025-08-29', 42.76244444444445, -3.126416666666667, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Sobron-Lantaron', 5, 0, 1, 1);

-- Registro 219/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('GF/0001', 4.0, 3, 0, 10, 10, 'Gastos fijos de explotación totales', 'Gastos fijos de explotación totales', '2025-08-31', '2025-08-31', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0, 10, 0, 1, 0);

-- Registro 220/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0085', 3.0, 2, 14, 1, 1, 'Revisión de válvulas acometidas para corte de agua en Larraño 11 (Llodio)', 'Revisión de válvulas acometidas para corte de agua en Larraño 11 (Llodio)', '2025-08-22', '2025-08-22', 43.1427004811616, -2.96483231731082, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 221/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0226', 5.0, 1, 0, 1, 4, 'Aviso por falta de tapa de arquetas saneamiento en colector Landaluze (Llodio)', 'Aviso de oficina por falta de tapas de saneamiento', '2025-08-22', '2025-08-22', 43.141403, -2.971872, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 4, 0, 1, 3);

-- Registro 222/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0086', 3.0, 2, 8, 1, 1, 'Instalación contador barracas - autos de choque (Llodio)', 'Instalación contador barracas - autos de choque (Llodio)', '2025-08-22', '2025-08-22', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 223/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0087', 3.0, 2, 8, 1, 1, 'Instalación contador churrería (Llodio)', 'Instalación contador churrería (Llodio)', '2025-08-22', '2025-08-22', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 224/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0088', 3.0, 2, 10, 5, 5, 'Sustitución de contador en Rivabellosa', 'Sustitución de contador en Ribabellosa', '2025-08-29', '2025-08-29', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa', 5, 0, 1, 0);

-- Registro 225/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0089', 3.0, 2, 10, 6, 6, 'Sustitución de contador en Sabando', 'Sustitución de contador en Sabando', '2025-08-29', '2025-08-29', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Sabando', 6, 0, 1, 0);

-- Registro 226/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0090', 3.0, 2, 8, 3, 3, 'Instalación de contador en Agurain', 'Instalación de contador en Agurain', '2025-08-29', '2025-08-29', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 0, 1, 0);

-- Registro 227/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0227', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Luja (Llodio)', 'Reparación de fuga en Luja', '2025-08-30', '2025-08-30', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 228/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0228', 5.0, 1, 0, 3, 26, 'Atasco de saneamiento en Calle Carnicerías (Agurain)', 'Atasco de saneamiento', '2025-08-30', '2025-08-30', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 26, 0, 1, 2);

-- Registro 229/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0229', 3.0, 1, 0, 5, 5, 'Reparación de fuga en Calle Los Olmos (Rivabellosa)', 'Reparación de fuga', '2025-08-30', '2025-08-30', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa-Rivera Alta', 5, 0, 1, 1);

-- Registro 230/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0230', 3.0, 1, 0, 1, 1, 'Aviso de fuga en Pozoportillo (Ozeka)', 'Acudir al aviso a ver', '2025-08-31', '2025-08-31', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ozeka', 1, 0, 1, 1);

-- Registro 231/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0231', 5.0, 1, 0, 1, 1, 'Atasco de saneamiento en La Estación (Amurrio)', 'Atasci de Saneamiento', '2025-08-31', '2025-08-31', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 2);

-- Registro 232/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('GF/0002', 4.0, 3, 0, 10, 10, 'Gestión documental del contrato', 'Gestión documental del contrato', '2025-08-31', '2025-08-31', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0, 10, 'ELENA', 1, 0);

-- Registro 233/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0091', 5.0, 2, 5, 6, 46, 'Inventario y digitalización redes saneamiento en Maeztu y Artziniega', 'Maeztu y Artziniega', '2025-08-31', '2025-08-31', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maeztu-Arraia/Maeztu', 46, 0, 1, 0);

-- Registro 234/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0232', 3.0, 1, 0, 1, 1, 'Aviso de fuga en Larraño y parque lamuza (Llodio)', 'Aviso de por fuga en bajada de Luja y aviso de fuente fugando en parque Lamuza. Se cierra acometida de la fuente.', '2025-08-30', '2025-08-30', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 235/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0233', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Luja (Llodio)', 'Reparación de fuga', '2025-09-01', '2025-09-02', 43.145086, -2.972267, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 236/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0234', 3.0, 1, 0, 1, 1, 'Sustituir válvulas acometidas en Artziniega', 'Sustituir válvulas acometidas en Artziniega', '2025-09-01', '2025-09-02', 43.121351, -3.129068, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 0, 1, 3);

-- Registro 237/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0092', 3.0, 2, 7, 3, 3, 'Localización de fugas en Opakua', 'Localización de fugas en Opakua', '2025-08-18', '2025-08-18', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Opacua', 3, 0, 1, 1);

-- Registro 238/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0093', 3.0, 2, 7, 4, 4, 'Localizar acometidas con fuga y buscar solución en Landa', 'Localizar acometidas con fuga y buscar solución en Landa', '2025-08-18', '2025-08-18', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Landa', 4, 0, 1, 1);

-- Registro 239/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0094', 2.0, 2, 3, 10, 10, 'Revisión de fosas sépticas-ALAVA', 'Revisión de fosas sépticas', '2025-08-18', '2025-08-18', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Todos los municipios', 10, 0, 1, 0);

-- Registro 240/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0095', 3.0, 2, 7, 5, 5, 'Localización de fuga por aviso de filtraciones en Salinas de Añana', 'Localización de fuga por aviso de filtraciones', '2025-08-18', '2025-08-18', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Salinas de Añana', 5, 0, 1, 1);

-- Registro 241/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0096', 3.0, 2, 7, 1, 1, 'Localización de fuga en Plaza Boriñaur (Amurrio)', 'Localización de fuga en Plaza Boriñaur (Amurrio)', '2025-08-19', '2025-08-19', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 1);

-- Registro 242/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0097', 3.0, 2, 7, 1, 1, 'Localizaciçon de fuga en La Estación (Amurrio)', 'Localizaciçon de fuga en La Estación (Amurrio)', '2025-08-21', '2025-08-21', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 1);

-- Registro 243/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0098', 3.0, 2, 7, 5, 5, 'Localización de fuga en Txistularis', 'Localización de fuga en Txistularis', '2025-08-21', '2025-08-21', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa', 5, 0, 1, 1);

-- Registro 244/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0099', 3.0, 2, 7, 4, 4, 'Localización de fuga en Luko', 'Localización de fuga en Luko', '2025-08-25', '2025-08-25', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Luko', 4, 0, 1, 1);

-- Registro 245/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0114', 3.0, 2, 7, 1, 1, 'Localización de fuga en  Ugarte', 'Calle Iturriaga', '2025-08-26', '2025-08-26', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ugarte', 1, 0, 1, 1);

-- Registro 246/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0100', 3.0, 2, 7, 1, 1, 'Localización de fuga en Ugarte', 'Localización de fuga en Ugarte', '2025-08-25', '2025-08-25', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 247/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0101', 3.0, 2, 19, 1, 1, 'Revisión de sectores Amurrio y Laudio', 'Revisión de sectores Amurrio y Laudio', '2025-08-26', '2025-08-26', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Laudio y Amurrio', 1, 0, 1, 0);

-- Registro 248/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0102', 5.0, 2, 1, 1, 1, 'Mantenimiento preventivo saneamiento Amurrio', 'Atasco Amurrio', '2025-08-26', '2025-08-26', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio-AIARA', 1, 0, 1, 2);

-- Registro 249/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0103', 3.0, 2, 4, 1, 1, 'Digitalización Perte en Amurrio', 'Digitalización Perte', '2025-08-27', '2025-08-27', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio-AIARA', 1, 0, 1, 0);

-- Registro 250/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0104', 5.0, 2, 5, 1, 1, 'Base de datos de fosas sépticas en Amurrio', 'Base de datos de fosas sépticas', '2025-08-28', '2025-08-28', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio-AIARA', 1, 0, 1, 0);

-- Registro 251/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0105', 3.0, 2, 19, 1, 1, 'Revisión de consumos Mendiko', 'Revisión de consumos Mendiko', '2025-08-28', '2025-08-28', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio-AIARA', 1, 0, 1, 0);

-- Registro 252/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0106', 3.0, 2, 11, 10, 10, 'Lectura de Contadores Sectoriales-ALAVA', 'Lectura de Contadores Sectoriales', '2025-08-29', '2025-08-29', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Todos los municipios-ALAVA', 10, 0, 1, 0);

-- Registro 253/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0107', 3.0, 2, 14, 1, 1, 'Comprobación de válvulas de acometida en Luiaondo', 'Comprobación de válvulas de acometida', '2025-08-25', '2025-08-25', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Luiando', 1, 0, 1, 0);

-- Registro 254/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0237', 3.0, 1, 0, 1, 1, 'Fuga en hidrante en Ostegieta', 'Cerrar hidrante', '2025-08-25', '2025-08-25', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 255/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0235', 3.0, 1, 0, 1, 1, 'Reparación fuga Larraño', 'Reparación fuga Larraño', '2025-08-27', '2025-08-27', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Larraño', 1, 0, 1, 1);

-- Registro 256/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0109', 5.0, 2, 1, 1, 4, 'Revisión colectores en Laudio', 'Revisión colectores', '2025-08-27', '2025-08-27', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 4, 0, 1, 0);

-- Registro 257/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0236', 3.0, 1, 0, 1, 1, 'Reparación fuga Iturriaga 2', 'Reparación fuga Iturriaga 2', '2025-08-28', '2025-08-28', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 258/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0110', 3.0, 2, 12, 1, 1, 'Corte de agua Arbol Malato 2-4 en Laudio', 'Corte de agua Arbol Malato 2-4', '2025-08-28', '2025-08-28', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 259/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0111', 3.0, 2, 8, 1, 1, 'Instalación Contador Arbol Malato 2 en Laudio', 'Instalación Contador Arbol Malato 2', '2025-08-28', '2025-08-28', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 260/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0112', 3.0, 2, 10, 1, 1, 'Sustitución contador Goienuri 11 3ºD en Laudio', 'Sustitución contador Goienuri 11 3ºD', '2025-08-29', '2025-08-29', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 261/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0113', 3.0, 2, 9, 1, 1, 'Retirada de contador Ruperto Urquijo 12 2º A en Laudio', 'Retirada de contador Ruperto Urquijo 12 2ºA', '2025-08-29', '2025-08-29', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 262/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0115', 3.0, 2, 10, 1, 1, 'Sustitución de contador en instituto Zaraobe', 'Sustitución contador Octave', '2025-09-01', '2025-09-01', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 0);

-- Registro 263/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0116', 5.0, 2, 3, 1, 3, 'Limpieza Sojo Red saneamiento en Sojo', 'Limpieza Sojo Red saneamiento', '2025-09-01', '2025-09-01', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Sojo', 3, 0, 1, 0);

-- Registro 264/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0238', 3.0, 1, 0, 5, 5, 'Fuga Rivabellosa', 'Arreglo de fuga', '2025-09-01', '2025-09-25', 42.707141, -2.914956, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa', 5, 0, 1, 1);

-- Registro 265/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0117', 3.0, 2, 7, 1, 1, 'Localizacion fugas abastecimiento en Llodio', 'Busqueda de fugas en sector centro -norte Laudio', '2025-09-01', '2025-09-01', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 266/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0118', 2.0, 2, 3, 1, 1, 'Limpieza mto. fosas septicas en Aiarealdea', 'Limpieza mto. fosas septicas', '2025-09-02', '2025-09-02', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'AIARALDEA', 1, 0, 1, 0);

-- Registro 267/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0119', 3.0, 2, 8, 3, 3, 'Instalación de contador en Agurain', 'Alta de contador. Instalación', '2025-09-02', '2025-09-02', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 0, 1, 0);

-- Registro 268/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0239', 3.0, 1, 0, 1, 1, 'Fuga en Kejana', 'Reparación fuga', '2025-09-02', '2025-09-02', 43.080398, -3.064624, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Quejana', 1, 0, 1, 1);

-- Registro 269/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0240', 3.0, 1, 0, 1, 1, 'Fuga Berganza', 'Reparacion Fuga', '2025-09-02', '2025-09-02', 43.055656, -2.935592, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Berganza-Baranbio', 1, 0, 1, 1);

-- Registro 270/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0241', 5.0, 1, 0, 3, 26, 'Atasco Agurain', 'Repación de atasco en Agurain', '2025-09-03', '2025-09-03', 42.848688, -2.391511, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 26, 0, 1, 2);

-- Registro 271/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0242', 3.0, 1, 0, 1, 1, 'Fuga Artziniega fibrocemento', 'Fuga de fibrocemento en Arceniaga', '2025-09-03', '2025-09-03', 43.132923, -3.115985, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 0, 1, 1);

-- Registro 272/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0243', 5.0, 1, 0, 3, 21, 'Atasco en cementerio de Alegria-Dulantzi', 'Atasco en cementerio', '2025-09-03', '2025-09-03', 42.842024, -2.519995, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 21, 0, 1, 2);

-- Registro 273/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0120', 2.0, 2, 3, 1, 1, 'Revisión F.Septicas en Aiaraldea y c.c.m.m', 'Revisión F.S en Aiaraldea', '2025-09-03', '2025-09-03', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'AIARALDEA', 1, 0, 1, 0);

-- Registro 274/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0121', 3.0, 2, 8, 1, 1, 'Intalación contador en Landako (Amurrio)', 'Se le da la vuelta al contador en la instalación', '2025-09-03', '2025-09-03', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Landako', 1, 0, 1, 0);

-- Registro 275/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0244', 3.0, 1, 0, 1, 1, 'Reparación de Fuga Artziniega', 'Reparación de Fuga Artziniega', '2025-09-03', '2025-09-03', 43.138378, -3.112667, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 0, 1, 1);

-- Registro 276/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0122', 2.0, 2, 3, 5, 5, 'Limpieza fosa en Arbígano (Ribera Alta)', 'Limpieza fosa en Arbígano (Ribera Alta)', '2025-09-03', '2025-09-03', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Arbígano', 5, 0, 1, 0);

-- Registro 277/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0123', 2.0, 2, 3, 1, 1, 'Limpieza Fosa en Larrimbe', 'Limpieza Fosa en Larrimbe', '2025-09-03', '2025-09-03', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Larrinbe', 1, 0, 1, 0);

-- Registro 278/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0245', 3.0, 1, 0, 1, 1, 'Colocar tapón en Murga', 'Colocar tapón en Murga', '2025-09-03', '2025-09-03', 43.082523, -3.01195, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Murga', 1, 0, 1, 3);

-- Registro 279/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0246', 2.0, 1, 0, 1, 1, 'Reparacion fuga en Erbi', 'Reparacion fuga en Erbi', '2025-09-04', '2025-09-04', 43.074505, -3.113119, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Erbi', 1, 0, 1, 1);

-- Registro 280/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0124', 3.0, 2, 10, 1, 1, 'Sustitución contador en Amurrio', 'Sustitución contador en Amurrio', '2025-09-04', '2025-09-04', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 0);

-- Registro 281/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0125', 3.0, 2, 7, 1, 1, 'Localización fugas en abastecimiento en Llodio', 'Localización fugas en abastecimiento en Llodio', '2025-09-04', '2025-09-04', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 282/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0247', 5.0, 1, 0, 5, 41, 'Desatascar colector de saneamiento en Anucita', 'Desatascar colector de saneamiento en Anucita', '2025-09-04', '2025-09-04', 42.801546, -2.899364, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Anucita', 41, 0, 1, 2);

-- Registro 283/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0248', 2.0, 1, 0, 6, 6, 'Reparación fuga acometida fuente en Arraya', 'Reparación fuga acometida fuente en Maeztu', '2025-09-02', '2025-09-02', 42.73949, -2.44667, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maeztu', 6, 0, 1, 1);

-- Registro 284/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0249', 5.0, 1, 0, 1, 1, 'Reparación saneamiento y desatasco en Amurrio', 'Reparación saneamiento fuga y desatasco en Aldai 38', '2025-09-01', '2025-09-08', 43.046377, -3.004386, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 2);

-- Registro 285/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0250', 3.0, 1, 0, 1, 1, 'Reparacion de fuga en Amurrio', 'Reparacion fuga en Aldai 38', '2025-09-01', '2025-09-01', 43.046377, -3.004386, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 1);

-- Registro 286/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0126', 3.0, 2, 8, 6, 6, 'Instalación contadores en Sabando', 'Reparando bebederos del pueblo en Sabando', '2025-09-04', '2025-09-04', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Sabando', 6, 0, 1, 0);

-- Registro 287/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0127', 5.0, 2, 3, 1, 4, 'Mantenimiento preventivo en saneamiento en Llodio', 'Mantenimiento cadena al camión de saneamiento', '2025-09-04', '2025-09-04', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 4, 0, 1, 0);

-- Registro 288/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0250', 5.0, 1, 0, 5, 44, 'Desatasco en Tuesta', 'Desatasco en Tuesta', '2025-09-04', '2025-09-04', 42.809203, -3.025301, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Tuesta', 44, 0, 1, 2);

-- Registro 289/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0128', 2.0, 2, 3, 1, 1, 'Limpieza de Fosa en Mimeza (Redes)', 'Limpieza de Fosa en Mimeza (Redes)', '2025-09-04', '2025-09-04', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Mimeza', 1, 0, 1, 0);

-- Registro 290/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0129', 2.0, 2, 3, 3, 3, 'Limpieza Fosa de Gereñu', 'Limpieza Fosa de Gereñu', '2025-09-08', '2025-09-08', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Gereñu', 3, 0, 1, 0);

-- Registro 291/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0130', 2.0, 2, 3, 4, 4, 'Limpieza de Fosa en Durana', 'Limpieza de Fosa en Durana', '2025-09-08', '2025-09-08', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Durana', 4, 0, 1, 0);

-- Registro 292/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0131', 3.0, 2, 7, 1, 1, 'Localización de Fugas en abastecimiento en Respaldiza', 'Localización de Fugas en abastecimiento en Respaldiza', '2025-09-09', '2025-09-09', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Respaldiza', 1, 0, 1, 1);

-- Registro 293/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0132', 2.0, 2, 3, 1, 1, 'Mantenimiento de Fosas en Arceniaga', 'Mantenimiento de Fosas en Artzeniaga', '2025-09-09', '2025-09-09', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 0, 1, 0);

-- Registro 294/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0133', 3.0, 2, 7, 1, 1, 'Localización de Fugas en Isasi (Llodio)', 'Localización de Fugas en Isasi', '2025-09-09', '2025-09-09', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 295/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0251', 3.0, 1, 0, 1, 1, 'Arreglar fuga en Santa Lucia - Bombeo', 'Arreglar fuga en Santa Lucia - Bombeo', '2025-09-07', '2025-09-07', 43.168678, -2.98103, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Santa lucia', 1, 0, 1, 1);

-- Registro 296/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0252', 3.0, 1, 0, 5, 5, 'Arreglar Fuga en Estavillo', 'Arreglar Fuga en Estavillo en arqueta', '2025-09-07', '2025-09-07', 42.72906, -2.857946, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Estabillo', 5, 0, 1, 1);

-- Registro 297/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0253', 5.0, 1, 0, 1, 2, 'Atasco en avenida Ametzola en Artzeniaga', 'Atasco en avenida Ametzola', '2025-09-06', '2025-09-06', 43.120674, -3.132833, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 2, 0, 1, 2);

-- Registro 298/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0254', 5.0, 1, 0, 5, 44, 'Atasco en Tuesta', 'Atasco en Tuesta', '2025-09-06', '2025-09-06', 42.809203, -3.025301, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Tuesta', 44, 0, 1, 2);

-- Registro 299/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0255', 3.0, 1, 0, 3, 3, 'Fuga en ElBurgo', 'Fuga en el Burgo', '2025-09-06', '2025-09-06', 42.84874, -2.544238, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Elburgo', 3, 0, 1, 1);

-- Registro 300/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0256', 3.0, 1, 0, 1, 1, 'Fuga en Maroño', 'Fuga en Maroño', '2025-09-06', '2025-09-06', 43.04186, -3.064138, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maroño', 1, 0, 1, 1);

-- Registro 301/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0257', 3.0, 1, 0, 1, 1, 'Fuga en Etxegoien', 'Fuga en Etxegoien', '2025-09-05', '2025-09-05', 43.043339, -3.02172, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Etxegoien', 1, 0, 1, 1);

-- Registro 302/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0348', 3.0, 1, 0, 5, 5, 'Fuga en Espejo', 'Fuga en Espejo', '2025-09-05', '2025-09-05', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Espejo', 5, 0, 1, 1);

-- Registro 303/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0134', 1.0, 2, 2, 1, 1, 'Limpiezas captaciones en Llanteno', 'Limpiezas captaciones en Llanteno', '2025-09-05', '2025-09-05', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llanteno', 1, 0, 1, 0);

-- Registro 304/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0258', 3.0, 1, 0, 6, 6, 'Fuga en Sabanto', 'Fuga en Sabando', '2025-09-05', '2025-09-05', 42.749722, -2.402171, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Sabando', 6, 0, 1, 1);

-- Registro 305/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0135', 3.0, 2, 8, 5, 5, 'Cambio de contador en Tuesta', 'Cambio de contador en Tuesta', '2025-09-10', '2025-09-10', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Tuesta', 5, 0, 1, 0);

-- Registro 306/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0136', 3.0, 2, 8, 5, 5, 'Cambio de contador en Ribabellosa', 'Cambio de contador en Ribabellosa en la residencia', '2025-09-10', '2025-09-10', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa', 5, 0, 1, 0);

-- Registro 307/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0259', 3.0, 1, 0, 5, 5, 'Reparacion de fuga en Berantevilla', 'Reparacion de fuga en Berantevilla', '2025-09-10', '2025-09-25', 42.683829, -2.860906, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Berantevilla', 5, 0, 1, 1);

-- Registro 308/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0137', 2.0, 2, 3, 3, 3, 'Mantenimiento de fosas septicas en Dulantzi-Usategui', 'Mantenimiento de fosas septicas en Dulantzi', '2025-09-05', '2025-09-05', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Dulantzi', 3, 0, 1, 0);

-- Registro 309/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0138', 5.0, 2, 5, 3, 21, 'Cartografia red saneamiento inventario en P.I.Usategui', 'Cartografia red saneamiento inventario', '2025-09-05', '2025-09-05', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Dulantzi', 21, 0, 1, 0);

-- Registro 310/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0139', 3.0, 2, 7, 3, 3, 'Localización de fugas en Elburgo', 'Localización de fugas en Elburgo', '2025-09-08', '2025-09-08', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Elburgo', 3, 0, 1, 1);

-- Registro 311/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0140', 3.0, 2, 7, 5, 5, 'Localización de fugas en Berantevilla', 'Localización de fugas en Berantevilla', '2025-09-08', '2025-09-08', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Berantevilla', 5, 0, 1, 1);

-- Registro 312/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0141', 2.0, 2, 3, 5, 5, 'Mantenimiento de fosas en Corro', 'Mantenimiento de fosas en Corro', '2025-09-08', '2025-09-08', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Corro', 5, 0, 1, 0);

-- Registro 313/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0142', 3.0, 2, 7, 1, 1, 'Localización de fugas  en Respaldiza', 'Localización de fugas  en Respaldiza', '2025-09-08', '2025-09-08', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Respaldiza', 1, 0, 1, 1);

-- Registro 314/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0143', 3.0, 2, 8, 3, 3, 'Instalacion de contadores en Alegria - Dulantzi', 'Instalacion de contadores en Txoznas', '2025-09-10', '2025-09-10', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 3, 0, 1, 0);

-- Registro 315/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0144', 3.0, 2, 8, 3, 3, 'Sustitución de contadores en Alegria - Dulantzi', 'Sustitución de contadores en Alegria', '2025-09-10', '2025-09-10', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 3, 0, 1, 0);

-- Registro 316/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0145', 3.0, 2, 8, 3, 3, 'Cambio de contador en Alegria - Dulantzi', 'Cambio de contador en Alegria - Dulantzi', '2025-09-10', '2025-09-10', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Dulantzi', 3, 0, 1, 0);

-- Registro 317/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0146', 2.0, 2, 3, 3, 3, 'Limpiezas de Fosa en Elburgo', 'Limpiezas de Fosa en Elburgo', '2025-09-10', '2025-09-10', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Elburgo', 3, 0, 1, 0);

-- Registro 318/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0147', 3.0, 2, 8, 1, 1, 'Cambio juntas de contador en Menagaray', 'Cambio juntas de contador en Menagaray', '2025-09-10', '2025-09-10', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Menagaray', 1, 0, 1, 0);

-- Registro 319/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0260', 3.0, 1, 0, 1, 1, 'Reparacion de acometida en fuente calle Vitoria en Areta', 'Reparacion de acometida en fuente calle Vitoria en Areta', '2025-09-10', '2025-09-10', 43.145808, -2.942549, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Areta', 1, 0, 1, 1);

-- Registro 320/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0261', 3.0, 1, 0, 1, 1, 'Corte de agua en Llodio', 'Corte de agua en Amurrio en Avda de Zumalakarregui 36', '2025-09-11', '2025-09-11', 43.143257, -2.963193, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'llodio', 1, 0, 1, 3);

-- Registro 321/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0148', 5.0, 2, 3, 1, 4, 'Mantenimiento saneamiento en Llodio', 'Limpiar arqueta de saneamiento en Llodio', '2025-09-11', '2025-09-11', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 4, 0, 1, 0);

-- Registro 322/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0262', 5.0, 1, 0, 1, 2, 'Limpiar tamizes en Artziniega', 'Limpiar tamizes en Artziniega', '2025-09-12', '2025-09-12', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 2, 0, 1, 2);

-- Registro 323/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0263', 5.0, 1, 0, 1, 1, 'Revision posible atasco en Plaza Lezarraga (Amurrio)', 'Revision posible atasco en Plaza Lezarraga (Amurrio)', '2025-09-11', '2025-09-11', 43.053054, -3.006012, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 2);

-- Registro 324/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0149', 3.0, 2, 8, 1, 1, 'Cambio de contador en Ferrocarriles Amurrio', 'Cambio de contador en Ferrocarriles Amurrioq', '2025-09-12', '2025-09-12', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 0);

-- Registro 325/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0264', 5.0, 1, 0, 1, 2, 'Desatasco en Artziniega', 'Desatasco en Artziniega', '2025-09-12', '2025-09-12', 43.119529, -3.132643, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 2, 0, 1, 2);

-- Registro 326/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0265', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Goienuri (Llodio)', 'Reparación de fuga en Goienuri (Llodio)', '2025-09-10', '2025-09-10', 43.149083, -2.97098, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 327/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0266', 3.0, 1, 0, 1, 1, 'Reparación de fuga en calle Vitoria en Llodio', 'Reparación de fuga en la fuente de calle Vitoria en Llodio', '2025-09-09', '2025-09-09', 43.145808, -2.942549, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 328/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0267', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Larraño', 'Reparación de fuga en Larraño (Llodio)', '2025-09-11', '2025-09-11', 43.145961, -2.973334, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 329/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0316', 5.0, 1, 0, 1, 2, 'Sustitución de Tapas en Artziniega', 'Sustitución de Tapas en Artziniega', '2025-09-17', '2025-09-17', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 2, 0, 1, 3);

-- Registro 330/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0268', 3.0, 1, 0, 5, 5, 'Sustitución de válvulas en Puentelarra', 'Sustitución de válvulas en Puentelarra', '2025-09-15', '2025-09-15', 42.751179, -3.048088, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Puentelarra', 5, 0, 1, 3);

-- Registro 331/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0269', 3.0, 1, 0, 5, 5, 'Reparación de fuga en Zambrana', 'Reparación de fuga en Zambrana', '2025-09-15', '2025-09-15', 42.660992, -2.879851, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Zambrana', 5, 0, 1, 1);

-- Registro 332/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0270', 3.0, 1, 0, 5, 5, 'Reparación de fuga en Espejo', 'Reparación de fuga junto armario de contadores en Espejo', '2025-09-15', '2025-09-15', 42.809639, -3.04665, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Espejo', 5, 0, 1, 1);

-- Registro 333/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0150', 3.0, 2, 10, 5, 5, 'Sustitución de contador en Espejo', 'Cambio de contador en Espejo', '2025-09-15', '2025-09-15', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Espejo', 5, 0, 1, 0);

-- Registro 334/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0151', 3.0, 2, 10, 5, 5, 'Sustitución de contador en Espejo', 'Cambio de contador en Espejo', '2025-09-15', '2025-09-15', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Espejo', 5, 0, 1, 0);

-- Registro 335/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0152', 3.0, 2, 8, 5, 5, 'Sustitución de contador en Villanañe', 'Cambio de contador en Villanañe', '2025-09-15', '2025-09-15', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Villanañe', 5, 0, 1, 0);

-- Registro 336/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0153', 3.0, 2, 8, 5, 5, 'Sustitución de contador en Villanañe', 'Sustitución de contador en Villanañe', '2025-09-15', '2025-09-15', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Villanañe', 5, 0, 1, 0);

-- Registro 337/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0154', 3.0, 2, 8, 5, 5, 'Sustitución de contador en Villanañe', 'Sustitución de contador en Villanañe', '2025-09-15', '2025-09-15', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Villanañe', 5, 0, 1, 0);

-- Registro 338/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0155', 3.0, 2, 8, 5, 5, 'Sustitución de contador en Villanañe', 'Sustitución de contador en Villanañe', '2025-09-15', '2025-09-15', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Villanañe', 5, 0, 1, 0);

-- Registro 339/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0156', 3.0, 2, 8, 5, 5, 'Sustitución de contador en Antezana de la Ribera', 'Sustitución de contador en Antezana de la Ribera', '2025-09-12', '2025-09-12', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Antezana de la Ribera', 5, 0, 1, 0);

-- Registro 340/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0157', 3.0, 2, 8, 5, 5, 'Sustitución de contador en Villanañe', 'Sustitución de contador en Villanañe', '2025-09-15', '2025-09-15', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Villanañe', 5, 0, 1, 0);

-- Registro 341/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0271', 3.0, 1, 0, 5, 5, 'Fuga en Espejo', 'Fuga en Espejo', '2025-09-09', '2025-09-09', 42.807508, -3.048196, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Espejo', 5, 0, 1, 1);

-- Registro 342/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0272', 3.0, 1, 0, 1, 1, 'Fuga en Etxegoien', 'Fuga en Etxegoien', '2025-09-08', '2025-09-08', 43.043398, -3.021365, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Etxegoien', 1, 0, 1, 1);

-- Registro 343/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0273', 3.0, 1, 0, 1, 1, 'Fuga Larrimbe', 'Fuga Larrimbe', '2025-09-08', '2025-09-08', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Larrinbe', 1, 0, 1, 1);

-- Registro 344/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0274', 3.0, 1, 0, 1, 1, 'Fuga en Iperrega en Baranbio', 'Fuga en Iperrega en Baranbio', '2025-09-08', '2025-09-08', 43.051224, -2.922641, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Iperrega-Baranbio', 1, 0, 1, 1);

-- Registro 345/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0158', 5.0, 2, 3, 1, 2, 'Saneamiento en Artziniega', 'Saneamiento en Artziniega', '2025-09-09', '2025-09-09', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 2, 0, 1, 0);

-- Registro 346/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0275', 3.0, 1, 0, 1, 1, 'Fuga Quejana', 'Fuga Quejana', '2025-09-10', '2025-09-10', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Quejana', 1, 0, 1, 1);

-- Registro 347/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0276', 3.0, 1, 0, 5, 5, 'Fuga en Barrio', 'Fuga en Barrio', '2025-09-10', '2025-09-10', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Barrio', 5, 0, 1, 1);

-- Registro 348/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0277', 3.0, 1, 0, 9, 9, 'Fuga en Oreitia', 'Fuga en Oreitia', '2025-09-11', '2025-09-11', 42.857737, -2.55864, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Oreitia', 9, 0, 1, 1);

-- Registro 349/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0278', 3.0, 1, 0, 1, 1, 'Fuga en Respaldiza en Zerrabe Ausoa  n4', 'Fuga en Respaldiza en Zerrabe Ausoa n4', '2025-09-11', '2025-09-11', 43.106322, -3.045192, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Respaldiza', 1, 0, 1, 1);

-- Registro 350/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0159', 3.0, 2, 17, 1, 1, 'Limpieza de Red en Aresketamendi (Amurrio)', 'Limpieza de Red en Aresketamendi (Amurrio)', '2025-09-11', '2025-09-11', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 0);

-- Registro 351/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0279', 3.0, 1, 0, 1, 1, 'Aviso por fuga en montante en Avda.Zumalakarregui n36', 'Aviso por fuga en montante en Avda.Zumalakarregui 36', '2025-09-11', '2025-09-11', 43.143474, -2.962918, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 352/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0160', 1.0, 2, 2, 3, 3, 'Limpieza capataciones en Araia ( Agurain)', 'Limpieza capataciones', '2025-09-12', '2025-09-12', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Araia', 3, 0, 1, 0);

-- Registro 353/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0280', 3.0, 1, 0, 5, 5, 'Fuga en Berantevilla', 'Fuga en Berantevilla', '2025-09-12', '2025-09-12', 42.683407, -2.85915, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Berantevilla', 5, 0, 1, 1);

-- Registro 354/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0281', 3.0, 1, 0, 5, 5, 'Fuga en Zambrana', 'Fuga en Zambrana', '2025-09-13', '2025-09-13', 42.664059, -2.880294, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Zambrana', 5, 0, 1, 1);

-- Registro 355/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0282', 3.0, 1, 0, 1, 1, 'Fuga Erbi', 'Fuga Erbi', '2025-09-13', '2025-09-13', 43.07443, -3.112962, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Erbi-Ayala', 1, 0, 1, 1);

-- Registro 356/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0283', 5.0, 1, 0, 3, 26, 'Atasco en Agurain', 'Atasco en Agurain', '2025-09-13', '2025-09-13', 42.847745, -2.394902, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 26, 0, 1, 2);

-- Registro 357/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0284', 3.0, 1, 0, 1, 1, 'Abonado sin agua en C/Virgen del carmen n27', 'Abonado sin agua en C/Virgen del carmen n27', '2025-09-13', '2025-09-13', 43.145232, -2.959005, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 3);

-- Registro 358/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0285', 5.0, 1, 0, 1, 2, 'Atasco en Artziniega en Bajada Resbalon', 'Atasco en Artziniega en Bajada Resbalon', '2025-09-14', '2025-09-14', 43.121208, -3.130148, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 2, 0, 1, 2);

-- Registro 359/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0286', 3.0, 1, 0, 3, 3, 'Abonado sin agua en Agurain', 'Abonado sin agua en Agurain', '2025-09-14', '2025-09-14', 42.849447, -2.38856, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 0, 1, 3);

-- Registro 360/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0287', 3.0, 1, 0, 1, 1, 'Reparación de Fuga en C/Maskuribai', 'Reparación de Fuga en C/Maskuribai', '2025-09-16', '2025-09-26', 43.050845, -2.999945, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 1);

-- Registro 361/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0288', 3.0, 1, 0, 1, 1, 'Reparación de Fuga en Menoio', 'Reparación de Fuga en Menoio', '2025-09-16', '2025-09-16', 43.069093, -3.073315, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Menoio', 1, 0, 1, 1);

-- Registro 362/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0289', 5.0, 1, 0, 1, 3, 'Desatasco en Luiando C/Padura n7', 'Desatasco en Luiando C/Padura n7', '2025-09-16', '2025-09-16', 43.09314, -3.002363, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Luiando', 3, 0, 1, 2);

-- Registro 363/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0290', 5.0, 1, 0, 5, 41, 'Reparación saneamiento en Anucita', 'Reparación saneamiento en Anucita', '2025-09-16', '2025-09-17', 42.801546, -2.899364, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Anucita', 41, 0, 1, 3);

-- Registro 364/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0370', 5.0, 1, 0, 5, 41, 'Desatasco en fabrica de Ribabellosa', 'Desatasco en fabrica de Ribabellosa', '2025-09-15', '2025-09-16', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa', 41, 0, 1, 2);

-- Registro 365/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0161', 3.0, 2, 8, 3, 3, 'Instalación de contador en Agurain', 'Instalación de contador en Agurain', '2025-09-12', '2025-09-12', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 0, 1, 0);

-- Registro 366/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0162', 3.0, 2, 9, 1, 1, 'Retirada de contador en Amurrio', 'Retirada de contador en Amurrio', '2025-09-12', '2025-09-12', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 0);

-- Registro 367/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0163', 3.0, 2, 10, 3, 3, 'Sustitución de contador en Alegria', 'Sustitución de contador en Alegria', '2025-09-12', '2025-09-12', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 3, 0, 1, 0);

-- Registro 368/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0164', 3.0, 2, 8, 1, 1, 'Instalación contador en Anuntzibai N5 (Llodio)', 'Instalación contador en Anuntzibai N5 (Llodio)', '2025-09-15', '2025-09-15', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 369/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0165', 3.0, 2, 10, 5, 5, 'Sustitución de contadores en Ribabellosa', 'Sustitución de contador en Ribabellosa', '2025-09-11', '2025-09-11', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa', 5, 0, 1, 0);

-- Registro 370/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0166', 3.0, 2, 10, 5, 5, 'Sustitución de contador en Espejo C/Las arenas n8', 'Sustitución de contador en Espejo C/Las arenas n8', '2025-09-15', '2025-09-15', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Espejo', 5, 0, 1, 0);

-- Registro 371/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0167', 3.0, 2, 8, 3, 3, 'Instalación de contador en Agurain', 'Instalación de contador en Agurain', '2025-09-15', '2025-09-15', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 0, 1, 0);

-- Registro 372/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0168', 3.0, 2, 8, 1, 1, 'Instalación de contador en Llodio C/Plaza Ostagieta n7', 'Instalación de contador en Llodio C/Plaza Ostagieta n7', '2025-09-15', '2025-09-15', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 373/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0169', 3.0, 2, 10, 1, 1, 'Sustitución de contador en Menoio', 'Sustitución de contador en Menoio', '2025-09-15', '2025-09-15', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Menoio', 1, 0, 1, 0);

-- Registro 374/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0170', 3.0, 2, 8, 6, 6, 'Instalación de contador en Maestu C/Corres n2', 'Instalación de contador en Maestu C/Corres n2', '2025-09-15', '2025-09-15', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maeztu', 6, 0, 1, 0);

-- Registro 375/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0171', 3.0, 2, 10, 1, 1, 'Sustitución de contador en Respaldiza', 'Sustitución de contador en Respaldiza', '2025-09-15', '2025-09-15', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Respaldiza', 1, 0, 1, 0);

-- Registro 376/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0172', 3.0, 2, 10, 5, 5, 'Sustitución de contador en Villanañe', 'Sustitución de contador en Villanañe (varios contadores)', '2025-09-15', '2025-09-15', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Villanañe', 5, 0, 1, 0);

-- Registro 377/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0300', 3.0, 1, 0, 1, 1, 'Reparación de Fuga en Maroño', 'Reparación de Fuga en Maroño', '2025-09-17', '2025-09-17', 43.035575, -3.072336, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maroño', 1, 0, 1, 1);

-- Registro 378/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0301', 3.0, 1, 0, 1, 1, 'Reparación de Fuga en Esquina de Abajo/Respaldiza', 'Reparación de Fuga en Esquina de Abajo/Respaldiza', '2025-09-17', '2025-09-17', 43.087997, -3.044206, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Esquina Abajo/Respaldiza', 1, 0, 1, 1);

-- Registro 379/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0302', 3.0, 1, 0, 5, 5, 'Reparación de albañilería y catas por fuga Facsa (Salinas de Añana)', 'Reparación de albañilería y catas por fuga Facsa (Salinas de Añana)', '2025-09-17', '2025-09-17', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Salinas de Añana', 5, 0, 1, 1);

-- Registro 380/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0176', 3.0, 2, 18, 1, 1, 'Ejecución de nueva acometida Inausa (Amurrio)', 'Ejecución de nueva acometida INAUSA (Amurrio)', '2025-09-17', '2025-09-17', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 0);

-- Registro 381/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0304', NULL, 0, 0, 10, 10, 0, 0, '1900-01-01', '1900-01-01', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0, 10, 0, 1, 3);

-- Registro 382/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0173', 3.0, 2, 10, 3, 3, 'Sustitución de contadores en Opacua', 'Sustitución de contadores en Opacua', '2025-09-17', '2025-09-17', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Opacua', 3, 0, 1, 0);

-- Registro 383/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0174', 3.0, 2, 8, 1, 1, 'Instalación de contador en riego en Llodio', 'Instalación de contador en riego en Llodio', '2025-09-17', '2025-09-17', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 384/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0175', 5.0, 2, 3, 3, 26, 'Mantenimiento preventivo saneamiento en Agurain', 'Mangtenimiento preventivo saneamiento en Agurain', '2025-09-17', '2025-09-17', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 26, 0, 1, 0);

-- Registro 385/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0303', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Areta (Llodio)', 'Reparación de fuga en Areta (Llodio)', '2025-09-17', '2025-09-17', 43.146928, -2.943302, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 386/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0305', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Izoria', 'Reparación de fuga en Izoria', '2025-09-18', '2025-09-18', 43.145001, -2.959971, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 387/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0306', 3.0, 1, 0, 1, 1, 'Reparación de fuga en el Parque Lamuza (Llodio)', 'Reparación de fuga en el Parque Lamuza', '2025-09-18', '2025-09-18', 43.14498, -2.965023, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 388/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0307', 1.0, 1, 0, 1, 1, 'Reparar fuga VRP de Arbaiza', 'Reparar fuga VRP de Arbaiza', '2025-09-18', '2025-09-18', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 1);

-- Registro 389/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0308', 3.0, 1, 0, 3, 3, 'Reparación de fuga en Elburgo', 'Reparación de fuga en Elburgo', '2025-09-18', '2025-09-18', 42.850552, -2.538936, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Elburgo', 3, 0, 1, 1);

-- Registro 390/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0177', 5.0, 2, 3, 3, 26, 'Mantenimiento de saneamiento en Agurain', 'Mantenimiento de saneamiento en Agurain', '2025-09-18', '2025-09-18', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 26, 0, 1, 0);

-- Registro 391/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0178', 3.0, 2, 10, 3, 3, 'Sustitución contadores en Alegria', 'Sustitución contadores en Alegria', '2025-09-18', '2025-09-18', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 3, 0, 1, 0);

-- Registro 392/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0179', 3.0, 2, 12, 1, 1, 'Corte de Agua en Urumea n4 (Llodio)', 'Corte de Agua en Urumea n4 (Llodio)', '2025-09-12', '2025-09-12', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 393/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0309', 3.0, 1, 0, 1, 1, 'Aviso de Fuga en la estación de Amurrio', 'Aviso de Fuga en la estación de Amurrio', '2025-09-16', '2025-09-16', 43.049001, -3.002075, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 1);

-- Registro 394/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0310', 5.0, 1, 0, 1, 2, 'Desatasco en Artziniega', 'Desatasco en Artziniega', '2025-09-18', '2025-09-19', 43.121027, -3.129796, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 2, 0, 1, 2);

-- Registro 395/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0311', 3.0, 1, 0, 3, 3, 'Fuga en Elburgo', 'Fuga en Elburgo', '2025-09-08', '2025-09-08', 42.849178, -2.546024, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Elburgo', 3, 0, 1, 1);

-- Registro 396/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0312', 3.0, 1, 0, 1, 1, 'Reparacion de fuga en Larrimbe', 'Reparacion de fuga en Larrimbe', '2025-09-15', '2025-09-15', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Larrinbe', 1, 0, 1, 1);

-- Registro 397/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0313', 5.0, 1, 0, 5, 41, 'Desatasco en Anucita', 'Desatasco en Anucita', '2025-09-15', '2025-09-15', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Anucita', 41, 0, 1, 2);

-- Registro 398/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0314', 3.0, 1, 0, 1, 1, 'Fuga en Llodio', 'Fuga en Llodio', '2025-09-15', '2025-09-15', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 399/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0315', 1.0, 1, 0, 1, 1, 'Fuga de Iperrega (Amurrio)', 'Fuga de Iperrega', '2025-09-16', '2025-09-16', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Iperrega-Baranbio', 1, 0, 1, 1);

-- Registro 400/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0317', 5.0, 1, 0, 1, 3, 'Desatasco en Zuaza (Campa)', 'Desatasco en Zuaza (Campa)', '2025-09-18', '2025-09-18', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Zuaza', 3, 0, 1, 2);

-- Registro 401/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0318', 3.0, 1, 0, 3, 3, 'Reparacion de fuga en la calle Galburu (Alegria)', 'Reparacion de fuga en la calle Galburu (Alegria)', '2025-09-18', '2025-09-19', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 3, 0, 1, 1);

-- Registro 402/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0319', 1.0, 1, 0, 1, 1, 'Reparacion de fuga en Iperrega (Baranbio)', 'Reparacion de fuga en Iperrega (Baranbio)', '2025-09-18', '2025-09-19', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Iperrega-Baranbio', 1, 0, 1, 1);

-- Registro 403/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0180', 1.0, 2, 2, 1, 1, 'Limpieza de captaciones en Aiara', 'Limpieza de captaciones en Aiara', '2025-09-19', '2025-09-19', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Aiaraldea', 1, 0, 1, 0);

-- Registro 404/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0320', 3.0, 1, 0, 3, 3, 'Reparacion fuga acometida Agurain', 'Reparacion fuga acometida Agurain', '2025-09-19', '2025-09-25', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 0, 1, 1);

-- Registro 405/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0321', 3.0, 1, 0, 1, 1, 'Fuga en Erbi', 'Fuga en Erbi', '2025-09-20', '2025-09-20', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Erbi', 1, 0, 1, 1);

-- Registro 406/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0322', 3.0, 1, 0, 5, 5, 'Abonado sin agua en Estabillo', 'Abonado sin agua en Estabillo', '2025-09-20', '2025-09-20', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Estabillo', 5, 0, 1, 3);

-- Registro 407/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0323', 5.0, 1, 0, 3, 21, 'Atasco en Alegria C/Larrainza', 'Atasco en Alegria C/Larrainza', '2025-09-20', '2025-09-20', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 21, 0, 1, 2);

-- Registro 408/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0324', 5.0, 1, 0, 1, 2, 'Atasco en Artziniega (Calle Abajo)', 'Atasco en Artziniega (Calle Abajo)', '2025-09-20', '2025-09-20', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 2, 0, 1, 2);

-- Registro 409/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0325', 3.0, 1, 0, 1, 1, 'Fuga en Murga', 'Fuga en Murga', '2025-09-20', '2025-09-20', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Murga', 1, 0, 1, 1);

-- Registro 410/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0326', 3.0, 1, 0, 6, 6, 'Fuga en Quintana', 'Fuga en Quintana', '2025-09-21', '2025-09-21', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Quintana', 6, 0, 1, 1);

-- Registro 411/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0327', 5.0, 1, 0, 1, 1, 'Atasco en Goikolarra(Amurrio)', 'Atasco en Goikolarra(Amurrio)', '2025-09-21', '2025-09-21', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 2);

-- Registro 412/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0181', 3.0, 2, 8, 1, 1, 'Instalación de contadores Plaza de Abastos (Llodio)', 'Instalación de contadores Plaza de Abastos (Llodio)', '2025-09-12', '2025-09-12', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 413/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0328', 3.0, 1, 0, 1, 1, 'Reparaciones de Fuga en Ugarte (Llodio)', 'Reparaciones de Fuga en Ugarte (Llodio)', '2025-09-21', '2025-09-24', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 1);

-- Registro 414/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0329', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Pozoportillo', 'Reparación de fuga en Pozoportillo', '2025-09-19', '2025-09-19', 43.067357, -3.09801, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Pozoportillo-Ozeka', 1, 0, 1, 1);

-- Registro 415/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0182', 3.0, 2, 8, 1, 1, 'Instalación de contador en Luiando', 'Instalación de contador en Luiando', '2025-09-19', '2025-09-19', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Luiando', 1, 0, 1, 0);

-- Registro 416/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0330', 3.0, 1, 0, 1, 1, 'Aviso poca presión en Zuaza', 'Aviso poca presión en Zuaza (Panaderia)(esta en mal estado)', '2025-09-19', '2025-09-25', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Zuaza', 1, 0, 1, 3);

-- Registro 417/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0331', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Murga 41', 'Reparación de fuga en Murga 41', '2025-09-20', '2025-09-20', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Murga', 1, 0, 1, 1);

-- Registro 418/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0332', 5.0, 1, 0, 3, 21, 'Desatascar lineas de saneamiento en Alegria', 'Desatascar lineas de saneamiento en Alegria', '2025-09-20', '2025-09-20', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 21, 0, 1, 2);

-- Registro 419/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0183', 2.0, 2, 3, 6, 6, 'Mantenimiento de fosas sépticas en Antoñana', 'Mantenimiento de fosas sépticas en Antoñana', '2025-09-22', '2025-09-22', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Antoñana', 6, 0, 1, 0);

-- Registro 420/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0333', 3.0, 1, 0, 1, 1, 'Aviso por fuga en Aldai n38 (Amurrio)', 'Aviso por fuga en Aldai n38 (Amurrio)', '2025-09-22', '2025-09-22', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 1);

-- Registro 421/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0334', 5.0, 1, 0, 1, 2, 'Reparación colector saneamiento Artziniega', 'Reparación colector saneamiento Artziniega', '2025-09-23', '2025-09-23', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 2, 0, 1, 3);

-- Registro 422/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0335', 5.0, 1, 0, 1, 4, 'Localización de fugas y revisión de arquetas de pluviales y saneamiento en Atxeta', 'Localización de fugas y revisión de arquetas de pluviales y saneamiento en Atxeta', '2025-09-23', '2025-09-23', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 4, 0, 1, 1);

-- Registro 423/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0336', 5.0, 1, 0, 5, 41, 'Reparación y desatasco colector pluviales en Ribabellosa', 'Reparación y desatasco colector pluviales en Ribabellosa', '2025-09-23', '2025-09-26', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa', 41, 0, 1, 2);

-- Registro 424/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0337', 3.0, 1, 0, 1, 1, 'Reparación y sustitución valvulas acometida C/Jose Matia (Llodio)', 'Reparación y sustitución valvulas acometida C/Jose Matia (Llodio)', '2025-09-23', '1900-01-01', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 'Llodio', 1, 0, 1, 3);

-- Registro 425/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0184', 3.0, 2, 9, 5, 5, 'Retirada de contador en Anucita', 'Retirada de contador en Anucita', '2025-09-23', '2025-09-23', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Anucita', 5, 0, 1, 0);

-- Registro 426/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0185', 3.0, 2, 8, 6, 6, 'Instalación contador en Oteo', 'Instalación contador en Oteo', '2025-09-23', '2025-09-23', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Oteo', 6, 0, 1, 0);

-- Registro 427/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0338', 5.0, 1, 0, 1, 2, 'Reparación saneamiento Artziniega', 'Reparación saneamiento Artziniega', '2025-09-24', '1900-01-01', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 'Artziniega', 2, 0, 1, 3);

-- Registro 428/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0186', 3.0, 2, 8, 1, 1, 'Instalación contador C/Virgen del Carmen n35 (Llodio)', 'Instalación contador C/Virgen del Carmen n35 (Llodio)', '2025-09-01', '2025-09-01', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 429/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0339', 3.0, 1, 0, 1, 1, 'Restablecer sector centro norte (Llodio)', 'Restablecer sector centro norte (Llodio)', '2025-09-22', '2025-09-22', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 3);

-- Registro 430/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0340', 3.0, 1, 0, 1, 1, 'Restablecer sector Bañoleibar (Amurrio)', 'Restablecer sector Bañoleibar (Amurrio)', '2025-09-22', '2025-09-22', 43.048882, -2.995148, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 3);

-- Registro 431/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0187', 3.0, 2, 13, 1, 1, 'Asistencia a Urbide y Ayto Llodio obra Lamuza', 'Asistencia a Urbide y Ayto Llodio obra Lamuza', '2025-09-23', '2025-09-23', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 432/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0188', 5.0, 2, 1, 3, 21, 'Mantenimiento preventivo saneamiento Alegría', 'Mantenimiento preventivo saneamiento Alegría', '2025-09-24', '2025-09-24', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 21, 0, 1, 0);

-- Registro 433/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0189', 3.0, 2, 13, 1, 1, 'Asistencia Técnica a Obra de Maroño', 'Asistencia Técnica a Obra de Maroño', '2025-09-22', '2025-09-22', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maroño', 1, 0, 1, 0);

-- Registro 434/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0341', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Zuaza', 'Reparación de fuga en Zuaza', '2025-09-24', '2025-09-24', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Zuaza', 1, 0, 1, 1);

-- Registro 435/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0342', 5.0, 1, 0, 1, 3, 'Desatasco de saneamiento en Luiando', 'Desatasco de saneamiento en Luiando', '2025-09-26', '2025-09-26', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Luiando', 3, 0, 1, 2);

-- Registro 436/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0190', 3.0, 2, 8, 1, 1, 'Instalación contador en Anuncibai (Llodio)', 'Instalación contador en Anuncibai (Llodio)', '2025-09-24', '2025-09-24', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 0);

-- Registro 437/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0191', 3.0, 2, 10, 1, 1, 'Sustitución de contadores en C/Avenida Gernica n6 (Artziniega)', 'Sustitución de contadores en C/Avenida Gernica n6 (Artziniega)', '2025-09-24', '2025-09-24', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 0, 1, 0);

-- Registro 438/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0192', 3.0, 2, 12, 1, 1, 'Corte de agua.Colocación avisos en C/Zabaleko n8 (Amurrio)', 'Corte de agua.Colocación avisos en C/Zabaleko n8 (Amurrio)', '2025-09-24', '2025-09-24', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 0);

-- Registro 439/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0193', 3.0, 2, 8, 6, 6, 'Instalación contadores Oteo', 'Instalación contadores Oteo', '2025-09-23', '2025-09-23', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Oteo', 6, 0, 1, 0);

-- Registro 440/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0194', 3.0, 2, 7, 3, 3, 'Localización de fugas en Agurain', 'Localización de fugas en Agurain', '2025-09-23', '2025-09-23', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 0, 1, 1);

-- Registro 441/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0343', 5.0, 1, 0, 3, 26, 'Revisión de saneamiento por filtraciones en garajes en Agurain', 'Revisión de saneamiento por filtraciones en garajes en Agurain', '2025-09-25', '2025-09-25', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 26, 0, 1, 1);

-- Registro 442/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0195', 5.0, 2, 1, 3, 26, 'Localización de redes saneamiento en Agurain', 'Localización de redes saneamiento en Agurain', '2025-09-15', '2025-09-18', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 26, 0, 1, 0);

-- Registro 443/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0196', 5.0, 2, 1, 5, 41, 'Revisión de red saneamiento Ribabellosa', 'Revisión de red saneamiento Ribabellosa', '2025-09-16', '2025-09-16', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa', 41, 0, 1, 0);

-- Registro 444/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0344', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Murga', 'Reparación de fuga en Murga', '2025-09-19', '2025-09-22', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Murga', 1, 0, 1, 1);

-- Registro 445/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0345', 5.0, 1, 0, 6, 48, 'Reparación de entrada a la fosa de Antoñana', 'Reparación de entrada a la fosa de Antoñana', '2025-09-22', '2025-09-25', 42.694143, -2.397965, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Antoñana', 48, 0, 1, 3);

-- Registro 446/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0197', 3.0, 2, 10, 5, 5, 'Sustitución de contador en C/ molino en Berantevilla', 'Insatalación de contador en Berantevilla', '2025-09-25', '2025-09-25', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Berantevilla', 5, 0, 1, 0);

-- Registro 447/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0346', 3.0, 1, 0, 5, 5, 'Reparación de fuga en Espejo', 'Reparación de fuga en Espejo', '2025-09-25', '2025-09-26', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Espejo', 5, 0, 1, 1);

-- Registro 448/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0347', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Erbi', 'Reparación de fuga en Erbi', '2025-09-22', '2025-09-25', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Erbi', 1, 0, 1, 1);

-- Registro 449/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0198', 5.0, 2, 1, 3, 21, 'Limpieza de colector de pluviales en Alegría', 'Limpieza de colector de pluviales en Alegría', '2025-09-25', '2025-09-25', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 21, 0, 1, 0);

-- Registro 450/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0199', 3.0, 2, 10, 5, 5, 'Sustitución de contador en C/Rio Ayuda n47 en Berantevilla', 'Sustitución de contador en C/Rio Ayuda n47 en Berantevilla', '2025-09-25', '2025-09-25', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Berantevilla', 5, 0, 1, 0);

-- Registro 451/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0200', 3.0, 2, 10, 5, 5, 'Sustitución de contador en C/La Venta n2 en Ribabellosa', 'Sustitución de contador en C/La Venta n2 en Ribabellosa', '2025-09-25', '2025-09-25', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa', 5, 0, 1, 0);

-- Registro 452/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0201', 3.0, 2, 7, 3, 3, 'Localización de fugas en abastecimiento en Agurain', 'Localización de fugas en abastecimiento en Agurain', '2025-09-25', '2025-09-25', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 0, 1, 1);

-- Registro 453/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0202', 3.0, 2, 7, 3, 3, 'Localización de fugas en Agurain', 'Localización de fugas en Agurain', '2025-09-24', '2025-09-24', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 0, 1, 1);

-- Registro 454/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0203', 3.0, 2, 7, 5, 5, 'Localización de fugas en abastecimiento en Arbígano', 'Localización de fugas en abastecimiento en Arbígano', '2025-09-23', '2025-09-23', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Arbígano', 5, 0, 1, 1);

-- Registro 455/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0204', 5.0, 2, 3, 1, 1, 'Aporte de pluviales al saneamiento en Onsoño', 'Aporte de pluviales al saneamiento en Onsoño', '2025-09-22', '2025-09-22', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Onsoño', 1, 0, 1, 0);

-- Registro 456/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0205', 3.0, 2, 7, 1, 1, 'Fuga en ramal Campijo-Santa Coloma', 'Fuga en ramal Campijo-Santa Coloma', '2025-09-22', '2025-09-22', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Santa Coloma', 1, 0, 1, 1);

-- Registro 457/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0206', 3.0, 2, 7, 1, 1, 'Humedades santuario de la Encina', 'Humedades santuario de La Encina', '2025-09-22', '2025-09-22', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'La Encina', 1, 0, 1, 0);

-- Registro 458/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0207', 3.0, 2, 7, 1, 1, 'Localización de fugas C/Zerralde n3 en Respaldiza', 'Localización de fugas C/Zerralde n3 en Respaldiza', '2025-09-19', '2025-09-19', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Respaldiza', 1, 0, 1, 1);

-- Registro 459/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0208', 1.0, 2, 7, 1, 1, 'Revisión en busca de fugas en la red de aducción en Atziniega', 'Revisión en busca de fugas en la red de aducción en Atziniega', '2025-09-18', '2025-09-18', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 0, 1, 1);

-- Registro 460/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0209', 3.0, 2, 7, 1, 1, 'Localización de fugas en Luiando debido a consumo elevado', 'Localización de fugas en Luiando debido a consumo elevado', '2025-09-16', '2025-09-16', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Luiando', 1, 0, 1, 1);

-- Registro 461/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0210', 5.0, 2, 1, 5, 41, 'Atasco en C/Venta el Bullon en Ribabellosa', 'Atasco en C/Venta el Bullon en Ribabellosa', '2025-09-15', '2025-09-15', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa', 41, 0, 1, 2);

-- Registro 462/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0211', 3.0, 2, 7, 4, 4, 'Localización de fugas en Elosu', 'Localización de fugas en Elosu', '2025-09-15', '2025-09-15', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Elosu', 4, 0, 1, 1);

-- Registro 463/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0212', 5.0, 2, 1, 3, 26, 'Revisión de zonas del saneamiento de Agurain', 'Revisión de zonas del saneamiento de Agurain', '2025-09-12', '2025-09-12', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 26, 0, 1, 0);

-- Registro 464/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0213', 3.0, 2, 7, 1, 1, 'Localización de fugas en Luiaondo', 'Localización fugas en Luiaondo por consumo elevado', '2025-09-12', '2025-09-12', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Luiando', 1, 0, 1, 1);

-- Registro 465/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0214', 3.0, 2, 7, 5, 5, 'Localización fuga en Berantevilla', 'Localización fuga en Berantevilla', '2025-09-11', '2025-09-11', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Berantevilla', 5, 0, 1, 1);

-- Registro 466/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0215', 5.0, 2, 21, 1, 1, 'Ejecución de informes de Fosas Septicas (OFICINA)', 'Ejecución de informes de Fosas Septicas (OFICINA)', '2025-09-11', '2025-09-11', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 0);

-- Registro 467/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('GF/0003', 4.0, 3, 0, 10, 10, 'Gastos fijos de explotación totales', 'Gastos fijos de explotación totales', '2025-09-01', '2025-09-30', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0, 10, 0, 1, 0);

-- Registro 468/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('GF/0004', 4.0, 3, 0, 10, 10, 'Gestión documental del contrato', 'Gestión documental del contrato', '2025-09-01', '2025-09-30', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0, 10, 'ELENA', 1, 0);

-- Registro 469/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0216', 5.0, 2, 5, 1, 1, 'Digitalización de redes abastecimiento y saneamiento', 'Ribabellosa, Agurain,Maeztu', '2025-09-01', '2025-09-30', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'JORGE', 1, 0);

-- Registro 470/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0217', 3.0, 2, 8, 1, 1, 'Instalación de contador en Artziniega C/Jauregia n6', 'Instalación de contador en Artziniega C/Jauregia n6', '2025-09-26', '2025-09-26', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 'KERMAN', 1, 0);

-- Registro 471/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0218', 3.0, 2, 8, 1, 1, 'Instalación de contador en Artziniega C/Ureta n1', 'Instalación de contador en Artziniega C/Ureta n1', '2025-09-26', '2025-09-26', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 'KERMAN', 1, 0);

-- Registro 472/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0349', 3.0, 1, 0, 3, 3, 'Asfaltado en cata Facsa en Gazeta', 'Asfaltado en cata Facsa en Gazeta', '2025-09-26', '2025-09-26', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Gazeta', 3, 'MIGUEL y ZOUITA', 1, 3);

-- Registro 473/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0350', 3.0, 1, 0, 1, 1, 'Reparación de fuga en C/Aldai n38', 'Reparación de fuga en Aldai', '2025-09-26', '2025-09-26', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'KERMAN', 1, 1);

-- Registro 474/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0351', 5.0, 1, 0, 1, 1, 'Atasco de saneamiento en Larrabe', 'Atasco de saneamiento en Larrabe', '2025-09-23', '2025-09-23', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'KERMAN y EMILIO', 1, 2);

-- Registro 475/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0352', 3.0, 1, 0, 1, 1, 'Reparación fuga Erbi', 'Reparación fuga Erbi', '2025-09-25', '2025-09-26', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Erbi', 1, 'KERMAN y EMILIO', 1, 1);

-- Registro 476/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0353', 5.0, 1, 0, 1, 1, 'Atasco en Delika', 'Atasco en Delika', '2025-09-26', '2025-09-26', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Delika', 1, 'MIGUEL', 1, 2);

-- Registro 477/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0219', 1.0, 2, 2, 1, 1, 'Limpieza Captaciones', 'Limpieza Captaciones', '2025-09-26', '2025-09-26', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Aiaraldea', 1, 0, 1, 0);

-- Registro 478/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0354', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Llanteno', 'Reparación de fuga en Llanteno', '2025-09-26', '2025-09-26', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llanteno', 1, 0, 1, 1);

-- Registro 479/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0355', 5.0, 1, 0, 5, 41, 'Desatasco en Ribabellosa en C/Manuel de Etxanobe', 'Desatasco en Ribabellosa en C/Manuel de Etxanobe', '2025-09-27', '2025-09-27', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa', 41, 0, 1, 2);

-- Registro 480/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0356', 3.0, 1, 0, 1, 1, 'Abonado sin agua ( Las Vegas )', 'Suciedad en contador', '2025-09-27', '2025-09-27', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Luiando', 1, 0, 1, 2);

-- Registro 481/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0357', 3.0, 1, 0, 1, 1, 'Aviso de fuga en C/Calle Arriba', 'Aviso de fuga en C/Calle Arriba', '2025-09-27', '2025-09-27', 43.120756, -3.128523, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 0, 1, 1);

-- Registro 482/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0358', 5.0, 1, 0, 5, 41, 'Atasco saneamiento Pobes', 'Atasco saneamiento Pobes', '2025-09-27', '2025-09-27', 42.800682, -2.910926, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Pobes', 41, 0, 1, 2);

-- Registro 483/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0359', 3.0, 1, 0, 1, 1, 'Corte de agua en C/Ruperto Urquijo n14 (URGENCIA)', 'Corte de agua en C/Ruperto Urquijo n14 (URGENCIA)', '2025-09-27', '2025-09-27', 43.1462093, -2.9629, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 0, 1, 3);

-- Registro 484/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0360', 3.0, 1, 0, 1, 1, 'Aviso de fuga en Barrataguren Artziniega', 'Aviso de fuga en Barrataguren Artziniega', '2025-09-28', '2025-09-28', 43.139591, -3.109249, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 0, 1, 1);

-- Registro 485/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0220', 3.0, 2, 7, 1, 1, 'Localización de fugas en Isasi (Llodio)', 'Localización de fugas en Isasi (Llodio)', '2025-09-26', '2025-09-26', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'ENEKO', 1, 1);

-- Registro 486/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0361', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Barrataguren y Clariant (Artziniega)', 'Reparación de fuga en Barrataguren y Clariant (Artziniega)', '2025-09-29', '2025-09-29', 43.139591, -3.109249, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 'MIGUEL', 1, 1);

-- Registro 487/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0221', 5.0, 2, 1, 3, 21, 'Limpieza preventiva en saneamiento en Alegría', 'Limpieza preventiva en saneamiento en Alegría', '2025-09-29', '2025-09-29', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 21, 'EMILIO Y MIGUEL', 1, 0);

-- Registro 488/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0362', 3.0, 1, 0, 1, 1, 'Comprobación de válvulas de acometida en C/Ruperto Urquijo n14 (Llodio)', 'Comprobación de válvulas de acometida en C/Ruperto Urquijo n14 (Llodio)', '2025-09-26', '2025-09-26', 43.15241, -2.973001, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 3);

-- Registro 489/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0363', 3.0, 1, 0, 1, 1, 'Cerramos acometida  C/Ruperto Urquijo n14 (Llodio)', 'Cerramos acometida a petición de los vecinos C/Ruperto Urquijo n14 (Llodio)', '2025-09-28', '2025-09-28', 43.1462093, -2.963372, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 3);

-- Registro 490/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0364', 3.0, 1, 0, 1, 1, 'Revisión de acometida en C/Batzalarrin n8 (Llodio)', 'Revisión de acometida en C/Batzalarrin n8 (Llodio)', '2025-09-29', '2025-09-29', 43.142287, -2.9629, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 3);

-- Registro 491/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0365', 3.0, 1, 0, 1, 1, 'Aviso de fuga en Isasi n20 (Llodio)', 'Aviso de fuga en Isasi n20 (Llodio)', '2025-09-29', '2025-09-29', 43.151171, -2.97138, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 1);

-- Registro 492/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0366', 3.0, 1, 0, 1, 1, 'Colocación de avisos de corte de agua C/Urumea n4-5', 'Colocación de avisos de corte de agua C/Urumea n4-5', '2025-09-26', '2025-09-26', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 3);

-- Registro 493/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0222', 3.0, 2, 13, 1, 1, 'Asistencia a aperajador municipal en C/Lateorro (colegio en Llodio)', 'Asistencia a aperajador municipal en C/Lateorro (colegio en Llodio)', '2025-09-29', '2025-09-29', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 0);

-- Registro 494/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0223', 3.0, 2, 11, 1, 1, 'Toma de lectura de contadores sectoriales en Llodio', 'Toma de lectura de contadores sectoriales en Llodio', '2025-09-29', '2025-09-29', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 0);

-- Registro 495/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0224', 3.0, 2, 7, 1, 1, 'Localización de fugas en (sector Areta) (Llodio)', 'Localización de fugas en (sector Areta) (Llodio)', '2025-09-30', '2025-09-30', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 1);

-- Registro 496/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0225', 3.0, 2, 7, 1, 1, 'Localización de fugas en (Sector centro Norte)', 'Localización de fugas en (Sector centro Norte) (Ambulatorio)', '2025-09-30', '2025-09-30', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 1);

-- Registro 497/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0226', 3.0, 2, 11, 3, 3, 'Lectura de contadores Sectoriales en Agurain y Alegría', 'Lectura de contadores Sectoriales en Agurain y Alegría', '2025-09-30', '2025-09-30', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 'EDUARDO Y ENEKO', 1, 0);

-- Registro 498/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0227', 3.0, 2, 8, 1, 1, 'Intalacion de contador por alta en C/Mendiko n2 (Amurrio)', 'Intalacion de contador por alta en C/Mendiko n2', '2025-09-24', '2025-09-24', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'TOMAS', 1, 0);

-- Registro 499/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0228', 3.0, 2, 7, 1, 1, 'Localización de fugas en C/Atxeta n2 (Llodio)', 'Localización de fugas en C/Atxeta n2 (Llodio)', '2025-09-26', '2025-09-26', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 1);

-- Registro 500/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0229', 3.0, 2, 10, 6, 6, 'Sustitución contador en Carretera vitoria Estella en Maeztu', 'Sustitución contador en Carretera vitoria Estella en Maeztu', '2025-09-30', '2025-09-30', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maeztu', 6, 'IÑIGO', 1, 0);

-- Registro 501/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0230', 3.0, 2, 10, 6, 6, 'Sustitución contador en Apellaniz', 'Sustitución contador en Apellaniz', '2025-09-30', '2025-09-30', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Apellaniz', 6, 'IÑIGO', 1, 0);

-- Registro 502/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0367', 3.0, 1, 0, 5, 5, 'Reparación de fuga en Basquiñuelas (Añana)', 'Reparación de fuga en Basquiñuelas (Añana)', '2025-09-30', '2025-10-02', 42.80785, -2.973698, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Basquiñuelas', 5, 'MIGUEL Y JOSEBA', 1, 1);

-- Registro 503/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0368', 5.0, 1, 0, 1, 4, 'Aviso atasco saneamiento colector Landaluze (Llodio)', 'Aviso atasco saneamiento colector Landaluze (Llodio)', '2025-10-01', '2025-10-01', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 4, 'EMILIO', 1, 2);

-- Registro 504/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0231', 5.0, 2, 1, 3, 26, 'Mantenimiento preventivo saneamiento Agurain', 'Mantenimiento preventivo saneamiento Agurain', '2025-10-01', '2025-10-01', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 26, 'EMILIO,ANGEL,KERMAN', 1, 0);

-- Registro 505/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0232', 3.0, 2, 11, 1, 1, 'Lectura de contadores sectoriales en Respaldiza', 'Lectura de contadores sectoriales en Respaldiza', '2025-10-01', '2025-10-01', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Respaldiza', 1, 'KERMAN', 1, 0);

-- Registro 506/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0233', 3.0, 2, 11, 1, 1, 'Lectura de contadores sectoriales en Delika,Sojo', 'Lectura de contadores sectoriales en Delika,Sojo', '2025-09-29', '2025-09-29', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'KERMAN', 1, 0);

-- Registro 507/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0234', 3.0, 2, 8, 3, 3, 'Instalación contador en Agurain', 'Instalación contador en Agurain', '2025-10-01', '2025-10-01', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 'KERMAN', 1, 0);

-- Registro 508/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0369', 3.0, 1, 0, 6, 6, 'Aviso de fugas en Antoñana y Gauna', 'Aviso de fugas en Antoñana y Gauna', '2025-10-01', '2025-10-01', 0.0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Antoñana', 6, 'BEÑAT', 1, 1);

-- Registro 509/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0371', 3.0, 1, 0, 1, 1, 'Desatasco en San Roque Amurrio', 'Desatasco en San Roque Amurrio', '2025-09-30', '2025-09-30', 43.069723, -2.988658, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 0, 1, 2);

-- Registro 510/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0235', 3.0, 2, 12, 1, 1, 'Colocación de avisos de corte de agua en Berganza', 'Colocación de avisos de corte de agua en Berganza', '2025-10-03', '2025-10-03', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Berganza', 1, 'IÑIGO', 1, 0);

-- Registro 511/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0236', 3.0, 2, 11, 3, 3, 'Lectura contadores sectoriales en Cuencas Mediterraneas', 'Lectura contadores sectoriales en Cuencas Mediterraneas', '2025-09-29', '2025-09-29', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Cuencas Mediterraneas', 3, 'ENEKO', 1, 0);

-- Registro 512/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0237', 3.0, 2, 10, 3, 3, 'Sustitución contadores en Apellaniz ,Alegría,Alda,Ulibarri', 'Sustitución contadores en Apellaniz ,Alegría,Alda,Ulibarri', '2025-09-30', '2025-09-30', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 3, 'IÑIGO', 1, 0);

-- Registro 513/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0238', 3.0, 2, 7, 1, 1, 'Recoger y leer equipos de fugas en el sector Isasi de Laudio', 'Recoger y leer equipos de fugas en el sector Isasi de Laudio', '2025-09-30', '2025-09-30', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'ENEKO', 1, 1);

-- Registro 514/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0239', 3.0, 2, 11, 3, 3, 'Lectura de contadores en cuencas de Mediterranea y Cantábricas', 'Lectura de contadores en cuencas de Mediterranea y Cantábricas', '2025-09-30', '2025-09-30', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Cuencas Mediterraneas', 3, 'ENEKO', 1, 0);

-- Registro 515/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0240', 3.0, 2, 11, 3, 3, 'Lectura de contadores en cuencas de Mediterranea', 'Lectura de contadores en cuencas de Mediterranea', '2025-10-01', '2025-10-01', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Cuencas Mediterraneas', 3, 'ENEKO', 1, 0);

-- Registro 516/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0241', 3.0, 2, 7, 3, 3, 'Localización de fugas en Agurain', 'Localización de fugas en Agurain', '2025-10-01', '2025-10-01', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 'ENEKO', 1, 1);

-- Registro 517/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0242', 3.0, 2, 7, 1, 1, 'Localización de fuga en sactor de Isasi Laudio', 'Localización de fuga en sector de Isasi Laudio', '2025-10-02', '2025-10-02', 43.15207, -2.972544, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'ENEKO', 1, 1);

-- Registro 518/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0243', 3.0, 2, 11, 3, 3, 'Lectura contadores sectoriales en Cuencas Mediterraneas', 'Lectura contadores sectoriales en Cuencas Mediterraneas', '2025-10-02', '2025-10-02', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Cuencas Mediterraneas', 3, 'ENEKO', 1, 0);

-- Registro 519/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0372', 5.0, 1, 0, 1, 1, 'Desatasco saneamiento en C/Jose Madinabeitia (Amurrio)', 'Desatasco saneamiento en C/Jose Madinabeitia (Amurrio)', '2025-09-29', '2025-09-29', 43.053076, -3.002347, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, NULL, 1, 2);

-- Registro 520/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0373', 5.0, 1, 0, 6, 6, 'Desatasco saneamiento Maeztu C/Tellazar', 'Desatasco saneamiento Maeztu C/Tellazar', '2025-10-02', '2025-10-02', 42.73839, -2.448526, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maeztu', 6, NULL, 1, 2);

-- Registro 521/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0244', 3.0, 2, 12, 1, 1, 'Corte de agua en Amurrio C/Frontón n4', 'Corte de agua en Amurrio  C/Frontón n4', '2025-10-02', '2025-10-02', 43.052953, -3.000685, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, NULL, 1, 0);

-- Registro 522/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0374', 3.0, 1, 0, 1, 1, 'Aviso falta de presión en la calle Otazu n2 (Luiando)', 'Aviso falta de presión en la calle Otazu n2 (Luiando)', '2025-10-02', '2025-10-02', 43.10736, -2.99594, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Luiando', 1, NULL, 1, 3);

-- Registro 523/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0375', 3.0, 1, 0, 6, 6, 'Fuga en Antoñana', 'Fuga en Antoñana', '2025-10-02', '2025-10-03', 42.695859, -2.397406, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Antoñana', 6, NULL, 1, 1);

-- Registro 524/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0245', 1.0, 2, 2, 1, 1, 'Limpieza de captaciones Agiel,Txintxetru,Lejarzo', 'Limpieza de captaciones Agiel,Txintxetru,Lejarzo', '2025-10-03', '2025-10-03', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maroño', 1, NULL, 1, 0);

-- Registro 525/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0246', 3.0, 2, 1, 1, 1, 'Mantenimiento preventivo saneamiento Llodio', 'Mantenimiento preventivo saneamiento Llodio', '2025-10-03', '2025-10-03', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, NULL, 1, 0);

-- Registro 526/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0376', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Erbi', 'Reparación de fuga en Erbi', '2025-10-03', '2025-10-04', 43.072038, -3.116147, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Erbi', 1, NULL, 1, 1);

-- Registro 527/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0377', 3.0, 1, 0, 3, 3, 'Fuga en vías del tren de Edar en Alegría', 'Fuga en vías del tren de Edar en Alegría', '2025-10-02', '2025-10-29', 42.848764, -2.513726, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 3, NULL, 1, 1);

-- Registro 528/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0378', 5.0, 1, 0, 1, 1, 'Desatasco en Murga en la campa', 'Desatasco en Murga en la campa', '2025-10-04', '2025-10-04', 43.079735, -3.02196, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Murga', 1, NULL, 1, 2);

-- Registro 529/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0379', 3.0, 1, 0, 1, 1, 'Fuga en Artziniega en Barrataguren', 'Fuga en Artziniega en Barrataguren', '2025-10-03', '2025-10-04', 43.138242, -3.112732, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, NULL, 1, 1);

-- Registro 530/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0380', 3.0, 1, 0, 5, 5, 'Fuga en Espejo C/La Iglesia n11', 'Fuga en Espejo C/La Iglesia n11', '2025-10-06', '2025-10-07', 42.808606, -3.049674, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Espejo', 5, NULL, 1, 1);

-- Registro 531/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0247', 3.0, 2, 7, 1, 1, 'Localizacion de fugas en Llodio', 'Localizacion de fugas en Llodio', '2025-09-30', '2025-09-30', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, NULL, 1, 1);

-- Registro 532/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0381', 3.0, 1, 0, 1, 1, 'Fuga en Larrinbe', 'Fuga en Larrinbe', '2025-10-06', '2025-10-07', 43.038108, -2.978011, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Larrinbe', 1, NULL, 1, 1);

-- Registro 533/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0382', 3.0, 1, 0, 3, 3, 'Reparación de fuga en Agurain C/Zadorra n33', 'Reparación de fuga en Agurain C/Zadorra n33', '2025-10-03', '2025-10-08', 42.854613, -2.390445, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 'JOSEBA E IÑIGO', 1, 1);

-- Registro 534/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0248', 3.0, 2, 9, 3, 3, 'Desistalación de contador en Agurain C/Entzia n7', 'Desistalación de contador en Agurain C/Entzia n7', '2025-10-02', '2025-10-02', 42.848011, -2.391488, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 'KERMAN', 1, 0);

-- Registro 535/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0249', 5.0, 2, 1, 3, 3, 'Desatasco en parque de C/Urzabal en Agurain', 'Desatasco en parque de C/Urzabal en Agurain', '2025-10-02', '2025-10-03', 42.848472, -2.390702, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 'EMILIO', 1, 2);

-- Registro 536/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0250', 3.0, 2, 9, 6, 6, 'Retirada de contador C/Mayor n B (kontrasta)', 'Retirada de contador C/Mayor n B (kontrasta)', '2025-10-02', '2025-10-02', 42.771027, -2.295877, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Kontrasta', 6, 'KERMAN', 1, 0);

-- Registro 537/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0251', 3.0, 2, 10, 3, 3, 'Cambio de contador en Añua Bidea n11 en Alegria', 'Cambio de contador en Añua Bidea n11 en Alegria', '2025-10-02', '2025-10-02', 42.839629, -2.514056, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 3, 'KERMAN', 1, 0);

-- Registro 538/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0252', 5.0, 2, 1, 3, 3, 'Mantenimiento preventivo saneamiento C/Urzabal en Agurain', 'Mantenimiento preventivo saneamiento C/Urzabal en Agurain', '2025-10-06', '2025-10-06', 42.848553, -2.39076, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 'EMILIO', 1, 0);

-- Registro 539/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0383', 3.0, 1, 0, 1, 1, 'Conexión nueva tubería y VRP (Bergantza)', 'Conexión nueva tubería y VRP (Bergantza)', '2025-10-02', '2025-10-08', 43.057099, -2.932138, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Berganza', 1, 'MIGUEL Y ANGEL', 1, 3);

-- Registro 540/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0384', 3.0, 1, 0, 3, 3, 'Fuga en acometida en Alegria C/Ursuleta n2', 'Fuga en acometida en Alegria C/Ursuleta n2', '2025-10-01', '2025-10-02', 42.84412, -2.512686, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 3, 'JOSEBA Y RAFHIR', 1, 1);

-- Registro 541/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0385', 3.0, 1, 0, 1, 1, 'Aviso de fuga en Zubiaur n3 (Llodio)', 'Aviso de fuga en Zubiaur n3 (Llodio)', '2025-10-01', '2025-10-01', 43.140611, -2.963704, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 1);

-- Registro 542/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0386', 3.0, 1, 0, 3, 3, 'Atendemos llamada de falta de agua en Agurain C/Mayor n24', 'Atendemos llamada de falta de agua en Agurain C/Mayor n24', '2025-10-02', '2025-10-02', 42.851, -2.38913, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 'EDUARDO Y BEÑAT', 1, 3);

-- Registro 543/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0387', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Atxarte n8 (Llodio)', 'Reparación de fuga en Atxarte n8 (Llodio)', '2025-10-02', '2025-10-09', 43.148282, -2.946378, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS,IÑIGO,BEÑAT,JAGOBA,ZOVITA,MIGUEL,EMILO,ANGEL', 1, 1);

-- Registro 544/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0252', 3.0, 2, 8, 1, 1, 'Instalación de contador en C/Batzalarrim n8 (Llodio)', 'Instalación de contador en C/Batzalarrim n8 (Llodio)', '2025-10-02', '2025-10-02', 43.14236, -2.963007, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 0);

-- Registro 545/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0253', 3.0, 2, 7, 1, 1, 'Localización de toma pirata en C/Zumalakarregui n50 (Llodio)', 'Localización de toma pirata en C/Zumalakarregui n50 (Llodio)', '2025-10-02', '2025-10-02', 43.141631, -2.964516, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 0);

-- Registro 546/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0254', 3.0, 2, 13, 3, 3, 'Toma de datos para obras y servicios Alegría', 'Toma de datos para obras y servicios Alegría', '2025-10-03', '2025-10-16', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 3, 'ENEKO', 1, 0);

-- Registro 547/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0388', 5.0, 1, 0, 1, 1, 'Atasco en Llanteno en Barrio Petiz', 'Atasco en Llanteno en Barrio Petiz', '2025-10-05', '2025-10-05', 43.109146, -3.097283, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llanteno', 1, 'V', 1, 2);

-- Registro 548/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0255', 3.0, 2, 17, 1, 1, 'Limpieza en red Artziniega', 'Limpieza en red Artziniega', '2025-10-05', '2025-10-05', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 'V', 1, 0);

-- Registro 549/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0256', 3.0, 2, 12, 1, 1, 'Corte de Agua Luiando  (Las Vegas)', 'Corte de Agua Luyando (Las Vegas)', '2025-10-05', '2025-10-05', 43.105146, -2.996815, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Luiando', 1, 'V', 1, 0);

-- Registro 550/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0257', 3.0, 2, 17, 1, 1, 'Limpieza de red Luiando', 'Limpieza de red Luiando', '2025-10-05', '2025-10-05', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Luiando', 1, 'V', 1, 0);

-- Registro 551/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0389', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Arraño (Llodio)', 'Reparación de fuga en Arraño (Llodio)', '2025-10-07', '2025-10-07', 43.147442, -2.975663, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'MIGUEL Y ANGEL', 1, 1);

-- Registro 552/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0390', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Isasi n32 (Llodio)', 'Reparación de fuga en Isasi n32 (Llodio)', '2025-10-06', '2025-10-08', 43.151945, -2.972527, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS,IÑIGO,JAGOBA,MIGUEL,EMILIO,ZOVITA,RAFNIR', 1, 1);

-- Registro 553/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0391', 5.0, 1, 0, 5, 5, 'Desatasco saneamiento en C/Solana en Zambrana', 'Desatasco saneamiento en C/Solana en Zambrana', '2025-10-07', '2025-10-07', 42.660472, -2.878625, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Zambrana', 5, 'EDU,EMILIO,KERMAN', 1, 2);

-- Registro 554/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0392', 3.0, 1, 0, 1, 1, 'Aviso por fuga en Larrazabal n2 (Llodio)', 'Aviso por fuga en Larrazabal n2 (Llodio)', '2025-10-07', '2025-10-07', 43.1408357, -2.9791306, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS E IÑIGO', 1, 1);

-- Registro 555/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0258', 5.0, 2, 1, 1, 1, 'Mantenimiento preventivo en Plaza Estación (Alegría)', 'Mantenimiento preventivo en Plaza Estación (Alegría)', '2025-10-07', '2025-10-07', 42.848794, -2.514262, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'EMILIO Y KERMAN', 1, 0);

-- Registro 556/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0259', 2.0, 2, 7, 3, 3, 'Revisión de fosas septicas cuencas mediterraneas', 'Revisión de fosas septicas cuencas mediterraneas', '2025-10-07', '2025-10-07', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Cuencas Mediterraneas', 3, 'ENEKO', 1, 0);

-- Registro 557/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0393', 3.0, 1, 0, 3, 3, 'Fuga en C/San Jorge n1 en Gazeta', 'Fuga en C/San Jorge n1 en Gazeta', '2025-10-07', '2025-10-07', 42.844486, -2.537951, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Gazeta', 3, 'V', 1, 1);

-- Registro 558/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0394', 3.0, 1, 0, 1, 1, 'Fuga en Santacoloma (Artziniega)', 'Fuga en Santacoloma (Artziniega)', '2025-10-07', '2025-10-08', 43.13817, -3.15801, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 'V', 1, 1);

-- Registro 559/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0260', 3.0, 2, 12, 1, 1, 'Corte de agua en C/Jose Madinabeitia (Amurrio)', 'Corte de agua en C/Jose Madinabeitia (Amurrio)', '2025-10-07', '2025-10-07', 43.053945, -3.001862, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'V', 1, 0);

-- Registro 560/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0395', 5.0, 1, 0, 3, 3, 'Descubrir tapa de saneamiento en Alegría', 'Descubrir tapa de saneamiento en Alegría', '2025-10-08', '2025-10-08', 42.849389, -2.513307, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 3, 'EDUARDO', 1, 3);

-- Registro 561/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0396', 3.0, 1, 0, 3, 3, 'Reparación de tubo en Agurain', 'Reparación de tubo en Agurain', '2025-10-08', '2025-10-08', 42.849762, -2.39043, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 'EDUARDO', 1, 3);

-- Registro 562/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0397', 5.0, 1, 0, 3, 3, 'Reparación en saneamiento Raíces-parque Aniturri (Agurain)', 'Reparación en saneamiento Raíces-parque Aniturri (Agurain)', '2025-10-08', '2025-10-14', 42.849762, -2.39043, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 'BEÑAT,ZOVITA,RAFNIR', 1, 3);

-- Registro 563/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0261', 3.0, 2, 8, 1, 1, 'Instalación de contador en Lateorro n 2 (Llodio)', 'Instalación de contador en Lateorro n 2 (Llodio)', '2025-10-08', '2025-10-08', 43.137761, -2.963345, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'IÑIGO', 1, 0);

-- Registro 564/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0262', 3.0, 2, 8, 1, 1, 'Instalación de contador en C/Padura n39 en Luiando', 'Instalación de contador en C/Padura n39 en Luiando', '2025-10-08', '2025-10-08', 43.095364, -3.001219, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Luiando', 1, 'IÑIGO', 1, 0);

-- Registro 565/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0263', 3.0, 2, 13, 1, 1, 'Asistencia técnica a Ayto Llodio para obra ambulatorio', 'Asistencia técnica a Ayto Llodio para obra ambulatorio', '2025-10-08', '2025-10-08', 43.140845, -2.959536, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 0);

-- Registro 566/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0264', 3.0, 2, 7, 1, 1, 'Localización de fugas, restablecimiento en Sector Isasi (Llodio)', 'Localización de fugas, restablecimiento en Sector Isasi (Llodio)', '2025-10-08', '2025-10-08', 43.151079, -2.9727381, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 1);

-- Registro 567/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0265', 3.0, 2, 8, 1, 1, 'Instalación de contador en Zumalakarregui n48 (Clarel)(Llodio)', 'Instalación de contador en Zumalakarregui n48 (Clarel)(Llodio)', '2025-10-08', '2025-10-08', 43.141631, -2.964516, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 0);

-- Registro 568/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0266', 3.0, 2, 8, 1, 1, 'Instalación de contador en Irukurutzeta n19 (Llodio)', 'Instalación de contador en Irukurutzeta n19 (Llodio)', '2025-10-10', '2025-10-10', 43.135161, -2.968514, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 0);

-- Registro 569/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0267', 3.0, 2, 10, 6, 6, 'Sustitución contador en Pol.Salbarte (Talcer S.L) en Alda', 'Sustitución contador en Pol.Salbarte (Talcer S.L) en Alda', '2025-10-09', '2025-10-09', 42.750463, -2.344318, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alda', 6, 'TOMAS', 1, 0);

-- Registro 570/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0268', 3.0, 2, 8, 3, 3, 'Instalación de contador en Gauna n66', 'Instalación de contador en Gauna n66', '2025-10-09', '2025-10-09', 42.825708, -2.493293, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Gauna', 3, 'IÑIGO', 1, 0);

-- Registro 571/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0269', 3.0, 2, 19, 6, 6, 'Sustitución de contador en Edar San Vicente Arana C/Virgen de Uralde S/N', 'Sustitución de contador en San Vicente C/Virgen de Uralde S/N', '2025-10-09', '2025-10-09', 42.736573, -2.361599, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'San Vicente de Arana', 6, 'TOMAS E IÑIGO', 1, 0);

-- Registro 572/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0270', 3.0, 2, 8, 1, 1, 'Instalación contador en C/Pintor Jose Arrue en (Llodio)', 'Instalación contador en  C/Pintor Jose Arrue en (Llodio)', '2025-10-08', '2025-10-08', 43.14556, -2.959504, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'IÑIGO', 1, 0);

-- Registro 573/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0271', 5.0, 2, 7, 3, 3, 'Recoger información en campo de las redes de saneamiento (Alegría)', 'Recoger información en campo de las redes de pluviales en saneamiento (Alegría)', '2025-10-08', '2025-10-08', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 3, 'ENEKO', 1, 0);

-- Registro 574/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0398', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Iturriaga n2 (Llodio)', 'Reparación de fuga en Iturriaga n2 (Llodio)', '2025-10-08', '2025-10-09', 43.146545, -2.968018, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS,RAFNIR,IÑIGO,ZOUITA', 1, 1);

-- Registro 575/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0272', 2.0, 2, 23, 1, 1, 'Limpieza Tamices en Onsoño,Añes,Kostera,Madaria,Aguiñiga,Lejarzo etc…', 'Limpieza Tamices en Onsoño,Añes,Kostera,Madaria,Aguiñiga,Lejarzo etc…', '2025-10-09', '2025-10-09', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Añes', 1, 'V', 1, 0);

-- Registro 576/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0399', 5.0, 1, 0, 5, 5, 'Atasco en Anucita n33', 'Atasco en Anucita n33', '2025-10-10', '2025-10-10', 42.80146, -2.8991730000000002, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Anucita', 5, 'KERMAN E IÑIGO', 1, 2);

-- Registro 577/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0273', 3.0, 2, 13, 3, 3, 'Asistencia técnica a Urbide (Alegría)', 'Asistencia técnica a Urbide (Alegría)', '2025-10-09', '2025-10-09', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 3, 'V', 1, 0);

-- Registro 578/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0274', 5.0, 2, 1, 3, 3, 'Mantenimiento preventivo saneamiento C/Aniturri y parque (Agurain)', 'Mantenimiento preventivo saneamiento C/Aniturri y parque (Agurain)', '2025-10-09', '2025-10-09', 42.849813, -2.390545, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 'EMILIO,MIGUEL', 1, 0);

-- Registro 579/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0275', 1.0, 2, 2, 1, 1, 'Limpieza de captaciones en Aiaraldea', 'Limpieza de captaciones en Aiaraldea', '2025-10-10', '2025-10-10', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Aiaraldea', 1, 'V', 1, 0);

-- Registro 580/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0400', 3.0, 1, 0, 5, 5, 'Fuga en Puentelarra C/San Nicolás', 'Fuga en Puentelarra  C/San Nicolás', '2025-10-10', '2025-10-10', 42.751276, -3.048088, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Puentelarra', 5, 'V', 1, 1);

-- Registro 581/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0401', 5.0, 1, 0, 1, 1, 'Desatasco tubería Landako (Amurrio)', 'Desatasco tubería Landako (Amurrio)', '2025-10-10', '2025-10-10', 43.051674, -2.996666, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'V', 1, 2);

-- Registro 582/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0402', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Amurrio ( edificio policia municipal)', 'Reparación de fuga en Amurrio ( edificio policia municipal)', '2025-10-10', '2025-10-10', 43.05117, -3.00232, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'MIGUEL', 1, 1);

-- Registro 583/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0403', 3.0, 1, 0, 1, 1, 'Fuga Esquina Abajo en Respaldiza', 'Fuga Esquina Abajo en Respaldiza', '2025-10-11', '2025-10-11', 43.087224, -3.043534, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Respaldiza', 1, 'V', 1, 1);

-- Registro 584/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0404', 3.0, 1, 0, 1, 1, 'Abonado sin agua en Artziniega C/Sandolla', 'Abonado sin agua en Artziniega C/Sandolla', '2025-10-11', '2025-10-11', 43.123508, -3.135839, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 'V', 1, 3);

-- Registro 585/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0405', 3.0, 1, 0, 5, 5, 'Reparación de fuga en Estabillo C/Mavilla', 'Reparación de fuga en Estabillo C/Mavilla', '2025-10-27', '2025-10-28', 42.729138, -2.857969, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Estabillo', 5, 'V', 1, 1);

-- Registro 586/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0406', 5.0, 1, 0, 9, 9, 'Atasco en Oreitia', 'Atasco en Oreitia', '2025-10-12', '2025-10-12', 42.858034, -2.557345, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Oreitia', 9, 'V', 1, 2);

-- Registro 587/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0276', 2.0, 2, 3, 3, 3, 'Limpieza de Fosas Sépticas en Opakua y Agurain', 'Limpieza de Fosas Sépticas en Opakua y Agurain', '2025-10-13', '2025-10-13', 42.827806, -2.357944, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 'EMILIO Y ANGEL', 1, 0);

-- Registro 588/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0408', 5.0, 1, 0, 1, 1, 'Desatasco Urbanización Axpe en Artziniega', 'Desatasco Urbanización Axpe en Artziniega', '2025-10-13', '2025-10-13', 43.119607, -3.134497, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 'MIGUEL KERMAN', 1, 2);

-- Registro 589/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0409', 3.0, 1, 0, 1, 1, 'Comprobar presión en contador en C/Sandolla n18 en Artziniega', 'Comprobar presión en contador en C/Sandolla n18 en Artziniega', '2025-10-13', '2025-10-13', 43.12404, -3.13479, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 'MIGUEL KERMAN', 1, 3);

-- Registro 590/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0410', 3.0, 1, 0, 1, 1, 'Fuga en C/Dionisio Aldama n2 en Amurrio', 'Fuga en C/Dionisio Aldama n2 en Amurrio', '2025-10-13', '2025-10-13', 43.050867, -3.000813, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'MIGUEL KERMAN', 1, 1);

-- Registro 591/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0411', 1.0, 1, 0, 1, 1, 'Fuga en Lejarzo', 'Fuga en Lejarzo', '2025-10-13', '2025-10-14', 43.056569, -3.12121, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Lejarzo', 1, 'MIGUEL KERMAN', 1, 1);

-- Registro 592/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0412', 3.0, 1, 0, 1, 1, 'Fuga en Respaldiza (Landeta)', 'Fuga en Respaldiza (Landeta)', '2025-10-13', '2025-10-14', 43.071173, -3.035659, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Respaldiza', 1, 'V', 1, 1);

-- Registro 593/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0413', 3.0, 1, 0, 1, 1, 'Fuga en Larraño en Llodio', 'Fuga en C/ Larraño en Llodio', '2025-10-13', '2025-10-14', 43.141288, -2.970825, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'V', 1, 1);

-- Registro 594/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0277', 3.0, 2, 11, 3, 3, 'Lectura en ruta de contadores Sectoriales en cuencas mediterraneas', 'Lectura en ruta de contadores Sectoriales en cuencas mediterraneas', '2025-10-13', '2025-10-13', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Cuencas mediterraneas', 3, 'ENEKO', 1, 0);

-- Registro 595/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0407', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Erbi', 'Reparación de fuga en Erbi', '2025-10-14', '2025-10-17', 43.074553, -3.113303, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Erbi', 1, 'KERMAN', 1, 1);

-- Registro 596/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0414', 3.0, 1, 0, 3, 3, 'Aviso abonado sin agua C/Arramel n1 (Agurain)', 'Aviso abonado sin agua C/Arramel n1 (Agurain)', '2025-10-09', '2025-10-09', 42.849801, -2.38849, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 'EDU', 1, 3);

-- Registro 597/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0278', 3.0, 2, 7, 1, 1, 'Localización de fugas abastecimiento en Sector Arza (Calle Gardia)', 'Localización de fugas abastecimiento en Sector Arza (Calle Gardia)', '2025-10-10', '2025-10-10', 43.133631, -2.971418, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 1);

-- Registro 598/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0279', 3.0, 2, 13, 1, 1, 'Asistencia técnica a obra municipal renovación anillo fibrocemento en P.Lamuza', 'Asistencia técnica a obra municipal renovación anillo fibrocemento en P.Lamuza', '2025-10-10', '2025-10-23', 43.144203, -2.964357, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 0);

-- Registro 599/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0280', 3.0, 2, 7, 1, 1, 'Localización de fugas en sector Katuxa Ibarra (Llodio)', 'Localización de fugas en sector Katuxa Ibarra (Llodio)', '2025-10-10', '2025-10-10', 43.133299, -2.971288, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 1);

-- Registro 600/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0281', 3.0, 2, 13, 1, 1, 'Asistencia técnica en Maroño n2', 'Asistencia técnica en Maroño n2', '2025-10-10', '2025-10-10', 43.043242, -3.06442, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maroño', 1, 'TOMAS', 1, 0);

-- Registro 601/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0282', 3.0, 2, 4, 5, 5, 'Digitalización de redes abastecimiento en Pobes', 'Digitalización de redes abastecimiento en Pobes', '2025-10-13', '2025-10-13', 42.801954, -2.911629, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Pobes', 5, 'TOMAS', 1, 0);

-- Registro 602/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0283', 3.0, 2, 7, 1, 1, 'Localización de fugas en Sector Ugarte (Llodio)', 'Localización de fugas en Sector Ugarte (Llodio)', '2025-10-14', '2025-10-14', 43.1465, -2.967408, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 1);

-- Registro 603/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0284', 3.0, 2, 13, 1, 1, 'Asistencia técnica a obra municipal Colegio Lateorro (Llodio)', 'Asistencia técnica a obra municipal Colegio Lateorro (Llodio)', '2025-10-14', '2025-10-14', 43.13848, -2.959153, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 0);

-- Registro 604/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0285', 3.0, 2, 13, 1, 1, 'Asistencia técnica a obra en Maroño', 'Asistencia técnica a obra en Maroño', '2025-10-14', '2025-10-14', 43.033358, -3.073682, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maroño', 1, 'TOMAS', 1, 0);

-- Registro 605/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0286', 3.0, 2, 8, 1, 1, 'Instalación contador para churrería (Amurrio)', 'Instalación contador para churrería (Amurrio)', '2025-10-14', '2025-10-14', 43.052227, -3.00114, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'KERMAN', 1, 0);

-- Registro 606/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0287', 3.0, 2, 10, 5, 5, 'Sustitución de contador C/Avenida Omecillo n5 (Villanañe)', 'Sustitución de contador C/Avenida Omecillo n5 (Villanañe)', '2025-10-14', '2025-10-14', 42.836417, -3.07138, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Villanañe', 5, 'KERMAN', 1, 0);

-- Registro 607/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0288', 3.0, 2, 8, 1, 1, 'Instalación de contador en churreria (caravana) en Amurrio', 'Instalación de contador en churreria (caravana) en Amurrio', '2025-10-14', '2025-10-14', 43.055695, -3.004394, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'KERMAN', 1, 0);

-- Registro 608/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0289', 5.0, 2, 1, 3, 3, 'Mantenimiento preventivo de limpieza de colector saneamiento (Agurain)', 'Mantenimiento preventivo de limpieza de colector saneamiento (Agurain)', '2025-10-14', '2025-10-14', 42.847327, -2.391009, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 'EMILIO MIGUEL', 1, 0);

-- Registro 609/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0290', 5.0, 2, 1, 1, 1, 'Mantenimiento preventivo en saneamiento en C/Isasi  (Llodio)', 'Mantenimiento preventivo en saneamiento en C/Isasi  (Llodio)', '2025-10-14', '2025-10-14', 43.150873, -2.971293, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'EMILIO MIGUEL', 1, 0);

-- Registro 610/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0291', 3.0, 2, 7, 5, 5, 'Localización de fugas en Maroño y Bellojín', 'Localización de fugas en Maroño y Bellojín', '2025-10-14', '2025-10-14', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Bellojín', 5, 'ENEKO', 1, 1);

-- Registro 611/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0415', 3.0, 1, 0, 1, 1, 'Fuga en Landeta (Respaldiza)', 'Fuga en Landeta (Respaldiza)', '2025-10-14', '2025-10-14', 43.071173, -3.035639, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Respaldiza', 1, 'V', 1, 1);

-- Registro 612/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0416', 3.0, 1, 0, 1, 1, 'Fuga en Larraño  (Llodio)', 'Fuga en Larraño (Llodio)', '2025-10-14', '2025-10-14', 43.15124, -2.983425, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'V', 1, 1);

-- Registro 613/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0417', 3.0, 1, 0, 1, 1, 'Fuga en Olabezar (La Cadena)', 'Fuga en Olabezar (La Cadena)', '2025-10-14', '2025-10-15', 43.05571, -3.015934, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Olabezar', 1, 'V', 1, 1);

-- Registro 614/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0418', 5.0, 1, 0, 1, 1, 'Atasco en Campijo en Artziniega', 'Atasco en Campijo en Artziniega', '2025-10-14', '2025-10-14', 43.147755, -3.159083, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 'V', 1, 2);

-- Registro 615/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0419', 3.0, 1, 0, 3, 3, 'Reparación de fuga en C/La Madura (Agurain)', 'Reparación de fuga en C/La Madura (Agurain)', '2025-10-14', '2025-10-15', 42.852939, -2.387135, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 'BEÑAT KERMAN', 1, 1);

-- Registro 616/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0420', 3.0, 1, 0, 5, 5, 'Fuga en Bellojín', 'Fuga en Bellojín', '2025-10-15', '2025-10-15', 43.121417, -3.096508, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Bellojín', 5, 'MIGUEL CHOVITA', 1, 1);

-- Registro 617/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0421', 3.0, 1, 0, 1, 1, 'Reparar fuga en Erbi', 'Reparar fuga en Erbi', '2025-10-15', '2025-10-15', 43.075035, -3.113745, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Erbi', 1, 'KERMAN', 1, 1);

-- Registro 618/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0292', 3.0, 2, 9, 3, 3, 'Desistalación contador C/Uribe s/n en Alegría', 'Desistalación contador C/Uribe s/n en Alegría', '2025-10-15', '2025-10-15', 42.839704, -2.51117, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 3, 'KERMAN', 1, 0);

-- Registro 619/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0422', 3.0, 1, 0, 1, 1, 'Fuga en válvula general en barrio Chabe n54 (Llanteno)', 'Fuga en válvula general en barrio Chabe n54 (Llanteno)', '2025-10-15', '2025-10-16', 43.121417, -3.096508, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llanteno', 1, 'KERMAN', 1, 1);

-- Registro 620/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0291', 5.0, 1, 0, 1, 1, 'Atasco en Olabezar ermita San Babilas pead 63', 'Atasco en Olabezar Hermita San Babilas pead 63', '2025-10-14', '2025-10-14', 43.07002, -3.011274, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Olabezar', 1, 'V', 1, 2);

-- Registro 621/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0292', 3.0, 1, 0, 1, 1, 'Aviso abonado sin agua en Larra (Llodio)', 'Aviso abonado sin agua en Larra (Llodio)', '2025-10-15', '2025-10-15', 43.12817, -2.9504, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'JOSEBA', 1, 3);

-- Registro 622/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0293', 3.0, 1, 0, 5, 5, 'Reparación de fuga en bajada deposito en Arbigano', 'Reparación de fuga en bajada deposito en Arbigano', '2025-10-21', '2025-10-21', 42.804418, -2.933458, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Arbígano', 5, 'MIGUEL', 1, 1);

-- Registro 623/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0294', 3.0, 1, 0, 1, 1, 'Reparación de acometida en INAUXA (Amurrio)', 'Reparación de acometida en INAUXA (Amurrio)', '2025-10-17', '2025-10-17', 43.03715, -2.99664, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'IÑIGO', 1, 3);

-- Registro 624/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0295', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Añes', 'Reparación de fuga en Añes', '2025-10-16', '2025-10-17', 43.058515, -3.132879, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Añes', 1, 'v', 1, 1);

-- Registro 625/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0296', 3.0, 1, 0, 1, 1, 'Reparación de fuga en acometida en Maroño', 'Reparación de fuga en acometida en Maroño', '2025-10-15', '2025-10-16', 43.041785, -3.062303, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maroño', 1, 'JOSEBA E IÑIGO', 1, 1);

-- Registro 626/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0297', 5.0, 1, 0, 1, 1, 'Desbroce y desatasco de arqueta saneamiento en Kostera', 'Desbroce y desatasco de arqueta saneamiento en Kostera', '2025-10-22', '2025-10-22', 43.103604, -3.101419, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Kostera', 1, 'KERMAN ZUITA', 1, 2);

-- Registro 627/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0298', 3.0, 1, 0, 1, 1, 'Aviso abonado sin agua en C/Nervión n14 (Llodio)', 'Aviso abonado sin agua en C/Nervión n14 (Llodio)', '2025-10-19', '2025-10-19', 43.142114, -2.962384, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'V', 1, 3);

-- Registro 628/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0299', 3.0, 1, 0, 5, 5, 'Aviso por fuga en Berantevilla en Camino las heras n17', 'Aviso por fuga en Berantevilla Camino las heras n17', '2025-10-19', '2025-10-19', 42.681951, -2.859392, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Berantevilla', 5, 'V', 1, 1);

-- Registro 629/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0293', 2.0, 2, 23, 1, 1, 'Limpieza de Tamices en Olabezar', 'Limpieza de Tamices en Olabezar', '2025-10-15', '2025-10-15', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Olabezar', 1, 'V', 1, 0);

-- Registro 630/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0294', 3.0, 2, 13, 5, 5, 'Asistencia técnica a obra Villanañe', 'Asistencia técnica a obra Villanañe', '2025-10-15', '2025-10-15', 42.836724, -3.07171, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Villanañe', 5, 'TOMAS', 1, 0);

-- Registro 631/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0295', 3.0, 2, 8, 1, 1, 'Instalación contador en Plaza Lexarraga n4 (Amurrio)', 'Instalación contador en Plaza Lexarraga n4 (Amurrio)', '2025-10-15', '2025-10-15', 43.052806, -3.005891, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'KERMAN', 1, 0);

-- Registro 632/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0296', 3.0, 2, 8, 1, 1, 'Instalación contador en Pol.Maskuribai B03 (Amurrio)', 'Instalación contador en Pol.Maskuribai B03 (Amurrio)', '2025-10-15', '2025-10-15', 43.045837, -3.00037, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'KERMAN', 1, 0);

-- Registro 633/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0297', 2.0, 2, 3, 5, 5, 'Mantenimiento de fosas sépticas en Corro', 'Mantenimiento de fosas sépticas en Corro', '2025-10-15', '2025-10-15', 42.873629, -3.174306, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Corro', 5, 'EMILIO ALBERTO', 1, 0);

-- Registro 634/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0298', 3.0, 2, 7, 1, 1, 'Localización de fugas en Amurrio y Maroño', 'Localización de fugas en Amurrio y Maroño', '2025-10-15', '2025-10-15', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maroño', 1, 'ENEKO', 1, 1);

-- Registro 635/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0299', 5.0, 2, 1, 1, 1, 'Mantenimiento preventivo en saneamiento Artziniega', 'Mantenimiento preventivo en saneamiento Artziniega', '2025-10-16', '2025-10-16', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 'EMILIO MIGUEL', 1, 0);

-- Registro 636/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0423', 3.0, 1, 0, 5, 5, 'Aviso de fuga  y avisos de corte de agua en Espejo', 'Aviso de fuga  y avisos de corte de agua en Espejo', '2025-10-14', '2025-10-14', 42.8101, -3.04675, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Espejo', 5, 'EDUARDO', 1, 1);

-- Registro 637/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0424', 1.0, 1, 0, 5, 5, 'Aviso por falta de agua en captaciones en Espejo', 'Aviso por falta de agua en captaciones en Espejo', '2025-10-14', '2025-10-14', 42.80874, -3.06457, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Espejo', 5, 'EDUARDO', 1, 3);

-- Registro 638/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0425', 3.0, 1, 0, 1, 1, 'Reparación de fuga en C/Atxarte (Llodio)', 'Reparación de fuga en C/Atxarte (Llodio)', '2025-10-21', '2025-10-23', 43.149672, -2.945507, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, NULL, 1, 1);

-- Registro 639/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0426', 5.0, 1, 0, 1, 1, 'Reparación de tapa de saneamiento en Aldaiturriaga (Amurrio)', 'Reparación de tapa de saneamiento en Aldaiturriaga (Amurrio)', '2025-10-21', '2025-10-21', 43.038227, -3.004061, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'ZOVITA Y MIGUEL', 1, 3);

-- Registro 640/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0300', 3.0, 2, 8, 1, 1, 'Intalación de contador en C/Federico Barrenengoa n21 (Amurrio)', 'Intalación de contador en C/Federico Barrenengoa n21 (Amurrio)', '2025-10-16', '2025-10-16', 43.053694, -3.005325, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'KERMAN', 1, 0);

-- Registro 641/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0301', 3.0, 2, 8, 1, 1, 'Intalación de contador en C/Plaza Osteguieta n7 (Llodio)', 'Intalación de contador en C/Plaza Osteguieta n7 (Llodio)', '2025-10-16', '2025-10-16', 43.14493, -2.962058, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'KERMAN', 1, 0);

-- Registro 642/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0302', 3.0, 2, 8, 1, 1, 'Instalación de contador en Plaza Osteguieta n7 (Llodio)', 'Instalación de contador en Plaza Osteguieta n7 (Llodio)', '2025-10-16', '2025-10-16', 43.14493, -2.962058, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'KERMAN', 1, 0);

-- Registro 643/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0303', 3.0, 2, 10, 1, 1, 'Sustitución de contador en C/Sandolla n11 (Atziniega)', 'Sustitución de contador en C/Sandolla n11 (Atziniega)', '2025-10-16', '2025-10-17', 43.12383, -3.135701, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 'KERMAN MIGUEL Y ZOVITA', 1, 0);

-- Registro 644/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0304', 3.0, 2, 5, 3, 3, 'Inventario y digitalización red de abastecimiento en (Alegría)', 'Inventario y digitalización red de abastecimiento en (Alegría)', '2025-10-16', '2025-10-17', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 3, 'ENEKO', 1, 0);

-- Registro 645/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0305', 3.0, 2, 9, 1, 1, 'Retirada contador C/Pagolar n10 (Llodio)', 'Retirada contador C/Pagolar n10 (Llodio)', '2025-10-16', '2025-10-16', 43.139386, -2.961702, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'KERMAN', 1, 0);

-- Registro 646/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0306', 1.0, 2, 2, 1, 1, 'Limpieza captaciones Katzabazo,Delika,Agiñiga,Intxulaspe,Artomana', 'Limpieza captaciones Katzabazo,Delika,Agiñiga,Intxulaspe,Artomana', '2025-10-17', '2025-10-17', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Delika', 1, 'V', 1, 0);

-- Registro 647/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0307', 3.0, 2, 12, 1, 1, 'Corte de Agua en Lateorro (Llodio)', 'Corte de Agua en Lateorro (Llodio)', '2025-10-17', '2025-10-17', 43.138773, -2.96048, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'IÑIGO', 1, 0);

-- Registro 648/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0308', 3.0, 2, 7, 5, 5, 'Localización de fugas en Villanueva de Valdegovia', 'Localización de fugas en Villanueva de Valdegovia', '2025-10-17', '2025-10-17', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Gaubea', 5, 'ENEKO', 1, 1);

-- Registro 649/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0309', 5.0, 2, 7, 3, 3, 'Mantenimiento preventivo saneamiento Alegría', 'Mantenimiento preventivo saneamiento Alegría', '2025-10-17', '2025-10-17', 42.852398, -2.39003, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 3, 'ANGEL KERMAN EDU', 1, 0);

-- Registro 650/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0310', 5.0, 2, 1, 3, 3, 'Mantenimiento preventivo saneamiento Agurain', 'Mantenimiento preventivo saneamiento Agurain', '2025-10-17', '2025-10-17', 42.852475, -2.390226, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 'ANGEL KERMAN EDU', 1, 0);

-- Registro 651/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0427', 5.0, 1, 0, 4, 4, 'Atasco en saneamiento en Zurbano', 'Atasco en saneamiento en Zurbano', '2025-10-18', '2025-10-18', 42.869999, -2.617144, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Zurbano', 4, 'V', 1, 2);

-- Registro 652/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0428', 3.0, 1, 0, 5, 5, 'Aviso abonado sin presión en Astúlez', 'Aviso abonado sin presión en Astúlez', '2025-10-18', '2025-10-18', 42.882237, -3.087401, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Astúlez', 5, 'V', 1, 3);

-- Registro 653/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0429', 3.0, 1, 0, 5, 5, 'Aviso por fuga en Pobes C/Fuente Pudia n48', 'Aviso por fuga en Pobes C/Fuente Pudia n48', '2025-10-18', '2025-10-18', 42.802503, -2.910875, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Pobes', 5, 'V', 1, 1);

-- Registro 654/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0430', 3.0, 1, 0, 5, 5, 'Aviso abonado sin agua en C/Gazarriza n11 (Rivabellosa)', 'Aviso abonado sin agua en C/Gazarriza n11 (Rivabellosa)', '2025-10-20', '2025-10-20', 42.710346, -2.918302, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa', 5, 'EDU', 1, 3);

-- Registro 655/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0311', 5.0, 2, 1, 1, 1, 'Mantenimiento preventivo enLlodio (Ellakuri,Tubacex,Gokoplaza)', 'Mantenimiento preventivo en Llodio (Ellakuri,Tubacex,Goikoplaza)', '2025-10-20', '2025-10-20', 43.134931, -2.968648, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'EMILIO MIGUEL', 1, 0);

-- Registro 656/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0312', 3.0, 2, 10, 5, 5, 'Sustitución de contador C/Arquitecto Jesus Guinea n94 (Villanueva)', 'Sustitución de contador C/Arquitecto Jesus Guinea N94 (Villanueva)', '2025-10-20', '2025-10-20', 42.847788, -3.104834, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Villanueva', 5, 'KERMAN Y ZOUITA', 1, 0);

-- Registro 657/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0431', 3.0, 1, 0, 5, 5, 'Reparación de fuga en C/Arquitecto Jesus Guinea n9 (Villanueva)', 'Reparación de fuga en C/Arquitecto Jesus Guinea n9 (Villanueva)', '2025-10-20', '2025-10-20', 42.84755, -3.101988, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Villanueva', 5, 'KERMAN Y ZOUITA', 1, 1);

-- Registro 658/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0432', 3.0, 1, 0, 5, 5, 'Reparación de fuga en C/Omecillo n13 (Espejo)', 'Reparación de fuga en C/Omecillo n13 (Espejo)', '2025-10-20', '2025-10-20', 42.808506, -3.050214, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Espejo', 5, 'KERMAN Y ZOUITA', 1, 1);

-- Registro 659/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0313', 3.0, 2, 8, 1, 1, 'Instalación contador C/Bañuetaibar n1 (Amurrio)', 'Instalación contador C/Bañuetaibar n1 (Amurrio)', '2025-10-20', '2025-10-20', 43.054042, -2.997814, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'KERMAN Y ZOUITA', 1, 0);

-- Registro 660/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0314', 3.0, 2, 8, 1, 1, 'Instalación contador C/Jose Pikatza n9 (Amurrio)', 'Instalación contador C/Jose Pikatza n9 (Amurrio)', '2025-10-20', '2025-10-20', 43.052826, -3.004529, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'KERMAN Y ZOUITA', 1, 0);

-- Registro 661/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0315', 3.0, 2, 12, 5, 5, 'Colocación de avisos corte de agua en Espejo', 'Colocación de avisos corte de agua en Espejo', '2025-10-21', '2025-10-21', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Espejo', 5, 'EDUARDO', 1, 0);

-- Registro 662/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0433', 3.0, 1, 0, 1, 1, 'Aviso por falta de presión en C/Asudio n1 (Llodio)', 'Aviso por falta de presión en C/Asudio n1 (Llodio)', '2025-10-21', '2025-10-21', 43.13935, -2.964354, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 3);

-- Registro 663/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0434', 5.0, 1, 0, 1, 1, 'Aviso por filtraciónes en saneamiento C/Nerbion n10 (Llodio)', 'Aviso por filtraciónes en C/Nerbioi n10 (Llodio)', '2025-10-21', '2025-10-22', 43.141786, -2.961946, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 1);

-- Registro 664/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0435', 3.0, 1, 0, 1, 1, 'Aviso por avería en C/Goikolarra (Amurrio)', 'Aviso por avería en C/Goikolarra (Amurrio)', '2025-10-21', '2025-10-21', 43.060304, -3.001991, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'IÑIGO', 1, 3);

-- Registro 665/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0316', 3.0, 2, 12, 1, 1, 'Corte de agua en Lateorro (Llodio)', 'Corte de agua en Lateorro (Llodio)', '2025-10-21', '2025-10-21', 43.138648, -2.961284, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'IÑIGO', 1, 0);

-- Registro 666/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0436', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Lekamaña n6', 'Reparación de fuga en Lekamaña n6', '2025-10-21', '2025-10-21', 43.020857, -2.996143, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Lekamaña', 1, 'IÑIGO', 1, 1);

-- Registro 667/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0437', 3.0, 1, 0, 5, 5, 'Reparación de fuga en C/Las Panlejas ( Pobes)', 'Reparación de fuga en C/Las Panlejas ( Pobes)', '2025-10-21', '2025-10-21', 42.803847, -2.908017, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Pobes', 5, 'KERMAN', 1, 1);

-- Registro 668/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0438', 3.0, 1, 0, 3, 3, 'Reparación de fuga en C/Sorginetxe-Arrizala (Opakua)', 'Reparación de fuga en C/Sorginetxe-Arrizala (Opakua)', '2025-10-21', '2025-10-21', 42.827923, -2.371849, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Opacua', 3, 'KERMAN', 1, 1);

-- Registro 669/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0317', 3.0, 2, 8, 1, 1, 'Instalación contador en Colegio Lateorro (Llodio)', 'Instalación contador en Colegio Lateorro (Llodio)', '2025-10-21', '2025-10-21', 43.13833, -2.95859, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'IÑIGO', 1, 0);

-- Registro 670/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0439', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Larrazabal n33-34 (Llodio)', 'Reparación de fuga en Larrazabal n33-34 (Llodio)', '2025-10-21', '2025-10-21', 43.140018, -2.981566, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'MIGUEL', 1, 1);

-- Registro 671/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0440', 3.0, 1, 0, 5, 5, 'Fuga en C/Mayor n33 en Berantevilla', 'Fuga en C/Mayor n33 en Berantevilla', '2025-10-20', '2025-10-21', 42.68366, -2.85699, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Berantevilla', 5, 'V', 1, 1);

-- Registro 672/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0441', 3.0, 1, 0, 5, 5, 'Reparación de Fuga en Pobes C/Fuente pudia n48', 'Fuga en Pobes C/Fuente pudia n48', '2025-10-20', '2025-10-21', 42.802503, -2.910875, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Pobes', 5, 'V', 1, 1);

-- Registro 673/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0318', 3.0, 2, 12, 3, 3, 'Corte de agua en Agurain C/HarriKrutz', 'Corte de agua en Agurain C/HarriKrutz', '2025-10-22', '2025-10-22', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 'V', 1, 0);

-- Registro 674/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0442', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Retes de Tudela', 'Reparación de fuga en Retes de Tudela', '2025-10-22', '2025-10-22', 43.114828, -3.169099, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Retes de Tudela', 1, 'V', 1, 1);

-- Registro 675/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0319', 2.0, 2, 3, 4, 4, 'Mantenimiento de fosas Sépticas en Mendibil', 'Mantenimiento de fosas Sépticas en Mendibil', '2025-10-22', '2025-10-22', 42.905536, -2.629608, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Mendibil', 4, 'EMILIO KERMAN', 1, 0);

-- Registro 676/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('GF/0005', 4.0, 3, 0, 10, 10, 'Gastos fijos de explotación totales', 'Gastos fijos de explotación totales', '2025-10-01', '2025-10-31', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL, 10, 'ELENA', 1, 0);

-- Registro 677/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('GF/0006', 4.0, 3, 0, 10, 10, 'Gestión documental del contrato', 'Gestión documental del contrato', '2025-10-01', '2025-10-31', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL, 10, 'ELENA', 1, 0);

-- Registro 678/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0320', 2.0, 2, 3, 4, 4, 'Vaciado y limpieza de fosas sépticas de Luko', 'Vaciado y limpieza de fosas sépticas de Luko', '2025-10-22', '2025-10-22', 42.93315, -2.641269, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Luko', 4, 'EMILIO KERMAN', 1, 0);

-- Registro 679/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0443', 3.0, 1, 0, 3, 3, 'Reparación de fuga en acometida en C/Gauna n43 (Gauna)', 'Reparación de fuga en acometida en C/Gauna n43 (Gauna)', '2025-10-22', '2025-10-22', 42.823961, -2.496554, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Gauna', 3, 'EDU ZOUITA', 1, 1);

-- Registro 680/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0444', 3.0, 1, 0, 1, 1, 'Aviso de falta de presión en C/Otazu n1 (Luiando)', 'Aviso de falta de presión en C/Otazu n1 (Luiando)', '2025-10-23', '2025-10-23', 43.106624, -2.996129, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Luiando', 1, 'TOMAS', 1, 3);

-- Registro 681/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0321', 5.0, 2, 1, 1, 1, 'Mantenimiento preventivo saneamiento TUBACEX en ArtzIniega', 'Mantenimiento preventivo saneamiento TUBACEX en Artzeniega', '2025-10-23', '2025-10-23', 43.12346, -3.11906, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, NULL, 1, 0);

-- Registro 682/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0445', 3.0, 1, 0, 5, 5, 'Reparación de fuga en Lacorzanilla  Berantevilla (Ermita la Virgen)', 'Reparación de fuga en Lacorzanilla  Berantevilla (Ermita la Virgen)', '2025-10-23', '2025-10-23', 42.67988, -2.88295, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Lacorzanilla', 5, 'EDU MIGUEL', 1, 1);

-- Registro 683/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0322', 3.0, 2, 12, 1, 1, 'Corte de agua en C/San Jose (Amurrio)', 'Corte de agua en C/San Jose (Amurrio)', '2025-10-23', '2025-10-23', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'V', 1, 0);

-- Registro 684/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0323', 3.0, 2, 8, 5, 5, 'Instalación contador C/La paz n7 (Rivabellosa)', 'Instalación contador C/La paz n7 (Rivabellosa)', '2025-10-23', '2025-10-23', 42.708427, -2.919311, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa', 5, 'KERMAN', 1, 0);

-- Registro 685/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0324', 3.0, 2, 9, 5, 5, 'Retirada contador junto al cemanterio en Jokano', 'Retirada contador junto al cemanterio en Jokano', '2025-10-23', '2025-10-23', 42.870985, -2.916945, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Jókano', 5, 'KERMAN', 1, 0);

-- Registro 686/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0446', 3.0, 1, 0, 5, 5, 'Reparar fuga en contador en C/Lorrabido n28 (Barrio)', 'Reparar fuga en contador en C/Lorrabido n28 (Barrio)', '2025-10-23', '2025-10-23', 42.808265, -3.088498, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Barrio', 5, 'KERMAN', 1, 1);

-- Registro 687/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0447', 3.0, 1, 0, 5, 5, 'Reparación de fuga en Carretera Bilbao 68 ( Espejo)', 'Reparación de fuga en Carretera Bilbao 68 ( Espejo)', '2025-10-23', '2025-10-23', 42.809968, -3.046787, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Espejo', 5, 'KERMAN', 1, 1);

-- Registro 688/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0448', 3.0, 1, 0, 1, 1, 'Aviso de fuga en C/Zumalakarregi n38 (Llodio)', 'Aviso de fuga en C/Zumalakarregi n38 (Llodio)', '2025-10-23', '2025-10-23', 43.14302, -2.96358, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'JOSEBA', 1, 1);

-- Registro 689/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0449', 3.0, 1, 0, 1, 1, 'Aviso por falta de agua en C/Larrimbe n29 (Amurrio)', 'Aviso por falta de agua en C/Larrimbe n29 (Amurrio)', '2025-10-24', '2025-10-25', 43.035997, -2.975046, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'MIGUEL JOSEBA', 1, 3);

-- Registro 690/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0325', 1.0, 2, 2, 1, 1, 'Limpieza de captaciones Aiaraldea', 'Limpieza de captaciones Aiaraldea', '2025-10-24', '2025-10-24', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Aiaraldea', 1, 'V', 1, 0);

-- Registro 691/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0326', 3.0, 2, 12, 1, 1, 'Corte de agua en C/Goikolarra en Amurrio', 'Corte de agua en C/Goikolarra en Amurrio', '2025-10-24', '2025-10-24', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'V', 1, 0);

-- Registro 692/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0327', 3.0, 2, 17, 1, 1, 'Limpieza de red en Olabezar (La Cadena)', 'Limpieza de red en Olabezar (La Cadena)', '2025-10-24', '2025-10-24', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Olabezar', 1, 'V', 1, 0);

-- Registro 693/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0328', 3.0, 2, 10, 1, 1, 'Sustitución de contador en C/Goikolarra (Amurrio)', 'Sustitución de contador en C/Goikolarra (Amurrio)', '2025-10-24', '2025-10-24', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'IÑIGO', 1, 0);

-- Registro 694/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0329', 3.0, 2, 8, 3, 3, 'Instalación contador C/Treviño n5 (Agurain)', 'Instalación contador C/Treviño n5 (Agurain)', '2025-10-24', '2025-10-24', 42.84681, -2.38901, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 'IÑIGO', 1, 0);

-- Registro 695/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0330', 5.0, 2, 1, 1, 1, 'Mantenimiento preventivo saneamiento C/Aldai (Amurrio)', 'Mantenimiento preventivo saneamiento C/Aldai (Amurrio)', '2025-10-24', '2025-10-24', 43.050425, -3.003176, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'EMILIO IÑIGO EDU MIGUEL', 1, 0);

-- Registro 696/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0450', 3.0, 1, 0, 5, 5, 'Aviso por falta de presión en C/Puente en Armiñon', 'Aviso por falta de presión en C/Puente en Armiñon', '2025-10-25', '2025-10-25', 42.723116, -2.874217, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Armiñon', 5, NULL, 1, 3);

-- Registro 697/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0451', 3.0, 1, 0, 1, 1, 'Fuga en Maroño', 'Fuga en Maroño', '2025-10-27', '2025-10-28', 43.043496, '-3,063023', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maroño', 1, 'V', 1, 1);

-- Registro 698/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0452', 3.0, 1, 0, 5, 5, 'Abonado sin agua en Espejo C/Las Arenas n6', 'Abonado sin agua en Espejo C/Las Arenas n6', '2025-10-25', '2025-10-25', 42.80991, -3.04542, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Espejo', 5, 'V', 1, 3);

-- Registro 699/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0453', 5.0, 1, 0, 1, 1, 'Atasco saneamiento C/Perrutxito n19-17 en Salinas de Añana', 'Atasco saneamiento C/Perrutxito n19-17 en Salinas de Añana', '2025-10-25', '2025-10-25', 42.801843, -2.984825, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, ' Salinas de Añana', 1, 'V', 1, 2);

-- Registro 700/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0334', 2.0, 2, 3, 5, 5, 'Limpieza y vaciado de fosa Anucita', 'Limpieza y vaciado de fosa Anucita', '2025-10-21', '2025-10-27', 42.804118, -2.906388, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Anucita', 5, 'ENEKO EMILIO KERMAN', 1, 0);

-- Registro 701/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0331', 3.0, 2, 7, 5, 5, 'Localización de fuga en Depósito reparto-Arbigano', 'Localización de fuga en Depósito reparto-Arbigano', '2025-10-20', '2025-10-20', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Arbígano', 5, 'ENEKO', 1, 1);

-- Registro 702/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0332', 3.0, 2, 20, 5, 5, 'Localización de fuga en bajada-Depósito en Armiñon', 'Localización de fuga en bajada-Depósito en Armiñon', '2025-10-20', '2025-10-20', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Armiñon', 5, 'ENEKO', 1, 1);

-- Registro 703/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0333', 3.0, 2, 7, 5, 5, 'Localización de fuga en Lacorzanilla', 'Localización de fuga en Lacorzanilla', '2025-10-21', '2025-10-21', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Lacorzanilla', 5, 'ENEKO', 1, 1);

-- Registro 704/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0335', 3.0, 2, 7, 1, 1, 'Localización de fuga en Retes de Tudela', 'Localización de fuga en Retes de Tudela', '2025-10-21', '2025-10-21', 43.114828, -3.169099, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Retes de Tudela', 1, 'ENEKO', 1, 1);

-- Registro 705/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0454', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Llanteno', 'Reparación de fuga en Llanteno', '2025-10-16', '2025-10-17', 43.11148, -3.09272, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llanteno', 1, 'KERMAN', 1, 1);

-- Registro 706/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0455', 3.0, 1, 0, 1, 1, 'Abonado sin presión en C/Larrimbe n29 (Amurrio)', 'Abonado sin presión en C/Larrimbe n29 (Amurrio)', '2025-10-27', '2025-10-27', 43.0442, -2.98561, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'ENEKO', 1, 3);

-- Registro 707/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0456', 3.0, 1, 0, 5, 5, 'Aviso abonado por llave de acometida que no cierra C/El Arenal n1 (Armiñon)', 'Aviso abonado por llave de acometida que no cierra C/El Arenal n1 (Armiñon)', '2025-10-27', '2025-10-27', 42.72285, -2.87034, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Armiñon', 5, 'EDU', 1, 1);

-- Registro 708/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0336', 3.0, 2, 10, 1, 1, 'Sustitución de contador de control en C/Arraño (Acometida atxa)', 'Sustitución de contador de control en C/Arraño (Acometida atxa)', '2025-10-27', '2025-10-27', 43.151313, -2.983195, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 0);

-- Registro 709/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0337', 5.0, 2, 1, 5, 5, 'Mantenimiento peventivo en vias de tren en Pobes', 'Mantenimiento peventivo en vias de tren en Pobes', '2025-10-27', '2025-10-27', 42.504575, -2.907587, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Pobes', 5, 'EMILIO KERMAN', 1, 0);

-- Registro 710/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0338', 5.0, 2, 1, 1, 1, 'Mantenimiento peventivo en Saneamiento en Artzeniaga', 'Mantenimiento peventivo en Saneamiento en Artzeniaga', '2025-10-31', '2025-10-31', 43.11951, -3.1326, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, NULL, 1, 0);

-- Registro 711/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0457', 5.0, 1, 0, 1, 1, 'Desatasco en C/Virgen del Carmen N36-38 (Llodio)', 'Desatasco en C/Virgen del Carmen N36-38 (Llodio)', '2025-10-28', '2025-10-28', 43.14598, -2.95818, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'EMILIO KERMAN', 1, 2);

-- Registro 712/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0339', 3.0, 2, 4, 1, 1, 'Revisión de la red de abastecimiento de Llanteno', 'Revisión de la red de abastecimiento de Llanteno', '2025-10-22', '2025-10-22', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llanteno', 1, 'ENEKO', 1, 0);

-- Registro 713/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0340', 3.0, 2, 11, 1, 1, 'Ruta de lecturas mensuales de caudalímetro', 'Ruta de lecturas mensuales de caudalímetro', '2025-10-22', '2025-10-22', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Aiaraldea', 1, 'ENEKO', 1, 0);

-- Registro 714/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0341', 5.0, 2, 3, 9, 9, 'Revisión sistemas depuradores de fosas en Oreitia', 'Revisión sistemas depuradores de fosas en Oreitia', '2025-10-23', '2025-10-23', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Oreitia', 9, 'ENEKO', 1, 0);

-- Registro 715/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0342', 3.0, 2, 7, 5, 5, 'Localización de fuga en Arbigano', 'Localización de fuga en Arbigano', '2025-10-23', '2025-10-23', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Arbígano', 5, 'ENEKO', 1, 1);

-- Registro 716/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0458', 3.0, 1, 0, 5, 5, 'Colocación llave acometida en C/Juan de Lazcano n10-12 (Zambrana)', 'Colocación llave acometida en C/Juan de Lazcano n12 (Zambrana)', '2025-10-27', '2025-10-31', 42.661366, -2.877274, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Zambrana', 5, 'KERMAN', 1, 3);

-- Registro 717/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0343', 3.0, 2, 4, 1, 1, 'Digitalización de redes abastecimiento y saneamiento', 'Lekamaña,Onsoño,Pobes,Alegría', '2025-10-01', '2025-10-31', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Aiaraldea', 1, 'JORGE', 1, 0);

-- Registro 718/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0459', 3.0, 1, 0, 1, 1, 'Colocación de avisos de corte de agua en C/Isasi n20 (Llodio)', 'Colocación de avisos de corte de agua en C/Isasi n20 (Llodio)', '2025-10-28', '2025-10-28', 43.151114, -2.971358, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 3);

-- Registro 719/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0460', 5.0, 1, 0, 1, 1, 'Desatasco saneamiento es Esquina Abajo n24  en Respaldiza', 'Desatasco saneamiento es Esquina Abajo n24  en Respaldiza', '2025-10-28', '2025-10-28', 43.09734, -3.043772, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Respaldiza', 1, 'EMILIO KERMAN', 1, 2);

-- Registro 720/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0461', 3.0, 1, 0, 5, 5, 'Acondicionamiento asfalto en Espejo por cata de Facsa', 'Acondicionamiento asfalto en Espejo por cata de Facsa', '2025-10-28', '2025-10-28', 42.80826, -3.04628, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Espejo', 5, 'MIGUEL KERMAN EMILIO ALBERTO', 1, 3);

-- Registro 721/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0462', 3.0, 1, 0, 1, 1, 'Reparación de fuga en C/Aldai n1', 'Reparación de fuga en C/Aldai n1', '2025-10-27', '2025-10-27', 43.05119, -3.00224, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'KHARIM RAFNIR', 1, 1);

-- Registro 722/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0463', 3.0, 1, 0, 1, 1, 'Fugas C/Esquina Abajo en Respaldiza', 'Fugas C/Esquina Abajo en Respaldiza', '2025-10-28', '2025-10-28', 43.086793, -3.043155, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Respaldiza', 1, 'MIGUEL Y ZOUITA', 1, 1);

-- Registro 723/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0464', 3.0, 1, 0, 1, 1, 'Reparación de fuga en C/Esquina Abajo n109 en Respaldiza', 'Reparación de fuga en C/Esquina Abajo n109 en Respaldiza', '2025-10-29', '2025-10-29', 43.083544, -3.044371, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Respaldiza', 1, 'MIGUEL', 1, 1);

-- Registro 724/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0344', 3.0, 2, 9, 1, 1, 'Retirada de contador en la C/Pagolar n10 (Llodio)', 'Retirada de contador en la C/Pagolar n10 (Llodio)', '2025-10-29', '2025-10-29', 43.139766, -2.961409, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'KERMAN JUAN', 1, 0);

-- Registro 725/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0345', 3.0, 2, 8, 1, 1, 'Intalación de contador en C/Javier Zaballa n3 (Llodio)', 'Intalación de contador en C/Javier Zaballa n3 (Llodio)', '2025-10-29', '2025-10-29', 43.139608, -2.965761, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'KERMAN JUAN', 1, 0);

-- Registro 726/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0346', 5.0, 2, 1, 1, 1, 'Mantenimiento preventivo saneamiento C/Izoria (Llodio)', 'Mantenimiento preventivo saneamiento C/Izoria (Llodio)', '2025-10-29', '2025-10-29', 43.144912, -2.9598317, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'EMILIO', 1, 0);

-- Registro 727/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0347', 3.0, 2, 11, 1, 1, 'Lectura de contadores septoriales (Amurrio y Aiaraldea)', 'Lectura de contadores septoriales (Amurrio y Aiaraldea)', '2025-10-29', '2025-10-31', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Aiaraldea', 1, 'KERMAN JUAN', 1, 0);

-- Registro 728/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0348', 3.0, 2, 12, 1, 1, 'Corte de Agua en Erbi por obra', 'Corte de Agua en Erbi por obra', '2025-10-27', '2025-10-27', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Erbi', 1, 'IÑIGO MIGUEL', 1, 0);

-- Registro 729/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0465', 3.0, 1, 0, 5, 5, 'Reparación de fuga en bajada depósito Arbígano', 'Reparación de fuga en bajada depósito Arbígano', '2025-10-27', '2025-10-27', 42.804418, -2.933458, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Arbígano', 5, 'MIGUEL IÑIGO', 1, 1);

-- Registro 730/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0466', 5.0, 1, 0, 1, 1, 'Desatasco saneamiento en C/Nervion n10 (Llodio)', 'Desatasco saneamiento en C/Nervion n10 (Llodio)', '2025-10-29', '2025-10-29', 43.142269, -2.962026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'EMILIO KERMAN TOMAS JUAN', 1, 2);

-- Registro 731/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0467', 1.0, 1, 0, 1, 1, 'Reparación de fuga en Lejarzo', 'Reparación de fuga en Lejarzo', '2025-10-30', '2025-10-31', 43.057961, -3.121699, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Lejarzo', 1, NULL, 1, 1);

-- Registro 732/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0468', 3.0, 1, 0, 1, 1, 'Instalación de tubería nueva para Larrinbe 29', 'Instalación de tubería nueva para Larrinbe 29', '2025-10-29', '2025-10-30', 43.044117, -2.98606, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'KERMAN', 1, 3);

-- Registro 733/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0349', 5.0, 2, 1, 1, 1, 'Mantenimiento preventivo saneamiento C/Fronton y Jose Madinabeitia (Amurrio)', 'Mantenimiento preventivo saneamiento C/Fronton y Jose Madinabeitia (Amurrio)', '2025-10-30', '2025-10-30', 43.053568, -3.00137, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'EMILIO RAFIN', 1, 0);

-- Registro 734/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0350', 3.0, 2, 13, 1, 1, 'Asistencia técnica a obra en ambulatorio OSAKIDETZA (Llodio)', 'Asistencia técnica a obra en ambulatorio OSAKIDETZA (Llodio)', '2025-10-30', '2025-10-30', 43.146759, -2.958293, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'IÑIGO', 1, 0);

-- Registro 735/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0351', 3.0, 2, 12, 1, 1, 'Corte de agua en C/Isasi n20 (Llodio)', 'Corte de agua en C/Isasi n20 (Llodio)', '2025-10-30', '2025-10-30', 43.151089, -2.971375, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'IÑIGO', 1, 0);

-- Registro 736/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0352', 3.0, 2, 12, 3, 3, 'Asistencia técnica para corte de agua ambulatorio Agurain', 'Asistencia técnica para corte de agua ambulatorio Agurain', '2025-10-29', '2025-10-29', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 'EDUARDO', 1, 0);

-- Registro 737/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0353', 3.0, 2, 13, 1, 1, 'Obra en parque Lamuza C/Lamuza en Llodio', 'Obra en parque Lamuza C/Lamuza en Llodio', '2025-10-30', '2025-11-05', 43.144102, -2.964035, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 0);

-- Registro 738/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0354', 3.0, 2, 13, 1, 1, 'Asistencia técnico en C/Nervión n10 (Llodio)', 'Asistencia técnico en C/Nervión n10 (Llodio)', '2025-10-30', '2025-10-30', 43.142269, -2.962026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 0);

-- Registro 739/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0355', 2.0, 2, 23, 1, 1, 'Limpieza y revisión tamices en Ozeka,Añes,Madaria,Onsoñoy Lejarzo', 'Limpieza y revisión tamices en Ozeka,Añes,Madaria,Onsoñoy Lejarzo', '2025-10-29', '2025-10-29', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ozeka', 1, 'MIGUEL', 1, 0);

-- Registro 740/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0356', 3.0, 2, 8, 1, 1, 'Instalación de contador en C/Etxegoienbidea n1 Amurrio', 'Instalación de contador en C/Etxegoienbidea n1 Amurrio', '2025-10-30', '2025-10-30', 43.051106, -3.00293, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'KERMAN', 1, 0);

-- Registro 741/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0357', 3.0, 2, 8, 1, 1, 'Instalación de contador en C/San Jose n12 (Amurrio)', 'Instalación de contador en C/San Jose n12 (Amurrio)', '2025-10-30', '2025-10-30', 43.059981, -2.998891, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'KERMAN', 1, 0);

-- Registro 742/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0358', 3.0, 2, 8, 1, 1, 'Instalación de contador en C/Jose Picaza n11 (Amurrio)', 'Instalación de contador en C/Jose Picaza n11 (Amurrio)', '2025-10-30', '2025-10-30', 43.0534, -3.004714, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'KERMAN', 1, 0);

-- Registro 743/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0469', 3.0, 1, 0, 3, 3, 'Reparación de fuga en C/Gazteiz n1 en Alegría', 'Reparación de fuga en C/Gazteiz n1 en Alegría', '2025-10-26', '2025-10-30', 42.841405, -2.513207, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 3, 'MIGUEL EDU', 1, 1);

-- Registro 744/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0470', 3.0, 1, 0, 5, 5, 'Reparación de fuga en C/Puente n2b en Armiñon', 'Reparación de fuga en C/Puente n2b en Armiñon', '2025-10-27', '1900-01-01', 42.72313, -2.87407, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 'Armiñon', 5, 'EDU ZOUITA BEÑAT', 1, 1);

-- Registro 745/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0471', 3.0, 1, 0, 1, 1, 'Sustitución de VRP en C/El Puente en Armiñon', 'Sustitución de VRP en C/El Puente en Armiñon', '2025-10-28', '2025-10-28', 42.722602, -2.876258, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'IÑIGO EDU', 1, 3);

-- Registro 746/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0359', 5.0, 2, 1, 1, 1, 'Mantenimiento preventivo saneamiento en Lekamaña (Amurrio)', 'Mantenimiento preventivo saneamiento en Lekamaña', '2025-10-31', '2025-10-31', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, NULL, 1, 0);

-- Registro 747/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0472', 3.0, 1, 0, 1, 1, 'Reparación de Fuga y reparación del tubo de saneamiento en Barrio Lekamaña en Amurrio', 'Reparación de Fuga y reparación del tubo de saneamiento en Barrio Lekamaña en Amurrio', '2025-10-30', '2025-10-31', 43.024181, -2.991913, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'KERMAN RAFHIR KARIM', 1, 1);

-- Registro 748/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0473', 2.0, 1, 0, 5, 5, 'Desatasco en Corro a la entrada de la fosa', 'Desatasco en Corro a la entrada de la fosa', '2025-10-31', '2025-10-31', 42.878242, -3.172295, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Corro', 5, 'MIGUEL RAFIR', 1, 2);

-- Registro 749/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0474', 3.0, 1, 0, 1, 1, 'Reparación de fuga junto al depósito de Artziniega', 'Reparación de fuga junto al depósito de Artziniega', '2025-10-31', '2025-10-31', 43.122805, -3.136286, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 'KERMAN', 1, 1);

-- Registro 750/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0360', 3.0, 2, 18, 1, 1, 'Ejecución y conexión acometida nueva en Murga n58', 'Ejecución y conexión acometida nueva en Murga n58', '2025-10-31', '2025-10-31', 43.07106, -3.0218, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Murga', 1, 'IÑIGO', 1, 0);

-- Registro 751/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0361', 3.0, 2, 17, 6, 6, 'Limpieza de red en Maeztu por aviso de cal', 'Limpieza de red en Maeztu por aviso de cal', '2025-10-23', '2025-10-23', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maeztu', 6, NULL, 1, 0);

-- Registro 752/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0362', 3.0, 2, 9, 1, 1, 'Desistalación de contador en C/Fronton n4 (Amurrio)', 'Desistalación de contador en C/Fronton n4 (Amurrio)', '2025-10-31', '2025-10-31', 43.053407, -3.001259, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'KERMAN', 1, 0);

-- Registro 753/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0475', 3.0, 1, 0, 1, 1, 'Reparación de fuga en C/Mendiko n49 (Amurrio)', 'Reparación de fuga en C/Mendiko n49 (Amurrio)', '2025-10-30', '2025-10-30', 43.06008, -3.00395, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'KERMAN JUAN RAFNIR', 1, 1);

-- Registro 754/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0476', 3.0, 1, 0, 5, 5, 'Sustitución VRP en Armiñon', 'Sustitución VRP en Armiñon', '2025-10-28', '2025-11-28', 42.722602, -2.876258, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Armiñon', 5, 'EDUARDO IÑIGO', 1, 3);

-- Registro 755/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0477', 5.0, 1, 0, 1, 1, 'Desatasco restaurante Maroño', 'Desatasco restaurante Maroño', '2025-11-01', '2025-11-01', 43.052153, -3.059349, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maroño', 1, 'KERMAN MANUEL', 1, 2);

-- Registro 756/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0478', 5.0, 1, 0, 1, 1, 'Vertido al río en C/Zalibar (Amurrio)', 'Vertido al río en C/Zalibar (Amurrio)', '2025-11-01', '2025-11-01', 43.06411, -2.99166, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'V', 1, 1);

-- Registro 757/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0479', 3.0, 1, 0, 6, 6, 'Fuga en Maeztu', 'Fuga en Maeztu', '2025-11-01', '1900-01-01', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maeztu', 6, 'V', 1, 1);

-- Registro 758/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0480', 3.0, 1, 0, 5, 5, 'Reposición de catas en llaves de acometida en C/Juan Lazcano n10 en Zambrana', 'Reposición de catas en llaves de acometida en C/Juan Lazcano n10 en Zambrana', '2025-10-31', '2025-10-31', 42.662074, -2.878043, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Zambrana', 5, NULL, 1, 3);

-- Registro 759/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0363', 5.0, 2, 1, 5, 5, 'Mantenimiento preventivo saneamiento en Corro', 'Mantenimiento preventivo saneamiento en Corro', '2025-11-03', '2025-11-03', 42.878863, -3.171893, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Corro', 5, NULL, 1, 0);

-- Registro 760/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0481', 5.0, 1, 0, 5, 5, 'Atasco en Espejo', 'Atasco en Espejo', '2025-11-02', '2025-11-02', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Espejo', 5, 'V', 1, 2);

-- Registro 761/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0482', 3.0, 1, 0, 1, 1, 'Fuga en Erbi', 'Fuga en Erbi', '2025-11-02', '2025-11-02', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Erbi', 1, 'V', 1, 1);

-- Registro 762/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0483', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Sojoguti (Artziniega)', 'Reparación de fuga en Sojoguti (Artziniega)', '2025-10-29', '2025-10-29', 43.11387, -3.127162, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 'KERMAN JUAN', 1, 1);

-- Registro 763/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0364', 3.0, 2, 14, 1, 1, 'Maniobras para dejar fuera de servicio anillo obra Lamuza (Llodio)', 'Maniobras para dejar fuera de servicio anillo obra Lamuza (Llodio)', '2025-11-03', '2025-11-03', 43.138126, -2.966805, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS IÑIGO', 1, 0);

-- Registro 764/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0484', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Barrio C/Las Llanas n19 (Respaldiza)', 'Reparación de fuga en Barrio C/Las Llanas n19 (Respaldiza)', '2025-11-03', '2025-11-03', 43.075833, -3.043474, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Respaldiza', 1, 'IÑIGO BEÑAT', 1, 1);

-- Registro 765/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0365', 5.0, 2, 1, 1, 1, 'Mantenimiento preventivo saneamiento en Llodio', 'Mantenimiento preventivo saneamiento en Llodio', '2025-11-03', '2025-11-03', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'IÑIGO', 1, 0);

-- Registro 766/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0366', 3.0, 2, 10, 1, 1, 'Sustitución de contador en Barrio C/Las Llanas n19 (Respaldiza)', 'Sustitución de contador en Barrio C/Las Llanas n19 (Respaldiza)', '2025-11-03', '2025-11-03', 43.075833, -3.043474, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Respaldiza', 1, 'IÑIGO', 1, 0);

-- Registro 767/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0485', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Erbi', 'Reparación de fuga en Erbi', '2025-11-03', '2025-11-03', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Erbi', 1, 'IÑIGO', 1, 1);

-- Registro 768/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0486', 3.0, 1, 0, 1, 1, 'Reparación de fuga en C/Maskuribai n1 (Amurrio)', 'Reparación de fuga en C/Maskuribai n1 (Amurrio)', '2025-10-31', '2025-11-03', 43.050671, -2.999931, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, NULL, 1, 1);

-- Registro 769/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0367', 3.0, 2, 12, 5, 5, 'Corte de agua en Estabillo C/La Picota', 'Corte de agua en Estabillo C/La Picota', '2025-10-11', '2025-10-11', 42.728534, -2.861591, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Estabillo', 5, 'V', 1, 0);

-- Registro 770/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0487', 5.0, 1, 0, 1, 1, 'Atasco en luiando zona Bar (Las Vegas)', 'Atasco en luiando zona Bar (Las Vegas)', '2025-10-29', '2025-10-29', 43.105146, -2.996815, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Luiando', 1, 'V', 1, 2);

-- Registro 771/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0488', 5.0, 1, 0, 1, 1, 'Atasco en salida urb.Palacio en Artziniega', 'Atasco en salida urb.Palacio en Artziniega', '2025-10-29', '2025-10-29', 43.120704, -3.132908, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 'V', 1, 2);

-- Registro 772/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0489', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Murga poligono', 'Reparación de fuga en Murga poligono', '2025-10-30', '2025-10-31', 43.067713, -3.022557, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Murga', 1, 'V', 1, 1);

-- Registro 773/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0490', 3.0, 1, 0, 5, 5, 'Reparación de fuga en Sobron', 'Reparación de fuga en Sobron', '2025-10-30', '2025-10-30', 42.762095, -3.088856, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Sobron', 5, 'V', 1, 1);

-- Registro 774/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0491', 5.0, 1, 0, 1, 1, 'Atasco Delika', 'Atasco Delika', '2025-10-30', '2025-10-30', 42.968293, -2.989891, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Delika', 1, 'V', 1, 2);

-- Registro 775/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0368', 1.0, 2, 2, 1, 1, 'Limpieza de captaciones Aiaraldea', 'Limpieza de captaciones Aiaraldea', '2025-10-31', '2025-10-31', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Aiaraldea', 1, 'V', 1, 0);

-- Registro 776/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0369', 3.0, 2, 17, 1, 1, 'Limpieza de red en Avda.Zumalakarregui (Llodio)', 'Limpieza de red en Avda.Zumalakarregui (Llodio)', '2025-11-03', '2025-11-03', 43.138525, -2.96734, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, NULL, 1, 0);

-- Registro 777/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0370', 3.0, 2, 17, 1, 1, 'Limpieza de red por avisos turbidez por maniobras (Gardea y Katuxa Ibarra) en Llodio', 'Limpieza de red por avisos turbidez por maniobras (Gardea y Katuxa Ibarra) en Llodio', '2025-11-04', '2025-11-04', 43.133224, -2.971361, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, NULL, 1, 0);

-- Registro 778/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0371', 3.0, 2, 9, 1, 1, 'Retirada de contador en C/Izoria n2 (Llodio)', 'Retirada de contador en C/Izoria n2 (Llodio)', '2025-11-04', '2025-11-04', 43.14512, -2.95962, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, NULL, 1, 0);

-- Registro 779/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0372', 5.0, 2, 3, 3, 3, 'Revisión del estado de Fosa en Cuencas Mediterraneas', 'Revisión del estado de Fosa en Cuencas Mediterraneas', '2025-10-31', '2025-10-31', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Cuencas Mediterraneas', 3, 'ENEKO', 1, 0);

-- Registro 780/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0373', 3.0, 2, 24, 5, 5, 'Verificación de presión de la red de abastecimiento en Armiñon', 'Verificación de presión de la red de abastecimiento en Armiñon', '2025-10-30', '2025-10-30', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Armiñon', 5, 'ENEKO', 1, 0);

-- Registro 781/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0374', 3.0, 2, 7, 5, 5, 'Localización de fuga en la depuradora de DFA  en Berantevilla', 'Localización de fuga en la depuradora de DFA  en Berantevilla', '2025-11-03', '2025-11-03', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Berantevilla', 5, 'ENEKO', 1, 1);

-- Registro 782/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0375', 3.0, 2, 11, 3, 3, 'Lectura contadores sectoriales en Cuencas Mediterraneas', 'Lectura contadores sectoriales en Cuencas Mediterraneas', '2025-10-30', '2025-10-30', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Cuencas Mediterraneas', 3, 'ENEKO', 1, 0);

-- Registro 783/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0492', 5.0, 1, 0, 5, 5, 'Sustitución de tubería de saneamiento en C/Santa Lucia en Espejo', 'Sustitución de tubería de saneamiento en C/Santa Lucia en Espejo', '2025-10-06', '2025-10-10', 42.809366, -3.044435, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Espejo', 5, NULL, 1, 3);

-- Registro 784/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0493', 3.0, 1, 0, 1, 1, 'Sustitución de hidrante en caminos viejos en Llodio', 'Sustitución de hidrante en caminos viejos en Llodio', '2025-10-22', '2025-10-23', 43.148367, -2.952608, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, NULL, 1, 3);

-- Registro 785/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0494', 5.0, 1, 0, 1, 1, 'Reparación de fuga en Lezarrega en Amurrio', 'Reparación de fuga en Lezarrega en Amurrio', '2025-10-13', '2025-10-13', 43.05023, -3.007654, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, NULL, 1, 1);

-- Registro 786/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0376', 2.0, 2, 23, 1, 1, 'Limpieza de Tamices en Añes,Kostera,Ozeka,Madaria,Antoñana,Delika,Artziniega y Lejarzo', 'Limpieza de Tamices en Añes,Kostera,Ozeka,Madaria,Antoñana,Delika,Artziniega y Lejarzo', '2025-10-30', '2025-10-31', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Aiaraldea', 1, NULL, 1, 0);

-- Registro 787/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0495', 3.0, 1, 0, 3, 3, 'Sustitución de boca de riego en C/Urzabal Kalea (Agurain)', 'Sustitución de boca de riego en Urzabal Kalea (Agurain)', '2025-10-21', '2025-10-21', 42.84892, -2.392219, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, NULL, 1, 3);

-- Registro 788/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0496', 5.0, 1, 0, 1, 1, 'Reparación de tapas de saneamiento C/Landaluce en Llodio', 'Reparación de tapas de saneamiento C/Landaluce en Llodio', '2025-10-08', '2025-10-08', 43.142077, -2.973372, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, NULL, 1, 3);

-- Registro 789/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0497', 3.0, 1, 0, 5, 5, 'Colocación de llave de acometida en C/Juan Lazcano n12 en Zambrana', 'Colocación de llave de acometida en C/Juan Lazcano n12 en Zambrana', '2025-11-03', '2025-11-03', 42.662074, -2.878043, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Zambrana', 5, 'KERMAN', 1, 3);

-- Registro 790/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0498', 5.0, 1, 0, 1, 1, 'Desatasco saneamiento en Artziniega', 'Desatasco saneamiento en Artziniega', '2025-11-03', '2025-11-03', 43.122096, -3.125956, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 'KERMAN,MIGUEL,ANGEL', 1, 2);

-- Registro 791/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0377', 3.0, 2, 9, 1, 1, 'Desistalación de contadores por baja en C/Jesus Galindez n3 en Amurrio', 'Desistalación de contadores por baja en C/Jesus Galindez n3 en Amurrio', '2025-11-03', '2025-11-03', 43.05184, -3.00418, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'KERMAN', 1, 0);

-- Registro 792/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0499', 5.0, 1, 0, 1, 1, 'Reparación de arqueta de saneamiento en Artziniega', 'Reparación de arqueta de saneamiento en Artziniega', '2025-11-04', '2025-11-04', 43.121775, -3.126393, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Artziniega', 1, 'ZOUITA BEÑAT REGOMART', 1, 3);

-- Registro 793/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0500', 3.0, 1, 0, 1, 1, 'Reparación de fuga en C/Elexondo en Amurrio', 'Reparación de fuga en C/Elexondo en Amurrio', '2025-11-04', '2025-11-04', 43.051872, -3.001577, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'IÑIGO', 1, 1);

-- Registro 794/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0501', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Baranbio', 'Reparación de fuga en Baranbio', '2025-11-04', '2025-11-04', 43.04588, -2.914159, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Baranbio', 1, 'IÑIGO', 1, 1);

-- Registro 795/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0502', 1.0, 1, 0, 1, 1, 'Reparación de fuga en Erbi en agua bruta', 'Reparación de fuga en Erbi en agua bruta', '2025-11-04', '2025-11-04', 43.076608, -3.107515, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Erbi', 1, 'IÑIGO', 1, 1);

-- Registro 796/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0378', 1.0, 2, 12, 1, 1, 'Corte de agua por rotura de tubería de aducción en Erbi', 'Corte de agua por rotura de tubería de aducción en Erbi', '2025-11-04', '2025-11-04', 43.07462, -3.11342, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Erbi', 1, 'IÑIGO', 1, 0);

-- Registro 797/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0379', 5.0, 2, 1, 3, 3, 'Recopilación de informacion para mejoras de las redes pluviales y fecales en Alegría', 'Recopilación de informacion para mejoras de las redes pluviales y fecales en Alegría', '2025-10-28', '2025-10-29', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegría', 3, 'ENEKO', 1, 0);

-- Registro 798/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0503', 5.0, 1, 0, 6, 6, 'Reparación de tapas de saneamiento en Maeztu', 'Reparación de tapas de saneamiento en Maeztu', '2025-10-15', '2025-10-17', 42.739217, -2.446961, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Maeztu', 6, NULL, 1, 3);

-- Registro 799/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0504', 5.0, 1, 0, 1, 1, 'Revisión saneamiento C/Nervión por aviso de filtraciones en Llodio', 'Revisión saneamiento C/Nervión por aviso de filtraciones en Llodio', '2025-11-05', '2025-11-05', 43.142116, -2.962116, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS IÑIGO KERMAN ANGEL', 1, 3);

-- Registro 800/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0380', 3.0, 2, 13, 1, 1, 'Asistencia técnica a organismos públicos y URBIDE', 'Asistencia técnica a organismos públicos y URBIDE', '2025-11-05', '2025-11-05', 43.131611, -2.967948, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'IÑIGO', 1, 0);

-- Registro 801/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0505', 5.0, 1, 0, 1, 1, 'Aviso de vertido en Ugarte en Llodio', 'Aviso de vertido en Ugarte en Llodio', '2025-11-05', '2025-11-05', 43.148433, -2.969549, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'IÑIGO KERMAN', 1, 1);

-- Registro 802/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0381', 2.0, 2, 1, 1, 1, 'Vaciado de fosa séptica en Lateorro en Llodio', 'Vaciado de fosa séptica en Lateorro en Llodio', '2025-11-05', '2025-11-05', 43.138487, -2.962412, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, NULL, 1, 0);

-- Registro 803/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0506', 3.0, 1, 0, 3, 3, 'Comprobación de fuga en contador en C/Santa Barbara  n1 en Agurain', 'Comprobación de fuga en contador en Santa Barbara  n1  en Agurain', '2025-11-05', '2025-11-05', 42.84876, -2.38994, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, NULL, 1, 1);

-- Registro 804/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0382', 3.0, 2, 10, 4, 4, 'Sustitución de contador en C/Santiagolarra n1 en Ullibarri-Gamboa', 'Sustitución de contador en C/Santiagolarra n1 en Ullibarri-Gamboa', '2025-11-05', '2025-11-05', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ullibarri-Gamboa', 4, 'GABI', 1, 0);

-- Registro 805/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0383', 3.0, 2, 10, 3, 3, 'Sustitución de contador en C/Zapatari n25 en Agurain', 'Sustitución de contador en C/Zapatari n25 en Agurain', '2025-11-05', '2025-11-05', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 'GABI', 1, 0);

-- Registro 806/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0384', 3.0, 2, 10, 3, 3, 'Sustitución de contador en C/Bitikuri n8 en Argomaniz', 'Sustitución de contador en C/Bitikuri n8 en Argomaniz', '2025-11-05', '2025-11-05', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Argomaniz', 3, 'GABI', 1, 0);

-- Registro 807/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0507', 3.0, 1, 0, 6, 6, 'Reparación de fuga en C/Bengara n9A en Apellaniz', 'Reparación de fuga en C/Bengara n9A en Apellaniz', '2025-11-05', '2025-11-05', 42.733064, -2.483158, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Apellaniz', 6, 'GABI', 1, 1);

-- Registro 808/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0508', 3.0, 1, 0, 5, 5, 'Reparación de fuga en contador en C/Colina n2 en Corro', 'Reparación de fuga en contador en C/Colina n2 en Corro', '2025-11-04', '2025-11-04', 42.880167, -3.171235, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Corro', 5, 'GABI', 1, 1);

-- Registro 809/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0509', 3.0, 1, 0, 5, 5, 'Reparación de fuga en contador en C/Alaguero n2 en Villanañe', 'Reparación de fuga en contador en C/Alaguero n2 en Villanañe', '2025-11-04', '2025-11-04', 42.83614, -3.07323, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Villanañe', 5, 'GABI', 1, 1);

-- Registro 810/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0510', 3.0, 1, 0, 5, 5, 'Reparación de fuga en contador en C/Alaguero n4 en Villanañe', 'Reparación de fuga en contador en C/Alaguero n4 en Villanañe', '2025-11-04', '2025-11-04', 42.835974, -3.072979, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Villanañe', 5, 'GABI', 1, 1);

-- Registro 811/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0385', 3.0, 2, 10, 5, 5, 'Sustitución de contador en C/Buenos Aires n8 en Lecicaña', 'Sustitución de contador en C/Buenos Aires n8 en Lecicaña', '2025-11-04', '2025-11-04', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Lecicaña', 5, 'GABI', 1, 0);

-- Registro 812/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0511', 3.0, 1, 0, 5, 5, 'Reparación de fuga en contador en Barrio del Campo n6 en Ocio', 'Reparación de fuga en contador en Barrio del Campo n6 en Ocio', '2025-11-04', '2025-11-04', 42.655643, -2.822465, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ocio', 5, 'GABI', 1, 1);

-- Registro 813/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0512', 3.0, 1, 0, 5, 5, 'Reparación de fuga en válvula de contador en C/Real n13 en Armiñon', 'Reparación de fuga en válvula de contador en C/Real n13 en Armiñon', '2025-11-06', '2025-11-06', 42.72218, -2.872695, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Armiñon', 5, 'GABI', 1, 1);

-- Registro 814/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0513', 3.0, 1, 0, 1, 1, 'Reparación de fuga en Erbi', 'Reparación de fuga en Erbi', '2025-11-06', '2025-11-06', 43.073281, -3.108409, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Erbi', 1, 'IÑIGO', 1, 1);

-- Registro 815/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0386', 5.0, 2, 1, 3, 3, 'Localizar acometidas saneamiento ,pluviales en Alegría', 'Localizar acometidas saneamiento ,pluviales en Alegría', '2025-11-06', '2025-11-06', 42.843777, -2.511185, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Alegria', 3, 'ANGEL Y KERMAN', 1, 0);

-- Registro 816/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0514', 3.0, 1, 0, 1, 1, 'Aviso por turbidez en Katuxa Ibarra (Palacio) en Llodio', 'Aviso por turbidez en Katuxa Ibarra (Palacio) en Llodio', '2025-11-06', '2025-11-06', 43.133439, -2.970685, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Llodio', 1, 'TOMAS', 1, 3);

-- Registro 817/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0515', 3.0, 1, 0, 1, 1, 'Reparación de fuga en C/Aldai n26 en Amurrio', 'Reparación de fuga en C/Aldai n26 en Amurrio', '2025-11-06', '1900-01-01', 43.047975, -3.004419, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Amurrio', 1, 'IÑIGO BEÑAT', 1, 1);

-- Registro 818/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0516', 3.0, 1, 0, 5, 5, 'Aviso fuga en Espejo', 'Aviso fuga en Espejo', '2025-11-09', '2025-11-09', 42.808616, -3.049801, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Espejo', 5, NULL, 1, 1);

-- Registro 819/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0517', 1.0, 1, 0, 1, 1, 'Aviso de fuga en Erbi', 'Aviso de fuga en Erbi', '2025-11-09', '2025-11-09', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Erbi', 1, NULL, 1, 1);

-- Registro 820/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0518', 5.0, 1, 0, 5, 5, 'Atasco y vaciado de fosa bar sociedad en Sobrón', 'Atasco y vaciado de fosa bar sociedad en Sobrón', '2025-11-09', '2025-11-09', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Sobrón', 5, NULL, 1, 2);

-- Registro 821/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0519', 3.0, 1, 0, 3, 3, 'Aviso abonados sin agua en C/Zenbidea en Argómaniz', 'Aviso abonados sin agua en C/Zenbidea en Argómaniz', '2025-11-08', '2025-11-08', 42.86748, -2.540494, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Argómaniz', 3, NULL, 1, 3);

-- Registro 822/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0520', 3.0, 1, 0, 1, 1, 'Reparación de fuga en el Molino (Zuaza)', 'Reparación de fuga en el Molino (Zuaza)', '2025-11-07', '2025-11-07', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Zuaza', 1, NULL, 1, 1);

-- Registro 823/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0521', 3.0, 1, 0, 3, 3, 'Reparación de fuga en Hijona', 'Reparación de fuga en Hijona', '2025-11-04', '2025-11-04', 42.814362, -2.546582, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Hijona', 3, 'EDUARDO MIGUEL', 1, 1);

-- Registro 824/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('OT/0522', 3.0, 1, 0, 3, 3, 'Reparación de fuga en Agurain', 'Reparación de fuga en Agurain', '2025-11-08', '2025-11-08', 42.857115, -2.38781, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Agurain', 3, 'EDUARDO MIGUEL', 1, 1);

-- Registro 825/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0387', 3.0, 2, 24, 5, 5, 'Revisión y verificación de contador en Rivabellosa', 'Revisión y verificación de contador en Rivabellosa', '2025-11-06', '2025-11-06', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ribabellosa', 5, NULL, 1, 0);

-- Registro 826/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0388', 3.0, 2, 10, 6, 6, 'Sustitución de contador C/Andra Mari n8 en Ullibarri Arana', 'Sustitución de contador C/Andra Mari n8 en Ullibarri Arana', '2025-11-07', '2025-11-07', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Ullibarri Arana', 6, NULL, 1, 0);

-- Registro 827/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0389', 3.0, 2, 10, 5, 5, 'Sustitución de contador C/Ires Palacios n6 Salinas de Añana', 'Sustitución de contador C/Ires Palacios n6 Salinas de Añana', '2025-11-07', '2025-11-07', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Salinas de Añana', 5, NULL, 1, 0);

-- Registro 828/828
INSERT INTO cert_dev.tbl_partes (codigo, red_id, tipo_trabajo_id, cod_trabajo_id, comarca_id, municipio_id, titulo, descripcion, fecha_inicio, fecha_fin, latitud, longitud, estado, observaciones, created_at, updated_at, descripcion_larga, descripcion_corta, id_estado, finalizada, localizacion, id_municipio, trabajadores, provincia_id, tipo_rep_id)
VALUES ('TP/0390', 3.0, 2, 10, 5, 5, 'Sustitución de contador C/Real n17 en Armiñon', 'Sustitución de contador C/Real n17 en Armiñon', '2025-11-07', '2025-11-07', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Armiñon', 5, 'GABI', 1, 0);


-- ============================================================================
-- FINALIZACIÓN
-- ============================================================================

COMMIT;
SET FOREIGN_KEY_CHECKS = 1;

-- Verificar inserción
SELECT COUNT(*) as 'Total registros en tbl_partes' FROM cert_dev.tbl_partes;

-- Mostrar últimos registros insertados
SELECT * FROM cert_dev.tbl_partes ORDER BY id DESC LIMIT 10;

-- ============================================================================
-- Script completado exitosamente
-- ============================================================================
