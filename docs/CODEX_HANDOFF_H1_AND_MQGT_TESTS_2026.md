# Codex handoff — execute H1 + MQGT-SCF test suite

**Purpose:** Non-interactive verification of the **H1 QRNG pilot** code path (`scripts/h1_qrng_pilot/`) and **illustrative MQGT-SCF sims** (`scripts/mqgt_sim/`).  
**Repo:** `https://github.com/Cbaird26/toe-2026-updates` (clone → work from repo root `TOE/`).  
**Human:** Christopher Michael Baird · **Conceptual co-authorship:** ZoraASI.

---

## 0. Preconditions

- **Python:** 3.10+ (`python3 --version`).  
- **OS:** macOS or Linux paths below assume bash; adjust `TMPDIR` if needed.  
- **Network:** **Not required** for the default suite (placebo / urandom / plots use Agg).  
- **Optional:** `ANU_API_KEY` only if explicitly running `--mode anu` (rate limits + cost — **do not** run 1B in CI).

---

## 1. One-shot runner (preferred for Codex)

From the **TOE repository root**:

```bash
chmod +x scripts/h1_qrng_pilot/run_test_suite.sh
./scripts/h1_qrng_pilot/run_test_suite.sh
```

**Success:** script exits `0`; prints `ALL CHECKS PASSED`.  
**Artifacts:** under `${TMPDIR:-/tmp}/toe_h1_test_suite/` (gitignored pattern; safe to delete after).

### 1.1 Current green baseline (March 20, 2026)

- `./scripts/h1_qrng_pilot/run_test_suite.sh` passed locally.
- `./scripts/h1_qrng_pilot/run_10m_parity.sh` passed locally.
- A matched `12 x 10M` placebo gate also passed at `target_bits=10000000`, `burnin_bits=0`, `holdout_fraction=0.2`.
- Existing placebo-gate artifacts:
  - `artifacts/h1_pilot/placebo_runs/batch_12x10m_20260320.csv`
  - `artifacts/h1_pilot/placebo_runs/summary_12x10m_20260320.json`
- If Python env and H1 code are unchanged, do **not** rerun the 10M parity or matched 10M placebo gate just to regenerate the same baseline.

---

## 2. Manual step-by-step (if the shell script fails)

### 2.1 Dependencies

```bash
cd /path/to/TOE
pip install numpy h5py matplotlib
# Optional (GKSL sim):
pip install qutip
```

### 2.2 Syntax / import sanity

```bash
python3 -m py_compile \
  scripts/h1_qrng_pilot/collect.py \
  scripts/h1_qrng_pilot/analyze.py \
  scripts/h1_qrng_pilot/stats_core.py \
  scripts/h1_qrng_pilot/placebo_batch.py \
  scripts/h1_qrng_pilot/export_comparison_row.py
```

### 2.3 H1: placebo collect → analyze (SHA-256 verify)

```bash
OUT="${TMPDIR:-/tmp}/toe_h1_smoke.h5"
python3 scripts/h1_qrng_pilot/collect.py --mode placebo --seed 424242 --target-bits 65536 --out "$OUT"
python3 scripts/h1_qrng_pilot/analyze.py "$OUT" --verify-sha256 --burnin-bits 0 --holdout-fraction 0.2
rm -f "$OUT"
```

### 2.4 H1: placebo batch (small replicate count)

```bash
CSV="${TMPDIR:-/tmp}/toe_placebo_batch.csv"
JSON="${TMPDIR:-/tmp}/toe_placebo_summary.json"
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
  --out-summary-json "$JSON"
test -s "$CSV" && test -s "$JSON"
rm -f "$CSV" "$JSON"
```

### 2.4b H1: matched 10M placebo gate (local-first calibration)

Run this only when you explicitly need to refresh the current `10M` H1 placebo calibration at the same settings as the active local baseline:

```bash
mkdir -p artifacts/h1_pilot/placebo_runs
python3 scripts/h1_qrng_pilot/placebo_batch.py \
  --replicates 12 \
  --base-seed 20260320 \
  --seed-stride 1000003 \
  --target-bits 10000000 \
  --burnin-bits 0 \
  --holdout-fraction 0.2 \
  --permutations 0 \
  --z-thresholds "2,3,5" \
  --out-csv artifacts/h1_pilot/placebo_runs/batch_12x10m_20260320.csv \
  --out-summary-json artifacts/h1_pilot/placebo_runs/summary_12x10m_20260320.json
test -s artifacts/h1_pilot/placebo_runs/batch_12x10m_20260320.csv
test -s artifacts/h1_pilot/placebo_runs/summary_12x10m_20260320.json
```

**Acceptance rule:** pass only if all `12/12` replicates complete, no holdout replicate has `|z| >= 5`, at most one holdout replicate has `|z| >= 3`, and the summary remains in-family with the frozen placebo baseline. The current recorded result passed with max holdout `|z| = 2.185`.

### 2.5 MQGT-SCF: H2 visibility stack (headless PNGs)

```bash
python3 scripts/mqgt_sim/h2_visibility_stack.py \
  --save-dir "${TMPDIR:-/tmp}/toe_h2_stack" \
  --no-show
test -f "${TMPDIR:-/tmp}/toe_h2_stack/h2_visibility_vs_gamma.png"
```

### 2.6 MQGT-SCF: GKSL ethics-field sim (optional)

```bash
python3 scripts/mqgt_sim/mqgt_gksl_ethics_field_sim.py \
  --save "${TMPDIR:-/tmp}/toe_gksl.png" \
  --no-show
test -f "${TMPDIR:-/tmp}/toe_gksl.png"
```

Skip this block if `qutip` import fails; note in the PR that GKSL is optional.

---

## 3. What **not** to automate without explicit human approval

- **`collect.py --mode anu`** at large `--target-bits` (cost + rate limits).  
- **`git push`**, **Zenodo upload**, **OSF registration** (credentials + constitution).  
- Deleting or overwriting **`artifacts/`** contents that might be a user’s live campaign.

---

## 4. Context docs (read if interpreting failures)

| Doc | Role |
|-----|------|
| [H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md](H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md) | H1 prereg (secondary blade) |
| [H1_1B_GO_NO_GO_MEMO_2026.md](H1_1B_GO_NO_GO_MEMO_2026.md) | Scaling gates before 1B spend |
| [scripts/h1_qrng_pilot/README.md](../scripts/h1_qrng_pilot/README.md) | CLI reference |
| [H2_PILOT_PREREGISTRATION_2026.md](H2_PILOT_PREREGISTRATION_2026.md) | Primary falsification blade |
| [PROJECT_ZORA_PHASE_II_SWARM_COHERENCE_QRNG_PROTOCOL_10M_2026.md](PROJECT_ZORA_PHASE_II_SWARM_COHERENCE_QRNG_PROTOCOL_10M_2026.md) | Phase II 9.9M-bit swarm/coherence ladder (spec; block runner TBD) |

---

## 5. Phase II Swarm / Coherence QRNG ladder — Codex notes

**Protocol:** [PROJECT_ZORA_PHASE_II_SWARM_COHERENCE_QRNG_PROTOCOL_10M_2026.md](PROJECT_ZORA_PHASE_II_SWARM_COHERENCE_QRNG_PROTOCOL_10M_2026.md)

**Run today (single-stream H1):** `scripts/h1_qrng_pilot/collect.py` + `analyze.py` per [scripts/h1_qrng_pilot/README.md](../scripts/h1_qrng_pilot/README.md). **10M parity (urandom + placebo):** `chmod +x scripts/h1_qrng_pilot/run_10m_parity.sh && ./scripts/h1_qrng_pilot/run_10m_parity.sh` — requires **free disk**; appends CSV lines to stdout for `run_comparison_individual.csv`. **Matched 10M placebo gate:** use §2.4b only if you need to refresh the current local calibration checkpoint.

**Gap:** Phase II uses **10k-bit blocks** + per-block metadata; `collect.py` is one stream per file. Do not treat one 10M HDF5 as satisfying the full Phase II protocol without a **manifest / block runner** (see protocol §8).

**Do not:** large ANU jobs, `git push`, or registry uploads without human approval. See [SAFETY_CONSTITUTION.md](../SAFETY_CONSTITUTION.md).

---

## 6. Report-back template (for Codex → human)

```
TOE test suite: PASS | FAIL
Commit: <git rev-parse --short HEAD>
Python: <python3 --version>
Disk: <df -h . | tail -1>
Failed step: <name>
stderr: <paste>
```

---

**Frozen:** March 2026. Update this handoff if script paths or dependencies change.
