# script/informes_exportacion.py
"""
Módulo de exportación de informes a Excel, Word y PDF
Genera documentos profesionales con agrupaciones, subtotales y formato corporativo
"""

import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import xlsxwriter
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


class InformesExportador:
    """Exportador de informes a múltiples formatos"""

    def __init__(self, schema: str):
        self.schema = schema
        self.logo_redes_path = None
        self.logo_urbide_path = None
        self._buscar_logos()

    def _buscar_logos(self):
        """Busca los logos en la raíz del proyecto y en la carpeta resources/images"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Directorios donde buscar (en orden de prioridad)
        directorios_busqueda = [
            os.path.join(base_dir, "resources", "images"),  # Carpeta resources/images (prioridad 1)
            base_dir,  # Raíz del proyecto (prioridad 2)
        ]

        for directorio in directorios_busqueda:
            if not os.path.exists(directorio):
                continue

            archivos = os.listdir(directorio)

            # Buscar logos con prioridad exacta
            for file in archivos:
                file_lower = file.lower()
                if not file_lower.endswith(('.png', '.jpg', '.jpeg')):
                    continue

                # Logo izquierdo (Logo Redes Urbide) - prioridad exacta
                if not self.logo_redes_path:
                    if file_lower in ["logo redes urbide.jpg", "logo redes urbide.png"]:
                        self.logo_redes_path = os.path.join(directorio, file)
                        print(f"✓ Logo izquierdo (Redes Urbide) encontrado: {file}")

                # Logo derecho (Logo Urbide) - prioridad exacta
                if not self.logo_urbide_path:
                    if file_lower in ["logo urbide.jpg", "logo urbide.png"]:
                        self.logo_urbide_path = os.path.join(directorio, file)
                        print(f"✓ Logo derecho (Urbide) encontrado: {file}")

            # Si ya encontramos ambos logos, salir
            if self.logo_redes_path and self.logo_urbide_path:
                break

        # Si aún no se encuentran, buscar alternativas en todos los directorios
        if not self.logo_redes_path or not self.logo_urbide_path:
            for directorio in directorios_busqueda:
                if not os.path.exists(directorio):
                    continue

                archivos = os.listdir(directorio)

                for file in archivos:
                    file_lower = file.lower()
                    if not file_lower.endswith(('.png', '.jpg', '.jpeg')):
                        continue

                    # Intentar con patrones flexibles como fallback
                    if not self.logo_redes_path and ("redes" in file_lower or file_lower == "logo.png"):
                        self.logo_redes_path = os.path.join(directorio, file)
                        print(f"⚠ Usando logo alternativo (izquierdo): {file}")

                    if not self.logo_urbide_path and "urbide" in file_lower and "redes" not in file_lower:
                        self.logo_urbide_path = os.path.join(directorio, file)
                        print(f"⚠ Usando logo alternativo (derecho): {file}")

    def exportar_a_excel(
        self,
        filepath: str,
        informe_nombre: str,
        columnas: List[str],
        datos: List[tuple],
        resultado_agrupacion: Optional[Dict] = None,
        proyecto_nombre: str = "",
        proyecto_codigo: str = ""
    ) -> bool:
        """
        Exporta el informe a Excel con formato profesional

        Args:
            filepath: Ruta del archivo Excel a crear
            informe_nombre: Nombre del informe
            columnas: Lista de nombres de columnas
            datos: Datos del informe
            resultado_agrupacion: Estructura de agrupaciones y totales (opcional)
            proyecto_nombre: Nombre del proyecto
            proyecto_codigo: Código del proyecto

        Returns:
            True si la exportación fue exitosa
        """
        try:
            workbook = xlsxwriter.Workbook(filepath)
            worksheet = workbook.add_worksheet(informe_nombre[:31])  # Excel limit 31 chars

            # Función helper para detectar y convertir fechas
            def detectar_y_convertir_fecha(valor_str):
                """Detecta formatos comunes de fecha y los convierte a datetime"""
                import re
                if not isinstance(valor_str, str):
                    return None

                # Detectar formatos comunes: DD/MM/YYYY, YYYY-MM-DD, DD-MM-YYYY
                patrones_fecha = [
                    (r'^\d{2}/\d{2}/\d{4}$', '%d/%m/%Y'),  # DD/MM/YYYY
                    (r'^\d{4}-\d{2}-\d{2}$', '%Y-%m-%d'),  # YYYY-MM-DD
                    (r'^\d{2}-\d{2}-\d{4}$', '%d-%m-%Y'),  # DD-MM-YYYY
                ]

                for patron, formato in patrones_fecha:
                    if re.match(patron, valor_str.strip()):
                        try:
                            from datetime import datetime as dt
                            return dt.strptime(valor_str.strip(), formato)
                        except ValueError:
                            continue
                return None

            # Definir formatos
            formato_titulo = workbook.add_format({
                'bold': True,
                'font_size': 20,
                'font_name': 'Calibri',
                'align': 'center',  # Centrado horizontal
                'valign': 'vcenter'  # Centrado vertical
            })

            formato_subtitulo = workbook.add_format({
                'font_size': 10,
                'font_name': 'Tahoma',
                'italic': True,
                'font_color': '#7C7C7C',
                'align': 'left'
            })

            formato_header_nivel0 = workbook.add_format({
                'bold': True,
                'font_size': 10,
                'font_name': 'Tahoma',
                'bg_color': '#4A6FA5',
                'font_color': 'white',
                'border': 1,
                'align': 'left',
                'valign': 'vcenter'
            })

            formato_header_nivel1 = workbook.add_format({
                'bold': True,
                'font_size': 9,
                'font_name': 'Tahoma',
                'bg_color': '#6B8FB8',
                'font_color': 'white',
                'border': 1,
                'align': 'left'
            })

            formato_header_nivel2 = workbook.add_format({
                'bold': True,
                'font_size': 9,
                'font_name': 'Tahoma',
                'bg_color': '#8AADC7',
                'font_color': 'white',
                'border': 1,
                'align': 'left'
            })

            formato_header_columnas = workbook.add_format({
                'bold': True,
                'font_size': 10,
                'font_name': 'Tahoma',
                'bg_color': '#D9D9D9',
                'border': 1,
                'align': 'center',
                'valign': 'vcenter'
            })

            formato_datos = workbook.add_format({
                'font_size': 8,
                'font_name': 'Tahoma',
                'border': 1
            })

            formato_moneda = workbook.add_format({
                'font_size': 8,
                'font_name': 'Tahoma',
                'num_format': '#,##0.00 €',
                'border': 1,
                'align': 'right',  # Alineación a la derecha
                'valign': 'vcenter'
            })

            formato_decimal = workbook.add_format({
                'font_size': 8,
                'font_name': 'Tahoma',
                'num_format': '#,##0.00',
                'border': 1,
                'align': 'right',  # Alineación a la derecha
                'valign': 'vcenter'
            })

            formato_subtotal = workbook.add_format({
                'bold': True,
                'font_size': 9,
                'font_name': 'Tahoma',
                'bg_color': '#E7E6E6',
                'num_format': '#,##0.00 €',
                'border': 1,
                'align': 'right',  # Alineación a la derecha
                'valign': 'vcenter'
            })

            formato_subtotal_texto = workbook.add_format({
                'bold': True,
                'font_size': 9,
                'font_name': 'Tahoma',
                'bg_color': '#E7E6E6',
                'border': 1,
                'align': 'left',  # Texto alineado a la izquierda
                'valign': 'vcenter'
            })

            formato_total = workbook.add_format({
                'bold': True,
                'font_size': 10,
                'font_name': 'Tahoma',
                'bg_color': '#C5D9F1',
                'num_format': '#,##0.00 €',
                'border': 2,
                'align': 'right',  # Alineación a la derecha
                'valign': 'vcenter'
            })

            formato_total_texto = workbook.add_format({
                'bold': True,
                'font_size': 10,
                'font_name': 'Tahoma',
                'bg_color': '#C5D9F1',
                'border': 2,
                'align': 'left',  # Texto alineado a la izquierda
                'valign': 'vcenter'
            })

            formato_fecha = workbook.add_format({
                'font_size': 10,
                'font_name': 'Calibri',
                'bold': True
            })

            # Formato para celdas de fecha (dd/mm/yyyy)
            formato_fecha_celda = workbook.add_format({
                'font_size': 8,
                'font_name': 'Tahoma',
                'border': 1,
                'num_format': 'dd/mm/yyyy',
                'align': 'left',
                'valign': 'vcenter'
            })

            # Fila actual
            row = 0

            # Configurar altura de la fila de encabezado para acomodar logos y título
            # 2.1 cm ≈ 59.5 puntos
            worksheet.set_row(row, 59.5)

            # Configurar ancho de primera y última columna para los logos
            worksheet.set_column(0, 0, 15)
            worksheet.set_column(len(columnas) - 1, len(columnas) - 1, 15)

            # Logo izquierdo (Logo Redes Urbide) - altura 2.1cm, alineado a la izquierda
            if self.logo_redes_path and os.path.exists(self.logo_redes_path):
                worksheet.insert_image(row, 0, self.logo_redes_path, {
                    'x_scale': 1.0,  # Escala 100%
                    'y_scale': 1.0,  # Escala 100%
                    'x_offset': 2,
                    'y_offset': 2,
                    'object_position': 1  # Mover con celda y redimensionar
                })

            # Título del informe - combinar todas las celdas excepto primera y última
            num_cols = len(columnas)
            # Merge desde columna 1 (segunda) hasta columna num_cols-2 (penúltima)
            if num_cols > 2:
                worksheet.merge_range(row, 1, row, num_cols - 2, informe_nombre.upper(), formato_titulo)
            else:
                worksheet.write(row, 1, informe_nombre.upper(), formato_titulo)

            # Logo derecho (Logo Urbide) - altura 2.1cm, alineado a la derecha
            if self.logo_urbide_path and os.path.exists(self.logo_urbide_path):
                # Para alinear a la derecha, calculamos el offset basado en el ancho de la columna
                # Ancho columna 15 ≈ 105 píxeles. Necesitamos offset para alinear a la derecha
                worksheet.insert_image(row, len(columnas) - 1, self.logo_urbide_path, {
                    'x_scale': 1.0,  # Escala 100%
                    'y_scale': 1.0,  # Escala 100%
                    'x_offset': 50,  # Offset para alinear a la derecha
                    'y_offset': 2,
                    'object_position': 1  # Mover con celda y redimensionar
                })

            row += 2  # Espacio después del encabezado

            # Información del proyecto
            if proyecto_nombre:
                worksheet.merge_range(row, 0, row, len(columnas) - 1, proyecto_nombre, formato_subtitulo)
                row += 1

            # Fecha
            fecha_actual = datetime.now().strftime("%d/%m/%Y")
            worksheet.write(row, 0, f"FECHA: {fecha_actual}", formato_fecha)
            row += 2

            # Si hay agrupaciones, exportar con estructura jerárquica
            if resultado_agrupacion and resultado_agrupacion.get('grupos'):
                row = self._exportar_grupos_excel(
                    worksheet,
                    workbook,
                    resultado_agrupacion['grupos'],
                    columnas,
                    row,
                    formato_header_nivel0,
                    formato_header_nivel1,
                    formato_header_nivel2,
                    formato_header_columnas,
                    formato_datos,
                    formato_moneda,
                    formato_decimal,
                    formato_subtotal,
                    formato_subtotal_texto,
                    formato_fecha_celda,
                    resultado_agrupacion.get('modo', 'detalle'),
                    resultado_agrupacion
                )

                # Totales generales - ALINEADOS CON LAS COLUMNAS CORRECTAS
                if resultado_agrupacion.get('totales_generales'):
                    row += 1
                    worksheet.write(row, 0, "═══ TOTAL GENERAL ═══", formato_total_texto)

                    # Obtener mapa de formatos de agregaciones
                    formatos_agregaciones = resultado_agrupacion.get('formatos_agregaciones', {})

                    # Crear formato para total sin moneda (para COUNT, etc.)
                    formato_total_entero = workbook.add_format({
                        'bold': True,
                        'font_size': 10,
                        'font_name': 'Tahoma',
                        'bg_color': '#C5D9F1',
                        'num_format': '#,##0',
                        'border': 2,
                        'align': 'right',
                        'valign': 'vcenter'
                    })

                    totales = resultado_agrupacion['totales_generales']
                    for key, valor in totales.items():
                        # Extraer el nombre del campo del key
                        campo_nombre = key.split('(')[1].rstrip(')')

                        # Determinar el formato según el tipo de agregación
                        formato_agg = formatos_agregaciones.get(key, 'ninguno')
                        formato_a_usar = formato_total if formato_agg == 'moneda' else formato_total_entero

                        # Buscar la columna correspondiente
                        if campo_nombre in columnas:
                            col_idx = columnas.index(campo_nombre)
                            worksheet.write(row, col_idx, valor, formato_a_usar)
                        elif campo_nombre == '*':
                            # COUNT(*) se escribe en la segunda columna, siempre como entero
                            worksheet.write(row, 1, valor, formato_total_entero)

            else:
                # Exportar sin agrupaciones (tabla simple)
                # Encabezados de columnas
                for col_idx, col_name in enumerate(columnas):
                    worksheet.write(row, col_idx, col_name, formato_header_columnas)
                    worksheet.set_column(col_idx, col_idx, 15)  # Ancho por defecto
                row += 1

                # Datos
                formatos_columnas = resultado_agrupacion.get('formatos_columnas', {}) if resultado_agrupacion else {}
                for fila_datos in datos:
                    for col_idx, valor in enumerate(fila_datos):
                        # Obtener el formato del campo según su columna
                        col_name = columnas[col_idx] if col_idx < len(columnas) else None
                        formato_campo = formatos_columnas.get(col_name, 'ninguno') if col_name else 'ninguno'

                        # Detectar y manejar fechas
                        fecha_dt = detectar_y_convertir_fecha(valor)
                        if fecha_dt:
                            worksheet.write_datetime(row, col_idx, fecha_dt, formato_fecha_celda)
                        # Aplicar formato según el tipo de campo
                        elif isinstance(valor, (int, float)):
                            if formato_campo == 'moneda':
                                worksheet.write(row, col_idx, valor, formato_moneda)
                            elif formato_campo == 'decimal':
                                worksheet.write(row, col_idx, valor, formato_decimal)
                            else:
                                # Por defecto, números decimales con 2 decimales
                                worksheet.write(row, col_idx, valor, formato_decimal)
                        else:
                            worksheet.write(row, col_idx, valor, formato_datos)
                    row += 1

            # Pie de página
            row += 2
            worksheet.write(row, 0, f"Generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}", formato_subtitulo)

            workbook.close()
            return True

        except Exception as e:
            print(f"Error al exportar a Excel: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _exportar_grupos_excel(
        self,
        worksheet,
        workbook,
        grupos: List[Dict],
        columnas: List[str],
        start_row: int,
        formato_nivel0,
        formato_nivel1,
        formato_nivel2,
        formato_header_columnas,
        formato_datos,
        formato_moneda,
        formato_decimal,
        formato_subtotal,
        formato_subtotal_texto,
        formato_fecha_celda,
        modo: str = 'detalle',
        resultado_agrupacion: Optional[Dict] = None
    ) -> int:
        """Exporta grupos jerárquicos a Excel (recursivo)"""
        # Función helper para detectar y convertir fechas
        def detectar_y_convertir_fecha(valor_str):
            """Detecta formatos comunes de fecha y los convierte a datetime"""
            import re
            if not isinstance(valor_str, str):
                return None

            # Detectar formatos comunes: DD/MM/YYYY, YYYY-MM-DD, DD-MM-YYYY
            patrones_fecha = [
                (r'^\d{2}/\d{2}/\d{4}$', '%d/%m/%Y'),  # DD/MM/YYYY
                (r'^\d{4}-\d{2}-\d{2}$', '%Y-%m-%d'),  # YYYY-MM-DD
                (r'^\d{2}-\d{2}-\d{4}$', '%d-%m-%Y'),  # DD-MM-YYYY
            ]

            for patron, formato in patrones_fecha:
                if re.match(patron, valor_str.strip()):
                    try:
                        from datetime import datetime as dt
                        return dt.strptime(valor_str.strip(), formato)
                    except ValueError:
                        continue
            return None

        row = start_row

        formatos_por_nivel = [formato_nivel0, formato_nivel1, formato_nivel2]

        for grupo in grupos:
            nivel = grupo.get('nivel', 0)
            clave = grupo.get('clave', '')
            campo = grupo.get('campo', '')
            datos = grupo.get('datos', [])
            subtotales = grupo.get('subtotales', {})
            subgrupos = grupo.get('subgrupos')

            formato_grupo = formatos_por_nivel[min(nivel, 2)]

            # Encabezado del grupo
            indent = "    " * nivel
            titulo_grupo = f"{indent}📁 {campo.upper()}: {clave}"
            worksheet.merge_range(row, 0, row, len(columnas) - 1, titulo_grupo, formato_grupo)
            worksheet.set_row(row, 20 + (5 * (2 - nivel)))  # Altura según nivel
            row += 1

            # Si hay subgrupos, procesarlos recursivamente
            if subgrupos:
                row = self._exportar_grupos_excel(
                    worksheet,
                    workbook,
                    subgrupos,
                    columnas,
                    row,
                    formato_nivel0,
                    formato_nivel1,
                    formato_nivel2,
                    formato_header_columnas,
                    formato_datos,
                    formato_moneda,
                    formato_decimal,
                    formato_subtotal,
                    formato_subtotal_texto,
                    formato_fecha_celda,
                    modo,
                    resultado_agrupacion
                )
            elif modo == 'detalle':
                # Encabezados de columnas para este grupo
                for col_idx, col_name in enumerate(columnas):
                    worksheet.write(row, col_idx, col_name, formato_header_columnas)
                row += 1

                # Datos del grupo
                for fila_datos in datos:
                    for col_idx, valor in enumerate(fila_datos):
                        # Obtener el formato del campo según su columna
                        col_name = columnas[col_idx] if col_idx < len(columnas) else None
                        formato_campo = resultado_agrupacion.get('formatos_columnas', {}).get(col_name, 'ninguno') if col_name else 'ninguno'

                        # Detectar y manejar fechas
                        fecha_dt = detectar_y_convertir_fecha(valor)
                        if fecha_dt:
                            worksheet.write_datetime(row, col_idx, fecha_dt, formato_fecha_celda)
                        # Aplicar formato según el tipo de campo
                        elif isinstance(valor, (int, float)):
                            if formato_campo == 'moneda':
                                worksheet.write(row, col_idx, valor, formato_moneda)
                            elif formato_campo == 'decimal':
                                worksheet.write(row, col_idx, valor, formato_decimal)
                            else:
                                # Por defecto, números decimales con 2 decimales
                                worksheet.write(row, col_idx, valor, formato_decimal)
                        else:
                            worksheet.write(row, col_idx, str(valor) if valor is not None else "", formato_datos)
                    row += 1

            # Subtotales del grupo - ALINEADOS CON LAS COLUMNAS CORRECTAS
            if subtotales:
                indent_subtotal = "    " * (nivel + 1)

                # Escribir "Subtotal" en la primera columna (con formato de texto)
                worksheet.write(row, 0, f"{indent_subtotal}▸ Subtotal", formato_subtotal_texto)

                # Obtener mapa de formatos de agregaciones
                formatos_agregaciones = resultado_agrupacion.get('formatos_agregaciones', {}) if resultado_agrupacion else {}

                # Crear formato para subtotal sin moneda (para COUNT, etc.)
                formato_subtotal_entero = workbook.add_format({
                    'bold': True,
                    'font_size': 9,
                    'font_name': 'Tahoma',
                    'bg_color': '#E7E6E6',
                    'num_format': '#,##0',
                    'border': 1,
                    'align': 'right',
                    'valign': 'vcenter'
                })

                # Mapear subtotales a las columnas correctas
                for key, valor in subtotales.items():
                    # Extraer el nombre del campo del key (ej: "SUM(presupuesto)" -> "presupuesto")
                    # El formato es "FUNCION(campo)" o "COUNT(*)"
                    campo_nombre = key.split('(')[1].rstrip(')')

                    # Determinar el formato según el tipo de agregación
                    formato_agg = formatos_agregaciones.get(key, 'ninguno')
                    formato_a_usar = formato_subtotal if formato_agg == 'moneda' else formato_subtotal_entero

                    # Buscar la columna correspondiente
                    if campo_nombre in columnas:
                        col_idx = columnas.index(campo_nombre)
                        worksheet.write(row, col_idx, valor, formato_a_usar)
                    elif campo_nombre == '*':
                        # COUNT(*) se escribe en la segunda columna, siempre como entero
                        worksheet.write(row, 1, valor, formato_subtotal_entero)

                row += 1

            row += 1  # Espacio entre grupos

        return row

    def exportar_a_word(
        self,
        filepath: str,
        informe_nombre: str,
        columnas: List[str],
        datos: List[tuple],
        resultado_agrupacion: Optional[Dict] = None,
        proyecto_nombre: str = "",
        proyecto_codigo: str = ""
    ) -> bool:
        """
        Exporta el informe a Word con formato profesional

        Args:
            filepath: Ruta del archivo Word a crear
            informe_nombre: Nombre del informe
            columnas: Lista de nombres de columnas
            datos: Datos del informe
            resultado_agrupacion: Estructura de agrupaciones y totales (opcional)
            proyecto_nombre: Nombre del proyecto
            proyecto_codigo: Código del proyecto

        Returns:
            True si la exportación fue exitosa
        """
        try:
            doc = Document()

            # Configurar márgenes y orientación
            sections = doc.sections
            for section in sections:
                # Cambiar a orientación horizontal (landscape)
                section.orientation = 1  # 1 = landscape, 0 = portrait
                # Intercambiar ancho y alto para landscape
                section.page_width, section.page_height = section.page_height, section.page_width
                section.top_margin = Cm(2)
                section.bottom_margin = Cm(2)
                section.left_margin = Cm(2)
                section.right_margin = Cm(2)
                # Configurar encabezado desde arriba: 0.2cm
                section.header_distance = Cm(0.2)

            # Encabezado con logos
            header = sections[0].header
            header_table = header.add_table(rows=1, cols=3, width=Inches(7))
            header_table.alignment = WD_TABLE_ALIGNMENT.CENTER

            # Configurar anchos de columnas: 3.5cm, 17cm, 3.5cm
            header_table.columns[0].width = Cm(3.5)
            header_table.columns[1].width = Cm(17)
            header_table.columns[2].width = Cm(3.5)

            # Logo izquierdo (Logo Redes Urbide) - altura 2.1cm
            if self.logo_redes_path and os.path.exists(self.logo_redes_path):
                cell_logo_left = header_table.rows[0].cells[0]
                cell_logo_left.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                paragraph = cell_logo_left.paragraphs[0]
                paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
                run = paragraph.add_run()
                run.add_picture(self.logo_redes_path, height=Cm(2.1))

            # Título del informe en el centro (entre los logos) - centrado horizontal y vertical
            cell_titulo = header_table.rows[0].cells[1]
            cell_titulo.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            paragraph_titulo = cell_titulo.paragraphs[0]
            paragraph_titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run_titulo = paragraph_titulo.add_run(informe_nombre.upper())
            run_titulo.font.name = 'Calibri'
            run_titulo.font.size = Pt(20)
            run_titulo.font.bold = True
            run_titulo.font.color.rgb = RGBColor(0, 0, 0)

            # Logo derecho (Logo Urbide) - altura 1.3cm
            if self.logo_urbide_path and os.path.exists(self.logo_urbide_path):
                cell_logo_right = header_table.rows[0].cells[2]
                cell_logo_right.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                paragraph = cell_logo_right.paragraphs[0]
                paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                run = paragraph.add_run()
                run.add_picture(self.logo_urbide_path, height=Cm(1.3))

            # Información del proyecto
            if proyecto_nombre:
                p = doc.add_paragraph(proyecto_nombre)
                p.runs[0].font.name = 'Tahoma'
                p.runs[0].font.size = Pt(10)
                p.runs[0].font.italic = True
                p.runs[0].font.color.rgb = RGBColor(124, 124, 124)

            # Fecha
            fecha_actual = datetime.now().strftime("%d/%m/%Y")
            p_fecha = doc.add_paragraph()
            run_fecha = p_fecha.add_run(f"FECHA: ")
            run_fecha.font.name = 'Calibri'
            run_fecha.font.size = Pt(10)
            run_fecha.font.bold = True
            run_valor = p_fecha.add_run(fecha_actual)
            run_valor.font.name = 'Calibri'
            run_valor.font.size = Pt(10)
            run_valor.font.bold = True

            doc.add_paragraph()  # Espacio

            # Si hay agrupaciones, exportar con estructura jerárquica
            if resultado_agrupacion and resultado_agrupacion.get('grupos'):
                self._exportar_grupos_word(
                    doc,
                    resultado_agrupacion['grupos'],
                    columnas,
                    resultado_agrupacion.get('modo', 'detalle'),
                    0,
                    resultado_agrupacion
                )

                # Totales generales
                if resultado_agrupacion.get('totales_generales'):
                    doc.add_paragraph()
                    p_total = doc.add_paragraph()
                    run_total = p_total.add_run("═══ TOTAL GENERAL ═══")
                    run_total.font.name = 'Tahoma'
                    run_total.font.size = Pt(12)
                    run_total.font.bold = True

                    totales = resultado_agrupacion['totales_generales']
                    for key, valor in totales.items():
                        p = doc.add_paragraph(f"{key}: {valor:,.2f} €" if isinstance(valor, (int, float)) else f"{key}: {valor}")
                        p.runs[0].font.name = 'Tahoma'
                        p.runs[0].font.size = Pt(10)
                        p.runs[0].font.bold = True

            else:
                # Exportar sin agrupaciones (tabla simple)
                table = doc.add_table(rows=1 + len(datos), cols=len(columnas))
                table.style = 'Light Grid Accent 1'

                # Encabezados
                header_cells = table.rows[0].cells
                for idx, col_name in enumerate(columnas):
                    cell = header_cells[idx]
                    cell.text = col_name
                    # Formato de encabezado
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            run.font.bold = True
                            run.font.name = 'Tahoma'
                            run.font.size = Pt(10)
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

                    # Color de fondo
                    self._set_cell_background(cell, "D9D9D9")

                # Datos
                formatos_columnas = resultado_agrupacion.get('formatos_columnas', {}) if resultado_agrupacion else {}
                for row_idx, fila_datos in enumerate(datos, start=1):
                    row_cells = table.rows[row_idx].cells
                    for col_idx, valor in enumerate(fila_datos):
                        cell = row_cells[col_idx]

                        # Obtener el formato del campo según su columna
                        col_name = columnas[col_idx] if col_idx < len(columnas) else None
                        formato_campo = formatos_columnas.get(col_name, 'ninguno') if col_name else 'ninguno'

                        # Aplicar formato según el tipo de campo
                        if isinstance(valor, (int, float)):
                            if formato_campo == 'moneda':
                                cell.text = f"{valor:,.2f} €"
                            else:
                                # Por defecto, números con 2 decimales
                                cell.text = f"{valor:,.2f}"
                        else:
                            cell.text = str(valor) if valor is not None else ""

                        # Formato de datos
                        for paragraph in cell.paragraphs:
                            for run in paragraph.runs:
                                run.font.name = 'Tahoma'
                                run.font.size = Pt(8)

            # Pie de página con paginación
            footer = sections[0].footer
            p_footer = footer.paragraphs[0]
            p_footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p_footer.add_run()
            run.font.name = 'Tahoma'
            run.font.size = Pt(8)

            # Añadir número de página
            self._add_page_number(p_footer.add_run())

            doc.save(filepath)
            return True

        except Exception as e:
            print(f"Error al exportar a Word: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _exportar_grupos_word(
        self,
        doc: Document,
        grupos: List[Dict],
        columnas: List[str],
        modo: str = 'detalle',
        nivel: int = 0,
        resultado_agrupacion: Optional[Dict] = None
    ):
        """Exporta grupos jerárquicos a Word (recursivo)"""
        for grupo in grupos:
            clave = grupo.get('clave', '')
            campo = grupo.get('campo', '')
            datos = grupo.get('datos', [])
            subtotales = grupo.get('subtotales', {})
            subgrupos = grupo.get('subgrupos')
            nivel_grupo = grupo.get('nivel', nivel)

            # Encabezado del grupo
            indent = "    " * nivel_grupo
            titulo_grupo = f"{indent}📁 {campo.upper()}: {clave}"

            p_grupo = doc.add_paragraph(titulo_grupo)
            run_grupo = p_grupo.runs[0]
            run_grupo.font.name = 'Calibri'
            run_grupo.font.bold = True

            # Color y tamaño según nivel
            if nivel_grupo == 0:
                run_grupo.font.size = Pt(12)
                run_grupo.font.color.rgb = RGBColor(74, 111, 165)
            elif nivel_grupo == 1:
                run_grupo.font.size = Pt(11)
                run_grupo.font.color.rgb = RGBColor(107, 143, 184)
            else:
                run_grupo.font.size = Pt(10)
                run_grupo.font.color.rgb = RGBColor(138, 173, 199)

            # Si hay subgrupos, procesarlos recursivamente
            if subgrupos:
                self._exportar_grupos_word(doc, subgrupos, columnas, modo, nivel_grupo, resultado_agrupacion)
            elif modo == 'detalle' and datos:
                # Crear tabla para los datos
                table = doc.add_table(rows=1 + len(datos), cols=len(columnas))
                table.style = 'Light List Accent 1'

                # Encabezados
                header_cells = table.rows[0].cells
                for idx, col_name in enumerate(columnas):
                    cell = header_cells[idx]
                    cell.text = col_name
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            run.font.bold = True
                            run.font.name = 'Tahoma'
                            run.font.size = Pt(9)

                # Datos
                formatos_columnas = resultado_agrupacion.get('formatos_columnas', {}) if resultado_agrupacion else {}
                for row_idx, fila_datos in enumerate(datos, start=1):
                    row_cells = table.rows[row_idx].cells
                    for col_idx, valor in enumerate(fila_datos):
                        cell = row_cells[col_idx]

                        # Obtener el formato del campo según su columna
                        col_name = columnas[col_idx] if col_idx < len(columnas) else None
                        formato_campo = formatos_columnas.get(col_name, 'ninguno') if col_name else 'ninguno'

                        # Aplicar formato según el tipo de campo
                        if isinstance(valor, (int, float)):
                            if formato_campo == 'moneda':
                                cell.text = f"{valor:,.2f} €"
                            else:
                                # Por defecto, números con 2 decimales
                                cell.text = f"{valor:,.2f}"
                        else:
                            cell.text = str(valor) if valor is not None else ""

                        for paragraph in cell.paragraphs:
                            for run in paragraph.runs:
                                run.font.name = 'Tahoma'
                                run.font.size = Pt(8)

            # Subtotales
            if subtotales:
                indent_subtotal = "    " * (nivel_grupo + 1)
                p_subtotal = doc.add_paragraph(f"{indent_subtotal}▸ Subtotal")
                run_subtotal = p_subtotal.runs[0]
                run_subtotal.font.name = 'Tahoma'
                run_subtotal.font.size = Pt(9)
                run_subtotal.font.bold = True

                for key, valor in subtotales.items():
                    valor_texto = f"{valor:,.2f} €" if isinstance(valor, (int, float)) else str(valor)
                    run_subtotal.add_text(f"  {key}={valor_texto}")

            doc.add_paragraph()  # Espacio entre grupos

    def _set_cell_background(self, cell, color_hex: str):
        """Establece el color de fondo de una celda en Word"""
        shading_elm = OxmlElement('w:shd')
        shading_elm.set(qn('w:fill'), color_hex)
        cell._element.get_or_add_tcPr().append(shading_elm)

    def _add_page_number(self, run):
        """Añade número de página a Word"""
        fldChar1 = OxmlElement('w:fldChar')
        fldChar1.set(qn('w:fldCharType'), 'begin')

        instrText = OxmlElement('w:instrText')
        instrText.set(qn('xml:space'), 'preserve')
        instrText.text = "PAGE"

        fldChar2 = OxmlElement('w:fldChar')
        fldChar2.set(qn('w:fldCharType'), 'end')

        run._r.append(fldChar1)
        run._r.append(instrText)
        run._r.append(fldChar2)

    def exportar_a_pdf(
        self,
        filepath: str,
        informe_nombre: str,
        columnas: List[str],
        datos: List[tuple],
        resultado_agrupacion: Optional[Dict] = None,
        proyecto_nombre: str = "",
        proyecto_codigo: str = ""
    ) -> bool:
        """
        Exporta el informe a PDF usando ReportLab directamente

        Args:
            filepath: Ruta del archivo PDF a crear
            informe_nombre: Nombre del informe
            columnas: Lista de nombres de columnas
            datos: Datos del informe
            resultado_agrupacion: Estructura de agrupaciones y totales (opcional)
            proyecto_nombre: Nombre del proyecto
            proyecto_codigo: Código del proyecto

        Returns:
            True si la exportación fue exitosa
        """
        try:
            # Crear el documento PDF en orientación horizontal
            # A4 landscape = 29.7cm x 21cm
            # Márgenes: 1cm a cada lado
            # Ancho disponible = 29.7cm - 1cm - 1cm = 27.7cm
            doc = SimpleDocTemplate(
                filepath,
                pagesize=landscape(A4),
                topMargin=1*cm,
                bottomMargin=1*cm,
                leftMargin=1*cm,
                rightMargin=1*cm
            )

            # Lista de elementos del documento
            elements = []

            # Estilos
            styles = getSampleStyleSheet()

            # Calcular ancho disponible para tablas
            ancho_pagina = landscape(A4)[0]  # 29.7cm en puntos
            ancho_disponible = ancho_pagina - (1*cm * 2)  # Restar márgenes (27.7cm en puntos)

            # Estilo para título
            style_titulo = ParagraphStyle(
                'Titulo',
                parent=styles['Heading1'],
                fontSize=20,
                textColor=colors.black,
                alignment=TA_CENTER,
                spaceAfter=12
            )

            # Estilo para subtítulo
            style_subtitulo = ParagraphStyle(
                'Subtitulo',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor('#7C7C7C'),
                italic=True,
                alignment=TA_LEFT,
                spaceAfter=6
            )

            # Crear tabla de encabezado con logos y título
            header_data = []
            header_row = []

            # Logo izquierdo (Logo Redes Urbide) - 2.1cm de altura
            if self.logo_redes_path and os.path.exists(self.logo_redes_path):
                img_left = Image(self.logo_redes_path, height=2.1*cm, width=None)
                header_row.append(img_left)
            else:
                header_row.append('')

            # Título en el centro
            titulo_para = Paragraph(informe_nombre.upper(), style_titulo)
            header_row.append(titulo_para)

            # Logo derecho (Logo Urbide) - 2.1cm de altura
            if self.logo_urbide_path and os.path.exists(self.logo_urbide_path):
                img_right = Image(self.logo_urbide_path, height=2.1*cm, width=None)
                header_row.append(img_right)
            else:
                header_row.append('')

            header_data.append(header_row)

            # Tabla de encabezado con anchos: 3.5cm, resto, 3.5cm
            # Ancho disponible = 27.7cm (calculado arriba)
            ancho_titulo = ancho_disponible - (3.5*cm * 2)  # 27.7cm - 7cm = 20.7cm
            header_table = Table(header_data, colWidths=[3.5*cm, ancho_titulo, 3.5*cm])
            header_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),   # Logo izquierdo alineado a la izquierda
                ('ALIGN', (1, 0), (1, 0), 'CENTER'), # Título centrado
                ('ALIGN', (2, 0), (2, 0), 'RIGHT'),  # Logo derecho alineado a la derecha
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            elements.append(header_table)
            elements.append(Spacer(1, 0.5*cm))

            # Información del proyecto
            if proyecto_nombre:
                p_proyecto = Paragraph(proyecto_nombre, style_subtitulo)
                elements.append(p_proyecto)

            # Fecha
            fecha_actual = datetime.now().strftime("%d/%m/%Y")
            style_fecha = ParagraphStyle(
                'Fecha',
                parent=styles['Normal'],
                fontSize=10,
                fontName='Helvetica-Bold',
                spaceAfter=12
            )
            p_fecha = Paragraph(f"FECHA: {fecha_actual}", style_fecha)
            elements.append(p_fecha)
            elements.append(Spacer(1, 0.5*cm))

            # Preparar datos de la tabla
            if resultado_agrupacion and resultado_agrupacion.get('grupos'):
                # Si hay agrupaciones, crear estructura jerárquica
                tabla_datos = self._crear_tabla_grupos_pdf(
                    resultado_agrupacion['grupos'],
                    columnas,
                    resultado_agrupacion.get('modo', 'detalle'),
                    resultado_agrupacion,
                    ancho_disponible
                )
                elements.extend(tabla_datos)

                # Totales generales
                if resultado_agrupacion.get('totales_generales'):
                    elements.append(Spacer(1, 0.3*cm))

                    style_total = ParagraphStyle(
                        'Total',
                        parent=styles['Normal'],
                        fontSize=12,
                        fontName='Helvetica-Bold',
                        spaceAfter=6
                    )
                    p_total = Paragraph("═══ TOTAL GENERAL ═══", style_total)
                    elements.append(p_total)

                    totales = resultado_agrupacion['totales_generales']
                    for key, valor in totales.items():
                        if isinstance(valor, (int, float)):
                            texto = f"{key}: {valor:,.2f} €"
                        else:
                            texto = f"{key}: {valor}"
                        p = Paragraph(texto, styles['Normal'])
                        elements.append(p)
            else:
                # Tabla simple sin agrupaciones
                tabla_datos = [columnas]

                # Formatear datos
                formatos_columnas = resultado_agrupacion.get('formatos_columnas', {}) if resultado_agrupacion else {}
                for fila in datos:
                    fila_formateada = []
                    for col_idx, valor in enumerate(fila):
                        col_name = columnas[col_idx] if col_idx < len(columnas) else None
                        formato_campo = formatos_columnas.get(col_name, 'ninguno') if col_name else 'ninguno'

                        if isinstance(valor, (int, float)):
                            if formato_campo == 'moneda':
                                fila_formateada.append(f"{valor:,.2f} €")
                            else:
                                fila_formateada.append(f"{valor:,.2f}")
                        else:
                            fila_formateada.append(str(valor) if valor is not None else "")
                    tabla_datos.append(fila_formateada)

                # Calcular anchos de columnas dinámicos
                num_columnas = len(columnas)
                ancho_por_columna = ancho_disponible / num_columnas
                col_widths = [ancho_por_columna] * num_columnas

                # Crear tabla con anchos dinámicos
                tabla = Table(tabla_datos, colWidths=col_widths)
                tabla.setStyle(TableStyle([
                    # Encabezado
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D9D9D9')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    # Datos
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                    # Bordes
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(tabla)

            # Pie de página
            elements.append(Spacer(1, 1*cm))
            style_footer = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.HexColor('#7C7C7C'),
                italic=True,
                alignment=TA_CENTER
            )
            p_footer = Paragraph(
                f"Generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}",
                style_footer
            )
            elements.append(p_footer)

            # Construir el PDF
            doc.build(elements)
            print(f"✓ PDF generado correctamente: {filepath}")
            return True

        except Exception as e:
            print(f"Error al exportar a PDF: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _crear_tabla_grupos_pdf(
        self,
        grupos: List[Dict],
        columnas: List[str],
        modo: str = 'detalle',
        resultado_agrupacion: Optional[Dict] = None,
        ancho_disponible: float = 24*cm
    ) -> List:
        """Crea elementos de tabla para grupos jerárquicos en PDF"""
        elements = []
        styles = getSampleStyleSheet()

        for grupo in grupos:
            clave = grupo.get('clave', '')
            campo = grupo.get('campo', '')
            datos = grupo.get('datos', [])
            subtotales = grupo.get('subtotales', {})
            subgrupos = grupo.get('subgrupos')
            nivel = grupo.get('nivel', 0)

            # Estilo del grupo según nivel
            if nivel == 0:
                bg_color = colors.HexColor('#4A6FA5')
                font_size = 12
            elif nivel == 1:
                bg_color = colors.HexColor('#6B8FB8')
                font_size = 11
            else:
                bg_color = colors.HexColor('#8AADC7')
                font_size = 10

            # Título del grupo
            indent = "    " * nivel
            titulo_grupo = f"{indent}📁 {campo.upper()}: {clave}"

            style_grupo = ParagraphStyle(
                f'Grupo{nivel}',
                parent=styles['Normal'],
                fontSize=font_size,
                fontName='Helvetica-Bold',
                textColor=colors.white,
                spaceAfter=6
            )

            # Crear tabla para el título del grupo
            grupo_data = [[Paragraph(titulo_grupo, style_grupo)]]
            grupo_table = Table(grupo_data, colWidths=[ancho_disponible])
            grupo_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), bg_color),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), font_size),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(grupo_table)
            elements.append(Spacer(1, 0.2*cm))

            # Si hay subgrupos, procesarlos recursivamente
            if subgrupos:
                sub_elements = self._crear_tabla_grupos_pdf(
                    subgrupos,
                    columnas,
                    modo,
                    resultado_agrupacion,
                    ancho_disponible
                )
                elements.extend(sub_elements)
            elif modo == 'detalle' and datos:
                # Crear tabla de datos
                tabla_datos = [columnas]
                formatos_columnas = resultado_agrupacion.get('formatos_columnas', {}) if resultado_agrupacion else {}

                for fila in datos:
                    fila_formateada = []
                    for col_idx, valor in enumerate(fila):
                        col_name = columnas[col_idx] if col_idx < len(columnas) else None
                        formato_campo = formatos_columnas.get(col_name, 'ninguno') if col_name else 'ninguno'

                        if isinstance(valor, (int, float)):
                            if formato_campo == 'moneda':
                                fila_formateada.append(f"{valor:,.2f} €")
                            else:
                                fila_formateada.append(f"{valor:,.2f}")
                        else:
                            fila_formateada.append(str(valor) if valor is not None else "")
                    tabla_datos.append(fila_formateada)

                # Calcular anchos de columnas dinámicos
                num_columnas = len(columnas)
                ancho_por_columna = ancho_disponible / num_columnas
                col_widths = [ancho_por_columna] * num_columnas

                tabla = Table(tabla_datos, colWidths=col_widths)
                tabla.setStyle(TableStyle([
                    # Encabezado
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D9D9D9')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    # Datos
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                    # Bordes
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(tabla)
                elements.append(Spacer(1, 0.2*cm))

            # Subtotales
            if subtotales:
                indent_subtotal = "    " * (nivel + 1)
                texto_subtotales = f"{indent_subtotal}▸ Subtotal"

                for key, valor in subtotales.items():
                    if isinstance(valor, (int, float)):
                        texto_subtotales += f"  {key}={valor:,.2f} €"
                    else:
                        texto_subtotales += f"  {key}={valor}"

                style_subtotal = ParagraphStyle(
                    'Subtotal',
                    parent=styles['Normal'],
                    fontSize=9,
                    fontName='Helvetica-Bold',
                    spaceAfter=6
                )

                subtotal_data = [[Paragraph(texto_subtotales, style_subtotal)]]
                subtotal_table = Table(subtotal_data, colWidths=[ancho_disponible])
                subtotal_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#E7E6E6')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(subtotal_table)

            elements.append(Spacer(1, 0.3*cm))

        return elements
