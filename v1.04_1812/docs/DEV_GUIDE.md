# Guía de Desarrollo — HidroFlowManager

## 1) Entorno
- Python 3.11 — Conda env: `hfm-py311`
- IDE: VSCode
- BD: MySQL 8 (`localhost:3307`)

## 2) Estructura del proyecto
- `main.py`: punto de entrada.
- `interface/`: GUI (CustomTkinter).
- `script/`: lógica/servicios (DB, export a Excel).
- `source/`: recursos (iconos, imágenes).
- `backup/`: SQL históricos (no restaurar sobre `mysql.*`).
- `build/` y `dist/`: artefactos de PyInstaller (generados).

## 3) Ejecutar en desarrollo
```bat
conda activate hfm-py311
cd D:\Dev\HFM\v1.04_1812
python main.py

## 4) Depuración (VSCode)

-Abre main.py y pulsa F5 con una configuración de Python.

-Alternativa: Terminal integrada → python main.py.

-Comprueba que el intérprete activo sea hfm-py311.

## 5) Estilo

Formato: Black (opcional).

Lint: flake8 básico (opcional).

Comentarios y nombres en español coherentes.

## 6) Dónde tocar según el cambio

Interfaz: interface\*.py

Exportación de certificaciones: script\certification_export.py

Acceso a datos / SQL: script\modulo_db.py

## 7) Empaquetado (resumen)

PyInstaller: HidroFlowManager.spec

Incluir source\ (y plantillas .xlsx si se usan) en datas del .spec.