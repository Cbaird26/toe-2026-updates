# Falsification Packet

A single document for a hostile-but-curious experimentalist: attack or replicate the core claim in one sitting. Aligned with the Zenodo record (A Theory of Everything / Unified ToE 2026) and the operational deformation of the Born rule evaluated across four channels.

**Zenodo:** [zenodo.org/records/18511550](https://zenodo.org/records/18511550)  
**Paper (local):** [papers_sources/A_Unified_Theory_of_Everything_CM_Baird_et_al_2026.pdf](../papers_sources/A_Unified_Theory_of_Everything_CM_Baird_et_al_2026.pdf)  
Canonical Zenodo citation for the 2026 Unified ToE paper (v216): https://zenodo.org/records/18511550.

---

## 1. Operational definition (outcome label / ethical weight E)

- **What E is:** The scalar "ethical weight" or outcome-label bias that deforms the Born rule. It is treated as a real dynamical field (with Φc) in the formalism.
- **Equation (minimal deformation):**  
  **P(i) ∝ |cᵢ|² · exp(−E/C)**  
  where outcome *i* has amplitude cᵢ, E is the ethical-weight field evaluated for that outcome, and C is a scale constant. Standard QM is recovered when E → 0 or C → ∞.
- **How E is assigned, measured, or proxied:** Defined operationally in the paper (see sections on outcome labeling, scalar structure, and constraint channels). E is not a free narrative label; it is tied to observable or protocol-defined quantities in each channel (QRNG, Higgs invisible, fifth-force, cosmology). Exact mapping: see paper and Zenodo supplementary materials.
- **Φc and E as dynamical fields:** See paper for the Lagrangian/field formulation; the deformation is expressed so that both are part of the dynamics, not ad hoc.

---

## 2. Parameterization

- **Free knobs:** Coupling(s) governing the deformation strength; scale C; any channel-specific parameters (e.g. QRNG threshold, fifth-force range). Listed explicitly in the paper and in the reproducibility package.
- **Priors:** Stated in the likelihood/prior setup in the Zenodo package (likelihoods, priors, sampling). Reproducible runs use the same priors unless explicitly varied.
- **Limit that recovers standard QM:** As the deformation coupling(s) → 0 (or C → ∞), the theory reduces to standard quantum mechanics (Born rule without the exp(−E/C) factor). No new physics in that limit; new effects decouple.

---

## 3. Three cleanest predictions

1. **QRNG channel:** Statistically detectable deviation from standard random distribution under the operational definition of E in the QRNG protocol. Specific prediction: see paper and Zenodo analysis scripts.
2. **Fifth-force / equivalence-principle channel:** Bounds on new scalar-mediated forces (or equivalence-principle violation) that are consistent with the deformed framework; tension with existing fifth-force and Eötvös-type experiments if the deformation is large. See digitized constraints and likelihood setup in the repo/Zenodo.
3. **Cosmology / particle channel:** Constraints from Higgs invisible decays (or other collider/cosmology observables) that either support or rule out the parameter region where the deformation is observable. See paper and multi-channel constraint package.

(Exact wording of each prediction and experimental cut should be taken from the paper and Zenodo description; the above are the three channels in compact form.)

---

## 4. Three cleanest ways it dies

1. **QRNG:** A well-powered, pre-registered QRNG experiment that controls for experimenter degrees of freedom and expectancy effects finds no deviation from standard randomness when analyzed with the same operational definition of E. The deformation is then excluded at the stated confidence level.
2. **Fifth-force / Eötvös:** Existing or new fifth-force and equivalence-principle experiments close the allowed parameter window for the scalar coupling to zero; the deformation is ruled out in the regime where it would have been observable.
3. **Multi-channel inconsistency:** The same parameter set cannot simultaneously satisfy QRNG, Higgs invisible, fifth-force, and cosmology constraints; the framework is overconstrained and fails a joint fit (or requires fine-tuning that is rejected by Occam / model comparison).

---

## 5. One-command reproduction and hash

- **Intended path:** Run the reproducibility package associated with the Zenodo record (scripts, likelihoods, priors, sampling). If the package lives in a sibling repo (e.g. **toe-empirical-validation** or **mqgt-analysis**), the one-command path and README will be linked here.
- **Current status:** Reproduction path and manifest are described in the Zenodo record. Code and manifests are included for re-run and audit. For a single command or script that runs the full analysis and produces figures, see the Zenodo deposit files or the repo [Cbaird26/toe-empirical-validation](https://github.com/Cbaird26/toe-empirical-validation) (if applicable).
- **Hash verifies everything:** When a fixed artifact (tarball, repo commit, or manifest) is provided, a checksum (e.g. SHA-256) verifies that the analysis has not been altered post hoc. The Zenodo record provides a fixed DOI and version; use the Zenodo file checksums for the deposited materials. For repo-based reproduction, pin to a specific commit and document the hash in the replication report.

**Placeholder (if not yet automated):**  
*"One-command reproduction: TBD. See Zenodo record and toe-empirical-validation (or mqgt-analysis) for scripts. Hash: document the commit or Zenodo version used."*
