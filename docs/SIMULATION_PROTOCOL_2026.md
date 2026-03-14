# Simulation Protocol 2026 (Block 3)

**Purpose:** Define reproducible simulation protocols for MQGT-SCF. Per [REMAINING_TASKS_2026](REMAINING_TASKS_2026.md) Block 3, [PATHS_TO_CLOSED_VERDICT](PATHS_TO_CLOSED_VERDICT.md).

**Status:** Protocol spec; scripts/notebooks to be implemented. Closure requires `make reproduce` (or equivalent) to succeed in a clean environment.

---

## 1. Primordial Φc–E seeding

**Target:** Initialize field configurations with specified asymmetries; run 10⁴+ iterations; log outputs.

### Protocol

1. **Initial conditions:** Draw (Φc₀, E₀) from a specified distribution (e.g., small perturbation around vacuum) with fixed seed.
2. **Evolution:** Integrate the coupled Klein–Gordon equations (or discrete proxy) for Φc and E under the canonical potential.
3. **Iterations:** Run ≥ 10⁴ independent realizations (or timesteps) with logged seed.
4. **Outputs:** Log final (Φc, E), convergence metrics, and checksums.

### Artifact

- **Script:** `scripts/primordial_seeding.py` or equivalent
- **Config:** Fixed parameter set (λ_c, λ_E, κ, ξ, etc.) from core spine
- **Log:** `results/primordial_seeding_YYYYMMDD.log` with seed, iteration count, summary stats

### Verification gate

Fresh clone + `./scripts/run_primordial_seeding.sh --seed 42` produces deterministic (or documented stochastic) output matching reference.

---

## 2. Zora recursive evolution

**Target:** Evolve discrete Φc–E dynamics to coherence saturation; log step count.

### Protocol

1. **State variables:** Discretized Φc(x), E(x) or lattice proxy obeying the unified Lagrangian (or discrete approximation).
2. **Recursion:** Step until coherence metric saturates (e.g., |ΔΦc| < ε) or max steps reached.
3. **Logging:** Step count, final coherence, E-gradient at exit.

### Artifact

- **Script:** In toe-empirical-validation or zoraasi-suite
- **Deterministic seed:** Document seed for reproducibility
- **Output:** `results/zora_evolution_run_*.json` with step_count, coherence_final, E_gradient

### Verification gate

Same seed yields same step count and final state (within floating-point tolerance).

---

## 3. Jhāna attractor simulations

**Target:** Confirm limit cycles in coupled Φc–E potential; match analytic fixed point Φc* = v(1 + ξ/λc tanh(E/C)).

### Protocol

1. **Coupled potential:** Use canonical V(Φc, E) with teleological source ξ.
2. **Steady state:** Integrate to t → ∞ (or large t); record Φc*, E*.
3. **Comparison:** Compute |Φc*_sim − Φc*_analytic| / Φc*_analytic; require < 1% for small ξ.

### Artifact

- **Notebook:** `notebooks/jhana_attractor.nb` or `field_evolution.nb`
- **Reference:** Analytic Φc* from [Zora_GKSL_Jhana_Addendum_2026.tex](../papers_sources/Zora_GKSL_Jhana_Addendum_2026.tex)
- **Output:** Plot of trajectory; table of (Φc*_sim, Φc*_analytic, relative error)

### Verification gate

Output matches analytic fixed point to within stated tolerance (e.g., 0.1%).

---

## 4. Docker / one-command reproduction

**Target:** `make reproduce` or `./scripts/run_all_simulations.sh` succeeds in clean environment.

### Artifacts

- **Dockerfile:** (optional) Image with deps; or `requirements.txt` + venv
- **Makefile:** `make reproduce` runs primordial + Zora + jhāna in sequence
- **README:** Document exact command and expected outputs

### Verification gate

`git clone ... && make reproduce` (or equivalent) produces all expected artifacts; no manual steps beyond clone + single command.

---

## 5. Falsifier

**Block 3 does not close if:** Notebooks fail to run, outputs drift from reference, or `make reproduce` fails in a clean environment.

---

## Cross-links

- [REMAINING_TASKS_2026](REMAINING_TASKS_2026.md) Block 3
- [PATHS_TO_CLOSED_VERDICT](PATHS_TO_CLOSED_VERDICT.md) Block 3
- [REPLICATION_LADDER](REPLICATION_LADDER.md)
- [Zora_GKSL_Jhana_Addendum_2026.tex](../papers_sources/Zora_GKSL_Jhana_Addendum_2026.tex)
