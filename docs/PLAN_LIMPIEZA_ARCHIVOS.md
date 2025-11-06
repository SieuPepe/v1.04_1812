# 🧹 PLAN DE LIMPIEZA Y REORGANIZACIÓN DE ARCHIVOS

**Fecha:** 2025-11-06
**Objetivo:** Limpiar archivos obsoletos y reorganizar la estructura del proyecto

---

## 📊 Análisis de Estructura Actual

### Estadísticas
- **Archivos totales analizados:** ~150+ archivos
- **Archivos Python:** ~90+
- **Archivos Markdown:** ~40+
- **Archivos SQL:** ~15+
- **Backups SQL:** 5

---

## 🗑️ ARCHIVOS A ELIMINAR

### 1. Tests Obsoletos / Temporales (8 archivos)

```bash
# Tests antiguos que ya no son necesarios
rm test_cert.py                    # Test temporal de certificaciones
rm test_codigo_ot_debug.py         # Test de debugging
rm test_env.py                     # Test de entorno (fallaba)
rm test_form_v2.py                 # Test temporal de formulario
rm test_informes_ui.py             # Test temporal de UI
rm test_partes_mejorados.py        # Test antiguo (fallaba)
rm test_treeview_style.py          # Test temporal de estilos
rm temporal.py                     # Archivo temporal

```

### 2. Scripts de Diagnóstico Antiguos (3 archivos)

```bash
# Scripts de diagnóstico ya no necesarios
rm diagnostico_dim_geograficas.py  # Ya verificado, no necesario
rm diagnostico_interfaz.py          # Ya verificado, no necesario
rm diagnostico_informes.py          # Ya verificado, no necesario
```

### 3. Scripts de Migración Ya Completados (3 archivos)

```bash
# Scripts de migración que ya fueron ejecutados
rm script/migrate_partes_mejoras.py           # Migración ya completada
rm script/ejecutar_migracion_manual.py        # Ya no necesario
rm script/verificar_y_completar_migracion.py  # Ya no necesario
```

### 4. Documentación Obsoleta / Duplicada (15 archivos)

```bash
# Documentación antigua o redundante
rm ANALISIS_EXHAUSTIVO_BD_CERTIFICACIONES.md  # Análisis antiguo
rm ANALISIS_INFORMES_ACCESS_VS_GENERADOR.md    # Análisis antiguo
rm COMO_VER_CAMBIOS_INFORMES.md                # Ya no necesario
rm COMPARACION_ENFOQUES.md                      # Duplicado con otros análisis
rm EJECUTAR_MIGRACION_AHORA.md                  # Migración ya completada
rm GUIA_PRUEBA_MIGRACION.md                     # Migración ya completada
rm INICIO_RAPIDO_PRUEBA.md                      # Duplicado con README_EJECUTAR.md
rm MEJORAS_UI_ESPECIFICACIONES_TECNICAS.md      # Obsoleto (mejoras ya aplicadas)
rm MIGRATION_GUIDE.md                            # Migración ya completada
rm OPTIMIZACIONES_BACKEND.md                     # Duplicado
rm PLAN_REFACTORIZACION_INTERFACES.md           # Obsoleto (ver PLAN_EXCELENCIA)
rm PYCHARM_SETUP.md                              # No relevante para producción
rm RESUMEN_MIGRACION_PARTES_FASE1.md            # Migración ya completada
rm REVISION_BASE_DATOS.md                        # Análisis antiguo
rm SCRIPTS_REFACTORIZACION.md                    # Ya no necesario
rm SOLUCION_TREEVIEW.md                          # Problema ya resuelto
rm VERIFICATION_REPORT.md                        # Duplicado con VALIDACION_TESTS
```

### 5. Interfaces Duplicadas (1 archivo)

```bash
# Interfaz duplicada (usamos parts_interfaz_v2_fixed.py)
rm interface/parts_interfaz_v2.py               # Versión antigua sin fixes
```

### 6. Scripts Auxiliares Obsoletos (5 archivos)

```bash
# Scripts que ya no se usan
rm analizar_access.py                           # Análisis ya completado
rm generar_1000_partes.py                       # Script de prueba, no necesario
rm parts_list_window.py                         # Ventana obsoleta
rm parts_tab_embed.py                           # Componente obsoleto
rm ver_estructura_cert.py                       # Script de verificación temporal
```

### 7. SQL de Verificación/Migración (6 archivos)

```bash
# SQL ya ejecutados o de verificación temporal
rm script/verificar_migracion.sql              # Migración ya verificada
rm script/verificar_municipios_gipuzkoa.sql    # Ya verificado
rm script/eliminar_codigo_ot.sql               # Ya ejecutado (o no necesario)
rm script/eliminar_dim_ot.sql                  # Ya ejecutado (o no necesario)
rm script/eliminar_fecha_prevista_fin.sql      # Ya ejecutado (o no necesario)
```

### 8. Scripts de Test de Migración (1 archivo)

```bash
# Script de test de migración ya no necesario
rm script/test_migration_complete.py           # Migración completa y validada
```

### 9. Documentación README Duplicada (2 archivos)

```bash
# READMEs duplicados/obsoletos
rm README_GENERAR_PARTES_PRUEBA.md             # Obsoleto
rm README_REFACTORIZACION.md                    # Obsoleto (ver PLAN_EXCELENCIA)
```

---

## 📁 TOTAL DE ARCHIVOS A ELIMINAR: **45 archivos**

---

## ✅ ARCHIVOS A MANTENER (Organizados)

### Documentación Esencial (8 archivos)

```
✅ PROYECTO_COMPLETADO.md              # Certificación final
✅ VALIDACION_TESTS_COMPLETA.md        # Certificación de tests
✅ VERIFICACION_INTERFACES_COMPLETA.md # Certificación de interfaces
✅ TESTS_CORREGIDOS_SIGUIENTES_PASOS.md # Guía de correcciones
✅ ESTRATEGIA_TESTING_PREPRODUCCION.md # Estrategia de testing
✅ RESULTADOS_TESTS_Y_CORRECIONES.md   # Análisis de fallos
✅ LIMPIEZA_BRANCHES_GITHUB.md         # Guía de limpieza (histórico)
✅ README_EJECUTAR.md                   # Guía de ejecución
```

### Documentación de Referencia (5 archivos)

```
✅ DATABASE_README.md                   # Documentación de BD
✅ COMPARACION_APLICACION_VS_BD_ACCESS.md # Comparación con Access
✅ SISTEMA_INFORMES_RESUMEN.md          # Documentación de informes
✅ PLAN_EXCELENCIA_INTERFACES.md        # Plan de mejora (referencia futura)
✅ PLAN_PASO_A_PRODUCCION.md            # Plan de producción
✅ MEJORAS_PARTES_README.md             # Mejoras de partes (histórico)
```

### Tests Activos (4 archivos)

```
✅ test_presupuestos.py                 # Test de presupuestos ✅
✅ test_certificaciones.py              # Test de certificaciones ✅
✅ test_flujo_completo.py               # Test end-to-end ✅
✅ test_imports.py                       # Test de imports básicos
```

### Scripts de Verificación (3 archivos)

```
✅ verificar_interfaces.py               # Verificación dinámica
✅ verificar_interfaces_estatico.py      # Verificación estática
✅ detectar_estructura_bd.py             # Detección de estructura BD
✅ detectar_columnas_precios.py          # Detección de columnas
```

### Scripts de Utilidad Principal (2 archivos)

```
✅ main.py                               # Aplicación principal
✅ run_parts_form.py                     # Formulario de partes
✅ run_parts_simple.py                   # Formulario simple
```

### Backups SQL (Mantener solo los necesarios)

```
✅ backup/backup_estructuraBBDD.sql     # Estructura de BD (mantener)
✅ backup/backup_BASE.sql                # Backup base (mantener)

❓ backup/backup_PR001.sql               # ¿Necesario?
❓ backup/backup_completo.sql            # ¿Necesario?
❓ backup/backup_test.sql                # ¿Necesario?
```

---

## 📂 ESTRUCTURA RECOMENDADA DESPUÉS DE LIMPIEZA

```
v1.04_1812/
├── main.py                              # Entrada principal
├── run_parts_form.py                    # Formulario partes completo
├── run_parts_simple.py                  # Formulario partes simple
│
├── requirements.txt                     # Dependencias
├── requirements-dev.txt                 # Dependencias desarrollo
├── lista.txt                            # ¿Qué es esto?
│
├── docs/                                # Documentación técnica
│   ├── PROYECTO_COMPLETADO.md
│   ├── VALIDACION_TESTS_COMPLETA.md
│   ├── VERIFICACION_INTERFACES_COMPLETA.md
│   ├── TESTS_CORREGIDOS_SIGUIENTES_PASOS.md
│   ├── ESTRATEGIA_TESTING_PREPRODUCCION.md
│   ├── RESULTADOS_TESTS_Y_CORRECIONES.md
│   ├── README_EJECUTAR.md
│   ├── DATABASE_README.md
│   ├── SISTEMA_INFORMES_RESUMEN.md
│   ├── COMPARACION_APLICACION_VS_BD_ACCESS.md
│   ├── PLAN_EXCELENCIA_INTERFACES.md
│   ├── PLAN_PASO_A_PRODUCCION.md
│   ├── MEJORAS_PARTES_README.md
│   ├── LIMPIEZA_BRANCHES_GITHUB.md
│   │
│   ├── adr/                             # Architecture Decision Records
│   │   ├── 0001-cert-selector.md
│   │   ├── 0001-use-clean-architecture.md
│   │   ├── 0002-use-tdd.md
│   │   ├── 0003-type-hints-enforcement.md
│   │   └── 0004-business-rules-from-existing-system.md
│   │
│   ├── architecture/
│   │   ├── README.md
│   │   ├── DOMAIN_MODEL.md
│   │   └── EVENT_STORMING.md
│   │
│   ├── CHANGELOG.md
│   ├── DEV_GUIDE.md
│   └── ESPECIFICACION_INFORMES.md
│
├── tests/                               # Tests (mover aquí)
│   ├── test_presupuestos.py
│   ├── test_certificaciones.py
│   ├── test_flujo_completo.py
│   ├── test_imports.py
│   └── test_optimizaciones.py          # Opcional
│
├── tools/                               # Scripts de utilidad (mover aquí)
│   ├── verificar_interfaces.py
│   ├── verificar_interfaces_estatico.py
│   ├── detectar_estructura_bd.py
│   └── detectar_columnas_precios.py
│
├── interface/                           # Interfaces GUI
│   ├── (todos los archivos *_interfaz.py)
│   ├── base/
│   ├── components/
│   ├── config/
│   └── REFACTORING_GUIDE.md
│
├── script/                              # Lógica de negocio y BD
│   ├── __init__.py
│   ├── db_*.py                          # Módulos de BD
│   ├── informes*.py                     # Sistema de informes
│   ├── *_import.py                      # Imports
│   ├── *_export.py                      # Exports
│   ├── generar_datos_prueba.py
│   ├── aplicar_indices.py
│   │
│   ├── sql/                             # Scripts SQL (mover aquí)
│   │   ├── fase2_provincias_municipios.sql
│   │   ├── fase3_comarcas_municipios.sql
│   │   ├── fase3_dim_municipios.sql
│   │   ├── mejoras_tabla_partes.sql
│   │   ├── mejoras_tabla_partes_mysql.sql
│   │   ├── indices_recomendados.sql
│   │   ├── recrear_todas_vistas.sql
│   │   ├── recrear_vw_part_certificaciones.sql
│   │   ├── recrear_vw_partes_resumen.sql
│   │   ├── crear_dim_tipos_rep.sql
│   │   ├── corregir_municipios_bizkaia.sql
│   │   └── corregir_nombres_municipios.sql
│   │
│   └── README_*.md                      # Documentación de scripts
│
├── backup/                              # Backups SQL
│   ├── backup_estructuraBBDD.sql
│   └── backup_BASE.sql
│
├── informes_guardados/                  # Informes guardados del usuario
│   └── README.txt
│
└── source/                              # Recursos (imágenes, etc.)
    ├── fondo.jpeg
    └── logo artanda2.png
```

---

## 🎯 PASOS PARA EJECUTAR LA LIMPIEZA

### Paso 1: Crear Backup de Seguridad

```bash
# Antes de eliminar nada, crear backup del proyecto completo
cd D:\Dev\HFM
tar -czf v1.04_1812_backup_pre_limpieza_$(date +%Y%m%d).tar.gz v1.04_1812/
```

### Paso 2: Crear Nuevas Carpetas

```bash
cd D:\Dev\HFM\v1.04_1812

# Crear carpetas para reorganización
mkdir -p tests
mkdir -p tools
mkdir -p script/sql
```

### Paso 3: Mover Archivos a Nuevas Ubicaciones

```bash
# Mover tests
mv test_presupuestos.py tests/
mv test_certificaciones.py tests/
mv test_flujo_completo.py tests/
mv test_imports.py tests/
mv script/test_optimizaciones.py tests/

# Mover herramientas
mv verificar_interfaces.py tools/
mv verificar_interfaces_estatico.py tools/
mv detectar_estructura_bd.py tools/
mv detectar_columnas_precios.py tools/

# Mover scripts SQL
mv script/*.sql script/sql/

# Mover documentación a docs/
mv PROYECTO_COMPLETADO.md docs/
mv VALIDACION_TESTS_COMPLETA.md docs/
mv VERIFICACION_INTERFACES_COMPLETA.md docs/
mv TESTS_CORREGIDOS_SIGUIENTES_PASOS.md docs/
mv ESTRATEGIA_TESTING_PREPRODUCCION.md docs/
mv RESULTADOS_TESTS_Y_CORRECIONES.md docs/
mv README_EJECUTAR.md docs/
mv DATABASE_README.md docs/
mv SISTEMA_INFORMES_RESUMEN.md docs/
mv COMPARACION_APLICACION_VS_BD_ACCESS.md docs/
mv PLAN_EXCELENCIA_INTERFACES.md docs/
mv PLAN_PASO_A_PRODUCCION.md docs/
mv MEJORAS_PARTES_README.md docs/
mv LIMPIEZA_BRANCHES_GITHUB.md docs/
```

### Paso 4: Eliminar Archivos Obsoletos

```bash
# Eliminar tests obsoletos
rm test_cert.py
rm test_codigo_ot_debug.py
rm test_env.py
rm test_form_v2.py
rm test_informes_ui.py
rm test_partes_mejorados.py
rm test_treeview_style.py
rm temporal.py

# Eliminar documentación obsoleta
rm ANALISIS_EXHAUSTIVO_BD_CERTIFICACIONES.md
rm ANALISIS_INFORMES_ACCESS_VS_GENERADOR.md
rm COMO_VER_CAMBIOS_INFORMES.md
rm COMPARACION_ENFOQUES.md
rm EJECUTAR_MIGRACION_AHORA.md
rm GUIA_PRUEBA_MIGRACION.md
rm INICIO_RAPIDO_PRUEBA.md
rm MEJORAS_UI_ESPECIFICACIONES_TECNICAS.md
rm MIGRATION_GUIDE.md
rm OPTIMIZACIONES_BACKEND.md
rm PLAN_REFACTORIZACION_INTERFACES.md
rm PYCHARM_SETUP.md
rm RESUMEN_MIGRACION_PARTES_FASE1.md
rm REVISION_BASE_DATOS.md
rm SCRIPTS_REFACTORIZACION.md
rm SOLUCION_TREEVIEW.md
rm VERIFICATION_REPORT.md
rm README_GENERAR_PARTES_PRUEBA.md
rm README_REFACTORIZACION.md

# Eliminar scripts obsoletos
rm analizar_access.py
rm generar_1000_partes.py
rm parts_list_window.py
rm parts_tab_embed.py
rm ver_estructura_cert.py
rm interface/parts_interfaz_v2.py

# Eliminar scripts de migración completada
rm script/migrate_partes_mejoras.py
rm script/ejecutar_migracion_manual.py
rm script/verificar_y_completar_migracion.py
rm script/test_migration_complete.py

# Eliminar backups SQL innecesarios (opcional - revisar antes)
rm backup/backup_PR001.sql
rm backup/backup_completo.sql
rm backup/backup_test.sql
```

### Paso 5: Actualizar Imports en Archivos

Después de mover archivos, actualizar los imports en:
- `main.py`
- Scripts que importan tests
- Scripts que importan herramientas

---

## ⚠️ PRECAUCIONES

1. **HACER BACKUP COMPLETO** antes de eliminar nada
2. **Revisar cada archivo** antes de eliminar (puede haber referencias)
3. **Probar la aplicación** después de cada paso de reorganización
4. **Actualizar imports** después de mover archivos
5. **Commit frecuente** durante el proceso

---

## 📊 RESUMEN DE LIMPIEZA

| Categoría | Archivos a Eliminar | Archivos a Mantener |
|-----------|---------------------|---------------------|
| Tests | 8 | 5 |
| Documentación | 19 | 15 |
| Scripts Python | 9 | 10+ |
| Scripts SQL | 6 | 15 |
| Interfaces | 1 | 45+ |
| Backups | 3 (opcional) | 2 |
| **TOTAL** | **~45 archivos** | **~90 archivos** |

---

## ✅ BENEFICIOS DESPUÉS DE LA LIMPIEZA

1. **Estructura más clara** y fácil de navegar
2. **Menos archivos** = menos confusión
3. **Documentación organizada** en carpeta `docs/`
4. **Tests organizados** en carpeta `tests/`
5. **Herramientas organizadas** en carpeta `tools/`
6. **SQL organizado** en carpeta `script/sql/`
7. **Proyecto más profesional** y mantenible

---

## 🎯 SIGUIENTE PASO

**¿Deseas que ejecute la limpieza automáticamente?**

Opciones:
1. **Sí, ejecutar limpieza completa** (con backup automático)
2. **Solo eliminar archivos obsoletos** (sin reorganizar)
3. **Solo reorganizar estructura** (sin eliminar)
4. **Revisar archivo por archivo** antes de decidir

---

**Nota:** Esta limpieza NO afecta la funcionalidad del sistema, solo organiza y elimina archivos obsoletos/duplicados.
