# =====================================================================
# Script de ejecución para Fase 3: dim_municipios
# =====================================================================
# Este script ejecuta el SQL de configuración de comarcas y municipios
# y realiza verificaciones automáticas de los resultados
# =====================================================================

# Configuración
$scriptPath = "script\fase3_dim_municipios.sql"
$mysqlUser = "root"
$mysqlPassword = "NuevaPass!2025"
$database = "cert_dev"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Fase 3: Configuración dim_municipios" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que existe el archivo SQL
if (-not (Test-Path $scriptPath)) {
    Write-Host "ERROR: No se encuentra el archivo $scriptPath" -ForegroundColor Red
    exit 1
}

Write-Host "1. Ejecutando script SQL..." -ForegroundColor Yellow
Write-Host ""

# Ejecutar el script SQL
$mysqlCmd = "mysql -u $mysqlUser -p$mysqlPassword $database"
Get-Content $scriptPath | & mysql -u $mysqlUser -p"$mysqlPassword" $database 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Falló la ejecución del script SQL" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "2. Script ejecutado correctamente" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Verificaciones" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificación 1: Estructura de dim_municipios
Write-Host "Verificación 1: Estructura de dim_municipios" -ForegroundColor Yellow
$query1 = "DESCRIBE dim_municipios;"
echo $query1 | mysql -u $mysqlUser -p"$mysqlPassword" $database
Write-Host ""

# Verificación 2: Comarcas por provincia
Write-Host "Verificación 2: Comarcas por provincia" -ForegroundColor Yellow
$query2 = @"
SELECT
    p.nombre AS Provincia,
    COUNT(c.id) AS Total_Comarcas
FROM dim_provincias p
LEFT JOIN dim_comarcas c ON c.provincia_id = p.id
GROUP BY p.id, p.nombre
ORDER BY p.id;
"@
echo $query2 | mysql -u $mysqlUser -p"$mysqlPassword" $database
Write-Host ""

# Verificación 3: Municipios por provincia
Write-Host "Verificación 3: Municipios por provincia" -ForegroundColor Yellow
$query3 = @"
SELECT
    p.nombre AS Provincia,
    COUNT(m.id) AS Total_Municipios
FROM dim_provincias p
LEFT JOIN dim_municipios m ON m.provincia_id = p.id
GROUP BY p.id, p.nombre
ORDER BY p.id;
"@
echo $query3 | mysql -u $mysqlUser -p"$mysqlPassword" $database
Write-Host ""
Write-Host "Esperado: Álava=51, Bizkaia=112, Gipuzkoa=88 (Total: 251)" -ForegroundColor Gray
Write-Host ""

# Verificación 4: Municipios por comarca
Write-Host "Verificación 4: Municipios por comarca" -ForegroundColor Yellow
$query4 = @"
SELECT
    c.comarca_nombre AS Comarca,
    p.nombre AS Provincia,
    COUNT(m.id) AS Total_Municipios
FROM dim_comarcas c
LEFT JOIN dim_provincias p ON c.provincia_id = p.id
LEFT JOIN dim_municipios m ON m.comarca_id = c.id
GROUP BY c.id, c.comarca_nombre, p.nombre
ORDER BY p.id, c.id;
"@
echo $query4 | mysql -u $mysqlUser -p"$mysqlPassword" $database
Write-Host ""

# Verificación 5: Primeros 10 municipios de Gipuzkoa
Write-Host "Verificación 5: Primeros 10 municipios de Gipuzkoa" -ForegroundColor Yellow
$query5 = @"
SELECT codigo_ine, nombre
FROM dim_municipios
WHERE provincia_id = 3
ORDER BY codigo_ine
LIMIT 10;
"@
echo $query5 | mysql -u $mysqlUser -p"$mysqlPassword" $database
Write-Host ""

# Verificación 6: Municipios activos por provincia
Write-Host "Verificación 6: Municipios activos/inactivos por provincia" -ForegroundColor Yellow
$query6 = @"
SELECT
    p.nombre AS Provincia,
    COUNT(*) as Total,
    SUM(m.activo) as Activos,
    COUNT(*) - SUM(m.activo) as Inactivos
FROM dim_municipios m
JOIN dim_provincias p ON m.provincia_id = p.id
GROUP BY p.id, p.nombre
ORDER BY p.id;
"@
echo $query6 | mysql -u $mysqlUser -p"$mysqlPassword" $database
Write-Host ""

# Verificación 7: Total general
Write-Host "Verificación 7: Totales generales" -ForegroundColor Yellow
$query7 = @"
SELECT
    'Provincias' as Entidad,
    COUNT(*) as Total
FROM dim_provincias
UNION ALL
SELECT
    'Comarcas',
    COUNT(*)
FROM dim_comarcas
UNION ALL
SELECT
    'Municipios',
    COUNT(*)
FROM dim_municipios;
"@
echo $query7 | mysql -u $mysqlUser -p"$mysqlPassword" $database
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Proceso completado" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "La tabla dim_municipios ha sido creada y poblada correctamente." -ForegroundColor Green
Write-Host "Revisa las verificaciones anteriores para confirmar los resultados." -ForegroundColor Green
Write-Host ""
Write-Host "Siguiente paso: Probar el programa de partes con los nuevos datos." -ForegroundColor Yellow
Write-Host ""
