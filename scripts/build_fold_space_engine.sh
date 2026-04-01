#!/usr/bin/env bash
# Build Fold-Space Engine (Vite) and copy static output to docs/ for local or private use.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APP="$ROOT/apps/fold-space-engine"
OUT="$ROOT/docs/fold-space-engine"

cd "$APP"
if [[ ! -d node_modules ]]; then
  npm install
fi
npm test
npm run build
rm -rf "$OUT"
mkdir -p "$OUT"
cp -R dist/. "$OUT/"
echo "OK: $OUT"
