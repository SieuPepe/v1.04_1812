# MAQUETA: INFORME DE ÓRDENES DE TRABAJO CON RECURSOS

## 📋 DESCRIPCIÓN GENERAL

**Nombre del Informe:** "Presupuesto Detallado"

**Categoría:** 💰 Presupuestos

**Descripción:** Listado de órdenes de trabajo clasificadas, filtradas y agrupadas según los criterios de la interfaz. Cada orden muestra sus detalles principales (Título, Fecha Fin, Municipio, Localización, Latitud, Longitud) seguido de una tabla con los recursos presupuestados de esa orden específica.

**Tipo de Informe:** Híbrido - Combina listado de órdenes con sub-tablas de recursos por orden

**Tabla Principal:** `tbl_partes`

**Tablas Relacionadas:** `tbl_part_presupuesto`, `tbl_pres_precios`, `tbl_pres_unidades`

---

## 🎯 CARACTERÍSTICAS PRINCIPALES

### 1. Criterios de Filtrado y Agrupación
- **Usa los mismos criterios que "Listado de Partes"**
- Filtros por: Red, Tipo de Trabajo, Municipio, Comarca, Provincia, Estado, Mes, Año, etc.
- Agrupación flexible: Se puede agrupar por cualquier campo disponible (Red, Tipo de Trabajo, Municipio, Comarca, Mes, Año, etc.) hasta 3 niveles jerárquicos

### 2. Estructura del Informe
Cada Orden de Trabajo se muestra con:

**A) Cabecera de la Orden:**
- **Primera línea:** Código de Orden de Trabajo a la izquierda + Título a la derecha (en la misma línea horizontal)
  - Ejemplo: `OT-0252          Reparación de tubería en Llodio`
- **Fecha:** Etiqueta "FECHA:" seguida del valor
- **Localización:** Etiqueta "LOCALIZACIÓN:" seguida del municipio/localización
- **Coordenadas:** Etiqueta "LATITUD:" con valor, seguido de "LONGITUD:" con valor (ambos en la misma fila)

**B) Tabla de Recursos Presupuestados:**
Tabla con 6 columnas (igual que "Recursos Presupuestados"):
- **Código** (codigo del precio)
- **Cantidad** (cantidad de la medición)
- **Ud.** (unidad)
- **Recurso / Material** (resumen/descripción)
- **Precio unitario** (coste)
- **Importe** (cantidad × coste)

**Diferencia clave:** La tabla muestra **solo las líneas de medición de ESA orden específica**, sin agrupar cantidades de múltiples órdenes.

### 3. Formato de Salida
- **PDF:** Vertical (portrait)
- **Excel:** Con formato y estructura jerárquica
- **Word:** Con estructura de tabla y formato profesional

---

## ⚙️ CONFIGURACIÓN TÉCNICA

### 1. Configuración en `informes_config.py`

```python
"Presupuesto Detallado": {
    "categoria": "💰 Presupuestos",
    "descripcion": "Relación de partes con sus mediciones presupuestadas. Subtotal por parte y total general.",
    "tabla_principal": "tbl_partes",
    "require_joins": ["tbl_part_presupuesto", "tbl_pres_precios", "tbl_pres_unidades"],
    "formato_pdf": "vertical",  # Portrait
    "tipo_especial": "ordenes_con_recursos",  # Tipo especial de informe híbrido
    "campos_fijos": True,  # Campos fijos para la cabecera de orden
    "subtabla_recursos": True,  # Indica que incluye sub-tabla de recursos

    # Campos de la ORDEN DE TRABAJO (cabecera)
    # Formato: Código y Título en la misma línea horizontal
    "campos_orden": {
        "codigo": {
            "nombre": "",  # Sin etiqueta, se muestra a la izquierda
            "tipo": "texto",
            "columna_bd": "codigo",
            "grupo": "Orden",
            "posicion": "izquierda_primera_fila"  # A la izquierda en la primera fila
        },
        "titulo": {
            "nombre": "",  # Sin etiqueta, se muestra a la derecha del código
            "tipo": "texto",
            "columna_bd": "titulo",
            "grupo": "Orden",
            "posicion": "derecha_primera_fila"  # A la derecha en la primera fila
        },
        "fecha_fin": {
            "nombre": "FECHA:",
            "tipo": "fecha",
            "columna_bd": "fecha_fin",
            "grupo": "Orden"
        },
        "municipio": {
            "nombre": "LOCALIZACIÓN:",  # Combina municipio y localización
            "tipo": "dimension",
            "columna_bd": "municipio_id",
            "tabla_dimension": "dim_municipios",
            "campo_nombre": "descripcion",
            "grupo": "Orden",
            "combinar_con": "localizacion"  # Se combina con localización
        },
        "localizacion": {
            "nombre": "",  # Se muestra junto con municipio
            "tipo": "texto",
            "columna_bd": "localizacion",
            "grupo": "Orden",
            "parte_de": "municipio"  # Es parte del campo municipio
        },
        "latitud": {
            "nombre": "LATITUD:",
            "tipo": "numerico",
            "columna_bd": "latitud",
            "formato": "decimal",
            "grupo": "Orden",
            "misma_fila_que": "longitud"  # Se muestra en la misma fila que longitud
        },
        "longitud": {
            "nombre": "LONGITUD:",
            "tipo": "numerico",
            "columna_bd": "longitud",
            "formato": "decimal",
            "grupo": "Orden",
            "misma_fila_que": "latitud"  # Se muestra en la misma fila que latitud
        }
    },

    # Campos para FILTRADO Y AGRUPACIÓN (mismos que Listado de Partes)
    "campos": {
        "mes": {
            "nombre": "Mes",
            "tipo": "calculado",
            "formula": "DATE_FORMAT(p.fecha_inicio, '%Y-%m')",
            "grupo": "Temporal"
        },
        "año": {
            "nombre": "Año",
            "tipo": "calculado",
            "formula": "YEAR(p.fecha_inicio)",
            "grupo": "Temporal"
        },
        "codigo": {
            "nombre": "Código",
            "tipo": "texto",
            "columna_bd": "codigo",
            "grupo": "Información Básica"
        },
        "estado": {
            "nombre": "Estado",
            "tipo": "texto",
            "columna_bd": "estado",
            "grupo": "Información Básica"
        },
        "red": {
            "nombre": "Red",
            "tipo": "dimension",
            "columna_bd": "red_id",
            "tabla_dimension": "dim_red",
            "campo_nombre": "descripcion",
            "grupo": "Dimensiones Técnicas"
        },
        "tipo_trabajo": {
            "nombre": "Tipo de Trabajo",
            "tipo": "dimension",
            "columna_bd": "tipo_trabajo_id",
            "tabla_dimension": "dim_tipo_trabajo",
            "campo_nombre": "descripcion",
            "grupo": "Dimensiones Técnicas"
        },
        "codigo_trabajo": {
            "nombre": "Código de Trabajo",
            "tipo": "dimension",
            "columna_bd": "cod_id",
            "tabla_dimension": "dim_cod",
            "campo_nombre": "descripcion",
            "grupo": "Dimensiones Técnicas"
        },
        "tipo_rep": {
            "nombre": "Tipo de Reparación",
            "tipo": "dimension",
            "columna_bd": "tipo_rep_id",
            "tabla_dimension": "dim_tipos_rep",
            "campo_nombre": "descripcion",
            "grupo": "Dimensiones Técnicas"
        },
        "provincia": {
            "nombre": "Provincia",
            "tipo": "dimension",
            "columna_bd": "provincia_id",
            "tabla_dimension": "dim_provincias",
            "campo_nombre": "descripcion",
            "grupo": "Ubicación"
        },
        "comarca": {
            "nombre": "Comarca",
            "tipo": "dimension",
            "columna_bd": "comarca_id",
            "tabla_dimension": "dim_comarcas",
            "campo_nombre": "descripcion",
            "grupo": "Ubicación"
        },
        "municipio": {
            "nombre": "Municipio",
            "tipo": "dimension",
            "columna_bd": "municipio_id",
            "tabla_dimension": "dim_municipios",
            "campo_nombre": "descripcion",
            "grupo": "Ubicación"
        },
        "trabajadores": {
            "nombre": "Trabajadores",
            "tipo": "texto",
            "columna_bd": "trabajadores",
            "grupo": "Información Básica"
        },
        "fecha_inicio": {
            "nombre": "Fecha Inicio",
            "tipo": "fecha",
            "columna_bd": "fecha_inicio",
            "grupo": "Temporal"
        },
        "fecha_fin": {
            "nombre": "Fecha Fin",
            "tipo": "fecha",
            "columna_bd": "fecha_fin",
            "grupo": "Temporal"
        },
        "finalizada": {
            "nombre": "Finalizada",
            "tipo": "boolean",
            "columna_bd": "finalizada",
            "grupo": "Información Básica"
        }
    },

    # Campos de la TABLA DE RECURSOS (sub-tabla por cada orden)
    "campos_recursos": {
        "codigo": {
            "nombre": "Código",
            "tipo": "texto",
            "tabla_relacion": "precio",
            "columna_bd": "codigo",
            "grupo": "Recurso"
        },
        "cantidad": {
            "nombre": "Cantidad",
            "tipo": "numerico",
            "columna_bd": "cantidad",
            "formato": "decimal",
            "grupo": "Recurso"
        },
        "unidad": {
            "nombre": "Ud.",
            "tipo": "dimension",
            "tabla_relacion": "precio",
            "columna_bd": "id_unidades",
            "tabla_dimension": "tbl_pres_unidades",
            "campo_nombre": "descripcion",
            "grupo": "Recurso"
        },
        "resumen": {
            "nombre": "Recurso / Material",
            "tipo": "texto",
            "tabla_relacion": "precio",
            "columna_bd": "resumen",
            "grupo": "Recurso"
        },
        "coste": {
            "nombre": "Precio unitario",
            "tipo": "numerico",
            "tabla_relacion": "precio",
            "columna_bd": "coste",
            "formato": "moneda",
            "grupo": "Recurso"
        },
        "coste_total": {
            "nombre": "Importe",
            "tipo": "calculado",
            "formula": "pres.cantidad * precio.coste",
            "formato": "moneda",
            "grupo": "Recurso"
        }
    },

    # Filtros permitidos (mismos que Listado de Partes)
    "filtros": {
        "mes": {
            "campo": "mes",
            "tipo": "mes",
            "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
        },
        "año": {
            "campo": "año",
            "tipo": "año",
            "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
        },
        "estado": {
            "campo": "estado",
            "tipo": "select",
            "operadores": ["Igual a", "Diferente de"],
            "valores": ["Pendiente", "En curso", "Finalizado"]
        },
        "red": {
            "campo": "red",
            "tipo": "select_bd",
            "operadores": ["Igual a", "Diferente de"],
            "tabla": "dim_red"
        },
        "tipo_trabajo": {
            "campo": "tipo_trabajo",
            "tipo": "select_bd",
            "operadores": ["Igual a", "Diferente de"],
            "tabla": "dim_tipo_trabajo"
        },
        "codigo_trabajo": {
            "campo": "codigo_trabajo",
            "tipo": "select_bd",
            "operadores": ["Igual a", "Diferente de"],
            "tabla": "dim_cod"
        },
        "tipo_rep": {
            "campo": "tipo_rep",
            "tipo": "select_bd",
            "operadores": ["Igual a", "Diferente de"],
            "tabla": "dim_tipos_rep"
        },
        "provincia": {
            "campo": "provincia",
            "tipo": "select_bd",
            "operadores": ["Igual a", "Diferente de"],
            "tabla": "dim_provincias"
        },
        "comarca": {
            "campo": "comarca",
            "tipo": "select_bd",
            "operadores": ["Igual a", "Diferente de"],
            "tabla": "dim_comarcas"
        },
        "municipio": {
            "campo": "municipio",
            "tipo": "select_bd",
            "operadores": ["Igual a", "Diferente de"],
            "tabla": "dim_municipios"
        },
        "trabajadores": {
            "campo": "trabajadores",
            "tipo": "texto",
            "operadores": ["Contiene", "No contiene"]
        },
        "fecha_inicio": {
            "campo": "fecha_inicio",
            "tipo": "fecha",
            "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
        },
        "fecha_fin": {
            "campo": "fecha_fin",
            "tipo": "fecha",
            "operadores": ["Igual a", "Posterior a", "Anterior a", "Entre"]
        },
        "finalizada": {
            "campo": "finalizada",
            "tipo": "boolean",
            "operadores": ["Igual a"]
        }
    },

    # Ordenaciones permitidas (mismas que Listado de Partes)
    "ordenaciones": [
        "mes",
        "año",
        "estado",
        "red",
        "tipo_trabajo",
        "provincia",
        "comarca",
        "municipio",
        "fecha_inicio",
        "fecha_fin",
        "tipo_rep"
    ],

    # Agrupaciones permitidas (mismas que Listado de Partes)
    "agrupaciones": {
        "campos_permitidos": [
            "mes",
            "año",
            "estado",
            "red",
            "tipo_trabajo",
            "codigo_trabajo",
            "tipo_rep",
            "provincia",
            "comarca",
            "municipio",
            "trabajadores"
        ],
        "max_niveles": 3,
        "modo_default": "detalle"
    },

    # No se usan agregaciones (no es un informe resumido)
    "agregaciones": {},

    # Campos que siempre se muestran en la cabecera de cada orden
    "campos_orden_default": [
        "codigo",
        "titulo",
        "fecha_fin",
        "municipio",
        "localizacion",
        "latitud",
        "longitud"
    ],

    # Campos que siempre se muestran en la tabla de recursos
    "campos_recursos_default": [
        "codigo",
        "cantidad",
        "unidad",
        "resumen",
        "coste",
        "coste_total"
    ]
}
```

---

### 2. Configuración en `pdf_config.py`

```python
"Presupuesto Detallado": {
    "orientacion": "vertical",  # Portrait
    "esquema_colores": "naranja",  # Esquema naranja para Presupuestos
    "mostrar_logos": True,
    "mostrar_fecha": False,  # NO mostrar fecha en encabezado (va en pie de página)
    "mostrar_proyecto": False,  # NO mostrar proyecto en encabezado
    "fuente_titulo": "Helvetica-Bold",
    "tamaño_titulo": 20,
    "color_titulo": "#E65100",  # Naranja oscuro
    "color_header_tabla": "#FFF3E0",  # Naranja muy claro
    "color_grupo_nivel0": "#E65100",  # Agrupación nivel 1 (ej: por Red, Tipo de Trabajo, Municipio)
    "color_grupo_nivel1": "#FF9800",  # Agrupación nivel 2
    "color_grupo_nivel2": "#FFB74D",  # Agrupación nivel 3
    "color_orden": "#FF9800",  # Color para la cabecera de cada orden
    "color_subtabla_header": "#FFCCBC",  # Color para encabezado de tabla de recursos
    "bordes_tabla": True,
    "filas_alternadas": True,

    # Configuración del PIE DE PÁGINA
    "pie_pagina_personalizado": {
        "mostrar_fecha": True,  # Fecha a la izquierda
        "mostrar_paginacion": True,  # "Página X de Y" a la derecha
        "formato_paginacion": "Página {pagina} de {total}",
        "fuente": "Helvetica",
        "tamaño_fuente": 9,
        "color_texto": "#666666"
    },

    # Configuración específica para este informe
    "espaciado_entre_ordenes": 10,  # Espacio vertical entre órdenes (pt)
    "mostrar_totales_por_orden": True,  # Mostrar total de importe por orden
    "mostrar_gran_total": True,  # Mostrar gran total al final del informe
}
```

---

### 3. Categoría en `informes_config.py`

El informe "Presupuesto Detallado" ya existe en la categoría "💰 Presupuestos":

```python
CATEGORIAS_INFORMES = {
    "💰 Presupuestos": [
        "Contrato",
        "Presupuesto Detallado",  # <-- MODIFICADO con nueva funcionalidad
        "Presupuesto Resumen"
    ],
    # ... resto de categorías ...
}
```

---

## 📊 ESTRUCTURA VISUAL DEL INFORME

### Ejemplo de Salida (PDF/Excel/Word)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  [Logo Redes Urbide]      PRESUPUESTO DETALLADO      [Logo Urbide]         │
└─────────────────────────────────────────────────────────────────────────────┘

[SI HAY AGRUPACIÓN - Ejemplo: Agrupado por Tipo de Trabajo]
────────────────────────────────────────────────────────────────────────────────
█ TIPO DE TRABAJO: Reparación
────────────────────────────────────────────────────────────────────────────────

    ┌─────────────────────────────────────────────────────────────────────┐
    │ OT-2025-001        Reparación urgente calle Mayor                   │
    ├─────────────────────────────────────────────────────────────────────┤
    │ FECHA:             15/11/2025                                       │
    │ LOCALIZACIÓN:      Valencia - Calle Mayor, 45                       │
    │ LATITUD:  39.4699                LONGITUD: -0.3763                  │
    └─────────────────────────────────────────────────────────────────────┘

    ┌────────┬──────────┬──────┬─────────────────────┬────────────┬──────────┐
    │ Código │ Cantidad │  Ud. │ Recurso / Material  │ Precio uni │  Importe │
    ├────────┼──────────┼──────┼─────────────────────┼────────────┼──────────┤
    │ R001   │    12.50 │   m  │ Tubería PVC 110mm   │    15.50 € │ 193.75 € │
    │ R025   │     2.00 │  Ud. │ Arqueta 40x40       │   125.00 € │ 250.00 € │
    │ M010   │     8.00 │   h  │ Oficial 1ª          │    25.00 € │ 200.00 € │
    ├────────┴──────────┴──────┴─────────────────────┴────────────┼──────────┤
    │                                              TOTAL ORDEN:   │ 643.75 € │
    └────────────────────────────────────────────────────────────┴──────────┘

    ┌─────────────────────────────────────────────────────────────────────┐
    │ OT-2025-002        Reparación de válvula defectuosa                 │
    ├─────────────────────────────────────────────────────────────────────┤
    │ FECHA:             20/11/2025                                       │
    │ LOCALIZACIÓN:      Valencia - Polígono industrial Norte             │
    │ LATITUD:  39.5125                LONGITUD: -0.3854                  │
    └─────────────────────────────────────────────────────────────────────┘

    ┌────────┬──────────┬──────┬─────────────────────┬────────────┬──────────┐
    │ Código │ Cantidad │  Ud. │ Recurso / Material  │ Precio uni │  Importe │
    ├────────┼──────────┼──────┼─────────────────────┼────────────┼──────────┤
    │ R001   │    25.00 │   m  │ Tubería PVC 110mm   │    15.50 € │ 387.50 € │
    │ R035   │     1.00 │  Ud. │ Válvula compuerta   │   350.00 € │ 350.00 € │
    │ M010   │    16.00 │   h  │ Oficial 1ª          │    25.00 € │ 400.00 € │
    │ M020   │    16.00 │   h  │ Peón                │    18.00 € │ 288.00 € │
    ├────────┴──────────┴──────┴─────────────────────┴────────────┼──────────┤
    │                                              TOTAL ORDEN:   │1,425.50 €│
    └────────────────────────────────────────────────────────────┴──────────┘

    ────────────────────────────────────────────────────────────────────────
    SUBTOTAL TIPO DE TRABAJO: Reparación                       2,069.25 €
    ────────────────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────────────────────────
█ TIPO DE TRABAJO: Mantenimiento
────────────────────────────────────────────────────────────────────────────────

    [... más órdenes ...]

================================================================================
                    TOTAL GENERAL:                          5,234.80 €
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│ 16/11/2025                                                 Página 1 de 3    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 LÓGICA DE CONSULTA SQL

### Query Principal (Pseudocódigo)

```sql
-- 1. Obtener lista de órdenes de trabajo según filtros y agrupaciones
SELECT
    p.id,
    p.codigo,
    p.titulo,
    p.fecha_fin,
    municipio_dim.descripcion AS municipio,
    p.localizacion,
    p.latitud,
    p.longitud,
    -- Campos para agrupación
    red_dim.descripcion AS red,
    tipo_trabajo_dim.descripcion AS tipo_trabajo,
    comarca_dim.descripcion AS comarca,
    provincia_dim.descripcion AS provincia,
    DATE_FORMAT(p.fecha_inicio, '%Y-%m') AS mes,
    YEAR(p.fecha_inicio) AS año
FROM tbl_partes p
LEFT JOIN dim_municipios municipio_dim ON p.municipio_id = municipio_dim.id
LEFT JOIN dim_red red_dim ON p.red_id = red_dim.id
LEFT JOIN dim_tipo_trabajo tipo_trabajo_dim ON p.tipo_trabajo_id = tipo_trabajo_dim.id
LEFT JOIN dim_comarcas comarca_dim ON p.comarca_id = comarca_dim.id
LEFT JOIN dim_provincias provincia_dim ON p.provincia_id = provincia_dim.id
WHERE [FILTROS APLICADOS]
ORDER BY [ORDENACIÓN APLICADA]
```

### Sub-Query por cada Orden (para obtener recursos)

```sql
-- 2. Para cada orden, obtener sus recursos presupuestados
SELECT
    precio.codigo AS Código,
    pres.cantidad AS Cantidad,
    unidad_dim.descripcion AS Ud,
    precio.resumen AS 'Recurso / Material',
    precio.coste AS 'Precio unitario',
    (pres.cantidad * precio.coste) AS Importe
FROM tbl_part_presupuesto pres
LEFT JOIN tbl_pres_precios precio ON pres.precio_id = precio.id
LEFT JOIN tbl_pres_unidades unidad_dim ON precio.id_unidades = unidad_dim.id
WHERE pres.parte_id = [ID_ORDEN]
  AND pres.cantidad > 0  -- Excluir cantidades cero
ORDER BY precio.codigo
```

---

## 📝 NOTAS DE IMPLEMENTACIÓN

### Archivos a Modificar

1. **`script/informes_config.py`**
   - Agregar "Listado de Órdenes de Trabajo" a `CATEGORIAS_INFORMES`
   - Agregar configuración completa en `INFORMES_DEFINICIONES`

2. **`script/pdf_config.py`**
   - Agregar configuración de PDF en `CONFIGURACIONES_PDF`

3. **`script/informes.py`** (o crear nuevo archivo)
   - Crear función `generar_informe_ordenes_con_recursos()`
   - Implementar lógica de doble consulta (órdenes + recursos por orden)
   - Manejar agrupaciones jerárquicas

4. **`script/pdf_agrupaciones.py`** (o crear variante)
   - Crear clase `PDFOrdenesConRecursos` que extienda `PDFAgrupaciones`
   - Implementar método para renderizar cabecera de orden + sub-tabla

5. **Archivos de exportación Excel/Word**
   - Adaptar generadores para incluir estructura de orden + sub-tabla

### Funciones Clave a Implementar

```python
def ejecutar_informe_ordenes_trabajo(config, filtros, agrupaciones, ordenacion):
    """
    Ejecuta el informe de Órdenes de Trabajo con sub-tablas de recursos

    1. Obtiene lista de órdenes según filtros/agrupaciones
    2. Para cada orden, obtiene sus recursos presupuestados
    3. Estructura los datos jerárquicamente
    4. Retorna estructura lista para PDF/Excel/Word
    """
    pass

def generar_pdf_ordenes_trabajo(datos, config_pdf):
    """
    Genera PDF con estructura especial:
    - Cabecera de orden (6 campos)
    - Sub-tabla de recursos (6 columnas)
    - Totales por orden
    - Agrupaciones si aplican
    """
    pass
```

### Consideraciones Especiales

1. **Performance:**
   - Usar JOIN eficiente para minimizar consultas
   - Considerar paginación si hay muchas órdenes

2. **Formato PDF:**
   - Portrait (vertical) para mantener consistencia con otros informes
   - Encabezado simplificado: Logos a ambos lados + Título (sin Proyecto ni Fecha)
   - Pie de página con:
     * Fecha a la izquierda
     * "Página X de Y" a la derecha
   - Salto de página entre órdenes si es necesario
   - Mantener orden + sub-tabla en misma página si es posible

3. **Totales:**
   - Total por orden (suma de importes de recursos)
   - Subtotales por agrupación si aplican
   - Gran total al final del informe

4. **Filtros:**
   - Solo filtros de órdenes (no de recursos)
   - Los recursos se muestran completos por cada orden filtrada

5. **Excel/Word:**
   - Usar formato jerárquico con sangría
   - Cabecera de orden en negrita
   - Sub-tabla con formato de tabla estándar

---

## ✅ VALIDACIÓN

### Casos de Prueba

1. **Sin agrupación:** Lista simple de órdenes con sus recursos
2. **Con agrupación por Tipo de Trabajo:** Órdenes agrupadas por tipo de trabajo, con subtotales
3. **Con agrupación por Municipio:** Órdenes agrupadas por municipio, con subtotales
4. **Con agrupación múltiple (Red > Municipio > Mes):** Jerarquía de 3 niveles
5. **Con filtros:** Solo órdenes de un municipio específico o tipo de trabajo
6. **Orden sin recursos:** Debe mostrar tabla vacía o mensaje
7. **Orden con muchos recursos:** Validar paginación/salto de página

---

## 📌 RESUMEN DE DIFERENCIAS CON OTROS INFORMES

| Aspecto | Listado de Partes | Recursos Presupuestados | **Nuevo: Órdenes de Trabajo** |
|---------|-------------------|-------------------------|-------------------------------|
| Tabla principal | tbl_partes | tbl_part_presupuesto | tbl_partes |
| ¿Muestra detalles de orden? | Sí (en columnas) | No | Sí (como cabecera) |
| ¿Muestra recursos? | No | Sí (agregados) | Sí (por orden) |
| Agregación de recursos | N/A | Sí (GROUP BY) | No (individual) |
| Estructura | Tabla única | Tabla única | Orden + Sub-tabla |
| Filtros | Por orden | Por orden y recurso | Por orden |
| Formato PDF | Horizontal | Vertical | Vertical |
| Agrupación | Flexible (Red, Tipo, etc.) | Flexible | Flexible (Red, Tipo, Municipio, etc.) |

---

**MAQUETA PREPARADA Y LISTA PARA IMPLEMENTACIÓN** ✅
