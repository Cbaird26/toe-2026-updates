#!/usr/bin/env bash
# git_update_all.sh — Commit, push, and sync all repos (TOE, Black-Book, public mirrors).
# Run from TOE root: ./scripts/git_update_all.sh

set -e
TOE="${TOE:-$(cd "$(dirname "$0")/.." && pwd)}"
BLACKBOOK="${BLACKBOOK:-$HOME/Downloads/mqgt_scf_reissue_2026-01-20_010939UTC}"

echo "=== 1. TOE — commit and push ==="
cd "$TOE"
git add -A
if ! git diff --cached --quiet 2>/dev/null; then
  git commit -m "Sync: Phase II cross-ref, Zenodo 19060024, corpus updates"
fi
git pull origin main 2>/dev/null || git pull origin main 2>/dev/null || true
git push origin main 2>&1

echo ""
echo "=== 2. Full sync (Black-Book → toe-empirical-validation, TOE → toe-2026-updates, iCloud) ==="
cd "$BLACKBOOK"
./scripts/sync_to_public_and_push.sh 2>&1

echo ""
echo "=== 3. Black-Book — push to public remote if configured ==="
cd "$BLACKBOOK"
if git remote get-url public-toe-empirical-validation &>/dev/null; then
  git add -A
  git commit -m "Sync: scripts, config" --allow-empty 2>/dev/null || true
  git push public-toe-empirical-validation main 2>&1 || echo "  Push failed."
else
  echo "  No public-toe-empirical-validation remote; sync script handles public mirrors."
fi

echo ""
echo "=== DONE ==="
