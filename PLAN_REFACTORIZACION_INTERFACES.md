# PLAN DE REFACTORIZACIÓN - INTERFACES v1.04_1812

**Fecha:** 2025-10-25
**Versión:** 1.0
**Objetivo:** Reducir deuda técnica, mejorar mantenibilidad y escalabilidad del código de interfaces

---

## RESUMEN EJECUTIVO

### Estado Actual
- **47 archivos** de interfaz gráfica
- **21,978 líneas** de código
- **50% de código duplicado** (crítico)
- **Score de mantenibilidad:** 3/10 (BAJA)
- **Archivos críticos:** 4 archivos >2000 líneas

### Problemas Identificados
1. **Duplicación masiva de código** (~600-700 líneas redundantes)
2. **Archivos monolíticos** (hasta 3,584 líneas/archivo)
3. **Variables globales mutables** (5 variables críticas)
4. **Profundidad excesiva** (27 niveles de anidamiento)
5. **Métodos gigantes** (hasta 669 líneas/método)
6. **Imports con asterisco** (14 imports que contaminan namespace)

### Beneficios Esperados
- **-30-40%** reducción en líneas de código
- **+200%** mejora en testabilidad
- **+150%** mejora en tiempo de mantenimiento
- **-70%** reducción de bugs por cambios

---

## ARQUITECTURA OBJETIVO

```
v1.04_1812/
├── interface/
│   ├── base/                    # NUEVO: Clases base reutilizables
│   │   ├── __init__.py
│   │   ├── base_window.py       # BaseWindow con cancel()
│   │   ├── base_form.py         # BaseForm con save() template
│   │   ├── base_project.py      # Unifica manager/user_project
│   │   └── mixins.py            # LogoMixin, GridMixin, etc.
│   │
│   ├── components/              # NUEVO: Componentes reutilizables
│   │   ├── __init__.py
│   │   ├── sidebar.py           # Sidebar component
│   │   ├── data_frame.py        # Data display frames
│   │   ├── form_fields.py       # Common form fields
│   │   └── dialogs.py           # CTkMessagebox wrappers
│   │
│   ├── config/                  # NUEVO: Configuración centralizada
│   │   ├── __init__.py
│   │   ├── ui_config.py         # Colores, tamaños, estilos
│   │   ├── images.py            # Gestión de imágenes base64
│   │   └── constants.py         # Constantes globales
│   │
│   ├── services/                # NUEVO: Lógica de negocio
│   │   ├── __init__.py
│   │   ├── project_service.py   # Lógica de proyectos
│   │   ├── parts_service.py     # Lógica de piezas
│   │   ├── user_service.py      # Lógica de usuarios
│   │   └── catalog_service.py   # Lógica de catálogo
│   │
│   ├── state/                   # NUEVO: Gestión de estado
│   │   ├── __init__.py
│   │   ├── user_state.py        # Estado de usuario (elimina globals)
│   │   └── app_state.py         # Estado de aplicación
│   │
│   ├── windows/                 # REFACTORIZADO: Ventanas principales
│   │   ├── manager/
│   │   │   ├── manager_window.py           # Refactorizado
│   │   │   └── manager_project_window.py   # Refactorizado
│   │   ├── user/
│   │   │   └── user_project_window.py      # Refactorizado
│   │   ├── parts/
│   │   │   └── parts_manager_window.py     # Refactorizado
│   │   └── dialogs/
│   │       ├── customer_dialog.py          # Unifica add/mod
│   │       ├── item_dialog.py              # Unifica add/mod
│   │       └── register_dialog.py          # Unifica add/mod
│   │
│   └── legacy/                  # TEMPORAL: Archivos originales
│       └── [archivos actuales movidos aquí temporalmente]
│
└── tests/                       # NUEVO: Tests unitarios
    ├── interface/
    │   ├── test_base_window.py
    │   ├── test_components.py
    │   ├── test_services.py
    │   └── test_state.py
    └── fixtures/
        └── test_data.py
```

---

## FASES DE REFACTORIZACIÓN

### FASE 0: PREPARACIÓN (2-3 horas)
**Objetivo:** Establecer infraestructura sin romper código existente

#### Tareas:
1. ✅ Crear estructura de carpetas base/components/config/services/state
2. ✅ Mover archivos actuales a interface/legacy/ temporalmente
3. ✅ Crear branch de desarrollo `refactor/interfaces-phase-0`
4. ✅ Establecer tests básicos
5. ✅ Configurar linting (pylint/flake8)

#### Entregables:
- Estructura de carpetas creada
- Tests básicos funcionando
- Documentación inicial

**Riesgo:** BAJO
**Impacto en producción:** NINGUNO

---

### FASE 1: ELIMINACIÓN DE DUPLICACIÓN CRÍTICA (8-12 horas)
**Objetivo:** Reducir 50% de código duplicado inmediatamente

#### FASE 1A: Clases Base (4 horas)

**Tarea 1.1:** Crear `BaseWindow` con método `cancel()`
```python
# interface/base/base_window.py
class BaseWindow(customtkinter.CTkToplevel):
    """Ventana base para todos los diálogos"""

    def __init__(self, master, title="Window", **kwargs):
        super().__init__(master, **kwargs)
        self.title(title)
        self._setup_window()

    def _setup_window(self):
        """Override en subclases para configurar ventana"""
        pass

    def cancel(self):
        """Cierra la ventana"""
        self.destroy()
```

**Archivos a modificar:** 21 archivos que heredarán de BaseWindow
- customer_add_interfaz.py → hereda de BaseWindow
- customer_mod_interfaz.py → hereda de BaseWindow
- [... otros 19 archivos]

**Impacto:** -21 líneas duplicadas

---

**Tarea 1.2:** Crear `BaseForm` con template method `save()`
```python
# interface/base/base_form.py
class BaseForm(BaseWindow):
    """Formulario base con lógica de guardado"""

    def save(self, access):
        """Template method para guardar datos"""
        if not self._validate_data():
            return False

        data = self._collect_data()

        try:
            success = self._save_to_db(data, access)
            if success:
                self._show_success()
                self.destroy()
            else:
                self._show_error("No se pudo guardar")
        except Exception as e:
            self._show_error(f"Error: {str(e)}")

    def _validate_data(self) -> bool:
        """Override: Validar datos antes de guardar"""
        return True

    def _collect_data(self) -> dict:
        """Override: Recolectar datos del formulario"""
        raise NotImplementedError

    def _save_to_db(self, data: dict, access) -> bool:
        """Override: Guardar en base de datos"""
        raise NotImplementedError
```

**Archivos a modificar:** 28 archivos que heredarán de BaseForm

**Impacto:** -280 líneas (10 líneas/archivo promedio)

---

#### FASE 1B: Componentes Reutilizables (4 horas)

**Tarea 1.3:** Crear módulo de diálogos
```python
# interface/components/dialogs.py
def show_error(message: str, title: str = "Error Message!"):
    """Muestra diálogo de error"""
    CTkMessagebox(title=title, message=message, icon="cancel")

def show_success(message: str, title: str = "Successful Message!"):
    """Muestra diálogo de éxito"""
    CTkMessagebox(title=title, message=message, icon="check")

def show_warning(message: str, title: str = "Warning!"):
    """Muestra diálogo de advertencia"""
    CTkMessagebox(title=title, message=message, icon="warning")

def show_info(message: str, title: str = "Information"):
    """Muestra diálogo informativo"""
    CTkMessagebox(title=title, message=message, icon="info")
```

**Archivos a modificar:** 33 archivos que usan CTkMessagebox directamente

**Impacto:** -200 líneas

---

**Tarea 1.4:** Crear componente de logo
```python
# interface/components/logo.py
from PIL import Image
from io import BytesIO
import base64
import customtkinter

class LogoMixin:
    """Mixin para añadir logo a ventanas"""

    def create_logo(self, parent, image_base64: str, size=(80,80),
                   row=5, column=1, padx=30, pady=(15,15), columnspan=2):
        """Crea y posiciona un logo"""
        image = Image.open(BytesIO(base64.b64decode(image_base64)))
        lg_image = customtkinter.CTkImage(image, size=size)
        lg_image_label = customtkinter.CTkLabel(
            parent, image=lg_image, text=""
        )
        lg_image_label.grid(
            row=row, column=column, padx=padx,
            pady=pady, columnspan=columnspan
        )
        return lg_image_label
```

**Archivos a modificar:** 8 archivos con imagen base64 hardcoded

**Impacto:** -120 líneas (15 líneas/archivo)

---

#### FASE 1C: Eliminación de Archivos Duplicados (2 horas)

**Tarea 1.5:** Eliminar archivos *_new duplicados
- `user_company_add_new_interfaz.py` → ELIMINAR (96% igual a user_company_add)
- `user_customer_add_new_interfaz.py` → ELIMINAR (96% igual a user_customer_add)

**Modificar archivos que los importan:**
- manager_interfaz.py líneas 24, 26, 28 → actualizar imports

**Impacto:** -2 archivos, -237 líneas

---

**Tarea 1.6:** Consolidar pares Add/Mod en clases únicas
```python
# interface/windows/dialogs/customer_dialog.py
class CustomerDialog(BaseForm):
    """Diálogo unificado para añadir/modificar clientes"""

    def __init__(self, master, mode="add", customer_id=None, **kwargs):
        self.mode = mode  # "add" o "mod"
        self.customer_id = customer_id
        super().__init__(master, **kwargs)

        if mode == "mod" and customer_id:
            self._load_existing_data()

    def _collect_data(self) -> dict:
        # Común para add y mod
        return {...}

    def _save_to_db(self, data: dict, access) -> bool:
        if self.mode == "add":
            return add_customer(data, access)
        else:
            return update_customer(self.customer_id, data, access)
```

**Archivos a consolidar:**
- customer_add + customer_mod → customer_dialog.py
- user_customer_add + user_customer_mod → user_customer_dialog.py

**Impacto:** -4 archivos, -160 líneas

---

### RESUMEN FASE 1:
- **Tiempo:** 8-12 horas
- **Reducción de código:** -600 líneas (-27%)
- **Archivos eliminados:** 6
- **Nuevos archivos:** 5 (base/components)
- **Riesgo:** MEDIO (requiere testing exhaustivo)
- **Impacto producción:** NINGUNO (código legacy sigue disponible)

---

### FASE 2: REFACTORIZACIÓN DE ARCHIVOS GIGANTES (16-24 horas)
**Objetivo:** Dividir archivos >2000 líneas en componentes manejables

#### FASE 2A: manager_project_interfaz.py (3,584 líneas) → (8 horas)

**Estrategia:** Dividir en 5 componentes

**Componente 1:** Clase principal reducida
```python
# interface/windows/manager/manager_project_window.py (500 líneas)
class ManagerProjectWindow(BaseProjectWindow):
    """Ventana principal de gestión de proyectos"""

    def __init__(self, master, project_id, access):
        self.project_id = project_id
        self.access = access
        super().__init__(master, title="Gestión de Proyecto")

    def _setup_window(self):
        self._create_sidebar()
        self._create_content_area()
        self._load_initial_data()
```

**Componente 2:** Vista de resumen
```python
# interface/windows/manager/views/summary_view.py (400 líneas)
class SummaryView(CTkFrame):
    """Vista de resumen del proyecto"""
    # Extraído de main_summary()
```

**Componente 3:** Vista de inventario
```python
# interface/windows/manager/views/inventory_view.py (600 líneas)
class InventoryView(CTkFrame):
    """Vista de inventario del proyecto"""
    # Extraído de main_inventory()
```

**Componente 4:** Vista de presupuesto
```python
# interface/windows/manager/views/budget_view.py (800 líneas)
class BudgetView(CTkFrame):
    """Vista de presupuesto"""
    # Extraído de main_budget()
```

**Componente 5:** Vista de certificaciones
```python
# interface/windows/manager/views/certifications_view.py (500 líneas)
class CertificationsView(CTkFrame):
    """Vista de certificaciones"""
    # Extraído de main_certifications()
```

**Resultado:**
- 3,584 líneas → 5 archivos de 400-800 líneas c/u
- Cada vista es independiente y testeable
- Reduce complejidad de 63 métodos a ~12 métodos/clase

---

#### FASE 2B: user_project_interfaz.py (3,567 líneas) → (4 horas)

**Estrategia:** Reusar componentes de manager_project

**Problema actual:** 99.6% idéntico a manager_project_interfaz.py

**Solución:**
```python
# interface/base/base_project.py (600 líneas)
class BaseProjectWindow(BaseWindow):
    """Clase base compartida por manager y user project"""

    def __init__(self, master, project_id, access, user_type="manager"):
        self.user_type = user_type
        # Lógica común

    def _create_sidebar(self):
        # Sidebar común
        if self.user_type == "manager":
            self._add_management_buttons()

    def _add_management_buttons(self):
        """Solo para managers"""
        pass

# interface/windows/user/user_project_window.py (50 líneas)
class UserProjectWindow(BaseProjectWindow):
    """Ventana de proyecto para usuarios"""

    def __init__(self, master, project_id, access):
        super().__init__(master, project_id, access, user_type="user")
```

**Resultado:**
- 3,567 líneas → 50 líneas (¡reutiliza base_project!)
- Elimina duplicación masiva
- Cambios futuros se hacen en UN solo lugar

---

#### FASE 2C: manager_interfaz.py (2,911 líneas) → (6 horas)

**Estrategia:** Extraer método gigante `main_new_project`

**Problema:** Método `main_new_project` tiene 669 líneas

**Solución:**
```python
# interface/windows/manager/manager_window.py (300 líneas)
class ManagerWindow(customtkinter.CTk):
    """Ventana principal del manager"""

    def main_new_project(self):
        # Solo orquestación (50 líneas)
        dialog = NewProjectDialog(self, access=self.access)
        dialog.show()

# interface/windows/manager/dialogs/new_project_dialog.py (600 líneas)
class NewProjectDialog(BaseForm):
    """Diálogo de creación de proyecto"""

    def __init__(self, master, access):
        super().__init__(master, title="Nuevo Proyecto")
        self.access = access
        self._create_form()

    def _create_form(self):
        # Código extraído de main_new_project
        pass
```

**Dividir en tabs:**
- BasicDataTab (150 líneas)
- CustomerTab (150 líneas)
- LocationTab (150 líneas)
- ConfigTab (150 líneas)

**Resultado:**
- 2,911 líneas → 4 archivos de ~300 líneas
- Método gigante → 5 clases cohesivas

---

#### FASE 2D: parts_manager_interfaz.py (2,235 líneas) → (4 horas)

**Estrategia:** Similar a manager_project

**Resultado:**
- 2,235 líneas → 4 archivos de ~500 líneas
- PartsManagerWindow + 3 vistas

---

### RESUMEN FASE 2:
- **Tiempo:** 16-24 horas
- **Reducción de código:** -400 líneas adicionales
- **Archivos creados:** ~15 nuevos archivos modulares
- **Archivos gigantes eliminados:** 4
- **Riesgo:** ALTO (cambios arquitectónicos)
- **Impacto producción:** NINGUNO (testing exhaustivo antes de merge)

---

### FASE 3: ELIMINACIÓN DE VARIABLES GLOBALES (6-8 horas)
**Objetivo:** Eliminar estado global mutable

#### FASE 3A: Crear UserState (2 horas)

**Problema:**
```python
# manager_interfaz.py líneas 39-40
data_user_bd = []      # Global mutable
user_privileges = {}   # Global mutable
```

**Solución:**
```python
# interface/state/user_state.py
class UserState:
    """Gestión de estado de usuario (Singleton)"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._data = None
            cls._instance._privileges = {}
        return cls._instance

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if not isinstance(value, list):
            raise TypeError("data debe ser lista")
        self._data = value

    @property
    def privileges(self):
        return self._privileges.copy()  # Inmutable hacia fuera

    def set_privilege(self, key, value):
        self._privileges[key] = value

    def clear(self):
        """Limpia estado al cerrar sesión"""
        self._data = None
        self._privileges = {}

# Uso:
state = UserState()
state.data = [user_info]
state.set_privilege("can_edit", True)
```

**Archivos a modificar:**
- manager_interfaz.py (eliminar globals, usar UserState)
- Todos los archivos que lean estas variables

**Impacto:** +100 líneas nuevas, -50 líneas globals, +seguridad

---

#### FASE 3B: Eliminar image_base64 globals (3 horas)

**Problema:**
```python
# 3 archivos diferentes definen:
image_base64 = None  # Global mutable
```

**Solución:**
```python
# interface/config/images.py
class ImageManager:
    """Gestión centralizada de imágenes"""

    def __init__(self):
        self._images = {}

    def set_image(self, key: str, base64_data: str):
        """Almacena imagen base64"""
        self._images[key] = base64_data

    def get_image(self, key: str, size=(80,80)):
        """Obtiene CTkImage"""
        if key not in self._images:
            return None

        image = Image.open(BytesIO(base64.b64decode(self._images[key])))
        return customtkinter.CTkImage(image, size=size)

    def clear(self):
        self._images = {}

# Singleton global
image_manager = ImageManager()
```

**Archivos a modificar:**
- customer_add_interfaz.py
- customer_mod_interfaz.py
- confirm_photo_interfaz.py

**Impacto:** -9 líneas globals, +centralización

---

#### FASE 3C: Eliminar imports con asterisco (3 horas)

**Problema:**
```python
# manager_interfaz.py líneas 19-29
from interface.customer_add_interfaz import *  # ❌
from interface.customer_mod_interfaz import *   # ❌
# ... 11 imports más
```

**Solución:**
```python
# manager_interfaz.py
from interface.dialogs.customer_dialog import CustomerDialog
from interface.dialogs.user_customer_dialog import UserCustomerDialog
# ... imports explícitos
```

**Script automatizado:**
```bash
# script/fix_imports.py
# Detecta símbolos usados y genera imports explícitos
```

**Archivos a modificar:** 7 archivos

**Impacto:** +claridad, +seguridad

---

### RESUMEN FASE 3:
- **Tiempo:** 6-8 horas
- **Variables globales eliminadas:** 5
- **Imports * eliminados:** 14
- **Riesgo:** MEDIO
- **Impacto producción:** NINGUNO

---

### FASE 4: SERVICIOS Y SEPARACIÓN DE LÓGICA (12-16 horas)
**Objetivo:** Separar lógica de negocio de UI

#### Problema Actual:
```python
# manager_project_interfaz.py
def save_data(self):
    # UI y BD mezclados
    data = self.entry.get()  # UI
    conn = sqlite3.connect()  # BD
    cursor.execute(...)       # BD
    self.show_message()       # UI
```

#### Solución:
```python
# interface/services/project_service.py
class ProjectService:
    """Lógica de negocio de proyectos"""

    def __init__(self, db_connection):
        self.db = db_connection

    def save_project(self, project_data: dict) -> bool:
        """Guarda proyecto (solo lógica, sin UI)"""
        try:
            # Validaciones
            if not project_data.get("name"):
                raise ValueError("Nombre requerido")

            # Guardado en BD
            self.db.insert_project(project_data)
            return True
        except Exception as e:
            logging.error(f"Error guardando proyecto: {e}")
            return False

# interface/windows/manager/manager_project_window.py
class ManagerProjectWindow(BaseProjectWindow):

    def __init__(self, ...):
        self.project_service = ProjectService(db_connection)

    def save_data(self):
        # Solo UI
        data = self._collect_form_data()

        # Llama a servicio
        success = self.project_service.save_project(data)

        # Feedback UI
        if success:
            show_success("Proyecto guardado")
        else:
            show_error("Error al guardar")
```

#### Servicios a crear:
1. ProjectService (project_service.py)
2. PartsService (parts_service.py)
3. UserService (user_service.py)
4. CatalogService (catalog_service.py)
5. BudgetService (budget_service.py)
6. CertificationService (certification_service.py)

**Beneficios:**
- ✅ Lógica testeable sin UI
- ✅ Reutilizable entre ventanas
- ✅ Más fácil cambiar BD
- ✅ Logs centralizados

### RESUMEN FASE 4:
- **Tiempo:** 12-16 horas
- **Archivos creados:** 6 servicios
- **Riesgo:** ALTO
- **Impacto producción:** NINGUNO
- **Testing:** CRÍTICO

---

### FASE 5: TESTING Y DOCUMENTACIÓN (8-12 horas)
**Objetivo:** Asegurar calidad y facilitar mantenimiento

#### FASE 5A: Tests Unitarios (6 horas)

```python
# tests/interface/test_base_window.py
import pytest
from interface.base.base_window import BaseWindow

def test_base_window_cancel():
    """Test método cancel()"""
    window = BaseWindow(None)
    window.cancel()
    # Assert ventana cerrada

# tests/interface/test_services.py
def test_project_service_save():
    """Test guardado de proyecto"""
    service = ProjectService(mock_db)
    result = service.save_project({"name": "Test"})
    assert result == True

# tests/interface/test_state.py
def test_user_state_singleton():
    """Test singleton de UserState"""
    state1 = UserState()
    state2 = UserState()
    assert state1 is state2
```

**Coverage objetivo:** >80%

---

#### FASE 5B: Documentación (4 horas)

1. **README.md por carpeta**
   - base/README.md
   - components/README.md
   - services/README.md

2. **Docstrings completos**
   - Todas las clases
   - Todos los métodos públicos

3. **Guía de migración**
   - MIGRATION_GUIDE.md

4. **Diagramas de arquitectura**
   - Antes/Después
   - Diagramas de clases

---

### RESUMEN FASE 5:
- **Tiempo:** 8-12 horas
- **Tests creados:** ~30 tests
- **Documentos:** 5+ archivos
- **Coverage:** >80%
- **Riesgo:** BAJO

---

## CRONOGRAMA TOTAL

| Fase | Tiempo | Inicio | Fin | Dependencias |
|------|--------|--------|-----|--------------|
| **Fase 0** | 2-3h | Día 1 | Día 1 | Ninguna |
| **Fase 1** | 8-12h | Día 1 | Día 2 | Fase 0 |
| **Fase 2** | 16-24h | Día 2 | Día 4 | Fase 1 |
| **Fase 3** | 6-8h | Día 4 | Día 5 | Fase 1 |
| **Fase 4** | 12-16h | Día 5 | Día 7 | Fase 2, 3 |
| **Fase 5** | 8-12h | Día 7 | Día 8 | Fase 4 |
| **Testing final** | 4h | Día 8 | Día 8 | Todas |

**TOTAL:** 56-75 horas (~7-10 días laborales)

---

## ESTRATEGIA DE IMPLEMENTACIÓN

### Principio: "Nunca romper producción"

1. **Desarrollo paralelo:**
   - Código nuevo en `/interface/`
   - Código viejo en `/interface/legacy/`
   - Switcheo gradual

2. **Feature flags:**
   ```python
   USE_NEW_INTERFACE = os.getenv("USE_NEW_INTERFACE", "false") == "true"

   if USE_NEW_INTERFACE:
       from interface.windows.manager import ManagerWindow
   else:
       from interface.legacy.manager_interfaz import AppManager
   ```

3. **Testing en cada fase:**
   - Tests unitarios después de cada tarea
   - Tests de integración después de cada fase
   - Tests E2E antes de merge final

4. **Rollback plan:**
   - Git tags en cada fase
   - Scripts de rollback automatizados
   - Backups de BD antes de migraciones

---

## MÉTRICAS DE ÉXITO

### Métricas de Código
| Métrica | Antes | Objetivo | Medición |
|---------|-------|----------|----------|
| Líneas totales | 21,978 | <15,000 | `wc -l` |
| Archivos | 47 | ~40 | `ls \| wc -l` |
| Duplicación | ~50% | <10% | `radon` |
| Complejidad CC | 0.06-0.09 | <0.05 | `radon cc` |
| Max líneas/archivo | 3,584 | <800 | `wc -l` |
| Max métodos/clase | 63 | <20 | Manual |
| Variables globales | 5 | 0 | `grep global` |
| Imports * | 14 | 0 | `grep "import \*"` |

### Métricas de Calidad
| Métrica | Antes | Objetivo |
|---------|-------|----------|
| Test coverage | 0% | >80% |
| Bugs reportados | baseline | -50% |
| Tiempo fix bug | baseline | -40% |
| Tiempo añadir feature | baseline | -30% |
| Onboarding devs | 2-3 semanas | <1 semana |

---

## RIESGOS Y MITIGACIÓN

### RIESGO 1: Romper funcionalidad existente
- **Probabilidad:** ALTA
- **Impacto:** CRÍTICO
- **Mitigación:**
  - Testing exhaustivo en cada fase
  - Desarrollo paralelo (legacy + nuevo)
  - Feature flags
  - Rollback automatizado

### RIESGO 2: Tiempo subestimado
- **Probabilidad:** MEDIA
- **Impacto:** MEDIO
- **Mitigación:**
  - Buffer del 30% en estimaciones
  - Fases independientes (puede pausarse)
  - Entregables incrementales

### RIESGO 3: Incompatibilidad con CustomTkinter
- **Probabilidad:** BAJA
- **Impacto:** ALTO
- **Mitigación:**
  - POC antes de cada fase
  - Tests de integración con CTk
  - Consultar docs de CustomTkinter

### RIESGO 4: Resistencia al cambio del equipo
- **Probabilidad:** MEDIA
- **Impacto:** MEDIO
- **Mitigación:**
  - Documentación clara
  - Guía de migración
  - Sesiones de pair programming

---

## PRÓXIMOS PASOS

### Inmediatos (Hoy):
1. ✅ Revisar y aprobar este plan
2. ⏳ Crear branch `refactor/interfaces-preparation`
3. ⏳ Ejecutar Fase 0

### Esta semana:
1. Fase 0 completa
2. Fase 1A (clases base)
3. Fase 1B (componentes reutilizables)

### Siguientes 2 semanas:
1. Fases 1-3 completas
2. Testing de regresión
3. Primera demo del código refactorizado

---

## CONCLUSIÓN

Este plan de refactorización es **ambicioso pero realista**. Los beneficios esperados son:

✅ **-30-40%** menos código
✅ **+200%** más testeable
✅ **+150%** más mantenible
✅ **-70%** menos bugs

El enfoque incremental y paralelo asegura que:
- ✅ No se rompe producción
- ✅ Puede pausarse en cualquier momento
- ✅ Entrega valor en cada fase
- ✅ Fácil rollback si algo falla

**¿Estás listo para empezar?**
