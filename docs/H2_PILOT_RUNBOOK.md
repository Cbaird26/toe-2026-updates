# H2 interferometric pilot — bench runbook (Phase-0)

Companion to [H2_PILOT_PREREGISTRATION_2026.md](H2_PILOT_PREREGISTRATION_2026.md). This is an **operational checklist**, not a substitute for lab safety, laser regs, or institutional approvals.

## 0. Before touching hardware

- Noise budget worksheet: list thermal, vibration, alignment drift, detector dark counts, **calibrated** \(\delta_{\mathrm{tot}}\) components.  
- Analysis order is **fixed** in the prereg: calibrate \(V_0\) and \(\delta_{\mathrm{tot}}\) **before** interpreting test runs.  
- If \(\delta_{\mathrm{tot}}\) must be revised, do it **before** unblinding test labels (document as protocol addendum).

## 1. Calibration block (control runs)

1. **Baseline visibility** \(V_0\): path-balanced configuration, no deliberate “test” perturbation. Log temperature, humidity, table isolation state.  
2. **Known-loss calibrator** (if available): introduce a **classical** attenuation / decoherence reference so measured visibility drop maps to instrument linearity.  
3. **Stability:** time-series of \(V\) over ≥3× planned test duration; ensure drift \(\ll \delta_{\mathrm{tot}}\) or fold drift into budget.

## 2. Test runs

- Record \((T, \Delta x)\) **as-installed** (measured, not nominal).  
- For each run: raw counts / interference fringe fits, fit uncertainty, environmental snapshot ID linking to logs.  
- **Do not** change analysis script thresholds after seeing test-run summaries.

## 3. Exclusion math (null path)

Simulation reference (repo): `python scripts/mqgt_sim/h2_visibility_stack.py --save-dir papers_sources/figures/h2_stack --no-show`

If null: report \(\Gamma_{\mathrm{floor}}\) from measured \(T,\Delta x,\delta_{\mathrm{tot}}\) and state exclusion of \(\Gamma > \Gamma_{\mathrm{floor}}\) **at the achieved budget** (per prereg).

## 4. Packaging for publication / Zenodo

- One manifest CSV/JSON: run id, timestamps, \(V/V_0\), \(T\), \(\Delta x\), \(\delta_{\mathrm{tot}}\) components, notes.  
- Figures from the frozen analysis script + commit hash.  
- Link **H1** only as secondary context: [H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md](H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md).

---

**Frozen checklist:** March 2026. Amend with dated addendum if steps change.
