# Script PowerShell para ejecutar fase2_provincias_municipios.sql
# Busca automáticamente la instalación de MySQL

Write-Host "Buscando MySQL..." -ForegroundColor Cyan

# Rutas comunes donde MySQL suele estar instalado
$mysqlPaths = @(
    "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe",
    "C:\Program Files\MySQL\MySQL Server 8.3\bin\mysql.exe",
    "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
    "C:\Program Files (x86)\MySQL\MySQL Server 8.4\bin\mysql.exe",
    "C:\Program Files (x86)\MySQL\MySQL Server 8.3\bin\mysql.exe",
    "C:\Program Files (x86)\MySQL\MySQL Server 8.0\bin\mysql.exe",
    "C:\xampp\mysql\bin\mysql.exe",
    "C:\wamp64\bin\mysql\mysql8.0.39\bin\mysql.exe",
    "C:\wamp\bin\mysql\mysql8.0.39\bin\mysql.exe"
)

# Buscar MySQL en las rutas comunes
$mysqlExe = $null
foreach ($path in $mysqlPaths) {
    if (Test-Path $path) {
        $mysqlExe = $path
        Write-Host "✓ MySQL encontrado en: $mysqlExe" -ForegroundColor Green
        break
    }
}

# Si no se encontró en rutas comunes, buscar en Program Files
if (-not $mysqlExe) {
    Write-Host "Buscando en directorios de MySQL..." -ForegroundColor Yellow

    $mysqlDirs = Get-ChildItem "C:\Program Files\MySQL" -Directory -ErrorAction SilentlyContinue |
                 Where-Object { $_.Name -like "MySQL Server*" }

    if ($mysqlDirs) {
        $latestVersion = $mysqlDirs | Sort-Object Name -Descending | Select-Object -First 1
        $testPath = Join-Path $latestVersion.FullName "bin\mysql.exe"
        if (Test-Path $testPath) {
            $mysqlExe = $testPath
            Write-Host "✓ MySQL encontrado en: $mysqlExe" -ForegroundColor Green
        }
    }
}

# Si aún no se encuentra, mostrar instrucciones
if (-not $mysqlExe) {
    Write-Host "`n❌ No se encontró MySQL en rutas comunes." -ForegroundColor Red
    Write-Host "`nOpciones:" -ForegroundColor Yellow
    Write-Host "1. Busca manualmente mysql.exe en tu sistema"
    Write-Host "2. O ejecuta el script en MySQL Workbench:"
    Write-Host "   - Abre MySQL Workbench"
    Write-Host "   - Conecta a cert_dev"
    Write-Host "   - File > Open SQL Script"
    Write-Host "   - Selecciona: script\fase2_provincias_municipios.sql"
    Write-Host "   - Presiona el rayo (Execute) o Ctrl+Shift+Enter"
    Write-Host "`n3. O ejecuta con la ruta completa:" -ForegroundColor Cyan
    Write-Host '   & "C:\Ruta\Completa\mysql.exe" -u root -pNuevaPass!2025 cert_dev < script\fase2_provincias_municipios.sql'
    exit 1
}

# Ejecutar el script SQL
Write-Host "`nEjecutando script SQL..." -ForegroundColor Cyan
Write-Host "Archivo: script\fase2_provincias_municipios.sql" -ForegroundColor Gray
Write-Host "Base de datos: cert_dev" -ForegroundColor Gray

try {
    $scriptPath = "script\fase2_provincias_municipios.sql"

    if (-not (Test-Path $scriptPath)) {
        Write-Host "❌ Error: No se encuentra el archivo $scriptPath" -ForegroundColor Red
        Write-Host "Asegúrate de ejecutar este script desde el directorio raíz del proyecto." -ForegroundColor Yellow
        exit 1
    }

    # Ejecutar MySQL
    Get-Content $scriptPath | & $mysqlExe -u root -pNuevaPass!2025 cert_dev

    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✓ Script ejecutado exitosamente!" -ForegroundColor Green
        Write-Host "`nVerificando resultados..." -ForegroundColor Cyan

        # Verificar los resultados
        $verifyQuery = "SELECT p.nombre AS provincia, p.nombre_euskera, COUNT(m.id) AS total_municipios FROM dim_provincias p LEFT JOIN tbl_municipios m ON m.provincia_id = p.id GROUP BY p.id, p.nombre, p.nombre_euskera ORDER BY p.codigo;"

        Write-Host "`nResumen de municipios por provincia:" -ForegroundColor Cyan
        $verifyQuery | & $mysqlExe -u root -pNuevaPass!2025 cert_dev -t

        Write-Host "`n✓ Fase 2 completada exitosamente!" -ForegroundColor Green
        Write-Host "Ahora puedes continuar con la actualización de las interfaces." -ForegroundColor Yellow
    } else {
        Write-Host "`n❌ Error al ejecutar el script. Código de salida: $LASTEXITCODE" -ForegroundColor Red
        Write-Host "Revisa los mensajes de error anteriores." -ForegroundColor Yellow
    }
} catch {
    Write-Host "`n❌ Error: $_" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}
