# HydroFlow Manager v2.0
## Manual de Generador de Informes

---

**Versión del Software:** 2.0
**Fecha de Publicación:** Noviembre 2025
**Empresa:** Artanda Ingeniería y Consultoría
**Audiencia:** Usuarios avanzados

---

## Tabla de Contenidos

1. [Introducción al Generador de Informes](#1-introducción-al-generador-de-informes)
2. [Acceso al Módulo](#2-acceso-al-módulo)
3. [Interfaz del Generador](#3-interfaz-del-generador)
4. [Tipos de Informes Disponibles](#4-tipos-de-informes-disponibles)
5. [Configuración Básica](#5-configuración-básica)
6. [Filtros Avanzados](#6-filtros-avanzados)
7. [Selección de Campos](#7-selección-de-campos)
8. [Sistema de Agrupaciones](#8-sistema-de-agrupaciones)
9. [Formatos de Exportación](#9-formatos-de-exportación)
10. [Guardar y Cargar Configuraciones](#10-guardar-y-cargar-configuraciones)
11. [Casos de Uso Prácticos](#11-casos-de-uso-prácticos)
12. [Tips y Trucos](#12-tips-y-trucos)

---

## 1. Introducción al Generador de Informes

### 1.1 ¿Qué es el Generador de Informes?

El **Generador de Informes** de HydroFlow Manager es una herramienta potente que permite crear informes personalizados a partir de los datos del proyecto. A diferencia de informes fijos, el generador permite:

✨ **Seleccionar exactamente qué campos mostrar**
✨ **Aplicar filtros complejos**
✨ **Agrupar datos de múltiples formas**
✨ **Exportar en varios formatos (PDF, Excel, Word)**
✨ **Guardar configuraciones para reutilizar**

### 1.2 Categorías de Informes

El sistema organiza los informes en **4 categorías principales**:

| Categoría | Informes Disponibles | Uso Típico |
|-----------|---------------------|------------|
| **📊 Partes** | Listado de Partes | Control de trabajos realizados |
| **📦 Recursos** | Recursos Presupuestados<br>Recursos Certificados<br>Recursos Pendientes<br>Listado de Partidas | Análisis de costes y materiales |
| **💰 Presupuestos** | Contrato<br>Presupuesto Detallado<br>Presupuesto Resumen | Presentación a cliente |
| **✅ Certificaciones** | Certificación Detallado<br>Certificación Resumen | Facturación mensual |

### 1.3 Flujo de Trabajo Típico

```
1. Seleccionar tipo de informe
   ↓
2. Configurar filtros (fechas, municipios, etc.)
   ↓
3. Elegir campos a mostrar
   ↓
4. Configurar agrupaciones (opcional)
   ↓
5. Previsualizar datos
   ↓
6. Exportar a PDF/Excel/Word
   ↓
7. Guardar configuración (opcional)
```

---

## 2. Acceso al Módulo

### 2.1 Desde el Menú Principal

![Acceso al módulo de informes](screenshots/reports_01_access.png)

1. En la barra lateral, haga clic en el icono **📄 Informes**
2. Se abrirá el **Generador de Informes**

### 2.2 Permisos Requeridos

- **Usuario normal:** Puede generar informes de consulta
- **Técnico:** Puede generar todos los informes
- **Administrador:** Acceso completo + gestión de plantillas

---

## 3. Interfaz del Generador

### 3.1 Vista General

![Interfaz del generador](screenshots/reports_02_interface.png)

La interfaz se divide en **5 pasos**:

```
┌─────────────────────────────────────────────────┐
│  PASO 1: Seleccionar Tipo de Informe           │
│  [Dropdown con categorías e informes]          │
└─────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────┐
│  PASO 2: Configurar Filtros                    │
│  [Fecha inicio] [Fecha fin]                    │
│  [☐ Municipios] [☐ Redes] [☐ Estado]          │
└─────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────┐
│  PASO 3: Seleccionar Campos                    │
│  [Campos disponibles]  →→  [Campos seleccionados]│
└─────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────┐
│  PASO 4: Configurar Agrupación                 │
│  [Sin agrupar ▼] [Por municipio ▼] [Por red ▼] │
└─────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────┐
│  PASO 5: Generar y Exportar                    │
│  [🔍 Previsualizar] [📄 PDF] [📊 Excel] [📝 Word]│
└─────────────────────────────────────────────────┘
```

### 3.2 Barra de Herramientas

| Botón | Función | Atajo |
|-------|---------|-------|
| 💾 Guardar Config | Guardar configuración actual | Ctrl+S |
| 📁 Cargar Config | Cargar configuración guardada | Ctrl+L |
| 🔄 Reset | Resetear a valores por defecto | Ctrl+R |
| ❓ Ayuda | Ver ayuda contextual | F1 |

---

## 4. Tipos de Informes Disponibles

### 4.1 Categoría: Partes (📊)

#### 4.1.1 Listado de Partes

**Descripción:** Relación completa de todos los partes con importes.

**Campos disponibles:**
- Código de parte
- Fecha
- Municipio
- Red
- Tipo de trabajo
- Estado
- Importe presupuestado
- Importe certificado
- Diferencia

**Agrupaciones posibles:**
- Por municipio
- Por red
- Por tipo de trabajo
- Por mes
- Por año

**Caso de uso:** Control diario de trabajos, seguimiento de partes pendientes.

---

### 4.2 Categoría: Recursos (📦)

#### 4.2.1 Recursos Presupuestados

**Descripción:** Listado de partidas presupuestadas por parte.

**Campos disponibles:**
- Código de parte
- Código de partida
- Descripción partida
- Unidad
- Cantidad presupuestada
- Precio unitario
- Importe

**Totales automáticos:**
- Suma por parte
- Suma total del informe

**Agrupaciones:**
- Por parte
- Por capítulo presupuestario
- Por naturaleza (Obra/Seguridad/etc.)

#### 4.2.2 Recursos Certificados

**Descripción:** Recursos que han sido certificados.

**Diferencia con Presupuestados:**
- Solo muestra cantidades certificadas
- Incluye fecha de certificación
- Calcula diferencias respecto presupuesto

**Campos adicionales:**
- Fecha de certificación
- Cantidad certificada
- Importe certificado
- % sobre presupuesto

#### 4.2.3 Recursos Pendientes

**Descripción:** Diferencia entre presupuestado y certificado.

**Campos clave:**
- Cantidad pendiente = Presupuestado - Certificado
- Importe pendiente
- % pendiente

**Caso de uso:** Planificación de próximas certificaciones.

#### 4.2.4 Listado de Partidas del Presupuesto

**Descripción:** Catálogo completo de partidas disponibles.

**Campos:**
- Código de partida
- Capítulo
- Descripción
- Unidad
- Precio unitario

---

### 4.3 Categoría: Presupuestos (💰)

#### 4.3.1 Contrato

**Descripción:** Presupuesto oficial para el contrato.

**Incluye:**
- Portada con datos del proyecto
- Capítulos y partidas
- Precios unitarios
- Mediciones
- Totales con GG, BI e IVA

**Formato:** Solo PDF (formato oficial)

#### 4.3.2 Presupuesto Detallado

**Descripción:** Desagregación completa del presupuesto.

**Estructura:**
```
CAPÍTULO 1: Excavaciones
  ├── 1.1 Excavación manual
  │   Descripción: ...
  │   Unidad: m³
  │   Cantidad: 150.00
  │   Precio: 25.50 €/m³
  │   Importe: 3,825.00 €
  │
  ├── 1.2 Excavación mecánica
  └── ...

  TOTAL CAPÍTULO 1: 15,420.00 €

CAPÍTULO 2: Instalaciones
  └── ...
```

**Configuraciones:**
- Con/sin descripciones
- Con/sin descomposición de precios
- Nivel de detalle (capítulo/partida/subpartida)

#### 4.3.3 Presupuesto Resumen

**Descripción:** Resumen por capítulos.

**Contenido:**
```
┌─────────────┬──────────────────────┬─────────────┐
│ Capítulo    │ Descripción          │ Importe     │
├─────────────┼──────────────────────┼─────────────┤
│ CAP01       │ Excavaciones         │  15,420.00 €│
│ CAP02       │ Instalaciones        │  48,200.00 €│
│ CAP03       │ Seguridad y Salud    │   3,250.00 €│
├─────────────┴──────────────────────┼─────────────┤
│ TOTAL PRESUPUESTO EJECUCIÓN MATERIAL│  66,870.00 €│
│ 13% Gastos Generales                │   8,693.10 €│
│ 6% Beneficio Industrial             │   4,012.20 €│
├─────────────────────────────────────┼─────────────┤
│ TOTAL BASE IMPONIBLE                │  79,575.30 €│
│ 21% IVA                             │  16,710.81 €│
├─────────────────────────────────────┼─────────────┤
│ TOTAL PRESUPUESTO CONTRATA (IVA INC)│  96,286.11 €│
└─────────────────────────────────────┴─────────────┘
```

---

### 4.4 Categoría: Certificaciones (✅)

#### 4.4.1 Certificación Detallado

**Descripción:** Certificación completa con todas las partidas.

**Estructura similar a Presupuesto Detallado, pero:**
- Incluye columna "Cantidad Certificada"
- Columna "Cantidad Presupuestada" (referencia)
- Columna "% Ejecutado"
- Resaltado de partidas completadas

**Secciones:**
1. **Datos de la Certificación**
   - Número de certificación
   - Período (fecha inicio - fecha fin)
   - Partes incluidos

2. **Detalle de Partidas**
   - Por capítulo
   - Con totales parciales

3. **Resumen Económico**
   - PEM
   - GG + BI
   - Base Imponible
   - IVA
   - Total

#### 4.4.2 Certificación Resumen

**Descripción:** Resumen ejecutivo de la certificación.

**Contenido:**
- Lista de partes incluidos
- Totales por capítulo
- Comparativa presupuesto vs ejecutado
- Gráfico de avance (opcional)

---

## 5. Configuración Básica

### 5.1 PASO 1: Seleccionar Tipo de Informe

![Selección de informe](screenshots/reports_03_select.png)

1. **Abrir el desplegable** de "Tipo de Informe"
2. Se mostrarán las categorías:
   ```
   📊 Partes
     → Listado de Partes

   📦 Recursos
     → Listado de Partidas del Presupuesto
     → Recursos Presupuestados
     → Recursos Certificados
     → Recursos Pendientes

   💰 Presupuestos
     → Contrato
     → Presupuesto Detallado
     → Presupuesto Resumen

   ✅ Certificaciones
     → Certificación Detallado
     → Certificación Resumen
   ```
3. **Seleccione el informe** deseado
4. La interfaz se actualizará mostrando opciones específicas

### 5.2 PASO 2: Configurar Filtros

#### 5.2.1 Filtros Temporales

**Rango de Fechas:**

```
[📅 Fecha Inicio: 01/01/2024] [📅 Fecha Fin: 31/12/2024]
```

- **Obligatorio** para la mayoría de informes
- Click en el icono de calendario para seleccionar
- Formato: DD/MM/AAAA

**Consejos:**
- Para un mes específico: 01/03/2024 - 31/03/2024
- Para el año completo: 01/01/2024 - 31/12/2024
- Para últimos 30 días: Use el botón "Último mes"

#### 5.2.2 Filtros Geográficos

**Municipios:**

```
☐ Todos los municipios
☑ Filtrar por municipios específicos
   [☑ Donostia]
   [☑ Errenteria]
   [☐ Irun]
   ...
```

**Redes:**

```
☐ Todas las redes
☑ Filtrar por redes
   [☑ Red A - Principal]
   [☑ Red B - Secundaria]
   [☐] Red C - Terciaria]
```

#### 5.2.3 Filtros de Estado

**Estado de Partes:**

```
[☑ Pendiente]  [☑ En Curso]  [☑ Finalizado]  [☐ Cancelado]
```

**Certificado:**

```
( ) Todos
( ) Solo certificados
(•) Solo no certificados
```

---

## 6. Filtros Avanzados

### 6.1 Filtros Combinados

Puede combinar múltiples filtros para consultas específicas:

**Ejemplo 1: Partes finalizados pero no certificados**
```
Fechas: 01/01/2024 - 31/03/2024
Estado: [☑ Finalizado]
Certificado: ( ) Solo no certificados
```

**Ejemplo 2: Trabajos de una red en un municipio**
```
Municipios: [☑ Donostia]
Redes: [☑ Red A]
```

### 6.2 Operadores de Filtro

Para campos numéricos (importes, cantidades):

| Operador | Descripción | Ejemplo |
|----------|-------------|---------|
| `=` | Igual a | Importe = 1000 |
| `>` | Mayor que | Cantidad > 50 |
| `<` | Menor que | Precio < 100 |
| `>=` | Mayor o igual | Importe >= 500 |
| `<=` | Menor o igual | Cantidad <= 200 |
| `Entre` | Rango | Importe entre 100 y 500 |

Para campos de texto:

| Operador | Descripción | Ejemplo |
|----------|-------------|---------|
| `Contiene` | Incluye texto | Descripción contiene "válvula" |
| `Empieza por` | Comienza con | Código empieza por "P-2024" |
| `Termina en` | Finaliza con | Código termina en "001" |
| `Exacto` | Coincidencia exacta | Estado exacto "Finalizado" |

---

## 7. Selección de Campos

### 7.1 Campos Disponibles vs Seleccionados

La interfaz muestra dos listas:

```
┌─────────────────────┐      ┌─────────────────────┐
│ CAMPOS DISPONIBLES  │      │ CAMPOS SELECCIONADOS│
├─────────────────────┤      ├─────────────────────┤
│ ☐ Código            │ →→   │ ☑ Fecha             │
│ ☐ Título            │      │ ☑ Municipio         │
│ ☐ Descripción       │  ←←  │ ☑ Red               │
│ ☐ Estado            │      │ ☑ Importe           │
│ ☐ Coordenadas       │      │                     │
│ ☐ Observaciones     │      │                     │
└─────────────────────┘      └─────────────────────┘
    [→→ Añadir >>]              [<< Quitar ←←]
```

### 7.2 Orden de Campos

**Cambiar el orden:**
1. Seleccione un campo en la lista derecha
2. Use los botones **↑ Subir** / **↓ Bajar**
3. El orden se refleja en el informe final

**Ejemplo:**

```
Original:           Reordenado:
1. Fecha            1. Código
2. Código           2. Fecha
3. Municipio        3. Municipio
4. Importe          4. Importe
```

### 7.3 Campos por Tipo de Informe

#### Listado de Partes - Campos Disponibles

| Grupo | Campos |
|-------|--------|
| **Temporal** | Año, Mes, Fecha |
| **Información Básica** | Código, Título, Descripción, Estado |
| **Dimensiones Técnicas** | Red, Tipo de Trabajo, Municipio |
| **Ubicación** | Dirección, Coordenadas X/Y |
| **Económicos** | Importe Presupuestado, Importe Certificado, Diferencia |

#### Recursos - Campos Disponibles

| Grupo | Campos |
|-------|--------|
| **Parte** | Código Parte, Fecha Parte |
| **Partida** | Código Partida, Descripción, Capítulo |
| **Medición** | Unidad, Cantidad, Precio Unitario, Importe |
| **Estado** | Certificado (Sí/No), Fecha Certificación |

### 7.4 Campos Calculados

Algunos campos se calculan automáticamente:

**% Ejecutado:**
```
% Ejecutado = (Cantidad Certificada / Cantidad Presupuestada) × 100
```

**Diferencia:**
```
Diferencia = Importe Presupuestado - Importe Certificado
```

**Pendiente:**
```
Pendiente = Cantidad Presupuestada - Cantidad Certificada
```

---

## 8. Sistema de Agrupaciones

### 8.1 ¿Qué son las Agrupaciones?

Las agrupaciones organizan los datos en secciones con subtotales.

**Sin agrupar:**
```
Parte-001  |  Red A  |  1,500 €
Parte-002  |  Red B  |  2,300 €
Parte-003  |  Red A  |  1,800 €
─────────────────────────────────
TOTAL:                  5,600 €
```

**Agrupado por Red:**
```
RED A
  Parte-001  |  1,500 €
  Parte-003  |  1,800 €
  ─────────────────────
  Subtotal Red A: 3,300 €

RED B
  Parte-002  |  2,300 €
  ─────────────────────
  Subtotal Red B: 2,300 €
─────────────────────────
TOTAL GENERAL:  5,600 €
```

### 8.2 Tipos de Agrupación

#### 8.2.1 Agrupación Simple

**Un solo nivel de agrupación:**

```
[Agrupar por: Municipio ▼]
```

Opciones:
- Sin agrupar
- Por municipio
- Por red
- Por tipo de trabajo
- Por mes
- Por año
- Por estado

#### 8.2.2 Agrupación Múltiple (Anidada)

**Varios niveles jerárquicos:**

```
[Nivel 1: Año ▼]
[Nivel 2: Mes ▼]
[Nivel 3: Red ▼]
```

**Resultado:**
```
2024
  ├── Enero
  │   ├── Red A
  │   │   ├── Parte-001: 1,500 €
  │   │   └── Parte-002: 1,200 €
  │   │   Subtotal Red A: 2,700 €
  │   │
  │   ├── Red B
  │   │   └── Parte-003: 2,100 €
  │   │   Subtotal Red B: 2,100 €
  │   │
  │   Subtotal Enero: 4,800 €
  │
  ├── Febrero
  │   └── ...
  │
  Total 2024: 45,600 €
```

### 8.3 Configuración de Agrupaciones

#### 8.3.1 Añadir Nivel de Agrupación

1. Click en **"+ Añadir Nivel"**
2. Seleccione el campo por el que agrupar
3. Configure opciones:
   - **Mostrar subtotales:** ☑
   - **Salto de página entre grupos:** ☐
   - **Orden:** Ascendente / Descendente

#### 8.3.2 Ejemplo: Certificación por Red y Municipio

**Configuración:**
```
Nivel 1: Red (ascendente)
  └─ Subtotales: ☑
  └─ Salto de página: ☑

Nivel 2: Municipio (ascendente)
  └─ Subtotales: ☑
  └─ Salto de página: ☐
```

**Resultado:**
```
═══════════════════════════════════
RED A - PRINCIPAL
═══════════════════════════════════

  DONOSTIA
  ─────────────────────────────────
  Parte-001  |  Válvula    |  1,500 €
  Parte-004  |  Brida      |  1,200 €
  ─────────────────────────────────
  Subtotal Donostia: 2,700 €

  ERRENTERIA
  ─────────────────────────────────
  Parte-007  |  Tubería    |  3,400 €
  ─────────────────────────────────
  Subtotal Errenteria: 3,400 €

───────────────────────────────────
TOTAL RED A: 6,100 €
═══════════════════════════════════

[Nueva página]

═══════════════════════════════════
RED B - SECUNDARIA
═══════════════════════════════════
  ...
```

### 8.4 Totales y Subtotales

**Tipos de totales:**

| Tipo | Descripción | Cuándo se muestra |
|------|-------------|-------------------|
| **Subtotal de grupo** | Suma dentro de un grupo | Final de cada grupo |
| **Subtotal de nivel** | Suma de un nivel completo | Final de nivel superior |
| **Total general** | Suma de todo el informe | Final del informe |

**Configuración de totales:**
```
☑ Mostrar subtotales por grupo
☑ Mostrar total general
☐ Incluir cuenta de registros
☑ Resaltar totales en negrita
```

---

## 9. Formatos de Exportación

### 9.1 Formato PDF

**Características:**
- Diseño profesional con encabezados
- Logo de la empresa
- Paginación automática
- Formato ideal para presentación a cliente

**Opciones de PDF:**
```
┌─────────────────────────────────────┐
│ OPCIONES DE EXPORTACIÓN PDF         │
├─────────────────────────────────────┤
│ Orientación:                        │
│  (•) Vertical  ( ) Horizontal       │
│                                     │
│ Tamaño de papel:                    │
│  [A4 ▼]                             │
│                                     │
│ ☑ Incluir portada                   │
│ ☑ Incluir índice                    │
│ ☑ Incluir pie de página con fecha   │
│ ☑ Numerar páginas                   │
│                                     │
│ Plantilla: [Estándar ▼]             │
└─────────────────────────────────────┘
```

**Plantillas disponibles:**
- **Estándar:** Diseño corporativo estándar
- **Ejecutivo:** Diseño minimalista para dirección
- **Técnico:** Con más detalles y especificaciones
- **Cliente:** Formato simplificado para cliente final

### 9.2 Formato Excel

**Características:**
- Datos editables
- Fórmulas automáticas en totales
- Formato condicional (opcional)
- Ideal para análisis posterior

**Opciones de Excel:**
```
┌─────────────────────────────────────┐
│ OPCIONES DE EXPORTACIÓN EXCEL       │
├─────────────────────────────────────┤
│ ☑ Autoajustar anchos de columna     │
│ ☑ Aplicar formato de tabla          │
│ ☑ Incluir filtros en encabezados    │
│ ☑ Congelar primera fila              │
│ ☐ Formato condicional en importes   │
│ ☑ Incluir hoja de resumen            │
│                                     │
│ Formato de números:                 │
│  (•) Europeo (1.234,56)             │
│  ( ) Americano (1,234.56)           │
└─────────────────────────────────────┘
```

**Hojas generadas:**
1. **Datos:** Tabla principal con los datos
2. **Resumen:** Totales y gráficos (si está activado)
3. **Metadatos:** Información sobre el informe

### 9.3 Formato Word

**Características:**
- Documento editable
- Tablas formateadas
- Ideal para personalización posterior

**Opciones de Word:**
```
┌─────────────────────────────────────┐
│ OPCIONES DE EXPORTACIÓN WORD        │
├─────────────────────────────────────┤
│ Plantilla base:                     │
│  [Informe_Plantilla.docx ▼]         │
│                                     │
│ ☑ Usar estilos de la plantilla      │
│ ☑ Incluir tabla de contenidos       │
│ ☑ Actualizar campos automáticamente │
│                                     │
│ Marcador de inserción de datos:    │
│  [TABLA_DE_DATOS]                   │
└─────────────────────────────────────┘
```

**Personalización de plantilla:**

1. Cree un documento Word con su formato
2. Inserte el marcador `[TABLA_DE_DATOS]` donde quiera la tabla
3. Guarde como `.docx` en `resources/plantillas/`
4. Selecciónelo en el desplegable de plantillas

### 9.4 Comparativa de Formatos

| Característica | PDF | Excel | Word |
|----------------|-----|-------|------|
| **Editable** | ❌ | ✅ | ✅ |
| **Diseño fijo** | ✅ | ❌ | ⚠️ |
| **Análisis de datos** | ❌ | ✅ | ❌ |
| **Presentación cliente** | ✅ | ⚠️ | ✅ |
| **Fórmulas** | ❌ | ✅ | ❌ |
| **Gráficos** | ✅ | ✅ | ⚠️ |
| **Portabilidad** | ✅ | ✅ | ✅ |

**Recomendación:**
- **PDF:** Certificaciones oficiales, presentaciones finales
- **Excel:** Análisis internos, planificación
- **Word:** Informes que requieren personalización de texto

---

## 10. Guardar y Cargar Configuraciones

### 10.1 ¿Por qué Guardar Configuraciones?

Si genera informes similares regularmente (ej: certificación mensual), **guardar la configuración** le ahorra tiempo:

✅ **Una vez configurado, reutilizar siempre**
✅ **Consistencia en informes periódicos**
✅ **Compartir configuraciones con colegas**

### 10.2 Guardar una Configuración

**Pasos:**

1. Configure el informe como desee:
   - Tipo de informe
   - Filtros
   - Campos
   - Agrupaciones

2. Click en **💾 "Guardar Configuración"**

3. Asigne un nombre descriptivo:
   ```
   ┌──────────────────────────────────┐
   │ Guardar Configuración            │
   ├──────────────────────────────────┤
   │ Nombre:                          │
   │ [Certificación Mensual Red A___]│
   │                                  │
   │ Descripción (opcional):          │
   │ [Certificación mensual de Red A  │
   │  para facturación______________]│
   │                                  │
   │ [Cancelar]  [Guardar]            │
   └──────────────────────────────────┘
   ```

4. Click en **"Guardar"**

**Ubicación del archivo:**
- Windows: `%APPDATA%/HydroFlow/informes_guardados/`
- Linux: `~/.config/hydroflow/informes_guardados/`
- Formato: JSON

### 10.3 Cargar una Configuración

**Pasos:**

1. Click en **📁 "Cargar Configuración"**

2. Se muestra lista de configuraciones guardadas:
   ```
   ┌────────────────────────────────────────┐
   │ Configuraciones Guardadas              │
   ├────────────────────────────────────────┤
   │ ☐ Certificación Mensual Red A          │
   │   Certificación Detallado | 12 campos  │
   │   Guardado: 15/10/2024 10:30          │
   │                                        │
   │ ☐ Presupuesto Completo Cliente         │
   │   Presupuesto Detallado | 8 campos    │
   │   Guardado: 01/10/2024 09:15          │
   │                                        │
   │ ☐ Análisis Recursos Mensuales          │
   │   Recursos Certificados | 15 campos   │
   │   Guardado: 20/09/2024 14:45          │
   │                                        │
   │ [Cancelar]  [Cargar Seleccionado]      │
   └────────────────────────────────────────┘
   ```

3. Seleccione la configuración
4. Click en **"Cargar Seleccionado"**
5. El formulario se rellena automáticamente

**Nota:** Los filtros de fecha NO se cargan (debe actualizarlos manualmente).

### 10.4 Gestionar Configuraciones

**Editar:**
1. Cargar configuración
2. Modificar lo necesario
3. Guardar con el mismo nombre (sobrescribe)

**Eliminar:**
1. Click derecho sobre una configuración
2. **"Eliminar"**
3. Confirmar

**Exportar/Compartir:**
```
Ubicación: %APPDATA%/HydroFlow/informes_guardados/
Archivo: certificacion_mensual_red_a.json

Puede copiar este archivo y compartirlo con colegas.
```

---

## 11. Casos de Uso Prácticos

### 11.1 Caso 1: Certificación Mensual

**Objetivo:** Generar certificación de marzo 2024 para facturar.

**Pasos:**

1. **Tipo de Informe:** Certificación Detallado

2. **Filtros:**
   - Fecha inicio: 01/03/2024
   - Fecha fin: 31/03/2024
   - Estado: [☑ Finalizado]
   - Certificado: Solo no certificados

3. **Campos:** (Todos por defecto)

4. **Agrupación:**
   - Nivel 1: Red
   - Nivel 2: Municipio

5. **Exportar:** PDF (Plantilla: Estándar)

6. **Guardar Config:** "Certificación Mensual"

**Próximo mes:** Solo cargar config y cambiar fechas.

---

### 11.2 Caso 2: Análisis de Recursos por Red

**Objetivo:** Ver qué recursos se han usado en cada red.

**Pasos:**

1. **Tipo de Informe:** Recursos Certificados

2. **Filtros:**
   - Fecha: Todo el año (01/01/2024 - 31/12/2024)
   - Redes: [☑ Red A] [☑ Red B]

3. **Campos:**
   - Código de parte
   - Red
   - Código de partida
   - Descripción
   - Cantidad certificada
   - Importe

4. **Agrupación:**
   - Nivel 1: Red
   - Nivel 2: Código de partida

5. **Exportar:** Excel (para análisis)

**Resultado:** Ver qué partidas se han usado más en cada red.

---

### 11.3 Caso 3: Presupuesto para Cliente

**Objetivo:** Presentación limpia del presupuesto.

**Pasos:**

1. **Tipo de Informe:** Presupuesto Detallado

2. **Filtros:** (Ninguno, mostrar todo)

3. **Campos:** Solo los esenciales
   - Código de partida
   - Descripción
   - Unidad
   - Cantidad
   - Precio unitario
   - Importe

4. **Agrupación:** Por capítulo

5. **Exportar:** PDF (Plantilla: Cliente)

**Personalización:**
- Sin descripciones técnicas muy largas
- Formato limpio y profesional

---

### 11.4 Caso 4: Control de Partes Pendientes

**Objetivo:** Listar trabajos sin certificar.

**Pasos:**

1. **Tipo de Informe:** Listado de Partes

2. **Filtros:**
   - Fecha: Últimos 3 meses
   - Estado: [☑ Finalizado]
   - Certificado: Solo no certificados

3. **Campos:**
   - Código
   - Fecha
   - Municipio
   - Red
   - Importe presupuestado

4. **Orden:** Por fecha (más antiguo primero)

5. **Exportar:** Excel (para seguimiento interno)

**Resultado:** Lista de trabajos listos para certificar.

---

## 12. Tips y Trucos

### 12.1 Optimización de Informes

**🚀 Rendimiento:**
- Filtre por fechas específicas (evite "Todo el histórico")
- Use agrupaciones solo cuando sea necesario
- Para análisis grandes, use Excel (más rápido que PDF)

**📊 Visualización:**
- En PDF: Máximo 15 campos para legibilidad
- En Excel: Puede incluir todos los campos
- Use orientación horizontal para muchas columnas

**💡 Presentación:**
- Para cliente: Menos es más (solo campos esenciales)
- Para interno: Incluya todos los detalles

### 12.2 Atajos de Teclado

| Atajo | Acción |
|-------|--------|
| `Ctrl + S` | Guardar configuración |
| `Ctrl + L` | Cargar configuración |
| `Ctrl + R` | Reset formulario |
| `Ctrl + P` | Generar PDF |
| `Ctrl + E` | Generar Excel |
| `F5` | Actualizar preview |

### 12.3 Resolución de Problemas

**Problema: "No hay datos para mostrar"**

✅ **Soluciones:**
- Verifique los filtros de fecha
- Verifique que hay partes en ese período
- Revise los filtros de estado/municipio

**Problema: "El PDF tarda mucho en generarse"**

✅ **Soluciones:**
- Reduzca el rango de fechas
- Disminuya el número de campos
- Simplifique las agrupaciones

**Problema: "Los totales no cuadran"**

✅ **Soluciones:**
- Verifique los filtros aplicados
- Compruebe que no hay datos duplicados
- Revise las agrupaciones (pueden estar sumando mal)

### 12.4 Mejores Prácticas

✅ **Nombres de Configuraciones:**
- Descriptivos: "Certificación Mensual Red A"
- NO genéricos: "Informe1", "Config_test"

✅ **Organización:**
- Cree una configuración por cada informe recurrente
- Documente el propósito en la descripción
- Revise y actualice configuraciones antiguas

✅ **Backup:**
- Haga backup periódico de la carpeta `informes_guardados/`
- Exporte configuraciones importantes

---

**Fin del Manual de Informes**

*Para más información sobre otros módulos, consulte el Manual de Usuario.*

**¿Necesita ayuda?** Contacte con soporte técnico.
