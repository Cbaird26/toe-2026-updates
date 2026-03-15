# QRNG Pre-Registration OSF Draft 2026

**Ready for OSF/AsPredicted paste.** Christopher Michael Baird | Baird–ZoraASI Collaboration | March 2026

---

## Copy below for OSF registration

---

### 1. Hypothesis

We will test whether the distribution of QRNG outcomes deviates from standard (uniform) randomness when outcomes are labeled according to the operational definition of E in the MQGT-SCF falsification packet. Null: no deviation. Alternative: deviation consistent with the E-weighted Born-rule deformation at the stated scale.

### 2. Operational definition of E

- E-labeling rule: Each outcome is assigned E via **`label_E`** in **`code/e_labeling.py`** in toe-empirical-validation (Cbaird26/toe-empirical-validation). Pin the commit hash when replicating; current spine commit: see [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md) §1.
- **If you change E labeling, you are running a different experiment.** Replication of the ladder uses the same E definition as in the falsification packet and the repo.

### 3. Design

- **QRNG source:** ANU Quantum Random Numbers API (https://qrng.anu.edu.au/contact/api-documentation/)
- **Sample size:** N = 50,000,000 bits (or 100,000,000 for ultra-large sensitivity), chosen by fixed protocol (long-baseline stability run)
- **Blocks/trials:** 100 blocks × 500,000 bits per block (or 1000 blocks × 100,000 bits); block order randomized
- **Control condition:** Synthetic null fixture (`run_all.sh --null-fixture`) to confirm pipeline returns no effect under standard randomness

### 4. Analysis plan

- **Primary test:** Chi-squared or binomial test on block-level p_hat; permutation test on block means; alpha = 0.05
- **Decision rule:** We will conclude [support for deformation] if p < 0.05 and effect direction consistent with E-weighting; [no deviation] otherwise. No optional stopping; no post hoc change to E labeling or analysis.
- **Sensitivity:** 50M bits → ~10⁻⁴ bias detection (OOM); 100M bits → ~10⁻⁵ (OOM)

### 5. Data and code

- **Data:** Will be deposited at Zenodo/OSF with DOI
- **Code:** toe-empirical-validation repo + commit hash; Zenodo supplement if bundled

### 6. Deviations

Any deviation from this pre-registration will be reported in the final report and justified.

**Registration link:** [paste OSF/AsPredicted URL here]

---

## Notes

- Register at https://osf.io or https://aspredicted.org before data collection
- Update commit hash in §2 to match run
- See [NEXT_QRNG_RUN_50M_2026.md](NEXT_QRNG_RUN_50M_2026.md) for cost and timeline
