#!/usr/bin/env bash
set -euo pipefail

# Simple helper to setup venv, install deps, and run the app (SQLite fallback).
# Usage:
#   ./run_local.sh           # setup & run the SQLite end-to-end runner
#   ./run_local.sh setup     # only setup venv and install deps
#   ./run_local.sh run       # same as no-args
#   ./run_local.sh add "Inception"
#   ./run_local.sh search "incep"
#   ./run_local.sh status 1 finished

VENV_DIR=.venv
REQ=requirements.txt

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtualenv in $VENV_DIR..."
  python3 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "Installing dependencies (quiet)..."
pip install -q -r "$REQ"

if [ ! -f .env ]; then
  echo ".env not found — copying from .env.example. Edit .env and set OMDB_API_KEY before running CLI commands."
  cp .env.example .env || true
fi

if [ $# -eq 0 ]; then
  echo "Running SQLite end-to-end runner..."
  PYTHONPATH=. python3 scripts/run_sqlite_local.py
  exit 0
fi

cmd="$1"
shift || true
case "$cmd" in
  setup)
    echo "Setup complete. Activate with: source $VENV_DIR/bin/activate" ;;
  run)
    PYTHONPATH=. python3 scripts/run_sqlite_local.py "$@" ;;
  add|search|status|remove|summary)
    PYTHONPATH=. python3 -m cli.main "$cmd" "$@" ;;
  *)
    echo "Usage: $0 [setup|run|add|search|status|remove|summary] args..."
    exit 1 ;;
esac
