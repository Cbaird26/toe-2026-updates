# H1 Frozen Cross-Run Summary (Placebo, ANU, Urandom)

**Date frozen:** March 19, 2026  
**Scope:** H1 QRNG pilot under the frozen estimator in `scripts/h1_qrng_pilot/collect.py` and `scripts/h1_qrng_pilot/analyze.py`  
**Status:** Negative-control / pipeline-hardening summary; not a new theory claim

---

## Bottom line

Under the frozen H1 estimator, the placebo batch, the `urandom` control, and the current ANU runs are qualitatively consistent with null behavior. No source currently stands out enough to justify protocol branching.

---

## Placebo Batch Aggregate

- Replicates: `500`
- Target bits per replicate: `200000`
- Burn-in bits: `1000`
- Holdout fraction: `0.2`
- `P(|z_train| >= 2) = 0.0420`
- `P(|z_hold| >= 2) = 0.0600`
- `P(|z_train| >= 3) = 0.0020`
- `P(|z_hold| >= 3) = 0.0040`
- `P(|z_train| >= 5) = 0.0000`
- `P(|z_hold| >= 5) = 0.0000`
- `Frac perm_p < 0.05 = 0.0400`

Interpretation: the frozen H1 pipeline behaves like a sane null pipeline under placebo calibration.

---

## Individual Runs

| run_id | source | bits_total | z_train | z_hold | p_hat_train | p_hat_hold | sha256_ok | notes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `anu_shake` | `anu` | `50016` | `+0.465` | `+0.550` | `0.5011621223` | `0.5027491752` | `true` | Live ANU shakedown |
| `anu_1m` | `anu` | `1000000` | `+1.483` | `+1.297` | `0.5008287500` | `0.5014500000` | `true` | Live ANU replicate 1 |
| `anu_1m_r2` | `anu` | `1000000` | `+0.195` | `+1.100` | `0.5001087500` | `0.5012300000` | `true` | Live ANU replicate 2 |
| `anu_10m` | `anu` | `10000000` | `-1.443` | `-0.041` | `0.4997448750` | `0.4999855000` | `true` | Live ANU scaled run |
| `urandom_1m` | `urandom` | `1000000` | `+0.541` | `+1.176` | `0.5003025000` | `0.5013150000` | `true` | OS CSPRNG harness control |

Interpretation: the ANU runs do not look qualitatively different from the `urandom` control under the frozen estimator.

---

## Readout

- The placebo aggregate is consistent with expected null behavior.
- The `urandom` control is in-family with the placebo baseline.
- The current ANU runs are also in-family with that baseline.
- No holdout result here is strong enough to justify changing the protocol or opening a broader test matrix.

---

## Provenance

- Local untracked comparison artifacts were generated under `artifacts/h1_pilot/` and are intentionally not versioned.
- The purpose of this document is to preserve the cross-run readout in the tracked docs lane without committing raw local artifacts or secrets.
