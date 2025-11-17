# script/pdf_templates.py
"""
Sistema de Plantillas PDF con ReportLab
Generación de informes PDF con control total del diseño, similar a Access
"""

import os
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from decimal import Decimal
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, Image, PageBreak, KeepTogether, Frame, PageTemplate as RLPageTemplate
)
from reportlab.pdfgen import canvas
from PIL import Image as PILImage


class NumberedCanvas(canvas.Canvas):
    """Canvas personalizado con encabezado y pie de página en todas las páginas"""

    def __init__(self, *args, **kwargs):
        # Extraer parámetros personalizados
        self.pdf_template = kwargs.pop('pdf_template', None)
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """Agregar información de página en todas las páginas guardadas"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        """Dibuja encabezado y pie de página"""
        if not self.pdf_template:
            return

        # Obtener número de página actual
        page_num = self._pageNumber

        # Dibujar encabezado
        self.draw_header()

        # Dibujar pie de página con numeración
        self.draw_footer(page_num, page_count)

    def draw_header(self):
        """Dibuja el encabezado con logos y título usando tabla sin bordes"""
        if not self.pdf_template:
            return

        template = self.pdf_template
        ancho_pagina, alto_pagina = template.pagesize

        # Posición del encabezado (cerca del borde superior)
        y_pos = alto_pagina - template.margen_superior_encabezado - template.altura_encabezado

        # Importar clases necesarias
        from reportlab.lib.enums import TA_CENTER
        from reportlab.platypus import Paragraph, Table, TableStyle, Image as RLImage
        from reportlab.lib.styles import ParagraphStyle

        # Estilo para el título (reducido a 8pt para evitar rebase con textos largos)
        estilo_titulo_header = ParagraphStyle(
            'TituloHeader',
            fontName='Helvetica-Bold',
            fontSize=8,
            textColor=colors.HexColor('#003366'),
            alignment=TA_CENTER,
            leading=9,  # Espaciado entre líneas reducido
            wordWrap='CJK'  # Permitir word wrap mejorado
        )

        titulo = template.titulo.upper()

        # Preparar contenido de las 3 celdas del encabezado
        tabla_data = [[]]

        # Celda 1: Logo izquierdo (Redes Urbide)
        logo_izq_celda = ""
        if template.logo_izquierdo_path and os.path.exists(template.logo_izquierdo_path):
            try:
                # Crear objeto Image de ReportLab
                logo_izq_img = RLImage(template.logo_izquierdo_path,
                                       width=2.2*cm, height=2.0*cm)
                logo_izq_celda = logo_izq_img
            except:
                logo_izq_celda = ""
        tabla_data[0].append(logo_izq_celda)

        # Celda 2: Título (Paragraph con ajuste automático)
        p_titulo = Paragraph(f"<b>{titulo}</b>", estilo_titulo_header)
        tabla_data[0].append(p_titulo)

        # Celda 3: Logo derecho (Urbide)
        logo_der_celda = ""
        if template.logo_derecho_path and os.path.exists(template.logo_derecho_path):
            try:
                # Crear objeto Image de ReportLab
                logo_der_img = RLImage(template.logo_derecho_path,
                                       width=3.9*cm, height=1.5*cm)
                logo_der_celda = logo_der_img
            except:
                logo_der_celda = ""
        tabla_data[0].append(logo_der_celda)

        # Anchos de columnas: Logo izq (2.2cm) + Título (12.6cm) + Logo der (3.9cm) = 18.7cm
        # Dar más espacio al título para evitar rebase con textos largos
        col_widths = [2.2*cm, 12.6*cm, 3.9*cm]

        # Crear tabla
        tabla_header = Table(tabla_data, colWidths=col_widths, rowHeights=[template.altura_encabezado])

        # Estilo de tabla sin bordes visibles
        estilo_tabla_header = TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),    # Logo izquierdo centrado
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),    # Título centrado
            ('ALIGN', (2, 0), (2, 0), 'CENTER'),    # Logo derecho centrado
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),  # Alineación vertical al centro
            ('LEFTPADDING', (0, 0), (-1, 0), 0),
            ('RIGHTPADDING', (0, 0), (-1, 0), 0),
            ('TOPPADDING', (0, 0), (-1, 0), 0),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 0),
            # Sin bordes
            ('BOX', (0, 0), (-1, -1), 0, colors.white),
            ('GRID', (0, 0), (-1, -1), 0, colors.white),
        ])

        tabla_header.setStyle(estilo_tabla_header)

        # Dibujar la tabla en el canvas
        w, h = tabla_header.wrap(0, 0)
        x_tabla = template.margen_izquierdo
        tabla_header.drawOn(self, x_tabla, y_pos)

        # Línea separadora
        self.setStrokeColor(colors.HexColor('#CCCCCC'))
        self.setLineWidth(0.5)
        y_linea = y_pos - 0.2 * cm
        self.line(
            template.margen_izquierdo,
            y_linea,
            ancho_pagina - template.margen_derecho,
            y_linea
        )

    def draw_footer(self, page_num, page_count):
        """Dibuja el pie de página con numeración"""
        if not self.pdf_template:
            return

        template = self.pdf_template
        ancho_pagina, _ = template.pagesize

        # Posición del pie de página (cerca del borde inferior)
        y_pos = template.margen_inferior_pie + template.altura_pie

        # Línea separadora (por encima del texto del pie)
        self.setStrokeColor(colors.HexColor('#CCCCCC'))
        self.setLineWidth(0.5)
        y_linea = y_pos + template.altura_pie
        self.line(
            template.margen_izquierdo,
            y_linea,
            ancho_pagina - template.margen_derecho,
            y_linea
        )

        # Texto del pie de página
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#999999'))

        # Fecha del informe (izquierda) - usa la fecha introducida al generar, no la de generación
        texto_izq = f"Fecha: {template.fecha}"
        self.drawString(template.margen_izquierdo, y_pos, texto_izq)

        # Numeración de página (centro)
        texto_pag = f"Página {page_num} de {page_count}"
        ancho_texto = self.stringWidth(texto_pag, 'Helvetica', 8)
        x_centro = (ancho_pagina - ancho_texto) / 2
        self.drawString(x_centro, y_pos, texto_pag)

        # Nombre de la aplicación (derecha)
        texto_der = "HydroFlow Manager v1.04"
        ancho_texto_der = self.stringWidth(texto_der, 'Helvetica', 8)
        x_der = ancho_pagina - template.margen_derecho - ancho_texto_der
        self.drawString(x_der, y_pos, texto_der)


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

        # Márgenes para el contenido del documento
        self.margen_izquierdo = 1.5 * cm
        self.margen_derecho = 1.5 * cm

        # Márgenes superior e inferior ajustados para encabezado y pie de página
        # El encabezado se dibuja en el espacio del margen superior
        self.margen_superior_encabezado = 0.8 * cm  # Espacio desde el borde hasta el encabezado
        self.altura_encabezado = 2.0 * cm  # Altura del encabezado (logos)
        self.altura_logo_derecho = 1.0 * cm  # Altura específica para el logo derecho
        self.espacio_tras_encabezado = 0.7 * cm  # Espacio entre encabezado y contenido
        self.margen_superior = self.margen_superior_encabezado + self.altura_encabezado + self.espacio_tras_encabezado  # Total: ~3.5cm

        # Pie de página
        self.margen_inferior_pie = 0.8 * cm  # Espacio desde el borde hasta el pie
        self.altura_pie = 0.5 * cm  # Altura del pie de página
        self.espacio_antes_pie = 0.7 * cm  # Espacio entre contenido y pie
        self.margen_inferior = self.margen_inferior_pie + self.altura_pie + self.espacio_antes_pie  # Total: ~2cm

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
            fontSize=16,
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
            fontSize=12,
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
        """
        El encabezado ahora se dibuja automáticamente en todas las páginas mediante NumberedCanvas.
        Este método se mantiene por compatibilidad pero no hace nada.
        """
        # Ya no se necesita agregar elementos, el canvas lo dibuja automáticamente
        pass

    def agregar_info_proyecto(self, mostrar_fecha=True):
        """Agrega información del proyecto

        Args:
            mostrar_fecha: Si False, no muestra la fecha (útil para informes que no la necesitan)
        """
        if self.proyecto_nombre:
            p_proyecto = Paragraph(f"<b>Proyecto:</b> {self.proyecto_nombre}", self.style_proyecto)
            self.elements.append(p_proyecto)

        if self.proyecto_codigo:
            p_codigo = Paragraph(f"<b>Código:</b> {self.proyecto_codigo}", self.style_subtitulo)
            self.elements.append(p_codigo)

        # Fecha (opcional)
        if mostrar_fecha:
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

        # Anchos personalizados para informes de Recursos (en cm convertido a puntos: 1cm = 28.35 puntos)
        # A4 vertical: 21cm - 3cm márgenes = 18cm disponible
        # Total: 1.5 + 2.0 + 1.0 + 9.5 + 2.0 + 2.0 = 18.0 cm
        anchos_recursos = {
            'Código': 1.5 * 28.35,            # 1.5 cm
            'codigo': 1.5 * 28.35,
            'Cantidad': 2.0 * 28.35,          # 2.0 cm
            'cantidad': 2.0 * 28.35,
            'Ud.': 1.0 * 28.35,               # 1.0 cm
            'unidad': 1.0 * 28.35,
            'Recurso / Material': 9.5 * 28.35,  # 9.5 cm
            'resumen': 9.5 * 28.35,
            'Precio unitario': 2.0 * 28.35,  # 2.0 cm
            'coste': 2.0 * 28.35,
            'Importe': 2.0 * 28.35,           # 2.0 cm
            'coste_total': 2.0 * 28.35
        }

        # Calcular anchos de columnas
        col_widths = []
        usa_anchos_personalizados = all(col in anchos_recursos for col in columnas)

        if usa_anchos_personalizados:
            # Usar anchos personalizados para informes de Recursos
            for col in columnas:
                col_widths.append(anchos_recursos[col])
        else:
            # Distribución equitativa para otros informes
            num_columnas = len(columnas)
            ancho_columna = ancho_disponible / num_columnas
            col_widths = [ancho_columna] * num_columnas

        # Estilo para celdas de datos (texto multilínea)
        estilo_celda = ParagraphStyle(
            'CeldaDatos',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            alignment=TA_LEFT,
            leading=11  # Espaciado entre líneas
        )

        # Estilo para celdas numéricas (alineadas a la derecha)
        estilo_celda_derecha = ParagraphStyle(
            'CeldaDatosDerecha',
            parent=estilo_celda,
            alignment=TA_RIGHT
        )

        # Preparar datos de la tabla
        tabla_datos = []

        # Encabezados (como Paragraph para permitir texto multilínea)
        encabezados_para = []
        estilo_encabezado = ParagraphStyle(
            'EncabezadoTabla',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#003366'),
            leading=12
        )
        for col_name in columnas:
            encabezados_para.append(Paragraph(f"<b>{col_name}</b>", estilo_encabezado))
        tabla_datos.append(encabezados_para)

        # Datos (como Paragraph para permitir texto multilínea y ajuste automático de altura)
        for fila in datos:
            fila_formateada = []
            for col_idx, valor in enumerate(fila):
                col_name = columnas[col_idx] if col_idx < len(columnas) else None
                formato = formatos_columnas.get(col_name, 'ninguno') if col_name else 'ninguno'

                # DEBUG: Imprimir nombres de columnas para verificar
                if col_idx == 0 and datos.index(fila) == 0:
                    print(f"DEBUG PDF - Columnas disponibles: {columnas}")
                    print(f"DEBUG PDF - Formatos: {formatos_columnas}")

                # DEBUG: Imprimir valor y tipo para la primera fila
                if datos.index(fila) == 0:
                    print(f"DEBUG PDF - Col '{col_name}': valor={valor}, tipo={type(valor).__name__}, formato={formato}")

                # Formatear según tipo
                texto_celda = ''
                usar_estilo_derecha = False

                if valor is None:
                    texto_celda = ''
                elif isinstance(valor, (int, float, Decimal)):
                    # Convertir Decimal a float para poder formatear
                    if isinstance(valor, Decimal):
                        valor = float(valor)

                    # Verificar si es coordenada geográfica (latitud/longitud)
                    # Hacer la búsqueda más robusta - case insensitive
                    es_coordenada = False
                    if col_name:
                        col_lower = col_name.lower()
                        es_coordenada = 'latitud' in col_lower or 'longitud' in col_lower or 'latitude' in col_lower or 'longitude' in col_lower

                    # DEBUG para ver si detecta coordenadas
                    if es_coordenada and datos.index(fila) == 0:
                        print(f"DEBUG PDF - Coordenada detectada: {col_name} = {valor}")

                    usar_estilo_derecha = True
                    if formato == 'moneda':
                        # Formato moneda: 2 decimales + símbolo €, formato español (1.234,56 €)
                        texto_celda = f"{valor:,.2f} €".replace(',', 'X').replace('.', ',').replace('X', '.')
                    elif es_coordenada:
                        # Coordenadas geográficas: 4 decimales, formato español (1,2345)
                        texto_celda = f"{valor:.4f}".replace('.', ',')
                    elif formato == 'decimal':
                        # Formato decimal: 2 decimales, formato español (1.234,56)
                        texto_celda = f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                    elif formato == 'porcentaje':
                        # Formato porcentaje: 2 decimales, formato español (12,34%)
                        texto_celda = f"{valor:.2f}%".replace('.', ',')
                    else:
                        # Por defecto: 2 decimales, formato español (1.234,56)
                        texto_celda = f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                else:
                    texto_celda = str(valor)

                # Crear Paragraph con el estilo apropiado
                estilo_a_usar = estilo_celda_derecha if usar_estilo_derecha else estilo_celda
                fila_formateada.append(Paragraph(texto_celda, estilo_a_usar))

            tabla_datos.append(fila_formateada)

        # Crear tabla con altura de fila dinámica (None permite que se ajuste al contenido)
        tabla = Table(tabla_datos, colWidths=col_widths, repeatRows=1)

        # Estilo de la tabla (estilo Access)
        estilo_tabla = [
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), self.color_header_tabla),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),

            # Datos
            ('TOPPADDING', (0, 1), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),

            # Bordes (estilo Access - bordes sutiles)
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#666666')),

            # Alineación vertical
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]

        # Aplicar color alternado a filas (estilo Access)
        for i in range(1, len(tabla_datos)):
            if i % 2 == 0:
                estilo_tabla.append(
                    ('BACKGROUND', (0, i), (-1, i), self.color_alternado)
                )

        tabla.setStyle(TableStyle(estilo_tabla))

        return tabla

    def crear_tabla_totales_finales(
        self,
        total_ejecucion_material: float,
        columnas: List[str],
        porcentaje_gg: float = 8.0,
        porcentaje_bi: float = 3.0
    ) -> Table:
        """
        Crea tabla con totales finales incluyendo Gastos Generales y Beneficio Industrial

        Args:
            total_ejecucion_material: Total de ejecución material
            columnas: Lista de nombres de columnas (para calcular anchos)
            porcentaje_gg: Porcentaje de Gastos Generales (por defecto 8%)
            porcentaje_bi: Porcentaje de Beneficio Industrial (por defecto 3%)

        Returns:
            Tabla con totales finales
        """
        from reportlab.lib.units import cm
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_RIGHT, TA_LEFT

        # Calcular ancho disponible
        ancho_disponible = self.pagesize[0] - self.margen_izquierdo - self.margen_derecho

        # Anchos personalizados para informes de Recursos
        anchos_recursos = {
            'Código': 1.5 * cm,
            'Cantidad': 2.0 * cm,
            'Ud.': 1.0 * cm,
            'Recurso / Material': 9.5 * cm,
            'Precio unitario': 2.0 * cm,
            'Importe': 2.0 * cm
        }

        # Usar anchos personalizados si coinciden con columnas de Recursos
        usa_anchos_personalizados = all(col in anchos_recursos for col in columnas)

        if usa_anchos_personalizados:
            # Para que entre "TOTAL EJECUCIÓN MATERIAL" sin problemas
            # Usar casi todo el ancho para texto, dejando espacio suficiente para importes
            ancho_texto = 14 * cm  # Ancho generoso para textos largos
            ancho_valor = 4 * cm   # Suficiente para importes con formato español
        else:
            ancho_texto = ancho_disponible * 0.75
            ancho_valor = ancho_disponible * 0.25

        # Calcular valores
        gastos_generales = total_ejecucion_material * (porcentaje_gg / 100.0)
        beneficio_industrial = total_ejecucion_material * (porcentaje_bi / 100.0)
        total_final = total_ejecucion_material + gastos_generales + beneficio_industrial

        # Formato moneda español
        def formato_moneda(valor):
            return f"{valor:,.2f} €".replace(',', 'X').replace('.', ',').replace('X', '.')

        # Estilo para texto
        estilo_texto = ParagraphStyle(
            'TotalesTexto',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            alignment=TA_RIGHT,
            leading=12
        )

        # Estilo para valores
        estilo_valor = ParagraphStyle(
            'TotalesValor',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            alignment=TA_RIGHT,
            leading=12
        )

        # Estilo para total final (más destacado)
        estilo_total_final = ParagraphStyle(
            'TotalFinal',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11,
            alignment=TA_RIGHT,
            leading=13
        )

        # Crear filas de datos
        tabla_datos = [
            [Paragraph("TOTAL EJECUCIÓN MATERIAL", estilo_texto), Paragraph(formato_moneda(total_ejecucion_material), estilo_valor)],
            [Paragraph(f"Gastos generales ({porcentaje_gg:.0f}%)", estilo_texto), Paragraph(formato_moneda(gastos_generales), estilo_valor)],
            [Paragraph(f"Beneficio Industrial ({porcentaje_bi:.0f}%)", estilo_texto), Paragraph(formato_moneda(beneficio_industrial), estilo_valor)],
            [Paragraph("TOTAL", estilo_total_final), Paragraph(formato_moneda(total_final), estilo_total_final)]
        ]

        # Crear tabla
        tabla = Table(tabla_datos, colWidths=[ancho_texto, ancho_valor])

        # Estilo de la tabla
        estilo_tabla = [
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            # Línea encima de TOTAL
            ('LINEABOVE', (0, 3), (-1, 3), 2, colors.black),

            # Fondo para la fila final
            ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#F0F0F0')),
        ]

        tabla.setStyle(TableStyle(estilo_tabla))

        return tabla

    def agregar_pie_pagina(self):
        """
        El pie de página ahora se dibuja automáticamente en todas las páginas mediante NumberedCanvas.
        Este método se mantiene por compatibilidad pero no hace nada.
        """
        # Ya no se necesita agregar elementos, el canvas lo dibuja automáticamente
        pass

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

            # Función para crear canvas personalizado con encabezado y pie de página
            def crear_canvas(filename, **kwargs):
                return NumberedCanvas(filename, pdf_template=self, **kwargs)

            # Construir el PDF usando el canvas personalizado
            doc.build(self.elements, canvasmaker=crear_canvas)
            return True

        except Exception as e:
            print(f"Error al generar PDF: {e}")
            import traceback
            traceback.print_exc()
            return False
