# Script PowerShell para verificar y corregir nombres de municipios
# ===================================================================

# Configuración
$verificarScript = "script\verificar_municipios_gipuzkoa.sql"
$corregirScript = "script\corregir_nombres_municipios.sql"
$mysqlUser = "root"
$mysqlPassword = "NuevaPass!2025"
$database = "cert_dev"

# Colores para output
function Write-Success {
    param([string]$message)
    Write-Host $message -ForegroundColor Green
}

function Write-Info {
    param([string]$message)
    Write-Host $message -ForegroundColor Cyan
}

function Write-Error-Custom {
    param([string]$message)
    Write-Host $message -ForegroundColor Red
}

function Write-Warning-Custom {
    param([string]$message)
    Write-Host $message -ForegroundColor Yellow
}

# Banner
Write-Host "`n========================================================" -ForegroundColor Yellow
Write-Host "CORRECCIÓN DE NOMBRES DE MUNICIPIOS" -ForegroundColor Yellow
Write-Host "========================================================`n" -ForegroundColor Yellow

# 1. Ejecutar verificación
Write-Info "PASO 1: Verificando estado actual de municipios..."
Write-Host ""

if (-Not (Test-Path $verificarScript)) {
    Write-Error-Custom "ERROR: No se encuentra el archivo $verificarScript"
    exit 1
}

try {
    Get-Content $verificarScript | mysql -u $mysqlUser -p$mysqlPassword $database

    if ($LASTEXITCODE -ne 0) {
        Write-Error-Custom "Error al ejecutar la verificación"
        exit 1
    }
} catch {
    Write-Error-Custom "Error inesperado durante verificación: $_"
    exit 1
}

Write-Host "`n========================================================" -ForegroundColor Yellow
Write-Host "PASO 2: CORRECCIÓN" -ForegroundColor Yellow
Write-Host "========================================================`n" -ForegroundColor Yellow

Write-Warning-Custom "ATENCIÓN: Este script actualizará los nombres de 88 municipios de Gipuzkoa."
Write-Host ""
Write-Host "¿Deseas continuar con la corrección? (S/N): " -NoNewline -ForegroundColor Yellow
$confirmation = Read-Host

if ($confirmation -ne 'S' -and $confirmation -ne 's') {
    Write-Info "Operación cancelada por el usuario."
    exit 0
}

# 2. Ejecutar corrección
Write-Info "`nEjecutando corrección de nombres..."

if (-Not (Test-Path $corregirScript)) {
    Write-Error-Custom "ERROR: No se encuentra el archivo $corregirScript"
    exit 1
}

try {
    Get-Content $corregirScript | mysql -u $mysqlUser -p$mysqlPassword $database

    if ($LASTEXITCODE -eq 0) {
        Write-Success "`n✓ Corrección ejecutada exitosamente"

        Write-Host "`n========================================================" -ForegroundColor Yellow
        Write-Host "RESUMEN" -ForegroundColor Yellow
        Write-Host "========================================================`n" -ForegroundColor Yellow

        Write-Success "Los nombres de los municipios de Gipuzkoa han sido actualizados."
        Write-Info "`nVerifica los cambios ejecutando:"
        Write-Host "Get-Content $verificarScript | mysql -u $mysqlUser -p$mysqlPassword $database"

    } else {
        Write-Error-Custom "`n✗ Error al ejecutar la corrección"
        exit 1
    }

} catch {
    Write-Error-Custom "`n✗ Error inesperado: $_"
    exit 1
}

Write-Host "`n========================================================`n" -ForegroundColor Yellow
