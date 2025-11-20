#!/usr/bin/env python3
"""
Test de conexión DIRECTA a cert_dev sin usar abstracciones
"""

import os
import sys
from pathlib import Path
import mysql.connector

# Cargar .env
try:
    from dotenv import load_dotenv
    project_root = Path(__file__).resolve().parent.parent.parent
    load_dotenv(dotenv_path=project_root / '.env')
except ImportError:
    pass

# Parámetros de conexión desde variables de entorno
config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_SCHEMA', 'cert_dev')
}

# Validar credenciales
if not config['user'] or not config['password']:
    print("ERROR: Se requieren credenciales en variables de entorno")
    print("Configure DB_USER y DB_PASSWORD en el archivo .env")
    sys.exit(1)

print("=" * 80)
print("TEST DE CONEXIÓN DIRECTA A cert_dev")
print("=" * 80)

try:
    # Conexión directa
    print(f"\n🔌 Conectando a {config['host']}:{config['port']} como {config['user']}...")
    conn = mysql.connector.connect(**config)

    print(f"   ✅ Conexión establecida")

    cursor = conn.cursor()

    # 1. Verificar esquema actual
    cursor.execute("SELECT DATABASE()")
    db_actual = cursor.fetchone()[0]
    print(f"\n📁 Esquema actual: {db_actual}")

    # 2. Contar registros en tbl_partes
    print(f"\n📊 Consultando tbl_partes...")
    cursor.execute("SELECT COUNT(*) FROM tbl_partes")
    total = cursor.fetchone()[0]
    print(f"   Total de registros: {total}")

    if total > 0:
        # 3. Mostrar primeros 10 registros
        cursor.execute("SELECT id, codigo FROM tbl_partes ORDER BY id LIMIT 10")
        print(f"\n   Primeros 10 registros:")
        for row in cursor.fetchall():
            print(f"      ID={row[0]}: '{row[1]}'")

        # 4. Buscar códigos específicos del Excel
        print(f"\n🔍 Buscando códigos del Excel:")
        codigos_test = ['OT/0121', 'OT/0453', 'GF/0001', 'GF/0002', 'TP/0278']

        for codigo in codigos_test:
            cursor.execute("SELECT id FROM tbl_partes WHERE codigo = %s", (codigo,))
            result = cursor.fetchone()
            if result:
                print(f"   ✅ '{codigo}' → ENCONTRADO (ID={result[0]})")
            else:
                print(f"   ❌ '{codigo}' → NO ENCONTRADO")
    else:
        print(f"   ⚠️  La tabla está VACÍA")

    cursor.close()
    conn.close()

    print("\n✅ Test completado")

except mysql.connector.Error as e:
    print(f"\n❌ Error de MySQL: {e}")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n")
