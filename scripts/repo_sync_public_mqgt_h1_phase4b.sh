#!/usr/bin/env bash
# Stage + commit the current TOE public-session bundle; optionally push to origin (public GitHub).
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

mkdir -p papers_sources/figures/h2_stack

git add \
  README.md \
  AGENTS.md \
  papers_sources/README.md \
  papers_sources/H1_QRNG_Pilot_Methods_Status_2026.tex \
  papers_sources/H1_QRNG_Pilot_Methods_Status_2026.pdf \
  papers_sources/H1_QRNG_Pilot_Methods_Status_2026Notes.bib \
  papers_sources/figures/README_figures.md \
  papers_sources/MQGT_SCF_Phase_II_2026/MQGT_SCF_Anchor_2026.tex \
  papers_sources/MQGT_SCF_Phase_II_2026/MQGT_SCF_Anchor_2026.pdf \
  papers_sources/MQGT_SCF_Phase_II_2026/MQGT_SCF_Anchor_2026_rxiverse_submission_metadata.txt \
  papers_sources/figures/mqgt_scf/zora_cooperative_games_results.json \
  papers_sources/figures/mqgt_scf/zora_cooperative_games_summary.png \
  scripts/mqgt_sim/mqgt_phase4_lattice_demo.py \
  scripts/mqgt_sim/mqgt_phase4b_symmetry_breaking_demo.py \
  scripts/mqgt_sim/mqgt_phase4b_parameter_sweep.py \
  scripts/mqgt_sim/fusion_zora_burn_figures.py \
  scripts/mqgt_sim/zora_cooperative_games_sim.py \
  scripts/mqgt_sim/README.md \
  scripts/h1_qrng_pilot/run_test_suite.sh \
  scripts/build_h1_methods_pdf.sh \
  scripts/zora_recursive_scalar_demo.py \
  docs/CODEX_HANDOFF.md \
  docs/CODEX_HANDOFF_FULL_SESSION_UPDATE.md \
  docs/CODEX_HANDOFF_FUSION_GITHUB_UPDATE.md \
  docs/H1_CURRENT_STATUS_MEMO_2026.md \
  docs/H1_PILOT_COMPARISON_SUMMARY.md \
  docs/H1_AT_1E9_DETECTION_TO_CALIBRATION.md \
  docs/PHASE_II_SUBMISSION_STATUS_2026.md \
  docs/CANONICAL_SPINE.md \
  docs/ZORA_CONTINUITY_LOG.md \
  docs/ZORA_COOPERATIVE_GAMES_SIMULATION_2026.md \
  docs/zora_coherence.html \
  docs/zora_fusion_console.html \
  docs/zora_dashboard.html \
  docs/zoraasi_dashboard.jsx \
  docs/zora_self_manifestation.html \
  papers_sources/figures/fusion_zora/ \
  papers_sources/figures/h2_stack/e_modulated_collapse.png \
  papers_sources/figures/h2_stack/ \
  papers_sources/figures/mqgt_scf/mqgt_scf_phi_e_gksl_concept.png \
  papers_sources/figures/mqgt_scf/ \
  papers_sources/MQGT_SCF_Phase_II_2026/ \
  phase_iv_b_sweep/ \
  scripts/mqgt_sim/mqgt_multi_channel_exclusion_plot.py \
  scripts/mqgt_sim/zora_gksl_e_modulated_collapse.py \
  scripts/repo_sync_public_mqgt_h1_phase4b.sh

if git diff --cached --quiet; then
  echo "Nothing staged (paths unchanged or already committed)."
else
  git commit -m "MQGT-SCF: publish full session artifacts and public sync surfaces"
fi

if [[ "$PUSH" -eq 1 ]]; then
  echo "== git push origin main (public) =="
  git push origin main
else
  echo "Skipping push. To publish: $0 --push"
fi

git status -sb
