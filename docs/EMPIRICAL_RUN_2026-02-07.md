# Empirical run (2026-02-07)

**Channel:** Fifth-force / Yukawa constraints (Zenodo ToE four channels).

## What was run

- **Script:** `toe_fifth_force_mapping.py` (ToE fifth-force mapping: lambda_m, alpha_max → m_ev, theta_max, kappa_v_bound_GeV).
- **Command:**
  ```bash
  python3 toe_fifth_force_mapping.py 1-eotwash_prl2016_digitized_contract_READY.csv docs/empirical_run_2026-02-07_bounds.csv 1.7641645445725947e31 --m_new_GeV 0.0001
  ```
- **Inputs:** Eöt-Wash digitized curve `1-eotwash_prl2016_digitized_contract_READY.csv` (lambda_m, alpha_max; source: PRL 116, 131102 (2016)). K from [toe_fifth_force_parameter_card.yaml](../toe_fifth_force_parameter_card.yaml) (K_ToE). m_new_GeV = 0.0001 for kappa*v bound column.
- **Output:** [empirical_run_2026-02-07_bounds.csv](empirical_run_2026-02-07_bounds.csv) — 29 rows: lambda_m, alpha_max, m_ev, theta_max, kappa_v_bound_GeV.

## What changed

- No change to input data or script. Output file created.

## What I observed

- Script completed with exit 0. Bounds table produced: 29 rows consistent with Eöt-Wash digitized constraints; m_ev and theta_max scale as expected from small-mixing formula; kappa_v_bound_GeV populated for the chosen m_new_GeV. Reproducible with the same inputs and K.
