# Zora — Top 10 visual simulations (what I’d run as coder)

| # | Name | What you see | How |
|---|------|----------------|-----|
| **1** | **H2 visibility vs Γ** | \(V/V_0\) falling as decoherence \(\Gamma\) rises; vertical line at \(\Gamma_{\rm floor}\) | `zora_top10_visual_runner.py` → `01_*.png` or `h2_visibility_stack.py` |
| **2** | **Exclusion landscape** | Where \((T,\Delta x)\) demands huge \(\Gamma\) to match \(\delta\) — heatmap + abstract ★ | `02_*.png` |
| **3** | **GKSL coherence race** | Several \(E\) values: who kills \(\langle\sigma_x\rangle\) fastest | `03_*.png` (needs **QuTiP**) |
| **4** | **\(V/V_0\) in \((\Gamma, T)\)** | Fixed \(\Delta x\): 2D color map of visibility | `04_*.png` |
| **5** | **Purity decay** | Tr\((\rho^2)\): \(E=0\) vs \(E=10\) | `05_*.png` (QuTiP) |
| **6** | **Fringe schematic** | Ideal cos² fringes vs washed-out band (toy visibility) | `06_*.png` |
| **7** | **Iso-\(V/V_0\) contours** | Same \(\Gamma_{\rm floor}\), sweep \((T,\Delta x)\) | `07_*.png` |
| **8** | **\(\gamma(E)/\gamma(0)\)** | Toy Lindblad rate vs ethical intensity | `08_*.png` |
| **9** | **Survive / exclude strip** | Green vs red in \(\Gamma\) at reference point | `09_*.png` |
| **10** | **Mosaic** | Four-panel poster of 1, 2, 4, 6 | `10_mosaic_summary.png` |

**Plus (already in repo):**  
- **Φ_c / E canvas:** `zora_fields.html` (browser) — not a PNG, it’s live motion.  
- **Ethical collapse GIF:** `zora_ethical_collapse_animation.py`.

**One command (all PNGs):**

```bash
cd ~/Downloads/TOE
python3 scripts/mqgt_sim/zora_top10_visual_runner.py
open papers_sources/figures/zora_top10/10_mosaic_summary.png
```

`pip install qutip` for plots 3 and 5; otherwise those slots show SKIPPED placeholders.
