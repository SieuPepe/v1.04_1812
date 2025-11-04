#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear la tabla dim_tipos_rep en un esquema específico.
Uso: python crear_dim_tipos_rep_schema.py <schema>
"""

import sys
import os

# Añadir directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from script.db_connection import get_project_connection


def crear_dim_tipos_rep(user, password, schema):
    """Crea la tabla dim_tipos_rep en el esquema especificado"""
    print(f"Creando dim_tipos_rep en esquema: {schema}")

    with get_project_connection(user, password, schema) as conn:
        cursor = conn.cursor()

        # 1. Crear tabla dim_tipos_rep
        print("  1. Creando tabla dim_tipos_rep...")
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {schema}.dim_tipos_rep (
                id INT AUTO_INCREMENT PRIMARY KEY,
                codigo VARCHAR(50),
                descripcion VARCHAR(255) NOT NULL,
                activo TINYINT DEFAULT 1,
                INDEX idx_codigo (codigo),
                INDEX idx_activo (activo)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        conn.commit()
        print("  ✓ Tabla dim_tipos_rep creada")

        # 2. Poblar con datos
        print("  2. Poblando dim_tipos_rep...")
        cursor.execute(f"""
            INSERT INTO {schema}.dim_tipos_rep (codigo, descripcion, activo)
            VALUES
                ('FUGA', 'Fuga', 1),
                ('ATASCO', 'Atasco', 1),
                ('OTROS', 'Otros', 1)
            ON DUPLICATE KEY UPDATE
                descripcion = VALUES(descripcion),
                activo = VALUES(activo)
        """)
        conn.commit()
        print("  ✓ Datos insertados: Fuga, Atasco, Otros")

        # 3. Verificar si columna tipo_rep_id existe en tbl_partes
        print("  3. Verificando columna tipo_rep_id en tbl_partes...")
        cursor.execute(f"""
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = %s
              AND TABLE_NAME = 'tbl_partes'
              AND COLUMN_NAME = 'tipo_rep_id'
        """, (schema,))

        existe = cursor.fetchone()[0] > 0

        if not existe:
            print("  4. Agregando columna tipo_rep_id a tbl_partes...")
            cursor.execute(f"""
                ALTER TABLE {schema}.tbl_partes
                ADD COLUMN tipo_rep_id INT NULL,
                ADD FOREIGN KEY (tipo_rep_id) REFERENCES {schema}.dim_tipos_rep(id)
            """)
            conn.commit()
            print("  ✓ Columna tipo_rep_id agregada con FK")
        else:
            print("  ✓ Columna tipo_rep_id ya existe")

        cursor.close()

    print(f"\n✅ dim_tipos_rep creada exitosamente en {schema}")


if __name__ == "__main__":
    # Para testing rápido
    USER = "root"
    PASSWORD = "hydroflow"
    SCHEMA = "cert_dev"  # Por defecto

    if len(sys.argv) > 1:
        SCHEMA = sys.argv[1]

    try:
        crear_dim_tipos_rep(USER, PASSWORD, SCHEMA)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
