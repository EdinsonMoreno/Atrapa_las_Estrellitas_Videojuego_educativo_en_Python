# -*- mode: python ; coding: utf-8 -*-
import sys
from PyInstaller.utils.hooks import collect_data_files

datas = [
    ('src/sonido_estrella.wav', '.'),
    ('src/sonido_bomba.wav', '.'),
    ('src/sonido_fondo.wav', '.'),
    ('src/sonido_gameover.wav', '.'),
    ('src/sonido_disparo.wav', '.'),
    ('src/sonido_explosion.wav', '.'),
    ('src/Fondo.png', '.'),
    ('src/progreso.json', '.'),
    ('Ico/a.png', 'Ico'),
    ('Logo/Logo.png', 'Logo')
]

# Si tienes una carpeta internal, agrega:
# datas += collect_data_files('internal')

block_cipher = None

a = Analysis(
    ['src/juego.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AtrapaLasEstrellitas',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='Ico/a.png'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AtrapaLasEstrellitas'
)
