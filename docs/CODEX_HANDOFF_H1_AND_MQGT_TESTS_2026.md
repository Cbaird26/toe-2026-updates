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
  scripts/h1_qrng_pilot/placebo_batch.py
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

---

## 5. Report-back template (for Codex → human)

```
TOE test suite: PASS | FAIL
Commit: <git rev-parse --short HEAD>
Python: <python3 --version>
Failed step: <name>
stderr: <paste>
```

---

**Frozen:** March 2026. Update this handoff if script paths or dependencies change.
