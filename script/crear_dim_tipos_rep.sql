-- ============================================================================
-- Script para crear la dimensión dim_tipos_rep (Tipos de Reparación)
-- Esta tabla categoriza los partes según el tipo de reparación
-- Valores: Fuga, Atasco, Otros
--
-- USO:
-- Para cert_dev:    mysql -u root -phydroflow cert_dev < crear_dim_tipos_rep.sql
-- Para proyecto_tipo: mysql -u root -phydroflow proyecto_tipo < crear_dim_tipos_rep.sql
-- Para cualquier esquema: Reemplazar 'cert_dev' abajo con el nombre del esquema
-- ============================================================================

-- IMPORTANTE: Edita esta línea con el nombre de tu esquema
SET @schema_name = DATABASE();  -- Usa el esquema activo de la conexión

-- Crear tabla dim_tipos_rep
SELECT CONCAT('Creando tabla dim_tipos_rep en esquema: ', @schema_name) AS Info;

CREATE TABLE IF NOT EXISTS dim_tipos_rep (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50),
    descripcion VARCHAR(255) NOT NULL,
    activo TINYINT DEFAULT 1,
    INDEX idx_codigo (codigo),
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Poblar con los 3 tipos de reparación
INSERT INTO dim_tipos_rep (codigo, descripcion, activo)
VALUES
    ('FUGA', 'Fuga', 1),
    ('ATASCO', 'Atasco', 1),
    ('OTROS', 'Otros', 1)
ON DUPLICATE KEY UPDATE
    descripcion = VALUES(descripcion),
    activo = VALUES(activo);

SELECT 'Datos insertados: Fuga, Atasco, Otros' AS Info;

-- Agregar columna tipo_rep_id a tbl_partes si no existe
SET @tablename = 'tbl_partes';
SET @columnname = 'tipo_rep_id';

-- Verificar si la columna existe
SET @column_exists = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = @schema_name
      AND TABLE_NAME = @tablename
      AND COLUMN_NAME = @columnname
);

-- Si no existe, agregarla
SET @sql = IF(
    @column_exists > 0,
    'SELECT "La columna tipo_rep_id ya existe en tbl_partes" AS Info',
    'ALTER TABLE tbl_partes ADD COLUMN tipo_rep_id INT NULL, ADD FOREIGN KEY (tipo_rep_id) REFERENCES dim_tipos_rep(id)'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Mensaje final
SELECT '✓ Tabla dim_tipos_rep creada y tbl_partes actualizada correctamente' AS Resultado;
