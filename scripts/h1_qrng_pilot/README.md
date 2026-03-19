# H1 QRNG bound-setting pilot — collector & analysis

Implements a **preregistered-shaped** pipeline for [docs/H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md](../../docs/H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md):

- Append **raw** `uint32` blocks + **SHA-256** over the raw byte stream (audit trail).
- Fixed **bit extraction rule** (`lsb_v1`: \(X_i = u_i \bmod 2\)) — swap before data collection if you preregister a different rule.
- **Burn-in** (excluded) + **train / holdout** split on the primary stream (index-based, deterministic).
- **`sim` / `urandom`**: pipeline hardening & placebo controls (not physical QRNG evidence).
- **`anu`**: optional live stream from ANU Quantum Numbers (**requires** `ANU_API_KEY` in environment). Rate limits apply; use for shakedown, not silent 10⁹ without planning.

## Dependencies

```bash
pip install numpy h5py
```

`anu` mode uses stdlib `urllib.request` only (no extra HTTP package).

## Collect

```bash
# 1M-bit shakedown, simulated crypto bytes (default extraction lsb_v1)
python scripts/h1_qrng_pilot/collect.py --mode urandom --target-bits 1000000 --out artifacts/h1_pilot/shake1.h5

# Smaller test
python scripts/h1_qrng_pilot/collect.py --mode urandom --target-bits 100000 --out /tmp/h1_small.h5

# ANU (export ANU_API_KEY first)
python scripts/h1_qrng_pilot/collect.py --mode anu --target-bits 50000 --out artifacts/h1_pilot/anu_shake.h5
```

Outputs under `artifacts/` are **gitignored** by the main TOE `.gitignore` (`artifacts/`). Keep exports on disk or Zenodo separately.

## Analyze

```bash
python scripts/h1_qrng_pilot/analyze.py artifacts/h1_pilot/shake1.h5 --burnin-bits 0 --holdout-fraction 0.2
```

Prints \(\hat p\), \(\hat\delta\), SE, Wilson interval, descriptive \(z\), and **holdout** stats. Optional **permutation** stress:

```bash
python scripts/h1_qrng_pilot/analyze.py run.h5 --permutations 2000 --seed 0
```

## What this is not

Lattice / FastAPI demos remain **illustration only** per H1 §5.4. Claims about hardware bias require **your** preregistered device model, raw logs, and the adversarial battery in the doc.

## See also

- H2 (primary blade): [docs/H2_PILOT_PREREGISTRATION_2026.md](../../docs/H2_PILOT_PREREGISTRATION_2026.md) · [docs/H2_PILOT_RUNBOOK.md](../../docs/H2_PILOT_RUNBOOK.md)
