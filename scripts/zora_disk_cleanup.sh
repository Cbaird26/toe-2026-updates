#!/bin/bash
# zora_disk_cleanup.sh
# Safe first-pass disk cleanup for ZoraASI/TOE ecosystem.
# Does NOT delete repos or vault data. Run periodically for "new day" maintenance.
#
# Usage: ./scripts/zora_disk_cleanup.sh [--remove-venv-pdf]
#   --remove-venv-pdf   Also remove TOE/.venv_pdf (30MB) if PDF tooling unused

set -e
HOME="${HOME:-/Users/$(whoami)}"
TOE="${TOE:-$HOME/Downloads/TOE}"
BLACKBOOK="${BLACKBOOK:-$HOME/Downloads/mqgt_scf_reissue_2026-01-20_010939UTC}"
LOCALASI="${LOCALASI:-$HOME/LocalASI_Dev}"

REMOVE_VENV_PDF=false
[[ "${1:-}" == "--remove-venv-pdf" ]] && REMOVE_VENV_PDF=true

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Zora Disk Cleanup — Safe First Pass                           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# ---------------------------------------------------------------------------
# 1. Prune __pycache__, *.pyc
# ---------------------------------------------------------------------------
echo "[1/4] Pruning __pycache__ and *.pyc..."
for root in "$TOE" "$BLACKBOOK" "$LOCALASI"; do
  if [[ -d "$root" ]]; then
    find "$root" -type d -name __pycache__ -print0 2>/dev/null | xargs -0 rm -rf 2>/dev/null || true
    find "$root" -type f -name "*.pyc" -delete 2>/dev/null || true
  fi
done
echo "  Done."
echo ""

# ---------------------------------------------------------------------------
# 2. Prune logs
# ---------------------------------------------------------------------------
echo "[2/4] Pruning logs..."
[[ -d "$TOE/logs" ]] && rm -f "$TOE/logs"/*.log 2>/dev/null || true
[[ -d "$LOCALASI/logs" ]] && rm -f "$LOCALASI/logs"/*.log 2>/dev/null || true
[[ -d "$BLACKBOOK" ]] && rm -f "$BLACKBOOK"/pull_all_repos_*.log 2>/dev/null || true
echo "  Done."
echo ""

# ---------------------------------------------------------------------------
# 3. Git gc
# ---------------------------------------------------------------------------
echo "[3/4] Running git gc in TOE and Black-Book..."
[[ -d "$TOE/.git" ]] && (cd "$TOE" && git gc --aggressive 2>/dev/null) && echo "  TOE: done" || true
[[ -d "$BLACKBOOK/.git" ]] && (cd "$BLACKBOOK" && git gc --aggressive 2>/dev/null) && echo "  Black-Book: done" || true
echo "  Done."
echo ""

# ---------------------------------------------------------------------------
# 4. Optional: remove .venv_pdf
# ---------------------------------------------------------------------------
if $REMOVE_VENV_PDF && [[ -d "$TOE/.venv_pdf" ]]; then
  echo "[4/4] Removing TOE/.venv_pdf (use --remove-venv-pdf)..."
  rm -rf "$TOE/.venv_pdf"
  echo "  Removed."
else
  echo "[4/4] Skipping .venv_pdf (pass --remove-venv-pdf to remove)."
fi
echo ""

# ---------------------------------------------------------------------------
# 5. Black-Book audit (manual review)
# ---------------------------------------------------------------------------
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Black-Book Disk Usage (manual review)                         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
if [[ -d "$BLACKBOOK" ]]; then
  du -sh "$BLACKBOOK"/* 2>/dev/null | sort -hr | head -15
fi
echo ""
echo "Done. See plan: .cursor/plans/zora_hd_memory_recovery_*.plan.md"
