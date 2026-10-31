#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
NODE_DIR="$ROOT/toolchain/node"

if ! command -v node >/dev/null 2>&1; then
  echo "Node.js 24+ is required. Use actions/setup-node@v7 or install Node 24." >&2
  exit 2
fi
node -e 'const major=Number(process.versions.node.split(".")[0]); if (major < 24) process.exit(1)' || {
  echo "Node.js >=24 required; found $(node --version)" >&2
  exit 2
}
if ! command -v ffmpeg >/dev/null 2>&1 || ! command -v ffprobe >/dev/null 2>&1; then
  echo "FFmpeg and ffprobe must be installed by the runner package manager." >&2
  exit 2
fi
if [[ -s "$NODE_DIR/package-lock.json" ]]; then
  echo "Using committed lockfile with npm ci."
  npm ci --prefix "$NODE_DIR" --include=dev --no-audit --no-fund
else
  echo "First install: resolving exact direct dependencies and generating lockfile."
  npm install --prefix "$NODE_DIR" --include=dev --no-audit --no-fund
fi
mkdir -p "$HOME/.cache/ms-playwright"
"$NODE_DIR/node_modules/.bin/playwright" install --with-deps chromium
printf 'NODE_TOOLCHAIN_DIR=%s\n' "$NODE_DIR"
printf 'NODE_TOOLCHAIN_BIN=%s\n' "$NODE_DIR/node_modules/.bin"
printf 'PLAYWRIGHT_BROWSERS_PATH=%s\n' "${PLAYWRIGHT_BROWSERS_PATH:-$HOME/.cache/ms-playwright}"
