# Aplicación de Índices SQL - Guía de Uso

## Descripción

Este directorio contiene los scripts necesarios para aplicar los índices recomendados que optimizan el rendimiento de las consultas en la base de datos.

## Archivos

- **`indices_recomendados.sql`**: Definición SQL de todos los índices recomendados con documentación
- **`aplicar_indices.py`**: Script Python para aplicar índices de forma programática y segura

## Uso del Script Python

### Sintaxis Básica

```bash
python script/aplicar_indices.py --user <usuario> --password <contraseña>
```

### Ejemplos

#### 1. Simulación (Dry-Run)
Muestra qué índices se crearían sin aplicar cambios reales:

```bash
python script/aplicar_indices.py --user root --password mipassword --dry-run
```

#### 2. Aplicar a Todos los Esquemas
Aplica índices a todos los esquemas de proyectos automáticamente:

```bash
python script/aplicar_indices.py --user root --password mipassword
```

#### 3. Aplicar a un Esquema Específico
Aplica índices solo al proyecto especificado:

```bash
python script/aplicar_indices.py --user root --password mipassword --schema PR_001
```

#### 4. Modo Verbose
Muestra información detallada del proceso:

```bash
python script/aplicar_indices.py --user root --password mipassword --verbose
```

## Parámetros

| Parámetro | Requerido | Descripción |
|-----------|-----------|-------------|
| `--user` | Sí | Usuario de MySQL con permisos de CREATE INDEX |
| `--password` | Sí | Contraseña del usuario |
| `--schema` | No | Esquema específico (aplica a todos si no se especifica) |
| `--dry-run` | No | Simula la ejecución sin aplicar cambios |
| `--verbose` | No | Muestra información detallada |

## Características del Script

### ✅ Seguridad
- Verifica que las tablas existan antes de crear índices
- Verifica que los índices no existan ya (evita errores)
- Modo dry-run para simular sin riesgos
- Manejo robusto de errores

### 📊 Logging Completo
- Salida en consola con formato claro
- Log persistente en `aplicar_indices.log`
- Resumen final con estadísticas

### 🎯 Inteligente
- Detecta automáticamente todos los esquemas de proyectos
- Salta tablas que no existen en esquemas antiguos
- Ejecuta ANALYZE TABLE automáticamente después de crear índices

## Índices que se Aplicarán

### tbl_partes (4 índices)
- `idx_partes_tipo_codigo` - Para generación de códigos
- `idx_partes_municipio` - Para JOINs con municipios
- `idx_partes_fecha_estado` - Para listados cronológicos
- `idx_partes_codigo` - Para búsquedas por código

### tbl_part_presupuesto (2 índices)
- `idx_part_presupuesto_parte_precio` - Covering index para SUM/GROUP BY
- `idx_part_presupuesto_parte` - Para JOINs simples

### tbl_part_certificacion (2 índices)
- `idx_part_cert_parte_certificada` - Para cálculos de certificaciones
- `idx_part_cert_pendientes` - Para listados de pendientes

### dim_municipios (2 índices)
- `idx_municipios_comarca` - Para JOINs con comarcas
- `idx_municipios_provincia` - Para JOINs con provincias

### Tablas Dimensionales (4 índices)
- `idx_red_descripcion` - dim_red
- `idx_tipo_trabajo_descripcion` - dim_tipo_trabajo
- `idx_codigo_trabajo_descripcion` - dim_codigo_trabajo
- `idx_tipos_rep_descripcion` - dim_tipos_rep

### tbl_parte_estados (1 índice)
- `idx_parte_estados_nombre` - Para búsquedas por nombre

**Total: 15 índices**

## Impacto Esperado

| Operación | Mejora Estimada |
|-----------|----------------|
| SELECT con GROUP BY | 50-80% más rápido |
| JOINs complejos | 30-40% más rápido |
| Búsquedas por código | 90%+ más rápido |
| Listados con filtros | 40-60% más rápido |

## Ejemplo de Salida

```
======================================================================
APLICACIÓN DE ÍNDICES RECOMENDADOS
======================================================================
Encontrados 3 esquemas de proyectos

======================================================================
Procesando esquema: PR_001
======================================================================
  ⟳ Creando índice idx_partes_tipo_codigo en tbl_partes...
  ✓ Índice idx_partes_tipo_codigo creado exitosamente
  ⚠ Índice idx_partes_municipio ya existe en tbl_partes
  ⟳ Creando índice idx_partes_fecha_estado en tbl_partes...
  ✓ Índice idx_partes_fecha_estado creado exitosamente
  ...

  Ejecutando ANALYZE TABLE para actualizar estadísticas...
  ✓ ANALYZE TABLE tbl_partes completado
  ✓ ANALYZE TABLE tbl_part_presupuesto completado

======================================================================
RESUMEN FINAL
======================================================================
Esquemas procesados: 3
Índices creados: 38
Índices ya existentes: 7
Índices fallidos: 0
======================================================================
```

## Uso del Archivo SQL Directo

Si prefieres aplicar los índices manualmente con MySQL:

```bash
mysql -u usuario -p < script/indices_recomendados.sql
```

O desde MySQL Workbench:
1. Abre el archivo `indices_recomendados.sql`
2. Selecciona el esquema del proyecto
3. Ejecuta el script

## Verificación

Para verificar que los índices se crearon correctamente:

```sql
-- Ver todos los índices de una tabla
SHOW INDEX FROM tbl_partes;

-- O usar information_schema
SELECT
    INDEX_NAME,
    COLUMN_NAME,
    SEQ_IN_INDEX,
    INDEX_TYPE
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = 'PR_001'
  AND TABLE_NAME = 'tbl_partes'
ORDER BY INDEX_NAME, SEQ_IN_INDEX;
```

## Mantenimiento

### Actualizar Estadísticas

Ejecuta periódicamente (mensual) para mantener el optimizador actualizado:

```sql
ANALYZE TABLE tbl_partes;
ANALYZE TABLE tbl_part_presupuesto;
ANALYZE TABLE tbl_part_certificacion;
ANALYZE TABLE dim_municipios;
```

### Verificar Uso de Índices

Usa EXPLAIN para verificar que las queries usen los índices:

```sql
EXPLAIN SELECT * FROM tbl_partes WHERE codigo = 'P-001';
```

Busca `type: ref` o `type: index` en lugar de `type: ALL` (full table scan).

## Notas Importantes

1. **Permisos**: El usuario debe tener privilegio `CREATE INDEX`
2. **Espacio**: Los índices ocupan espacio adicional (~5-10% del tamaño de la tabla)
3. **Tiempo**: La creación de índices puede tomar varios segundos en tablas grandes
4. **Bloqueos**: MySQL puede bloquear las tablas brevemente durante la creación

## Soporte

Para problemas o preguntas:
- Revisa el log en `aplicar_indices.log`
- Usa `--verbose` para más información
- Usa `--dry-run` para probar sin riesgos
