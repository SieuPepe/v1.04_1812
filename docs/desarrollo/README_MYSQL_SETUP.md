# Configuración de MySQL para HydroFlow Manager

Este documento explica cómo configurar la conexión a MySQL para ejecutar los scripts de preparación de datos.

## Problema Actual

El script `fase1_preparacion_datos.py` no puede conectarse a MySQL porque:
- El servidor MySQL no está ejecutándose, o
- La configuración de conexión es incorrecta

## Diagnóstico Rápido

Ejecute el script de diagnóstico para identificar el problema:

```bash
python script/check_mysql.py
```

**Modo interactivo:** Si no tiene configuradas las credenciales en variables de entorno, el script le solicitará el usuario y la contraseña de forma segura por consola.

Este script verificará:
1. Si MySQL está ejecutándose
2. Si puede conectarse con las credenciales configuradas
3. Si la base de datos existe

## Configuración por Defecto

Los scripts usan la siguiente configuración por defecto:

```
Host:        localhost
Puerto:      3307
Usuario:     root
Contraseña:  root
Base de datos: proyecto_tipo
```

## Opciones de Configuración

### Opción 1: Modo Interactivo (Más Simple)

Si no configura variables de entorno, los scripts le solicitarán las credenciales por consola:

```bash
python script/check_mysql.py
```

El script le preguntará:
- Usuario de MySQL (por defecto: root)
- Contraseña (se oculta al escribir)

**Ventajas:**
- No requiere configuración previa
- La contraseña no queda guardada en variables de entorno
- Ideal para uso ocasional

### Opción 2: Variables de Entorno (Recomendado para uso frecuente)

Configure las siguientes variables de entorno antes de ejecutar los scripts:

**Windows (PowerShell):**
```powershell
$env:DB_HOST = "localhost"
$env:DB_PORT = "3307"
$env:DB_USER = "root"
$env:DB_PASSWORD = "root"
```

**Windows (CMD):**
```cmd
set DB_HOST=localhost
set DB_PORT=3307
set DB_USER=root
set DB_PASSWORD=root
```

**Linux/Mac:**
```bash
export DB_HOST=localhost
export DB_PORT=3307
export DB_USER=root
export DB_PASSWORD=root
```

### Opción 3: Archivo .env

1. Copie el archivo `.env.example` a `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edite `.env` con sus valores:
   ```
   DB_HOST=localhost
   DB_PORT=3307
   DB_USER=root
   DB_PASSWORD=root
   ```

**Nota:** El archivo `.env` está en `.gitignore` y no se subirá al repositorio.

## Pasos para Iniciar MySQL

### Si usa XAMPP:
1. Abra el XAMPP Control Panel
2. Haga clic en "Start" junto a MySQL
3. Verifique que el estado sea "Running"

### Si usa MySQL standalone:
1. Abra "Services" (services.msc en Windows)
2. Busque el servicio "MySQL" o "MySQL80"
3. Haga clic derecho → "Start"

### Si usa MySQL Workbench:
1. Abra MySQL Workbench
2. Conéctese a su instancia local
3. Verifique que puede ejecutar consultas

## Verificar el Puerto de MySQL

Si MySQL está en un puerto diferente (típicamente 3306):

1. Ejecute en MySQL:
   ```sql
   SHOW VARIABLES LIKE 'port';
   ```

2. Configure la variable `DB_PORT` con el puerto correcto

## Crear la Base de Datos

Si la base de datos `proyecto_tipo` no existe:

```sql
CREATE DATABASE proyecto_tipo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

O desde la línea de comandos:
```bash
mysql -u root -p -e "CREATE DATABASE proyecto_tipo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

## Probar la Conexión

Una vez configurado:

1. Ejecute el diagnóstico:
   ```bash
   python script/check_mysql.py
   ```

2. Si todo está bien, ejecute el script principal:
   ```bash
   python script/fase1_preparacion_datos.py
   ```

## Solución de Problemas Comunes

### Error: "Can't connect to MySQL server"
- **Causa:** MySQL no está ejecutándose
- **Solución:** Inicie el servidor MySQL (ver sección "Pasos para Iniciar MySQL")

### Error: "Access denied for user"
- **Causa:** Usuario o contraseña incorrectos
- **Solución:** Verifique las credenciales en las variables de entorno

### Error: "Unknown database 'proyecto_tipo'"
- **Causa:** La base de datos no existe
- **Solución:** Cree la base de datos (ver sección "Crear la Base de Datos")

### Error: "Can't connect to MySQL server on '127.0.0.1' (10061)"
- **Causa:** MySQL está escuchando en otro puerto o no está ejecutándose
- **Solución:**
  1. Verifique el puerto con `SHOW VARIABLES LIKE 'port';`
  2. Configure `DB_PORT` correctamente

## Contacto

Si los problemas persisten, proporcione la salida completa de:
```bash
python script/check_mysql.py
```
