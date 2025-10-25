# ADR 0003: Enforcement de Type Hints 100%

**Fecha:** 2025-10-25
**Estado:** Aceptado
**Autores:** Claude Code, SieuPepe

---

## Contexto

Python es un lenguaje **dinámicamente tipado**, lo que causa problemas:

1. **Errores en runtime:** `AttributeError` cuando esperas un objeto y recibes `None`
2. **Refactorización arriesgada:** No sabes qué métodos usan qué tipos
3. **IDE limitado:** Auto-completado y refactorings no funcionan bien
4. **Documentación implícita:** No está claro qué tipos acepta/retorna una función

**Ejemplo de problema actual:**
```python
# ¿Qué retorna esta función? ¿Puede ser None?
def get_project(project_id):
    # ...código...
    return result  # ¿dict? ¿Project? ¿None?
```

---

## Decisión

Requerimos **Type Hints 100%** en todo el código nuevo, validado con **mypy strict mode**.

### Regla Estricta

```python
# ✅ CORRECTO - Type hints completos
from typing import Optional
from uuid import UUID

def get_project(project_id: UUID) -> Optional[Project]:
    """
    Obtiene un proyecto por ID.

    Args:
        project_id: UUID del proyecto

    Returns:
        Proyecto si existe, None si no
    """
    ...

# ❌ INCORRECTO - Sin type hints
def get_project(project_id):
    ...
```

### Mypy Strict Mode

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true        # ← Obliga type hints
disallow_incomplete_defs = true     # ← Obliga completar todos los tipos
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
```

---

## Tipos de Type Hints Requeridos

### 1. Funciones y Métodos

```python
# Parámetros y retorno
def calculate_total(amount: Decimal, tax_rate: Decimal) -> Money:
    ...

# Sin retorno
def log_message(message: str) -> None:
    ...

# Métodos de clase
@classmethod
def create(cls, name: str) -> "Project":
    ...

# Métodos estáticos
@staticmethod
def validate_code(code: str) -> bool:
    ...
```

### 2. Variables

```python
# Variables de instancia
class Project:
    name: str
    budget: Money
    created_at: datetime

# Variables de módulo
DEFAULT_CURRENCY: str = "EUR"
MAX_NAME_LENGTH: int = 200

# Variables locales (cuando no es obvio)
projects: List[Project] = []
result: Optional[Project] = None
```

### 3. Dataclasses

```python
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Money:
    """Value Object para dinero."""
    amount: Decimal
    currency: str

    def __add__(self, other: "Money") -> "Money":
        ...
```

### 4. Protocols (Interfaces)

```python
from typing import Protocol, Optional
from uuid import UUID

class IProjectRepository(Protocol):
    """Interface del repositorio de proyectos."""

    def save(self, project: Project) -> None:
        ...

    def get_by_id(self, project_id: UUID) -> Optional[Project]:
        ...
```

### 5. Generics

```python
from typing import TypeVar, Generic, List

T = TypeVar('T')

class Repository(Generic[T]):
    """Repositorio genérico."""

    def get_all(self) -> List[T]:
        ...

    def get_by_id(self, id: UUID) -> Optional[T]:
        ...
```

### 6. Union Types y Optional

```python
from typing import Union, Optional

# Optional[X] es equivalente a Union[X, None]
def get_project(id: UUID) -> Optional[Project]:
    ...

# Union para múltiples tipos posibles
def process_input(data: Union[str, int, dict]) -> Result:
    ...

# Python 3.10+ syntax (cuando migremos)
# def get_project(id: UUID) -> Project | None:
#     ...
```

---

## Beneficios

### 1. Detección de Errores en Tiempo de Desarrollo

```python
# ❌ mypy detecta este error ANTES de ejecutar
def calculate_total(items: List[Item]) -> Money:
    total = 0  # mypy error: incompatible type (int != Money)
    for item in items:
        total += item.price  # mypy error: Money + Money -> Money, not int
    return total
```

**Sin type hints:** Error en runtime `TypeError: unsupported operand type(s)`
**Con type hints:** Error en editor/CI ANTES de ejecutar

### 2. IDE Superpowers

```python
project: Project = get_project(id)

# IDE sabe que project es Project, entonces auto-completa:
project.name         # ✅ Sugerido
project.budget       # ✅ Sugerido
project.activate()   # ✅ Sugerido
project.foo()        # ❌ Error: Project no tiene método foo
```

### 3. Refactorización Segura

```python
# Renombrar método: IDE encuentra TODOS los usos
class Project:
    def calculate_cost(self) -> Money:  # Renombrar a calculate_total_cost
        ...

# Si falta type hint, IDE puede no encontrar algunos usos
```

### 4. Documentación Auto-Generada

```python
def create_project(
    name: str,
    budget: Money,
    customer_id: UUID,
    date_range: DateRange
) -> Result[Project]:
    """
    Crea un nuevo proyecto.

    Los tipos ya están documentados en la firma.
    No necesitas repetirlos en el docstring.
    """
    ...
```

### 5. Tests Más Confiables

```python
# Mock con tipos correctos
def test_create_project(mock_repo: IProjectRepository):
    # mypy verifica que mock_repo implementa IProjectRepository
    use_case = CreateProjectUseCase(mock_repo)
    ...
```

---

## Herramientas

### 1. mypy - Type Checker

```bash
# Verificar tipos
mypy src

# Con pretty output
mypy src --pretty

# Solo errores críticos
mypy src --no-error-summary
```

### 2. Pre-commit Hook

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/pre-commit/mirrors-mypy
  rev: v1.8.0
  hooks:
    - id: mypy
      additional_dependencies: [types-all]
```

### 3. CI/CD

```yaml
# .github/workflows/ci.yml
- name: Type check with mypy
  run: mypy src --pretty
```

### 4. IDE Integration

**VSCode:** Python extension + Pylance
**PyCharm:** Soporte nativo
**Vim/Neovim:** coc-pyright

---

## Casos Especiales

### 1. Código Legacy

```python
# Para código legacy, usar # type: ignore
from v1.04_1812.interface.legacy import old_function

result = old_function()  # type: ignore[no-untyped-call]
```

### 2. Librerías sin Stubs

```python
# pyproject.toml
[[tool.mypy.overrides]]
module = "customtkinter.*"
ignore_missing_imports = true
```

### 3. Any (uso limitado)

```python
from typing import Any

# Solo cuando realmente puede ser cualquier tipo
def serialize(obj: Any) -> str:
    return json.dumps(obj)
```

**Regla:** Evitar `Any`, solo usarlo cuando sea realmente necesario.

### 4. Forward References

```python
from __future__ import annotations  # Python 3.7+

class Parent:
    def get_child(self) -> Child:  # ✅ OK con __future__
        ...

class Child:
    def get_parent(self) -> Parent:
        ...
```

---

## Estrategia de Implementación

### Fase 1: Domain Layer
- **100% type hints** desde el inicio
- **mypy strict:** Sin excepciones
- **CI fail:** Si mypy encuentra error

### Fase 2+: Resto de Capas
- **100% type hints** obligatorio
- **Gradual:** Añadir tipos a código legacy cuando se toque

### Código Legacy
- **No modificar:** Dejar sin type hints
- **Cuando se toque:** Añadir type hints
- **Usar # type: ignore:** Para evitar errores

---

## Métricas

### Coverage de Type Hints

```bash
# Usando mypy --strict y contando errores
mypy src --strict 2>&1 | grep "error:" | wc -l
```

**Objetivo:** 0 errores de mypy

### Dashboard

- Integrar con SonarQube o similar
- Tracking de type coverage en CI

---

## Ejemplos Completos

### Entidad con Types

```python
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from ..value_objects.money import Money
from ..exceptions import ValidationError


@dataclass
class Project:
    """Entidad de dominio: Proyecto."""

    id: UUID
    name: str
    code: str
    budget: Money
    status: str = "draft"
    created_at: datetime = field(default_factory=datetime.now)
    _parts: List[Part] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not self.name:
            raise ValidationError("Nombre requerido")

    @classmethod
    def create(
        cls,
        name: str,
        code: str,
        budget: Money
    ) -> Project:
        return cls(
            id=uuid4(),
            name=name,
            code=code,
            budget=budget
        )

    def activate(self) -> None:
        if self.status != "draft":
            raise ValidationError("Solo se pueden activar proyectos draft")
        self.status = "active"

    def calculate_total(self) -> Money:
        total: Money = Money(0, self.budget.currency)
        part: Part
        for part in self._parts:
            total = total + part.cost
        return total
```

### Use Case con Types

```python
from typing import Optional
from uuid import UUID

from src.domain.entities.project import Project
from src.domain.repositories.project_repository import IProjectRepository
from src.application.dtos.project_dto import ProjectDTO, ProjectResponseDTO
from .result import Result


class CreateProjectUseCase:
    """Caso de uso: Crear proyecto."""

    def __init__(self, repo: IProjectRepository) -> None:
        self._repo = repo

    def execute(self, data: ProjectDTO) -> Result[ProjectResponseDTO]:
        """
        Ejecuta el caso de uso.

        Args:
            data: Datos del proyecto

        Returns:
            Result con ProjectResponseDTO si success, error si falla
        """
        try:
            # Crear entidad
            project: Project = Project.create(
                name=data.name,
                code=data.code,
                budget=data.budget
            )

            # Guardar
            self._repo.save(project)

            # Retornar DTO de respuesta
            response: ProjectResponseDTO = ProjectResponseDTO.from_entity(project)
            return Result.success(response)

        except ValidationError as e:
            return Result.failure(str(e))
```

---

## Consecuencias

### Positivas
- ✅ Errores detectados en desarrollo
- ✅ IDE muy poderoso
- ✅ Refactorización segura
- ✅ Documentación automática
- ✅ Código auto-documentado

### Negativas
- ❌ Curva de aprendizaje (1-2 días)
- ❌ Más código (type hints verbosos)
- ❌ Mypy puede ser lento en proyectos grandes

---

## Recursos

- [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)
- [Mypy Documentation](https://mypy.readthedocs.io/)
- [Python Type Checking Guide](https://realpython.com/python-type-checking/)
- [typing module](https://docs.python.org/3/library/typing.html)

---

## Decisión Final

**APROBADO** - Type hints 100% + mypy strict
**Fecha de decisión:** 2025-10-25
**Enforcement:** CI/CD + Pre-commit hooks
