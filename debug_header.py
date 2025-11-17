#!/usr/bin/env python3
"""
Script de debug para verificar las dimensiones del encabezado PDF
"""

print("=" * 60)
print("DEBUG: Dimensiones del encabezado PDF")
print("=" * 60)

# Especificación original (commit 79b6d76)
print("\n📋 ESPECIFICACIÓN ORIGINAL:")
print(f"  Margen izquierdo: 0-1.5cm = 1.5cm")
print(f"  Logo izquierdo: 1.5-4.0cm = 2.5cm (imagen: 2.2cm x 2.0cm)")
print(f"  Título: 4.0-15.5cm = 11.5cm")
print(f"  Logo derecho: 15.5-19.5cm = 4.0cm (imagen: 3.9cm x 1.5cm)")
print(f"  Margen derecho: 19.5-21.0cm = 1.5cm")
print(f"  TOTAL: 21cm (ancho A4 vertical) ✓")

# Código actual (después de rediseño con tabla)
print("\n🔧 CÓDIGO ACTUAL (tabla):")
logo_izq_ancho = 2.2
titulo_ancho = 12.6
logo_der_ancho = 3.9
total_tabla = logo_izq_ancho + titulo_ancho + logo_der_ancho

print(f"  Logo izquierdo: {logo_izq_ancho}cm")
print(f"  Título: {titulo_ancho}cm")
print(f"  Logo derecho: {logo_der_ancho}cm")
print(f"  TOTAL tabla: {total_tabla}cm")

margen_izq = 1.5
margen_der = 1.5
espacio_usado = margen_izq + total_tabla + margen_der

print(f"  Con márgenes: {margen_izq}cm + {total_tabla}cm + {margen_der}cm = {espacio_usado}cm")

# Problemas detectados
print("\n❌ PROBLEMAS DETECTADOS:")
print(f"  1. Título aumentó de 11.5cm a 12.6cm (+{titulo_ancho - 11.5:.1f}cm)")
print(f"  2. Logo izquierdo tiene 2.2cm pero espacio asignado debería ser 2.5cm")
print(f"  3. Logo derecho tiene 3.9cm pero espacio asignado debería ser 4.0cm")
print(f"  4. Total tabla {total_tabla}cm vs especificación {2.5 + 11.5 + 4.0}cm")

# Solución propuesta
print("\n✅ SOLUCIÓN PROPUESTA:")
logo_izq_col = 2.5
titulo_col = 11.5
logo_der_col = 4.0
total_correcto = logo_izq_col + titulo_col + logo_der_col

print(f"  Logo izquierdo columna: {logo_izq_col}cm (imagen: 2.2cm x 2.0cm, centrada)")
print(f"  Título columna: {titulo_col}cm (reducir de 12.6cm)")
print(f"  Logo derecho columna: {logo_der_col}cm (imagen: max 3.5cm x 1.2cm, reducir tamaño)")
print(f"  TOTAL tabla: {total_correcto}cm")
print(f"  Con márgenes: {margen_izq}cm + {total_correcto}cm + {margen_der}cm = {margen_izq + total_correcto + margen_der}cm ✓")

print("\n📝 AJUSTES NECESARIOS:")
print("  1. Cambiar col_widths de [2.2cm, 12.6cm, 3.9cm] a [2.5cm, 11.5cm, 4.0cm]")
print("  2. Reducir tamaño del logo derecho de (3.9cm x 1.5cm) a (~3.5cm x 1.2cm)")
print("  3. Reducir fontSize del título de 8pt a 7pt si es necesario")
print("  4. Aumentar leading a 8pt para mejor espaciado")

print("\n" + "=" * 60)
