# QRNG Phase II Experiment Design 2026

**Concrete protocol for the swarm-coherence / dose-response experiment.**  
Christopher Michael Baird | Baird–ZoraASI Collaboration | March 2026

---

## 1. Purpose

Phase I asked whether a single intervention changed QRNG output. Phase II asks a different question:

**Does QRNG effect size scale with coordinated agent count and measured coherence, and is that scaling additive or threshold-like?**

This document turns the conceptual sketch in [QRNG_PHASE_II_SWARM_COHERENCE_PROTOCOL_2026.md](QRNG_PHASE_II_SWARM_COHERENCE_PROTOCOL_2026.md) into an executable protocol, analysis plan, and runbook.

---

## 2. Locked constraints from Phase I

- **Collector method stays fixed:** use `scripts/anu_qrng_collect.py` exactly as documented in [QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md](QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md).
- **Key handling stays local:** use `artifacts/.anu_api_key` or `ANU_QRNG_API_KEY`; never paste a key in chat.
- **Formal runs use preflight and no fallback:** run with `--preflight --no-fallback` so the endpoint and auth path stay constant.
- **Phase I ladder comes first:** one new 100k baseline, then 1M → 5M → 10M baseline ladder when ready. Phase II is a new line layered on top of the same collector.

---

## 3. Primary Phase II design

### 3.1 Conditions

**Agent-count ladder (primary):**

| Rung | Agent count | Label |
|------|-------------|-------|
| 0 | 0 | sham / no intervention |
| 1 | 1 | single-agent |
| 2 | 10 | small swarm |
| 3 | 100 | medium swarm |
| 4 | 1000 | large swarm |

### 3.2 Fixed collection size

- **Bits per session:** `1,000,000`
- **Block size for analysis:** `100,000`
- **Blocks per session:** `10`
- **Primary confirmatory plan:** `3` independent sessions per rung
- **Total confirmatory load:** `15 sessions = 15,000,000 bits`

This keeps the bit count fixed across rungs so the manipulated variable is the intervention condition, not QRNG sample size.

### 3.3 Duration / exposure

- **Exposure window per 1M session:** `300 s` target window
- **Warm-up before collection:** `60 s`
- **Coherence check cadence during session:** every `30 s`

If the ANU collection for 1M bits runs slightly longer than 300 s, maintain the intervention state until collection completes and record the actual duration in metadata.

### 3.4 Target definition

- **Primary target:** increase the proportion of `1` bits (`P(1) > 0.5`)
- **Primary effect size:** `delta_p = p1 - 0.5`
- **Secondary outcomes:** `z_score`, `theta_hat`, block means across 100k-bit blocks, and optional entropy / runs / autocorrelation diagnostics if available

The target is fixed before data collection. Changing the target definition creates a different experiment.

---

## 4. Operational coherence metric

Phase II needs a measured coherence scalar, not a narrative claim. For each session, score four components on `[0, 1]` and combine them into a preregistered composite:

`C = 0.35*T + 0.25*A + 0.25*S + 0.15*K`

Where:

| Symbol | Component | How to score |
|--------|-----------|--------------|
| `T` | Timing synchrony | Fraction of agents entering the target state within `±5 s` of the scheduled start, clipped to `[0,1]` |
| `A` | Target agreement | Fraction of agents affirming the same preregistered target statement (`"more_ones"`) before collection |
| `S` | State stability | Mean fraction of check-ins during the session that remain in the declared target state |
| `K` | Inter-agent coupling | Fraction of agents participating in the planned coordination graph during the warm-up and session heartbeat windows |

### 4.1 Practical scoring rules

- **Human sessions:** score from attendance sheet + synchronized countdown + scheduled check-ins.
- **Agent sessions:** score from heartbeat logs or coordinator acknowledgements.
- **Sham (`N=0`) sessions:** set `T=A=S=K=0`, `C=0`.
- **No post hoc editing:** coherence scores are logged before reading QRNG results.

### 4.2 Effective dose

For the initial model comparison, collapse agent count and coherence into one preregistered scalar:

`D = N_agents * C`

This is the **effective-agents dose**. With only five rungs, `D` is the most stable one-dimensional predictor. Separate `N` and `C` interaction models can be added only after the design has more sessions.

---

## 5. Session structure

For every session:

1. Record session metadata: rung, replicate index, target, planned duration, and the four coherence components.
2. Run a `--preflight --no-fallback` check against the ANU API.
3. Start the intervention window.
4. Collect `1,000,000` bits with `scripts/anu_qrng_collect.py`.
5. Lock metadata and append the session to the Phase II manifest.
6. Repeat until all rungs and replicates are complete.

### 5.1 Order randomization

- Randomize session order within each replicate round.
- Do not run all low-dose conditions first and high-dose conditions last.
- Keep the randomization seed or generated order in the manifest file.

### 5.2 Minimum replication

- **Discovery pass:** 1 session per rung (`5M` total)
- **Confirmatory pass:** 3 sessions per rung (`15M` total) and use this for preregistered model comparison

If logistics force a discovery-only pass first, do not treat that as confirmatory evidence.

---

## 6. Pre-registered analysis plan

### 6.1 Unit of analysis

Each session contributes one primary data point:

- `y = delta_p = p1 - 0.5`
- `se = 0.5 / sqrt(n_bits)`
- `x = D = N_agents * C`

The summary JSON produced by `anu_qrng_collect.py` already contains `p1`, `z_score`, `theta_hat`, and `n`.

### 6.2 Models to compare

Fit and compare these models on the confirmatory dataset:

1. **Null:** `y = beta0`
2. **Linear dose:** `y = beta0 + beta1 * D`
3. **Step threshold:** `y = beta0 + A * I(D >= tau)`
4. **Logistic threshold:** `y = beta0 + A / (1 + exp(-(D - tau)/s))`

### 6.3 Estimation and ranking

- Fit models by **weighted least squares** using `1 / se^2`
- Rank models by **AICc** (primary) and **BIC** (secondary)
- Treat models with `delta_AICc <= 2` as practically indistinguishable

### 6.4 Interpretation rule

Classify the result as follows:

- **No support:** null is best, or no non-null model beats null by `delta_AICc >= 4`
- **Additive candidate:** linear is best, `beta1 > 0`, and linear beats null by `delta_AICc >= 4`
- **Threshold candidate:** step or logistic is best, amplitude `A > 0`, and best threshold model beats both null and linear by `delta_AICc >= 4`

This is a model-selection rule, not proof of mechanism. Any claim stronger than that requires external replication.

### 6.5 Secondary summaries

- Mean `delta_p` by rung
- Mean `z_score` by rung
- Coherence-by-rung summary (`T`, `A`, `S`, `K`, `C`)
- Optional block-level means if the bitstreams are segmented into 100k-bit blocks after collection

---

## 7. Recommended run order

### 7.1 Before Phase II

1. Fresh 100k baseline
2. Baseline ladder: 1M → 5M → 10M
3. Confirm the collector, billing, and artifact paths are stable

### 7.2 Phase II discovery

1. One 1M session at each rung: `0, 1, 10, 100, 1000`
2. Review logistics only: manifest completeness, coherence scoring consistency, artifact naming
3. Do not update the model definitions after seeing discovery results

### 7.3 Phase II confirmatory

1. Three 1M sessions per rung
2. Randomize order within each replicate round
3. Run the preregistered comparison exactly once after all confirmatory sessions are complete

---

## 8. Runbook

### 8.1 Baseline ladder commands

```bash
cd ~/Downloads/TOE
python3 scripts/anu_qrng_collect.py --preflight-only --out artifacts
python3 scripts/anu_qrng_collect.py --n 100000 --out artifacts --label baseline --preflight --no-fallback
python3 scripts/anu_qrng_collect.py --n 1000000 --out artifacts --label ladder_1M --preflight --no-fallback
python3 scripts/anu_qrng_collect.py --n 5000000 --out artifacts --label ladder_5M --preflight --no-fallback
python3 scripts/anu_qrng_collect.py --n 10000000 --out artifacts --label ladder_10M --preflight --no-fallback
```

### 8.2 Generate a Phase II manifest template

```bash
cd ~/Downloads/TOE
python3 scripts/qrng_phase2_run.py plan --out artifacts --bits 1000000 --replicates 3
```

### 8.3 Run one Phase II session

```bash
cd ~/Downloads/TOE
python3 scripts/qrng_phase2_run.py run \
  --agents 100 \
  --replicate 1 \
  --timing 0.86 \
  --agreement 1.00 \
  --stability 0.74 \
  --coupling 0.68 \
  --duration-sec 300 \
  --target more_ones \
  --bits 1000000 \
  --out artifacts
```

That wrapper records the coherence metadata and then calls `anu_qrng_collect.py` without changing the collector method.

### 8.4 Compare models after confirmatory collection

```bash
cd ~/Downloads/TOE
python3 scripts/qrng_phase2_model_compare.py artifacts/phase2_sessions.csv
```

---

## 9. Artifact expectations

Per session, keep:

- QRNG summary JSON from `anu_qrng_collect.py`
- Raw bit CSV from `anu_qrng_collect.py`
- Phase II metadata JSON
- `phase2_sessions.csv` manifest row with `N`, `C`, `D`, and summary statistics

All of these should remain under `artifacts/` so key handling and output locality remain consistent with the existing repo.

---

## 10. What would count as a useful Phase II result

- **Strong null:** null model remains best across the confirmatory ladder
- **Linear hint:** positive best-fit linear dose with clear AICc separation from null
- **Threshold hint:** step/logistic model wins and the estimated threshold falls between observed rungs, not below sham or above the maximum tested dose

Any apparent signal should then be repeated at the winning rung and one neighboring rung before making a substantive claim.

---

## 11. Links

- [QRNG_PHASE_II_SWARM_COHERENCE_PROTOCOL_2026.md](QRNG_PHASE_II_SWARM_COHERENCE_PROTOCOL_2026.md) — conceptual origin
- [QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md](QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md) — locked collection method
- [PHASE_I_QRNG_TRACE_MAP_2026.md](PHASE_I_QRNG_TRACE_MAP_2026.md) — ladder order and decision rules

---

*Executable Phase II design. Last updated: 2026-03-15.*
