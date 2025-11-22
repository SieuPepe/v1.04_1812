# -*- mode: python ; coding: utf-8 -*-
# HydroFlow Manager v2.0 - PyInstaller Configuration


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('resources/images/*.jpeg', 'resources/images'),
        ('resources/images/*.png', 'resources/images'),
        ('resources/images/*.ico', 'resources/images'),
        ('resources/images/*.jpg', 'resources/images'),
        ('output/*.xlsx', 'output'),
        ('interface/*.py', 'interface'),
        ('script/*.py', 'script'),
        ('informes_guardados', 'informes_guardados'),  # Directorio para configs de informes
        ('plantillas/*.docx', 'plantillas'),  # Plantillas Word para generación de PDFs
        ('.env.example', '.'),  # Incluir plantilla de configuración (NO incluir .env real)
        ('INSTALACION.md', '.'),  # Guía de instalación
        ('docs/manual/*.md', 'docs/manual'),  # Manuales de usuario
    ],
    hiddenimports=[
        # Base de datos
        'mysql.connector',
        'mysql.connector.pooling',

        # GUI
        'tkcalendar',
        'customtkinter',
        'CTkMessagebox',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',

        # Visualización
        'matplotlib',
        'matplotlib.backends.backend_tkagg',

        # Procesamiento de datos
        'pandas',  # v2.0 - Agregado para procesamiento de datos
        'numpy',

        # Exportación
        'openpyxl',
        'xlsxwriter',
        'docx',
        'reportlab',
        'reportlab.platypus',
        'reportlab.lib',
        'reportlab.lib.pagesizes',
        'reportlab.lib.styles',
        'reportlab.lib.colors',

        # Windows COM (Word/PDF)
        'win32com',
        'win32com.client',
        'pythoncom',

        # Configuración v2.0
        'dotenv',  # v2.0 - Para cargar archivos .env
        'pathlib',
        'getpass',

        # Utilidades
        'subprocess',
        'json',
        'csv',
        'datetime',
        'decimal',

        # Módulos internos - Informes
        'script.informes_storage',
        'script.informes',
        'script.informes_config',
        'script.informes_exportacion',
        'script.plantillas_config',
        'interface.informes_interfaz',

        # Módulos internos - Configuración v2.0
        'script.db_config',
        'script.db_user_config',
        'script.db_connection',
        'script.db_core',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Excluir módulos de desarrollo/testing
        'pytest',
        'unittest',
        'test',
        'tests',
        '_pytest',
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='HidroFlowManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resources\\images\\logo.ico'],
)
