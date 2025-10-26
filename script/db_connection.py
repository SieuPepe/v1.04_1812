"""
Gestión de conexiones a la base de datos.

Este módulo proporciona clases y funciones para manejar conexiones
a MySQL de forma eficiente y segura usando context managers.
"""

import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
from typing import Optional, Dict, Any
from .db_config import get_config


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
