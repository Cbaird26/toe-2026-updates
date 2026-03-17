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
| **ANU QRNG intervention** | TOE_Corpus_2026 (Desktop): `scripts/anu_qrng_collect.py`, etc. | Raw ANU API collection, block-randomized control/intervention, permutation testing |

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
| 5,000,000 | ~611 | ~$3.05 |
| 10,000,000 | 1,221 | $6.11 |
| 100,000,000 | ~12,207 | ~$60 |

**Recommended workflow:** Run `--pilot` (10k bits) first to validate API, logging, and analysis before full run.

**Billing:** API is paid ($0.005/request). Verify credit card or AWS billing before large runs (10M / 50M / 100M).

---

## Graduated ladder and decision rules

**Ladder (recommended order):** 100k (done) → 1M → 5M → 10M for initial runs; 50M/100M when possible (see [NEXT_QRNG_RUN_50M_2026.md](NEXT_QRNG_RUN_50M_2026.md)). See [PHASE_I_QRNG_TRACE_MAP_2026.md](PHASE_I_QRNG_TRACE_MAP_2026.md) for full table (cost, sensitivity, purpose).

- **Advance to next rung if:** pipeline integrity tests pass, RNG baseline tests pass, no API / logging errors.
- **Optionally stop escalation if:** effect size < 10⁻⁴ and p > 0.1 across ≥3 runs.

---

## Scripts (Expected)

| Script | Purpose |
|--------|---------|
| anu_qrng_collect.py | Collect bits from ANU API; supports --bits, --pilot |
| anu_qrng_experiment.py | Block-randomized control/intervention; --analyze, --analyze-blocks |
| qrng_test_suite.py | Bias, runs, entropy, autocorrelation, serial pairs |
| qrng_compare_runs.py | Compare runs; KS test, permutation on block means |

**Location (recovered):** The QRNG collector and pipeline live in **TOE_Corpus_2026 on Desktop**: `~/Desktop/TOE_Corpus_2026`. Scripts: `scripts/anu_qrng_collect.py` (uses `--n`, `--out`, `--label`), plus anu_qrng_experiment.py, qrng_test_suite.py, qrng_compare_runs.py as in the method doc. **Method constancy:** Replication and any further runs must use the same scripts and process; see [QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md](QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md).

**Discovery / Consolidation:**
- **Primary path:** Black-Book `experiments/` (e.g. `experiments/anu_qrng_collect.py`) — target location for consolidation.
- **Alternative:** Dedicated `mqgt-qrng` or `toe-qrng- intervention` repo if ANU track grows.
- **Current state:** Scripts may exist in local ad hoc folders; replicators use toe-empirical-validation E-labeling pipeline for official ladder. For ANU intervention replication, check `experiments/` and ANU_QRNG_INTERVENTION_PIPELINE for latest script locations.

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
