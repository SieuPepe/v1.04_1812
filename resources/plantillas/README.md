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

### Paso 1: Abrir la Plantilla

Abre la plantilla que deseas personalizar en **Microsoft Word**:

```
resources/plantillas/Plantilla_Presupuesto.docx
```

### Paso 2: Diseñar Visualmente

Diseña el documento como lo harías normalmente en Word:

- ✅ Cambia colores, fuentes, logos
- ✅ Añade encabezados y pies de página
- ✅ Personaliza márgenes y orientación
- ✅ Agrega imágenes corporativas
- ✅ Configura estilos de párrafo

**IMPORTANTE:** No necesitas programar nada. Diseña visualmente.

### Paso 3: Insertar Marcadores

Los **marcadores** son palabras especiales que el programa reemplazará automáticamente con datos reales.

Coloca estos marcadores donde quieras que aparezcan los datos:

| Marcador | Se reemplaza con |
|----------|------------------|
| `[TITULO_DEL_INFORME]` | Nombre del informe (ej: "Listado de Partes") |
| `[FECHA]` | Fecha de generación del informe |
| `[PROYECTO_NOMBRE]` | Nombre del proyecto |
| `[PROYECTO_CODIGO]` | Código del proyecto |
| `[TABLA_DE_DATOS]` | **Tabla completa con los datos del informe** |
| `[TOTAL_REGISTROS]` | Número total de registros |
| `[FILTROS_APLICADOS]` | Descripción de filtros aplicados |
| `[EMPRESA]` | Nombre de la empresa |
| `[USUARIO]` | Usuario que genera el informe |

#### Ejemplo de Uso:

```
┌─────────────────────────────────────────┐
│                                         │
│   [TITULO_DEL_INFORME]                  │
│   Fecha: [FECHA]                        │
│   Proyecto: [PROYECTO_NOMBRE]           │
│                                         │
│   [TABLA_DE_DATOS]                      │
│                                         │
│   Total de registros: [TOTAL_REGISTROS] │
│                                         │
└─────────────────────────────────────────┘
```

El programa reemplazará automáticamente:

```
┌─────────────────────────────────────────┐
│                                         │
│   Listado de Partes                     │
│   Fecha: 16/11/2024                     │
│   Proyecto: Urbanización El Pinar       │
│                                         │
│   [Tabla con 50 registros de partes]   │
│                                         │
│   Total de registros: 50                │
│                                         │
└─────────────────────────────────────────┘
```

### Paso 4: Guardar

Guarda el archivo `.docx` y **listo**. La próxima vez que generes un informe de ese tipo, usará tu diseño personalizado.

---

## 🔧 Mapeo Automático

El sistema selecciona automáticamente la plantilla correcta según el tipo de informe:

```python
# Configurado en: script/plantillas_config.py

"Listado de Partes"                    → Plantilla_Partes.docx
"Listado de Partidas del Presupuesto"  → Plantilla_Recursos.docx
"Consumo de Recursos"                  → Plantilla_Recursos.docx
"Contrato"                             → Plantilla_Presupuesto.docx
"Presupuesto Detallado"                → Plantilla_Presupuesto.docx
"Certificación Detallado"              → Plantilla_Certificacion.docx
"Informe de Avance"                    → Plantilla_Planificacion.docx
```

Si un informe no tiene plantilla específica, usa `Plantilla_Generica.docx`.

---

## 📝 Consejos de Diseño

### ✅ Buenas Prácticas

1. **Usa estilos de Word**: Define estilos para títulos, tablas, etc. (no formato directo)
2. **Orientación adecuada**: Landscape para informes con muchas columnas
3. **Márgenes apropiados**: 2cm suele ser óptimo
4. **Logos en encabezado**: Usa encabezado/pie de página para logos corporativos
5. **Colores corporativos**: Define una paleta de colores y úsala consistentemente

### ❌ Evitar

1. **No uses macros VBA** - No funcionarán en el proceso de conversión
2. **No uses campos calculados complejos** - Usa solo marcadores `[MARCADOR]`
3. **No pongas tablas complejas donde va `[TABLA_DE_DATOS]`** - El programa crea la tabla automáticamente
4. **No uses fuentes raras** - Usa fuentes estándar (Arial, Calibri, Times New Roman)

---

## 🛠️ Solución de Problemas

### Problema: La plantilla no se está usando

**Verificar:**
1. ¿El nombre del archivo es exacto? (ej: `Plantilla_Partes.docx`)
2. ¿Está en el directorio correcto? (`resources/plantillas/`)
3. ¿El tipo de informe está mapeado? (ver `script/plantillas_config.py`)

**Solución:**
- Verifica que el archivo exista: `resources/plantillas/Plantilla_XXX.docx`
- Si falta, copia una plantilla existente y personalízala

### Problema: Los marcadores no se reemplazan

**Verificar:**
1. ¿Usaste los corchetes `[ ]` correctamente?
2. ¿El marcador está escrito exactamente como se indica? (case-sensitive)
3. ¿No hay espacios extra dentro de los corchetes?

**Ejemplo correcto:**   `[TITULO_DEL_INFORME]`
**Ejemplo incorrecto:** `[ TITULO_DEL_INFORME ]` ← espacios extra
**Ejemplo incorrecto:** `[titulo_del_informe]` ← minúsculas

### Problema: La tabla se ve mal

**Verificar:**
1. ¿Hay suficiente espacio alrededor del marcador `[TABLA_DE_DATOS]`?
2. ¿La orientación de la página es adecuada? (Landscape para tablas anchas)
3. ¿Los márgenes son suficientemente pequeños?

**Solución:**
- Usa orientación **Horizontal (Landscape)** para tablas con >6 columnas
- Reduce márgenes a 1.5cm si la tabla es muy ancha
- Deja `[TABLA_DE_DATOS]` en su propia línea, sin texto alrededor

### Problema: El PDF no se genera

**Verificar:**
1. ¿Tienes Microsoft Word instalado? (Windows)
2. ¿O tienes LibreOffice instalado? (alternativa gratuita)
3. ¿Las dependencias Python están instaladas?

**Solución:**
```bash
# Verificar dependencias
python verificar_dependencias_pdf.py

# Instalar LibreOffice (alternativa gratuita)
# https://www.libreoffice.org/download/download/
```

---

## 📦 Empaquetado con PyInstaller

Las plantillas se incluyen automáticamente en el ejecutable gracias a la configuración en `HidroFlowManager.spec`:

```python
datas=[
    ('resources/plantillas/*.docx', 'resources/plantillas')
]
```

**IMPORTANTE:** Si agregas nuevas plantillas, asegúrate de:
1. Guardarlas con extensión `.docx`
2. Colocarlas en `resources/plantillas/`
3. Actualizar `script/plantillas_config.py` si es un nuevo tipo de informe
4. Recompilar con PyInstaller

---

## 📚 Más Información

Para más detalles sobre el sistema de generación de PDFs, consulta:

- **Documentación completa:** `docs/GENERACION_PDF.md`
- **Configuración de plantillas:** `script/plantillas_config.py`
- **Exportador de informes:** `script/informes_exportacion.py`

---

## 🆘 Ayuda

Si tienes problemas con las plantillas:

1. Ejecuta el script de verificación:
   ```bash
   python verificar_dependencias_pdf.py
   ```

2. Revisa los logs de la aplicación

3. Consulta `docs/GENERACION_PDF.md` para solución de problemas detallada

---

**HydroFlow Manager v1.04**
Sistema de Gestión de Proyectos Hidráulicos
