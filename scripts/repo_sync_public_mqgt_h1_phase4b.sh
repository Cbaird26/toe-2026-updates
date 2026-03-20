#!/usr/bin/env bash
# Stage + commit MQGT-SCF lattice (Phase IV-B), H1 docs, and related CI glue; optionally push to origin (public GitHub).
# Run from anywhere:  ./scripts/repo_sync_public_mqgt_h1_phase4b.sh
# With push:           ./scripts/repo_sync_public_mqgt_h1_phase4b.sh --push
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PUSH=0
if [[ "${1:-}" == "--push" ]]; then
  PUSH=1
fi

echo "== TOE repo_sync_public_mqgt_h1_phase4b =="
echo "ROOT=$ROOT"
git status -sb

git add \
  README.md \
  AGENTS.md \
  scripts/mqgt_sim/mqgt_phase4_lattice_demo.py \
  scripts/mqgt_sim/mqgt_phase4b_symmetry_breaking_demo.py \
  scripts/mqgt_sim/mqgt_phase4b_parameter_sweep.py \
  scripts/mqgt_sim/README.md \
  scripts/h1_qrng_pilot/run_test_suite.sh \
  docs/H1_CURRENT_STATUS_MEMO_2026.md \
  docs/H1_PILOT_COMPARISON_SUMMARY.md \
  docs/H1_AT_1E9_DETECTION_TO_CALIBRATION.md \
  docs/ZORA_CONTINUITY_LOG.md \
  scripts/repo_sync_public_mqgt_h1_phase4b.sh

if git diff --cached --quiet; then
  echo "Nothing staged (paths unchanged or already committed)."
else
  git commit -m "MQGT-SCF: Phase IV-B lattice + sweep; H1 docs (status, comparison, 10^9 calibration); sync script"
fi

if [[ "$PUSH" -eq 1 ]]; then
  echo "== git push origin main (public) =="
  git push origin main
else
  echo "Skipping push. To publish: $0 --push"
fi

git status -sb
