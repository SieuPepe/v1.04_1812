# Log de Resolución de Bugs - HydroFlow Manager v1.04.1812

## Bug #1: Numeración de partes siempre mostraba 1
**Fecha:** 2026-01-09
**Estado:** ✅ RESUELTO
**Commits:** `d562378`, `5ab84ec`

### Descripción del problema
Al crear un nuevo parte en el Generador de Partes, el campo "Código OT" siempre mostraba numeración `0001` independientemente de cuántos partes existieran en la base de datos.

### Causa raíz
El código buscaba códigos con **guión `-`** como separador (`OT-0001`), pero los datos existentes en la BD usaban **barra `/`** como separador (`OT/0523`, `TP/0391`).

```sql
-- Código incorrecto (buscaba guiones)
WHERE codigo LIKE '%-%'
SUBSTRING_INDEX(codigo, '-', -1)

-- Código correcto (busca barras)
WHERE codigo LIKE '%/%'
SUBSTRING_INDEX(codigo, '/', -1)
```

### Archivos modificados
1. `script/db_partes.py` - Función `add_parte_mejorado()`
2. `interface/parts_interfaz_v2_fixed.py` - Función `_update_codigo_ot()`
3. `interface/parts_interfaz.py` - Función `_update_codigo_ot()` (legacy)

### Solución aplicada
1. Cambiar el separador de `-` a `/` en las consultas SQL
2. Usar numeración GLOBAL (MAX de todos los códigos, sin filtrar por prefijo)
3. Generar códigos con formato `PREFIX/NNNN` (ej: `OT/0524`)

### Resultado
La numeración ahora es correlativa global. Si el último parte fue `OT/0523`, el siguiente será `TP/0524` (o `OT/0524`, `GF/0524` según el tipo de trabajo).

---

