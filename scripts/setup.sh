#!/usr/bin/env bash
set -euo pipefail

echo "==> Creating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "==> Installing cyberhosp with dev dependencies..."
pip install -e ".[dev]"

echo "==> Done. Activate with: source .venv/bin/activate"
