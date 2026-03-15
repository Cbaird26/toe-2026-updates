# Falsification Packet

A single document for a hostile-but-curious experimentalist: attack or replicate the core claim in one sitting. Aligned with the Zenodo record (A Theory of Everything / Unified ToE 2026) and the operational deformation of the Born rule evaluated across four channels.

**Zenodo:** [zenodo.org/records/18520596](https://zenodo.org/records/18520596)  
**Paper (local):** [papers_sources/A_Unified_Theory_of_Everything_CM_Baird_et_al_2026.pdf](../papers_sources/A_Unified_Theory_of_Everything_CM_Baird_et_al_2026.pdf)  
Canonical Zenodo citation for the 2026 Unified ToE paper (v216): https://doi.org/10.5281/zenodo.18520596.

---

## 1. Operational definition (outcome label / ethical weight E)

- **What E is:** The scalar ethical weighting field entering branch selection through a preregistered estimator.
- **Canonical deformation equation:**  
  **P_eta(i) = p_i · exp(eta Eᵢ) / Σ_j p_j · exp(eta Eⱼ)** where **p_i = |cᵢ|²** and **Eᵢ = ΔEᵢ / C_E**.  
  Standard QM is recovered when **eta → 0**, **ΔEᵢ → 0**, or **C_E → ∞**.
- **Canonical estimator pipeline (must be fixed before data collection):**
  1. Use only the canonical observable family `n(x,t)` and `s(x,t)` for the mainline estimator.
  2. Fix weights to `(0.7, 0.3)` for `(n,s)` in the headline protocol.
  3. Compute local ethical density: `e(x,t) = 0.7 n(x,t) + 0.3 s(x,t)`.
  4. Integrate over analysis region `V`: `E_R(t) = ∫_V e(x,t) d^3x`.
  5. Score each outcome branch at preregistered horizon `t*`:
     `ΔE_a = E_R^(a)(t*) - E_R^baseline(t*)`.
  6. Normalize branch weight by calibration constant `C_E`: `E_a = ΔE_a / C_E`.
- **Protocol boundary:** The above is the canonical estimator. Any alternate mapping is appendix-only sensitivity analysis and must be labeled secondary.
- **QRNG channel (concrete):** In the spine repo [toe-empirical-validation](https://github.com/Cbaird26/toe-empirical-validation), E-labeling is implemented in `code/e_labeling.py` (function family `label_E`). Pin commit hash (or Zenodo version) before running.
- **Pinned spine commit (current external contract):** `163418b9ff5410825133cffd75a5e0d37fbc1ce4` — toe-empirical-validation at this SHA provides the current campaign baseline, protocol docs, dry-run artifacts, and E-labeling. Use `git checkout 163418b9ff5410825133cffd75a5e0d37fbc1ce4` (or the full SHA) for replication of the present package. Earlier tags (`spine-v0.1`, `spine-v0.1.1`) are legacy baselines and are not the current external contract.
- **Φc and E as dynamical fields:** See paper for the Lagrangian/field formulation; the deformation is expressed so that both are part of the dynamics, not ad hoc.

---

## 2. Parameterization

- **Free knobs:** Coupling(s) governing the deformation strength; scale C; any channel-specific parameters (e.g. QRNG threshold, fifth-force range). Listed explicitly in the paper and in the reproducibility package.
- **Priors:** Stated in the likelihood/prior setup in the Zenodo package (likelihoods, priors, sampling). Reproducible runs use the same priors unless explicitly varied.
- **Limit that recovers standard QM:** As **eta → 0** (or **ΔE → 0**, or **C_E → ∞**), the theory reduces to standard quantum mechanics without ethics-weighted tilt. No new physics in that limit; new effects decouple.

---

## 3. Three cleanest predictions

1. **QRNG channel:** Statistically detectable deviation from standard random distribution under the operational definition of E in the QRNG protocol. Specific prediction: see paper and Zenodo analysis scripts.
2. **Fifth-force / equivalence-principle channel:** Bounds on new scalar-mediated forces (or equivalence-principle violation) that are consistent with the deformed framework; tension with existing fifth-force and Eötvös-type experiments if the deformation is large. See digitized constraints and likelihood setup in the repo/Zenodo.
3. **Cosmology / particle channel:** Constraints from Higgs invisible decays (or other collider/cosmology observables) that either support or rule out the parameter region where the deformation is observable. See paper and multi-channel constraint package.

(Exact wording of each prediction and experimental cut should be taken from the paper and Zenodo description; the above are the three channels in compact form.)

### 3.1 Flagship falsifier (primary)

- **Observable:** Interferometric visibility ratio `V/V0` for spatial superposition runs.
- **Model form:**  
  `V/V0 ≈ exp(-Gamma * T * Delta_x^2)`  
  where `T` is superposition time, `Delta_x` path separation, and `Gamma` is the effective collapse/deformation rate.
- **Null expectation (standard baseline):** `Gamma = 0` up to instrument/systematics floor.
- **Decisive sensitivity threshold:** for target fractional visibility precision `delta`, exclusion requires  
  `Gamma <= |ln(1-delta)| / (T * Delta_x^2)`  
  using preregistered analysis and full systematics disclosure.
- **Why this is flagship:** single-channel, quantitative, directly maps to one deforming rate, and yields immediate exclusion bounds.

---

## 4. Three cleanest ways it dies

1. **QRNG:** A well-powered, pre-registered QRNG experiment that controls for experimenter degrees of freedom and expectancy effects finds no deviation from standard randomness when analyzed with the same operational definition of E. The deformation is then excluded at the stated confidence level.
2. **Fifth-force / Eötvös:** Existing or new fifth-force and equivalence-principle experiments close the allowed parameter window for the scalar coupling to zero; the deformation is ruled out in the regime where it would have been observable.
3. **Multi-channel inconsistency:** The same parameter set cannot simultaneously satisfy QRNG, Higgs invisible, fifth-force, and cosmology constraints; the framework is overconstrained and fails a joint fit (or requires fine-tuning that is rejected by Occam / model comparison).

---

## 5. One-command reproduction and hash

- **Intended path:** Run the reproducibility package associated with the Zenodo record (scripts, likelihoods, priors, sampling). The package lives in the spine repo [Cbaird26/toe-empirical-validation](https://github.com/Cbaird26/toe-empirical-validation) (or [Cbaird26/mqgt-analysis](https://github.com/Cbaird26/mqgt-analysis)); a single entrypoint runs one channel (QRNG or fifth-force + cosmology), produces figures/constraints, and supports a checksum or pinned artifact.
- **One-command reproduction (pin commit before running):**
  1. Clone and enter the repo:  
     `git clone https://github.com/Cbaird26/toe-empirical-validation.git && cd toe-empirical-validation`
  2. Pin the artifact: record the commit hash with `git rev-parse HEAD` (run before any pull; document this hash in your replication report).
  3. Run the analysis for one channel:  
     `./run_all.sh`  
     or, if the repo uses a different entrypoint, follow the README in that repo for the single command that runs the analysis and produces figures. For QRNG channel only, use the script or command documented in the repo README.
  4. Compare outputs to Zenodo-supplied materials or to the figures in the Evidence paper; document any deviation.
- **Hash verifies everything:** When a fixed artifact (tarball, repo commit, or manifest) is provided, a checksum (e.g. SHA-256) verifies that the analysis has not been altered post hoc. The Zenodo record provides a fixed DOI and version; use the Zenodo file checksums for the deposited materials. **For repo-based reproduction, always pin to a specific commit (e.g. `git checkout <SHA>`) and document that commit hash in the replication report.**
- **Replication ladder:** For the full step-by-step ladder (clone → run → compare → “it lives or dies here” criterion), see [REPLICATION_LADDER.md](REPLICATION_LADDER.md).

---

## 6. External evidence admissibility registry (2026)

- Canonical tiered registry: [EVIDENCE_REGISTRY_2026.md](EVIDENCE_REGISTRY_2026.md)
- Ingest/audit memo: [EVIDENCE_INGEST_MEMO_2026.md](EVIDENCE_INGEST_MEMO_2026.md)

Policy:
- Tier A/B may inform decision gates when explicitly cited.
- Tier C is context only and cannot be decisive for falsification/survival claims.
