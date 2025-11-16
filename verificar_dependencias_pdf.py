#!/usr/bin/env python3
"""
Script de verificación de dependencias para generación de PDFs
HydroFlow Manager v1.04

Ejecutar: python verificar_dependencias_pdf.py
"""

import sys
import os
import platform

def print_header(text):
    """Imprime un encabezado formateado"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def check_ok(text):
    """Imprime mensaje de éxito"""
    print(f"  ✓ {text}")

def check_warning(text):
    """Imprime mensaje de advertencia"""
    print(f"  ⚠ {text}")

def check_error(text):
    """Imprime mensaje de error"""
    print(f"  ✗ {text}")

def check_python_dependencies():
    """Verifica dependencias Python"""
    print_header("1. Dependencias Python")

    dependencies = [
        ("python-docx", "docx"),
        ("pillow", "PIL"),
        ("reportlab", "reportlab"),
        ("xlsxwriter", "xlsxwriter"),
        ("openpyxl", "openpyxl"),
    ]

    all_ok = True
    for name, module in dependencies:
        try:
            __import__(module)
            check_ok(f"{name} instalado")
        except ImportError:
            check_error(f"{name} NO instalado")
            all_ok = False

    return all_ok

def check_windows_dependencies():
    """Verifica dependencias específicas de Windows"""
    print_header("2. Dependencias Windows (solo para Windows)")

    if platform.system() != 'Windows':
        check_warning("No estás en Windows, pywin32 no es necesario")
        return True

    try:
        import win32com.client
        import pythoncom
        check_ok("pywin32 instalado correctamente")

        # Intentar conectar con Microsoft Word
        try:
            pythoncom.CoInitialize()
            word = win32com.client.Dispatch('Word.Application')
            word.Visible = False
            version = word.Version
            check_ok(f"Microsoft Word {version} detectado y funcional")
            word.Quit()
            pythoncom.CoUninitialize()
            return True
        except Exception as e:
            check_warning(f"pywin32 instalado pero Word no disponible: {e}")
            check_warning("Se usará LibreOffice como alternativa si está instalado")
            return False

    except ImportError:
        check_error("pywin32 NO instalado")
        print("         Instalar con: pip install pywin32")
        return False

def check_libreoffice():
    """Verifica si LibreOffice está instalado"""
    print_header("3. LibreOffice (alternativa de conversión)")

    # Rutas comunes de LibreOffice
    if platform.system() == 'Windows':
        paths = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        ]
    else:
        paths = [
            "/usr/bin/libreoffice",
            "/usr/local/bin/libreoffice",
            "/snap/bin/libreoffice",
        ]

    for path in paths:
        if os.path.exists(path):
            check_ok(f"LibreOffice encontrado en: {path}")
            return True

    check_warning("LibreOffice NO encontrado")
    print("         Descargar desde: https://www.libreoffice.org/download/")
    return False

def check_templates():
    """Verifica que existan las plantillas"""
    print_header("4. Plantillas Word")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    plantillas_dir = os.path.join(base_dir, "plantillas")

    if not os.path.exists(plantillas_dir):
        check_error(f"Carpeta 'plantillas' no encontrada en {base_dir}")
        return False

    plantillas_encontradas = []
    for file in os.listdir(plantillas_dir):
        if file.endswith('.docx'):
            plantillas_encontradas.append(file)
            check_ok(f"Plantilla encontrada: {file}")

    if not plantillas_encontradas:
        check_warning("No se encontraron plantillas .docx en la carpeta plantillas/")
        return False

    return True

def check_logos():
    """Verifica que existan los logos"""
    print_header("5. Logos Corporativos")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(base_dir, "resources", "images")

    if not os.path.exists(images_dir):
        check_error(f"Carpeta 'resources/images' no encontrada")
        return False

    logos = [
        "Logo Redes Urbide.jpg",
        "Logo Urbide.jpg",
    ]

    all_ok = True
    for logo in logos:
        logo_path = os.path.join(images_dir, logo)
        if os.path.exists(logo_path):
            check_ok(f"Logo encontrado: {logo}")
        else:
            check_warning(f"Logo NO encontrado: {logo}")
            all_ok = False

    return all_ok

def main():
    """Función principal"""
    print("\n" + "=" * 70)
    print("  VERIFICACIÓN DE DEPENDENCIAS - GENERACIÓN DE PDFs")
    print("  HydroFlow Manager v1.04")
    print("=" * 70)
    print(f"\nSistema operativo: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")

    # Ejecutar verificaciones
    results = {
        "Python Dependencies": check_python_dependencies(),
        "Windows Dependencies": check_windows_dependencies(),
        "LibreOffice": check_libreoffice(),
        "Templates": check_templates(),
        "Logos": check_logos(),
    }

    # Resumen final
    print_header("RESUMEN")

    all_passed = all(results.values())
    conversion_ok = results["Windows Dependencies"] or results["LibreOffice"]

    if all_passed and conversion_ok:
        check_ok("TODAS las dependencias están instaladas correctamente")
        check_ok("El sistema puede generar PDFs sin problemas")
    elif results["Python Dependencies"] and conversion_ok:
        check_warning("Dependencias Python OK, conversión a PDF disponible")
        check_warning("Algunas dependencias opcionales faltan (ver arriba)")
    elif results["Python Dependencies"]:
        check_warning("Dependencias Python OK")
        check_error("NO hay software de conversión Word→PDF instalado")
        print("\n  Se pueden generar documentos Word (.docx)")
        print("  pero NO se pueden convertir automáticamente a PDF")
        print("\n  Soluciones:")
        print("    1. Instalar Microsoft Office (Windows)")
        print("    2. Instalar LibreOffice (gratis): https://www.libreoffice.org/")
    else:
        check_error("Faltan dependencias críticas")
        print("\n  Ejecutar: pip install -r requirements.txt")

    print("\n" + "=" * 70)
    print("\nPara más información, consultar: docs/GENERACION_PDF.md")
    print("=" * 70 + "\n")

    return 0 if (results["Python Dependencies"] and conversion_ok) else 1

if __name__ == "__main__":
    sys.exit(main())
