"""
Gestor de perfiles de conexión.
Permite guardar y cargar diferentes configuraciones de conexión (Local, VPN, etc.)
"""

import os
import json
from typing import Dict, Optional, List

# Ruta del archivo de configuración
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILES_FILE = os.path.join(CONFIG_DIR, "connection_profiles.json")


def _get_default_config() -> dict:
    """Retorna configuración por defecto si no existe el archivo."""
    return {
        "active_profile": "local",
        "profiles": {
            "local": {
                "name": "Local",
                "host": "127.0.0.1",
                "port": 3306,
                "schema": "cert_dev"
            }
        }
    }


def load_profiles() -> dict:
    """
    Carga los perfiles de conexión desde el archivo JSON.

    Returns:
        dict: Configuración con perfiles y perfil activo
    """
    try:
        if os.path.exists(PROFILES_FILE):
            with open(PROFILES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Crear archivo con configuración por defecto
            config = _get_default_config()
            save_profiles(config)
            return config
    except Exception as e:
        print(f"Error cargando perfiles: {e}")
        return _get_default_config()


def save_profiles(config: dict) -> bool:
    """
    Guarda los perfiles de conexión en el archivo JSON.

    Args:
        config: Diccionario con la configuración completa

    Returns:
        bool: True si se guardó correctamente
    """
    try:
        with open(PROFILES_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error guardando perfiles: {e}")
        return False


def get_active_profile() -> Optional[dict]:
    """
    Obtiene el perfil de conexión activo.

    Returns:
        dict: Datos del perfil activo o None
    """
    config = load_profiles()
    active_id = config.get("active_profile")
    profiles = config.get("profiles", {})
    return profiles.get(active_id)


def get_profile_names() -> List[str]:
    """
    Obtiene lista de nombres de perfiles disponibles.

    Returns:
        List[str]: Lista de IDs de perfiles
    """
    config = load_profiles()
    return list(config.get("profiles", {}).keys())


def get_profile(profile_id: str) -> Optional[dict]:
    """
    Obtiene un perfil específico por su ID.

    Args:
        profile_id: ID del perfil

    Returns:
        dict: Datos del perfil o None
    """
    config = load_profiles()
    return config.get("profiles", {}).get(profile_id)


def set_active_profile(profile_id: str) -> bool:
    """
    Establece el perfil activo.

    Args:
        profile_id: ID del perfil a activar

    Returns:
        bool: True si se estableció correctamente
    """
    config = load_profiles()
    if profile_id in config.get("profiles", {}):
        config["active_profile"] = profile_id
        return save_profiles(config)
    return False


def add_profile(profile_id: str, name: str, host: str, port: int, schema: str) -> bool:
    """
    Añade un nuevo perfil de conexión.

    Args:
        profile_id: ID único del perfil
        name: Nombre descriptivo
        host: Host/IP del servidor
        port: Puerto de conexión
        schema: Esquema por defecto

    Returns:
        bool: True si se añadió correctamente
    """
    config = load_profiles()
    config["profiles"][profile_id] = {
        "name": name,
        "host": host,
        "port": port,
        "schema": schema
    }
    return save_profiles(config)


def update_profile(profile_id: str, name: str, host: str, port: int, schema: str) -> bool:
    """
    Actualiza un perfil existente.

    Args:
        profile_id: ID del perfil a actualizar
        name: Nuevo nombre
        host: Nuevo host
        port: Nuevo puerto
        schema: Nuevo esquema

    Returns:
        bool: True si se actualizó correctamente
    """
    config = load_profiles()
    if profile_id in config.get("profiles", {}):
        config["profiles"][profile_id] = {
            "name": name,
            "host": host,
            "port": port,
            "schema": schema
        }
        return save_profiles(config)
    return False


def delete_profile(profile_id: str) -> bool:
    """
    Elimina un perfil de conexión.

    Args:
        profile_id: ID del perfil a eliminar

    Returns:
        bool: True si se eliminó correctamente
    """
    config = load_profiles()
    profiles = config.get("profiles", {})

    # No permitir eliminar el último perfil
    if len(profiles) <= 1:
        return False

    # No permitir eliminar el perfil activo
    if config.get("active_profile") == profile_id:
        return False

    if profile_id in profiles:
        del profiles[profile_id]
        return save_profiles(config)
    return False


def test_connection(host: str, port: int, user: str, password: str) -> tuple:
    """
    Prueba la conexión con los parámetros dados.

    Args:
        host: Host del servidor
        port: Puerto
        user: Usuario
        password: Contraseña

    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            connection_timeout=5
        )
        conn.close()
        return True, "Conexión exitosa"
    except Exception as e:
        return False, str(e)
