# HydroFlow Manager - Instalación y Configuración

## 📋 Resumen de Cambios Implementados

Se han implementado las siguientes mejoras de seguridad y configuración:

### ✅ 1. Sistema de Configuración Persistente
- **NO** se guardan contraseñas en archivos
- Configuración de host, puerto y usuario persistente
- Soporte para conexiones locales y remotas
- Configuración por usuario (no global)

### ✅ 2. Eliminación de Credenciales Hardcodeadas
- Eliminadas TODAS las credenciales hardcodeadas del código
- Scripts actualizados para solicitar credenciales
- Soporte para variables de entorno

### ✅ 3. Script de Backup/Restore Fácil de Usar
- Backup completo de todos los esquemas
- Compresión automática
- Fácil restauración en otras máquinas

---

## 🚀 Instalación en Nueva Máquina

### Paso 1: Instalar MySQL/MariaDB

Asegúrese de tener MySQL o MariaDB instalado y en funcionamiento.

**Windows:**
- Descargar desde: https://dev.mysql.com/downloads/installer/
- Puerto por defecto: 3306 o 3307

**Linux:**
```bash
sudo apt-get install mysql-server
# o
sudo apt-get install mariadb-server
```

### Paso 2: Restaurar Base de Datos (si viene de otra instalación)

Si tiene un backup de otra instalación:

```bash
# Copiar el archivo .gz al directorio de backups
python tools/crear_backup_bd.py --restore backups/hydroflow_backup_YYYYMMDD_HHMMSS.sql.gz
```

El script solicitará:
- Usuario MySQL (con privilegios de administrador)
- Contraseña
- Confirmación (escriba 'SI' para continuar)

### Paso 3: Configurar Conexión

Ejecute el asistente de configuración:

```bash
python tools/configurar_instalacion.py
```

El asistente le preguntará:
1. **Tipo de conexión**: Local o Remota
2. **Host**: IP o nombre del servidor (si es remoto)
3. **Puerto**: Puerto de MySQL/MariaDB (default: 3307)
4. **Usuario**: Usuario de MySQL con privilegios
5. **¿Recordar usuario?**: Si desea guardar el usuario

**IMPORTANTE**: La contraseña NO se guarda y se solicitará cada vez que inicie la aplicación.

### Paso 4: Instalar Aplicación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Compilar ejecutable (opcional)
python build.py --all
```

---

## 🔧 Configuración

### Ubicación de Archivos de Configuración

**Windows:**
```
%APPDATA%\HydroFlow\connection.json
```

**Linux/Mac:**
```
~/.config/hydroflow/connection.json
```

### Configuración Manual

Puede editar manualmente usando:

```bash
# Ver configuración actual
python script/db_user_config.py --show

# Configurar interactivamente
python script/db_user_config.py --configure

# Cambiar un valor específico
python script/db_user_config.py --set host 192.168.1.100
python script/db_user_config.py --set port 3306

# Reiniciar configuración
python script/db_user_config.py --reset
```

### Variables de Entorno (Opcional)

También puede usar variables de entorno (tienen prioridad sobre el archivo de configuración):

**Windows:**
```cmd
set DB_HOST=localhost
set DB_PORT=3307
set DB_USER=root
set DB_PASSWORD=mipassword
```

**Linux/Mac:**
```bash
export DB_HOST=localhost
export DB_PORT=3307
export DB_USER=root
export DB_PASSWORD=mipassword
```

---

## 💾 Backup y Restauración

### Crear Backup

```bash
# Backup en directorio por defecto (./backups)
python tools/crear_backup_bd.py

# Backup en directorio personalizado
python tools/crear_backup_bd.py --output /ruta/personalizada
```

El script generará dos archivos:
- `hydroflow_backup_YYYYMMDD_HHMMSS.sql` - Backup completo
- `hydroflow_backup_YYYYMMDD_HHMMSS.sql.gz` - Backup comprimido

**Recomendación**: Use el archivo `.gz` para ahorrar espacio.

### Restaurar Backup

```bash
python tools/crear_backup_bd.py --restore backups/hydroflow_backup_YYYYMMDD_HHMMSS.sql.gz
```

⚠️ **ADVERTENCIA**: La restauración sobrescribirá los datos existentes.

---

## 🔒 Seguridad

### Buenas Prácticas Implementadas

✅ **Contraseñas NO se guardan en disco**
- Se solicitan en cada inicio de sesión
- No hay archivos de texto plano con credenciales

✅ **Configuración por usuario**
- Cada usuario de Windows/Linux tiene su propia configuración
- No afecta a otros usuarios del sistema

✅ **Variables de entorno soportadas**
- Permite configuración flexible en entornos corporativos
- Compatibilidad con sistemas de gestión de configuración

✅ **Sin credenciales hardcodeadas**
- Todo el código fuente está limpio
- Scripts de utilidad solicitan credenciales

### Recomendaciones Adicionales

1. **Usuario MySQL con privilegios mínimos**: Cree usuarios específicos para cada proyecto con solo los permisos necesarios.

2. **Backups regulares**: Configure backups automáticos periódicos.

3. **Conexión remota**: Si usa conexión remota, asegúrese de:
   - Usar SSL/TLS si es posible
   - Configurar firewall correctamente
   - Usar contraseñas fuertes

---

## 🆘 Solución de Problemas

### Error: "No se puede conectar a MySQL"

**Posibles causas:**
- MySQL/MariaDB no está en funcionamiento
- Host o puerto incorrectos
- Firewall bloqueando la conexión

**Solución:**
```bash
# Verificar que MySQL está corriendo
# Windows (en Services.msc buscar MySQL)
# Linux:
sudo systemctl status mysql

# Probar conexión manualmente
mysql -h localhost -P 3307 -u root -p

# Verificar configuración
python script/db_user_config.py --show
```

### Error: "Credenciales inválidas"

**Solución:**
1. Verificar usuario y contraseña:
   ```bash
   mysql -u root -p
   ```
2. Reconfigurar:
   ```bash
   python tools/configurar_instalacion.py
   ```

### Error: "No se encuentra archivo de configuración"

**Solución:**
```bash
# Ejecutar asistente de configuración
python tools/configurar_instalacion.py
```

### Restablecer Configuración

```bash
# Eliminar configuración actual y empezar de nuevo
python script/db_user_config.py --reset
python tools/configurar_instalacion.py
```

---

## 📝 Notas para el Instalador

### Creación del Instalador con Inno Setup

El instalador debe incluir:

1. **Post-instalación automática**: Ejecutar `configurar_instalacion.py` después de instalar archivos

2. **Acceso directo**: Crear acceso directo a HydroFlowManager.exe

3. **Documentación**: Incluir este README en el instalador

### Ejemplo de sección en installer.iss

```iss
[Run]
; Ejecutar configuración inicial después de instalar
Filename: "{app}\python.exe"; Parameters: "tools\configurar_instalacion.py"; \
    Description: "Configurar conexión a base de datos"; \
    Flags: postinstall nowait

[Icons]
; Crear acceso directo en escritorio
Name: "{commondesktop}\HydroFlow Manager"; \
    Filename: "{app}\HidroFlowManager.exe"

[Files]
; Incluir documentación
Source: "INSTALACION_Y_CONFIGURACION.md"; DestDir: "{app}"; Flags: isreadme
```

---

## 📞 Soporte

Para problemas o preguntas:

1. Verificar este documento primero
2. Revisar los logs de la aplicación
3. Contactar al administrador del sistema

---

## 📄 Licencia y Créditos

HydroFlow Manager - Sistema de Gestión de Proyectos Hidráulicos
© 2025 - Todos los derechos reservados
