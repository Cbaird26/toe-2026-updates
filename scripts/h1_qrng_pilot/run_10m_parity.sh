#!/usr/bin/env bash
# Collect 10M-bit streams for urandom + placebo (parity with existing anu_10m at 10M).
# ANU: optional second 10M replicate — see README; existing anu_10m row already covers 10M ANU.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
OUT="${ROOT}/artifacts/h1_pilot"
mkdir -p "$OUT"

if [ -x "${ROOT}/.venv/bin/python" ]; then
  PYTHON="${ROOT}/.venv/bin/python"
else
  PYTHON="python3"
fi

echo "== H1 10M parity (urandom + placebo) =="
echo "PYTHON=$PYTHON"
echo "OUT=$OUT"

"$PYTHON" scripts/h1_qrng_pilot/collect.py \
  --mode urandom \
  --target-bits 10000000 \
  --out "$OUT/urandom_10m.h5"

"$PYTHON" scripts/h1_qrng_pilot/collect.py \
  --mode placebo \
  --seed 20260319 \
  --target-bits 10000000 \
  --out "$OUT/placebo_10m.h5"

echo "== analyze (verify SHA-256) =="
"$PYTHON" scripts/h1_qrng_pilot/analyze.py "$OUT/urandom_10m.h5" \
  --verify-sha256 --burnin-bits 0 --holdout-fraction 0.2
"$PYTHON" scripts/h1_qrng_pilot/analyze.py "$OUT/placebo_10m.h5" \
  --verify-sha256 --burnin-bits 0 --holdout-fraction 0.2

echo "== CSV rows (append to artifacts/h1_pilot/run_comparison_individual.csv) =="
"$PYTHON" scripts/h1_qrng_pilot/export_comparison_row.py \
  --run-id urandom_10m --source urandom --h5 "$OUT/urandom_10m.h5" \
  --notes "OS CSPRNG 10M parity"
"$PYTHON" scripts/h1_qrng_pilot/export_comparison_row.py \
  --run-id placebo_10m --source placebo --h5 "$OUT/placebo_10m.h5" \
  --notes "PCG64 placebo 10M single file seed 20260319"

echo "Done."
