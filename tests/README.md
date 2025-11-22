# Suite de Tests - HydroFlow Manager v2.0

## 📋 Descripción

Esta carpeta contiene la suite de tests automatizados para HydroFlow Manager v2.0. Los tests verifican la funcionalidad del sistema en diferentes niveles:

- **Imports y Configuración**: Verificación de módulos y configuración base
- **Optimizaciones**: Tests de rendimiento y optimizaciones de BD
- **Presupuestos**: Funcionalidad de gestión de presupuestos
- **Certificaciones**: Funcionalidad de certificaciones
- **Flujo Completo**: Tests end-to-end de flujos completos

## 🚀 Ejecución Rápida

### Ejecutar Todos los Tests

```powershell
# Desde el directorio raíz del proyecto
.\run_tests.ps1
```

### Ejecutar un Test Individual

```powershell
# Configurar PYTHONPATH
$env:PYTHONPATH = (Get-Location).Path

# Ejecutar test específico
python tests/test_imports.py
python tests/test_optimizaciones.py
python tests/test_presupuestos.py
python tests/test_certificaciones.py
python tests/test_flujo_completo.py
```

## 📋 Requisitos Previos

### 1. Entorno Virtual Activado

```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1
```

### 2. Archivo .env Configurado

Los tests requieren credenciales de base de datos. Asegúrate de tener un archivo `.env` configurado:

```bash
# .env (en el directorio raíz)
DB_HOST=localhost
DB_PORT=3307
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_SCHEMA=cert_dev
DB_MANAGER_SCHEMA=manager
```

**Nota:** El archivo `.env` NO está en el repositorio (está en `.gitignore`). Crea el tuyo desde `.env.example`:

```powershell
copy .env.example .env
notepad .env
```

### 3. Base de Datos Disponible

Los tests requieren acceso a una base de datos MySQL/MariaDB con:
- Esquema `manager` configurado
- Esquema de proyecto de prueba (ej: `cert_dev`)
- Usuario con permisos adecuados

## 📊 Descripción de Tests

### test_imports.py

**Objetivo:** Verificar que todos los módulos se importan correctamente

**Tests incluidos:**
1. Módulos base (db_config, db_connection)
2. Configuración (lectura de .env, valores por defecto)
3. Compatibilidad con modulo_db
4. MySQL Connector instalado
5. Funciones disponibles
6. Variables de entorno

**Ejecución:**
```powershell
python tests/test_imports.py
```

**Salida esperada:**
```
✅ PASS - Módulos base
✅ PASS - Configuración
✅ PASS - Compatibilidad modulo_db
✅ PASS - MySQL Connector
✅ PASS - Funciones disponibles
✅ PASS - Variables de entorno

Resultado: 6/6 pruebas pasadas
✅ CONFIGURACIÓN COMPLETA - TODO FUNCIONANDO CORRECTAMENTE
```

### test_optimizaciones.py

**Objetivo:** Verificar optimizaciones de rendimiento

**Tests incluidos:**
- Connection pooling
- Índices de base de datos
- Consultas optimizadas

### test_presupuestos.py

**Objetivo:** Verificar funcionalidad de presupuestos

**Tests incluidos:**
- Importación de presupuestos
- Gestión de partidas
- Cálculos de precios

### test_certificaciones.py

**Objetivo:** Verificar funcionalidad de certificaciones

**Tests incluidos:**
- Creación de certificaciones
- Líneas de certificación
- Estados y validaciones

### test_flujo_completo.py

**Objetivo:** Tests end-to-end de flujos completos

**Tests incluidos:**
- Creación de proyecto completo
- Carga de partes
- Asignación de presupuesto
- Generación de certificaciones

## 🔧 Troubleshooting

### Error: "No module named 'script'"

**Causa:** PYTHONPATH no configurado

**Solución:**
```powershell
$env:PYTHONPATH = (Get-Location).Path
python tests/test_imports.py
```

### Error: "Can't connect to MySQL server"

**Causa:** Credenciales incorrectas o BD no disponible

**Solución:**
1. Verificar que MySQL está ejecutándose
2. Verificar credenciales en `.env`
3. Verificar puerto (3306 o 3307)

```powershell
# Verificar configuración
python dev_tools/verificacion/test_conexion_directa.py
```

### Error: "DB_USER or DB_PASSWORD not found"

**Causa:** Archivo `.env` no existe o no tiene credenciales

**Solución:**
```powershell
# Crear .env desde plantilla
copy .env.example .env

# Editar y agregar credenciales
notepad .env
```

### Tests fallan con "Schema not found"

**Causa:** Esquemas de BD no creados

**Solución:**
1. Verificar que existen los esquemas `manager` y `cert_dev`
2. Crear esquemas si es necesario
3. Consultar `docs/manual/Guia_Instalacion_BD_v2.0.md`

## 📝 Agregar Nuevos Tests

Para agregar un nuevo test:

1. Crear archivo en `tests/test_nueva_funcionalidad.py`
2. Seguir la estructura de los tests existentes
3. Agregar al script `run_tests.ps1`

### Plantilla de Test

```python
#!/usr/bin/env python3
"""
Test de [Funcionalidad]
"""

import sys
from pathlib import Path

# Configurar path
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

def test_funcionalidad_1():
    """Prueba 1: [Descripción]"""
    print("=" * 70)
    print("Prueba 1: [Nombre]...")
    print("=" * 70)

    try:
        # Tu código de test aquí
        assert True, "Condición que debe cumplirse"
        print("✅ Test pasado")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Ejecutar todos los tests"""
    results = []
    results.append(("Funcionalidad 1", test_funcionalidad_1()))

    # Resumen
    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"\nResultado: {passed}/{total} pruebas pasadas")
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

## 🎯 Cobertura de Tests

| Módulo | Test | Cobertura |
|--------|------|-----------|
| db_config | test_imports.py | ✅ 100% |
| db_connection | test_imports.py | ✅ 100% |
| modulo_db | test_imports.py | ✅ 100% |
| Optimizaciones | test_optimizaciones.py | ✅ |
| Presupuestos | test_presupuestos.py | ✅ |
| Certificaciones | test_certificaciones.py | ✅ |
| Flujo completo | test_flujo_completo.py | ✅ |

## 📞 Soporte

Si encuentras problemas con los tests:

1. Verifica los requisitos previos arriba
2. Consulta la sección de Troubleshooting
3. Revisa los logs de error detallados
4. Consulta la documentación técnica en `docs/manual/Manual_Tecnico_v2.0.md`
