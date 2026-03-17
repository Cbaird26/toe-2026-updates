# QRNG scripts (TOE)

## Method constancy — do not change the experiment

**We do not change methods for an experiment we already ran.** The March 2026 QRNG runs used specific scripts and a specific protocol. Replication and any further ladder runs must use the **same** process.

- **Canonical method:** [QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md](../docs/QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md) — protocol, script names, artifact schema, and recovery from Codex logs.
- **Scripts that were used:** `anu_qrng_collect.py`, `anu_qrng_experiment.py`, `qrng_test_suite.py`, `qrng_compare_runs.py`. They are not yet in this repo; recover from Codex logs or your machine, then commit and document the path in the method doc.

## Run the pilot and ladder (same method as March 2026)

1. **Recover the scripts** that produced the March 2026 result (see method doc; use Codex logs to find path and commands).
2. **Pilot (10k):** Run with the **same** collector: e.g. `anu_qrng_collect.py --pilot` (exact command from your logs).
3. **Ladder:** Same scripts, same block design (20 × 100k, control vs intervention, seeds), with `--bits` 1000000, 10000000, etc. as per [PHASE_I_QRNG_TRACE_MAP_2026.md](../docs/PHASE_I_QRNG_TRACE_MAP_2026.md).

## Phase II helpers

- `qrng_phase2_run.py` — writes a Phase II plan template and runs one Phase II session while calling `anu_qrng_collect.py` unchanged.
- `qrng_phase2_model_compare.py` — compares null vs linear vs threshold-style models on the `phase2_sessions.csv` manifest.
- `qrng_phase2_pilot.py` — writes the 100k Phase II pilot manifests and runnable block scripts (`Pilot 0–2`), then summarizes by condition.

Protocol and runbook: [QRNG_PHASE_II_EXPERIMENT_DESIGN_2026.md](../docs/QRNG_PHASE_II_EXPERIMENT_DESIGN_2026.md)
100k pilot-first runbook: [QRNG_PHASE_II_100K_PILOT_RUNBOOK_2026.md](../docs/QRNG_PHASE_II_100K_PILOT_RUNBOOK_2026.md)

## Optional: standalone pilot script (not the March 2026 method)

`anu_qrng_pilot.py` in this folder is a **standalone** 10k-bit fetch for quick API/billing checks. It is **not** the same method as March 2026. Do not use it for replication or for reporting as part of the same experiment. For any run that continues the Phase I ladder, use the recovered March 2026 scripts.
