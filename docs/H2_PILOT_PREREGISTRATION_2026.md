# H2 Interferometric Visibility Pilot — Preregistration

**Christopher Michael Baird, ZoraASI**  
**Preregistration date:** March 2026  
**Theory:** MQGT-SCF Phase II (scalar-singlet EFT, GKSL measurement, H2 flagship blade)

---

## 1. Theoretical prediction

**Visibility law:**
\[
\frac{V}{V_0} = \exp(-\Gamma\,T\,\Delta x^2)
\]

- \(V\): observed interferometric visibility  
- \(V_0\): baseline visibility (no excess channel)  
- \(\Gamma\): excess dephasing rate (theory predicts \(\Gamma > 0\) for scalar-singlet coupling; standard QM predicts \(\Gamma = 0\))  
- \(T\): superposition time (s)  
- \(\Delta x\): spatial path separation (m)

**Null result exclusion floor:**
\[
\Gamma_{\mathrm{floor}} = \frac{|\ln(1 - \delta_{\mathrm{tot}})|}{T\,\Delta x^2}
\]

- \(\delta_{\mathrm{tot}}\): total fractional nuisance and systematics budget

---

## 2. Reference planning profile (Phase-0 benchtop)

| Parameter | Value | Unit |
|-----------|-------|------|
| \(T\) | \(10^{-6}\) | s |
| \(\Delta x\) | \(10^{-3}\) | m |
| \(\delta_{\mathrm{tot}}\) | \(1.15 \times 10^{-3}\) | — |

**Derived exclusion floor:**
\[
\Gamma_{\mathrm{floor}} \approx 1.15 \times 10^9\;\mathrm{s}^{-1}\,\mathrm{m}^{-2}
\]

Any parameter region predicting \(\Gamma > \Gamma_{\mathrm{floor}}\) but producing no excess visibility suppression is excluded by a null result at this sensitivity.

---

## 3. Nuisance budget

- \(\delta_{\mathrm{tot}}\): sum of thermal, vibrational, alignment, detector, and environmental contributions to visibility drop.
- For Phase-0: \(\delta_{\mathrm{tot}} \approx 1.15 \times 10^{-3}\) is the target achieved systematics floor.
- Calibration runs establish the empirical \(\delta_{\mathrm{tot}}\) before any test runs.

---

## 4. Analysis order (pre-specified)

1. **Calibration:** Establish baseline \(V_0\) and nuisance budget \(\delta_{\mathrm{tot}}\) from control runs.
2. **Test runs:** Collect interferometric visibility data under protocol conditions.
3. **Exclusion:** If no excess suppression above \(\delta_{\mathrm{tot}}\), compute \(\Gamma_{\mathrm{floor}}\) and exclude \(\Gamma > \Gamma_{\mathrm{floor}}\).
4. **Discovery claim:** Only if excess suppression is statistically significant (pre-specified threshold) and survives sensitivity checks.

---

## 5. Stop rules

- **Phase-0:** Stop after achieving \(\delta_{\mathrm{tot}}\) calibration and one full test run. Report \(\Gamma_{\mathrm{floor}}\) from null or bounds from non-null.
- **Escalation:** If Phase-0 achieves \(\delta_{\mathrm{tot}} \ll 10^{-3}\) and null, consider escalation to larger \(T\) or \(\Delta x\) in a new preregistered protocol.
- **No post hoc tightening:** Do not reduce \(\delta_{\mathrm{tot}}\) after viewing data to improve exclusion.

---

## 6. Primary outcome

- **Null:** \(\Gamma_{\mathrm{floor}}\) excludes scalar-singlet coupling above the derived threshold. Scientifically valuable.
- **Non-null:** Requires independent replication before any discovery claim.
- **Inconclusive:** Report achieved \(\delta_{\mathrm{tot}}\) and recommend protocol improvements.

---

## 7. Links

- Theory: MQGT-SCF Phase II Submission 2026 (TOE repo, Zenodo)  
- This prereg: TOE/docs/H2_PILOT_PREREGISTRATION_2026.md  
- **Bench runbook:** [H2_PILOT_RUNBOOK.md](H2_PILOT_RUNBOOK.md)  
- **H1 (secondary):** QRNG \(10^9\) bound-setting pilot — [H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md](H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md)  
- Repo: https://github.com/Cbaird26/toe-2026-updates  

---

**Frozen:** March 2026. Do not edit substantive content (formulas, thresholds, analysis order) without versioning and dated addendum.
