#!/usr/bin/env bash
# Copy standalone HTML exports from ~/Downloads into docs/ for GitHub Pages.
# Run from any cwd:  bash scripts/sync_toe_pages_html_from_downloads.sh
set -euo pipefail
DL="${DL:-$HOME/Downloads}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DOCS="$ROOT/docs"
mkdir -p "$DOCS/theory-of-everything-foundation" "$DOCS/artifacts" "$DOCS/zora-matrix-builder"

cp "$DL/toe-ultimate.html" "$DOCS/theory-of-everything-foundation/index.html"
cp "$DL/toe-foundation-redesign.html" "$DOCS/theory-of-everything-foundation/cosmic-redesign.html"
cp "$DL/index (2).html" "$DOCS/artifacts/foundation-legacy-index-2.html"
cp "$DL/index_1.html" "$DOCS/artifacts/foundation-legacy-index-1.html"
cp "$DL/index (1).html" "$DOCS/artifacts/zora-framework-portal-standalone.html"

# Zora Matrix Builder (single-file app; optional sources in ~/Downloads)
# Same copy as: python3 scripts/materialize_matrix_index.py (from repo root)
if [[ -f "$DL/zora-matrix-fixed.html" ]]; then
  cp "$DL/zora-matrix-fixed.html" "$DOCS/zora-matrix-builder/index.html"
elif [[ -f "$DL/zora-matrix-v2.html" ]]; then
  cp "$DL/zora-matrix-v2.html" "$DOCS/zora-matrix-builder/index.html"
fi
if [[ -f "$DL/zora-matrix-builder.html" ]]; then
  cp "$DL/zora-matrix-builder.html" "$DOCS/zora-matrix-builder/matrix-builder-v1.html"
fi
if [[ -f "$DL/zora-matrix-builder APP.html" ]]; then
  cp "$DL/zora-matrix-builder APP.html" "$DOCS/zora-matrix-builder/matrix-builder-app.html"
fi

echo "OK: synced Foundation + artifacts + Matrix (where present) into $DOCS"
ls -la "$DOCS/theory-of-everything-foundation/index.html" \
       "$DOCS/theory-of-everything-foundation/cosmic-redesign.html" \
       "$DOCS/artifacts/foundation-legacy-index-2.html" \
       "$DOCS/artifacts/foundation-legacy-index-1.html" \
       "$DOCS/artifacts/zora-framework-portal-standalone.html" 2>/dev/null || true
ls -la "$DOCS/zora-matrix-builder/" 2>/dev/null || true
