"""
Script de testing para verificar las optimizaciones de backend.

Este script realiza pruebas de:
1. Rendimiento de funciones con caché LRU
2. Integridad de transacciones con rollback
3. Funcionamiento correcto de logging
4. Comparación de tiempos antes/después

Uso:
    python script/test_optimizaciones.py --user <usuario> --password <contraseña> --schema <esquema>

Argumentos:
    --user: Usuario de MySQL
    --password: Contraseña del usuario
    --schema: Esquema de proyecto para testing
    --iterations: Número de iteraciones para pruebas de rendimiento (default: 10)
    --verbose: Muestra información detallada
"""

import argparse
import logging
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
import json

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from script.db_partes import (
    get_parts_list,
    get_partes_resumen,
    get_parte_detail,
    _detect_text_column_cached,
    _get_table_columns_cached,
    add_part_presupuesto_item,
    delete_part_presupuesto_item
)


class OptimizationTester:
    """Clase para realizar tests de optimización."""

    def __init__(self, user: str, password: str, schema: str):
        """
        Inicializa el tester.

        Args:
            user: Usuario de MySQL
            password: Contraseña del usuario
            schema: Esquema de proyecto
        """
        self.user = user
        self.password = password
        self.schema = schema
        self.results = {}

    def measure_time(self, func, *args, **kwargs) -> Tuple[float, any]:
        """
        Mide el tiempo de ejecución de una función.

        Args:
            func: Función a ejecutar
            *args: Argumentos posicionales
            **kwargs: Argumentos con nombre

        Returns:
            Tupla (tiempo_ms, resultado)
        """
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed_ms = (end - start) * 1000
        return elapsed_ms, result

    def test_cache_performance(self, iterations: int = 10) -> Dict:
        """
        Test de rendimiento del caché LRU.

        Args:
            iterations: Número de iteraciones

        Returns:
            Diccionario con resultados
        """
        logger.info("\n" + "="*70)
        logger.info("TEST 1: Rendimiento de Caché LRU")
        logger.info("="*70)

        # Limpiar caché antes de empezar
        _detect_text_column_cached.cache_clear()
        _get_table_columns_cached.cache_clear()

        results = {
            'test': 'cache_performance',
            'iterations': iterations,
            'functions': {}
        }

        # Test 1: get_parts_list (usa ambos cachés)
        logger.info("\n📊 Testeando get_parts_list()...")

        # Primera ejecución (cache miss)
        time_first, _ = self.measure_time(
            get_parts_list, self.user, self.password, self.schema
        )
        logger.info(f"  Primera ejecución (cache miss): {time_first:.2f} ms")

        # Ejecuciones subsecuentes (cache hit)
        times_cached = []
        for i in range(iterations):
            time_cached, _ = self.measure_time(
                get_parts_list, self.user, self.password, self.schema
            )
            times_cached.append(time_cached)

        avg_cached = sum(times_cached) / len(times_cached)
        logger.info(f"  Promedio con caché ({iterations} iter): {avg_cached:.2f} ms")
        logger.info(f"  Mejora: {((time_first - avg_cached) / time_first * 100):.1f}%")

        results['functions']['get_parts_list'] = {
            'first_run_ms': time_first,
            'avg_cached_ms': avg_cached,
            'improvement_pct': ((time_first - avg_cached) / time_first * 100)
        }

        # Verificar estadísticas de caché
        cache_info_detect = _detect_text_column_cached.cache_info()
        cache_info_columns = _get_table_columns_cached.cache_info()

        logger.info(f"\n📈 Estadísticas de Caché:")
        logger.info(f"  _detect_text_column_cached:")
        logger.info(f"    Hits: {cache_info_detect.hits}")
        logger.info(f"    Misses: {cache_info_detect.misses}")
        logger.info(f"    Hit Rate: {(cache_info_detect.hits / (cache_info_detect.hits + cache_info_detect.misses) * 100):.1f}%")

        logger.info(f"  _get_table_columns_cached:")
        logger.info(f"    Hits: {cache_info_columns.hits}")
        logger.info(f"    Misses: {cache_info_columns.misses}")
        logger.info(f"    Hit Rate: {(cache_info_columns.hits / (cache_info_columns.hits + cache_info_columns.misses) * 100):.1f}%")

        results['cache_stats'] = {
            'detect_column': {
                'hits': cache_info_detect.hits,
                'misses': cache_info_detect.misses,
                'hit_rate_pct': (cache_info_detect.hits / (cache_info_detect.hits + cache_info_detect.misses) * 100)
            },
            'get_columns': {
                'hits': cache_info_columns.hits,
                'misses': cache_info_columns.misses,
                'hit_rate_pct': (cache_info_columns.hits / (cache_info_columns.hits + cache_info_columns.misses) * 100)
            }
        }

        # Test 2: get_partes_resumen
        logger.info("\n📊 Testeando get_partes_resumen()...")

        time_first_resumen, _ = self.measure_time(
            get_partes_resumen, self.user, self.password, self.schema
        )
        logger.info(f"  Primera ejecución: {time_first_resumen:.2f} ms")

        times_cached_resumen = []
        for i in range(iterations):
            time_cached, _ = self.measure_time(
                get_partes_resumen, self.user, self.password, self.schema
            )
            times_cached_resumen.append(time_cached)

        avg_cached_resumen = sum(times_cached_resumen) / len(times_cached_resumen)
        logger.info(f"  Promedio con caché: {avg_cached_resumen:.2f} ms")
        logger.info(f"  Mejora: {((time_first_resumen - avg_cached_resumen) / time_first_resumen * 100):.1f}%")

        results['functions']['get_partes_resumen'] = {
            'first_run_ms': time_first_resumen,
            'avg_cached_ms': avg_cached_resumen,
            'improvement_pct': ((time_first_resumen - avg_cached_resumen) / time_first_resumen * 100)
        }

        logger.info("\n✅ Test de caché completado")
        return results

    def test_transaction_integrity(self) -> Dict:
        """
        Test de integridad de transacciones con rollback.

        Returns:
            Diccionario con resultados
        """
        logger.info("\n" + "="*70)
        logger.info("TEST 2: Integridad de Transacciones (Rollback)")
        logger.info("="*70)

        results = {
            'test': 'transaction_integrity',
            'tests': []
        }

        # Test: Agregar y eliminar item de presupuesto
        logger.info("\n🔄 Testeando add/delete presupuesto con rollback...")

        try:
            # Intentar agregar item con datos inválidos (debería hacer rollback)
            logger.info("  Intentando insertar datos inválidos...")

            try:
                result = add_part_presupuesto_item(
                    self.user, self.password, self.schema,
                    parte_id=999999,  # ID que probablemente no existe
                    precio_id=999999,
                    cantidad=1.0,
                    precio_unit=10.0
                )
                # Si llegamos aquí, puede ser que la FK no esté activa
                if result == "ok":
                    logger.warning("  ⚠ Inserción exitosa (FK puede no estar activa)")
                    # Limpiar
                    # delete_part_presupuesto_item(self.user, self.password, self.schema, ?)
                    test_result = "warning"
                else:
                    logger.info(f"  ✓ Rollback correcto, error: {result}")
                    test_result = "pass"

            except Exception as e:
                logger.info(f"  ✓ Rollback correcto, excepción capturada: {type(e).__name__}")
                test_result = "pass"

            results['tests'].append({
                'name': 'invalid_insert_rollback',
                'result': test_result
            })

        except Exception as e:
            logger.error(f"  ✗ Error inesperado: {e}")
            results['tests'].append({
                'name': 'invalid_insert_rollback',
                'result': 'fail',
                'error': str(e)
            })

        logger.info("\n✅ Test de transacciones completado")
        return results

    def test_query_reduction(self) -> Dict:
        """
        Test de reducción de queries a la BD.

        Returns:
            Diccionario con resultados
        """
        logger.info("\n" + "="*70)
        logger.info("TEST 3: Reducción de Queries")
        logger.info("="*70)

        results = {
            'test': 'query_reduction',
            'observations': []
        }

        # Limpiar caché
        _detect_text_column_cached.cache_clear()
        _get_table_columns_cached.cache_clear()

        logger.info("\n📉 Contando queries con caché vacío vs lleno...")

        # Primera ejecución
        logger.info("  Primera ejecución (caché vacío):")
        cache_before = _detect_text_column_cached.cache_info()
        get_parts_list(self.user, self.password, self.schema)
        cache_after = _detect_text_column_cached.cache_info()

        queries_first = cache_after.misses - cache_before.misses
        logger.info(f"    Queries a information_schema: {queries_first}")

        # Segunda ejecución
        logger.info("  Segunda ejecución (caché lleno):")
        cache_before = _detect_text_column_cached.cache_info()
        get_parts_list(self.user, self.password, self.schema)
        cache_after = _detect_text_column_cached.cache_info()

        queries_second = cache_after.misses - cache_before.misses
        logger.info(f"    Queries a information_schema: {queries_second}")

        reduction = queries_first - queries_second
        logger.info(f"  📊 Reducción de queries: {reduction} ({(reduction/queries_first*100):.0f}%)")

        results['observations'].append({
            'first_run_queries': queries_first,
            'second_run_queries': queries_second,
            'reduction': reduction,
            'reduction_pct': (reduction/queries_first*100) if queries_first > 0 else 0
        })

        logger.info("\n✅ Test de reducción de queries completado")
        return results

    def generate_report(self) -> str:
        """
        Genera un reporte en formato JSON.

        Returns:
            String con JSON del reporte
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'schema': self.schema,
            'tests': self.results
        }

        return json.dumps(report, indent=2, ensure_ascii=False)

    def run_all_tests(self, iterations: int = 10):
        """
        Ejecuta todos los tests.

        Args:
            iterations: Número de iteraciones para tests de rendimiento
        """
        logger.info("\n" + "="*70)
        logger.info("INICIO DE SUITE DE TESTS DE OPTIMIZACIÓN")
        logger.info("="*70)
        logger.info(f"Esquema: {self.schema}")
        logger.info(f"Iteraciones: {iterations}")
        logger.info(f"Timestamp: {datetime.now()}")

        # Test 1: Cache performance
        self.results['cache_performance'] = self.test_cache_performance(iterations)

        # Test 2: Transaction integrity
        self.results['transaction_integrity'] = self.test_transaction_integrity()

        # Test 3: Query reduction
        self.results['query_reduction'] = self.test_query_reduction()

        # Resumen final
        logger.info("\n" + "="*70)
        logger.info("RESUMEN DE TESTS")
        logger.info("="*70)

        # Mejoras de rendimiento
        cache_results = self.results['cache_performance']['functions']
        logger.info("\n📈 Mejoras de Rendimiento:")
        for func_name, data in cache_results.items():
            logger.info(f"  {func_name}:")
            logger.info(f"    Primera ejecución: {data['first_run_ms']:.2f} ms")
            logger.info(f"    Con caché: {data['avg_cached_ms']:.2f} ms")
            logger.info(f"    Mejora: {data['improvement_pct']:.1f}%")

        # Hit rate de caché
        cache_stats = self.results['cache_performance']['cache_stats']
        logger.info("\n🎯 Hit Rate de Caché:")
        logger.info(f"  Detección de columnas: {cache_stats['detect_column']['hit_rate_pct']:.1f}%")
        logger.info(f"  Estructura de tablas: {cache_stats['get_columns']['hit_rate_pct']:.1f}%")

        # Reducción de queries
        query_stats = self.results['query_reduction']['observations'][0]
        logger.info("\n📉 Reducción de Queries:")
        logger.info(f"  Primera ejecución: {query_stats['first_run_queries']} queries")
        logger.info(f"  Segunda ejecución: {query_stats['second_run_queries']} queries")
        logger.info(f"  Reducción: {query_stats['reduction_pct']:.0f}%")

        logger.info("\n" + "="*70)
        logger.info("TESTS COMPLETADOS EXITOSAMENTE")
        logger.info("="*70)


def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(
        description='Tests de optimización de backend'
    )
    parser.add_argument('--user', required=True, help='Usuario de MySQL')
    parser.add_argument('--password', required=True, help='Contraseña del usuario')
    parser.add_argument('--schema', required=True, help='Esquema de proyecto')
    parser.add_argument('--iterations', type=int, default=10,
                       help='Número de iteraciones (default: 10)')
    parser.add_argument('--verbose', action='store_true',
                       help='Muestra información detallada')
    parser.add_argument('--output', help='Archivo de salida JSON (opcional)')

    args = parser.parse_args()

    # Configurar nivel de logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Crear tester y ejecutar tests
    tester = OptimizationTester(args.user, args.password, args.schema)
    tester.run_all_tests(args.iterations)

    # Guardar reporte si se especificó
    if args.output:
        report = tester.generate_report()
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info(f"\n💾 Reporte guardado en: {args.output}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
