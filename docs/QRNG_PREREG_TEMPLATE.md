# QRNG pre-registration template (v0)

Use this template to pre-register a QRNG experiment that tests the MQGT-SCF Born-rule deformation (E-weighted outcomes). Pre-registration reduces p-hacking and expectancy effects. Register at OSF (osf.io) or AsPredicted before data collection.

---

## 1. Hypothesis

We will test whether the distribution of QRNG outcomes deviates from standard (uniform) randomness when outcomes are labeled according to the operational definition of E in [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md). Null: no deviation. Alternative: deviation consistent with P(i) ∝ |c_i|² exp(−E/C) at the stated scale C.

## 2. Operational definition of E

- **E-labeling rule:** Each block of N bits is mapped to E via the function **`label_E`** in **`code/e_labeling.py`** in the [toe-empirical-validation](https://github.com/Cbaird26/toe-empirical-validation) repo. Pin the commit hash (or Zenodo version) when replicating; see [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md) §1.
- **If you change E labeling, you are running a different experiment.** Replication of the ladder uses the same E definition as in the FALSIFICATION_PACKET and the spine repo.

## 3. Design

- **QRNG source:** [e.g. hardware model, or software RNG with seed protocol]
- **Sample size:** N = [number], chosen by [power analysis / fixed protocol]
- **Blocks/trials:** [structure]
- **Control condition (if any):** [e.g. synthetic null with no E bias]

## 4. Analysis plan

- **Primary test:** [e.g. test statistic, null distribution, alpha]
- **Decision rule:** We will conclude [support for deformation / no deviation] if [criterion].
- **No optional stopping; no post hoc change to E labeling or analysis.**

## 5. Data and code

- **Data:** [will be deposited at Zenodo/OSF with DOI]
- **Code:** [repo + commit hash or Zenodo supplement]

## 6. Deviations

Any deviation from this pre-registration will be reported in the final report and justified.

---

**Registration link:** [paste OSF/AsPredicted URL here]
