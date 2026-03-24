#!/usr/bin/env bash
# Build papers_sources/H1_QRNG_Pilot_Methods_Status_2026.pdf (pdfLaTeX x2, no BibTeX).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEX="$ROOT/papers_sources/H1_QRNG_Pilot_Methods_Status_2026.tex"
OUTDIR="$ROOT/papers_sources"
cd "$OUTDIR"
pdflatex -interaction=nonstopmode -halt-on-error "$(basename "$TEX")"
pdflatex -interaction=nonstopmode -halt-on-error "$(basename "$TEX")"
echo "OK: $OUTDIR/H1_QRNG_Pilot_Methods_Status_2026.pdf"
