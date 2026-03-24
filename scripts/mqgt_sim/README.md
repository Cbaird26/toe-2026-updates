# MQGT-SCF illustrative simulations

## Top 10 visual sims (batch)

**Table + runner:** [TOP_10_VISUAL_SIMULATIONS.md](TOP_10_VISUAL_SIMULATIONS.md) · `python scripts/mqgt_sim/zora_top10_visual_runner.py` → `papers_sources/figures/zora_top10/*.png`

---

## Multi-channel exclusion plot (Phase II)

**Script:** `mqgt_multi_channel_exclusion_plot.py` — (m_Φ, sin²θ) plane with Eöt-Wash, Higgs invisible, QRNG prediction, viable island.

```bash
python scripts/mqgt_sim/mqgt_multi_channel_exclusion_plot.py --out-dir papers_sources/figures/mqgt_scf
```

Output: `papers_sources/figures/mqgt_scf/mqgt_scf_multi_channel_exclusion.png`. Used in the Phase II anchor paper and parameter card as parameter-space context.

---

## H2 paper-aligned stack

**Observable:** \(V/V_0=\exp(-\Gamma T\Delta x^2)\). Script: **`h2_visibility_stack.py`** — visibility vs \(\Gamma\), 2D exclusion landscape. See **[H2_SIMULATION_STACK.md](H2_SIMULATION_STACK.md)** for GKSL/HTML bridge.

```bash
python scripts/mqgt_sim/h2_visibility_stack.py
python scripts/mqgt_sim/h2_visibility_stack.py --save-dir papers_sources/figures/h2_stack
```

---

## `mqgt_phase4_lattice_demo.py`

**What it is:** A repo-native exploratory 2D lattice toy using only `numpy` + `matplotlib`. It evolves toy `phi_c` and `E` scalar fields on a periodic grid with explicit Euler updates, quartic local restoring terms, clipping, and an exploratory alignment coupling.

**What it is *not*:** Not the canonical H1/H2 evidence model, not a calibrated implementation of the hardened Phase II deformation law, and not a replacement for H2 interferometry as the primary falsification lane. The coupling term here is a visualization / research scaffold only.

**Run**

```bash
python scripts/mqgt_sim/mqgt_phase4_lattice_demo.py
python scripts/mqgt_sim/mqgt_phase4_lattice_demo.py --save-dir papers_sources/figures/phase4_lattice --no-show
```

**Outputs with `--save-dir`:**

- `mqgt_phase4_lattice_demo.png` — final `phi_c` / `E` field views plus metric traces
- `mqgt_phase4_lattice_demo_summary.json` — parameters, final metrics, and histories

**Parameters:** `--grid-size`, `--steps`, `--dt`, `--seed`, `--xi`, `--kappa`, `--m-c`, `--m-e`, `--save-dir`, `--no-show`.

---

## `mqgt_phase4b_symmetry_breaking_demo.py` (Phase IV-B)

**What it is:** A companion lattice toy that keeps Phase IV’s “pretty picture” role but addresses a known pedagogical artifact: Phase IV’s heuristic `coherence = exp(-mean|∇φ|)` **rewards a flat field**, so a relaxing uniform vacuum can look “highly coherent.” Phase IV-B uses **signed** `Φ_c` and `E`, a **double-well** local potential with explicit `λ_φ`, `λ_E`, **φ–E coupling** `-g φ E`, tilt `-ξ(φ + κ E)`, and **damped second-order** (symplectic Euler–style) dynamics on a periodic grid. Coherence is a **bounded** score in `[0,1]` that combines positive mean alignment with `Φ_c`, low variance, and low roughness—so **flat `φ≈0` does not score as maximal coherence**. Status strings (`FALSE_VACUUM_OR_QUIET`, `DOMAIN_COARSENING`, `PARTIAL_ALIGNMENT`, `ATTRACTOR_LOCKED`, etc.) are **toy phase labels** for exploration, not physical claims.

**What it is *not*:** Same invariant as Phase IV: **not** H1/H2 evidence, not a calibrated Phase II deformation law, not a substitute for **H2 interferometry** as the primary falsification lane. The Zora / `mqgt_sim` stack is an **execution and exploration** layer; preregistered H2 remains the main scientific discriminator.

**Run**

```bash
python scripts/mqgt_sim/mqgt_phase4b_symmetry_breaking_demo.py
python scripts/mqgt_sim/mqgt_phase4b_symmetry_breaking_demo.py --save-dir papers_sources/figures/phase4b_lattice --no-show
```

**Outputs with `--save-dir`:**

- `mqgt_phase4b_symmetry_breaking_demo.png` — final `Φ_c` / `E` snapshots plus mean traces and coherence / variance / roughness
- `mqgt_phase4b_symmetry_breaking_demo_summary.json` — parameters, final metrics, histories

**Parameters:** `--grid-size`, `--steps`, `--substeps` (integrator steps per recorded frame), `--dt`, `--seed`, `--xi`, `--kappa`, `--gamma`, `--g-couple`, `--lambda-phi`, `--lambda-e`, `--v-phi`, `--v-e`, `--no-default-injections`, `--inject-spec` (JSON list of Gaussian bumps keyed by frame index), `--save-dir`, `--no-show`.

Built-in default Gaussian **injections** (unless `--no-default-injections`) keep the lattice from trivially washing out to a quiet false vacuum; override or extend with `--inject-spec` (list of objects: `step`, `field` (`phi` or `E`), `x_norm`, `y_norm`, `magnitude`, optional `sigma_norm`).

---

## `mqgt_phase4b_parameter_sweep.py`

**What it is:** A repo-native parameter sweep for the existing Phase IV-B lattice model. It **reuses** `Phase4bLattice` from `mqgt_phase4b_symmetry_breaking_demo.py` exactly, runs multiple seeds over a grid of `xi`, `gamma`, and `g`, and saves a CSV plus heatmaps for **lock rate** and **mean final coherence**.

**Sweep policy:** This script intentionally runs with **no default injections**. Unlike the demo, it does not seed Gaussian bumps, so the outputs reflect the intrinsic behavior of the shared Phase IV-B dynamics across parameter space rather than injected pattern selection.

**What it is *not*:** Same invariant as the rest of the `mqgt_sim` stack: **not** H1/H2 evidence, not a calibrated Phase II deformation law, and not a substitute for **H2 interferometry** as the primary falsification lane.

**Run**

```bash
python scripts/mqgt_sim/mqgt_phase4b_parameter_sweep.py
python scripts/mqgt_sim/mqgt_phase4b_parameter_sweep.py \
  --xis "0.000,0.010,0.020" \
  --gammas "0.05,0.15" \
  --g-couples "0.00,0.18" \
  --seeds 3 \
  --steps 120 \
  --substeps 2 \
  --grid-size 32 \
  --outdir papers_sources/figures/phase4b_sweep
```

**Outputs with `--outdir`:**

- `phase4b_parameter_sweep_results.csv` — one row per `(xi, gamma, g, seed)` point with final metrics/status
- `summary.md` — compact sweep summary and per-`g` aggregate notes
- `lock_rate_g_*.png` — fraction of seeds ending in `ATTRACTOR_LOCKED`
- `mean_coherence_g_*.png` — mean final coherence at each `(xi, gamma)` point

**Current full-session bundle:** the repository currently tracks a sweep export in `phase_iv_b_sweep/` with `summary.md`, `phase_iv_b_sweep_results.csv`, and the current heatmaps. This bundle is exploratory only.

**Parameters:** `--xis`, `--gammas`, `--g-couples`, `--seeds`, `--steps`, `--substeps`, `--grid-size`, `--dt`, `--kappa`, `--lambda-phi`, `--lambda-e`, `--v-phi`, `--v-e`, `--outdir`.

---

## `fusion_zora_burn_figures.py`

**What it is:** 0D D–T power-balance model with Bosch–Hale reactivity, alpha heating, confinement, bremsstrahlung, and coherence scalar χ coupling (τ_E,eff, η_α). Generates baseline vs coherence-controlled temperature/Lawson trajectories and a burn outcome phase map vs (τ_E, χ). For fusion-zora draft figures.

**What it is *not*:** Not a reactor design tool; illustrative simulation only.

**Run**

```bash
python scripts/mqgt_sim/fusion_zora_burn_figures.py
python scripts/mqgt_sim/fusion_zora_burn_figures.py --out-dir papers_sources/figures/fusion_zora --include-existing
```

**Outputs:** `baseline_vs_controlled.png`, `phase_map.png`, optional `fusion-zora-populated.pdf` (add `--include-existing` to embed ppo_* figures if present).

**Parameters:** `--out-dir`, `--pdf`, `--include-existing`, `--pdf-only`.

**Live fusion console:** [docs/zora_fusion_console.html](../../docs/zora_fusion_console.html) — browser toy with sliders (n [0.1–3×10²⁰ m⁻³], τ_E [1–6 s], T₀ [5–25 keV], χ [0–1], Z_eff [1–2]), Zora toggle (τ_E,eff and η_α coupling), pulse Φc, T/Q strip charts. Uses a_tau=0.45, a_alpha=0.12. Illustrative only.

---

## GitHub Pages demos

- **`../../docs/zora_coherence.html`** — Kuramoto-style coherence visualization. Exploratory only; not a referee-safe physics artifact.
- **`../../docs/zora_fusion_console.html`** — 0D D–T fusion browser toy. Illustrative only.

---

## `zora_fields.html` (visual)

**What it is:** Standalone HTML5 canvas animation—no external libraries. Cyan waves (toy **Φ_c** motif) and gold/magenta geometric web (toy **E** motif). Metaphorical / aesthetic only; not a numerical field solve.

**Run:** Open in any browser (double-click or `open scripts/mqgt_sim/zora_fields.html` on macOS).

---

## `zora_gksl_collapse_demo.py`

**What it is:** Same GKSL two-level physics as below; **dark-background** plot of coherence `⟨σ_x⟩` for `E=0` vs `E=10` (matches the discussed notebook-style demo).

```bash
python scripts/mqgt_sim/zora_gksl_collapse_demo.py
```

---

## `mqgt_gksl_ethics_field_sim.py`

**What it is:** A minimal two-level open quantum system solved with the GKSL (Lindblad) master equation in [QuTiP](https://qutip.org/). The Lindblad rate is scaled by a parameter `E` (toy “ethical field” intensity). Higher `E` → faster loss of coherence (`⟨σ_x⟩` decays faster).

**What it is *not*:** Not calibrated to Phase II’s H2 floor (Γ_floor), QRNG, or any real experiment. It is scaffolding to explore how an **E-modulated dissipator** behaves numerically—aligned with companion interpretations; the referee-facing Phase II paper treats Φ_c and E as dynamical scalars and centers falsifiability on interferometry.

**Install**

```bash
pip install qutip numpy matplotlib
```

**Run**

```bash
cd /path/to/TOE
python scripts/mqgt_sim/mqgt_gksl_ethics_field_sim.py --save papers_sources/figures/gksl_e_field_toy.png --no-show
```

Or open an interactive plot:

```bash
python scripts/mqgt_sim/mqgt_gksl_ethics_field_sim.py
```

**Parameters:** `--e-baseline`, `--e-high`, `--steps`, `--t-max`, `--gamma-0`, `--kappa`.

## Results & GIF locally

- **Observed behavior** (baseline vs high E): [RESULTS_AND_ANIMATION_NOTES.md](RESULTS_AND_ANIMATION_NOTES.md)
- **Animated GIF:** `python scripts/mqgt_sim/zora_ethical_collapse_animation.py -o zora_ethical_collapse.gif` (needs Pillow; run locally if sandbox fails)

## Links

- Phase II submission: `papers_sources/MQGT-SCF_Phase_II_Submission_2026.tex`
- Status / archives: `docs/PHASE_II_SUBMISSION_STATUS_2026.md`
- **H1 QRNG pilot (collector + analysis):** `scripts/h1_qrng_pilot/README.md`
- **H2 bench runbook:** `docs/H2_PILOT_RUNBOOK.md`
