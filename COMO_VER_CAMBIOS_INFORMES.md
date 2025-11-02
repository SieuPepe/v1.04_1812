# Cómo ver los cambios en la interfaz de Informes

## Estado actual

Todos los cambios están confirmados en el código:
- ✅ TreeView con fuente de 12pt (antes 10pt)
- ✅ Panel izquierdo de 280px de ancho (antes 250px)
- ✅ Secciones Clasificación y Filtros con scroll
- ✅ Espaciado reducido en toda la interfaz

## Pasos para ver los cambios

### 1. Ejecutar la aplicación
```bash
python main.py
```

### 2. Navegar a la interfaz de Informes
- En el menú principal, selecciona **"Generador de Partes"**
- Una vez dentro, busca la pestaña **"Informes"** (debería ser la última pestaña)
- Haz clic en la pestaña "Informes"

### 3. Qué deberías ver

#### Panel Izquierdo (TreeView):
```
TIPO DE INFORME
├── 📊 Partes
│   ├── Informe Tipo 1
│   ├── Informe Tipo 2
│   ├── Informe Tipo 3
│   ├── Informe Tipo 4
│   └── Informe Tipo 5
├── 📦 Recursos
│   ├── Informe Tipo 1
│   ├── Informe Tipo 2
│   ├── Informe Tipo 3
│   └── Informe Tipo 4
├── 💰 Presupuestos
│   └── ...
├── ✅ Certificaciones
│   └── ...
└── 📅 Planificación
    └── ...
```

**Cambios visibles:**
- Texto más grande y legible (12pt)
- Panel más ancho (280px)

#### Panel Derecho:
Deberías ver 4 secciones verticales:

1. **CLASIFICACIÓN**
   - Botón "+ Añadir clasificación"
   - Contenedor con scroll (si hay muchas clasificaciones)

2. **FILTROS**
   - Botón "+ Añadir filtro"
   - Lógica: Y / O
   - Contenedor con scroll (si hay muchos filtros)

3. **SELECCIÓN DE CAMPOS**
   - Checkboxes para campos disponibles según categoría
   - Área con scroll para muchos campos

4. **PRESENTACIÓN**
   - Formato de salida: Tabla / Lista / Tarjetas
   - Ordenar por: (campos disponibles)
   - Orden: Ascendente / Descendente

#### Barra de Acciones (inferior):
```
[Vista previa] [Exportar Word] [Exportar Excel] [Exportar PDF] [Imprimir]
```

## Si NO ves los cambios

### Verificación 1: ¿Estás en la pestaña correcta?
- El módulo de Informes está dentro del **Generador de Partes**
- No está en el menú principal
- Busca una pestaña llamada "Informes" junto a otras pestañas como "Listado", "Nuevo Parte", etc.

### Verificación 2: Limpiar caché de Python
```bash
# En Windows (PowerShell)
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force
Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force

# En Linux/Mac
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -rf {} +
```

### Verificación 3: Reiniciar completamente
1. Cerrar completamente la aplicación (no solo minimizar)
2. Limpiar caché (comando anterior)
3. Volver a ejecutar: `python main.py`

### Verificación 4: Verificar que el código está actualizado
```bash
# Verificar que tienes los últimos commits
git log --oneline -5

# Deberías ver:
# 0adb943 fix: Hacer get_parte_detail compatible...
# 57d442d ui: Mejorar espaciado y legibilidad...
# 54b7f62 feat: Implementar Fase 1 - Infraestructura...
```

### Verificación 5: Buscar errores en logs
Si la pestaña "Informes" no aparece o aparece en blanco:
- Revisa la consola donde ejecutaste `python main.py`
- Busca errores de tipo `ModuleNotFoundError` o `ImportError`
- Busca errores de base de datos

## Solución de problemas comunes

### Problema: "No veo la pestaña Informes"
**Solución:** Verifica que `interface/parts_manager_interfaz.py` tenga el método `main_informes()` actualizado:
```bash
grep -A 10 "def main_informes" interface/parts_manager_interfaz.py
```

### Problema: "La pestaña aparece pero en blanco"
**Solución:** Revisa errores en consola. Posibles causas:
- Error de base de datos (columnas faltantes)
- Error de importación
- Error de CustomTkinter

### Problema: "Veo la interfaz pero no los cambios de tamaño/fuente"
**Solución:**
1. Verifica el archivo tiene los cambios:
   ```bash
   grep "font=('Segoe UI', 12)" interface/informes_interfaz.py
   grep "width=280" interface/informes_interfaz.py
   ```
2. Si aparecen, limpia caché y reinicia completamente

## Contacto
Si después de seguir todos estos pasos aún no ves los cambios, proporciona:
1. Captura de pantalla de lo que ves
2. Output de `git log --oneline -5`
3. Errores en la consola (si hay)
