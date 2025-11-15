# script/informes_exportacion.py
"""
Módulo de exportación de informes a Excel, Word y PDF
Genera documentos profesionales con agrupaciones, subtotales y formato corporativo
"""

import os
import re
from datetime import datetime, date
from typing import List, Dict, Any, Optional
import xlsxwriter
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import subprocess
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
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

    def _es_fecha(self, valor) -> bool:
        """Detecta si un valor es una fecha"""
        # Detectar datetime.datetime y datetime.date
        if isinstance(valor, (datetime, date)):
            return True
        if isinstance(valor, str):
            # Detectar formatos comunes de fecha: DD/MM/YYYY, YYYY-MM-DD, DD-MM-YYYY
            patrones_fecha = [
                r'^\d{2}/\d{2}/\d{4}$',  # DD/MM/YYYY
                r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
                r'^\d{2}-\d{2}-\d{4}$',  # DD-MM-YYYY
                r'^\d{1,2}/\d{1,2}/\d{4}$',  # D/M/YYYY o DD/M/YYYY
            ]
            for patron in patrones_fecha:
                if re.match(patron, str(valor).strip()):
                    return True
        return False

    def _convertir_fecha_excel(self, valor):
        """Convierte un valor de fecha a datetime para Excel"""
        # Si ya es datetime o date, convertir a datetime
        if isinstance(valor, datetime):
            return valor
        if isinstance(valor, date):
            return datetime.combine(valor, datetime.min.time())
        if isinstance(valor, str):
            valor = str(valor).strip()
            # Intentar parsear diferentes formatos
            formatos = [
                '%d/%m/%Y',  # DD/MM/YYYY
                '%Y-%m-%d',  # YYYY-MM-DD
                '%d-%m-%Y',  # DD-MM-YYYY
                '%Y-%m-%d %H:%M:%S',  # YYYY-MM-DD HH:MM:SS
                '%d/%m/%Y %H:%M:%S',  # DD/MM/YYYY HH:MM:SS
            ]
            for formato in formatos:
                try:
                    return datetime.strptime(valor, formato)
                except ValueError:
                    continue
        return None

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

            # Configurar impresión: horizontal y ajustar todas las columnas en una página
            worksheet.set_landscape()  # Orientación horizontal
            worksheet.fit_to_pages(1, 0)  # Ajustar ancho a 1 página, alto ilimitado

            # Definir formatos
            formato_titulo = workbook.add_format({
                'bold': True,
                'font_size': 20,
                'font_name': 'Calibri',
                'align': 'left',
                'valign': 'vcenter'
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

            formato_fecha_celda = workbook.add_format({
                'font_size': 8,
                'font_name': 'Tahoma',
                'num_format': 'dd/mm/yyyy',
                'border': 1,
                'align': 'center',
                'valign': 'vcenter'
            })

            # Fila actual
            row = 0

            # Configurar altura de la primera fila: 2.1cm = ~59.5 puntos
            # (2.1cm / 2.54cm/inch * 72 puntos/inch = 59.5)
            worksheet.set_row(row, 59.5)

            # Configurar ancho de primera y última columna para los logos
            worksheet.set_column(0, 0, 15)
            worksheet.set_column(len(columnas) - 1, len(columnas) - 1, 15)

            # Logo izquierdo (Logo Redes Urbide) - alineado a la izquierda
            # Altura de imagen: 2.1cm
            if self.logo_redes_path and os.path.exists(self.logo_redes_path):
                worksheet.insert_image(row, 0, self.logo_redes_path, {
                    'x_scale': 1.0,
                    'y_scale': 1.0,
                    'x_offset': 2,   # Alineado a la izquierda con pequeño margen
                    'y_offset': 2,
                    'object_position': 1
                })

            # Título del informe - combinar todas las celdas excepto primera y última
            num_cols = len(columnas)
            # Merge desde columna 1 (segunda) hasta columna num_cols-2 (penúltima)
            if num_cols > 2:
                worksheet.merge_range(row, 1, row, num_cols - 2, informe_nombre.upper(), formato_titulo)
            else:
                worksheet.write(row, 1, informe_nombre.upper(), formato_titulo)

            # Logo derecho (Logo Urbide) - alineado a la derecha
            # Altura de imagen: 2.1cm
            if self.logo_urbide_path and os.path.exists(self.logo_urbide_path):
                # Para alinear a la derecha, calculamos el offset basado en el ancho de la columna
                # Ancho columna 15 ≈ 105 píxeles. Necesitamos offset para alinear a la derecha
                worksheet.insert_image(row, len(columnas) - 1, self.logo_urbide_path, {
                    'x_scale': 1.0,
                    'y_scale': 1.0,
                    'x_offset': 50,  # Offset para alinear a la derecha
                    'y_offset': 2,
                    'object_position': 1
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

                        # Aplicar formato según el tipo de campo
                        if isinstance(valor, (int, float)):
                            if formato_campo == 'moneda':
                                worksheet.write(row, col_idx, valor, formato_moneda)
                            elif formato_campo == 'decimal':
                                worksheet.write(row, col_idx, valor, formato_decimal)
                            else:
                                # Por defecto, números decimales con 2 decimales
                                worksheet.write(row, col_idx, valor, formato_decimal)
                        elif self._es_fecha(valor):
                            # Detectar y formatear fechas
                            fecha_dt = self._convertir_fecha_excel(valor)
                            if fecha_dt:
                                worksheet.write_datetime(row, col_idx, fecha_dt, formato_fecha_celda)
                            else:
                                worksheet.write(row, col_idx, valor, formato_datos)
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
        modo: str = 'detalle',
        resultado_agrupacion: Optional[Dict] = None
    ) -> int:
        """Exporta grupos jerárquicos a Excel (recursivo)"""
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

                        # Aplicar formato según el tipo de campo
                        if isinstance(valor, (int, float)):
                            if formato_campo == 'moneda':
                                worksheet.write(row, col_idx, valor, formato_moneda)
                            elif formato_campo == 'decimal':
                                worksheet.write(row, col_idx, valor, formato_decimal)
                            else:
                                # Por defecto, números decimales con 2 decimales
                                worksheet.write(row, col_idx, valor, formato_decimal)
                        elif self._es_fecha(valor):
                            # Detectar y formatear fechas
                            fecha_dt = self._convertir_fecha_excel(valor)
                            if fecha_dt:
                                # Necesitamos obtener formato_fecha_celda desde la función padre
                                formato_fecha_celda = workbook.add_format({
                                    'font_size': 8,
                                    'font_name': 'Tahoma',
                                    'num_format': 'dd/mm/yyyy',
                                    'border': 1,
                                    'align': 'center',
                                    'valign': 'vcenter'
                                })
                                worksheet.write_datetime(row, col_idx, fecha_dt, formato_fecha_celda)
                            else:
                                worksheet.write(row, col_idx, str(valor) if valor is not None else "", formato_datos)
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

            # Configurar márgenes y orientación horizontal
            sections = doc.sections
            for section in sections:
                # Cambiar a orientación horizontal (landscape)
                section.orientation = 1  # 1 = landscape, 0 = portrait
                # Intercambiar ancho y alto para landscape
                section.page_width, section.page_height = section.page_height, section.page_width
                section.top_margin = Cm(1)  # 1cm según especificación
                section.bottom_margin = Cm(1)  # 1cm según especificación
                section.left_margin = Cm(1)  # 1cm según especificación
                section.right_margin = Cm(1)  # 1cm según especificación
                # Configurar encabezado desde arriba: 0,2cm
                section.header_distance = Cm(0.2)

            # Encabezado con logos, título y fecha
            # Ancho total disponible: 29.7cm (A4 landscape) - 2cm (márgenes) = 27.7cm
            header = sections[0].header
            header_table = header.add_table(rows=2, cols=3, width=Cm(27.7))
            header_table.alignment = WD_TABLE_ALIGNMENT.CENTER

            # Configurar anchos de columnas: 4cm (logo), resto para título, 4cm (logo)
            header_table.columns[0].width = Cm(4)
            header_table.columns[1].width = Cm(19.7)  # 27.7 - 4 - 4
            header_table.columns[2].width = Cm(4)

            # === FILA 1: Logos y Título ===

            # Logo izquierdo (Logo Redes Urbide) - altura máxima 2cm
            if self.logo_redes_path and os.path.exists(self.logo_redes_path):
                cell_logo_left = header_table.rows[0].cells[0]
                cell_logo_left.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                paragraph = cell_logo_left.paragraphs[0]
                paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
                run = paragraph.add_run()
                run.add_picture(self.logo_redes_path, height=Cm(2))  # Altura máxima 2cm

            # Título del informe en el centro
            cell_titulo = header_table.rows[0].cells[1]
            cell_titulo.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            paragraph_titulo = cell_titulo.paragraphs[0]
            paragraph_titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run_titulo = paragraph_titulo.add_run(informe_nombre.upper())
            run_titulo.font.name = 'Calibri'
            run_titulo.font.size = Pt(18)
            run_titulo.font.bold = True
            run_titulo.font.color.rgb = RGBColor(0, 0, 0)

            # Logo derecho (Logo Urbide) - altura máxima 2cm
            if self.logo_urbide_path and os.path.exists(self.logo_urbide_path):
                cell_logo_right = header_table.rows[0].cells[2]
                cell_logo_right.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                paragraph = cell_logo_right.paragraphs[0]
                paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                run = paragraph.add_run()
                run.add_picture(self.logo_urbide_path, height=Cm(2))  # Altura máxima 2cm

            # === FILA 2: Fecha (solo en la columna central) ===

            # Fecha de generación centrada
            fecha_actual = datetime.now().strftime("%d/%m/%Y")
            cell_fecha = header_table.rows[1].cells[1]
            cell_fecha.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            paragraph_fecha = cell_fecha.paragraphs[0]
            paragraph_fecha.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run_fecha = paragraph_fecha.add_run(f"Fecha: {fecha_actual}")
            run_fecha.font.name = 'Calibri'
            run_fecha.font.size = Pt(10)
            run_fecha.font.bold = True
            run_fecha.font.color.rgb = RGBColor(100, 100, 100)

            # Información del proyecto (opcional)
            if proyecto_nombre:
                p = doc.add_paragraph(proyecto_nombre)
                p.runs[0].font.name = 'Tahoma'
                p.runs[0].font.size = Pt(10)
                p.runs[0].font.italic = True
                p.runs[0].font.color.rgb = RGBColor(124, 124, 124)
                doc.add_paragraph()  # Espacio después del proyecto
            else:
                doc.add_paragraph()  # Espacio inicial si no hay proyecto

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
                # Ancho de página: 29.7cm - 2cm (márgenes) = 27.7cm
                table = doc.add_table(rows=1 + len(datos), cols=len(columnas))
                table.style = 'Light Grid Accent 1'
                table.autofit = False
                table.allow_autofit = False

                # Ajustar ancho de tabla al ancho de página (27.7cm)
                table.width = Cm(27.7)

                # Distribuir ancho equitativamente entre columnas
                col_width = Cm(27.7 / len(columnas))
                for column in table.columns:
                    column.width = col_width

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
                table.autofit = False
                table.allow_autofit = False

                # Ajustar ancho de tabla al ancho de página (27.7cm)
                table.width = Cm(27.7)

                # Distribuir ancho equitativamente entre columnas
                col_width = Cm(27.7 / len(columnas))
                for column in table.columns:
                    column.width = col_width

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
        Exporta el informe a PDF generando primero un Word y convirtiéndolo a PDF

        Args:
            filepath: Ruta del archivo PDF a crear
            informe_nombre: Nombre del informe
            columnas: Lista de nombres de columnas
            datos: Datos del informe
            resultado_agrupacion: Estructura de agrupaciones y totales (opcional)
            proyecto_nombre: Nombre del proyecto (no se usa, se deja vacío)
            proyecto_codigo: Código del proyecto (no se usa, se deja vacío)

        Returns:
            True si la exportación fue exitosa
        """
        import tempfile

        try:
            # Paso 1: Generar el archivo Word temporal
            print("Generando archivo Word temporal...")
            temp_word = tempfile.NamedTemporaryFile(suffix='.docx', delete=False)
            temp_word_path = temp_word.name
            temp_word.close()

            # Usar la misma función de exportar_a_word
            exito_word = self.exportar_a_word(
                filepath=temp_word_path,
                informe_nombre=informe_nombre,
                columnas=columnas,
                datos=datos,
                resultado_agrupacion=resultado_agrupacion,
                proyecto_nombre=proyecto_nombre,
                proyecto_codigo=proyecto_codigo
            )

            if not exito_word:
                print("Error al generar el archivo Word temporal")
                return False

            # Paso 2: Convertir Word a PDF usando el sistema
            print(f"Convirtiendo Word a PDF: {temp_word_path} -> {filepath}")

            # Intentar diferentes métodos de conversión
            exito_conversion = self._convertir_word_a_pdf(temp_word_path, filepath)

            # Paso 3: Limpiar archivo temporal
            try:
                os.unlink(temp_word_path)
            except:
                pass

            if exito_conversion:
                print(f"✓ PDF generado correctamente: {filepath}")
                return True
            else:
                print("✗ Error al convertir Word a PDF")
                return False

        except Exception as e:
            print(f"Error al exportar a PDF: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _convertir_word_a_pdf(self, word_path: str, pdf_path: str) -> bool:
        """
        Convierte un archivo Word a PDF usando diferentes métodos disponibles

        Args:
            word_path: Ruta del archivo Word de entrada
            pdf_path: Ruta del archivo PDF de salida

        Returns:
            True si la conversión fue exitosa
        """
        import platform

        # Método 1: Intentar con win32com (Microsoft Word COM)
        if platform.system() == 'Windows':
            try:
                import win32com.client
                import pythoncom

                pythoncom.CoInitialize()
                word = win32com.client.Dispatch('Word.Application')
                word.Visible = False

                # Abrir documento
                doc = word.Documents.Open(os.path.abspath(word_path))

                # Guardar como PDF (wdFormatPDF = 17)
                doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17)
                doc.Close()
                word.Quit()

                pythoncom.CoUninitialize()

                print("✓ Conversión exitosa usando Microsoft Word COM")
                return True

            except Exception as e:
                print(f"⚠ No se pudo usar Word COM: {e}")

        # Método 2: Intentar con LibreOffice (si está instalado)
        try:
            # Buscar LibreOffice en ubicaciones comunes
            libreoffice_paths = [
                r"C:\Program Files\LibreOffice\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
                "/usr/bin/libreoffice",
                "/usr/local/bin/libreoffice",
            ]

            soffice_path = None
            for path in libreoffice_paths:
                if os.path.exists(path):
                    soffice_path = path
                    break

            if soffice_path:
                cmd = [
                    soffice_path,
                    "--headless",
                    "--convert-to", "pdf",
                    "--outdir", os.path.dirname(os.path.abspath(pdf_path)),
                    os.path.abspath(word_path)
                ]

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

                # LibreOffice genera el PDF con el mismo nombre que el Word
                generated_pdf = os.path.join(
                    os.path.dirname(os.path.abspath(pdf_path)),
                    os.path.splitext(os.path.basename(word_path))[0] + '.pdf'
                )

                if os.path.exists(generated_pdf):
                    # Mover al destino final si es diferente
                    if generated_pdf != os.path.abspath(pdf_path):
                        import shutil
                        shutil.move(generated_pdf, pdf_path)

                    print("✓ Conversión exitosa usando LibreOffice")
                    return True

        except Exception as e:
            print(f"⚠ No se pudo usar LibreOffice: {e}")

        # Método 3: Mensaje de error si ningún método funcionó
        print("\n" + "="*70)
        print("ERROR: No se pudo convertir el documento Word a PDF")
        print("="*70)
        print("\nSoluciones posibles:")
        print("1. Instalar Microsoft Word")
        print("2. Instalar LibreOffice: https://www.libreoffice.org/download/")
        print("3. Instalar la librería win32com: pip install pywin32")
        print("\nEl archivo Word se guardó correctamente en:")
        print(f"   {word_path}")
        print("\nPuede abrir este archivo y guardarlo manualmente como PDF.")
        print("="*70 + "\n")

        return False

    def exportar_a_pdf_old(
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
        [VERSIÓN ANTIGUA] Exporta el informe a PDF usando ReportLab
        Esta función se mantiene por compatibilidad pero ya no se usa

        Args:
            filepath: Ruta del archivo PDF a crear
            informe_nombre: Nombre del informe
            columnas: Lista de nombres de columnas
            datos: Datos del informe
            resultado_agrupacion: Estructura de agrupaciones y totales (opcional)
            proyecto_nombre: Nombre del proyecto (no se usa, se deja vacío)
            proyecto_codigo: Código del proyecto (no se usa, se deja vacío)

        Returns:
            True si la exportación fue exitosa
        """
        try:
            # Crear documento PDF en orientación horizontal
            doc = SimpleDocTemplate(
                filepath,
                pagesize=landscape(A4),
                rightMargin=1*cm,
                leftMargin=1*cm,
                topMargin=1*cm,
                bottomMargin=1*cm
            )

            # Elementos del documento
            elements = []

            # Estilos
            styles = getSampleStyleSheet()
            titulo_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=20,
                textColor=colors.HexColor('#000000'),
                spaceAfter=12,
                alignment=TA_CENTER
            )

            # Encabezado con logos y título
            header_data = []
            header_row = []

            # Logo izquierdo (Logo Redes Urbide)
            if self.logo_redes_path and os.path.exists(self.logo_redes_path):
                logo_redes = Image(self.logo_redes_path, width=3.5*cm, height=2.1*cm, kind='proportional')
                header_row.append(logo_redes)
            else:
                header_row.append("")

            # Título en el centro
            titulo_para = Paragraph(informe_nombre.upper(), titulo_style)
            header_row.append(titulo_para)

            # Logo derecho (Logo Urbide)
            if self.logo_urbide_path and os.path.exists(self.logo_urbide_path):
                logo_urbide = Image(self.logo_urbide_path, width=3.5*cm, height=2.1*cm, kind='proportional')
                header_row.append(logo_urbide)
            else:
                header_row.append("")

            header_data.append(header_row)

            # Crear tabla del encabezado
            header_table = Table(header_data, colWidths=[3.5*cm, 17*cm, 3.5*cm])
            header_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            elements.append(header_table)
            elements.append(Spacer(1, 0.5*cm))

            # Fecha
            fecha_actual = datetime.now().strftime("%d/%m/%Y")
            fecha_style = ParagraphStyle(
                'Fecha',
                parent=styles['Normal'],
                fontSize=10,
                fontName='Helvetica-Bold'
            )
            fecha_para = Paragraph(f"FECHA: {fecha_actual}", fecha_style)
            elements.append(fecha_para)
            elements.append(Spacer(1, 0.3*cm))

            # Preparar datos de la tabla
            table_data = []

            # Si hay agrupaciones, procesarlas
            if resultado_agrupacion and resultado_agrupacion.get('grupos'):
                # Encabezados de columna
                table_data.append(columnas)

                # Procesar grupos recursivamente
                def procesar_grupos_pdf(grupos, nivel=0):
                    for grupo in grupos:
                        # Encabezado del grupo
                        grupo_row = [grupo.get('titulo', '')] + [''] * (len(columnas) - 1)
                        table_data.append(grupo_row)

                        # Filas de datos del grupo
                        if grupo.get('filas'):
                            for fila in grupo['filas']:
                                table_data.append(list(fila))

                        # Subtotal del grupo
                        if grupo.get('subtotal'):
                            subtotal_row = ['SUBTOTAL:'] + [''] * (len(columnas) - 1)
                            table_data.append(subtotal_row)

                        # Subgrupos
                        if grupo.get('subgrupos'):
                            procesar_grupos_pdf(grupo['subgrupos'], nivel + 1)

                procesar_grupos_pdf(resultado_agrupacion['grupos'])

                # Totales generales
                if resultado_agrupacion.get('totales'):
                    total_row = ['TOTAL GENERAL:'] + [''] * (len(columnas) - 1)
                    table_data.append(total_row)

            else:
                # Sin agrupaciones, tabla simple
                table_data.append(columnas)
                for fila in datos:
                    # Convertir valores a strings
                    fila_str = []
                    for valor in fila:
                        if isinstance(valor, (datetime, date)):
                            fila_str.append(valor.strftime('%d/%m/%Y'))
                        elif valor is None:
                            fila_str.append('')
                        else:
                            fila_str.append(str(valor))
                    table_data.append(fila_str)

            # Calcular anchos de columna dinámicamente
            num_cols = len(columnas)
            ancho_disponible = 24*cm  # Ancho total disponible en landscape
            col_widths = [ancho_disponible / num_cols] * num_cols

            # Crear tabla
            data_table = Table(table_data, colWidths=col_widths, repeatRows=1)

            # Estilos de la tabla
            table_style = TableStyle([
                # Encabezado
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D9D9D9')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('TOPPADDING', (0, 0), (-1, 0), 6),

                # Datos
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F0F0')]),
            ])

            data_table.setStyle(table_style)
            elements.append(data_table)

            # Construir PDF
            doc.build(elements)

            print(f"✓ PDF generado correctamente: {filepath}")
            return True

        except Exception as e:
            print(f"Error al exportar a PDF: {e}")
            import traceback
            traceback.print_exc()
            return False
