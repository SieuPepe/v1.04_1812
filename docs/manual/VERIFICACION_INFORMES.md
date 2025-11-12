# Verificación del Sistema de Informes - HydroFlow Manager

## 📊 Estado Actual del Sistema de Informes

### Archivos del Sistema

```
script/
├── informes.py                    # Lógica principal de generación
├── informes_config.py             # Definiciones de informes
├── informes_header_config.py      # Configuración de cabeceras
├── informes_storage.py            # Almacenamiento de configuraciones
└── informes_exportacion.py        # Exportación a Excel/PDF

interface/
└── informes_interfaz.py           # Interfaz gráfica
```

### Categorías de Informes Disponibles

1. **📊 Partes**
   - Listado de Partes

2. **📦 Recursos**
   - Listado de Partidas del Presupuesto
   - Consumo de Recursos
   - Trabajos por Actuación

3. **💰 Presupuestos**
   - Contrato
   - Presupuesto Detallado
   - Presupuesto Resumen

4. **✅ Certificaciones**
   - Certificación Detallado
   - Certificación Resumen

5. **📅 Planificación**
   - Informe de Avance

---

## ✅ Características Implementadas

### 1. Sistema Flexible de Definición de Informes

**Archivo**: `script/informes_config.py`

Cada informe se define con:
- **Tabla principal**: Tabla base del informe
- **Campos disponibles**: Con tipo, fórmulas SQL, formato
- **Filtros**: Operadores y valores permitidos
- **Ordenaciones**: Campos por los que se puede ordenar
- **Agrupaciones**: GROUP BY visual con múltiples niveles
- **Agregaciones**: Funciones COUNT, SUM, AVG, MIN, MAX

**Ejemplo de definición**:
```python
"Listado de Partes": {
    "categoria": "📊 Partes",
    "tabla_principal": "tbl_partes",
    "campos": {
        "codigo": {
            "nombre": "Código",
            "tipo": "texto",
            "columna_bd": "codigo",
            "grupo": "Información Básica"
        },
        "presupuesto": {
            "nombre": "Presupuesto",
            "tipo": "calculado",
            "formula": "COALESCE((SELECT SUM(...)))",
            "formato": "moneda",
            "grupo": "Económico"
        }
    }
}
```

### 2. Detección Automática de Columnas

**Archivo**: `script/informes.py` (líneas 11-73)

- Detecta automáticamente qué columna usar para dimensiones
- Busca por nombres comunes (nombre, descripcion, etc.)
- Fallback inteligente si no encuentra

### 3. Construcción Dinámica de Queries

**Funciones principales**:
- `build_filter_condition()`: Construye condiciones SQL para filtros
- `build_query()`: Construye query completo con filtros, ordenaciones y agrupaciones

### 4. Soporte para Agrupaciones (GROUP BY)

**Características**:
- Agrupación visual por múltiples campos
- Subtotales por grupo
- Total general
- Hasta 3 niveles de agrupación

---

## ⚠️ Aspectos a Verificar Antes de Fase 3

### 1. **Queries de Campos Calculados**

**Archivo**: `script/informes_config.py`

**¿Qué verificar?**:
- ¿Las fórmulas SQL son correctas?
- ¿Las subconsultas funcionan con datos reales?
- ¿Los JOIN están completos?

**Ejemplo de campo que debe verificarse**:
```python
"presupuesto": {
    "formula": "COALESCE((SELECT SUM(pp.cantidad * pp.precio_unit) FROM tbl_part_presupuesto pp WHERE pp.parte_id = p.id), 0)"
}
```

**Cómo probar**:
```sql
-- Ejecutar directamente en MySQL para verificar
SELECT
    p.id,
    p.codigo,
    COALESCE((SELECT SUM(pp.cantidad * pp.precio_unit)
              FROM tbl_part_presupuesto pp
              WHERE pp.parte_id = p.id), 0) as presupuesto
FROM tbl_partes p
LIMIT 10;
```

### 2. **Tablas de Dimensiones**

**Archivo**: `script/informes_config.py` (líneas 88-125)

**¿Qué verificar?**:
- ¿Existen todas las tablas de dimensión referenciadas?
- ¿Los nombres de columnas coinciden?

**Tablas referenciadas**:
- `dim_red`
- `dim_tipo_trabajo`
- `dim_codigo_trabajo`
- `dim_provincias`
- `dim_comarcas`
- `dim_municipios`
- `dim_tipos_rep`
- `tbl_pres_capitulos`
- `tbl_pres_unidades`
- `tbl_pres_naturaleza`

**Cómo verificar**:
```sql
-- Verificar que existen las tablas
SHOW TABLES LIKE 'dim_%';
SHOW TABLES LIKE 'tbl_pres_%';

-- Verificar columnas de cada tabla
DESCRIBE dim_red;
DESCRIBE dim_tipo_trabajo;
-- etc...
```

### 3. **Relaciones entre Tablas**

**¿Qué verificar?**:
- ¿Los campos ID existen en ambas tablas?
- ¿Los tipos de datos coinciden?
- ¿Hay Foreign Keys configuradas?

**Relaciones críticas**:
```
tbl_partes.red_id → dim_red.id
tbl_partes.tipo_trabajo_id → dim_tipo_trabajo.id
tbl_partes.cod_trabajo_id → dim_codigo_trabajo.id
tbl_partes.municipio_id → dim_municipios.id
tbl_part_presupuesto.parte_id → tbl_partes.id
tbl_part_presupuesto.precio_id → tbl_pres_precios.id
```

**Cómo verificar**:
```sql
-- Verificar Foreign Keys
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'cert_dev'
  AND REFERENCED_TABLE_NAME IS NOT NULL;
```

### 4. **Formato de Fechas**

**¿Qué verificar?**:
- ¿Las columnas de fecha son tipo DATE/DATETIME?
- ¿Las fórmulas DATE_FORMAT funcionan correctamente?

**Campos con fechas**:
```python
"mes": {
    "formula": "DATE_FORMAT(p.fecha_inicio, '%Y-%m')"
},
"año": {
    "formula": "YEAR(p.fecha_inicio)"
}
```

**Cómo probar**:
```sql
SELECT
    fecha_inicio,
    DATE_FORMAT(fecha_inicio, '%Y-%m') as mes,
    YEAR(fecha_inicio) as año
FROM tbl_partes
WHERE fecha_inicio IS NOT NULL
LIMIT 10;
```

### 5. **Agrupaciones (GROUP BY)**

**Archivo**: `script/informes_config.py` (líneas 345-366)

**¿Qué verificar?**:
- ¿Los campos de agrupación son compatibles?
- ¿Las agregaciones funcionan correctamente?

**Ejemplo a probar**:
```sql
-- Agrupar partes por mes y estado
SELECT
    DATE_FORMAT(p.fecha_inicio, '%Y-%m') as mes,
    p.estado,
    COUNT(*) as total_partes,
    SUM(COALESCE((SELECT SUM(pp.cantidad * pp.precio_unit)
                  FROM tbl_part_presupuesto pp
                  WHERE pp.parte_id = p.id), 0)) as total_presupuesto
FROM tbl_partes p
WHERE p.fecha_inicio IS NOT NULL
GROUP BY DATE_FORMAT(p.fecha_inicio, '%Y-%m'), p.estado
ORDER BY mes, estado;
```

---

## 🔍 Lista de Verificación Práctica

### Paso 1: Verificar Estructura de Base de Datos

```bash
# Ejecutar script de verificación
python script/verificar_esquemas.py
```

Verificar manualmente:
```sql
USE cert_dev;

-- 1. Verificar tablas principales
SHOW TABLES;

-- 2. Verificar columnas de tbl_partes
DESCRIBE tbl_partes;

-- 3. Verificar dimensiones
DESCRIBE dim_red;
DESCRIBE dim_tipo_trabajo;
DESCRIBE dim_codigo_trabajo;
DESCRIBE dim_municipios;

-- 4. Verificar tablas de presupuesto
DESCRIBE tbl_part_presupuesto;
DESCRIBE tbl_pres_precios;
```

### Paso 2: Probar Queries de Informes

```sql
-- Test 1: Listado básico de partes con presupuesto
SELECT
    p.id,
    p.codigo,
    p.descripcion,
    p.estado,
    COALESCE((SELECT SUM(pp.cantidad * pp.precio_unit)
              FROM tbl_part_presupuesto pp
              WHERE pp.parte_id = p.id), 0) as presupuesto
FROM tbl_partes p
LIMIT 10;

-- Test 2: Partes con dimensiones
SELECT
    p.id,
    p.codigo,
    r.descripcion as red,
    tt.descripcion as tipo_trabajo,
    m.nombre as municipio
FROM tbl_partes p
LEFT JOIN dim_red r ON p.red_id = r.id
LEFT JOIN dim_tipo_trabajo tt ON p.tipo_trabajo_id = tt.id
LEFT JOIN dim_municipios m ON p.municipio_id = m.id
LIMIT 10;

-- Test 3: Agrupación por mes
SELECT
    DATE_FORMAT(p.fecha_inicio, '%Y-%m') as mes,
    COUNT(*) as num_partes,
    SUM(COALESCE((SELECT SUM(pp.cantidad * pp.precio_unit)
                  FROM tbl_part_presupuesto pp
                  WHERE pp.parte_id = p.id), 0)) as total_presupuesto
FROM tbl_partes p
WHERE p.fecha_inicio IS NOT NULL
GROUP BY DATE_FORMAT(p.fecha_inicio, '%Y-%m')
ORDER BY mes;
```

### Paso 3: Probar en la Interfaz

```bash
# Ejecutar aplicación
python main.py

# O ejecutar ejecutable
./HidroFlowManager.exe
```

**Operaciones a probar**:
1. ✅ Acceder al módulo de Informes
2. ✅ Seleccionar "Listado de Partes"
3. ✅ Aplicar filtros (por estado, fecha, etc.)
4. ✅ Agregar ordenación
5. ✅ Probar agrupación (por mes, estado, etc.)
6. ✅ Exportar a Excel
7. ✅ Exportar a PDF
8. ✅ Verificar totales y subtotales

### Paso 4: Verificar Exportación

**Excel**:
- ✅ Se exportan todos los campos
- ✅ Formato de números correcto (€, decimales)
- ✅ Totales al final
- ✅ Subtotales por grupo (si hay agrupación)

**PDF**:
- ✅ Cabecera con logo empresa
- ✅ Datos del proyecto
- ✅ Contenido completo
- ✅ Paginación correcta
- ✅ Totales visibles

---

## 📝 Posibles Modificaciones Necesarias

### 1. Agregar/Modificar Campos Calculados

**Ubicación**: `script/informes_config.py`

Si necesita agregar un nuevo campo calculado:
```python
"nuevo_campo": {
    "nombre": "Nombre Visible",
    "tipo": "calculado",
    "formula": "COALESCE((SELECT ... FROM ... WHERE ...), 0)",
    "formato": "moneda",  # o "decimal", "entero", "porcentaje"
    "grupo": "Económico"
}
```

### 2. Agregar Nuevos Filtros

```python
"filtros": {
    "nuevo_filtro": {
        "campo": "nombre_campo",
        "tipo": "select_bd",  # o "texto", "numerico", "fecha", "booleano"
        "operadores": ["Igual a", "Diferente de"],
        "tabla": "dim_tabla"  # si es select_bd
    }
}
```

### 3. Agregar Nuevos Informes

```python
"Nuevo Informe": {
    "categoria": "📊 Categoría",
    "descripcion": "Descripción del informe",
    "tabla_principal": "tbl_nombre",
    "campos": { ... },
    "filtros": { ... },
    "ordenaciones": [ ... ],
    "agrupaciones": { ... },
    "campos_default": [ ... ]
}
```

### 4. Modificar Formato de Exportación

**Ubicación**: `script/informes_exportacion.py`

- Cambiar colores de cabeceras
- Modificar formato de moneda
- Ajustar ancho de columnas
- Cambiar fuentes y tamaños

---

## 🐛 Errores Comunes y Soluciones

### Error: "Column 'X' not found"

**Causa**: Campo referenciado no existe en la tabla
**Solución**:
1. Verificar esquema de la tabla: `DESCRIBE tabla_nombre`
2. Actualizar definición en `informes_config.py`

### Error: "Unknown table 'dim_X'"

**Causa**: Tabla de dimensión no existe
**Solución**:
1. Verificar: `SHOW TABLES LIKE 'dim_%'`
2. Crear tabla faltante o actualizar configuración

### Error: "Invalid use of group function"

**Causa**: Función de agregación usada sin GROUP BY
**Solución**: Verificar que todos los campos no agregados estén en GROUP BY

### Error: Datos no coinciden con lo esperado

**Causa**: Joins incorrectos o filtros mal aplicados
**Solución**: Ejecutar query manualmente en MySQL para depurar

---

## 📋 Checklist Final

Antes de continuar con Fase 3, verificar:

- [ ] Todas las tablas de dimensión existen
- [ ] Todos los campos calculados funcionan
- [ ] Filtros se aplican correctamente
- [ ] Ordenación funciona
- [ ] Agrupaciones muestran subtotales
- [ ] Exportación a Excel funciona
- [ ] Exportación a PDF funciona
- [ ] Totales son correctos
- [ ] Formato de moneda es correcto (€)
- [ ] Fechas se muestran correctamente
- [ ] No hay errores SQL en logs

---

## 📞 Próximos Pasos

Una vez verificado todo:

1. **Documentar cambios necesarios**: Crear lista de modificaciones
2. **Implementar modificaciones**: Actualizar `informes_config.py`
3. **Probar nuevamente**: Ejecutar checklist completo
4. **Continuar con Fase 3**: Una vez todo funcione correctamente

---

## 📝 Notas

- Los informes usan queries SQL dinámicos generados en tiempo de ejecución
- Cualquier cambio en estructura de BD requiere actualizar `informes_config.py`
- El sistema es flexible y permite agregar nuevos informes fácilmente
- La detección automática de columnas facilita el mantenimiento
