# script/pdf_templates.py
"""
Sistema de Plantillas PDF con ReportLab
Generación de informes PDF con control total del diseño, similar a Access
"""

import os
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, Image, PageBreak, KeepTogether, Frame, PageTemplate
)
from reportlab.pdfgen import canvas
from PIL import Image as PILImage


class PDFTemplate:
    """Clase base para plantillas PDF con configuración común"""

    def __init__(
        self,
        schema: str,
        orientacion: str = "horizontal",  # horizontal o vertical
        titulo: str = "",
        subtitulo: str = "",
        proyecto_nombre: str = "",
        proyecto_codigo: str = "",
        fecha: str = ""
    ):
        """
        Inicializa la plantilla PDF

        Args:
            schema: Nombre del esquema de BD
            orientacion: "horizontal" o "vertical"
            titulo: Título principal del informe
            subtitulo: Subtítulo del informe
            proyecto_nombre: Nombre del proyecto
            proyecto_codigo: Código del proyecto
            fecha: Fecha del informe (si no se proporciona, usa fecha actual)
        """
        self.schema = schema
        self.orientacion = orientacion
        self.titulo = titulo
        self.subtitulo = subtitulo
        self.proyecto_nombre = proyecto_nombre
        self.proyecto_codigo = proyecto_codigo
        self.fecha = fecha if fecha else datetime.now().strftime("%d/%m/%Y")

        # Configurar tamaño de página
        if orientacion == "horizontal":
            self.pagesize = landscape(A4)  # 29.7 x 21 cm
        else:
            self.pagesize = A4  # 21 x 29.7 cm

        # Márgenes (en cm)
        self.margen_superior = 1.5 * cm
        self.margen_inferior = 1.5 * cm
        self.margen_izquierdo = 1.5 * cm
        self.margen_derecho = 1.5 * cm

        # Buscar logos
        self.logo_izquierdo_path = None
        self.logo_derecho_path = None
        self._buscar_logos()

        # Estilos
        self._configurar_estilos()

        # Almacenar elementos del documento
        self.elements = []

    def _buscar_logos(self):
        """Busca los logos en las ubicaciones estándar"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Directorios donde buscar
        directorios = [
            os.path.join(base_dir, "resources", "images"),
            base_dir
        ]

        for directorio in directorios:
            if not os.path.exists(directorio):
                continue

            archivos = os.listdir(directorio)

            for file in archivos:
                file_lower = file.lower()
                if not file_lower.endswith(('.png', '.jpg', '.jpeg')):
                    continue

                # Logo izquierdo (Redes Urbide)
                if not self.logo_izquierdo_path:
                    if file_lower in ["logo redes urbide.jpg", "logo redes urbide.png"]:
                        self.logo_izquierdo_path = os.path.join(directorio, file)

                # Logo derecho (Urbide)
                if not self.logo_derecho_path:
                    if file_lower in ["logo urbide.jpg", "logo urbide.png"]:
                        self.logo_derecho_path = os.path.join(directorio, file)

            if self.logo_izquierdo_path and self.logo_derecho_path:
                break

    def _configurar_estilos(self):
        """Configura los estilos del documento (similares a Access)"""
        self.styles = getSampleStyleSheet()

        # Estilo para título principal
        self.style_titulo = ParagraphStyle(
            'TituloPrincipal',
            parent=self.styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=20,
            textColor=colors.HexColor('#003366'),  # Azul oscuro (Access)
            alignment=TA_CENTER,
            spaceAfter=6,
            spaceBefore=0
        )

        # Estilo para subtítulo
        self.style_subtitulo = ParagraphStyle(
            'Subtitulo',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            textColor=colors.HexColor('#666666'),
            alignment=TA_LEFT,
            spaceAfter=3
        )

        # Estilo para información del proyecto
        self.style_proyecto = ParagraphStyle(
            'Proyecto',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11,
            textColor=colors.HexColor('#003366'),
            alignment=TA_LEFT,
            spaceAfter=6
        )

        # Estilo para fecha
        self.style_fecha = ParagraphStyle(
            'Fecha',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.HexColor('#666666'),
            alignment=TA_LEFT,
            spaceAfter=12
        )

        # Estilo para encabezados de grupo nivel 0
        self.style_grupo_nivel0 = ParagraphStyle(
            'GrupoNivel0',
            parent=self.styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=11,
            textColor=colors.white,
            alignment=TA_LEFT,
            leftIndent=6,
            spaceAfter=0,
            spaceBefore=0
        )

        # Estilo para encabezados de grupo nivel 1
        self.style_grupo_nivel1 = ParagraphStyle(
            'GrupoNivel1',
            parent=self.styles['Heading3'],
            fontName='Helvetica-Bold',
            fontSize=10,
            textColor=colors.white,
            alignment=TA_LEFT,
            leftIndent=12,
            spaceAfter=0,
            spaceBefore=0
        )

        # Estilo para encabezados de grupo nivel 2
        self.style_grupo_nivel2 = ParagraphStyle(
            'GrupoNivel2',
            parent=self.styles['Heading3'],
            fontName='Helvetica-Bold',
            fontSize=9,
            textColor=colors.white,
            alignment=TA_LEFT,
            leftIndent=18,
            spaceAfter=0,
            spaceBefore=0
        )

        # Estilo para pie de página
        self.style_pie = ParagraphStyle(
            'Pie',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            textColor=colors.HexColor('#999999'),
            alignment=TA_CENTER,
            spaceAfter=0
        )

        # Colores de fondo para grupos (estilo Access)
        self.color_grupo_nivel0 = colors.HexColor('#003366')  # Azul oscuro
        self.color_grupo_nivel1 = colors.HexColor('#4472C4')  # Azul medio
        self.color_grupo_nivel2 = colors.HexColor('#8FAADC')  # Azul claro

        # Colores para tabla
        self.color_header_tabla = colors.HexColor('#D9E2F3')  # Azul muy claro (Access)
        self.color_alternado = colors.HexColor('#F2F2F2')  # Gris claro para filas alternas
        self.color_subtotal = colors.HexColor('#E7E6E6')  # Gris para subtotales
        self.color_total = colors.HexColor('#C5D9F1')  # Azul claro para total

    def agregar_encabezado(self):
        """Agrega el encabezado del documento con logos y título"""
        # Calcular ancho disponible
        ancho_disponible = self.pagesize[0] - self.margen_izquierdo - self.margen_derecho

        # Crear tabla de encabezado con 3 columnas: logo izq | título | logo der
        header_data = []
        header_row = []

        # Altura deseada para logos (2 cm)
        altura_logo = 2.0 * cm

        # Logo izquierdo
        if self.logo_izquierdo_path and os.path.exists(self.logo_izquierdo_path):
            try:
                # Calcular ancho proporcional
                img = PILImage.open(self.logo_izquierdo_path)
                aspect_ratio = img.size[0] / img.size[1]
                ancho_logo = altura_logo * aspect_ratio
                logo_izq = Image(self.logo_izquierdo_path, width=ancho_logo, height=altura_logo)
                header_row.append(logo_izq)
            except:
                header_row.append('')
        else:
            header_row.append('')

        # Título en el centro
        titulo_para = Paragraph(f"<b>{self.titulo.upper()}</b>", self.style_titulo)
        header_row.append(titulo_para)

        # Logo derecho
        if self.logo_derecho_path and os.path.exists(self.logo_derecho_path):
            try:
                # Calcular ancho proporcional
                img = PILImage.open(self.logo_derecho_path)
                aspect_ratio = img.size[0] / img.size[1]
                ancho_logo = altura_logo * aspect_ratio
                logo_der = Image(self.logo_derecho_path, width=ancho_logo, height=altura_logo)
                header_row.append(logo_der)
            except:
                header_row.append('')
        else:
            header_row.append('')

        header_data.append(header_row)

        # Calcular anchos de columnas: 3.5cm | resto | 3.5cm
        ancho_logos = 3.5 * cm
        ancho_titulo = ancho_disponible - (2 * ancho_logos)

        header_table = Table(header_data, colWidths=[ancho_logos, ancho_titulo, ancho_logos])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),
            ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        self.elements.append(header_table)
        self.elements.append(Spacer(1, 0.3 * cm))

    def agregar_info_proyecto(self):
        """Agrega información del proyecto"""
        if self.proyecto_nombre:
            p_proyecto = Paragraph(f"<b>Proyecto:</b> {self.proyecto_nombre}", self.style_proyecto)
            self.elements.append(p_proyecto)

        if self.proyecto_codigo:
            p_codigo = Paragraph(f"<b>Código:</b> {self.proyecto_codigo}", self.style_subtitulo)
            self.elements.append(p_codigo)

        # Fecha
        p_fecha = Paragraph(f"<b>Fecha:</b> {self.fecha}", self.style_fecha)
        self.elements.append(p_fecha)

        self.elements.append(Spacer(1, 0.4 * cm))

    def crear_tabla_simple(
        self,
        columnas: List[str],
        datos: List[tuple],
        formatos_columnas: Optional[Dict[str, str]] = None
    ) -> Table:
        """
        Crea una tabla simple sin agrupaciones

        Args:
            columnas: Lista de nombres de columnas
            datos: Lista de tuplas con los datos
            formatos_columnas: Diccionario con formatos por columna ('moneda', 'decimal', 'fecha', etc.)

        Returns:
            Tabla configurada
        """
        if not formatos_columnas:
            formatos_columnas = {}

        # Calcular ancho disponible
        ancho_disponible = self.pagesize[0] - self.margen_izquierdo - self.margen_derecho

        # Calcular anchos de columnas (distribución equitativa)
        num_columnas = len(columnas)
        ancho_columna = ancho_disponible / num_columnas
        col_widths = [ancho_columna] * num_columnas

        # Preparar datos de la tabla
        tabla_datos = []

        # Encabezados
        tabla_datos.append(columnas)

        # Datos
        for fila in datos:
            fila_formateada = []
            for col_idx, valor in enumerate(fila):
                col_name = columnas[col_idx] if col_idx < len(columnas) else None
                formato = formatos_columnas.get(col_name, 'ninguno') if col_name else 'ninguno'

                # Formatear según tipo
                if valor is None:
                    fila_formateada.append('')
                elif isinstance(valor, (int, float)):
                    if formato == 'moneda':
                        fila_formateada.append(f"{valor:,.2f} €")
                    elif formato == 'decimal':
                        fila_formateada.append(f"{valor:,.2f}")
                    elif formato == 'porcentaje':
                        fila_formateada.append(f"{valor:.1f}%")
                    else:
                        fila_formateada.append(f"{valor:,.2f}")
                else:
                    fila_formateada.append(str(valor))

            tabla_datos.append(fila_formateada)

        # Crear tabla
        tabla = Table(tabla_datos, colWidths=col_widths, repeatRows=1)

        # Estilo de la tabla (estilo Access)
        estilo_tabla = [
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), self.color_header_tabla),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#003366')),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),

            # Datos
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('TOPPADDING', (0, 1), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 4),

            # Bordes (estilo Access - bordes sutiles)
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#666666')),

            # Alineación derecha para columnas numéricas
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]

        # Aplicar color alternado a filas (estilo Access)
        for i in range(1, len(tabla_datos)):
            if i % 2 == 0:
                estilo_tabla.append(
                    ('BACKGROUND', (0, i), (-1, i), self.color_alternado)
                )

        # Aplicar alineación derecha a columnas numéricas
        for col_idx, col_name in enumerate(columnas):
            formato = formatos_columnas.get(col_name, 'ninguno')
            if formato in ['moneda', 'decimal', 'porcentaje']:
                estilo_tabla.append(
                    ('ALIGN', (col_idx, 1), (col_idx, -1), 'RIGHT')
                )

        tabla.setStyle(TableStyle(estilo_tabla))

        return tabla

    def agregar_pie_pagina(self):
        """Agrega el pie de página"""
        self.elements.append(Spacer(1, 1 * cm))
        fecha_generacion = datetime.now().strftime('%d/%m/%Y a las %H:%M')
        p_pie = Paragraph(
            f"Generado el {fecha_generacion} | HydroFlow Manager v1.04",
            self.style_pie
        )
        self.elements.append(p_pie)

    def generar_pdf(self, filepath: str) -> bool:
        """
        Genera el archivo PDF

        Args:
            filepath: Ruta donde guardar el PDF

        Returns:
            True si se generó correctamente
        """
        try:
            doc = SimpleDocTemplate(
                filepath,
                pagesize=self.pagesize,
                topMargin=self.margen_superior,
                bottomMargin=self.margen_inferior,
                leftMargin=self.margen_izquierdo,
                rightMargin=self.margen_derecho
            )

            doc.build(self.elements)
            return True

        except Exception as e:
            print(f"Error al generar PDF: {e}")
            import traceback
            traceback.print_exc()
            return False
