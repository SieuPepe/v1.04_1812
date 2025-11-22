# ============================================================================
# Build Config Wizard - Compilar Asistente de Configuración
# ============================================================================
#
# Este script compila el asistente de configuración post-instalación
#
# Uso:
#   .\installer\build_config.ps1
#
# Resultado:
#   dist/HydroFlowManager_Config.exe
#
# ============================================================================

$Host.UI.RawUI.ForegroundColor = "White"

Write-Host ""
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host "Build Config Wizard - HydroFlow Manager v1.04" -ForegroundColor Cyan
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "installer\config_wizard.py")) {
    Write-Host "Error: Este script debe ejecutarse desde el directorio raiz del proyecto" -ForegroundColor Red
    exit 1
}

# Verificar PyInstaller
try {
    $pyinstaller = Get-Command pyinstaller -ErrorAction Stop
    Write-Host "PyInstaller encontrado: $($pyinstaller.Source)" -ForegroundColor Green
} catch {
    Write-Host "PyInstaller no esta instalado" -ForegroundColor Red
    Write-Host "  Instalando PyInstaller..." -ForegroundColor Yellow
    pip install pyinstaller
}

# Limpiar builds anteriores del config wizard
if (Test-Path "dist\HydroFlowManager_Config.exe") {
    Write-Host "Limpiando ejecutable anterior..." -ForegroundColor Yellow
    Remove-Item "dist\HydroFlowManager_Config.exe" -Force
}

# Compilar
Write-Host ""
Write-Host "Compilando asistente de configuracion..." -ForegroundColor Cyan
Write-Host ""

# Argumentos de PyInstaller
$pyinstallerArgs = @(
    "installer\config_wizard.py",
    "--name=HydroFlowManager_Config",
    "--onefile",
    "--windowed",
    "--clean",
    "--uac-admin",
    "--hidden-import=tkinter",
    "--hidden-import=tkinter.ttk",
    "--hidden-import=tkinter.messagebox",
    "--hidden-import=mysql.connector"
)

# Agregar icono si existe
if (Test-Path "resources\images\logo.ico") {
    $pyinstallerArgs += "--icon=resources\images\logo.ico"
    Write-Host "Icono incluido: resources\images\logo.ico" -ForegroundColor Green
}

Write-Host ""

# Ejecutar PyInstaller
& pyinstaller $pyinstallerArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host ("=" * 80) -ForegroundColor Green
    Write-Host "Compilacion Exitosa!" -ForegroundColor Green
    Write-Host ("=" * 80) -ForegroundColor Green
    Write-Host ""

    $exePath = "dist\HydroFlowManager_Config.exe"
    if (Test-Path $exePath) {
        $size = (Get-Item $exePath).Length / 1MB
        $sizeRounded = [math]::Round($size, 2)
        Write-Host "Ejecutable creado:" -ForegroundColor Green
        Write-Host "  Ruta: $exePath" -ForegroundColor White
        Write-Host "  Tamanio: $sizeRounded MB" -ForegroundColor White
        Write-Host ""

        Write-Host "Proximos pasos:" -ForegroundColor Cyan
        Write-Host "  1. Compile el instalador completo: .\installer\build_inno_setup.ps1" -ForegroundColor White
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
