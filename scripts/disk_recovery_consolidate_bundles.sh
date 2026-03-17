#!/bin/bash
# Consolidate redundant mqgt/reissue bundles — move to Trash to free space.
# Canonical Black-Book: mqgt_scf_reissue_2026-01-20_010939UTC
# Run with --dry-run to preview; without to execute.

set -e
DOWNLOADS="${DOWNLOADS:-$HOME/Downloads}"
KEEP="mqgt_scf_reissue_2026-01-20_010939UTC"  # Canonical Black-Book
DRY_RUN=false
[[ "$1" == "--dry-run" ]] && DRY_RUN=true

echo "=== mqgt/reissue bundle consolidation ==="
echo "Keeping: $KEEP"
echo ""

for dir in "$DOWNLOADS"/mqgt_* "$DOWNLOADS"/*reissue* "$DOWNLOADS"/*regen* 2>/dev/null; do
  [[ ! -d "$dir" ]] && continue
  name=$(basename "$dir")
  [[ "$name" == "$KEEP" ]] && continue
  # Skip TOE, reissued_files, toe_fifth_force - different purpose
  [[ "$name" == "TOE" ]] && continue
  [[ "$name" =~ ^reissued_files ]] && continue
  [[ "$name" == "toe_fifth_force_constraints_pack" ]] && continue
  size=$(du -sh "$dir" 2>/dev/null | cut -f1)
  if $DRY_RUN; then
    echo "[DRY-RUN] Would move to Trash: $name ($size)"
  else
    echo "Moving to Trash: $name ($size)"
    mv "$dir" "$HOME/.Trash/${name}_$(date +%s)" 2>/dev/null || echo "  (skip: $dir)"
  fi
done
echo ""
echo "Done."
