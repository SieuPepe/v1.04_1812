"""
Módulo de configuración de HydroFlow Manager.
"""

from .connection_manager import (
    load_profiles,
    save_profiles,
    get_active_profile,
    get_profile_names,
    get_profile,
    set_active_profile,
    add_profile,
    update_profile,
    delete_profile,
    test_connection
)

__all__ = [
    'load_profiles',
    'save_profiles',
    'get_active_profile',
    'get_profile_names',
    'get_profile',
    'set_active_profile',
    'add_profile',
    'update_profile',
    'delete_profile',
    'test_connection'
]
