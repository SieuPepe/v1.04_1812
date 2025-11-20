# HydroFlow Manager v2.0
## Guía de Instalación de Base de Datos

---

**Versión del Software:** 2.0
**Fecha de Publicación:** Noviembre 2025
**Empresa:** Artanda Ingeniería y Consultoría
**Audiencia:** Administradores de sistemas, Responsables de IT

---

## Tabla de Contenidos

1. [Introducción](#1-introducción)
2. [Requisitos Previos](#2-requisitos-previos)
3. [Instalación de MySQL/MariaDB](#3-instalación-de-mysqlmariadb)
4. [Configuración Inicial del Servidor](#4-configuración-inicial-del-servidor)
5. [Creación de Esquemas](#5-creación-de-esquemas)
6. [Importación de Datos Iniciales](#6-importación-de-datos-iniciales)
7. [Configuración de Usuarios y Permisos](#7-configuración-de-usuarios-y-permisos)
8. [Verificación de la Instalación](#8-verificación-de-la-instalación)
9. [Configuración de HydroFlow Manager](#9-configuración-de-hydroflow-manager)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Introducción

### 1.1 Propósito de esta Guía

Esta guía proporciona **instrucciones paso a paso** para instalar y configurar la base de datos MySQL/MariaDB necesaria para HydroFlow Manager v2.0.

### 1.2 Alcance

- ✅ Instalación de MySQL 8.0+ o MariaDB 10.5+
- ✅ Configuración básica de seguridad
- ✅ Creación de esquemas necesarios
- ✅ Importación de estructura y catálogos
- ✅ Configuración de usuarios y permisos
- ✅ Pruebas de conectividad

### 1.3 Tiempo Estimado

| Tarea | Tiempo |
|-------|--------|
| Instalación de MySQL | 15-30 min |
| Configuración inicial | 10-15 min |
| Creación de esquemas | 5-10 min |
| Importación de datos | 10-20 min |
| Configuración de usuarios | 5-10 min |
| **TOTAL** | **45-85 min** |

---

## 2. Requisitos Previos

### 2.1 Hardware

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| **CPU** | 2 cores | 4 cores |
| **RAM** | 4 GB | 8 GB o más |
| **Disco** | 20 GB libres | 50 GB libres (SSD) |

### 2.2 Software

- **Sistema Operativo:**
  - Windows 10/11 (64-bit)
  - Windows Server 2016+
  - Linux (Ubuntu 20.04+, Debian 10+, CentOS 8+)

- **Privilegios:**
  - Cuenta con permisos de administrador
  - Capacidad de instalar software
  - Acceso para configurar firewall

### 2.3 Conectividad

- **Puerto 3306** disponible (o alternativo si se desea cambiar)
- Acceso de red si se configura para conexiones remotas

### 2.4 Archivos Necesarios

Descargue los siguientes archivos del paquete de instalación:

```
HydroFlowManager_v2.0_DB/
├── instaladores/
│   ├── mysql-installer-community-8.0.xx.msi (Windows)
│   └── mariadb-10.5.xx.deb (Linux)
├── scripts/
│   ├── 01_crear_esquemas.sql
│   ├── 02_manager_estructura.sql
│   ├── 03_manager_catalogos.sql
│   ├── 04_proyecto_tipo_estructura.sql
│   └── 05_vistas_y_procedimientos.sql
└── README.txt
```

---

## 3. Instalación de MySQL/MariaDB

### 3.1 Instalación en Windows

#### 3.1.1 Descargar MySQL

1. Visite: https://dev.mysql.com/downloads/installer/
2. Descargue **MySQL Installer Community** (versión web o completa)
3. Guarde el archivo `.msi`

#### 3.1.2 Ejecutar el Instalador

1. **Doble click** en `mysql-installer-community-8.0.xx.msi`
2. Acepte los términos de licencia
3. Seleccione tipo de instalación:

```
┌─────────────────────────────────────────┐
│  Tipo de Instalación                    │
├─────────────────────────────────────────┤
│  ( ) Developer Default                  │
│  (•) Server only           ← SELECCIONE │
│  ( ) Full                               │
│  ( ) Custom                             │
└─────────────────────────────────────────┘
```

4. Click **"Next"** y luego **"Execute"**
5. Espere a que se descarguen e instalen los componentes

#### 3.1.3 Configuración del Servidor

**Tipo y Networking:**

```
┌─────────────────────────────────────────┐
│  Config Type: [Development Computer ▼]  │
│                                         │
│  Port: [3306____________]               │
│                                         │
│  ☑ Open Windows Firewall port          │
└─────────────────────────────────────────┘
```

**Autenticación:**

```
┌─────────────────────────────────────────┐
│  Authentication Method                   │
├─────────────────────────────────────────┤
│  (•) Use Strong Password Encryption     │
│      (RECOMMENDED)                      │
│                                         │
│  ( ) Use Legacy Authentication          │
└─────────────────────────────────────────┘
```

Seleccione **"Use Strong Password Encryption"**

**Contraseña de Root:**

```
┌─────────────────────────────────────────┐
│  MySQL Root Password                     │
├─────────────────────────────────────────┤
│  Password: [********************]       │
│  Confirm:  [********************]       │
│                                         │
│  ⚠️  Guarde esta contraseña en lugar    │
│     seguro - la necesitará después      │
└─────────────────────────────────────────┘
```

⚠️ **IMPORTANTE:** Use una contraseña segura y guárdela en un lugar seguro.

**Servicio de Windows:**

```
┌─────────────────────────────────────────┐
│  Windows Service                         │
├─────────────────────────────────────────┤
│  ☑ Configure MySQL Server as Windows    │
│    Service                              │
│                                         │
│  Service Name: [MySQL80______]          │
│                                         │
│  ☑ Start the MySQL Server at System    │
│    Startup                              │
└─────────────────────────────────────────┘
```

Mantenga ambas opciones marcadas.

5. Click **"Next"** → **"Execute"** → **"Finish"**

#### 3.1.4 Verificar Instalación

Abra **PowerShell** como administrador:

```powershell
# Verificar que el servicio está ejecutándose
Get-Service MySQL80

# Debe mostrar:
# Status: Running

# Conectar a MySQL
mysql -u root -p
# Introduzca la contraseña de root

# Si conecta correctamente, verá:
# mysql>
```

---

### 3.2 Instalación en Linux (Ubuntu/Debian)

#### 3.2.1 Actualizar Repositorios

```bash
sudo apt-get update
```

#### 3.2.2 Instalar MySQL Server

```bash
sudo apt-get install mysql-server
```

Durante la instalación:
- En Ubuntu 20.04+, puede que NO pida contraseña de root
- Se configurará más adelante

#### 3.2.3 Verificar Servicio

```bash
# Verificar estado
sudo systemctl status mysql

# Debe mostrar: Active (running)

# Iniciar (si no está ejecutándose)
sudo systemctl start mysql

# Habilitar inicio automático
sudo systemctl enable mysql
```

#### 3.2.4 Configuración de Seguridad

```bash
sudo mysql_secure_installation
```

**Responda a las preguntas:**

```
1. VALIDATE PASSWORD COMPONENT
   ¿Instalar componente de validación de contraseñas?
   → y (sí)

2. Password Validation Policy
   Level (0=LOW, 1=MEDIUM, 2=STRONG)
   → 1 (MEDIUM)

3. New password for root
   → Introduzca contraseña segura

4. Remove anonymous users?
   → y (sí)

5. Disallow root login remotely?
   → y (sí) [Solo para servidor local]
   → n (no) [Si necesita acceso remoto]

6. Remove test database?
   → y (sí)

7. Reload privilege tables now?
   → y (sí)
```

#### 3.2.5 Configurar Contraseña de Root (Ubuntu 20.04+)

Si MySQL no pidió contraseña durante la instalación:

```bash
# Conectar sin contraseña
sudo mysql

# En el prompt de MySQL:
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'tu_contraseña_segura';
FLUSH PRIVILEGES;
EXIT;

# Ahora puede conectar con:
mysql -u root -p
```

---

### 3.3 Instalación en Linux (CentOS/RHEL)

```bash
# Descargar repositorio de MySQL
wget https://dev.mysql.com/get/mysql80-community-release-el8-1.noarch.rpm

# Instalar repositorio
sudo rpm -ivh mysql80-community-release-el8-1.noarch.rpm

# Instalar MySQL Server
sudo yum install mysql-server

# Iniciar servicio
sudo systemctl start mysqld

# Obtener contraseña temporal de root
sudo grep 'temporary password' /var/log/mysqld.log

# Conectar con contraseña temporal
mysql -u root -p

# Cambiar contraseña
ALTER USER 'root'@'localhost' IDENTIFIED BY 'Nueva_Contraseña_123!';

# Configurar inicio automático
sudo systemctl enable mysqld
```

---

## 4. Configuración Inicial del Servidor

### 4.1 Conectar a MySQL

```bash
# Windows (PowerShell o CMD)
mysql -u root -p

# Linux
mysql -u root -p
```

### 4.2 Configuración de Parámetros

```sql
-- Conectado como root, ejecutar:

-- Mostrar configuración actual
SHOW VARIABLES LIKE 'max_connections';
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';

-- Configurar conexiones máximas (si es necesario)
SET GLOBAL max_connections = 200;

-- Configurar buffer pool de InnoDB
-- Recomendación: 70% de RAM disponible
-- Para 8GB RAM: 5GB
SET GLOBAL innodb_buffer_pool_size = 5368709120;

-- Verificar zona horaria
SELECT @@global.time_zone, @@session.time_zone;

-- Establecer zona horaria (si es necesario)
SET GLOBAL time_zone = '+01:00';  -- CET (Madrid)
```

### 4.3 Configuración Permanente

**Windows:**
Editar: `C:\ProgramData\MySQL\MySQL Server 8.0\my.ini`

**Linux:**
Editar: `/etc/mysql/mysql.conf.d/mysqld.cnf`

```ini
[mysqld]
# Configuración básica
port = 3306
bind-address = 0.0.0.0  # Permitir conexiones remotas
max_connections = 200

# InnoDB (motor de almacenamiento)
innodb_buffer_pool_size = 5G
innodb_log_file_size = 512M

# Character set
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

# Logging (para debugging)
log_error = /var/log/mysql/error.log
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 2

# Seguridad
skip-name-resolve
local-infile = 0
```

**Reiniciar MySQL:**

```bash
# Windows
net stop MySQL80
net start MySQL80

# Linux
sudo systemctl restart mysql
```

---

## 5. Creación de Esquemas

### 5.1 Esquemas Necesarios

HydroFlow Manager requiere **3 tipos de esquemas**:

1. **manager** - Esquema maestro (usuarios, catálogos)
2. **proyecto_tipo** - Plantilla vacía para nuevos proyectos
3. **Esquemas de proyectos** - Uno por cada proyecto (ej: PR001, CERT_DEV)

### 5.2 Crear Esquemas Manualmente

```sql
-- Conectar a MySQL
mysql -u root -p

-- Crear esquema manager
CREATE DATABASE IF NOT EXISTS manager
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Crear esquema proyecto_tipo
CREATE DATABASE IF NOT EXISTS proyecto_tipo
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Crear esquema de ejemplo (cert_dev)
CREATE DATABASE IF NOT EXISTS cert_dev
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Verificar creación
SHOW DATABASES;
```

### 5.3 Crear Esquemas desde Script

```bash
# Usar el script proporcionado
mysql -u root -p < scripts/01_crear_esquemas.sql
```

**Contenido de 01_crear_esquemas.sql:**

```sql
-- Crear esquemas si no existen
CREATE DATABASE IF NOT EXISTS manager
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE DATABASE IF NOT EXISTS proyecto_tipo
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE DATABASE IF NOT EXISTS cert_dev
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Mostrar esquemas creados
SHOW DATABASES LIKE '%manager%';
SHOW DATABASES LIKE '%proyecto%';
SHOW DATABASES LIKE '%cert%';
```

---

## 6. Importación de Datos Iniciales

### 6.1 Orden de Importación

⚠️ **IMPORTANTE:** Importar en este orden exacto:

```
1. manager - Estructura (tablas vacías)
2. manager - Catálogos (datos de referencia)
3. proyecto_tipo - Estructura (79 tablas vacías)
4. cert_dev - Copiar estructura desde proyecto_tipo
5. Vistas y procedimientos
```

### 6.2 Importar Estructura de Manager

```bash
# Importar estructura
mysql -u root -p manager < scripts/02_manager_estructura.sql
```

**Verificar:**

```sql
USE manager;
SHOW TABLES;

-- Debe mostrar aproximadamente:
-- tbl_usuarios
-- tbl_proyectos
-- tbl_catalogo_hidraulica
-- tbl_familia
-- ...
-- (Total: ~40 tablas)
```

### 6.3 Importar Catálogos de Manager

```bash
# Importar catálogos con datos
mysql -u root -p manager < scripts/03_manager_catalogos.sql
```

**Verificar datos:**

```sql
USE manager;

-- Verificar catálogo hidráulico
SELECT COUNT(*) FROM tbl_catalogo_hidraulica;
-- Debe retornar >100 registros

-- Verificar municipios
SELECT COUNT(*) FROM list_municipios;
-- Debe retornar ~251 municipios
```

### 6.4 Importar Estructura de proyecto_tipo

```bash
# Importar estructura (SOLO tablas vacías)
mysql -u root -p proyecto_tipo < scripts/04_proyecto_tipo_estructura.sql
```

⚠️ **CRÍTICO:** `proyecto_tipo` debe estar **completamente vacío** (sin datos).

**Verificar:**

```sql
USE proyecto_tipo;

-- Ver todas las tablas
SHOW TABLES;
-- Debe mostrar 79 tablas

-- Verificar que NO hay datos
SELECT TABLE_NAME, TABLE_ROWS
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'proyecto_tipo'
  AND TABLE_ROWS > 0;

-- NO debe retornar ninguna fila
```

### 6.5 Crear Esquema cert_dev

```bash
# Copiar estructura desde proyecto_tipo
mysql -u root -p cert_dev < scripts/04_proyecto_tipo_estructura.sql
```

**Datos de ejemplo (opcional):**

```bash
# Si desea datos de prueba
mysql -u root -p cert_dev < scripts/06_cert_dev_datos_prueba.sql
```

### 6.6 Crear Vistas y Procedimientos

```bash
# Crear vistas en todos los esquemas
mysql -u root -p < scripts/05_vistas_y_procedimientos.sql
```

**Verificar vistas:**

```sql
-- Ver vistas en cert_dev
USE cert_dev;
SHOW FULL TABLES WHERE TABLE_TYPE = 'VIEW';

-- Debe mostrar:
-- vw_presupuesto
-- vw_certificaciones
-- vw_partes_resumen
-- ...
```

---

## 7. Configuración de Usuarios y Permisos

### 7.1 Usuario de Aplicación

⚠️ **NO usar root en producción**

Crear usuario específico para HydroFlow Manager:

```sql
-- Crear usuario para aplicación
CREATE USER 'hydroflow_app'@'localhost'
IDENTIFIED BY 'Contraseña_Segura_123!';

-- Para permitir conexiones remotas:
CREATE USER 'hydroflow_app'@'%'
IDENTIFIED BY 'Contraseña_Segura_123!';
```

### 7.2 Otorgar Permisos

```sql
-- Permisos en esquema manager
GRANT SELECT, INSERT, UPDATE, DELETE
ON manager.*
TO 'hydroflow_app'@'localhost';

-- Permisos en proyecto_tipo (solo lectura)
GRANT SELECT
ON proyecto_tipo.*
TO 'hydroflow_app'@'localhost';

-- Permisos en cert_dev
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX
ON cert_dev.*
TO 'hydroflow_app'@'localhost';

-- Permisos para crear nuevos proyectos
GRANT CREATE, DROP
ON `PR%`.*
TO 'hydroflow_app'@'localhost';

GRANT CREATE, DROP
ON `CERT%`.*
TO 'hydroflow_app'@'localhost';

-- Aplicar cambios
FLUSH PRIVILEGES;
```

### 7.3 Usuario Administrador (opcional)

Para gestión de la BD:

```sql
-- Usuario admin con más permisos
CREATE USER 'hydroflow_admin'@'localhost'
IDENTIFIED BY 'Admin_Password_456!';

-- Todos los permisos excepto GRANT
GRANT ALL PRIVILEGES
ON manager.*
TO 'hydroflow_admin'@'localhost';

GRANT ALL PRIVILEGES
ON proyecto_tipo.*
TO 'hydroflow_admin'@'localhost';

GRANT ALL PRIVILEGES
ON cert_dev.*
TO 'hydroflow_admin'@'localhost';

FLUSH PRIVILEGES;
```

### 7.4 Verificar Permisos

```sql
-- Ver permisos de un usuario
SHOW GRANTS FOR 'hydroflow_app'@'localhost';

-- Debe mostrar algo como:
-- GRANT SELECT, INSERT, UPDATE, DELETE ON `manager`.* TO 'hydroflow_app'@'localhost'
-- GRANT SELECT ON `proyecto_tipo`.* TO 'hydroflow_app'@'localhost'
-- ...
```

---

## 8. Verificación de la Instalación

### 8.1 Test de Conectividad

```bash
# Probar conexión con usuario de aplicación
mysql -u hydroflow_app -p

# Si conecta, la configuración es correcta
```

### 8.2 Verificar Esquemas y Datos

```sql
-- Ver todos los esquemas
SHOW DATABASES;

-- Debe mostrar al menos:
-- manager
-- proyecto_tipo
-- cert_dev

-- Verificar tablas en manager
USE manager;
SHOW TABLES;

-- Verificar datos en catálogo
SELECT COUNT(*) as num_elementos FROM tbl_catalogo_hidraulica;
SELECT COUNT(*) as num_municipios FROM list_municipios;

-- Verificar estructura en cert_dev
USE cert_dev;
SHOW TABLES;
SELECT COUNT(*) as num_tablas FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'cert_dev';
-- Debe ser 79
```

### 8.3 Test de Escritura

```sql
USE cert_dev;

-- Insertar un proyecto de prueba
INSERT INTO tbl_proyectos (codigo, nombre, provincia, activo)
VALUES ('TEST001', 'Proyecto de prueba', 'Gipuzkoa', 1);

-- Verificar inserción
SELECT * FROM tbl_proyectos WHERE codigo = 'TEST001';

-- Eliminar proyecto de prueba
DELETE FROM tbl_proyectos WHERE codigo = 'TEST001';
```

### 8.4 Checklist de Verificación

- [ ] MySQL/MariaDB instalado y ejecutándose
- [ ] Esquema `manager` creado con ~40 tablas
- [ ] Catálogos en `manager` con datos (>100 elementos)
- [ ] Esquema `proyecto_tipo` creado con 79 tablas vacías
- [ ] Esquema `cert_dev` creado con estructura completa
- [ ] Usuario `hydroflow_app` creado
- [ ] Permisos otorgados correctamente
- [ ] Test de conexión exitoso
- [ ] Test de escritura exitoso

---

## 9. Configuración de HydroFlow Manager

### 9.1 Crear Archivo .env

En el directorio de instalación de HydroFlow Manager, cree el archivo `.env`:

**Windows:** `C:\Program Files\HydroFlowManager\.env`
**Linux:** `/opt/hydroflow/.env`

```env
# Configuración de Base de Datos
DB_HOST=localhost
DB_PORT=3306
DB_MANAGER_SCHEMA=manager
DB_EXAMPLE_SCHEMA=cert_dev

# Usuario de aplicación (NO incluir contraseña aquí)
# DB_USER=hydroflow_app
# DB_PASSWORD= (la aplicación la solicitará)

# Connection pooling
DB_USE_POOLING=true

# Directorios
INFORMES_DIR=./informes_guardados
EXPORT_DIR=./exportados
BACKUP_DIR=./backups
```

### 9.2 Primera Ejecución

1. **Ejecutar HydroFlowManager.exe**

2. **Login inicial:**
   - Usuario: (el que creó el instalador o `admin`)
   - Contraseña: (proporcionada por instalador)

3. **Configuración de BD:**
   - Si aparece el asistente de configuración:
     - Host: `localhost`
     - Puerto: `3306`
     - Usuario: `hydroflow_app`
     - Contraseña: (la que configuró en MySQL)

4. **Verificar conexión:**
   - Si conecta correctamente, verá la lista de proyectos
   - Seleccione `cert_dev` para probar

### 9.3 Configuración de Conexión Remota

Si la BD está en otro servidor:

```env
# En .env
DB_HOST=192.168.1.100  # IP del servidor MySQL
DB_PORT=3306
```

**En el servidor MySQL:**

```sql
-- Permitir acceso desde IP específica
CREATE USER 'hydroflow_app'@'192.168.1.50'
IDENTIFIED BY 'contraseña';

GRANT SELECT, INSERT, UPDATE, DELETE
ON manager.*, cert_dev.*
TO 'hydroflow_app'@'192.168.1.50';

FLUSH PRIVILEGES;
```

**Firewall:**

```bash
# Linux - Abrir puerto 3306
sudo ufw allow from 192.168.1.50 to any port 3306

# Windows - Crear regla
netsh advfirewall firewall add rule name="MySQL Remote" dir=in action=allow protocol=TCP localport=3306 remoteip=192.168.1.50
```

---

## 10. Troubleshooting

### 10.1 Error: "Can't connect to MySQL server"

**Causa:** MySQL no está ejecutándose o puerto bloqueado

**Solución:**

```bash
# Windows
net start MySQL80

# Linux
sudo systemctl start mysql

# Verificar puerto
netstat -an | grep 3306
```

### 10.2 Error: "Access denied for user"

**Causa:** Usuario no existe o contraseña incorrecta

**Solución:**

```sql
-- Verificar usuario
SELECT User, Host FROM mysql.user WHERE User = 'hydroflow_app';

-- Recrear usuario
DROP USER IF EXISTS 'hydroflow_app'@'localhost';
CREATE USER 'hydroflow_app'@'localhost' IDENTIFIED BY 'nueva_contraseña';
GRANT ALL PRIVILEGES ON manager.*, cert_dev.* TO 'hydroflow_app'@'localhost';
FLUSH PRIVILEGES;
```

### 10.3 Error: "Unknown database 'manager'"

**Causa:** Esquema no creado

**Solución:**

```bash
mysql -u root -p < scripts/01_crear_esquemas.sql
```

### 10.4 Error: "Table doesn't exist"

**Causa:** Scripts de estructura no importados

**Solución:**

```bash
# Importar estructura completa
mysql -u root -p manager < scripts/02_manager_estructura.sql
mysql -u root -p cert_dev < scripts/04_proyecto_tipo_estructura.sql
```

### 10.5 Problemas de Rendimiento

**Síntoma:** Consultas muy lentas

**Solución:**

```sql
-- Aumentar buffer pool
SET GLOBAL innodb_buffer_pool_size = 5368709120;  -- 5GB

-- Crear índices faltantes
USE cert_dev;
CREATE INDEX idx_fecha ON tbl_partes(fecha_inicio);
CREATE INDEX idx_municipio ON tbl_partes(id_municipio);

-- Optimizar tablas
OPTIMIZE TABLE tbl_partes;
OPTIMIZE TABLE tbl_presupuesto;
```

### 10.6 Error: "Too many connections"

**Causa:** Límite de conexiones alcanzado

**Solución:**

```sql
-- Ver conexiones actuales
SHOW PROCESSLIST;

-- Aumentar límite
SET GLOBAL max_connections = 200;

-- Hacer permanente en my.cnf/my.ini
[mysqld]
max_connections = 200
```

---

## Anexo A: Scripts SQL Completos

### A.1 Script Completo de Creación

```sql
-- 01_crear_esquemas.sql

-- Crear esquemas principales
CREATE DATABASE IF NOT EXISTS manager
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE DATABASE IF NOT EXISTS proyecto_tipo
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE DATABASE IF NOT EXISTS cert_dev
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Verificar
SHOW DATABASES;
```

### A.2 Script de Usuario y Permisos

```sql
-- 07_crear_usuario_app.sql

-- Usuario de aplicación
CREATE USER IF NOT EXISTS 'hydroflow_app'@'localhost'
IDENTIFIED BY 'CAMBIAR_ESTA_CONTRASEÑA';

-- Permisos en manager
GRANT SELECT, INSERT, UPDATE, DELETE
ON manager.* TO 'hydroflow_app'@'localhost';

-- Permisos en proyecto_tipo (solo lectura)
GRANT SELECT
ON proyecto_tipo.* TO 'hydroflow_app'@'localhost';

-- Permisos en proyectos
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP
ON cert_dev.* TO 'hydroflow_app'@'localhost';

GRANT CREATE, DROP
ON `PR%`.* TO 'hydroflow_app'@'localhost';

FLUSH PRIVILEGES;

-- Verificar
SHOW GRANTS FOR 'hydroflow_app'@'localhost';
```

---

## Anexo B: Comandos Útiles de MySQL

```sql
-- Ver información del servidor
SELECT VERSION();
SELECT @@datadir;
SELECT @@port;

-- Ver tamaño de esquemas
SELECT
    TABLE_SCHEMA,
    ROUND(SUM(DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 2) AS 'Size (MB)'
FROM information_schema.TABLES
WHERE TABLE_SCHEMA IN ('manager', 'proyecto_tipo', 'cert_dev')
GROUP BY TABLE_SCHEMA;

-- Ver usuarios
SELECT User, Host FROM mysql.user;

-- Ver procesos activos
SHOW PROCESSLIST;

-- Ver variables de configuración
SHOW VARIABLES LIKE 'max_connections';
SHOW VARIABLES LIKE 'innodb%';

-- Ver estado del servidor
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Uptime';
```

---

**Fin de la Guía de Instalación de Base de Datos**

*Para soporte adicional, consulte el Manual Técnico o contacte con el departamento de IT.*

**¿Instalación completada con éxito?** Proceda con la instalación de HydroFlow Manager (ver Manual de Usuario).
