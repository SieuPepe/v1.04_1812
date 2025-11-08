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
import subprocess


class InformesExportador:
    """Exportador de informes a múltiples formatos"""

    def __init__(self, schema: str):
        self.schema = schema
        self.logo_redes_path = None
        self.logo_urbide_path = None
        self._buscar_logos()

    def _buscar_logos(self):
        """Busca los logos en la carpeta source con búsqueda flexible"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        source_dir = os.path.join(base_dir, "source")

        if os.path.exists(source_dir):
            archivos = os.listdir(source_dir)

            # Buscar logos con diferentes patrones
            patrones_izquierdo = ["redes", "artanda", "logo"]
            patrones_derecho = ["urbide", "artanda2"]

            for file in archivos:
                file_lower = file.lower()
                if not file_lower.endswith(('.png', '.jpg', '.jpeg')):
                    continue

                # Logo izquierdo
                if not self.logo_redes_path:
                    for patron in patrones_izquierdo:
                        if patron in file_lower:
                            self.logo_redes_path = os.path.join(source_dir, file)
                            print(f"✓ Logo izquierdo encontrado: {file}")
                            break

                # Logo derecho
                if not self.logo_urbide_path:
                    for patron in patrones_derecho:
                        if patron in file_lower:
                            self.logo_urbide_path = os.path.join(source_dir, file)
                            print(f"✓ Logo derecho encontrado: {file}")
                            break

            # Si no se encuentra el logo izquierdo, usar el primero disponible
            if not self.logo_redes_path:
                for file in archivos:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')) and 'logo' in file.lower():
                        self.logo_redes_path = os.path.join(source_dir, file)
                        print(f"⚠ Usando logo por defecto (izquierdo): {file}")
                        break

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

            # Fila actual
            row = 0

            # Insertar logos si existen
            if self.logo_redes_path and os.path.exists(self.logo_redes_path):
                worksheet.insert_image(row, 0, self.logo_redes_path, {'x_scale': 0.15, 'y_scale': 0.15})

            if self.logo_urbide_path and os.path.exists(self.logo_urbide_path):
                worksheet.insert_image(row, len(columnas) - 2, self.logo_urbide_path, {'x_scale': 0.15, 'y_scale': 0.15})

            row += 5  # Espacio para logos

            # Título del informe
            worksheet.merge_range(row, 0, row, len(columnas) - 1, informe_nombre.upper(), formato_titulo)
            worksheet.set_row(row, 30)
            row += 2

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
                    resultado_agrupacion['grupos'],
                    columnas,
                    row,
                    formato_header_nivel0,
                    formato_header_nivel1,
                    formato_header_nivel2,
                    formato_header_columnas,
                    formato_datos,
                    formato_moneda,
                    formato_subtotal,
                    formato_subtotal_texto,
                    resultado_agrupacion.get('modo', 'detalle')
                )

                # Totales generales - ALINEADOS CON LAS COLUMNAS CORRECTAS
                if resultado_agrupacion.get('totales_generales'):
                    row += 1
                    worksheet.write(row, 0, "═══ TOTAL GENERAL ═══", formato_total_texto)

                    totales = resultado_agrupacion['totales_generales']
                    for key, valor in totales.items():
                        # Extraer el nombre del campo del key
                        campo_nombre = key.split('(')[1].rstrip(')')

                        # Buscar la columna correspondiente
                        if campo_nombre in columnas:
                            col_idx = columnas.index(campo_nombre)
                            worksheet.write(row, col_idx, valor, formato_total)
                        elif campo_nombre == '*':
                            # COUNT(*) se escribe en la segunda columna
                            worksheet.write(row, 1, valor, formato_total)

            else:
                # Exportar sin agrupaciones (tabla simple)
                # Encabezados de columnas
                for col_idx, col_name in enumerate(columnas):
                    worksheet.write(row, col_idx, col_name, formato_header_columnas)
                    worksheet.set_column(col_idx, col_idx, 15)  # Ancho por defecto
                row += 1

                # Datos
                for fila_datos in datos:
                    for col_idx, valor in enumerate(fila_datos):
                        # Detectar si es moneda
                        if isinstance(valor, (int, float)) and col_idx > 0:
                            worksheet.write(row, col_idx, valor, formato_moneda)
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
        grupos: List[Dict],
        columnas: List[str],
        start_row: int,
        formato_nivel0,
        formato_nivel1,
        formato_nivel2,
        formato_header_columnas,
        formato_datos,
        formato_moneda,
        formato_subtotal,
        formato_subtotal_texto,
        modo: str = 'detalle'
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
                    subgrupos,
                    columnas,
                    row,
                    formato_nivel0,
                    formato_nivel1,
                    formato_nivel2,
                    formato_header_columnas,
                    formato_datos,
                    formato_moneda,
                    formato_subtotal,
                    formato_subtotal_texto,
                    modo
                )
            elif modo == 'detalle':
                # Encabezados de columnas para este grupo
                for col_idx, col_name in enumerate(columnas):
                    worksheet.write(row, col_idx, col_name, formato_header_columnas)
                row += 1

                # Datos del grupo
                for fila_datos in datos:
                    for col_idx, valor in enumerate(fila_datos):
                        if isinstance(valor, (int, float)) and col_idx > 0:
                            worksheet.write(row, col_idx, valor, formato_moneda)
                        else:
                            worksheet.write(row, col_idx, str(valor) if valor is not None else "", formato_datos)
                    row += 1

            # Subtotales del grupo - ALINEADOS CON LAS COLUMNAS CORRECTAS
            if subtotales:
                indent_subtotal = "    " * (nivel + 1)

                # Escribir "Subtotal" en la primera columna (con formato de texto)
                worksheet.write(row, 0, f"{indent_subtotal}▸ Subtotal", formato_subtotal_texto)

                # Mapear subtotales a las columnas correctas
                for key, valor in subtotales.items():
                    # Extraer el nombre del campo del key (ej: "SUM(presupuesto)" -> "presupuesto")
                    # El formato es "FUNCION(campo)" o "COUNT(*)"
                    campo_nombre = key.split('(')[1].rstrip(')')

                    # Buscar la columna correspondiente
                    if campo_nombre in columnas:
                        col_idx = columnas.index(campo_nombre)
                        worksheet.write(row, col_idx, valor, formato_subtotal)
                    elif campo_nombre == '*':
                        # COUNT(*) se escribe en la segunda columna
                        worksheet.write(row, 1, valor, formato_subtotal)

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

            # Configurar márgenes
            sections = doc.sections
            for section in sections:
                section.top_margin = Cm(2)
                section.bottom_margin = Cm(2)
                section.left_margin = Cm(2)
                section.right_margin = Cm(2)

            # Encabezado con logos
            header = sections[0].header
            header_table = header.add_table(rows=1, cols=3, width=Inches(7))
            header_table.alignment = WD_TABLE_ALIGNMENT.CENTER

            # Logo izquierdo
            if self.logo_redes_path and os.path.exists(self.logo_redes_path):
                cell_logo_left = header_table.rows[0].cells[0]
                paragraph = cell_logo_left.paragraphs[0]
                run = paragraph.add_run()
                run.add_picture(self.logo_redes_path, width=Inches(1.2))

            # Espacio central
            header_table.rows[0].cells[1].text = ""

            # Logo derecho
            if self.logo_urbide_path and os.path.exists(self.logo_urbide_path):
                cell_logo_right = header_table.rows[0].cells[2]
                paragraph = cell_logo_right.paragraphs[0]
                paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                run = paragraph.add_run()
                run.add_picture(self.logo_urbide_path, width=Inches(1.5))

            # Título del informe
            titulo = doc.add_heading(informe_nombre.upper(), level=1)
            titulo.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = titulo.runs[0]
            run.font.name = 'Calibri'
            run.font.size = Pt(24)
            run.font.color.rgb = RGBColor(0, 0, 0)

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
                    resultado_agrupacion.get('modo', 'detalle')
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
                for row_idx, fila_datos in enumerate(datos, start=1):
                    row_cells = table.rows[row_idx].cells
                    for col_idx, valor in enumerate(fila_datos):
                        cell = row_cells[col_idx]
                        if isinstance(valor, (int, float)):
                            cell.text = f"{valor:,.2f} €" if col_idx > 0 else str(valor)
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
        nivel: int = 0
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
                self._exportar_grupos_word(doc, subgrupos, columnas, modo, nivel_grupo)
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
                for row_idx, fila_datos in enumerate(datos, start=1):
                    row_cells = table.rows[row_idx].cells
                    for col_idx, valor in enumerate(fila_datos):
                        cell = row_cells[col_idx]
                        if isinstance(valor, (int, float)):
                            cell.text = f"{valor:,.2f} €" if col_idx > 0 else str(valor)
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
        Exporta el informe a PDF (genera Word y lo convierte a PDF)

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
            # Generar Word temporal
            word_path = filepath.replace('.pdf', '_temp.docx')

            if not self.exportar_a_word(
                word_path,
                informe_nombre,
                columnas,
                datos,
                resultado_agrupacion,
                proyecto_nombre,
                proyecto_codigo
            ):
                return False

            # Convertir a PDF usando LibreOffice (si está disponible)
            try:
                subprocess.run([
                    'libreoffice',
                    '--headless',
                    '--convert-to', 'pdf',
                    '--outdir', os.path.dirname(filepath),
                    word_path
                ], check=True, capture_output=True)

                # Renombrar si es necesario
                generated_pdf = word_path.replace('.docx', '.pdf')
                if generated_pdf != filepath and os.path.exists(generated_pdf):
                    os.rename(generated_pdf, filepath)

                # Eliminar Word temporal
                if os.path.exists(word_path):
                    os.remove(word_path)

                return True

            except (subprocess.CalledProcessError, FileNotFoundError):
                # Si LibreOffice no está disponible, dejar el archivo Word
                print("LibreOffice no disponible. Se ha generado el archivo Word.")
                print(f"Puede convertirlo manualmente a PDF: {word_path}")
                return True

        except Exception as e:
            print(f"Error al exportar a PDF: {e}")
            import traceback
            traceback.print_exc()
            return False
