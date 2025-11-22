# =============================================================================
# Script de Ejecución de Tests - HydroFlow Manager v2.0
# =============================================================================
# 
# Este script ejecuta todos los tests del proyecto en orden lógico
#
# Requisitos:
#   - Entorno virtual activado (hydroflow)
#   - Archivo .env configurado con credenciales válidas
#   - Acceso a la base de datos MySQL
#
# Uso:
#   .\run_tests.ps1
#
# =============================================================================

Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host " HydroFlow Manager v2.0 - Suite de Tests" -ForegroundColor Cyan
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
    Write-Host "   Se recomienda activar el entorno 'hydroflow'" -ForegroundColor Yellow
    Write-Host ""
}

# Verificar que existe el archivo .env
if (-not (Test-Path ".env")) {
    Write-Host "❌ ERROR: No se encontró el archivo .env" -ForegroundColor Red
    Write-Host ""
    Write-Host "   El archivo .env es necesario para las credenciales de BD" -ForegroundColor Yellow
    Write-Host "   Copia .env.example como .env y configura tus credenciales:" -ForegroundColor Yellow
    Write-Host "   copy .env.example .env" -ForegroundColor Gray
    Write-Host "   notepad .env" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

# Configurar PYTHONPATH
$env:PYTHONPATH = (Get-Location).Path

Write-Host "✅ Configuración inicial verificada" -ForegroundColor Green
Write-Host ""

# Función para ejecutar un test
function Run-Test {
    param(
        [string]$TestName,
        [string]$TestPath
    )
    
    Write-Host "──────────────────────────────────────────────────────────────────────────" -ForegroundColor Gray
    Write-Host " TEST: $TestName" -ForegroundColor White
    Write-Host "──────────────────────────────────────────────────────────────────────────" -ForegroundColor Gray
    Write-Host ""
    
    python $TestPath
    $exitCode = $LASTEXITCODE
    
    Write-Host ""
    if ($exitCode -eq 0) {
        Write-Host "✅ $TestName - PASS" -ForegroundColor Green
        return $true
    } else {
        Write-Host "❌ $TestName - FAIL" -ForegroundColor Red
        return $false
    }
}

# Contadores
$totalTests = 0
$passedTests = 0

# Lista de tests a ejecutar (en orden de dependencias)
$tests = @(
    @{Name="Imports y Configuración"; Path="tests/test_imports.py"},
    @{Name="Optimizaciones"; Path="tests/test_optimizaciones.py"},
    @{Name="Presupuestos"; Path="tests/test_presupuestos.py"},
    @{Name="Certificaciones"; Path="tests/test_certificaciones.py"},
    @{Name="Flujo Completo"; Path="tests/test_flujo_completo.py"}
)

Write-Host "🧪 Ejecutando suite de tests..." -ForegroundColor Cyan
Write-Host ""

foreach ($test in $tests) {
    $totalTests++
    if (Test-Path $test.Path) {
        if (Run-Test -TestName $test.Name -TestPath $test.Path) {
            $passedTests++
        }
    } else {
        Write-Host "⚠️  $($test.Name) - SKIP (archivo no encontrado: $($test.Path))" -ForegroundColor Yellow
    }
    Write-Host ""
}

# Resumen final
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host " RESUMEN DE TESTS" -ForegroundColor Cyan
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tests ejecutados: $passedTests / $totalTests" -ForegroundColor White

$percentage = [math]::Round(($passedTests / $totalTests) * 100, 2)

if ($passedTests -eq $totalTests) {
    Write-Host "✅ TODOS LOS TESTS PASARON ($percentage%)" -ForegroundColor Green
    $exitStatus = 0
} elseif ($passedTests -ge ($totalTests * 0.8)) {
    Write-Host "⚠️  LA MAYORÍA DE TESTS PASARON ($percentage%)" -ForegroundColor Yellow
    Write-Host "   Revisa los tests fallidos arriba" -ForegroundColor Yellow
    $exitStatus = 1
} else {
    Write-Host "❌ MUCHOS TESTS FALLARON ($percentage%)" -ForegroundColor Red
    Write-Host "   Revisa los errores arriba" -ForegroundColor Yellow
    $exitStatus = 1
}

Write-Host ""
Write-Host "==========================================================================" -ForegroundColor Cyan

exit $exitStatus
