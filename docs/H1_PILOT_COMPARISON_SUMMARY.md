# H1 pilot — comparison summary (report lane)

**Companion:** [H1_CURRENT_STATUS_MEMO_2026.md](H1_CURRENT_STATUS_MEMO_2026.md) (interpretation and framework ordering).  
**Machine-readable rows:** `artifacts/h1_pilot/run_comparison_individual.csv` (same runs as the table below; regenerate when new runs are added).

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
- Matched 10M gate (2026-03-20): 12 replicates at `target_bits=10000000` `burnin_bits=0` `holdout_fraction=0.2`; artifacts: `artifacts/h1_pilot/placebo_runs/batch_12x10m_20260320.csv`, `artifacts/h1_pilot/placebo_runs/summary_12x10m_20260320.json`
- 10M gate tails: `P(|z_train| >= 2)=0.0000`, `P(|z_hold| >= 2)=0.0833`, `P(|z_train| >= 3)=0.0000`, `P(|z_hold| >= 3)=0.0000`, `P(|z_train| >= 5)=0.0000`, `P(|z_hold| >= 5)=0.0000`
- 10M gate acceptance: PASS (`12/12` complete; no holdout `|z| >= 3`; max holdout `|z| = 2.185`)

## Individual ANU, urandom, and placebo runs

| run_id | source | bits_total | z_train | z_hold | p_hat_train | p_hat_hold | holdout Wilson 95% | sha256_ok | notes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| anu_shake | anu | 50016 | +0.465 | +0.550 | 0.5011621223 | 0.5027491752 | [0.492952, 0.512545] | true | Live ANU shakedown |
| anu_1m | anu | 1000000 | +1.483 | +1.297 | 0.5008287500 | 0.5014500000 | [0.499259, 0.503641] | true | Live ANU replicate 1 |
| anu_1m_r2 | anu | 1000000 | +0.195 | +1.100 | 0.5001087500 | 0.5012300000 | [0.499039, 0.503421] | true | Live ANU replicate 2 |
| anu_10m | anu | 10000000 | -1.443 | -0.041 | 0.4997448750 | 0.4999855000 | [0.499293, 0.500678] | true | Live ANU scaled run |
| urandom_1m | urandom | 1000000 | +0.541 | +1.176 | 0.5003025000 | 0.5013150000 | [0.499124, 0.503506] | true | OS CSPRNG harness control |
| urandom_10m | urandom | 10000000 | +0.586 | -0.752 | 0.5001036250 | 0.4997340000 | [0.499041, 0.500427] | true | OS CSPRNG 10M parity |
| placebo_10m | placebo | 10000000 | -1.365 | +0.195 | 0.4997587500 | 0.5000690000 | [0.499376, 0.500762] | true | PCG64 placebo 10M single file seed 20260319 |

## Readout

- Placebo aggregate looks consistent with a healthy null pipeline.
- The matched 12x10M placebo batch also remained in-family and passed the local acceptance gate.
- The 10M placebo parity run remains in-family with the placebo null calibration and does not introduce a new holdout excursion.
- ANU runs do not look qualitatively different from the urandom controls under the frozen estimator, including the new 10M parity run.
- No current run shows a holdout result that stands out from the null calibration strongly enough to justify protocol branching.
