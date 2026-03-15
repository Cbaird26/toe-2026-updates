# QRNG Meditation Intervention Experiment Report

**March 2026 | Christopher Michael Baird | Baird–ZoraASI Collaboration**

---

## Summary

Three independent runs of a block-randomized QRNG meditation intervention experiment. Total bits: 6,000,000. Result: **Failure to Reject Null Hypothesis**. No detectable meditation effect on quantum randomness under this protocol.

---

## Protocol

- **Block design:** 20 blocks × 100,000 bits = 2,000,000 bits per run
- **Conditions:** Control vs. intervention (meditation during collection)
- **Block order:** Randomized (seeds 42, 123, 456)
- **API:** ANU Quantum Random Numbers; single endpoint; no fallback
- **Analysis:** Permutation test on block means (10k permutations)

---

## Results

| Run | Control mean P(1) | Intervention mean P(1) | Difference (I − C) | Permutation p |
|-----|-------------------|------------------------|--------------------|---------------|
| 1 (seed 42)  | 0.4997 | 0.5006 | +0.00094 | 0.17 |
| 2 (seed 123) | 0.4996 | 0.5003 | +0.00069 | 0.37 |
| 3 (seed 456) | 0.5004 | 0.4997 | −0.00064 | 0.28 |
| **Pooled (60 blocks)** | 0.4997 | 0.5000 | **+0.00033** | **0.41** |

---

## Interpretation

- **Pooled difference:** Δ ≈ 3.3×10⁻⁴
- **Permutation p:** 0.41
- **Conclusion:** Data are consistent with the null hypothesis. No statistically significant difference between control and intervention blocks.
- **Run 3 sign flip:** Intervention < control in run 3; expected under randomness when no real effect exists.

---

## Pipeline Validation

- QRNG acquisition: working
- Block randomization: working
- Statistical diagnostics: bias, runs, entropy, autocorrelation—all within expected ranges
- Replication: three independent runs completed

---

## Sensitivity

- **Achieved:** ~3×10⁻⁴ bias scale
- **For smaller effects:** Larger datasets (10⁷–10⁹ bits) required

---

## Artifacts

- `artifacts/qrng_experiment_*_blocks.json` — block summaries with embedded comparison
- `artifacts/qrng_experiment_*_report.json` — full diagnostics
- `artifacts/qrng_experiment_*_plots.png` — visualizations

---

## Related

- [REPLICATION_LADDER.md](REPLICATION_LADDER.md) — QRNG pre-registration template
- [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md) — E-labeling, falsification criteria
- [CONSTRAINT_MAP_100.md](CONSTRAINT_MAP_100.md) — ruled out vs. still open

---

*Science means reporting the data, not the wish.*
