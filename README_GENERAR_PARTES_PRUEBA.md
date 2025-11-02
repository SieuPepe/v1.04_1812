# 🔧 Generador de 1000 Partes Aleatorias para Pruebas

## 📋 Descripción

Script Python para generar **1000 partes aleatorias** con datos realistas distribuidos entre:
- ✅ **Todos los estados**: Pendiente, En curso, Finalizado, Cerrado
- ✅ **Todas las provincias**: Álava, Bizkaia, Gipuzkoa
- ✅ **Todos los municipios**: 251 municipios del País Vasco
- ✅ **Todas las redes**: Distribución uniforme
- ✅ **Todos los tipos de trabajo**: Distribución uniforme
- ✅ **Coordenadas GPS realistas**: Dentro de los límites del País Vasco

## 🎯 Propósito

Generar datos de prueba para validar el **Sistema de Informes** con:
- Filtros dinámicos
- Clasificaciones por provincia, estado, tipo de trabajo
- Exportaciones a Excel, Word, PDF
- Visualización de grandes volúmenes de datos

---

## 🚀 Uso

### **Opción 1: Credenciales por defecto**

```bash
python generar_1000_partes.py
```

Usa credenciales por defecto:
- Usuario: `aperez`
- Password: `WGueXNk9`
- Schema: `cert_dev`
- Cantidad: 1000 partes

### **Opción 2: Credenciales personalizadas**

```bash
python generar_1000_partes.py <usuario> <password>
```

Ejemplo:
```bash
python generar_1000_partes.py miusuario mipassword
```

### **Opción 3: Cantidad personalizada**

```bash
python generar_1000_partes.py <usuario> <password> <num_partes>
```

Ejemplo para generar 500 partes:
```bash
python generar_1000_partes.py aperez WGueXNk9 500
```

---

## 📊 Distribución de Datos

### **Estados (distribución realista)**
- 🟡 **Pendiente**: 30% (~300 partes)
- 🔵 **En curso**: 35% (~350 partes)
- 🟢 **Finalizado**: 25% (~250 partes)
- ⚫ **Cerrado**: 10% (~100 partes)

### **Provincias**
- Distribución uniforme entre las 3 provincias
- ~333 partes por provincia

### **Municipios**
- Distribución aleatoria entre los 251 municipios
- Coordenadas GPS ajustadas a cada provincia

### **Fechas**
- **Fecha inicio**: Aleatoria entre 2023-01-01 y 2025-12-31
- **Fecha prevista fin**: 7-90 días después de inicio
- **Fecha fin**: Solo si estado es "Finalizado" o "Cerrado"
- Lógica temporal respetada: inicio < prevista < fin

### **Coordenadas GPS (WGS84)**
- **Álava**: lat 42.5-43.1, lon -3.2 a -2.4
- **Bizkaia**: lat 43.0-43.5, lon -3.2 a -2.6
- **Gipuzkoa**: lat 43.0-43.4, lon -2.3 a -1.7

---

## 📝 Campos Generados

Cada parte incluye:

| Campo | Tipo | Ejemplo |
|-------|------|---------|
| **titulo** | Texto | "Reparación de tubería #42" |
| **descripcion** | Texto | "Trabajos de mantenimiento en la red de distribución" |
| **descripcion_corta** | Texto | Primeros 100 caracteres de descripción |
| **descripcion_larga** | Texto | Descripción + metadata de generación |
| **estado** | Enum | Pendiente / En curso / Finalizado / Cerrado |
| **fecha_inicio** | Date | Aleatoria 2023-2025 |
| **fecha_fin** | Date | Solo si Finalizado o Cerrado |
| **fecha_prevista_fin** | Date | inicio + 7-90 días |
| **provincia_id** | Int | 1 (Álava), 2 (Bizkaia), 3 (Gipuzkoa) |
| **municipio_id** | Int | ID de municipio válido de la provincia |
| **red_id** | Int | ID de red existente en dim_red |
| **tipo_trabajo_id** | Int | ID de tipo existente en dim_tipo_trabajo |
| **cod_trabajo_id** | Int | ID de código existente en dim_codigo_trabajo |
| **trabajadores** | Texto | "Juan Pérez, Carlos García" |
| **localizacion** | Texto | "Calle Mayor, 42" |
| **latitud** | Float | Coordenada GPS ajustada a provincia |
| **longitud** | Float | Coordenada GPS ajustada a provincia |
| **codigo** | String | Generado automáticamente (OT/GF/TP-AAAA-NNNN) |

---

## ⚡ Tiempo de Ejecución

**Estimado:**
- 1000 partes: ~3-5 minutos (depende de la velocidad de la BD)
- Progreso cada 50 partes
- Mensajes de estado en tiempo real

**Ejemplo de salida:**
```
================================================================================
🔧 GENERADOR DE 1000 PARTES ALEATORIAS
================================================================================

Conectando a schema: cert_dev
Usuario: aperez

📊 Obteniendo dimensiones de la base de datos...
  ✅ Redes disponibles: 3
  ✅ Tipos de trabajo: 4
  ✅ Códigos de trabajo: 5
  ✅ Provincias: 3
  ✅ Municipios provincia 1: 51
  ✅ Municipios provincia 2: 112
  ✅ Municipios provincia 3: 88

🚀 Generando 1000 partes aleatorias...

  ✅ Progreso: 50/1000 (5.0%) - Último: GF-2024-0050
  ✅ Progreso: 100/1000 (10.0%) - Último: OT-2024-0100
  ✅ Progreso: 150/1000 (15.0%) - Último: TP-2024-0150
  ...
  ✅ Progreso: 1000/1000 (100.0%) - Último: GF-2025-0234

================================================================================
🎉 GENERACIÓN COMPLETADA
================================================================================

✅ Partes creadas exitosamente: 998
❌ Errores: 2
📊 Tasa de éxito: 99.8%

📈 DISTRIBUCIÓN ESPERADA:
  • Estados:
    - Pendiente: ~300 partes (30%)
    - En curso: ~350 partes (35%)
    - Finalizado: ~250 partes (25%)
    - Cerrado: ~100 partes (10%)
  • Provincias: Distribuido uniformemente entre 3 provincias
  • Redes: Distribuido uniformemente entre 3 redes
  • Tipos de trabajo: Distribuido uniformemente entre 4 tipos

✨ ¡Listo para probar el sistema de informes!
================================================================================
```

---

## 🔍 Verificación

Después de ejecutar, puedes verificar en la aplicación:

1. **Gestión de Partes → Resumen**: Deberías ver 1000+ partes
2. **Informes**:
   - Filtrar por provincia → Deberías ver ~333 partes por provincia
   - Filtrar por estado "Pendiente" → Deberías ver ~300 partes
   - Clasificar por municipio → Deberías ver distribución variada

---

## 🛠️ Requisitos

- Python 3.7+
- Conexión a base de datos MySQL
- Módulos Python: `mysql-connector-python`

Instalar dependencias:
```bash
pip install mysql-connector-python
```

---

## ⚠️ Notas Importantes

1. **Schema**: El script usa `cert_dev` por defecto. Modifica la variable `SCHEMA` si necesitas otro schema.

2. **Duplicados**: El script puede generar duplicados si se ejecuta múltiples veces. No hay verificación de duplicados.

3. **Eliminación**: Si necesitas eliminar las partes de prueba, usa:
   ```sql
   DELETE FROM tbl_partes WHERE descripcion_larga LIKE '%Parte generada automáticamente para pruebas%';
   ```

4. **Dimensiones requeridas**: El script necesita que existan registros en:
   - `dim_red`
   - `dim_tipo_trabajo`
   - `dim_codigo_trabajo`
   - `dim_provincias`
   - `dim_comarcas`
   - `dim_municipios`

---

## 📧 Soporte

Si encuentras errores durante la generación:
- Verifica que las credenciales sean correctas
- Verifica que el schema exista
- Verifica que las tablas de dimensiones tengan datos
- Revisa los primeros 10 mensajes de error para identificar problemas

---

**¡Listo para generar datos de prueba!** 🎉
