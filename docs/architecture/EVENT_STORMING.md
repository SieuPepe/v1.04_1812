# EVENT STORMING - HydroFlow Manager

**Fecha:** 2025-10-25
**Participantes:** Claude Code, SieuPepe
**Duración:** Sesión de análisis del código existente

---

## 🎯 OBJETIVO

Modelar el dominio completo del sistema HydroFlow Manager a través de Event Storming,
identificando eventos, comandos, agregados y contextos delimitados.

---

## 📊 METODOLOGÍA

Event Storming usa **colores** para representar diferentes conceptos:

- 🟠 **Domain Events:** Eventos que ocurrieron (pasado)
- 🔵 **Commands:** Acciones que disparan eventos
- 🟡 **Aggregates:** Entidades con lógica de negocio
- 👤 **Actors:** Quién ejecuta los comandos
- 💜 **Policies:** Reglas de negocio / Procesos automáticos
- 🟢 **Read Models:** Vistas/Consultas
- 🔴 **Hotspots:** Problemas/Dudas a resolver

---

## 🌊 FLUJO 1: GESTIÓN DE REGISTROS (ARQUETAS)

### Timeline de Eventos

```
[Manager] → 🔵 CrearRegistro → 🟡 Registro → 🟠 RegistroCreado
                                    ↓
[Manager] → 🔵 AñadirElemento → 🟡 Elemento → 🟠 ElementoAñadido
                                    ↓
[Manager] → 🔵 SubirFotografía → 🟡 Fotografía → 🟠 FotografíaSubida
                                    ↓
[Manager] → 🔵 IniciarTrabajo → 🟡 Registro → 🟠 TrabajoIniciado
                                    ↓
                            💜 Policy: Estado → WIP
                                    ↓
[Manager] → 🔵 FinalizarRegistro → 🟡 Registro → 🟠 RegistroFinalizado
                                    ↓
                            💜 Policy: Estado → Finalizado
                                    ↓
[Manager] → 🔵 CompletarRegistro → 🟡 Registro → 🟠 RegistroCompletado
                                    ↓
                            💜 Policy: Estado → Completado
```

### Domain Events 🟠

1. **RegistroCreado**
   - Agregado: Registro
   - Datos: id, código (auto-generado), municipio, fecha_creacion
   - Trigger: Comando CrearRegistro

2. **ElementoHidráulicoAñadido**
   - Agregado: Registro
   - Datos: id_elemento, tipo, catálogo_ref, orden, orientación, material
   - Trigger: Comando AñadirElementoHidráulico

3. **ElementoNoHidráulicoAñadido**
   - Agregado: Registro
   - Datos: id_elemento, tipo_registro, modelo, marca
   - Trigger: Comando AñadirElementoNoHidráulico

4. **FotografíaAñadida**
   - Agregado: Registro
   - Datos: id_foto, tipo_foto, imagen_base64, fecha
   - Trigger: Comando SubirFotografía

5. **RegistroActualizado**
   - Agregado: Registro
   - Datos: campos modificados, fecha_actualizacion
   - Trigger: Comando ActualizarRegistro

6. **EstadoCambiado**
   - Agregado: Registro
   - Datos: estado_anterior, estado_nuevo, motivo
   - Trigger: Comandos IniciarTrabajo, FinalizarRegistro, CompletarRegistro

7. **RegistroEliminado**
   - Agregado: Registro
   - Datos: id, código, motivo
   - Trigger: Comando EliminarRegistro

### Commands 🔵

1. **CrearRegistro**
   - Actor: 👤 Manager
   - Params: municipio, descripción
   - Business Rules: Código auto-generado, estado inicial = Pendiente

2. **AñadirElementoHidráulico**
   - Actor: 👤 Manager
   - Params: id_registro, id_catalogo_hidraulica, orden, orientación
   - Business Rules: Orden secuencial, elemento debe existir en catálogo

3. **AñadirElementoNoHidráulico**
   - Actor: 👤 Manager
   - Params: id_registro, id_catalogo_registros
   - Business Rules: Elemento debe existir en catálogo

4. **SubirFotografía**
   - Actor: 👤 Manager/User
   - Params: id_registro, tipo_foto, imagen_base64
   - Business Rules: Formato válido, tamaño máximo

5. **IniciarTrabajo**
   - Actor: 👤 Manager
   - Params: id_registro
   - Business Rules: Estado debe ser Pendiente → WIP

6. **FinalizarRegistro**
   - Actor: 👤 Manager
   - Params: id_registro
   - Business Rules: Estado debe ser WIP → Finalizado

7. **CompletarRegistro**
   - Actor: 👤 Manager
   - Params: id_registro
   - Business Rules: Estado debe ser Finalizado → Completado

8. **ActualizarRegistro**
   - Actor: 👤 Manager
   - Params: id_registro, campos_a_actualizar
   - Business Rules: Registro debe existir

9. **EliminarRegistro**
   - Actor: 👤 Manager
   - Params: id_registro
   - Business Rules: No debe tener presupuestos ni certificaciones

### Aggregates 🟡

#### **Registro (Inventario)**
```
Registro
├── id: UUID
├── codigo: String (auto-generado A-XXXX)
├── municipio: Municipio (Value Object)
├── descripcion: String
├── estado: EstadoRegistro (Enum: Pendiente, WIP, Finalizado, Completado)
├── elementos: List<Elemento>
├── fotografias: List<Fotografia>
├── created_at: DateTime
└── updated_at: DateTime

Methods:
- create(municipio, descripcion) → Registro
- añadirElemento(elemento: Elemento) → void
- subirFotografia(fotografia: Fotografia) → void
- iniciarTrabajo() → void  // Pendiente → WIP
- finalizar() → void        // WIP → Finalizado
- completar() → void        // Finalizado → Completado
- validarTransicionEstado(nuevoEstado) → bool
```

#### **Elemento**
```
Elemento
├── id: UUID
├── tipo: TipoElemento (Enum: Hidráulico, NoHidráulico)
├── orden: Integer
├── catalogo_ref: CatalogoReference (Value Object)
└── especificaciones: Map<String, String>

Types:
- ElementoHidraulico extends Elemento
  - orientación: Orientacion
  - material: Material
  - dn_inicial: DN
  - dn_final: DN
  - presion_nominal: PN

- ElementoNoHidraulico extends Elemento
  - tipo_registro: TipoRegistro
  - modelo: String
  - marca: String
```

#### **Fotografia**
```
Fotografia (Value Object)
├── tipo: TipoFoto
├── imagen_base64: String
└── fecha: DateTime

Rules:
- Inmutable
- Validar formato base64
```

### Policies 💜

1. **Auto-generación de Código**
   - Trigger: RegistroCreado
   - Action: Generar código formato A-XXXX (incremental)

2. **Validación de Transición de Estados**
   - Trigger: EstadoCambiado
   - Rules:
     ```
     Pendiente → WIP ✅
     WIP → Finalizado ✅
     Finalizado → Completado ✅
     Cualquier otro cambio ❌
     ```

3. **Auditoría de Cambios**
   - Trigger: Cualquier evento
   - Action: Registrar fecha_actualizacion

### Read Models 🟢

1. **VistaResumenRegistros**
   - Total registros
   - Por estado (Pendiente, WIP, Finalizado, Completado)
   - Por municipio
   - Por tipo de certificación

2. **VistaDetalleRegistro**
   - Datos completos del registro
   - Lista de elementos (ordenados)
   - Fotografías
   - Presupuestos asociados
   - Certificaciones asociadas

---

## 🌊 FLUJO 2: GESTIÓN DE PARTES DE TRABAJO

### Timeline de Eventos

```
[Manager] → 🔵 CrearParte → 🟡 Parte → 🟠 ParteCreada
                                ↓
[Manager] → 🔵 AsociarOT → 🟡 Parte → 🟠 OTAsociada
                                ↓
[Manager] → 🔵 AsociarRed → 🟡 Parte → 🟠 RedAsociada
                                ↓
[Manager] → 🔵 DefinirTrabajo → 🟡 Parte → 🟠 TrabajoDefinido
```

### Domain Events 🟠

1. **ParteCreada**
   - Agregado: Parte
   - Datos: id, codigo (auto-generado), descripción, fecha_creacion

2. **OrdenDeTrabajoAsociada**
   - Agregado: Parte
   - Datos: id_ot, nombre_ot

3. **RedAsociada**
   - Agregado: Parte
   - Datos: id_red, nombre_red

4. **TipoTrabajoDefinido**
   - Agregado: Parte
   - Datos: id_tipo_trabajo, id_cod_trabajo

5. **ParteEliminada**
   - Agregado: Parte
   - Datos: id, motivo

### Commands 🔵

1. **CrearParte**
   - Actor: 👤 Manager
   - Params: descripción (opcional)
   - Business Rules: Código auto-generado

2. **AsociarOrdenDeTrabajo**
   - Actor: 👤 Manager
   - Params: id_parte, id_ot
   - Business Rules: OT debe existir

3. **AsociarRed**
   - Actor: 👤 Manager
   - Params: id_parte, id_red
   - Business Rules: Red debe existir

4. **DefinirTipoDeTrabajo**
   - Actor: 👤 Manager
   - Params: id_parte, id_tipo_trabajo, id_cod_trabajo
   - Business Rules: Tipo y código deben existir

5. **EliminarParte**
   - Actor: 👤 Manager
   - Params: id_parte
   - Business Rules: No debe tener presupuestos ni certificaciones

### Aggregates 🟡

#### **Parte**
```
Parte
├── id: UUID
├── codigo: String (auto-generado)
├── orden_trabajo: OrdenTrabajo (Value Object)
├── red: Red (Value Object)
├── tipo_trabajo: TipoTrabajo (Value Object)
├── codigo_trabajo: CodigoTrabajo (Value Object)
├── descripcion: String
└── created_at: DateTime

Methods:
- create(descripcion?) → Parte
- asociarOT(ot: OrdenTrabajo) → void
- asociarRed(red: Red) → void
- definirTrabajo(tipo: TipoTrabajo, codigo: CodigoTrabajo) → void
- validarAsociaciones() → bool
```

### Policies 💜

1. **Auto-generación de Código de Parte**
   - Trigger: ParteCreada
   - Action: Generar código único

2. **Validación de Dimensiones**
   - Trigger: AsociarOT, AsociarRed, DefinirTrabajo
   - Action: Validar que existan en catálogos

---

## 🌊 FLUJO 3: GESTIÓN DE PRESUPUESTOS

### Timeline de Eventos

```
[Manager] → 🔵 CrearPresupuesto → 🟡 Presupuesto → 🟠 PresupuestoCreado
                                       ↓
[Manager] → 🔵 AñadirPartida → 🟡 Partida → 🟠 PartidaAñadida
                                       ↓
                            💜 Policy: Calcular Subtotal
                                       ↓
[Manager] → 🔵 ModificarCantidad → 🟡 Partida → 🟠 CantidadModificada
                                       ↓
                            💜 Policy: Recalcular Subtotal
                                       ↓
[Manager] → 🔵 AgruparPartidas → 🟡 Grupo → 🟠 PartidasAgrupadas
                                       ↓
                            🟢 Read Model: Total Presupuesto
```

### Domain Events 🟠

1. **PresupuestoCreado**
   - Agregado: Presupuesto
   - Datos: id, id_proyecto/registro, fecha_creacion

2. **PartidaAñadida**
   - Agregado: Presupuesto
   - Datos: id_partida, codigo, descripción, cantidad, precio_unitario, subtotal
   - Business Rule: subtotal = cantidad × precio_unitario

3. **CantidadModificada**
   - Agregado: Partida
   - Datos: cantidad_anterior, cantidad_nueva, subtotal_nuevo

4. **PrecioModificado**
   - Agregado: Partida
   - Datos: precio_anterior, precio_nuevo, subtotal_nuevo

5. **PartidaEliminada**
   - Agregado: Presupuesto
   - Datos: id_partida, motivo

6. **GrupoDePartidasCreado**
   - Agregado: GrupoPartidas
   - Datos: id_grupo, nombre, partidas_incluidas

7. **TotalPresupuestoCalculado**
   - Agregado: Presupuesto
   - Datos: total, fecha_cálculo
   - Trigger: Policy después de modificaciones

### Commands 🔵

1. **CrearPresupuesto**
   - Actor: 👤 Manager
   - Params: id_proyecto/registro
   - Business Rules: Proyecto debe existir

2. **AñadirPartida**
   - Actor: 👤 Manager
   - Params: id_presupuesto, id_partida_catalogo, cantidad
   - Business Rules:
     * Partida debe existir en catálogo
     * Cantidad > 0
     * Calcular subtotal automáticamente

3. **ModificarCantidad**
   - Actor: 👤 Manager
   - Params: id_partida_presupuesto, nueva_cantidad
   - Business Rules:
     * Cantidad > 0
     * Recalcular subtotal

4. **ModificarPrecioUnitario**
   - Actor: 👤 Manager
   - Params: id_partida_presupuesto, nuevo_precio
   - Business Rules:
     * Precio >= 0
     * Recalcular subtotal

5. **EliminarPartida**
   - Actor: 👤 Manager
   - Params: id_partida_presupuesto
   - Business Rules: No debe estar certificada

6. **AgruparPartidas**
   - Actor: 👤 Manager
   - Params: nombre_grupo, lista_partidas
   - Business Rules: Partidas deben existir en presupuesto

7. **CalcularTotalPresupuesto**
   - Actor: 💜 System (Policy)
   - Trigger: Automático después de cambios
   - Cálculo: SUM(todas las partidas.subtotal)

### Aggregates 🟡

#### **Presupuesto**
```
Presupuesto
├── id: UUID
├── proyecto_id: UUID (Registro o Parte)
├── partidas: List<PartidaPresupuesto>
├── grupos: List<GrupoPartidas>
├── total: Money (calculado)
└── created_at: DateTime

Methods:
- create(proyecto_id) → Presupuesto
- añadirPartida(partida: PartidaPresupuesto) → void
- modificarCantidad(id_partida, cantidad) → void
- modificarPrecio(id_partida, precio) → void
- eliminarPartida(id_partida) → void
- calcularTotal() → Money
- agruparPartidas(grupo: GrupoPartidas) → void

Invariants:
- Total siempre es la suma de partidas
- No puede haber partidas duplicadas
```

#### **PartidaPresupuesto**
```
PartidaPresupuesto (Entity dentro de Presupuesto)
├── id: UUID
├── codigo: String (del catálogo)
├── descripcion: String
├── capitulo: Capitulo (Value Object)
├── naturaleza: Naturaleza (Enum: Material, ManoObra, Equipamiento)
├── unidad: Unidad (Value Object: m, m², m³, h, etc.)
├── cantidad: Decimal
├── precio_unitario: Money
└── subtotal: Money (calculado)

Methods:
- create(catalogo_ref, cantidad) → PartidaPresupuesto
- modificarCantidad(cantidad) → void
- modificarPrecio(precio) → void
- calcularSubtotal() → Money

Invariants:
- subtotal = cantidad × precio_unitario
- cantidad > 0
- precio_unitario >= 0
```

#### **GrupoPartidas**
```
GrupoPartidas
├── id: UUID
├── nombre: String
├── partidas: List<PartidaPresupuesto>
└── subtotal_grupo: Money (calculado)

Methods:
- create(nombre, partidas) → GrupoPartidas
- añadirPartida(partida) → void
- eliminarPartida(partida_id) → void
- calcularSubtotalGrupo() → Money
```

### Value Objects

#### **Money**
```
Money (Immutable)
├── amount: Decimal
└── currency: String (EUR)

Methods:
- add(other: Money) → Money
- subtract(other: Money) → Money
- multiply(factor: Decimal) → Money
- divide(divisor: Decimal) → Money
- equals(other: Money) → bool

Invariants:
- Currency must match for operations
- Amount can be negative (for adjustments)
```

#### **Capitulo**
```
Capitulo (Value Object)
├── codigo: String (PA000, PA001, etc.)
└── descripcion: String

Examples:
- PA000: PARTIDAS TIPO
- PA001: MOVIMIENTO DE TIERRAS
- PA002: FONTANERÍA
```

#### **Unidad**
```
Unidad (Value Object)
├── codigo: String (m, m², m³, h, etc.)
└── descripcion: String

Examples:
- m: Metro lineal
- m²: Metro cuadrado
- m³: Metro cúbico
- h: Hora
- ud: Unidad
```

### Policies 💜

1. **Auto-cálculo de Subtotal**
   - Trigger: PartidaAñadida, CantidadModificada, PrecioModificado
   - Action: subtotal = cantidad × precio_unitario

2. **Auto-cálculo de Total Presupuesto**
   - Trigger: Cualquier cambio en partidas
   - Action: total = SUM(partidas.subtotal)

3. **Validación de Precios del Catálogo**
   - Trigger: AñadirPartida
   - Action: Verificar que precio_unitario coincide con catálogo (advertir si difiere)

### Read Models 🟢

1. **VistaResumenPresupuesto**
   - Total general
   - Total por capítulo
   - Total por naturaleza (Material, Mano de Obra, etc.)
   - Total por grupo

2. **VistaDetallePresupuesto**
   - Lista completa de partidas
   - Ordenado por capítulo y código
   - Subtotales por sección

3. **VistaComparativaPresupuesto**
   - Presupuesto estimado
   - Presupuesto ejecutado (certificaciones)
   - Diferencia
   - Porcentaje de ejecución

---

## 🌊 FLUJO 4: GESTIÓN DE CERTIFICACIONES

### Timeline de Eventos

```
[Manager] → 🔵 CrearCertificación → 🟡 Certificación → 🟠 CertificaciónCreada
                                         ↓
[Manager] → 🔵 CertificarCantidad → 🟡 Certificación → 🟠 CantidadCertificada
                                         ↓
                            💜 Policy: Validar ≤ Presupuestado
                                         ↓
                            💜 Policy: Calcular Importe
                                         ↓
[Manager] → 🔵 AprobarCertificación → 🟡 Certificación → 🟠 CertificaciónAprobada
                                         ↓
                            🟢 Read Model: Total Certificado
```

### Domain Events 🟠

1. **CertificaciónCreada**
   - Agregado: Certificación
   - Datos: id, id_partida_presupuesto, fecha_certificacion

2. **CantidadCertificada**
   - Agregado: Certificación
   - Datos: cantidad_certificada, precio_unitario, importe_certificado
   - Business Rule: cantidad_certificada ≤ cantidad_presupuestada

3. **PorcentajeDeEjecuciónCalculado**
   - Agregado: Certificación
   - Datos: porcentaje (0-100%)
   - Cálculo: (cantidad_certificada / cantidad_presupuestada) × 100

4. **CertificaciónAprobada**
   - Agregado: Certificación
   - Datos: aprobada_por, fecha_aprobacion

5. **CertificaciónRechazada**
   - Agregado: Certificación
   - Datos: rechazada_por, motivo, fecha_rechazo

6. **TotalCertificadoCalculado**
   - Agregado: Proyecto/Parte
   - Datos: total_certificado, fecha_cálculo
   - Trigger: Policy después de certificaciones

### Commands 🔵

1. **CrearCertificación**
   - Actor: 👤 Manager
   - Params: id_partida_presupuesto
   - Business Rules: Partida debe existir en presupuesto

2. **CertificarCantidad**
   - Actor: 👤 Manager
   - Params: id_certificacion, cantidad_certificada
   - Business Rules:
     * cantidad_certificada > 0
     * cantidad_certificada ≤ cantidad_presupuestada
     * Calcular importe automáticamente

3. **ModificarCantidadCertificada**
   - Actor: 👤 Manager
   - Params: id_certificacion, nueva_cantidad
   - Business Rules: Mismas que CertificarCantidad

4. **AprobarCertificación**
   - Actor: 👤 Manager
   - Params: id_certificacion
   - Business Rules: Certificación debe estar completa

5. **RechazarCertificación**
   - Actor: 👤 Manager
   - Params: id_certificacion, motivo
   - Business Rules: Debe proporcionar motivo

6. **EliminarCertificación**
   - Actor: 👤 Manager
   - Params: id_certificacion
   - Business Rules: No debe estar aprobada

### Aggregates 🟡

#### **Certificación**
```
Certificación
├── id: UUID
├── partida_presupuesto_id: UUID
├── cantidad_certificada: Decimal
├── precio_unitario: Money
├── importe_certificado: Money (calculado)
├── porcentaje_ejecucion: Decimal (0-100)
├── estado: EstadoCertificacion (Enum: Borrador, Aprobada, Rechazada)
├── aprobada_por: String?
├── fecha_certificacion: DateTime
└── fecha_aprobacion: DateTime?

Methods:
- create(partida_presupuesto_id) → Certificación
- certificarCantidad(cantidad, precio) → void
- modificarCantidad(cantidad) → void
- calcularImporte() → Money
- calcularPorcentajeEjecucion(cantidad_presupuestada) → Decimal
- aprobar(usuario) → void
- rechazar(usuario, motivo) → void
- validarCantidad(cantidad_presupuestada) → bool

Invariants:
- importe_certificado = cantidad_certificada × precio_unitario
- porcentaje = (cantidad_certificada / cantidad_presupuestada) × 100
- cantidad_certificada ≤ cantidad_presupuestada
- Si aprobada, no se puede modificar
```

### Policies 💜

1. **Auto-cálculo de Importe Certificado**
   - Trigger: CantidadCertificada, ModificarCantidadCertificada
   - Action: importe = cantidad_certificada × precio_unitario

2. **Auto-cálculo de Porcentaje de Ejecución**
   - Trigger: CantidadCertificada
   - Action: porcentaje = (cantidad_certificada / cantidad_presupuestada) × 100

3. **Validación de Cantidad Máxima**
   - Trigger: CertificarCantidad
   - Action: Verificar que cantidad_certificada ≤ cantidad_presupuestada
   - Si excede: Rechazar comando con error

4. **Auto-cálculo de Total Certificado del Proyecto**
   - Trigger: Cualquier cambio en certificaciones
   - Action: total_certificado = SUM(certificaciones.importe_certificado)

5. **Bloqueo de Modificación de Certificaciones Aprobadas**
   - Trigger: ModificarCantidadCertificada, EliminarCertificación
   - Action: Si estado = Aprobada, rechazar comando

### Read Models 🟢

1. **VistaResumenCertificaciones**
   - Total certificado
   - Total presupuestado
   - Diferencia (presupuesto - certificado)
   - Porcentaje global de ejecución

2. **VistaDetalleCertificaciones**
   - Lista de certificaciones por partida
   - Estado de cada certificación
   - Importes certificados

3. **VistaComparativaPresupuestoVsCertificación**
   - Por cada partida:
     * Cantidad presupuestada
     * Cantidad certificada
     * Diferencia
     * Porcentaje ejecutado

---

## 🌊 FLUJO 5: GESTIÓN DE CATÁLOGOS

### Timeline de Eventos

```
[Manager] → 🔵 AñadirElementoCatálogo → 🟡 CatalogoHidraulica → 🟠 ElementoAñadidoACatálogo
                                             ↓
                            💜 Policy: Validar Especificaciones
                                             ↓
[Manager] → 🔵 ActualizarPrecio → 🟡 CatalogoHidraulica → 🟠 PrecioActualizado
```

### Domain Events 🟠

1. **ElementoHidráulicoAñadidoACatálogo**
   - Agregado: CatalogoHidraulica
   - Datos: familia, tipo, marca, modelo, especificaciones técnicas, precio

2. **ElementoNoHidráulicoAñadidoACatálogo**
   - Agregado: CatalogoRegistros
   - Datos: tipo_registro, marca, modelo, caracteristicas, precio

3. **PrecioDeCatálogoActualizado**
   - Agregado: CatalogoHidraulica/CatalogoRegistros
   - Datos: precio_anterior, precio_nuevo, fecha_actualizacion

4. **ElementoDeCatálogoEliminado**
   - Agregado: CatalogoHidraulica/CatalogoRegistros
   - Datos: id, referencia, motivo

### Commands 🔵

1. **AñadirElementoHidráulicoACatálogo**
   - Actor: 👤 Manager
   - Params: familia, tipo, marca, modelo, dn, dnf, pn, precio, etc.
   - Business Rules: Todas las especificaciones deben ser válidas

2. **AñadirElementoNoHidráulicoACatálogo**
   - Actor: 👤 Manager
   - Params: tipo_registro, marca, modelo, caracteristicas, precio
   - Business Rules: Tipo debe existir

3. **ActualizarPrecioDeCatálogo**
   - Actor: 👤 Manager
   - Params: id_elemento, nuevo_precio
   - Business Rules: Precio >= 0

4. **EliminarElementoDeCatálogo**
   - Actor: 👤 Manager
   - Params: id_elemento
   - Business Rules: No debe estar usado en registros existentes

### Aggregates 🟡

#### **CatalogoHidraulica**
```
CatalogoHidraulica
├── id: UUID
├── familia: Familia (Enum: Válvulas, Accesorios, Tuberías, etc.)
├── tipo_elemento: TipoElemento
├── marca: String
├── modelo: String
├── referencia: String
├── caracteristicas: String
├── especificaciones: EspecificacionesTecnicas
├── precio: Money
└── cod_presupuesto: String

EspecificacionesTecnicas:
├── dn_inicial: DN (Diámetro Nominal)
├── dn_final: DN
├── pn: PN (Presión Nominal)
├── angulo: Decimal?
└── ref_cad: String?

Methods:
- create(...) → CatalogoHidraulica
- actualizarPrecio(precio) → void
- validarEspecificaciones() → bool
```

---

## 🏛️ BOUNDED CONTEXTS (Contextos Delimitados)

### 1. REGISTRO CONTEXT (Inventario/Arquetas)

**Responsabilidad:** Gestión de registros de arquetas con elementos hidráulicos

**Aggregates:**
- Registro (Root)
- Elemento
- Fotografia

**Events:**
- RegistroCreado, ElementoAñadido, FotografíaSubida, EstadoCambiado

**Language:**
- Registro/Arqueta
- Elemento Hidráulico
- Elemento No Hidráulico
- Estados (Pendiente, WIP, Finalizado, Completado)

---

### 2. WORK ORDER CONTEXT (Partes de Trabajo)

**Responsabilidad:** Gestión de partes/órdenes de trabajo

**Aggregates:**
- Parte (Root)
- OrdenTrabajo
- Red
- TipoTrabajo

**Events:**
- ParteCreada, OTAsociada, RedAsociada, TrabajoDefinido

**Language:**
- Parte
- Orden de Trabajo (OT)
- Red
- Tipo de Trabajo
- Código de Trabajo

---

### 3. BUDGETING CONTEXT (Presupuestos)

**Responsabilidad:** Cálculo y gestión de presupuestos

**Aggregates:**
- Presupuesto (Root)
- PartidaPresupuesto
- GrupoPartidas

**Value Objects:**
- Money
- Capitulo
- Unidad

**Events:**
- PresupuestoCreado, PartidaAñadida, CantidadModificada, TotalCalculado

**Language:**
- Presupuesto
- Partida
- Capítulo
- Naturaleza (Material, Mano de Obra)
- Unidad (m, m², m³, h)
- Subtotal
- Total

**Shared Kernel con:** Registro Context, Work Order Context

---

### 4. CERTIFICATION CONTEXT (Certificaciones)

**Responsabilidad:** Certificación de obra ejecutada

**Aggregates:**
- Certificación (Root)

**Events:**
- CertificaciónCreada, CantidadCertificada, CertificaciónAprobada

**Language:**
- Certificación
- Cantidad Certificada
- Importe Certificado
- Porcentaje de Ejecución
- Estado (Borrador, Aprobada, Rechazada)

**Shared Kernel con:** Budgeting Context

---

### 5. CATALOG CONTEXT (Catálogos)

**Responsabilidad:** Gestión de catálogos de productos

**Aggregates:**
- CatalogoHidraulica (Root)
- CatalogoRegistros (Root)

**Events:**
- ElementoAñadidoACatálogo, PrecioActualizado

**Language:**
- Familia (Válvulas, Accesorios, etc.)
- Tipo de Elemento
- Especificaciones Técnicas (DN, PN, etc.)
- Marca, Modelo, Referencia

**Upstream de:** Registro Context

---

## 🔗 RELACIONES ENTRE CONTEXTOS

```
CATALOG CONTEXT
   ↓ (upstream)
REGISTRO CONTEXT ←→ BUDGETING CONTEXT ←→ CERTIFICATION CONTEXT
   ↓                      ↑
WORK ORDER CONTEXT ──────┘
```

**Tipo de relaciones:**
- → Upstream/Downstream
- ←→ Shared Kernel

---

## 📖 GLOSARIO DE LENGUAJE UBICUO

### Términos del Dominio

**Registro / Arqueta:**
Instalación subterránea que contiene elementos hidráulicos y permite el acceso a tuberías.

**Elemento Hidráulico:**
Componente técnico de una instalación de agua (válvulas, codos, reducciones, etc.).

**Elemento No Hidráulico:**
Componente estructural del registro (marco, tapa, etc.).

**Parte / Work Order:**
Orden de trabajo asociada a una red específica con un tipo de trabajo definido.

**Presupuesto:**
Estimación de costes de un proyecto basada en partidas presupuestarias.

**Partida:**
Línea de presupuesto con código, descripción, unidad, cantidad y precio.

**Capítulo:**
Agrupación de partidas por tipo de trabajo (Movimiento de tierras, Fontanería, etc.).

**Certificación:**
Reconocimiento oficial de trabajo ejecutado para fines de facturación.

**Cantidad Certificada:**
Cantidad de trabajo realmente ejecutado y aprobado para pago.

**Importe Certificado:**
Valor monetario de la cantidad certificada.

**Porcentaje de Ejecución:**
Proporción de trabajo ejecutado respecto al presupuestado (0-100%).

**DN (Diámetro Nominal):**
Diámetro interior aproximado de una tubería o accesorio.

**PN (Presión Nominal):**
Presión máxima de trabajo de un componente hidráulico.

**Naturaleza de Partida:**
Clasificación de la partida (Material, Mano de Obra, Equipamiento, etc.).

**Estado del Registro:**
- **Pendiente:** Recién creado, sin iniciar trabajo
- **WIP (Work In Progress):** Trabajo en curso
- **Finalizado:** Trabajo completado, pendiente de verificación
- **Completado:** Verificado y cerrado

---

## 🎯 AGGREGATE DESIGN GUIDELINES

### Principios

1. **Consistency Boundary:**
   - Cada Aggregate es un boundary de consistencia transaccional
   - Operaciones dentro de un Aggregate son atómicas

2. **Small Aggregates:**
   - Preferir Aggregates pequeños
   - Solo incluir entidades estrictamente necesarias para invariantes

3. **Reference by ID:**
   - Aggregates se referencian por ID, no por objeto
   - Ejemplo: Certificación tiene `partida_presupuesto_id`, no objeto `PartidaPresupuesto`

4. **Eventual Consistency Between Aggregates:**
   - Consistencia inmediata DENTRO del Aggregate
   - Consistencia eventual ENTRE Aggregates

### Aggregates Identificados

```
1. Registro (Root)
   └── Elemento (Entity)
   └── Fotografia (Value Object)

2. Parte (Root)
   └── [Sin entidades hijas, solo Value Objects]

3. Presupuesto (Root)
   └── PartidaPresupuesto (Entity)
   └── GrupoPartidas (Entity)

4. Certificación (Root)
   └── [Sin entidades hijas]

5. CatalogoHidraulica (Root)
   └── EspecificacionesTecnicas (Value Object)

6. CatalogoRegistros (Root)
   └── [Sin entidades hijas]
```

---

## 🚨 HOTSPOTS (Problemas/Dudas a Resolver)

### 1. 🔴 Validación de Cantidad Certificada vs Presupuestada

**Problema:** ¿Qué ocurre si se intenta certificar más cantidad de la presupuestada?

**Opciones:**
- A) Rechazar (hard rule)
- B) Permitir con advertencia
- C) Permitir y ajustar presupuesto automáticamente

**Decisión necesaria:** ¿Cuál es la política del negocio?

---

### 2. 🔴 Eliminación de Registros/Partes con Presupuestos

**Problema:** ¿Se puede eliminar un Registro que tiene Presupuestos asociados?

**Opciones:**
- A) No permitir (hard delete)
- B) Soft delete (marcar como eliminado)
- C) Cascade delete (eliminar todo)

**Decisión necesaria:** ¿Cuál es la política del negocio?

---

### 3. 🔴 Actualización de Precios del Catálogo

**Problema:** Si se actualiza el precio en el catálogo, ¿afecta a presupuestos existentes?

**Opciones:**
- A) No afecta (precio se copia al crear partida)
- B) Afecta solo si no está certificado
- C) Siempre afecta (precio es referencia)

**Decisión necesaria:** ¿Cuál es la política del negocio?

---

### 4. 🔴 Estados de Certificación

**Problema:** El código no muestra estados explícitos de certificación (Borrador, Aprobada, etc.)

**Decisión necesaria:** ¿Existen estados? ¿O es simplemente crear y certificar?

---

## 📊 PRÓXIMOS PASOS

1. ✅ Resolver Hotspots con el usuario
2. ✅ Validar el modelo con el negocio
3. ✅ Documentar decisiones en ADRs
4. ✅ Comenzar implementación del Domain Layer

---

**Fin del Event Storming**
**Siguiente:** Implementar Domain Layer basado en este modelo
