# Solución al Problema de Fuente del TreeView

## 🔍 Problema Identificado

El TreeView de Informes NO estaba mostrando la fuente más grande debido a un **conflicto de estilos de ttk.Style**.

### Causas Raíz:

1. **`ttk.Style()` es un singleton global** - Todas las llamadas a `ttk.Style()` devuelven el mismo objeto
2. **`parts_manager_interfaz.py`** configura un estilo global con fuente de 11pt en su `__init__`
3. **El estilo global sobrescribía** el estilo personalizado de Informes
4. **Orden de ejecución**: El estilo se configuraba ANTES de crear el widget

---

## ✅ Solución Implementada: DOBLE ENFOQUE

He implementado **DOS métodos simultáneos** para asegurar que la fuente cambie:

### Método 1: Estilo Personalizado (14pt bold)
```python
style = ttk.Style()
style.configure("InformesCustom.Treeview",
                font=('Segoe UI', 14, 'bold'),
                rowheight=32)
self.tree.configure(style="InformesCustom.Treeview")
```

### Método 2: Tags Directos (14pt bold)
```python
import tkinter.font as tkfont
custom_font = tkfont.Font(family='Segoe UI', size=14, weight='bold')
self.tree.tag_configure('custom_font', font=custom_font)

# Aplicar a cada item
self.tree.insert("", "end", text="Categoría", tags=('custom_font',))
```

### Cambios Clave:

1. **Fuente aumentada a 14pt BOLD** (antes 11pt regular)
2. **Altura de fila aumentada a 32px** (antes 35px del global)
3. **Estilo configurado DESPUÉS de crear el widget**
4. **Nombre de estilo único**: `InformesCustom.Treeview`
5. **Tags aplicados a cada item** como respaldo

---

## 🔧 Cómo Probar el Fix

### PASO 1: Verificar que el sistema de estilos funciona

Ejecuta este test antes de actualizar la aplicación:

```powershell
python test_treeview_style.py
```

**Qué verificar:**
- Se abrirá una ventana con DOS TreeView lado a lado
- El de la IZQUIERDA: fuente 11pt (más pequeña)
- El de la DERECHA: fuente 13pt (más grande)
- Si ambos se ven **IGUALES**, hay un problema con ttk.Style en tu sistema

### PASO 2: Actualizar el código

```powershell
# 1. Traer cambios
git fetch origin
git merge origin/claude/add-reports-tab-parts-generator-011CUim4HSH2XKM4WdDrx9xR

# 2. Verificar commit
git log --oneline -2
# Deberías ver: a501cf4 fix: Aplicar fuente 14pt bold al TreeView...

# 3. Verificar que el código tiene el doble enfoque
Select-String -Path "interface/informes_interfaz.py" -Pattern "InformesCustom.Treeview"
Select-String -Path "interface/informes_interfaz.py" -Pattern "tags=\('custom_font'"
```

### PASO 3: Ejecutar la aplicación

```powershell
python main.py
```

### PASO 4: Navegar a Informes

1. Clic en "Generador de Partes"
2. Clic en botón "Informes" en el sidebar izquierdo
3. **Observar el TreeView de categorías**

---

## 📸 Qué Deberías Ver

### ANTES (Pantallazo 10 y 11):
```
📊 Partes          ← Fuente 11pt regular, texto pequeño
📦 Recursos
💰 Presupuestos
✅ Certificaciones
📅 Planificación
```

### DESPUÉS (con el fix):
```
📊 Partes          ← Fuente 14pt BOLD, texto MÁS GRANDE y NEGRITA
📦 Recursos
💰 Presupuestos
✅ Certificaciones
📅 Planificación
```

**Diferencia visual esperada:**
- Texto **notablemente más grande** (27% más grande: 11pt → 14pt)
- Texto en **negrita** (weight='bold')
- Filas con **más espacio** (rowheight 32px)
- Panel **más ancho** (300px vs 250px original)

---

## 🐛 Si TODAVÍA No Funciona

Si después de aplicar el fix el texto sigue viéndose igual, ejecuta este diagnóstico:

```powershell
python -c "
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
style = ttk.Style()

# Test 1: ¿Se puede crear un estilo personalizado?
style.configure('Test.Treeview', font=('Segoe UI', 20, 'bold'))
tree = ttk.Treeview(root, style='Test.Treeview')
tree.insert('', 'end', text='TEST')

print('Estilo aplicado:', style.lookup('Test.Treeview', 'font'))
print('Si ves None o algo diferente a (\'Segoe UI\', 20, \'bold\'), hay un problema con ttk.Style')
"
```

### Posibles problemas adicionales:

1. **Windows High DPI Scaling**: Puede estar interfiriendo con las fuentes
   - Solución: Desactivar DPI scaling para Python

2. **Versión de Tkinter**: Algunas versiones tienen bugs con ttk.Style
   - Verifica con: `python -c "import tkinter; print(tkinter.TkVersion)"`

3. **CustomTkinter interfiriendo**: Aunque no debería afectar ttk widgets
   - Verifica versión: `pip show customtkinter`

---

## 📊 Comparación de Cambios

| Aspecto | Original | Intento 1 | Intento 2 | ACTUAL (Fix) |
|---------|----------|-----------|-----------|--------------|
| Fuente | 10pt | 12pt | 13pt | **14pt BOLD** |
| Rowheight | 25px | 25px | 28px | **32px** |
| Ancho panel | 250px | 280px | 280px | **300px** |
| Método | Style global | Style custom | Style custom | **Style + Tags** |
| Timing | Antes de crear | Antes de crear | Antes de crear | **Después de crear** |
| Nombre estilo | Treeview | Informes.Treeview | Informes.Treeview | **InformesCustom.Treeview** |

---

## 🎯 Próximos Pasos

1. **Ejecuta el test**: `python test_treeview_style.py`
   - Si los dos TreeView se ven DIFERENTES → Sistema funciona bien → Actualiza el código
   - Si los dos TreeView se ven IGUALES → Problema con ttk.Style → Necesitamos otro enfoque

2. **Actualiza el código** con git merge

3. **Ejecuta la aplicación** y navega a Informes

4. **Toma un pantallazo** (Pantallazo12.jpg) y súbelo al branch

5. **Reporta el resultado**:
   - ✅ "Se ve más grande" → ¡Éxito!
   - ❌ "Sigue igual" → Proporci ona output del diagnóstico

---

## 📝 Notas Técnicas

- El enfoque de **tags** es más robusto que Style porque se aplica directamente a cada item
- La fuente se configura con `tkinter.font.Font` que es más explícito que string tuples
- El timing es crítico: configurar DESPUÉS de pack/grid asegura que el widget está completamente inicializado
- Los tags sobreviven a re-configuraciones globales de Style

---

**Ejecuta ahora**: `python test_treeview_style.py` y reporta si ves diferencia entre los dos TreeView.
