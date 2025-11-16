# Plantillas Word para Informes PDF

Este directorio contiene las plantillas Word utilizadas para generar informes en formato PDF.

## 📁 Plantillas Disponibles

| Plantilla | Informes que la usan |
|-----------|----------------------|
| **Plantilla_Partes.docx** | Listado de Partes |
| **Plantilla_Recursos.docx** | Listado de Partidas del Presupuesto, Consumo de Recursos, Trabajos por Actuación |
| **Plantilla_Presupuesto.docx** | Contrato, Presupuesto Detallado, Presupuesto Resumen |
| **Plantilla_Certificacion.docx** | Certificación Detallado, Certificación Resumen |
| **Plantilla_Planificacion.docx** | Informe de Avance |
| **Plantilla_Generica.docx** | Plantilla por defecto (fallback) |
| **Plantilla Listado Partes.docx** | Plantilla legacy (compatibilidad) |

---

## 🎨 Personalizar Plantillas

### Paso 1: Abrir la plantilla en Microsoft Word

Abre la plantilla que deseas personalizar (ej: `Plantilla_Partes.docx`)

### Paso 2: Diseñar visualmente

Diseña el documento como desees:
- Añade logos corporativos
- Cambia colores, fuentes, estilos
- Añade encabezados y pies de página
- Inserta tu marca de agua o imágenes de fondo

### Paso 3: Insertar marcadores

Donde desees que aparezcan datos dinámicos, inserta los siguientes **marcadores de texto**:

| Marcador | Se reemplaza por |
|----------|------------------|
| `[TITULO_DEL_INFORME]` | Nombre del informe en mayúsculas |
| `[FECHA]` | Fecha de generación (dd/mm/yyyy) |
| `[PROYECTO_NOMBRE]` | Nombre del proyecto |
| `[PROYECTO_CODIGO]` | Código del proyecto |
| `[TABLA_DE_DATOS]` | **Tabla completa con los datos** |
| `[TOTAL_REGISTROS]` | Número de registros |
| `[FILTROS_APLICADOS]` | Descripción de filtros |

**Ejemplo de uso en la plantilla:**

```
Empresa: Tu Empresa S.L.
─────────────────────────────────

[TITULO_DEL_INFORME]

Fecha: [FECHA]
Proyecto: [PROYECTO_NOMBRE]

─────────────────────────────────

[TABLA_DE_DATOS]

─────────────────────────────────
Total de registros: [TOTAL_REGISTROS]
```

### Paso 4: Guardar la plantilla

Guarda el archivo Word en este directorio (`plantillas/`).

**IMPORTANTE**:
- El nombre del archivo debe coincidir exactamente con el definido en `script/plantillas_config.py`
- Usar formato `.docx` (no `.doc` ni otros formatos)

---

## 🔧 Configuración Técnica

### Mapeo de Informes a Plantillas

El archivo `script/plantillas_config.py` define qué plantilla usar para cada tipo de informe:

```python
PLANTILLAS_POR_INFORME = {
    "Listado de Partes": "Plantilla_Partes.docx",
    "Contrato": "Plantilla_Presupuesto.docx",
    # ...
}
```

### Añadir Nueva Plantilla

1. Crea tu plantilla Word con los marcadores
2. Guárdala en `plantillas/NuevaPlantilla.docx`
3. Edita `script/plantillas_config.py`:
   ```python
   PLANTILLAS_POR_INFORME = {
       "Mi Nuevo Informe": "NuevaPlantilla.docx",
       # ...
   }
   ```

---

## ✅ Verificar Plantillas

Para verificar que todas las plantillas necesarias existen:

```bash
python -c "from script.plantillas_config import verificar_plantillas_necesarias; print(verificar_plantillas_necesarias())"
```

---

## 💡 Consejos de Diseño

### Logos
- Inserta los logos **directamente** en la plantilla Word
- Los logos corporativos ya están en `resources/images/`
- Puedes referenciarlos desde la plantilla

### Tablas
- **NO** crees tablas manualmente en la plantilla
- Usa el marcador `[TABLA_DE_DATOS]` donde quieras la tabla
- La tabla se genera automáticamente con los datos del informe

### Orientación de página
- **Landscape (horizontal)**: Recomendado para informes con muchas columnas
- **Portrait (vertical)**: Para informes simples o resúmenes

### Estilos
- Usa estilos de Word (Título 1, Título 2, Normal, etc.)
- Los estilos se mantienen al generar el PDF
- Mantén consistencia entre todas las plantillas

### Marcas de agua
- Puedes añadir marcas de agua en Word: `Diseño → Marca de agua`
- Ejemplo: "BORRADOR", "CONFIDENCIAL", logo atenuado

---

## 🚀 Flujo de Generación

```
Usuario exporta informe
         ↓
Sistema selecciona plantilla según tipo de informe
         ↓
Copia la plantilla al archivo destino
         ↓
Reemplaza marcadores ([TITULO], [FECHA], etc.)
         ↓
Inserta tabla de datos en [TABLA_DE_DATOS]
         ↓
Guarda documento Word
         ↓
Convierte a PDF (si se solicitó PDF)
         ↓
Entrega archivo final al usuario
```

---

## 📝 Formato de los Datos

### Tablas Generadas

Las tablas generadas automáticamente incluyen:
- **Encabezados** con los nombres de las columnas
- **Datos** formateados según el tipo:
  - Moneda: `1.234,56 €`
  - Decimal: `1.234,56`
  - Fechas: `dd/mm/yyyy`
  - Texto: tal cual
- **Subtotales** si el informe tiene agrupaciones
- **Total general** al final

### Agrupaciones

Si el informe tiene agrupaciones (ej: por mes, por provincia):
- Se crean **secciones** por cada grupo
- Cada sección tiene su **subtotal**
- Al final aparece el **total general**

---

## 🛠️ Solución de Problemas

### ❌ "No se encontró la plantilla"

**Causa**: El archivo de plantilla no existe o tiene nombre incorrecto

**Solución**:
1. Verifica que existe `plantillas/NombrePlantilla.docx`
2. Verifica el nombre exacto en `script/plantillas_config.py`
3. Asegúrate de que no hay espacios extra o mayúsculas diferentes

### ❌ "Los marcadores no se reemplazan"

**Causa**: Los marcadores no están escritos exactamente como se esperan

**Solución**:
1. Copia los marcadores exactamente: `[TITULO_DEL_INFORME]`
2. Usa mayúsculas, corchetes y guiones bajos como se muestra
3. No añadas espacios dentro de los corchetes

### ❌ "La tabla no aparece"

**Causa**: El marcador `[TABLA_DE_DATOS]` no está presente

**Solución**:
1. Añade `[TABLA_DE_DATOS]` donde quieras la tabla
2. Asegúrate de que está en un párrafo separado
3. No lo pongas dentro de una tabla existente

### ❌ "El PDF se ve diferente al Word"

**Causa**: La conversión Word→PDF puede variar ligeramente

**Solución**:
1. Usa estilos estándar de Word
2. Evita formatos muy complejos
3. Prueba la plantilla exportando un informe de prueba
4. Ajusta según el resultado del PDF, no del Word

---

## 📚 Referencias

- Documentación completa: `docs/GENERACION_PDF.md`
- Configuración de plantillas: `script/plantillas_config.py`
- Código de exportación: `script/informes_exportacion.py`

---

**Última actualización**: Noviembre 2025
**Versión**: 1.04
