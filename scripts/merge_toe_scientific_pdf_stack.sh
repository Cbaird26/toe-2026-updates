#!/usr/bin/env bash
# Merge the documented scientific ToE packet PDFs into one file (order from docs/TOE_RECENT_WORK_STACK_2026.md).
#
# Order:
#   1. Addendum_2026_ToE_Companion.pdf
#   2. Main ToE PDF (default: A_Theory_of_Everything_CM_Baird_et_al_2026.pdf; override with MAIN_TOE=... or --main-toe)
#   3. Evidence_Emergent_Matter_Quantum_Vacuum_MQGT-SCF_2026.pdf
#   4. MQGT_SCF_Phase_II_2026/MQGT_SCF_Anchor_2026.pdf
#   5. H1_QRNG_Pilot_Methods_Status_2026.pdf
#   6. TOE_Recent_Work_Addendum_2026[_physics].pdf
#
# Usage:
#   bash scripts/merge_toe_scientific_pdf_stack.sh [--physics|--full] [--main-toe PATH] [--out PATH] [--dry-run]
#
# Requires: pdfunite (Poppler) or gs (Ghostscript).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PAPERS="$ROOT/papers_sources"

MODE=physics
OUT=""
MAIN=""
DRY=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --physics)
      MODE=physics
      shift
      ;;
    --full)
      MODE=full
      shift
      ;;
    --main-toe)
      MAIN="$2"
      shift 2
      ;;
    --out)
      OUT="$2"
      shift 2
      ;;
    --dry-run)
      DRY=1
      shift
      ;;
    -h|--help)
      sed -n '1,25p' "$0" | tail -n +2
      exit 0
      ;;
    *)
      echo "Unknown option: $1 (use --help)" >&2
      exit 1
      ;;
  esac
done

if [[ -z "${MAIN}" ]]; then
  MAIN="${MAIN_TOE:-$PAPERS/A_Theory_of_Everything_CM_Baird_et_al_2026.pdf}"
fi

if [[ "${MODE}" == full ]]; then
  RECENT="$PAPERS/TOE_Recent_Work_Addendum_2026.pdf"
  DEFAULT_OUT="$PAPERS/TOE_scientific_stack_merged_full_2026.pdf"
else
  RECENT="$PAPERS/TOE_Recent_Work_Addendum_2026_physics.pdf"
  DEFAULT_OUT="$PAPERS/TOE_scientific_stack_merged_physics_2026.pdf"
fi

if [[ -z "${OUT}" ]]; then
  OUT="$DEFAULT_OUT"
fi

FILES=(
  "$PAPERS/Addendum_2026_ToE_Companion.pdf"
  "$MAIN"
  "$PAPERS/Evidence_Emergent_Matter_Quantum_Vacuum_MQGT-SCF_2026.pdf"
  "$PAPERS/MQGT_SCF_Phase_II_2026/MQGT_SCF_Anchor_2026.pdf"
  "$PAPERS/H1_QRNG_Pilot_Methods_Status_2026.pdf"
  "$RECENT"
)

echo "Merge order (${MODE} addendum at slot 6):"
i=1
for f in "${FILES[@]}"; do
  printf '  %d. %s\n' "$i" "$f"
  if [[ ! -f "$f" ]]; then
    echo "ERROR: missing file: $f" >&2
    if [[ "$f" == "$MAIN" ]]; then
      echo "Hint: set MAIN_TOE or pass --main-toe PATH to your canonical main ToE PDF." >&2
      echo "Candidates in papers_sources (if present):" >&2
      ls -1 "$PAPERS"/A_Theory_of_Everything*.pdf "$PAPERS"/A_Unified_Theory*.pdf "$PAPERS"/MQGT_SCF_Unified*.pdf 2>/dev/null | sed 's/^/  /' >&2 || true
    fi
    exit 1
  fi
  i=$((i + 1))
done

if [[ "$DRY" -eq 1 ]]; then
  echo "Dry run: would write -> $OUT"
  exit 0
fi

merge_pdfunite() {
  pdfunite "$@" "$OUT"
}

merge_gs() {
  gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -dPDFSETTINGS=/default -sOutputFile="$OUT" "$@"
}

if command -v pdfunite >/dev/null 2>&1; then
  merge_pdfunite "${FILES[@]}"
elif command -v gs >/dev/null 2>&1; then
  merge_gs "${FILES[@]}"
else
  echo "ERROR: need pdfunite (Poppler) or gs (Ghostscript) on PATH." >&2
  echo "  macOS: brew install poppler   # or: brew install ghostscript" >&2
  exit 1
fi

echo "OK: $OUT"
