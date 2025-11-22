# ============================================================================
# Build Installer - Compilar Wizard de Instalación
# ============================================================================
#
# Este script compila el setup_wizard.py en un ejecutable standalone (.exe)
# que puede ser distribuido a los usuarios finales.
#
# Requisitos:
# - PyInstaller instalado: pip install pyinstaller
# - Python 3.8+
#
# Uso:
#   .\installer\build_installer.ps1
#
# Resultado:
#   dist/HydroFlowManager_Setup.exe
#
# ============================================================================

$Host.UI.RawUI.ForegroundColor = "White"

Write-Host ""
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host "Build Installer - HydroFlow Manager v2.0" -ForegroundColor Cyan
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "installer\setup_wizard.py")) {
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

# Limpiar builds anteriores
if (Test-Path "build") {
    Write-Host "Limpiando directorio build..." -ForegroundColor Yellow
    Remove-Item "build" -Recurse -Force
}

if (Test-Path "dist\HydroFlowManager_Setup.exe") {
    Write-Host "Limpiando ejecutable anterior..." -ForegroundColor Yellow
    Remove-Item "dist\HydroFlowManager_Setup.exe" -Force
}

# Compilar
Write-Host ""
Write-Host "Compilando wizard de instalacion..." -ForegroundColor Cyan
Write-Host ""

$pyinstallerArgs = @(
    "installer\setup_wizard.py",
    "--name=HydroFlowManager_Setup",
    "--onefile",
    "--windowed",
    "--icon=resources\icon.ico",
    "--add-data=.env.example;.",
    "--add-data=INSTALACION.md;.",
    "--add-data=backups;backups",
    "--hidden-import=tkinter",
    "--hidden-import=tkinter.ttk",
    "--hidden-import=tkinter.scrolledtext",
    "--hidden-import=tkinter.filedialog",
    "--hidden-import=tkinter.messagebox",
    "--clean"
)

# Ejecutar PyInstaller
& pyinstaller $pyinstallerArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host ("=" * 80) -ForegroundColor Green
    Write-Host "Compilacion Exitosa!" -ForegroundColor Green
    Write-Host ("=" * 80) -ForegroundColor Green
    Write-Host ""

    $exePath = "dist\HydroFlowManager_Setup.exe"
    if (Test-Path $exePath) {
        $size = (Get-Item $exePath).Length / 1MB
        $sizeRounded = [math]::Round($size, 2)
        Write-Host "Ejecutable creado:" -ForegroundColor Green
        Write-Host "  Ruta: $exePath" -ForegroundColor White
        Write-Host "  Tamanio: $sizeRounded MB" -ForegroundColor White
        Write-Host ""

        Write-Host "Proximos pasos:" -ForegroundColor Cyan
        Write-Host "  1. Pruebe el instalador: .\$exePath" -ForegroundColor White
        Write-Host "  2. Distribuya el archivo .exe a los usuarios finales" -ForegroundColor White
        Write-Host ""

        # Preguntar si quiere ejecutar
        $run = Read-Host "Desea ejecutar el instalador ahora? (s/n)"
        if ($run -eq "s") {
            Start-Process $exePath
        }
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
