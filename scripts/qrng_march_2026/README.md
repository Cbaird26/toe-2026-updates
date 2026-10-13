# QRNG scripts — March 2026 method (canonical copies)

Byte-for-byte copies of the four scripts that produced the March 13–14, 2026 QRNG result (6M bits, 3 runs, seeds 42/123/456), taken from `TOE_Corpus_2026` at commit `21fc9a7` on 2026-10-13. They are committed here so the frozen method no longer depends on a Desktop folder or on session logs.

| Script | Purpose |
|--------|---------|
| `anu_qrng_collect.py` | Collect bits from the ANU API (`--n`, `--out`, `--label`; key from `--api-key`, `ANU_QRNG_API_KEY`, or `artifacts/.anu_api_key`) |
| `anu_qrng_experiment.py` | Block-randomized control/intervention runs; `--analyze`, `--analyze-blocks` |
| `qrng_test_suite.py` | Bias, runs, entropy, autocorrelation, block frequency, serial pairs |
| `qrng_compare_runs.py` | Cross-run comparison; KS test, permutation on block means |

Method of record: [docs/QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md](../../docs/QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md). Do not modify these files; a new experiment gets a new folder.
