import os
from pathlib import Path

print("=" * 60)
print("DIAGNÓSTICO DE CONFIGURACIÓN .env")
print("=" * 60)

# 1. Verificar ubicación del .env
env_file = Path(__file__).parent / '.env'
print(f"\n1. Archivo .env ubicación: {env_file}")
print(f"   ¿Existe? {env_file.exists()}")

if env_file.exists():
    print(f"   Tamaño: {env_file.stat().st_size} bytes")

# 2. Verificar python-dotenv
print("\n2. python-dotenv:")
try:
    from dotenv import load_dotenv

    print(f"   ✅ Instalado correctamente")
except ImportError:
    print("   ❌ NO INSTALADO")

# 3. Cargar .env
print("\n3. Cargando .env:")
try:
    from dotenv import load_dotenv

    loaded = load_dotenv(dotenv_path=env_file, override=True)
    print(f"   load_dotenv() retornó: {loaded}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 4. Verificar variables de entorno
print("\n4. Variables de entorno después de cargar .env:")
env_vars = ['DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASSWORD', 'DB_SCHEMA']
for var in env_vars:
    value = os.getenv(var)
    if value:
        if var == 'DB_PASSWORD':
            print(f"   {var} = {'*' * len(value)} (longitud: {len(value)} caracteres)")
        else:
            print(f"   {var} = {value}")
    else:
        print(f"   {var} = ❌ NO CONFIGURADA")

# 5. Verificar db_config
print("\n5. Usando script/db_config.py:")
try:
    from script.db_config import get_config

    config = get_config()
    print(f"   Host: {config.host}")
    print(f"   Port: {config.port}")
    print(f"   User: {config.user if config.user else '❌ NO CONFIGURADO'}")
    if config.password:
        print(
            f"   Password: {'*' * len(config.password)} (longitud: {len(config.password)} caracteres)")
    else:
        print(f"   Password: ❌ NO CONFIGURADO")
    print(f"   Schema: {config.default_schema}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback

    traceback.print_exc()

# 6. Intentar conexión real
print("\n6. PRUEBA DE CONEXIÓN A MYSQL:")
try:
    from script.db_config import get_config
    import mysql.connector

    config = get_config()

    print(f"   Intentando conectar con:")
    print(f"   - Host: {config.host}")
    print(f"   - Port: {config.port}")
    print(f"   - User: {config.user}")
    print(f"   - Password: {'*' * len(config.password) if config.password else 'VACÍA'}")
    print(f"   - Database: {config.default_schema}")

    conn = mysql.connector.connect(
        host=config.host,
        port=config.port,
        user=config.user,
        password=config.password,
        database=config.default_schema
    )

    print("\n   ✅ ¡CONEXIÓN EXITOSA!")

    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"   MySQL Version: {version[0]}")
    cursor.close()
    conn.close()

except Exception as e:
    print(f"\n   ❌ ERROR DE CONEXIÓN: {e}")

print("\n" + "=" * 60)
