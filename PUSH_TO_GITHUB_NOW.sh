#!/bin/bash
# Run this in your terminal to push everything to GitHub.
# chmod +x PUSH_TO_GITHUB_NOW.sh && ./PUSH_TO_GITHUB_NOW.sh

set -e
echo "=== 1. TOE ==="
cd "$(dirname "$0")"
git add -A
git status -s
git commit -m "Sync: corpus REVTeX, handoff docs" --allow-empty
git pull origin main 2>/dev/null || git pull origin main
git push origin main
echo ""

echo "=== 2. Full Sync (toe-empirical-validation, toe-2026-updates, iCloud) ==="
cd "$HOME/Downloads/mqgt_scf_reissue_2026-01-20_010939UTC"
./scripts/sync_to_public_and_push.sh
echo ""

echo "=== 3. Black-Book ==="
git push public-toe-empirical-validation main 2>/dev/null || echo "Run: git push public-toe-empirical-validation main"
echo ""
echo "=== DONE ==="
