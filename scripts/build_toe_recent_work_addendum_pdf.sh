#!/usr/bin/env bash
# Build papers_sources/TOE_Recent_Work_Addendum_2026.pdf (full) and optionally the physics-only variant.
# Usage:
#   bash scripts/build_toe_recent_work_addendum_pdf.sh              # full only
#   bash scripts/build_toe_recent_work_addendum_pdf.sh --physics    # full + physics PDFs
#   bash scripts/build_toe_recent_work_addendum_pdf.sh --physics-only  # physics PDF only
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUTDIR="$ROOT/papers_sources"
cd "$OUTDIR"

build_tex() {
  local base="$1"
  pdflatex -interaction=nonstopmode -halt-on-error "$base"
  pdflatex -interaction=nonstopmode -halt-on-error "$base"
}

MODE=full
for arg in "$@"; do
  case "$arg" in
    --physics)
      MODE=both
      ;;
    --physics-only)
      MODE=physics
      ;;
    *)
      echo "Unknown option: $arg" >&2
      echo "Usage: $0 [--physics | --physics-only]" >&2
      exit 1
      ;;
  esac
done

case "$MODE" in
  full)
    build_tex "TOE_Recent_Work_Addendum_2026.tex"
    echo "OK: $OUTDIR/TOE_Recent_Work_Addendum_2026.pdf"
    ;;
  both)
    build_tex "TOE_Recent_Work_Addendum_2026.tex"
    echo "OK: $OUTDIR/TOE_Recent_Work_Addendum_2026.pdf"
    build_tex "TOE_Recent_Work_Addendum_2026_physics.tex"
    echo "OK: $OUTDIR/TOE_Recent_Work_Addendum_2026_physics.pdf"
    ;;
  physics)
    build_tex "TOE_Recent_Work_Addendum_2026_physics.tex"
    echo "OK: $OUTDIR/TOE_Recent_Work_Addendum_2026_physics.pdf"
    ;;
esac
