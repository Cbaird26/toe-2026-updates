#!/usr/bin/env bash
# Build the real Cbaird26/zoraasi app and copy Vite output into docs/zoraasi-mobile/
# Requires: git, node 18+, npm 9+
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$ROOT/.zoraasi_build"
OUT_DIR="$ROOT/docs/zoraasi-mobile"
SKIN="$ROOT/scripts/zoraasi-mobile.css"
REPO="https://github.com/Cbaird26/zoraasi.git"

if [ "${CI:-}" = "true" ]; then
  set -x
fi

echo "==> ZoraASI mobile Pages build"
echo "    ROOT=$ROOT"

command -v git >/dev/null || { echo "git required"; exit 1; }
command -v npm >/dev/null || { echo "npm required"; exit 1; }

rm -rf "$BUILD_DIR"
echo "==> Cloning $REPO"
git clone --depth 1 "$REPO" "$BUILD_DIR"

cd "$BUILD_DIR"

echo "==> Injecting mobile CSS + import"
cp "$SKIN" src/mobile.css
if ! grep -q 'mobile.css' src/main.jsx; then
  printf '%s\n%s\n' 'import "./mobile.css";' "$(cat src/main.jsx)" > src/main.jsx.tmp
  mv src/main.jsx.tmp src/main.jsx
fi

echo "==> Viewport meta in index.html"
if ! grep -q 'viewport' index.html; then
  perl -0777 -i -pe 's/<head>/<head>\n    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">/' index.html
fi

echo "==> npm install && npm run build"
if [ -f package-lock.json ]; then
  npm ci || npm install
else
  npm install
fi
npm run build

test -d dist || { echo "dist/ missing"; exit 1; }

echo "==> Copy dist -> $OUT_DIR"
rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"
cp -R dist/. "$OUT_DIR/"

echo "==> Done. Commit with:"
echo "    git add docs/zoraasi-mobile && git commit -m 'ZoraASI: ship upstream Vite build for zoraasi-mobile'"
