#!/usr/bin/env python3
"""
Test para verificar cómo se aplican los estilos de TreeView
"""

import tkinter as tk
from tkinter import ttk

print("=" * 70)
print("TEST DE ESTILOS DE TREEVIEW")
print("=" * 70)

root = tk.Tk()
root.title("Test TreeView Styles")
root.geometry("800x600")

# Crear dos frames lado a lado
frame1 = tk.Frame(root, bg="#2a2d2e")
frame1.pack(side="left", fill="both", expand=True, padx=10, pady=10)

frame2 = tk.Frame(root, bg="#2a2d2e")
frame2.pack(side="left", fill="both", expand=True, padx=10, pady=10)

# Configurar estilo global (como parts_manager)
style = ttk.Style()
style.theme_use('clam')

print("\n1. Configurando estilo GLOBAL 'Treeview' (11pt)...")
style.configure("Treeview",
                background="#2a2d2e",
                foreground="white",
                fieldbackground="#2a2d2e",
                rowheight=35,
                font=('Segoe UI', 11),
                borderwidth=0)

# TreeView 1 - Sin estilo personalizado (usa global)
tk.Label(frame1, text="TreeView GLOBAL (11pt)",
         bg="#2a2d2e", fg="white", font=('Segoe UI', 14, 'bold')).pack(pady=5)

tree1 = ttk.Treeview(frame1, show="tree")
tree1.pack(fill="both", expand=True)

# Poblar tree1
cat1 = tree1.insert("", "end", text="📊 Categoría 1")
tree1.insert(cat1, "end", text="  Item 1")
tree1.insert(cat1, "end", text="  Item 2")

print(f"   TreeView 1 creado (sin style= parameter)")
print(f"   Fuente configurada: ('Segoe UI', 11)")

# Configurar estilo personalizado
print("\n2. Configurando estilo PERSONALIZADO 'Informes.Treeview' (13pt)...")
style.configure("Informes.Treeview",
                background="#2a2d2e",
                foreground="white",
                fieldbackground="#2a2d2e",
                rowheight=28,
                font=('Segoe UI', 13),
                borderwidth=0)

# TreeView 2 - Con estilo personalizado
tk.Label(frame2, text="TreeView PERSONALIZADO (13pt)",
         bg="#2a2d2e", fg="white", font=('Segoe UI', 14, 'bold')).pack(pady=5)

tree2 = ttk.Treeview(frame2, show="tree", style="Informes.Treeview")
tree2.pack(fill="both", expand=True)

# Poblar tree2
cat2 = tree2.insert("", "end", text="📊 Categoría 1")
tree2.insert(cat2, "end", text="  Item 1")
tree2.insert(cat2, "end", text="  Item 2")

print(f"   TreeView 2 creado (con style='Informes.Treeview')")
print(f"   Fuente configurada: ('Segoe UI', 13)")

# Verificar configuraciones
print("\n3. Verificando configuraciones aplicadas...")
print(f"\nEstilo 'Treeview':")
try:
    font_config = style.lookup("Treeview", "font")
    print(f"   Font: {font_config}")
except Exception as e:
    print(f"   Error: {e}")

print(f"\nEstilo 'Informes.Treeview':")
try:
    font_config = style.lookup("Informes.Treeview", "font")
    print(f"   Font: {font_config}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 70)
print("INSTRUCCIONES:")
print("=" * 70)
print("Compara visualmente ambos TreeView:")
print("- El de la IZQUIERDA debería tener fuente 11pt (más pequeña)")
print("- El de la DERECHA debería tener fuente 13pt (más grande)")
print("\nSi ambos se ven IGUALES, hay un problema con ttk.Style en tu sistema.")
print("=" * 70)

root.mainloop()
