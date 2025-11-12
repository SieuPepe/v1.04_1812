# Explicación: Campo precio_unit en tbl_part_presupuesto

## Pregunta

¿Realmente se utiliza la columna `precio_unit` en `tbl_part_presupuesto`? Porque el precio unitario asociado a un material está registrado en la tabla `tbl_pres_precios`.

## Respuesta

**SÍ, se utiliza y es fundamental para el correcto funcionamiento del sistema.**

### Razón de diseño: Snapshot de precios

El campo `precio_unit` en `tbl_part_presupuesto` almacena una **copia (snapshot)** del precio unitario en el momento de asignar la partida al presupuesto del parte. Este patrón de diseño se conoce como "historización de precios" y tiene varias ventajas importantes:

### Ventajas del diseño actual

1. **Histórico de precios**
   - Cuando se asigna una partida a un parte, se copia el precio actual de `tbl_pres_precios.coste` a `tbl_part_presupuesto.precio_unit`
   - Este precio queda "congelado" en el presupuesto del parte
   - Permite saber exactamente qué precio se utilizó en cada parte

2. **Independencia de cambios futuros**
   - Si los precios en `tbl_pres_precios` cambian (inflación, actualizaciones, etc.), los presupuestos históricos NO se ven afectados
   - Los partes antiguos mantienen los precios con los que fueron presupuestados

3. **Auditoría y trazabilidad**
   - Se puede comparar el precio original del presupuesto con el precio actual
   - Permite análisis de desviaciones de precios a lo largo del tiempo
   - Cumple con requisitos de auditoría para proyectos largos

4. **Ajustes manuales**
   - Permite hacer ajustes específicos del precio para casos particulares
   - Por ejemplo: descuentos especiales, precios negociados, etc.
   - Sin afectar el precio maestro en `tbl_pres_precios`

### Flujo de datos

```
┌─────────────────────┐
│  tbl_pres_precios   │
│                     │
│  id: 20003          │
│  codigo: "MO.001"   │
│  coste: 45.50 €     │  ← Precio MAESTRO (puede cambiar)
└─────────────────────┘
           │
           │ Al asignar partida al parte
           │ se COPIA el precio
           ▼
┌─────────────────────────┐
│  tbl_part_presupuesto   │
│                         │
│  id: 1                  │
│  parte_id: 123          │
│  precio_id: 20003       │ ← Referencia al precio maestro
│  cantidad: 8.0          │
│  precio_unit: 45.50 €   │ ← SNAPSHOT del precio (congelado)
│  fecha: 2025-09-08      │
└─────────────────────────┘
```

### Cálculos que utilizan precio_unit

El campo `precio_unit` se utiliza en múltiples lugares:

1. **Vista vw_part_presupuesto** (línea 545 en db_core.py)
   ```sql
   SELECT ...
          pp.precio_unit,
          (pp.cantidad * pp.precio_unit) AS coste
   FROM tbl_part_presupuesto pp
   ```

2. **Vista vw_partes_resumen** (línea 600 en db_core.py)
   ```sql
   SELECT ...
          SUM(pp.cantidad * pp.precio_unit) AS total_presupuesto
   FROM tbl_part_presupuesto pp
   ```

3. **Función get_parts_list** (línea 347 en db_partes.py)
   ```sql
   COALESCE(SUM(pp.cantidad * pp.precio_unit), 0) AS presupuesto
   ```

### Conclusión

El campo `precio_unit` NO es redundante. Es una implementación correcta del patrón "snapshot de precios históricos" que:
- Preserva la integridad de presupuestos antiguos
- Permite auditoría y trazabilidad
- Facilita ajustes específicos sin afectar precios maestros
- Es una práctica recomendada en sistemas de gestión de proyectos y presupuestos

## Referencias

- Código: `script/db_partes.py` líneas 771-793
- Código: `script/db_core.py` líneas 534-550
- Código: `tools/alimentar_presupuestos_partes.py` líneas 67-68

---
*Documentación técnica - HydroFlow Manager v1.04*
*Fecha: 2025-11-11*
