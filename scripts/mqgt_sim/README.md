# MQGT-SCF illustrative simulations

## Top 10 visual sims (batch)

**Table + runner:** [TOP_10_VISUAL_SIMULATIONS.md](TOP_10_VISUAL_SIMULATIONS.md) · `python scripts/mqgt_sim/zora_top10_visual_runner.py` → `papers_sources/figures/zora_top10/*.png`

---

## H2 paper-aligned stack

**Observable:** \(V/V_0=\exp(-\Gamma T\Delta x^2)\). Script: **`h2_visibility_stack.py`** — visibility vs \(\Gamma\), 2D exclusion landscape. See **[H2_SIMULATION_STACK.md](H2_SIMULATION_STACK.md)** for GKSL/HTML bridge.

```bash
python scripts/mqgt_sim/h2_visibility_stack.py
python scripts/mqgt_sim/h2_visibility_stack.py --save-dir papers_sources/figures/h2_stack
```

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
