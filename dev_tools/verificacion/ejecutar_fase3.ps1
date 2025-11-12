# Script PowerShell para ejecutar Fase 3: Comarcas y Municipios
# ==============================================================

# Configuración
$scriptPath = "script\fase3_comarcas_municipios.sql"
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

# Banner
Write-Host "`n================================================" -ForegroundColor Yellow
Write-Host "FASE 3: RELACIONAR COMARCAS Y COMPLETAR MUNICIPIOS" -ForegroundColor Yellow
Write-Host "================================================`n" -ForegroundColor Yellow

# Verificar que el archivo SQL existe
if (-Not (Test-Path $scriptPath)) {
    Write-Error-Custom "ERROR: No se encuentra el archivo $scriptPath"
    exit 1
}

Write-Info "Archivo SQL encontrado: $scriptPath"

# Mostrar resumen de cambios
Write-Host "`nEste script realizará las siguientes operaciones:" -ForegroundColor Yellow
Write-Host "1. Añadir campo provincia_id a dim_comarcas (tabla existente)"
Write-Host "2. Relacionar comarcas existentes de Álava (ids 1-6) con provincia_id=1"
Write-Host "3. Insertar 2 comarcas nuevas:"
Write-Host "   - Gipuzkoa (id 7, provincia_id=3)"
Write-Host "   - Bizkaia (id 8, provincia_id=2)"
Write-Host "4. Añadir campo comarca_id a tbl_municipios"
Write-Host "5. Actualizar municipios de Bizkaia con comarca_id=8"
Write-Host "6. Actualizar municipios de Álava con comarca_id=3 (LLANA)"
Write-Host "7. Insertar 88 municipios de Gipuzkoa con comarca_id=7"

# Confirmación
Write-Host "`n¿Deseas continuar? (S/N): " -NoNewline -ForegroundColor Yellow
$confirmation = Read-Host

if ($confirmation -ne 'S' -and $confirmation -ne 's') {
    Write-Info "Operación cancelada por el usuario."
    exit 0
}

# Ejecutar el script SQL
Write-Info "`nEjecutando script SQL..."

try {
    Get-Content $scriptPath | mysql -u $mysqlUser -p$mysqlPassword $database

    if ($LASTEXITCODE -eq 0) {
        Write-Success "`n✓ Script ejecutado exitosamente"

        # Mostrar estadísticas
        Write-Host "`n================================================" -ForegroundColor Yellow
        Write-Host "ESTADÍSTICAS FINALES" -ForegroundColor Yellow
        Write-Host "================================================`n" -ForegroundColor Yellow

        Write-Info "Consultando estadísticas de la base de datos..."

        $statsQuery = @"
SELECT 'COMARCAS POR PROVINCIA' AS seccion;
SELECT p.nombre AS provincia, COUNT(c.id) AS total_comarcas
FROM dim_provincias p
LEFT JOIN dim_comarcas c ON c.provincia_id = p.id
GROUP BY p.id, p.nombre
ORDER BY p.codigo;

SELECT '' AS separador;
SELECT 'MUNICIPIOS POR PROVINCIA' AS seccion;
SELECT p.nombre AS provincia, COUNT(m.id) AS total_municipios
FROM dim_provincias p
LEFT JOIN tbl_municipios m ON m.provincia_id = p.id
GROUP BY p.id, p.nombre
ORDER BY p.codigo;

SELECT '' AS separador;
SELECT 'MUNICIPIOS POR COMARCA' AS seccion;
SELECT p.nombre AS provincia, c.nombre AS comarca, COUNT(m.id) AS municipios
FROM dim_provincias p
LEFT JOIN dim_comarcas c ON c.provincia_id = p.id
LEFT JOIN tbl_municipios m ON m.comarca_id = c.id
GROUP BY p.id, p.nombre, c.id, c.nombre
ORDER BY p.codigo, c.id;
"@

        $statsQuery | mysql -u $mysqlUser -p$mysqlPassword $database

        Write-Success "`n✓ Fase 3 completada con éxito"
        Write-Info "`nPróximos pasos:"
        Write-Host "- Revisar las estadísticas anteriores"
        Write-Host "- Verificar que los municipios se han insertado correctamente"
        Write-Host "- Si es necesario, asignar municipios de Álava a sus cuadrillas específicas"
        Write-Host "- Actualizar la interfaz para usar las nuevas tablas de comarcas"

    } else {
        Write-Error-Custom "`n✗ Error al ejecutar el script SQL"
        exit 1
    }

} catch {
    Write-Error-Custom "`n✗ Error inesperado: $_"
    exit 1
}

Write-Host "`n================================================`n" -ForegroundColor Yellow
