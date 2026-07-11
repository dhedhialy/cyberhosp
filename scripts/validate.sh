#!/usr/bin/env bash
set -euo pipefail

echo "==> Running ruff linter..."
ruff check src/ tests/

echo "==> Running tests..."
pytest -v --cov=src/cyberhosp tests/

echo "==> All checks passed."
