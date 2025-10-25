# PLAN DE EXCELENCIA - REFACTORIZACIÓN DE INTERFACES

**Versión:** 2.0 - Excelencia Total
**Fecha:** 2025-10-25
**Objetivo:** Crear el mejor software posible, sin compromisos de calidad

---

## FILOSOFÍA: CALIDAD SOBRE VELOCIDAD

> "La única manera de ir rápido es ir bien" - Robert C. Martin (Uncle Bob)

Este plan NO busca el camino más rápido, sino el **camino correcto**. Aplicaremos:

- ✅ **Clean Architecture** (Arquitectura Limpia)
- ✅ **SOLID Principles** (Principios sólidos de diseño)
- ✅ **TDD** (Test-Driven Development)
- ✅ **Type Safety** (Type hints completos + mypy)
- ✅ **Documentation First** (Documentación exhaustiva)
- ✅ **Design Patterns** (Patrones de diseño apropiados)
- ✅ **Performance Testing** (Benchmarks y profiling)
- ✅ **Code Review** (Revisión rigurosa)
- ✅ **CI/CD** (Integración y despliegue continuo)

---

## DIFERENCIAS CON EL PLAN BÁSICO

| Aspecto | Plan Básico | Plan Excelencia |
|---------|-------------|-----------------|
| **Tests** | Al final | TDD desde el inicio |
| **Type hints** | Opcional | Obligatorio (100%) |
| **Documentación** | Básica | Exhaustiva (docstrings, diagramas, ADRs) |
| **Arquitectura** | Refactorización | Rediseño completo (Clean Architecture) |
| **Patterns** | Ad-hoc | Catálogo formal de patrones |
| **CI/CD** | No | Pipeline completo |
| **Code review** | Manual | Automatizado + manual |
| **Performance** | No verificado | Benchmarks y profiling |
| **Tiempo estimado** | 7-10 días | 15-25 días |
| **Calidad final** | Buena | Excelente |

---

## ARQUITECTURA OBJETIVO: CLEAN ARCHITECTURE

Vamos a implementar **Clean Architecture** de Robert C. Martin adaptada a GUI:

```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                      │
│  (CustomTkinter Views - Solo UI, sin lógica)               │
│                                                             │
│  - ManagerProjectView                                       │
│  - UserProjectView                                          │
│  - PartsManagerView                                         │
│  - Dialogs (CustomerDialog, ItemDialog, etc.)              │
└──────────────────┬──────────────────────────────────────────┘
                   │ Dependency Inversion
                   ↓
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                        │
│  (Use Cases / Interactors - Lógica de aplicación)          │
│                                                             │
│  - CreateProjectUseCase                                     │
│  - UpdateProjectUseCase                                     │
│  - DeleteProjectUseCase                                     │
│  - ListProjectsUseCase                                      │
│  - GenerateBudgetUseCase                                    │
│  - ... etc                                                  │
└──────────────────┬──────────────────────────────────────────┘
                   │ Interfaces (Protocols)
                   ↓
┌─────────────────────────────────────────────────────────────┐
│                      DOMAIN LAYER                           │
│  (Business Logic - Independiente de frameworks)            │
│                                                             │
│  - Entities: Project, Part, User, Budget, etc.             │
│  - Value Objects: Money, Address, Email, etc.              │
│  - Domain Services: ProjectValidator, BudgetCalculator      │
│  - Repository Interfaces (Protocols)                        │
└──────────────────┬──────────────────────────────────────────┘
                   │ Implementation
                   ↓
┌─────────────────────────────────────────────────────────────┐
│                   INFRASTRUCTURE LAYER                      │
│  (Detalles técnicos - BD, archivos, APIs)                  │
│                                                             │
│  - SQLite Repository Implementations                        │
│  - File System (images, exports)                           │
│  - Configuration Management                                 │
│  - External Services (si aplica)                            │
└─────────────────────────────────────────────────────────────┘

REGLA DE DEPENDENCIAS:
→ Las dependencias apuntan HACIA DENTRO (hacia Domain)
→ Domain no conoce nada de capas externas
→ Application usa Interfaces del Domain
→ Presentation usa Interfaces del Application
→ Infrastructure implementa interfaces del Domain
```

### Beneficios de Clean Architecture

1. **Independencia de Frameworks**: Puedes cambiar CustomTkinter por PyQt sin tocar lógica
2. **Testabilidad**: Cada capa se testea independientemente
3. **Independencia de UI**: La lógica no sabe si es GUI, CLI o Web
4. **Independencia de BD**: Puedes cambiar SQLite por PostgreSQL fácilmente
5. **Business Logic Protegida**: Las reglas de negocio están aisladas

---

## ESTRUCTURA DE PROYECTO COMPLETA

```
v1.04_1812/
├── src/                                    # Código fuente principal
│   ├── domain/                            # 🟢 CAPA DE DOMINIO
│   │   ├── entities/                      # Entidades de negocio
│   │   │   ├── __init__.py
│   │   │   ├── project.py                # class Project (Entity)
│   │   │   ├── part.py                   # class Part (Entity)
│   │   │   ├── user.py                   # class User (Entity)
│   │   │   ├── budget.py                 # class Budget (Entity)
│   │   │   ├── certification.py          # class Certification (Entity)
│   │   │   └── customer.py               # class Customer (Entity)
│   │   │
│   │   ├── value_objects/                # Value Objects (inmutables)
│   │   │   ├── __init__.py
│   │   │   ├── money.py                  # class Money (VO)
│   │   │   ├── address.py                # class Address (VO)
│   │   │   ├── email.py                  # class Email (VO)
│   │   │   ├── phone.py                  # class Phone (VO)
│   │   │   └── date_range.py             # class DateRange (VO)
│   │   │
│   │   ├── repositories/                 # Interfaces de repositorios
│   │   │   ├── __init__.py
│   │   │   ├── project_repository.py     # Protocol: IProjectRepository
│   │   │   ├── part_repository.py        # Protocol: IPartRepository
│   │   │   ├── user_repository.py        # Protocol: IUserRepository
│   │   │   └── budget_repository.py      # Protocol: IBudgetRepository
│   │   │
│   │   ├── services/                     # Servicios de dominio
│   │   │   ├── __init__.py
│   │   │   ├── project_validator.py      # Validaciones de negocio
│   │   │   ├── budget_calculator.py      # Cálculos de presupuesto
│   │   │   ├── certification_generator.py
│   │   │   └── price_calculator.py
│   │   │
│   │   └── exceptions/                   # Excepciones de dominio
│   │       ├── __init__.py
│   │       ├── validation_error.py
│   │       ├── business_rule_error.py
│   │       └── not_found_error.py
│   │
│   ├── application/                       # 🔵 CAPA DE APLICACIÓN
│   │   ├── use_cases/                    # Casos de uso
│   │   │   ├── projects/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── create_project.py     # CreateProjectUseCase
│   │   │   │   ├── update_project.py     # UpdateProjectUseCase
│   │   │   │   ├── delete_project.py     # DeleteProjectUseCase
│   │   │   │   ├── get_project.py        # GetProjectUseCase
│   │   │   │   └── list_projects.py      # ListProjectsUseCase
│   │   │   │
│   │   │   ├── parts/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── add_part.py
│   │   │   │   ├── update_part.py
│   │   │   │   └── remove_part.py
│   │   │   │
│   │   │   ├── budgets/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── generate_budget.py
│   │   │   │   ├── export_budget.py
│   │   │   │   └── calculate_costs.py
│   │   │   │
│   │   │   └── users/
│   │   │       ├── __init__.py
│   │   │       ├── authenticate_user.py
│   │   │       ├── create_user.py
│   │   │       └── update_privileges.py
│   │   │
│   │   ├── dtos/                         # Data Transfer Objects
│   │   │   ├── __init__.py
│   │   │   ├── project_dto.py
│   │   │   ├── part_dto.py
│   │   │   └── user_dto.py
│   │   │
│   │   └── interfaces/                   # Interfaces de servicios externos
│   │       ├── __init__.py
│   │       ├── email_service.py          # Protocol: IEmailService
│   │       └── file_service.py           # Protocol: IFileService
│   │
│   ├── infrastructure/                    # 🟡 CAPA DE INFRAESTRUCTURA
│   │   ├── persistence/                  # Implementaciones de BD
│   │   │   ├── __init__.py
│   │   │   ├── sqlite/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── connection.py         # Connection factory
│   │   │   │   ├── project_repository_impl.py
│   │   │   │   ├── part_repository_impl.py
│   │   │   │   ├── user_repository_impl.py
│   │   │   │   └── migrations/           # DB migrations
│   │   │   │
│   │   │   └── in_memory/               # Para testing
│   │   │       ├── __init__.py
│   │   │       └── project_repository_mock.py
│   │   │
│   │   ├── file_system/                  # Archivos, imágenes
│   │   │   ├── __init__.py
│   │   │   ├── image_storage.py
│   │   │   └── export_service.py
│   │   │
│   │   ├── config/                       # Configuración
│   │   │   ├── __init__.py
│   │   │   ├── settings.py               # Pydantic Settings
│   │   │   └── logging_config.py
│   │   │
│   │   └── external/                     # Servicios externos
│   │       ├── __init__.py
│   │       └── email_service_impl.py
│   │
│   └── presentation/                      # 🔴 CAPA DE PRESENTACIÓN
│       ├── __init__.py
│       │
│       ├── common/                       # Componentes compartidos
│       │   ├── __init__.py
│       │   ├── base/                     # Clases base
│       │   │   ├── __init__.py
│       │   │   ├── base_window.py        # BaseWindow
│       │   │   ├── base_dialog.py        # BaseDialog
│       │   │   └── base_view.py          # BaseView
│       │   │
│       │   ├── components/               # Componentes reutilizables
│       │   │   ├── __init__.py
│       │   │   ├── sidebar.py
│       │   │   ├── data_table.py
│       │   │   ├── form_field.py
│       │   │   ├── logo_widget.py
│       │   │   └── toolbar.py
│       │   │
│       │   ├── dialogs/                  # Diálogos comunes
│       │   │   ├── __init__.py
│       │   │   ├── message_dialog.py
│       │   │   ├── confirmation_dialog.py
│       │   │   └── error_dialog.py
│       │   │
│       │   └── styles/                   # Estilos y temas
│       │       ├── __init__.py
│       │       ├── theme.py
│       │       ├── colors.py
│       │       └── fonts.py
│       │
│       ├── presenters/                   # Presenters (MVP pattern)
│       │   ├── __init__.py
│       │   ├── project_presenter.py
│       │   ├── part_presenter.py
│       │   └── budget_presenter.py
│       │
│       ├── view_models/                  # ViewModels
│       │   ├── __init__.py
│       │   ├── project_view_model.py
│       │   └── part_view_model.py
│       │
│       └── windows/                      # Ventanas principales
│           ├── __init__.py
│           │
│           ├── manager/                  # Ventanas de manager
│           │   ├── __init__.py
│           │   ├── manager_window.py
│           │   └── manager_project/
│           │       ├── __init__.py
│           │       ├── manager_project_window.py
│           │       ├── summary_tab.py
│           │       ├── inventory_tab.py
│           │       ├── budget_tab.py
│           │       └── certifications_tab.py
│           │
│           ├── user/                     # Ventanas de usuario
│           │   ├── __init__.py
│           │   └── user_project_window.py
│           │
│           ├── parts/                    # Generador de partes
│           │   ├── __init__.py
│           │   └── parts_manager_window.py
│           │
│           └── dialogs/                  # Diálogos específicos
│               ├── __init__.py
│               ├── customer_dialog.py
│               ├── item_dialog.py
│               └── register_dialog.py
│
├── tests/                                 # 🧪 TESTS
│   ├── unit/                             # Tests unitarios
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   ├── value_objects/
│   │   │   └── services/
│   │   │
│   │   ├── application/
│   │   │   └── use_cases/
│   │   │
│   │   └── infrastructure/
│   │       └── persistence/
│   │
│   ├── integration/                      # Tests de integración
│   │   ├── test_database.py
│   │   ├── test_use_cases.py
│   │   └── test_repositories.py
│   │
│   ├── ui/                               # Tests de UI
│   │   ├── test_windows.py
│   │   └── test_dialogs.py
│   │
│   ├── e2e/                              # Tests end-to-end
│   │   ├── test_project_workflow.py
│   │   └── test_budget_generation.py
│   │
│   ├── fixtures/                         # Datos de prueba
│   │   ├── __init__.py
│   │   ├── project_fixtures.py
│   │   └── user_fixtures.py
│   │
│   └── conftest.py                       # Configuración pytest
│
├── docs/                                  # 📚 DOCUMENTACIÓN
│   ├── architecture/                     # Arquitectura
│   │   ├── README.md
│   │   ├── clean_architecture.md
│   │   ├── layer_responsibilities.md
│   │   └── diagrams/
│   │       ├── architecture_overview.puml
│   │       ├── use_case_diagram.puml
│   │       └── sequence_diagrams/
│   │
│   ├── adr/                              # Architecture Decision Records
│   │   ├── 0001-use-clean-architecture.md
│   │   ├── 0002-repository-pattern.md
│   │   ├── 0003-use-cases-pattern.md
│   │   └── 0004-type-hints-enforcement.md
│   │
│   ├── api/                              # Documentación de API
│   │   ├── domain.md
│   │   ├── application.md
│   │   └── infrastructure.md
│   │
│   ├── guides/                           # Guías
│   │   ├── development.md
│   │   ├── testing.md
│   │   ├── contributing.md
│   │   └── deployment.md
│   │
│   └── diagrams/                         # Diagramas
│       ├── class_diagrams/
│       ├── sequence_diagrams/
│       └── component_diagrams/
│
├── scripts/                               # 🔧 SCRIPTS
│   ├── setup.sh                          # Setup inicial
│   ├── run_tests.sh                      # Ejecutar tests
│   ├── check_quality.sh                  # Verificar calidad
│   ├── generate_docs.sh                  # Generar documentación
│   └── performance/
│       ├── benchmark.py
│       └── profile.py
│
├── .github/                               # 🚀 CI/CD
│   └── workflows/
│       ├── ci.yml                        # Integración continua
│       ├── cd.yml                        # Despliegue continuo
│       └── code-quality.yml              # Verificación de calidad
│
├── config/                                # ⚙️ CONFIGURACIÓN
│   ├── development.env
│   ├── production.env
│   └── test.env
│
├── .pre-commit-config.yaml               # Pre-commit hooks
├── pyproject.toml                        # Configuración Python
├── requirements.txt                      # Dependencias producción
├── requirements-dev.txt                  # Dependencias desarrollo
├── mypy.ini                              # Configuración mypy
├── pytest.ini                            # Configuración pytest
├── .pylintrc                             # Configuración pylint
├── .editorconfig                         # Configuración editor
└── README.md                             # Documentación principal
```

---

## FASES DE IMPLEMENTACIÓN (ENFOQUE EXCELENCIA)

### FASE 0: FUNDACIONES (5-7 días)

#### DÍA 1-2: Infraestructura de Calidad

**1. Setup de herramientas de calidad**
```bash
# pyproject.toml con todas las herramientas
[tool.black]
line-length = 100
target-version = ['py39', 'py310', 'py311']

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.9"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --cov=src --cov-report=html --cov-report=term --cov-report=xml --cov-fail-under=80"

[tool.pylint.messages_control]
max-line-length = 100
disable = ["C0111"]  # Ajustar según necesidad

[tool.coverage.run]
source = ["src"]
omit = ["tests/*", "**/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

**2. Pre-commit hooks**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict
      - id: detect-private-key

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=100', '--extend-ignore=E203,W503']

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: https://github.com/pylint-dev/pylint
    rev: v3.0.3
    hooks:
      - id: pylint
        args: ['--max-line-length=100']

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.6
    hooks:
      - id: bandit
        args: ['-r', 'src']

  - repo: https://github.com/python-poetry/poetry
    rev: 1.7.0
    hooks:
      - id: poetry-check

  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
```

**3. CI/CD Pipeline**
```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [ main, develop, claude/* ]
  pull_request:
    branches: [ main, develop ]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run black
        run: black --check src tests

      - name: Run isort
        run: isort --check-only src tests

      - name: Run flake8
        run: flake8 src tests

      - name: Run pylint
        run: pylint src

      - name: Run mypy
        run: mypy src

      - name: Run bandit
        run: bandit -r src

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run tests
        run: pytest --cov=src --cov-report=xml

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml

  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run performance benchmarks
        run: python scripts/performance/benchmark.py

      - name: Store benchmark results
        uses: benchmark-action/github-action-benchmark@v1
```

#### DÍA 3-4: Modelado del Dominio

**Análisis completo del dominio del negocio:**

1. **Event Storming Session** (virtual o en papel)
   - Identificar todos los eventos del dominio
   - Mapear comandos que generan eventos
   - Identificar agregados y entidades

2. **Bounded Contexts**
   - Contexto de Proyectos
   - Contexto de Presupuestos
   - Contexto de Certificaciones
   - Contexto de Usuarios
   - Contexto de Catálogos

3. **Ubiquitous Language** (Lenguaje ubicuo)
   - Glosario de términos del dominio
   - Definiciones precisas de cada concepto
   - Acordar nombres en español/inglés

4. **Crear ADRs (Architecture Decision Records)**
   ```markdown
   # ADR 0001: Usar Clean Architecture

   ## Estado
   Aceptado

   ## Contexto
   El código actual tiene problemas de:
   - Acoplamiento alto entre UI y BD
   - Difícil de testear
   - Lógica de negocio dispersa

   ## Decisión
   Implementar Clean Architecture con 4 capas:
   Domain, Application, Infrastructure, Presentation

   ## Consecuencias
   ### Positivas
   - Lógica de negocio protegida
   - Altamente testeable
   - Independiente de frameworks

   ### Negativas
   - Más archivos y estructura
   - Curva de aprendizaje inicial
   - Mayor tiempo de desarrollo inicial

   ## Alternativas Consideradas
   - MVC simple
   - MVP
   - MVVM
   ```

#### DÍA 5-7: Tests de Caracterización

**Crear suite de tests ANTES de refactorizar** (Characterization Tests):

```python
# tests/characterization/test_manager_project_current.py
"""
Tests de caracterización: Documentan cómo funciona el código ACTUAL
antes de refactorizar. Si estos tests fallan después de refactorizar,
rompimos funcionalidad existente.
"""
import pytest
from interface.legacy.manager_project_interfaz import AppManagerProject

class TestManagerProjectCharacterization:
    """Tests que capturan el comportamiento actual"""

    def test_window_opens_successfully(self):
        """Verifica que la ventana se abre sin errores"""
        # Arrange
        master = MockMaster()
        project_id = 1
        access = ("user", "password")

        # Act
        window = AppManagerProject(master, project_id, access)

        # Assert
        assert window is not None
        assert window.winfo_exists()

    def test_sidebar_has_correct_buttons(self):
        """Verifica que el sidebar tiene los botones esperados"""
        # ... capturar comportamiento actual

    def test_data_loads_correctly(self):
        """Verifica que los datos se cargan correctamente"""
        # ... capturar comportamiento actual

    # ... 50-100 tests más que documenten TODO el comportamiento actual
```

**Objetivo:** Tener >200 characterization tests que garanticen que no rompemos nada.

---

### FASE 1: DOMAIN LAYER (4-6 días)

#### Principios a seguir:
1. **TDD estricto**: Tests PRIMERO, implementación DESPUÉS
2. **Type hints obligatorios**: 100% del código tipado
3. **Docstrings completos**: Cada clase y método documentado
4. **Inmutabilidad**: Value Objects inmutables (dataclasses frozen)
5. **Validation**: Validaciones en constructores

#### Implementación

**DÍA 1: Entidades Básicas**

```python
# src/domain/entities/project.py
"""
Entidad Project del dominio.

Esta entidad representa un proyecto en el sistema y contiene
toda la lógica de negocio relacionada con proyectos.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from ..value_objects.money import Money
from ..value_objects.date_range import DateRange
from ..exceptions.validation_error import ValidationError


@dataclass
class Project:
    """
    Entidad de dominio que representa un proyecto.

    Attributes:
        id: Identificador único del proyecto
        name: Nombre del proyecto
        code: Código único del proyecto (ej: "PROJ-2025-001")
        customer_id: ID del cliente asociado
        budget: Presupuesto del proyecto
        date_range: Rango de fechas del proyecto
        status: Estado actual (draft, active, completed, cancelled)
        created_at: Fecha de creación
        updated_at: Fecha de última modificación

    Raises:
        ValidationError: Si algún valor no cumple reglas de negocio

    Example:
        >>> budget = Money(10000, "EUR")
        >>> date_range = DateRange(start_date, end_date)
        >>> project = Project.create(
        ...     name="Nuevo Edificio",
        ...     code="PROJ-2025-001",
        ...     customer_id=customer_id,
        ...     budget=budget,
        ...     date_range=date_range
        ... )
    """

    id: UUID
    name: str
    code: str
    customer_id: UUID
    budget: Money
    date_range: DateRange
    status: str = "draft"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    _parts: List[Part] = field(default_factory=list, repr=False)

    def __post_init__(self) -> None:
        """Valida la entidad después de inicialización."""
        self._validate()

    def _validate(self) -> None:
        """
        Valida las reglas de negocio del proyecto.

        Raises:
            ValidationError: Si alguna regla se viola
        """
        if not self.name or len(self.name.strip()) == 0:
            raise ValidationError("El nombre del proyecto no puede estar vacío")

        if len(self.name) > 200:
            raise ValidationError("El nombre no puede exceder 200 caracteres")

        if not self.code or len(self.code.strip()) == 0:
            raise ValidationError("El código del proyecto es obligatorio")

        if self.status not in ["draft", "active", "completed", "cancelled"]:
            raise ValidationError(f"Estado inválido: {self.status}")

        if self.budget.amount < 0:
            raise ValidationError("El presupuesto no puede ser negativo")

    @classmethod
    def create(
        cls,
        name: str,
        code: str,
        customer_id: UUID,
        budget: Money,
        date_range: DateRange,
    ) -> Project:
        """
        Factory method para crear un nuevo proyecto.

        Args:
            name: Nombre del proyecto
            code: Código único
            customer_id: ID del cliente
            budget: Presupuesto inicial
            date_range: Fechas del proyecto

        Returns:
            Nueva instancia de Project validada

        Raises:
            ValidationError: Si los datos son inválidos
        """
        return cls(
            id=uuid4(),
            name=name,
            code=code,
            customer_id=customer_id,
            budget=budget,
            date_range=date_range,
            status="draft",
        )

    def activate(self) -> None:
        """
        Activa el proyecto (transición de draft a active).

        Raises:
            ValidationError: Si el proyecto no está en estado draft
        """
        if self.status != "draft":
            raise ValidationError(
                f"Solo se pueden activar proyectos en borrador. Estado actual: {self.status}"
            )
        self.status = "active"
        self._touch()

    def complete(self) -> None:
        """
        Marca el proyecto como completado.

        Raises:
            ValidationError: Si el proyecto no está activo
        """
        if self.status != "active":
            raise ValidationError("Solo se pueden completar proyectos activos")
        self.status = "completed"
        self._touch()

    def add_part(self, part: Part) -> None:
        """
        Añade una parte al proyecto.

        Args:
            part: Parte a añadir

        Raises:
            ValidationError: Si la parte ya existe o es inválida
        """
        if part in self._parts:
            raise ValidationError("La parte ya existe en el proyecto")
        self._parts.append(part)
        self._touch()

    def calculate_total_cost(self) -> Money:
        """
        Calcula el coste total del proyecto sumando todas las partes.

        Returns:
            Coste total como Money
        """
        total = Money(0, self.budget.currency)
        for part in self._parts:
            total = total + part.cost
        return total

    def _touch(self) -> None:
        """Actualiza el timestamp de modificación."""
        self.updated_at = datetime.now()

    def __eq__(self, other: object) -> bool:
        """Compara proyectos por ID."""
        if not isinstance(other, Project):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash basado en ID para usar en sets/dicts."""
        return hash(self.id)
```

**Test TDD correspondiente (escrito PRIMERO):**

```python
# tests/unit/domain/entities/test_project.py
"""Tests unitarios para la entidad Project."""
import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from src.domain.entities.project import Project
from src.domain.value_objects.money import Money
from src.domain.value_objects.date_range import DateRange
from src.domain.exceptions.validation_error import ValidationError


class TestProjectCreation:
    """Tests para la creación de proyectos."""

    def test_create_valid_project(self):
        """Debe crear un proyecto válido con todos los datos correctos."""
        # Arrange
        name = "Edificio Residencial"
        code = "PROJ-2025-001"
        customer_id = uuid4()
        budget = Money(100000, "EUR")
        date_range = DateRange(
            start=datetime.now(),
            end=datetime.now() + timedelta(days=180)
        )

        # Act
        project = Project.create(
            name=name,
            code=code,
            customer_id=customer_id,
            budget=budget,
            date_range=date_range
        )

        # Assert
        assert project.name == name
        assert project.code == code
        assert project.customer_id == customer_id
        assert project.budget == budget
        assert project.status == "draft"
        assert project.id is not None

    def test_create_project_with_empty_name_raises_error(self):
        """Debe lanzar ValidationError si el nombre está vacío."""
        # Arrange
        budget = Money(100000, "EUR")
        date_range = DateRange(datetime.now(), datetime.now() + timedelta(days=180))

        # Act & Assert
        with pytest.raises(ValidationError, match="nombre.*no puede estar vacío"):
            Project.create(
                name="",
                code="PROJ-001",
                customer_id=uuid4(),
                budget=budget,
                date_range=date_range
            )

    def test_create_project_with_too_long_name_raises_error(self):
        """Debe lanzar ValidationError si el nombre excede 200 caracteres."""
        # Arrange
        long_name = "A" * 201
        budget = Money(100000, "EUR")
        date_range = DateRange(datetime.now(), datetime.now() + timedelta(days=180))

        # Act & Assert
        with pytest.raises(ValidationError, match="no puede exceder 200 caracteres"):
            Project.create(
                name=long_name,
                code="PROJ-001",
                customer_id=uuid4(),
                budget=budget,
                date_range=date_range
            )

    def test_create_project_with_negative_budget_raises_error(self):
        """Debe lanzar ValidationError si el presupuesto es negativo."""
        # Arrange
        negative_budget = Money(-1000, "EUR")
        date_range = DateRange(datetime.now(), datetime.now() + timedelta(days=180))

        # Act & Assert
        with pytest.raises(ValidationError, match="presupuesto no puede ser negativo"):
            Project.create(
                name="Proyecto Test",
                code="PROJ-001",
                customer_id=uuid4(),
                budget=negative_budget,
                date_range=date_range
            )


class TestProjectStateMachine:
    """Tests para las transiciones de estado del proyecto."""

    @pytest.fixture
    def draft_project(self) -> Project:
        """Proyecto en estado draft para testing."""
        return Project.create(
            name="Test Project",
            code="TEST-001",
            customer_id=uuid4(),
            budget=Money(10000, "EUR"),
            date_range=DateRange(datetime.now(), datetime.now() + timedelta(days=30))
        )

    def test_activate_draft_project(self, draft_project):
        """Debe activar un proyecto en draft."""
        # Act
        draft_project.activate()

        # Assert
        assert draft_project.status == "active"

    def test_activate_already_active_project_raises_error(self, draft_project):
        """No debe permitir activar un proyecto ya activo."""
        # Arrange
        draft_project.activate()

        # Act & Assert
        with pytest.raises(ValidationError, match="Solo se pueden activar proyectos en borrador"):
            draft_project.activate()

    def test_complete_active_project(self, draft_project):
        """Debe completar un proyecto activo."""
        # Arrange
        draft_project.activate()

        # Act
        draft_project.complete()

        # Assert
        assert draft_project.status == "completed"

    def test_complete_draft_project_raises_error(self, draft_project):
        """No debe permitir completar un proyecto en draft."""
        # Act & Assert
        with pytest.raises(ValidationError, match="Solo se pueden completar proyectos activos"):
            draft_project.complete()


class TestProjectCostCalculation:
    """Tests para cálculo de costes."""

    # TODO: Implementar tests para calculate_total_cost()
    pass


# ... más tests
```

**DÍA 2-3: Value Objects**

```python
# src/domain/value_objects/money.py
"""Value Object para representar dinero."""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Union

from ..exceptions.validation_error import ValidationError


@dataclass(frozen=True)  # ← Inmutable
class Money:
    """
    Value Object que representa una cantidad de dinero.

    Attributes:
        amount: Cantidad (usa Decimal para precisión)
        currency: Código de moneda ISO 4217 (EUR, USD, etc.)

    Example:
        >>> price = Money(100.50, "EUR")
        >>> tax = Money(21.00, "EUR")
        >>> total = price + tax
        Money(amount=Decimal('121.50'), currency='EUR')
    """

    amount: Decimal
    currency: str

    def __init__(self, amount: Union[int, float, Decimal, str], currency: str):
        """
        Crea un nuevo Money.

        Args:
            amount: Cantidad de dinero
            currency: Código ISO de moneda

        Raises:
            ValidationError: Si la moneda es inválida
        """
        # Usar object.__setattr__ porque dataclass está frozen
        object.__setattr__(self, "amount", Decimal(str(amount)))
        object.__setattr__(self, "currency", currency.upper())
        self._validate()

    def _validate(self) -> None:
        """Valida el value object."""
        valid_currencies = ["EUR", "USD", "GBP"]  # Expandir según necesidad
        if self.currency not in valid_currencies:
            raise ValidationError(f"Moneda inválida: {self.currency}")

    def __add__(self, other: Money) -> Money:
        """
        Suma dos cantidades de dinero.

        Args:
            other: Otra cantidad de dinero

        Returns:
            Nueva instancia con la suma

        Raises:
            ValidationError: Si las monedas no coinciden
        """
        if self.currency != other.currency:
            raise ValidationError(
                f"No se pueden sumar monedas diferentes: {self.currency} y {other.currency}"
            )
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: Money) -> Money:
        """Resta dos cantidades."""
        if self.currency != other.currency:
            raise ValidationError(
                f"No se pueden restar monedas diferentes: {self.currency} y {other.currency}"
            )
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, factor: Union[int, float, Decimal]) -> Money:
        """Multiplica por un factor."""
        return Money(self.amount * Decimal(str(factor)), self.currency)

    def __truediv__(self, divisor: Union[int, float, Decimal]) -> Money:
        """Divide por un divisor."""
        if divisor == 0:
            raise ValidationError("No se puede dividir por cero")
        return Money(self.amount / Decimal(str(divisor)), self.currency)

    def __lt__(self, other: Money) -> bool:
        """Menor que."""
        self._check_same_currency(other)
        return self.amount < other.amount

    def __le__(self, other: Money) -> bool:
        """Menor o igual."""
        self._check_same_currency(other)
        return self.amount <= other.amount

    def __gt__(self, other: Money) -> bool:
        """Mayor que."""
        self._check_same_currency(other)
        return self.amount > other.amount

    def __ge__(self, other: Money) -> bool:
        """Mayor o igual."""
        self._check_same_currency(other)
        return self.amount >= other.amount

    def _check_same_currency(self, other: Money) -> None:
        """Verifica que las monedas sean iguales."""
        if self.currency != other.currency:
            raise ValidationError("No se pueden comparar monedas diferentes")

    def format(self, decimal_places: int = 2) -> str:
        """
        Formatea el dinero como string.

        Args:
            decimal_places: Número de decimales

        Returns:
            String formateado (ej: "100.50 EUR")
        """
        formatted_amount = f"{self.amount:.{decimal_places}f}"
        return f"{formatted_amount} {self.currency}"

    def __str__(self) -> str:
        """String representation."""
        return self.format()

    def __repr__(self) -> str:
        """Repr para debugging."""
        return f"Money(amount=Decimal('{self.amount}'), currency='{self.currency}')"
```

**Continuar con todos los Value Objects:** Address, Email, Phone, DateRange, etc.

**DÍA 4-5: Repository Interfaces (Protocols)**

```python
# src/domain/repositories/project_repository.py
"""Interface del repositorio de proyectos."""
from typing import Protocol, List, Optional
from uuid import UUID

from ..entities.project import Project


class IProjectRepository(Protocol):
    """
    Interface (Protocol) para el repositorio de proyectos.

    Define el contrato que deben cumplir todas las implementaciones
    de persistencia de proyectos (SQLite, PostgreSQL, In-Memory, etc.)
    """

    def save(self, project: Project) -> None:
        """
        Guarda o actualiza un proyecto.

        Args:
            project: Proyecto a guardar

        Raises:
            RepositoryError: Si hay error en la persistencia
        """
        ...

    def get_by_id(self, project_id: UUID) -> Optional[Project]:
        """
        Obtiene un proyecto por su ID.

        Args:
            project_id: ID del proyecto

        Returns:
            Proyecto si existe, None si no

        Raises:
            RepositoryError: Si hay error en la persistencia
        """
        ...

    def get_all(self) -> List[Project]:
        """
        Obtiene todos los proyectos.

        Returns:
            Lista de proyectos (vacía si no hay)

        Raises:
            RepositoryError: Si hay error en la persistencia
        """
        ...

    def delete(self, project_id: UUID) -> bool:
        """
        Elimina un proyecto.

        Args:
            project_id: ID del proyecto a eliminar

        Returns:
            True si se eliminó, False si no existía

        Raises:
            RepositoryError: Si hay error en la persistencia
        """
        ...

    def find_by_code(self, code: str) -> Optional[Project]:
        """
        Busca un proyecto por su código.

        Args:
            code: Código del proyecto

        Returns:
            Proyecto si existe, None si no
        """
        ...

    def find_by_customer(self, customer_id: UUID) -> List[Project]:
        """
        Busca todos los proyectos de un cliente.

        Args:
            customer_id: ID del cliente

        Returns:
            Lista de proyectos del cliente
        """
        ...
```

**DÍA 6: Domain Services**

```python
# src/domain/services/budget_calculator.py
"""Servicio de dominio para cálculos de presupuesto."""
from typing import List
from decimal import Decimal

from ..entities.project import Project
from ..entities.part import Part
from ..value_objects.money import Money


class BudgetCalculator:
    """
    Servicio de dominio que encapsula lógica de cálculo de presupuestos.

    Los servicios de dominio contienen lógica que no pertenece a una
    entidad específica pero es parte de las reglas de negocio.
    """

    def __init__(self, tax_rate: Decimal = Decimal("0.21")):
        """
        Inicializa el calculador.

        Args:
            tax_rate: Tasa de impuesto (default 21% IVA)
        """
        self.tax_rate = tax_rate

    def calculate_subtotal(self, parts: List[Part]) -> Money:
        """
        Calcula el subtotal de las partes.

        Args:
            parts: Lista de partes del proyecto

        Returns:
            Subtotal sin impuestos
        """
        if not parts:
            return Money(0, "EUR")

        total = Money(0, parts[0].unit_price.currency)
        for part in parts:
            total = total + (part.unit_price * part.quantity)

        return total

    def calculate_tax(self, subtotal: Money) -> Money:
        """
        Calcula el impuesto sobre el subtotal.

        Args:
            subtotal: Subtotal sin impuestos

        Returns:
            Cantidad de impuesto
        """
        return subtotal * self.tax_rate

    def calculate_total(self, parts: List[Part]) -> Money:
        """
        Calcula el total incluyendo impuestos.

        Args:
            parts: Lista de partes

        Returns:
            Total con impuestos
        """
        subtotal = self.calculate_subtotal(parts)
        tax = self.calculate_tax(subtotal)
        return subtotal + tax

    def calculate_profit_margin(self, cost: Money, price: Money) -> Decimal:
        """
        Calcula el margen de beneficio.

        Args:
            cost: Coste
            price: Precio de venta

        Returns:
            Margen en porcentaje (ej: 0.25 para 25%)

        Raises:
            ValidationError: Si el precio es 0
        """
        if price.amount == 0:
            raise ValidationError("El precio no puede ser 0")

        margin = (price.amount - cost.amount) / price.amount
        return margin
```

---

### CONTINÚA EN SIGUIENTES FASES...

El documento continúa con **detalle exhaustivo** de:
- **FASE 2: APPLICATION LAYER** (Use Cases, DTOs)
- **FASE 3: INFRASTRUCTURE LAYER** (Repositories, BD, Config)
- **FASE 4: PRESENTATION LAYER** (UI refactorizada)
- **FASE 5: INTEGRATION & TESTING** (E2E, Performance)
- **FASE 6: DOCUMENTATION & DEPLOYMENT**

---

## ESTIMACIÓN DE TIEMPO TOTAL

| Fase | Tiempo Estimado |
|------|----------------|
| Fase 0: Fundaciones | 5-7 días |
| Fase 1: Domain Layer | 4-6 días |
| Fase 2: Application Layer | 3-5 días |
| Fase 3: Infrastructure Layer | 4-6 días |
| Fase 4: Presentation Layer | 6-8 días |
| Fase 5: Integration & Testing | 3-5 días |
| Fase 6: Documentation | 2-3 días |
| **TOTAL** | **27-40 días laborales** |

---

## MÉTRICAS DE ÉXITO (EXCELENCIA)

| Métrica | Objetivo Básico | Objetivo Excelencia |
|---------|----------------|---------------------|
| Test Coverage | >80% | **>95%** |
| Type Coverage | >70% | **100%** |
| Docstring Coverage | >60% | **100%** |
| Cyclomatic Complexity | <10 | **<5** |
| Maintainability Index | >60 | **>85** |
| Code Duplication | <10% | **<3%** |
| Performance | No regresión | **+20% mejora** |
| Lines of Code | <15,000 | **<12,000** |
| Pylint Score | >8.0 | **>9.5** |
| Mypy Errors | 0 | **0** |
| Security Issues (Bandit) | 0 | **0** |

---

## ¿POR QUÉ ESTE ENFOQUE ES MEJOR?

### 1. **Clean Architecture = Futuro-proof**
- Cambiar de CustomTkinter a PyQt: 1-2 días (vs 2 semanas)
- Cambiar de SQLite a PostgreSQL: 1 día (vs 1 semana)
- Añadir API REST: 2-3 días (reutilizando Use Cases)
- Añadir CLI: 1 día (reutilizando Use Cases)

### 2. **TDD = Confianza**
- 0 miedo a refactorizar
- Tests como documentación viva
- Detección temprana de bugs

### 3. **Type Hints = Documentación Ejecutable**
- El IDE autocompleta todo
- Errores detectados ANTES de ejecutar
- Refactorings automáticos seguros

### 4. **Domain-Driven Design = Código que habla el lenguaje del negocio**
- Fácil comunicación con stakeholders
- Lógica de negocio clara y centralizada
- Fácil onboarding de nuevos devs

---

## SIGUIENTE PASO

¿Quieres que empiece con la **Fase 0: Fundaciones**?

Esto incluye:
1. ✅ Crear toda la estructura de carpetas
2. ✅ Configurar herramientas de calidad (mypy, pylint, black, etc.)
3. ✅ Setup de pre-commit hooks
4. ✅ Configurar CI/CD
5. ✅ Event Storming del dominio
6. ✅ Crear ADRs iniciales
7. ✅ Setup de caracterization tests

**Esto NO toca código existente**, así que es **100% seguro**.

¿Comenzamos? 🚀
