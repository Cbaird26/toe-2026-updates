# H1 pipeline calibration snapshot — March 2026

**Purpose:** Repo-local, citable summary of **null calibration** (placebo batch + individual ANU / urandom runs) for the H1 QRNG pilot tooling. This document is **sanitized** (no API keys, `.env` paths, or raw HDF5 blobs). Full machine artifacts may live under `artifacts/` locally and are typically **not** versioned.

**Frozen estimator:** `lsb_v1` (least-significant bit extraction as implemented in `scripts/h1_qrng_pilot/`). **Holdout:** train/hold split per run attributes (e.g. `holdout_fraction=0.2` in placebo batch); see run metadata in archived pilot outputs for exact conventions.

**Metadata**

| Field | Value |
|-------|--------|
| Snapshot date | March 2026 |
| Source aggregate | `artifacts/h1_pilot/comparison_summary.md` (local) |
| Repo commit | `[fill at publish]` |

---

## Placebo batch aggregate

- Replicates: 500 at target_bits=200000 burnin_bits=1000 holdout_fraction=0.2
- P(|z_train| >= 2): 0.0420
- P(|z_hold| >= 2): 0.0600
- P(|z_train| >= 3): 0.0020
- P(|z_hold| >= 3): 0.0040
- P(|z_train| >= 5): 0.0000
- P(|z_hold| >= 5): 0.0000
- Frac perm_p < 0.05: 0.0400

---

## Individual ANU and urandom runs

| run_id | source | bits_total | z_train | z_hold | p_hat_train | p_hat_hold | holdout Wilson 95% | sha256_ok | notes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| anu_shake | anu | 50016 | +0.465 | +0.550 | 0.5011621223 | 0.5027491752 | [0.492952, 0.512545] | true | Live ANU shakedown |
| anu_1m | anu | 1000000 | +1.483 | +1.297 | 0.5008287500 | 0.5014500000 | [0.499259, 0.503641] | true | Live ANU replicate 1 |
| anu_1m_r2 | anu | 1000000 | +0.195 | +1.100 | 0.5001087500 | 0.5012300000 | [0.499039, 0.503421] | true | Live ANU replicate 2 |
| anu_10m | anu | 10000000 | -1.443 | -0.041 | 0.4997448750 | 0.4999855000 | [0.499293, 0.500678] | true | Live ANU scaled run |
| urandom_1m | urandom | 1000000 | +0.541 | +1.176 | 0.5003025000 | 0.5013150000 | [0.499124, 0.503506] | true | OS CSPRNG harness control |

---

## Readout (from local comparison summary)

- Placebo aggregate looks consistent with a healthy null pipeline.
- ANU runs do not look qualitatively different from the urandom control under the frozen estimator.
- No current run shows a holdout result that stands out from the null calibration strongly enough to justify protocol branching.

---

## Frozen conclusion (one sentence)

**Placebo null calibration, urandom harness, and ANU shakedown/replicates are in-family under the frozen `lsb_v1` estimator; there is no basis for protocol branching on these March 2026 pilot readouts.**

---

**Strategic context:** [H2_vs_H1_DECISION_MEMO_2026.md](H2_vs_H1_DECISION_MEMO_2026.md) · [H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md](H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md)
