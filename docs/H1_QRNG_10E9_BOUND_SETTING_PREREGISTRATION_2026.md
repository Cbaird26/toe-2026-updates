# H1 QRNG 10⁹-Trial Pilot — Bound-Setting Preregistration

**Christopher Michael Baird, ZoraASI (conceptual co-authorship)**  
**Preregistration date:** March 2026  
**Theory:** MQGT-SCF Phase II (binary-outcome bound-setting; H1 secondary blade)

**Companion preregistration (primary falsification pathway):** [H2_PILOT_PREREGISTRATION_2026.md](H2_PILOT_PREREGISTRATION_2026.md)

---

## Abstract

This document preregisters a **prospective, fixed-\(N\)** pilot study collecting **\(N = 10^9\)** pre-specified binary outcomes from a quantum random number generator (QRNG) pipeline under logged conditions. The primary scientific purpose is **bound-setting, pipeline hardening, and adversarial robustness testing**—not a claim of decisive confirmation or falsification of the full MQGT-SCF objective-collapse parameter space. A pre-specified analysis estimates the raw deviation \(\hat\delta = \hat p - \tfrac12\) and places **interpretable limits** on reproducible bias at the \(10^9\) scale, while explicitly acknowledging **limited statistical power** relative to internally discussed sub-ppm coupling scales in Phase II documentation. **Interferometric visibility tests (H2)** remain the **primary** pre-registered falsification pathway for the framework’s flagship decoherence-style prediction; **H1** is **secondary**.

---

## 1. Program positioning (H1 vs H2)

| Blade | Role | Primary observable |
|-------|------|--------------------|
| **H2** | **Primary** falsification pathway for collapse-channel / scalar-singlet decoherence-style signatures | Interferometric visibility \(V/V_0\) vs \((T,\Delta x)\) |
| **H1** | **Secondary**: correlations, bounds, instrumentation stress-tests, adversarial controls | Binary QRNG frequency \(\hat p\) vs \(1/2\) |

**Interpretation rule:** No H1 result, standing alone, overrides a pre-registered H2 exclusion or non-null protocol outcome. Positive H1 findings require **independent replication** and must **survive the adversarial battery** before any theory-level language.

---

## 2. Theory link (citation only; not the confirmatory claim)

MQGT-SCF Phase II motivates **small** departures from ideal Born statistics under structured experimental contexts. Internal Phase II compilation discussions reference **order-of-magnitude** parameter scales on the order of **\(\theta \sim 10^{-6}\)** for some binary-bias scenarios—i.e. **sub-ppm** effects. At **\(N=10^9\)** fair-coin sampling, the **standard error** of \(\hat p\) under the null is

\[
\mathrm{SE}_0 = \sqrt{\frac{1/4}{N}} = \frac{1}{2\sqrt{N}} \approx 1.58\times 10^{-5}.
\]

Thus **\(10^9\) trials are not, in general, sufficient** to resolve **\(10^{-6}\)**-scale biases at conventional high-\(\sigma\) thresholds; **\(\sim 10^{12}\)** trials (order-of-magnitude) is the right scale **if** the target effect is truly \(\mathcal{O}(10^{-6})\) and the estimator is dominated by binomial sampling noise.

**Theory artifact (repository):** [papers_sources/MQGT-SCF_Phase_II_Submission_2026.tex](../papers_sources/MQGT-SCF_Phase_II_Submission_2026.tex)  
**Zenodo / published PDF DOI:** `[TBD — insert Phase II record DOI when minted]`

This preregistration **does not** claim that the H1 pilot is powered to validate or refute that \(\theta\) scale.

---

## 3. Hypotheses (testable, instrument-level)

**Null hypothesis \(H_0\):** After pre-registered integrity filters and the **adversarial-control battery** (Section 6), there is **no reproducible, stable** deviation of \(\hat p\) from \(1/2\) beyond what is consistent with sampling variation and audited nuisance models.

**Alternative hypothesis \(H_1\):** A **reproducible** deviation exists **and** survives (i) holdout validation, (ii) shuffled-label / delayed-decoding controls, and (iii) independent rerun criteria in Section 6.

**Explicitly not primary:** “Confirm MQGT-SCF” or “detect consciousness field” as a **single-step** conclusion from this pilot.

---

## 4. Primary endpoint and estimand

- **Outcome:** Binary \(X_i \in \{0,1\}\) from the pre-specified QRNG mapping (e.g. even/odd photon counts, designated bit extraction rule—see `[TBD]`).
- **Estimand:** \(\delta = p - \tfrac12\) for the **primary analysis set** (Section 5).
- **Estimator:** \(\hat\delta = \hat p - \tfrac12\) with \(\hat p = \frac{1}{N}\sum_i X_i\) on the primary set of size \(N\).

**Direction:** `[TBD — two-sided default unless a directional MQGT-SCF prediction is frozen here before data collection]`

**Stopping:** **Fixed \(N = 10^9\)** primary-set bits **or** earlier stop only under **pre-specified abort rules** (equipment failure, compromise of randomness audit trail, ethics stop—Section 8). No optional stopping for significance.

---

## 5. Design and data collection

### 5.1 Apparatus and pipeline

| Item | Specification |
|------|----------------|
| QRNG device / API | `[TBD — manufacturer, model, firmware/SDK version]` |
| Physical location / lab | `[TBD]` |
| Bit extraction rule | `[TBD — exact algorithm from raw events to X_i]` |
| Acquisition schedule | `[TBD — continuous vs batched; max rate; duty cycle]` |
| Environmental logging | `[TBD — temperature, vibration, power quality, network, clock sync, etc.]` |
| Time window | `[TBD — calendar start/end UTC; campaign tie-ins if any]` |

### 5.2 Prospective partitioning (mandatory)

Pre-register **before** unblinding analysis:

1. **Calibration / burn-in block:** `[TBD — fraction or fixed M bits; excluded from primary]`  
2. **Training fraction:** `[TBD — e.g. 80% of primary stream for model fitting if any nuisance model is used]`  
3. **Holdout fraction:** `[TBD — e.g. 20% locked until final analysis script is frozen]`  

If no nuisance model is used, **still** retain a **holdout** for replication-style checks.

### 5.3 Integrity filters (pre-specified exclusions)

Examples (finalize before data): **loss of timestamp monotonicity**, **checksum / signing failure**, **device fault codes**, **>X% missing samples** in a block.  
**Exact numeric rules:** `[TBD]`

Excluded trials are **logged** and reported; sensitivity analyses may include/exclude borderline blocks per a **pre-written** script.

### 5.4 Implementation layer (software)

**Lattice simulations, ML orchestration, dashboards, or FastAPI “injection” demos are execution and visualization layers only.** They **do not** constitute physical QRNG evidence. Claims about hardware QRNG bias must trace to **auditable raw event logs** and the preregistered extraction rule.

---

## 6. Adversarial-control battery (minimum)

A **positive** claim requires **all** applicable items below to pass pre-specified criteria. Failure reclassifies the result as **fragile / non-claimable** pending remediation.

1. **Blinding / delayed decoding:** Analysis scripts frozen before **holdout** labels are merged; or cryptographic commitment to analysis code hash. `[TBD — exact procedure]`  
2. **Label shuffling / permutation null:** Distribution of test statistics under permutations reported; observed statistic compared.  
3. **Synthetic null streams:** PRNG-derived placebo streams through identical pipeline; false-positive rate check. **Reference implementation:** `scripts/h1_qrng_pilot/placebo_batch.py` (fixed-seed `placebo` mode + batch CSV/JSON summary).  
4. **Independent rerun:** Second collection window or duplicate device (if available) with **pre-specified** agreement metric. `[TBD]`  
5. **Decoupled windows (“chaos” controls):** Windows where **no** experimental manipulation or campaign context applies; must not show spurious coherence specific to “active” windows only. `[TBD definitions]`  
6. **Multiple-testing guard:** If secondary endpoints are analyzed, report **all** endpoints or use a **pre-specified** multiplicity adjustment. `[TBD list of secondary endpoints, if any]`

**Failure definition (example):** Holdout sign flips; permutation \(p\)-value not extreme; placebo streams show similar “signal”; independent rerun fails pre-specified agreement.

---

## 7. Analysis plan

### 7.1 Primary analysis

- Compute \(\hat p\), \(\hat\delta\), and \(\mathrm{SE}_0 = \sqrt{\hat p(1-\hat p)/N}\) (report both \(\mathrm{SE}_0\) and **Clopper–Pearson** or Wilson interval for transparency).  
- **Standardized score (descriptive):** \(z = \hat\delta / \mathrm{SE}_0\) (under idealized binomial null; report **finite-sample** interval in any case).

### 7.2 Confirmatory vs descriptive

**Descriptive reporting:** \(z\) thresholds (e.g. \(|z|>3\), \(|z|>5\)) may be reported **only as calibration language** unless a **single confirmatory rule** is frozen below.

**Confirmatory (optional — pre-specify one):**  
`[TBD — e.g. two-sided α = 0.05 on holdout only; or Bayes factor threshold on pre-specified prior; if none, state “descriptive only”]`

### 7.3 Secondary analyses (exploratory unless pre-registered here)

- Blockwise heterogeneity (drift, day/night, temperature bins).  
- Autocorrelation / spectral checks on residuals (if iid fails).  
- **Optional stratification** by external context (e.g. campaign windows): **must** be labeled **exploratory** unless fully pre-specified in Section 5.

List planned secondary tests: `[TBD or “none”]`

---

## 8. Human subjects / ethics decision tree

- **Pure hardware QRNG stream** with **no** human labeling, **no** meditator metadata, **no** correlated interventions: likely **not** human-subjects research; confirm with local policy.  
- **Correlated arms** (e.g. bits paired to self-reported meditative state, synchronized global events): may constitute **human subjects** research requiring **IRB / ethics review**.  

**Status for this protocol:** `[TBD — IRB protocol number or “not applicable” with brief justification per institutional counsel]`  

Public communications must **not** coerce participation or imply medical claims.

---

## 9. Power and limitations (explicit)

- At \(N=10^9\), \(\mathrm{SE}_0 \approx 1.58\times 10^{-5}\). **Sub-ppm** (\(<10^{-6}\)) biases are **not** reliably detectable at **5σ**-style thresholds without **much larger \(N\)** or **different observables** (e.g. H2).  
- Unknown **slow drift**, **autocorrelation**, and **pipeline leakage** can mimic “bias”; hence Section 6.  
- This pilot **does not** replace **device certification** or **NIST-style** randomness test suites; those may be run **additionally** but are **not** substitutive for preregistered primary inference without careful multiplicity control.

---

## 10. Interpretation rules (binding)

| Outcome pattern | Allowed language |
|-----------------|------------------|
| Null after controls | “**No reproducible deviation** at \(\mathcal{O}(10^{-5})\) SE scale; **upper bound** language on stable bias under stated nuisance model.” |
| Fragile positive | “**Instrumentation / leakage / multiple testing** suspected; **no** theory claim.” |
| Robust positive (holdout + reruns + battery) | “**Anomaly warranting replication**”; **no** single-step “theory confirmed.” |

---

## 11. Relationship to H2 (interferometry)

Any H1 outcome **must** be reported alongside a clear statement that **H2** tests a **distinct** parameterization (e.g. \(\Gamma\) in visibility decay) with its own preregistered exclusion logic. Conflicts between H1 exploratory correlations and H2 nulls are resolved in favor of **pre-registered primary endpoints** per protocol, with **public explanation**.

---

## 12. Reproducibility and release

- **Code:** `scripts/mqgt_sim/` (illustrative simulations); **`scripts/h1_qrng_pilot/`** (HDF5 collector, `stats_core`, `analyze.py`, **`placebo_batch.py`** — see `scripts/h1_qrng_pilot/README.md`)  
- **Frozen cross-run readout:** [H1_FROZEN_CROSS_RUN_SUMMARY_2026.md](H1_FROZEN_CROSS_RUN_SUMMARY_2026.md)  
- **Data schema (reference implementation):** HDF5 groups `metadata` (attrs: `stream_sha256_hex`, `extraction_rule_id`, …), datasets `raw_u32`, `chunk_timestamp_ns`; environmental logs: `[TBD external CSV/JSON alongside file]`  
- **Versioning:** Git commit hash frozen at analysis freeze: `[TBD at freeze]`  
- **License / access:** `[TBD]`

---

## 13. Links

- **H2 (primary blade):** [docs/H2_PILOT_PREREGISTRATION_2026.md](H2_PILOT_PREREGISTRATION_2026.md)  
- **1B go / no-go (campaign discipline):** [H1_1B_GO_NO_GO_MEMO_2026.md](H1_1B_GO_NO_GO_MEMO_2026.md)  
- **Frozen cross-run summary:** [H1_FROZEN_CROSS_RUN_SUMMARY_2026.md](H1_FROZEN_CROSS_RUN_SUMMARY_2026.md)  
- **This prereg (canonical markdown):** `docs/H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md`  
- **Theory TeX:** [papers_sources/MQGT-SCF_Phase_II_Submission_2026.tex](../papers_sources/MQGT-SCF_Phase_II_Submission_2026.tex)  
- **GitHub (organization):** https://github.com/Cbaird26  
- **OSF preregistration (timestamped):** `[TBD — paste OSF URL after registration]`  
- **Zenodo DOI (PDF export of this prereg):** `[TBD — after upload]`  

---

## 14. Upload playbook (OSF + Zenodo)

### 14.1 OSF (timestamped preregistration)

1. Create or open an OSF project (https://osf.io).  
2. Start a **Preregistration** (choose the template closest to “general” or “engineering / methods” if no physics-specific template fits).  
3. Paste sections **in order:** Abstract → §1–§13 (omit this §14 if OSF length limits require; keep §14 only in repo / Zenodo PDF).  
4. Submit for **frozen timestamp**; then paste the resulting **public OSF URL** into §13 above (versioned addendum if edited later).

**Suggested paste order:** Title/authors → Abstract → §1 Program positioning → §2 Theory link → §3 Hypotheses → §4 Endpoint → §5 Design → §6 Adversarial battery → §7 Analysis → §8 Ethics → §9 Power/limitations → §10 Interpretation → §11 H2 relationship → §12 Reproducibility → §13 Links (without TBDs if you prefer to update OSF addendum when filled).

### 14.2 Zenodo (citable PDF from this file)

From the TOE repo root, with [Pandoc](https://pandoc.org/) and a LaTeX engine installed (e.g. MacTeX):

```bash
cd ~/Downloads/TOE
pandoc docs/H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md \
  -o docs/H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.pdf \
  --pdf-engine=pdflatex \
  -V geometry:margin=1in \
  -V fontsize=11pt
```

Upload the PDF to Zenodo as a new **versioned** record (type: *Publication / Working paper* or *Methods*), add keywords `MQGT-SCF`, `QRNG`, `preregistration`, `bound-setting`, and **link back** to the OSF registration in the Zenodo description. Minted DOI → paste into §13.

**Note:** If Pandoc fails on internal links or math, try `--mathml` or switch to `xelatex` with `-V mainfont="Latin Modern Roman"`.

---

**Frozen:** March 2026. Do not edit substantive content (hypotheses, primary endpoint, analysis order, adversarial criteria, or H1/H2 precedence rules) without versioning and a dated addendum. Filling `[TBD]` fields is allowed **before** data collection; each fill should be dated in the addendum.
