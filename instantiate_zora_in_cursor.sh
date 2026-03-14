#!/bin/bash
# instantiate_zora_in_cursor.sh
# Full Resource Pull: ZoraASI + iCloud + git. Cursor acts as Zora (no local model).
# Run: ./instantiate_zora_in_cursor.sh
# Or: bash instantiate_zora_in_cursor.sh

set -e
HOME="${HOME:-/Users/$(whoami)}"
TOE="${TOE:-$HOME/Downloads/TOE}"
BLACKBOOK="${BLACKBOOK:-$HOME/Downloads/mqgt_scf_reissue_2026-01-20_010939UTC}"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Instantiate Zora in Cursor — Full Resource Pull               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# ---------------------------------------------------------------------------
# 1. ZoraASI multi-source instantiation (iCloud, Google Drive, OneDrive, local)
# ---------------------------------------------------------------------------
echo "[1/3] ZoraASI instantiation (all sources)..."
cd "$TOE"
if [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
fi
python instantiate_zoraasi.py
echo ""

# ---------------------------------------------------------------------------
# 2. Zora full sync (iCloud + git, no local model)
# ---------------------------------------------------------------------------
echo "[2/3] Zora full sync (iCloud + git)..."
if [ -f "$BLACKBOOK/home/zora_sync_no_local.sh" ]; then
  bash "$BLACKBOOK/home/zora_sync_no_local.sh"
else
  echo "  ⚠ zora_sync_no_local.sh not found at $BLACKBOOK/home/"
fi
echo ""

# ---------------------------------------------------------------------------
# 3. Health check (update ZORA_READY_STATUS.md)
# ---------------------------------------------------------------------------
echo "[3/3] Running health check..."
if [ -f "$TOE/scripts/zora_health_check.sh" ]; then
  bash "$TOE/scripts/zora_health_check.sh" 2>/dev/null || true
fi
echo ""

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Next: Open Cursor with TOE workspace                          ║"
echo "╠════════════════════════════════════════════════════════════════╣"
echo "║  cursor $TOE/toe-and-repos.code-workspace                       ║"
echo "║                                                                ║"
echo "║  Then enable: .cursor/rules/zora-as-cursor.mdc                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo "— Zora"
