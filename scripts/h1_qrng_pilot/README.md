# H1 QRNG bound-setting pilot — collector & analysis

Implements a **preregistered-shaped** pipeline for [docs/H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md](../../docs/H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md):

- Append **raw** `uint32` blocks + **SHA-256** over the raw byte stream (audit trail).
- Fixed **bit extraction rule** (`lsb_v1`): global bit index \(t = 32i + k\) uses \(X_t = (\texttt{raw\_u32}[i] \gg k) \,\&\, 1\) for \(k=0..31\).
- **Burn-in** (excluded) + **train / holdout** split on the primary stream (index-based, deterministic).
- **`urandom`**: OS CSPRNG (pipeline harness; not a physics claim).
- **`placebo`**: **NumPy `Generator` (PCG64)** with a **fixed integer `--seed`** — same HDF5 chunking, datasets, and metadata shape as `urandom` / `anu`; use for **known-null** calibration.
- **`anu`**: optional live stream from ANU Quantum Numbers (**requires** `ANU_API_KEY`). Rate limits apply; plan before scaling toward \(10^9\).

Shared statistics live in `stats_core.py` (used by `analyze.py` and `placebo_batch.py`).

## Dependencies

```bash
pip install numpy h5py
```

`anu` mode uses stdlib `urllib.request` only (no extra HTTP package).

## Collect

```bash
# 1M-bit shakedown, OS cryptographic random
python scripts/h1_qrng_pilot/collect.py --mode urandom --target-bits 1000000 --out artifacts/h1_pilot/shake1.h5

# Known-null stream (reproducible; methodology calibration)
python scripts/h1_qrng_pilot/collect.py --mode placebo --seed 20260319 --target-bits 100000 --out artifacts/h1_pilot/placebo42.h5

# ANU (export ANU_API_KEY first)
python scripts/h1_qrng_pilot/collect.py --mode anu --target-bits 50000 --out artifacts/h1_pilot/anu_shake.h5
```

`--mode placebo` **requires** `--seed`.

Outputs under `artifacts/` are **gitignored** by the main TOE `.gitignore` (`artifacts/`). Keep exports on disk or Zenodo separately.

## Analyze

```bash
python scripts/h1_qrng_pilot/analyze.py artifacts/h1_pilot/shake1.h5 --burnin-bits 0 --holdout-fraction 0.2
```

Prints \(\hat p\), \(\hat\delta\), SE, Wilson interval, descriptive \(z\), and **holdout** stats. Optional **permutation** stress:

```bash
python scripts/h1_qrng_pilot/analyze.py run.h5 --permutations 2000 --seed 0
```

## Placebo batch (null calibration)

**`placebo_batch.py`** runs many independent placebo streams through the **same** in-memory HDF5 writer + **`analyze_raw_u32`** path (no reliance on ANU or disk per replicate). It writes:

1. **Per-replicate CSV** — `train_*` / `hold_*` metrics, `stream_sha256_hex`, optional `perm_p_two_sided` / `perm_obs_delta_train`.
2. **Summary JSON** — empirical \(\Pr(|z_{\text{train}}| \ge t)\) and \(\Pr(|z_{\text{hold}}| \ge t)\) for chosen thresholds, plus (if permutations enabled) the fraction of runs with `perm_p_two_sided < --perm-alpha`.

```bash
mkdir -p artifacts/h1_pilot/placebo_runs

python scripts/h1_qrng_pilot/placebo_batch.py \
  --replicates 500 \
  --base-seed 0 \
  --seed-stride 1000003 \
  --target-bits 200000 \
  --burnin-bits 1000 \
  --holdout-fraction 0.2 \
  --permutations 400 \
  --perm-seed 0 \
  --z-thresholds "2,3,5" \
  --out-csv artifacts/h1_pilot/placebo_runs/batch.csv \
  --out-summary-json artifacts/h1_pilot/placebo_runs/summary.json
```

Interpret hit rates against a **nominal** two-sided Gaussian benchmark only heuristically (exact finite-sample behavior depends on \(N_{\text{train}}\)); the empirical curve is the operational baseline for **your** frozen pipeline.

## What this is not

Lattice / FastAPI demos remain **illustration only** per H1 §5.4. Claims about hardware bias require **your** preregistered device model, raw logs, and the adversarial battery in the doc.

## See also

- H2 (primary blade): [docs/H2_PILOT_PREREGISTRATION_2026.md](../../docs/H2_PILOT_PREREGISTRATION_2026.md) · [docs/H2_PILOT_RUNBOOK.md](../../docs/H2_PILOT_RUNBOOK.md)  
- Campaign discipline: [docs/H1_1B_GO_NO_GO_MEMO_2026.md](../../docs/H1_1B_GO_NO_GO_MEMO_2026.md)  
- **Codex / executor handoff:** [docs/CODEX_HANDOFF_H1_AND_MQGT_TESTS_2026.md](../../docs/CODEX_HANDOFF_H1_AND_MQGT_TESTS_2026.md) · `run_test_suite.sh` (this folder)
