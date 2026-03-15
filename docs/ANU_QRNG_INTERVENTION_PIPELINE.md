# ANU QRNG Intervention Pipeline

**Christopher Michael Baird | Baird–ZoraASI Collaboration | March 2026**

---

## Purpose

Documents the ANU Quantum Random Numbers API–based intervention pipeline: raw collection, block-randomized control/intervention design, permutation testing. This is a **separate track** from the toe-empirical-validation E-labeling pipeline; the two can be bridged for MQGT-SCF constraint analysis.

**Related:** [REPLICATION_LADDER.md](REPLICATION_LADDER.md) | [QRNG_MEDITATION_INTERVENTION_REPORT_MARCH_2026.md](QRNG_MEDITATION_INTERVENTION_REPORT_MARCH_2026.md) | [EXPERIMENTAL_PREDICTIONS_STUB_2026.md](EXPERIMENTAL_PREDICTIONS_STUB_2026.md)

---

## Pipeline vs. toe-empirical-validation

| Pipeline | Location | Purpose |
|----------|----------|---------|
| **toe-empirical-validation** | Cbaird26/toe-empirical-validation | E-labeling, constraint fitting, falsification; `run_all.sh --channel qrng` |
| **ANU QRNG intervention** | (scripts: anu_qrng_collect.py, anu_qrng_experiment.py, qrng_test_suite.py) | Raw ANU API collection, block-randomized control/intervention, permutation testing |

**Bridge option:** Run ANU-collected bits through toe-empirical-validation E-labeling for MQGT-SCF constraint analysis.

1. Export ANU bits to CSV with columns: `block_index`, `condition`, `value` (0/1 per bit, or block-level p_hat).
2. Reshape to blocks of 64 bits (or match `block_size` in `code/qrng_pipeline.py`).
3. Call `label_E(bits)` from `code/e_labeling.py` per block.
4. Feed E values into the constraint pipeline. **Future:** Extend `qrng_pipeline.py` with `--input-csv <path>` to ingest ANU CSV directly; would reshape to blocks and run E-labeling internally. (Not yet implemented; manual bridge for now.)

---

## Cost Model

**Key correction:** 100,000 bits ≠ 100,000 requests. Each request returns 1024 uint8 values = 8192 bits.

| Bits | Requests | Cost (@ $0.005/request) |
|------|----------|-------------------------|
| 10,000 | 2 | $0.01 |
| 100,000 | 13 | $0.07 |
| 1,000,000 | 123 | $0.62 |
| 10,000,000 | 1,221 | $6.11 |
| 100,000,000 | ~12,207 | ~$60 |

**Recommended workflow:** Run `--pilot` (10k bits) first to validate API, logging, and analysis before full run.

---

## Scripts (Expected)

| Script | Purpose |
|--------|---------|
| anu_qrng_collect.py | Collect bits from ANU API; supports --bits, --pilot |
| anu_qrng_experiment.py | Block-randomized control/intervention; --analyze, --analyze-blocks |
| qrng_test_suite.py | Bias, runs, entropy, autocorrelation, serial pairs |
| qrng_compare_runs.py | Compare runs; KS test, permutation on block means |

**Location (March 2026):** ANU-specific scripts (anu_qrng_collect.py, anu_qrng_experiment.py, qrng_test_suite.py, qrng_compare_runs.py) are not yet in Black-Book or cbaird26 repos. March 2026 runs used ad hoc collection; consolidation target: Black-Book `experiments/` or a dedicated `mqgt-qrng` repo. When located, update this section.

---

## Artifacts Schema

- `*_bits.csv` — raw bit stream (session_id, request_index, timestamp_utc, condition, value)
- `*_blocks.json` — block summaries (block_index, condition, n_bits, p_hat, ones, zeros, entropy, runs_z, block_comparison)
- `*_report.json` — full diagnostics (bias_p_value, runs_z_score, autocorrelation, entropy, etc.)
- `*_plots.png` — cumulative deviation, block means, autocorrelation spectrum

---

## Protocol (March 2026 Run)

- 20 blocks × 100k bits = 2M bits per run
- Randomized block order (seeds 42, 123, 456)
- Control vs. intervention (meditation during collection)
- Single API endpoint; no fallback
- Permutation test on block means (10k permutations)

---

## Next Experiments

- **Long baseline stability:** 50M–100M bits; entropy/autocorrelation over time
- **Cross-generator correlation:** ANU + second QRNG source
- **Ultra-large sensitivity:** 100M bits (~$60) for ~10⁻⁴ bias
