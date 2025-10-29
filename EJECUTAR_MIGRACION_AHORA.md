# ✅ INSTRUCCIONES: Ejecutar Migración (CORREGIDA)

## 🔍 ¿Qué Pasó?

El script de prueba automático **intentó ejecutar la migración**, pero falló porque:
1. Tu MySQL no soporta la sintaxis `ADD COLUMN IF NOT EXISTS` (solo MariaDB)
2. Había un bug en la función Python `get_estados_parte()`

## ✅ ¿Qué Se Corrigió?

1. ✅ **Nuevo script SQL compatible**: `mejoras_tabla_partes_mysql.sql`
   - Usa procedimientos almacenados para verificar columnas
   - Compatible con MySQL 5.7+

2. ✅ **Bug en Python corregido**: `db_partes.py`
   - `get_estados_parte()` ahora devuelve diccionarios en lugar de tuplas

## 🚀 PASOS PARA EJECUTAR LA MIGRACIÓN

### Opción 1: Script Automático (RECOMENDADO)

```powershell
# Desde PowerShell en D:\Dev\HFM\v1.04_1812
python script\ejecutar_migracion_manual.py --user root --password TU_PASSWORD --schema cert_dev
```

**Reemplaza**:
- `root` con tu usuario de MySQL
- `TU_PASSWORD` con tu contraseña
- `cert_dev` con tu esquema de prueba

Este script:
- ✅ Lee el SQL compatible
- ✅ Ejecuta comando por comando
- ✅ Muestra progreso en tiempo real
- ✅ Maneja errores benignos automáticamente
- ✅ Genera reporte final

---

### Opción 2: MySQL Workbench (Manual)

1. Abre MySQL Workbench
2. Conecta a tu base de datos
3. Ejecuta:
   ```sql
   USE cert_dev;
   ```
4. Abre el archivo: `script/mejoras_tabla_partes_mysql.sql`
5. Ejecuta todo el script (⚡ botón "Execute")
6. Revisa los mensajes

---

## 📊 Resultado Esperado

### ✅ Si Todo Va Bien:

```
================================================================================
📊 RESUMEN DE EJECUCIÓN
================================================================================
✅ Comandos exitosos: 50+
⚠️  Advertencias: 2-3 (normales: "Ya existe", "Tabla opcional")
❌ Errores críticos: 0

🎉 ¡MIGRACIÓN COMPLETADA CON ÉXITO!
```

### ⚠️ Si Hay Problemas:

El script te mostrará:
- Qué comando falló
- El mensaje de error específico
- Sugerencia de cómo revertir

---

## 🔍 Verificar que Funcionó

Después de ejecutar la migración, verifica:

```powershell
# Ejecutar test SIN migración (solo verificar)
python script\test_migration_complete.py --user root --password TU_PASSWORD --schema cert_dev --skip-migration
```

Deberías ver:
```
✅ Migración completada correctamente
✅ Todas las estructuras creadas
✅ Funciones Python funcionando
```

---

## 🔄 Si Necesitas Revertir

Si algo sale mal:

```powershell
# Desde PowerShell
mysql -u root -p cert_dev < backup_cert_dev_antes_migracion.sql
```

Luego puedes reintentar la migración.

---

## 📝 ¿Qué Se Creará?

La migración añadirá a tu esquema `cert_dev`:

### 1. Tabla nueva: `tbl_parte_estados`
- 5 estados: Pendiente, En curso, Finalizada, Cancelada, Suspendida

### 2. Columnas nuevas en `tbl_partes`:
- ✅ `titulo` - Título descriptivo
- ✅ `descripcion_larga` - Descripción detallada
- ✅ `descripcion_corta` - Resumen breve
- ✅ `fecha_inicio` - Fecha de inicio
- ✅ `fecha_fin` - Fecha de finalización
- ✅ `fecha_prevista_fin` - Fecha estimada
- ✅ `id_estado` - Estado actual (FK)
- ✅ `finalizada` - Booleano de finalización
- ✅ `localizacion` - Ubicación textual
- ✅ `id_municipio` - Municipio (FK opcional)

### 3. Vista: `vw_partes_completo`
- Consulta mejorada con JOINs

### 4. Triggers (2):
- Sincronización automática entre `finalizada` y `id_estado`

### 5. Índices (6):
- Optimización de consultas

---

## 🎯 COMANDO PARA COPIAR Y PEGAR

```powershell
python script\ejecutar_migracion_manual.py --user root --password TU_PASSWORD --schema cert_dev
```

**¡Ejecuta este comando ahora!** 🚀

---

## 📞 Después de la Migración

Una vez que la migración funcione correctamente:

1. ✅ Verifica con el test: `python script\test_migration_complete.py ... --skip-migration`
2. ✅ Prueba las funciones Python
3. ✅ Aplica a otros esquemas si todo está OK
4. ✅ Implementa cambios en interfaces

---

## ⚠️ Notas Importantes

- La migración es **idempotente**: si ya existen algunas columnas, las mantiene
- Los **triggers automáticos** sincronizan `finalizada` con `id_estado`
- La **vista** facilita consultas legibles
- Los **índices** mejoran el rendimiento

---

¿Listo? **Copia y pega el comando de arriba** y ejecuta la migración. 🚀
