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

def check_error(text):
    """Imprime mensaje de error"""
    print(f"  ✗ {text}")

def check_warning(text):
    """Imprime mensaje de advertencia"""
    print(f"  ⚠ {text}")

def check_python_dependencies():
    """Verifica que las dependencias Python estén instaladas"""
    print_header("Dependencias Python")

    dependencias = {
        'docx': 'python-docx',
        'reportlab': 'reportlab',
    }

    # Solo en Windows verificar pywin32
    if platform.system() == 'Windows':
        dependencias['win32com'] = 'pywin32'

    todas_instaladas = True

    for modulo, nombre_paquete in dependencias.items():
        try:
            if modulo == 'docx':
                import docx
                version = docx.__version__ if hasattr(docx, '__version__') else 'desconocida'
            elif modulo == 'reportlab':
                import reportlab
                version = reportlab.Version
            elif modulo == 'win32com':
                import win32com.client
                version = 'instalado'

            check_ok(f"{nombre_paquete}: Instalado (versión {version})")
        except ImportError:
            check_error(f"{nombre_paquete}: NO INSTALADO")
            todas_instaladas = False

    if not todas_instaladas:
        print("\n  Para instalar las dependencias faltantes:")
        print("  pip install -r requirements.txt")

    return todas_instaladas

def check_word_software():
    """Verifica que esté instalado software de conversión Word→PDF"""
    print_header("Software de Conversión PDF")

    software_encontrado = False

    # Verificar Microsoft Word (Windows)
    if platform.system() == 'Windows':
        try:
            import win32com.client
            word = win32com.client.Dispatch("Word.Application")
            version = word.Version
            word.Quit()
            check_ok(f"Microsoft Word: Detectado (versión {version})")
            software_encontrado = True
        except:
            check_warning("Microsoft Word: No detectado")

    # Verificar LibreOffice (multiplataforma)
    libreoffice_paths = [
        r"C:\Program Files\LibreOffice\program\soffice.exe",  # Windows
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",  # Windows 32-bit
        "/usr/bin/soffice",  # Linux
        "/usr/bin/libreoffice",  # Linux alternativo
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",  # macOS
    ]

    for path in libreoffice_paths:
        if os.path.exists(path):
            check_ok(f"LibreOffice: Detectado ({path})")
            software_encontrado = True
            break

    if not software_encontrado and platform.system() != 'Windows':
        check_warning("LibreOffice: No detectado")

    if not software_encontrado:
        print("\n  RECOMENDACIÓN:")
        print("  Instalar LibreOffice (alternativa gratuita):")
        print("  https://www.libreoffice.org/download/download/")

    return software_encontrado

def check_plantillas():
    """Verifica que existan las plantillas necesarias"""
    print_header("Plantillas")

    # Directorio de plantillas
    base_dir = os.path.dirname(os.path.abspath(__file__))
    plantillas_dir = os.path.join(base_dir, "resources", "plantillas")

    if not os.path.exists(plantillas_dir):
        check_error(f"Directorio de plantillas no encontrado: {plantillas_dir}")
        return False

    # Plantillas necesarias
    plantillas_necesarias = [
        "Plantilla Listado Partes.docx",  # Legacy
        "Plantilla_Partes.docx",
        "Plantilla_Recursos.docx",
        "Plantilla_Presupuesto.docx",
        "Plantilla_Certificacion.docx",
        "Plantilla_Planificacion.docx",
        "Plantilla_Generica.docx",
    ]

    todas_encontradas = True
    for plantilla in plantillas_necesarias:
        ruta = os.path.join(plantillas_dir, plantilla)
        if os.path.exists(ruta):
            check_ok(f"{plantilla}: Encontrada")
        else:
            check_warning(f"{plantilla}: NO ENCONTRADA (opcional)")
            todas_encontradas = False

    return todas_encontradas

def check_logos():
    """Verifica que existan los logos corporativos"""
    print_header("Logos Corporativos")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    logos_dir = os.path.join(base_dir, "resources", "images")

    if not os.path.exists(logos_dir):
        check_warning(f"Directorio de imágenes no encontrado: {logos_dir}")
        return False

    logos = [
        "logo.png",
        "logo.ico",
        "logo.jpeg",
        "logo.jpg",
    ]

    alguno_encontrado = False
    for logo in logos:
        ruta = os.path.join(logos_dir, logo)
        if os.path.exists(ruta):
            check_ok(f"{logo}: Encontrado")
            alguno_encontrado = True

    if not alguno_encontrado:
        check_warning("No se encontraron logos corporativos (opcional)")

    return alguno_encontrado

def main():
    """Función principal"""
    print_header("Verificación de Dependencias para Generación de PDFs")
    print(f"  Sistema operativo: {platform.system()} {platform.release()}")
    print(f"  Python: {sys.version.split()[0]}")

    # Verificar cada componente
    python_ok = check_python_dependencies()
    software_ok = check_word_software()
    plantillas_ok = check_plantillas()
    logos_ok = check_logos()

    # Resumen
    print_header("RESUMEN")

    if not python_ok:
        check_error("Faltan dependencias críticas")
        print("  Ejecutar: pip install -r requirements.txt")

    if not software_ok:
        check_warning("No se detectó software de conversión PDF")
        print("  Sin Microsoft Word o LibreOffice, solo se podrán generar archivos .docx")
        print("  Instalar LibreOffice: https://www.libreoffice.org/download/download/")

    if not plantillas_ok:
        check_warning("Faltan algunas plantillas")
        print("  Las plantillas faltantes se pueden crear copiando una existente")

    if python_ok and (software_ok or plantillas_ok):
        check_ok("Sistema listo para generar informes")
        if software_ok:
            check_ok("Puede generar archivos Word y PDF")
        else:
            check_warning("Solo puede generar archivos Word (no PDF)")

    print("=" * 70)
    print("\nPara más información, consultar: docs/GENERACION_PDF.md")
    print("=" * 70)

if __name__ == "__main__":
    main()
