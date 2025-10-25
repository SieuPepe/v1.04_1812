# ADR 0004: Reglas de Negocio Identificadas en el Sistema Actual

**Fecha:** 2025-10-25
**Estado:** Documentado (basado en análisis del código existente)
**Autores:** Claude Code, SieuPepe

---

## Contexto

Durante el Event Storming se identificaron 4 **Hotspots** (reglas de negocio críticas) que requerían clarificación.
Se realizó análisis exhaustivo del código existente para descubrir cómo funciona actualmente el sistema.

---

## Análisis del Código Actual

### Archivos Analizados
- `/v1.04_1812/script/db_projects.py` - Funciones de base de datos
- `/v1.04_1812/interface/manager_project_interfaz.py` - Interfaz principal
- `/backup/backup_estructuraBBDD.sql` - Esquema de base de datos

---

## HALLAZGO 1: Cantidad Certificada vs Presupuestada

### Pregunta Original
¿Qué ocurre si se intenta certificar más cantidad de la presupuestada?

### Hallazgos del Código

**Estructura de Datos:**
```sql
-- Tabla de presupuesto
CREATE TABLE tbl_presupuesto (
  id int,
  id_partida int,
  cantidad double,        -- Cantidad PRESUPUESTADA
  ...
)

-- Tabla de certificación
CREATE TABLE tbl_pres_certificacion (
  id int,
  id_partida int,
  cantidad_certificada double,  -- Cantidad CERTIFICADA
  certificada int,              -- 0=no, 1=si
  ...
)
```

**Funciones de Certificación (db_projects.py):**

```python
# Línea 979: add_cost_item
def add_cost_item(user, password, schema, data):
    """Añade un item a la tabla de certificación"""
    sql_query = """
        INSERT INTO tbl_pres_certificacion
        (id_partida, cantidad_certificada, ...)
        VALUES (%s, %s, ...)
    """
    # ❌ NO HAY VALIDACIÓN de cantidad_certificada <= cantidad_presupuestada
    cursor.execute(sql_query, data_values)

# Línea 923: mod_amount_cost_item
def mod_amount_cost_item(user, password, schema, amount, id_item):
    """Modifica las cantidades de la tabla de certificaciones"""
    sql_query = """
        UPDATE tbl_pres_certificacion
        SET cantidad_certificada = %s
        WHERE id = %s
    """
    # ❌ NO HAY VALIDACIÓN de límites
    cursor.execute(sql_query, (amount, id_item))

# Línea 962: cert_cost_item
def cert_cost_item(user, password, schema, id_item):
    """Certifica un item"""
    sql_query = """
        UPDATE tbl_pres_certificacion
        SET certificada = 1, fecha_certificacion=NOW()
        WHERE id = %s
    """
    # ❌ NO HAY VALIDACIÓN antes de certificar
    cursor.execute(sql_query)
```

**Búsqueda de Validaciones:**
- Patrón buscado: `if cantidad_certificada <= cantidad_presupuestada`
- Resultado: **NO ENCONTRADO**
- Única validación: `if cantidad <= 0` (solo valida positivo)

### Decisión Actual del Sistema

**RESPUESTA: C) Sin Validación - Permite Sobre-Certificación**

El sistema actual **NO valida** que cantidad_certificada ≤ cantidad_presupuestada.

### Implicaciones

**Positivas:**
- Flexibilidad para certificar trabajo adicional
- No bloquea flujo si hubo cambios en obra

**Negativas:**
- ❌ Riesgo de sobre-facturación sin control
- ❌ Presupuesto puede ser irrelevante
- ❌ Difícil detectar errores de captura

### Recomendación para Modelo de Dominio

**Implementar en Clean Architecture:**

```python
class Certificación:
    def certificar_cantidad(
        self,
        cantidad: Decimal,
        cantidad_presupuestada: Decimal
    ) -> None:
        """
        Certifica cantidad con validación opcional.

        Business Rule:
        - ADVERTENCIA (warning) si cantidad > presupuestada
        - NO bloquea, solo alerta
        """
        if cantidad > cantidad_presupuestada:
            # Log warning pero permite continuar
            logger.warning(
                f"Sobre-certificación detectada: {cantidad} > {cantidad_presupuestada}"
            )

        self.cantidad_certificada = cantidad
        self.importe_certificado = self._calcular_importe()
```

**Rationale:** Mantener flexibilidad actual pero añadir visibilidad mediante logging.

---

## HALLAZGO 2: Eliminación de Registros/Partidas

### Pregunta Original
¿Se puede eliminar un registro/partida que tiene presupuestos/certificaciones?

### Hallazgos del Código

**Funciones de Eliminación (db_projects.py):**

```python
# Línea 902: delete_budget_item
def delete_budget_item(user, password, schema, id_item):
    """Borra item de la tabla presupuesto"""
    sql_query = f"DELETE FROM {schema}.tbl_presupuesto WHERE id = {id_item}"
    # ❌ NO HAY VALIDACIÓN previa
    cursor.execute(sql_query)
    conexion.commit()

# Línea 941: delete_cost_item
def delete_cost_item(user, password, schema, id_item):
    """Borra item de la tabla de certificación"""
    sql_query = f"DELETE FROM {schema}.tbl_pres_certificacion WHERE id = {id_item}"
    # ❌ NO HAY VALIDACIÓN de estado 'certificada'
    cursor.execute(sql_query)
    conexion.commit()
```

**Interfaz de Usuario (manager_project_interfaz.py línea 3319):**

```python
def delete_cost_event_no_cert(self, i, select_data):
    id_bd = self.id_bd_items_no_cert[i - 1]
    # ❌ NO HAY confirmación o validación
    result = delete_cost_item(...)
    # Reinicia frame directamente
```

**Búsqueda de Validaciones:**
- Patrón: `if estado`, `if certificada`, `confirm`, `validate`
- Resultado: **NO ENCONTRADO**
- NO hay validación de dependencias antes de DELETE

### Decisión Actual del Sistema

**RESPUESTA: C) Hard Delete sin Validaciones**

El sistema actual ejecuta **DELETE directo** sin:
- ✗ Verificar dependencias
- ✗ Verificar estado (certificada/no certificada)
- ✗ Confirmación explícita
- ✗ Soft delete (mantener histórico)

### Implicaciones

**Negativas:**
- ❌ Pérdida de datos irreversible
- ❌ Puede romper integridad referencial
- ❌ No hay auditoría de eliminaciones
- ❌ Imposible recuperar datos eliminados por error

### Recomendación para Modelo de Dominio

**Implementar en Clean Architecture:**

```python
class Certificación:
    def puede_eliminarse(self) -> bool:
        """
        Verifica si la certificación puede eliminarse.

        Business Rules:
        - NO permitir eliminar si certificada (certificada=1)
        - Permitir eliminar si borrador (certificada=0)
        """
        if self.estado == EstadoCertificacion.CERTIFICADA:
            raise CertificacionCertificadaError(
                "No se puede eliminar una certificación ya certificada"
            )
        return True

    def eliminar(self) -> None:
        """Elimina la certificación si es posible."""
        self.puede_eliminarse()  # Valida primero
        # Marcar como eliminada (soft delete preferible)
        self.deleted_at = datetime.now()
```

**Rationale:** Añadir validaciones para prevenir pérdida accidental de datos certificados.

---

## HALLAZGO 3: Precios del Catálogo en Presupuestos

### Pregunta Original
Cuando se actualiza el precio del catálogo, ¿afecta a presupuestos existentes?

### Hallazgos del Código

**Estructura de Datos:**

```sql
-- Catálogo de precios (maestro)
CREATE TABLE tbl_pres_precios (
  id int,
  codigo text,
  coste double,         -- PRECIO UNITARIO EN CATÁLOGO
  ...
)

-- Presupuesto del proyecto
CREATE TABLE tbl_presupuesto (
  id int,
  id_partida int,       -- FK → tbl_pres_precios
  cantidad double,
  -- ❌ NO HAY: precio_unitario, precio_snapshot, precio_copia
  ...
)

-- Certificación
CREATE TABLE tbl_pres_certificacion (
  id int,
  id_partida int,       -- FK → tbl_pres_precios
  cantidad_certificada double,
  -- ❌ NO HAY: precio_unitario guardado
  ...
)
```

**Función de Añadir al Presupuesto (db_projects.py línea 1067):**

```python
def add_budget_item(user, password, schema, data):
    """Añade item al presupuesto del proyecto"""
    sql_query = """
        INSERT INTO tbl_presupuesto
        (id_partida, cantidad, id_proyecto, id_arqueta, grupo)
        VALUES (%s, %s, %s, %s, %s)
    """
    # ✅ Solo guarda: id_partida (FK), NO precio
    # El precio se obtiene mediante JOIN en consultas
```

**Consultas de Lectura (db_core.py línea 418):**

```python
sql_query = """
    SELECT
        p.id,
        p.codigo,
        COALESCE(gp.coste, p.coste) AS coste_total,  -- JOIN para obtener precio
        b.cantidad
    FROM tbl_presupuesto b
    INNER JOIN tbl_pres_precios p ON b.id_partida = p.id
    ...
"""
# ✅ El precio se lee SIEMPRE del catálogo en tiempo de consulta
```

### Decisión Actual del Sistema

**RESPUESTA: B) Referencia Dinámica (FK) - Cambios Retroactivos**

El sistema actual:
- **NO copia** el precio al crear el presupuesto
- **Solo guarda** id_partida (Foreign Key)
- **Obtiene precio** mediante JOIN en tiempo de lectura
- **Cambios en catálogo** afectan a presupuestos antiguos automáticamente

### Implicaciones

**Positivas:**
- ✅ Precios siempre actualizados
- ✅ No hay duplicación de datos
- ✅ Mantenimiento centralizado

**Negativas:**
- ❌ NO hay histórico de precios
- ❌ Presupuesto certificado puede cambiar retrospectivamente
- ❌ Imposible auditar precio en momento de certificación
- ❌ Riesgo legal: el precio certificado puede diferir del momento de certificación

### Ejemplo del Problema

```
1. Enero 2025: Presupuesto creado con Válvula (id=123) a 50€
2. Marzo 2025: Certificación de 10 válvulas = 500€
3. Junio 2025: Precio de válvula actualizado en catálogo a 60€
4. Julio 2025: Consulta de certificación = 10 × 60€ = 600€ (❌ CAMBIÓ)
```

### Recomendación para Modelo de Dominio

**Implementar en Clean Architecture:**

```python
@dataclass
class PartidaPresupuesto:
    """
    Entity: Partida de presupuesto.

    Business Rule: SNAPSHOT del precio en momento de creación.
    """
    id: UUID
    codigo: str
    precio_unitario: Money  # ✅ COPIAR precio al crear (snapshot)
    precio_catalogo_ref: UUID  # ✅ Referencia al catálogo para comparación
    cantidad: Decimal
    subtotal: Money  # Calculado

    @classmethod
    def from_catalogo(
        cls,
        catalogo_ref: CatalogoPrecio,
        cantidad: Decimal
    ) -> "PartidaPresupuesto":
        """
        Crea partida desde catálogo.

        ✅ COPIA el precio (snapshot) en momento de creación.
        """
        return cls(
            id=uuid4(),
            codigo=catalogo_ref.codigo,
            precio_unitario=catalogo_ref.coste.copy(),  # SNAPSHOT
            precio_catalogo_ref=catalogo_ref.id,  # Referencia
            cantidad=cantidad,
            subtotal=catalogo_ref.coste * cantidad
        )

    def comparar_con_catalogo(
        self,
        catalogo: CatalogoPrecio
    ) -> Optional[Money]:
        """
        Compara precio guardado vs catálogo actual.

        Returns:
            Diferencia si hay cambio, None si es igual
        """
        if self.precio_unitario != catalogo.coste:
            return catalogo.coste - self.precio_unitario
        return None
```

**Rationale:**
- Guardar snapshot del precio para mantener histórico
- Mantener referencia al catálogo para detectar cambios
- Permite auditoría y cumplimiento legal

---

## HALLAZGO 4: Estados de Certificación

### Pregunta Original
¿Las certificaciones tienen estados (Borrador, Aprobada, Rechazada)?

### Hallazgos del Código

**Estructura de Datos:**

```sql
CREATE TABLE tbl_pres_certificacion (
  id int,
  id_partida int,
  cantidad_certificada double,
  fecha_certificacion datetime,
  certificada int,          -- ✅ Campo INT (0 o 1), NO estado textual
  ...
  -- ❌ NO HAY: estado VARCHAR, aprobada_por, rechazada, motivo_rechazo
)
```

**Función de Certificación (db_projects.py línea 962):**

```python
def cert_cost_item(user, password, schema, id_item):
    """Certifica un item"""
    sql_query = """
        UPDATE tbl_pres_certificacion
        SET certificada = 1,              -- Solo marca como 1
            fecha_certificacion = NOW()
        WHERE id = %s
    """
    # ✅ Simple: 0 → 1 (no certificada → certificada)
    # ❌ NO HAY: estados intermedios, aprobación, rechazo
```

**Interfaz de Usuario (manager_project_interfaz.py línea 3343):**

```python
# Clasificación de items en 2 tablas:
for sublist in items_cost:
    if sublist[-2] == 0:
        items_no_cert.append(sublist)  # TABLA 1: No certificadas
    else:
        items_cert.append(sublist)     # TABLA 2: Certificadas

# ✅ Solo 2 estados: 0 (no) o 1 (si)
```

**Búsqueda de Workflow:**
- Patrones buscados: `aprobar`, `rechazar`, `pending`, `approved`, `rejected`
- Resultado: **NO ENCONTRADO**
- NO hay funciones de aprobación/rechazo

### Decisión Actual del Sistema

**RESPUESTA: C) Estados Simples (Booleano 0/1)**

El sistema actual tiene **solo 2 estados**:
- `certificada = 0` → No certificada (borrador)
- `certificada = 1` → Certificada

**NO existe:**
- ✗ Estado "Aprobada"
- ✗ Estado "Rechazada"
- ✗ Estado "Pendiente de aprobación"
- ✗ Workflow de aprobación/rechazo
- ✗ Campo "aprobada_por"
- ✗ Fecha de aprobación separada

### Implicaciones

**Positivas:**
- ✅ Simplicidad
- ✅ Flujo rápido (sin aprobaciones)

**Negativas:**
- ❌ Sin control de autorización
- ❌ Cualquiera puede certificar sin aprobación
- ❌ No hay auditoría de quién aprobó
- ❌ Difícil implementar segregación de funciones

### Recomendación para Modelo de Dominio

**Implementar en Clean Architecture:**

```python
from enum import Enum

class EstadoCertificacion(Enum):
    """
    Estados de una certificación.

    Backward compatible con sistema actual:
    - BORRADOR = certificada 0
    - CERTIFICADA = certificada 1

    Nuevos estados para futuro:
    - PENDIENTE_APROBACION
    - APROBADA
    - RECHAZADA
    """
    BORRADOR = "borrador"              # certificada = 0
    CERTIFICADA = "certificada"        # certificada = 1
    # Futuros (no implementados en sistema actual):
    # PENDIENTE_APROBACION = "pendiente_aprobacion"
    # APROBADA = "aprobada"
    # RECHAZADA = "rechazada"

@dataclass
class Certificación:
    """
    Aggregate Root: Certificación.

    Implementa estados simples (compatible con sistema actual)
    pero preparado para expandir a workflow completo.
    """
    id: UUID
    estado: EstadoCertificacion
    aprobada_por: Optional[str] = None  # Futuro
    fecha_aprobacion: Optional[datetime] = None  # Futuro

    def certificar(self) -> None:
        """
        Marca como certificada.

        Sistema actual: Simple cambio de estado.
        Futuro: Podría requerir aprobación.
        """
        if self.estado != EstadoCertificacion.BORRADOR:
            raise EstadoInvalidoError("Solo se puede certificar desde borrador")

        self.estado = EstadoCertificacion.CERTIFICADA
        self.fecha_certificacion = datetime.now()

    def aprobar(self, usuario: str) -> None:
        """
        Aprueba la certificación (extensión futura).

        No implementado en sistema actual.
        """
        # Preparado para futuro workflow
        if self.estado != EstadoCertificacion.CERTIFICADA:
            raise EstadoInvalidoError("Solo se pueden aprobar certificaciones certificadas")

        # self.estado = EstadoCertificacion.APROBADA
        self.aprobada_por = usuario
        self.fecha_aprobacion = datetime.now()
```

**Rationale:** Mantener compatibilidad con sistema actual pero preparar para expansión futura.

---

## Decisiones Finales

### Para el Modelo de Dominio (Clean Architecture)

| Aspecto | Sistema Actual | Implementación Recomendada |
|---------|----------------|---------------------------|
| **Validación cantidad certificada** | Sin validación | ⚠️ Log warning si excede, pero permitir |
| **Eliminación de partidas** | DELETE directo | ✅ Validar estado antes de eliminar |
| **Precios en presupuesto** | FK dinámica (JOIN) | ✅ Snapshot + referencia para auditoría |
| **Estados de certificación** | Booleano (0/1) | ✅ Enum preparado para expansión |

### Principios de Diseño

1. **Backward Compatibility:**
   - Mantener comportamiento actual donde sea razonable
   - Mejorar con validaciones opcionales (warnings, no errores)

2. **Auditoría y Trazabilidad:**
   - Añadir campos de auditoría (created_by, updated_by)
   - Guardar snapshots de precios
   - Logging de operaciones críticas

3. **Extensibilidad:**
   - Diseñar para expansión futura (workflows, estados)
   - No romper flujo actual

4. **Seguridad de Datos:**
   - Soft delete preferible a hard delete
   - Validaciones para prevenir pérdida de datos

---

## Próximos Pasos

1. ✅ Actualizar DOMAIN_MODEL.md con estas decisiones
2. ✅ Implementar Value Objects con validaciones opcionales
3. ✅ Implementar Entities con snapshots de precios
4. ✅ Añadir logging para operaciones críticas
5. ✅ Crear tests que validen comportamiento backward-compatible

---

**Fecha de decisión:** 2025-10-25
**Revisión:** Después de implementar Domain Layer
