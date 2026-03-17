# Codex brief: Implement the new QRNG Phase II experiment (dose-response / swarm-coherence)

**Goal:** Design and specify (and, where possible, implement) the **new** QRNG experiment so it can actually happen. The user has API keys and will provide them via the existing local-file method. No key in chat.

**Christopher Michael Baird | March 2026**

---

## 1. What we want

Phase I tested **single intervention vs control** (one condition at a time). The **new experiment** tests:

- **Dose-response / threshold:** Does effect size depend on **number of agents** and **coherence**?
- **Hypothesis A (additive):** Δp ∝ N for small N.
- **Hypothesis B (threshold):** Effect ≈ 0 for C < C_crit; effect > 0 for C ≥ C_crit.

We need this new design fully specified and, where feasible, implemented so the user (or an agent with terminal access) can run it.

---

## 2. What’s already in place (TOE repo)

| Item | Path / note |
|------|----------------|
| **TOE repo** | `~/Downloads/TOE` |
| **Phase II conceptual protocol** | [docs/QRNG_PHASE_II_SWARM_COHERENCE_PROTOCOL_2026.md](QRNG_PHASE_II_SWARM_COHERENCE_PROTOCOL_2026.md) — variables, hypotheses A/B, design direction, order of operations |
| **Method (do not change)** | [docs/QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md](QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md) — script names, protocol, key resolution |
| **Trace map & ladder** | [docs/PHASE_I_QRNG_TRACE_MAP_2026.md](PHASE_I_QRNG_TRACE_MAP_2026.md) — 100k first, then 1M → 5M → 10M; decision rules |
| **Pipeline & cost** | [docs/ANU_QRNG_INTERVENTION_PIPELINE.md](ANU_QRNG_INTERVENTION_PIPELINE.md) — cost table, artifacts schema |
| **Bit collector** | `scripts/anu_qrng_collect.py` — `--n`, `--out`, `--label`; reads key from `artifacts/.anu_api_key` or env `ANU_QRNG_API_KEY` |
| **Runner (ladder)** | `scripts/run_qrng_experiments.sh` — `baseline | 1M | 5M | 10M | ladder` |
| **Artifacts** | `artifacts/` (gitignored); key file: `artifacts/.anu_api_key` |

**Order already agreed:** (1) One new 100k baseline. (2) Bit-count ladder 1M → 5M → 10M when ready. (3) Then Phase II swarm-coherence: agent-count ladder (0, 1, 10, 100, 1k first), coherence metric, pre-registered models.

---

## 3. API key — no paste in chat

- The user **has** ANU QRNG API keys (paid and free).
- Keys are stored **only in local files**; never paste keys in chat.
- **Key location for runs from TOE repo:** `TOE/artifacts/.anu_api_key`. The user can copy from `~/Desktop/TOE_Corpus_2026/artifacts/.anu_api_key` or create `TOE/artifacts/.anu_api_key` and paste the key there once (outside chat).
- The collector resolves key in this order: `--api-key` → env `ANU_QRNG_API_KEY` → `artifacts/.anu_api_key`.
- If Codex runs the collector, ensure the run uses the repo root as cwd so `artifacts/.anu_api_key` is found (or set `ANU_QRNG_API_KEY` from a secure source). Do not ask the user to paste the key.

---

## 4. What Codex should deliver

1. **Concrete Phase II protocol**
   - Agent-count rungs: 0 (sham), 1, 10, 100, 1k (and optionally 10k+ later), with fixed QRNG N per rung.
   - **Coherence metric:** Operational definition (e.g. C = w₁(timing synchrony) + w₂(target agreement) + w₃(state stability) + w₄(inter-agent coupling)) and how to measure it per run.
   - Duration / exposure per condition (e.g. 1 s, 1 min, 10 min).
   - Target type (e.g. block means, entropy, autocorrelation) and how it maps to analysis.

2. **Analysis plan (pre-registration-ready)**
   - Models to compare: null, linear (Δp ∝ N), logistic threshold, phase-transition step (or equivalent).
   - Exact comparison (e.g. AIC/BIC or Bayes factors), and how QRNG output (e.g. block means, p_hat) is turned into effect size for each model.

3. **Runbook / scripts (if feasible)**
   - How to run each agent-count condition (e.g. “N=1” = single intervention block, “N=10” = 10 coordinated agents, etc.) and how that integrates with the existing `anu_qrng_collect.py` (same method) or with a thin wrapper that preserves method constancy.
   - If Phase II needs new scripts (e.g. for “N agents” or coherence logging), they should live under `TOE/scripts/` and be documented in the method doc as an extension, without replacing the March 2026 collector.

4. **Bit-count runs (100k, 1M, 5M, 10M)**
   - If Codex has working terminal access: run the test `cd ~/Downloads/TOE && /bin/echo cursor-ok && pwd && python3 --version`; if output appears, run the baseline then ladder using `scripts/anu_qrng_collect.py` or `run_qrng_experiments.sh` from TOE (with key in `artifacts/.anu_api_key`).
   - If no terminal output: produce a single “run script” or list of commands the user can execute to get 100k, 1M, 5M, 10M data so Phase II has inputs.

---

## 5. Constraints

- **Method constancy:** The March 2026 collection method (single ANU API, no fallback, same script and protocol) is fixed. Phase II adds agent-count and coherence layers on top; it does not replace the collector.
- **Coherence before scale:** Do not jump to 1M agents. Test 1, 10, 100, 1k with a defined coherence metric first.
- **No key in chat:** All key handling via local file or env; user will ensure `artifacts/.anu_api_key` exists where runs execute.

---

## 6. Repo layout (quick ref)

```
TOE/
├── docs/
│   ├── QRNG_PHASE_II_SWARM_COHERENCE_PROTOCOL_2026.md   # Conceptual protocol
│   ├── QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md          # Method lock
│   ├── PHASE_I_QRNG_TRACE_MAP_2026.md                  # Ladder, order of ops
│   ├── ANU_QRNG_INTERVENTION_PIPELINE.md               # Cost, schema
│   └── CODEX_QRNG_PHASE_II_EXPERIMENT_BRIEF.md         # This file
├── scripts/
│   ├── anu_qrng_collect.py   # ANU bit collection (--n, --out, --label)
│   └── run_qrng_experiments.sh  # baseline | 1M | 5M | 10M | ladder
└── artifacts/                 # gitignored; .anu_api_key here
```

---

## 7. One-line ask for Codex

**“Using the TOE repo and [QRNG_PHASE_II_SWARM_COHERENCE_PROTOCOL_2026.md](QRNG_PHASE_II_SWARM_COHERENCE_PROTOCOL_2026.md), produce the full Phase II experiment design: concrete agent-count ladder (0,1,10,100,1k), operational coherence metric, pre-registered model comparison (null/linear/threshold), and a runbook or scripts so the new experiment can be run. API keys are provided locally via `artifacts/.anu_api_key`; do not ask for or use keys in chat. If your terminal works, run the 100k baseline and 1M/5M/10M ladder from TOE; otherwise give the user the exact commands to run.”**

---

*Last updated: 2026-03-15. User has API keys; provide everything needed for the new experiment to happen.*
