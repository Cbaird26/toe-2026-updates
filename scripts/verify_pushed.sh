#!/usr/bin/env bash
# Verify that the TOE repo is aligned with origin/main and that key doc strings exist on the remote.
# From TOE repo root: ./scripts/verify_pushed.sh
# Exit 0 if all checks pass; non-zero otherwise.
set -e
TOE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$TOE_ROOT"

echo "=== 1. Sync check ==="
git fetch origin
HEAD=$(git rev-parse HEAD)
ORIGIN_MAIN=$(git rev-parse origin/main)
if [[ "$HEAD" != "$ORIGIN_MAIN" ]]; then
  echo "FAIL: HEAD ($HEAD) != origin/main ($ORIGIN_MAIN). Push or pull to align."
  exit 1
fi
echo "OK: HEAD == origin/main"

echo ""
echo "=== 2. Remote content check (REPLICATION_LADDER) ==="
if ! git show origin/main:docs/REPLICATION_LADDER.md 2>/dev/null | grep -q "./scripts/run_all.sh"; then
  echo "FAIL: './scripts/run_all.sh' not found in origin/main:docs/REPLICATION_LADDER.md"
  exit 1
fi
echo "OK: canonical command string present"

if ! git show origin/main:docs/REPLICATION_LADDER.md 2>/dev/null | grep -q "qrng-falsification-claim"; then
  echo "FAIL: 'qrng-falsification-claim' not found in origin/main:docs/REPLICATION_LADDER.md"
  exit 1
fi
echo "OK: falsification anchor present"

echo ""
echo "=== All checks passed: GitHub has the current state. ==="
