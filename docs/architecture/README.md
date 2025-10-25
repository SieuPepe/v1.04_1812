# Arquitectura del Sistema - v1.04_1812

**Última actualización:** 2025-10-25
**Versión:** 2.0 - Clean Architecture

---

## Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Principios Arquitectónicos](#principios-arquitectónicos)
3. [Capas de la Arquitectura](#capas-de-la-arquitectura)
4. [Flujo de Datos](#flujo-de-datos)
5. [Patrones de Diseño](#patrones-de-diseño)
6. [Convenciones de Código](#convenciones-de-código)

---

## Visión General

Este proyecto implementa **Clean Architecture** (Robert C. Martin) con 4 capas claramente separadas:

```
┌─────────────────────────────────────────────────┐
│         PRESENTATION LAYER (UI)                 │
│  CustomTkinter Views, Windows, Dialogs         │
│                      ↓                          │
│         APPLICATION LAYER (Use Cases)           │
│  CreateProject, GenerateBudget, etc.           │
│                      ↓                          │
│         DOMAIN LAYER (Business Logic)           │
│  Entities, Value Objects, Domain Services      │
│                      ↑                          │
│      INFRASTRUCTURE LAYER (Technical)           │
│  SQLite, File System, External APIs            │
└─────────────────────────────────────────────────┘

Regla: Dependencias apuntan HACIA DENTRO (hacia Domain)
```

### Objetivos

1. **Independencia de Frameworks:** Cambiar GUI/BD es trivial
2. **Testabilidad:** Lógica testeable sin UI
3. **Mantenibilidad:** Código organizado y limpio
4. **Escalabilidad:** Fácil añadir features
5. **Calidad:** Type hints 100%, TDD, >90% coverage

---

## Principios Arquitectónicos

### 1. Dependency Rule (Regla de Dependencia)

> "Las dependencias del código fuente solo pueden apuntar HACIA DENTRO"

```
Presentation → Application → Domain
       ↓              ↓
Infrastructure ←──────┘
```

**Implicaciones:**
- Domain no conoce Application, Infrastructure ni Presentation
- Application conoce Domain pero no Infrastructure ni Presentation
- Infrastructure y Presentation conocen Domain y Application

### 2. SOLID Principles

#### S - Single Responsibility Principle
Cada clase tiene una única responsabilidad.

```python
# ✅ CORRECTO
class ProjectValidator:
    """Solo valida proyectos."""
    def validate(self, project: Project) -> List[str]:
        ...

class ProjectRepository:
    """Solo persiste proyectos."""
    def save(self, project: Project) -> None:
        ...
```

#### O - Open/Closed Principle
Abierto para extensión, cerrado para modificación.

```python
# ✅ CORRECTO - Extensible via Protocol
class IProjectRepository(Protocol):
    def save(self, project: Project) -> None:
        ...

# Nuevas implementaciones sin modificar código existente
class SQLiteProjectRepository:
    ...

class PostgreSQLProjectRepository:
    ...
```

#### L - Liskov Substitution Principle
Los subtipos deben ser sustituibles por sus tipos base.

```python
# ✅ CORRECTO
def process_repository(repo: IProjectRepository):
    # Funciona con CUALQUIER implementación de IProjectRepository
    repo.save(project)
```

#### I - Interface Segregation Principle
Interfaces específicas mejor que una genérica.

```python
# ✅ CORRECTO - Interfaces segregadas
class IReadRepository(Protocol):
    def get_by_id(self, id: UUID) -> Optional[T]:
        ...

class IWriteRepository(Protocol):
    def save(self, entity: T) -> None:
        ...

# Cliente solo depende de lo que necesita
class ReadOnlyService:
    def __init__(self, repo: IReadRepository):
        ...
```

#### D - Dependency Inversion Principle
Depender de abstracciones, no de concreciones.

```python
# ✅ CORRECTO
class CreateProjectUseCase:
    def __init__(self, repo: IProjectRepository):  # ← Abstracción (Protocol)
        self._repo = repo

# ❌ INCORRECTO
class CreateProjectUseCase:
    def __init__(self, repo: SQLiteProjectRepository):  # ← Concreción
        self._repo = repo
```

### 3. DRY (Don't Repeat Yourself)

Evitar duplicación de código.

```python
# ✅ CORRECTO - Reutilizar
class BaseEntity:
    id: UUID
    created_at: datetime

class Project(BaseEntity):
    name: str
    # Hereda id y created_at

class User(BaseEntity):
    username: str
    # Hereda id y created_at
```

### 4. YAGNI (You Aren't Gonna Need It)

No implementar funcionalidad que no se necesita ahora.

```python
# ❌ INCORRECTO - Over-engineering
class Project:
    def export_to_xml(self):  # Nadie pidió XML
        ...

    def export_to_json(self):  # Nadie pidió JSON
        ...

    def export_to_yaml(self):  # Nadie pidió YAML
        ...

# ✅ CORRECTO - Solo lo necesario
class Project:
    def to_dict(self):  # Simple, se puede extender después
        ...
```

---

## Capas de la Arquitectura

### Layer 1: Domain (src/domain/)

**Responsabilidad:** Lógica de negocio pura

**Contenido:**
- **Entities:** Objetos con identidad (Project, User, Part)
- **Value Objects:** Objetos inmutables (Money, Email, Address)
- **Repository Interfaces:** Contracts (IProjectRepository)
- **Domain Services:** Lógica que no pertenece a una entidad
- **Exceptions:** Errores de dominio

**Reglas:**
- ✅ Sin dependencias externas (ni siquiera frameworks)
- ✅ 100% testeable sin mocks
- ✅ Type hints obligatorios
- ✅ Inmutabilidad donde sea posible

**Ejemplo:**
```python
# src/domain/entities/project.py
@dataclass
class Project:
    """Entidad de dominio: Proyecto."""
    id: UUID
    name: str
    budget: Money

    def activate(self) -> None:
        """Activa el proyecto."""
        if self.status != "draft":
            raise ValidationError("Solo se pueden activar proyectos draft")
        self.status = "active"
```

### Layer 2: Application (src/application/)

**Responsabilidad:** Orquestación de casos de uso

**Contenido:**
- **Use Cases:** Lógica de aplicación (CreateProject, GenerateBudget)
- **DTOs:** Objetos de transferencia de datos
- **Service Interfaces:** Contracts para servicios externos

**Reglas:**
- ✅ Depende solo de Domain
- ✅ Sin lógica de negocio (esa va en Domain)
- ✅ Orquesta entidades y servicios
- ✅ Retorna DTOs, no Entities

**Ejemplo:**
```python
# src/application/use_cases/projects/create_project.py
class CreateProjectUseCase:
    """Caso de uso: Crear proyecto."""

    def __init__(self, repo: IProjectRepository):
        self._repo = repo

    def execute(self, data: ProjectDTO) -> Result[ProjectResponseDTO]:
        # 1. Crear entidad (Domain)
        project = Project.create(data.name, data.budget)

        # 2. Validar (Domain Service)
        validator = ProjectValidator()
        validator.validate(project)

        # 3. Persistir (Infrastructure via interface)
        self._repo.save(project)

        # 4. Retornar DTO
        return Result.success(ProjectResponseDTO.from_entity(project))
```

### Layer 3: Infrastructure (src/infrastructure/)

**Responsabilidad:** Implementaciones técnicas

**Contenido:**
- **Persistence:** Repositorios (SQLite, PostgreSQL, In-Memory)
- **File System:** Manejo de archivos e imágenes
- **Config:** Configuración de la aplicación
- **External:** APIs externas

**Reglas:**
- ✅ Implementa interfaces del Domain
- ✅ No expone detalles técnicos hacia arriba
- ✅ Intercambiable sin afectar lógica

**Ejemplo:**
```python
# src/infrastructure/persistence/sqlite/project_repository_impl.py
class SQLiteProjectRepository:
    """Implementación SQLite del repositorio de proyectos."""

    def __init__(self, connection: sqlite3.Connection):
        self._conn = connection

    def save(self, project: Project) -> None:
        """Guarda proyecto en SQLite."""
        cursor = self._conn.cursor()
        cursor.execute(
            "INSERT INTO projects (id, name, budget) VALUES (?, ?, ?)",
            (str(project.id), project.name, float(project.budget.amount))
        )
        self._conn.commit()

    def get_by_id(self, project_id: UUID) -> Optional[Project]:
        """Obtiene proyecto por ID."""
        cursor = self._conn.cursor()
        row = cursor.execute(
            "SELECT id, name, budget FROM projects WHERE id = ?",
            (str(project_id),)
        ).fetchone()

        if not row:
            return None

        return Project(
            id=UUID(row[0]),
            name=row[1],
            budget=Money(row[2], "EUR")
        )
```

### Layer 4: Presentation (src/presentation/)

**Responsabilidad:** Interfaz de usuario

**Contenido:**
- **Windows:** Ventanas principales
- **Dialogs:** Diálogos modales
- **Components:** Componentes reutilizables
- **Presenters:** MVP pattern
- **ViewModels:** Estado de la UI

**Reglas:**
- ✅ Depende de Application (Use Cases)
- ✅ Solo UI, sin lógica de negocio
- ✅ Testeable con mocks

**Ejemplo:**
```python
# src/presentation/windows/manager/manager_project_window.py
class ManagerProjectWindow(BaseWindow):
    """Ventana de gestión de proyectos."""

    def __init__(self, create_use_case: CreateProjectUseCase):
        self._create_use_case = create_use_case
        super().__init__()

    def on_save_clicked(self) -> None:
        """Handler del botón guardar."""
        # 1. Recoger datos del formulario
        data = ProjectDTO(
            name=self.name_entry.get(),
            budget=Money(float(self.budget_entry.get()), "EUR")
        )

        # 2. Ejecutar Use Case
        result = self._create_use_case.execute(data)

        # 3. Mostrar resultado
        if result.is_success:
            show_success("Proyecto creado")
            self.close()
        else:
            show_error(result.error)
```

---

## Flujo de Datos

### Ejemplo: Crear Proyecto

```
1. USER clicks "Guardar"
         ↓
2. PRESENTATION (ManagerProjectWindow)
   - Recoger datos del formulario
   - Crear ProjectDTO
         ↓
3. APPLICATION (CreateProjectUseCase)
   - Validar datos
   - Crear entidad Project
         ↓
4. DOMAIN (Project.create())
   - Aplicar reglas de negocio
   - Validaciones
         ↓
5. APPLICATION continúa
   - Llamar repository.save()
         ↓
6. INFRASTRUCTURE (SQLiteProjectRepository)
   - Persistir en BD
         ↓
7. APPLICATION retorna Result
         ↓
8. PRESENTATION muestra resultado
   - show_success() o show_error()
```

### Diagrama de Secuencia

```
User → ManagerProjectWindow → CreateProjectUseCase → Project.create()
                ↓                      ↓                     ↓
            form data              ProjectDTO          Project entity
                                       ↓                     ↓
                               IProjectRepository      Validations
                                       ↓
                          SQLiteProjectRepository
                                       ↓
                                   Database
```

---

## Patrones de Diseño

### 1. Repository Pattern

**Propósito:** Abstraer persistencia de datos

```python
# Domain: Interface
class IProjectRepository(Protocol):
    def save(self, project: Project) -> None:
        ...

# Infrastructure: Implementaciones
class SQLiteProjectRepository:  # Para producción
    ...

class InMemoryProjectRepository:  # Para tests
    ...
```

### 2. Use Case Pattern

**Propósito:** Encapsular lógica de aplicación

```python
class CreateProjectUseCase:
    """Un caso de uso = una acción del usuario."""

    def execute(self, data: ProjectDTO) -> Result:
        # Toda la lógica para crear proyecto
        ...
```

### 3. DTO Pattern (Data Transfer Object)

**Propósito:** Transferir datos entre capas

```python
@dataclass
class ProjectDTO:
    """DTO para crear proyecto."""
    name: str
    budget: Money

@dataclass
class ProjectResponseDTO:
    """DTO de respuesta."""
    id: UUID
    name: str
    budget: Money

    @classmethod
    def from_entity(cls, project: Project) -> "ProjectResponseDTO":
        return cls(id=project.id, name=project.name, budget=project.budget)
```

### 4. Value Object Pattern

**Propósito:** Objetos inmutables definidos por sus valores

```python
@dataclass(frozen=True)  # Inmutable
class Money:
    """Value Object para dinero."""
    amount: Decimal
    currency: str

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Monedas diferentes")
        return Money(self.amount + other.amount, self.currency)
```

### 5. Factory Pattern

**Propósito:** Encapsular creación de objetos complejos

```python
class ProjectFactory:
    """Factory para crear proyectos."""

    @staticmethod
    def create_from_dto(dto: ProjectDTO) -> Project:
        return Project.create(
            name=dto.name,
            code=ProjectFactory._generate_code(),
            budget=dto.budget
        )

    @staticmethod
    def _generate_code() -> str:
        return f"PROJ-{datetime.now().year}-{uuid4().hex[:6].upper()}"
```

### 6. Result Pattern

**Propósito:** Manejar éxito/fracaso sin excepciones

```python
@dataclass
class Result(Generic[T]):
    """Result type para operaciones."""
    value: Optional[T] = None
    error: Optional[str] = None

    @property
    def is_success(self) -> bool:
        return self.error is None

    @classmethod
    def success(cls, value: T) -> "Result[T]":
        return cls(value=value)

    @classmethod
    def failure(cls, error: str) -> "Result[T]":
        return cls(error=error)

# Uso
result = create_project(data)
if result.is_success:
    print(f"Created: {result.value}")
else:
    print(f"Error: {result.error}")
```

---

## Convenciones de Código

### Naming Conventions

```python
# Classes: PascalCase
class ProjectRepository:
    ...

# Functions/methods: snake_case
def get_project_by_id():
    ...

# Constants: UPPER_SNAKE_CASE
MAX_NAME_LENGTH = 200
DEFAULT_CURRENCY = "EUR"

# Private: _leading_underscore
class Project:
    def _validate(self):  # Private method
        ...

    def __private_implementation(self):  # Name mangling
        ...

# Protocols (Interfaces): INameProtocol
class IProjectRepository(Protocol):
    ...
```

### File Organization

```python
# One class per file (preferably)
# src/domain/entities/project.py
class Project:
    ...

# src/domain/entities/user.py
class User:
    ...

# Multiple related classes OK if small
# src/domain/value_objects/money.py
class Money:
    ...

class Currency:
    ...
```

### Import Organization (isort)

```python
# 1. Standard library
import os
import sys
from datetime import datetime
from typing import List, Optional

# 2. Third-party
import customtkinter
from PIL import Image

# 3. First-party (src)
from src.domain.entities.project import Project
from src.domain.value_objects.money import Money
```

### Docstrings (Google Style)

```python
def calculate_total(items: List[Item]) -> Money:
    """
    Calcula el total de una lista de items.

    Args:
        items: Lista de items a sumar

    Returns:
        Total como Money

    Raises:
        ValueError: Si items está vacío
        ValidationError: Si algún item es inválido

    Example:
        >>> items = [Item(price=Money(10, "EUR")), Item(price=Money(20, "EUR"))]
        >>> total = calculate_total(items)
        >>> print(total)
        Money(amount=Decimal('30'), currency='EUR')
    """
    ...
```

---

## Recursos Adicionales

- [ADR 0001: Clean Architecture](../adr/0001-use-clean-architecture.md)
- [ADR 0002: TDD](../adr/0002-use-tdd.md)
- [ADR 0003: Type Hints](../adr/0003-type-hints-enforcement.md)
- [Guía de Desarrollo](../guides/development.md)
- [Guía de Testing](../guides/testing.md)

---

**Última revisión:** 2025-10-25
