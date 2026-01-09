# Changelog - HydroFlow Manager

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

---

## [1.05] - 2026-01-09

### ✨ Añadido

#### Documentación de Usuario
- **Manual de Usuario en PDF** (180 KB) - Guía completa de todas las funcionalidades
- **Manual de Informes en PDF** (170 KB) - Documentación exhaustiva del generador de informes
- **Guía Técnica en PDF** (194 KB) - Manual técnico para administradores
- **Accesos directos en menú de inicio** para acceder a los manuales
- **Integración en menú de Ayuda** de la aplicación
- Script `convert_manuals_to_pdf.py` para regenerar PDFs desde Markdown

#### Sistema de Instalación
- Manuales integrados en el instalador (installer/HydroFlowManager.iss)
- Accesos directos automáticos en el menú de inicio de Windows
- Apertura de manuales multiplataforma (Windows/macOS/Linux)

### 🔧 Cambiado
- Actualizada versión del instalador a v1.05
- Mejorados mensajes de error al abrir manuales
- Optimizada función de apertura de documentos PDF

### 📚 Documentación
- Generados PDFs profesionales con estilos mejorados
- CSS optimizado para impresión y visualización
- Formato consistente en todos los manuales

---

## [1.04] - 2025-11-12

### ✨ Añadido

#### Sistema de Informes Dinámicos
- **Generador de informes avanzado** con interfaz gráfica intuitiva
- **Filtros dinámicos** con operadores múltiples (Igual a, Mayor que, Menor que, Entre, Contiene)
- **Selector de fechas visual** (DateEntry/Calendar) para filtros de tipo "Entre"
- **Lógica AND/OR** configurable entre filtros múltiples
- **Clasificación de datos** (ordenamiento) por múltiples campos
- **Selección de campos** a mostrar en el informe
- **Vista previa** de resultados antes de exportar
- **Exportación múltiple**: Excel (.xlsx), Word (.docx), PDF
- **Guardar/Cargar configuraciones** de informes frecuentes
- **Gestión de configuraciones guardadas**: editar, eliminar, duplicar

#### Mejoras de Base de Datos
- Soporte para **dimensiones geográficas** (comarcas, municipios)
- **Auto-detección de columnas** para joins con tablas dimensionales
- Verificación de integridad de base de datos con script verificar_integridad_completa.py
- Scripts de migración y limpieza de datos geográficos

#### Infraestructura y Herramientas
- Script maestro fase1_preparacion_datos.py para preparación automatizada
- Scripts de backup y verificación de esquemas
- Generador de partes con validación de esquemas
- Sistema de validación de códigos OT y nomenclatura

### 🔧 Cambiado

#### Reorganización del Proyecto (FASE 2)
- Movidos **scripts de generación** a directorio tools/
- Movidos **scripts auxiliares** a directorio script/
- Reorganizada **documentación técnica** en docs/desarrollo/
- Creado directorio tools/ para herramientas de desarrollo
- Eliminados 11 archivos obsoletos (tests, pantallazos, temporales)

#### Mejoras de Configuración
- Creado .env.produccion.template con configuración para cliente
- Documentación de variables de entorno mejorada
- Configuración centralizada en script/db_config.py

#### Base de Datos
- Actualizada nomenclatura de columnas geográficas (comarca_nombre, municipio_nombre)
- Mejorada estructura de dim_municipios para Álava
- Agregados códigos postales a municipios

### 🐛 Corregido

- Corregidos errores SQL en verificador de integridad
- Restringido generador de partes solo a esquemas válidos
- Corregido campo nombre a municipio_nombre en scripts SQL
- Corregidos scripts de dim_municipios y códigos postales
- Solucionados problemas de importación de dependencias (tkcalendar, openpyxl)

### 📚 Documentación

#### Nuevos Documentos
- README_PLAN_IMPLEMENTACION.md - Plan completo de implementación (6 fases)
- PLAN_PASO_A_PRODUCCION.md - Plan detallado para paso a producción
- FASE1_PREPARACION_DATOS.md - Documentación de FASE 1
- PRECIO_UNIT_EXPLICACION.md - Explicación del sistema de precios
- tools/README.md - Documentación de herramientas
- docs/desarrollo/README.md - Índice de documentación técnica

#### Documentos Reorganizados
- Movidos a docs/desarrollo/:
  - README_BUILD.md
  - ANALISIS_EXHAUSTIVO_INFORMES.md
  - ANALISIS_EXHAUSTIVO_COMPLETO.md
  - INSTRUCCIONES_IMPORTACION.md
  - PROBLEMA_Y_SOLUCION.md

### 🗑️ Eliminado

#### Archivos Obsoletos
- test_informes_completo.py - Test obsoleto
- run_parts_form.py - Script de desarrollo
- run_parts_simple.py - Script de desarrollo
- lista.txt - Archivo temporal
- 7 archivos Pantallazo*.jpg - Capturas de desarrollo

### 🔐 Seguridad

- Creado template de configuración sin credenciales hardcodeadas
- Documentadas mejores prácticas de permisos de base de datos
- Instrucciones para crear usuario no-root en producción

### 📦 Dependencias

#### Nuevas Dependencias
- tkcalendar>=1.6.0 - Selector de fechas para informes
- openpyxl>=3.0.0 - Exportación a Excel
- python-docx>=0.8.0 - Exportación a Word
- reportlab>=3.6.0 - Exportación a PDF

---

## [1.03] - 2025-11-06

### Añadido
- Estructura base de documentación (docs/)
- Directorios para ADR, SQL, imágenes
- DEV_GUIDE.md - Guía de desarrollo inicial

### Cambiado
- Organización inicial del proyecto

---

## [1.02] - 2025-11-01

### Añadido
- Sistema base de gestión de partes
- Módulo de presupuestos
- Módulo de certificaciones
- Interfaz con customtkinter

### Cambiado
- Migración de tkinter estándar a customtkinter

---

## [1.01] - 2025-10-20

### Añadido
- Conexión a base de datos MySQL
- Sistema de login
- Gestión básica de proyectos

---

## [1.00] - 2025-10-15

### Añadido
- Versión inicial del proyecto
- Estructura de base de datos multi-esquema
- Arquitectura manager + proyectos individuales

---

## Tipos de Cambios

- ✨ Añadido - Nuevas características
- 🔧 Cambiado - Cambios en funcionalidad existente
- 🗑️ Eliminado - Características eliminadas
- 🐛 Corregido - Correcciones de bugs
- 🔐 Seguridad - Mejoras de seguridad
- 📚 Documentación - Cambios solo en documentación
- 📦 Dependencias - Cambios en dependencias

---

## Próximos Pasos (Roadmap)

### FASE 3: Desarrollo de Manuales (En Planificación)
- [ ] Manual de Usuario completo con capturas
- [ ] Manual de Informes detallado paso a paso
- [ ] Guía Técnica/Código
- [ ] Ventana "Acerca de" en la aplicación

### FASE 4: Empaquetado (En Planificación)
- [ ] Actualizar requirements.txt final
- [ ] Configurar PyInstaller (.spec)
- [ ] Compilar ejecutable standalone
- [ ] Crear instalador Windows (NSIS/Inno Setup)

### FASE 5: Datos Definitivos (En Planificación)
- [ ] Cargar datos reales del cliente
- [ ] Validación exhaustiva
- [ ] Backup de producción final

### FASE 6: Instalación Synology (En Planificación)
- [ ] Instalar MySQL en Synology NAS
- [ ] Configurar clientes Windows
- [ ] Capacitación de usuarios
- [ ] Puesta en producción

---

**Versión actual:** 1.04  
**Última actualización:** 2025-11-12  
**Próxima versión planeada:** 1.05 (Post-producción)
