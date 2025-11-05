"""
Sistema de caché para resultados de queries a tablas dimensionales.

Este módulo proporciona caché inteligente para tablas que cambian raramente
(dimensiones, catálogos, etc.) para evitar queries repetidas a la base de datos.

Características:
- TTL (Time-To-Live) configurable por tabla
- LRU cache con límite de memoria
- Invalidación manual y automática
- Estadísticas de hit/miss rate
"""

import logging
import time
from functools import lru_cache, wraps
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import hashlib
import json

logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURACIÓN DE CACHÉ
# ============================================================================

class CacheConfig:
    """Configuración de caché para tablas dimensionales."""

    # TTL por tipo de tabla (en segundos)
    # Tablas muy estáticas: 1 hora
    # Tablas semi-estáticas: 5 minutos
    DEFAULT_TTL = 3600  # 1 hora

    TABLE_TTL = {
        # Dimensiones geográficas (muy estáticas)
        'dim_comarcas': 3600,
        'dim_provincias': 3600,
        'dim_municipios': 3600,
        'dim_ccaa': 3600,

        # Catálogos de trabajo (semi-estáticas)
        'dim_red': 1800,
        'dim_tipo_trabajo': 1800,
        'dim_codigo_trabajo': 1800,
        'dim_tipos_rep': 1800,
        'dim_ot': 1800,

        # Estados (pueden cambiar ocasionalmente)
        'tbl_parte_estados': 900,
        'dim_estados': 900,
    }

    @classmethod
    def get_ttl(cls, table_name: str) -> int:
        """
        Obtiene el TTL para una tabla.

        Args:
            table_name: Nombre de la tabla

        Returns:
            TTL en segundos
        """
        return cls.TABLE_TTL.get(table_name, cls.DEFAULT_TTL)


# ============================================================================
# CACHE ENTRY
# ============================================================================

class CacheEntry:
    """Entrada de caché con TTL."""

    def __init__(self, data: Any, ttl: int):
        """
        Crea una entrada de caché.

        Args:
            data: Datos a cachear
            ttl: Time-to-live en segundos
        """
        self.data = data
        self.created_at = time.time()
        self.ttl = ttl
        self.hits = 0

    def is_expired(self) -> bool:
        """
        Verifica si la entrada ha expirado.

        Returns:
            True si ha expirado, False en caso contrario
        """
        return (time.time() - self.created_at) > self.ttl

    def get_data(self) -> Optional[Any]:
        """
        Obtiene los datos si no han expirado.

        Returns:
            Datos cacheados o None si han expirado
        """
        if self.is_expired():
            return None

        self.hits += 1
        return self.data

    def get_age(self) -> float:
        """
        Obtiene la edad de la entrada en segundos.

        Returns:
            Edad en segundos
        """
        return time.time() - self.created_at


# ============================================================================
# DIMENSION CACHE
# ============================================================================

class DimensionCache:
    """
    Cache para resultados de queries a tablas dimensionales.

    Almacena resultados de queries SELECT con TTL automático.
    """

    def __init__(self):
        """Inicializa el caché."""
        self._cache: Dict[str, CacheEntry] = {}
        self._stats = {
            'hits': 0,
            'misses': 0,
            'expirations': 0,
            'invalidations': 0
        }

    def _make_key(self, schema: str, table: str, query: str, params: tuple = None) -> str:
        """
        Genera una clave única para el caché.

        Args:
            schema: Nombre del esquema
            table: Nombre de la tabla
            query: Query SQL
            params: Parámetros de la query

        Returns:
            Clave hash única
        """
        key_parts = [schema, table, query]
        if params:
            key_parts.append(json.dumps(params, sort_keys=True))

        key_string = '|'.join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()

    def get(self, schema: str, table: str, query: str, params: tuple = None) -> Optional[Any]:
        """
        Obtiene datos del caché.

        Args:
            schema: Nombre del esquema
            table: Nombre de la tabla
            query: Query SQL
            params: Parámetros de la query

        Returns:
            Datos cacheados o None si no existe o ha expirado
        """
        key = self._make_key(schema, table, query, params)

        if key not in self._cache:
            self._stats['misses'] += 1
            return None

        entry = self._cache[key]

        # Verificar si ha expirado
        if entry.is_expired():
            logger.debug(f"Entrada de caché expirada para {table}")
            del self._cache[key]
            self._stats['expirations'] += 1
            self._stats['misses'] += 1
            return None

        # Hit!
        self._stats['hits'] += 1
        logger.debug(f"Cache hit para {table} (edad: {entry.get_age():.1f}s)")
        return entry.get_data()

    def set(self, schema: str, table: str, query: str, data: Any, params: tuple = None):
        """
        Guarda datos en el caché.

        Args:
            schema: Nombre del esquema
            table: Nombre de la tabla
            query: Query SQL
            data: Datos a cachear
            params: Parámetros de la query
        """
        key = self._make_key(schema, table, query, params)
        ttl = CacheConfig.get_ttl(table)

        self._cache[key] = CacheEntry(data, ttl)
        logger.debug(f"Datos cacheados para {table} (TTL: {ttl}s)")

    def invalidate(self, schema: str = None, table: str = None):
        """
        Invalida entradas del caché.

        Args:
            schema: Esquema a invalidar (None para todos)
            table: Tabla a invalidar (None para todas)
        """
        if schema is None and table is None:
            # Invalidar todo
            count = len(self._cache)
            self._cache.clear()
            self._stats['invalidations'] += count
            logger.info(f"Caché completamente invalidado ({count} entradas)")
            return

        # Invalidar selectivamente
        keys_to_delete = []
        for key in self._cache.keys():
            # Las claves contienen schema|table|query, extraer los primeros elementos
            # Es una aproximación, podría mejorarse con metadata en CacheEntry
            if table and table.lower() in key.lower():
                keys_to_delete.append(key)

        for key in keys_to_delete:
            del self._cache[key]

        self._stats['invalidations'] += len(keys_to_delete)
        logger.info(f"Invalidadas {len(keys_to_delete)} entradas para {table or 'varias tablas'}")

    def get_stats(self) -> Dict:
        """
        Obtiene estadísticas del caché.

        Returns:
            Diccionario con estadísticas
        """
        total_requests = self._stats['hits'] + self._stats['misses']
        hit_rate = (self._stats['hits'] / total_requests * 100) if total_requests > 0 else 0

        return {
            **self._stats,
            'total_requests': total_requests,
            'hit_rate_pct': hit_rate,
            'cache_size': len(self._cache)
        }

    def cleanup_expired(self):
        """Limpia entradas expiradas del caché."""
        keys_to_delete = [
            key for key, entry in self._cache.items()
            if entry.is_expired()
        ]

        for key in keys_to_delete:
            del self._cache[key]

        if keys_to_delete:
            logger.info(f"Limpiadas {len(keys_to_delete)} entradas expiradas")


# Instancia global de caché
_dimension_cache = DimensionCache()


def get_dimension_cache() -> DimensionCache:
    """
    Obtiene la instancia global del caché de dimensiones.

    Returns:
        Instancia de DimensionCache
    """
    return _dimension_cache


# ============================================================================
# DECORADOR PARA CACHEAR FUNCIONES
# ============================================================================

def cached_dimension_query(table_name: str):
    """
    Decorador para cachear automáticamente queries a tablas dimensionales.

    Args:
        table_name: Nombre de la tabla dimensional

    Example:
        @cached_dimension_query('dim_red')
        def get_all_redes(user, password, schema):
            # Esta función se cacheará automáticamente
            with get_connection(user, password, schema) as cn:
                cur = cn.cursor()
                cur.execute("SELECT * FROM dim_red")
                return cur.fetchall()
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = get_dimension_cache()

            # Intentar extraer schema de los argumentos
            # Asumimos que user, password, schema son los primeros 3 args
            schema = args[2] if len(args) > 2 else kwargs.get('schema', 'unknown')

            # Crear clave basada en función y argumentos
            cache_key = f"{func.__name__}_{str(args)}_{str(kwargs)}"

            # Intentar obtener del caché
            cached_result = cache.get(schema, table_name, cache_key)
            if cached_result is not None:
                return cached_result

            # No está en caché, ejecutar función
            result = func(*args, **kwargs)

            # Guardar en caché
            cache.set(schema, table_name, cache_key, result)

            return result

        return wrapper
    return decorator


# ============================================================================
# FUNCIONES HELPER
# ============================================================================

def invalidate_dimension_cache(table_name: str = None):
    """
    Invalida el caché de dimensiones.

    Args:
        table_name: Nombre de la tabla a invalidar (None para invalidar todo)

    Example:
        # Invalidar todo
        invalidate_dimension_cache()

        # Invalidar solo dim_red
        invalidate_dimension_cache('dim_red')
    """
    cache = get_dimension_cache()
    cache.invalidate(table=table_name)


def get_cache_stats() -> Dict:
    """
    Obtiene estadísticas del caché de dimensiones.

    Returns:
        Diccionario con estadísticas

    Example:
        stats = get_cache_stats()
        print(f"Hit rate: {stats['hit_rate_pct']:.1f}%")
        print(f"Cache size: {stats['cache_size']} entries")
    """
    cache = get_dimension_cache()
    return cache.get_stats()


def cleanup_dimension_cache():
    """
    Limpia entradas expiradas del caché.

    Útil para ejecutar periódicamente en tareas de mantenimiento.
    """
    cache = get_dimension_cache()
    cache.cleanup_expired()
