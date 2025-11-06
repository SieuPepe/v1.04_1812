# DISEÑO: Sistema de Agrupación (GROUP BY) para Informes
## HydroFlow Manager v1.04

**Fecha:** 2025-11-06
**Estado:** 🎯 DISEÑO EN REVISIÓN
**Funcionalidad:** Agrupación de datos similar a GROUP BY de SQL

---

## 📋 RESUMEN EJECUTIVO

Se añadirá funcionalidad de **agrupación** (GROUP BY) al sistema de informes, permitiendo:
- Agrupar datos por uno o múltiples campos
- Aplicar funciones de agregación (COUNT, SUM, AVG, MIN, MAX)
- Combinar agrupación con filtros y ordenamiento existentes
- Generar informes tipo resumen/consolidado

---

## 🎯 OBJETIVO

Permitir al usuario generar informes agrupados como:

### Ejemplo 1: Total presupuestado por provincia
```
Provincia       | Total Presupuesto | Nº Partes
----------------|-------------------|----------
Álava           | 125,450.00 €     | 15
Bizkaia         | 342,780.50 €     | 28
Gipuzkoa        | 198,320.75 €     | 21
```

### Ejemplo 2: Promedio certificado por Red y Estado
```
Red      | Estado     | Avg Certificado | Count
---------|------------|-----------------|------
AT       | Finalizado | 12,340.50 €    | 8
AT       | En curso   | 8,920.00 €     | 5
BT       | Finalizado | 5,120.30 €     | 12
```

### Ejemplo 3: Total pendiente por Tipo de Trabajo
```
Tipo de Trabajo | Total Pendiente | Max Pendiente | Min Pendiente
----------------|-----------------|---------------|---------------
Reparación      | 45,230.00 €    | 12,000.00 €  | 1,200.00 €
Mantenimiento   | 23,450.00 €    | 8,500.00 €   | 500.00 €
Instalación     | 67,890.00 €    | 25,000.00 €  | 3,400.00 €
```

---

## 🏗️ ARQUITECTURA DEL SISTEMA

### 1. Componentes a Modificar

```
script/
├── informes_config.py          ← Añadir config de agrupación
├── informes.py                 ← Modificar build_query() y ejecutar_informe()
└── informes_storage.py         ← Guardar configuraciones de agrupación

interface/
└── informes_interfaz.py        ← Añadir UI de agrupación

tests/
└── test_agrupacion_informes.py ← Crear tests nuevos
```

### 2. Flujo de Datos

```
┌──────────────────────────────────────────────────┐
│ INTERFAZ (informes_interfaz.py)                  │
│                                                   │
│ Usuario selecciona:                               │
│ - Campos de agrupación: [provincia, red]         │
│ - Campos agregados:                               │
│     * presupuesto → SUM                           │
│     * certificado → AVG                           │
│     * codigo → COUNT                              │
└───────────────────┬──────────────────────────────┘
                    │
                    ↓
┌──────────────────────────────────────────────────┐
│ LÓGICA (informes.py)                             │
│                                                   │
│ build_query() genera:                             │
│                                                   │
│ SELECT                                            │
│   provincia_dim.nombre AS provincia,              │
│   red_dim.descripcion AS red,                     │
│   SUM(presupuesto_formula) AS presupuesto_total,  │
│   AVG(certificado_formula) AS certificado_avg,    │
│   COUNT(p.id) AS num_partes                       │
│ FROM schema.tbl_partes p                          │
│ LEFT JOIN schema.dim_provincias provincia_dim     │
│   ON p.provincia_id = provincia_dim.id            │
│ LEFT JOIN schema.dim_red red_dim                  │
│   ON p.red_id = red_dim.id                        │
│ WHERE [filtros aplicados]                         │
│ GROUP BY provincia_dim.nombre, red_dim.descripcion│
│ ORDER BY [clasificaciones aplicadas]              │
└───────────────────┬──────────────────────────────┘
                    │
                    ↓
┌──────────────────────────────────────────────────┐
│ BASE DE DATOS (MySQL)                            │
│                                                   │
│ Ejecuta query GROUP BY                            │
│ Retorna datos agrupados                           │
└──────────────────────────────────────────────────┘
```

---

## 📊 ESPECIFICACIÓN TÉCNICA

### 1. Estructura de Datos de Agrupación

```python
# Estructura para definir una agrupación
agrupaciones = [
    {
        'campo': 'provincia',           # Campo por el que agrupar
        'tipo': 'dimension'              # tipo del campo (dimension, texto, fecha)
    },
    {
        'campo': 'red',
        'tipo': 'dimension'
    }
]

# Estructura para definir agregaciones
agregaciones = [
    {
        'campo': 'presupuesto',         # Campo a agregar
        'funcion': 'SUM',                # Función de agregación
        'alias': 'total_presupuesto'     # Nombre en resultado
    },
    {
        'campo': 'certificado',
        'funcion': 'AVG',
        'alias': 'promedio_certificado'
    },
    {
        'campo': 'codigo',              # Contar registros
        'funcion': 'COUNT',
        'alias': 'num_partes'
    }
]
```

### 2. Funciones de Agregación Soportadas

| Función | Descripción | Aplicable a |
|---------|-------------|-------------|
| **COUNT** | Contar registros | Todos los campos |
| **SUM** | Suma total | Campos numéricos, moneda, calculados |
| **AVG** | Promedio | Campos numéricos, moneda, calculados |
| **MIN** | Valor mínimo | Campos numéricos, moneda, fechas |
| **MAX** | Valor máximo | Campos numéricos, moneda, fechas |
| **COUNT DISTINCT** | Contar valores únicos | Todos los campos |

### 3. Campos Agrupables

**Todos los campos pueden usarse para agrupar**, pero los más comunes serán:

#### Dimensiones (más usadas):
- `estado` - Agrupar por estado del parte
- `red` - Agrupar por tipo de red
- `tipo_trabajo` - Agrupar por tipo de trabajo
- `codigo_trabajo` - Agrupar por código de trabajo
- `provincia` - Agrupar por provincia
- `comarca` - Agrupar por comarca
- `municipio` - Agrupar por municipio
- `tipo_rep` - Agrupar por tipo de reparación

#### Fechas (con diferentes granularidades):
- `fecha_inicio` - Por fecha completa, año, mes, año-mes
- `fecha_fin` - Por fecha completa, año, mes, año-mes
- `creado_en` - Por fecha de creación
- `actualizado_en` - Por fecha de actualización

#### Texto:
- `finalizada` - Sí/No
- `localizacion` - Por localización

### 4. Campos Agregables

**Solo campos numéricos y calculados** pueden agregarse con SUM/AVG/MIN/MAX:

- `presupuesto` - Campo calculado (totalizable)
- `certificado` - Campo calculado (totalizable)
- `pendiente` - Campo calculado (totalizable)
- `latitud` - Numérico (AVG para centro geográfico)
- `longitud` - Numérico (AVG para centro geográfico)

**COUNT** puede aplicarse a cualquier campo.

---

## 🖥️ DISEÑO DE INTERFAZ

### Ubicación: Panel derecho de informes, nueva pestaña "Agrupación"

```
┌─────────────────────────────────────────────────────────────┐
│ [Filtros] [Clasificación] [📊 Agrupación] [Campos] [Config] │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ ┌─── AGRUPAR POR ────────────────────────────────────────┐   │
│ │                                                         │   │
│ │ ┌─ Campo 1 ────────────────────────────────────────┐   │   │
│ │ │ Campo: [Provincia ▼]              [🗑️ Quitar]    │   │   │
│ │ └─────────────────────────────────────────────────┘   │   │
│ │                                                         │   │
│ │ ┌─ Campo 2 ────────────────────────────────────────┐   │   │
│ │ │ Campo: [Red ▼]                    [🗑️ Quitar]    │   │   │
│ │ └─────────────────────────────────────────────────┘   │   │
│ │                                                         │   │
│ │                 [➕ Añadir Campo de Agrupación]         │   │
│ │                                                         │   │
│ └─────────────────────────────────────────────────────────┘   │
│                                                               │
│ ┌─── AGREGAR (FUNCIONES) ───────────────────────────────┐   │
│ │                                                         │   │
│ │ ┌─ Agregación 1 ──────────────────────────────────┐   │   │
│ │ │ Campo: [Presupuesto ▼]   Función: [SUM ▼]       │   │   │
│ │ │ Alias: [total_presupuesto     ]  [🗑️ Quitar]    │   │   │
│ │ └─────────────────────────────────────────────────┘   │   │
│ │                                                         │   │
│ │ ┌─ Agregación 2 ──────────────────────────────────┐   │   │
│ │ │ Campo: [Certificado ▼]   Función: [AVG ▼]       │   │   │
│ │ │ Alias: [promedio_certificado]  [🗑️ Quitar]      │   │   │
│ │ └─────────────────────────────────────────────────┘   │   │
│ │                                                         │   │
│ │ ┌─ Agregación 3 ──────────────────────────────────┐   │   │
│ │ │ Campo: [Código ▼]        Función: [COUNT ▼]     │   │   │
│ │ │ Alias: [num_partes       ]     [🗑️ Quitar]      │   │   │
│ │ └─────────────────────────────────────────────────┘   │   │
│ │                                                         │   │
│ │                 [➕ Añadir Agregación]                  │   │
│ │                                                         │   │
│ └─────────────────────────────────────────────────────────┘   │
│                                                               │
│ ⚠️ Nota: Cuando se aplica agrupación, solo se muestran      │
│    campos agrupados y campos con funciones de agregación.   │
│                                                               │
│            [🗑️ Limpiar Agrupación]                           │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Validaciones UI:

1. **Si hay agrupación activa**:
   - Solo se pueden seleccionar en "Campos a mostrar":
     * Campos incluidos en "Agrupar por"
     * Campos incluidos en "Agregar (funciones)"

2. **Si NO hay agrupación**:
   - Funciona como hasta ahora (mostrar cualquier campo)

3. **Función según tipo de campo**:
   - Numéricos/Moneda/Calculados: SUM, AVG, MIN, MAX, COUNT
   - Dimensiones/Texto: COUNT, COUNT DISTINCT
   - Fechas: MIN, MAX, COUNT

---

## 🔧 IMPLEMENTACIÓN TÉCNICA

### 1. Modificar `informes_config.py`

```python
# Añadir funciones de agregación disponibles
FUNCIONES_AGREGACION = {
    'COUNT': {
        'nombre': 'Contar',
        'descripcion': 'Cuenta el número de registros',
        'aplicable_a': ['todos']
    },
    'COUNT_DISTINCT': {
        'nombre': 'Contar únicos',
        'descripcion': 'Cuenta valores únicos',
        'aplicable_a': ['todos']
    },
    'SUM': {
        'nombre': 'Suma',
        'descripcion': 'Suma todos los valores',
        'aplicable_a': ['numerico', 'moneda', 'calculado']
    },
    'AVG': {
        'nombre': 'Promedio',
        'descripcion': 'Calcula el promedio',
        'aplicable_a': ['numerico', 'moneda', 'calculado']
    },
    'MIN': {
        'nombre': 'Mínimo',
        'descripcion': 'Encuentra el valor mínimo',
        'aplicable_a': ['numerico', 'moneda', 'calculado', 'fecha']
    },
    'MAX': {
        'nombre': 'Máximo',
        'descripcion': 'Encuentra el valor máximo',
        'aplicable_a': ['numerico', 'moneda', 'calculado', 'fecha']
    }
}

# Añadir a definición de cada informe
INFORMES_DEFINICIONES = {
    "Resumen de Partes": {
        # ... configuración existente ...

        # NUEVO: Configuración de agrupación
        "agrupacion": {
            "habilitada": True,
            "campos_agrupables": [
                "estado", "red", "tipo_trabajo", "codigo_trabajo",
                "provincia", "comarca", "municipio", "tipo_rep",
                "fecha_inicio", "fecha_fin", "finalizada"
            ],
            "campos_agregables": {
                "presupuesto": ["SUM", "AVG", "MIN", "MAX", "COUNT"],
                "certificado": ["SUM", "AVG", "MIN", "MAX", "COUNT"],
                "pendiente": ["SUM", "AVG", "MIN", "MAX", "COUNT"],
                "latitud": ["AVG", "MIN", "MAX", "COUNT"],
                "longitud": ["AVG", "MIN", "MAX", "COUNT"],
                "codigo": ["COUNT", "COUNT_DISTINCT"],
                "descripcion": ["COUNT"],
                # Cualquier campo puede tener COUNT
                "*": ["COUNT"]
            }
        }
    }
}
```

### 2. Modificar `build_query()` en `informes.py`

```python
def build_query(informe_nombre, filtros=None, clasificaciones=None,
                campos_seleccionados=None, agrupaciones=None, agregaciones=None,
                schema="", user="", password=""):
    """
    Construye un query SQL dinámico para un informe

    Args:
        ... (args existentes) ...
        agrupaciones: Lista de dicts con campos de agrupación
                     [{'campo': 'provincia', 'tipo': 'dimension'}, ...]
        agregaciones: Lista de dicts con agregaciones
                     [{'campo': 'presupuesto', 'funcion': 'SUM', 'alias': 'total'}, ...]

    Returns:
        String con el query SQL completo con GROUP BY si aplica
    """

    # ... código existente para obtener definición ...

    # ========== DETERMINAR SI HAY AGRUPACIÓN ==========
    hay_agrupacion = agrupaciones and len(agrupaciones) > 0

    if hay_agrupacion:
        # MODO AGRUPACIÓN: SELECT incluye campos agrupados + agregaciones
        select_parts = []
        group_by_parts = []

        # 1. Añadir campos de agrupación al SELECT y GROUP BY
        for agrup in agrupaciones:
            campo_key = agrup['campo']
            campo = campos_def.get(campo_key)
            if campo:
                if campo['tipo'] == 'dimension':
                    alias_dim = f"{campo_key}_dim"
                    tabla_dim = campo['tabla_dimension']
                    campo_nombre = _detectar_columna_texto(user, password, schema, tabla_dim)

                    select_parts.append(f"{alias_dim}.{campo_nombre} AS {campo_key}")
                    group_by_parts.append(f"{alias_dim}.{campo_nombre}")
                else:
                    columna_bd = campo.get('columna_bd', campo_key)
                    select_parts.append(f"p.{columna_bd} AS {campo_key}")
                    group_by_parts.append(f"p.{columna_bd}")

        # 2. Añadir agregaciones al SELECT
        if agregaciones:
            for agreg in agregaciones:
                campo_key = agreg['campo']
                funcion = agreg['funcion']
                alias = agreg.get('alias', f"{campo_key}_{funcion.lower()}")

                campo = campos_def.get(campo_key)
                if campo:
                    if campo['tipo'] == 'calculado':
                        # Campo calculado
                        formula = campo['formula']
                        # ... reemplazar tablas con schema ...
                        expresion = f"({formula})"
                    elif campo['tipo'] == 'dimension':
                        # Para dimensiones, agregar por ID
                        expresion = f"p.{campo['columna_bd']}"
                    else:
                        # Campo directo
                        expresion = f"p.{campo['columna_bd']}"

                    # Construir función de agregación
                    if funcion == 'COUNT_DISTINCT':
                        select_parts.append(f"COUNT(DISTINCT {expresion}) AS {alias}")
                    else:
                        select_parts.append(f"{funcion}({expresion}) AS {alias}")

        # Construir cláusula GROUP BY
        group_by_clause = "GROUP BY " + ", ".join(group_by_parts)

    else:
        # MODO NORMAL: SELECT como hasta ahora (código existente)
        select_parts = []
        # ... código existente ...
        group_by_clause = ""

    # ========== QUERY FINAL ==========
    query = f"{select_clause}\n{from_clause}"
    if where_clause:
        query += f"\n{where_clause}"
    if group_by_clause:
        query += f"\n{group_by_clause}"
    if order_by_clause:
        query += f"\n{order_by_clause}"

    return query
```

### 3. Modificar `ejecutar_informe()` en `informes.py`

```python
def ejecutar_informe(user, password, schema, informe_nombre, filtros=None,
                     clasificaciones=None, campos_seleccionados=None,
                     agrupaciones=None, agregaciones=None):
    """
    Ejecuta un informe y devuelve los datos con totales

    Args:
        ... (args existentes) ...
        agrupaciones: Lista de agrupaciones
        agregaciones: Lista de agregaciones

    Returns:
        Tuple (columnas, datos, totales)
    """
    try:
        # Construir query CON agrupaciones
        query = build_query(
            informe_nombre, filtros, clasificaciones, campos_seleccionados,
            agrupaciones, agregaciones,  # ← NUEVO
            schema, user, password
        )

        # ... resto del código igual ...

        return columnas, datos, totales

    except Exception as e:
        print(f"Error al ejecutar informe: {e}")
        import traceback
        traceback.print_exc()
        return [], [], {}
```

### 4. Añadir pestaña de Agrupación en `informes_interfaz.py`

```python
def _create_agrupacion_tab(self):
    """Crea la pestaña de Agrupación"""
    # Frame principal con scroll
    main_frame = customtkinter.CTkScrollableFrame(self.tabs_content)

    # === SECCIÓN: AGRUPAR POR ===
    agrupar_frame = customtkinter.CTkFrame(main_frame)
    agrupar_frame.pack(fill="x", padx=10, pady=10)

    title = customtkinter.CTkLabel(
        agrupar_frame,
        text="AGRUPAR POR",
        font=customtkinter.CTkFont(size=12, weight="bold")
    )
    title.pack(anchor="w", padx=10, pady=(10, 5))

    # Contenedor de campos de agrupación
    self.agrupaciones_container = customtkinter.CTkFrame(agrupar_frame)
    self.agrupaciones_container.pack(fill="x", padx=10, pady=5)

    # Botón añadir agrupación
    add_btn = customtkinter.CTkButton(
        agrupar_frame,
        text="➕ Añadir Campo de Agrupación",
        command=self._add_agrupacion
    )
    add_btn.pack(pady=10)

    # === SECCIÓN: AGREGAR (FUNCIONES) ===
    agregar_frame = customtkinter.CTkFrame(main_frame)
    agregar_frame.pack(fill="x", padx=10, pady=10)

    title = customtkinter.CTkLabel(
        agregar_frame,
        text="AGREGAR (FUNCIONES)",
        font=customtkinter.CTkFont(size=12, weight="bold")
    )
    title.pack(anchor="w", padx=10, pady=(10, 5))

    # Contenedor de agregaciones
    self.agregaciones_container = customtkinter.CTkFrame(agregar_frame)
    self.agregaciones_container.pack(fill="x", padx=10, pady=5)

    # Botón añadir agregación
    add_btn = customtkinter.CTkButton(
        agregar_frame,
        text="➕ Añadir Agregación",
        command=self._add_agregacion
    )
    add_btn.pack(pady=10)

    # === NOTA INFORMATIVA ===
    nota = customtkinter.CTkLabel(
        main_frame,
        text="⚠️ Nota: Cuando se aplica agrupación, solo se muestran campos agrupados y agregados.",
        font=customtkinter.CTkFont(size=10),
        text_color="yellow"
    )
    nota.pack(pady=10)

    # Botón limpiar
    clear_btn = customtkinter.CTkButton(
        main_frame,
        text="🗑️ Limpiar Agrupación",
        command=self._clear_agrupacion,
        fg_color="red"
    )
    clear_btn.pack(pady=10)

    return main_frame
```

---

## ✅ VALIDACIONES Y REGLAS

### Regla 1: GROUP BY requiere agregación o agrupación

Si se especifica GROUP BY, **todos los campos en el SELECT** deben ser:
- Parte de la cláusula GROUP BY, O
- Dentro de una función de agregación (SUM, AVG, etc.)

❌ **Incorrecto:**
```sql
SELECT provincia, codigo, SUM(presupuesto)
FROM tbl_partes
GROUP BY provincia  -- ❌ 'codigo' no está en GROUP BY ni agregado
```

✅ **Correcto:**
```sql
SELECT provincia, COUNT(codigo), SUM(presupuesto)
FROM tbl_partes
GROUP BY provincia  -- ✅ codigo está dentro de COUNT()
```

### Regla 2: Validación en UI

Cuando el usuario activa agrupación:
1. Deshabilitar selección de campos que no estén agrupados/agregados
2. Mostrar advertencia si intenta seleccionar campo inválido
3. Actualizar automáticamente lista de campos disponibles

### Regla 3: Compatibilidad con Filtros y Clasificación

- ✅ **FILTROS** (WHERE): Compatible, se aplica ANTES de GROUP BY
- ✅ **CLASIFICACIÓN** (ORDER BY): Compatible, se aplica DESPUÉS de GROUP BY
- ✅ Puede combinar: WHERE + GROUP BY + ORDER BY

---

## 📝 EJEMPLOS DE QUERIES GENERADOS

### Ejemplo 1: Agrupar por Provincia, sumar presupuesto

**Configuración:**
- Agrupar por: `provincia`
- Agregaciones: `presupuesto → SUM`, `codigo → COUNT`

**Query generado:**
```sql
SELECT
    provincia_dim.nombre AS provincia,
    SUM(COALESCE((SELECT SUM(pp.cantidad * pp.precio_unit)
                  FROM cert_dev.tbl_part_presupuesto pp
                  WHERE pp.parte_id = p.id), 0)) AS total_presupuesto,
    COUNT(p.codigo) AS num_partes
FROM cert_dev.tbl_partes p
LEFT JOIN cert_dev.dim_provincias provincia_dim
    ON p.provincia_id = provincia_dim.id
GROUP BY provincia_dim.nombre
ORDER BY total_presupuesto DESC
```

### Ejemplo 2: Agrupar por Red y Tipo de Trabajo, promedios

**Configuración:**
- Agrupar por: `red`, `tipo_trabajo`
- Agregaciones: `presupuesto → AVG`, `certificado → AVG`, `codigo → COUNT`

**Query generado:**
```sql
SELECT
    red_dim.descripcion AS red,
    tipo_trabajo_dim.descripcion AS tipo_trabajo,
    AVG(presupuesto_formula) AS promedio_presupuesto,
    AVG(certificado_formula) AS promedio_certificado,
    COUNT(p.id) AS num_partes
FROM cert_dev.tbl_partes p
LEFT JOIN cert_dev.dim_red red_dim ON p.red_id = red_dim.id
LEFT JOIN cert_dev.dim_tipo_trabajo tipo_trabajo_dim
    ON p.tipo_trabajo_id = tipo_trabajo_dim.id
GROUP BY red_dim.descripcion, tipo_trabajo_dim.descripcion
ORDER BY red_dim.descripcion, tipo_trabajo_dim.descripcion
```

### Ejemplo 3: Agrupar por Estado con filtro de fecha

**Configuración:**
- Filtros: `fecha_inicio >= '2024-01-01'`
- Agrupar por: `estado`
- Agregaciones: `presupuesto → SUM`, `pendiente → SUM`, `codigo → COUNT`

**Query generado:**
```sql
SELECT
    p.estado AS estado,
    SUM(presupuesto_formula) AS total_presupuesto,
    SUM(pendiente_formula) AS total_pendiente,
    COUNT(p.id) AS num_partes
FROM cert_dev.tbl_partes p
WHERE p.fecha_inicio >= '2024-01-01'
GROUP BY p.estado
ORDER BY total_presupuesto DESC
```

---

## 🧪 PLAN DE TESTING

### Tests Unitarios (test_agrupacion_informes.py)

```python
def test_agrupacion_simple_provincia():
    """Test: Agrupar por provincia, contar partes"""
    agrupaciones = [{'campo': 'provincia', 'tipo': 'dimension'}]
    agregaciones = [{'campo': 'codigo', 'funcion': 'COUNT', 'alias': 'num_partes'}]

    query = build_query('Resumen de Partes',
                        agrupaciones=agrupaciones,
                        agregaciones=agregaciones,
                        schema='cert_dev', user='user', password='pass')

    assert 'GROUP BY' in query
    assert 'COUNT(' in query
    assert 'provincia_dim.nombre' in query

def test_agrupacion_multiple_red_tipo():
    """Test: Agrupar por red y tipo_trabajo, sumar presupuesto"""
    agrupaciones = [
        {'campo': 'red', 'tipo': 'dimension'},
        {'campo': 'tipo_trabajo', 'tipo': 'dimension'}
    ]
    agregaciones = [
        {'campo': 'presupuesto', 'funcion': 'SUM', 'alias': 'total'}
    ]

    query = build_query('Resumen de Partes',
                        agrupaciones=agrupaciones,
                        agregaciones=agregaciones,
                        schema='cert_dev', user='user', password='pass')

    assert 'GROUP BY red_dim.descripcion, tipo_trabajo_dim.descripcion' in query
    assert 'SUM(' in query

def test_agrupacion_con_filtros():
    """Test: Agrupación combinada con filtros"""
    filtros = [{'campo': 'estado', 'operador': 'Igual a', 'valor': 'Finalizado'}]
    agrupaciones = [{'campo': 'provincia', 'tipo': 'dimension'}]
    agregaciones = [{'campo': 'presupuesto', 'funcion': 'SUM', 'alias': 'total'}]

    query = build_query('Resumen de Partes',
                        filtros=filtros,
                        agrupaciones=agrupaciones,
                        agregaciones=agregaciones,
                        schema='cert_dev', user='user', password='pass')

    assert 'WHERE' in query
    assert 'GROUP BY' in query
    assert "estado = 'Finalizado'" in query

def test_ejecutar_informe_agrupado():
    """Test: Ejecutar informe con agrupación real en BD"""
    agrupaciones = [{'campo': 'estado', 'tipo': 'texto'}]
    agregaciones = [
        {'campo': 'codigo', 'funcion': 'COUNT', 'alias': 'num_partes'},
        {'campo': 'presupuesto', 'funcion': 'SUM', 'alias': 'total'}
    ]

    columnas, datos, totales = ejecutar_informe(
        user='user',
        password='pass',
        schema='cert_dev',
        informe_nombre='Resumen de Partes',
        agrupaciones=agrupaciones,
        agregaciones=agregaciones
    )

    assert len(columnas) == 3  # estado, num_partes, total
    assert len(datos) > 0
    assert 'estado' in columnas
```

### Tests de Integración

1. **Test UI**: Añadir agrupación desde interfaz, ejecutar, verificar resultado
2. **Test performance**: Agrupar 1000+ registros, verificar tiempo de respuesta
3. **Test combinación**: Filtros + Agrupación + Clasificación simultáneos

---

## 📅 CRONOGRAMA DE IMPLEMENTACIÓN

### Fase 1: Backend (2-3 horas)
- ✅ Modificar `informes_config.py` - Añadir configuración de agrupación
- ✅ Modificar `build_query()` - Implementar lógica GROUP BY
- ✅ Modificar `ejecutar_informe()` - Pasar parámetros de agrupación
- ✅ Tests unitarios de backend

### Fase 2: Interfaz (3-4 horas)
- ✅ Crear pestaña "Agrupación" en `informes_interfaz.py`
- ✅ Implementar controles de agrupación
- ✅ Implementar controles de agregación
- ✅ Validaciones UI (campos disponibles según agrupación)
- ✅ Integrar con botón "Generar Informe"

### Fase 3: Testing y Documentación (1-2 horas)
- ✅ Tests de integración
- ✅ Pruebas con datos reales
- ✅ Documentar en `docs/SISTEMA_INFORMES_RESUMEN.md`
- ✅ Crear guía de usuario para agrupación

**TOTAL ESTIMADO: 6-9 horas de desarrollo**

---

## ❓ PREGUNTAS PARA EL USUARIO

Antes de implementar, necesito confirmar:

1. **Funciones de agregación**:
   - ¿Las 6 funciones propuestas (COUNT, COUNT DISTINCT, SUM, AVG, MIN, MAX) son suficientes?
   - ¿Necesitas alguna función adicional? (MEDIAN, STDDEV, etc.)

2. **Granularidad de fechas**:
   - ¿Quieres agrupar fechas por diferentes niveles?
     * Por día completo (2024-01-15)
     * Por mes (2024-01)
     * Por año (2024)
     * Por trimestre (Q1 2024)

3. **Límite de agrupaciones**:
   - ¿Hay un límite de campos por los que se puede agrupar simultáneamente?
   - ¿Máximo 3-4 campos? ¿O ilimitado?

4. **Orden de prioridad**:
   - ¿Esta funcionalidad es urgente o puedo tomarme tiempo para hacer una implementación robusta?

5. **Visualización**:
   - ¿Los resultados agrupados se muestran solo en tabla?
   - ¿Te gustaría ver gráficos también? (barras, pie chart, etc.)

---

## ✅ SIGUIENTE PASO

Una vez confirmes el diseño y respondas las preguntas, procederé con la implementación en este orden:

1. Backend (`informes_config.py` + `informes.py`)
2. Tests unitarios
3. Interfaz (`informes_interfaz.py`)
4. Tests de integración
5. Documentación

¿Apruebas este diseño? ¿Algún cambio o adición?
