# Canonical ZoraASI Top 10 Simulations

Physics-first hybrid set: four interactive demos plus six reproducible batch artifacts.
The public landing page is [zora_top10_simulations.html](https://cbaird26.github.io/toe-2026-updates/zora_top10_simulations.html).

| Rank | Simulation | Category | Command | Primary output | Public link | Disclaimer level |
|---|---|---|---|---|---|---|
| 1 | H2 Visibility Explorer | Interactive | `open docs/h2_visibility_explorer.html` | `docs/h2_visibility_explorer.html` | [H2 Visibility Explorer](https://cbaird26.github.io/toe-2026-updates/h2_visibility_explorer.html) | `Paper-aligned illustrative calculator` |
| 2 | MQGT-SCF GKSL Dynamics Viewer | Interactive | `open docs/mqgt_scf_gksl_dynamics_viewer.html` | `docs/mqgt_scf_gksl_dynamics_viewer.html` | [GKSL Dynamics Viewer](https://cbaird26.github.io/toe-2026-updates/mqgt_scf_gksl_dynamics_viewer.html) | `Exploratory toy; not calibrated to Γ_floor` |
| 3 | Zora Fusion Console | Interactive | `open docs/zora_fusion_console.html` | `docs/zora_fusion_console.html` | [Fusion Console](https://cbaird26.github.io/toe-2026-updates/zora_fusion_console.html) | `Illustrative 0D burn toy` |
| 4 | MQGT-SCF Topological Phase Space | Interactive | `open docs/phase-space.html` | `docs/phase-space.html` | [Topological Phase Space](https://cbaird26.github.io/toe-2026-updates/phase-space.html) | `Exploratory only` |
| 5 | H2 visibility stack | Batch | `python scripts/mqgt_sim/h2_visibility_stack.py --save-dir papers_sources/figures/zora_top10/h2_visibility_stack --no-show` | `papers_sources/figures/zora_top10/h2_visibility_stack/h2_visibility_vs_gamma.png` | [Public artifact](https://cbaird26.github.io/toe-2026-updates/assets/top10/h2_visibility_stack.png) | `Paper-aligned reproducible figure` |
| 6 | Multi-channel exclusion plot | Batch | `python scripts/mqgt_sim/mqgt_multi_channel_exclusion_plot.py --out-dir papers_sources/figures/zora_top10/mqgt_scf --no-show` | `papers_sources/figures/zora_top10/mqgt_scf/mqgt_scf_multi_channel_exclusion.png` | [Public artifact](https://cbaird26.github.io/toe-2026-updates/assets/top10/multi_channel_exclusion.png) | `Parameter-space context; not a direct discovery claim` |
| 7 | E-modulated GKSL collapse | Batch | `python scripts/mqgt_sim/zora_gksl_e_modulated_collapse.py --save papers_sources/figures/zora_top10/h2_stack/e_modulated_collapse.png --no-show` | `papers_sources/figures/zora_top10/h2_stack/e_modulated_collapse.png` | [Public artifact](https://cbaird26.github.io/toe-2026-updates/assets/top10/e_modulated_gksl_collapse.png) | `Exploratory QuTiP simulation` |
| 8 | Phase IV-B symmetry-breaking lattice | Batch | `python scripts/mqgt_sim/mqgt_phase4b_symmetry_breaking_demo.py --save-dir papers_sources/figures/zora_top10/phase4b_demo --no-show --grid-size 48 --steps 180 --substeps 2` | `papers_sources/figures/zora_top10/phase4b_demo/mqgt_phase4b_symmetry_breaking_demo.png` | [Public artifact](https://cbaird26.github.io/toe-2026-updates/assets/top10/phase4b_symmetry_breaking.png) | `Exploratory only` |
| 9 | Phase IV-B parameter sweep | Batch | `python scripts/mqgt_sim/mqgt_phase4b_parameter_sweep.py --outdir papers_sources/figures/zora_top10/phase4b_sweep --xis 0.000,0.010,0.020 --gammas 0.05,0.15,0.20 --g-couples 0.18 --seeds 2 --steps 120 --substeps 2 --grid-size 32` | `papers_sources/figures/zora_top10/phase4b_sweep/mean_coherence_g_0.180.png` | [Public artifact](https://cbaird26.github.io/toe-2026-updates/assets/top10/phase4b_parameter_sweep.png) | `Exploratory sweep summary` |
| 10 | Fusion burn figures | Batch | `python scripts/mqgt_sim/fusion_zora_burn_figures.py --out-dir papers_sources/figures/zora_top10/fusion_zora` | `papers_sources/figures/zora_top10/fusion_zora/baseline_vs_controlled.png` | [Public artifact](https://cbaird26.github.io/toe-2026-updates/assets/top10/fusion_burn_figures.png) | `Illustrative only; not a reactor design tool` |

## Canonical batch command

To regenerate the six batch artifacts and their public docs-side copies in one pass:

```bash
cd ~/Downloads/TOE
python scripts/mqgt_sim/zora_top10_visual_runner.py
python scripts/mqgt_sim/zora_top10_visual_runner.py --skip-qutip
```

This runner writes:

- Batch artifacts: `papers_sources/figures/zora_top10/`
- Public thumbnails and representative artifact copies: `docs/assets/top10/`
- Batch-suite poster: `papers_sources/figures/zora_top10/batch_suite_mosaic.png`

## Deliberate exclusions

- `zora_closure_explorer.html` remains public and linked from the dashboard, but it is a closure/specification map, not a simulation.
- `zora_coherence.html`, `attention.html`, and `nbody.html` remain public exploratory demos, but they are outside the canonical top 10.
