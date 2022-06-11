# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['alien_invasion.py'],
    pathex=[],
    binaries=[],
    datas=[('images/alien.png', 'images'),('images/ship.bmp','images'),('high_score.json','.'),('music/Explo_Large.wav','music'),('music/Explo_Small.wav','music'),('music/Bullet_Whiz.wav','music'),('music/order_music.mp3','music')],
    hiddenimports=['pygame.pkgdata'],
    hookspath=[],
    hooksconfig={},
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='alien_invasion',
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
    icon='alien.ico',
)
