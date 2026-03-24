#!/usr/bin/env bash
# Build MQGT_SCF_Anchor_2026.pdf from the Phase II anchor TeX (revtex).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEX="$ROOT/papers_sources/MQGT_SCF_Phase_II_2026/MQGT_SCF_Anchor_2026.tex"
DIR="$(dirname "$TEX")"
BASE="$(basename "$TEX" .tex)"
cd "$DIR"
echo "== Building $BASE.pdf in $DIR =="
pdflatex -interaction=nonstopmode "$BASE.tex"
pdflatex -interaction=nonstopmode "$BASE.tex"
echo "== Done: $DIR/$BASE.pdf =="
ls -la "$BASE.pdf"
