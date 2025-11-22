# ============================================================================
# Build Inno Setup - Compilar Instalador Profesional
# ============================================================================
#
# Este script compila el instalador profesional usando Inno Setup
#
# Requisitos:
#   - Inno Setup 6.0+ instalado
#   - HydroFlowManager.exe en dist\
#   - HydroFlowManager_Config.exe en dist\
#
# Uso:
#   .\installer\build_inno_setup.ps1
#
# Resultado:
#   dist\HydroFlowManager_v1.04_Setup.exe
#
# ============================================================================

$Host.UI.RawUI.ForegroundColor = "White"

Write-Host ""
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host "Build Inno Setup Installer - HydroFlow Manager v1.04" -ForegroundColor Cyan
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "installer\HydroFlowManager.iss")) {
    Write-Host "ERROR: Este script debe ejecutarse desde el directorio raiz del proyecto" -ForegroundColor Red
    exit 1
}

# Verificar que los ejecutables existen
if (-not (Test-Path "dist\HydroFlowManager.exe")) {
    Write-Host "ERROR: No se encontro dist\HydroFlowManager.exe" -ForegroundColor Red
    Write-Host "  Ejecute primero: .\installer\build_app.ps1" -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path "dist\HydroFlowManager_Config.exe")) {
    Write-Host "ERROR: No se encontro dist\HydroFlowManager_Config.exe" -ForegroundColor Red
    Write-Host "  Ejecute primero: .\installer\build_config.ps1" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ HydroFlowManager.exe encontrado" -ForegroundColor Green
Write-Host "✓ HydroFlowManager_Config.exe encontrado" -ForegroundColor Green
Write-Host ""

# Buscar Inno Setup Compiler
$InnoSetupPaths = @(
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    "C:\Program Files\Inno Setup 6\ISCC.exe",
    "C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
    "C:\Program Files\Inno Setup 5\ISCC.exe"
)

$ISCC = $null
foreach ($path in $InnoSetupPaths) {
    if (Test-Path $path) {
        $ISCC = $path
        break
    }
}

if (-not $ISCC) {
    Write-Host "ERROR: Inno Setup Compiler no encontrado" -ForegroundColor Red
    Write-Host ""
    Write-Host "Inno Setup no esta instalado o no esta en las rutas por defecto." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Descargue e instale Inno Setup desde:" -ForegroundColor Yellow
    Write-Host "  https://jrsoftware.org/isdl.php" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Luego ejecute este script nuevamente." -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Inno Setup Compiler encontrado: $ISCC" -ForegroundColor Green
Write-Host ""

# Limpiar instalador anterior
if (Test-Path "dist\HydroFlowManager_v1.04_Setup.exe") {
    Write-Host "Limpiando instalador anterior..." -ForegroundColor Yellow
    Remove-Item "dist\HydroFlowManager_v1.04_Setup.exe" -Force
}

# Compilar con Inno Setup
Write-Host "Compilando instalador con Inno Setup..." -ForegroundColor Cyan
Write-Host ""

& $ISCC "installer\HydroFlowManager.iss"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host ("=" * 80) -ForegroundColor Green
    Write-Host "Compilacion Exitosa!" -ForegroundColor Green
    Write-Host ("=" * 80) -ForegroundColor Green
    Write-Host ""

    $installerPath = "dist\HydroFlowManager_v1.04_Setup.exe"
    if (Test-Path $installerPath) {
        $size = (Get-Item $installerPath).Length / 1MB
        $sizeRounded = [math]::Round($size, 2)
        Write-Host "Instalador creado:" -ForegroundColor Green
        Write-Host "  Ruta: $installerPath" -ForegroundColor White
        Write-Host "  Tamanio: $sizeRounded MB" -ForegroundColor White
        Write-Host ""

        Write-Host "Este instalador incluye:" -ForegroundColor Cyan
        Write-Host "  ✓ Interfaz profesional de instalacion" -ForegroundColor White
        Write-Host "  ✓ Seleccion de carpeta de instalacion" -ForegroundColor White
        Write-Host "  ✓ Creacion de accesos directos" -ForegroundColor White
        Write-Host "  ✓ Asistente de configuracion post-instalacion" -ForegroundColor White
        Write-Host "  ✓ Todas las dependencias incluidas" -ForegroundColor White
        Write-Host ""
    }
} else {
    Write-Host ""
    Write-Host ("=" * 80) -ForegroundColor Red
    Write-Host "Error en la Compilacion" -ForegroundColor Red
    Write-Host ("=" * 80) -ForegroundColor Red
    Write-Host ""
    Write-Host "Revise los errores arriba y vuelva a intentar" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
