# ADR 0002: Usar Test-Driven Development (TDD)

**Fecha:** 2025-10-25
**Estado:** Aceptado
**Autores:** Claude Code, SieuPepe

---

## Contexto

El código actual **no tiene tests automatizados**, lo que resulta en:

1. **Miedo a refactorizar:** No hay forma de saber si rompiste algo
2. **Bugs en producción:** Errores no detectados hasta que usuarios reportan
3. **Refactorización arriesgada:** Cada cambio puede romper funcionalidad
4. **Regresiones frecuentes:** Arreglar bug A puede romper feature B

Con Clean Architecture, es **crítico** tener tests porque:
- La arquitectura tiene muchas capas
- Los componentes están desacoplados
- Las interfaces (Protocols) deben estar bien testeadas

---

## Decisión

Adoptaremos **Test-Driven Development (TDD)** estricto:

### Ciclo TDD (Red-Green-Refactor)

```
1. RED    → Escribir test que falla
2. GREEN  → Escribir código mínimo para que pase
3. REFACTOR → Mejorar código manteniendo tests verdes
4. REPEAT
```

### Reglas TDD

1. **No escribir código de producción sin test que falle primero**
2. **No escribir más test del necesario para fallar**
3. **No escribir más código del necesario para pasar el test**

### Tipos de Tests

#### 1. Unit Tests (95% de los tests)
```python
# tests/unit/domain/entities/test_project.py
def test_create_project_with_valid_data():
    # Arrange
    project = Project.create(name="Test", budget=Money(10000, "EUR"))

    # Act & Assert
    assert project.name == "Test"
    assert project.budget.amount == 10000
```

**Características:**
- Ultra-rápidos (<0.001s cada uno)
- Sin dependencias externas
- Prueban una unidad aislada

#### 2. Integration Tests (4% de los tests)
```python
# tests/integration/test_project_repository.py
def test_save_and_retrieve_project(sqlite_db):
    # Arrange
    repo = SQLiteProjectRepository(sqlite_db)
    project = Project.create(name="Test", ...)

    # Act
    repo.save(project)
    retrieved = repo.get_by_id(project.id)

    # Assert
    assert retrieved.name == project.name
```

**Características:**
- Prueban integración entre componentes
- Usan BD/archivos reales (en memoria)
- Más lentos (10-100ms)

#### 3. UI Tests (0.5% de los tests)
```python
# tests/ui/test_project_window.py
def test_project_window_displays_data(mock_use_case):
    # Arrange
    window = ProjectWindow(mock_use_case)

    # Act
    window.load_project(project_id)

    # Assert
    assert window.name_label.text == "Expected Name"
```

**Características:**
- Prueban UI sin lógica
- Usan mocks para use cases
- Lentos (100-500ms)

#### 4. E2E Tests (0.5% de los tests)
```python
# tests/e2e/test_project_workflow.py
def test_complete_project_creation_workflow(app):
    # Arrange
    app.login("manager", "password")

    # Act
    app.click("new_project")
    app.fill_form({"name": "Test", "budget": 10000})
    app.click("save")

    # Assert
    assert app.message == "Proyecto guardado"
    assert app.project_exists("Test")
```

**Características:**
- Prueban flujo completo
- Más lentos (1-5s)
- Menos cantidad

---

## Objetivos de Coverage

### Mínimo Aceptable
- **Unit tests:** >80% coverage
- **Integration tests:** >60% coverage
- **Overall:** >80% coverage

### Objetivo de Excelencia
- **Unit tests:** >95% coverage
- **Integration tests:** >80% coverage
- **Overall:** >90% coverage

### Capas por Coverage Target

| Capa | Unit Coverage | Integration Coverage |
|------|---------------|---------------------|
| Domain | **>95%** | N/A |
| Application | **>90%** | >70% |
| Infrastructure | >70% | **>85%** |
| Presentation | >60% | >50% |

---

## Consecuencias

### Positivas

1. **Confianza Total**
   - Refactorizar sin miedo
   - Tests garantizan que funciona

2. **Documentación Viva**
   - Tests muestran cómo usar el código
   - Ejemplos ejecutables

3. **Diseño Mejor**
   - TDD fuerza código testeable
   - Código testeable = código desacoplado

4. **Detección Temprana**
   - Bugs encontrados en segundos
   - No llegan a producción

5. **Regresiones Imposibles**
   - Tests previenen que bugs vuelvan
   - CI/CD valida cada commit

### Negativas

1. **Tiempo Inicial**
   - Escribir tests toma tiempo
   - ~30-40% más tiempo inicialmente

2. **Disciplina Requerida**
   - Fácil saltarse TDD bajo presión
   - Requiere compromiso del equipo

3. **Mantenimiento de Tests**
   - Tests también necesitan mantenimiento
   - Pueden volverse frágiles

---

## Herramientas

### Framework: pytest
```bash
# Ejecutar todos los tests
pytest

# Solo unit tests
pytest tests/unit -m unit

# Con coverage
pytest --cov=src --cov-report=html

# Rápido (solo tests que fallaron)
pytest --lf
```

### Plugins pytest
- `pytest-cov`: Coverage
- `pytest-mock`: Mocking
- `pytest-xdist`: Tests en paralelo
- `pytest-watch`: Auto-rerun

### Mocking
- `unittest.mock`: Mocks estándar
- `pytest-mock`: Wrapper de mock
- Repositorios in-memory para tests

---

## Ejemplo Completo TDD

### 1. RED - Test que falla

```python
# tests/unit/domain/entities/test_project.py
def test_project_cannot_have_negative_budget():
    """Should raise ValidationError for negative budget."""
    with pytest.raises(ValidationError, match="presupuesto no puede ser negativo"):
        Project.create(
            name="Test",
            budget=Money(-1000, "EUR"),  # ❌ Negativo
        )
```

**Resultado:** ❌ Test FALLA (Project aún no valida)

### 2. GREEN - Código mínimo

```python
# src/domain/entities/project.py
@dataclass
class Project:
    budget: Money

    def __post_init__(self):
        if self.budget.amount < 0:
            raise ValidationError("El presupuesto no puede ser negativo")
```

**Resultado:** ✅ Test PASA

### 3. REFACTOR - Mejorar

```python
# src/domain/entities/project.py
@dataclass
class Project:
    budget: Money

    def __post_init__(self):
        self._validate()

    def _validate(self) -> None:
        """Valida las reglas de negocio."""
        if self.budget.amount < 0:
            raise ValidationError("El presupuesto no puede ser negativo")
        # Más validaciones aquí...
```

**Resultado:** ✅ Tests PASAN, código más limpio

### 4. REPEAT

Añadir más tests:
- test_project_name_cannot_be_empty()
- test_project_name_max_length_200()
- test_project_code_is_required()
- ...

---

## Estrategia de Implementación

### Fase 1: Domain Layer
- **100% TDD:** Escribir test PRIMERO, siempre
- **Coverage objetivo:** >95%
- **Sin excepciones:** Todo método testeado

### Fase 2: Application Layer
- **TDD estricto:** Tests antes de código
- **Coverage objetivo:** >90%
- **Mocks:** Para repositorios

### Fase 3: Infrastructure Layer
- **TDD + Integration tests**
- **Coverage objetivo:** >85%
- **BD en memoria:** Para tests rápidos

### Fase 4: Presentation Layer
- **Tests de UI:** Con mocks de use cases
- **Coverage objetivo:** >70%
- **No tests de CustomTkinter:** Solo nuestra lógica

---

## Métricas

Tracking en CI/CD:

```yaml
# .github/workflows/ci.yml
- name: Run tests with coverage
  run: pytest --cov=src --cov-fail-under=80

- name: Upload coverage report
  uses: codecov/codecov-action@v4
```

Dashboard de coverage: https://codecov.io

---

## Excepciones

**NO se requiere test para:**
- `__init__.py` vacíos
- Código legacy (v1.04_1812/interface/legacy/)
- Scripts de migración one-time
- Configuración trivial (constants)

**Sí se requiere test para:**
- TODO lo demás, sin excepción

---

## Recursos

- [Test Driven Development (Kent Beck)](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)
- [Pytest Documentation](https://docs.pytest.org/)
- [Clean Architecture + TDD](https://herbertograca.com/2017/11/16/explicit-architecture-01-ddd-hexagonal-onion-clean-cqrs-how-i-put-it-all-together/)

---

## Decisión Final

**APROBADO** - TDD estricto en todas las fases
**Fecha de decisión:** 2025-10-25
**Revisión:** Continua (cada sprint)
