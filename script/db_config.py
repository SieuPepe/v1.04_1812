"""
Configuración centralizada de base de datos.

Este módulo maneja toda la configuración de conexión a la base de datos,
incluyendo host, puerto, y esquemas.

Configuración mediante (en orden de prioridad):
1. Variables de entorno
2. Archivo de configuración del usuario
3. Valores por defecto
"""

import os
from pathlib import Path
from typing import Optional


class DatabaseConfig:
    """Configuración de base de datos centralizada."""

    # Valores por defecto (pueden ser sobrescritos por variables de entorno o config de usuario)
    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = 3307
    DEFAULT_MANAGER_SCHEMA = 'manager'
    DEFAULT_EXAMPLE_SCHEMA = 'cert_dev'

    # Esquemas válidos para el generador de partes
    # Solo estos esquemas están preparados con las tablas necesarias
    VALID_PARTS_GENERATOR_SCHEMAS = ['cert_dev']

    def __init__(self):
        """Inicializa la configuración desde variables de entorno o valores por defecto."""
        self._load_config()

    def _load_user_config(self):
        """
        Intenta cargar la configuración del usuario desde db_user_config.

        Returns:
            dict: Configuración del usuario, o None si no existe
        """
        try:
            from .db_user_config import get_connection_config
            user_config = get_connection_config()
            if user_config.is_configured:
                return user_config.config
        except (ImportError, Exception):
            pass
        return None

    def _load_config(self):
        """
        Carga configuración con la siguiente prioridad:
        1. Variables de entorno (más alta)
        2. Archivo de configuración del usuario
        3. Valores por defecto
        """
        # Intentar cargar configuración de usuario
        user_config = self._load_user_config()

        # Host: env var > user config > default
        if os.getenv('DB_HOST'):
            self.host = os.getenv('DB_HOST')
        elif user_config and 'host' in user_config:
            self.host = user_config['host']
        else:
            self.host = self.DEFAULT_HOST

        # Port: env var > user config > default
        if os.getenv('DB_PORT'):
            self.port = int(os.getenv('DB_PORT'))
        elif user_config and 'port' in user_config:
            self.port = user_config['port']
        else:
            self.port = self.DEFAULT_PORT

        # Esquemas (solo desde env var o default)
        self.manager_schema = os.getenv('DB_MANAGER_SCHEMA', self.DEFAULT_MANAGER_SCHEMA)
        self.example_schema = os.getenv('DB_EXAMPLE_SCHEMA', self.DEFAULT_EXAMPLE_SCHEMA)

    @property
    def connection_params(self) -> dict:
        """
        Retorna los parámetros base de conexión (sin credenciales).

        Returns:
            dict: Diccionario con host y port
        """
        return {
            'host': self.host,
            'port': self.port
        }

    def get_connection_params(self, database: Optional[str] = None) -> dict:
        """
        Retorna parámetros de conexión incluyendo opcionalmente la base de datos.

        Args:
            database: Nombre de la base de datos (opcional)

        Returns:
            dict: Parámetros de conexión
        """
        params = self.connection_params.copy()
        if database:
            params['database'] = database
        return params

    def get_manager_connection_params(self) -> dict:
        """Retorna parámetros para conectar al esquema manager."""
        return self.get_connection_params(self.manager_schema)

    def get_project_connection_params(self, project_code: str) -> dict:
        """
        Retorna parámetros para conectar a un esquema de proyecto.

        Args:
            project_code: Código del proyecto

        Returns:
            dict: Parámetros de conexión al proyecto
        """
        return self.get_connection_params(project_code)


# Instancia global de configuración
config = DatabaseConfig()


def get_config() -> DatabaseConfig:
    """
    Retorna la instancia de configuración global.

    Returns:
        DatabaseConfig: Configuración de base de datos
    """
    return config


def reload_config():
    """Recarga la configuración desde las variables de entorno."""
    global config
    config = DatabaseConfig()
    return config
