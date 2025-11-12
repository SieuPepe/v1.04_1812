# Estructura del Proyecto HydroFlow Manager

## 📁 Organización de Carpetas

```
v1.04_1812/
├── interface/              # Interfaces gráficas (GUI)
│   └── *.py               # Ventanas de la aplicación
│
├── script/                # Lógica de negocio y BD
│   ├── db_*.py           # Módulos de base de datos
│   ├── informes*.py      # Sistema de informes
│   └── ctk_*.py          # Widgets personalizados
│
├── resources/             # Recursos de la aplicación
│   └── images/           # Imágenes, logos e iconos
│
├── tools/                 # Herramientas de usuario final
│   ├── crear_backup_bd.py
│   └── configurar_instalacion.py
│
├── dev_tools/             # Herramientas de desarrollo (NO en producción)
│   ├── importacion/      # Scripts de importación de datos
│   ├── generadores/      # Generadores de datos/SQL
│   ├── verificacion/     # Scripts de verificación/debug
│   └── requirements-dev.txt  # Dependencias de desarrollo
│
├── docs/                  # Documentación
│   ├── manual/           # Manuales de usuario e instalación
│   └── desarrollo/       # Documentación de desarrollo
│
├── tests/                 # Tests automáticos
│   └── test_*.py
│
├── build/                 # Archivos de compilación (auto-generado)
├── dist/                  # Distribución compilada (auto-generado)
└── backups/              # Backups de BD (auto-generado)
```

## 📦 Archivos Principales

### Aplicación
- `main.py` - Punto de entrada de la aplicación
- `HidroFlowManager.spec` - Configuración de PyInstaller
- `build.py` - Script de compilación
- `requirements.txt` - Dependencias Python

### Configuración
- `.env.example` - Template de configuración para desarrollo
- `.env.produccion.template` - Template de configuración para producción
- `.gitignore` - Archivos a ignorar en git
- `pyproject.toml` - Configuración del proyecto Python

### Documentación
- `docs/manual/INSTALACION_Y_CONFIGURACION.md` - Guía de instalación
- `docs/manual/VERIFICACION_INFORMES.md` - Guía de verificación de informes
- `docs/manual/ESTRUCTURA_PROYECTO.md` - Este documento
- `docs/manual/LIMPIEZA_PROYECTO.md` - Historial de limpieza del proyecto

## 🚀 Para Producción

Archivos que **SÍ** deben incluirse en el instalador:
- `interface/` (completo)
- `script/` (sin READMEs de desarrollo)
- `resources/` (completo)
- `tools/` (completo)
- `main.py`
- `requirements.txt`
- Documentación de usuario

Archivos que **NO** deben incluirse:
- `dev_tools/` (herramientas de desarrollo)
- `docs/desarrollo/` (documentación interna)
- `tests/` (tests de desarrollo)
- `.git/` (control de versiones)
- `build/`, `dist/` (temporales de compilación)

## 🔧 Para Desarrollo

Si necesita modificar/desarrollar:
- Clonar repositorio completo
- Los scripts en `dev_tools/` ayudan con:
  - Importación de datos desde Access/Excel
  - Generación de datos de prueba
  - Verificación de integridad
  - Scripts SQL automáticos

## 📝 Notas

- Las imágenes están en `resources/images/`
- Los scripts de desarrollo están en `dev_tools/`
- Los manuales de usuario están en `docs/manual/`
- La documentación de desarrollo está en `docs/desarrollo/`
- Las dependencias de desarrollo están en `dev_tools/requirements-dev.txt`
- Las dependencias de producción están en `requirements.txt` (raíz)
