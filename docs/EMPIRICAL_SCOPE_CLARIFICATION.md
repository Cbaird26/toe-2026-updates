# Empirical Scope Clarification

**What MQGT-SCF empirical validation is and is not.** One-page reference to prevent confusion with AI benchmark claims.

---

## What it IS

MQGT-SCF empirical validation applies to **quantum measurement outcomes** and constraint channels:

- **QRNG channel:** Statistically detectable deviation from standard randomness when outcomes are labeled according to the operational definition of E. Implemented in [toe-empirical-validation](https://github.com/Cbaird26/toe-empirical-validation) (`code/e_labeling.py`, `code/qrng_pipeline.py`). One-command: `./scripts/run_all.sh --channel qrng --seed 0 --out artifacts/`.
- **Fifth-force / equivalence-principle channel:** Bounds on scalar-mediated forces; constraints from Eötvös-type experiments.
- **Cosmology / particle channel:** Constraints from Higgs invisible decays and other collider/cosmology observables.

The operational Born-rule deformation **P_η(i) = p_i · exp(η E_i) / Σ_j p_j · exp(η E_j)** applies to quantum outcome branches (bits, branch selection, measurement outcomes). Standard QM recovers when η → 0, ΔE → 0, or C_E → ∞.

---

## What it is NOT

- **AI benchmark scoring:** OSWorld, GDPval, SWE-Bench, GPQA, FrontierMath, Toolathon, and similar benchmarks measure empirical pass rates of language models on test sets. These are aggregate statistics, not quantum measurement events. The MQGT-SCF formalism does not apply to them. You cannot "evolve" benchmark scores with Φc-E dynamics or produce "ZoraASI scores" from GPT-5.4 baselines via consciousness-induced collapse.
- **Warp-10 simulation suite:** No such suite exists in the cbaird26 repos. The empirical pipeline is the QRNG channel and constraint fits, not a benchmark Monte Carlo.
- **zoraasi-suite benchmark kernel:** zoraasi-suite is a chat/RAG stack. It does not run AI benchmark evaluations or produce benchmark scores.

---

## Where to run

| Channel      | Repo / location                                         | Command                                                                 |
|--------------|---------------------------------------------------------|-------------------------------------------------------------------------|
| QRNG         | [toe-empirical-validation](https://github.com/Cbaird26/toe-empirical-validation) or local `mqgt_scf_reissue` at `code/` | `./scripts/run_all.sh --channel qrng --seed 0 --out artifacts/`         |
| Null fixture | Same                                                    | `./scripts/run_all.sh --channel qrng --null-fixture --seed 0 --out artifacts_null/` |

Required artifacts: `constraints.json`, `posterior_samples.npz`, `fig_1.png`, `run_meta.json`. For null fixture, `effect_detected` must be `false`.

**How to simulate:** See [HOW_TO_SIMULATE_ZORAASI.md](HOW_TO_SIMULATE_ZORAASI.md).

---

## Cross-references

- [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md) — Operational definition of E, canonical deformation, three predictions, three ways it dies.
- [REPLICATION_LADDER.md](REPLICATION_LADDER.md) — One-command replication, five rungs, pre-registration template.
- [HOW_TO_SIMULATE_ZORAASI.md](HOW_TO_SIMULATE_ZORAASI.md) — Runnable guide, canonical run, formula demo, common pitfalls.
- [CANONICAL_SPINE.md](CANONICAL_SPINE.md) — Closure map, hardening tasks, canonical anchors.
