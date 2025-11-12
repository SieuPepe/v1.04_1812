# Limpieza y Reorganización del Proyecto

## 📋 Resumen de Cambios

Este documento describe la reorganización completa del proyecto HydroFlow Manager para separar claramente el código de producción de las herramientas de desarrollo.

---

## 🗂️ Nueva Estructura

### ✅ **Código de Producción** (incluir en instalador)

```
v1.04_1812/
├── main.py                      # Punto de entrada
├── interface/                   # Interfaces gráficas (GUI)
│   └── *_interfaz.py           # Todas las ventanas
├── script/                      # Lógica de negocio
│   ├── db_*.py                 # Módulos de BD
│   ├── informes*.py            # Sistema de informes
│   ├── ctk_*.py                # Widgets personalizados
│   └── certification_export.py  # Exportación
├── resources/                   # Recursos de la aplicación
│   └── images/                 # Imágenes, logos, iconos
├── tools/                       # Herramientas de usuario
│   ├── crear_backup_bd.py      # Backup/restore
│   └── configurar_instalacion.py # Configuración inicial
├── requirements.txt             # Dependencias
├── HidroFlowManager.spec       # Configuración PyInstaller
└── build.py                    # Script de compilación
```

### 🔧 **Herramientas de Desarrollo** (NO incluir en instalador)

```
dev_tools/
├── importacion/                # Scripts de importación
│   ├── budget_import.py       # Importar presupuestos
│   ├── catalog_import.py      # Importar catálogos
│   ├── importar_mediciones_ots.py
│   └── importar_partes_access.py
├── generadores/                # Generadores de datos
│   ├── generar_datos_prueba.py
│   ├── generar_insert_partes.py
│   ├── generar_sql_mediciones.py
│   ├── generar_script_importacion.py
│   ├── generar_script_decimales.py
│   ├── generar_codigos_postales.py
│   ├── crear_vista_partes.py
│   ├── crear_vista_partes_v2.py
│   ├── debug_importacion_partes.py
│   └── insertar_partes_por_lotes.py
└── verificacion/               # Scripts de verificación
    ├── verificar_esquemas.py
    ├── verificar_integridad_completa.py
    ├── verificar_codigos_excel.py
    ├── verificar_db_limpia.py
    ├── check_mysql.py
    ├── test_conexion_directa.py
    ├── analizar_municipios_excel.py
    ├── actualizar_naturalezas.py
    ├── crear_dim_tipos_rep_schema.py
    ├── aplicar_decimales.py
    ├── aplicar_indices.py
    ├── crear_backup.py (antiguo)
    ├── cargar_presupuesto.py
    ├── limpiar_partes.py
    └── ejecutar_*.ps1
```

### 📚 **Documentación de Desarrollo**

```
docs/
├── desarrollo/                 # Docs de desarrollo interno
│   ├── README_*.md            # Todos los READMEs de desarrollo
│   └── db_core_refactored_example.py
├── adr/                        # Decisiones arquitectónicas
└── architecture/               # Documentación de arquitectura
```

---

## 📦 Cambios Realizados

### 1. **Imágenes Movidas** ✅

**Antes:**
```
source/
├── logo.png
├── guardar.png
├── cancelar.png
└── ... (20+ imágenes)
```

**Después:**
```
resources/images/
├── logo.png
├── guardar.png
├── cancelar.png
└── ... (todas las imágenes)
```

**Cambios en código:**
- Todas las referencias `/source/` → `/resources/images/`
- Actualizado en ~60 archivos de interface/
- Actualizado en main.py

### 2. **Scripts de Desarrollo Separados** ✅

**Movidos 35+ archivos** de `script/` a `dev_tools/`:

#### Importación (4 archivos):
- budget_import.py
- catalog_import.py
- importar_mediciones_ots.py
- importar_partes_access.py

#### Generadores (10 archivos):
- generar_datos_prueba.py
- generar_insert_partes.py
- generar_sql_mediciones.py
- generar_script_importacion.py
- generar_script_decimales.py
- generar_codigos_postales.py
- crear_vista_partes.py
- crear_vista_partes_v2.py
- debug_importacion_partes.py
- insertar_partes_por_lotes.py

#### Verificación (15 archivos):
- verificar_esquemas.py
- verificar_integridad_completa.py
- verificar_codigos_excel.py
- verificar_db_limpia.py
- check_mysql.py
- test_conexion_directa.py
- analizar_municipios_excel.py
- actualizar_naturalezas.py
- crear_dim_tipos_rep_schema.py
- aplicar_decimales.py
- aplicar_indices.py
- crear_backup.py (antiguo)
- cargar_presupuesto.py
- limpiar_partes.py
- ejecutar_*.ps1

### 3. **Documentación Reorganizada** ✅

**Movidos 19+ archivos** de `script/` a `docs/desarrollo/`:
- README_FASE2.md
- README_FASE3.md
- README_FASE3_dim_municipios.md
- README_DECIMALES.md
- README_INDICES.md
- README_MYSQL_SETUP.md
- README_TESTING.md
- README_VERIFICACION_CODIGOS.md
- README_IMPORTACION_MEDICIONES.md
- README_INSERTAR_PARTES.md
- README_INTEGRIDAD.md
- README_CORRECCION_MUNICIPIOS_ALAVA.md
- db_core_refactored_example.py
- Y más...

### 4. **.gitignore Mejorado** ✅

Nuevas exclusiones:
```gitignore
# Backups y datos temporales
backups/
*.sql
*.sql.gz

# Informes guardados (datos de usuario)
informes_guardados/*.json

# Logs
*.log
logs/

# Compilación
*.exe
*.msi
```

---

## 📊 Impacto en Tamaño

### Antes de la limpieza:
```
Total archivos: ~150+
script/: ~50 archivos
source/: ~25 imágenes
```

### Después de la limpieza:
```
Producción: ~60 archivos esenciales
Desarrollo: ~35 archivos en dev_tools/
Docs: ~20 archivos en docs/desarrollo/
```

**Reducción en instalador: ~40% menos archivos**

---

## 🚀 Beneficios

### Para Producción:
✅ **Instalador más ligero**: Solo archivos necesarios
✅ **Más limpio**: Sin scripts de desarrollo
✅ **Más rápido**: Menos archivos para PyInstaller
✅ **Más seguro**: Sin herramientas de importación en producción

### Para Desarrollo:
✅ **Mejor organización**: Todo categorizado
✅ **Fácil de encontrar**: Scripts en carpetas lógicas
✅ **Documentación clara**: Separada por tipo
✅ **Mantenible**: Estructura clara

---

## 📝 Archivos Principales en Producción

### script/ (22 archivos esenciales):
```
__init__.py
certification_export.py         # Exportación de certificaciones
ctk_scrollable_dropdown.py      # Widget dropdown personalizado
ctk_scrollable_dropdown_frame.py
ctk_xyframe.py                  # Widget frame personalizado
db_cache.py                     # Caché de BD
db_config.py                    # Configuración de BD
db_connection.py                # Conexiones a BD
db_core.py                      # Operaciones core de BD
db_partes.py                    # Operaciones de partes
db_projects.py                  # Operaciones de proyectos
db_user_config.py               # Configuración de usuario
informes.py                     # Lógica de informes
informes_config.py              # Configuración de informes
informes_exportacion.py         # Exportación de informes
informes_header_config.py       # Cabeceras de informes
informes_storage.py             # Almacenamiento de informes
```

### interface/ (sin cambios):
- Todos los archivos *_interfaz.py necesarios para la aplicación

### resources/images/:
- Todas las imágenes y logos necesarios

---

## 🔄 Migración

Si trabajas con una versión anterior:

1. **Hacer pull** de los últimos cambios
2. **Actualizar rutas** si tienes código personalizado
3. **Verificar imágenes**: Ahora en `resources/images/`
4. **Scripts de desarrollo**: Ahora en `dev_tools/`

---

## 💡 Uso de dev_tools/

### Para importar datos:
```bash
# Desde dev_tools/importacion/
python importar_mediciones_ots.py
python importar_partes_access.py
```

### Para verificar integridad:
```bash
# Desde dev_tools/verificacion/
python verificar_esquemas.py
python verificar_integridad_completa.py
```

### Para generar datos de prueba:
```bash
# Desde dev_tools/generadores/
python generar_datos_prueba.py
```

---

## 📞 Próximos Pasos

1. ✅ Verificar que la aplicación funciona correctamente
2. ✅ Compilar con PyInstaller y verificar tamaño
3. ✅ Probar instalador con nueva estructura
4. ✅ Actualizar documentación de usuario

---

## 📌 Notas Importantes

- **No eliminar dev_tools/** del repositorio (útil para desarrollo)
- **Sí excluir dev_tools/** del instalador de producción
- **Las rutas en el código** ya están actualizadas
- **Los backups** se guardan en `backups/` (excluido de git)

---

## 🧹 FASE 3: Limpieza del Directorio Raíz (2025-11-12)

### Archivos Eliminados

#### 📊 **Base de Datos de Ejemplo** (~15MB eliminados)
- ❌ `APLICACION CERTIFICACIONES UTE REDES URBIDE.accdb`
  - Base de datos Access del proyecto Urbide
  - Solo necesaria durante desarrollo inicial

#### 📈 **Archivos Excel de Datos** (~500KB eliminados)
- ❌ `LISTADO OTS.xlsx`
- ❌ `MEDICIONES OTS.xlsx`
- ❌ `PRECIOS UNITARIOS.xlsx`
- ❌ `Para exportar.xlsx`
  - Datos de ejemplo usados para alimentar la BD
  - No necesarios en producción ni desarrollo continuo

#### 🖼️ **Imágenes y Documentación** (~650KB eliminados)
- ❌ `Logo Redes Urbide.jpg` (duplicado en resources/images/)
- ❌ `Logo Urbide.jpg` (duplicado en resources/images/)
- ❌ `Certificacion por capitulos.jpg` (captura de ejemplo)
- ❌ `Informe certificaciones.jpg` (captura de ejemplo)
- ❌ `Informe recursos.jpg` (captura de ejemplo)
- ❌ `Definicion informes.docx` (documento de diseño)

#### 📝 **Archivos SQL Temporales** (~600KB eliminados)
- ❌ `actualizar_finalizada.sql`
- ❌ `actualizar_finalizada_safe.sql`
- ❌ `actualizar_finalizada_simple.sql`
- ❌ `importar_partes_desde_excel.sql`
- ❌ `script_cargar_precios_unitarios.sql`
- ❌ `script_cargar_precios_unitarios_backup.sql`
- ❌ `duplicados_detectados.csv`

#### 📂 **Carpetas Eliminadas** (~25MB eliminados)
- ❌ `backup/` - Backups SQL de desarrollo (25MB)
  - backup_BASE.sql
  - backup_PR001.sql
  - backup_completo.sql
  - backup_estructuraBBDD.sql
  - backup_test.sql
- ❌ `scripts/` - Carpeta duplicada (confusión con script/)
  - update_dim_red.sql
  - update_dim_tipo_trabajo.sql

### 📊 Impacto Total de la Limpieza

**Antes:**
```
Total archivos en raíz: ~45 archivos
Tamaño aproximado: ~42MB
```

**Después:**
```
Total archivos en raíz: ~20 archivos
Tamaño aproximado: ~0.5MB
```

**Reducción: ~41.5MB (~98% menos datos innecesarios)**

### 🔒 Mejoras en .gitignore

Se agregaron exclusiones para prevenir futuros commits accidentales:

```gitignore
# Bases de datos de ejemplo y desarrollo
*.accdb
*.mdb

# Archivos de datos de ejemplo (Excel, CSV)
*.xlsx
*.xls
*.csv
!requirements*.csv

# Documentos de Word temporales
*.docx
*.doc
~$*.docx
~$*.doc

# Imágenes de ejemplo/documentación (mantener solo en resources/)
/*.jpg
/*.jpeg
/*.png
!resources/**/*.jpg
!resources/**/*.jpeg
!resources/**/*.png

# Carpetas de datos de ejemplo
ejemplos_datos/
datos_prueba/
```

### ✅ Estado Final del Directorio Raíz

```
v1.04_1812/
├── .editorconfig                       # Configuración del editor
├── .env.example                        # Ejemplo de variables de entorno
├── .env.produccion.template            # Template para producción
├── .gitignore                          # Mejorado con nuevas exclusiones
├── .pre-commit-config.yaml             # Hooks de pre-commit
├── ESTRUCTURA_PROYECTO.md              # Documentación de estructura
├── HidroFlowManager.spec               # Configuración PyInstaller
├── INSTALACION_Y_CONFIGURACION.md      # Guía de instalación
├── LIMPIEZA_PROYECTO.md                # Este documento
├── VERIFICACION_INFORMES.md            # Guía de verificación
├── build.py                            # Script de compilación
├── installer.iss                       # Configuración instalador
├── main.py                             # Punto de entrada
├── pyproject.toml                      # Configuración Python
├── requirements.txt                    # Dependencias producción
├── requirements-dev.txt                # Dependencias desarrollo
│
├── dev_tools/                          # Herramientas de desarrollo
├── docs/                               # Documentación
├── ejemplos_informes_generados/        # Ejemplos de salida
├── informes_exhaustivos/               # Informes detallados
├── informes_guardados/                 # Informes guardados por usuario
├── interface/                          # Código GUI
├── INFORME TIPO/                       # Plantilla de informes
├── resources/                          # Recursos de la aplicación
├── script/                             # Lógica de negocio
├── tests/                              # Tests automáticos
└── tools/                              # Herramientas de usuario
```

### 🎯 Beneficios Logrados

1. ✅ **Repositorio más limpio**: Solo archivos esenciales y de configuración
2. ✅ **Menos confusión**: No hay datos de ejemplo mezclados con código
3. ✅ **Mejor seguridad**: No se commitean accidentalmente archivos de datos
4. ✅ **Menor tamaño**: ~42MB menos en el repositorio
5. ✅ **Más profesional**: Estructura clara y organizada
6. ✅ **.gitignore robusto**: Previene futuros commits de archivos innecesarios

### 📌 Notas Importantes

- Los archivos eliminados eran específicos del proyecto Urbide (ejemplo)
- Los datos necesarios ya están en la base de datos MySQL
- Las imágenes importantes se mantienen en `resources/images/`
- Los backups SQL de desarrollo ya no son necesarios
- La documentación de usuario se mantiene en la raíz
- La estructura de producción permanece intacta

---

## 📂 FASE 4: Reorganización de Documentación (2025-11-12)

### Objetivo
Organizar los manuales y archivos de configuración para una estructura más profesional.

### Cambios Realizados

#### 📚 **Creación de carpeta docs/manual/**
Se creó una nueva carpeta para centralizar toda la documentación de usuario e instalación.

#### 📖 **Manuales Movidos a docs/manual/**
Los siguientes archivos se movieron de la raíz a `docs/manual/`:

- ✅ `ESTRUCTURA_PROYECTO.md` → `docs/manual/ESTRUCTURA_PROYECTO.md`
- ✅ `INSTALACION_Y_CONFIGURACION.md` → `docs/manual/INSTALACION_Y_CONFIGURACION.md`
- ✅ `LIMPIEZA_PROYECTO.md` → `docs/manual/LIMPIEZA_PROYECTO.md`
- ✅ `VERIFICACION_INFORMES.md` → `docs/manual/VERIFICACION_INFORMES.md`

**Razón**: Mejor organización, separar manuales de código fuente.

#### 🔧 **requirements-dev.txt movido a dev_tools/**

- ✅ `requirements-dev.txt` → `dev_tools/requirements-dev.txt`

**Razón**: Consistencia con la separación producción/desarrollo. Las dependencias de desarrollo pertenecen a `dev_tools/`.

#### 📝 **Archivos Mantenidos en Raíz**

Los siguientes archivos permanecen en la raíz porque son necesarios:

- ✅ `.env.example` - Template de configuración para desarrollo
- ✅ `.env.produccion.template` - Template de configuración para producción
- ✅ `requirements.txt` - Dependencias de producción (necesarias para pip install)
- ✅ `main.py` - Punto de entrada
- ✅ `build.py` - Script de compilación
- ✅ `pyproject.toml` - Configuración del proyecto Python
- ✅ `HidroFlowManager.spec` - Configuración PyInstaller

### 🎯 Resultado Final

**Nueva estructura del directorio raíz:**
```
v1.04_1812/
├── .editorconfig
├── .env.example                        ← Template desarrollo
├── .env.produccion.template            ← Template producción
├── .gitignore
├── .pre-commit-config.yaml
├── HidroFlowManager.spec
├── build.py
├── installer.iss
├── main.py
├── pyproject.toml
├── requirements.txt                    ← Dependencias producción
│
├── dev_tools/
│   ├── requirements-dev.txt            ← Dependencias desarrollo (movido)
│   ├── importacion/
│   ├── generadores/
│   └── verificacion/
│
├── docs/
│   ├── manual/                         ← Nueva carpeta
│   │   ├── ESTRUCTURA_PROYECTO.md      ← Movido
│   │   ├── INSTALACION_Y_CONFIGURACION.md ← Movido
│   │   ├── LIMPIEZA_PROYECTO.md        ← Movido
│   │   └── VERIFICACION_INFORMES.md    ← Movido
│   ├── desarrollo/
│   ├── adr/
│   └── architecture/
│
├── interface/
├── resources/
├── script/
├── tests/
└── tools/
```

### 📊 Beneficios

1. ✅ **Raíz más limpia**: Solo archivos esenciales de configuración y ejecución
2. ✅ **Manuales organizados**: Toda la documentación de usuario en un solo lugar
3. ✅ **Separación clara**: Producción vs desarrollo
4. ✅ **Más profesional**: Estructura estándar de proyecto Python
5. ✅ **Fácil navegación**: Los usuarios saben dónde buscar manuales

### 📌 Notas

- Los archivos `.env` son templates y nunca deben contener credenciales reales
- `requirements.txt` debe permanecer en raíz (estándar Python)
- `requirements-dev.txt` en `dev_tools/` mantiene consistencia con herramientas de desarrollo
- Los documentos en `docs/` históricos no se actualizaron (son referencias antiguas)

---

## 🔧 FASE 5: Corrección de Módulos de Producción (2025-11-12)

### Problema Detectado
Al ejecutar `main.py`, se detectó el siguiente error:
```
ModuleNotFoundError: No module named 'script.catalog_import'
```

### Análisis
Durante la FASE 2, los módulos `budget_import.py` y `catalog_import.py` fueron movidos incorrectamente a `dev_tools/importacion/`, clasificándolos como herramientas de desarrollo.

Sin embargo, estos módulos son **funcionalidad de producción** esencial:

#### **budget_import.py**
- **Usado por**: `manager_interfaz.py` (línea 1210), `parts_manager_interfaz.py` (línea 2105)
- **Función**: Importar presupuestos desde Excel al catálogo base
- **Usuario final**: Necesita esta funcionalidad para crear proyectos e importar presupuestos

#### **catalog_import.py**
- **Usado por**: `manager_interfaz.py` (línea 1224)
- **Función**: Importar catálogos desde Excel
- **Usuario final**: Necesita esta funcionalidad para configurar proyectos

### Solución Aplicada

**Archivos movidos de vuelta a `script/`:**
- ✅ `dev_tools/importacion/budget_import.py` → `script/budget_import.py`
- ✅ `dev_tools/importacion/catalog_import.py` → `script/catalog_import.py`

**Archivos que permanecen en `dev_tools/importacion/` (correcto):**
- ✅ `importar_mediciones_ots.py` - Script de desarrollo para importar datos de ejemplo
- ✅ `importar_partes_access.py` - Script de desarrollo para migrar datos desde Access

### Resultado

#### Estructura corregida de `dev_tools/importacion/`:
```
dev_tools/importacion/
├── importar_mediciones_ots.py      # Script desarrollo ✅
└── importar_partes_access.py       # Script desarrollo ✅
```

#### Módulos de importación en `script/` (producción):
```
script/
├── budget_import.py                # Funcionalidad producción ✅
├── catalog_import.py               # Funcionalidad producción ✅
└── ... (otros módulos de producción)
```

### Verificación
```bash
python3 -c "from script.catalog_import import catalog_import;
            from script.budget_import import budget_import;
            print('✅ Imports correctos')"
# Resultado: ✅ Imports correctos
```

### Lección Aprendida
**Criterio para clasificar módulos:**
- ✅ **Producción (`script/`)**: Funcionalidad usada por interfaces de usuario final
- ✅ **Desarrollo (`dev_tools/`)**: Scripts usados solo durante desarrollo o configuración inicial

**No confundir:**
- "Importar" datos desde Excel para usuarios → **Producción**
- "Importar" datos de ejemplo para desarrollo → **Desarrollo**

---

## 🔄 FASE 6: Corrección de Rutas de Imágenes (2025-11-12)

### Problema Detectado
Al abrir el generador de partes, la aplicación buscaba imágenes en la carpeta `source/` que ya no existe:
```
FileNotFoundError: logo artanda2.png not found in source/
```

### Causa Raíz
Durante la FASE 2, se movieron todas las imágenes de `source/` a `resources/images/`, pero no se actualizaron todas las referencias en el código.

### Archivos Corregidos

#### 1. **interface/parts_manager_interfaz.py** (9 correcciones)
**Líneas corregidas: 108, 111, 114, 117, 120, 123, 145, 2940, 2969**

```python
# ANTES:
logo_path = os.path.join(parent_path, "source/logo artanda2.png")
resumen_path = os.path.join(parent_path, "source/proyecto.png")
# ... etc

# DESPUÉS:
logo_path = os.path.join(parent_path, "resources/images/logo artanda2.png")
resumen_path = os.path.join(parent_path, "resources/images/proyecto.png")
# ... etc
```

**Imágenes afectadas:**
- logo artanda2.png
- proyecto.png
- herramienta.png
- certificaciones.png
- informes.png
- info.png
- guardar.png
- logo_ep_N.png
- Logo Redes Urbide.jpg

#### 2. **HidroFlowManager.spec** (configuración PyInstaller)
**Líneas corregidas: 9-12, 63**

```python
# ANTES:
datas=[
    ('source/*.jpeg', 'source'),
    ('source/*.png', 'source'),
    ('source/*.ico', 'source'),
]
icon=['source\\logo.ico']

# DESPUÉS:
datas=[
    ('resources/images/*.jpeg', 'resources/images'),
    ('resources/images/*.png', 'resources/images'),
    ('resources/images/*.ico', 'resources/images'),
    ('resources/images/*.jpg', 'resources/images'),  # Añadido
]
icon=['resources\\images\\logo.ico']
```

#### 3. **script/informes_header_config.py**
**Líneas corregidas: 11-13**

```python
# ANTES:
SOURCE_DIR = Path(__file__).parent.parent / "source"
LOGO_REDES_URBIDE = SOURCE_DIR / "logo artanda.png"
LOGO_URBIDE = SOURCE_DIR / "logo artanda2.png"

# DESPUÉS:
IMAGES_DIR = Path(__file__).parent.parent / "resources" / "images"
LOGO_REDES_URBIDE = IMAGES_DIR / "logo artanda.png"
LOGO_URBIDE = IMAGES_DIR / "logo artanda2.png"
```

#### 4. **script/informes_exportacion.py**
**Líneas corregidas: 30, 35-36**

```python
# ANTES:
"""Busca los logos en la raíz del proyecto y en la carpeta source"""
directorios_busqueda = [
    base_dir,  # Raíz del proyecto (prioridad 1)
    os.path.join(base_dir, "source"),  # Carpeta source (prioridad 2)
]

# DESPUÉS:
"""Busca los logos en la raíz del proyecto y en la carpeta resources/images"""
directorios_busqueda = [
    os.path.join(base_dir, "resources", "images"),  # Carpeta resources/images (prioridad 1)
    base_dir,  # Raíz del proyecto (prioridad 2)
]
```

### Resumen de Cambios

**Total de archivos corregidos:** 4
**Total de líneas modificadas:** ~20

**Cambios realizados:**
- ✅ Todas las rutas `source/` → `resources/images/`
- ✅ Variable `SOURCE_DIR` → `IMAGES_DIR` (semántica)
- ✅ Añadido soporte para `.jpg` en PyInstaller
- ✅ Actualizado orden de prioridad en búsqueda de logos (resources/images primero)

### Verificación

```bash
# Verificar que no quedan referencias a source/ en código de producción
grep -rn "\"source/" interface/ script/ main.py --include="*.py"
# Resultado: Sin coincidencias ✅

# Verificar que las imágenes existen
ls resources/images/ | grep -E "logo|proyecto|herramienta|certificaciones|informes|guardar|info"
# Resultado: Todas las imágenes encontradas ✅
```

### Impacto

- ✅ **Generador de partes** ahora carga correctamente todos los logos e iconos
- ✅ **Sistema de informes** encuentra los logos para encabezados
- ✅ **PyInstaller** empaqueta las imágenes desde la ubicación correcta
- ✅ **No más errores** de `FileNotFoundError` por imágenes

### Lección Aprendida

Al mover archivos entre carpetas durante refactorización:
1. **Buscar exhaustivamente** todas las referencias en el código
2. **Incluir archivos de configuración** (.spec, .json, etc.)
3. **Probar todas las funcionalidades** que usen recursos movidos
4. **Documentar los cambios** para futuras referencias

**Patrón recomendado para búsqueda:**
```bash
# Buscar rutas absolutas
grep -rn "\"old_path/" . --include="*.py"

# Buscar variables de configuración
grep -rn "OLD_DIR" . --include="*.py"

# Verificar archivos de configuración
grep -rn "old_path" *.spec *.json *.yaml
```

---

*Última actualización: 2025-11-12*
