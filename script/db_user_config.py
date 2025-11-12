#!/usr/bin/env python3
"""
Módulo de configuración persistente de conexión a base de datos
================================================================

Este módulo maneja la configuración de conexión del usuario, permitiendo:
- Configurar host, puerto y usuario de la base de datos
- Guardar la configuración de forma persistente (SIN contraseñas)
- Solicitar la contraseña en cada inicio de sesión
- Soportar conexiones locales y remotas

La contraseña NUNCA se guarda en disco por seguridad.

Ubicación del archivo de configuración:
- Windows: %APPDATA%/HydroFlow/connection.json
- Linux/Mac: ~/.config/hydroflow/connection.json
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict
import getpass


class ConnectionConfig:
    """Gestiona la configuración de conexión a la base de datos"""

    def __init__(self):
        """Inicializa el gestor de configuración"""
        self.config_dir = self._get_config_dir()
        self.config_file = self.config_dir / 'connection.json'
        self.config = self._load_config()

    def _get_config_dir(self) -> Path:
        """
        Obtiene el directorio de configuración según el sistema operativo.

        Returns:
            Path al directorio de configuración
        """
        if os.name == 'nt':  # Windows
            base_dir = Path(os.getenv('APPDATA', Path.home() / 'AppData' / 'Roaming'))
            config_dir = base_dir / 'HydroFlow'
        else:  # Linux/Mac
            config_dir = Path.home() / '.config' / 'hydroflow'

        # Crear directorio si no existe
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir

    def _load_config(self) -> Dict:
        """
        Carga la configuración desde el archivo.

        Returns:
            Diccionario con la configuración, o valores por defecto
        """
        default_config = {
            'host': 'localhost',
            'port': 3307,
            'user': '',
            'remember_user': False,
            'connection_type': 'local'  # 'local' o 'remote'
        }

        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge con default para asegurar que existan todos los campos
                    return {**default_config, **loaded_config}
            except Exception as e:
                print(f"⚠ Error al cargar configuración: {e}")
                print("  Usando configuración por defecto")
                return default_config
        else:
            return default_config

    def _save_config(self):
        """Guarda la configuración actual en el archivo"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            print(f"✗ Error al guardar configuración: {e}")
            return False

    def configure_connection(self, interactive=True) -> bool:
        """
        Configura la conexión de forma interactiva o programática.

        Args:
            interactive: Si True, solicita datos al usuario. Si False, usa valores actuales.

        Returns:
            True si la configuración fue exitosa
        """
        if interactive:
            print("\n" + "="*70)
            print("CONFIGURACIÓN DE CONEXIÓN A BASE DE DATOS")
            print("="*70)
            print("\n⚠ La contraseña NO se guardará por seguridad.")
            print("Se solicitará cada vez que inicie la aplicación.\n")

            # Tipo de conexión
            print("Tipo de conexión:")
            print("  1. Base de datos local (localhost)")
            print("  2. Base de datos en servidor remoto")

            while True:
                choice = input("\nSeleccione una opción [1/2]: ").strip()
                if choice == '1':
                    self.config['connection_type'] = 'local'
                    self.config['host'] = 'localhost'
                    break
                elif choice == '2':
                    self.config['connection_type'] = 'remote'
                    break
                else:
                    print("✗ Opción inválida. Ingrese 1 o 2.")

            # Si es remoto, solicitar host
            if self.config['connection_type'] == 'remote':
                print("\nIngrese la dirección del servidor:")
                print("  (puede ser una IP como 192.168.1.100 o un nombre de dominio)")
                host = input(f"Host [{self.config.get('host', '')}]: ").strip()
                if host:
                    self.config['host'] = host

            # Puerto
            print(f"\nPuerto de MySQL/MariaDB:")
            port_input = input(f"Puerto [{self.config.get('port', 3307)}]: ").strip()
            if port_input:
                try:
                    self.config['port'] = int(port_input)
                except ValueError:
                    print("⚠ Puerto inválido. Usando valor por defecto.")

            # Usuario
            print("\nUsuario de base de datos:")
            print("  (debe tener permisos de administrador para crear proyectos)")
            user = input(f"Usuario [{self.config.get('user', 'root')}]: ").strip()
            if user:
                self.config['user'] = user

            # Recordar usuario
            remember = input("\n¿Recordar usuario? [S/n]: ").strip().lower()
            self.config['remember_user'] = remember != 'n'

            # Guardar configuración
            print("\n" + "-"*70)
            print("Resumen de configuración:")
            print(f"  Tipo:    {self.config['connection_type']}")
            print(f"  Host:    {self.config['host']}")
            print(f"  Puerto:  {self.config['port']}")
            print(f"  Usuario: {self.config['user']}")
            print("-"*70)

            confirm = input("\n¿Guardar esta configuración? [S/n]: ").strip().lower()
            if confirm == 'n':
                print("✗ Configuración cancelada")
                return False

            if self._save_config():
                print(f"\n✓ Configuración guardada en: {self.config_file}")
                return True
            else:
                return False

        else:
            # Modo no interactivo: solo guardar config actual
            return self._save_config()

    def get_connection_params(self, password: Optional[str] = None,
                            database: Optional[str] = None,
                            ask_password: bool = True) -> Dict:
        """
        Obtiene los parámetros de conexión.

        Args:
            password: Contraseña (si None y ask_password=True, la solicita)
            database: Nombre de la base de datos (opcional)
            ask_password: Si True, solicita la contraseña si no se proporciona

        Returns:
            Diccionario con parámetros de conexión
        """
        params = {
            'host': self.config['host'],
            'port': self.config['port'],
            'user': self.config['user']
        }

        # Solicitar contraseña si es necesario
        if password is None and ask_password:
            password = getpass.getpass(f"Contraseña para {self.config['user']}@{self.config['host']}: ")

        if password:
            params['password'] = password

        if database:
            params['database'] = database

        return params

    def get_credentials(self, ask_password: bool = True) -> tuple:
        """
        Obtiene usuario y contraseña.

        Args:
            ask_password: Si True, solicita la contraseña

        Returns:
            Tupla (user, password)
        """
        user = self.config['user']
        password = None

        if ask_password:
            password = getpass.getpass(f"Contraseña para {user}@{self.config['host']}: ")

        return user, password

    def update_setting(self, key: str, value) -> bool:
        """
        Actualiza un valor de configuración.

        Args:
            key: Clave a actualizar
            value: Nuevo valor

        Returns:
            True si se guardó exitosamente
        """
        if key in self.config:
            self.config[key] = value
            return self._save_config()
        else:
            print(f"✗ Configuración '{key}' no existe")
            return False

    def reset_config(self) -> bool:
        """
        Reinicia la configuración a valores por defecto.

        Returns:
            True si se eliminó exitosamente
        """
        try:
            if self.config_file.exists():
                self.config_file.unlink()
            self.config = self._load_config()
            print("✓ Configuración reiniciada")
            return True
        except Exception as e:
            print(f"✗ Error al reiniciar configuración: {e}")
            return False

    def show_current_config(self):
        """Muestra la configuración actual"""
        print("\n" + "="*70)
        print("CONFIGURACIÓN ACTUAL")
        print("="*70)
        print(f"Archivo:  {self.config_file}")
        print(f"Tipo:     {self.config['connection_type']}")
        print(f"Host:     {self.config['host']}")
        print(f"Puerto:   {self.config['port']}")
        print(f"Usuario:  {self.config['user']}")
        print(f"Recordar: {'Sí' if self.config.get('remember_user') else 'No'}")
        print("="*70 + "\n")

    @property
    def is_configured(self) -> bool:
        """
        Verifica si ya existe una configuración guardada.

        Returns:
            True si el archivo de configuración existe
        """
        return self.config_file.exists() and self.config.get('user', '') != ''


# Singleton para acceso global
_connection_config_instance = None


def get_connection_config() -> ConnectionConfig:
    """
    Obtiene la instancia global de configuración de conexión.

    Returns:
        Instancia de ConnectionConfig
    """
    global _connection_config_instance
    if _connection_config_instance is None:
        _connection_config_instance = ConnectionConfig()
    return _connection_config_instance


def main():
    """Función principal para configurar desde línea de comandos"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Configuración de conexión a base de datos',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--configure', action='store_true',
                        help='Configurar la conexión')
    parser.add_argument('--show', action='store_true',
                        help='Mostrar configuración actual')
    parser.add_argument('--reset', action='store_true',
                        help='Reiniciar configuración')
    parser.add_argument('--set', nargs=2, metavar=('KEY', 'VALUE'),
                        help='Establecer un valor (ej: --set host 192.168.1.100)')

    args = parser.parse_args()

    config = get_connection_config()

    if args.configure:
        config.configure_connection(interactive=True)
    elif args.show:
        config.show_current_config()
    elif args.reset:
        confirm = input("¿Está seguro de reiniciar la configuración? [s/N]: ").strip().lower()
        if confirm == 's':
            config.reset_config()
    elif args.set:
        key, value = args.set
        # Convertir tipos según la clave
        if key == 'port':
            value = int(value)
        elif key == 'remember_user':
            value = value.lower() in ('true', 'yes', 's', '1')

        if config.update_setting(key, value):
            print(f"✓ {key} = {value}")
    else:
        parser.print_help()
        print("\nConfiguración actual:")
        config.show_current_config()


if __name__ == '__main__':
    main()
