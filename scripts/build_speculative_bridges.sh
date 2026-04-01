#!/usr/bin/env bash
# Build PDFs for papers_sources/speculative_bridges/*.tex (pdflatex, one pass each).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/papers_sources/speculative_bridges"
for f in \
  Foldspace_Navigation_Variational_Branch_Selection_2026.tex \
  Foldspace_Navigation_MQGTSCF_Norma_Paradigm_2026.tex \
  Cosmic_Keyboard_Timeline_Selection_2026.tex
do
  pdflatex -interaction=nonstopmode -halt-on-error "$f"
done
echo "OK: $ROOT/papers_sources/speculative_bridges/*.pdf (if pdflatex succeeded)"
