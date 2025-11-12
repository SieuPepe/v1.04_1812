# Guía de Compilación - HydroFlow Manager

Esta guía explica cómo compilar HydroFlow Manager desde el código fuente para crear un ejecutable e instalador de Windows.

## 📋 Requisitos Previos

### Software Necesario

1. **Python 3.9 o superior**
   - Descargar desde: https://www.python.org/downloads/
   - Asegúrate de marcar "Add Python to PATH" durante la instalación

2. **PyInstaller** (para compilar el ejecutable)
   ```bash
   pip install pyinstaller
   ```

3. **Inno Setup 6** (para crear el instalador)
   - Descargar desde: https://jrsoftware.org/isdl.php
   - Solo necesario si quieres crear el instalador .exe completo

### Dependencias de Python

Instalar todas las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

## 🚀 Compilación Rápida

### Opción 1: Todo en Uno (Recomendado)

Compila el ejecutable Y crea el instalador en un solo paso:

```bash
python build.py --all
```

Este comando:
1. ✓ Verifica todas las dependencias
2. ✓ Limpia archivos de compilación anteriores
3. ✓ Compila el ejecutable con PyInstaller
4. ✓ Crea el instalador con Inno Setup (incluye LibreOffice)

**Resultado:**
- `dist/HidroFlowManager.exe` - Ejecutable standalone
- `dist/HydroFlowManager_Setup_v1.04.1812.exe` - Instalador completo (~50 MB)

---

### Opción 2: Solo Ejecutable

Si solo necesitas el .exe (sin instalador):

```bash
python build.py --exe
```

**Resultado:**
- `dist/HidroFlowManager.exe` - Ejecutable portable

---

### Opción 3: Solo Instalador

Si ya tienes el ejecutable y solo quieres crear el instalador:

```bash
python build.py --installer
```

**Requisito:** Debe existir `dist/HidroFlowManager.exe`

---

## 🛠️ Compilación Manual

Si prefieres ejecutar los pasos manualmente:

### Paso 1: Compilar con PyInstaller

```bash
pyinstaller --clean --noconfirm HidroFlowManager.spec
```

Esto creará:
- `build/` - Archivos temporales de compilación
- `dist/HidroFlowManager.exe` - Ejecutable final

### Paso 2: Crear Instalador con Inno Setup

**Opción A - Interfaz gráfica:**
1. Abrir Inno Setup Compiler
2. Abrir el archivo `installer.iss`
3. Clic en "Build" → "Compile"

**Opción B - Línea de comandos:**
```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

---

## 📦 Características del Instalador

El instalador creado con `installer.iss` incluye:

### ✅ Instalación Automática de LibreOffice

El instalador descarga e instala **automáticamente** LibreOffice (necesario para exportar a PDF):

- **Versión incluida:** LibreOffice 24.2.0
- **Tamaño descarga:** ~300 MB
- **Detección inteligente:** Si LibreOffice ya está instalado, se omite la descarga
- **Instalación silenciosa:** Sin intervención del usuario
- **Configurable:** El usuario puede optar por NO instalar LibreOffice

### 🎯 Otras Características

- ✓ Instalación en `C:\Program Files\HydroFlow Manager`
- ✓ Accesos directos en Menú Inicio y Escritorio
- ✓ Desinstalador completo
- ✓ Permisos adecuados para carpetas de datos
- ✓ Interfaz moderna en español
- ✓ Icono personalizado

---

## 🧹 Limpieza

Para limpiar archivos de compilación:

```bash
python build.py --clean
```

Esto elimina:
- `build/` - Archivos temporales de PyInstaller
- `dist/` - Ejecutables e instaladores generados
- `__pycache__/` - Archivos Python compilados

---

## ⚙️ Configuración Avanzada

### Modificar el archivo .spec (PyInstaller)

Edita `HidroFlowManager.spec` para:

- Cambiar icono de la aplicación
- Añadir/quitar archivos incluidos
- Modificar imports ocultos
- Cambiar opciones de compilación

**Ejemplo - Cambiar icono:**
```python
exe = EXE(
    ...
    icon=['source\\mi_icono.ico'],  # Cambiar aquí
)
```

### Modificar el instalador (Inno Setup)

Edita `installer.iss` para:

- Cambiar versión de LibreOffice incluida
- Modificar directorios de instalación
- Añadir/quitar componentes
- Personalizar interfaz

**Ejemplo - Actualizar versión de LibreOffice:**
```inno
#define LibreOfficeVersion "24.8.0"  ; Nueva versión
#define LibreOfficeURL "https://download.documentfoundation.org/libreoffice/stable/24.8.0/win/x86_64/LibreOffice_24.8.0_Win_x64.msi"
```

---

## 🐛 Solución de Problemas

### Error: "PyInstaller no está instalado"

**Solución:**
```bash
pip install pyinstaller
```

### Error: "No se encontró Inno Setup"

**Solución:**
1. Instalar Inno Setup desde: https://jrsoftware.org/isdl.php
2. O especificar ruta manualmente en `build.py`

### Error: "Módulo XXX no encontrado"

**Solución:**
```bash
pip install -r requirements.txt
```

### El ejecutable no inicia / Error al importar módulos

**Solución:**
1. Verificar que todos los módulos estén en `hiddenimports` en el archivo `.spec`
2. Ejecutar con `python build.py --clean --all` para forzar recompilación

### LibreOffice no se descarga en el instalador

**Posibles causas:**
- Sin conexión a internet durante la instalación
- Firewall bloqueando la descarga
- URL de descarga obsoleta

**Solución:**
1. Instalar LibreOffice manualmente desde: https://www.libreoffice.org
2. O actualizar la URL en `installer.iss`

---

## 📝 Estructura de Archivos Generados

```
v1.04_1812/
├── build/                          # Temporal (PyInstaller)
│   └── HidroFlowManager/
│       └── (archivos de compilación)
│
├── dist/                           # Archivos finales
│   ├── HidroFlowManager.exe       # Ejecutable standalone
│   └── HydroFlowManager_Setup_v1.04.1812.exe  # Instalador
│
├── HidroFlowManager.spec          # Configuración PyInstaller
├── installer.iss                  # Configuración Inno Setup
└── build.py                       # Script de compilación
```

---

## 📊 Tamaños Aproximados

| Archivo | Tamaño |
|---------|--------|
| `HidroFlowManager.exe` | ~80 MB |
| `HydroFlowManager_Setup_*.exe` (sin LibreOffice) | ~50 MB |
| Descarga de LibreOffice durante instalación | ~300 MB |
| Instalación completa en disco | ~500 MB |

---

## 🔐 Firma Digital (Opcional)

Para firmar el ejecutable y el instalador (recomendado para distribución):

### Firmar Ejecutable
```bash
signtool sign /f certificado.pfx /p password /t http://timestamp.digicert.com dist/HidroFlowManager.exe
```

### Firmar Instalador
```bash
signtool sign /f certificado.pfx /p password /t http://timestamp.digicert.com dist/HydroFlowManager_Setup_*.exe
```

**Requisitos:**
- Certificado de firma de código (.pfx)
- Windows SDK instalado

---

## 📞 Soporte

Si encuentras problemas durante la compilación:

1. Verifica que cumples todos los requisitos previos
2. Ejecuta `python build.py --clean --all` para recompilar desde cero
3. Revisa los logs de error en la consola
4. Consulta la sección de solución de problemas arriba

---

## 📄 Licencia

Este proyecto está bajo la licencia especificada en el archivo `LICENSE`.

---

**Última actualización:** Enero 2025
**Versión del documento:** 1.0
