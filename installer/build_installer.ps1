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

# Argumentos base de PyInstaller
$pyinstallerArgs = @(
    "installer\setup_wizard.py",
    "--name=HydroFlowManager_Setup",
    "--onefile",
    "--windowed"
)

# Agregar icono si existe
if (Test-Path "resources\icon.ico") {
    $pyinstallerArgs += "--icon=resources\icon.ico"
    Write-Host "Icono incluido: resources\icon.ico" -ForegroundColor Green
} else {
    Write-Host "Icono no encontrado (opcional)" -ForegroundColor Yellow
}

# Agregar archivos de datos si existen
if (Test-Path ".env.example") {
    $pyinstallerArgs += "--add-data=.env.example;."
    Write-Host "Archivo incluido: .env.example" -ForegroundColor Green
}

if (Test-Path "INSTALACION.md") {
    $pyinstallerArgs += "--add-data=INSTALACION.md;."
    Write-Host "Archivo incluido: INSTALACION.md" -ForegroundColor Green
}

if (Test-Path "requirements.txt") {
    $pyinstallerArgs += "--add-data=requirements.txt;."
    Write-Host "Archivo incluido: requirements.txt" -ForegroundColor Green
} else {
    Write-Host "requirements.txt no encontrado (recomendado)" -ForegroundColor Yellow
}

# Agregar backups solo si existe el directorio
if (Test-Path "backups") {
    $pyinstallerArgs += "--add-data=backups;backups"
    Write-Host "Directorio incluido: backups\" -ForegroundColor Green
} else {
    Write-Host "Directorio backups\ no encontrado (opcional)" -ForegroundColor Yellow
    Write-Host "  El instalador permitira seleccionar archivos SQL manualmente" -ForegroundColor Yellow
}

# Agregar imports y opciones finales
$pyinstallerArgs += @(
    "--hidden-import=tkinter",
    "--hidden-import=tkinter.ttk",
    "--hidden-import=tkinter.scrolledtext",
    "--hidden-import=tkinter.filedialog",
    "--hidden-import=tkinter.messagebox",
    "--clean"
)

Write-Host ""

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
