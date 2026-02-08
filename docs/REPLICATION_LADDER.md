# Replication Ladder

A public checklist to make replication **social**, not just technical. Don't believe us—re-run us. Then go one step further.

**Zenodo:** [zenodo.org/records/18511550](https://zenodo.org/records/18511550)  
**Falsification Packet:** [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md)

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
Design a test in which the deformation is *absent* (e.g. synthetic data generated under standard QM, or a control condition). Run the same analysis pipeline; the framework should not claim a detection (or should assign negligible posterior weight to the deformation). Document the null setup and the result. This is the strongest check against false positive or confirmation bias.

---

## Credit line

**First independent lab (or researcher) to complete rungs (a)–(b) and submit a short replication report gets credited in the next version of the paper (e.g. v217).** Symbolic; no monetary commitment. The report should include: run environment, command(s), hash or Zenodo version, and a one-paragraph summary of agreement or deviation.

---

## Pre-registration (QRNG)

To strengthen the QRNG channel against expectancy effects, experimenter degrees of freedom, and p-hacking: **pre-register at least one new QRNG protocol variant** that specifies in advance the outcome labeling, sample size, analysis plan, and decision rule. Link to OSF or equivalent when created.

**Pre-registration template:** TBD. (When available, link will be added here.)

---

## Replication report template (optional)

When submitting a replication, include:

- **Environment:** OS, Python/R version, key packages and versions.
- **Artifact:** Zenodo DOI and version, or repo commit hash, used for scripts and data.
- **Commands:** Exact one-liner or script invocation that produced your run.
- **Figures / results:** Brief description: reproduced / not reproduced; if not, where and why they differ.
- **Rung(s) completed:** (a)–(e) as above.
- **Deviation from paper:** Any substantive difference in setup, prior, or interpretation.

This can be submitted as an issue, a short PDF, or an OSF pre-registration supplement, as agreed with the authors.
