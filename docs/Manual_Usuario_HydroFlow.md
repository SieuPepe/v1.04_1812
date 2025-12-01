# Manual de Usuario
## HydroFlow Manager v1.04

**Sistema de Gestión Integral para Proyectos Hidráulicos**

---

## Índice

1. [Introducción](#1-introducción)
2. [Inicio de Sesión](#2-inicio-de-sesión)
3. [Selección de Rol](#3-selección-de-rol)
4. [Panel de Usuario Técnico](#4-panel-de-usuario-técnico)
5. [Panel de Administrador de Proyecto](#5-panel-de-administrador-de-proyecto)
6. [Generador de Partes](#6-generador-de-partes)
7. [Gestión de Presupuestos](#7-gestión-de-presupuestos)
8. [Gestión de Inventario](#8-gestión-de-inventario)
9. [Certificaciones](#9-certificaciones)
10. [Preguntas Frecuentes](#10-preguntas-frecuentes)

---

## 1. Introducción

### 1.1 ¿Qué es HydroFlow Manager?

HydroFlow Manager v1.04 es un sistema integral de gestión diseñado específicamente para proyectos de obras hidráulicas. Permite:

✅ **Gestión de proyectos** - Control completo de múltiples proyectos simultáneos
✅ **Registro de trabajos** - Partes y órdenes de trabajo detallados
✅ **Control presupuestario** - Presupuestos, certificaciones y seguimiento económico
✅ **Inventario técnico** - Catálogo de elementos hidráulicos y registros
✅ **Informes profesionales** - Generación de reportes personalizados

### 1.2 Requisitos del Sistema

**Software:**
- Windows 10/11 (64-bit)
- MySQL 8.0 o superior
- Conexión a base de datos configurada

**Acceso:**
- Usuario y contraseña proporcionados por el administrador
- Permisos asignados según rol (Técnico o Administrador)

---

## 2. Inicio de Sesión

### 2.1 Pantalla de Login

Al ejecutar HydroFlow Manager, verá la pantalla principal de inicio de sesión:

**[CAPTURA: Pantalla de login con campos usuario y contraseña]**

**Elementos de la pantalla:**
1. **Logo de la empresa** - Identificación visual
2. **Campo Usuario** - Ingrese su nombre de usuario
3. **Campo Contraseña** - Ingrese su contraseña (oculta con asteriscos)
4. **Botón Login** - Presione para acceder al sistema

### 2.2 Proceso de Acceso

**Paso 1:** Ejecute `HydroFlowManager.exe`

**Paso 2:** Ingrese sus credenciales
- **Usuario:** Su nombre de usuario asignado
- **Contraseña:** Su contraseña (sensible a mayúsculas/minúsculas)

**Paso 3:** Presione el botón **"Login"**

### 2.3 Posibles Errores

❌ **"Error de conexión a la base de datos"**
- Verifique que MySQL esté corriendo
- Contacte al administrador del sistema

❌ **"Usuario o contraseña incorrectos"**
- Verifique sus credenciales
- Asegúrese de no tener Bloq Mayús activado

❌ **"No tiene permisos para acceder"**
- Su usuario no tiene permisos asignados
- Contacte al administrador

---

## 3. Selección de Rol

### 3.1 Pantalla de Roles

Después de autenticarse correctamente, verá la pantalla de selección de rol:

**[CAPTURA: Pantalla con tres opciones de rol - Técnico, Administrador, Generador de Partes]**

### 3.2 Roles Disponibles

#### 🔧 **Técnico**
**¿Para quién?** Personal de campo que registra trabajos realizados

**Funciones:**
- Ver información de proyectos
- Registrar nuevos trabajos (partes)
- Consultar presupuestos
- Acceder a inventarios
- Generar informes básicos

**Limitaciones:**
- No puede modificar presupuestos base
- No puede crear nuevos proyectos
- No puede gestionar usuarios

---

#### 👔 **Administrador de Proyecto**
**¿Para quién?** Gestores y jefes de proyecto

**Funciones:**
- ✅ Todas las funciones de Técnico, más:
- Crear y gestionar proyectos
- Modificar presupuestos
- Crear y modificar certificaciones
- Gestión completa de catálogos
- Acceso a informes avanzados
- Exportación de datos

---

#### 📋 **Generador de Partes**
**¿Para quién?** Usuarios que solo necesitan crear partes/órdenes de trabajo

**Funciones:**
- Crear nuevos partes rápidamente
- Asignar recursos a partes
- Modificar partes existentes
- Consultar histórico de partes

**Limitaciones:**
- Solo acceso al generador de partes
- No accede a otras secciones

---

### 3.3 ¿Cómo Elegir?

**Seleccione el rol según su función:**
1. **Si registra trabajos en campo** → Técnico
2. **Si gestiona proyectos completos** → Administrador
3. **Si solo crea órdenes de trabajo** → Generador de Partes

Presione sobre la imagen del rol deseado para continuar.

---

## 4. Panel de Usuario Técnico

### 4.1 Selección de Proyecto

**[CAPTURA: Diálogo de selección de proyecto]**

Al acceder como Técnico, primero debe seleccionar el proyecto en el que trabajará:

1. Aparecerá un diálogo con la lista de proyectos disponibles
2. Seleccione el código del proyecto de la lista desplegable
3. Presione **"Abrir proyecto"**

### 4.2 Pantalla Principal

**[CAPTURA: Panel principal de usuario técnico con menú lateral]**

**Estructura de la pantalla:**

**Menú Lateral (izquierda):**
- 📊 Resumen del Proyecto
- 📁 Inventario
- 🔧 Catálogo de Piezas
- 💰 Presupuesto
- ✅ Certificaciones
- 📑 Informes

**Panel Central:**
- Contenido dinámico según sección seleccionada

**Encabezado:**
- Logo de la empresa
- Nombre del proyecto activo
- Usuario conectado

---

### 4.3 Resumen del Proyecto

**[CAPTURA: Vista de resumen con estadísticas]**

Muestra información general del proyecto:

**Datos Generales:**
- Código del proyecto
- Nombre del proyecto
- Cliente/empresa
- Fecha de inicio
- Provincia y municipio

**Estadísticas:**
- Total de partes registrados
- Partes pendientes
- Partes en curso
- Partes finalizados
- Presupuesto total
- Importe certificado
- Importe pendiente

---

### 4.4 Gestión de Inventario

#### 4.4.1 Crear Nuevo Registro

**[CAPTURA: Formulario de nuevo registro/arqueta]**

**Paso 1:** En el menú lateral, seleccione **"Inventario"**

**Paso 2:** Presione el botón **"+ Nuevo Registro"**

**Paso 3:** Complete el formulario:

**Campos Obligatorios:**
- **Municipio** - Seleccione de la lista desplegable
- **Descripción** - Describa el registro/arqueta

**Campos Opcionales:**
- **Elementos** - Añada elementos hidráulicos y no hidráulicos
- **Fotografías** - Cargue fotos del registro
- **Documentos PDF** - Adjunte planos o documentación

**Paso 4:** Presione **"Guardar"**

El sistema generará automáticamente un código único (ej: A-0001).

---

#### 4.4.2 Añadir Elementos al Registro

**[CAPTURA: Interfaz de selección de elementos]**

Al crear o editar un registro, puede añadir elementos:

**Elementos No Hidráulicos:**
1. Presione el botón **"Añadir Elementos"**
2. Seleccione **"Elemento No Hidráulico"**
3. Elija el **Tipo** (ej: Tapa, Marco)
4. Seleccione el **Modelo**
5. Ingrese la **Cantidad**
6. Presione **"Añadir"**

**Elementos Hidráulicos:**
1. Seleccione **"Elemento Hidráulico"**
2. Elija la **Familia** (ej: Válvulas, Hidrantes)
3. Seleccione el **Tipo de Elemento** (se filtra según familia)
4. Elija la **Marca**
5. Especifique el **Modelo**
6. Ingrese la **Cantidad**
7. Presione **"Añadir"**

**Vista de Elementos Añadidos:**
- Tabla con todos los elementos del registro
- Botón **"Eliminar"** para quitar elementos
- Actualización automática de cantidades

---

#### 4.4.3 Cargar Fotografías

**[CAPTURA: Ventana de carga de fotografías]**

**Paso 1:** En el formulario de registro, presione **"Añadir Imagen"**

**Paso 2:** Navegue y seleccione la imagen (formatos: JPG, PNG, BMP)

**Paso 3:** La imagen se cargará automáticamente

**Funcionalidades:**
- **Navegación:** Botones "Anterior" / "Siguiente"
- **Indicador:** Muestra "Imagen X de Y"
- **Vista previa:** Ajuste automático al tamaño de ventana
- **Múltiples imágenes:** Añada todas las necesarias

---

### 4.5 Catálogo de Piezas

El catálogo permite consultar y agregar elementos al sistema.

#### 4.5.1 Catálogo Hidráulico

**[CAPTURA: Listado de catálogo hidráulico]**

**Visualización:**
- Tabla con todos los elementos hidráulicos disponibles
- Filtros por Familia, Tipo, Marca
- Búsqueda por texto

**Agregar Nuevo Elemento:**

**[CAPTURA: Formulario de nuevo elemento hidráulico]**

1. Presione **"+ Añadir Elemento Hidráulico"**
2. Complete los campos:
   - **Familia** - Categoría principal
   - **Tipo** - Tipo específico dentro de familia
   - **Marca** - Fabricante
   - **Modelo** - Referencia del modelo
   - **Presión Nominal** - En bar
   - **Temperatura** - Rango de trabajo
   - **Diámetro** - En mm
   - **Descripción Técnica** - Características
   - **Precio** - Coste unitario
3. Presione **"Guardar"**

---

#### 4.5.2 Catálogo de Registros

**[CAPTURA: Listado de catálogo de registros]**

Similar al catálogo hidráulico pero para registros/arquetas:

**Campos:**
- Tipo de Registro
- Modelo
- Material
- Dimensiones
- Profundidad
- Capacidad
- Norma aplicable
- Precio

---

### 4.6 Presupuestos

#### 4.6.1 Visualización de Presupuesto

**[CAPTURA: Vista de presupuesto base con capítulos y partidas]**

**Estructura jerárquica:**
```
📁 Capítulo PA001 - Obra Civil
  ├─ Partida 01.001 - Excavación manual
  ├─ Partida 01.002 - Relleno con material seleccionado
  └─ ...
📁 Capítulo PA002 - Instalaciones
  ├─ Partida 02.001 - Tubería PVC DN 200
  └─ ...
```

**Información mostrada:**
- Código de partida
- Descripción
- Unidad de medida
- Cantidad
- Precio unitario
- Importe total

---

#### 4.6.2 Consulta de Precios

**Como Técnico, puede:**
✅ Ver presupuestos
✅ Consultar precios unitarios
✅ Buscar partidas específicas
✅ Exportar presupuestos

**No puede:**
❌ Modificar precios
❌ Añadir nuevas partidas al presupuesto base
❌ Eliminar partidas

---

### 4.7 Informes

**[CAPTURA: Panel de generación de informes]**

Permite generar reportes personalizados.

#### 4.7.1 Generar un Informe Básico

**Paso 1: Seleccionar Tipo de Informe**
- En el panel izquierdo, navegue por las categorías:
  - 📊 Partes
  - 📦 Recursos
  - 💰 Presupuestos
  - ✅ Certificaciones

**Paso 2: Configurar Filtros (opcional)**

**[CAPTURA: Panel de filtros]**

Añada filtros para personalizar el informe:
1. Presione **"+ Añadir Filtro"**
2. Seleccione el **Campo** (ej: Estado, Fecha, Red)
3. Elija el **Operador** (ej: Igual a, Mayor que, Contiene)
4. Ingrese el **Valor**
5. Presione **"Aplicar"**

**Paso 3: Seleccionar Campos**

**[CAPTURA: Panel de selección de campos]**

Marque las casillas de los campos que desea mostrar:
- ☑ Código
- ☑ Fecha
- ☑ Descripción
- ☐ Trabajadores
- ☑ Importe

**Paso 4: Ejecutar y Exportar**

1. Presione **"Generar Informe"**
2. Revise la vista previa
3. Presione **"Exportar"** y elija formato:
   - 📄 PDF
   - 📊 Excel
   - 📝 Word

---

## 5. Panel de Administrador de Proyecto

### 5.1 Acceso al Panel

**[CAPTURA: Pantalla principal de administrador]**

Como Administrador, tiene acceso completo al sistema.

**Menú Principal:**
- ➕ Nuevo Proyecto
- 🔧 Gestión de Proyectos
- 👥 Usuarios
- ✅ Certificaciones
- 📊 Informes

---

### 5.2 Crear Nuevo Proyecto

**[CAPTURA: Formulario de nuevo proyecto]**

**Paso 1:** En el menú principal, seleccione **"Nuevo Proyecto"**

**Paso 2:** Complete los datos del proyecto:

**Información General:**
- **Código del Proyecto** - Auto-generado (ej: PR001)
- **Nombre del Proyecto** - Denominación completa
- **Cliente/Empresa** - Seleccione o cree nuevo
- **Provincia** - Ubicación
- **Municipio** - Localidad principal

**Información Contractual:**
- **Fecha de Inicio** - Inicio del contrato
- **Fecha de Fin** - Fin previsto
- **Presupuesto Total** - Importe contratado

**Información Técnica:**
- **Tipo de Obra** - Agua potable, Saneamiento, etc.
- **Red** - Red 1, Red 2, etc.
- **Descripción** - Detalles del proyecto

**Paso 3:** Presione **"Crear Proyecto"**

El sistema creará automáticamente:
- Esquema de base de datos del proyecto
- Estructura de tablas
- Vistas a catálogos compartidos
- Permisos iniciales

---

### 5.3 Gestión de Proyectos Existentes

**[CAPTURA: Selector de proyectos]**

**Paso 1:** Seleccione **"Gestión de Proyectos"**

**Paso 2:** Elija el proyecto de la lista

**Paso 3:** Acceda al panel de gestión del proyecto

**[CAPTURA: Panel de gestión con pestañas]**

**Pestañas disponibles:**
1. **Resumen** - Vista general y estadísticas
2. **Inventario** - Gestión completa de registros
3. **Catálogo de Piezas** - Mantenimiento de catálogos
4. **Presupuesto** - Gestión presupuestaria completa
5. **Certificaciones** - Control de certificaciones

---

### 5.4 Gestión de Presupuestos (Administrador)

#### 5.4.1 Crear Presupuesto Base

**[CAPTURA: Interfaz de presupuesto vacío]**

**Paso 1: Crear Capítulos**

1. Presione **"+ Añadir Capítulo"**
2. Complete:
   - **Código** - (ej: PA001, PA002)
   - **Nombre** - (ej: "Obra Civil", "Instalaciones")
   - **Descripción** - Detalle del capítulo
3. Presione **"Guardar"**

---

**Paso 2: Añadir Partidas al Capítulo**

**[CAPTURA: Formulario de nueva partida]**

1. Seleccione el capítulo
2. Presione **"+ Añadir Partida"**
3. Complete los datos:

   **Identificación:**
   - **Código de Partida** - (ej: 01.001, 01.002)
   - **Descripción** - Trabajo a realizar

   **Clasificación:**
   - **Naturaleza** - Tipo de costo (M.O., Material, Maquinaria)
   - **Unidades** - Unidad de medida (m³, ml, ud, m²)

   **Economía:**
   - **Cantidad** - Medición contratada
   - **Precio Unitario** - Coste por unidad
   - **Importe** - Se calcula automáticamente (Cantidad × Precio)

4. Presione **"Guardar"**

---

**Paso 3: Crear Grupos de Partidas (opcional)**

**[CAPTURA: Formulario de grupo de partidas]**

Los grupos permiten agrupar partidas relacionadas:

1. Presione **"+ Crear Grupo"**
2. Complete:
   - **Código** - Auto-generado (PA0001)
   - **Nombre del Grupo** - (ej: "Acometidas Domiciliarias")
   - **Descripción** - Qué incluye
3. Presione **"Guardar"**

4. Añada ítems al grupo:
   - Similar a añadir partidas
   - Los ítems pertenecen solo al grupo

---

#### 5.4.2 Modificar Presupuesto

**[CAPTURA: Edición de partida existente]**

Para modificar una partida:
1. Seleccione la partida en la tabla
2. Presione **"Editar"**
3. Modifique los campos necesarios
4. Presione **"Guardar Cambios"**

**Puede modificar:**
- ✅ Descripción
- ✅ Cantidad
- ✅ Precio unitario
- ✅ Naturaleza y unidades

**No puede modificar:**
- ❌ Código de partida (identificador único)
- ❌ Capítulo (debe eliminar y recrear)

---

#### 5.4.3 Importar Presupuesto

**[CAPTURA: Diálogo de importación]**

Puede importar presupuestos desde archivos externos:

1. Presione **"Importar"**
2. Seleccione el archivo (Excel, CSV)
3. Mapee las columnas:
   - Código → Columna A
   - Descripción → Columna B
   - Cantidad → Columna C
   - Precio → Columna D
4. Presione **"Importar Datos"**
5. Revise el resultado

---

### 5.5 Gestión de Usuarios

**[CAPTURA: Panel de gestión de usuarios]**

Como Administrador, puede gestionar usuarios de la base de datos.

#### 5.5.1 Crear Nuevo Usuario

**[CAPTURA: Formulario de nuevo usuario]**

**Paso 1:** Presione **"+ Nuevo Usuario"**

**Paso 2:** Complete el formulario:

**Credenciales:**
- **Nombre de Usuario** - Login del usuario
- **Contraseña** - Mínimo 8 caracteres
- **Confirmar Contraseña** - Debe coincidir

**Permisos:**
- **Rol** - Técnico o Administrador
- **Proyectos Accesibles** - Marque los proyectos a los que tendrá acceso

**Datos Personales (opcionales):**
- Nombre completo
- Email
- Teléfono

**Paso 3:** Presione **"Crear Usuario"**

---

#### 5.5.2 Modificar Permisos

**[CAPTURA: Edición de permisos de usuario]**

Para cambiar permisos de un usuario existente:

1. Seleccione el usuario de la lista
2. Presione **"Editar Permisos"**
3. Modifique:
   - Rol
   - Proyectos accesibles
   - Estado (Activo/Inactivo)
4. Presione **"Guardar Cambios"**

---

## 6. Generador de Partes

### 6.1 Acceso al Generador

**[CAPTURA: Pantalla principal del generador de partes]**

El Generador de Partes es una herramienta especializada para crear órdenes de trabajo rápidamente.

**Estructura:**
- **Botón destacado:** "➕ Añadir Parte" (verde)
- **Tabla de partes:** Lista de todos los partes creados
- **Filtros:** Búsqueda y filtrado rápido
- **Pestañas:** Resumen, Partes, Presupuesto, Certificaciones, Informes, Ayuda

---

### 6.2 Crear un Nuevo Parte

**[CAPTURA: Formulario de nuevo parte]**

**Paso 1:** Presione el botón verde **"➕ Añadir Parte"**

**Paso 2:** Complete los campos obligatorios:

**Información Básica:**
- **Red** ⚡ OBLIGATORIO - Tipo de red (Red 1, Red 2, etc.)
- **Tipo de Trabajo** ⚡ OBLIGATORIO - (Reparación, Instalación, Mantenimiento)
- **Código de Trabajo** ⚡ OBLIGATORIO - Clasificación del trabajo

**Código Auto-generado:**
- El sistema generará automáticamente un código único
- Formato: `[Red]-[Tipo]-[Número]` (ej: R1-REP-0001)

---

**Información Adicional (opcional pero recomendada):**

**Descripción:**
- **Título** - Nombre corto del trabajo
- **Descripción** - Detalle completo del trabajo realizado

**Localización:**
- **Provincia** - Ubicación
- **Comarca** - Comarca
- **Municipio** - Municipio específico
- **Localización** - Dirección o punto de referencia
- **Coordenadas GPS** - Latitud y Longitud (si disponible)

**Fechas:**
- **Fecha de Inicio** - Cuándo comenzó el trabajo
- **Fecha de Fin** - Cuándo finalizó

**Estado:**
- **Pendiente** - Aún no iniciado
- **En Curso** - Actualmente en ejecución
- **Finalizado** - Trabajo completado

**Personal:**
- **Trabajadores** - Nombres del personal asignado

---

**Paso 3:** Presione **"Guardar"**

El parte se creará y aparecerá en la lista principal.

---

### 6.3 Modificar un Parte

**[CAPTURA: Edición de parte existente]**

Para editar un parte ya creado:

1. En la tabla de partes, seleccione el parte a modificar
2. Doble clic o botón **"Editar"**
3. Modifique los campos necesarios
4. Presione **"Guardar Cambios"**

---

### 6.4 Añadir Recursos a un Parte

**[CAPTURA: Asignación de recursos a parte]**

Para asignar partidas del presupuesto al parte:

**Paso 1:** Seleccione el parte

**Paso 2:** Presione **"Añadir Recursos"**

**Paso 3:** Aparecerá el listado de partidas del presupuesto

**Paso 4:** Para cada partida a añadir:
1. Seleccione la partida
2. Ingrese la **Cantidad** ejecutada
3. Presione **"Añadir"**

**Vista de Recursos Asignados:**
- Tabla con todas las partidas del parte
- Cantidades asignadas
- Importes calculados automáticamente
- Botón **"Eliminar"** para quitar recursos

---

### 6.5 Buscar y Filtrar Partes

**[CAPTURA: Barra de búsqueda y filtros]**

**Búsqueda Rápida:**
- Campo de texto en la parte superior
- Escriba: código, descripción, red, tipo
- La tabla se filtrará automáticamente

**Filtros Avanzados:**
1. Presione **"Filtros"**
2. Configure filtros por:
   - Estado (Pendiente, En Curso, Finalizado)
   - Red
   - Tipo de Trabajo
   - Rango de fechas
   - Municipio
3. Presione **"Aplicar Filtros"**

---

### 6.6 Vista de Resumen

**[CAPTURA: Pestaña de resumen con estadísticas]**

La pestaña **"Resumen"** muestra:

**Estadísticas Generales:**
- Total de partes
- Partes por estado (gráfico de tarta)
- Partes por red (gráfico de barras)
- Partes por mes (evolución temporal)

**Económicas:**
- Importe total presupuestado
- Importe total certificado
- Importe pendiente

---

## 7. Gestión de Presupuestos

### 7.1 Estructura del Presupuesto

Un presupuesto en HydroFlow Manager se organiza jerárquicamente:

```
📁 PROYECTO
  └─ 📁 PRESUPUESTO BASE
      ├─ 📁 Capítulo PA001 - Obra Civil
      │   ├─ 📄 Partida 01.001 - Excavación
      │   ├─ 📄 Partida 01.002 - Relleno
      │   └─ 📦 Grupo PA0001 - Acometidas
      │       ├─ 📄 Item 1 - Zanja
      │       └─ 📄 Item 2 - Tubería
      ├─ 📁 Capítulo PA002 - Instalaciones
      │   ├─ 📄 Partida 02.001 - Tubería DN200
      │   └─ ...
      └─ ...
```

### 7.2 Componentes del Presupuesto

#### Capítulo
Agrupación principal de partidas relacionadas.

**Ejemplo:**
- PA001 - Obra Civil
- PA002 - Instalaciones Hidráulicas
- PA003 - Instalaciones Eléctricas

#### Partida
Unidad de trabajo específica con precio.

**Componentes:**
- Código (ej: 01.001)
- Descripción (ej: "Excavación mecánica en zanja")
- Unidad (m³, ml, ud, m²)
- Cantidad
- Precio unitario
- Importe = Cantidad × Precio

#### Grupo de Partidas
Conjunto de ítems relacionados (opcional).

**Uso típico:**
- Agrupar trabajos repetitivos
- Facilitar la gestión de trabajos similares

---

### 7.3 Naturaleza de Costos

**[CAPTURA: Selector de naturaleza]**

Cada partida debe clasificarse por naturaleza:

| Naturaleza | Descripción | Ejemplo |
|-----------|-------------|---------|
| **M.O.** | Mano de Obra | Instalador, Peón |
| **MAT** | Material | Tubería, Cemento |
| **MAQ** | Maquinaria | Excavadora, Camión |
| **AUX** | Auxiliares | Transporte, Limpieza |

---

### 7.4 Unidades de Medida

**[CAPTURA: Selector de unidades]**

Unidades estándar disponibles:

| Código | Descripción | Uso Típico |
|--------|-------------|-----------|
| **m³** | Metro cúbico | Excavación, Hormigón |
| **ml** | Metro lineal | Tubería, Cable |
| **m²** | Metro cuadrado | Pavimento, Pintura |
| **ud** | Unidad | Arquetas, Válvulas |
| **kg** | Kilogramo | Acero, Material |
| **t** | Tonelada | Áridos, Material pesado |
| **h** | Hora | Mano de obra, Maquinaria |
| **pa** | Partida alzada | Trabajo completo |

---

### 7.5 Exportar Presupuesto

**[CAPTURA: Opciones de exportación]**

Puede exportar el presupuesto en varios formatos:

**Paso 1:** En la vista de presupuesto, presione **"Exportar"**

**Paso 2:** Seleccione el formato:

**📄 PDF - Presupuesto Detallado**
- Todos los capítulos y partidas
- Mediciones y precios
- Totales por capítulo
- Total general

**📊 Excel - Datos Tabulados**
- Una fila por partida
- Todas las columnas
- Fácil de procesar

**📝 Word - Documento Editable**
- Tabla formateada
- Logos y encabezados
- Personalizable

---

## 8. Gestión de Inventario

### 8.1 ¿Qué es el Inventario?

El inventario registra todos los **elementos físicos** del proyecto:

- 🔧 Arquetas y registros
- 💧 Válvulas y elementos hidráulicos
- 📍 Ubicaciones georreferenciadas
- 📸 Fotografías y documentación

---

### 8.2 Crear un Registro Completo

**Ejemplo práctico:** Registro de una arqueta

**Paso 1: Información Básica**

**[CAPTURA: Formulario de registro con campos básicos]**

- **Código:** A-0025 (auto-generado)
- **Municipio:** Seleccionar de lista
- **Descripción:** "Arqueta de acometida en C/ Mayor nº 15"

---

**Paso 2: Añadir Elementos No Hidráulicos**

**[CAPTURA: Selector de elementos no hidráulicos]**

Añada elementos estructurales:

**Ejemplo:**
- **Tipo:** Tapa de Registro
  - **Modelo:** Tapa Fundición D-400
  - **Cantidad:** 1

- **Tipo:** Marco
  - **Modelo:** Marco Cuadrado 60x60
  - **Cantidad:** 1

---

**Paso 3: Añadir Elementos Hidráulicos**

**[CAPTURA: Selector de elementos hidráulicos]**

**Ejemplo 1: Válvula**
- **Familia:** Válvulas
- **Tipo:** Compuerta
- **Marca:** Belgicast
- **Modelo:** BC-150
- **Diámetro:** DN 150
- **Cantidad:** 1

**Ejemplo 2: Tubería**
- **Familia:** Tuberías
- **Tipo:** PVC
- **Marca:** Molecor
- **Modelo:** TOM DN 200 PN16
- **Cantidad:** 5 (metros)

---

**Paso 4: Cargar Fotografías**

**[CAPTURA: Visor de fotografías con navegación]**

1. Presione **"Añadir Imagen"**
2. Seleccione foto desde su equipo
3. Repita para todas las fotos necesarias
4. Use botones "Anterior"/"Siguiente" para navegar

**Recomendaciones:**
- ✅ Foto general del registro
- ✅ Detalle de elementos principales
- ✅ Estado antes de intervención
- ✅ Estado después de intervención

---

**Paso 5: Documentación PDF**

**[CAPTURA: Visor de PDFs]**

Si tiene planos o documentación:
1. Presione **"Añadir Documento PDF"**
2. Seleccione el archivo PDF
3. El sistema mostrará la primera página
4. Use navegación para ver todas las páginas

---

**Paso 6: Guardar**

Presione **"Guardar Registro"**

El registro quedará almacenado con:
- ✅ Código único
- ✅ Todos los elementos
- ✅ Fotografías (codificadas en base64)
- ✅ Documentos PDF
- ✅ Fecha de creación

---

### 8.3 Modificar Registro Existente

**[CAPTURA: Lista de registros con botón editar]**

Para modificar un registro:

1. En la lista de inventario, seleccione el registro
2. Presione **"Editar"**
3. Modifique los campos necesarios:
   - Descripción
   - Añadir/eliminar elementos
   - Añadir/eliminar fotos
4. Presione **"Guardar Cambios"**

---

### 8.4 Buscar Registros

**[CAPTURA: Barra de búsqueda de inventario]**

**Búsqueda por:**
- Código (ej: A-0025)
- Municipio
- Descripción (palabras clave)
- Elementos contenidos

**Filtros:**
- Por municipio
- Por tipo de registro
- Con/sin fotografías
- Por fecha de creación

---

## 9. Certificaciones

### 9.1 ¿Qué es una Certificación?

Una **certificación** es el documento que acredita la realización de trabajos y permite su facturación.

**Proceso:**
1. Se ejecutan trabajos (partes)
2. Se registran recursos utilizados
3. Se **certifica** el trabajo realizado
4. Se genera documento de certificación
5. Se factura al cliente

---

### 9.2 Certificación Individual

**[CAPTURA: Formulario de certificación individual]**

Para certificar un parte específico:

**Paso 1:** Acceda a **Certificaciones** → **Nueva Certificación**

**Paso 2:** Complete el formulario:

**Datos de la Certificación:**
- **Fecha de Certificación** - Fecha del certificado
- **Código del Parte** - Seleccione de la lista
- **Descripción** - (se carga automáticamente del parte)

**Recursos Certificados:**
El sistema mostrará todos los recursos del parte.

Para cada recurso:
- **Cantidad Presupuestada** - (informativo)
- **Cantidad a Certificar** - Ingrese cantidad ejecutada
- **Precio Unitario** - (informativo)
- **Importe** - Se calcula automáticamente

**Paso 3:** Revise los totales:
- Importe total presupuestado
- Importe a certificar
- Porcentaje de ejecución

**Paso 4:** Presione **"Guardar Certificación"**

---

### 9.3 Certificación por Lotes

**[CAPTURA: Interfaz de certificación por lotes]**

Para certificar múltiples partes simultáneamente:

**Paso 1:** Acceda a **Certificaciones** → **Certificación por Lotes**

**Paso 2:** Configure filtros:
- **Fecha de Certificación** - Fecha común para todos
- **Búsqueda** - Filtre partes por código, descripción, red

**Paso 3:** Tabla de partes:

**[CAPTURA: Tabla con selección múltiple]**

La tabla muestra:
- ☑ Checkbox de selección
- Código del parte
- Red
- Descripción
- Presupuesto
- Certificado previamente
- Pendiente

**Paso 4:** Seleccione partes a certificar:
- Click en checkbox para seleccionar individual
- Ctrl+Click para selección múltiple
- Puede seleccionar todos los visibles

**Paso 5:** Presione **"Certificar Seleccionados"**

**⚠️ ADVERTENCIA:**
```
Esta función certifica el PARTE COMPLETO al 100%.
Todos los recursos presupuestados del parte se
certificarán en su totalidad.
```

**Paso 6:** Confirme la acción

El sistema certificará automáticamente todos los partes seleccionados con la fecha indicada.

---

### 9.4 Consultar Certificaciones

**[CAPTURA: Listado de certificaciones]**

**Vista de certificaciones:**
- Tabla con todas las certificaciones realizadas
- Columnas:
  - Código de certificación
  - Fecha
  - Código del parte
  - Importe certificado
  - Estado

**Filtros disponibles:**
- Por fecha (rango)
- Por parte
- Por estado (Pendiente, Aprobada, Facturada)

---

### 9.5 Exportar Certificación

**[CAPTURA: Opciones de exportación de certificación]**

**Formatos disponibles:**

**📄 PDF - Certificación Oficial**
- Formato oficial de certificación
- Incluye:
  - Datos del proyecto
  - Datos del cliente
  - Listado de trabajos certificados
  - Importes parciales y totales
  - Firmas (si configuradas)

**📊 Excel - Detalle de Partidas**
- Una fila por partida certificada
- Columnas: Código, Descripción, Cantidad, Precio, Importe
- Fácil de procesar contablemente

---

### 9.6 Anular Certificación

**[CAPTURA: Confirmación de anulación]**

Si necesita anular una certificación:

**⚠️ PRECAUCIÓN:** Esta acción no se puede deshacer

**Paso 1:** Seleccione la certificación

**Paso 2:** Presione **"Anular Certificación"**

**Paso 3:** Confirme la acción

**Efectos:**
- ❌ La certificación se marca como anulada
- ↩️ Las cantidades certificadas vuelven a pendientes
- 📊 Se actualiza el estado del parte
- 📝 Queda registro de la anulación (auditoría)

---

## 10. Preguntas Frecuentes

### 10.1 Inicio de Sesión

**P: ¿Olvidé mi contraseña, qué hago?**

R: Contacte al administrador del sistema. Solo él puede resetear contraseñas por seguridad.

---

**P: ¿Por qué dice "Error de conexión a la base de datos"?**

R: Posibles causas:
1. MySQL no está corriendo → Contacte al administrador
2. Red sin conexión → Verifique su conexión
3. Servidor caído → Contacte soporte técnico

---

### 10.2 Partes y Trabajos

**P: ¿Puedo modificar un parte ya certificado?**

R: No directamente. Debe:
1. Anular la certificación
2. Modificar el parte
3. Volver a certificar

---

**P: ¿Cómo elimino un parte?**

R: Solo los Administradores pueden eliminar partes. Como Técnico, puede cambiar el estado a "Cancelado" pero no eliminarlo.

---

**P: ¿El código del parte se genera automáticamente?**

R: Sí. El formato es: `[Código Proyecto]-[Tipo Trabajo]-[Número Secuencial]`

Ejemplo: `PR001-REP-0025`

---

### 10.3 Presupuestos

**P: ¿Puedo añadir partidas que no están en el presupuesto base?**

R: Solo como Administrador. Los Técnicos solo pueden usar partidas existentes.

---

**P: ¿Cómo sé qué partida usar para cada trabajo?**

R: Consulte con el responsable del proyecto. Cada partida tiene una descripción detallada que indica su uso.

---

**P: ¿El precio unitario puede cambiar?**

R: Solo el Administrador puede modificar precios del presupuesto base.

---

### 10.4 Inventario

**P: ¿Es obligatorio cargar fotografías?**

R: No es obligatorio, pero es muy recomendable para:
- Documentar el estado inicial
- Justificar trabajos realizados
- Resolver reclamaciones

---

**P: ¿Qué tamaño pueden tener las fotos?**

R: El sistema acepta fotos de hasta 5 MB. Se recomienda:
- Resolución: 1920x1080 (Full HD)
- Formato: JPG
- Tamaño: 1-3 MB

---

**P: ¿Puedo eliminar una foto ya cargada?**

R: Sí, en modo edición del registro, puede eliminar fotos.

---

### 10.5 Certificaciones

**P: ¿Puedo certificar parcialmente un parte?**

R: Sí, en **Certificación Individual** puede especificar cantidades menores a las presupuestadas.

En **Certificación por Lotes**, se certifica el 100% del parte.

---

**P: ¿Qué pasa si certifico de más?**

R: El sistema permite certificar hasta el 100% de lo presupuestado. No puede exceder esa cantidad sin modificar primero el presupuesto.

---

**P: ¿Puedo certificar el mismo parte varias veces?**

R: Sí. Puede hacer certificaciones parciales sucesivas hasta alcanzar el 100% del presupuesto del parte.

---

### 10.6 Informes

**P: ¿Los informes se guardan automáticamente?**

R: No. Debe exportarlos en el formato deseado (PDF, Excel, Word). Puede guardar la **configuración** del informe para reutilizarla.

---

**P: ¿Puedo compartir configuraciones de informes con otros usuarios?**

R: Sí, exportando el archivo de configuración (.json) desde la carpeta `informes_guardados`.

---

**P: ¿El informe se actualiza automáticamente?**

R: No. Los informes se generan con los datos del momento de ejecución. Debe regenerar el informe para ver datos actualizados.

---

### 10.7 General

**P: ¿Hay límite de proyectos en el sistema?**

R: No hay límite técnico. Depende de la capacidad del servidor de base de datos.

---

**P: ¿Los datos están respaldados?**

R: Sí. El administrador debe realizar backups periódicos de la base de datos.

---

**P: ¿Puedo trabajar sin conexión a internet?**

R: Sí, si el servidor MySQL está en la red local. No requiere internet, solo conexión al servidor de base de datos.

---

**P: ¿Hay versión móvil o web?**

R: Actualmente solo versión de escritorio Windows. Versión web puede estar en desarrollo futuro.

---

**P: ¿Cómo reporto un error o sugiero una mejora?**

R: Contacte con el equipo de desarrollo a través del administrador del sistema.

---

## Apéndice A: Atajos de Teclado

| Atajo | Función |
|-------|---------|
| `Ctrl + N` | Nuevo registro (en contexto actual) |
| `Ctrl + S` | Guardar |
| `Ctrl + F` | Buscar |
| `Ctrl + P` | Imprimir/Exportar a PDF |
| `Ctrl + E` | Exportar |
| `Esc` | Cancelar/Cerrar ventana |
| `F1` | Ayuda |
| `F5` | Actualizar datos |

---

## Apéndice B: Glosario de Términos

**Parte:** Orden de trabajo que documenta una intervención específica.

**Certificación:** Documento que acredita trabajos realizados y autoriza su facturación.

**Partida:** Unidad de precio del presupuesto (ej: "Excavación mecánica").

**Capítulo:** Agrupación de partidas relacionadas en el presupuesto.

**Naturaleza:** Clasificación del tipo de costo (M.O., Material, Maquinaria).

**Registro:** Elemento físico inventariado (arqueta, válvula, etc.).

**Red:** Tipo de red (Red 1, Red 2, etc.) que clasifica los trabajos.

**OT:** Orden de Trabajo (sinónimo de Parte).

---

## Apéndice C: Contacto y Soporte

**Soporte Técnico:**
- Email: [email de soporte]
- Teléfono: [teléfono]
- Horario: Lunes a Viernes, 9:00 - 18:00

**Administrador del Sistema:**
- Contacte al responsable IT de su organización

**Documentación Adicional:**
- Manual de Informes (generación de reportes avanzados)
- Guía Técnica (para administradores)

---

**Fin del Manual de Usuario**

*HydroFlow Manager v1.04*
*Documento versión 1.0 - Noviembre 2025*
