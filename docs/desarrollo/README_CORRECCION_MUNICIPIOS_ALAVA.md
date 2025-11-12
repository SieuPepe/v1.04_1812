# Corrección de Municipios de Álava en dim_municipios

## Resumen del Problema

Se detectaron **problemas graves** en los datos de municipios de Álava en la tabla `dim_municipios`:

### Estadísticas de Errores
- **Total de problemas encontrados:** 39
- **Municipios que faltaban:** 5
- **Códigos incorrectos (no existen en INE):** 4
- **Municipios con códigos desplazados:** 30

## Problemas Detectados

### 1. Municipios que Faltaban
Códigos INE que no estaban en la base de datos:
- `01039` - Moreda de Álava/Moreda Araba
- `01055` - Valdegovía/Gaubea
- `01063` - Zuia
- `01901` - Iruña Oka/Iruña de Oca (código especial)
- `01902` - Lantarón (código especial)

### 2. Códigos Incorrectos
Códigos que NO existen en el INE pero estaban en la base de datos:
- `01024` (debería ser `01056` para Harana/Valle de Arana)
- `01025` (debería ser `01901` para Iruña Oka/Iruña de Oca)
- `01026` (debería ser `01027` para Iruraiz-Gauna)
- `01035` (debería ser `01036` para Laudio/Llodio)

### 3. Desplazamiento Sistemático
El problema más grave era un **desplazamiento sistemático** donde los nombres de municipios estaban asignados a códigos incorrectos. Por ejemplo:

| Código | ❌ Nombre Incorrecto (antes) | ✅ Nombre Correcto (INE) |
|--------|------------------------------|--------------------------|
| 01004  | Armiñón                      | Artziniega               |
| 01006  | Arraia-Maeztu                | Armiñón                  |
| 01018  | Vitoria-Gasteiz              | Zigoitia                 |
| 01019  | Zigoitia                     | Kripan                   |
| 01020  | Elburgo/Burgelu              | Kuartango                |
| 01059  | Legutiano                    | Vitoria-Gasteiz          |

## Fuente de Datos Oficial

Los datos correctos se obtuvieron del **Instituto Nacional de Estadística (INE)**:
- Fuente: Relación de municipios y códigos por provincias (enero 2025)
- Repositorio verificado: https://github.com/codeforspain/ds-organizacion-administrativa
- Total de municipios oficiales en Álava: **51**

## Códigos de Provincia

Confirmados según especificación:
- **provincia_id = 1** → Álava/Araba
- **provincia_id = 2** → Bizkaia
- **provincia_id = 3** → Gipuzkoa

## Solución Aplicada

### Archivos Modificados

1. **`script/sql/corregir_municipios_alava.sql`** (NUEVO)
   - Script de corrección que elimina todos los registros de Álava
   - Inserta los 51 municipios con códigos INE oficiales
   - Incluye verificación del resultado

2. **`script/sql/fase3_dim_municipios.sql`** (ACTUALIZADO)
   - Corregida la sección de municipios de Álava
   - Ahora usa códigos INE oficiales
   - Documentación mejorada con distribución por cuadrillas

### Distribución por Cuadrillas/Comarcas

Los 51 municipios se distribuyen así:
- **Cuadrilla de Vitoria** (comarca_id=3): 19 municipios
- **Cuadrilla de Ayala** (comarca_id=1): 7 municipios
- **Cuadrilla de Laguardia/Rioja Alavesa** (comarca_id=2): 18 municipios
- **Cuadrilla de Añana** (comarca_id=5): 6 municipios
- **Cuadrilla de Campezo** (comarca_id=6): 1 municipio

## Cómo Aplicar la Corrección

### Opción 1: Script de Corrección Específico
```bash
mysql -u usuario -p nombre_bd < script/sql/corregir_municipios_alava.sql
```

### Opción 2: Regenerar Toda la Tabla
```bash
# Ejecutar el script completo actualizado
mysql -u usuario -p nombre_bd < script/sql/fase3_dim_municipios.sql
```

## Verificación Post-Corrección

Después de aplicar la corrección, verificar:

```sql
-- Verificar total de municipios de Álava
SELECT COUNT(*) as total FROM dim_municipios WHERE provincia_id = 1;
-- Debe retornar: 51

-- Verificar que no hay códigos incorrectos
SELECT codigo_ine, nombre FROM dim_municipios
WHERE provincia_id = 1
AND codigo_ine IN (1024, 1025, 1026, 1035);
-- Debe retornar: 0 filas

-- Verificar códigos especiales
SELECT codigo_ine, nombre FROM dim_municipios
WHERE provincia_id = 1
AND codigo_ine IN (1901, 1902);
-- Debe retornar: 2 filas (Iruña Oka y Lantarón)

-- Verificar un municipio específico
SELECT codigo_ine, nombre FROM dim_municipios
WHERE codigo_ine = 1059;
-- Debe retornar: 01059 - Vitoria-Gasteiz (NO "Legutiano")
```

## Impacto en el Sistema

### Posibles Problemas Derivados
Si ya había datos vinculados a municipios con códigos incorrectos:

1. **Partes de trabajo** podrían estar asociados a municipios incorrectos
2. **Informes por municipio** mostrarían datos erróneos
3. **Estadísticas geográficas** estarían distorsionadas

### Recomendaciones
1. ✅ **Aplicar la corrección lo antes posible**
2. ⚠️ **Revisar datos existentes** que referencien municipios de Álava
3. 📊 **Regenerar informes** que incluyan datos por municipio
4. 🔍 **Auditar registros** creados antes de la corrección

## Prevención Futura

Para evitar este tipo de problemas:
1. ✅ Siempre verificar códigos INE contra fuente oficial
2. ✅ Usar archivos de datos oficiales del INE
3. ✅ Implementar validaciones en la aplicación
4. ✅ Crear tests automatizados que verifiquen códigos INE

---

**Última actualización:** 2025-11-10
**Fuente de datos:** INE - Relación de municipios (enero 2025)
