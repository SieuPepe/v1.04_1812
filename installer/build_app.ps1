# ============================================================================
# Build HydroFlow Manager Application - Compilar Aplicación Principal
# ============================================================================
#
# Este script compila la aplicación principal HydroFlow Manager en un
# ejecutable standalone con TODAS las dependencias incluidas.
#
# Requisitos:
# - PyInstaller instalado: pip install pyinstaller
# - Python 3.8+
# - Todas las dependencias instaladas: pip install -r requirements.txt
#
# Uso:
#   .\installer\build_app.ps1
#
# Resultado:
#   dist/HydroFlowManager.exe (aplicación principal)
#
# ============================================================================

$Host.UI.RawUI.ForegroundColor = "White"

Write-Host ""
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host "Build HydroFlow Manager Application v1.04" -ForegroundColor Cyan
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "main.py")) {
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

if (Test-Path "dist\HydroFlowManager.exe") {
    Write-Host "Limpiando ejecutable anterior..." -ForegroundColor Yellow
    Remove-Item "dist\HydroFlowManager.exe" -Force
}

# Compilar
Write-Host ""
Write-Host "Compilando aplicacion principal HydroFlow Manager..." -ForegroundColor Cyan
Write-Host ""

# Argumentos base de PyInstaller
$pyinstallerArgs = @(
    "main.py",
    "--name=HydroFlowManager",
    "--onefile",
    "--windowed",
    "--clean"
)

# Agregar icono si existe
if (Test-Path "resources\icon.ico") {
    $pyinstallerArgs += "--icon=resources\icon.ico"
    Write-Host "Icono incluido: resources\icon.ico" -ForegroundColor Green
} else {
    Write-Host "Icono no encontrado (opcional)" -ForegroundColor Yellow
}

# Agregar recursos necesarios
if (Test-Path "resources") {
    $pyinstallerArgs += "--add-data=resources;resources"
    Write-Host "Directorio incluido: resources\" -ForegroundColor Green
}

# Imports ocultos necesarios
$pyinstallerArgs += @(
    "--hidden-import=tkinter",
    "--hidden-import=tkinter.ttk",
    "--hidden-import=tkinter.scrolledtext",
    "--hidden-import=tkinter.filedialog",
    "--hidden-import=tkinter.messagebox",
    "--hidden-import=customtkinter",
    "--hidden-import=CTkMessagebox",
    "--hidden-import=tkcalendar",
    "--hidden-import=PIL",
    "--hidden-import=PIL._tkinter_finder",
    "--hidden-import=matplotlib",
    "--hidden-import=pandas",
    "--hidden-import=openpyxl",
    "--hidden-import=xlsxwriter",
    "--hidden-import=docx",
    "--hidden-import=reportlab",
    "--hidden-import=mysql.connector",
    "--hidden-import=dotenv",
    "--collect-all=customtkinter",
    "--collect-all=CTkMessagebox"
)

Write-Host ""
Write-Host "Iniciando compilacion (puede tardar varios minutos)..." -ForegroundColor Yellow
Write-Host ""

# Ejecutar PyInstaller
& pyinstaller $pyinstallerArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host ("=" * 80) -ForegroundColor Green
    Write-Host "Compilacion Exitosa!" -ForegroundColor Green
    Write-Host ("=" * 80) -ForegroundColor Green
    Write-Host ""

    $exePath = "dist\HydroFlowManager.exe"
    if (Test-Path $exePath) {
        $size = (Get-Item $exePath).Length / 1MB
        $sizeRounded = [math]::Round($size, 2)
        Write-Host "Ejecutable creado:" -ForegroundColor Green
        Write-Host "  Ruta: $exePath" -ForegroundColor White
        Write-Host "  Tamanio: $sizeRounded MB" -ForegroundColor White
        Write-Host ""

        Write-Host "Proximos pasos:" -ForegroundColor Cyan
        Write-Host "  1. Compile el configurador: .\installer\build_config.ps1" -ForegroundColor White
        Write-Host "  2. Luego compile el instalador: .\installer\build_inno_setup.ps1" -ForegroundColor White
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
