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
| 3 (seed 456) † | 0.4993 | 0.4997 | +0.00045 | 0.52 |
| **Pooled (60 blocks)** † | 0.4995 | 0.5002 | **+0.00069** | **0.09** |

† Corrected 14 October 2026 — see the Erratum at the end of this report. The values first published here for run 3 (0.5004 / 0.4997 / −0.00064 / 0.28) and for the pool (+0.00033 / 0.41) did not match the raw run files.

---

## Interpretation

- **Pooled difference:** Δ ≈ 6.9×10⁻⁴ (corrected; see Erratum)
- **Permutation p:** 0.09 (10,000 permutations; not significant at α = 0.05, and far from the α = 0.01 promotion threshold used in GATE-03)
- **Conclusion:** Data are consistent with the null hypothesis. No statistically significant difference between control and intervention blocks.
- **Per-run pattern:** intervention was slightly above control in all three runs (+0.0009, +0.0007, +0.0004); none is individually significant, and a 7×10⁻⁴ pooled shift is well inside the ~3×10⁻⁴ per-block binomial noise of this design.

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

## Method (do not change)

The exact process and scripts used for this experiment are documented in [QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md](QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md). Replication and any further ladder runs must use the same method.

## Erratum (14 October 2026): run-3 row and pooled values corrected

The run-3 row and the pooled row of the results table were wrong in the version of this report published in March 2026. They read: run 3 — control 0.5004, intervention 0.4997, I − C = −0.00064, p = 0.28; pooled — +0.00033, p = 0.41. Runs 1 and 2 were correct.

**Evidence.** The raw block file for run 3, `qrng_experiment_20260314_010459_ccb8f429_blocks.json` (SHA-256 `2e985fee7ae2a605cabfc57a9ae2c9b6034537c0df2267bacc9c01cdfb1a8729`), carries the analysis written by `anu_qrng_experiment.py --analyze-blocks` the same night (`analyzed_at` 2026-03-14T05:15:32Z): control mean 0.499293, intervention mean 0.499740, difference +0.000447, permutation p 0.522 over 10 control and 10 intervention blocks. Recomputing the means from the 20 per-block values gives the same numbers. No artifact from the 13–14 March sessions contains a control mean of 0.5004 or a difference of −0.00064; the published row has no source in the data and is treated as a transcription error. With the correct run 3, the 60-block pool gives I − C = +0.000693 and permutation p = 0.091 (GATE-03 analyzer, 10,000 permutations, deterministic seed), reproducing the July 2026 re-analysis in [mqgt-gate03-external-reproduction](https://github.com/Cbaird26/mqgt-gate03-external-reproduction) exactly. The three raw run files are now published there under `data/formal_runs_2026-03-14/` with their hashes.

**What changes and what does not.** The conclusion is unchanged: no significant difference between intervention and control. The pooled p moves from 0.41 to 0.09, so the null result is less emphatic than first stated, and the "run-3 sign flip" remark above was an artefact of the wrong row — all three runs in fact have intervention marginally above control. Documents that quoted the pooled p = 0.41 (`PHASE_I_RESULTS_SUMMARY_2026.md`, `PHASE_I_QRNG_TRACE_MAP_2026.md`, `CODEX_HANDOFF_QRNG.md`, `CLAIM_LEDGER_2026.md`) were updated on the same date with a correction marker. Status: resolved.

## Related

- [REPLICATION_LADDER.md](REPLICATION_LADDER.md) — QRNG pre-registration template
- [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md) — E-labeling, falsification criteria
- [CONSTRAINT_MAP_100.md](CONSTRAINT_MAP_100.md) — ruled out vs. still open

---

*Science means reporting the data, not the wish.*
