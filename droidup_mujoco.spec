# PyInstaller single-file bundle for the E1 21-DOF MuJoCo simulation.
from pathlib import Path

from PyInstaller.utils.hooks import collect_dynamic_libs, collect_submodules
import mujoco

ROOT = Path(SPECPATH).resolve()
MUJOCO_ROOT = Path(mujoco.__file__).resolve().parent
datas = [
    (str(ROOT / "assets" / "droidup" / "e1_21dof"), "assets/droidup/e1_21dof"),
    (str(ROOT / "simulate" / "configs" / "e1_21dof_full.json"), "simulate/configs"),
]
binaries = []
for library in MUJOCO_ROOT.rglob("*.so*"):
    # Python extension modules are picked up through normal imports. The
    # remaining shared objects are MuJoCo itself and its rendering plugins.
    if ".cpython-" not in library.name:
        binaries.append((str(library), str(Path("mujoco") / library.relative_to(MUJOCO_ROOT).parent)))
binaries += collect_dynamic_libs("glfw")
hiddenimports = [
    *collect_submodules("droidup"),
    "grpc",
    "grpc.aio",
    "tqdm",
]

a = Analysis(
    [str(ROOT / "simulate" / "droidup_mujoco.py")],
    pathex=[str(ROOT / "simulate")],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=1,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="droidup-mujoco",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
