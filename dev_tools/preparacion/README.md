# Scripts de Preparación para Producción

Este directorio contiene scripts para preparar la base de datos antes de compilar y distribuir HydroFlow Manager v2.0.

## 📋 Contenido

### `preparar_bd_produccion.ps1` (Windows)

Script PowerShell para preparar la base de datos en entornos Windows.

**Uso:**
```powershell
.\dev_tools\preparacion\preparar_bd_produccion.ps1
```

### `preparar_bd_produccion.py` (Multiplataforma)

Script Python para preparar la base de datos en Windows, Linux o Mac.

**Uso:**
```bash
python dev_tools/preparacion/preparar_bd_produccion.py
```

## 🎯 ¿Qué hacen estos scripts?

Los scripts de preparación realizan las siguientes tareas:

### 1. Verificación de Requisitos
- Verifica que el archivo `.env` esté configurado
- Valida que `mysql` y `mysqldump` estén instalados
- Comprueba las credenciales de base de datos

### 2. Validación de Conexión
- Prueba la conexión a MySQL/MariaDB
- Verifica la versión del servidor

### 3. Validación de Esquemas
- Comprueba que el esquema `manager` existe
- Comprueba que el esquema `proyecto_tipo` existe

### 4. Validación de Datos
- **Verifica que `proyecto_tipo` esté limpio** (sin datos de prueba)
- Comprueba tablas transaccionales:
  - `tbl_partes` (debe estar vacía)
  - `tbl_part_presupuesto` (debe estar vacía)
  - `tbl_part_certificacion` (debe estar vacía)
- Las tablas de catálogo (ej: `tbl_pres_precios`) **pueden** tener datos

### 5. Creación de Backups
Crea backups en `backups/produccion/<timestamp>/`:

- **`manager_estructura_y_datos.sql`**
  - Backup completo del esquema manager
  - Incluye estructura + datos de proyectos

- **`proyecto_tipo_completo.sql`**
  - Backup completo del esquema proyecto_tipo
  - Incluye estructura + datos de catálogos

- **`proyecto_tipo_solo_estructura.sql`**
  - Solo la estructura (sin datos)
  - Útil para crear proyectos vacíos

### 6. Reporte de Validación
- Genera `reporte_validacion.txt` con:
  - Información de esquemas procesados
  - Conteo de registros en tablas transaccionales
  - Conteo de registros en catálogos
  - Próximos pasos recomendados

## ⚠️ Advertencias Importantes

### Datos de Prueba en proyecto_tipo

Si el script encuentra datos de prueba en `proyecto_tipo`, mostrará advertencias:

```
⚠ Tabla 'tbl_partes' tiene 15 registros
⚠ Se encontraron datos de prueba en 'proyecto_tipo'
  RECOMENDACIÓN: Limpie los datos antes de crear el backup
```

**Solución:** Limpiar datos de prueba antes de continuar:

```sql
-- Eliminar partes de prueba
DELETE FROM tbl_partes WHERE codigo LIKE 'TEST%';

-- Eliminar presupuestos huérfanos
DELETE FROM tbl_part_presupuesto
WHERE parte_id NOT IN (SELECT id FROM tbl_partes);

-- Eliminar certificaciones huérfanas
DELETE FROM tbl_part_certificacion
WHERE parte_id NOT IN (SELECT id FROM tbl_partes);
```

### Catálogos de Precios

**Es normal y esperado** que `tbl_pres_precios` tenga datos. Esta tabla contiene:
- Catálogo de precios de referencia
- Códigos de partidas estándar
- Descripciones y costes unitarios

**NO elimine** estos datos. Son necesarios para el funcionamiento de la aplicación.

## 📁 Estructura de Backups

```
backups/
└── produccion/
    └── 20250122_143052/
        ├── manager_estructura_y_datos.sql
        ├── proyecto_tipo_completo.sql
        ├── proyecto_tipo_solo_estructura.sql
        └── reporte_validacion.txt
```

## 🔧 Requisitos Previos

### 1. Archivo .env Configurado

Debe existir un archivo `.env` en el directorio raíz con:

```bash
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_MANAGER_SCHEMA=manager
DB_EXAMPLE_SCHEMA=proyecto_tipo
```

### 2. MySQL Client Tools Instalados

**Windows:**
- Instalar MySQL Community Server
- O instalar solo MySQL Client
- Agregar al PATH: `C:\Program Files\MySQL\MySQL Server 8.0\bin`

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install mysql-client
```

**Linux (CentOS/RHEL):**
```bash
sudo yum install mysql
```

**macOS:**
```bash
brew install mysql-client
```

### 3. Permisos de Base de Datos

El usuario configurado en `.env` debe tener permisos para:
- SELECT en todos los esquemas
- Ejecutar SHOW DATABASES
- Leer INFORMATION_SCHEMA

**No requiere** permisos de escritura (solo lectura).

## 🚀 Flujo de Trabajo Recomendado

### Antes de Compilar

1. **Preparar base de datos:**
   ```powershell
   # Windows
   .\dev_tools\preparacion\preparar_bd_produccion.ps1

   # Linux/Mac
   python dev_tools/preparacion/preparar_bd_produccion.py
   ```

2. **Revisar el reporte:**
   - Abrir `backups/produccion/<timestamp>/reporte_validacion.txt`
   - Verificar que no hay advertencias
   - Si hay advertencias, limpiar datos y volver a ejecutar

3. **Compilar aplicación:**
   ```powershell
   # Windows
   .\build.ps1

   # Consultar docs/COMPILACION_Y_DISTRIBUCION.md
   ```

### Para Distribución

Los backups creados deben incluirse en la distribución:

1. **Copiar backups a directorio de distribución:**
   ```powershell
   # Crear carpeta sql/ en distribución
   mkdir dist/HydroFlowManager/sql

   # Copiar backups más recientes
   copy backups/produccion/<timestamp>/*.sql dist/HydroFlowManager/sql/
   ```

2. **Incluir en paquete ZIP:**
   - El instalador puede usar estos archivos SQL
   - El usuario puede importarlos durante la instalación

## 📝 Uso de Backups

### Restaurar Esquema manager

```bash
mysql -h localhost -u root -p < manager_estructura_y_datos.sql
```

### Restaurar Esquema proyecto_tipo

```bash
# Opción 1: Con datos de catálogo
mysql -h localhost -u root -p < proyecto_tipo_completo.sql

# Opción 2: Solo estructura (sin datos)
mysql -h localhost -u root -p < proyecto_tipo_solo_estructura.sql
```

### Crear Nuevo Proyecto desde Plantilla

```sql
-- Crear esquema del nuevo proyecto
CREATE DATABASE mi_nuevo_proyecto;

-- Importar estructura desde proyecto_tipo
USE mi_nuevo_proyecto;
SOURCE proyecto_tipo_solo_estructura.sql;
```

## 🔍 Troubleshooting

### Error: "mysql command not found"

**Solución:**
- Instalar MySQL Client
- Agregar al PATH
- Reiniciar terminal después de modificar PATH

### Error: "Access denied for user"

**Solución:**
- Verificar credenciales en `.env`
- Verificar que el usuario tiene permisos de lectura
- Probar conexión manual: `mysql -h localhost -u root -p`

### Error: "Esquema 'proyecto_tipo' no existe"

**Solución:**
- Crear el esquema antes de ejecutar el script
- O ajustar `DB_EXAMPLE_SCHEMA` en `.env` al nombre correcto

### Advertencia: "Datos de prueba encontrados"

**No es un error**, solo una advertencia.

**Opciones:**
1. Limpiar los datos y volver a ejecutar (recomendado)
2. Continuar de todos modos (el backup incluirá los datos de prueba)

## 📞 Soporte

Para más información:
- Consulte `docs/manual/Guia_Instalacion_BD_v2.0.md`
- Consulte `INSTALACION.md` en el directorio raíz
- Revise el reporte de validación generado

## 📄 Licencia

Estos scripts son parte de HydroFlow Manager v2.0 y están sujetos a la misma licencia.
