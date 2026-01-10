"""
Script de diagnostico para verificar conexion con Ollama.
Ejecuta: python test_ollama.py
"""

print("=" * 50)
print("DIAGNOSTICO DE CONEXION CON OLLAMA")
print("=" * 50)

# Test 1: Verificar urllib (stdlib)
print("\n1. Probando con urllib (libreria estandar)...")
try:
    import urllib.request
    import json

    req = urllib.request.Request(
        "http://localhost:11434/api/tags",
        headers={'Accept': 'application/json'}
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        data = json.loads(response.read().decode('utf-8'))
        models = [m['name'] for m in data.get('models', [])]
        print(f"   OK! Modelos encontrados: {models}")
except Exception as e:
    print(f"   ERROR: {type(e).__name__}: {e}")

# Test 2: Verificar requests
print("\n2. Probando con requests...")
try:
    import requests
    response = requests.get("http://localhost:11434/api/tags", timeout=5)
    if response.status_code == 200:
        data = response.json()
        models = [m['name'] for m in data.get('models', [])]
        print(f"   OK! Modelos encontrados: {models}")
    else:
        print(f"   ERROR: Status code {response.status_code}")
except ImportError:
    print("   requests no esta instalado (pip install requests)")
except Exception as e:
    print(f"   ERROR: {type(e).__name__}: {e}")

# Test 3: Verificar comando ollama
print("\n3. Probando comando 'ollama'...")
try:
    import subprocess
    result = subprocess.run(['ollama', '--version'], capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        print(f"   OK! {result.stdout.strip()}")
    else:
        print(f"   ERROR: {result.stderr}")
except FileNotFoundError:
    print("   ollama no esta en PATH (normal en Windows con app de escritorio)")
except Exception as e:
    print(f"   ERROR: {type(e).__name__}: {e}")

# Test 4: Verificar puerto
print("\n4. Probando conexion al puerto 11434...")
try:
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    result = sock.connect_ex(('localhost', 11434))
    sock.close()
    if result == 0:
        print("   OK! Puerto 11434 abierto")
    else:
        print(f"   ERROR: Puerto cerrado o no accesible (codigo: {result})")
except Exception as e:
    print(f"   ERROR: {type(e).__name__}: {e}")

print("\n" + "=" * 50)
print("Si el test 1 o 2 funcionan, Ollama esta listo.")
print("Si fallan, asegurate de que Ollama esta ejecutandose.")
print("=" * 50)
