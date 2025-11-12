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

*Última actualización: 2025-11-12*
