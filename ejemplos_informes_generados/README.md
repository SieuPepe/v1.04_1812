# Ejemplos de Informes Generados

Este directorio contiene ejemplos de todos los tipos de informes que puede generar el sistema de reportes de HydroFlow Manager v1.04.

## 📂 Estructura

```
ejemplos_informes_generados/
├── README.md                              (Este archivo)
├── Listado_Completo_Partes.csv           (Informe completo sin filtros)
├── RESUMEN_EJECUTIVO.json                 (Estadísticas generales)
├── ANALISIS_COMPLETO.txt                  (Análisis textual)
│
├── por_partidas/                          (Informes filtrados por partidas)
│   └── 5 selecciones aleatorias con metadatos
│
└── por_periodos_y_grupos/                 (Informes agrupados)
    └── 8 tipos de agrupaciones diferentes
```

## 🎯 Tipos de Informes

### 1. Informe Básico Completo
- **Archivo:** `Listado_Completo_Partes.csv`
- **Descripción:** Listado de todas las partes sin filtros ni agrupaciones
- **Registros:** 100 partes
- **Campos:** 16 columnas (código, descripción, estado, red, tipo_trabajo, importes, fechas, etc.)

### 2. Informes por Partidas Seleccionadas
- **Directorio:** `por_partidas/`
- **Descripción:** Informes filtrados por códigos de parte específicos
- **Cantidad:** 5 selecciones aleatorias
- **Características:**
  - Cada selección incluye archivo CSV con los datos
  - Cada selección incluye archivo JSON con metadatos y estadísticas
  - Las partidas fueron seleccionadas aleatoriamente (entre 5 y 11 por informe)

**Ejemplo de metadatos:**
```json
{
  "nombre": "Selección_Aleatoria_#1",
  "tipo_informe": "Listado de Partes",
  "filtro": "Por Partidas Seleccionadas",
  "partidas_seleccionadas": ["GF-2024-0082", "GF-2025-0044", ...],
  "num_resultados": 9,
  "estadisticas": {
    "total_presupuesto": 268114.77,
    "total_certificado": 36366.83,
    "total_pendiente": 231747.94,
    "estados": {
      "Pendiente": 5,
      "En curso": 3,
      "Finalizado": 1
    }
  }
}
```

### 3. Informes Agrupados (GROUP BY)
- **Directorio:** `por_periodos_y_grupos/`
- **Descripción:** Informes con datos agregados por diferentes dimensiones

#### Agrupaciones Disponibles:

| Archivo | Agrupación | Grupos | Descripción |
|---------|-----------|--------|-------------|
| `Informe_Por_Mes.csv` | Mes | 20 | Datos agregados por mes (YYYY-MM) |
| `Informe_Por_Año.csv` | Año | 2 | Datos agregados por año |
| `Informe_Por_Estado.csv` | Estado | 3 | Totales por estado (Pendiente/En curso/Finalizado) |
| `Informe_Por_Provincia.csv` | Provincia | 8 | Totales por provincia |
| `Informe_Por_Comarca.csv` | Comarca | 13 | Totales por comarca |
| `Informe_Por_Municipio.csv` | Municipio | 11 | Totales por municipio |
| `Informe_Por_Tipo_Trabajo.csv` | Tipo Trabajo | 3 | Totales por tipo (OT/GF/TP) |
| `Informe_Por_Provincia_y_Estado.csv` | Provincia × Estado | 24 | Agrupación combinada (2 niveles) |

**Campos en informes agrupados:**
- `grupo`: Valor del campo de agrupación
- `cantidad`: Número de partes en el grupo
- `total_presupuesto`: Suma de presupuestos
- `total_certificado`: Suma de certificados
- `total_pendiente`: Suma de pendientes

**Para agrupaciones combinadas, se incluyen múltiples campos de agrupación:**
- `provincia`, `estado`: Campos de agrupación
- `cantidad`, `total_presupuesto`, etc.: Totales agregados

## 📊 Resumen Ejecutivo

El archivo `RESUMEN_EJECUTIVO.json` contiene:

- Totales generales (presupuesto, certificado, pendiente)
- Distribución por estados
- Distribución temporal (por año y por mes)
- Distribución geográfica (por provincia)
- Top 5 provincias por presupuesto
- Porcentaje de certificación global

## 🔢 Datos de Ejemplo

Los datos de ejemplo fueron generados con las siguientes características:

- **Total de partes:** 100
- **Rango de fechas:** Enero 2024 - Octubre 2025
- **Presupuesto total:** €2,825,263.36
- **Certificado total:** €1,361,976.10
- **Pendiente:** €1,463,287.26
- **Tasa de certificación:** 48.21%

**Distribución por estado:**
- Pendiente: 29 partes
- En curso: 32 partes
- Finalizado: 39 partes

**Provincias incluidas:**
Álava, Bizkaia, Gipuzkoa, Navarra (País Vasco)
Barcelona, Girona (Cataluña)
Madrid, Valencia

## 🚀 Cómo usar estos ejemplos

### Importar en Excel
```bash
# Abrir cualquier archivo CSV en Excel
# Los datos se importarán correctamente con separador de coma
```

### Analizar con Python
```python
import pandas as pd

# Leer informe completo
df = pd.read_csv('Listado_Completo_Partes.csv')

# Leer informe agrupado
df_provincia = pd.read_csv('por_periodos_y_grupos/Informe_Por_Provincia.csv')

# Leer resumen ejecutivo
import json
with open('RESUMEN_EJECUTIVO.json', 'r') as f:
    resumen = json.load(f)

print(f"Total partes: {resumen['total_partes']}")
print(f"Presupuesto total: €{resumen['importes_totales']['presupuesto']:,.2f}")
```

### Validar cálculos
```python
# Verificar que pendiente = presupuesto - certificado
df['pendiente_calculado'] = df['presupuesto'] - df['certificado']
df['diferencia'] = df['pendiente'] - df['pendiente_calculado']

# Debe dar todo 0 (o muy cercano a 0 por redondeos)
print(df['diferencia'].abs().max())  # Esperado: 0
```

## ✅ Validaciones Realizadas

Todos los archivos han sido validados:

✅ Todos los códigos son únicos
✅ Los importes tienen exactamente 2 decimales
✅ Los cálculos de pendiente son correctos
✅ Los totales de las agrupaciones suman el total general
✅ Las fechas son coherentes (fecha_fin >= fecha_inicio)
✅ Los estados son coherentes con los certificados
✅ No hay valores nulos donde no deberían existir

## 📝 Notas

- Los archivos CSV usan coma (,) como separador
- La codificación es UTF-8
- Los decimales usan punto (.) como separador
- Las fechas están en formato ISO (YYYY-MM-DD)
- Los importes NO incluyen símbolo de moneda

## 🔗 Archivos Relacionados

- **Generador de ejemplos:** `../generar_ejemplos_informes.py`
- **Análisis exhaustivo:** `../ANALISIS_EXHAUSTIVO_INFORMES.md`
- **Código del sistema:** `../script/informes.py`

---

**Generado:** 2025-11-08
**Sistema:** HydroFlow Manager v1.04
