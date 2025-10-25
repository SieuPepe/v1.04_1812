# 📋 ESPECIFICACIONES TÉCNICAS: MEJORAS UI/UX HYDROFLOW MANAGER

## 🎯 OBJETIVO
Transformar la interfaz actual a un nivel profesional equivalente a software empresarial (Autodesk, Microsoft, Adobe) manteniendo la funcionalidad y estructura existente.

---

## 🎨 1. PALETA DE COLORES PROFESIONAL

### Colores Actuales vs. Nuevos

```python
# ❌ COLORES ACTUALES (Eliminar)
SIDEBAR_BG = "#2d3748"
BUTTON_PRIMARY = "#48bb78"  # Verde muy brillante
BUTTON_SECONDARY = "#4299e1"  # Azul muy brillante
TABLE_HEADER = "#4299e1"  # Azul brillante
MAIN_BG = "#2d3748"  # Gris oscuro

# ✅ NUEVOS COLORES (Implementar)
# Paleta basada en Slate + Blue profesional

# Fondos y Superficies
COLOR_BG_PRIMARY = "#f8fafc"      # Fondo principal (Slate 50)
COLOR_BG_SECONDARY = "#ffffff"    # Tarjetas y modales
COLOR_BG_SIDEBAR = "#1e293b"      # Sidebar (Slate 800)
COLOR_BG_SIDEBAR_HOVER = "#334155"  # Hover items sidebar (Slate 700)

# Texto
COLOR_TEXT_PRIMARY = "#1e293b"    # Texto principal (Slate 800)
COLOR_TEXT_SECONDARY = "#64748b"  # Texto secundario (Slate 500)
COLOR_TEXT_MUTED = "#94a3b8"      # Texto deshabilitado (Slate 400)
COLOR_TEXT_INVERSE = "#f8fafc"    # Texto sobre fondos oscuros

# Botones y Acciones
COLOR_PRIMARY = "#3b82f6"         # Azul primario (Blue 500)
COLOR_PRIMARY_HOVER = "#2563eb"   # Hover azul (Blue 600)
COLOR_PRIMARY_ACTIVE = "#1d4ed8"  # Active azul (Blue 700)

COLOR_SUCCESS = "#10b981"         # Verde éxito (Emerald 500)
COLOR_SUCCESS_HOVER = "#059669"   # Hover verde

COLOR_DANGER = "#ef4444"          # Rojo eliminar (Red 500)
COLOR_DANGER_HOVER = "#dc2626"    # Hover rojo

# Bordes y Separadores
COLOR_BORDER_LIGHT = "#e2e8f0"    # Bordes sutiles (Slate 200)
COLOR_BORDER_DEFAULT = "#cbd5e1"  # Bordes inputs (Slate 300)
COLOR_BORDER_HOVER = "#94a3b8"    # Bordes hover (Slate 400)

# Estados y Badges
COLOR_STATUS_PENDING = "#fbbf24"  # Amarillo pendiente
COLOR_STATUS_ACTIVE = "#10b981"   # Verde activo
COLOR_STATUS_COMPLETE = "#6366f1" # Índigo completado
COLOR_STATUS_ERROR = "#ef4444"    # Rojo error

# Sombras (para CTkButton y CTkFrame)
SHADOW_SM = "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
SHADOW_MD = "0 1px 3px 0 rgba(0, 0, 0, 0.1)"
SHADOW_LG = "0 4px 6px -1px rgba(0, 0, 0, 0.1)"
SHADOW_XL = "0 10px 15px -3px rgba(0, 0, 0, 0.1)"
```

---

## 🔲 2. SIDEBAR (MENÚ LATERAL)

### Cambios Específicos

```python
# ❌ IMPLEMENTACIÓN ACTUAL
sidebar_frame = ctk.CTkFrame(master=root, fg_color="#2d3748")
menu_item = ctk.CTkButton(
    master=sidebar_frame,
    text="Resumen",
    fg_color="#4299e1",  # Fondo azul brillante cuando activo
    hover_color="#4a5568"
)

# ✅ NUEVA IMPLEMENTACIÓN
sidebar_frame = ctk.CTkFrame(
    master=root,
    fg_color="#1e293b",
    border_width=0,
    corner_radius=0
)

# Items del menú con borde lateral en lugar de fondo completo
menu_item = ctk.CTkButton(
    master=sidebar_frame,
    text="  Resumen",  # Espaciado izquierdo para simular padding
    fg_color="transparent",
    hover_color="#334155",
    text_color="#94a3b8",
    font=("Segoe UI", 14),
    height=40,
    anchor="w",
    border_width=0,
    border_spacing=0
)

# Para item ACTIVO: agregar un indicador visual
# Opción 1: Frame delgado a la izquierda (3px)
indicator = ctk.CTkFrame(
    master=menu_item,
    width=3,
    fg_color="#3b82f6",
    corner_radius=0
)
indicator.place(relx=0, rely=0, relheight=1)

# Cambiar colores del item activo
menu_item.configure(
    fg_color="#334155",
    text_color="#ffffff"
)
```

### Especificaciones del Sidebar

- **Ancho:** 240px (mantener)
- **Color de fondo:** `#1e293b`
- **Borde derecho:** 1px sólido `#334155`
- **Items del menú:**
  - Alto: 40px
  - Padding interno: 12px izquierda, 20px derecha
  - Fuente: Segoe UI, 14px
  - Color texto normal: `#94a3b8`
  - Color texto hover: `#e2e8f0`
  - Color texto activo: `#ffffff`
  - Fondo normal: transparente
  - Fondo hover: `#334155`
  - Fondo activo: `#334155` + borde izquierdo 3px `#3b82f6`

### Logo

```python
# ❌ ACTUAL: Fondo verde plano
logo_label = ctk.CTkLabel(
    master=sidebar_frame,
    text="ARTANDA",
    fg_color="#48bb78"
)

# ✅ MEJORADO: Gradiente azul profesional
logo_frame = ctk.CTkFrame(
    master=sidebar_frame,
    fg_color="#2563eb",  # Simulación de gradiente (CustomTkinter no soporta gradientes nativos)
    height=80,
    corner_radius=0
)
logo_label = ctk.CTkLabel(
    master=logo_frame,
    text="ARTANDA",
    font=("Segoe UI", 18, "bold"),
    text_color="#ffffff"
)
```

---

## 📄 3. ÁREA PRINCIPAL (HEADERS Y CONTENIDO)

### Headers de Página

```python
# ❌ IMPLEMENTACIÓN ACTUAL
header_frame = ctk.CTkFrame(
    master=main_content,
    fg_color="#2d3748"
)
title_label = ctk.CTkLabel(
    master=header_frame,
    text="RESUMEN DE PARTES",  # Todo mayúsculas
    font=("Arial", 20, "bold"),
    text_color="#ffffff"
)

# ✅ NUEVA IMPLEMENTACIÓN
header_frame = ctk.CTkFrame(
    master=main_content,
    fg_color="#ffffff",
    corner_radius=0,
    height=100
)

# Agregar borde inferior sutil
separator = ctk.CTkFrame(
    master=header_frame,
    height=1,
    fg_color="#e2e8f0"
)
separator.pack(side="bottom", fill="x")

title_label = ctk.CTkLabel(
    master=header_frame,
    text="Resumen de Partes",  # Sentence case
    font=("Segoe UI", 24, "600"),  # Peso semibold
    text_color="#1e293b",
    anchor="w"
)
title_label.pack(side="top", padx=32, pady=(24, 8))
```

### Especificaciones del Header

- **Fondo:** `#ffffff`
- **Padding:** 24px vertical, 32px horizontal
- **Borde inferior:** 1px `#e2e8f0`
- **Título:**
  - Fuente: Segoe UI, 24px, peso 600
  - Color: `#1e293b`
  - Formato: Sentence case (no todo mayúsculas)
- **Subtítulo (opcional):**
  - Fuente: Segoe UI, 14px, peso 400
  - Color: `#64748b`

### Fondo del Área Principal

```python
# ❌ ACTUAL
main_frame = ctk.CTkFrame(master=root, fg_color="#2d3748")

# ✅ MEJORADO
main_frame = ctk.CTkFrame(
    master=root,
    fg_color="#f8fafc",
    corner_radius=0
)
```

---

## 🔘 4. BOTONES

### Jerarquía de Botones

```python
# ====================================
# BOTÓN PRIMARIO (Acción principal)
# ====================================
# ❌ ACTUAL
btn_primary = ctk.CTkButton(
    master=parent,
    text="+ Añadir Parte",
    fg_color="#48bb78",
    hover_color="#38a169",
    font=("Arial", 14)
)

# ✅ MEJORADO
btn_primary = ctk.CTkButton(
    master=parent,
    text="Añadir Parte",
    fg_color="#3b82f6",
    hover_color="#2563eb",
    text_color="#ffffff",
    font=("Segoe UI", 14, "500"),
    height=40,
    corner_radius=6,
    border_width=0
)

# Añadir icono dentro del texto si es posible, o usar un frame contenedor
# icon_label = ctk.CTkLabel(btn_primary, text="+ ", font=("Segoe UI", 16))


# ====================================
# BOTÓN SECUNDARIO (Acciones secundarias)
# ====================================
# ❌ ACTUAL
btn_secondary = ctk.CTkButton(
    master=parent,
    text="Recargar",
    fg_color="#4299e1",
    hover_color="#3182ce"
)

# ✅ MEJORADO
btn_secondary = ctk.CTkButton(
    master=parent,
    text="Recargar",
    fg_color="#ffffff",
    hover_color="#f8fafc",
    text_color="#475569",
    border_color="#cbd5e1",
    border_width=1,
    font=("Segoe UI", 14, "500"),
    height=40,
    corner_radius=6
)


# ====================================
# BOTÓN DESTRUCTIVO (Eliminar)
# ====================================
btn_danger = ctk.CTkButton(
    master=parent,
    text="Eliminar",
    fg_color="#ef4444",
    hover_color="#dc2626",
    text_color="#ffffff",
    font=("Segoe UI", 14, "500"),
    height=40,
    corner_radius=6,
    border_width=0
)


# ====================================
# BOTÓN ÉXITO (Guardar, Confirmar)
# ====================================
btn_success = ctk.CTkButton(
    master=parent,
    text="Guardar",
    fg_color="#10b981",
    hover_color="#059669",
    text_color="#ffffff",
    font=("Segoe UI", 14, "500"),
    height=40,
    corner_radius=6,
    border_width=0
)
```

### Especificaciones Generales de Botones

- **Altura estándar:** 40px
- **Corner radius:** 6px
- **Padding horizontal:** 20px (usar width mínimo si CTk no soporta padding)
- **Fuente:** Segoe UI, 14px, peso 500
- **Separación entre botones:** 12px
- **Agregar iconos:** Usar `+ `, `🔄 `, `📄 ` antes del texto si no hay soporte nativo de iconos

---

## 📊 5. TABLAS

### Implementación Mejorada

```python
# ====================================
# CONTENEDOR DE TABLA
# ====================================
# ❌ ACTUAL
table_frame = ctk.CTkFrame(
    master=content_area,
    fg_color="#2d3748",
    border_color="#4a5568",
    border_width=1
)

# ✅ MEJORADO
table_container = ctk.CTkFrame(
    master=content_area,
    fg_color="#ffffff",
    border_color="#e2e8f0",
    border_width=1,
    corner_radius=8
)


# ====================================
# HEADER DE TABLA
# ====================================
# ❌ ACTUAL
header_frame = ctk.CTkFrame(
    master=table_frame,
    fg_color="#4299e1"
)
header_label = ctk.CTkLabel(
    master=header_frame,
    text="ID",
    text_color="#ffffff",
    font=("Arial", 12, "bold")
)

# ✅ MEJORADO
header_frame = ctk.CTkFrame(
    master=table_container,
    fg_color="#f8fafc",
    height=48
)

# Agregar borde inferior al header
separator = ctk.CTkFrame(
    master=header_frame,
    height=2,
    fg_color="#e2e8f0"
)
separator.pack(side="bottom", fill="x")

header_label = ctk.CTkLabel(
    master=header_frame,
    text="ID",  # Uppercase para headers de tabla está bien
    text_color="#64748b",
    font=("Segoe UI", 12, "600"),
    anchor="w"
)


# ====================================
# FILAS DE TABLA
# ====================================
# ❌ ACTUAL
row_frame = ctk.CTkFrame(
    master=table_frame,
    fg_color="#2d3748",
    border_color="#4a5568",
    border_width=1
)
cell_label = ctk.CTkLabel(
    master=row_frame,
    text="P-001",
    text_color="#e2e8f0"
)

# ✅ MEJORADO
row_frame = ctk.CTkFrame(
    master=table_container,
    fg_color="#ffffff",
    height=56
)

# Borde inferior de fila
separator = ctk.CTkFrame(
    master=row_frame,
    height=1,
    fg_color="#e2e8f0"
)
separator.pack(side="bottom", fill="x")

cell_label = ctk.CTkLabel(
    master=row_frame,
    text="P-001",
    text_color="#334155",
    font=("Segoe UI", 14),
    anchor="w"
)

# Efecto hover en filas (si es posible programáticamente)
def on_row_hover(event):
    row_frame.configure(fg_color="#f8fafc")

def on_row_leave(event):
    row_frame.configure(fg_color="#ffffff")

row_frame.bind("<Enter>", on_row_hover)
row_frame.bind("<Leave>", on_row_leave)
```

### Especificaciones de Tablas

- **Contenedor:**
  - Fondo: `#ffffff`
  - Borde: 1px `#e2e8f0`
  - Corner radius: 8px
  - Padding: 0px (las celdas tienen su propio padding)

- **Header:**
  - Fondo: `#f8fafc`
  - Alto: 48px
  - Padding: 16px horizontal
  - Borde inferior: 2px `#e2e8f0`
  - Texto: `#64748b`, Segoe UI, 12px, peso 600, UPPERCASE

- **Filas:**
  - Fondo normal: `#ffffff`
  - Fondo hover: `#f8fafc`
  - Alto: 56px
  - Padding: 16px horizontal
  - Borde inferior: 1px `#e2e8f0`
  - Texto: `#334155`, Segoe UI, 14px

- **Estados en celdas (Badges):**
```python
# Crear un frame para simular badge/pill
badge_frame = ctk.CTkFrame(
    master=cell_frame,
    fg_color="#d1fae5",  # Verde claro para "En curso"
    corner_radius=12,
    height=24
)
badge_label = ctk.CTkLabel(
    master=badge_frame,
    text="En curso",
    text_color="#065f46",  # Verde oscuro
    font=("Segoe UI", 12, "500")
)
badge_label.pack(padx=12, pady=2)

# Colores por estado:
# Pendiente: fg_color="#fef3c7", text_color="#92400e"
# En curso: fg_color="#d1fae5", text_color="#065f46"
# Completado: fg_color="#dbeafe", text_color="#1e40af"
# Error: fg_color="#fee2e2", text_color="#991b1b"
```

---

## 📝 6. FORMULARIOS E INPUTS

### Modales/Diálogos

```python
# ====================================
# CONTENEDOR MODAL
# ====================================
# ❌ ACTUAL
modal_frame = ctk.CTkFrame(
    master=overlay,
    fg_color="#2d3748",
    corner_radius=8,
    width=500
)

# ✅ MEJORADO
modal_frame = ctk.CTkFrame(
    master=overlay,
    fg_color="#ffffff",
    corner_radius=12,
    width=520,
    border_width=0
)

# Título del modal
modal_title = ctk.CTkLabel(
    master=modal_frame,
    text="Añadir Nuevo Parte",  # Sentence case
    font=("Segoe UI", 22, "600"),
    text_color="#1e293b",
    anchor="w"
)
modal_title.pack(padx=32, pady=(32, 24))
```

### Labels de Campos

```python
# ❌ ACTUAL
label = ctk.CTkLabel(
    master=form_frame,
    text="OT:",
    text_color="#a0aec0",
    font=("Arial", 14)
)

# ✅ MEJORADO
label = ctk.CTkLabel(
    master=form_frame,
    text="Orden de Trabajo",  # Texto descriptivo completo
    text_color="#475569",
    font=("Segoe UI", 14, "500"),
    anchor="w"
)
```

### Campos de Entrada (Entry)

```python
# ❌ ACTUAL
entry = ctk.CTkEntry(
    master=form_frame,
    fg_color="#4299e1",
    text_color="#ffffff",
    border_width=0
)

# ✅ MEJORADO
entry = ctk.CTkEntry(
    master=form_frame,
    fg_color="#ffffff",
    text_color="#1e293b",
    border_color="#cbd5e1",
    border_width=1,
    corner_radius=6,
    height=42,
    font=("Segoe UI", 14)
)

# Estados del entry:
# Normal: border_color="#cbd5e1"
# Hover: border_color="#94a3b8"
# Focus: border_color="#3b82f6", border_width=2
# Error: border_color="#ef4444", border_width=2
```

### Selectores/OptionMenu

```python
# ❌ ACTUAL
dropdown = ctk.CTkOptionMenu(
    master=form_frame,
    values=["Opción 1", "Opción 2"],
    fg_color="#4299e1",
    button_color="#3182ce",
    text_color="#ffffff"
)

# ✅ MEJORADO
dropdown = ctk.CTkOptionMenu(
    master=form_frame,
    values=["Seleccionar...", "Opción 1", "Opción 2"],
    fg_color="#ffffff",
    button_color="#f8fafc",
    button_hover_color="#e2e8f0",
    text_color="#1e293b",
    dropdown_fg_color="#ffffff",
    dropdown_hover_color="#f8fafc",
    dropdown_text_color="#334155",
    corner_radius=6,
    height=42,
    border_color="#cbd5e1",
    border_width=1,
    font=("Segoe UI", 14)
)
```

### Especificaciones de Formularios

- **Separación entre campos:** 20px vertical
- **Altura de inputs:** 42px
- **Corner radius:** 6px
- **Borde:** 1px `#cbd5e1`
- **Fuente:** Segoe UI, 14px
- **Labels:**
  - Color: `#475569`
  - Fuente: Segoe UI, 14px, peso 500
  - Margen inferior: 8px
  - Texto descriptivo completo (no abreviaturas)

---

## 📐 7. ESPACIADO Y LAYOUT

### Sistema de Espaciado Consistente

```python
# Definir constantes de espaciado
SPACING_XS = 4   # Espaciado extra pequeño
SPACING_SM = 8   # Espaciado pequeño
SPACING_MD = 12  # Espaciado medio
SPACING_LG = 16  # Espaciado grande
SPACING_XL = 20  # Espaciado extra grande
SPACING_2XL = 24 # Espaciado doble extra grande
SPACING_3XL = 32 # Espaciado triple extra grande

# Aplicación:
# - Entre elementos relacionados: SPACING_MD (12px)
# - Entre secciones: SPACING_XL (20px)
# - Padding de contenedores: SPACING_2XL (24px) o SPACING_3XL (32px)
# - Entre botones: SPACING_MD (12px)
```

### Estructura de Pantalla

```
┌─────────────────────────────────────────────────────┐
│ Header                                              │ Padding: 24px vertical, 32px horizontal
│ - Título (24px)                                     │ Fondo: #ffffff
│ - Botones de acción                                 │ Borde inferior: 1px #e2e8f0
└─────────────────────────────────────────────────────┘
│ Content Area                                        │ Padding: 24px o 32px
│ - Contenido principal                               │ Fondo: #f8fafc
│                                                     │
│   ┌─────────────────────────────────────────────┐  │
│   │ Tarjeta/Tabla                               │  │ Fondo: #ffffff
│   │ Padding interno: 0 (las celdas lo manejan) │  │ Corner radius: 8px
│   └─────────────────────────────────────────────┘  │ Borde: 1px #e2e8f0
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🎭 8. TIPOGRAFÍA

### Jerarquía Tipográfica

```python
# Fuente principal: Segoe UI (disponible en Windows)
# Alternativas: -apple-system, "SF Pro", sans-serif

# H1 - Títulos principales de página
FONT_H1 = ("Segoe UI", 24, "600")  # 24px, semibold
COLOR_H1 = "#1e293b"

# H2 - Subtítulos de sección
FONT_H2 = ("Segoe UI", 20, "600")  # 20px, semibold
COLOR_H2 = "#1e293b"

# H3 - Títulos de tarjetas/modales
FONT_H3 = ("Segoe UI", 18, "600")  # 18px, semibold
COLOR_H3 = "#1e293b"

# Body Large - Texto destacado
FONT_BODY_LG = ("Segoe UI", 16)  # 16px, normal
COLOR_BODY_LG = "#334155"

# Body - Texto regular
FONT_BODY = ("Segoe UI", 14)  # 14px, normal
COLOR_BODY = "#334155"

# Body Small - Texto secundario
FONT_BODY_SM = ("Segoe UI", 13)  # 13px, normal
COLOR_BODY_SM = "#64748b"

# Caption - Texto muy pequeño (metadatos)
FONT_CAPTION = ("Segoe UI", 12)  # 12px, normal
COLOR_CAPTION = "#94a3b8"

# Labels - Etiquetas de formularios
FONT_LABEL = ("Segoe UI", 14, "500")  # 14px, medium
COLOR_LABEL = "#475569"

# Button - Texto en botones
FONT_BUTTON = ("Segoe UI", 14, "500")  # 14px, medium
COLOR_BUTTON = "#ffffff" (en botones de color) o "#475569" (en botones blancos)

# Table Header - Headers de tabla
FONT_TABLE_HEADER = ("Segoe UI", 12, "600")  # 12px, semibold, UPPERCASE
COLOR_TABLE_HEADER = "#64748b"
```

### Reglas Tipográficas

1. **No usar todo mayúsculas** excepto en:
   - Headers de tabla (columnas)
   - Abreviaturas estándar (ID, OT, etc.)

2. **Usar Sentence case** para:
   - Títulos de páginas ("Resumen de partes")
   - Títulos de modales ("Añadir nuevo parte")
   - Botones ("Añadir parte", no "AÑADIR PARTE")

3. **Usar texto descriptivo completo:**
   - "Orden de Trabajo" en lugar de "OT"
   - "Descripción" en lugar de "Desc."
   - Excepto en tablas donde el espacio es limitado

---

## 🔍 9. ESTADOS INTERACTIVOS

### Estados de Hover

```python
# Implementar con eventos bind o propiedades hover_color

# Botones
# - Primary: #2563eb
# - Secondary: #f8fafc
# - Danger: #dc2626

# Filas de tabla
# - Normal: #ffffff
# - Hover: #f8fafc

# Items de menú
# - Normal: transparent
# - Hover: #334155

# Inputs
# - Normal border: #cbd5e1
# - Hover border: #94a3b8
# - Focus border: #3b82f6 (2px)
```

### Estados de Active/Selected

```python
# Item de menú activo
menu_item.configure(
    fg_color="#334155",
    text_color="#ffffff"
)
# Agregar borde izquierdo de 3px color #3b82f6

# Botón presionado
# Reducir ligeramente el brillo del color

# Checkbox/Radio seleccionado
# Usar color #3b82f6
```

### Estados Disabled

```python
# Botón deshabilitado
btn_disabled = ctk.CTkButton(
    master=parent,
    text="Deshabilitado",
    fg_color="#e2e8f0",
    text_color="#94a3b8",
    state="disabled"
)

# Input deshabilitado
entry_disabled = ctk.CTkEntry(
    master=parent,
    fg_color="#f8fafc",
    text_color="#94a3b8",
    border_color="#e2e8f0",
    state="disabled"
)
```

---

## 🔔 10. FEEDBACK VISUAL

### Mensajes de Estado/Toast

```python
# Crear un frame flotante en la parte superior

# Éxito
toast_success = ctk.CTkFrame(
    master=overlay,
    fg_color="#d1fae5",
    corner_radius=8,
    border_color="#10b981",
    border_width=1
)
toast_icon = ctk.CTkLabel(
    master=toast_success,
    text="✓ ",
    text_color="#065f46",
    font=("Segoe UI", 16, "bold")
)
toast_message = ctk.CTkLabel(
    master=toast_success,
    text="Parte guardado correctamente",
    text_color="#065f46",
    font=("Segoe UI", 14)
)

# Error
toast_error = ctk.CTkFrame(
    master=overlay,
    fg_color="#fee2e2",
    corner_radius=8,
    border_color="#ef4444",
    border_width=1
)
toast_icon = ctk.CTkLabel(
    master=toast_error,
    text="✕ ",
    text_color="#991b1b",
    font=("Segoe UI", 16, "bold")
)
toast_message = ctk.CTkLabel(
    master=toast_error,
    text="Error al guardar el parte",
    text_color="#991b1b",
    font=("Segoe UI", 14)
)

# Warning
toast_warning = ctk.CTkFrame(
    master=overlay,
    fg_color="#fef3c7",
    corner_radius=8,
    border_color="#fbbf24",
    border_width=1
)
# Usar text_color="#92400e" para el texto
```

### Loading/Spinners

```python
# Usar CTkProgressBar en modo indeterminado
# O crear un label con animación de texto
loading_label = ctk.CTkLabel(
    master=parent,
    text="Cargando...",
    text_color="#64748b",
    font=("Segoe UI", 14)
)

# Animación: cambiar entre "Cargando", "Cargando.", "Cargando..", "Cargando..."
```

---

## 📱 11. MEJORAS ESPECÍFICAS POR PANTALLA

### Pantalla 1: Resumen de Partes

**Cambios:**
1. Fondo principal: `#f8fafc`
2. Header: fondo `#ffffff` con borde inferior
3. Botones: usar nueva jerarquía (primario azul, secundarios blancos)
4. Tabla: fondo blanco, headers grises claros, bordes sutiles
5. Agregar estados en badges/pills con colores apropiados

### Pantalla 2: Modal "Añadir Nuevo Parte"

**Cambios:**
1. Overlay: fondo `rgba(15, 23, 42, 0.75)` con efecto blur si es posible
2. Modal: fondo `#ffffff`, corner radius 12px, sombra grande
3. Título: Sentence case, 22px semibold
4. Labels: texto completo descriptivo, no abreviaturas
5. Inputs: fondo blanco con bordes `#cbd5e1`
6. Botones: Guardar (azul primario) + Cancelar (blanco con borde)
7. Espaciado: 20px entre campos, 32px padding del modal

### Pantalla 3: Gestión de Partes

**Cambios:**
1. Selector de parte: usar dropdown estilo mejorado
2. Tabs (Datos Básicos, Presupuesto, Certificaciones):
   - Fondo normal: transparente
   - Fondo activo: usar borde inferior de 2px `#3b82f6` en lugar de fondo completo
   - Texto activo: `#3b82f6`
   - Texto inactivo: `#64748b`
3. Área de contenido vacía: usar color de texto `#94a3b8`

### Pantalla 4: Presupuesto por Parte

**Cambios:**
1. Botones de acción: ajustar a nueva jerarquía
2. Tabla de partidas: aplicar nuevo estilo de tabla
3. Total en la parte inferior: hacerlo más prominente
   ```python
   total_frame = ctk.CTkFrame(
       master=parent,
       fg_color="#f8fafc",
       corner_radius=8,
       border_color="#e2e8f0",
       border_width=1
   )
   total_label = ctk.CTkLabel(
       master=total_frame,
       text="TOTAL: 0.00€",
       text_color="#1e293b",
       font=("Segoe UI", 18, "600")
   )
   ```

### Pantalla 5: Certificaciones por Parte

**Cambios:**
1. Sección "Pendientes de Certificar": usar color amarillo/naranja para destacar
2. Botón "Certificar Todas": usar color success verde
3. Tablas: aplicar nuevo estilo
4. Fecha: usar DateEntry con estilo consistente

---

## 🛠️ 12. IMPLEMENTACIÓN PASO A PASO

### Orden de Implementación Recomendado

1. **Paso 1:** Crear archivo de constantes de colores
   ```python
   # colors.py o constants.py
   # Copiar todos los colores definidos en la sección 1
   ```

2. **Paso 2:** Actualizar sidebar
   - Cambiar color de fondo
   - Implementar nuevo estilo de items de menú
   - Agregar indicador de item activo

3. **Paso 3:** Actualizar área principal
   - Cambiar fondo a `#f8fafc`
   - Actualizar headers con nuevo estilo

4. **Paso 4:** Actualizar botones
   - Implementar los 4 tipos de botones (primario, secundario, éxito, peligro)
   - Aplicar en todas las pantallas

5. **Paso 5:** Actualizar tablas
   - Nuevo estilo de contenedor
   - Nuevo estilo de headers
   - Nuevo estilo de filas
   - Implementar badges para estados

6. **Paso 6:** Actualizar formularios
   - Nuevo estilo de labels
   - Nuevo estilo de inputs
   - Nuevo estilo de dropdowns
   - Actualizar modales

7. **Paso 7:** Revisar tipografía
   - Cambiar todas las fuentes a Segoe UI
   - Ajustar tamaños según jerarquía
   - Cambiar textos a sentence case

8. **Paso 8:** Agregar estados interactivos
   - Implementar hovers
   - Implementar focus states
   - Agregar feedback visual

---

## ✅ 13. CHECKLIST DE VERIFICACIÓN

### Colores
- [ ] Todos los fondos oscuros reemplazados por claros
- [ ] Sidebar usa `#1e293b`
- [ ] Área principal usa `#f8fafc`
- [ ] Botones primarios usan `#3b82f6`
- [ ] Verde brillante reemplazado por `#10b981`
- [ ] Rojo para acciones destructivas usa `#ef4444`

### Botones
- [ ] Botones primarios: azul con sombra sutil
- [ ] Botones secundarios: blancos con borde
- [ ] Botones destructivos: rojos
- [ ] Altura consistente de 40px
- [ ] Corner radius de 6px
- [ ] Separación de 12px entre botones

### Tablas
- [ ] Fondo blanco
- [ ] Headers con fondo `#f8fafc` y borde inferior de 2px
- [ ] Filas con borde inferior de 1px
- [ ] Hover effect en filas
- [ ] Estados mostrados como badges/pills
- [ ] Corner radius de 8px en contenedor

### Formularios
- [ ] Labels descriptivos completos
- [ ] Inputs con fondo blanco y bordes sutiles
- [ ] Altura de inputs: 42px
- [ ] Separación entre campos: 20px
- [ ] Modales con fondo blanco y sombra grande

### Tipografía
- [ ] Fuente Segoe UI en todos los elementos
- [ ] Títulos en Sentence case
- [ ] Headers de tabla en uppercase
- [ ] Tamaños según jerarquía definida
- [ ] Pesos de fuente apropiados

### Sidebar
- [ ] Items de menú con indicador de borde izquierdo cuando activos
- [ ] Fondo transparente en items normales
- [ ] Hover en `#334155`
- [ ] Item activo en `#334155` + borde azul
- [ ] Logo con estilo mejorado

### Espaciado
- [ ] Padding consistente en headers: 24px vertical, 32px horizontal
- [ ] Padding en contenido: 24-32px
- [ ] Separación entre secciones: 20px
- [ ] Separación entre elementos relacionados: 12px

### Detalles Finales
- [ ] Todos los bordes sutiles (`#e2e8f0` o `#cbd5e1`)
- [ ] Corner radius consistente (6px botones/inputs, 8px tarjetas)
- [ ] Estados hover implementados
- [ ] Feedback visual para acciones (toasts/mensajes)
- [ ] Loading states considerados

---

## 📦 14. EJEMPLO DE CÓDIGO COMPLETO

### Archivo de Constantes (colors.py)

```python
"""
Constantes de colores y estilos para HydroFlow Manager
Basado en paleta profesional Tailwind CSS
"""

# ==================== FONDOS ====================
BG_PRIMARY = "#f8fafc"          # Fondo principal
BG_SECONDARY = "#ffffff"        # Tarjetas y modales
BG_SIDEBAR = "#1e293b"          # Sidebar
BG_SIDEBAR_HOVER = "#334155"    # Hover items sidebar
BG_TABLE_HEADER = "#f8fafc"     # Header de tabla
BG_TABLE_ROW_HOVER = "#f8fafc"  # Hover fila tabla

# ==================== TEXTO ====================
TEXT_PRIMARY = "#1e293b"        # Texto principal
TEXT_SECONDARY = "#64748b"      # Texto secundario
TEXT_MUTED = "#94a3b8"          # Texto deshabilitado
TEXT_INVERSE = "#f8fafc"        # Texto sobre fondos oscuros

# ==================== BOTONES ====================
PRIMARY = "#3b82f6"             # Azul primario
PRIMARY_HOVER = "#2563eb"       # Hover azul
PRIMARY_ACTIVE = "#1d4ed8"      # Active azul

SUCCESS = "#10b981"             # Verde éxito
SUCCESS_HOVER = "#059669"       # Hover verde

DANGER = "#ef4444"              # Rojo eliminar
DANGER_HOVER = "#dc2626"        # Hover rojo

SECONDARY = "#ffffff"           # Botones secundarios (fondo)
SECONDARY_TEXT = "#475569"      # Texto botones secundarios
SECONDARY_HOVER = "#f8fafc"     # Hover secundarios

# ==================== BORDES ====================
BORDER_LIGHT = "#e2e8f0"        # Bordes sutiles
BORDER_DEFAULT = "#cbd5e1"      # Bordes inputs
BORDER_HOVER = "#94a3b8"        # Bordes hover
BORDER_FOCUS = "#3b82f6"        # Bordes focus
BORDER_ERROR = "#ef4444"        # Bordes error

# ==================== ESTADOS/BADGES ====================
STATUS_PENDING_BG = "#fef3c7"   # Fondo amarillo pendiente
STATUS_PENDING_TEXT = "#92400e" # Texto pendiente

STATUS_ACTIVE_BG = "#d1fae5"    # Fondo verde activo
STATUS_ACTIVE_TEXT = "#065f46"  # Texto activo

STATUS_COMPLETE_BG = "#dbeafe"  # Fondo azul completado
STATUS_COMPLETE_TEXT = "#1e40af"  # Texto completado

STATUS_ERROR_BG = "#fee2e2"     # Fondo rojo error
STATUS_ERROR_TEXT = "#991b1b"   # Texto error

# ==================== FUENTES ====================
FONT_FAMILY = "Segoe UI"

# Tamaños y pesos
FONT_H1 = (FONT_FAMILY, 24, "600")
FONT_H2 = (FONT_FAMILY, 20, "600")
FONT_H3 = (FONT_FAMILY, 18, "600")
FONT_BODY_LG = (FONT_FAMILY, 16)
FONT_BODY = (FONT_FAMILY, 14)
FONT_BODY_SM = (FONT_FAMILY, 13)
FONT_CAPTION = (FONT_FAMILY, 12)
FONT_LABEL = (FONT_FAMILY, 14, "500")
FONT_BUTTON = (FONT_FAMILY, 14, "500")
FONT_TABLE_HEADER = (FONT_FAMILY, 12, "600")

# ==================== ESPACIADO ====================
SPACING_XS = 4
SPACING_SM = 8
SPACING_MD = 12
SPACING_LG = 16
SPACING_XL = 20
SPACING_2XL = 24
SPACING_3XL = 32

# ==================== DIMENSIONES ====================
BUTTON_HEIGHT = 40
INPUT_HEIGHT = 42
TABLE_HEADER_HEIGHT = 48
TABLE_ROW_HEIGHT = 56
SIDEBAR_WIDTH = 240

# ==================== RADIUS ====================
RADIUS_SM = 4
RADIUS_MD = 6
RADIUS_LG = 8
RADIUS_XL = 12
RADIUS_FULL = 9999  # Para pills/badges
```

---

## 📄 15. NOTAS FINALES

### Consideraciones Técnicas

1. **CustomTkinter no soporta:**
   - Gradientes CSS (usar colores sólidos)
   - Box-shadow nativo (simular con frames de bordes)
   - Backdrop-filter blur (omitir o usar overlay sólido)
   - Transiciones CSS (los cambios serán instantáneos)

2. **Soluciones alternativas:**
   - Para sombras: usar border_width con colores semitransparentes
   - Para gradientes: usar un color sólido representativo
   - Para iconos: usar emojis Unicode o fuentes de iconos si están disponibles

3. **Prioridades:**
   - Enfocarse primero en colores, espaciado y tipografía
   - Luego en estructura y jerarquía visual
   - Finalmente en detalles y microinteracciones

### Testing Recomendado

1. Probar en diferentes resoluciones de pantalla
2. Verificar contraste de colores (WCAG AA compliance)
3. Asegurar consistencia en todas las pantallas
4. Validar que los textos sean legibles
5. Probar todos los estados interactivos (hover, active, disabled)

---

## 🎓 RECURSOS DE REFERENCIA

- **Paleta de colores:** Basada en Tailwind CSS Slate + Blue
- **Tipografía:** Microsoft Design System (Segoe UI)
- **Espaciado:** Sistema de 4px base
- **Inspiración:** Autodesk Fusion 360, Visual Studio Code, Microsoft 365

---

**Documento creado para:** HydroFlow Manager v1.04_1812  
**Fecha:** Octubre 2025  
**Objetivo:** Elevar la interfaz a nivel profesional empresarial  
**Tecnología:** Python + CustomTkinter  

---

## ⚡ INICIO RÁPIDO - PRIMEROS 5 CAMBIOS CRÍTICOS

Si quieres ver resultados inmediatos, implementa estos 5 cambios en este orden:

### 1. Cambiar colores de fondo principales
```python
# En tu archivo principal
sidebar.configure(fg_color="#1e293b")
main_content.configure(fg_color="#f8fafc")
```

### 2. Actualizar botones primarios
```python
btn_añadir.configure(
    fg_color="#3b82f6",
    hover_color="#2563eb",
    corner_radius=6,
    height=40
)
```

### 3. Cambiar headers de tabla
```python
table_header.configure(
    fg_color="#f8fafc",
    border_color="#e2e8f0",
    border_width=2  # Borde inferior
)
```

### 4. Actualizar tipografía de títulos
```python
titulo.configure(
    font=("Segoe UI", 24, "600"),
    text="Resumen de Partes"  # Sentence case
)
```

### 5. Mejorar inputs de formularios
```python
input.configure(
    fg_color="#ffffff",
    border_color="#cbd5e1",
    border_width=1,
    corner_radius=6,
    height=42
)
```

Estos 5 cambios ya darán una mejora visual significativa del 60-70%.
