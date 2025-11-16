# Generación de Informes PDF en HydroFlow Manager

## Descripción General

HydroFlow Manager genera informes PDF utilizando un **método híbrido Word → PDF**:
1. Se crea un documento Word (.docx) desde una plantilla
2. Se convierte automáticamente a PDF usando herramientas del sistema

Este enfoque permite:
- ✅ Diseño visual fácil de plantillas en Microsoft Word
- ✅ Sin código complejo de layout
- ✅ Múltiples plantillas para diferentes tipos de informes
- ✅ Calidad profesional garantizada
- ✅ **El mismo archivo .docx se usa tanto para Word como para PDF**

---

## Dependencias Requeridas

### 1. **Dependencias Python (Obligatorias)**

Instaladas automáticamente con `requirements.txt`:

```bash
pip install -r requirements.txt
```

Incluye:
- `python-docx>=0.8.0` - Generación de documentos Word
- `reportlab>=3.6.0` - Generación alternativa de PDFs
- `pywin32>=305` - Conversión Word→PDF en Windows (solo Windows)

### 2. **Software de Conversión PDF (Requerido para generar PDFs)**

Elige **UNA** de estas opciones:

#### Opción A: Microsoft Office (Recomendado para Windows)
- **Ventaja:** Mejor calidad, conversión perfecta
- **Desventaja:** Software de pago
- **Instalación:** Incluido en Microsoft Office
- **Compatibilidad:** Solo Windows

#### Opción B: LibreOffice (Alternativa Gratuita)
- **Ventaja:** Gratis, multiplataforma
- **Desventaja:** Conversión ligeramente menos precisa
- **Instalación:** https://www.libreoffice.org/download/download/
- **Compatibilidad:** Windows, Linux, macOS

**IMPORTANTE:** Sin al menos uno de estos, solo se podrán generar archivos `.docx` (Word), NO `.pdf`.

---

## Sistema de Plantillas Word

HydroFlow Manager utiliza **plantillas Word (.docx)** como base para generar los PDFs. Esto permite:
- Diseño visual fácil en Microsoft Word (WYSIWYG)
- Sin necesidad de programar layouts complejos
- Personalización por tipo de informe

### Ubicación de Plantillas

```
resources/plantillas/
├── Plantilla_Partes.docx           # Para: Listado de Partes
├── Plantilla_Recursos.docx         # Para: Listado de Partidas, Consumo, Trabajos por Actuación
├── Plantilla_Presupuesto.docx      # Para: Contrato, Presupuesto Detallado/Resumen
├── Plantilla_Certificacion.docx    # Para: Certificación Detallado/Resumen
├── Plantilla_Planificacion.docx    # Para: Informe de Avance
├── Plantilla_Generica.docx         # Plantilla por defecto (fallback)
└── Plantilla Listado Partes.docx   # Plantilla legacy (compatibilidad)
```

### Mapeo Automático de Plantillas

El sistema selecciona automáticamente la plantilla apropiada según el tipo de informe:

| Tipo de Informe | Plantilla Usada |
|-----------------|-----------------|
| Listado de Partes | `Plantilla_Partes.docx` |
| Listado de Partidas del Presupuesto | `Plantilla_Recursos.docx` |
| Consumo de Recursos | `Plantilla_Recursos.docx` |
| Trabajos por Actuación | `Plantilla_Recursos.docx` |
| Contrato | `Plantilla_Presupuesto.docx` |
| Presupuesto Detallado | `Plantilla_Presupuesto.docx` |
| Presupuesto Resumen | `Plantilla_Presupuesto.docx` |
| Certificación Detallado | `Plantilla_Certificacion.docx` |
| Certificación Resumen | `Plantilla_Certificacion.docx` |
| Informe de Avance | `Plantilla_Planificacion.docx` |
| *(Sin mapeo)* | `Plantilla_Generica.docx` |

**Configurado en:** `script/plantillas_config.py`

---

## Marcadores en Plantillas

Las plantillas usan **marcadores** (placeholders) que se reemplazan automáticamente con datos reales:

| Marcador | Descripción | Ejemplo |
|----------|-------------|---------|
| `[TITULO_DEL_INFORME]` | Nombre del informe | "LISTADO DE PARTES" |
| `[FECHA]` | Fecha de generación | "16/11/2024" |
| `[PROYECTO_NOMBRE]` | Nombre del proyecto | "Urbanización El Pinar" |
| `[PROYECTO_CODIGO]` | Código del proyecto | "URB-2024-001" |
| `[TABLA_DE_DATOS]` | **Tabla completa con datos** | *(Tabla generada)* |
| `[TOTAL_REGISTROS]` | Número de registros | "125" |
| `[FILTROS_APLICADOS]` | Filtros aplicados | "Fecha: 01/01/2024 - 31/12/2024" |
| `[EMPRESA]` | Nombre de la empresa | "HydroFlow S.L." |
| `[USUARIO]` | Usuario que genera | "admin" |

### Cómo usar marcadores:

1. Abre la plantilla en Word: `resources/plantillas/Plantilla_XXX.docx`
2. Coloca el marcador donde quieras que aparezca el dato
3. Guarda y listo

**Ejemplo:**
```
INFORME: [TITULO_DEL_INFORME]
Fecha: [FECHA]
Proyecto: [PROYECTO_NOMBRE]

[TABLA_DE_DATOS]

Total de registros: [TOTAL_REGISTROS]
```

---

## Personalizar Plantillas

### Paso 1: Seleccionar Plantilla

Identifica qué plantilla usar según el tipo de informe (ver tabla arriba).

### Paso 2: Editar en Word

1. Abre la plantilla en **Microsoft Word**
2. Diseña visualmente:
   - Cambia colores, fuentes, logos
   - Añade encabezados y pies de página
   - Personaliza márgenes y orientación
   - Agrega imágenes corporativas
3. Mantén los marcadores `[MARCADOR]` donde quieras datos dinámicos

### Paso 3: Guardar

Guarda el archivo `.docx` con el **mismo nombre**. La próxima vez que generes ese tipo de informe, usará tu diseño personalizado.

**IMPORTANTE:**
- ✅ **Sí:** Usa estilos de Word, colores, fuentes estándar
- ❌ **No:** Macros VBA, campos calculados complejos, fuentes raras

---

## Flujo Técnico: Word → PDF

```
┌─────────────────────────────────────────────────────┐
│ 1. Usuario genera informe PDF                      │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│ 2. Sistema selecciona plantilla según tipo informe │
│    → script/plantillas_config.py                    │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│ 3. Genera archivo Word temporal (.docx)            │
│    → script/informes_exportacion.py:exportar_a_word│
│    → Copia plantilla y reemplaza marcadores        │
│    → Inserta tabla de datos                        │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│ 4. Convierte Word → PDF                            │
│    → script/informes_exportacion.py:exportar_a_pdf │
│                                                     │
│    Métodos de conversión (en orden de prioridad):  │
│    a) Microsoft Word COM (Windows)                 │
│    b) LibreOffice (multiplataforma)                │
│    c) Reportlab (fallback básico)                  │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│ 5. PDF final guardado                              │
│    → Archivo temporal .docx eliminado              │
└─────────────────────────────────────────────────────┘
```

**IMPORTANTE:** El mismo archivo `.docx` se usa tanto para exportación Word como para PDF. No hay dos procesos separados.

---

## Configuración de PyInstaller

Para empaquetar correctamente el ejecutable con las plantillas incluidas:

### HidroFlowManager.spec

```python
datas=[
    ('resources/plantillas/*.docx', 'resources/plantillas')  # Incluir plantillas
],
hiddenimports=[
    'docx',
    'reportlab',
    'reportlab.platypus',
    'reportlab.lib',
    'win32com',
    'win32com.client',
    'pythoncom',
    'subprocess',
    'script.plantillas_config',
    'script.informes_exportacion'
]
```

---

## Verificación de Dependencias

Ejecuta el script de verificación para asegurarte de que todo esté configurado:

```bash
python verificar_dependencias_pdf.py
```

**Salida esperada:**

```
======================================================================
  Verificación de Dependencias para Generación de PDFs
======================================================================

[Dependencias Python]
  ✓ python-docx: Instalado (versión 0.8.11)
  ✓ reportlab: Instalado (versión 3.6.12)
  ✓ pywin32: Instalado (versión 305)

[Software de Conversión PDF]
  ✓ Microsoft Word: Detectado (versión 16.0)
  ✓ LibreOffice: Detectado (/usr/bin/soffice)

[Plantillas]
  ✓ Plantilla_Partes.docx: Encontrada
  ✓ Plantilla_Recursos.docx: Encontrada
  ✓ Plantilla_Presupuesto.docx: Encontrada
  ✓ Plantilla_Certificacion.docx: Encontrada
  ✓ Plantilla_Planificacion.docx: Encontrada
  ✓ Plantilla_Generica.docx: Encontrada
  ✓ Plantilla Listado Partes.docx: Encontrada (legacy)

======================================================================
  RESUMEN
======================================================================
  ✓ Todas las dependencias están instaladas correctamente
  ✓ Sistema listo para generar PDFs
======================================================================
```

---

## Solución de Problemas

### Problema: "No se pudo generar el PDF"

**Verificar:**
1. ¿Tienes Microsoft Word o LibreOffice instalado?
2. ¿Las dependencias Python están instaladas?

**Solución:**
```bash
# Verificar dependencias
python verificar_dependencias_pdf.py

# Instalar LibreOffice (alternativa gratuita)
# https://www.libreoffice.org/download/download/

# Reinstalar dependencias Python
pip install --upgrade -r requirements.txt
```

---

### Problema: "Plantilla no encontrada"

**Verificar:**
1. ¿Las plantillas existen en `resources/plantillas/`?
2. ¿El nombre del archivo es exacto? (ej: `Plantilla_Partes.docx`)

**Solución:**
```bash
# Verificar que existan las plantillas
ls resources/plantillas/*.docx

# Si faltan, copiar de la plantilla base
cp "resources/plantillas/Plantilla Listado Partes.docx" resources/plantillas/Plantilla_Generica.docx
```

---

### Problema: "Los marcadores no se reemplazan"

**Verificar:**
1. ¿Los marcadores están escritos exactamente como se indica? (case-sensitive)
2. ¿No hay espacios extra dentro de los corchetes?

**Correcto:**   `[TITULO_DEL_INFORME]`
**Incorrecto:** `[ TITULO_DEL_INFORME ]` ← espacios extra

---

### Problema: "El PDF se ve diferente al Word"

**Causa:** Diferencias en el motor de renderizado de Word vs LibreOffice.

**Solución:**
1. Usa Microsoft Word en lugar de LibreOffice (conversión más precisa)
2. Usa fuentes estándar (Arial, Calibri, Times New Roman)
3. Evita diseños muy complejos

---

### Problema: "Error: win32com no disponible"

**Causa:** pywin32 no está instalado (solo Windows).

**Solución:**
```bash
pip install pywin32==305

# Después de instalar, ejecutar:
python Scripts/pywin32_postinstall.py -install
```

---

## Archivos Relacionados

| Archivo | Descripción |
|---------|-------------|
| `script/plantillas_config.py` | Configuración de plantillas y mapeo de informes |
| `script/informes_exportacion.py` | Lógica de exportación Word y PDF |
| `resources/plantillas/*.docx` | Plantillas Word para cada tipo de informe |
| `resources/plantillas/README.md` | Guía detallada para personalizar plantillas |
| `verificar_dependencias_pdf.py` | Script de verificación de dependencias |
| `HidroFlowManager.spec` | Configuración de empaquetado PyInstaller |
| `requirements.txt` | Dependencias Python del proyecto |

---

## Próximos Pasos

1. **Personalizar plantillas**: Abre cada plantilla en Word y personalízala con tu branding corporativo
2. **Instalar software de conversión**: Asegúrate de tener Microsoft Word o LibreOffice
3. **Verificar dependencias**: Ejecuta `python verificar_dependencias_pdf.py`
4. **Generar informe de prueba**: Usa la aplicación para generar un PDF de prueba

---

**HydroFlow Manager v1.04**
Sistema de Gestión de Proyectos Hidráulicos
