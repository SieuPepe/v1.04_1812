-- Script SEGURO para actualizar las descripciones de dim_codigo_trabajo
-- Este script actualiza solo las descripciones sin eliminar registros
-- Útil cuando hay referencias de claves foráneas activas
--
-- Uso: Ejecutar este script en cada base de datos de proyecto que necesite actualización
-- mysql -u [usuario] -p [nombre_db] < actualizar_dim_codigo_trabajo_seguro.sql

-- Actualizar los 22 códigos de trabajo con sus descripciones correctas
-- Si el registro existe (por id), lo actualiza; si no existe, lo inserta

INSERT INTO dim_codigo_trabajo (id, codigo, descripcion, activo) VALUES
(1, '1', 'Mantenimiento preventivo saneamiento', 1),
(2, '2', 'Limpieza captaciones', 1),
(3, '3', 'Mantenimiento fosas sépticas', 1),
(4, '4', 'Inventario y digitalización redes abastecimiento', 1),
(5, '5', 'Inventario y digitalización redes saneamiento', 1),
(6, '6', 'Inventario y digitalización aducción', 1),
(7, '7', 'Localización fugas abastecimiento', 1),
(8, '8', 'Instalación contadores', 1),
(9, '9', 'Desinstalación contadores', 1),
(10, '10', 'Sustitución contadores', 1),
(11, '11', 'Lectura contadores sectoriales', 1),
(12, '12', 'Cortes de agua', 1),
(13, '13', 'Asistencia técnica a URBIDE y organismos públicos', 1),
(14, '14', 'Maniobras válvulas', 1),
(15, '15', 'Gestión de la explotación', 1),
(16, '16', 'Limpieza colectores pluviales', 1),
(17, '17', 'Limpieza de red abastecimiento', 1),
(18, '18', 'Ejecución y conexión acometida', 1),
(19, '19', 'Revisión de sectores', 1),
(20, '20', 'Localización de fugas en Saneamiento', 1),
(21, '21', 'Realización de informes de Saneamiento', 1),
(22, '22', 'Realización de informes de Abastecimiento', 1)
ON DUPLICATE KEY UPDATE
    codigo = VALUES(codigo),
    descripcion = VALUES(descripcion),
    activo = VALUES(activo);

-- Desactivar registros antiguos si existen (id > 22)
UPDATE dim_codigo_trabajo
SET activo = 0
WHERE id > 22;

-- Verificar la actualización
SELECT COUNT(*) as total_codigos_trabajo_activos FROM dim_codigo_trabajo WHERE activo = 1;
SELECT * FROM dim_codigo_trabajo ORDER BY id;
