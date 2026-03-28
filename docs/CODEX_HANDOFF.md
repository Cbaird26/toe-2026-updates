# Codex / executor handoff (TOE)

**Repo (private):** [cbaird26/toe-2026-updates](https://github.com/Cbaird26/toe-2026-updates) — clone and push only with GitHub access and **explicit human** approval; work from the repository root (`TOE/`).
**Verified baseline:** `ec33369`

## Do this first (no network required)

```bash
cd /path/to/TOE
chmod +x scripts/h1_qrng_pilot/run_test_suite.sh
./scripts/h1_qrng_pilot/run_test_suite.sh
```

**Success:** exit code `0` and `ALL CHECKS PASSED`.

## Current local H1 baseline (March 20, 2026)

- Green baseline already recorded locally: `run_test_suite.sh` passed, `run_10m_parity.sh` passed, and a matched `12 x 10M` placebo gate passed at `target_bits=10000000`, `burnin_bits=0`, `holdout_fraction=0.2`.
- Current 10M placebo artifacts: `artifacts/h1_pilot/placebo_runs/batch_12x10m_20260320.csv` and `artifacts/h1_pilot/placebo_runs/summary_12x10m_20260320.json`.
- If Python env and H1 code are unchanged, **do not rerun** the 10M parity or matched 10M placebo gate just to reconfirm the same baseline; use the existing artifacts and summaries.

## Full procedure & manual fallback

**→ [CODEX_HANDOFF_H1_AND_MQGT_TESTS_2026.md](CODEX_HANDOFF_H1_AND_MQGT_TESTS_2026.md)** — H1 pilot (`collect`, `analyze`, `placebo_batch`), MQGT-SCF smoke (H2 stack, Phase IV lattice, Phase IV-B, optional GKSL), **do-not** list, **report-back** template.

## Optional human-approved jobs (not CI)

| Task | Command / doc |
|------|-----------------|
| 10M urandom + placebo parity | `scripts/h1_qrng_pilot/run_10m_parity.sh` — see [scripts/h1_qrng_pilot/README.md](../scripts/h1_qrng_pilot/README.md) |
| Matched 12x10M placebo gate | `scripts/h1_qrng_pilot/placebo_batch.py` at `target_bits=10000000`, `burnin_bits=0`, `holdout_fraction=0.2`; see full handoff for artifacts + acceptance rule |
| Phase II Swarm / coherence ladder (spec) | [PROJECT_ZORA_PHASE_II_SWARM_COHERENCE_QRNG_PROTOCOL_10M_2026.md](PROJECT_ZORA_PHASE_II_SWARM_COHERENCE_QRNG_PROTOCOL_10M_2026.md) — block runner **not** fully implemented; `collect.py` alone is single-stream |
| Public sync (maintainers) | [README.md](../README.md#syncing-this-repo-to-github-public) · `scripts/repo_sync_public_mqgt_h1_phase4b.sh` |
| Full session update (all artifacts) | [CODEX_HANDOFF_FULL_SESSION_UPDATE.md](CODEX_HANDOFF_FULL_SESSION_UPDATE.md) — incorporate all posted artifacts, align parameters, commit + push |
| Fusion + GitHub update | [CODEX_HANDOFF_FUSION_GITHUB_UPDATE.md](CODEX_HANDOFF_FUSION_GITHUB_UPDATE.md) — commit + push fusion console, figures, script |

## Safety & authority

- **[SAFETY_CONSTITUTION.md](../SAFETY_CONSTITUTION.md)** — no `git push`, Zenodo, OSF, or large paid API runs without **explicit human** approval.
- **H2** remains the primary physics falsification lane; H1 / QRNG is secondary (see [H2_PILOT_PREREGISTRATION_2026.md](H2_PILOT_PREREGISTRATION_2026.md)).

## Related: Zora Finance OS (separate repo)

Repo boundaries and dashboard handoff links (not H1 scope): **[CODEX_HANDOFF_ZORA_REPO_BOUNDARIES_2026-03-25.md](handoffs/2026-03/CODEX_HANDOFF_ZORA_REPO_BOUNDARIES_2026-03-25.md)**.

## Quick report-back

```
TOE test suite: PASS | FAIL
Commit: <git rev-parse --short HEAD>
Python: <python3 --version>
Disk: <df -h . | tail -1>
Failed step: <name>
stderr: <paste>
```
