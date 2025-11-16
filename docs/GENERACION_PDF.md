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

---

## Dependencias Requeridas

### 1. **Dependencias Python (Obligatorias)**

Instaladas automáticamente con `pip install -r requirements.txt`:

```
python-docx >= 0.8.0      # Manipulación de documentos Word
pillow >= 10.0.0          # Procesamiento de imágenes (logos)
reportlab >= 3.6.0        # Generación directa de PDF (método alternativo)
```

### 2. **Dependencias Windows (Obligatorias en Windows)**

Para conversión Word → PDF en Windows:

```
pywin32 >= 305            # Acceso a Microsoft Word COM
```

**Instalación:**
```bash
pip install pywin32
```

**Nota**: Esta dependencia solo se instala en Windows (`sys_platform == 'win32'`)

---

## Software del Sistema (Para conversión Word → PDF)

La conversión Word → PDF requiere **uno** de los siguientes programas instalados:

### **Opción 1: Microsoft Word (Recomendado para Windows)**

- ✅ **Ventajas**: Conversión perfecta, respeta todos los estilos
- ✅ **Calidad**: Excelente
- ❌ **Desventaja**: Requiere licencia de Microsoft Office

**Detección automática**: El sistema usa `win32com.client` para comunicarse con Word

### **Opción 2: LibreOffice (Alternativa gratuita)**

- ✅ **Ventajas**: Gratuito, multiplataforma, buen resultado
- ✅ **Calidad**: Muy buena
- ⚠️ **Limitación**: Algunos estilos pueden variar ligeramente

**Instalación**:
- Windows: Descargar desde https://www.libreoffice.org/download/
- Linux: `sudo apt install libreoffice`
- macOS: Descargar desde https://www.libreoffice.org/download/

**Ubicaciones buscadas automáticamente**:
```
Windows:
  - C:\Program Files\LibreOffice\program\soffice.exe
  - C:\Program Files (x86)\LibreOffice\program\soffice.exe

Linux/Mac:
  - /usr/bin/libreoffice
  - /usr/local/bin/libreoffice
```

---

## Prioridad de Conversión

El sistema intenta los métodos en este orden:

1. **Microsoft Word COM** (solo Windows, si Word está instalado)
2. **LibreOffice** (multiplataforma, si está instalado)
3. **Error** (si ninguno está disponible)

Si falla la conversión, el sistema:
- ✅ Genera el archivo Word correctamente
- ⚠️ Muestra mensaje con instrucciones de instalación
- 💡 Permite conversión manual posterior

---

## Sistema de Plantillas

### Ubicación de Plantillas

```
plantillas/
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
|------------------|-----------------|
| Listado de Partes | Plantilla_Partes.docx |
| Listado de Partidas del Presupuesto | Plantilla_Recursos.docx |
| Consumo de Recursos | Plantilla_Recursos.docx |
| Trabajos por Actuación | Plantilla_Recursos.docx |
| Contrato | Plantilla_Presupuesto.docx |
| Presupuesto Detallado | Plantilla_Presupuesto.docx |
| Presupuesto Resumen | Plantilla_Presupuesto.docx |
| Certificación Detallado | Plantilla_Certificacion.docx |
| Certificación Resumen | Plantilla_Certificacion.docx |
| Informe de Avance | Plantilla_Planificacion.docx |

📝 **Configuración**: Edita `script/plantillas_config.py` para cambiar el mapeo

### Marcadores de Texto

Las plantillas Word usan **marcadores de texto** que se reemplazan automáticamente:

| Marcador | Descripción | Ejemplo |
|----------|-------------|---------|
| `[TITULO_DEL_INFORME]` | Nombre del informe | "LISTADO DE PARTES" |
| `[FECHA]` | Fecha de generación | "16/11/2025" |
| `[PROYECTO_NOMBRE]` | Nombre del proyecto | "Proyecto Redes Municipales" |
| `[TABLA_DE_DATOS]` | Tabla con datos del informe | *(tabla completa)* |

### Crear Nueva Plantilla

1. **Abrir Microsoft Word**
2. **Diseñar el documento** con logos, estilos, encabezados, pies de página
3. **Insertar marcadores** donde se deben reemplazar datos:
   ```
   Título: [TITULO_DEL_INFORME]
   Fecha: [FECHA]

   [TABLA_DE_DATOS]
   ```
4. **Guardar** en `plantillas/NombrePlantilla.docx`
5. **Modificar código** (si es necesario) para usar la nueva plantilla

**Ventajas**:
- ✅ Diseño WYSIWYG (lo que ves es lo que obtienes)
- ✅ Sin programación de layouts
- ✅ Reutilización de estilos corporativos

---

## Configuración del Instalador (PyInstaller)

El archivo `HidroFlowManager.spec` incluye:

### Datos empaquetados:
```python
datas=[
    ...
    ('plantillas/*.docx', 'plantillas')  # Incluir todas las plantillas
]
```

### Imports ocultos:
```python
hiddenimports=[
    'docx',                    # python-docx
    'reportlab',               # ReportLab
    'reportlab.platypus',
    'reportlab.lib',
    'reportlab.lib.pagesizes',
    'reportlab.lib.styles',
    'reportlab.lib.colors',
    'win32com',                # Para Word COM
    'win32com.client',
    'pythoncom',
    'subprocess',              # Para LibreOffice
    ...
]
```

---

## Verificación de Instalación

### Paso 1: Instalar dependencias Python
```bash
pip install -r requirements.txt
```

### Paso 2: Verificar instalación (Windows)
```bash
python -c "import win32com.client; print('✓ pywin32 instalado correctamente')"
```

### Paso 3: Verificar software de conversión

**Windows - Microsoft Word:**
```bash
python -c "import win32com.client; w = win32com.client.Dispatch('Word.Application'); print('✓ Microsoft Word disponible'); w.Quit()"
```

**Cualquier SO - LibreOffice:**
```bash
# Windows
"C:\Program Files\LibreOffice\program\soffice.exe" --version

# Linux/Mac
libreoffice --version
```

---

## Solución de Problemas

### ❌ Error: "No se pudo convertir el documento Word a PDF"

**Causa**: No hay software de conversión instalado

**Solución**:
1. Instalar Microsoft Office (Windows) o LibreOffice (multiplataforma)
2. Verificar que el ejecutable esté en las rutas esperadas
3. Como alternativa temporal: abrir el archivo .docx manualmente y "Guardar como PDF"

### ❌ Error: "No module named 'win32com'"

**Causa**: pywin32 no está instalado

**Solución**:
```bash
pip install pywin32
```

### ❌ Error: "No se encontró la plantilla"

**Causa**: Archivo de plantilla faltante

**Solución**:
1. Verificar que existe `plantillas/Plantilla Listado Partes.docx`
2. Crear plantilla si no existe (ver sección "Crear Nueva Plantilla")

### ❌ Los logos no aparecen en el PDF

**Causa**: Archivos de logo faltantes

**Solución**:
1. Verificar que existen:
   - `resources/images/Logo Redes Urbide.jpg`
   - `resources/images/Logo Urbide.jpg`
2. Las imágenes deben estar en formato JPG o PNG

---

## Método Alternativo: ReportLab Directo

El código incluye `exportar_a_pdf_old()` que genera PDFs directamente con ReportLab.

**NO se recomienda** porque:
- ❌ Requiere programar layouts manualmente
- ❌ Difícil ajustar diseños
- ❌ Mucho tiempo de desarrollo

**Usar solo si**:
- No se puede instalar Microsoft Word ni LibreOffice
- Se requiere generación de PDFs en servidor sin GUI

---

## Resumen de Comandos

### Instalación completa (Windows):
```bash
# 1. Instalar dependencias Python
pip install -r requirements.txt

# 2. Instalar Microsoft Office o LibreOffice
# (descargar manualmente desde sitio oficial)

# 3. Verificar
python -c "import docx; import win32com.client; print('✓ Todo OK')"
```

### Instalación completa (Linux):
```bash
# 1. Instalar dependencias Python
pip install -r requirements.txt

# 2. Instalar LibreOffice
sudo apt install libreoffice

# 3. Verificar
python -c "import docx; print('✓ Todo OK')"
```

---

## Contacto y Soporte

Para problemas con la generación de PDFs:
1. Verificar que todas las dependencias estén instaladas
2. Revisar los logs en consola para mensajes de error específicos
3. Consultar este documento para soluciones comunes

**Autor**: HydroFlow Manager Development Team
**Versión**: 1.04
**Fecha**: Noviembre 2025
