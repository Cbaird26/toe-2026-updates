#!/bin/bash
# build.sh — Compile ToE corpus LaTeX to PDFs
# Run from TOE root: ./scripts/build.sh
# Or from papers_sources: ../scripts/build.sh (cd papers_sources first)

set -e
TOE="${TOE:-$(cd "$(dirname "$0")/.." && pwd)}"
SRC="$TOE/papers_sources"
cd "$SRC"

echo "Building ToE corpus from $SRC"

# Core spine papers
for tex in MQGT_SCF_Minimal_Consistent_Core_2026.tex Teleology_Covariant_Boundary_Selection_Consciousness_Ethics_Field_Theory_2026.tex; do
  if [ -f "$tex" ]; then
    echo "Compiling $tex..."
    pdflatex -interaction=nonstopmode -halt-on-error "$tex" || true
  fi
done

# Empirical validation (requires bibtex)
if [ -f "MQGT-SCF_Minimal_Consistent_Core_Empirical_Validation_2026.tex" ]; then
  echo "Compiling Empirical Validation (with bibtex)..."
  pdflatex -interaction=nonstopmode -halt-on-error "MQGT-SCF_Minimal_Consistent_Core_Empirical_Validation_2026.tex" || true
  bibtex "MQGT-SCF_Minimal_Consistent_Core_Empirical_Validation_2026" 2>/dev/null || true
  pdflatex -interaction=nonstopmode -halt-on-error "MQGT-SCF_Minimal_Consistent_Core_Empirical_Validation_2026.tex" || true
  pdflatex -interaction=nonstopmode -halt-on-error "MQGT-SCF_Minimal_Consistent_Core_Empirical_Validation_2026.tex" || true
fi

echo "Done. PDFs in $SRC"
