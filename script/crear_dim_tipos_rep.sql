-- Script para crear la dimensión dim_tipos_rep (Tipos de Reparación)
-- Esta tabla categoriza los partes según el tipo de reparación
-- Valores: Fuga, Atasco, Otros

-- Crear tabla dim_tipos_rep (en esquema plantilla proyecto_tipo)
CREATE TABLE IF NOT EXISTS proyecto_tipo.dim_tipos_rep (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50),
    descripcion VARCHAR(255) NOT NULL,
    activo TINYINT DEFAULT 1,
    INDEX idx_codigo (codigo),
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Poblar con los 3 tipos de reparación
INSERT INTO proyecto_tipo.dim_tipos_rep (codigo, descripcion, activo)
VALUES
    ('FUGA', 'Fuga', 1),
    ('ATASCO', 'Atasco', 1),
    ('OTROS', 'Otros', 1)
ON DUPLICATE KEY UPDATE
    descripcion = VALUES(descripcion),
    activo = VALUES(activo);

-- Agregar columna tipo_rep_id a tbl_partes (en proyecto_tipo)
-- Primero verificar si la columna ya existe antes de agregarla
SET @dbname = 'proyecto_tipo';
SET @tablename = 'tbl_partes';
SET @columnname = 'tipo_rep_id';
SET @preparedStatement = (SELECT IF(
  (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE
      TABLE_SCHEMA = @dbname
      AND TABLE_NAME = @tablename
      AND COLUMN_NAME = @columnname
  ) > 0,
  'SELECT 1',  -- La columna ya existe, no hacer nada
  CONCAT('ALTER TABLE ', @dbname, '.', @tablename, ' ADD COLUMN tipo_rep_id INT NULL, ADD FOREIGN KEY (tipo_rep_id) REFERENCES ', @dbname, '.dim_tipos_rep(id)')
));
PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;

-- Mensaje final
SELECT 'Tabla dim_tipos_rep creada y tbl_partes actualizada correctamente' AS resultado;
