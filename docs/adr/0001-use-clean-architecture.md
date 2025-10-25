# ADR 0001: Usar Clean Architecture

**Fecha:** 2025-10-25
**Estado:** Aceptado
**Autores:** Claude Code, SieuPepe
**Decisores:** SieuPepe

---

## Contexto

El código actual de interfaces tiene los siguientes problemas:

1. **Acoplamiento alto:** UI mezclada con lógica de negocio y acceso a BD
2. **Testabilidad baja:** Imposible testear lógica sin GUI
3. **Mantenibilidad baja:** Archivos de 3,500+ líneas con 60+ métodos
4. **Duplicación masiva:** 50% del código está duplicado
5. **Cambiar frameworks:** Muy costoso cambiar CustomTkinter por otro

### Requisito del usuario

> "Quiero el mejor software posible. NO me importa si tardamos más tiempo."

Esto indica que la prioridad es **calidad a largo plazo** sobre velocidad de entrega.

---

## Decisión

Adoptaremos **Clean Architecture** (Robert C. Martin) con 4 capas claramente separadas:

### 1. Domain Layer (Capa de Dominio)
- **Responsabilidad:** Lógica de negocio pura
- **Contenido:** Entidades, Value Objects, Repository Interfaces, Domain Services
- **Dependencias:** NINGUNA (núcleo independiente)
- **Ubicación:** `src/domain/`

### 2. Application Layer (Capa de Aplicación)
- **Responsabilidad:** Casos de uso de la aplicación
- **Contenido:** Use Cases, DTOs, Service Interfaces
- **Dependencias:** Solo Domain Layer
- **Ubicación:** `src/application/`

### 3. Infrastructure Layer (Capa de Infraestructura)
- **Responsabilidad:** Implementaciones técnicas
- **Contenido:** Repositories (SQLite), File System, Config, External APIs
- **Dependencias:** Domain, Application
- **Ubicación:** `src/infrastructure/`

### 4. Presentation Layer (Capa de Presentación)
- **Responsabilidad:** Interfaz de usuario
- **Contenido:** Windows, Dialogs, Presenters, ViewModels
- **Dependencias:** Application, Domain (via interfaces)
- **Ubicación:** `src/presentation/`

### Regla de Dependencia

```
Presentation → Application → Domain
       ↓              ↓
Infrastructure ←──────┘

IMPORTANTE: Las dependencias apuntan HACIA DENTRO (hacia Domain)
```

---

## Consecuencias

### Positivas

1. **Independencia de Frameworks**
   - Cambiar de CustomTkinter a PyQt: 1-2 días (vs 2 semanas)
   - Cambiar de SQLite a PostgreSQL: 1 día (vs 1 semana)

2. **Testabilidad Extrema**
   - Lógica de negocio testeable en 0.001s (vs 500ms con GUI)
   - Tests independientes de UI
   - Coverage puede ser >95%

3. **Reutilización**
   - Use Cases sirven para: GUI, CLI, API REST, gRPC
   - Añadir API REST: 1 día (solo adaptadores)

4. **Mantenibilidad**
   - Cada capa tiene responsabilidad clara
   - Cambios localizados (no en cascada)
   - Fácil onboarding (<1 semana)

5. **Escalabilidad**
   - Añadir features no rompe existentes
   - Equipos pueden trabajar en capas diferentes
   - Crece sin volverse unmaintainable

### Negativas

1. **Complejidad Inicial**
   - Más archivos (60+ archivos vs 47 actuales)
   - Curva de aprendizaje (1-2 días)
   - Require entender arquitectura

2. **Tiempo de Desarrollo**
   - Fase inicial: 27-40 días (vs 7-10 días refactorización simple)
   - Más código "glue" (adaptadores, DTOs)

3. **Over-engineering**
   - Puede ser excesivo para proyectos muy pequeños
   - Requiere disciplina del equipo

---

## Alternativas Consideradas

### Alternativa 1: MVC Simple
**Pros:** Rápido, fácil de entender
**Contras:** UI y lógica todavía acopladas, difícil testear
**Razón de rechazo:** No cumple requisito de "mejor software posible"

### Alternativa 2: MVP (Model-View-Presenter)
**Pros:** Mejor que MVC, separa lógica de UI
**Contras:** No separa lógica de negocio de infraestructura
**Razón de rechazo:** Insuficiente para proyectos a largo plazo

### Alternativa 3: MVVM (Model-View-ViewModel)
**Pros:** Bueno para binding de datos
**Contras:** Específico para UI reactiva, no separa infraestructura
**Razón de rechazo:** No es arquitectura completa

### Alternativa 4: Hexagonal Architecture (Ports & Adapters)
**Pros:** Similar a Clean Architecture, muy buena
**Contras:** Más compleja, menos documentación
**Razón de rechazo:** Clean Architecture es más conocida y documentada

---

## Implementación

### Fase 0: Fundaciones (actual)
- ✅ Crear estructura de carpetas
- ✅ Configurar herramientas de calidad
- ✅ ADRs iniciales
- ⏳ Event Storming del dominio

### Fases Futuras
- Fase 1: Domain Layer (4-6 días)
- Fase 2: Application Layer (3-5 días)
- Fase 3: Infrastructure Layer (4-6 días)
- Fase 4: Presentation Layer (6-8 días)
- Fase 5: Integration & Testing (3-5 días)

---

## Recursos

- [Clean Architecture (Uncle Bob)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Clean Architecture Book](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164)
- [Python Clean Architecture Example](https://github.com/pcah/python-clean-architecture)

---

## Notas

Esta decisión es **reversible parcialmente:**
- Se puede volver a arquitectura simple después de Fase 1-2
- Difícil reversión después de Fase 3-4
- Imposible reversión después de Fase 5

**Punto de no retorno:** Fase 3 (Infrastructure)

---

## Decisión Final

**APROBADO** - Implementar Clean Architecture completa
**Fecha de decisión:** 2025-10-25
**Próxima revisión:** Después de Fase 1 (Domain Layer)
