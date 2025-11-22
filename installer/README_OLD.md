# HydroFlow Manager v2.0 - Sistema de Instalación

Este directorio contiene el sistema de instalación gráfico de HydroFlow Manager v2.0, diseñado para usuarios sin conocimientos técnicos.

## 📋 Contenido

### `setup_wizard.py`
Wizard de instalación gráfico (GUI) con interfaz Tkinter.

**Características:**
- Interfaz gráfica paso a paso
- Verifica que MySQL esté corriendo
- Configura la conexión a MySQL
- Crea los esquemas de base de datos
- Importa datos iniciales
- Instala dependencias de Python
- Genera archivo `.env` automáticamente

### `build_installer.ps1`
Script PowerShell para compilar el wizard en un ejecutable standalone.

**Uso:**
```powershell
.\installer\build_installer.ps1
```

**Resultado:**
- `dist/HydroFlowManager_Setup.exe` - Instalador ejecutable

## 🎯 Cómo Funciona el Instalador

### Paso 1: Bienvenida
- Muestra información sobre lo que se va a instalar
- Lista los requisitos previos

### Paso 2: Verificación de MySQL
- Verifica que MySQL/MariaDB esté instalado
- Comprueba que el servicio MySQL esté corriendo
- **Busca en ubicaciones comunes:**
  - `C:\Program Files\MySQL\MySQL Server 8.0\`
  - `C:\xampp\mysql\`
  - `C:\wamp64\bin\mysql\`

> **IMPORTANTE:** MySQL/MariaDB debe estar instalado **antes** de ejecutar este instalador. El instalador NO instala MySQL, solo configura la conexión.

### Paso 3: Configuración de Base de Datos
- Solicita al usuario:
  - Host (por defecto: localhost)
  - Puerto (por defecto: 3306)
  - Usuario (por defecto: root)
  - Contraseña
  - Nombres de esquemas (opcionales)

### Paso 4: Probar Conexión
- Prueba la conexión a MySQL con las credenciales proporcionadas
- Muestra mensaje de éxito o error
- Muestra la versión de MySQL conectada

### Paso 5: Crear Esquemas
- Crea los siguientes esquemas en MySQL:
  - `manager` - Esquema maestro de proyectos
  - `proyecto_tipo` - Plantilla de proyecto tipo
  - `cert_dev` - Esquema de trabajo/desarrollo

### Paso 6: Importar Datos
- Permite seleccionar archivos SQL de backup
- Auto-detecta archivos en `backups/produccion/`
- Importa:
  - `manager_estructura_y_datos.sql`
  - `proyecto_tipo_completo.sql`

### Paso 7: Instalar Dependencias
- Instala las dependencias de Python desde `requirements.txt`
- Muestra progreso en tiempo real
- Usa `pip install -r requirements.txt`

### Paso 8: Finalización
- Genera el archivo `.env` con la configuración
- Muestra resumen de instalación
- Proporciona instrucciones para ejecutar la aplicación

## 🚀 Compilar el Instalador

### Requisitos Previos

1. **Python 3.8+** instalado
2. **PyInstaller** instalado:
   ```bash
   pip install pyinstaller
   ```

### Compilación

```powershell
# Desde el directorio raíz del proyecto
.\installer\build_installer.ps1
```

El script:
1. Verifica que PyInstaller esté instalado
2. Limpia builds anteriores
3. Compila `setup_wizard.py` en un ejecutable
4. Incluye archivos necesarios:
   - `.env.example`
   - `INSTALACION.md`
   - Backups SQL en `backups/`
5. Genera `dist/HydroFlowManager_Setup.exe`

### Resultado

```
dist/
└── HydroFlowManager_Setup.exe   (~15-20 MB)
```

Este ejecutable es **standalone** y puede distribuirse a los usuarios finales.

## 📦 Distribución a Usuarios

### Opción 1: Instalador Standalone

Distribuir solo el ejecutable:
```
HydroFlowManager_Setup.exe
```

El instalador:
- Incluye el wizard de instalación
- Incluye plantillas de configuración
- **PERO:** No incluye backups SQL (el usuario debe proporcionarlos)

### Opción 2: Paquete Completo (Recomendado)

Crear un ZIP con:
```
HydroFlowManager_v2.0/
├── HydroFlowManager_Setup.exe
├── backups/
│   └── produccion/
│       └── <timestamp>/
│           ├── manager_estructura_y_datos.sql
│           └── proyecto_tipo_completo.sql
├── INSTALACION.md
└── README.txt
```

**Ventajas:**
- Usuario tiene todo lo necesario
- Backups SQL incluidos
- Documentación incluida

### Crear el Paquete Completo

```powershell
# Crear estructura
mkdir HydroFlowManager_v2.0
copy dist\HydroFlowManager_Setup.exe HydroFlowManager_v2.0\
copy -Recurse backups\produccion HydroFlowManager_v2.0\backups\produccion
copy INSTALACION.md HydroFlowManager_v2.0\

# Crear README para el usuario
@"
HydroFlow Manager v2.0 - Paquete de Instalación

REQUISITOS PREVIOS:
1. MySQL/MariaDB instalado y corriendo
2. Credenciales de MySQL (usuario y contraseña con permisos)

INSTALACIÓN:
1. Ejecute HydroFlowManager_Setup.exe
2. Siga las instrucciones del asistente paso a paso
3. El instalador configurará todo automáticamente

IMPORTANTE:
- El instalador NO instala MySQL. MySQL debe estar instalado previamente.
- Asegúrese de tener las credenciales de MySQL disponibles.
- El proceso toma aproximadamente 5-10 minutos.

Para más información, consulte INSTALACION.md
"@ | Out-File HydroFlowManager_v2.0\README.txt -Encoding UTF8

# Comprimir
Compress-Archive -Path HydroFlowManager_v2.0 -DestinationPath HydroFlowManager_v2.0_Setup.zip
```

## 🔧 Desarrollo y Testing

### Ejecutar el Wizard Sin Compilar

```bash
python installer/setup_wizard.py
```

Útil para desarrollo y testing.

### Modificar el Wizard

El archivo `setup_wizard.py` está organizado en métodos por paso:
- `step_welcome()` - Paso 1
- `step_verify_mysql()` - Paso 2
- `step_configure_database()` - Paso 3
- `step_test_connection()` - Paso 4
- `step_create_schemas()` - Paso 5
- `step_import_data()` - Paso 6
- `step_install_dependencies()` - Paso 7
- `step_finish()` - Paso 8

Para agregar un nuevo paso:
1. Crear método `step_mi_paso()`
2. Agregarlo a la lista en `show_step()`
3. Recompilar el instalador

### Testing del Instalador

1. **Test en entorno limpio:**
   - Usar máquina virtual con MySQL instalado
   - Probar instalación desde cero

2. **Test de errores:**
   - Probar con MySQL detenido
   - Probar con credenciales incorrectas
   - Probar sin permisos suficientes

3. **Test de UI:**
   - Verificar que todos los botones funcionan
   - Verificar que la navegación entre pasos es correcta
   - Verificar que los logs se muestran correctamente

## 📝 Configuración Generada

### Archivo .env

El instalador genera automáticamente el archivo `.env`:

```bash
# HydroFlow Manager v2.0 - Configuración
# Generado automáticamente por el instalador

# Servidor MySQL
DB_HOST=localhost
DB_PORT=3306

# Credenciales (MANTENER SEGURO)
DB_USER=root
DB_PASSWORD=<contraseña_ingresada>

# Esquemas
DB_MANAGER_SCHEMA=manager
DB_EXAMPLE_SCHEMA=proyecto_tipo
DB_SCHEMA=cert_dev

# Rendimiento
DB_USE_POOLING=true
```

## 🐛 Troubleshooting

### Error: "MySQL no encontrado"

**Causa:** MySQL no está en el PATH o no está instalado

**Solución:**
1. Instalar MySQL/MariaDB
2. O agregar MySQL al PATH:
   ```
   C:\Program Files\MySQL\MySQL Server 8.0\bin
   ```
3. Reiniciar el instalador

### Error: "No se pudo conectar a MySQL"

**Causa:** Credenciales incorrectas o servicio no corriendo

**Solución:**
1. Verificar que MySQL esté corriendo (Servicios de Windows)
2. Verificar usuario y contraseña
3. Verificar puerto (3306 por defecto, puede ser 3307)

### Error: "Error al crear esquemas"

**Causa:** Usuario sin permisos suficientes

**Solución:**
1. Usar usuario `root` con permisos completos
2. O otorgar permisos:
   ```sql
   GRANT ALL PRIVILEGES ON *.* TO 'usuario'@'localhost';
   FLUSH PRIVILEGES;
   ```

### Error: "Error al importar datos"

**Causa:** Archivos SQL no encontrados o corruptos

**Solución:**
1. Verificar que los archivos SQL existan en `backups/produccion/`
2. Regenerar backups con `preparar_bd_produccion.ps1`
3. Seleccionar archivos manualmente en el paso 6

### El instalador se congela

**Causa:** Instalación de dependencias Python tarda mucho

**Solución:**
1. Esperar (puede tardar 5-10 minutos)
2. Verificar conexión a Internet
3. Si persiste, instalar dependencias manualmente:
   ```bash
   pip install -r requirements.txt
   ```

## 📄 Archivos Generados Durante Instalación

El instalador crea/modifica:
- `.env` - Configuración de base de datos
- Esquemas en MySQL (manager, proyecto_tipo, cert_dev)
- Datos importados desde SQL
- Dependencias de Python instaladas

## 🔒 Seguridad

### Credenciales

- Las credenciales se solicitan durante la instalación
- Se guardan en `.env` (archivo local, no se sube a Git)
- **ADVERTENCIA:** `.env` contiene credenciales en texto plano
- **Recomendación:** Proteger el archivo `.env` con permisos adecuados

### Archivos SQL

- Los backups SQL contienen estructura y datos
- Verificar que no contengan datos sensibles antes de distribuir
- Usar `preparar_bd_produccion.ps1` para generar backups limpios

## 📞 Soporte

Para problemas con el instalador:
1. Consultar este README
2. Consultar `INSTALACION.md` en el directorio raíz
3. Revisar los logs del instalador

## 📚 Documentación Relacionada

- `INSTALACION.md` - Guía de instalación manual
- `docs/COMPILACION_Y_DISTRIBUCION.md` - Guía de compilación
- `dev_tools/preparacion/README.md` - Preparación de base de datos
- `docs/CHANGELOG_v2.0.md` - Changelog completo de v2.0

## 📄 Licencia

Este instalador es parte de HydroFlow Manager v2.0 y está sujeto a la misma licencia.
