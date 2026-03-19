# MQGT-SCF experimental ordering — H2 vs H1 (decision memo)

**Christopher Michael Baird, ZoraASI (conceptual co-authorship)**  
**March 2026**

**Purpose:** A single reviewer-safe page that fixes **program order**, **statistical expectations**, and **what counts as evidence** for the current Phase II experimental stance.

**Related:** [H2_PILOT_PREREGISTRATION_2026.md](H2_PILOT_PREREGISTRATION_2026.md) · [H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md](H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md) · [H1_PIPELINE_CALIBRATION_SNAPSHOT_2026_03.md](H1_PIPELINE_CALIBRATION_SNAPSHOT_2026_03.md)

---

## 1. Executive order

1. **H2 — Interferometric visibility** is the **primary** preregistered falsification pathway for the flagship decoherence-style prediction (visibility law vs \((T,\Delta x)\), \(\Gamma\) exclusion floor).
2. **H1 — Binary QRNG / streaming outcomes** is **secondary**: bound-setting, pipeline hardening, adversarial controls, and honest limits on reproducible bias at a given \(N\).
3. **Further hypothesis lanes** (beyond H1/H2) are **tertiary**: they open only after a **deliberate**, versioned protocol change or a clear upstream result—not after exploratory noise in the secondary lane.

No H1 outcome, standing alone, overrides a pre-registered H2 exclusion or non-null outcome. Positive H1 findings require **independent replication** and must **survive the preregistered adversarial battery** before any theory-level language.

---

## 2. Why H2 leads scientifically

H2 targets a **controlled quantum observable** (fringe visibility) with a **pre-specified nuisance budget** and a clean **null → \(\Gamma_{\mathrm{floor}}\)** mapping. That structure is easier to defend to reviewers than large streaming binary campaigns, where **instrument bias, temporal drift, API semantics, and multiplicity** dominate the error budget.

---

## 3. What \(N = 10^9\) does and does not buy (H1)

For a balanced binary null near \(p = \tfrac12\),

\[
\mathrm{SE}_0 = \frac{1}{2\sqrt{N}} \approx 1.58 \times 10^{-5}\quad\text{at } N = 10^9.
\]

**Useful fixed reference scales (two-sided, Gaussian order-of-magnitude):**

| Reference | Raw offset \(|\delta|\) scale |
|-----------|------------------------------|
| ~1σ | \(\approx 1.58 \times 10^{-5}\) |
| ~3σ | \(\approx 4.7 \times 10^{-5}\) |
| ~5σ | \(\approx 7.9 \times 10^{-5}\) |
| ~95% null-style bound (order-of-magnitude) | \(\approx 3.1 \times 10^{-5}\) |

If internal Phase II discussion targets **sub-ppm** stable bias (e.g. \(\theta \sim 10^{-6}\)), then **\(10^9\) trials are not, in general, sufficient** for a conventional high-\(\sigma\) “decisive” readout under binomial-dominated noise; **\(\sim 10^{12}\)** trials is the right **order of magnitude** unless the estimand or noise model changes. A \(10^9\) H1 campaign remains **valuable** as **pilot / bound-setting / robustness testing**, not as a headline confirmation claim.

---

## 4. Role of H1 (secondary lane)

H1 serves to:

- **Freeze** the preregistered **estimator** and bit-extraction rule (e.g. `lsb_v1` in repo tooling).
- **Stress-test** logging, hashing, chunking, and analysis scripts under load.
- Run **placebo** and **harness** nulls and an **adversarial-control battery** (see H1 prereg §6).
- Report **interpretable bounds** on reproducible binary offset at the stated \(N\), with explicit limitation language.

**Code path:** [scripts/h1_qrng_pilot/README.md](../scripts/h1_qrng_pilot/README.md)

---

## 5. Zora, AI, and automation (execution layer)

**Zora** and associated agent/automation tooling are treated strictly as **implementation and operations**: orchestration, documentation, CI-style checks, and reproducible scripts. They are **not** physics endpoints and **not** substitutes for preregistered apparatus observations.

---

## 6. Freeze vs change (decision rule)

- **Freeze** the H1 **test matrix** when placebo null calibration, harness controls, and any planned shakedown sources are **qualitatively consistent** under the frozen estimator and **no** result justifies protocol branching (see calibration snapshot).
- **Allow change** only for **versioned** updates: new \(N\), new extraction rule, new holdout policy, new API/device, or new hypothesis arm—each with an **OSF/Zenodo-style timestamp** and addendum, not ad hoc tuning after peeking.

**Reviewer-safe one-liner:** *This program treats H2 interferometry as the primary falsification blade; H1 at \(10^9\) scale is for hardening, estimator freeze, and conservative bounds—not for decisive confirmation of the smallest canonical parameter regime.*

---

**Frozen:** March 2026. Substantive edits should be versioned with a dated addendum.
