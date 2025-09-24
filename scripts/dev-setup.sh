#!/usr/bin/env bash
set -euo pipefail

# Usage: scripts/dev-setup.sh [--gui]
# Creates venv, installs core deps, and optionally GUI deps.

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

pip install -r requirements-core.txt

if [[ "${1-}" == "--gui" ]]; then
  pip install -r requirements.txt
fi

if [ ! -f .env ]; then
  cp .env.example .env
fi

echo "Setup concluído. Ative a venv com: source .venv/bin/activate" \
     "e rode pytest -q ou make gui."
