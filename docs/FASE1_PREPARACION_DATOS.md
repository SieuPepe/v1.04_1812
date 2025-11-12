# FASE 1: PREPARACIÓN DE DATOS

**HydroFlow Manager v1.04**
**Duración estimada:** 1-2 días
**Estado:** En progreso

---

## Objetivo

Preparar y validar los datos del sistema mediante:
1. Verificación de base de datos limpia
2. Carga de presupuesto desde Excel
3. Importación de partes desde Access
4. Testing completo de informes

Cada paso genera un backup incremental para poder restaurar en caso de problemas.

---

## Requisitos Previos

### Software necesario

- Python 3.7+
- MySQL Server 8.0+ (puerto 3307 por defecto)
- mysqldump (incluido con MySQL)

### Datos necesarios

- ✓ Base de datos MySQL corriendo y accesible
- ⏳ Archivo Excel con presupuesto (estructura requerida abajo)
- ✓ Archivo Access: `APLICACION CERTIFICACIONES UTE REDES URBIDE.accdb`

### Estructura del archivo Excel de presupuesto

El archivo Excel debe contener **exactamente** estas 4 hojas:

| Hoja | Columnas requeridas |
|------|-------------------|
| `tbl_pres_naturaleza` | `tipo` |
| `tbl_pres_unidades` | `unidad` |
| `tbl_pres_capitulos` | `codigo_capitulo`, `naturaleza`, `capitulo` |
| `tbl_pres_precios` | `codigo_partida`, `naturaleza`, `unidades`, `resumen`, `descripcion`, `coste`, `codigo_capitulo` |

---

## Scripts Disponibles

### 1. `verificar_db_limpia.py`

Verifica que las tablas de presupuesto y partes estén vacías.

```bash
python3 script/verificar_db_limpia.py [esquema]
```

**Salida esperada:**
```
======================================================================
VERIFICANDO BASE DE DATOS: proyecto_tipo
======================================================================

  tbl_presupuesto               ✓ VACÍA
  tbl_pres_certificacion        ✓ VACÍA
  tbl_proy_presupuesto          ✓ VACÍA
  tbl_partes                    ✓ VACÍA
  tbl_partes_materiales         ✓ VACÍA
  tbl_partes_maquinaria         ✓ VACÍA
  tbl_partes_mano_obra          ✓ VACÍA

======================================================================
✓ LA BASE DE DATOS ESTÁ LIMPIA (SIN PRESUPUESTOS NI PARTES)
======================================================================
```

### 2. `crear_backup.py`

Crea un backup completo de un esquema MySQL.

```bash
python3 script/crear_backup.py <nombre_backup> [esquema] [descripcion]
```

**Ejemplos:**
```bash
# Backup de BBDD limpia
python3 script/crear_backup.py backup_nopres_nopartes proyecto_tipo "BBDD limpia"

# Backup con presupuesto
python3 script/crear_backup.py backup_con_presupuesto proyecto_tipo "Con presupuesto"

# Backup completo
python3 script/crear_backup.py backup_completo_pruebas proyecto_tipo "Completo con partes"
```

**Ubicación de backups:** `backup/`

### 3. `cargar_presupuesto.py`

Importa presupuesto desde archivo Excel.

```bash
python3 script/cargar_presupuesto.py <archivo_excel>
```

**Ejemplo:**
```bash
python3 script/cargar_presupuesto.py ~/presupuesto_proyecto.xlsx
```

### 4. `importar_partes_access.py`

Importa partes desde base de datos Microsoft Access.

```bash
python3 script/importar_partes_access.py <archivo_access.accdb> [metodo]
```

**Métodos disponibles:**
- `auto` - Detecta automáticamente (por defecto)
- `pyodbc` - Usa pyodbc (requiere drivers ODBC)
- `mdbtools` - Usa mdbtools (Linux)
- `csv` - Importa desde CSV exportado manualmente

**Ejemplo:**
```bash
python3 script/importar_partes_access.py "APLICACION CERTIFICACIONES UTE REDES URBIDE.accdb"
```

**Nota sobre Access:**
La importación desde Access en Linux requiere herramientas adicionales:
- **Opción 1 (pyodbc):** Requiere drivers ODBC de Microsoft
- **Opción 2 (mdbtools):** Solo para .mdb (Access antiguo)
- **Opción 3 (CSV):** Exportar manualmente desde Access y luego importar

### 5. `fase1_preparacion_datos.py` ⭐ SCRIPT MAESTRO

Ejecuta automáticamente todos los pasos de la FASE 1.

```bash
python3 script/fase1_preparacion_datos.py
```

Este script es **interactivo** y te guía paso a paso.

---

## Procedimiento Manual (Paso a Paso)

### PASO 1: Verificar BBDD limpia y crear backup

```bash
# 1.1. Verificar que la BBDD está limpia
python3 script/verificar_db_limpia.py proyecto_tipo

# 1.2. Si está limpia, crear backup
python3 script/crear_backup.py backup_nopres_nopartes proyecto_tipo \
  "BBDD limpia sin presupuestos ni partes"
```

**Resultado esperado:**
- ✓ Script de verificación confirma BBDD limpia
- ✓ Archivo creado: `backup/backup_nopres_nopartes.sql` (~4.6 MB)

---

### PASO 2: Cargar presupuesto y crear backup

```bash
# 2.1. Cargar presupuesto desde Excel
python3 script/cargar_presupuesto.py ~/ruta/al/presupuesto.xlsx

# 2.2. Crear backup con presupuesto
python3 script/crear_backup.py backup_con_presupuesto proyecto_tipo \
  "BBDD con presupuesto cargado"
```

**Resultado esperado:**
- ✓ Presupuesto cargado exitosamente
- ✓ Archivo creado: `backup/backup_con_presupuesto.sql` (~5.0 MB)
- ✓ Tablas pobladas: `tbl_pres_naturaleza`, `tbl_pres_unidades`, `tbl_pres_capitulos`, `tbl_pres_precios`

---

### PASO 3: Cargar partes (Access) y crear backup

```bash
# 3.1. Importar partes desde Access
python3 script/importar_partes_access.py \
  "APLICACION CERTIFICACIONES UTE REDES URBIDE.accdb"

# 3.2. Crear backup completo
python3 script/crear_backup.py backup_completo_pruebas proyecto_tipo \
  "BBDD completa con presupuestos y partes de prueba"
```

**Resultado esperado:**
- ✓ Partes importados desde Access
- ✓ Archivo creado: `backup/backup_completo_pruebas.sql` (~5.2 MB)
- ✓ Tabla `tbl_partes` poblada con datos

**Si la importación desde Access falla:**

Ver sección "Solución de Problemas" más abajo.

---

### PASO 4: Testing completo de informes

Este paso es **manual** y requiere:

1. **Iniciar la aplicación**
   ```bash
   python3 main.py
   ```

2. **Generar todos los informes disponibles:**
   - Informes de partes
   - Informes de certificaciones
   - Informes agrupados (por red, municipio, tipo de trabajo, etc.)
   - Informes con filtros

3. **Verificar datos:**
   - ✓ Todos los campos se muestran correctamente
   - ✓ Los cálculos son correctos
   - ✓ Los totales coinciden
   - ✓ No hay datos faltantes o NULL inesperados

4. **Comparar con informes del cliente:**
   - Abrir informes del cliente (en `INFORME TIPO/`)
   - Comparar estructura y datos
   - Documentar diferencias

5. **Documentar resultados:**
   - Anotar cualquier discrepancia
   - Capturar pantallas si es necesario
   - Preparar lista de ajustes necesarios

---

## Procedimiento Automático (Recomendado)

```bash
python3 script/fase1_preparacion_datos.py
```

El script maestro ejecuta todos los pasos automáticamente y te guía de forma interactiva.

---

## Verificación de Resultados

Al finalizar la FASE 1, debes tener:

### Archivos de Backup

```bash
ls -lh backup/
```

Deberías ver:
- ✓ `backup_nopres_nopartes.sql` - Base limpia
- ✓ `backup_con_presupuesto.sql` - Con presupuesto
- ✓ `backup_completo_pruebas.sql` - Completo con partes

### Base de Datos Poblada

```sql
-- Conectar a MySQL
mysql -h localhost -P 3307 -u root -p

-- Verificar datos
USE proyecto_tipo;

-- Contar registros de presupuesto
SELECT COUNT(*) as total_capitulos FROM tbl_pres_capitulos;
SELECT COUNT(*) as total_precios FROM tbl_pres_precios;

-- Contar partes
SELECT COUNT(*) as total_partes FROM tbl_partes;

-- Ver muestra de datos
SELECT * FROM tbl_partes LIMIT 5;
```

### Informes Generados

Carpeta con capturas de pantalla de todos los informes probados.

---

## Solución de Problemas

### MySQL no está disponible

**Error:**
```
✗ ERROR DE CONEXIÓN: 2003 (HY000): Can't connect to MySQL server on 'localhost:3307'
```

**Solución:**
```bash
# Verificar si MySQL está corriendo
ps aux | grep mysql

# En Docker
docker ps | grep mysql
docker-compose up -d mysql

# Servicio del sistema
sudo systemctl start mysql

# Verificar puerto
netstat -tlnp | grep 3307
```

### Error al importar presupuesto

**Error:** "No se encontraron las hojas requeridas"

**Solución:**
1. Abrir el archivo Excel
2. Verificar que tiene exactamente estas hojas:
   - `tbl_pres_naturaleza`
   - `tbl_pres_unidades`
   - `tbl_pres_capitulos`
   - `tbl_pres_precios`
3. Verificar nombres exactos (sensible a mayúsculas/minúsculas)

### Error al importar desde Access (Linux)

**Problema:** pyodbc y mdbtools no disponibles

**Solución 1 - Instalar mdbtools (solo .mdb):**
```bash
sudo apt-get install mdbtools

# Listar tablas
mdb-tables -1 archivo.accdb

# Exportar tabla a CSV
mdb-export archivo.accdb NombreTabla > tabla.csv

# Importar CSV
python3 script/importar_partes_access.py tabla.csv csv
```

**Solución 2 - Exportar desde Windows:**
1. Abrir Access en Windows
2. Exportar tablas necesarias a CSV
3. Transferir CSVs a Linux
4. Importar usando el script

**Solución 3 - Instalar pyodbc + drivers (avanzado):**
```bash
# Instalar pyodbc
pip install pyodbc

# Instalar drivers ODBC de Microsoft
# (Ver documentación de Microsoft)
```

### Backup muy grande / sin espacio

**Solución:**
```bash
# Comprimir backup
gzip backup/backup_completo_pruebas.sql

# Verificar espacio disponible
df -h

# Limpiar backups antiguos si es necesario
```

---

## Restaurar desde Backup

Si necesitas restaurar la base de datos a un estado anterior:

```bash
# Restaurar backup
mysql -h localhost -P 3307 -u root -p proyecto_tipo < backup/backup_nopres_nopartes.sql

# O con nombre de archivo
mysql -h localhost -P 3307 -u root -p proyecto_tipo < backup/backup_con_presupuesto.sql
```

**ADVERTENCIA:** Esto sobrescribirá todos los datos actuales.

---

## Próximos Pasos

Una vez completada la FASE 1:

- ✓ FASE 1: Preparación de datos ← **ESTÁS AQUÍ**
- ⏳ FASE 2: Limpieza del proyecto (~45 archivos obsoletos)
- ⏳ FASE 3: Desarrollo de manuales (3-4 días)
- ⏳ FASE 4: Empaquetado (crear instalador)
- ⏳ FASE 5: Datos definitivos (Access actualizado del cliente)
- ⏳ FASE 6: Instalación Synology (servidor + clientes)

**Tiempo total estimado:** 9-13 días laborables + soporte

---

## Checklist de Completitud

Antes de pasar a FASE 2, verifica:

- [ ] MySQL corriendo y accesible
- [ ] `backup_nopres_nopartes.sql` creado
- [ ] Presupuesto cargado correctamente
- [ ] `backup_con_presupuesto.sql` creado
- [ ] Partes importados desde Access
- [ ] `backup_completo_pruebas.sql` creado
- [ ] Todos los informes probados
- [ ] Informes comparados con los del cliente
- [ ] Documentadas las diferencias (si las hay)
- [ ] No hay errores en logs

---

## Contacto y Soporte

Si encuentras problemas o necesitas ayuda con la FASE 1, documenta:

1. Paso donde falló
2. Mensaje de error completo
3. Salida del comando
4. Configuración del sistema

---

**Última actualización:** 2025-11-10
**Versión del documento:** 1.0
