#!/usr/bin/env python3
"""
Script de compilación para HydroFlow Manager
Automatiza la creación del ejecutable y el instalador

Requisitos:
    - PyInstaller: pip install pyinstaller
    - Inno Setup: https://jrsoftware.org/isdl.php (solo Windows)

Uso:
    python build.py --all          # Compila ejecutable e instalador
    python build.py --exe          # Solo compila ejecutable
    python build.py --installer    # Solo crea instalador (requiere exe compilado)
    python build.py --clean        # Limpia archivos de compilación
"""

import os
import sys
import shutil
import subprocess
import argparse
from pathlib import Path


class Colors:
    """Colores ANSI para output en terminal"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_step(message):
    """Imprime un paso del proceso"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")


def print_success(message):
    """Imprime mensaje de éxito"""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")


def print_error(message):
    """Imprime mensaje de error"""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")


def print_warning(message):
    """Imprime mensaje de advertencia"""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")


def print_info(message):
    """Imprime mensaje informativo"""
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")


def check_dependencies():
    """Verifica que las dependencias necesarias estén instaladas"""
    print_step("Verificando dependencias")

    # Verificar Python
    python_version = sys.version_info
    if python_version < (3, 9):
        print_error(f"Se requiere Python 3.9 o superior. Versión actual: {python_version.major}.{python_version.minor}")
        return False
    print_success(f"Python {python_version.major}.{python_version.minor}.{python_version.micro}")

    # Verificar PyInstaller
    try:
        import PyInstaller
        print_success(f"PyInstaller {PyInstaller.__version__}")
    except ImportError:
        print_error("PyInstaller no está instalado")
        print_info("Instalar con: pip install pyinstaller")
        return False

    # Verificar dependencias del proyecto
    dependencies = [
        'customtkinter',
        'mysql.connector',
        'tkcalendar',
        'PIL',
        'matplotlib',
        'openpyxl',
        'xlsxwriter',
        'docx',
        'reportlab'
    ]

    missing = []
    for dep in dependencies:
        try:
            if dep == 'mysql.connector':
                __import__('mysql.connector')
            elif dep == 'PIL':
                __import__('PIL')
            elif dep == 'docx':
                __import__('docx')
            else:
                __import__(dep)
            print_success(f"{dep}")
        except ImportError:
            missing.append(dep)
            print_error(f"{dep} - NO INSTALADO")

    if missing:
        print_warning("\nDependencias faltantes. Instalar con:")
        print_info("pip install -r requirements.txt")
        return False

    return True


def clean_build():
    """Limpia archivos de compilación anteriores"""
    print_step("Limpiando archivos de compilación anteriores")

    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.pyc', '*.pyo', '*.spec~']

    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print_success(f"Eliminado: {dir_name}/")

    # Buscar y eliminar __pycache__ en subdirectorios
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                path = os.path.join(root, dir_name)
                shutil.rmtree(path)
                print_success(f"Eliminado: {path}")

    print_success("Limpieza completada")


def build_executable():
    """Compila el ejecutable con PyInstaller"""
    print_step("Compilando ejecutable con PyInstaller")

    if not os.path.exists('HidroFlowManager.spec'):
        print_error("No se encontró HidroFlowManager.spec")
        return False

    try:
        # Ejecutar PyInstaller
        cmd = ['pyinstaller', '--clean', '--noconfirm', 'HidroFlowManager.spec']
        print_info(f"Ejecutando: {' '.join(cmd)}")

        result = subprocess.run(cmd, check=True, capture_output=True, text=True)

        # Mostrar output
        if result.stdout:
            print(result.stdout)

        # Verificar que se creó el ejecutable
        exe_path = Path('dist') / 'HidroFlowManager.exe'
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print_success(f"Ejecutable creado: {exe_path} ({size_mb:.2f} MB)")
            return True
        else:
            print_error("El ejecutable no se creó correctamente")
            return False

    except subprocess.CalledProcessError as e:
        print_error(f"Error durante la compilación: {e}")
        if e.stderr:
            print(e.stderr)
        return False
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        return False


def build_installer():
    """Crea el instalador con Inno Setup"""
    print_step("Creando instalador con Inno Setup")

    # Verificar que existe el ejecutable
    exe_path = Path('dist') / 'HidroFlowManager.exe'
    if not exe_path.exists():
        print_error("No se encontró el ejecutable en dist/")
        print_info("Ejecute primero: python build.py --exe")
        return False

    # Buscar Inno Setup
    inno_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe",
    ]

    iscc_path = None
    for path in inno_paths:
        if os.path.exists(path):
            iscc_path = path
            break

    if not iscc_path:
        print_error("No se encontró Inno Setup")
        print_info("Descargar desde: https://jrsoftware.org/isdl.php")
        print_info("O especifique la ruta manualmente con --iscc-path")
        return False

    print_success(f"Inno Setup encontrado: {iscc_path}")

    # Compilar instalador
    try:
        cmd = [iscc_path, 'installer.iss']
        print_info(f"Ejecutando: {' '.join(cmd)}")

        result = subprocess.run(cmd, check=True, capture_output=True, text=True)

        if result.stdout:
            print(result.stdout)

        # Verificar que se creó el instalador
        installer_pattern = Path('dist') / 'HydroFlowManager_Setup_*.exe'
        installers = list(Path('dist').glob('HydroFlowManager_Setup_*.exe'))

        if installers:
            installer = installers[0]
            size_mb = installer.stat().st_size / (1024 * 1024)
            print_success(f"Instalador creado: {installer} ({size_mb:.2f} MB)")
            return True
        else:
            print_error("El instalador no se creó correctamente")
            return False

    except subprocess.CalledProcessError as e:
        print_error(f"Error durante la creación del instalador: {e}")
        if e.stderr:
            print(e.stderr)
        return False
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        return False


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Script de compilación para HydroFlow Manager',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--all', action='store_true',
                        help='Compila ejecutable e instalador')
    parser.add_argument('--exe', action='store_true',
                        help='Solo compila el ejecutable')
    parser.add_argument('--installer', action='store_true',
                        help='Solo crea el instalador')
    parser.add_argument('--clean', action='store_true',
                        help='Limpia archivos de compilación')
    parser.add_argument('--no-deps-check', action='store_true',
                        help='Omite verificación de dependencias')

    args = parser.parse_args()

    # Si no se especifica ninguna opción, mostrar ayuda
    if not any([args.all, args.exe, args.installer, args.clean]):
        parser.print_help()
        return

    print(f"""
{Colors.HEADER}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════╗
║                   HYDROFLOW MANAGER - BUILD                       ║
║                        Compilador v1.0                            ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
    """)

    # Limpieza
    if args.clean:
        clean_build()
        print_success("\n✓ Limpieza completada exitosamente\n")
        return

    # Verificar dependencias (excepto si se indica lo contrario)
    if not args.no_deps_check:
        if not check_dependencies():
            print_error("\n✗ Verificación de dependencias fallida\n")
            sys.exit(1)

    success = True

    # Compilar ejecutable
    if args.all or args.exe:
        clean_build()
        if not build_executable():
            success = False

    # Crear instalador
    if success and (args.all or args.installer):
        if not build_installer():
            success = False

    # Resultado final
    if success:
        print(f"""
{Colors.OKGREEN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════╗
║                  ✓ COMPILACIÓN EXITOSA                            ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
        """)

        if args.all:
            print_info("Archivos generados:")
            print(f"  • Ejecutable: dist/HidroFlowManager.exe")
            print(f"  • Instalador: dist/HydroFlowManager_Setup_*.exe")
            print()
    else:
        print(f"""
{Colors.FAIL}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════╗
║                  ✗ COMPILACIÓN FALLIDA                            ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
        """)
        sys.exit(1)


if __name__ == '__main__':
    main()
