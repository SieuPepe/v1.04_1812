# Verificación de Integridad de Datos

## Descripción

Script para verificar la integridad de datos de partes y presupuestos en la base de datos.

## Problema Resuelto: Esquema cert_dev no aparece

### Causa

El esquema `cert_dev` estaba siendo filtrado intencionalmente en el archivo `interface/select_project_interfaz.py`.

### Solución Aplicada

Se eliminó `"cert_dev"` de la lista de esquemas excluidos en la línea 29 del archivo:

**Antes:**
```python
schema_filter = [elemento for elemento in schemas if all(exclude not in elemento for exclude in ["power_bi","cert_dev","_schema", "manager", "mysql", "sys"])]
```

**Después:**
```python
schema_filter = [elemento for elemento in schemas if all(exclude not in elemento for exclude in ["power_bi","_schema", "manager", "mysql", "sys"])]
```

Ahora el esquema `cert_dev` aparecerá en la lista de proyectos disponibles al arrancar la aplicación.

## Script de Verificación de Integridad

### Ubicación

`script/verificar_integridad_completa.py`

### Funcionalidades

El script verifica:

#### 1. Integridad de Partes (tbl_partes)
- ✓ Partes con código válido
- ✓ Fechas consistentes (fecha_fin >= fecha_inicio)
- ✓ Referencias a municipios válidas
- ✓ Estados válidos
- ✓ Distribución por estado

#### 2. Integridad de Presupuestos (tbl_presupuesto)
- ✓ Presupuestos con partida asignada
- ✓ Referencias a partidas válidas
- ✓ Cantidades válidas (> 0)
- ✓ Grupos asignados

#### 3. Integridad de Relación Partes-Presupuesto (tbl_part_presupuesto)
- ✓ Referencias a partes válidas
- ✓ Referencias a presupuestos válidas
- ✓ Fechas de certificación
- ✓ Cantidades certificadas vs presupuestadas
- ✓ Partes con/sin presupuesto

#### 4. Consistencia General
- ✓ Códigos de partes duplicados
- ✓ Rangos de fechas
- ✓ Datos huérfanos

### Uso

#### Verificar esquema cert_dev (predeterminado)
```bash
python3 script/verificar_integridad_completa.py
```

#### Verificar otro esquema
```bash
python3 script/verificar_integridad_completa.py PR001
```

### Requisitos Previos

**IMPORTANTE:** El servidor MySQL debe estar corriendo en el puerto 3307.

Para iniciar MySQL:
```bash
# En Windows
net start MySQL

# O desde MySQL Workbench o XAMPP

# Verificar que está corriendo
netstat -an | findstr 3307
```

### Salida del Script

El script muestra:

1. **Verificación de tablas**: Confirma que existen todas las tablas necesarias
2. **Estadísticas**: Conteo de registros por tabla
3. **Verificaciones de integridad**: Resultados detallados por categoría
4. **Resumen final**: Errores críticos y advertencias

#### Tipos de Mensajes

- ✓ **Verde/Check**: Verificación exitosa
- ✗ **Rojo/Cruz**: Error crítico que debe corregirse
- ⚠ **Amarillo/Advertencia**: Advertencia, no crítico pero debe revisarse
- ℹ **Información**: Datos informativos

### Ejemplo de Salida

```
======================================================================
VERIFICACIÓN DE INTEGRIDAD DE DATOS
Partes y Presupuestos
======================================================================

Esquema a verificar: cert_dev
✓ Conectado al esquema: cert_dev

=== VERIFICANDO EXISTENCIA DE TABLAS ===
  ✓ tbl_partes
  ✓ tbl_part_presupuesto
  ✓ tbl_presupuesto
  ✓ tbl_pres_precios
  ✓ tbl_parte_estados
  ✓ dim_municipios

=== ESTADÍSTICAS DE TABLAS ===
  Partes                             :    150 registros
  Partes-Presupuesto (relación)      :    450 registros
  Presupuesto                        :    120 registros
  Precios de partidas                :     80 registros

[... verificaciones detalladas ...]

======================================================================
RESUMEN DE VERIFICACIÓN DE INTEGRIDAD
======================================================================

  ✓ ¡NO SE ENCONTRARON PROBLEMAS!
  ✓ La integridad de los datos es correcta

======================================================================
```

### Código de Salida

- `0`: Verificación exitosa, sin errores críticos
- `1`: Se encontraron errores críticos

Esto permite usar el script en pipelines de CI/CD:

```bash
python3 script/verificar_integridad_completa.py cert_dev
if [ $? -eq 0 ]; then
    echo "Integridad verificada correctamente"
else
    echo "Se encontraron problemas de integridad"
    exit 1
fi
```

## Notas Importantes

1. **Conexión a la BD**: El script usa credenciales por defecto (localhost:3307, root). Puede modificarse en el código si es necesario.

2. **Advertencias vs Errores**:
   - **Errores**: Problemas de integridad referencial que pueden causar fallos en la aplicación
   - **Advertencias**: Inconsistencias que no afectan funcionamiento pero deben revisarse

3. **Performance**: El script está optimizado con índices. Para esquemas grandes puede tardar algunos segundos.

## Solución de Problemas

### Error: Can't connect to MySQL server on 'localhost:3307'

**Causa**: El servidor MySQL no está corriendo o no está escuchando en el puerto 3307.

**Solución**:
1. Verificar que MySQL esté corriendo
2. Verificar el puerto con: `netstat -an | findstr 3307`
3. Si está en otro puerto, modificar en el script

### Error: Access denied for user 'root'@'localhost'

**Causa**: Contraseña incorrecta o usuario sin permisos.

**Solución**:
1. Verificar credenciales en el script
2. Asegurarse de que el usuario tenga permisos de lectura en el esquema

### Error: Unknown database 'cert_dev'

**Causa**: El esquema no existe.

**Solución**:
1. Verificar esquemas disponibles: `SHOW DATABASES;`
2. Usar el nombre correcto del esquema como parámetro

## Mantenimiento

Para agregar nuevas verificaciones, editar el archivo y añadir métodos en la clase `IntegrityChecker`.

Ejemplo:
```python
def verify_nueva_tabla_integrity(self):
    """Verifica integridad de nueva_tabla"""
    print("\n=== VERIFICANDO NUEVA TABLA ===")
    # ... tu código aquí
```

Luego añadir la llamada en `run_all_checks()`.
