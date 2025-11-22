#!/usr/bin/env python3
"""
Script para convertir los manuales Markdown a PDF
usando markdown y weasyprint
"""

import os
import sys
from pathlib import Path
import markdown
from weasyprint import HTML, CSS

# Configuración
MANUALS = [
    {
        'input': 'docs/Manual_Usuario_HydroFlow.md',
        'output': 'docs/Manual_Usuario_HydroFlow.pdf',
        'title': 'Manual de Usuario - HydroFlow Manager v2.0'
    },
    {
        'input': 'docs/Manual_Informes_HydroFlow.md',
        'output': 'docs/Manual_Informes_HydroFlow.pdf',
        'title': 'Manual de Informes - HydroFlow Manager v2.0'
    },
    {
        'input': 'docs/Guia_Tecnica_HydroFlow.md',
        'output': 'docs/Guia_Tecnica_HydroFlow.pdf',
        'title': 'Guía Técnica - HydroFlow Manager v2.0'
    }
]

# CSS para mejorar la presentación del PDF
PDF_CSS = """
@page {
    margin: 2cm;
    @top-center {
        content: string(doctitle);
        font-size: 9pt;
        color: #666;
    }
    @bottom-center {
        content: counter(page);
        font-size: 9pt;
        color: #666;
    }
}

body {
    font-family: "DejaVu Sans", Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #333;
    max-width: 100%;
}

h1 {
    color: #1a5490;
    font-size: 24pt;
    margin-top: 30px;
    margin-bottom: 20px;
    border-bottom: 3px solid #1a5490;
    padding-bottom: 10px;
    page-break-before: always;
}

h1:first-of-type {
    page-break-before: avoid;
}

h2 {
    color: #2a6ab0;
    font-size: 18pt;
    margin-top: 25px;
    margin-bottom: 15px;
    border-bottom: 2px solid #2a6ab0;
    padding-bottom: 8px;
}

h3 {
    color: #3a7ac0;
    font-size: 14pt;
    margin-top: 20px;
    margin-bottom: 10px;
}

h4 {
    color: #4a8ad0;
    font-size: 12pt;
    margin-top: 15px;
    margin-bottom: 8px;
}

code {
    background-color: #f4f4f4;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: "DejaVu Sans Mono", "Courier New", monospace;
    font-size: 10pt;
}

pre {
    background-color: #f8f8f8;
    border: 1px solid #ddd;
    border-left: 4px solid #1a5490;
    padding: 15px;
    overflow-x: auto;
    border-radius: 5px;
    page-break-inside: avoid;
}

pre code {
    background-color: transparent;
    padding: 0;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
    page-break-inside: avoid;
}

th {
    background-color: #1a5490;
    color: white;
    padding: 12px;
    text-align: left;
    font-weight: bold;
}

td {
    border: 1px solid #ddd;
    padding: 10px;
}

tr:nth-child(even) {
    background-color: #f9f9f9;
}

blockquote {
    border-left: 4px solid #1a5490;
    padding-left: 20px;
    margin-left: 0;
    color: #555;
    font-style: italic;
}

ul, ol {
    margin: 15px 0;
    padding-left: 30px;
}

li {
    margin: 8px 0;
}

a {
    color: #1a5490;
    text-decoration: none;
}

img {
    max-width: 100%;
    height: auto;
}

hr {
    border: none;
    border-top: 2px solid #ddd;
    margin: 30px 0;
}

.page-break {
    page-break-after: always;
}
"""

def convert_markdown_to_pdf(input_file, output_file, title):
    """Convierte un archivo Markdown a PDF"""

    print(f"\n{'='*70}")
    print(f"Convirtiendo: {input_file}")
    print(f"Destino: {output_file}")
    print(f"{'='*70}")

    # Leer el archivo Markdown
    if not os.path.exists(input_file):
        print(f"❌ ERROR: No se encontró el archivo {input_file}")
        return False

    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convertir Markdown a HTML
    md = markdown.Markdown(extensions=[
        'extra',
        'codehilite',
        'tables',
        'fenced_code',
        'toc'
    ])
    html_content = md.convert(md_content)

    # Crear HTML completo con metadatos
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # Convertir HTML a PDF
    try:
        HTML(string=full_html).write_pdf(
            output_file,
            stylesheets=[CSS(string=PDF_CSS)]
        )

        # Verificar que se creó el PDF
        if os.path.exists(output_file):
            size_mb = os.path.getsize(output_file) / (1024 * 1024)
            print(f"✅ PDF creado exitosamente ({size_mb:.2f} MB)")
            return True
        else:
            print(f"❌ ERROR: El PDF no se creó correctamente")
            return False

    except Exception as e:
        print(f"❌ ERROR al generar PDF: {e}")
        return False

def main():
    """Función principal"""
    print("\n" + "="*70)
    print("CONVERSIÓN DE MANUALES MARKDOWN A PDF")
    print("HydroFlow Manager v2.0")
    print("="*70)

    success_count = 0
    failed_count = 0

    for manual in MANUALS:
        if convert_markdown_to_pdf(
            manual['input'],
            manual['output'],
            manual['title']
        ):
            success_count += 1
        else:
            failed_count += 1

    # Resumen final
    print("\n" + "="*70)
    print("RESUMEN DE CONVERSIÓN")
    print("="*70)
    print(f"✅ Exitosos: {success_count}")
    print(f"❌ Fallidos: {failed_count}")
    print("="*70)

    if failed_count == 0:
        print("\n✅ ¡Todos los manuales se convirtieron correctamente!")
        print("\nArchivos PDF generados:")
        for manual in MANUALS:
            if os.path.exists(manual['output']):
                size_mb = os.path.getsize(manual['output']) / (1024 * 1024)
                print(f"  • {manual['output']} ({size_mb:.2f} MB)")
        return 0
    else:
        print("\n❌ Algunos manuales no se pudieron convertir.")
        print("Revise los errores arriba.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
