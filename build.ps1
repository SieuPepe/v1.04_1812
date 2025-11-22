# =============================================================================
# Script de Compilación - HydroFlow Manager v2.0
# =============================================================================
# 
# Este script compila la aplicación usando PyInstaller para crear un
# ejecutable distribuible para Windows.
#
# Requisitos:
#   - Python 3.8+
#   - Entorno virtual activado (hydroflow)
#   - PyInstaller instalado: pip install pyinstaller
#
# Uso:
#   .\build.ps1
#
# =============================================================================

Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host " HydroFlow Manager v2.0 - Script de Compilación" -ForegroundColor Cyan
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "main.py")) {
    Write-Host "❌ ERROR: No se encontró main.py" -ForegroundColor Red
    Write-Host "   Ejecuta este script desde el directorio raíz del proyecto" -ForegroundColor Yellow
    exit 1
}

# Verificar que el entorno virtual está activado
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  ADVERTENCIA: No se detectó un entorno virtual activado" -ForegroundColor Yellow
    Write-Host "   Se recomienda activar el entorno 'hydroflow' primero:" -ForegroundColor Yellow
    Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "¿Continuar de todos modos? (s/N)"
    if ($continue -ne "s") {
        exit 0
    }
}

# Verificar que PyInstaller está instalado
Write-Host "📦 Verificando PyInstaller..." -ForegroundColor Green
$pyinstaller = Get-Command pyinstaller -ErrorAction SilentlyContinue
if (-not $pyinstaller) {
    Write-Host "❌ PyInstaller no está instalado" -ForegroundColor Red
    Write-Host "   Instalando PyInstaller..." -ForegroundColor Yellow
    pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error al instalar PyInstaller" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ PyInstaller encontrado" -ForegroundColor Green
Write-Host ""

# Limpiar compilaciones anteriores
Write-Host "🧹 Limpiando compilaciones anteriores..." -ForegroundColor Green
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
    Write-Host "   ✓ Eliminado directorio 'build'" -ForegroundColor Gray
}
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
    Write-Host "   ✓ Eliminado directorio 'dist'" -ForegroundColor Gray
}
Write-Host ""

# Compilar con PyInstaller
Write-Host "🔨 Iniciando compilación..." -ForegroundColor Green
Write-Host "   Esto puede tardar varios minutos..." -ForegroundColor Yellow
Write-Host ""

pyinstaller HidroFlowManager.spec --clean --noconfirm

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Error durante la compilación" -ForegroundColor Red
    Write-Host "   Revisa los mensajes de error arriba" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "✅ Compilación completada exitosamente" -ForegroundColor Green
Write-Host ""

# Verificar que el ejecutable fue creado
if (Test-Path "dist\HidroFlowManager.exe") {
    $exeSize = (Get-Item "dist\HidroFlowManager.exe").Length / 1MB
    Write-Host "📦 Ejecutable generado: dist\HidroFlowManager.exe" -ForegroundColor Green
    Write-Host "   Tamaño: $([math]::Round($exeSize, 2)) MB" -ForegroundColor Gray
} else {
    Write-Host "❌ No se encontró el ejecutable generado" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host " PRÓXIMOS PASOS" -ForegroundColor Cyan
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Probar el ejecutable:" -ForegroundColor White
Write-Host "   .\dist\HidroFlowManager.exe" -ForegroundColor Gray
Write-Host ""
Write-Host "2. El ejecutable está en: dist\HidroFlowManager.exe" -ForegroundColor White
Write-Host ""
Write-Host "3. Para distribuir, copiar:" -ForegroundColor White
Write-Host "   - dist\HidroFlowManager.exe" -ForegroundColor Gray
Write-Host "   - .env.example (como plantilla)" -ForegroundColor Gray
Write-Host "   - INSTALACION.md (guía de instalación)" -ForegroundColor Gray
Write-Host "   - docs\manual\ (manuales de usuario)" -ForegroundColor Gray
Write-Host ""
Write-Host "4. IMPORTANTE:" -ForegroundColor Yellow
Write-Host "   - El usuario debe crear su propio archivo .env" -ForegroundColor Gray
Write-Host "   - Configurar DB_HOST, DB_PORT, DB_USER, DB_PASSWORD" -ForegroundColor Gray
Write-Host "   - Seguir las instrucciones en INSTALACION.md" -ForegroundColor Gray
Write-Host ""
Write-Host "==========================================================================" -ForegroundColor Cyan

