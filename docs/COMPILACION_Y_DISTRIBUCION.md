# Guía de Compilación y Distribución - HydroFlow Manager v2.0

## 📦 Compilación del Ejecutable

### Requisitos Previos

1. **Python 3.8 o superior** instalado
2. **Entorno virtual** configurado con todas las dependencias:
   ```powershell
   pip install -r requirements.txt
   pip install pyinstaller
   ```
3. **Windows** (para generar ejecutable .exe de Windows)

### Proceso de Compilación

#### Opción A: Script Automatizado (Recomendado)

```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Ejecutar script de compilación
.\build.ps1
```

El script automáticamente:
- ✅ Verifica dependencias
- ✅ Limpia compilaciones anteriores
- ✅ Compila con PyInstaller
- ✅ Verifica el resultado

#### Opción B: Compilación Manual

```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Limpiar compilaciones anteriores (opcional)
Remove-Item -Recurse -Force build, dist

# Compilar
pyinstaller HidroFlowManager.spec --clean --noconfirm
```

### Resultado de la Compilación

Después de la compilación exitosa, encontrarás:

```
dist/
  └── HidroFlowManager.exe    # Ejecutable principal (~100-150 MB)
```

## 📂 Preparación del Paquete de Distribución

### Estructura del Paquete

Crear una carpeta con la siguiente estructura para distribuir:

```
HydroFlowManager_v2.0/
├── HidroFlowManager.exe      # Ejecutable compilado
├── .env.example              # Plantilla de configuración
├── INSTALACION.md            # Guía de instalación
└── docs/
    └── manual/
        ├── Manual_Usuario_v2.0.md
        ├── Manual_Tecnico_v2.0.md
        ├── Manual_Informes_v2.0.md
        └── Guia_Instalacion_BD_v2.0.md
```

### Script de Empaquetado

```powershell
# Crear carpeta de distribución
$version = "2.0"
$distFolder = "HydroFlowManager_v$version"

New-Item -ItemType Directory -Force -Path $distFolder

# Copiar archivos necesarios
Copy-Item "dist\HidroFlowManager.exe" -Destination $distFolder
Copy-Item ".env.example" -Destination $distFolder
Copy-Item "INSTALACION.md" -Destination $distFolder
Copy-Item "docs\manual" -Destination "$distFolder\docs" -Recurse

# Crear archivo ZIP
Compress-Archive -Path $distFolder -DestinationPath "HydroFlowManager_v$version.zip"

Write-Host "✅ Paquete creado: HydroFlowManager_v$version.zip"
```

## 🚀 Distribución

### Contenido del Paquete

El paquete ZIP debe incluir:

1. **HidroFlowManager.exe** - Ejecutable principal
2. **.env.example** - Plantilla de configuración (IMPORTANTE)
3. **INSTALACION.md** - Instrucciones de instalación
4. **docs/manual/** - Documentación completa

### Instrucciones para el Cliente

Proporcionar al cliente:

1. **Archivo ZIP** con el paquete completo
2. **Credenciales de base de datos** (separadas, seguras)
3. **Instrucciones de instalación** (ver INSTALACION.md)

### Pasos de Instalación en Cliente

El cliente debe:

1. **Descomprimir** el archivo ZIP
2. **Crear archivo .env** desde .env.example:
   ```powershell
   cd HydroFlowManager_v2.0
   copy .env.example .env
   notepad .env
   ```
3. **Configurar credenciales** en .env:
   ```bash
   DB_HOST=localhost
   DB_PORT=3307
   DB_USER=su_usuario
   DB_PASSWORD=su_contraseña
   DB_SCHEMA=cert_dev
   DB_MANAGER_SCHEMA=manager
   ```
4. **Ejecutar** HidroFlowManager.exe

## 🔧 Troubleshooting de Compilación

### Error: "PyInstaller not found"

**Solución:**
```powershell
pip install pyinstaller
```

### Error: "Module not found" durante compilación

**Causa:** Falta una dependencia en requirements.txt o en hiddenimports del .spec

**Solución:**
1. Instalar la dependencia faltante
2. Agregar a `hiddenimports` en HidroFlowManager.spec
3. Recompilar

### Error: Ejecutable muy grande (>200 MB)

**Causa:** PyInstaller incluye muchas bibliotecas

**Solución:**
1. Revisar excludes en .spec
2. Considerar compilación con --onedir en lugar de --onefile (más rápido de iniciar)

### Error al ejecutar el .exe: "Failed to execute script"

**Posibles causas:**
1. Falta algún recurso (imagen, archivo)
2. Problema con rutas relativas
3. Módulo no incluido en hiddenimports

**Solución:**
1. Revisar logs de PyInstaller
2. Probar en modo debug: pyinstaller --debug=all
3. Verificar que todos los recursos estén en datas

## 📋 Checklist Pre-Distribución

Antes de entregar al cliente, verificar:

- [ ] Ejecutable compila sin errores
- [ ] Ejecutable inicia correctamente (en máquina limpia si es posible)
- [ ] Login funciona con credenciales de prueba
- [ ] .env.example está incluido
- [ ] INSTALACION.md está incluido
- [ ] Manuales están incluidos
- [ ] Versión correcta mostrada en "Acerca de" (v2.0)
- [ ] Tamaño del paquete es razonable (~100-150 MB)
- [ ] Archivo ZIP creado correctamente

## 🔐 Seguridad

**IMPORTANTE - NO incluir:**
- ❌ Archivo `.env` con credenciales reales
- ❌ Archivos de base de datos (.sql con datos sensibles)
- ❌ Logs con información sensible
- ❌ Archivos de backup con datos

**SÍ incluir:**
- ✅ `.env.example` (plantilla sin credenciales)
- ✅ Documentación
- ✅ Ejecutable
- ✅ Scripts SQL de estructura (sin datos)

## 📞 Soporte Post-Instalación

Proporcionar al cliente:

1. **Documentación completa** (incluida en el paquete)
2. **Contacto de soporte** técnico
3. **Procedimiento de actualización** (futuras versiones)
4. **Backup recomendado** antes de actualizaciones
