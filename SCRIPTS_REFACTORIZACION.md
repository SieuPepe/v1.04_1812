# SCRIPTS Y COMANDOS ÚTILES - REFACTORIZACIÓN

Este documento contiene comandos bash y scripts útiles para ejecutar durante la refactorización.

---

## ANÁLISIS DE CÓDIGO

### 1. Contar líneas por archivo
```bash
# Todos los archivos de interfaz
find v1.04_1812/interface -name "*.py" -exec wc -l {} \; | sort -rn

# Top 10 archivos más grandes
find v1.04_1812/interface -name "*.py" -exec wc -l {} \; | sort -rn | head -10

# Total de líneas
find v1.04_1812/interface -name "*.py" -exec wc -l {} \; | awk '{sum+=$1} END {print sum}'
```

### 2. Buscar código duplicado
```bash
# Método específico repetido
grep -rn "def cancel" v1.04_1812/interface/ | wc -l

# Comparar dos archivos
diff -u v1.04_1812/interface/manager_project_interfaz.py \
        v1.04_1812/interface/user_project_interfaz.py | wc -l

# Ver diferencias visuales
diff -y v1.04_1812/interface/user_company_add_interfaz.py \
        v1.04_1812/interface/user_company_add_new_interfaz.py | less
```

### 3. Encontrar variables globales
```bash
# Keyword 'global'
grep -rn "global " v1.04_1812/interface/

# Variables a nivel de módulo (no indentadas)
grep -rn "^[a-z_][a-z0-9_]* = " v1.04_1812/interface/

# Imports con asterisco
grep -rn "from .* import \*" v1.04_1812/interface/
```

### 4. Complejidad ciclomática
```bash
# Instalar radon si no está
pip install radon

# Análisis de complejidad
radon cc v1.04_1812/interface/ -s -a

# Solo archivos complejos (CC > 10)
radon cc v1.04_1812/interface/ -s -n B

# Métodos muy complejos (CC > 20)
radon cc v1.04_1812/interface/ -s -n A
```

### 5. Métricas de mantenibilidad
```bash
# Índice de mantenibilidad (0-100, >20 es bueno)
radon mi v1.04_1812/interface/ -s

# Ranking de peores archivos
radon mi v1.04_1812/interface/ -s -n B
```

### 6. Halstead metrics (volumen, dificultad, esfuerzo)
```bash
radon hal v1.04_1812/interface/ -f
```

---

## PREPARACIÓN FASE 0

### 1. Crear estructura de carpetas
```bash
cd /home/user/v1.04_1812

# Crear estructura nueva
mkdir -p v1.04_1812/interface/base
mkdir -p v1.04_1812/interface/components
mkdir -p v1.04_1812/interface/config
mkdir -p v1.04_1812/interface/services
mkdir -p v1.04_1812/interface/state
mkdir -p v1.04_1812/interface/windows/manager
mkdir -p v1.04_1812/interface/windows/user
mkdir -p v1.04_1812/interface/windows/parts
mkdir -p v1.04_1812/interface/windows/dialogs
mkdir -p v1.04_1812/interface/legacy
mkdir -p tests/interface
mkdir -p tests/fixtures

# Crear __init__.py en cada carpeta
find v1.04_1812/interface -type d -exec touch {}/__init__.py \;
find tests -type d -exec touch {}/__init__.py \;

echo "✅ Estructura de carpetas creada"
```

### 2. Mover archivos a legacy (opcional, para desarrollo paralelo)
```bash
# ADVERTENCIA: Solo ejecutar si quieres desarrollo paralelo
# Copia de seguridad primero
cp -r v1.04_1812/interface v1.04_1812/interface_backup_$(date +%Y%m%d)

# Mover archivos actuales a legacy
mv v1.04_1812/interface/*.py v1.04_1812/interface/legacy/

echo "✅ Archivos movidos a legacy"
```

### 3. Configurar Git
```bash
# Crear branch
git checkout -b refactor/interfaces-phase-0

# Verificar cambios
git status

# Commit inicial
git add .
git commit -m "Fase 0: Estructura inicial de refactorización de interfaces"
```

---

## FASE 1: ELIMINACIÓN DE DUPLICACIÓN

### 1. Encontrar todos los archivos con cancel()
```bash
# Lista de archivos
grep -l "def cancel(self):" v1.04_1812/interface/*.py > /tmp/files_with_cancel.txt

# Ver contenido
cat /tmp/files_with_cancel.txt

# Contar
wc -l /tmp/files_with_cancel.txt
```

### 2. Encontrar todos los CTkMessagebox
```bash
# Buscar patterns
grep -rn "CTkMessagebox" v1.04_1812/interface/ | wc -l

# Agrupar por tipo
echo "=== ERROR ==="
grep -rn 'CTkMessagebox.*"Error' v1.04_1812/interface/ | wc -l

echo "=== SUCCESS ==="
grep -rn 'CTkMessagebox.*"Success' v1.04_1812/interface/ | wc -l

echo "=== WARNING ==="
grep -rn 'CTkMessagebox.*"Warning' v1.04_1812/interface/ | wc -l
```

### 3. Buscar imágenes base64 hardcoded
```bash
# Archivos con image_base64
grep -l "image_base64" v1.04_1812/interface/*.py

# Ver definiciones
grep -n "image_base64 = " v1.04_1812/interface/*.py
```

### 4. Comparar pares de archivos add/mod
```bash
# Crear script de comparación
cat > /tmp/compare_pairs.sh << 'EOF'
#!/bin/bash

compare_files() {
    file1=$1
    file2=$2
    echo "=== Comparing $file1 vs $file2 ==="
    diff_lines=$(diff $file1 $file2 | wc -l)
    total_lines=$(wc -l < $file1)
    similarity=$(echo "scale=2; (1 - $diff_lines / $total_lines) * 100" | bc)
    echo "Similarity: ${similarity}%"
    echo "Different lines: $diff_lines"
    echo ""
}

cd v1.04_1812/interface

compare_files "customer_add_interfaz.py" "customer_mod_interfaz.py"
compare_files "user_customer_add_interfaz.py" "user_customer_mod_interfaz.py"
compare_files "user_company_add_interfaz.py" "user_company_mod_interfaz.py"
compare_files "reg_catalog_hidro_add_interfaz.py" "reg_catalog_hidro_mod_interfaz.py"
EOF

chmod +x /tmp/compare_pairs.sh
/tmp/compare_pairs.sh
```

---

## FASE 2: REFACTORIZACIÓN DE ARCHIVOS GIGANTES

### 1. Analizar métodos de archivos grandes
```bash
# Extraer todos los métodos con su tamaño
analyze_methods() {
    file=$1
    echo "=== Methods in $file ==="
    awk '
    /^[[:space:]]*def / {
        if (method_name != "") {
            print method_name, ":", lines, "lines"
        }
        method_name = $2
        lines = 0
    }
    { lines++ }
    END {
        if (method_name != "") {
            print method_name, ":", lines, "lines"
        }
    }
    ' $file | sort -t: -k2 -rn
}

# Ejecutar para archivos grandes
analyze_methods v1.04_1812/interface/manager_project_interfaz.py
analyze_methods v1.04_1812/interface/user_project_interfaz.py
analyze_methods v1.04_1812/interface/manager_interfaz.py
analyze_methods v1.04_1812/interface/parts_manager_interfaz.py
```

### 2. Contar líneas de anidamiento
```bash
# Máxima profundidad de indentación
max_indent() {
    file=$1
    max=$(grep -E '^ +' $file | sed 's/[^ ].*//' | awk '{print length}' | sort -rn | head -1)
    levels=$((max / 4))
    echo "$file: $levels niveles de anidamiento ($max espacios)"
}

max_indent v1.04_1812/interface/manager_project_interfaz.py
max_indent v1.04_1812/interface/user_project_interfaz.py
max_indent v1.04_1812/interface/manager_interfaz.py
max_indent v1.04_1812/interface/parts_manager_interfaz.py
```

### 3. Extraer método a archivo nuevo (template)
```bash
# Script para extraer método a archivo separado
cat > /tmp/extract_method.py << 'EOF'
#!/usr/bin/env python3
import sys
import re

def extract_method(source_file, method_name, output_file):
    """Extrae un método a un archivo nuevo"""
    with open(source_file, 'r') as f:
        lines = f.readlines()

    # Encontrar inicio y fin del método
    start = None
    indent_level = None
    method_lines = []

    for i, line in enumerate(lines):
        if start is None:
            if re.match(rf'^\s*def {method_name}\s*\(', line):
                start = i
                indent_level = len(line) - len(line.lstrip())
                method_lines.append(line)
        else:
            # Dentro del método
            current_indent = len(line) - len(line.lstrip())

            # Fin del método: nueva def al mismo nivel o menor
            if line.strip() and current_indent <= indent_level and not line.strip().startswith('#'):
                break

            method_lines.append(line)

    if not method_lines:
        print(f"Método {method_name} no encontrado")
        return

    # Escribir a archivo nuevo
    with open(output_file, 'w') as f:
        f.write("# Método extraído automáticamente\n\n")
        f.writelines(method_lines)

    print(f"✅ Método {method_name} extraído a {output_file}")
    print(f"   {len(method_lines)} líneas")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: extract_method.py <source_file> <method_name> <output_file>")
        sys.exit(1)

    extract_method(sys.argv[1], sys.argv[2], sys.argv[3])
EOF

chmod +x /tmp/extract_method.py

# Ejemplo de uso:
# /tmp/extract_method.py \
#   v1.04_1812/interface/manager_interfaz.py \
#   main_new_project \
#   /tmp/main_new_project_extracted.py
```

---

## FASE 3: VARIABLES GLOBALES

### 1. Reemplazar variables globales por UserState
```bash
# Script de reemplazo automático
cat > /tmp/replace_globals.sh << 'EOF'
#!/bin/bash

# Buscar todas las referencias a data_user_bd
echo "=== Referencias a data_user_bd ==="
grep -rn "data_user_bd" v1.04_1812/interface/ | grep -v ".pyc"

# Buscar todas las referencias a user_privileges
echo "=== Referencias a user_privileges ==="
grep -rn "user_privileges" v1.04_1812/interface/ | grep -v ".pyc"

# TODO: Reemplazar manualmente cada uso por:
# from interface.state.user_state import UserState
# state = UserState()
# state.data  # en lugar de data_user_bd
# state.privileges  # en lugar de user_privileges
EOF

chmod +x /tmp/replace_globals.sh
/tmp/replace_globals.sh
```

### 2. Eliminar imports con asterisco
```bash
# Script para convertir import * a imports explícitos
cat > /tmp/fix_imports.py << 'EOF'
#!/usr/bin/env python3
import re
import sys

def find_used_symbols(file_path, imported_module):
    """Encuentra qué símbolos del módulo importado se usan en el archivo"""
    # Esto es simplificado - requiere análisis más profundo en producción
    with open(file_path, 'r') as f:
        content = f.read()

    # Buscar nombres que podrían venir del módulo
    # (esto es heurístico, no perfecto)
    potential_symbols = re.findall(r'\b([A-Z][a-zA-Z0-9_]*)\b', content)

    return list(set(potential_symbols))

def fix_star_import(file_path, line_number):
    """Intenta arreglar un import * específico"""
    print(f"Revisar manualmente: {file_path}:{line_number}")
    print("Sugerencia: Usa tu IDE para auto-import")

if __name__ == "__main__":
    # Encontrar todos los imports *
    import subprocess
    result = subprocess.run(
        ["grep", "-rn", "from .* import \\*", "v1.04_1812/interface/"],
        capture_output=True, text=True
    )

    for line in result.stdout.splitlines():
        parts = line.split(':')
        if len(parts) >= 2:
            file_path = parts[0]
            line_num = parts[1]
            print(f"⚠️  {file_path}:{line_num}")
EOF

chmod +x /tmp/fix_imports.py
/tmp/fix_imports.py
```

---

## TESTING

### 1. Configurar pytest
```bash
# Instalar dependencias
pip install pytest pytest-cov pytest-mock

# Crear pytest.ini
cat > pytest.ini << 'EOF'
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --cov=v1.04_1812/interface --cov-report=html --cov-report=term
EOF

echo "✅ pytest configurado"
```

### 2. Ejecutar tests
```bash
# Todos los tests
pytest

# Solo tests de interfaz
pytest tests/interface/

# Con coverage
pytest --cov=v1.04_1812/interface --cov-report=html

# Tests específicos
pytest tests/interface/test_base_window.py

# Ver coverage
open htmlcov/index.html  # En Linux: xdg-open
```

### 3. Test de regresión visual
```bash
# Capturar screenshots antes de refactorización
cat > /tmp/capture_screenshots.py << 'EOF'
#!/usr/bin/env python3
"""
Script para capturar screenshots de todas las ventanas
Ejecutar ANTES y DESPUÉS de la refactorización para comparar
"""
import os
from datetime import datetime

# TODO: Implementar captura automática de screenshots
# usando pyautogui o similar

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = f"/tmp/screenshots_{timestamp}"
os.makedirs(output_dir, exist_ok=True)

print(f"Capturas guardadas en: {output_dir}")
EOF
```

---

## MONITOREO DEL PROGRESO

### 1. Dashboard de métricas
```bash
cat > /tmp/metrics_dashboard.sh << 'EOF'
#!/bin/bash

echo "================================"
echo "   MÉTRICAS DE REFACTORIZACIÓN"
echo "================================"
echo ""

echo "📁 ARCHIVOS"
echo "  Total archivos: $(find v1.04_1812/interface -name "*.py" | wc -l)"
echo "  Archivos >1000 líneas: $(find v1.04_1812/interface -name "*.py" -exec wc -l {} \; | awk '$1 > 1000' | wc -l)"
echo ""

echo "📊 CÓDIGO"
total_lines=$(find v1.04_1812/interface -name "*.py" -exec wc -l {} \; | awk '{sum+=$1} END {print sum}')
echo "  Total líneas: $total_lines"
echo "  Objetivo: <15000"
echo ""

echo "🔍 PROBLEMAS"
globals=$(grep -r "global " v1.04_1812/interface/ | wc -l)
echo "  Keyword 'global': $globals (objetivo: 0)"

star_imports=$(grep -r "from .* import \*" v1.04_1812/interface/ | wc -l)
echo "  Import *: $star_imports (objetivo: 0)"

cancel_methods=$(grep -r "def cancel(self):" v1.04_1812/interface/ | wc -l)
echo "  Método cancel() duplicado: $cancel_methods (objetivo: 1)"
echo ""

echo "✅ TESTS"
if [ -d "tests/interface" ]; then
    test_files=$(find tests/interface -name "test_*.py" | wc -l)
    echo "  Archivos de test: $test_files"
else
    echo "  Archivos de test: 0"
fi
echo ""

echo "================================"
EOF

chmod +x /tmp/metrics_dashboard.sh
/tmp/metrics_dashboard.sh
```

### 2. Tracking de progreso por fase
```bash
cat > PROGRESS.md << 'EOF'
# PROGRESO DE REFACTORIZACIÓN

## Fase 0: Preparación
- [ ] Estructura de carpetas creada
- [ ] Tests básicos configurados
- [ ] Branch creado

## Fase 1: Eliminación de Duplicación
- [ ] BaseWindow creado
- [ ] BaseForm creado
- [ ] Módulo dialogs creado
- [ ] LogoMixin creado
- [ ] Archivos *_new eliminados
- [ ] Pares Add/Mod consolidados

## Fase 2: Archivos Gigantes
- [ ] manager_project_interfaz.py refactorizado
- [ ] user_project_interfaz.py refactorizado
- [ ] manager_interfaz.py refactorizado
- [ ] parts_manager_interfaz.py refactorizado

## Fase 3: Variables Globales
- [ ] UserState creado
- [ ] ImageManager creado
- [ ] Imports * eliminados

## Fase 4: Servicios
- [ ] ProjectService creado
- [ ] PartsService creado
- [ ] UserService creado
- [ ] CatalogService creado
- [ ] BudgetService creado
- [ ] CertificationService creado

## Fase 5: Testing
- [ ] Tests unitarios >80% coverage
- [ ] Documentación completa
- [ ] Guía de migración

## Métricas Actuales
- Líneas de código: 21978 → _____ (objetivo: <15000)
- Archivos: 47 → _____ (objetivo: ~40)
- Variables globales: 5 → _____ (objetivo: 0)
- Imports *: 14 → _____ (objetivo: 0)
- Test coverage: 0% → _____ (objetivo: >80%)
EOF

echo "✅ Archivo PROGRESS.md creado"
```

---

## GIT WORKFLOW

### Durante el desarrollo
```bash
# Commit frecuente de cambios pequeños
git add v1.04_1812/interface/base/base_window.py
git commit -m "feat: Añadir clase BaseWindow con método cancel()"

# Push a branch
git push -u origin refactor/interfaces-phase-0
```

### Al terminar cada fase
```bash
# Tag de la fase
git tag -a "refactor-phase-1-complete" -m "Fase 1: Duplicación eliminada"
git push origin refactor-phase-1-complete

# Merge a rama principal (después de testing)
git checkout claude/refactor-interface-architecture-011CUU2ZNsxAxGWkZeWGQjom
git merge refactor/interfaces-phase-1
git push
```

### Rollback si algo falla
```bash
# Volver a un tag anterior
git checkout refactor-phase-0-complete

# O deshacer último commit
git reset --hard HEAD~1
```

---

## UTILIDADES FINALES

### 1. Backup antes de cambios grandes
```bash
# Backup completo
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz v1.04_1812/interface/

# Backup de BD si aplica
cp database.db database.db.backup_$(date +%Y%m%d)
```

### 2. Linting automático
```bash
# Instalar herramientas
pip install black isort flake8 pylint

# Formatear código
black v1.04_1812/interface/
isort v1.04_1812/interface/

# Verificar estilo
flake8 v1.04_1812/interface/
pylint v1.04_1812/interface/
```

### 3. Generar documentación
```bash
# Instalar sphinx
pip install sphinx sphinx-rtd-theme

# Inicializar
cd docs
sphinx-quickstart

# Generar
make html
```

---

## CHECKLIST FINAL ANTES DE MERGE

```bash
cat > /tmp/pre_merge_checklist.sh << 'EOF'
#!/bin/bash

echo "🔍 CHECKLIST PRE-MERGE"
echo "====================="
echo ""

# 1. Tests pasan
echo "1. Ejecutando tests..."
if pytest; then
    echo "   ✅ Tests pasan"
else
    echo "   ❌ Tests fallan - NO HACER MERGE"
    exit 1
fi

# 2. Coverage >80%
echo "2. Verificando coverage..."
coverage=$(pytest --cov=v1.04_1812/interface --cov-report=term | grep "TOTAL" | awk '{print $4}' | tr -d '%')
if [ $coverage -ge 80 ]; then
    echo "   ✅ Coverage: ${coverage}%"
else
    echo "   ⚠️  Coverage: ${coverage}% (objetivo: >80%)"
fi

# 3. Linting
echo "3. Ejecutando linting..."
if flake8 v1.04_1812/interface/ --count; then
    echo "   ✅ Linting OK"
else
    echo "   ⚠️  Hay warnings de linting"
fi

# 4. No hay variables globales
echo "4. Verificando variables globales..."
globals_count=$(grep -r "global " v1.04_1812/interface/*.py | wc -l)
if [ $globals_count -eq 0 ]; then
    echo "   ✅ No hay variables globales"
else
    echo "   ⚠️  Hay $globals_count usos de 'global'"
fi

# 5. No hay import *
echo "5. Verificando imports..."
star_imports=$(grep -r "from .* import \*" v1.04_1812/interface/*.py | wc -l)
if [ $star_imports -eq 0 ]; then
    echo "   ✅ No hay import *"
else
    echo "   ⚠️  Hay $star_imports imports con *"
fi

echo ""
echo "====================="
echo "Revisión completada"
EOF

chmod +x /tmp/pre_merge_checklist.sh
```

---

¡Estos scripts te ayudarán a ejecutar la refactorización de manera sistemática y segura!
