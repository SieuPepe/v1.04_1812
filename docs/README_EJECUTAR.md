# Cómo ejecutar las aplicaciones

## ⚠️ IMPORTANTE: Ejecutar desde la raíz del proyecto

Todos los scripts deben ejecutarse desde el directorio raíz del proyecto (`v1.04_1812`) para que los imports funcionen correctamente.

## 📝 Formularios de Partes

### Formulario Completo (Recomendado)
Incluye todos los campos de Fase 1 + Provincias y Municipios:

```powershell
# Desde PowerShell en el directorio raíz
python run_parts_form.py
```

**Características:**
- ✅ Código OT dinámico (GF/OT/TP con numeración independiente)
- ✅ Todos los campos: título, descripciones, fechas
- ✅ Selector de Provincia (Álava, Bizkaia, Gipuzkoa)
- ✅ Selector de Municipio (filtrado por provincia, searchable)
- ✅ Estado, localización, etc.

### Formulario Simple
Solo campos básicos (RED, TIPO, CÓDIGO):

```powershell
python run_parts_simple.py
```

**Características:**
- ✅ Código OT dinámico (GF/OT/TP con numeración independiente)
- ✅ Campos básicos: Red, Tipo de trabajo, Código de trabajo
- ✅ Descripción opcional
- ⚠️ No incluye campos de ubicación ni provincias

## 🔧 Configuración

### Credenciales de Base de Datos

Edita los archivos `run_parts_form.py` o `run_parts_simple.py` para cambiar las credenciales:

```python
USER = "root"
PASSWORD = "TuPasswordAqui"
SCHEMA = "cert_dev"
```

### Requisitos previos

1. **Base de datos configurada:**
   - Ejecutar `script/fase2_provincias_municipios.sql` (ya hecho)
   - Verificar que existan las tablas: `dim_provincias`, `tbl_municipios`

2. **Dependencias Python instaladas:**
   ```powershell
   pip install customtkinter CTkMessagebox tkcalendar mysql-connector-python
   ```

## ❌ Error común

**Si ves este error:**
```
ModuleNotFoundError: No module named 'script'
```

**Causa:** Estás ejecutando el archivo directamente desde la carpeta `interface/`

**Solución:** Ejecuta desde la raíz del proyecto usando los scripts de entrada:
```powershell
# MAL (desde interface/)
cd interface
python parts_interfaz_v2_fixed.py  # ❌ Error

# BIEN (desde raíz)
cd D:\Dev\HFM\v1.04_1812
python run_parts_form.py  # ✅ Funciona
```

## 🗂️ Estructura del proyecto

```
v1.04_1812/
├── run_parts_form.py          # ⭐ Ejecutar formulario completo
├── run_parts_simple.py         # ⭐ Ejecutar formulario simple
├── interface/
│   ├── parts_interfaz_v2_fixed.py    # Formulario completo
│   └── parts_interfaz.py              # Formulario simple
├── script/
│   ├── db_partes.py                   # Funciones de base de datos
│   ├── modulo_db.py                   # Exports
│   └── fase2_provincias_municipios.sql
└── README_EJECUTAR.md          # Este archivo
```

## 🐛 Troubleshooting

### Error: mysql-connector no encontrado
```powershell
pip install mysql-connector-python
```

### Error: customtkinter no encontrado
```powershell
pip install customtkinter
```

### Error: No se puede conectar a MySQL
- Verifica que MySQL esté ejecutándose
- Revisa las credenciales en el script de entrada
- Verifica que la base de datos `cert_dev` exista

### La ventana no se abre
- Verifica que estés en el entorno virtual correcto:
  ```powershell
  conda activate hydroflow
  ```
- Ejecuta desde la raíz del proyecto

## 📊 Verificar que la base de datos está lista

```sql
-- Conectar a MySQL y ejecutar:
USE cert_dev;

-- Verificar provincias (debe mostrar 3 filas)
SELECT * FROM dim_provincias;

-- Verificar municipios de Álava (debe mostrar 51 filas)
SELECT COUNT(*) FROM tbl_municipios WHERE provincia_id = 1;

-- Verificar municipios de Bizkaia (debe mostrar ~115 filas)
SELECT COUNT(*) FROM tbl_municipios WHERE provincia_id = 2;
```

## ✅ Todo funcionando correctamente

Si ejecutas desde la raíz con `python run_parts_form.py` deberías ver:
1. Ventana del formulario
2. Selector de Provincia con 3 opciones
3. Selector de Municipio que se actualiza según la provincia
4. Campo "Código OT" que se actualiza al cambiar el Tipo de Trabajo
