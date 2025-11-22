# HydroFlow Manager v2.0
## Manual de Usuario

---

**Versión del Software:** 2.0
**Fecha de Publicación:** Noviembre 2025
**Empresa:** Artanda Ingeniería y Consultoría

---

## Tabla de Contenidos

1. [Introducción](#1-introducción)
2. [Requisitos del Sistema](#2-requisitos-del-sistema)
3. [Instalación y Configuración](#3-instalación-y-configuración)
4. [Inicio de Sesión](#4-inicio-de-sesión)
5. [Interfaz Principal](#5-interfaz-principal)
6. [Módulo de Proyectos](#6-módulo-de-proyectos)
7. [Módulo de Partes de Trabajo](#7-módulo-de-partes-de-trabajo)
8. [Módulo de Presupuestos](#8-módulo-de-presupuestos)
9. [Módulo de Certificaciones](#9-módulo-de-certificaciones)
10. [Módulo de Informes](#10-módulo-de-informes)
11. [Gestión de Catálogos](#11-gestión-de-catálogos)
12. [Configuración Avanzada](#12-configuración-avanzada)
13. [Resolución de Problemas](#13-resolución-de-problemas)
14. [Soporte Técnico](#14-soporte-técnico)

---

## 1. Introducción

### 1.1 ¿Qué es HydroFlow Manager?

**HydroFlow Manager** es un sistema integral de gestión de proyectos hidráulicos diseñado específicamente para empresas de ingeniería y construcción. La aplicación permite gestionar de forma eficiente todos los aspectos de proyectos de redes hidráulicas, desde la planificación hasta la certificación final.

### 1.2 Características Principales

- **Gestión de Proyectos Multi-esquema:** Trabaje con múltiples proyectos simultáneamente
- **Generador de Partes de Trabajo:** Cree y gestione partes detallados con recursos asociados
- **Control de Presupuestos:** Gestione presupuestos por capítulos y partidas
- **Certificaciones:** Genere certificaciones de obra con cálculos automáticos
- **Sistema de Informes Avanzado:** Más de 15 tipos de informes configurables
- **Catálogos Personalizables:** Gestione catálogos de materiales hidráulicos y registros
- **Configuración Flexible:** Compatible con servidores MySQL locales o remotos
- **Exportación Multi-formato:** Exporte a PDF, Excel y Word

### 1.3 Novedades de la Versión 2.0

✨ **Configuración de Base de Datos Flexible**
- Soporte para servidores MySQL locales y remotos
- Configuración mediante archivo `.env` sin valores hardcodeados
- Puerto configurable (3306 estándar o personalizado)

✨ **Mejoras de Rendimiento**
- Sistema de connection pooling optimizado
- Carga más rápida de datos en tablas

✨ **Interfaz Mejorada**
- Treeview con mejor legibilidad y fuentes más grandes
- Iconos actualizados y más intuitivos

✨ **Sistema de Informes**
- Nuevas plantillas de informes
- Guardar y cargar configuraciones de informes
- Exportación mejorada a múltiples formatos

---

## 2. Requisitos del Sistema

### 2.1 Requisitos Mínimos

| Componente | Especificación Mínima |
|------------|----------------------|
| **Sistema Operativo** | Windows 10 (64-bit) o superior |
| **Procesador** | Intel Core i3 o equivalente |
| **Memoria RAM** | 4 GB |
| **Disco Duro** | 500 MB espacio libre |
| **Resolución de Pantalla** | 1366 x 768 píxeles |
| **Base de Datos** | MySQL 8.0+ o MariaDB 10.5+ |

### 2.2 Requisitos Recomendados

| Componente | Especificación Recomendada |
|------------|---------------------------|
| **Sistema Operativo** | Windows 11 (64-bit) |
| **Procesador** | Intel Core i5 o superior |
| **Memoria RAM** | 8 GB o más |
| **Disco Duro** | 1 GB espacio libre (SSD recomendado) |
| **Resolución de Pantalla** | 1920 x 1080 píxeles o superior |

### 2.3 Software Adicional Requerido

- **MySQL Server 8.0+** o **MariaDB 10.5+**
- **Microsoft Office** (opcional, para editar documentos exportados)
- **Adobe Acrobat Reader** (para visualizar PDFs generados)

---

## 3. Instalación y Configuración

### 3.1 Instalación del Software

1. **Ejecute el instalador** `HydroFlowManager_v2.0_Setup.exe`
2. Siga el asistente de instalación
3. Seleccione el directorio de instalación (por defecto: `C:\Program Files\HydroFlowManager`)
4. Aguarde a que finalice la instalación

### 3.2 Configuración de Base de Datos

#### 3.2.1 Configuración Inicial Automática

Al iniciar la aplicación por primera vez, se le pedirá configurar la conexión a la base de datos:

1. **Tipo de Servidor:**
   - **Servidor Local (localhost):** Si MySQL está en la misma máquina
   - **Servidor Remoto:** Si MySQL está en otra máquina o red

2. **Datos de Conexión:**
   - **Host:** `localhost` o IP del servidor (ej: `192.168.1.100`)
   - **Puerto:** `3306` (estándar) o puerto personalizado
   - **Usuario:** Usuario de MySQL con permisos adecuados
   - **Contraseña:** Contraseña del usuario

3. **Recordar Configuración:**
   - Marque esta opción para no tener que configurar en cada inicio

#### 3.2.2 Configuración Manual (Avanzado)

Para usuarios avanzados, puede editar directamente el archivo `.env`:

```env
# Configuración de Base de Datos
DB_HOST=localhost
DB_PORT=3306
DB_MANAGER_SCHEMA=manager
DB_EXAMPLE_SCHEMA=cert_dev

# Connection pooling
DB_USE_POOLING=true

# Directorios
INFORMES_DIR=./informes_guardados
EXPORT_DIR=./exportados
BACKUP_DIR=./backups
```

**⚠️ Importante:** No incluya credenciales en este archivo en entornos compartidos.

### 3.3 Verificación de la Instalación

Para verificar que la instalación fue exitosa:

1. Ejecute `HydroFlowManager.exe`
2. Debería aparecer la pantalla de inicio de sesión
3. Si aparece un error de conexión, verifique la configuración de MySQL

---

## 4. Inicio de Sesión

### 4.1 Pantalla de Login

![Pantalla de Login](./screenshots/01_login.png)

La pantalla de inicio presenta:
- **Logo de la empresa** en la parte superior
- **Campos de autenticación:**
  - Usuario
  - Contraseña
- **Botón "Login"** para acceder al sistema

### 4.2 Credenciales de Acceso

Las credenciales son proporcionadas por el administrador del sistema. Existen diferentes niveles de acceso:

| Tipo de Usuario | Permisos |
|-----------------|----------|
| **Administrador** | Acceso completo a todos los módulos |
| **Técnico** | Crear y modificar partes, presupuestos |
| **Consulta** | Solo visualización de datos |

### 4.3 Primer Acceso

En el primer acceso con credenciales de administrador:
1. Se le solicitará crear un usuario maestro
2. Configure la base de datos si no se hizo durante la instalación
3. Importe los catálogos iniciales (opcional)

---

## 5. Interfaz Principal

### 5.1 Descripción General

![Interfaz Principal](./screenshots/02_main_interface.png)

La interfaz principal se divide en:

1. **Barra Lateral de Navegación** (izquierda)
   - Logo de la empresa
   - Botones de navegación entre módulos
   - Botón "Añadir Parte" (verde)

2. **Área de Trabajo Principal** (centro-derecha)
   - Contenido dinámico según el módulo seleccionado
   - Tablas de datos
   - Formularios de entrada

3. **Barra de Estado** (inferior)
   - Proyecto activo
   - Usuario conectado
   - Mensajes del sistema

### 5.2 Módulos Principales

Los módulos disponibles en la barra lateral son:

| Icono | Módulo | Descripción |
|-------|--------|-------------|
| 📊 | **Resumen** | Vista general del proyecto |
| 🔧 | **Partes** | Gestión de partes de trabajo |
| 💰 | **Presupuesto** | Control de presupuestos |
| ✅ | **Certificaciones** | Gestión de certificaciones |
| 📄 | **Informes** | Generador de informes |
| ❓ | **Ayuda** | Ayuda y acerca de |

### 5.3 Navegación entre Módulos

Para cambiar de módulo:
1. Haga clic en el botón correspondiente en la barra lateral
2. El área principal actualizará su contenido
3. El botón activo se mostrará resaltado

---

## 6. Módulo de Proyectos

### 6.1 Selección de Proyecto

Al iniciar sesión, se le presentará la lista de proyectos disponibles:

![Selección de Proyecto](./screenshots/03_select_project.png)

**Campos mostrados:**
- Código del proyecto
- Nombre del proyecto
- Cliente
- Estado (Activo/Finalizado)

**Acciones disponibles:**
- **Abrir:** Cargar el proyecto seleccionado
- **Nuevo:** Crear un nuevo proyecto
- **Editar:** Modificar datos del proyecto
- **Eliminar:** Borrar proyecto (solo administradores)

### 6.2 Crear Nuevo Proyecto

Para crear un proyecto nuevo:

1. Click en **"Nuevo Proyecto"**
2. Complete el formulario:

| Campo | Descripción | Obligatorio |
|-------|-------------|-------------|
| **Código** | Identificador único (ej: CERT_2024_001) | ✅ |
| **Nombre** | Nombre descriptivo del proyecto | ✅ |
| **Cliente** | Cliente o empresa contratante | ✅ |
| **Descripción** | Descripción detallada | ❌ |
| **Fecha Inicio** | Fecha de inicio del proyecto | ✅ |
| **Fecha Fin** | Fecha estimada de finalización | ❌ |
| **Presupuesto Total** | Valor total del proyecto | ❌ |

3. Click en **"Guardar"**

### 6.3 Datos Económicos del Proyecto

Cada proyecto tiene asociados parámetros económicos:

- **Gastos Generales (%):** Porcentaje sobre PEM
- **Beneficio Industrial (%):** Porcentaje sobre PEM
- **IVA (%):** Impuesto aplicable
- **Presupuesto Base de Licitación**

Estos valores se utilizan automáticamente en los cálculos de certificaciones.

---

## 7. Módulo de Partes de Trabajo

### 7.1 Vista General de Partes

![Módulo de Partes](./screenshots/04_parts_module.png)

El módulo de partes muestra una tabla con todos los partes creados:

**Columnas principales:**
- Código del parte
- Fecha
- Registro/Arqueta
- Municipio
- Estado (Pendiente/En Curso/Finalizado)
- Importe

**Barra de herramientas:**
- 🔍 **Buscar:** Filtrar partes
- ➕ **Nuevo Parte:** Crear parte
- ✏️ **Editar:** Modificar parte seleccionado
- 🗑️ **Eliminar:** Borrar parte
- 📄 **Exportar:** Generar documento del parte

### 7.2 Crear un Nuevo Parte

#### 7.2.1 Datos Generales

1. Click en **"➕ Añadir Parte"** (botón verde)
2. Se abrirá el formulario de nuevo parte:

![Formulario Nuevo Parte](./screenshots/05_new_part_form.png)

**Sección 1: Información General**

| Campo | Descripción |
|-------|-------------|
| **Código Parte** | Generado automáticamente (ej: P-2024-001) |
| **Fecha** | Fecha de realización del trabajo |
| **Red** | Red hidráulica asociada |
| **Municipio** | Municipio donde se realiza el trabajo |
| **Registro/Arqueta** | Código del registro o arqueta |

**Sección 2: Ubicación**

| Campo | Descripción |
|-------|-------------|
| **Dirección** | Calle y número |
| **Coordenadas X** | Coordenada Este (UTM) |
| **Coordenadas Y** | Coordenada Norte (UTM) |
| **Observaciones** | Notas adicionales |

#### 7.2.2 Añadir Recursos al Parte

Cada parte puede tener asociados:

**1. Mano de Obra**
- Operario
- Oficial
- Peón
- Horas trabajadas
- Precio/hora

**2. Maquinaria**
- Retroexcavadora
- Camión
- Compactadora
- Horas de uso
- Precio/hora

**3. Materiales**
- Elementos hidráulicos del catálogo
- Registros del catálogo
- Cantidad
- Precio unitario

Para añadir un recurso:
1. Click en la pestaña correspondiente (Mano de Obra / Maquinaria / Materiales)
2. Click en **"+ Añadir"**
3. Seleccione el elemento del catálogo
4. Introduzca cantidad/horas
5. El importe se calcula automáticamente

#### 7.2.3 Presupuesto del Parte

La pestaña **"Presupuesto"** permite asociar partidas presupuestarias:

1. Click en **"Añadir Partida"**
2. Busque la partida en el catálogo de presupuesto
3. Introduzca la cantidad certificada
4. El importe se calcula automáticamente

**Cálculo Automático:**
```
Importe Partida = Cantidad × Precio Unitario
Importe Total Parte = Σ(Importes de todas las partidas)
```

### 7.3 Editar un Parte Existente

1. Seleccione el parte en la tabla
2. Click en **"✏️ Editar"**
3. Modifique los campos necesarios
4. Click en **"Guardar Cambios"**

**Nota:** Los partes certificados tienen restricciones de edición.

### 7.4 Eliminar un Parte

1. Seleccione el parte en la tabla
2. Click en **"🗑️ Eliminar"**
3. Confirme la eliminación

⚠️ **Advertencia:** Esta acción no se puede deshacer. Los partes certificados no pueden eliminarse.

---

## 8. Módulo de Presupuestos

### 8.1 Vista de Presupuesto

![Módulo de Presupuesto](./screenshots/06_budget_module.png)

El módulo de presupuesto organiza las partidas en una estructura jerárquica:

**Estructura:**
```
Capítulo 1: Excavaciones
  ├── 1.1 Excavación manual
  ├── 1.2 Excavación mecánica
  └── 1.3 Relleno compactado
Capítulo 2: Instalaciones
  ├── 2.1 Tuberías
  └── 2.2 Registros
```

### 8.2 Añadir Capítulo

1. Click en **"+ Añadir Capítulo"**
2. Complete los datos:
   - Código (ej: CAP01)
   - Nombre del capítulo
   - Naturaleza (Obra, Seguridad, etc.)
3. Click en **"Guardar"**

### 8.3 Añadir Partida

1. Seleccione el capítulo padre
2. Click en **"+ Añadir Partida"**
3. Complete el formulario:

| Campo | Descripción |
|-------|-------------|
| **Código Partida** | Identificador único |
| **Naturaleza** | Obra/Seguridad/etc. |
| **Unidad** | m, m², m³, ud, etc. |
| **Resumen** | Descripción corta |
| **Descripción** | Descripción detallada |
| **Precio Unitario** | Coste por unidad |
| **Cantidad** | Cantidad presupuestada |

El **coste total** se calcula automáticamente: `Cantidad × Precio Unitario`

### 8.4 Importar Presupuesto desde Excel

Para importar un presupuesto completo:

1. Prepare un archivo Excel con las hojas:
   - `tbl_pres_naturaleza`
   - `tbl_pres_unidades`
   - `tbl_pres_capitulos`
   - `tbl_pres_precios`

2. En la aplicación: **Menú → Importar → Presupuesto**
3. Seleccione el archivo Excel
4. Verifique la previsualización
5. Click en **"Importar"**

### 8.5 Actualizar Precios

Para actualizar precios de partidas:

1. Seleccione la partida
2. Click en **"Actualizar Precio"**
3. Introduzca el nuevo precio
4. Confirme la actualización

⚠️ **Nota:** Los partes ya certificados mantendrán el precio anterior.

---

## 9. Módulo de Certificaciones

### 9.1 Crear Certificación

![Módulo de Certificaciones](./screenshots/07_cert_module.png)

Las certificaciones agrupan partes de trabajo para facturación:

1. Click en **"Nueva Certificación"**
2. Seleccione el período:
   - Fecha inicio
   - Fecha fin
3. Seleccione los partes a incluir
4. Click en **"Generar Certificación"**

### 9.2 Cálculo Automático

El sistema calcula automáticamente:

```
PEM (Presupuesto Ejecución Material) = Σ Importes de Partes
Gastos Generales = PEM × % GG
Beneficio Industrial = PEM × % BI
Base Imponible = PEM + GG + BI
IVA = Base Imponible × % IVA
TOTAL CERTIFICACIÓN = Base Imponible + IVA
```

### 9.3 Exportar Certificación

Formatos disponibles:
- **PDF:** Documento final para cliente
- **Excel:** Para análisis y edición
- **Word:** Para personalización

---

## 10. Módulo de Informes

### 10.1 Generador de Informes

![Módulo de Informes](./screenshots/08_reports_module.png)

El generador de informes permite crear reportes personalizados:

**Paso 1: Seleccionar Tipo de Informe**
- Presupuesto Detallado
- Presupuesto Resumen
- Certificación por Red
- Listado de Órdenes de Trabajo
- Recursos Utilizados
- Y más...

**Paso 2: Configurar Filtros**
- Rango de fechas
- Municipios
- Redes
- Estado de partes

**Paso 3: Seleccionar Campos**
- Marque los campos a incluir en el informe
- Ordene las columnas arrastrando

**Paso 4: Configurar Agrupación**
- Sin agrupación
- Por municipio
- Por red
- Por tipo de trabajo
- Agrupación personalizada

**Paso 5: Formato de Salida**
- PDF (recomendado)
- Excel
- Word

### 10.2 Guardar Configuración de Informe

Para reutilizar configuraciones:

1. Configure el informe como desee
2. Click en **"💾 Guardar Configuración"**
3. Asigne un nombre (ej: "Certificación Mensual Red A")
4. La configuración se guarda automáticamente

### 10.3 Cargar Configuración Guardada

1. Click en **"📁 Cargar Configuración"**
2. Seleccione de la lista de configuraciones guardadas
3. El informe se configura automáticamente

### 10.4 Tipos de Informes Disponibles

| Informe | Descripción | Uso Típico |
|---------|-------------|------------|
| **Presupuesto Detallado** | Listado completo de partidas | Presentación a cliente |
| **Presupuesto Resumen** | Resumen por capítulos | Análisis rápido |
| **Certificación Red** | Certificación por red hidráulica | Facturación mensual |
| **Órdenes de Trabajo** | Listado de todos los partes | Control interno |
| **Recursos Certificados** | Materiales y mano de obra | Análisis de costes |
| **Certificación Pendiente** | Trabajos sin certificar | Planificación |

---

## 11. Gestión de Catálogos

### 11.1 Catálogo de Elementos Hidráulicos

El catálogo contiene:
- Válvulas
- Conexiones
- Bridas
- Tuberías
- Accesorios

**Campos del catálogo:**
- Familia
- Tipo
- Marca
- Modelo
- Características técnicas (DN, PN, ángulo)
- Precio

### 11.2 Catálogo de Registros

Tipos de registros:
- Arquetas
- Registros de acera
- Cámaras
- Pozos

**Campos:**
- Tipo
- Proveedor
- Dimensiones (A × B × C)
- Precio

### 11.3 Añadir Elemento al Catálogo

1. **Menú → Catálogos → Elementos Hidráulicos**
2. Click en **"+ Añadir"**
3. Complete todos los campos técnicos
4. Click en **"Guardar"**

### 11.4 Importar Catálogo desde Excel

Para importaciones masivas:

1. Prepare archivo Excel con las hojas correspondientes
2. **Menú → Importar → Catálogo**
3. Seleccione el archivo
4. Verifique previsualización
5. Click en **"Importar"**

---

## 12. Configuración Avanzada

### 12.1 Configuración de Base de Datos

**Acceso:** Menú → Configuración → Base de Datos

#### 12.1.1 Cambiar Servidor

Para cambiar de servidor local a remoto o viceversa:

1. **Menú → Configuración → Base de Datos**
2. Click en **"Reconfigurar"**
3. Seleccione el tipo de conexión:
   - Servidor Local
   - Servidor Remoto
4. Introduzca los datos del nuevo servidor
5. Click en **"Probar Conexión"**
6. Si es exitosa, click en **"Guardar"**

#### 12.1.2 Connection Pooling

Para mejorar el rendimiento:

```env
DB_USE_POOLING=true
```

**Beneficios:**
- Conexiones más rápidas (~1ms vs ~50ms)
- Mejor rendimiento en operaciones múltiples
- Gestión eficiente de recursos

### 12.2 Configuración de Directorios

**Ubicación del archivo:** `.env` en directorio de instalación

```env
# Directorio para configuraciones de informes guardadas
INFORMES_DIR=./informes_guardados

# Directorio para documentos exportados
EXPORT_DIR=./exportados

# Directorio para backups
BACKUP_DIR=./backups
```

### 12.3 Backups Automáticos

Para activar backups automáticos:

```env
AUTO_BACKUP_ENABLED=true
BACKUP_FREQUENCY_HOURS=24
```

Los backups se guardarán en la carpeta especificada en `BACKUP_DIR`.

### 12.4 Niveles de Log

Para debugging o soporte técnico:

```env
LOG_LEVEL=INFO
```

Opciones:
- `DEBUG`: Información muy detallada
- `INFO`: Información general (recomendado)
- `WARNING`: Solo advertencias
- `ERROR`: Solo errores críticos

---

## 13. Resolución de Problemas

### 13.1 Problemas de Conexión a Base de Datos

**Síntoma:** "Error al conectar a la base de datos: 2003"

**Soluciones:**

1. **Verificar que MySQL está ejecutándose:**
   ```cmd
   net start MySQL
   ```

2. **Verificar el puerto:**
   - El puerto estándar es `3306`
   - Si usa otro puerto, verifique en `.env`:
     ```env
     DB_PORT=3307
     ```

3. **Verificar credenciales:**
   - Usuario y contraseña correctos
   - Usuario tiene permisos en la base de datos

4. **Verificar firewall:**
   - Permita conexiones al puerto MySQL
   - Para servidor remoto, abra el puerto en el firewall

**Comando de verificación:**
```cmd
mysql -h localhost -P 3306 -u usuario -p
```

### 13.2 Problema: Aplicación se Cierra Inesperadamente

**Causas comunes:**
1. Falta de memoria RAM
2. Archivo de configuración corrupto
3. Base de datos inaccesible

**Solución:**
1. Cierre otras aplicaciones
2. Elimine el archivo `.env` y reconfigure
3. Verifique logs en `logs/aplicacion.log`

### 13.3 Problema: Los Informes no se Generan

**Verificaciones:**
1. Hay datos para el período seleccionado
2. Tiene permisos de escritura en la carpeta `EXPORT_DIR`
3. No hay otro archivo abierto con el mismo nombre

**Solución:**
1. Verifique los filtros aplicados
2. Ejecute la aplicación como administrador
3. Cambie el directorio de exportación

### 13.4 Problema: Lentitud en la Aplicación

**Optimizaciones:**

1. **Activar connection pooling:**
   ```env
   DB_USE_POOLING=true
   ```

2. **Cerrar ventanas no utilizadas**

3. **Limpiar datos antiguos:**
   - Archive proyectos finalizados
   - Elimine partes de prueba

4. **Verificar recursos del sistema:**
   - RAM disponible
   - Espacio en disco
   - Conexión de red (si usa servidor remoto)

---

## 14. Soporte Técnico

### 14.1 Información de Contacto

**Artanda Ingeniería y Consultoría**

📧 **Email:** soporte@artanda.com
📞 **Teléfono:** +34 XXX XXX XXX
🌐 **Web:** www.artanda.com

**Horario de Soporte:**
- Lunes a Viernes: 9:00 - 18:00 (CET)
- Urgencias: Disponible 24/7 para clientes Premium

### 14.2 Antes de Contactar con Soporte

Tenga preparada la siguiente información:

1. **Versión del software:**
   - Menú → Ayuda → Acerca de
   - Versión: 2.0

2. **Descripción del problema:**
   - ¿Qué estaba haciendo cuando ocurrió?
   - ¿Es reproducible?
   - ¿Desde cuándo ocurre?

3. **Archivos de log:**
   - Ubicación: `logs/aplicacion.log`
   - Adjunte los últimos 100 líneas

4. **Capturas de pantalla:**
   - Del error si es visible
   - De la configuración relevante

### 14.3 Actualizaciones

Las actualizaciones se publican regularmente:

- **Actualizaciones Menores (2.0.x):** Correcciones de bugs
- **Actualizaciones Mayores (2.x):** Nuevas funcionalidades

Para verificar actualizaciones:
- **Menú → Ayuda → Buscar Actualizaciones**

### 14.4 Recursos Adicionales

📚 **Documentación:**
- Manual Técnico (para administradores)
- Manual de Informes (uso avanzado del generador)
- Guía de Instalación de Base de Datos

🎥 **Videotutoriales:**
- Canal de YouTube: youtube.com/artanda
- Curso completo de HydroFlow Manager

💬 **Comunidad:**
- Foro de usuarios: forum.artanda.com
- Grupo de Telegram: @hydroflowmanager

### 14.5 Acerca de HydroFlow Manager v2.0

![Acerca de](./screenshots/09_about.png)

**HydroFlow Manager v2.0**
Desarrollado por Artanda Ingeniería y Consultoría
© 2024-2025 Todos los derechos reservados

**Tecnologías utilizadas:**
- Python 3.8+
- MySQL 8.0+
- CustomTkinter (Interfaz moderna)
- ReportLab (Generación de PDFs)

**Licencia:** Software propietario
**Soporte:** Incluido durante el primer año

---

## Apéndices

### Apéndice A: Atajos de Teclado

| Atajo | Acción |
|-------|--------|
| `Ctrl + N` | Nuevo parte |
| `Ctrl + S` | Guardar |
| `Ctrl + E` | Editar seleccionado |
| `Ctrl + D` | Eliminar seleccionado |
| `Ctrl + F` | Buscar |
| `Ctrl + P` | Generar informe |
| `F1` | Ayuda |
| `F5` | Actualizar datos |

### Apéndice B: Códigos de Error Comunes

| Código | Descripción | Solución |
|--------|-------------|----------|
| `ERR-001` | Error de conexión BD | Verificar MySQL y credenciales |
| `ERR-002` | Permisos insuficientes | Ejecutar como administrador |
| `ERR-003` | Archivo no encontrado | Verificar rutas de configuración |
| `ERR-004` | Formato de archivo incorrecto | Usar plantilla oficial |
| `ERR-005` | Espacio en disco insuficiente | Liberar espacio |

### Apéndice C: Formato de Archivos de Importación

Ver documentación técnica para especificaciones detalladas de:
- Formato Excel para presupuestos
- Formato Excel para catálogos
- Estructura de archivos CSV

---

**Fin del Manual de Usuario**

*Para más información, consulte el Manual Técnico o contacte con soporte técnico.*
