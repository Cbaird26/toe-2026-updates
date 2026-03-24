# MQGT-SCF Phase II figures

## Multi-channel exclusion plot

**File:** `mqgt_scf_multi_channel_exclusion.png`

Parameter plane (m_Φ, sin²θ_hΦ) with three constraint channels:

- **Eöt-Wash fifth-force** — excluded region from short-range gravity tests
- **Higgs invisible decay** — excluded region (BR < 0.11)
- **QRNG prediction** — θ ≈ 3.7×10⁻⁶ → sin²θ ≈ 1.4×10⁻¹¹
- **H2 Phase-0 nuisance floor** — δ_tot = 1.15×10⁻³
- **Viable island** — unexcluded region (m_Φ ~ 10³–10⁵ eV, sin²θ ~ 10⁻³¹–10⁻³⁶)

**Regenerate:**

```bash
python scripts/mqgt_sim/mqgt_multi_channel_exclusion_plot.py --out-dir papers_sources/figures/mqgt_scf
```

Used in: Phase II anchor paper, parameter card appendix, multi-channel constraint discussion.

## Concept figure

**File:** `mqgt_scf_phi_e_gksl_concept.png`

Conceptual artwork for the Anchor / Phase II explanatory stack: Φc, E, and GKSL measurement channel feeding a stabilized-reality motif.

- Explanatory / conceptual only
- Not a referee-safe evidence figure
- Does not replace `papers_sources/mqgt-scf-diagram.png`
