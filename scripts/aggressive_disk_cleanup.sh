#!/bin/bash
# Aggressive disk cleanup — run when very low on space (< 1GB free).
# Run: bash scripts/aggressive_disk_cleanup.sh

set -e
echo "=== Aggressive Disk Cleanup ==="

# 1. Empty Trash (frees space from moved bundles)
echo "[1] Emptying Trash..."
rm -rf ~/.Trash/* 2>/dev/null || true
echo "    Done."

# 2. Cursor / IDE caches
echo "[2] Clearing Cursor cache..."
rm -rf ~/Library/Application\ Support/Cursor/Cache/* 2>/dev/null || true
rm -rf ~/Library/Application\ Support/Cursor/CachedData/* 2>/dev/null || true
echo "    Done."

# 3. VS Code cache
echo "[3] Clearing VS Code cache..."
rm -rf ~/Library/Application\ Support/Code/Cache/* 2>/dev/null || true
echo "    Done."

# 4. Dev caches
echo "[4] Purging pip, npm, yarn, Homebrew..."
pip cache purge 2>/dev/null || true
npm cache clean --force 2>/dev/null || true
yarn cache clean 2>/dev/null || true
brew cleanup --prune=all 2>/dev/null || true
echo "    Done."

# 5. Browser caches (Safari, Chrome)
echo "[5] Clearing browser caches..."
rm -rf ~/Library/Caches/com.apple.Safari/* 2>/dev/null || true
rm -rf ~/Library/Caches/Google/Chrome/* 2>/dev/null || true
echo "    Done."

# 6. Xcode DerivedData (again)
echo "[6] Clearing Xcode DerivedData..."
rm -rf ~/Library/Developer/Xcode/DerivedData/* 2>/dev/null || true
echo "    Done."

# 7. Docker prune (if Docker installed)
if command -v docker &>/dev/null; then
  echo "[7] Docker system prune..."
  docker system prune -af 2>/dev/null || true
  echo "    Done."
else
  echo "[7] Docker not found, skipping."
fi

# 8. Time Machine local snapshots (often 10-50GB!)
echo "[8] Checking Time Machine local snapshots..."
SNAPS=$(tmutil listlocalsnapshots / 2>/dev/null)
if [ -n "$SNAPS" ]; then
  echo "    Found local snapshots. To delete (frees significant space):"
  echo "    tmutil deletelocalsnapshots /"
  echo "    Run that command manually if desired."
else
  echo "    None found."
fi

echo ""
echo "=== Cleanup complete. Check free space: df -h / ==="
