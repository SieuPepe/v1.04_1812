# script/pdf_agrupaciones.py
"""
Sistema de Agrupaciones Dinámicas para PDFs
Manejo de tablas con agrupaciones multinivel (similar a Access)
"""

from typing import List, Dict, Any, Optional
from decimal import Decimal
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, KeepTogether
from script.pdf_templates import PDFTemplate


class PDFAgrupaciones(PDFTemplate):
    """Plantilla PDF con soporte para agrupaciones dinámicas"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def crear_tabla_agrupada(
        self,
        columnas: List[str],
        datos: List[tuple],
        resultado_agrupacion: Dict,
        modo: str = 'detalle'
    ) -> List:
        """
        Crea tabla con agrupaciones dinámicas

        Args:
            columnas: Lista de nombres de columnas
            datos: Datos originales (no se usan directamente con agrupaciones)
            resultado_agrupacion: Diccionario con estructura de agrupaciones
            modo: 'detalle' o 'resumen'

        Returns:
            Lista de elementos (tablas y espaciadores)
        """
        elementos = []

        formatos_columnas = resultado_agrupacion.get('formatos_columnas', {})
        formatos_agregaciones = resultado_agrupacion.get('formatos_agregaciones', {})
        grupos = resultado_agrupacion.get('grupos', [])

        if not grupos:
            # Sin agrupaciones, crear tabla simple
            tabla = self.crear_tabla_simple(columnas, datos, formatos_columnas)
            elementos.append(tabla)
        else:
            # Crear tablas para cada grupo
            elementos_grupos = self._procesar_grupos(
                grupos,
                columnas,
                formatos_columnas,
                formatos_agregaciones,
                modo
            )
            elementos.extend(elementos_grupos)

            # Totales generales
            totales_generales = resultado_agrupacion.get('totales_generales', {})
            if totales_generales:
                elementos.append(Spacer(1, 0.5 * cm))
                tabla_totales = self._crear_tabla_totales_generales(
                    totales_generales,
                    columnas,
                    formatos_agregaciones
                )
                elementos.append(tabla_totales)

        return elementos

    def _procesar_grupos(
        self,
        grupos: List[Dict],
        columnas: List[str],
        formatos_columnas: Dict[str, str],
        formatos_agregaciones: Dict[str, str],
        modo: str,
        nivel: int = 0
    ) -> List:
        """
        Procesa grupos de forma recursiva

        Args:
            grupos: Lista de grupos a procesar
            columnas: Nombres de columnas
            formatos_columnas: Formatos por columna
            formatos_agregaciones: Formatos por agregación
            modo: 'detalle' o 'resumen'
            nivel: Nivel actual de agrupación (0, 1, 2)

        Returns:
            Lista de elementos del PDF
        """
        elementos = []

        for grupo in grupos:
            campo = grupo.get('campo', '')
            clave = grupo.get('clave', '')
            datos = grupo.get('datos', [])
            subtotales = grupo.get('subtotales', {})
            subgrupos = grupo.get('subgrupos')

            # Crear encabezado del grupo
            elementos_grupo = []

            # Título del grupo
            tabla_titulo_grupo = self._crear_titulo_grupo(campo, clave, nivel)
            elementos_grupo.append(tabla_titulo_grupo)
            elementos_grupo.append(Spacer(1, 0.15 * cm))

            # Si hay subgrupos, procesarlos recursivamente
            if subgrupos:
                elementos_subgrupos = self._procesar_grupos(
                    subgrupos,
                    columnas,
                    formatos_columnas,
                    formatos_agregaciones,
                    modo,
                    nivel + 1
                )
                elementos_grupo.extend(elementos_subgrupos)

            # Si es modo detalle y hay datos, mostrar tabla de datos
            elif modo == 'detalle' and datos:
                tabla_datos = self._crear_tabla_datos_grupo(
                    columnas,
                    datos,
                    formatos_columnas
                )
                elementos_grupo.append(tabla_datos)
                elementos_grupo.append(Spacer(1, 0.1 * cm))

            # Subtotales del grupo
            if subtotales:
                tabla_subtotales = self._crear_tabla_subtotales(
                    subtotales,
                    columnas,
                    formatos_agregaciones,
                    nivel
                )
                elementos_grupo.append(tabla_subtotales)
                elementos_grupo.append(Spacer(1, 0.2 * cm))

            # Usar KeepTogether para evitar que el grupo se divida entre páginas
            # (solo para grupos pequeños)
            if len(elementos_grupo) <= 5:
                elementos.append(KeepTogether(elementos_grupo))
            else:
                elementos.extend(elementos_grupo)

            elementos.append(Spacer(1, 0.3 * cm))

        return elementos

    def _crear_titulo_grupo(self, campo: str, clave: str, nivel: int) -> Table:
        """
        Crea tabla con título del grupo

        Args:
            campo: Nombre del campo de agrupación
            clave: Valor de la agrupación
            nivel: Nivel de agrupación (0, 1, 2)

        Returns:
            Tabla con el título
        """
        # Seleccionar estilo y color según nivel
        if nivel == 0:
            estilo = self.style_grupo_nivel0
            color_fondo = self.color_grupo_nivel0
        elif nivel == 1:
            estilo = self.style_grupo_nivel1
            color_fondo = self.color_grupo_nivel1
        else:
            estilo = self.style_grupo_nivel2
            color_fondo = self.color_grupo_nivel2

        # Crear indentación visual
        indent = "  " * nivel
        icono = "📁" if nivel == 0 else "📂" if nivel == 1 else "📄"
        texto = f"{indent}{icono} {campo.upper()}: {clave}"

        # Crear párrafo con el texto
        p_titulo = Paragraph(texto, estilo)

        # Calcular ancho disponible
        ancho_disponible = self.pagesize[0] - self.margen_izquierdo - self.margen_derecho

        # Crear tabla de una celda para el título
        tabla_titulo = Table([[p_titulo]], colWidths=[ancho_disponible])
        tabla_titulo.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), color_fondo),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8 + (nivel * 6)),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6 - nivel),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6 - nivel),
            ('BOX', (0, 0), (-1, -1), 1, color_fondo.clone(alpha=0.8)),
        ]))

        return tabla_titulo

    def _crear_tabla_datos_grupo(
        self,
        columnas: List[str],
        datos: List[tuple],
        formatos_columnas: Dict[str, str]
    ) -> Table:
        """
        Crea tabla con los datos de un grupo

        Args:
            columnas: Nombres de columnas
            datos: Datos del grupo
            formatos_columnas: Formatos por columna

        Returns:
            Tabla con los datos
        """
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER

        # Calcular ancho disponible
        ancho_disponible = self.pagesize[0] - self.margen_izquierdo - self.margen_derecho

        # Anchos personalizados para informes de Recursos (igual que en pdf_templates.py)
        anchos_recursos = {
            'Código': 1.5 * cm,
            'codigo': 1.5 * cm,
            'Cantidad': 2.0 * cm,
            'cantidad': 2.0 * cm,
            'Ud.': 1.0 * cm,
            'unidad': 1.0 * cm,
            'Recurso / Material': 9.5 * cm,
            'resumen': 9.5 * cm,
            'Precio unitario': 2.0 * cm,
            'coste': 2.0 * cm,
            'Importe': 2.0 * cm,
            'coste_total': 2.0 * cm
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
            'CeldaDatosGrupo',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            alignment=TA_LEFT,
            leading=10
        )

        # Estilo para celdas numéricas (alineadas a la derecha)
        estilo_celda_derecha = ParagraphStyle(
            'CeldaDatosGrupoDerecha',
            parent=estilo_celda,
            alignment=TA_RIGHT
        )

        # Estilo para encabezados
        estilo_encabezado = ParagraphStyle(
            'EncabezadoGrupo',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#003366'),
            leading=11
        )

        # Preparar datos
        tabla_datos = []

        # Encabezados (como Paragraph)
        encabezados_para = []
        for col_name in columnas:
            encabezados_para.append(Paragraph(f"<b>{col_name}</b>", estilo_encabezado))
        tabla_datos.append(encabezados_para)

        # Datos (como Paragraph para texto multilínea)
        for fila in datos:
            fila_formateada = []
            for col_idx, valor in enumerate(fila):
                col_name = columnas[col_idx] if col_idx < len(columnas) else None
                formato = formatos_columnas.get(col_name, 'ninguno') if col_name else 'ninguno'

                # Formatear
                texto_celda = ''
                usar_estilo_derecha = False

                if valor is None:
                    texto_celda = ''
                elif isinstance(valor, (int, float, Decimal)):
                    # Convertir Decimal a float para poder formatear
                    if isinstance(valor, Decimal):
                        valor = float(valor)

                    # Verificar si es coordenada geográfica (latitud/longitud) - case insensitive
                    es_coordenada = False
                    if col_name:
                        col_lower = col_name.lower()
                        es_coordenada = 'latitud' in col_lower or 'longitud' in col_lower or 'latitude' in col_lower or 'longitude' in col_lower

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

                # Crear Paragraph
                estilo_a_usar = estilo_celda_derecha if usar_estilo_derecha else estilo_celda
                fila_formateada.append(Paragraph(texto_celda, estilo_a_usar))

            tabla_datos.append(fila_formateada)

        # Crear tabla
        tabla = Table(tabla_datos, colWidths=col_widths, repeatRows=1)

        # Estilo
        estilo_tabla = [
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), self.color_header_tabla),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),

            # Datos
            ('TOPPADDING', (0, 1), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),

            # Bordes
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#666666')),

            # Alineación vertical
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]

        # Color alternado
        for i in range(1, len(tabla_datos)):
            if i % 2 == 0:
                estilo_tabla.append(
                    ('BACKGROUND', (0, i), (-1, i), self.color_alternado)
                )

        tabla.setStyle(TableStyle(estilo_tabla))

        return tabla

    def _crear_tabla_subtotales(
        self,
        subtotales: Dict[str, Any],
        columnas: List[str],
        formatos_agregaciones: Dict[str, str],
        nivel: int
    ) -> Table:
        """
        Crea tabla con subtotales

        Args:
            subtotales: Diccionario con subtotales
            columnas: Nombres de columnas
            formatos_agregaciones: Formatos por agregación
            nivel: Nivel del grupo

        Returns:
            Tabla con subtotales
        """
        # Calcular ancho disponible
        ancho_disponible = self.pagesize[0] - self.margen_izquierdo - self.margen_derecho

        # Anchos personalizados para informes de Recursos (igual que en pdf_templates.py)
        anchos_recursos = {
            'Código': 1.5 * cm,
            'codigo': 1.5 * cm,
            'Cantidad': 2.0 * cm,
            'cantidad': 2.0 * cm,
            'Ud.': 1.0 * cm,
            'unidad': 1.0 * cm,
            'Recurso / Material': 9.5 * cm,
            'resumen': 9.5 * cm,
            'Precio unitario': 2.0 * cm,
            'coste': 2.0 * cm,
            'Importe': 2.0 * cm,
            'coste_total': 2.0 * cm
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

        # Crear fila de subtotales
        fila_subtotal = [''] * len(columnas)

        # Texto en primera columna
        indent = "  " * (nivel + 1)
        fila_subtotal[0] = f"{indent}▸ Subtotal"

        # Mapear subtotales a las columnas correctas
        for key, valor in subtotales.items():
            # Extraer nombre del campo (ej: "SUM(presupuesto)" -> "presupuesto")
            if '(' in key and ')' in key:
                campo_nombre = key.split('(')[1].rstrip(')')
            else:
                campo_nombre = key

            # Determinar formato
            formato = formatos_agregaciones.get(key, 'ninguno')

            # Formatear valor
            if isinstance(valor, (int, float, Decimal)):
                # Convertir Decimal a float para poder formatear
                if isinstance(valor, Decimal):
                    valor = float(valor)

                if formato == 'moneda':
                    # Formato moneda: 2 decimales + símbolo €
                    valor_formateado = f"{valor:,.2f} €".replace(',', 'X').replace('.', ',').replace('X', '.')
                elif formato == 'decimal':
                    # Formato decimal: 2 decimales
                    valor_formateado = f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                elif formato == 'entero':
                    valor_formateado = f"{int(valor):,}".replace(',', '.')
                else:
                    # Por defecto: 2 decimales
                    valor_formateado = f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            else:
                valor_formateado = str(valor)

            # Buscar columna correspondiente
            if campo_nombre in columnas:
                col_idx = columnas.index(campo_nombre)
                fila_subtotal[col_idx] = valor_formateado
            elif campo_nombre == '*':
                # COUNT(*) va en la segunda columna
                fila_subtotal[1] = valor_formateado

        # Crear tabla
        tabla_subtotal = Table([fila_subtotal], colWidths=col_widths)

        # Estilo
        estilo = [
            ('BACKGROUND', (0, 0), (-1, -1), self.color_subtotal),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#999999')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]

        # Alineación derecha para columnas numéricas (todas excepto la primera)
        for col_idx in range(1, num_columnas):
            if fila_subtotal[col_idx]:  # Solo si hay valor
                estilo.append(
                    ('ALIGN', (col_idx, 0), (col_idx, 0), 'RIGHT')
                )

        tabla_subtotal.setStyle(TableStyle(estilo))

        return tabla_subtotal

    def _crear_tabla_totales_generales(
        self,
        totales: Dict[str, Any],
        columnas: List[str],
        formatos_agregaciones: Dict[str, str]
    ) -> Table:
        """
        Crea tabla con totales generales

        Args:
            totales: Diccionario con totales
            columnas: Nombres de columnas
            formatos_agregaciones: Formatos por agregación

        Returns:
            Tabla con totales
        """
        # Calcular ancho disponible
        ancho_disponible = self.pagesize[0] - self.margen_izquierdo - self.margen_derecho

        # Anchos personalizados para informes de Recursos (igual que en pdf_templates.py)
        anchos_recursos = {
            'Código': 1.5 * cm,
            'codigo': 1.5 * cm,
            'Cantidad': 2.0 * cm,
            'cantidad': 2.0 * cm,
            'Ud.': 1.0 * cm,
            'unidad': 1.0 * cm,
            'Recurso / Material': 9.5 * cm,
            'resumen': 9.5 * cm,
            'Precio unitario': 2.0 * cm,
            'coste': 2.0 * cm,
            'Importe': 2.0 * cm,
            'coste_total': 2.0 * cm
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

        # Crear fila de totales
        fila_total = [''] * len(columnas)
        fila_total[0] = "═══ TOTAL GENERAL ═══"

        # Mapear totales a columnas
        for key, valor in totales.items():
            # Extraer nombre del campo
            if '(' in key and ')' in key:
                campo_nombre = key.split('(')[1].rstrip(')')
            else:
                campo_nombre = key

            # Determinar formato
            formato = formatos_agregaciones.get(key, 'ninguno')

            # Formatear valor
            if isinstance(valor, (int, float, Decimal)):
                # Convertir Decimal a float para poder formatear
                if isinstance(valor, Decimal):
                    valor = float(valor)

                if formato == 'moneda':
                    # Formato moneda: 2 decimales + símbolo €
                    valor_formateado = f"{valor:,.2f} €".replace(',', 'X').replace('.', ',').replace('X', '.')
                elif formato == 'decimal':
                    # Formato decimal: 2 decimales
                    valor_formateado = f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                elif formato == 'entero':
                    valor_formateado = f"{int(valor):,}".replace(',', '.')
                else:
                    # Por defecto: 2 decimales
                    valor_formateado = f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            else:
                valor_formateado = str(valor)

            # Buscar columna
            if campo_nombre in columnas:
                col_idx = columnas.index(campo_nombre)
                fila_total[col_idx] = valor_formateado
            elif campo_nombre == '*':
                fila_total[1] = valor_formateado

        # Crear tabla
        tabla_total = Table([fila_total], colWidths=col_widths)

        # Estilo (más destacado que subtotales)
        estilo = [
            ('BACKGROUND', (0, 0), (-1, -1), self.color_total),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#003366')),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#003366')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]

        # Alineación derecha para columnas numéricas
        for col_idx in range(1, num_columnas):
            if fila_total[col_idx]:
                estilo.append(
                    ('ALIGN', (col_idx, 0), (col_idx, 0), 'RIGHT')
                )

        tabla_total.setStyle(TableStyle(estilo))

        return tabla_total
