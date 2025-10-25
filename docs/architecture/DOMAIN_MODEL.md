# MODELO DE DOMINIO - HydroFlow Manager

**Fecha:** 2025-10-25
**Basado en:** Event Storming del código existente

---

## 📊 VISIÓN GENERAL

HydroFlow Manager es un sistema para gestionar:
1. **Registros de arquetas** con elementos hidráulicos
2. **Partes de trabajo** asociadas a redes
3. **Presupuestos** compartidos entre registros y partes
4. **Certificaciones** de obra ejecutada
5. **Catálogos** de elementos hidráulicos y no hidráulicos

---

## 🏛️ BOUNDED CONTEXTS

```
┌─────────────────────────────────────────────────────────────┐
│                   HYDROFLOW MANAGER                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────────┐     ┌────────────────┐                 │
│  │   CATALOG     │────>│    REGISTRO    │                 │
│  │   CONTEXT     │     │    CONTEXT     │                 │
│  └───────────────┘     └────────┬───────┘                 │
│         │                       │                          │
│         │              ┌────────▼───────┐                 │
│         │              │   BUDGETING    │                 │
│         │              │    CONTEXT     │                 │
│         │              └────────┬───────┘                 │
│         │                       │                          │
│         │              ┌────────▼───────┐                 │
│         │              │ CERTIFICATION  │                 │
│         │              │    CONTEXT     │                 │
│         │              └────────────────┘                 │
│         │                                                  │
│         │                       ▲                          │
│         │              ┌────────┴───────┐                 │
│         └─────────────>│  WORK ORDER    │                 │
│                        │    CONTEXT     │                 │
│                        └────────────────┘                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔷 DOMAIN MODEL - ENTIDADES Y VALUE OBJECTS

### Context: REGISTRO

#### Aggregate: Registro (Root)

```python
@dataclass
class Registro:
    """
    Aggregate Root: Registro de Arqueta.

    Representa una arqueta subterránea que contiene elementos
    hidráulicos y permite acceso a tuberías.
    """
    id: UUID
    codigo: CodigoRegistro  # Value Object (formato A-XXXX)
    municipio: Municipio  # Value Object
    descripcion: str
    estado: EstadoRegistro  # Value Object (Enum)
    elementos: List[Elemento]  # Entities
    fotografias: List[Fotografia]  # Value Objects
    created_at: datetime
    updated_at: datetime

    # Domain Methods
    def añadir_elemento(self, elemento: Elemento) -> None:
        """Añade un elemento al registro."""
        if elemento in self.elementos:
            raise DomainError("El elemento ya existe")
        self.elementos.append(elemento)
        self._touch()

    def iniciar_trabajo(self) -> None:
        """Transición: Pendiente → WIP."""
        if self.estado != EstadoRegistro.PENDIENTE:
            raise EstadoInvalidoError("Solo se puede iniciar desde Pendiente")
        self.estado = EstadoRegistro.WIP
        self._touch()

    def finalizar(self) -> None:
        """Transición: WIP → Finalizado."""
        if self.estado != EstadoRegistro.WIP:
            raise EstadoInvalidoError("Solo se puede finalizar desde WIP")
        self.estado = EstadoRegistro.FINALIZADO
        self._touch()

    def completar(self) -> None:
        """Transición: Finalizado → Completado."""
        if self.estado != EstadoRegistro.FINALIZADO:
            raise EstadoInvalidoError("Solo se puede completar desde Finalizado")
        self.estado = EstadoRegistro.COMPLETADO
        self._touch()

    def _touch(self) -> None:
        """Actualiza timestamp de modificación."""
        self.updated_at = datetime.now()
```

#### Entity: Elemento

```python
@dataclass
class Elemento:
    """
    Entity: Elemento instalado en un registro.

    Puede ser hidráulico (válvula, codo) o no hidráulico (marco, tapa).
    """
    id: UUID
    tipo: TipoElemento  # Enum: Hidráulico, NoHidráulico
    orden: int
    catalogo_ref: CatalogoReference  # Value Object
    especificaciones: Dict[str, str]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Elemento):
            return NotImplemented
        return self.id == other.id
```

#### Value Objects

```python
@dataclass(frozen=True)
class CodigoRegistro:
    """Value Object: Código único de registro (A-XXXX)."""
    value: str

    def __post_init__(self):
        if not re.match(r'^A-\d{4}$', self.value):
            raise ValueError(f"Código inválido: {self.value}")

    @classmethod
    def generar(cls, numero: int) -> "CodigoRegistro":
        """Genera código con formato A-XXXX."""
        return cls(f"A-{numero:04d}")

@dataclass(frozen=True)
class EstadoRegistro(Enum):
    """Estados posibles de un registro."""
    PENDIENTE = 3
    WIP = 1
    FINALIZADO = 2
    COMPLETADO = 4

@dataclass(frozen=True)
class Fotografia:
    """Value Object: Fotografía en base64."""
    tipo: TipoFoto
    imagen_base64: str
    fecha: datetime

    def __post_init__(self):
        if not self._es_base64_valido(self.imagen_base64):
            raise ValueError("Formato base64 inválido")
```

---

### Context: WORK ORDER

#### Aggregate: Parte (Root)

```python
@dataclass
class Parte:
    """
    Aggregate Root: Parte de Trabajo.

    Orden de trabajo asociada a una red con tipo de trabajo específico.
    """
    id: UUID
    codigo: str  # Auto-generado
    orden_trabajo: OrdenTrabajo  # Value Object
    red: Red  # Value Object
    tipo_trabajo: TipoTrabajo  # Value Object
    codigo_trabajo: CodigoTrabajo  # Value Object
    descripcion: Optional[str]
    created_at: datetime

    def asociar_orden_trabajo(self, ot: OrdenTrabajo) -> None:
        """Asocia una orden de trabajo a la parte."""
        self.orden_trabajo = ot

    def asociar_red(self, red: Red) -> None:
        """Asocia una red a la parte."""
        self.red = red

    def definir_trabajo(
        self,
        tipo: TipoTrabajo,
        codigo: CodigoTrabajo
    ) -> None:
        """Define el tipo y código de trabajo."""
        self.tipo_trabajo = tipo
        self.codigo_trabajo = codigo

    def esta_completa(self) -> bool:
        """Verifica si todas las dimensiones están definidas."""
        return all([
            self.orden_trabajo,
            self.red,
            self.tipo_trabajo,
            self.codigo_trabajo
        ])
```

---

### Context: BUDGETING

#### Aggregate: Presupuesto (Root)

```python
@dataclass
class Presupuesto:
    """
    Aggregate Root: Presupuesto de Proyecto/Parte.

    Contiene partidas presupuestarias y calcula el total.
    """
    id: UUID
    proyecto_id: UUID  # Referencia a Registro o Parte
    partidas: List[PartidaPresupuesto]  # Entities
    grupos: List[GrupoPartidas]  # Entities
    created_at: datetime

    def añadir_partida(self, partida: PartidaPresupuesto) -> None:
        """Añade una partida al presupuesto."""
        if self._partida_existe(partida.codigo):
            raise DomainError("La partida ya existe en el presupuesto")
        self.partidas.append(partida)

    def modificar_cantidad(
        self,
        partida_id: UUID,
        cantidad: Decimal
    ) -> None:
        """Modifica la cantidad de una partida."""
        partida = self._buscar_partida(partida_id)
        partida.modificar_cantidad(cantidad)

    def calcular_total(self) -> Money:
        """Calcula el total del presupuesto."""
        total = Money(Decimal("0"), "EUR")
        for partida in self.partidas:
            total = total + partida.subtotal
        return total

    def _partida_existe(self, codigo: str) -> bool:
        return any(p.codigo == codigo for p in self.partidas)

    def _buscar_partida(self, partida_id: UUID) -> PartidaPresupuesto:
        for partida in self.partidas:
            if partida.id == partida_id:
                return partida
        raise NotFoundError(f"Partida {partida_id} no encontrada")
```

#### Entity: PartidaPresupuesto

```python
@dataclass
class PartidaPresupuesto:
    """
    Entity: Partida de presupuesto.

    Línea individual del presupuesto con cantidad, precio y subtotal.
    """
    id: UUID
    codigo: str
    descripcion: str
    capitulo: Capitulo  # Value Object
    naturaleza: Naturaleza  # Enum
    unidad: Unidad  # Value Object
    cantidad: Decimal
    precio_unitario: Money
    subtotal: Money  # Calculado

    def __post_init__(self):
        """Valida y calcula subtotal."""
        self._validar()
        self.subtotal = self._calcular_subtotal()

    def modificar_cantidad(self, cantidad: Decimal) -> None:
        """Modifica la cantidad y recalcula subtotal."""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser > 0")
        self.cantidad = cantidad
        self.subtotal = self._calcular_subtotal()

    def modificar_precio(self, precio: Money) -> None:
        """Modifica el precio unitario y recalcula subtotal."""
        if precio.amount < 0:
            raise ValueError("El precio no puede ser negativo")
        self.precio_unitario = precio
        self.subtotal = self._calcular_subtotal()

    def _calcular_subtotal(self) -> Money:
        """Calcula subtotal = cantidad × precio_unitario."""
        return self.precio_unitario * self.cantidad

    def _validar(self) -> None:
        """Valida invariantes de la partida."""
        if self.cantidad <= 0:
            raise ValueError("Cantidad debe ser > 0")
        if self.precio_unitario.amount < 0:
            raise ValueError("Precio no puede ser negativo")
```

#### Value Objects

```python
@dataclass(frozen=True)
class Money:
    """Value Object: Dinero con moneda."""
    amount: Decimal
    currency: str = "EUR"

    def __add__(self, other: "Money") -> "Money":
        self._check_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        self._check_same_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, factor: Decimal) -> "Money":
        return Money(self.amount * factor, self.currency)

    def _check_same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError("Monedas diferentes")

@dataclass(frozen=True)
class Capitulo:
    """Value Object: Capítulo de presupuesto."""
    codigo: str  # PA000, PA001, etc.
    descripcion: str

    def __post_init__(self):
        if not re.match(r'^PA\d{3}$', self.codigo):
            raise ValueError(f"Código de capítulo inválido: {self.codigo}")

@dataclass(frozen=True)
class Unidad:
    """Value Object: Unidad de medida."""
    codigo: str  # m, m², m³, h, ud
    descripcion: str

class Naturaleza(Enum):
    """Naturaleza de la partida."""
    MATERIAL = "Material"
    MANO_OBRA = "Mano de Obra"
    EQUIPAMIENTO = "Equipamiento"
    OTROS = "Otros"
```

---

### Context: CERTIFICATION

#### Aggregate: Certificación (Root)

```python
@dataclass
class Certificación:
    """
    Aggregate Root: Certificación de Obra Ejecutada.

    Reconocimiento oficial de trabajo ejecutado para facturación.
    """
    id: UUID
    partida_presupuesto_id: UUID  # Referencia
    cantidad_certificada: Decimal
    precio_unitario: Money
    importe_certificado: Money  # Calculado
    porcentaje_ejecucion: Decimal  # 0-100
    estado: EstadoCertificacion  # Enum
    aprobada_por: Optional[str]
    fecha_certificacion: datetime
    fecha_aprobacion: Optional[datetime]

    def certificar_cantidad(
        self,
        cantidad: Decimal,
        cantidad_presupuestada: Decimal,
        precio: Money
    ) -> None:
        """Certifica una cantidad de trabajo ejecutado."""
        if cantidad > cantidad_presupuestada:
            raise CantidadExcedidaError(
                f"Cantidad certificada ({cantidad}) > "
                f"presupuestada ({cantidad_presupuestada})"
            )

        self.cantidad_certificada = cantidad
        self.precio_unitario = precio
        self.importe_certificado = self._calcular_importe()
        self.porcentaje_ejecucion = self._calcular_porcentaje(
            cantidad_presupuestada
        )

    def aprobar(self, usuario: str) -> None:
        """Aprueba la certificación."""
        if self.estado == EstadoCertificacion.APROBADA:
            raise DomainError("La certificación ya está aprobada")

        self.estado = EstadoCertificacion.APROBADA
        self.aprobada_por = usuario
        self.fecha_aprobacion = datetime.now()

    def rechazar(self, usuario: str, motivo: str) -> None:
        """Rechaza la certificación."""
        if self.estado == EstadoCertificacion.APROBADA:
            raise DomainError("No se puede rechazar una certificación aprobada")

        self.estado = EstadoCertificacion.RECHAZADA
        # TODO: Guardar motivo del rechazo

    def puede_modificarse(self) -> bool:
        """Verifica si la certificación puede modificarse."""
        return self.estado != EstadoCertificacion.APROBADA

    def _calcular_importe(self) -> Money:
        """Calcula importe = cantidad × precio."""
        return self.precio_unitario * self.cantidad_certificada

    def _calcular_porcentaje(
        self,
        cantidad_presupuestada: Decimal
    ) -> Decimal:
        """Calcula porcentaje de ejecución."""
        if cantidad_presupuestada == 0:
            return Decimal("0")

        return (
            self.cantidad_certificada / cantidad_presupuestada
        ) * Decimal("100")

class EstadoCertificacion(Enum):
    """Estados de una certificación."""
    BORRADOR = "Borrador"
    APROBADA = "Aprobada"
    RECHAZADA = "Rechazada"
```

---

### Context: CATALOG

#### Aggregate: CatalogoHidraulica (Root)

```python
@dataclass
class CatalogoHidraulica:
    """
    Aggregate Root: Elemento del Catálogo Hidráulico.

    Representa un producto disponible con especificaciones técnicas.
    """
    id: UUID
    familia: Familia  # Enum
    tipo_elemento: TipoElemento
    marca: str
    modelo: str
    referencia: str
    caracteristicas: str
    especificaciones: EspecificacionesTecnicas  # Value Object
    precio: Money
    cod_presupuesto: str

    def actualizar_precio(self, nuevo_precio: Money) -> None:
        """Actualiza el precio del elemento."""
        if nuevo_precio.amount < 0:
            raise ValueError("El precio no puede ser negativo")
        self.precio = nuevo_precio

@dataclass(frozen=True)
class EspecificacionesTecnicas:
    """Value Object: Especificaciones técnicas de elemento hidráulico."""
    dn_inicial: DN  # Diámetro Nominal
    dn_final: Optional[DN]
    pn: PN  # Presión Nominal
    angulo: Optional[Decimal]
    ref_cad: Optional[str]

class Familia(Enum):
    """Familias de elementos hidráulicos."""
    VALVULAS = "Válvulas"
    ACCESORIOS = "Accesorios"
    TUBERIAS = "Tuberías"
    OTROS = "Otros"
```

---

## 🔗 REPOSITORY INTERFACES

```python
from typing import Protocol, Optional, List
from uuid import UUID

class IRegistroRepository(Protocol):
    """Interface del repositorio de registros."""

    def save(self, registro: Registro) -> None:
        """Guarda o actualiza un registro."""
        ...

    def get_by_id(self, registro_id: UUID) -> Optional[Registro]:
        """Obtiene un registro por ID."""
        ...

    def get_by_codigo(self, codigo: str) -> Optional[Registro]:
        """Obtiene un registro por código."""
        ...

    def get_all(self) -> List[Registro]:
        """Obtiene todos los registros."""
        ...

    def delete(self, registro_id: UUID) -> bool:
        """Elimina un registro."""
        ...

# Similar para: IParteRepository, IPresupuestoRepository,
#               ICertificacionRepository, ICatalogoRepository
```

---

## 📐 DOMAIN SERVICES

```python
class PresupuestoCalculator:
    """
    Domain Service: Calculadora de Presupuestos.

    Encapsula lógica de cálculo que no pertenece a una entidad específica.
    """

    def __init__(self, tax_rate: Decimal = Decimal("0.21")):
        self.tax_rate = tax_rate

    def calcular_total_con_impuestos(
        self,
        presupuesto: Presupuesto
    ) -> Money:
        """Calcula total incluyendo impuestos."""
        subtotal = presupuesto.calcular_total()
        impuesto = subtotal * self.tax_rate
        return subtotal + impuesto

    def calcular_margen(
        self,
        coste: Money,
        precio: Money
    ) -> Decimal:
        """Calcula margen de beneficio."""
        if precio.amount == 0:
            raise ValueError("El precio no puede ser 0")
        return (precio.amount - coste.amount) / precio.amount

class CertificacionValidator:
    """
    Domain Service: Validador de Certificaciones.

    Valida reglas de negocio complejas de certificaciones.
    """

    def validar_cantidad_certificable(
        self,
        cantidad_a_certificar: Decimal,
        cantidad_presupuestada: Decimal,
        cantidad_ya_certificada: Decimal
    ) -> bool:
        """
        Valida que la cantidad a certificar no exceda límites.

        Returns:
            True si es válida

        Raises:
            CantidadExcedidaError si excede presupuestado
        """
        total_certificado = cantidad_ya_certificada + cantidad_a_certificar

        if total_certificado > cantidad_presupuestada:
            raise CantidadExcedidaError(
                f"Total certificado ({total_certificado}) > "
                f"presupuestado ({cantidad_presupuestada})"
            )

        return True
```

---

## 🚨 DOMAIN EXCEPTIONS

```python
class DomainError(Exception):
    """Error base del dominio."""
    pass

class EstadoInvalidoError(DomainError):
    """Error de transición de estado inválida."""
    pass

class CantidadExcedidaError(DomainError):
    """Error cuando cantidad certificada excede presupuestada."""
    pass

class NotFoundError(DomainError):
    """Error cuando no se encuentra una entidad."""
    pass

class ValidationError(DomainError):
    """Error de validación de reglas de negocio."""
    pass
```

---

## 📏 INVARIANTS (Reglas de Negocio)

### Registro
- ✅ Código único y auto-generado (formato A-XXXX)
- ✅ Transiciones de estado válidas:
  * Pendiente → WIP
  * WIP → Finalizado
  * Finalizado → Completado
- ✅ Elementos tienen orden secuencial

### Presupuesto
- ✅ Total = SUM(partidas.subtotal)
- ✅ Partida.subtotal = cantidad × precio_unitario
- ✅ Cantidad de partida > 0
- ✅ Precio unitario >= 0

### Certificación
- ✅ cantidad_certificada ≤ cantidad_presupuestada
- ✅ importe_certificado = cantidad_certificada × precio_unitario
- ✅ porcentaje_ejecucion = (certificada / presupuestada) × 100
- ✅ No se puede modificar si está aprobada

---

## 🎯 PRÓXIMOS PASOS

1. ✅ Implementar Value Objects (Money, Capitulo, Unidad, etc.)
2. ✅ Implementar Entities (Registro, Presupuesto, etc.)
3. ✅ Implementar Repository Interfaces (Protocols)
4. ✅ Implementar Domain Services
5. ✅ Crear tests unitarios (TDD)

---

**Fin del Modelo de Dominio**
**Ver también:** EVENT_STORMING.md para flujos completos
