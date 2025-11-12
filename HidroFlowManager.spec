# -*- mode: python ; coding: utf-8 -*-


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
        ('informes_guardados', 'informes_guardados')  # Directorio para configs de informes
    ],
    hiddenimports=[
        'mysql.connector',
        'tkcalendar',
        'customtkinter',
        'CTkMessagebox',
        'PIL',
        'matplotlib',
        'openpyxl',
        'xlsxwriter',
        'docx',
        'reportlab',
        'script.informes_storage',
        'script.informes',
        'script.informes_config',
        'script.informes_exportacion',
        'interface.informes_interfaz'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
