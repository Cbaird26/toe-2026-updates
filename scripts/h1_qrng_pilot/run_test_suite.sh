#!/usr/bin/env bash
# H1 + MQGT-SCF non-interactive smoke tests for Codex / CI (run from TOE repo root).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

TMP="${TMPDIR:-/tmp}/toe_h1_test_suite"
mkdir -p "$TMP"

if [ -x "$ROOT/.venv/bin/python3" ]; then
  PYTHON="$ROOT/.venv/bin/python3"
else
  PYTHON="python3"
fi

echo "== TOE test suite =="
echo "ROOT=$ROOT"
echo "TMP=$TMP"
"$PYTHON" --version

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

echo "== py_compile H1 pilot =="
"$PYTHON" -m py_compile \
  scripts/h1_qrng_pilot/collect.py \
  scripts/h1_qrng_pilot/analyze.py \
  scripts/h1_qrng_pilot/stats_core.py \
  scripts/h1_qrng_pilot/placebo_batch.py \
  scripts/h1_qrng_pilot/export_comparison_row.py \
  scripts/mqgt_sim/mqgt_phase4_lattice_demo.py \
  scripts/mqgt_sim/mqgt_phase4b_symmetry_breaking_demo.py \
  scripts/mqgt_sim/mqgt_phase4b_parameter_sweep.py \
  || fail "py_compile"

echo "== H1 placebo collect + analyze + sha256 =="
H5="$TMP/smoke.h5"
"$PYTHON" scripts/h1_qrng_pilot/collect.py --mode placebo --seed 424242 --target-bits 65536 --out "$H5"
"$PYTHON" scripts/h1_qrng_pilot/analyze.py "$H5" --verify-sha256 --burnin-bits 0 --holdout-fraction 0.2 \
  || fail "analyze"
rm -f "$H5"

echo "== H1 placebo_batch (12 replicates) =="
CSV="$TMP/batch.csv"
JSON="$TMP/summary.json"
"$PYTHON" scripts/h1_qrng_pilot/placebo_batch.py \
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
"$PYTHON" scripts/mqgt_sim/h2_visibility_stack.py --save-dir "$H2DIR" --no-show \
  || fail "h2_visibility_stack"
test -f "$H2DIR/h2_visibility_vs_gamma.png" || fail "missing h2 png"

echo "== MQGT-SCF mqgt_phase4_lattice_demo (Agg) =="
P4DIR="$TMP/phase4_lattice"
"$PYTHON" scripts/mqgt_sim/mqgt_phase4_lattice_demo.py \
  --grid-size 16 \
  --steps 24 \
  --dt 0.04 \
  --seed 123 \
  --save-dir "$P4DIR" \
  --no-show \
  || fail "phase4 lattice demo"
test -f "$P4DIR/mqgt_phase4_lattice_demo.png" || fail "missing phase4 png"
test -f "$P4DIR/mqgt_phase4_lattice_demo_summary.json" || fail "missing phase4 json"

echo "== MQGT-SCF mqgt_phase4b_symmetry_breaking_demo (Agg) =="
P4BDIR="$TMP/phase4b_lattice"
"$PYTHON" scripts/mqgt_sim/mqgt_phase4b_symmetry_breaking_demo.py \
  --grid-size 16 \
  --steps 20 \
  --substeps 2 \
  --dt 0.04 \
  --seed 123 \
  --save-dir "$P4BDIR" \
  --no-show \
  || fail "phase4b lattice demo"
test -f "$P4BDIR/mqgt_phase4b_symmetry_breaking_demo.png" || fail "missing phase4b png"
test -f "$P4BDIR/mqgt_phase4b_symmetry_breaking_demo_summary.json" || fail "missing phase4b json"

echo "== MQGT-SCF mqgt_phase4b_parameter_sweep (Agg) =="
P4BSWEEPDIR="$TMP/phase4b_sweep"
"$PYTHON" scripts/mqgt_sim/mqgt_phase4b_parameter_sweep.py \
  --xis "0.000,0.020" \
  --gammas "0.05,0.15" \
  --g-couples "0.00" \
  --seeds 1 \
  --steps 8 \
  --substeps 1 \
  --grid-size 12 \
  --outdir "$P4BSWEEPDIR" \
  || fail "phase4b parameter sweep"
test -f "$P4BSWEEPDIR/phase4b_parameter_sweep_results.csv" || fail "missing phase4b sweep csv"
test -f "$P4BSWEEPDIR/summary.md" || fail "missing phase4b sweep summary"
test -f "$P4BSWEEPDIR/lock_rate_g_0.000.png" || fail "missing phase4b sweep lock heatmap"
test -f "$P4BSWEEPDIR/mean_coherence_g_0.000.png" || fail "missing phase4b sweep coherence heatmap"

echo "== MQGT-SCF mqgt_gksl_ethics_field_sim (optional qutip) =="
GKSLOUT="$TMP/gksl.png"
if "$PYTHON" -c "import qutip" 2>/dev/null; then
  "$PYTHON" scripts/mqgt_sim/mqgt_gksl_ethics_field_sim.py --save "$GKSLOUT" --no-show \
    || fail "gksl sim"
  test -f "$GKSLOUT" || fail "missing gksl png"
else
  echo "SKIP: qutip not installed"
fi

echo "ALL CHECKS PASSED"
echo "Artifacts (safe to rm -rf): $TMP"
exit 0
