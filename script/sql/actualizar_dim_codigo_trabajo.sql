-- Script para actualizar las descripciones de dim_codigo_trabajo
-- Este script actualiza los 22 códigos de trabajo con sus descripciones correctas
--
-- Uso: Ejecutar este script en cada base de datos de proyecto que necesite actualización
-- mysql -u [usuario] -p [nombre_db] < actualizar_dim_codigo_trabajo.sql

-- Primero, limpiamos la tabla para asegurar datos consistentes
TRUNCATE TABLE dim_codigo_trabajo;

-- Resetear el AUTO_INCREMENT
ALTER TABLE dim_codigo_trabajo AUTO_INCREMENT = 1;

-- Insertar los 22 códigos de trabajo con sus descripciones correctas
INSERT INTO dim_codigo_trabajo (codigo, descripcion, activo) VALUES
('1', 'Mantenimiento preventivo saneamiento', 1),
('2', 'Limpieza captaciones', 1),
('3', 'Mantenimiento fosas sépticas', 1),
('4', 'Inventario y digitalización redes abastecimiento', 1),
('5', 'Inventario y digitalización redes saneamiento', 1),
('6', 'Inventario y digitalización aducción', 1),
('7', 'Localización fugas abastecimiento', 1),
('8', 'Instalación contadores', 1),
('9', 'Desinstalación contadores', 1),
('10', 'Sustitución contadores', 1),
('11', 'Lectura contadores sectoriales', 1),
('12', 'Cortes de agua', 1),
('13', 'Asistencia técnica a URBIDE y organismos públicos', 1),
('14', 'Maniobras válvulas', 1),
('15', 'Gestión de la explotación', 1),
('16', 'Limpieza colectores pluviales', 1),
('17', 'Limpieza de red abastecimiento', 1),
('18', 'Ejecución y conexión acometida', 1),
('19', 'Revisión de sectores', 1),
('20', 'Localización de fugas en Saneamiento', 1),
('21', 'Realización de informes de Saneamiento', 1),
('22', 'Realización de informes de Abastecimiento', 1);

-- Verificar la inserción
SELECT COUNT(*) as total_codigos_trabajo FROM dim_codigo_trabajo;
SELECT * FROM dim_codigo_trabajo ORDER BY id;
