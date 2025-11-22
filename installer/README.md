# HydroFlow Manager v1.04 - Sistema de Instalación Profesional

Sistema de instalación profesional con Inno Setup para HydroFlow Manager v1.04, diseñado para distribución a usuarios finales.

## 🎯 Características del Instalador

### ✨ Profesional y Completo
- **Interfaz moderna** estilo Windows (como VSCode, Discord, etc.)
- **Selección de carpeta** de instalación
- **Accesos directos** automáticos (escritorio y menú inicio)
- **Asistente de configuración** post-instalación
- **Desinstalador** incluido

### 📦 Todo Incluido (Offline)
- **Todas las dependencias** Python embebidas (sin conexión a internet)
- **Recursos** y archivos necesarios incluidos
- **Documentación** integrada
- Instalador **standalone** de ~150-200 MB

### 🔒 Seguro y Profesional
- Verificación de requisitos previos (MySQL)
- Configuración guiada paso a paso
- Gestión segura de credenciales (.env)
- Desinstalación limpia

## 📋 Arquitectura del Sistema

### Componentes

```
installer/
├── build_all.ps1                    # Script maestro - USAR ESTE
├── build_app.ps1                    # Compila aplicación principal
├── build_config.ps1                 # Compila configurador
├── build_inno_setup.ps1             # Compila instalador final
├── config_wizard.py                 # Asistente de configuración (simplificado)
├── HydroFlowManager.iss             # Script Inno Setup
├── LEER_ANTES_DE_INSTALAR.txt       # Info pre-instalación
├── LEER_DESPUES_DE_INSTALAR.txt     # Info post-instalación
└── README_NEW.md                    # Esta documentación

dist/
├── HydroFlowManager.exe             # App principal (generado)
├── HydroFlowManager_Config.exe      # Configurador (generado)
└── HydroFlowManager_v1.04_Setup.exe # Instalador final (generado)
```

### Flujo de Compilación

```
1. build_app.ps1
   └─> Compila main.py
       └─> dist/HydroFlowManager.exe (app principal con todas las dependencias)

2. build_config.ps1
   └─> Compila config_wizard.py
       └─> dist/HydroFlowManager_Config.exe (asistente de configuración)

3. build_inno_setup.ps1
   └─> Empaqueta ambos .exe con Inno Setup
       └─> dist/HydroFlowManager_v1.04_Setup.exe (instalador profesional)
```

### Flujo de Instalación (Usuario Final)

```
1. Usuario ejecuta HydroFlowManager_v1.04_Setup.exe
   ├─> Pantalla de bienvenida
   ├─> Licencia
   ├─> Selección de carpeta
   ├─> Selección de componentes (iconos)
   ├─> Verificación de MySQL
   └─> Instalación de archivos

2. Post-instalación automática:
   └─> Se ejecuta HydroFlowManager_Config.exe
       ├─> Configurar conexión MySQL
       ├─> Probar conexión
       └─> Generar archivo .env

3. Usuario ejecuta HydroFlowManager.exe
   └─> Aplicación lista para usar
```

## 🚀 Compilar el Instalador

### Requisitos Previos

1. **Python 3.8+** instalado
2. **PyInstaller**:
   ```powershell
   pip install pyinstaller
   ```

3. **Todas las dependencias del proyecto**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Inno Setup 6.0+** instalado:
   - Descargar de: https://jrsoftware.org/isdl.php
   - Instalar en la ruta por defecto

### Compilación Completa (Recomendado)

```powershell
# Desde el directorio raíz del proyecto
.\installer\build_all.ps1
```

Este script:
1. Compila la aplicación principal (`HydroFlowManager.exe`)
2. Compila el configurador (`HydroFlowManager_Config.exe`)
3. Genera el instalador con Inno Setup (`HydroFlowManager_v1.04_Setup.exe`)

**Resultado:** `dist\HydroFlowManager_v1.04_Setup.exe` (~150-200 MB)

### Compilación por Pasos (Opcional)

Si necesita compilar componentes individuales:

```powershell
# 1. Compilar solo la aplicación principal
.\installer\build_app.ps1

# 2. Compilar solo el configurador
.\installer\build_config.ps1

# 3. Compilar solo el instalador (requiere los 2 anteriores)
.\installer\build_inno_setup.ps1
```

## 📦 Distribución

### Archivo a Distribuir

```
dist/HydroFlowManager_v1.04_Setup.exe
```

Este único archivo contiene TODO lo necesario:
- ✅ Aplicación principal con todas las dependencias Python
- ✅ Asistente de configuración
- ✅ Recursos y documentación
- ✅ Scripts de instalación y desinstalación

### Requisitos del Usuario Final

El usuario SOLO necesita:
1. **Windows** 7/8/10/11 (64-bit recomendado)
2. **MySQL o MariaDB** instalado y corriendo
3. **Base de datos HydroFlow** ya creada e importada
4. **Credenciales** de acceso a MySQL

**NO necesita:**
- ❌ Python instalado
- ❌ Dependencias Python
- ❌ Conexión a internet
- ❌ Conocimientos técnicos

### Cómo Distribuir

**Opción 1: Archivo único** (Recomendado)
```
HydroFlowManager_v1.04_Setup.exe
```

**Opción 2: Con documentación extra**
```
HydroFlowManager_v1.04/
├── HydroFlowManager_v1.04_Setup.exe
├── INSTRUCCIONES.txt
└── MANUAL_USUARIO.pdf (si existe)
```

## 🔧 Configuración Post-Instalación

### Asistente de Configuración

El instalador ejecuta automáticamente `HydroFlowManager_Config.exe` que:

1. **Bienvenida**
   - Explica el proceso
   - Lista requisitos previos

2. **Configurar Base de Datos**
   - Host (localhost)
   - Puerto (3307 por defecto)
   - Usuario (root)
   - Contraseña
   - Nombres de esquemas

3. **Probar Conexión**
   - Verifica credenciales
   - Verifica que los esquemas existen
   - Muestra versión de MySQL

4. **Finalización**
   - Genera archivo `.env`
   - Muestra resumen

### Archivo .env Generado

```ini
# HydroFlow Manager v1.04 - Configuración
DB_HOST=localhost
DB_PORT=3307
DB_USER=root
DB_PASSWORD=<contraseña_ingresada>
DB_MANAGER_SCHEMA=manager
DB_EXAMPLE_SCHEMA=proyecto_tipo
DB_SCHEMA=cert_dev
DB_USE_POOLING=true
```

## 🐛 Troubleshooting

### Error: PyInstaller no encontrado

```powershell
pip install pyinstaller
```

### Error: Inno Setup no encontrado

1. Descargar de: https://jrsoftware.org/isdl.php
2. Instalar en ruta por defecto: `C:\Program Files (x86)\Inno Setup 6\`

### Error: HydroFlowManager.exe no encontrado

```powershell
# Compilar primero la aplicación
.\installer\build_app.ps1
```

### Error: Faltan dependencias Python

```powershell
# Instalar todas las dependencias
pip install -r requirements.txt
```

### El instalador es muy grande

Normal. El instalador incluye TODAS las dependencias Python (~150-200 MB).
Esto es intencional para que funcione offline.

### El antivirus bloquea el instalador

Falso positivo común en ejecutables PyInstaller. Agregar a excepciones.

## 📝 Personalización

### Cambiar Icono

Reemplazar: `resources\icon.ico`

### Cambiar Puerto Por Defecto

Editar `installer/config_wizard.py`:
```python
'db_port': tk.StringVar(value='3307'),  # Cambiar aquí
```

### Cambiar Mensajes de Instalación

Editar:
- `installer/LEER_ANTES_DE_INSTALAR.txt`
- `installer/LEER_DESPUES_DE_INSTALAR.txt`

### Modificar Script Inno Setup

Editar: `installer/HydroFlowManager.iss`

Documentación Inno Setup: https://jrsoftware.org/ishelp/

## 📊 Comparación con Sistema Anterior

| Característica | Sistema Anterior | Sistema Nuevo |
|----------------|------------------|---------------|
| **Interfaz** | Wizard simple | Instalador profesional |
| **Selección de carpeta** | ❌ No | ✅ Sí |
| **Accesos directos** | ❌ No | ✅ Sí |
| **Dependencias** | Se descargan | ✅ Incluidas |
| **Conexión internet** | Requerida | ❌ No necesaria |
| **Crea esquemas** | ✅ Sí | ❌ No (asume BD lista) |
| **Importa datos** | ✅ Sí | ❌ No (asume BD lista) |
| **Instala Python deps** | ✅ Sí | ❌ No (ya incluidas) |
| **Tamaño** | ~15-20 MB | ~150-200 MB |
| **Profesionalismo** | Básico | ⭐⭐⭐⭐⭐ |

## 🗑️ Archivos Obsoletos

Los siguientes archivos del sistema anterior ya NO se usan:

- ~~`installer/setup_wizard.py`~~ → Reemplazado por `config_wizard.py`
- ~~`installer/build_installer.ps1`~~ → Reemplazado por `build_all.ps1`

Se conservan por compatibilidad pero se pueden eliminar.

## 📚 Documentación Relacionada

- `LICENSE.txt` - Licencia del software
- `INSTALACION.md` - Guía de instalación manual (raíz del proyecto)
- `README.md` - Documentación general del proyecto
- Inno Setup Docs: https://jrsoftware.org/ishelp/

## 💡 Notas Importantes

### Para Desarrolladores

- **NO compilar** con dependencias de desarrollo
- **Probar** siempre en máquina limpia antes de distribuir
- **Verificar** que el antivirus no bloquee
- **Documentar** cambios de versión en el script .iss

### Para Distribución

- El instalador es **standalone** (auto-contenido)
- Se puede distribuir por **email, USB, descarga directa**
- **No requiere** instalación de Python
- **No requiere** conexión a internet
- Usuario **debe tener MySQL ya instalado**

### Puerto 3307

El puerto por defecto es **3307** (no 3306) según especificación del proyecto.
Usuarios con MySQL en 3306 pueden cambiarlo en el asistente de configuración.

## ✅ Checklist Pre-Distribución

Antes de distribuir el instalador a usuarios finales:

- [ ] Compilado con `build_all.ps1` sin errores
- [ ] Probado en máquina limpia (sin Python)
- [ ] Verificado que se crean accesos directos
- [ ] Verificado que el configurador funciona
- [ ] Verificado que la aplicación se ejecuta correctamente
- [ ] Antivirus no bloquea (o agregado a excepciones)
- [ ] Archivo de salida: `HydroFlowManager_v1.04_Setup.exe`
- [ ] Tamaño razonable (~150-200 MB)
- [ ] Documentación actualizada

## 📞 Soporte

Para problemas con el sistema de instalación:
1. Consultar esta documentación
2. Revisar sección Troubleshooting
3. Verificar logs de compilación

---

**HydroFlow Manager v1.04** - Sistema de Instalación Profesional
Compilado con PyInstaller + Inno Setup
