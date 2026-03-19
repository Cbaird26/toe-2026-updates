#!/usr/bin/env bash
# Build Phase II PDF for ai.viXra submission.
# Run from TOE repo root: ./scripts/build_phase2_for_aivixra.sh
#
# Output: papers_sources/MQGT_SCF_PhaseII_2026.pdf (< 5 MB for viXra)

set -e
TOE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$TOE_ROOT"
TEX="papers_sources/MQGT-SCF_Phase_II_Submission_2026.tex"
OUT="papers_sources/MQGT_SCF_PhaseII_2026.pdf"

if [[ ! -f "$TEX" ]]; then
  echo "Missing: $TEX"
  exit 1
fi

echo "Compiling (pdflatex x2)..."
(cd papers_sources && pdflatex -interaction=nonstopmode "$(basename "$TEX")" >/dev/null)
(cd papers_sources && pdflatex -interaction=nonstopmode "$(basename "$TEX")" >/dev/null)

PDF_BASE="${TEX%.tex}.pdf"
if [[ -f "$PDF_BASE" ]]; then
  cp "$PDF_BASE" "$OUT"
  SIZE=$(stat -f%z "$OUT" 2>/dev/null || stat -c%s "$OUT" 2>/dev/null)
  SIZE_MB=$(awk "BEGIN { printf \"%.2f\", $SIZE/1048576 }")
  echo "Built: $OUT ($SIZE_MB MB)"
  if [[ $SIZE -gt 5242880 ]]; then
    echo "WARNING: > 5 MB. Compress for viXra: gs -sDEVICE=pdfwrite -dPDFSETTINGS=/ebook -o ${OUT%.pdf}_compressed.pdf $OUT"
  fi
else
  echo "Expected PDF not found: $PDF_BASE"
  exit 1
fi
