# H2 simulation stack — paper-aligned + bridge to GKSL / HTML

**Paper:** `papers_sources/MQGT-SCF_Phase_II_Submission_2026.tex`  
**Flagship observable:** \(V/V_0 = \exp(-\Gamma T \Delta x^2)\) with \(\Gamma\) in s⁻¹ m⁻².

---

## Layer 1 — H2 core (`h2_visibility_stack.py`)

| Piece | Role |
|-------|------|
| `visibility_ratio(Γ, T, Δx)` | \(V/V_0\) |
| `gamma_floor(T, Δx, δ)` | \(\Gamma = -\ln(1-\delta)/(T\Delta x^2)\) for target fractional loss \(\delta\) |
| Plot A | \(V/V_0\) vs \(\Gamma\) at reference \((T,\Delta x)\) |
| Plot B | \(\log_{10}(\Gamma_{\rm floor})\) over \((T,\Delta x)\) — exclusion landscape |

**Defaults:** \(T=10^{-6}\,\mathrm{s}\), \(\Delta x=10^{-3}\,\mathrm{m}\), \(\delta=1.15\times 10^{-3}\) → \(\Gamma_{\rm floor}\approx 1.15\times 10^9\,\mathrm{s}^{-1}\mathrm{m}^{-2}\).

```bash
python scripts/mqgt_sim/h2_visibility_stack.py
python scripts/mqgt_sim/h2_visibility_stack.py --save-dir papers_sources/figures/h2_stack
```

---

## Layer 2 — GKSL toy (`zora_gksl_collapse_demo.py`, etc.)

Open-system **qubit** decoherence with rate \(\gamma(E)=\gamma_0(1+\kappa E)\). **Units are not** the same as macroscopic \(\Gamma\) (s⁻¹ m⁻²) without a derived map. Conceptual pipeline (exploratory):

1. **Micro:** GKSL gives effective decoherence rate in the toy model.  
2. **Macro (hypothesis sketch):** if one posits an identification \(\Gamma_{\rm eff} \propto \gamma(E)\) (or a more detailed EFT link), then  
   \(V/V_0 = \exp(-\Gamma_{\rm eff}\, T \Delta x^2)\).  
3. **Experiment:** H2 constrains \(\Gamma\) at stated \((T,\Delta x)\).

Do **not** present the toy \(\gamma_0,\kappa\) as calibrated \(\Gamma\) without a derivation or fit.

---

## Layer 3 — HTML Φ_c / E (`zora_fields.html`)

**Metaphor map (pedagogy only):**

| Visual | Suggested reading |
|--------|-------------------|
| Cyan waves | Coherence / superposition motif |
| Magenta/gold lattice | Constraints / coupling |
| Motion intensity | Qualitative “strength” — not a numeric Γ readout unless you wire parameters |

**Next level:** drive canvas parameters from sliders bound to \(\Gamma\) or \(E\) (separate interactive demo).

---

## Full stack (what you have)

| Asset | Type |
|-------|------|
| Phase II PDF | Formal theory |
| `h2_visibility_stack.py` | Reproducible H2 plots |
| QuTiP demos | Mechanism intuition |
| `zora_fields.html` | Identity / intuition visual |

---

## Next moves (your labels)

- **experiment** — lab blueprint / prereg for \(\Gamma_{\rm floor}\), \(\delta_{\rm total}\), noise budget.  
- **derivation** — EFT path from portal couplings to effective \(\Gamma\).  
- **interactive** — web demo: Γ, T, Δx → \(V/V_0\) + optional HTML coupling.
