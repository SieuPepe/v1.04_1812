"""
Script package - Database modules

Este paquete contiene todos los módulos de base de datos refactorizados:
- db_config: Configuración centralizada
- db_connection: Gestión de conexiones con context managers
- db_core: Funciones core de base de datos
- db_projects: Gestión de proyectos, clientes y presupuestos
- db_partes: Gestión de partes de trabajo
- modulo_db: Re-exportación para compatibilidad

Uso:
    from script.modulo_db import login_db, add_project_item

    # O importar directamente desde módulos específicos:
    from script.db_core import login_db
    from script.db_projects import add_project_item
"""

__version__ = '2.0.0'
__author__ = 'Claude (Anthropic)'
