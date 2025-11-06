# ESTRATEGIA DE TESTING PRE-PRODUCCIÓN
## HydroFlow Manager v1.04

**Documento creado:** 2025-11-05
**Estado:** Pendiente de ejecución

---

## 📋 RESUMEN EJECUTIVO

Este documento lista todos los tests que DEBEN ejecutarse antes de pasar el software a producción.

**IMPORTANTE:** Todos estos tests requieren:
- MySQL 8.0+ instalado y configurado
- Dependencias Python instaladas (`pip install -r requirements.txt`)
- Archivo `.env` configurado con credenciales de BD
- Base de datos con datos de prueba

---

## 🎯 TESTS EXISTENTES A EJECUTAR

### **1. Tests de Configuración y Conexión**

#### `test_env.py`
**Propósito:** Verificar configuración .env y conexión a MySQL
**Ejecutar:** `python test_env.py`
**Valida:**
- Archivo .env existe y está configurado
- python-dotenv instalado
- Variables de entorno cargadas correctamente
- Conexión exitosa a MySQL
- Versión de MySQL

**Tiempo estimado:** 1 minuto

---

#### `test_imports.py`
**Propósito:** Verificar que todos los módulos se importan correctamente
**Ejecutar:** `python test_imports.py`
**Valida:**
- Módulos base (db_config, db_connection)
- Configuración cargada correctamente
- Compatibilidad con modulo_db
- mysql.connector instalado
- Funciones clave disponibles
- Variables de entorno

**Resultado esperado:** 6/6 pruebas pasadas
**Tiempo estimado:** 2 minutos

---

### **2. Tests de Funcionalidad de Partes**

#### `test_partes_mejorados.py`
**Propósito:** Test completo del ciclo de vida de partes
**Ejecutar:** `python test_partes_mejorados.py`
**Valida:**
- Obtener estados disponibles
- Crear parte nuevo con campos mejorados
- Modificar parte existente
- Finalizar parte (cambio de estado)
- Listar partes con campos mejorados
- Verificar parte en vista vw_partes_completo

**⚠️ NOTA:** Este script tiene credenciales hardcodeadas que DEBEN cambiarse antes de ejecutar:
```python
USER = 'root'
PASSWORD = 'NuevaPass!2025'  # ⚠️ CAMBIAR
SCHEMA = 'cert_dev'           # ⚠️ CAMBIAR
```

**Resultado esperado:** 6 tests completados exitosamente
**Tiempo estimado:** 3-5 minutos

---

### **3. Tests de Optimizaciones de Backend**

#### `script/test_optimizaciones.py`
**Propósito:** Verificar optimizaciones de rendimiento
**Ejecutar:** `python script/test_optimizaciones.py --user <user> --password <pass> --schema <schema>`
**Valida:**
- Rendimiento de funciones con caché LRU
- Integridad de transacciones con rollback
- Funcionamiento correcto de logging
- Comparación de tiempos antes/después

**Resultado esperado:** Mejoras de rendimiento visibles (reducción ~90% en llamadas con caché)
**Tiempo estimado:** 10-15 minutos

---

### **4. Tests de Migración**

#### `script/test_migration_complete.py`
**Propósito:** Verificar migración completa de datos desde Access
**Ejecutar:** `python script/test_migration_complete.py`
**Valida:**
- Migración completa de partes históricos
- Integridad de datos migrados
- Referencias correctas entre tablas
- Validación de fechas y estados

**⚠️ CRÍTICO:** Ejecutar ANTES de producción para verificar que todos los datos históricos se migraron correctamente

**Tiempo estimado:** 5-10 minutos

---

### **5. Tests de Diagnóstico**

#### `diagnostico_informes.py`
**Propósito:** Verificar que el módulo de informes funciona correctamente
**Ejecutar:** `python diagnostico_informes.py`
**Valida:**
- Datos en tbl_partes
- Query SQL del informe se genera correctamente
- Dimensiones geográficas funcionan
- JOINs con tablas de dimensión correctos
- Informe devuelve resultados

**⚠️ NOTA:** Cambiar credenciales hardcodeadas antes de ejecutar:
```python
USER = "root"
PASSWORD = "NuevaPass!2025"  # ⚠️ CAMBIAR
SCHEMA = "HFM"                # ⚠️ CAMBIAR
```

**Tiempo estimado:** 3-5 minutos

---

#### `diagnostico_dim_geograficas.py`
**Propósito:** Verificar dimensiones geográficas (provincias, comarcas, municipios)
**Ejecutar:** `python diagnostico_dim_geograficas.py`
**Valida:**
- Tablas de dimensión existen
- Datos geográficos cargados correctamente
- Referencias entre provincia → comarca → municipio
- Nomenclatura de columnas correcta

**Tiempo estimado:** 2-3 minutos

---

#### `diagnostico_interfaz.py`
**Propósito:** Verificar estado de interfaces gráficas
**Ejecutar:** `python diagnostico_interfaz.py`
**Valida:**
- CustomTkinter instalado
- Iconos y recursos existen
- Ventanas se pueden crear sin errores

**Tiempo estimado:** 2-3 minutos

---

### **6. Scripts de Generación de Datos de Prueba**

#### `generar_1000_partes.py`
**Propósito:** Generar 1000 partes de prueba para testing de rendimiento
**Ejecutar:** `python generar_1000_partes.py`
**Uso:** Testing de rendimiento con volúmenes grandes

**⚠️ SOLO EJECUTAR EN AMBIENTE DE DESARROLLO**

**Tiempo estimado:** 10-20 minutos

---

## 🆕 TESTS ADICIONALES RECOMENDADOS

### **7. Tests de Módulos Principales**

#### `test_presupuestos.py` (CREAR)
**Propósito:** Verificar funcionalidad de presupuestos
**Debe validar:**
- Crear presupuesto desde catálogo
- Modificar cantidades y precios
- Calcular totales correctamente
- Vincular con parte
- Exportar presupuesto

**Tiempo estimado:** 5-10 minutos

---

#### `test_certificaciones.py` (CREAR)
**Propósito:** Verificar funcionalidad de certificaciones
**Debe validar:**
- Crear certificación desde presupuesto
- Marcar conceptos como certificados
- Calcular pendiente correctamente
- Certificación por lotes
- Exportar certificación

**Tiempo estimado:** 5-10 minutos

---

#### `test_informes_completo.py` (CREAR)
**Propósito:** Test exhaustivo del módulo de informes
**Debe validar:**
- Crear informe básico (todos los campos)
- Aplicar filtros simples (Igual a, Mayor que, etc.)
- Aplicar filtro "Entre" con fechas (DateEntry)
- Aplicar filtro "Entre" con números
- Lógica AND/OR entre filtros
- Clasificaciones (ordenamiento)
- Verificar totalizadores (sumas)
- Vista previa en pantalla
- Exportar a Excel
- Exportar a Word
- Exportar a PDF
- Guardar configuración de informe
- Cargar configuración guardada
- Eliminar configuración
- Probar con dimensiones geográficas (comarca, municipio)

**⚠️ CRÍTICO:** Este es el módulo NUEVO de v1.04, requiere testing exhaustivo

**Tiempo estimado:** 30-45 minutos

---

### **8. Tests de Integración**

#### `test_flujo_completo.py` (CREAR)
**Propósito:** Test del flujo completo de trabajo
**Debe validar:**
- Crear parte nuevo
- Agregar presupuesto al parte
- Generar certificación del presupuesto
- Generar informe con este parte
- Verificar datos en cada paso
- Eliminar datos de prueba

**⚠️ CRÍTICO:** Este test valida el flujo end-to-end del sistema

**Tiempo estimado:** 15-20 minutos

---

#### `test_performance.py` (CREAR)
**Propósito:** Test de rendimiento con datos reales
**Debe validar:**
- Cargar informes con grandes volúmenes (1000+ partes)
- Medir tiempo de respuesta
- Verificar uso de memoria
- Testing de exportación de informes grandes (>500 registros)
- Verificar que no se cuelgue la aplicación

**Tiempo estimado:** 20-30 minutos

---

### **9. Tests de UI/UX**

#### `test_ui_completo.py` (CREAR)
**Propósito:** Verificar aspectos visuales y de usabilidad
**Debe validar:**
- Todos los iconos cargan correctamente
- Responsive (redimensionamiento de ventanas)
- Ventanas modales aparecen al frente
- Navegación entre módulos funciona
- Mensajes de error son claros y útiles
- Campos obligatorios se validan
- Botones disabled/enabled correctamente

**Tiempo estimado:** 20-30 minutos

---

## 📊 RESUMEN DE TIEMPOS

| Categoría | Tests | Tiempo Estimado |
|-----------|-------|-----------------|
| **Existentes** | 7 tests | 40-55 minutos |
| **A Crear** | 5 tests | 90-135 minutos |
| **TOTAL** | 12 tests | **130-190 minutos** |
| **Días laborables (8h)** | | **0.5-1 día** |

---

## ⚠️ ELEMENTOS CRÍTICOS ANTES DE PRODUCCIÓN

### 🔴 **OBLIGATORIO**

1. ✅ **test_env.py** - Conexión a BD funciona
2. ✅ **test_imports.py** - Todos los módulos se importan
3. ✅ **test_migration_complete.py** - Datos históricos migrados
4. ✅ **diagnostico_informes.py** - Módulo de informes funciona
5. ✅ **test_informes_completo.py** (CREAR) - Testing exhaustivo de informes
6. ✅ **test_flujo_completo.py** (CREAR) - Flujo end-to-end funciona

### 🟠 **RECOMENDADO**

7. test_partes_mejorados.py
8. test_optimizaciones.py
9. diagnostico_dim_geograficas.py
10. test_presupuestos.py (CREAR)
11. test_certificaciones.py (CREAR)

### 🟡 **OPCIONAL**

12. test_performance.py (CREAR)
13. test_ui_completo.py (CREAR)

---

## 🚨 ADVERTENCIAS IMPORTANTES

### **Credenciales Hardcodeadas**

Los siguientes archivos tienen credenciales hardcodeadas que DEBEN cambiarse antes de ejecutar:

- `test_partes_mejorados.py`: líneas 18-20
- `diagnostico_informes.py`: líneas 11-13

**Cambiar por:**
```python
import os
USER = os.getenv('DB_USER', 'root')
PASSWORD = os.getenv('DB_PASSWORD')
SCHEMA = os.getenv('DB_EXAMPLE_SCHEMA', 'proyecto_tipo')
```

---

### **Requisitos Previos**

Antes de ejecutar CUALQUIER test:

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Crear archivo .env:
   ```bash
   cp .env.example .env
   # Editar .env con tus valores
   ```

3. Verificar MySQL corriendo:
   ```bash
   mysql -u root -p -e "SELECT VERSION();"
   ```

4. Verificar esquemas existen:
   ```bash
   mysql -u root -p -e "SHOW DATABASES LIKE 'manager';"
   mysql -u root -p -e "SHOW DATABASES LIKE 'proyecto_tipo';"
   ```

---

## 📝 CHECKLIST DE EJECUCIÓN

Usar esta checklist al ejecutar los tests:

### **Pre-Testing**
- [ ] MySQL 8.0+ instalado y corriendo
- [ ] Dependencias Python instaladas
- [ ] Archivo .env configurado
- [ ] Credenciales hardcodeadas cambiadas
- [ ] Base de datos con datos de prueba

### **Tests Obligatorios**
- [ ] test_env.py ejecutado ✅
- [ ] test_imports.py ejecutado ✅
- [ ] test_migration_complete.py ejecutado ✅
- [ ] diagnostico_informes.py ejecutado ✅
- [ ] test_informes_completo.py creado y ejecutado ✅
- [ ] test_flujo_completo.py creado y ejecutado ✅

### **Tests Recomendados**
- [ ] test_partes_mejorados.py ejecutado ✅
- [ ] test_optimizaciones.py ejecutado ✅
- [ ] diagnostico_dim_geograficas.py ejecutado ✅
- [ ] test_presupuestos.py creado y ejecutado ✅
- [ ] test_certificaciones.py creado y ejecutado ✅

### **Tests Opcionales**
- [ ] test_performance.py creado y ejecutado ✅
- [ ] test_ui_completo.py creado y ejecutado ✅

### **Post-Testing**
- [ ] Todos los tests pasaron
- [ ] Errores corregidos
- [ ] Documentación actualizada
- [ ] Código listo para producción

---

## 📄 GENERACIÓN DE REPORTE

Después de ejecutar todos los tests, generar un reporte:

```bash
# Crear directorio de reportes
mkdir -p test_reports

# Ejecutar tests y guardar salida
python test_env.py > test_reports/test_env_report.txt 2>&1
python test_imports.py > test_reports/test_imports_report.txt 2>&1
# ... etc para cada test

# Generar reporte consolidado
cat test_reports/*.txt > test_reports/REPORTE_FINAL_TESTING.txt
```

---

**Última actualización:** 2025-11-05
**Estado:** Documento creado - Pendiente ejecución de tests
**Próximo paso:** Ejecutar tests en ambiente con BD configurada
