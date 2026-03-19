#!/usr/bin/env bash
# H1 + MQGT-SCF non-interactive smoke tests for Codex / CI (run from TOE repo root).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

TMP="${TMPDIR:-/tmp}/toe_h1_test_suite"
mkdir -p "$TMP"

echo "== TOE test suite =="
echo "ROOT=$ROOT"
echo "TMP=$TMP"
python3 --version

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

echo "== py_compile H1 pilot =="
python3 -m py_compile \
  scripts/h1_qrng_pilot/collect.py \
  scripts/h1_qrng_pilot/analyze.py \
  scripts/h1_qrng_pilot/stats_core.py \
  scripts/h1_qrng_pilot/placebo_batch.py \
  || fail "py_compile"

echo "== H1 placebo collect + analyze + sha256 =="
H5="$TMP/smoke.h5"
python3 scripts/h1_qrng_pilot/collect.py --mode placebo --seed 424242 --target-bits 65536 --out "$H5"
python3 scripts/h1_qrng_pilot/analyze.py "$H5" --verify-sha256 --burnin-bits 0 --holdout-fraction 0.2 \
  || fail "analyze"
rm -f "$H5"

echo "== H1 placebo_batch (12 replicates) =="
CSV="$TMP/batch.csv"
JSON="$TMP/summary.json"
python3 scripts/h1_qrng_pilot/placebo_batch.py \
  --replicates 12 \
  --base-seed 7 \
  --target-bits 40000 \
  --burnin-bits 512 \
  --holdout-fraction 0.2 \
  --permutations 150 \
  --perm-seed 99 \
  --z-thresholds "2,3,5" \
  --out-csv "$CSV" \
  --out-summary-json "$JSON" \
  || fail "placebo_batch"
test -s "$CSV" || fail "empty CSV"
test -s "$JSON" || fail "empty JSON"

echo "== MQGT-SCF h2_visibility_stack (Agg) =="
H2DIR="$TMP/h2_stack"
python3 scripts/mqgt_sim/h2_visibility_stack.py --save-dir "$H2DIR" --no-show \
  || fail "h2_visibility_stack"
test -f "$H2DIR/h2_visibility_vs_gamma.png" || fail "missing h2 png"

echo "== MQGT-SCF mqgt_gksl_ethics_field_sim (optional qutip) =="
GKSLOUT="$TMP/gksl.png"
if python3 -c "import qutip" 2>/dev/null; then
  python3 scripts/mqgt_sim/mqgt_gksl_ethics_field_sim.py --save "$GKSLOUT" --no-show \
    || fail "gksl sim"
  test -f "$GKSLOUT" || fail "missing gksl png"
else
  echo "SKIP: qutip not installed"
fi

echo "ALL CHECKS PASSED"
echo "Artifacts (safe to rm -rf): $TMP"
exit 0
