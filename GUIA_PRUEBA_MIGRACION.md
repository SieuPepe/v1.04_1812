# GUÍA DE PRUEBA: MIGRACIÓN DE MEJORAS DE PARTES

## 🎯 OBJETIVO

Probar la migración de mejoras de partes en un proyecto de prueba antes de aplicarla a producción.

---

## ⚠️ ANTES DE EMPEZAR

### Requisitos:
- ✅ Acceso a MySQL con usuario administrador
- ✅ Al menos un esquema/proyecto con tabla `tbl_partes`
- ✅ Python 3.9+ instalado
- ✅ Repositorio actualizado (`git pull`)

---

## 📋 PASO 1: BACKUP DE SEGURIDAD

**IMPORTANTE**: Siempre hacer backup antes de cualquier migración.

### Opción A: Backup de un esquema específico
```bash
# Reemplaza 'cert_dev' con tu esquema de prueba
mysqldump -u tu_usuario -p cert_dev > backup_cert_dev_antes_migracion.sql
```

### Opción B: Backup de todos los esquemas
```bash
mysqldump -u tu_usuario -p --all-databases > backup_completo_antes_migracion.sql
```

### Verificar backup creado:
```bash
ls -lh backup_*.sql
# Debe mostrar el archivo con tamaño > 0
```

---

## 📋 PASO 2: IDENTIFICAR PROYECTO DE PRUEBA

Conecta a MySQL y lista tus proyectos:

```bash
mysql -u tu_usuario -p
```

```sql
-- Ver todos los esquemas
SHOW DATABASES;

-- Ver esquemas que tienen tabla tbl_partes
SELECT TABLE_SCHEMA
FROM information_schema.TABLES
WHERE TABLE_NAME = 'tbl_partes';
```

**Elige uno para prueba**. Recomiendo usar `cert_dev` si existe, o el que menos impacto tenga.

Anota el nombre: `_____________________`

---

## 📋 PASO 3: VERIFICAR ESTADO ACTUAL

Antes de migrar, verifica el estado actual de la tabla:

```sql
-- Usar tu esquema de prueba
USE cert_dev;  -- ← Cambiar por tu esquema

-- Ver estructura actual
DESCRIBE tbl_partes;

-- Contar registros actuales
SELECT COUNT(*) AS total_partes FROM tbl_partes;

-- Ver algunos partes existentes
SELECT id, codigo, descripcion, creado_en
FROM tbl_partes
ORDER BY id DESC
LIMIT 5;
```

**Anota cuántos partes hay**: `_____` partes

---

## 📋 PASO 4: EJECUTAR MIGRACIÓN

### Opción A: Migración con DRY-RUN (Simulación)

Primero, simula sin hacer cambios:

```bash
cd /home/user/v1.04_1812

python script/migrate_partes_mejoras.py \
  --user tu_usuario \
  --password tu_password \
  --schema cert_dev \
  --dry-run
```

**Debe mostrar**:
```
🔸 MODO DRY-RUN: No se ejecutarán cambios

Esquemas que se migrarían:
  • cert_dev
```

### Opción B: Migración Real en UN Esquema

Si el dry-run se ve bien, ejecuta la migración real:

```bash
python script/migrate_partes_mejoras.py \
  --user tu_usuario \
  --password tu_password \
  --schema cert_dev
```

**Output esperado**:
```
================================================================================
  MIGRACIÓN: Mejoras de Órdenes de Trabajo (tbl_partes)
================================================================================

📄 Leyendo script SQL: script/mejoras_tabla_partes.sql
   ✅ Script cargado (XXXXX caracteres)

🎯 Esquema específico: cert_dev

🚀 Iniciando migración...

[1/1] cert_dev... ✅ Completado exitosamente

================================================================================
  RESUMEN DE MIGRACIÓN
================================================================================
  ✅ Exitosos:  1
  ⏭️  Omitidos:  0
  ❌ Errores:   0
  📊 Total:     1
================================================================================

🎉 ¡Migración completada exitosamente!
```

### Posibles Errores:

**Error: "Access denied"**
→ Usuario/contraseña incorrectos

**Error: "Table 'tbl_partes' doesn't exist"**
→ El esquema no tiene sistema de partes, se omitirá (normal)

**Error: "Duplicate column name 'titulo'"**
→ La migración ya se aplicó antes (ejecutar es seguro, es idempotente)

---

## 📋 PASO 5: VERIFICAR MIGRACIÓN EXITOSA

Conecta a MySQL y verifica los cambios:

```sql
USE cert_dev;  -- Tu esquema

-- ============================================================================
-- VERIFICACIÓN 1: Nueva tabla tbl_parte_estados
-- ============================================================================
SELECT * FROM tbl_parte_estados ORDER BY orden;
```

**Resultado esperado:**
```
+----+-------------+--------------------------------+-------+--------+
| id | nombre      | descripcion                    | orden | activo |
+----+-------------+--------------------------------+-------+--------+
|  1 | Pendiente   | Parte pendiente de iniciar     |     1 |      1 |
|  2 | En curso    | Parte en ejecución             |     2 |      1 |
|  3 | Finalizada  | Parte completada con éxito     |     3 |      1 |
|  4 | Cancelada   | Parte cancelada                |     4 |      1 |
|  5 | Suspendida  | Parte temporalmente suspendida |     5 |      1 |
+----+-------------+--------------------------------+-------+--------+
5 rows in set
```

✅ **Si ves esto, la tabla de estados se creó correctamente**

---

```sql
-- ============================================================================
-- VERIFICACIÓN 2: Nuevos campos en tbl_partes
-- ============================================================================
DESCRIBE tbl_partes;
```

**Busca estos campos nuevos** (deben aparecer):
- `titulo` (varchar 255)
- `descripcion_larga` (text)
- `descripcion_corta` (varchar 100)
- `fecha_inicio` (date)
- `fecha_fin` (date)
- `fecha_prevista_fin` (date)
- `id_estado` (int)
- `finalizada` (tinyint)
- `localizacion` (varchar 255)
- `id_municipio` (int)

✅ **Si ves estos 10-11 campos nuevos, la migración de tabla fue correcta**

---

```sql
-- ============================================================================
-- VERIFICACIÓN 3: Vista vw_partes_completo
-- ============================================================================
SHOW CREATE VIEW vw_partes_completo\G
```

**Debe mostrar** la definición completa de la vista.

```sql
-- Ver datos de la vista
SELECT * FROM vw_partes_completo LIMIT 5;
```

✅ **Si la vista existe y devuelve datos, está correcta**

---

```sql
-- ============================================================================
-- VERIFICACIÓN 4: Triggers creados
-- ============================================================================
SHOW TRIGGERS WHERE `Table` = 'tbl_partes'\G
```

**Debe mostrar 2 triggers:**
- `trg_partes_sync_finalizada_insert`
- `trg_partes_sync_finalizada_update`

✅ **Si ves los 2 triggers, la sincronización automática está activa**

---

```sql
-- ============================================================================
-- VERIFICACIÓN 5: Índices creados
-- ============================================================================
SHOW INDEX FROM tbl_partes;
```

**Busca estos índices nuevos:**
- `idx_partes_estado`
- `idx_partes_finalizada`
- `idx_partes_fecha_inicio`
- `idx_partes_fecha_fin`
- `idx_partes_municipio`
- `idx_partes_estado_fecha`

✅ **Si ves estos índices, la optimización está activa**

---

```sql
-- ============================================================================
-- VERIFICACIÓN 6: Datos migrados (valores por defecto)
-- ============================================================================
SELECT
    id,
    codigo,
    titulo,
    descripcion_corta,
    id_estado,
    finalizada
FROM tbl_partes
LIMIT 5;
```

**Debe mostrar:**
- `titulo`: Tendrá valores (copiados de descripción o "Parte XXXXX")
- `descripcion_corta`: Tendrá valores (truncados de descripción)
- `id_estado`: Todos en `1` (Pendiente)
- `finalizada`: Todos en `0` (FALSE)

✅ **Si los registros antiguos tienen valores, la migración de datos fue correcta**

---

```sql
-- ============================================================================
-- VERIFICACIÓN 7: Contar registros (no debe haber pérdida)
-- ============================================================================
SELECT COUNT(*) AS total_partes_despues FROM tbl_partes;
```

**Comparar con el número anotado antes** en PASO 3.

✅ **Deben ser iguales (no se perdió ningún registro)**

---

## 📋 PASO 6: PROBAR TRIGGERS

Vamos a probar que los triggers funcionan:

```sql
-- Insertar un parte de prueba
INSERT INTO tbl_partes (ot_id, red_id, tipo_trabajo_id, cod_trabajo_id, titulo, id_estado)
VALUES (1, 1, 1, 1, 'Test de triggers', 2);  -- Estado: En curso

-- Ver el parte creado
SELECT id, codigo, titulo, id_estado, finalizada
FROM tbl_partes
WHERE titulo = 'Test de triggers';
```

**Debe mostrar:**
- `id_estado`: `2` (En curso)
- `finalizada`: `0` (FALSE)

✅ **Correcto**

---

```sql
-- Cambiar estado a Finalizada
UPDATE tbl_partes
SET id_estado = 3
WHERE titulo = 'Test de triggers';

-- Verificar que 'finalizada' cambió automáticamente
SELECT id, codigo, titulo, id_estado, finalizada, fecha_fin
FROM tbl_partes
WHERE titulo = 'Test de triggers';
```

**Debe mostrar:**
- `id_estado`: `3` (Finalizada)
- `finalizada`: `1` (TRUE) ← **Cambió automáticamente**
- `fecha_fin`: Fecha de hoy ← **Se puso automáticamente**

✅ **Triggers funcionando correctamente**

---

```sql
-- Cambiar 'finalizada' directamente
UPDATE tbl_partes
SET finalizada = 0
WHERE titulo = 'Test de triggers';

-- Verificar que 'id_estado' cambió automáticamente
SELECT id, codigo, titulo, id_estado, finalizada
FROM tbl_partes
WHERE titulo = 'Test de triggers';
```

**Debe mostrar:**
- `id_estado`: `2` (En curso) ← **Cambió automáticamente de 3 a 2**
- `finalizada`: `0` (FALSE)

✅ **Sincronización bidireccional funciona**

---

```sql
-- Limpiar: Eliminar parte de prueba
DELETE FROM tbl_partes WHERE titulo = 'Test de triggers';
```

---

## 📋 PASO 7: PROBAR FUNCIONES PYTHON

Crea un archivo de test:

```bash
cd /home/user/v1.04_1812
nano test_partes_mejorados.py
```

Copia este contenido (ajusta credenciales):

```python
#!/usr/bin/env python3
"""Test de funciones mejoradas de partes"""
import sys
from script.modulo_db import (
    add_parte_mejorado,
    mod_parte_mejorado,
    get_estados_parte,
    list_partes_mejorado
)

# ============================================================================
# CONFIGURACIÓN - AJUSTA ESTOS VALORES
# ============================================================================
USER = 'tu_usuario'
PASSWORD = 'tu_password'
SCHEMA = 'cert_dev'  # Tu esquema de prueba

print("=" * 80)
print("  TEST DE FUNCIONES MEJORADAS DE PARTES")
print("=" * 80)
print()

# ============================================================================
# TEST 1: Obtener estados
# ============================================================================
print("TEST 1: Obtener estados disponibles")
print("-" * 80)
try:
    estados = get_estados_parte(USER, PASSWORD, SCHEMA)
    print(f"✅ {len(estados)} estados encontrados:")
    for id, nombre, descripcion, orden in estados:
        print(f"   {id}. {nombre:15} - {descripcion}")
    print()
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)

# ============================================================================
# TEST 2: Crear parte mejorado
# ============================================================================
print("TEST 2: Crear parte con campos mejorados")
print("-" * 80)
try:
    new_id, codigo = add_parte_mejorado(
        USER, PASSWORD, SCHEMA,
        ot_id=1,
        red_id=1,
        tipo_trabajo_id=1,
        cod_trabajo_id=1,
        titulo='Test de parte mejorado',
        descripcion='Descripción original',
        descripcion_corta='Test corto',
        descripcion_larga='Este es un test detallado de la funcionalidad mejorada con todos los campos nuevos.',
        fecha_inicio='2025-10-29',
        fecha_prevista_fin='2025-10-30',
        id_estado=1,  # Pendiente
        localizacion='Oficina central - Sala de pruebas'
    )
    print(f"✅ Parte creado exitosamente:")
    print(f"   ID: {new_id}")
    print(f"   Código: {codigo}")
    print()
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)

# ============================================================================
# TEST 3: Modificar parte
# ============================================================================
print("TEST 3: Modificar parte (cambiar estado y fecha)")
print("-" * 80)
try:
    result = mod_parte_mejorado(
        USER, PASSWORD, SCHEMA,
        parte_id=new_id,
        id_estado=2,  # Cambiar a "En curso"
        fecha_inicio='2025-10-29',
        localizacion='Oficina central - En ejecución'
    )
    if result == "ok":
        print(f"✅ Parte {codigo} modificado exitosamente")
        print(f"   Estado cambiado a: En curso")
    else:
        print(f"⚠️  Resultado: {result}")
    print()
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)

# ============================================================================
# TEST 4: Finalizar parte
# ============================================================================
print("TEST 4: Finalizar parte")
print("-" * 80)
try:
    result = mod_parte_mejorado(
        USER, PASSWORD, SCHEMA,
        parte_id=new_id,
        id_estado=3,  # Finalizada
        fecha_fin='2025-10-29'
    )
    if result == "ok":
        print(f"✅ Parte {codigo} finalizado exitosamente")
    else:
        print(f"⚠️  Resultado: {result}")
    print()
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)

# ============================================================================
# TEST 5: Listar partes mejorados
# ============================================================================
print("TEST 5: Listar partes con campos mejorados")
print("-" * 80)
try:
    partes = list_partes_mejorado(USER, PASSWORD, SCHEMA, limit=5)
    print(f"✅ {len(partes)} partes encontrados (mostrando últimos):")
    for i, p in enumerate(partes, 1):
        print(f"\n   {i}. {p.get('codigo')} - {p.get('titulo', 'Sin título')[:40]}")
        print(f"      Estado: {p.get('estado', 'N/A')}")
        print(f"      Fechas: {p.get('fecha_inicio') or 'N/A'} → {p.get('fecha_fin') or 'N/A'}")
        print(f"      Localización: {p.get('localizacion', 'N/A')[:50]}")
        if p.get('dias_duracion'):
            print(f"      Duración: {p.get('dias_duracion')} días")
    print()
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)

# ============================================================================
# RESUMEN
# ============================================================================
print("=" * 80)
print("  RESUMEN DE TESTS")
print("=" * 80)
print("✅ TEST 1: Obtener estados - OK")
print("✅ TEST 2: Crear parte mejorado - OK")
print("✅ TEST 3: Modificar parte - OK")
print("✅ TEST 4: Finalizar parte - OK")
print("✅ TEST 5: Listar partes mejorados - OK")
print()
print("🎉 TODOS LOS TESTS COMPLETADOS EXITOSAMENTE")
print()
print(f"Parte de prueba creado: {codigo} (ID: {new_id})")
print("Puedes verificarlo en MySQL o eliminarlo si deseas.")
print()
```

Guarda el archivo (Ctrl+O, Enter, Ctrl+X) y ejecuta:

```bash
chmod +x test_partes_mejorados.py
python test_partes_mejorados.py
```

**Output esperado:**
```
================================================================================
  TEST DE FUNCIONES MEJORADAS DE PARTES
================================================================================

TEST 1: Obtener estados disponibles
--------------------------------------------------------------------------------
✅ 5 estados encontrados:
   1. Pendiente        - Parte pendiente de iniciar
   2. En curso         - Parte en ejecución
   3. Finalizada       - Parte completada con éxito
   4. Cancelada        - Parte cancelada
   5. Suspendida       - Parte temporalmente suspendida

TEST 2: Crear parte con campos mejorados
--------------------------------------------------------------------------------
✅ Parte creado exitosamente:
   ID: 123
   Código: PT-00123

TEST 3: Modificar parte (cambiar estado y fecha)
--------------------------------------------------------------------------------
✅ Parte PT-00123 modificado exitosamente
   Estado cambiado a: En curso

TEST 4: Finalizar parte
--------------------------------------------------------------------------------
✅ Parte PT-00123 finalizado exitosamente

TEST 5: Listar partes con campos mejorados
--------------------------------------------------------------------------------
✅ 5 partes encontrados (mostrando últimos):

   1. PT-00123 - Test de parte mejorado
      Estado: Finalizada
      Fechas: 2025-10-29 → 2025-10-29
      Localización: Oficina central - En ejecución
      Duración: 0 días

   [... otros partes ...]

================================================================================
  RESUMEN DE TESTS
================================================================================
✅ TEST 1: Obtener estados - OK
✅ TEST 2: Crear parte mejorado - OK
✅ TEST 3: Modificar parte - OK
✅ TEST 4: Finalizar parte - OK
✅ TEST 5: Listar partes mejorados - OK

🎉 TODOS LOS TESTS COMPLETADOS EXITOSAMENTE

Parte de prueba creado: PT-00123 (ID: 123)
Puedes verificarlo en MySQL o eliminarlo si deseas.
```

---

## 📋 PASO 8: VERIFICAR EN MYSQL EL PARTE DE PRUEBA

```sql
USE cert_dev;

-- Ver el parte creado por Python
SELECT *
FROM vw_partes_completo
WHERE titulo = 'Test de parte mejorado'\G
```

**Debe mostrar todos los campos** con los valores que pasaste en Python.

✅ **Integración Python ↔ MySQL funciona correctamente**

---

## 📋 PASO 9: (OPCIONAL) LIMPIAR PARTE DE PRUEBA

Si quieres eliminar el parte de test:

```sql
DELETE FROM tbl_partes
WHERE titulo = 'Test de parte mejorado';

-- Verificar eliminación
SELECT COUNT(*) FROM tbl_partes WHERE titulo = 'Test de parte mejorado';
-- Debe devolver 0
```

---

## ✅ CHECKLIST FINAL

Marca lo que has verificado:

- [ ] Backup realizado
- [ ] Migración ejecutada sin errores
- [ ] Tabla `tbl_parte_estados` creada con 5 estados
- [ ] 10-11 campos nuevos en `tbl_partes`
- [ ] Vista `vw_partes_completo` existe
- [ ] 2 Triggers creados
- [ ] 6 Índices nuevos creados
- [ ] Datos antiguos migrados (títulos generados)
- [ ] Sin pérdida de registros
- [ ] Trigger de finalizada → estado funciona
- [ ] Trigger de estado → finalizada funciona
- [ ] Función `get_estados_parte()` funciona
- [ ] Función `add_parte_mejorado()` funciona
- [ ] Función `mod_parte_mejorado()` funciona
- [ ] Función `list_partes_mejorado()` funciona

---

## 🎉 SI TODO ESTÁ ✅

**¡MIGRACIÓN EXITOSA!**

Ahora puedes:
1. **Aplicar a más proyectos** (si tienes varios):
   ```bash
   python script/migrate_partes_mejoras.py --user USER --password PASS
   ```

2. **Continuar con las interfaces** (siguiente fase)

3. **Usar las nuevas funciones** en tu código

---

## ❌ SI ALGO FALLÓ

### Restaurar desde Backup

```bash
# Restaurar esquema completo
mysql -u tu_usuario -p cert_dev < backup_cert_dev_antes_migracion.sql

# Verificar restauración
mysql -u tu_usuario -p -e "USE cert_dev; SELECT COUNT(*) FROM tbl_partes;"
```

### Revisar Logs

El script Python muestra errores detallados. Los más comunes:

1. **"Access denied"** → Credenciales incorrectas
2. **"Table doesn't exist"** → Esquema sin sistema de partes (normal)
3. **"Duplicate column"** → Migración ya aplicada (OK, es idempotente)

---

## 📞 SIGUIENTE PASO

Una vez que hayas completado todos los checks, **avísame** y te prepararé:

1. **Documento de cambios en interfaces** con código específico
2. **Mockups de la nueva interfaz**
3. **Plan de implementación de interfaces**

---

**Preparado por**: Claude Code
**Fecha**: 29 de octubre de 2025
**Versión**: 1.0
