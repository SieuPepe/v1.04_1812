# 🚀 Inicio Rápido - Prueba de Migración

Esta guía te ayudará a probar la migración de mejoras de partes de forma rápida y sencilla.

## 📋 Prerrequisitos

- ✅ Backup completado: `backup_cert_dev_antes_migracion.sql`
- ✅ Base de datos MySQL corriendo en localhost:3307
- ✅ Esquema de prueba identificado (ej: `cert_dev`)
- ✅ Credenciales de MySQL disponibles

## 🎯 Opción 1: Prueba Automática Completa (RECOMENDADO)

Esta es la forma más rápida y completa. Un solo comando ejecuta todo el proceso:

```bash
# Ejecutar desde el directorio raíz del proyecto
python script/test_migration_complete.py \
    --user root \
    --password tu_password \
    --schema cert_dev
```

### ¿Qué hace este script?

1. ✅ Verifica que el esquema existe
2. ✅ Verifica que existe `tbl_partes`
3. ✅ Muestra el estado PRE-migración
4. ✅ Ejecuta la migración SQL
5. ✅ Verifica el estado POST-migración
6. ✅ Prueba las funciones Python
7. ✅ Muestra un resumen completo

### Resultado esperado

```
================================================================================
  RESUMEN FINAL
================================================================================

🎉 ¡TODAS LAS VERIFICACIONES PASARON CON ÉXITO!

✅ Migración completada correctamente
✅ Todas las estructuras creadas
✅ Funciones Python funcionando

📝 Próximos pasos:
   1. Revisar los resultados de las verificaciones
   2. Probar las funciones Python con datos reales
   3. Aplicar migración a otros esquemas si todo está OK
   4. Implementar cambios en interfaces de usuario
```

---

## 🎯 Opción 2: Verificación Manual con SQL

Si prefieres verificar manualmente en MySQL Workbench:

### Paso 1: Ejecutar migración manualmente

```bash
python script/migrate_partes_mejoras.py \
    --user root \
    --password tu_password \
    --schema cert_dev
```

### Paso 2: Verificar en MySQL Workbench

1. Abre MySQL Workbench
2. Conecta a tu base de datos
3. Ejecuta: `USE cert_dev;`
4. Abre el archivo: `script/verificar_migracion.sql`
5. Ejecuta cada sección y verifica los resultados

---

## 🎯 Opción 3: Dry-Run (Simulación sin cambios)

Si quieres ver qué haría la migración sin ejecutarla:

```bash
python script/migrate_partes_mejoras.py \
    --user root \
    --password tu_password \
    --dry-run
```

Esto mostrará los esquemas que se migrarían sin hacer cambios reales.

---

## 📊 ¿Qué se crea en la migración?

### 1. Nueva tabla: `tbl_parte_estados`
- 5 estados predefinidos: Pendiente, En curso, Finalizada, Cancelada, Suspendida

### 2. Nuevas columnas en `tbl_partes`:
- `titulo` - Título descriptivo
- `descripcion_larga` - Descripción detallada
- `descripcion_corta` - Resumen breve
- `fecha_inicio` - Fecha de inicio
- `fecha_fin` - Fecha de finalización
- `fecha_prevista_fin` - Fecha estimada
- `id_estado` - Estado actual (FK)
- `finalizada` - Booleano (compatibilidad Access)
- `localizacion` - Ubicación textual
- `id_municipio` - Municipio (FK opcional)

### 3. Vista: `vw_partes_completo`
- Consulta mejorada con todos los campos legibles

### 4. Triggers:
- `trg_partes_sync_finalizada_insert` - Sincroniza al insertar
- `trg_partes_sync_finalizada_update` - Sincroniza al actualizar

### 5. Índices (6 nuevos):
- Optimización de consultas frecuentes

---

## 🐍 Nuevas Funciones Python

Después de la migración, tendrás disponibles:

```python
from script.modulo_db import (
    get_estados_parte,
    add_parte_mejorado,
    mod_parte_mejorado,
    list_partes_mejorado
)

# Obtener lista de estados
estados = get_estados_parte(user, password, schema)

# Crear parte con nuevos campos
parte_id, msg = add_parte_mejorado(
    user, password, schema,
    ot_id=1, red_id=1, tipo_trabajo_id=1, cod_trabajo_id=1,
    titulo="Reparación urgente",
    descripcion_corta="Fuga en tubería principal",
    fecha_inicio="2025-10-29",
    id_estado=2,  # En curso
    localizacion="Calle Mayor 123"
)

# Listar partes con nuevos campos
partes = list_partes_mejorado(user, password, schema, limit=10)
```

---

## ⚠️ Troubleshooting

### Error: "Table tbl_partes doesn't exist"
**Solución**: El esquema no tiene tabla de partes. Usa otro esquema o crea la estructura base primero.

### Error: "Duplicate column name"
**Solución**: La migración ya fue aplicada. Usa `--skip-migration` en el test script.

### Error: "Access denied"
**Solución**: Verifica usuario y contraseña de MySQL.

### La migración parece no hacer nada
**Respuesta**: El script es idempotente. Si las columnas ya existen, simplemente las mantiene.

---

## 📞 Próximos Pasos

Una vez que la migración funcione correctamente:

1. ✅ **Aplicar a otros esquemas**: Ejecuta sin `--schema` para migrar todos
2. ✅ **Implementar interfaces**: Actualizar formularios de partes
3. ✅ **Pruebas en producción**: Probar con usuarios reales
4. ✅ **Continuar con Fase 2**: Implementar siguientes mejoras

---

## 📚 Documentación Completa

- `GUIA_PRUEBA_MIGRACION.md` - Guía detallada paso a paso (712 líneas)
- `MEJORAS_PARTES_README.md` - Documentación técnica completa (539 líneas)
- `script/verificar_migracion.sql` - Queries de verificación manual
- `script/test_migration_complete.py` - Script de prueba automática

---

## 💾 Revertir la Migración (si es necesario)

Si algo sale mal y necesitas revertir:

```bash
# Restaurar desde backup
mysql -u root -p cert_dev < backup_cert_dev_antes_migracion.sql
```

---

¡Listo para empezar! 🚀

**Comando recomendado para iniciar:**

```bash
python script/test_migration_complete.py --user root --password tu_password --schema cert_dev
```
