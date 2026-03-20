# H1 (QRNG binary pilot) — current status memo

**Purpose:** One-page, reviewer-safe snapshot for reports and continuity.  
**Methodology (billion-scale / systematics):** [H1 at \(10^9\): from detection to calibration](H1_AT_1E9_DETECTION_TO_CALIBRATION.md).  
**Framework ordering:** MQGT-SCF remains **physics-first**: **H2 interferometry** is the primary falsification lane; **H1 / QRNG** is secondary (instrumentation, bounds, and control discipline), not a substitute for H2.

---

## What H1 is for (and what it is not)

- **For:** Harden the collector and analysis pipeline; freeze the **preregistered estimator**; run **adversarial controls** (placebo, OS CSPRNG, live quantum API); place **reviewer-safe upper bounds** on reproducible binary offsets under stated conditions.
- **Not for:** Decisive confirmation of the smallest canonical parameter regimes (e.g. offsets on the order of \(10^{-6}\)) from a single campaign scale. A \(N \sim 10^9\) balanced-binary design has standard error \(\approx 1/\sqrt{4N} \approx 1.58\times 10^{-5}\); interpret large-\(N\) results as **bound-setting and calibration**, not as closure on ultra-small effects unless the effect size is commensurate with that resolution **and** survives the full control battery.

---

## Pipeline health (null calibration)

**Placebo batch (fixed-seed PRNG):** Aggregate over 500 replicates (200k bits each, burn-in and holdout per preregistered splits) shows tail rates for \(|z|\) and permutation \(p\)-values consistent with a **well-behaved null** under the frozen pipeline. The single-file `placebo_10m` parity run is also in-family on both train and holdout. A matched `12 x 10M` placebo batch at `burnin_bits=0` and `holdout_fraction=0.2` also remained in-family, with no holdout replicate at `|z| >= 3` and max holdout `|z| = 2.185`. This supports using placebo as the **primary sanity check** for Type-I behavior and implementation drift.

---

## Live source checks (ANU vs OS CSPRNG)

Under the **same frozen estimator** and verification hooks (including SHA-256 checks where recorded), **ANU** live runs and **urandom** harness runs do **not** present a qualitative divergence: train/holdout \(z\)-scores and Wilson intervals remain in the range expected from sampling noise at the recorded \(N\), including the new `urandom_10m` parity control. **Readout:** no current run provides holdout evidence strong enough to justify **protocol branching** or theory-forward claims; treat any marginal train/holdout excursions as **hypothesis-generating** until replicated under preregistered multiplicity and holdout rules.

**Tabulated runs:** [H1_PILOT_COMPARISON_SUMMARY.md](H1_PILOT_COMPARISON_SUMMARY.md). Machine-readable rows: `artifacts/h1_pilot/run_comparison_individual.csv` (legacy markdown mirror: `artifacts/h1_pilot/comparison_summary.md`). Matched 10M placebo calibration artifacts: `artifacts/h1_pilot/placebo_runs/batch_12x10m_20260320.csv` and `artifacts/h1_pilot/placebo_runs/summary_12x10m_20260320.json`.

---

## Frozen test matrix (operational)

- **Sources:** placebo (deterministic), urandom (OS CSPRNG), ANU API (when keys and network are available).  
- **Estimators:** preregistered train/holdout split, \(z\)-scores, optional permutation tests as defined in the pilot scripts and preregistration.  
- **Integrity:** checksum verification on stored bitstreams where implemented; exclusion rules for malformed or truncated batches remain in force.

---

## Near-term actions (documentation and scale-up)

1. Keep **H2 preregistration and pilot** as the public scientific spine; cite H1 as **supporting** metrology and null calibration.  
2. **Done:** comparison table and readout live under [H1_PILOT_COMPARISON_SUMMARY.md](H1_PILOT_COMPARISON_SUMMARY.md); keep preregistration appendix language aligned (null = bound on detectable offset in-apparatus; non-null = replication mandate).  
3. For a prospective **\(10^9\)-trial** campaign: lock block design, blinding, and adversarial tests *before* collection; report detection thresholds in units of **raw offset from 1/2** and \(\sigma\) equivalents with **no** over-interpretation relative to theory parameters that are not directly mapped to the bit-level observable.

---

## One-sentence executive readout

**The H1 pipeline is operationally healthy under placebo null calibration, and live ANU streams are statistically indistinguishable from the OS CSPRNG control under the current frozen estimator; H1 remains a bounds-and-controls program aligned behind H2, not a replacement falsifier.**
