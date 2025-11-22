# ============================================================================
# HydroFlow Manager v2.0 - Script de Preparacion de Base de Datos
# ============================================================================
#
# Este script ayuda a preparar la base de datos para produccion:
# 1. Crear backups de esquemas limpios (proyecto_tipo y manager)
# 2. Validar que proyecto_tipo no tiene datos de prueba
# 3. Generar reportes de validacion
# 4. Preparar scripts SQL para instalacion
#
# IMPORTANTE: Ejecutar ANTES de compilar y distribuir
#
# Requisitos:
# - MySQL Client (mysqldump) instalado y en PATH
# - Archivo .env configurado con credenciales
# - Acceso a base de datos con permisos de lectura
#
# Uso:
#   .\dev_tools\preparacion\preparar_bd_produccion.ps1
#
# ============================================================================

# Configuración de colores
$Host.UI.RawUI.ForegroundColor = "White"

function Write-Header {
    param([string]$Message)
    Write-Host ""
    Write-Host "=" * 80 -ForegroundColor Cyan
    Write-Host $Message -ForegroundColor Cyan
    Write-Host "=" * 80 -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor White
}

# ============================================================================
# PASO 1: Verificar requisitos
# ============================================================================

Write-Header "PASO 1: Verificacion de Requisitos"

# Verificar que estamos en el directorio raiz del proyecto
if (-not (Test-Path "main.py")) {
    Write-Error "Este script debe ejecutarse desde el directorio raiz del proyecto"
    exit 1
}
Write-Success "Directorio correcto"

# Verificar archivo .env
if (-not (Test-Path ".env")) {
    Write-Error "Archivo .env no encontrado"
    Write-Info "  Cree el archivo .env desde .env.example"
    Write-Info "  Consulte INSTALACION.md para mas detalles"
    exit 1
}
Write-Success "Archivo .env encontrado"

# Cargar variables de entorno desde .env
Write-Info "Cargando configuracion desde .env..."
Get-Content .env | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
        $name = $matches[1].Trim()
        $value = $matches[2].Trim()
        Set-Item -Path "env:$name" -Value $value
    }
}

# Obtener configuración
$DB_HOST = $env:DB_HOST
$DB_PORT = $env:DB_PORT
$DB_USER = $env:DB_USER
$DB_PASSWORD = $env:DB_PASSWORD
$DB_MANAGER_SCHEMA = $env:DB_MANAGER_SCHEMA
$DB_EXAMPLE_SCHEMA = if ($env:DB_EXAMPLE_SCHEMA) { $env:DB_EXAMPLE_SCHEMA } else { "proyecto_tipo" }

# Validar credenciales
if (-not $DB_USER -or -not $DB_PASSWORD) {
    Write-Error "DB_USER o DB_PASSWORD no configurados en .env"
    exit 1
}
Write-Success "Credenciales cargadas desde .env"

# Verificar mysqldump
$mysqldump = Get-Command mysqldump -ErrorAction SilentlyContinue
if (-not $mysqldump) {
    Write-Warning "mysqldump no encontrado en PATH"
    Write-Info "  Buscando en ubicaciones comunes..."

    # Ubicaciones comunes de MySQL - buscar XAMPP/WAMP primero (mas compatibles)
    $mysqlPaths = @(
        "C:\xampp\mysql\bin",
        "C:\wamp64\bin\mysql\mysql8.0.27\bin",
        "C:\wamp64\bin\mysql\mysql8.0.28\bin",
        "C:\wamp64\bin\mysql\mysql8.0.31\bin",
        "C:\wamp\bin\mysql\mysql8.0.27\bin",
        "C:\Program Files\MySQL\MySQL Server 8.0\bin",
        "C:\Program Files\MySQL\MySQL Server 8.4\bin",
        "C:\Program Files\MySQL\MySQL Server 5.7\bin"
    )

    # Buscar dinámicamente en wamp64
    if (Test-Path "C:\wamp64\bin\mysql") {
        $wampMysqlDirs = Get-ChildItem "C:\wamp64\bin\mysql" -Directory | ForEach-Object { "$($_.FullName)\bin" }
        $mysqlPaths += $wampMysqlDirs
    }

    $found = $false
    foreach ($path in $mysqlPaths) {
        if (Test-Path "$path\mysqldump.exe") {
            Write-Info "  Probando MySQL en: $path"

            # Verificar que mysql.exe funcione
            $testExe = "$path\mysql.exe"
            try {
                $testOutput = & $testExe --version 2>&1
                if ($LASTEXITCODE -eq 0) {
                    Write-Success "MySQL encontrado y funcional en: $path"
                    Write-Info "  Agregando al PATH temporalmente..."
                    $env:Path = "$path;$env:Path"
                    $found = $true
                    break
                }
            } catch {
                Write-Info "  MySQL en $path no es compatible (posible problema de arquitectura)"
                continue
            }
        }
    }

    if (-not $found) {
        Write-Error "mysqldump no encontrado o no compatible"
        Write-Info ""
        Write-Info "  SOLUCIONES:"
        Write-Info "  1. Si tiene XAMPP instalado:"
        Write-Info "     - Agregue C:\xampp\mysql\bin al PATH"
        Write-Info "  2. Si tiene MySQL instalado:"
        Write-Info "     - Agregue la carpeta bin de MySQL al PATH"
        Write-Info "  3. O ejecute este script desde MySQL Command Line Client"
        Write-Info ""
        Write-Info "  Para agregar al PATH permanentemente:"
        Write-Info "  - Win+X > Sistema > Configuracion avanzada > Variables de entorno"
        Write-Info "  - Editar PATH y agregar la ruta de MySQL bin"
        exit 1
    }

    # Verificar nuevamente
    $mysqldump = Get-Command mysqldump -ErrorAction SilentlyContinue
}
Write-Success "mysqldump disponible: $($mysqldump.Source)"

# Verificar mysql client
$mysql = Get-Command mysql -ErrorAction SilentlyContinue
if (-not $mysql) {
    Write-Error "mysql client no encontrado (deberia estar en el mismo directorio que mysqldump)"
    exit 1
}
Write-Success "mysql client disponible: $($mysql.Source)"

# ============================================================================
# PASO 2: Verificar conexión a base de datos
# ============================================================================

Write-Header "PASO 2: Verificacion de Conexion a Base de Datos"

Write-Info "Conectando a ${DB_HOST}:${DB_PORT} como $DB_USER..."

# Test de conexión
$testQuery = "SELECT VERSION();"
$testResult = & mysql -h $DB_HOST -P $DB_PORT -u $DB_USER -p"$DB_PASSWORD" -e $testQuery 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Error "No se pudo conectar a la base de datos"
    Write-Info "  Verifique las credenciales en .env"
    Write-Info "  Verifique que MySQL esté ejecutándose"
    exit 1
}

Write-Success "Conexión exitosa"
Write-Info "  Versión de MySQL: $(($testResult | Select-String 'VERSION').Line)"

# ============================================================================
# PASO 3: Validar que los esquemas existen
# ============================================================================

Write-Header "PASO 3: Validación de Esquemas"

# Verificar esquema manager
Write-Info "Verificando esquema '$DB_MANAGER_SCHEMA'..."
$checkManager = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '$DB_MANAGER_SCHEMA';"
$resultManager = & mysql -h $DB_HOST -P $DB_PORT -u $DB_USER -p"$DB_PASSWORD" -e $checkManager 2>&1

if ($LASTEXITCODE -ne 0 -or $resultManager -notmatch $DB_MANAGER_SCHEMA) {
    Write-Error "Esquema '$DB_MANAGER_SCHEMA' no existe"
    Write-Info "  Cree el esquema manager antes de continuar"
    exit 1
}
Write-Success "Esquema '$DB_MANAGER_SCHEMA' encontrado"

# Verificar esquema proyecto_tipo
Write-Info "Verificando esquema '$DB_EXAMPLE_SCHEMA'..."
$checkExample = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '$DB_EXAMPLE_SCHEMA';"
$resultExample = & mysql -h $DB_HOST -P $DB_PORT -u $DB_USER -p"$DB_PASSWORD" -e $checkExample 2>&1

if ($LASTEXITCODE -ne 0 -or $resultExample -notmatch $DB_EXAMPLE_SCHEMA) {
    Write-Error "Esquema '$DB_EXAMPLE_SCHEMA' no existe"
    Write-Info "  Cree el esquema proyecto_tipo antes de continuar"
    exit 1
}
Write-Success "Esquema '$DB_EXAMPLE_SCHEMA' encontrado"

# ============================================================================
# PASO 4: Validar que proyecto_tipo está limpio (sin datos de prueba)
# ============================================================================

Write-Header "PASO 4: Validación de Datos en proyecto_tipo"

Write-Info "Verificando que '$DB_EXAMPLE_SCHEMA' no tiene datos de prueba..."

# Tablas que NO deben tener datos (datos transaccionales)
$tablasDatos = @(
    "tbl_partes",
    "tbl_part_presupuesto",
    "tbl_part_certificacion"
)

$datosEncontrados = $false

foreach ($tabla in $tablasDatos) {
    $countQuery = "SELECT COUNT(*) as count FROM ${DB_EXAMPLE_SCHEMA}.${tabla};"
    $result = & mysql -h $DB_HOST -P $DB_PORT -u $DB_USER -p"$DB_PASSWORD" -N -e $countQuery 2>&1

    if ($LASTEXITCODE -eq 0) {
        $count = [int]($result -replace '\s', '')
        if ($count -gt 0) {
            Write-Warning "Tabla '$tabla' tiene $count registros"
            $datosEncontrados = $true
        } else {
            Write-Success "Tabla '$tabla' está vacía"
        }
    }
}

if ($datosEncontrados) {
    Write-Warning "Se encontraron datos de prueba en '$DB_EXAMPLE_SCHEMA'"
    Write-Info "  RECOMENDACION: Limpie los datos antes de crear el backup"
    Write-Info "  Las tablas de catalogos (tbl_pres_precios, etc.) pueden tener datos"
    Write-Info ""
    $continuar = Read-Host "Desea continuar de todos modos? (s/n)"
    if ($continuar -ne "s") {
        Write-Info "Operacion cancelada por el usuario"
        exit 0
    }
} else {
    Write-Success "Esquema '$DB_EXAMPLE_SCHEMA' esta limpio (sin datos transaccionales)"
}

# ============================================================================
# PASO 5: Crear directorio de backups
# ============================================================================

Write-Header "PASO 5: Preparacion de Directorio de Backups"

$backupDir = "backups/produccion"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupPath = "$backupDir/$timestamp"

if (-not (Test-Path $backupPath)) {
    New-Item -ItemType Directory -Path $backupPath -Force | Out-Null
    Write-Success "Directorio creado: $backupPath"
} else {
    Write-Success "Directorio ya existe: $backupPath"
}

# ============================================================================
# PASO 6: Backup del esquema manager (solo estructura + datos de referencia)
# ============================================================================

Write-Header "PASO 6: Backup de Esquema 'manager'"

$managerBackup = "$backupPath/manager_estructura_y_datos.sql"

Write-Info "Creando backup de '$DB_MANAGER_SCHEMA' (estructura + datos)..."
Write-Info "  Destino: $managerBackup"

& mysqldump -h $DB_HOST -P $DB_PORT -u $DB_USER -p"$DB_PASSWORD" `
    --single-transaction `
    --routines `
    --triggers `
    --events `
    --databases $DB_MANAGER_SCHEMA `
    --result-file=$managerBackup 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Error "Error al crear backup de '$DB_MANAGER_SCHEMA'"
    exit 1
}

$fileSize = (Get-Item $managerBackup).Length / 1KB
$fileSizeRounded = [math]::Round($fileSize, 2)
Write-Success "Backup creado: $managerBackup ($fileSizeRounded KB)"

# ============================================================================
# PASO 7: Backup del esquema proyecto_tipo (estructura + catálogos)
# ============================================================================

Write-Header "PASO 7: Backup de Esquema 'proyecto_tipo'"

$proyectoTipoBackup = "$backupPath/proyecto_tipo_completo.sql"

Write-Info "Creando backup de '$DB_EXAMPLE_SCHEMA' (estructura + datos de catálogo)..."
Write-Info "  Destino: $proyectoTipoBackup"

& mysqldump -h $DB_HOST -P $DB_PORT -u $DB_USER -p"$DB_PASSWORD" `
    --single-transaction `
    --routines `
    --triggers `
    --events `
    --databases $DB_EXAMPLE_SCHEMA `
    --result-file=$proyectoTipoBackup 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Error "Error al crear backup de '$DB_EXAMPLE_SCHEMA'"
    exit 1
}

$fileSize = (Get-Item $proyectoTipoBackup).Length / 1KB
$fileSizeRounded = [math]::Round($fileSize, 2)
Write-Success "Backup creado: $proyectoTipoBackup ($fileSizeRounded KB)"

# Tambien crear backup de solo estructura (sin datos)
$proyectoTipoEstructura = "$backupPath/proyecto_tipo_solo_estructura.sql"

Write-Info "Creando backup de estructura (sin datos)..."
Write-Info "  Destino: $proyectoTipoEstructura"

& mysqldump -h $DB_HOST -P $DB_PORT -u $DB_USER -p"$DB_PASSWORD" `
    --single-transaction `
    --no-data `
    --routines `
    --triggers `
    --events `
    --databases $DB_EXAMPLE_SCHEMA `
    --result-file=$proyectoTipoEstructura 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Error "Error al crear backup de estructura"
    exit 1
}

$fileSize = (Get-Item $proyectoTipoEstructura).Length / 1KB
$fileSizeRounded = [math]::Round($fileSize, 2)
Write-Success "Backup de estructura creado: $proyectoTipoEstructura ($fileSizeRounded KB)"

# ============================================================================
# PASO 8: Generar reporte de validacion
# ============================================================================

Write-Header "PASO 8: Generacion de Reporte de Validacion"

$reportePath = "$backupPath/reporte_validacion.txt"

Write-Info "Generando reporte de validacion..."

$reporte = @"
================================================================================
REPORTE DE VALIDACION - PREPARACION PARA PRODUCCION
================================================================================

Fecha y hora: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Usuario: $env:USERNAME
Host BD: ${DB_HOST}:${DB_PORT}

================================================================================
ESQUEMAS PROCESADOS
================================================================================

1. ESQUEMA MANAGER: $DB_MANAGER_SCHEMA
   - Backup completo: manager_estructura_y_datos.sql
   - Contiene: Tabla de proyectos y configuracion global

2. ESQUEMA PROYECTO_TIPO: $DB_EXAMPLE_SCHEMA
   - Backup completo: proyecto_tipo_completo.sql
   - Backup estructura: proyecto_tipo_solo_estructura.sql
   - Contiene: Estructura de tablas + catalogos de precios

================================================================================
VALIDACION DE DATOS
================================================================================

Tablas transaccionales en '$DB_EXAMPLE_SCHEMA':

"@

foreach ($tabla in $tablasDatos) {
    $countQuery = "SELECT COUNT(*) as count FROM ${DB_EXAMPLE_SCHEMA}.${tabla};"
    $result = & mysql -h $DB_HOST -P $DB_PORT -u $DB_USER -p"$DB_PASSWORD" -N -e $countQuery 2>&1

    if ($LASTEXITCODE -eq 0) {
        $count = [int]($result -replace '\s', '')
        if ($count -eq 0) {
            $status = "OK (vacia)"
        } else {
            $status = "ADVERTENCIA ($count registros)"
        }
        $reporte += "`r`n  - ${tabla}: $status"
    }
}

$reporte += @"


================================================================================
CATALOGOS EN '$DB_EXAMPLE_SCHEMA'
================================================================================

"@

# Verificar tablas de catalogo
$tablasCatalogo = @("tbl_pres_precios")

foreach ($tabla in $tablasCatalogo) {
    $countQuery = "SELECT COUNT(*) as count FROM ${DB_EXAMPLE_SCHEMA}.${tabla};"
    $result = & mysql -h $DB_HOST -P $DB_PORT -u $DB_USER -p"$DB_PASSWORD" -N -e $countQuery 2>&1

    if ($LASTEXITCODE -eq 0) {
        $count = [int]($result -replace '\s', '')
        $reporte += "`r`n  - ${tabla}: $count registros"
    }
}

$reporte += @"


================================================================================
ARCHIVOS GENERADOS
================================================================================

  - $managerBackup
  - $proyectoTipoBackup
  - $proyectoTipoEstructura
  - $reportePath

================================================================================
PROXIMOS PASOS
================================================================================

1. Revisar este reporte de validacion

2. Si hay advertencias, considere limpiar datos de prueba:
   - DELETE FROM tbl_partes WHERE codigo LIKE 'TEST%';
   - DELETE FROM tbl_part_presupuesto WHERE parte_id NOT IN (SELECT id FROM tbl_partes);
   - DELETE FROM tbl_part_certificacion WHERE parte_id NOT IN (SELECT id FROM tbl_partes);

3. Si todo esta correcto, puede proceder con la compilacion:
   - Ejecute: .\build.ps1
   - Consulte: docs/COMPILACION_Y_DISTRIBUCION.md

4. Los backups estan listos para:
   - Instalacion en nuevos servidores
   - Recuperacion de desastres
   - Distribucion con la aplicacion

================================================================================
FIN DEL REPORTE
================================================================================
"@

$reporte | Out-File -FilePath $reportePath -Encoding UTF8

Write-Success "Reporte generado: $reportePath"

# Mostrar resumen
Write-Host ""
Write-Host ("=" * 80) -ForegroundColor Green
Write-Host "PREPARACION COMPLETADA EXITOSAMENTE" -ForegroundColor Green
Write-Host ("=" * 80) -ForegroundColor Green
Write-Host ""
Write-Info "Backups creados en: $backupPath"
Write-Info "  - manager_estructura_y_datos.sql"
Write-Info "  - proyecto_tipo_completo.sql"
Write-Info "  - proyecto_tipo_solo_estructura.sql"
Write-Info "  - reporte_validacion.txt"
Write-Host ""
Write-Info "Revise el reporte de validacion para verificar que todo esta correcto"
Write-Host ""

# Abrir reporte automaticamente
$abrir = Read-Host "Desea abrir el reporte de validacion? (s/n)"
if ($abrir -eq "s") {
    notepad $reportePath
}

Write-Host ""
Write-Success "Proceso completado. La base de datos esta lista para produccion."
Write-Host ""
