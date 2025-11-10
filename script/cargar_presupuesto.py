#!/usr/bin/env python3
"""
Script para cargar presupuesto desde archivo Excel
HydroFlow Manager v1.04 - FASE 1: PREPARACIÓN DE DATOS
"""
import sys
from pathlib import Path

# Añadir directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from script.budget_import import budget_import


def main():
    """Carga un presupuesto desde archivo Excel a la base de datos."""

    # Configuración
    USER = 'root'
    PASSWORD = 'root'
    SCHEMA = 'proyecto_tipo'

    if len(sys.argv) < 2:
        print("=" * 70)
        print("CARGAR PRESUPUESTO DESDE EXCEL")
        print("=" * 70)
        print()
        print("Uso:")
        print(f"  {sys.argv[0]} <archivo_excel>")
        print()
        print("El archivo Excel debe contener las siguientes hojas:")
        print("  - tbl_pres_capitulos")
        print("  - tbl_pres_precios")
        print("  - tbl_pres_naturaleza")
        print("  - tbl_pres_unidades")
        print()
        print("Ejemplo:")
        print(f"  {sys.argv[0]} presupuesto_proyecto.xlsx")
        sys.exit(1)

    archivo_excel = sys.argv[1]
    archivo_path = Path(archivo_excel)

    if not archivo_path.exists():
        print(f"ERROR: El archivo '{archivo_excel}' no existe")
        sys.exit(1)

    print("=" * 70)
    print("CARGAR PRESUPUESTO DESDE EXCEL")
    print("=" * 70)
    print(f"Archivo: {archivo_path.name}")
    print(f"Esquema: {SCHEMA}")
    print()

    try:
        print("Importando presupuesto...")
        resultado = budget_import(USER, PASSWORD, SCHEMA, str(archivo_path))

        if resultado == "ok":
            print()
            print("=" * 70)
            print("✓ PRESUPUESTO CARGADO EXITOSAMENTE")
            print("=" * 70)
            print()
            print("Próximo paso:")
            print("  - Crear backup: python script/crear_backup.py backup_con_presupuesto proyecto_tipo")
            print()
            sys.exit(0)
        else:
            print()
            print("=" * 70)
            print("✗ ERROR AL CARGAR PRESUPUESTO")
            print("=" * 70)
            print(f"Error: {resultado}")
            print()
            sys.exit(1)

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
