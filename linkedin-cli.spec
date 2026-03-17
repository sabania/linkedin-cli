# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = []
binaries = []
hiddenimports = [
    'nodriver', 'nodriver.core', 'nodriver.cdp',
    'websockets',
    'typer', 'click', 'rich',
    'auth', 'linkedin_wrapper', 'nodriver_adapter',
    'commands', 'commands.profile', 'commands.feed', 'commands.posts',
    'commands.connections', 'commands.search', 'commands.messaging',
    'commands.jobs', 'commands.company', 'commands.notifications',
    'commands.signals', 'commands.config',
]
tmp_ret = collect_all('nodriver')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    [],
    exclude_binaries=True,
    name='linkedin-cli',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='linkedin-cli',
)
