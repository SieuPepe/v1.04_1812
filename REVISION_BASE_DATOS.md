# Revisión de Base de Datos: APLICACION CERTIFICACIONES UTE REDES URBIDE

## Información General
- **Archivo**: APLICACION CERTIFICACIONES UTE REDES URBIDE.accdb
- **Tipo**: Microsoft Access Database
- **Tamaño**: 15 MB
- **Fecha de modificación**: 28 de octubre de 2025
- **Propósito**: Gestión de certificaciones para UTE Redes Urbide (redes de distribución de agua y saneamiento)

## Ámbito Geográfico
La base de datos gestiona trabajos en múltiples municipios de Álava:
- Agurain, Aiara, Aiaraldea, Amurrio
- Alegría, Apellániz, Araia, Arceniaga, Artziniega
- Barambio, Berantevilla, Bernedo
- Campezo y otros municipios

## Estructura de Tablas Principales

### 1. LISTADO OTS (Listado de Órdenes de Trabajo)
Tabla principal que contiene las órdenes de trabajo.

**Campos identificados:**
- `COD_TRABAJO`: Código de trabajo
- `TIPO_DE_TRABAJOS`: Tipo de trabajo a realizar
- `TITULO_OT`: Título de la orden de trabajo
- `DESCRIPCION_OT` / `DESC_CORTA_OT`: Descripción larga y corta
- `FECHA_INICIO`: Fecha de inicio
- `FECHA_FIN`: Fecha de finalización
- `FINALIZADA`: Estado de finalización (Sí/No)
- `COORDENADAS_X`: Coordenada X
- `LATITUD`: Latitud
- `LONGITUD`: Longitud
- `LOCALIZACION`: Localización del trabajo
- `RED`: Tipo de red (Distribución/Saneamiento)

### 2. MEDICIONES OTS (Mediciones de Órdenes de Trabajo)
Tabla que registra las mediciones y materiales utilizados.

**Campos identificados:**
- `id_OT`: Identificador de la orden de trabajo (clave foránea)
- `CODIGO_MAT`: Código del material
- `CANTIDAD`: Cantidad utilizada

### 3. PRECIOS UNITARIOS
Tabla con el cuadro de precios para materiales y trabajos.

**Campos identificados:**
- `CODIGO`: Código del precio unitario
- `CAPITULO`: Capítulo al que pertenece
- `DESCRIPCION`: Descripción del concepto
- `UNIDAD`: Unidad de medida
- `PRECIO_UNIDAD`: Precio por unidad

### 4. Cuadro_Precios
Tabla complementaria de precios.

**Campos identificados:**
- `codigo`: Código
- `descripcion`: Descripción

### 5. TIPO DE TRABAJOS
Catálogo de tipos de trabajos.

**Campos identificados:**
- `Id`: Identificador
- `TRABAJOS`: Descripción del tipo de trabajo

### 6. TRABAJOS PROGRAMADOS
Tabla de trabajos programados.

**Campos identificados:**
- `Id`: Identificador

### 7. Datos_OT
Datos adicionales de órdenes de trabajo.

**Campos identificados:**
- `OT`: Orden de trabajo

## Consultas (Queries)

### Consulta mediciones OT
Consulta que relaciona las mediciones con las órdenes de trabajo mediante el campo `id_OT`.

## Campos Calculados

### COSTE_TOTAL
```
COSTE_TOTAL = [PRECIO UNIDAD] * [CANTIDAD]
```
Calcula el coste total multiplicando el precio unitario por la cantidad.

### IMPORTE
Campo para almacenar importes totales de certificaciones.

### Suma_De_COSTE_TOTAL
Agregación que suma todos los costes totales.

## Tipos de Redes Gestionadas

1. **Distribución (red en alta)**: Red de distribución de agua potable
2. **Saneamiento**: Red de alcantarillado y saneamiento

## Formularios Identificados

### Certificaciones Llodio
Formulario para gestionar certificaciones específicas de Llodio.

**Elementos del formulario:**
- Cuadros combinados (dropdowns) para selección de datos
- Comandos/botones numerados (Comando1, Comando4, Comando9, etc.)
- Etiquetas para campos como CANTIDAD, COSTE_TOTAL, PRECIO_UNIDAD
- Secciones: EncabezadoDelFormulario, PieDelFormulario

## Informes Identificados

Se detectaron múltiples informes con estructura estándar:
- **EncabezadoDelInforme** (Encabezado)
- **PieDelInforme** (Pie de página)

Informes mencionados:
- Informes de Abastecimiento
- Informes de Saneamiento
- Certificaciones por municipio

## Tipos de Trabajos Detectados

Ejemplos de trabajos encontrados en la base de datos:
- Acometida de agua potable a barraqueros
- Restablecer sector centro norte (Llodio)
- Trabajos de digitalización
- Trabajos de gestión
- Excavación y colocación de materiales

## Personal/Usuarios Detectados

Nombres que podrían ser técnicos o usuarios del sistema:
- Eduardo
- Elena
- Emilio
- Eneko

## Observaciones Técnicas

1. **Relaciones entre tablas**:
   - LISTADO OTS (1) → MEDICIONES OTS (N) mediante id_OT
   - MEDICIONES OTS → PRECIOS UNITARIOS mediante CODIGO_MAT

2. **Cálculos automáticos**:
   - La base de datos calcula automáticamente costes totales
   - Incluye funciones de agregación (SUM) para totales

3. **Geolocalización**:
   - Las órdenes de trabajo incluyen coordenadas X/Y y Latitud/Longitud
   - Permite mapeo de trabajos realizados

4. **Sistema de capítulos**:
   - Los precios están organizados por capítulos
   - Facilita la organización de presupuestos

## Funcionalidad Principal

La base de datos permite:
1. Registrar órdenes de trabajo con ubicación geográfica
2. Asociar mediciones y materiales a cada OT
3. Calcular costes automáticamente basados en precios unitarios
4. Generar certificaciones por municipio
5. Diferenciar entre trabajos de distribución y saneamiento
6. Hacer seguimiento del estado de finalización
7. Generar informes de abastecimiento y saneamiento

## Recomendaciones

1. **Documentación**: Crear un manual de usuario detallado
2. **Backup**: Implementar copias de seguridad regulares (la base de datos ya pesa 15MB)
3. **Migración**: Considerar migrar a un sistema más robusto (SQL Server, PostgreSQL) si el volumen crece
4. **Validación**: Implementar validaciones en los formularios para evitar datos inconsistentes
5. **Auditoría**: Añadir campos de auditoría (usuario, fecha de creación/modificación)
6. **Índices**: Revisar índices en campos clave para mejorar rendimiento
7. **Normalización**: Verificar que no exista redundancia de datos

## Conclusión

La base de datos está diseñada para gestionar de manera integral las certificaciones de trabajos realizados en redes de agua y saneamiento de múltiples municipios de Álava. Incluye gestión de:
- Órdenes de trabajo geolocalizadas
- Mediciones y materiales
- Precios unitarios
- Cálculo automático de costes
- Generación de certificaciones e informes

La estructura parece adecuada para su propósito, aunque podría beneficiarse de algunas mejoras técnicas para escalabilidad y mantenimiento a largo plazo.
