# PLAN DE PASO A PRODUCCIÓN - HydroFlow Manager v1.04

## 📋 ÍNDICE
1. [Preparación Base de Datos](#1-preparación-base-de-datos)
2. [Limpieza de Código y Archivos](#2-limpieza-de-código-y-archivos)
3. [Actualización de Dependencias](#3-actualización-de-dependencias)
4. [Testing y Validación](#4-testing-y-validación)
5. [Compilación y Empaquetado](#5-compilación-y-empaquetado)
6. [Documentación de Usuario](#6-documentación-de-usuario)
7. [Backup y Seguridad](#7-backup-y-seguridad)
8. [Instalación en Cliente](#8-instalación-en-cliente)
9. [Post-Despliegue](#9-post-despliegue)

---

## 1. PREPARACIÓN BASE DE DATOS

### 1.1 Migración de Datos Históricos
**Prioridad: CRÍTICA**

- [ ] **Cargar todos los partes históricos desde Access**
  - Script: `script/ejecutar_migracion_manual.py`
  - Verificar que todos los partes del Access se hayan migrado
  - Validar integridad de datos (fechas, OTs, estados)
  - Comprobar relaciones: partes → presupuestos → certificaciones
  - Ejecutar script de verificación: `script/verificar_y_completar_migracion.py`
  - **Estimación:** 4-6 horas

- [ ] **Revisar y corregir carga de presupuesto de referencia**
  - Verificar script: `script/budget_import.py`
  - Comprobar que todos los conceptos del catálogo se carguen correctamente
  - Validar precios unitarios y unidades de medida
  - Asegurar relación correcta con tbl_catalogo
  - **Estimación:** 2-3 horas

- [ ] **Validar dimensiones (dim_*)**
  - Verificar que todas las tablas dim_red, dim_tipo_trabajo, etc. estén pobladas
  - Comprobar dim_provincias, dim_comarcas, dim_municipios (geografía)
  - Validar nomenclatura de columnas (comarca_nombre, municipio_nombre, etc.)
  - **Estimación:** 1 hora

- [ ] **Crear backup completo pre-producción**
  - Exportar base de datos completa con todos los datos migrados
  - Guardar en `backup/backup_produccion_YYYYMMDD.sql`
  - Documentar estructura de tablas y relaciones
  - **Estimación:** 1 hora

### 1.2 Optimización de Base de Datos

- [ ] **Revisar índices**
  - Verificar índices en tablas principales (tbl_partes, tbl_proyectos, tbl_ots)
  - Crear índices para búsquedas frecuentes (por fecha, por estado, por OT)
  - **Estimación:** 2 horas

- [ ] **Limpieza de datos**
  - Eliminar registros de prueba/test
  - Normalizar formatos de fecha
  - Validar datos nulos en campos obligatorios
  - **Estimación:** 2 horas

---

## 2. LIMPIEZA DE CÓDIGO Y ARCHIVOS

### 2.1 Eliminar Archivos de Desarrollo

- [ ] **Eliminar archivos de test y diagnóstico**
  ```bash
  rm test_*.py
  rm diagnostico*.py
  rm analizar_access.py
  rm temporal.py
  ```
  - **Lista completa:**
    - test_cert.py
    - test_codigo_ot_debug.py
    - test_env.py
    - test_form_v2.py
    - test_imports.py
    - test_informes_ui.py
    - test_partes_mejorados.py
    - test_treeview_style.py
    - diagnostico_dim_geograficas.py
    - diagnostico_interfaz.py
    - analizar_access.py
    - temporal.py
  - **Estimación:** 15 minutos

- [ ] **Eliminar archivos de desarrollo**
  ```bash
  rm run_parts_*.py
  rm lista.txt
  ```
  - **Estimación:** 5 minutos

- [ ] **Eliminar pantallazos y documentación de desarrollo**
  ```bash
  rm Pantallazo*.jpg
  ```
  - **Mantener:** Documentos MD necesarios (mover a docs/)
  - **Estimación:** 10 minutos

### 2.2 Limpiar Documentación

- [ ] **Reorganizar documentos markdown**
  - Mover documentos técnicos a `docs/desarrollo/`
  - Mantener solo README.md, CHANGELOG.md en raíz
  - Crear `docs/usuario/` para manuales de usuario
  - **Archivos a mover:**
    - ANALISIS_*.md → docs/desarrollo/
    - COMPARACION_*.md → docs/desarrollo/
    - GUIA_*.md → docs/desarrollo/
    - PLAN_*.md → docs/desarrollo/
    - MEJORAS_*.md → docs/desarrollo/
    - MIGRATION_*.md → docs/desarrollo/
    - SISTEMA_INFORMES_RESUMEN.md → docs/desarrollo/
  - **Estimación:** 30 minutos

- [ ] **Actualizar CHANGELOG.md**
  - Documentar todas las características de v1.04
  - Incluir mejoras de sistema de informes
  - Listar bugs corregidos
  - **Estimación:** 1 hora

### 2.3 Configuración

- [ ] **Limpiar archivos de configuración**
  - Eliminar .env de desarrollo (mantener .env.example)
  - Verificar que .env esté en .gitignore
  - Crear .env.produccion.template con valores para el cliente
  - **Estimación:** 15 minutos

---

## 3. ACTUALIZACIÓN DE DEPENDENCIAS

### 3.1 Verificar Dependencias

- [ ] **Agregar dependencias faltantes a requirements.txt**
  ```python
  # Agregar:
  tkcalendar>=1.6.0  # Usado en sistema de informes
  openpyxl>=3.0.0    # Para exportación Excel
  python-docx>=0.8.0 # Para exportación Word
  reportlab>=3.6.0   # Para exportación PDF
  ```
  - **Estimación:** 15 minutos

- [ ] **Verificar versiones mínimas**
  - Python >= 3.8
  - MySQL >= 8.0
  - customtkinter >= 5.0.0
  - **Estimación:** 15 minutos

- [ ] **Crear requirements-produccion.txt** (sin dependencias de dev)
  ```bash
  # Sin:
  # - pytest, black, flake8, etc. (están en requirements-dev.txt)
  ```
  - **Estimación:** 10 minutos

### 3.2 Congelar Dependencias

- [ ] **Generar requirements.lock**
  ```bash
  pip freeze > requirements.lock
  ```
  - Incluir versiones exactas para reproducibilidad
  - **Estimación:** 5 minutos

---

## 4. TESTING Y VALIDACIÓN

### 4.1 Testing Funcional Completo

- [ ] **Módulo de Login**
  - [ ] Login con credenciales correctas
  - [ ] Login con credenciales incorrectas
  - [ ] Recuperación de contraseña (si aplica)
  - **Estimación:** 30 minutos

- [ ] **Módulo de Partes**
  - [ ] Crear nuevo parte
  - [ ] Editar parte existente
  - [ ] Eliminar parte
  - [ ] Filtros y búsquedas
  - [ ] Validación de campos obligatorios
  - [ ] Relación con OTs y proyectos
  - **Estimación:** 2 horas

- [ ] **Módulo de Presupuestos**
  - [ ] Crear presupuesto desde catálogo
  - [ ] Modificar cantidades y precios
  - [ ] Calcular totales correctamente
  - [ ] Vincular con parte
  - **Estimación:** 1 hora

- [ ] **Módulo de Certificaciones**
  - [ ] Crear certificación desde presupuesto
  - [ ] Marcar conceptos como certificados
  - [ ] Calcular pendiente correctamente
  - [ ] Exportar certificación
  - **Estimación:** 1.5 horas

- [ ] **Módulo de Informes (NUEVO)**
  - [ ] Crear informe básico (todos los campos)
  - [ ] Aplicar filtros simples (Igual a, Mayor que, etc.)
  - [ ] Aplicar filtro "Entre" con fechas (DateEntry)
  - [ ] Aplicar filtro "Entre" con números
  - [ ] Lógica AND/OR entre filtros
  - [ ] Clasificaciones (ordenamiento)
  - [ ] Verificar totalizadores (sumas)
  - [ ] Vista previa en pantalla
  - [ ] Exportar a Excel
  - [ ] Exportar a Word
  - [ ] Exportar a PDF
  - [ ] **Guardar configuración de informe**
  - [ ] **Cargar configuración guardada**
  - [ ] **Eliminar configuración**
  - [ ] Probar con dimensiones geográficas (comarca, municipio)
  - **Estimación:** 4 horas

### 4.2 Testing de Integración

- [ ] **Flujo completo: Parte → Presupuesto → Certificación**
  - Crear parte nuevo
  - Agregar presupuesto
  - Generar certificación
  - Generar informe con este parte
  - **Estimación:** 1 hora

- [ ] **Testing de base de datos**
  - Verificar integridad referencial
  - Comprobar cascadas (DELETE, UPDATE)
  - Validar triggers si existen
  - **Estimación:** 1 hora

### 4.3 Testing de Rendimiento

- [ ] **Cargar informes con grandes volúmenes**
  - Probar con 1000+ partes
  - Medir tiempo de respuesta
  - Verificar uso de memoria
  - **Estimación:** 1 hora

- [ ] **Testing de exportación**
  - Exportar informes grandes (>500 registros)
  - Verificar que no se cuelgue la aplicación
  - **Estimación:** 30 minutos

### 4.4 Testing de UI/UX

- [ ] **Verificar todos los iconos cargan correctamente**
- [ ] **Comprobar responsive (redimensionamiento)**
- [ ] **Validar que ventanas modales aparezcan al frente**
- [ ] **Probar navegación entre módulos**
- [ ] **Verificar mensajes de error son claros**
- **Estimación:** 1.5 horas

---

## 5. COMPILACIÓN Y EMPAQUETADO

### 5.1 Preparar Compilación

- [ ] **Actualizar HidroFlowManager.spec**
  - Verificar que incluya todos los módulos
  - Agregar hiddenimports si es necesario:
    ```python
    hiddenimports=[
        'mysql.connector',
        'tkcalendar',
        'customtkinter',
        'CTkMessagebox',
        'PIL',
        'matplotlib',
        'openpyxl',
        'docx',
        'reportlab',
        'script.informes_storage'  # NUEVO módulo
    ]
    ```
  - Verificar que incluya recursos (source/*.png, source/*.ico)
  - Verificar icono de aplicación: source/logo.ico
  - **Estimación:** 30 minutos

- [ ] **Crear directorio informes_guardados**
  - Agregar carpeta vacía para configuraciones de informes
  - Incluir README.txt explicando su uso
  - **Estimación:** 10 minutos

### 5.2 Compilar con PyInstaller

- [ ] **Compilación Windows**
  ```bash
  pyinstaller HidroFlowManager.spec
  ```
  - Verificar que se genera dist/HidroFlowManager.exe
  - Tamaño aproximado: 80-150 MB
  - **Estimación:** 15 minutos (compilación)

- [ ] **Testing del ejecutable**
  - Probar en máquina SIN Python instalado
  - Verificar que cargue correctamente
  - Comprobar que se conecta a base de datos
  - Probar todas las funcionalidades principales
  - **Estimación:** 2 horas

### 5.3 Empaquetado Final

- [ ] **Crear estructura de instalación**
  ```
  HydroFlowManager_v1.04/
  ├── HidroFlowManager.exe
  ├── LEEME.txt (instrucciones de instalación)
  ├── CHANGELOG.txt
  ├── config/
  │   └── .env.template
  ├── informes_guardados/
  │   └── README.txt
  ├── docs/
  │   ├── Manual_Usuario.pdf
  │   └── Manual_Informes.pdf
  └── backup/
      └── estructura_base_datos.sql
  ```
  - **Estimación:** 1 hora

- [ ] **Crear instalador (opcional)**
  - Usar Inno Setup o NSIS para crear setup.exe
  - Incluir opciones de instalación
  - Crear accesos directos
  - **Estimación:** 3 horas

---

## 6. DOCUMENTACIÓN DE USUARIO

### 6.1 Manual de Usuario

- [ ] **Crear Manual_Usuario.pdf**
  - Introducción a la aplicación
  - Requisitos del sistema
  - Instalación y configuración inicial
  - Módulo de Login
  - Módulo de Partes (crear, editar, eliminar)
  - Módulo de Presupuestos
  - Módulo de Certificaciones
  - Screenshots de cada pantalla
  - **Estimación:** 8 horas

- [ ] **Crear Manual_Informes.pdf (NUEVO)**
  - Introducción al generador de informes
  - Seleccionar tipo de informe
  - Agregar filtros (operadores, valores)
  - Lógica AND/OR entre filtros
  - Usar selector de fechas (calendario)
  - Clasificar datos (ordenamiento)
  - Seleccionar campos a mostrar
  - Vista previa de resultados
  - Exportar a Excel, Word, PDF
  - **Guardar/Cargar configuraciones de informes**
  - Casos de uso comunes:
    - "Partes en curso por OT"
    - "Partes certificados en rango de fechas"
    - "Resumen económico por comarca"
  - Screenshots paso a paso
  - **Estimación:** 6 horas

### 6.2 Documentación Técnica

- [ ] **Crear Manual_Tecnico.pdf**
  - Arquitectura de la aplicación
  - Estructura de base de datos (diagrama ER)
  - Descripción de tablas principales
  - Configuración de .env
  - Backup y restauración
  - Solución de problemas comunes
  - **Estimación:** 4 horas

- [ ] **Crear Guia_Instalacion_BD.pdf**
  - Instalación de MySQL
  - Creación de esquemas
  - Importación de estructura
  - Importación de datos
  - Configuración de permisos
  - **Estimación:** 2 horas

---

## 7. BACKUP Y SEGURIDAD

### 7.1 Backups

- [ ] **Crear backup completo final**
  ```bash
  mysqldump -u root -p --all-databases > backup/backup_produccion_final_YYYYMMDD.sql
  ```
  - **Estimación:** 30 minutos

- [ ] **Crear backup solo estructura**
  ```bash
  mysqldump -u root -p --no-data --all-databases > backup/estructura_produccion_YYYYMMDD.sql
  ```
  - Para instalaciones nuevas en cliente
  - **Estimación:** 15 minutos

- [ ] **Crear backup solo datos**
  ```bash
  mysqldump -u root -p --no-create-info --all-databases > backup/datos_produccion_YYYYMMDD.sql
  ```
  - **Estimación:** 15 minutos

### 7.2 Seguridad

- [ ] **Revisar permisos de base de datos**
  - Usuario de aplicación con permisos mínimos necesarios
  - NO usar root en producción
  - **Estimación:** 30 minutos

- [ ] **Revisar manejo de contraseñas**
  - Verificar que .env no se incluya en distribución
  - Comprobar que no hay contraseñas hardcodeadas
  - **Estimación:** 30 minutos

- [ ] **Crear script de backup automático para cliente**
  ```bash
  # backup_automatico.bat (Windows)
  # Se ejecuta diariamente vía Task Scheduler
  ```
  - **Estimación:** 1 hora

---

## 8. INSTALACIÓN EN CLIENTE

### 8.1 Pre-Instalación

- [ ] **Documento de requisitos previos**
  - Windows 10/11 (64-bit)
  - MySQL 8.0 o superior instalado
  - 4 GB RAM mínimo (8 GB recomendado)
  - 500 MB espacio en disco
  - Conexión de red al servidor MySQL
  - **Estimación:** 30 minutos

- [ ] **Checklist de pre-instalación**
  - [ ] MySQL instalado y corriendo
  - [ ] Backup de datos existentes (si aplica)
  - [ ] Credenciales de administrador MySQL
  - [ ] Red configurada (si MySQL remoto)
  - **Estimación:** 15 minutos

### 8.2 Instalación Base de Datos

- [ ] **Crear esquema de base de datos**
  ```sql
  CREATE DATABASE hidroflow_produccion;
  ```
  - **Estimación:** 5 minutos

- [ ] **Importar estructura**
  ```bash
  mysql -u root -p hidroflow_produccion < backup/estructura_produccion.sql
  ```
  - **Estimación:** 10 minutos

- [ ] **Importar datos iniciales**
  - Catálogos (dim_*, tbl_catalogo)
  - Datos históricos migrados
  - **Estimación:** 30 minutos

- [ ] **Crear usuario de aplicación**
  ```sql
  CREATE USER 'hidroflow_app'@'localhost' IDENTIFIED BY 'contraseña_segura';
  GRANT SELECT, INSERT, UPDATE, DELETE ON hidroflow_produccion.* TO 'hidroflow_app'@'localhost';
  FLUSH PRIVILEGES;
  ```
  - **Estimación:** 10 minutos

### 8.3 Instalación Aplicación

- [ ] **Copiar ejecutable a carpeta de instalación**
  - Recomendado: C:\Program Files\HydroFlowManager\
  - **Estimación:** 5 minutos

- [ ] **Configurar .env**
  - Copiar .env.template a .env
  - Configurar credenciales de base de datos
  - Configurar host y puerto
  - **Estimación:** 10 minutos

- [ ] **Crear accesos directos**
  - Escritorio
  - Menú Inicio
  - **Estimación:** 5 minutos

### 8.4 Verificación de Instalación

- [ ] **Ejecutar aplicación por primera vez**
  - Verificar conexión a base de datos
  - Login con usuario administrador
  - **Estimación:** 10 minutos

- [ ] **Testing básico en cliente**
  - Crear un parte de prueba
  - Crear un presupuesto
  - Generar un informe
  - Guardar y cargar configuración de informe
  - **Estimación:** 1 hora

---

## 9. POST-DESPLIEGUE

### 9.1 Capacitación

- [ ] **Capacitación básica (2-3 horas)**
  - Navegación general
  - Crear partes
  - Gestión de presupuestos
  - Generar certificaciones
  - **Estimación:** 3 horas

- [ ] **Capacitación módulo de informes (1-2 horas)**
  - Generar informes básicos
  - Usar filtros avanzados
  - Guardar configuraciones frecuentes
  - Exportar a diferentes formatos
  - **Estimación:** 2 horas

### 9.2 Soporte Post-Instalación

- [ ] **Período de soporte inicial (1-2 semanas)**
  - Resolver dudas
  - Ajustar configuraciones
  - Corregir problemas menores
  - **Estimación:** variable

- [ ] **Crear canal de comunicación**
  - Email de soporte
  - Teléfono de contacto
  - Sistema de tickets (opcional)
  - **Estimación:** 30 minutos

### 9.3 Seguimiento

- [ ] **Primera revisión (1 semana)**
  - Verificar funcionamiento
  - Recoger feedback
  - Ajustar si es necesario
  - **Estimación:** 2 horas

- [ ] **Segunda revisión (1 mes)**
  - Verificar uso regular
  - Identificar mejoras
  - Planificar actualizaciones
  - **Estimación:** 2 horas

---

## 📊 RESUMEN DE ESTIMACIONES

| Fase | Tiempo Estimado |
|------|----------------|
| 1. Base de Datos | 12-16 horas |
| 2. Limpieza | 2-3 horas |
| 3. Dependencias | 1 hora |
| 4. Testing | 15-18 horas |
| 5. Compilación | 6-8 horas |
| 6. Documentación | 20-24 horas |
| 7. Backup y Seguridad | 3-4 horas |
| 8. Instalación Cliente | 3-4 horas |
| 9. Post-Despliegue | 7-9 horas |
| **TOTAL** | **69-87 horas** |
| **Días laborables (8h/día)** | **9-11 días** |

---

## ⚠️ ELEMENTOS CRÍTICOS

### 🔴 Prioridad MÁXIMA
1. ✅ **Migración completa de partes históricos** - SIN ESTO NO SE PUEDE DESPLEGAR
2. ✅ **Validación de presupuesto de referencia** - DATOS CRÍTICOS
3. ✅ **Backup completo pre-producción** - SEGURIDAD
4. ✅ **Testing módulo de informes completo** - NUEVA FUNCIONALIDAD

### 🟠 Prioridad ALTA
5. Testing funcional completo de todos los módulos
6. Documentación de usuario (manuales)
7. Compilación y testing del ejecutable

### 🟡 Prioridad MEDIA
8. Optimización de base de datos
9. Documentación técnica
10. Instalador automatizado

---

## 📝 NOTAS ADICIONALES

### Módulo de Informes - Puntos de Atención

El nuevo módulo de informes implementa funcionalidades avanzadas que requieren validación especial:

1. **DateEntry (Selector de Calendario)**
   - Verificar que tkcalendar esté en requirements.txt
   - Probar formato de fecha (yyyy-mm-dd)
   - Validar operador "Entre" con dos calendarios

2. **Configuraciones Guardadas**
   - Verificar que directorio `informes_guardados/` se cree automáticamente
   - Probar guardar/cargar/eliminar configuraciones
   - Validar que las configuraciones restauren correctamente:
     - Filtros con valores
     - Lógica AND/OR
     - Clasificaciones
     - Campos seleccionados

3. **Dimensiones Geográficas**
   - Validar que dim_comarcas, dim_municipios funcionen
   - Comprobar auto-detección de columnas (comarca_nombre, municipio_nombre)
   - Probar filtros por comarca/municipio

4. **Campos Calculados**
   - Presupuesto (subquery)
   - Certificado (subquery)
   - Pendiente (cálculo)
   - Verificar rendimiento con muchos registros

### Dependencias Nuevas a Agregar

```txt
# requirements.txt - AGREGAR:
tkcalendar>=1.6.0
openpyxl>=3.0.0
python-docx>=0.8.0
reportlab>=3.6.0
```

### Estructura de Archivos para Distribución

```
dist/
└── HydroFlowManager_v1.04_Installer/
    ├── HidroFlowManager.exe (ejecutable principal)
    ├── LEEME.txt
    ├── CHANGELOG.txt
    ├── config/
    │   └── .env.template
    ├── informes_guardados/  (directorio para configs)
    │   └── README.txt
    ├── docs/
    │   ├── Manual_Usuario.pdf
    │   ├── Manual_Informes.pdf
    │   ├── Manual_Tecnico.pdf
    │   └── Guia_Instalacion_BD.pdf
    ├── backup/
    │   ├── estructura_base_datos.sql
    │   └── backup_automatico.bat
    └── source/  (si es necesario, iconos y recursos)
```

---

## ✅ CHECKLIST FINAL PRE-ENTREGA

Verificar TODOS estos puntos antes de entregar al cliente:

- [ ] Base de datos con todos los datos históricos migrados
- [ ] Presupuesto de referencia validado
- [ ] Backup completo realizado
- [ ] Todos los archivos de test eliminados
- [ ] Documentación reorganizada
- [ ] requirements.txt actualizado con tkcalendar, openpyxl, etc.
- [ ] CHANGELOG.md actualizado
- [ ] HidroFlowManager.spec actualizado con nuevos módulos
- [ ] Ejecutable compilado y probado
- [ ] Testing funcional completo realizado
- [ ] Manuales de usuario generados (PDF)
- [ ] Estructura de instalación preparada
- [ ] Scripts de backup automático creados
- [ ] Instalación en cliente verificada
- [ ] Capacitación planificada

---

**Documento creado:** 2025-11-03
**Versión:** 1.0
**Proyecto:** HydroFlow Manager v1.04
**Módulo nuevo:** Sistema de Generación de Informes Dinámicos con Guardar/Cargar Configuraciones
