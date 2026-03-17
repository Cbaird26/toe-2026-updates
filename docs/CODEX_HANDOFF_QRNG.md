# Codex handoff: QRNG program (TOE)

**Give this to Codex so it can continue the QRNG work without losing context.** Christopher Michael Baird | March 2026

---

## QRNG closure in git (main)

- **Close-out:** `c5e6886` — Close Phase II QRNG 100k swarm pilot: non-replication of Pilot 2 signal; protocol closed with no scaling.
- **Follow-up:** `4c4d866` — Add QRNG swarm protocol audit and lessons learned notes.

Cite these when linking corpus or reports to the archived closure.

---

## Where everything lives

| What | Path |
|------|------|
| **TOE repo (primary)** | `~/Downloads/TOE` |
| **Docs** | `TOE/docs/` |
| **Scripts** | `TOE/scripts/` — `anu_qrng_collect.py`, `run_qrng_experiments.sh` |
| **Artifacts & key** | `TOE/artifacts/` (gitignored). API key: `artifacts/.anu_api_key` — **never paste key in chat.** User has keys; they live in that file. |

---

## Current state

- **Phase I:** Closed. Single intervention vs control → no detectable effect (6M bits, 3 runs; pooled p = 0.41). Method locked in [QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md](QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md).
- **Baseline 100k:** Already run from TOE; wrote `artifacts/anu_qrng_baseline_*_summary.json` and `*_bits.csv`. p1 ≈ 0.4987, z ≈ -0.83 (null-like).
- **Runner:** [run_qrng_experiments.sh](TOE/scripts/run_qrng_experiments.sh) runs from TOE by default, uses `--preflight --no-fallback`. Targets: `baseline | 1M | 5M | 10M | remaining | ladder`.
- **Remaining ladder (Stage A):** 1M, 5M, 10M — not yet run. After 10M, Stage B = pause and evaluate; Stage C = branch to 50M/100M or Phase II swarm at 100k first. See [QRNG_STAGED_PROGRAM_AND_BUDGET_2026.md](QRNG_STAGED_PROGRAM_AND_BUDGET_2026.md).

---

## Commands (run from TOE root)

```bash
cd ~/Downloads/TOE
```

**Test terminal / preflight:**
```bash
/bin/echo cursor-ok && pwd && python3 --version
```

**Run remaining ladder (1M + 5M + 10M):**
```bash
./scripts/run_qrng_experiments.sh remaining
```

**Or one at a time:**
```bash
./scripts/run_qrng_experiments.sh 1M
./scripts/run_qrng_experiments.sh 5M
./scripts/run_qrng_experiments.sh 10M
```

Key is read from `artifacts/.anu_api_key`; user has already set this up. Do not ask for the key in chat.

---

## Key docs (read in this order if needed)

1. **[QRNG_STAGED_PROGRAM_AND_BUDGET_2026.md](QRNG_STAGED_PROGRAM_AND_BUDGET_2026.md)** — Three lanes, stage gates, budget rule, 100k swarm pilot. Single “how we don’t blow finances” reference.
2. **[PHASE_I_QRNG_TRACE_MAP_2026.md](PHASE_I_QRNG_TRACE_MAP_2026.md)** — Ladder table, order of ops, decision rules, links to all QRNG docs.
3. **[QRNG_PHASE_II_SWARM_COHERENCE_PROTOCOL_2026.md](QRNG_PHASE_II_SWARM_COHERENCE_PROTOCOL_2026.md)** — Phase II direction: dose-response, agent count, coherence, threshold (after 100k–1M–5M–10M).
4. **[CODEX_QRNG_PHASE_II_EXPERIMENT_BRIEF.md](CODEX_QRNG_PHASE_II_EXPERIMENT_BRIEF.md)** — Full brief for implementing the Phase II experiment (concrete protocol, coherence metric, runbook). Use this when the user asks Codex to “do the new experiment design.”

---

## What to do next (depending on ask)

- **“Run the remaining ladder”** → Run `./scripts/run_qrng_experiments.sh remaining` from TOE; then read new `artifacts/*_summary.json` and interpret 100k + 1M + 5M + 10M.
- **“Design/implement Phase II”** → Follow [CODEX_QRNG_PHASE_II_EXPERIMENT_BRIEF.md](CODEX_QRNG_PHASE_II_EXPERIMENT_BRIEF.md): agent-count ladder (0,1,10,100,1k), operational coherence metric, pre-registered model comparison, runbook. Start at 100k bits for swarm pilots; do not jump to 1M agents.
- **“Help with budget / staging”** → Use [QRNG_STAGED_PROGRAM_AND_BUDGET_2026.md](QRNG_STAGED_PROGRAM_AND_BUDGET_2026.md); do not spend 50M/100M unless 10M gives a reason.

---

## Rules

- **API key:** Only in local file `artifacts/.anu_api_key`. Never request or echo the key in chat.
- **Method:** Same collector and protocol as March 2026; no new script that replaces it. Phase II adds conditions/metadata on top.
- **Stage gates:** Finish 1M/5M/10M (Stage A), then evaluate (Stage B), then decide branch (Stage C). No auto-escalation to 50M/100M.

---

*Handoff for Codex. Last updated: 2026-03-15.*
