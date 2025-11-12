#!/usr/bin/env python3
"""
Script de Configuración Inicial de HydroFlow Manager
=====================================================

Este script debe ejecutarse durante la primera instalación para configurar
la conexión a la base de datos.

Uso:
    python configurar_instalacion.py
"""

import sys
import os
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from script.db_user_config import get_connection_config
from script import db_core


def print_header():
    """Imprime el encabezado del instalador"""
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║                HYDROFLOW MANAGER - CONFIGURACIÓN INICIAL          ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

Bienvenido a HydroFlow Manager.

Este asistente le ayudará a configurar la conexión a la base de datos.

IMPORTANTE:
- Necesita tener MySQL/MariaDB instalado y en funcionamiento
- Debe conocer las credenciales de un usuario con privilegios administrativos
- La contraseña NO se guardará en disco por seguridad

""")


def test_connection(config):
    """
    Prueba la conexión con las credenciales configuradas.

    Args:
        config: Instancia de ConnectionConfig

    Returns:
        True si la conexión fue exitosa
    """
    print("\n" + "="*70)
    print("PROBANDO CONEXIÓN...")
    print("="*70)

    user, password = config.get_credentials(ask_password=True)

    print(f"\nConectando a {config.config['host']}:{config.config['port']}...")

    try:
        conn, error = db_core.login_db(user, password)

        if error:
            print(f"\n✗ Error de conexión: {error}")
            print("\nPosibles causas:")
            print("  • Usuario o contraseña incorrectos")
            print("  • MySQL/MariaDB no está en funcionamiento")
            print("  • Host o puerto incorrectos")
            print("  • Firewall bloqueando la conexión")
            return False

        print("\n✓ ¡Conexión exitosa!")
        print("\nLa configuración es correcta.")

        return True

    except Exception as e:
        print(f"\n✗ Error inesperado: {e}")
        return False


def main():
    """Función principal"""
    print_header()

    # Obtener configuración
    config = get_connection_config()

    # Si ya está configurado, preguntar si desea reconfigurar
    if config.is_configured:
        print("⚠ Ya existe una configuración guardada.")
        config.show_current_config()

        response = input("¿Desea reconfigurar la conexión? [s/N]: ").strip().lower()
        if response != 's':
            print("\nManteniendo configuración actual.")
            print("Para reconfigurar más tarde, ejecute:")
            print("  python configurar_instalacion.py")
            return

        print("\nReconfigurando...")

    # Configurar conexión
    if not config.configure_connection(interactive=True):
        print("\n✗ Configuración cancelada")
        sys.exit(1)

    # Probar conexión
    print("\n" + "="*70)
    print("¿Desea probar la conexión ahora?")
    print("  (Se le solicitará la contraseña para verificar)")
    response = input("\nProbar conexión [S/n]: ").strip().lower()

    if response != 'n':
        if test_connection(config):
            print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║                  ✓ CONFIGURACIÓN COMPLETADA                       ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

La aplicación está lista para usarse.

PRÓXIMOS PASOS:
1. Ejecute HydroFlowManager
2. Ingrese con sus credenciales de base de datos
3. ¡Comience a trabajar!

NOTA: Se le solicitará la contraseña cada vez que inicie la aplicación
      por razones de seguridad.
            """)
        else:
            print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║                  ⚠ CONFIGURACIÓN CON ERRORES                      ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

La configuración se guardó, pero la conexión falló.

Verifique:
- Que MySQL/MariaDB esté en funcionamiento
- Que el host y puerto sean correctos
- Que las credenciales sean válidas

Para reconfigurar, ejecute nuevamente:
  python configurar_instalacion.py
            """)
            sys.exit(1)
    else:
        print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║                  ✓ CONFIGURACIÓN GUARDADA                         ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

La configuración se guardó exitosamente.

Para probar la conexión más tarde, puede iniciar HydroFlowManager.

        """)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Configuración cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}")
        sys.exit(1)
