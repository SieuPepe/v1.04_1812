# Guía de Instalación - HydroFlow Manager v2.0

## 📋 Requisitos Previos

- Python 3.8 o superior
- MySQL 8.0+ o MariaDB 10.5+
- pip (gestor de paquetes de Python)

## 🚀 Instalación Rápida

### 1. Clonar o Descargar el Proyecto

```bash
git clone <url-del-repositorio>
cd v1.04_1812
```

### 2. Crear Entorno Virtual (Recomendado)

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos

#### 4.1 Crear el archivo .env

Copia el archivo de ejemplo y edítalo:

**Windows:**
```powershell
copy .env.example .env
notepad .env
```

**Linux/Mac:**
```bash
cp .env.example .env
nano .env
```

#### 4.2 Configurar las variables en .env

**IMPORTANTE:** Edita el archivo `.env` con tus credenciales reales:

```bash
# Configuración del servidor
DB_HOST=localhost          # O la IP de tu servidor MySQL
DB_PORT=3307              # 3306 (estándar) o 3307 según tu instalación

# Credenciales (REQUERIDO - cambiar estos valores)
DB_USER=root              # Tu usuario de MySQL
DB_PASSWORD=tu_password   # Tu contraseña de MySQL

# Esquemas
DB_MANAGER_SCHEMA=manager
DB_EXAMPLE_SCHEMA=cert_dev
DB_SCHEMA=cert_dev

# Rendimiento
DB_USE_POOLING=true
```

**Notas:**
- El archivo `.env` NO se sube al repositorio (está en `.gitignore`)
- Cada instalación debe tener su propio `.env` con sus credenciales
- **NUNCA** compartas el archivo `.env` con contraseñas reales

### 5. Verificar Conexión a Base de Datos

Ejecuta el script de verificación:

```bash
python dev_tools/verificacion/test_conexion_directa.py
```

Si la conexión es exitosa, verás:
```
✅ Conexión establecida
📁 Esquema actual: cert_dev
📊 Total de registros: ...
```

### 6. Ejecutar la Aplicación

```bash
python main.py
```

## 🔧 Configuración Avanzada

### Configuración para Servidor Remoto

Si tu base de datos está en un servidor remoto:

```bash
DB_HOST=192.168.1.100    # IP del servidor
DB_PORT=3306
DB_USER=hydroflow_user
DB_PASSWORD=contraseña_segura
```

### Múltiples Entornos

Puedes crear archivos de configuración para diferentes entornos:

- `.env.local` - Desarrollo local
- `.env.staging` - Servidor de pruebas
- `.env.production` - Producción

Carga el que necesites:
```bash
# Linux/Mac
export $(cat .env.production | xargs)
python main.py

# Windows PowerShell
Get-Content .env.production | ForEach-Object {
    $name, $value = $_.split('=')
    Set-Content env:\$name $value
}
python main.py
```

## ❗ Solución de Problemas

### Error: "Can't connect to MySQL server on 'localhost:3306'"

**Causa:** El puerto configurado no es correcto.

**Solución:**
1. Verifica qué puerto usa tu MySQL:
   ```bash
   # Windows
   netstat -an | findstr 3306
   
   # Linux/Mac
   netstat -an | grep 3306
   ```

2. Actualiza `DB_PORT` en tu `.env`:
   ```bash
   DB_PORT=3307  # O el puerto que encontraste
   ```

### Error: "Access denied for user 'root'@'localhost'"

**Causa:** Credenciales incorrectas.

**Solución:**
1. Verifica tu usuario y contraseña de MySQL
2. Actualiza `DB_USER` y `DB_PASSWORD` en `.env`

### Error: "No module named 'dotenv'"

**Causa:** Falta la librería python-dotenv.

**Solución:**
```bash
pip install python-dotenv
```

### Error: "ERROR: Se requieren credenciales de base de datos"

**Causa:** El archivo `.env` no existe o no tiene DB_USER y DB_PASSWORD.

**Solución:**
1. Verifica que existe el archivo `.env` en el directorio raíz
2. Verifica que tiene las líneas DB_USER y DB_PASSWORD
3. Asegúrate de que no estén comentadas (sin # al inicio)

## 📚 Documentación Adicional

Para más información consulta:
- `docs/manual/Manual_Usuario_v2.0.md` - Manual de usuario completo
- `docs/manual/Manual_Tecnico_v2.0.md` - Documentación técnica
- `docs/manual/Guia_Instalacion_BD_v2.0.md` - Instalación detallada de MySQL

## 🆘 Soporte

Si encuentras problemas:
1. Revisa la sección de solución de problemas arriba
2. Consulta los manuales en la carpeta `docs/manual/`
3. Verifica que todas las dependencias estén instaladas: `pip list`

