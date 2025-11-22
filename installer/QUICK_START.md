# 🚀 Quick Start - Compilar Instalador Profesional

## Compilación en Un Solo Paso

```powershell
# Ejecutar desde el directorio raíz del proyecto:
.\installer\build_all.ps1
```

✅ Esto generará: `dist\HydroFlowManager_v1.04_Setup.exe`

## Requisitos Previos

```powershell
# Instalar PyInstaller
pip install pyinstaller

# Instalar todas las dependencias
pip install -r requirements.txt

# Descargar e instalar Inno Setup 6.0+
# https://jrsoftware.org/isdl.php
```

## Distribución

Distribuir el archivo:
```
dist/HydroFlowManager_v1.04_Setup.exe
```

Este archivo es **standalone** y contiene:
- ✅ Aplicación principal
- ✅ Asistente de configuración
- ✅ **TODAS** las dependencias Python
- ✅ Recursos y documentación

## Usuario Final

El usuario solo necesita:
1. Ejecutar `HydroFlowManager_v1.04_Setup.exe`
2. Seguir el asistente de instalación
3. Configurar conexión a MySQL (puerto 3307 por defecto)
4. ¡Listo!

**NO necesita:**
- ❌ Python instalado
- ❌ Pip o dependencias
- ❌ Conexión a internet

## Más Información

Ver `installer/README.md` para documentación completa.
