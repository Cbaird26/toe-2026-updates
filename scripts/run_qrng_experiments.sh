#!/usr/bin/env bash
# Run ANU QRNG experiments (same method as March 2026).
# Run this script from the TOE workspace root, or set TOE_CORPUS_2026 to override.
#
# Usage:
#   ./run_qrng_experiments.sh baseline   # 100k bits (~$0.07)
#   ./run_qrng_experiments.sh 1M         # 1M bits (~$0.62)
#   ./run_qrng_experiments.sh 5M         # 5M bits (~$3.05)
#   ./run_qrng_experiments.sh 10M        # 10M bits (~$6.11)
#   ./run_qrng_experiments.sh ladder     # baseline + 1M + 5M + 10M in sequence
#   ./run_qrng_experiments.sh remaining  # 1M + 5M + 10M in sequence
#
# Key: read from artifacts/.anu_api_key (see docs/QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md)

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_BASE="$(cd "$SCRIPT_DIR/.." && pwd)"
BASE="${TOE_CORPUS_2026:-$DEFAULT_BASE}"
OUT="artifacts/"

if [[ ! -d "$BASE" ]]; then
  echo "Workspace not found at: $BASE"
  echo "Set TOE_CORPUS_2026 if you want to run against a different repo root."
  exit 1
fi

cd "$BASE" || exit 1
if [[ ! -f scripts/anu_qrng_collect.py ]]; then
  echo "scripts/anu_qrng_collect.py not found in $BASE"
  exit 1
fi

run_baseline() {
  echo "--- Running baseline 100k bits ---"
  python3 scripts/anu_qrng_collect.py --n 100000 --out "$OUT" --label baseline --preflight --no-fallback
}

run_1M() {
  echo "--- Running 1M bits ---"
  python3 scripts/anu_qrng_collect.py --n 1000000 --out "$OUT" --label ladder_1M --preflight --no-fallback
}

run_5M() {
  echo "--- Running 5M bits ---"
  python3 scripts/anu_qrng_collect.py --n 5000000 --out "$OUT" --label ladder_5M --preflight --no-fallback
}

run_10M() {
  echo "--- Running 10M bits ---"
  python3 scripts/anu_qrng_collect.py --n 10000000 --out "$OUT" --label ladder_10M --preflight --no-fallback
}

case "${1:-baseline}" in
  baseline) run_baseline ;;
  1M)       run_1M ;;
  5M)       run_5M ;;
  10M)      run_10M ;;
  remaining)
    run_1M
    run_5M
    run_10M
    echo "--- Remaining ladder (1M + 5M + 10M) complete ---"
    ;;
  ladder)
    run_baseline
    run_1M
    run_5M
    run_10M
    echo "--- Ladder (baseline + 1M + 5M + 10M) complete ---"
    ;;
  *)
    echo "Usage: $0 baseline|1M|5M|10M|remaining|ladder"
    exit 1
    ;;
esac

echo "Done. Artifacts in $BASE/$OUT"
