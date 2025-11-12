# Verificación de Códigos: Excel → tbl_partes

## Descripción

Este conjunto de herramientas verifica que todos los códigos del archivo **MEDICIONES OTS.xlsx** existen en la tabla `tbl_partes` de la base de datos.

## Archivos

```
script/
├── verificar_codigos_excel.py          # Script Python (análisis completo)
└── sql/
    └── verificar_codigos_excel.sql     # Script SQL (para MySQL Workbench)
```

---

## Opción 1: Ejecutar en MySQL Workbench (RECOMENDADO)

### Pasos:

1. Abrir MySQL Workbench
2. Conectarse a la base de datos `cert_dev`
3. Abrir el archivo: `script/sql/verificar_codigos_excel.sql`
4. Ejecutar todo el script: **Ctrl+Shift+Enter** o botón ⚡
5. Revisar los resultados en las pestañas de salida

### Resultados que obtendrás:

#### 1. RESUMEN GENERAL
```
┌─────────────────┬───────────────────┬──────────────────┬────────────────────┬───────────────────┬──────────────────────┐
│ Analisis        │ Total_Codigos_Excel│ Total_Codigos_BD │ Codigos_Encontrados│ Codigos_Faltantes │ Porcentaje_Cobertura │
├─────────────────┼───────────────────┼──────────────────┼────────────────────┼───────────────────┼──────────────────────┤
│ RESUMEN GENERAL │ 821               │ 828              │ 650                │ 171               │ 79.2                 │
└─────────────────┴───────────────────┴──────────────────┴────────────────────┴───────────────────┴──────────────────────┘
```

#### 2. CÓDIGOS ENCONTRADOS
Lista completa de códigos que SÍ están en `tbl_partes`:
```
┌────────────────────┬──────────────┬──────────┬──────────────────────────┬──────────────┐
│ Estado             │ Codigo_Excel │ Parte_ID │ Descripcion              │ Tipo_Trabajo │
├────────────────────┼──────────────┼──────────┼──────────────────────────┼──────────────┤
│ CÓDIGOS ENCONTRADOS│ GF-0001      │ 1        │ Gastos de Administración │ Gastos Fijos │
│ CÓDIGOS ENCONTRADOS│ OT-0092      │ 92       │ Reparación Bombeo X      │ Ord Trabajo  │
│ ...                │ ...          │ ...      │ ...                      │ ...          │
└────────────────────┴──────────────┴──────────┴──────────────────────────┴──────────────┘
```

#### 3. CÓDIGOS FALTANTES
Lista completa de códigos que NO están en `tbl_partes`:
```
┌──────────────────┬──────────────┬─────────┬────────────────────┐
│ Estado           │ Codigo_Excel │ Prefijo │ Observacion        │
├──────────────────┼──────────────┼─────────┼────────────────────┤
│ CÓDIGOS FALTANTES│ OT-0362      │ OT      │ NO EXISTE EN BD    │
│ CÓDIGOS FALTANTES│ OT-0458      │ OT      │ NO EXISTE EN BD    │
│ CÓDIGOS FALTANTES│ TP-0048      │ TP      │ NO EXISTE EN BD    │
│ ...              │ ...          │ ...     │ ...                │
└──────────────────┴──────────────┴─────────┴────────────────────┘
```

#### 4. RESUMEN POR TIPO
```
┌─────────┬─────────────┬──────────────┬───────────┬───────────────┐
│ Prefijo │ Total_Excel │ Encontrados  │ Faltantes │ Porcentaje_OK │
├─────────┼─────────────┼──────────────┼───────────┼───────────────┤
│ GF      │ 6           │ 6            │ 0         │ 100.0         │
│ OT      │ 434         │ 350          │ 84        │ 80.6          │
│ TP      │ 381         │ 294          │ 87        │ 77.2          │
└─────────┴─────────────┴──────────────┴───────────┴───────────────┘
```

#### 5. VISTA RÁPIDA
- Primeros 10 códigos faltantes
- Últimos 10 códigos faltantes

---

## Opción 2: Ejecutar Script Python

### Requisitos:
```bash
pip install pandas openpyxl mysql-connector-python
```

### Uso:
```bash
cd /home/user/v1.04_1812
python script/verificar_codigos_excel.py
```

### Salida:

El script realizará:

1. **Lectura del Excel**: Lee `MEDICIONES OTS.xlsx` y extrae códigos únicos
2. **Generación del SQL**: Crea `script/sql/verificar_codigos_excel.sql` (siempre)
3. **Verificación en BD**: Si puede conectarse, verifica y genera reporte
4. **Reporte**: Crea `script/codigos_faltantes.txt` si hay códigos faltantes

```
======================================================================
VERIFICACIÓN DE CÓDIGOS: EXCEL → tbl_partes
======================================================================

✓ Excel leído: MEDICIONES OTS.xlsx
  Total de registros: 2778
  Códigos únicos encontrados: 821

✓ Script SQL generado: script/sql/verificar_codigos_excel.sql
  Puedes ejecutarlo directamente en MySQL Workbench

✓ Conectado a la base de datos: cert_dev

✓ Códigos en tbl_partes: 828

======================================================================
VERIFICACIÓN DE CÓDIGOS
======================================================================

Total de códigos en Excel: 821
  ✓ Códigos encontrados en BD: 650
  ✗ Códigos faltantes en BD: 171

Porcentaje de cobertura: 79.2%

======================================================================
CÓDIGOS FALTANTES EN tbl_partes
======================================================================

  1. OT-0362
  2. OT-0458
  3. OT-0500
  ...

----------------------------------------------------------------------
RESUMEN POR TIPO
----------------------------------------------------------------------
  GF: 0 códigos faltantes
  OT: 84 códigos faltantes
  TP: 87 códigos faltantes

✓ Reporte guardado en: script/codigos_faltantes.txt

======================================================================
VERIFICACIÓN COMPLETADA
======================================================================
```

---

## Datos Analizados

- **Archivo Excel**: `MEDICIONES OTS.xlsx` (raíz del proyecto)
- **Total de registros en Excel**: 2,778
- **Códigos únicos en Excel**: 821
- **Formato original**: `OT/0121`, `TP/0278`, `GF/0045`
- **Formato normalizado**: `OT-0121`, `TP-0278`, `GF-0045`

### Distribución de códigos:
- **GF** (Gastos Fijos): 6 códigos
- **OT** (Órdenes de Trabajo): 434 códigos
- **TP** (Trabajos Programados): 381 códigos

---

## Acciones si hay códigos faltantes

Si el análisis muestra códigos faltantes, tienes dos opciones:

### Opción A: Importar partes faltantes
Si los códigos son válidos y deben estar en la BD:
1. Identificar el Excel fuente con los datos completos de esos partes
2. Usar `script/generar_script_importacion.py` para generar SQL de importación
3. Ejecutar el SQL generado en MySQL Workbench

### Opción B: Corregir Excel de mediciones
Si los códigos son erróneos:
1. Abrir `MEDICIONES OTS.xlsx`
2. Buscar las filas con los códigos faltantes
3. Corregir los códigos según la tabla `tbl_partes`
4. Volver a ejecutar este script de verificación

---

## Notas Técnicas

### Formato de códigos
- El script normaliza automáticamente: `OT/0121` → `OT-0121`
- Los códigos duplicados se eliminan (solo se cuenta una vez)
- Los valores nulos se ignoran

### Tabla temporal
- El script SQL crea una tabla temporal `tmp_codigos_excel`
- Se elimina automáticamente al cerrar la conexión de MySQL
- No modifica ninguna tabla existente (solo lectura)

### Performance
- El script SQL es muy rápido (< 1 segundo)
- El script Python depende del tamaño del Excel (~ 5 segundos)

---

## Archivos Generados

| Archivo | Descripción | Cuándo se crea |
|---------|-------------|----------------|
| `script/sql/verificar_codigos_excel.sql` | Script SQL completo con 821 códigos | Siempre |
| `script/codigos_faltantes.txt` | Lista de códigos faltantes | Solo si hay faltantes |

---

## Troubleshooting

### Error: "No se encuentra el archivo Excel"
- Verificar que `MEDICIONES OTS.xlsx` está en la raíz del proyecto
- Path esperado: `/home/user/v1.04_1812/MEDICIONES OTS.xlsx`

### Error: "Can't connect to MySQL server"
- No es un error crítico: el script SQL ya fue generado
- Puedes ejecutar el SQL directamente en MySQL Workbench
- Para conectarse desde Python, verificar:
  - MySQL está corriendo
  - Credenciales son correctas (user: cert_dev, password: urbide)
  - Base de datos `cert_dev` existe

### Error: "No se encuentra la columna 'parte_id'"
- Verificar que el Excel tiene la columna `parte_id`
- El script mostrará las columnas disponibles en el mensaje de error

---

## Historial

- **2025-01-12**: Versión inicial
  - Script Python con verificación completa
  - Generación automática de SQL
  - 821 códigos únicos detectados en Excel
