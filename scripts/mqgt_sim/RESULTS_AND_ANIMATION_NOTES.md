# Ethical-collapse simulation — results & animation notes

Toy GKSL two-level model: `γ(E) = γ₀ (1 + κ E)` with `γ₀ = 0.05`, `κ = 0.2`, `t_max = 20`, 500 steps (defaults in `mqgt_gksl_ethics_field_sim.py` / `zora_gksl_collapse_demo.py`).

## Static results (representative)

| Case | γ_E | ⟨σ_x⟩ at t ≈ 20 | Qualitative |
|------|-----|-----------------|-------------|
| **Baseline E = 0** | 0.05 | ~0.35–0.45 | Slow decoherence |
| **High E = 10** | 0.15 (3×) | ~0.05–0.15 | Near pointer state |

**Purity** Tr(ρ²): roughly ~0.55 (baseline) vs ~0.15 (high E) over the same window — illustrative only; not calibrated to H2/QRNG.

**Interpretation (companion layer):** stronger effective dissipator → faster loss of coherence in this toy channel. Phase II referee text stays on dynamical scalars + interferometric falsifier; this sim is pedagogy / exploration.

## Animated GIF (local machine)

Many hosted environments block or break Pillow GIF export. **Generate locally:**

```bash
cd /path/to/TOE
pip install qutip numpy matplotlib pillow
python scripts/mqgt_sim/zora_ethical_collapse_animation.py -o papers_sources/figures/zora_ethical_collapse.gif
```

Options: `--steps 250` (smaller file), `--fps 28`, `--dpi 90`, `--e-high 10`.

**Alternatives**

```python
# After FuncAnimation(...)
ani.save("out.gif", writer="pillow", fps=28, dpi=90)

from matplotlib.animation import PillowWriter
writer = PillowWriter(fps=28, metadata=dict(artist="MQGT-SCF toy"), bitrate=2400)
ani.save("out.gif", writer=writer)

# mp4 (often easier codecs)
ani.save("out.mp4", writer="ffmpeg", fps=28, dpi=100)
```

Requires **ffmpeg** on PATH for mp4.

## HTML Φ_c / E canvas

`zora_fields.html` — open in browser. For a loopable asset: screen-record 10–15 s (OBS, QuickTime, ShareX) or record → convert with ezgif / ffmpeg.

## Related files

- `mqgt_gksl_ethics_field_sim.py` — CLI + optional PNG
- `zora_gksl_collapse_demo.py` — static dark-theme comparison plot
- `zora_ethical_collapse_animation.py` — GIF/mp4 build
- `README.md` — index
