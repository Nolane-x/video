#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
PROFILE="$1"
case "$PROFILE" in
  editorial) REQUIREMENTS="$ROOT/toolchain/python/editorial/requirements.txt" ;;
  manim) REQUIREMENTS="$ROOT/toolchain/python/manim/requirements.txt" ;;
  audio-ml) REQUIREMENTS="$ROOT/toolchain/python/audio-ml/requirements.txt" ;;
  *) echo "Usage: $0 {editorial|manim|audio-ml}" >&2; exit 2 ;;
esac
PYTHON_BIN=python3.12
command -v "$PYTHON_BIN" >/dev/null 2>&1 || { echo "Python 3.12 is required" >&2; exit 2; }
VENV="$ROOT/toolchain/.venvs/$PROFILE"
"$PYTHON_BIN" -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install --requirement "$REQUIREMENTS"
printf 'Python profile %s installed at %s\n' "$PROFILE" "$VENV"
