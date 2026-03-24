# Phase IV-B parameter sweep summary

This sweep reuses the current `Phase4bLattice` dynamics exactly and runs without default injections so the maps reflect intrinsic lattice behavior.

- xis: [0.0, 0.01, 0.02]
- gammas: [0.05, 0.15, 0.2]
- g_couples: [0.18]
- seeds per point: 2
- steps: 120
- substeps: 2
- grid_size: 32
- dt: 0.04
- csv: `phase4b_parameter_sweep_results.csv`

## g = 0.180

- mean coherence across all seeds/points: 0.327
- lock fraction across all seeds/points: 0.000
- heatmap: `lock_rate_g_0.180.png`
- heatmap: `mean_coherence_g_0.180.png`

