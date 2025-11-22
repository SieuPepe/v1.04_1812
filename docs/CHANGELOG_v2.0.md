# HydroFlow Manager v2.0 - Changelog

## 📋 Resumen de Cambios

HydroFlow Manager v2.0 es una actualización importante que elimina todos los valores hardcodeados de configuración de base de datos y proporciona un sistema flexible de instalación mediante variables de entorno.

**Fecha de Release:** 2025-01-22
**Versión:** 2.0
**Tipo:** Major Update

## 🎯 Objetivos de la Versión

1. **Eliminación de valores hardcodeados**
   - Credenciales de base de datos
   - Direcciones IP y puertos
   - Nombres de esquemas

2. **Flexibilidad de instalación**
   - Configuración mediante archivo `.env`
   - Soporte para diferentes puertos (3306, 3307, etc.)
   - Soporte para servidores locales y remotos

3. **Seguridad mejorada**
   - No incluir credenciales en el código fuente
   - Archivo `.env` en `.gitignore`
   - Guías de instalación segura

4. **Preparación para distribución**
   - Scripts de compilación automatizados
   - Sistema de backups de base de datos
   - Suite de tests actualizada

## 🔧 Cambios Técnicos

### Configuración de Base de Datos

#### script/db_config.py

**Cambios:**
- Agregado soporte para `python-dotenv`
- Carga explícita de archivo `.env` con cálculo de ruta relativa
- Prioridad de configuración: .env → user_config → defaults

**Código agregado:**
```python
# Cargar variables de entorno desde .env
try:
    from dotenv import load_dotenv
    _project_root = Path(__file__).resolve().parent.parent
    _env_path = _project_root / '.env'
    load_dotenv(dotenv_path=_env_path, override=False)
except ImportError:
    pass
```

**Impacto:** El archivo `.env` se carga automáticamente desde cualquier directorio de ejecución.

#### Variables de Entorno Soportadas

```bash
# Servidor
DB_HOST=localhost          # Default: localhost
DB_PORT=3306              # Default: 3306

# Credenciales (REQUERIDAS)
DB_USER=root              # Sin default
DB_PASSWORD=contraseña    # Sin default

# Esquemas
DB_MANAGER_SCHEMA=manager           # Default: manager
DB_EXAMPLE_SCHEMA=proyecto_tipo     # Default: proyecto_tipo
DB_SCHEMA=cert_dev                  # Para desarrollo/tests

# Rendimiento
DB_USE_POOLING=true                 # Default: true
```

### Archivos Modificados

#### 1. Scripts de Desarrollo y Tools

**dev_tools/verificacion/test_conexion_directa.py**
- Agregada carga de `.env`
- Eliminado hardcoded: `password='Lauburu1969'`
- Usa variables de entorno con validación

**dev_tools/importacion/importar_mediciones_ots.py**
- Eliminadas constantes `DEFAULT_USER` y `DEFAULT_PASSWORD`
- Argumentos `--user` y `--password` con fallback a `.env`
- Validación de credenciales

**tools/alimentar_presupuestos_partes.py**
- Eliminado: `USER = os.getenv('DB_USER', 'root')`
- Eliminado: `PASSWORD = os.getenv('DB_PASSWORD', 'Lauburu1969')`
- Ahora requiere variables de entorno, no tiene fallbacks

**tools/detectar_columnas_precios.py**
- Eliminado hardcoded: `PASSWORD = os.getenv('DB_PASSWORD', 'NuevaPass!2025')`
- Requiere credenciales desde `.env`

#### 2. Interfaces (CRÍTICO - Producción)

**interface/cert_lotes_interfaz.py**
- **CRÍTICO:** Eliminadas credenciales de producción del bloque de test
- Antes (líneas 439-440):
  ```python
  USER = "root"
  PASSWORD = "NuevaPass!2025"
  ```
- Después:
  ```python
  USER = os.getenv('DB_USER') or input("Usuario de BD: ")
  PASSWORD = os.getenv('DB_PASSWORD') or getpass.getpass("Contraseña de BD: ")
  ```

#### 3. Suite de Tests

**tests/test_imports.py**
- ✅ Ya era compatible con v2.0
- Verifica variables de entorno correctamente

**tests/test_presupuestos.py**
- Agregada carga de `.env`
- Cambiado `DB_EXAMPLE_SCHEMA` → `DB_SCHEMA`
- Validación de credenciales mejorada
- Eliminado fallback `'TU_PASSWORD_AQUI'`

**tests/test_certificaciones.py**
- Mismos cambios que `test_presupuestos.py`
- Ahora usa `.env` correctamente

**tests/test_flujo_completo.py**
- Mismos cambios que `test_presupuestos.py`
- Validación de credenciales

**tests/test_optimizaciones.py**
- Agregada carga de `.env`
- Argumentos de línea de comando ahora opcionales
- Usa `.env` como fallback si no se proporcionan args
- Docstring actualizado con nuevo uso

### Nuevos Archivos

#### 1. Documentación

**INSTALACION.md**
- Guía completa de instalación paso a paso
- Configuración de `.env`
- Troubleshooting (incluyendo puerto 3306 vs 3307)
- Configuración para servidor remoto

**.env.example**
- Plantilla completa con documentación inline
- 105 líneas de comentarios y ejemplos
- Explica cada variable de entorno
- Notas de seguridad y valores por defecto

**docs/COMPILACION_Y_DISTRIBUCION.md**
- Guía completa de compilación con PyInstaller
- Pasos de distribución
- Checklist de seguridad
- Troubleshooting de compilación

**tests/README.md**
- Documentación de suite de tests
- Instrucciones de ejecución
- Troubleshooting de tests
- Plantilla para nuevos tests

**dev_tools/preparacion/README.md**
- Guía de scripts de preparación de BD
- Uso de backups
- Flujo de trabajo recomendado

**docs/CHANGELOG_v2.0.md** (este archivo)
- Changelog completo de la versión

#### 2. Scripts de Automatización

**build.ps1**
- Script PowerShell de compilación automatizada
- Verifica requisitos
- Limpia builds anteriores
- Ejecuta PyInstaller
- Proporciona instrucciones post-build

**run_tests.ps1**
- Ejecuta toda la suite de tests automáticamente
- Verifica `.env`
- Configura `PYTHONPATH`
- Genera resumen de resultados

**dev_tools/preparacion/preparar_bd_produccion.ps1**
- Script PowerShell para preparar BD antes de compilar
- Valida que no hay datos de prueba
- Crea backups de esquemas
- Genera reporte de validación

**dev_tools/preparacion/preparar_bd_produccion.py**
- Versión Python del script de preparación
- Multiplataforma (Windows/Linux/Mac)
- Misma funcionalidad que la versión PowerShell

#### 3. Configuración

**HydroFlowManager.spec** (actualizado)
- Agregado `pandas` a hiddenimports (v2.0)
- Agregado `dotenv` a hiddenimports (v2.0)
- Incluye `.env.example` en `datas`
- Incluye `INSTALACION.md` en `datas`
- Incluye manuales en `docs/manual/*.md`
- Excluye tests de la compilación

## 📊 Estadísticas de Cambios

### Archivos Modificados
- **16 archivos** con valores hardcodeados eliminados
- **5 archivos de tests** actualizados para v2.0
- **1 archivo crítico** de producción corregido (cert_lotes_interfaz.py)

### Archivos Creados
- **9 nuevos archivos** de documentación
- **4 nuevos scripts** de automatización
- **1 plantilla** de configuración (.env.example)

### Líneas de Código
- **~2,000 líneas** de documentación agregadas
- **~500 líneas** de scripts de automatización
- **~100 líneas** de código de configuración modificadas

## 🔒 Seguridad

### Credenciales Eliminadas del Código

**Contraseñas eliminadas:**
- `'Lauburu1969'` (8 archivos)
- `'NuevaPass!2025'` (8 archivos)

**Usuarios hardcodeados eliminados:**
- `'root'` (11 archivos)

**Puertos/IPs eliminados:**
- `3307` hardcoded (5 archivos)
- `localhost` hardcoded (3 archivos)

### Archivo .gitignore

El archivo `.env` está en `.gitignore` para prevenir que las credenciales se suban al repositorio:

```gitignore
# Environment variables
.env
.env.local
.env.*.local
```

## 📦 Instalación y Distribución

### Para Desarrolladores

1. **Clonar repositorio:**
   ```bash
   git clone <repo>
   cd v1.04_1812
   ```

2. **Configurar entorno:**
   ```bash
   # Crear .env desde plantilla
   copy .env.example .env

   # Editar .env con tus credenciales
   notepad .env
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   pip install python-dotenv
   ```

4. **Ejecutar tests:**
   ```powershell
   .\run_tests.ps1
   ```

### Para Compilación

1. **Preparar base de datos:**
   ```powershell
   .\dev_tools\preparacion\preparar_bd_produccion.ps1
   ```

2. **Compilar aplicación:**
   ```powershell
   .\build.ps1
   ```

3. **Distribuir:**
   - Ejecutable: `dist/HidroFlowManager.exe`
   - Incluir: `.env.example`
   - Incluir: `INSTALACION.md`
   - Incluir: Backups SQL de `backups/produccion/`

### Para Instalación en Cliente

1. **Descomprimir paquete**

2. **Configurar .env:**
   ```bash
   copy .env.example .env
   notepad .env
   ```

3. **Restaurar base de datos:**
   ```bash
   mysql -u root -p < sql/manager_estructura_y_datos.sql
   mysql -u root -p < sql/proyecto_tipo_completo.sql
   ```

4. **Ejecutar aplicación:**
   ```
   HidroFlowManager.exe
   ```

## 🧪 Testing

### Suite de Tests

**Tests actualizados para v2.0:**
- `test_imports.py` - Verifica imports y configuración
- `test_optimizaciones.py` - Tests de rendimiento con caché
- `test_presupuestos.py` - Funcionalidad de presupuestos
- `test_certificaciones.py` - Funcionalidad de certificaciones
- `test_flujo_completo.py` - Tests end-to-end

**Ejecución:**
```powershell
# Ejecutar todos los tests
.\run_tests.ps1

# Ejecutar test individual
python tests/test_imports.py
```

**Requisitos para tests:**
- Archivo `.env` configurado
- Base de datos accesible
- Esquemas `manager` y `cert_dev` creados

## 🔄 Migración desde v1.x

### Pasos de Migración

1. **Crear archivo .env:**
   ```bash
   copy .env.example .env
   ```

2. **Configurar credenciales:**
   Editar `.env` con las credenciales que antes estaban hardcodeadas

3. **Actualizar scripts personalizados:**
   Si creaste scripts personalizados que usaban valores hardcodeados, actualízalos para usar variables de entorno

4. **Probar conexión:**
   ```bash
   python dev_tools/verificacion/test_conexion_directa.py
   ```

### Cambios que Requieren Atención

**Puerto de MySQL:**
- Si usabas puerto **3307**, asegúrate de configurar `DB_PORT=3307` en `.env`
- El default es ahora **3306** (estándar de MySQL)

**Nombres de esquemas:**
- Si tus esquemas tienen nombres diferentes a `manager` y `proyecto_tipo`, configúralos en `.env`

## 🐛 Problemas Conocidos y Soluciones

### Error: "Can't connect to MySQL server on 'localhost:3306'"

**Causa:** El puerto en `.env` no coincide con tu instalación MySQL

**Solución:**
```bash
# En .env, cambiar:
DB_PORT=3307  # Si tu MySQL usa puerto 3307
```

### Error: "DB_USER or DB_PASSWORD not found"

**Causa:** Archivo `.env` no existe o no tiene credenciales

**Solución:**
```bash
copy .env.example .env
notepad .env
# Configurar DB_USER y DB_PASSWORD
```

### Tests fallan con "Schema not found"

**Causa:** Esquemas no creados en la base de datos

**Solución:**
```sql
CREATE DATABASE manager;
CREATE DATABASE cert_dev;
```

## 📝 Notas para Mantenimiento

### Agregar Nueva Configuración

1. **Agregar variable a .env.example:**
   ```bash
   # Nueva configuración
   MI_NUEVA_CONFIG=valor_default
   ```

2. **Documentar en INSTALACION.md**

3. **Actualizar db_config.py si es necesario**

4. **Actualizar tests**

### Convenciones

- **Nombres de variables:** `DB_` prefix para variables de BD
- **Valores por defecto:** Usar valores estándar de MySQL (puerto 3306, etc.)
- **Documentación:** Siempre documentar en .env.example con comentarios

## 🙏 Agradecimientos

Gracias a todos los que reportaron problemas con valores hardcodeados y ayudaron a diseñar un sistema de configuración flexible.

## 📞 Soporte

Para preguntas o problemas:

1. Consultar `INSTALACION.md`
2. Consultar `docs/COMPILACION_Y_DISTRIBUCION.md`
3. Revisar este CHANGELOG
4. Consultar `tests/README.md` para problemas de testing

## 📄 Licencia

HydroFlow Manager v2.0 mantiene la misma licencia que versiones anteriores.

---

**Versión:** 2.0
**Fecha:** 2025-01-22
**Estado:** Listo para Producción
