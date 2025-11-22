# ============================================================================
# Build All - Compilar Todo el Paquete de Instalación
# ============================================================================
#
# Este script compila TODOS los componentes del instalador en el orden correcto:
# 1. Aplicación principal (HydroFlowManager.exe)
# 2. Asistente de configuración (HydroFlowManager_Config.exe)
# 3. Instalador profesional con Inno Setup (HydroFlowManager_v1.04_Setup.exe)
#
# Requisitos:
#   - Python 3.8+
#   - PyInstaller: pip install pyinstaller
#   - Inno Setup 6.0+ instalado en la ruta por defecto
#   - Todas las dependencias: pip install -r requirements.txt
#
# Uso:
#   .\installer\build_all.ps1
#
# Resultado:
#   dist\HydroFlowManager_v1.04_Setup.exe (instalador final)
#
# ============================================================================

$Host.UI.RawUI.ForegroundColor = "White"
$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host "BUILD ALL - HydroFlow Manager v1.04" -ForegroundColor Cyan
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host ""

# Verificar directorio
if (-not (Test-Path "main.py")) {
    Write-Host "ERROR: Este script debe ejecutarse desde el directorio raiz del proyecto" -ForegroundColor Red
    exit 1
}

# ============================================================================
# PASO 1: Compilar Aplicación Principal
# ============================================================================

Write-Host ""
Write-Host ("=" * 80) -ForegroundColor Yellow
Write-Host "PASO 1/3: Compilando aplicacion principal..." -ForegroundColor Yellow
Write-Host ("=" * 80) -ForegroundColor Yellow
Write-Host ""

& .\installer\build_app.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Fallo la compilacion de la aplicacion principal" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "dist\HydroFlowManager.exe")) {
    Write-Host ""
    Write-Host "ERROR: No se encontro dist\HydroFlowManager.exe" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✓ Aplicacion principal compilada correctamente" -ForegroundColor Green

# ============================================================================
# PASO 2: Compilar Asistente de Configuración
# ============================================================================

Write-Host ""
Write-Host ("=" * 80) -ForegroundColor Yellow
Write-Host "PASO 2/3: Compilando asistente de configuracion..." -ForegroundColor Yellow
Write-Host ("=" * 80) -ForegroundColor Yellow
Write-Host ""

& .\installer\build_config.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Fallo la compilacion del asistente de configuracion" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "dist\HydroFlowManager_Config.exe")) {
    Write-Host ""
    Write-Host "ERROR: No se encontro dist\HydroFlowManager_Config.exe" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✓ Asistente de configuracion compilado correctamente" -ForegroundColor Green

# ============================================================================
# PASO 3: Compilar Instalador con Inno Setup
# ============================================================================

Write-Host ""
Write-Host ("=" * 80) -ForegroundColor Yellow
Write-Host "PASO 3/3: Compilando instalador profesional con Inno Setup..." -ForegroundColor Yellow
Write-Host ("=" * 80) -ForegroundColor Yellow
Write-Host ""

& .\installer\build_inno_setup.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Fallo la compilacion del instalador con Inno Setup" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "dist\HydroFlowManager_v1.04_Setup.exe")) {
    Write-Host ""
    Write-Host "ERROR: No se encontro dist\HydroFlowManager_v1.04_Setup.exe" -ForegroundColor Red
    exit 1
}

# ============================================================================
# FINALIZACIÓN
# ============================================================================

Write-Host ""
Write-Host ("=" * 80) -ForegroundColor Green
Write-Host "COMPILACION COMPLETA - EXITO!" -ForegroundColor Green
Write-Host ("=" * 80) -ForegroundColor Green
Write-Host ""

$installerPath = "dist\HydroFlowManager_v1.04_Setup.exe"
$size = (Get-Item $installerPath).Length / 1MB
$sizeRounded = [math]::Round($size, 2)

Write-Host "Instalador creado exitosamente:" -ForegroundColor Green
Write-Host "  Ruta: $installerPath" -ForegroundColor White
Write-Host "  Tamanio: $sizeRounded MB" -ForegroundColor White
Write-Host ""

Write-Host "Componentes incluidos:" -ForegroundColor Cyan
Write-Host "  ✓ HydroFlowManager.exe (aplicacion principal)" -ForegroundColor White
Write-Host "  ✓ HydroFlowManager_Config.exe (configurador)" -ForegroundColor White
Write-Host "  ✓ Todas las dependencias Python embebidas" -ForegroundColor White
Write-Host "  ✓ Recursos y documentacion" -ForegroundColor White
Write-Host ""

Write-Host "Caracteristicas del instalador:" -ForegroundColor Cyan
Write-Host "  ✓ Interfaz profesional estilo Windows" -ForegroundColor White
Write-Host "  ✓ Seleccion de carpeta de instalacion" -ForegroundColor White
Write-Host "  ✓ Creacion automatica de accesos directos" -ForegroundColor White
Write-Host "  ✓ Asistente de configuracion post-instalacion" -ForegroundColor White
Write-Host "  ✓ Desinstalador incluido" -ForegroundColor White
Write-Host ""

Write-Host "Proximos pasos:" -ForegroundColor Cyan
Write-Host "  1. Probar el instalador: .\$installerPath" -ForegroundColor White
Write-Host "  2. Distribuir el archivo .exe a los usuarios finales" -ForegroundColor White
Write-Host ""

# Preguntar si quiere ejecutar
$run = Read-Host "Desea ejecutar el instalador ahora? (s/n)"
if ($run -eq "s") {
    Write-Host ""
    Write-Host "Ejecutando instalador..." -ForegroundColor Yellow
    Start-Process $installerPath
}

Write-Host ""
