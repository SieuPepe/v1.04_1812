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

*Última actualización: 2025-11-12*
