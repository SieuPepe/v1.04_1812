# Testing de Optimizaciones - Guía de Uso

## Descripción

Script automatizado para verificar y medir el impacto de las optimizaciones implementadas en el backend.

## Tests Incluidos

### 1. Test de Rendimiento de Caché LRU
Mide la mejora de rendimiento gracias al caché implementado:
- Primera ejecución (cache miss)
- Ejecuciones subsecuentes (cache hit)
- Cálculo de mejora porcentual
- Estadísticas de hit rate

**Funciones testeadas:**
- `get_parts_list()`
- `get_partes_resumen()`
- `_detect_text_column_cached()`
- `_get_table_columns_cached()`

### 2. Test de Integridad de Transacciones
Verifica que el rollback funcione correctamente:
- Inserción de datos inválidos
- Verificación de rollback automático
- Manejo de excepciones

**Funciones testeadas:**
- `add_part_presupuesto_item()`
- `delete_part_presupuesto_item()`

### 3. Test de Reducción de Queries
Cuenta el número de queries a la base de datos:
- Queries con caché vacío
- Queries con caché lleno
- Cálculo de reducción

## Uso

### Sintaxis Básica

```bash
python script/test_optimizaciones.py --user <usuario> --password <contraseña> --schema <esquema>
```

### Ejemplos

#### Test Básico
```bash
python script/test_optimizaciones.py --user root --password mipassword --schema PR_001
```

#### Test con Más Iteraciones
```bash
python script/test_optimizaciones.py --user root --password mipassword --schema PR_001 --iterations 20
```

#### Test con Salida JSON
```bash
python script/test_optimizaciones.py \
  --user root \
  --password mipassword \
  --schema PR_001 \
  --output resultados_test.json
```

#### Test Verbose
```bash
python script/test_optimizaciones.py \
  --user root \
  --password mipassword \
  --schema PR_001 \
  --verbose
```

## Parámetros

| Parámetro | Requerido | Default | Descripción |
|-----------|-----------|---------|-------------|
| `--user` | Sí | - | Usuario de MySQL |
| `--password` | Sí | - | Contraseña del usuario |
| `--schema` | Sí | - | Esquema de proyecto para testing |
| `--iterations` | No | 10 | Número de iteraciones para pruebas |
| `--output` | No | - | Archivo JSON para guardar resultados |
| `--verbose` | No | False | Muestra información detallada |

## Ejemplo de Salida

```
======================================================================
INICIO DE SUITE DE TESTS DE OPTIMIZACIÓN
======================================================================
Esquema: PR_001
Iteraciones: 10
Timestamp: 2025-11-05 10:30:45

======================================================================
TEST 1: Rendimiento de Caché LRU
======================================================================

📊 Testeando get_parts_list()...
  Primera ejecución (cache miss): 280.45 ms
  Promedio con caché (10 iter): 142.33 ms
  Mejora: 49.2%

📈 Estadísticas de Caché:
  _detect_text_column_cached:
    Hits: 45
    Misses: 8
    Hit Rate: 84.9%
  _get_table_columns_cached:
    Hits: 123
    Misses: 3
    Hit Rate: 97.6%

📊 Testeando get_partes_resumen()...
  Primera ejecución: 210.12 ms
  Promedio con caché: 105.67 ms
  Mejora: 49.7%

✅ Test de caché completado

======================================================================
TEST 2: Integridad de Transacciones (Rollback)
======================================================================

🔄 Testeando add/delete presupuesto con rollback...
  Intentando insertar datos inválidos...
  ✓ Rollback correcto, excepción capturada: IntegrityError

✅ Test de transacciones completado

======================================================================
TEST 3: Reducción de Queries
======================================================================

📉 Contando queries con caché vacío vs lleno...
  Primera ejecución (caché vacío):
    Queries a information_schema: 6
  Segunda ejecución (caché lleno):
    Queries a information_schema: 0
  📊 Reducción de queries: 6 (100%)

✅ Test de reducción de queries completado

======================================================================
RESUMEN DE TESTS
======================================================================

📈 Mejoras de Rendimiento:
  get_parts_list:
    Primera ejecución: 280.45 ms
    Con caché: 142.33 ms
    Mejora: 49.2%
  get_partes_resumen:
    Primera ejecución: 210.12 ms
    Con caché: 105.67 ms
    Mejora: 49.7%

🎯 Hit Rate de Caché:
  Detección de columnas: 84.9%
  Estructura de tablas: 97.6%

📉 Reducción de Queries:
  Primera ejecución: 6 queries
  Segunda ejecución: 0 queries
  Reducción: 100%

======================================================================
TESTS COMPLETADOS EXITOSAMENTE
======================================================================

💾 Reporte guardado en: resultados_test.json
```

## Formato del Reporte JSON

```json
{
  "timestamp": "2025-11-05T10:30:45.123456",
  "schema": "PR_001",
  "tests": {
    "cache_performance": {
      "test": "cache_performance",
      "iterations": 10,
      "functions": {
        "get_parts_list": {
          "first_run_ms": 280.45,
          "avg_cached_ms": 142.33,
          "improvement_pct": 49.2
        },
        "get_partes_resumen": {
          "first_run_ms": 210.12,
          "avg_cached_ms": 105.67,
          "improvement_pct": 49.7
        }
      },
      "cache_stats": {
        "detect_column": {
          "hits": 45,
          "misses": 8,
          "hit_rate_pct": 84.9
        },
        "get_columns": {
          "hits": 123,
          "misses": 3,
          "hit_rate_pct": 97.6
        }
      }
    },
    "transaction_integrity": {
      "test": "transaction_integrity",
      "tests": [
        {
          "name": "invalid_insert_rollback",
          "result": "pass"
        }
      ]
    },
    "query_reduction": {
      "test": "query_reduction",
      "observations": [
        {
          "first_run_queries": 6,
          "second_run_queries": 0,
          "reduction": 6,
          "reduction_pct": 100.0
        }
      ]
    }
  }
}
```

## Interpretación de Resultados

### ✅ Resultados Esperados

| Métrica | Valor Esperado | Descripción |
|---------|---------------|-------------|
| Mejora de rendimiento | 40-60% | Con caché vs sin caché |
| Hit rate de caché | >80% | En ejecuciones repetidas |
| Reducción de queries | 80-100% | Con caché lleno |
| Test de rollback | pass | Debe manejar errores correctamente |

### ⚠️ Señales de Alerta

- **Mejora < 30%**: El caché puede no estar funcionando
- **Hit rate < 70%**: Verificar configuración de caché
- **Reducción queries < 50%**: Investigar uso de caché
- **Test rollback fail**: Verificar manejo de transacciones

## Automatización

### Integración con CI/CD

Puedes integrar este script en pipelines de CI/CD:

```yaml
# Ejemplo para GitHub Actions
- name: Test optimizaciones
  run: |
    python script/test_optimizaciones.py \
      --user ${{ secrets.DB_USER }} \
      --password ${{ secrets.DB_PASSWORD }} \
      --schema ${{ env.TEST_SCHEMA }} \
      --output test_results.json

- name: Upload results
  uses: actions/upload-artifact@v2
  with:
    name: test-results
    path: test_results.json
```

### Script de Testing Continuo

```bash
#!/bin/bash
# test_continuo.sh

SCHEMAS=("PR_001" "PR_002" "PR_003")

for schema in "${SCHEMAS[@]}"; do
  echo "Testing schema: $schema"
  python script/test_optimizaciones.py \
    --user root \
    --password mipassword \
    --schema "$schema" \
    --output "test_results_$schema.json"
done

echo "Tests completados para todos los esquemas"
```

## Troubleshooting

### Error: "No module named 'script.db_partes'"

Asegúrate de ejecutar desde el directorio raíz del proyecto:

```bash
cd /ruta/al/proyecto
python script/test_optimizaciones.py ...
```

### Error: "Access denied for user"

Verifica que las credenciales sean correctas y que el usuario tenga permisos.

### Resultados inconsistentes

Si los resultados varían mucho entre ejecuciones:
- Ejecuta con más iteraciones (`--iterations 50`)
- Verifica que la BD no esté bajo carga
- Reinicia la conexión entre tests

## Comparación con Baseline

Para comparar con versiones anteriores:

```bash
# Ejecutar antes de las optimizaciones
git checkout commit_anterior
python script/test_optimizaciones.py ... --output baseline.json

# Ejecutar después de las optimizaciones
git checkout rama_actual
python script/test_optimizaciones.py ... --output optimizado.json

# Comparar resultados
python -m json.tool baseline.json
python -m json.tool optimizado.json
```

## Notas

1. **Datos de prueba**: El esquema debe contener datos representativos
2. **Carga del servidor**: Ejecutar con la BD bajo carga normal
3. **Múltiples ejecuciones**: Promediar resultados de varias ejecuciones
4. **Hardware**: Los tiempos varían según el hardware

## Referencias

- `OPTIMIZACIONES_BACKEND.md`: Documentación completa de optimizaciones
- `script/db_partes.py`: Implementación de funciones optimizadas
- `script/indices_recomendados.sql`: Índices SQL recomendados
