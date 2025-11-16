#!/usr/bin/env python3
"""
Script de diagnóstico y reparación de configuraciones de informes
HydroFlow Manager v1.04

Ejecutar: python reparar_configuraciones.py
"""

import os
import json
import sys
from datetime import datetime

def print_header(text):
    """Imprime un encabezado formateado"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_ok(text):
    """Imprime mensaje de éxito"""
    print(f"  ✓ {text}")

def print_warning(text):
    """Imprime mensaje de advertencia"""
    print(f"  ⚠ {text}")

def print_error(text):
    """Imprime mensaje de error"""
    print(f"  ✗ {text}")

def diagnosticar_configuraciones():
    """Diagnostica configuraciones guardadas"""
    print_header("Diagnóstico de Configuraciones de Informes")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(base_dir, "informes_guardados")

    if not os.path.exists(config_dir):
        print_error(f"Directorio no encontrado: {config_dir}")
        return

    print(f"\nDirectorio: {config_dir}")

    archivos_json = [f for f in os.listdir(config_dir) if f.endswith('.json')]

    if not archivos_json:
        print_warning("No se encontraron archivos de configuración (.json)")
        return

    print(f"\nEncontrados {len(archivos_json)} archivos .json\n")

    archivos_ok = []
    archivos_corruptos = []

    for filename in archivos_json:
        filepath = os.path.join(config_dir, filename)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # Validar estructura
            if not isinstance(config, dict):
                raise ValueError("No es un diccionario")

            # Validar campos mínimos
            nombre = config.get('nombre', filename[:-5])
            informe_base = config.get('informe_base', '')

            print_ok(f"{filename}")
            print(f"     Nombre: {nombre}")
            print(f"     Informe base: {informe_base}")

            archivos_ok.append(filename)

        except json.JSONDecodeError as e:
            print_error(f"{filename}")
            print(f"     Error JSON: {e}")
            archivos_corruptos.append((filename, f"JSON inválido: {e}"))

        except Exception as e:
            print_error(f"{filename}")
            print(f"     Error: {e}")
            archivos_corruptos.append((filename, str(e)))

    # Resumen
    print_header("Resumen del Diagnóstico")

    print(f"\n  Archivos OK: {len(archivos_ok)}")
    print(f"  Archivos corruptos: {len(archivos_corruptos)}")

    if archivos_corruptos:
        print("\n  Archivos con problemas:")
        for filename, error in archivos_corruptos:
            print(f"    - {filename}: {error}")

        print("\n  ¿Desea eliminar los archivos corruptos? (s/n): ", end='')
        respuesta = input().strip().lower()

        if respuesta == 's':
            for filename, _ in archivos_corruptos:
                filepath = os.path.join(config_dir, filename)
                try:
                    os.remove(filepath)
                    print_ok(f"Eliminado: {filename}")
                except Exception as e:
                    print_error(f"No se pudo eliminar {filename}: {e}")

    print("\n" + "=" * 70)

def main():
    """Función principal"""
    diagnosticar_configuraciones()

if __name__ == "__main__":
    main()
