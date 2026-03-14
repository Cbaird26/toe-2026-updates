# External Replication Bundle 2026

This is the outsider-ready summary of the current concrete science package.

## Frozen contract

- TOE commit: `69f952d07e9cddca4fb898e46bb1a0f0336d32b1`
- toe-empirical-validation commit: `163418b9ff5410825133cffd75a5e0d37fbc1ce4`

## Recommended outsider replication order

1. Verify the frozen contract and manifest.
2. Reproduce H1 simulation-primary battery.
3. Inspect the H2 benchtop reference budget and H2 memo.
4. Inspect the H3 executable posterior summary and H3 memo.

## Canonical commands

```bash
git clone https://github.com/Cbaird26/toe-empirical-validation.git
cd toe-empirical-validation
git checkout 163418b9ff5410825133cffd75a5e0d37fbc1ce4

# H1
./.venv/bin/python experiments/h1_null_battery.py --out artifacts_h1_sim_primary --n-seeds 20 --n-model-seeds 20

# H2
./.venv/bin/python experiments/h2_instrument_budget.py --out artifacts_h2_benchtop_optical --delta-meas 1e-4 --T-s 1e-6 --delta-x-m 1e-3 --sigma-T-frac 1e-4 --sigma-dx-frac 5e-4 --vibration-frac 5e-4 --em-frac 1e-4 --thermal-frac 2e-4

# H3
./.venv/bin/python experiments/h3_joint_posterior.py --out artifacts_h3_joint
```

## Expected key outputs

- `artifacts_h1_sim_primary/null_battery_summary.json`
- `artifacts_h2_benchtop_optical/h2_instrument_budget.json`
- `artifacts_h3_joint/jointfit_summary.json`

## Checksum manifest

| File | SHA-256 |
| --- | --- |
| `docs/FROZEN_EXTERNAL_CONTRACT_2026.md` | `8027f75b2844b6ec04e081f35f8623d7ecda299874cfc2129bc7fce1bb84dd4a` |
| `docs/HYPOTHESIS_CAMPAIGN_ARTIFACT_MANIFEST_2026.md` | `95aebecf916a19a1f5624cdd34bb963eef2082b1cee00acd63316893ff398c9c` |
| `papers_sources/H2_NEXT_EXPERIMENT_MEMO_2026.pdf` | `a8b7e7451d58f704dc67f2b519b05587d7a5e2dddddc76387dca551dde4bfa77` |
| `papers_sources/H3_RESULT_MEMO_2026.pdf` | `70039568fc3fd0ee46a078ffe927e6bfb7e01492b2ea56e4f8693f9fba50de89` |
| `artifacts_h1_sim_primary/null_battery_summary.json` | `dbeb379bfb1e2a4e8f578b29ce2e3583f57f080f3179b051d05c23baf9380d2e` |
| `artifacts_h2_benchtop_optical/h2_instrument_budget.json` | `0428324ac63739147842d4398037f174be09fbad55cd4a38b8ab920289826c63` |
| `artifacts_h3_joint/jointfit_summary.json` | `54dc51023341df78bd84c230f29ac100a5c317cd6893e6b05a1ece7008063df2` |

## Claim boundary

- H1: simulation-primary stress-test result, not hardware detection claim
- H2: benchtop pilot planning/result floor, not decisive flagship discovery claim
- H3: executable multi-channel prototype result, not final global posterior
