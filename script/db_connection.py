"""
Gestión de conexiones a la base de datos.

Este módulo proporciona clases y funciones para manejar conexiones
a MySQL de forma eficiente y segura usando context managers.

Incluye connection pooling para mejorar el rendimiento:
- Pool de conexiones para reducir latencia de ~50ms a ~1ms
- Reutilización de conexiones existentes
- Límites configurables de pool por usuario/esquema
"""

import mysql.connector
from mysql.connector import Error, pooling
from contextlib import contextmanager
from typing import Optional, Dict, Any
import logging
from .db_config import get_config

logger = logging.getLogger(__name__)


# ============================================================================
# CONNECTION POOLING
# ============================================================================

class ConnectionPoolManager:
    """
    Gestor de pools de conexiones a MySQL.

    Mantiene un pool de conexiones por cada combinación de user/database
    para reutilizar conexiones y reducir latencia.

    Configuración:
    - pool_size: 5 conexiones por pool (default)
    - pool_name: Auto-generado basado en user/database
    - pool_reset_session: True (reset automático de sesión)
    """

    # Diccionario de pools: {(user, database): MySQLConnectionPool}
    _pools: Dict[tuple, pooling.MySQLConnectionPool] = {}

    # Configuración de pool
    DEFAULT_POOL_SIZE = 5
    DEFAULT_POOL_NAME_PREFIX = "hydroflow_pool"

    @classmethod
    def get_pool(cls, user: str, password: str, database: Optional[str] = None) -> pooling.MySQLConnectionPool:
        """
        Obtiene o crea un pool de conexiones para user/database.

        Args:
            user: Usuario de MySQL
            password: Contraseña del usuario
            database: Nombre de la base de datos (opcional)

        Returns:
            Pool de conexiones MySQL
        """
        # Crear clave única para el pool
        pool_key = (user, database or '')

        # Si el pool ya existe, retornarlo
        if pool_key in cls._pools:
            logger.debug(f"Usando pool existente para {user}/{database or 'sin_db'}")
            return cls._pools[pool_key]

        # Crear nuevo pool
        logger.info(f"Creando nuevo pool de conexiones para {user}/{database or 'sin_db'}")

        config = get_config()
        pool_config = config.connection_params.copy()
        pool_config['user'] = user
        pool_config['password'] = password

        if database:
            pool_config['database'] = database

        # Configuración del pool
        pool_name = f"{cls.DEFAULT_POOL_NAME_PREFIX}_{user}_{database or 'nodb'}"
        pool_config['pool_name'] = pool_name
        pool_config['pool_size'] = cls.DEFAULT_POOL_SIZE
        pool_config['pool_reset_session'] = True

        try:
            pool = pooling.MySQLConnectionPool(**pool_config)
            cls._pools[pool_key] = pool
            logger.info(f"Pool '{pool_name}' creado con {cls.DEFAULT_POOL_SIZE} conexiones")
            return pool

        except Error as e:
            logger.error(f"Error creando pool de conexiones: {e}")
            raise ConnectionError(f"Error creando pool: {e}")

    @classmethod
    def get_connection_from_pool(cls, user: str, password: str, database: Optional[str] = None):
        """
        Obtiene una conexión del pool.

        Args:
            user: Usuario de MySQL
            password: Contraseña del usuario
            database: Nombre de la base de datos (opcional)

        Returns:
            Conexión MySQL del pool

        Raises:
            Error: Si no hay conexiones disponibles en el pool
        """
        pool = cls.get_pool(user, password, database)

        try:
            connection = pool.get_connection()
            logger.debug(f"Conexión obtenida del pool para {user}/{database or 'sin_db'}")
            return connection

        except Error as e:
            logger.error(f"Error obteniendo conexión del pool: {e}")
            raise

    @classmethod
    def close_all_pools(cls):
        """Cierra todos los pools de conexiones."""
        logger.info(f"Cerrando {len(cls._pools)} pools de conexiones")
        cls._pools.clear()

    @classmethod
    def get_pool_stats(cls) -> Dict:
        """
        Obtiene estadísticas de los pools de conexiones.

        Returns:
            Diccionario con estadísticas de cada pool
        """
        stats = {}
        for (user, database), pool in cls._pools.items():
            key = f"{user}/{database or 'sin_db'}"
            stats[key] = {
                'pool_name': pool.pool_name,
                'pool_size': pool._pool_size
            }
        return stats


class DatabaseConnection:
    """Manejador de conexiones a la base de datos con context manager."""

    def __init__(self, user: str, password: str, database: Optional[str] = None):
        """
        Inicializa el manejador de conexión.

        Args:
            user: Usuario de la base de datos
            password: Contraseña del usuario
            database: Nombre de la base de datos (opcional)
        """
        self.user = user
        self.password = password
        self.database = database
        self.config = get_config()
        self._connection = None

    def __enter__(self):
        """Abre la conexión cuando se entra al contexto."""
        params = self.config.connection_params.copy()
        params['user'] = self.user
        params['password'] = self.password

        if self.database:
            params['database'] = self.database

        try:
            self._connection = mysql.connector.connect(**params)
            return self._connection
        except Error as e:
            raise ConnectionError(f"Error al conectar a la base de datos: {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra la conexión cuando se sale del contexto."""
        if self._connection and self._connection.is_connected():
            self._connection.close()


@contextmanager
def get_connection(user: str, password: str, database: Optional[str] = None):
    """
    Context manager para obtener una conexión a la base de datos.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        database: Nombre de la base de datos (opcional)

    Yields:
        Connection: Conexión a MySQL

    Example:
        with get_connection('user', 'pass', 'schema') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM table")
    """
    config = get_config()
    params = config.connection_params.copy()
    params['user'] = user
    params['password'] = password

    if database:
        params['database'] = database

    connection = None
    try:
        connection = mysql.connector.connect(**params)
        yield connection
    except Error as e:
        raise ConnectionError(f"Error al conectar a la base de datos: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()


@contextmanager
def get_manager_connection(user: str, password: str):
    """
    Context manager para obtener una conexión al esquema manager.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario

    Yields:
        Connection: Conexión al esquema manager

    Example:
        with get_manager_connection('user', 'pass') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tbl_cliente")
    """
    config = get_config()
    with get_connection(user, password, config.manager_schema) as conn:
        yield conn


@contextmanager
def get_project_connection(user: str, password: str, project_code: str):
    """
    Context manager para obtener una conexión a un esquema de proyecto.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        project_code: Código del proyecto

    Yields:
        Connection: Conexión al esquema del proyecto

    Example:
        with get_project_connection('user', 'pass', 'PRJ001') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tbl_partes")
    """
    with get_connection(user, password, project_code) as conn:
        yield conn


def execute_query(user: str, password: str, query: str, params: tuple = None,
                  database: Optional[str] = None, fetch: str = 'all') -> Any:
    """
    Ejecuta una consulta SELECT y retorna los resultados.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        query: Consulta SQL
        params: Parámetros de la consulta (opcional)
        database: Nombre de la base de datos (opcional)
        fetch: Tipo de fetch ('all', 'one', 'many')

    Returns:
        Resultados de la consulta

    Example:
        results = execute_query('user', 'pass', 'SELECT * FROM table WHERE id=%s', (1,))
    """
    with get_connection(user, password, database) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params or ())

        if fetch == 'one':
            result = cursor.fetchone()
        elif fetch == 'many':
            result = cursor.fetchmany()
        else:  # 'all'
            result = cursor.fetchall()

        cursor.close()
        return result


def execute_transaction(user: str, password: str, queries: list,
                       database: Optional[str] = None) -> str:
    """
    Ejecuta múltiples consultas en una transacción.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        queries: Lista de tuplas (query, params)
        database: Nombre de la base de datos (opcional)

    Returns:
        str: 'ok' si la transacción fue exitosa

    Raises:
        Error: Si hay algún error en la transacción

    Example:
        queries = [
            ("INSERT INTO table (col) VALUES (%s)", ('value1',)),
            ("UPDATE table SET col=%s WHERE id=%s", ('value2', 1))
        ]
        execute_transaction('user', 'pass', queries, 'schema')
    """
    with get_connection(user, password, database) as conn:
        cursor = conn.cursor()
        try:
            conn.start_transaction()

            for query, params in queries:
                cursor.execute(query, params or ())

            conn.commit()
            cursor.close()
            return "ok"

        except Error as e:
            conn.rollback()
            cursor.close()
            raise e


def execute_insert(user: str, password: str, query: str, params: tuple = None,
                   database: Optional[str] = None) -> int:
    """
    Ejecuta una consulta INSERT y retorna el ID insertado.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        query: Consulta SQL INSERT
        params: Parámetros de la consulta
        database: Nombre de la base de datos (opcional)

    Returns:
        int: ID del registro insertado

    Example:
        new_id = execute_insert('user', 'pass', 'INSERT INTO table (col) VALUES (%s)', ('value',))
    """
    with get_connection(user, password, database) as conn:
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            cursor.execute(query, params or ())
            new_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            return new_id

        except Error as e:
            conn.rollback()
            cursor.close()
            raise e


def execute_update(user: str, password: str, query: str, params: tuple = None,
                   database: Optional[str] = None) -> str:
    """
    Ejecuta una consulta UPDATE/DELETE.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        query: Consulta SQL UPDATE/DELETE
        params: Parámetros de la consulta
        database: Nombre de la base de datos (opcional)

    Returns:
        str: 'ok' si fue exitosa

    Example:
        execute_update('user', 'pass', 'UPDATE table SET col=%s WHERE id=%s', ('value', 1))
    """
    with get_connection(user, password, database) as conn:
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            cursor.execute(query, params or ())
            conn.commit()
            cursor.close()
            return "ok"

        except Error as e:
            conn.rollback()
            cursor.close()
            raise e


# ============================================================================
# CONNECTION POOLING - CONTEXT MANAGERS
# ============================================================================

@contextmanager
def get_connection_pooled(user: str, password: str, database: Optional[str] = None):
    """
    Context manager para obtener una conexión del pool.

    Obtiene una conexión reutilizable del pool de conexiones,
    reduciendo la latencia de ~50ms a ~1ms.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        database: Nombre de la base de datos (opcional)

    Yields:
        Connection: Conexión a MySQL desde el pool

    Example:
        with get_connection_pooled('user', 'pass', 'schema') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM table")

    Note:
        La conexión se retorna automáticamente al pool al salir del contexto.
    """
    connection = None
    try:
        connection = ConnectionPoolManager.get_connection_from_pool(user, password, database)
        yield connection
    except Error as e:
        raise ConnectionError(f"Error al conectar a la base de datos desde pool: {e}")
    finally:
        # La conexión se retorna al pool automáticamente al cerrarla
        if connection and connection.is_connected():
            connection.close()


@contextmanager
def get_manager_connection_pooled(user: str, password: str):
    """
    Context manager para obtener una conexión pooled al esquema manager.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario

    Yields:
        Connection: Conexión al esquema manager desde pool

    Example:
        with get_manager_connection_pooled('user', 'pass') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tbl_cliente")
    """
    config = get_config()
    with get_connection_pooled(user, password, config.manager_schema) as conn:
        yield conn


@contextmanager
def get_project_connection_pooled(user: str, password: str, project_code: str):
    """
    Context manager para obtener una conexión pooled a un esquema de proyecto.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        project_code: Código del proyecto

    Yields:
        Connection: Conexión al esquema del proyecto desde pool

    Example:
        with get_project_connection_pooled('user', 'pass', 'PRJ001') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tbl_partes")
    """
    with get_connection_pooled(user, password, project_code) as conn:
        yield conn


# ============================================================================
# AUTO-SELECTION DE POOLING
# ============================================================================

# Variable para activar/desactivar pooling globalmente
import os
USE_CONNECTION_POOLING = os.getenv('DB_USE_POOLING', 'true').lower() in ('true', '1', 'yes')


def get_connection_auto(user: str, password: str, database: Optional[str] = None):
    """
    Auto-selecciona entre conexión normal o pooled según configuración.

    Usa la variable de entorno DB_USE_POOLING para decidir:
    - DB_USE_POOLING=true (default): Usa connection pooling
    - DB_USE_POOLING=false: Usa conexiones directas

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        database: Nombre de la base de datos (opcional)

    Yields:
        Connection: Conexión a MySQL (pooled o directa)

    Example:
        with get_connection_auto('user', 'pass', 'schema') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM table")
    """
    if USE_CONNECTION_POOLING:
        return get_connection_pooled(user, password, database)
    else:
        return get_connection(user, password, database)


def get_project_connection_auto(user: str, password: str, project_code: str):
    """
    Auto-selecciona entre conexión normal o pooled para proyectos.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        project_code: Código del proyecto

    Yields:
        Connection: Conexión al esquema del proyecto

    Example:
        with get_project_connection_auto('user', 'pass', 'PRJ001') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tbl_partes")
    """
    if USE_CONNECTION_POOLING:
        return get_project_connection_pooled(user, password, project_code)
    else:
        return get_project_connection(user, password, project_code)
