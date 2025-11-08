# Informes Exhaustivos - Todas las Combinaciones Posibles

Este directorio contiene **124 archivos** que representan **TODAS** las combinaciones posibles de informes del sistema de reportes de HydroFlow Manager v1.04.

## 📊 Resumen Rápido

- **Total archivos:** 124 (103 CSV + 21 JSON)
- **Tamaño total:** 446 KB
- **Partes de prueba:** 200
- **Presupuesto total:** €5,101,724.96
- **Certificado:** €2,458,535.08 (48.19%)
- **Pendiente:** €2,643,189.88

## 📁 Estructura

```
informes_exhaustivos/
├── RESUMEN_GLOBAL.json                      Estadísticas globales
├── 01_sin_agrupacion/                       1 archivo
├── 02_agrupacion_simple/                    10 archivos
├── 03_agrupacion_doble/                     19 archivos
├── 04_agrupacion_triple/                    10 archivos
├── 05_filtrados/                            19 archivos
├── 06_filtros_combinados/                   24 archivos
└── 07_por_partidas/                         40 archivos
```

## 🎯 Categorías

### 1. Sin Agrupación (1 archivo)
- **Listado_Completo.csv:** 200 partes sin agrupar

### 2. Agrupación Simple - 1 campo (10 archivos)
- Por Mes, Año, Estado, Red, Tipo Trabajo
- Por Código Trabajo, Tipo Reparación
- Por Provincia, Comarca, Municipio

### 3. Agrupación Doble - 2 campos (19 archivos)
- **Temporales:** año×mes, año×estado, mes×estado, mes×provincia
- **Geográficas:** provincia×comarca, comarca×municipio
- **Operacionales:** estado×tipo, red×estado, tipo×provincia
- **19 combinaciones relevantes**

### 4. Agrupación Triple - 3 campos (10 archivos)
- **Máxima granularidad:** mes×provincia×estado (161 grupos)
- **Jerárquica:** provincia×comarca×municipio
- **Combinadas:** año×provincia×estado, mes×tipo×estado
- **10 combinaciones clave**

### 5. Filtrados (19 archivos)
- **Por Estado:** Pendiente, En curso, Finalizado (3 archivos)
- **Por Provincia:** 8 provincias (8 archivos)
- **Por Tipo Trabajo:** OT, GF, TP (3 archivos)
- **Por Red:** 5 redes (5 archivos)

### 6. Filtros Combinados (24 archivos)
- **Estado × Provincia:** 15 combinaciones
- **Estado × Tipo Trabajo:** 9 combinaciones

### 7. Por Partidas (40 archivos)
- **20 selecciones aleatorias** de partidas (5-20 por selección)
- **Cada selección:** 1 CSV + 1 JSON de metadatos

## 📈 Informes Destacados

### Top 5 por Granularidad

| Archivo | Grupos | Utilidad |
|---------|--------|----------|
| `Por_mes_provincia_estado.csv` | 161 | Máximo detalle temporal-geográfico |
| `Por_mes_tipo_trabajo_estado.csv` | 119 | Evolución mensual por tipo |
| `Por_mes_y_provincia.csv` | 115 | Serie temporal regional |
| `Por_año_mes_provincia.csv` | 115 | Histórico regional completo |
| `Por_provincia_tipo_trabajo_estado.csv` | 69 | Análisis regional operacional |

### Más Útiles para Dashboards

1. **RESUMEN_GLOBAL.json** - KPIs generales
2. **Por_Estado.csv** - Distribución de estados
3. **Por_Provincia.csv** - Distribución geográfica
4. **Por_mes.csv** - Evolución temporal
5. **Por_provincia_y_estado.csv** - Matriz región-estado

## 🚀 Cómo Usar

### Importar en Excel

```bash
# Cualquier archivo CSV se puede abrir directamente en Excel
# Separador: coma (,)
# Codificación: UTF-8
```

### Analizar con Python

```python
import pandas as pd
import json

# Leer resumen global
with open('RESUMEN_GLOBAL.json', 'r') as f:
    resumen = json.load(f)

print(f"Total partes: {resumen['total_partes']}")
print(f"Total archivos: {resumen['total_archivos_generados']}")

# Leer cualquier informe
df = pd.read_csv('01_sin_agrupacion/Listado_Completo.csv')
print(f"Registros: {len(df)}")

# Leer informe agrupado
df_prov = pd.read_csv('02_agrupacion_simple/Por_Provincia.csv')
print(df_prov)

# Leer metadatos de selección
with open('07_por_partidas/Seleccion_01_metadata.json', 'r') as f:
    metadata = json.load(f)
    print(f"Partidas seleccionadas: {metadata['num_partidas']}")
```

### Casos de Uso Comunes

#### Dashboard Gerencial
```
RESUMEN_GLOBAL.json
+ Por_Estado.csv
+ Por_Provincia.csv
+ Por_mes.csv
```

#### Análisis Regional
```
Por_provincia_y_estado.csv
+ Por_provincia_comarca_municipio.csv
+ Provincia_*.csv (8 archivos)
```

#### Seguimiento de Proyectos
```
Seleccion_*.csv (20 selecciones)
+ Estado_*.csv
+ Por_mes_estado.csv
```

#### Análisis de Infraestructura
```
Por_red_y_tipo_trabajo.csv
+ Por_red_y_estado.csv
+ Red_*.csv (5 archivos)
```

## ✅ Validaciones

- ✅ Todos los totales suman correctamente
- ✅ Todos los decimales tienen exactamente 2 posiciones
- ✅ Fórmula `pendiente = presupuesto - certificado` verificada
- ✅ Fechas coherentes (`fecha_fin >= fecha_inicio`)
- ✅ Estados coherentes con certificados
- ✅ Jerarquía geográfica correcta
- ✅ 200 códigos únicos sin duplicados

## 📊 Estadísticas

### Por Categoría

| Categoría | Archivos | % Total |
|-----------|----------|---------|
| Sin agrupación | 1 | 0.8% |
| Agrupación simple | 10 | 8.1% |
| Agrupación doble | 19 | 15.4% |
| Agrupación triple | 10 | 8.1% |
| Filtrados | 19 | 15.4% |
| Filtros combinados | 24 | 19.5% |
| Por partidas | 40 | 32.5% |

### Distribución de Datos

- **Estados:** Pendiente (67), En curso (65), Finalizado (68)
- **Provincias:** 8 (distribución equilibrada)
- **Tipos Trabajo:** OT (67), GF (71), TP (62)
- **Redes:** 5 (distribución aleatoria)
- **Meses:** 20 (ene-2024 a oct-2025)

## 📝 Notas

- Los archivos CSV usan **coma (,)** como separador
- La codificación es **UTF-8**
- Los decimales usan **punto (.)** como separador
- Las fechas están en formato **ISO (YYYY-MM-DD)**
- Los importes **NO incluyen** símbolo de moneda

## 🔗 Documentación

- **Análisis completo:** `../ANALISIS_EXHAUSTIVO_COMPLETO.md`
- **Script generador:** `../generar_todos_informes_exhaustivo.py`
- **Documentación original:** `../ANALISIS_EXHAUSTIVO_INFORMES.md`

## 💡 Recomendaciones

### Para Principiantes
1. Empezar con `RESUMEN_GLOBAL.json` para entender los datos
2. Ver `Listado_Completo.csv` para ver todos los registros
3. Explorar `Por_Estado.csv` y `Por_Provincia.csv` para resúmenes

### Para Análisis Avanzado
1. Usar agrupaciones dobles para análisis cruzados
2. Explorar agrupaciones triples para máximo detalle
3. Combinar filtros para análisis específicos

### Para Dashboards
1. `RESUMEN_GLOBAL.json` para KPIs
2. Agrupaciones simples para gráficos principales
3. Agrupaciones dobles para tablas dinámicas
4. Selecciones de partidas para seguimiento de proyectos

---

**Generado:** 2025-11-08
**Sistema:** HydroFlow Manager v1.04
**Versión:** 2.0 - Generación Exhaustiva
