# Sistema de Plantillas PDF con ReportLab

## 📋 Descripción

Sistema de generación de PDFs profesionales con **control total del diseño** usando ReportLab. Diseñado para reemplazar el sistema anterior de Word→PDF y proporcionar un control fino sobre el diseño, similar a Microsoft Access.

## 🎯 Características Principales

### ✅ Control Total del Diseño
- **Sin dependencias externas**: No requiere Microsoft Word ni LibreOffice
- **Diseño programático**: Control total sobre colores, fuentes, tamaños, márgenes
- **Renderizado consistente**: El mismo PDF en cualquier sistema operativo
- **Diseño similar a Access**: Estilos inspirados en los informes de Microsoft Access

### 🎨 Plantillas Personalizables por Tipo de Informe
Cada tipo de informe tiene su propia configuración de colores y estilos:

| Categoría | Tipos de Informe | Esquema de Color |
|-----------|------------------|------------------|
| **📊 Partes** | Listado de Partes | Azul (#003366) |
| **📦 Recursos** | Partidas, Consumo, Trabajos | Verde (#2E7D32) |
| **💰 Presupuestos** | Contrato, Detallado, Resumen | Naranja (#E65100) |
| **✅ Certificaciones** | Detallado, Resumen | Morado (#6A1B9A) |
| **📅 Planificación** | Informe de Avance | Teal (#00695C) |

### 📊 Agrupaciones Dinámicas
- **Soporte multinivel**: Hasta 3 niveles de agrupación
- **Subtotales automáticos**: Por cada nivel de agrupación
- **Totales generales**: Al final del informe
- **Modo detalle/resumen**: Configurable por informe
- **Encabezados de grupo destacados**: Con colores diferenciados por nivel

### 🖼️ Diseño Profesional
- **Logos en encabezado**: Logo izquierdo y derecho
- **Tablas con bordes**: Estilo Access con bordes sutiles
- **Filas alternadas**: Mejor legibilidad
- **Alineación automática**: Números a la derecha, texto a la izquierda
- **Formato de moneda**: Automático para campos económicos
- **Pies de página**: Con fecha de generación y marca de agua

## 📁 Estructura del Sistema

```
script/
├── pdf_templates.py       # Clase base para plantillas PDF
├── pdf_agrupaciones.py    # Soporte para agrupaciones dinámicas
├── pdf_config.py          # Configuración por tipo de informe
└── informes_exportacion.py # Integración con el sistema de informes
```

### 1. `pdf_templates.py` - Clase Base

Proporciona la funcionalidad base para todas las plantillas PDF:

```python
from script.pdf_templates import PDFTemplate

pdf = PDFTemplate(
    schema="mi_proyecto",
    orientacion="horizontal",  # o "vertical"
    titulo="Mi Informe",
    proyecto_nombre="Proyecto X",
    proyecto_codigo="PX-001",
    fecha="16/11/2025"
)

# Agregar encabezado con logos
pdf.agregar_encabezado()

# Agregar info del proyecto
pdf.agregar_info_proyecto()

# Crear tabla simple
tabla = pdf.crear_tabla_simple(
    columnas=["Código", "Descripción", "Precio"],
    datos=[
        ("001", "Material A", 150.50),
        ("002", "Material B", 275.00)
    ],
    formatos_columnas={"Precio": "moneda"}
)
pdf.elements.append(tabla)

# Agregar pie de página
pdf.agregar_pie_pagina()

# Generar PDF
pdf.generar_pdf("mi_informe.pdf")
```

### 2. `pdf_agrupaciones.py` - Agrupaciones Dinámicas

Extiende la clase base con soporte para agrupaciones multinivel:

```python
from script.pdf_agrupaciones import PDFAgrupaciones

pdf = PDFAgrupaciones(
    schema="mi_proyecto",
    orientacion="horizontal",
    titulo="Listado de Partes por Red y Estado",
    proyecto_nombre="Proyecto X"
)

pdf.agregar_encabezado()
pdf.agregar_info_proyecto()

# Crear tabla con agrupaciones
elementos = pdf.crear_tabla_agrupada(
    columnas=["Código", "Descripción", "Presupuesto"],
    datos=datos_originales,
    resultado_agrupacion={
        'grupos': [
            {
                'nivel': 0,
                'campo': 'Red',
                'clave': 'Agua potable',
                'datos': [...],
                'subtotales': {'SUM(presupuesto)': 15000.00},
                'subgrupos': [...]
            }
        ],
        'totales_generales': {'SUM(presupuesto)': 50000.00},
        'formatos_columnas': {'Presupuesto': 'moneda'},
        'formatos_agregaciones': {'SUM(presupuesto)': 'moneda'},
        'modo': 'detalle'
    },
    modo='detalle'
)

pdf.elements.extend(elementos)
pdf.agregar_pie_pagina()
pdf.generar_pdf("informe_agrupado.pdf")
```

### 3. `pdf_config.py` - Configuración por Tipo de Informe

Define estilos específicos para cada tipo de informe:

```python
from script.pdf_config import obtener_configuracion_pdf, aplicar_configuracion_a_plantilla

# Obtener configuración para un tipo de informe
config = obtener_configuracion_pdf("Listado de Partes")

# Resultado:
# {
#     'orientacion': 'horizontal',
#     'esquema_colores': 'azul',
#     'color_titulo': '#003366',
#     'color_header_tabla': '#D9E2F3',
#     'color_grupo_nivel0': '#003366',
#     'color_grupo_nivel1': '#4472C4',
#     'color_grupo_nivel2': '#8FAADC',
#     'mostrar_logos': True,
#     'mostrar_fecha': True,
#     'bordes_tabla': True,
#     'filas_alternadas': True,
#     'pie_pagina_personalizado': None
# }

# Aplicar configuración a una plantilla
pdf = PDFAgrupaciones(...)
pdf = aplicar_configuracion_a_plantilla(pdf, config)
```

## 🔧 Personalización

### Personalizar Colores de un Tipo de Informe

Editar `script/pdf_config.py`:

```python
CONFIGURACIONES_PDF = {
    "Listado de Partes": {
        "orientacion": "horizontal",
        "color_titulo": "#FF0000",  # Rojo
        "color_header_tabla": "#FFE0E0",  # Rojo claro
        "color_grupo_nivel0": "#CC0000",  # Rojo oscuro
        "color_grupo_nivel1": "#FF6666",  # Rojo medio
        "color_grupo_nivel2": "#FF9999",  # Rojo claro
        # ... resto de configuración
    }
}
```

### Crear Nueva Configuración para un Informe Personalizado

```python
CONFIGURACIONES_PDF = {
    # ... configuraciones existentes ...

    "Mi Informe Personalizado": {
        "orientacion": "vertical",  # Vertical en lugar de horizontal
        "esquema_colores": "personalizado",
        "mostrar_logos": True,
        "mostrar_fecha": True,
        "mostrar_proyecto": True,
        "fuente_titulo": "Helvetica-Bold",
        "tamaño_titulo": 22,
        "color_titulo": "#1A237E",  # Índigo oscuro
        "color_header_tabla": "#E8EAF6",  # Índigo muy claro
        "color_grupo_nivel0": "#1A237E",
        "color_grupo_nivel1": "#3F51B5",
        "color_grupo_nivel2": "#7986CB",
        "bordes_tabla": True,
        "filas_alternadas": True,
        "pie_pagina_personalizado": "MI TEXTO PERSONALIZADO"
    }
}
```

### Personalizar Márgenes y Dimensiones

Editar `script/pdf_templates.py`:

```python
# En __init__ de PDFTemplate
self.margen_superior = 2.0 * cm  # En lugar de 1.5cm
self.margen_inferior = 2.0 * cm
self.margen_izquierdo = 2.5 * cm
self.margen_derecho = 2.5 * cm
```

## 📊 Formatos Soportados

### Formatos de Columnas

Los siguientes formatos se aplican automáticamente a las columnas:

- **`moneda`**: 1,234.56 €
- **`decimal`**: 1,234.56
- **`porcentaje`**: 12.5%
- **`entero`**: 1,234
- **`fecha`**: dd/mm/yyyy (automático)
- **`ninguno`**: Sin formato especial

### Formatos de Agregaciones

Para subtotales y totales generales:

- **`SUM(campo)`**: Suma, formato según el campo
- **`COUNT(*)`**: Cuenta, formato entero
- **`AVG(campo)`**: Promedio, formato decimal
- **`MIN(campo)`**: Mínimo
- **`MAX(campo)`**: Máximo

## 🎨 Estilos de Tabla (Estilo Access)

### Encabezados de Tabla
- **Fondo**: Color claro del esquema (ej: #D9E2F3 para azul)
- **Texto**: Color oscuro del esquema (ej: #003366 para azul)
- **Fuente**: Helvetica-Bold, 9pt
- **Alineación**: Centrada

### Datos de Tabla
- **Fuente**: Helvetica, 8pt
- **Alineación**: Izquierda para texto, derecha para números
- **Bordes**: Sutiles (#CCCCCC)
- **Filas alternadas**: Color gris claro (#F2F2F2)

### Encabezados de Grupo
- **Nivel 0**: Fondo oscuro del esquema, texto blanco, icono 📁
- **Nivel 1**: Fondo medio del esquema, texto blanco, icono 📂
- **Nivel 2**: Fondo claro del esquema, texto blanco, icono 📄

### Subtotales
- **Fondo**: Gris (#E7E6E6)
- **Texto**: Negro (#333333)
- **Fuente**: Helvetica-Bold, 9pt
- **Icono**: ▸

### Total General
- **Fondo**: Color claro del esquema (#C5D9F1)
- **Texto**: Color oscuro del esquema (#003366)
- **Fuente**: Helvetica-Bold, 10pt
- **Borde**: Grueso (2pt)

## 🔄 Migración desde el Sistema Anterior

### Antes (Word → PDF)
```python
exito = exportador.exportar_a_pdf(
    filepath="informe.pdf",
    informe_nombre="Listado de Partes",
    columnas=columnas,
    datos=datos,
    resultado_agrupacion=agrupaciones,
    proyecto_nombre="Mi Proyecto"
)
# Requería Word o LibreOffice instalado
# Conversión lenta
# Resultados inconsistentes
```

### Ahora (ReportLab)
```python
exito = exportador.exportar_a_pdf(
    filepath="informe.pdf",
    informe_nombre="Listado de Partes",
    columnas=columnas,
    datos=datos,
    resultado_agrupacion=agrupaciones,
    proyecto_nombre="Mi Proyecto"
)
# Sin dependencias externas
# Generación rápida
# Resultados consistentes
# Misma interfaz, implementación mejorada
```

**Nota**: El método anterior sigue disponible como `exportar_a_pdf_word()` para compatibilidad.

## 🚀 Ventajas sobre el Sistema Anterior

| Aspecto | Sistema Anterior (Word→PDF) | Sistema Nuevo (ReportLab) |
|---------|----------------------------|---------------------------|
| **Dependencias** | Word o LibreOffice | Solo ReportLab |
| **Velocidad** | Lenta (conversión) | Rápida (directo) |
| **Consistencia** | Variable según software | 100% consistente |
| **Control diseño** | Limitado | Total |
| **Agrupaciones** | Problemáticas | Nativas y robustas |
| **Colores** | Fijos en plantilla | Dinámicos por informe |
| **Mantenimiento** | Complejo (archivos .docx) | Simple (código Python) |

## 🐛 Solución de Problemas

### Problema: Los logos no aparecen

**Solución**: Verificar que los logos existen en:
```
resources/images/Logo Redes Urbide.jpg
resources/images/Logo Urbide.jpg
```

O en la raíz del proyecto.

### Problema: Colores incorrectos

**Verificar**: Configuración en `script/pdf_config.py`
```python
config = obtener_configuracion_pdf("Tu Tipo de Informe")
print(config)  # Verificar colores
```

### Problema: Tablas muy anchas

**Solución**: Las tablas se ajustan automáticamente al ancho de página. Si hay muchas columnas, considerar:
1. Usar orientación horizontal
2. Reducir el número de columnas mostradas
3. Ajustar márgenes en `pdf_templates.py`

### Problema: Agrupaciones no se muestran

**Verificar**: Que `resultado_agrupacion` contenga estructura de `grupos`:
```python
print(resultado_agrupacion.get('grupos'))
# Debe retornar lista de diccionarios con estructura de grupos
```

## 📚 Ejemplos Completos

Ver ejemplos en:
- `test_informes_completo.py`: Tests de generación de informes
- `interface/informes_interfaz.py`: Integración con interfaz gráfica

## 🔗 Referencias

- [ReportLab Documentation](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [Especificación de Colores](https://www.rapidtables.com/web/color/RGB_Color.html)

---

**HydroFlow Manager v1.04** | Sistema de Gestión de Proyectos Hidráulicos
