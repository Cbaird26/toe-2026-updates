# Replication Ladder

A public checklist to make replication **social**, not just technical. Don't believe us—re-run us. Then go one step further.

**Zenodo:** [zenodo.org/records/18511550](https://zenodo.org/records/18511550)  
**Falsification Packet:** [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md)

---

## One-command replication ladder (single channel)

Use this for a minimal "run once and compare" replication. The primary channel for this ladder is **QRNG**.

1. **Clone repo:**  
   `git clone https://github.com/Cbaird26/toe-empirical-validation.git && cd toe-empirical-validation`

2. **Verify artifact integrity:** If using Zenodo-supplied data or scripts, run checksum verification before any analysis. Example:
   ```bash
   sha256sum -c zenodo_manifest.sha256
   ```
   (Or `shasum -a 256 -c zenodo_manifest.sha256` on macOS.) Document the Zenodo version and manifest so replicators don't argue about corrupted downloads or drift. **If no manifest is supplied in the repo or Zenodo package, skip this step and document that in your replication report.**

3. **Pin and run:**  
   Record `git rev-parse HEAD`, then run the **canonical one-command** (must exist in this repo):
   ```bash
   ./scripts/run_all.sh --channel qrng --seed 0 --out artifacts/
   ```
   If the repo uses a different entrypoint, the README must document the single equivalent command; replicators use that command and no other. No ad hoc scripts for the official ladder.

4. **Compare (concrete):**  
   Check that the run produced the expected artifacts and that they match the reference (Zenodo or paper) within stated tolerances.
   - **Expected outputs:** e.g. `artifacts/fig_1.png`, `artifacts/constraints.json`, `artifacts/posterior_samples.npz` (or the filenames documented in the repo README).
   - **Comparison rules:**  
     - Figures: pixel diff or SSIM within tolerance (e.g. seed variance only; document in repo).  
     - Numerics: same summary stats within floating-point epsilon (e.g. 1e-10) for the same seed; or document allowed variance for different seeds.  
   - Document any deviation (file missing, tolerance exceeded) in your replication report.
   - **Optional:** In the spine repo, run `./scripts/compare_artifacts.sh artifacts/ reference_artifacts/` for automated comparison (see toe-empirical-validation README for tolerances).

**It lives or dies here (QRNG channel):** If a well-powered, pre-registered QRNG experiment under the same operational definition of E finds no deviation from standard randomness, the deformation is excluded at the stated confidence level (see [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md#qrng-falsification-claim)). Reproduction confirms that the analysis pipeline and constraints match the paper; independent replication of the experiment is the falsification test.

**E is fixed for this ladder:** The operational definition of E (outcome labeling) is given in [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md) and implemented in this repo (toe-empirical-validation). If you change E labeling, you are running a different experiment; the "it lives or dies here" criterion applies only when E is defined as in the packet and repo.

---

## Five rungs (in order)

**(a) Run the scripts.**  
Obtain the reproducibility package (Zenodo deposit or linked repo, e.g. toe-empirical-validation). Install dependencies, run the analysis scripts, and confirm they complete without error. Document environment (OS, interpreter version, key packages) and the exact command(s) used.

**(b) Reproduce the figures.**  
Using the same data (or Zenodo-supplied data) and the same priors/likelihoods, regenerate the figures reported in the paper. Compare to the published figures; note any deviation (e.g. from different random seeds or platform-specific numerics).

**(c) Swap priors.**  
Re-run the analysis with at least one alternative prior (e.g. different scale or support for the deformation parameter). Report whether conclusions are robust or prior-sensitive. This tests whether the claimed constraints are stable under reasonable prior choice.

**(d) Add one new constraint channel.**  
Introduce one additional observable or dataset (e.g. another QRNG protocol, a different fifth-force bound, or a cosmology observable) into the likelihood. Fit the model with the extended constraint set. Report whether the framework accommodates the new channel or becomes overconstrained.

**(e) Attempt an adversarial null test.**  
Design a test in which the deformation is *absent* (e.g. synthetic data generated under standard QM, or a control condition). Run the same analysis pipeline; the framework should not claim a detection (or should assign negligible posterior weight to the deformation). Document the null setup and the result. This is the strongest check against false positive or confirmation bias. **Synthetic null fixture:** This repo (toe-empirical-validation) should ship a canonical null dataset (or generator) that produces data under standard QM (no E deformation). Replicators run the same pipeline on this fixture; the framework must return "no effect." Example: `./scripts/run_all.sh --channel qrng --null-fixture --seed 0 --out artifacts_null/`. Null fixture details: see toe-empirical-validation README.

---

## Credit line

**First independent lab (or researcher) to complete rungs (a)–(b) and submit a short replication report gets credited in the next version of the paper (e.g. v217).** Symbolic; no monetary commitment. The report should include: run environment, command(s), hash or Zenodo version, and a one-paragraph summary of agreement or deviation.

---

## Pre-registration (QRNG)

To strengthen the QRNG channel against expectancy effects, experimenter degrees of freedom, and p-hacking: **pre-register at least one new QRNG protocol variant** that specifies in advance the outcome labeling, sample size, analysis plan, and decision rule. Link to OSF or equivalent when created.

**Pre-registration template (v0):** See **Appendix A** below. Register at OSF (osf.io) or AsPredicted before data collection and include the registration link in your replication report.

---

## Environment (replicators must report)

- **OS:** e.g. macOS 14.x, Ubuntu 22.04
- **CPU/GPU:** optional but helpful for numeric variance
- **Python:** `python --version` (e.g. 3.10.x)
- **Deps:** `pip freeze > requirements_replication.txt` or `conda env export > environment.yml`
- **Container (if used):** image name + digest/hash (e.g. `docker images --digests`)
- **One-liner to recreate:** e.g. `docker run --rm -v $(pwd)/artifacts:/out <image> ./scripts/run_all.sh --channel qrng --seed 0 --out /out`

---

## Replication report template (optional)

When submitting a replication, include:

- **Environment:** OS, Python/R version, key packages and versions (or use the Environment section above).
- **Artifact:** Zenodo DOI and version, or repo commit hash, used for scripts and data.
- **Commands:** Exact one-liner or script invocation that produced your run.
- **Figures / results:** Brief description: reproduced / not reproduced; if not, where and why they differ.
- **Rung(s) completed:** (a)–(e) as above.
- **Deviation from paper:** Any substantive difference in setup, prior, or interpretation.

This can be submitted as an issue, a short PDF, or an OSF pre-registration supplement, as agreed with the authors.

---

## Appendix A: QRNG pre-registration template (v0)

Use this template to pre-register a QRNG experiment that tests the MQGT-SCF Born-rule deformation (E-weighted outcomes). Pre-registration reduces p-hacking and expectancy effects. Register at OSF (osf.io) or AsPredicted before data collection.

### 1. Hypothesis

We will test whether the distribution of QRNG outcomes deviates from standard (uniform) randomness when outcomes are labeled according to the operational definition of E in the falsification packet. Null: no deviation. Alternative: deviation consistent with the E-weighted deformation at the stated scale.

### 2. Operational definition of E

- E-labeling rule: Each outcome is assigned E via **`label_E`** in **`code/e_labeling.py`** in toe-empirical-validation. Pin the commit hash when replicating; spine commit for this ladder: **`56578d5`** (full SHA in [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md) §1).
- **If you change E labeling, you are running a different experiment.** Replication of the ladder uses the same E definition as in the falsification packet and the repo.

### 3. Design

- QRNG source: hardware model (or software RNG + seeding protocol)
- Sample size: N = [number], chosen by [power analysis / fixed protocol]
- Blocks/trials: [structure]
- Control condition (if any): [e.g. synthetic null with no E bias]

### 4. Analysis plan

- Primary test: [test statistic, null distribution, alpha]
- Decision rule: We will conclude [support for deformation / no deviation] if [criterion].
- No optional stopping; no post hoc change to E labeling or analysis.

### 5. Data and code

- Data: will be deposited at Zenodo/OSF with DOI
- Code: repo + commit hash or Zenodo supplement

### 6. Deviations

Any deviation from this pre-registration will be reported in the final report and justified.

**Registration link:** [paste OSF/AsPredicted URL here]
