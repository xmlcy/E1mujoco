#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON:-python3}"

if ! "${PYTHON_BIN}" -c 'import PyInstaller, droidup, grpc, mujoco, numpy' >/dev/null 2>&1; then
  cat >&2 <<'EOF'
Missing build dependencies. Activate the build environment and install:
  PyInstaller, numpy, grpcio, mujoco, tqdm, droidup-api, droidup-client
The DroidUp wheels are provided separately by DroidUp SDK.
EOF
  exit 1
fi

cd "${ROOT}"
"${PYTHON_BIN}" -m PyInstaller --clean --noconfirm --distpath dist --workpath build droidup_mujoco.spec
chmod +x dist/droidup-mujoco
echo "Built: ${ROOT}/dist/droidup-mujoco"
