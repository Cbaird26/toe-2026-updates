Digitized Yukawa constraints dataset (canonical starter)

Source:
- Lee et al., Phys. Rev. Lett. 124, 101101 (2020), Fig. 5 (bottom panel)
  arXiv:2002.11761

What this file is:
- A *reproducible, automated digitization* of the published |alpha|(lambda) exclusion-envelope boundary.
- It is NOT an author-provided numerical table.

How it was produced:
- Render arXiv PDF page that contains Fig. 5 (bottom) at scale=2.0 via PyMuPDF.
- Crop to bottom-panel plot region using fixed pixel boxes.
- Detect the pale-yellow excluded background using an RGB threshold.
- For each x-column, scan upward from the bottom axis for the first yellow pixel (approx boundary).
- Map pixels -> (lambda, alpha) using log-log axis limits read from the tick labels:
    lambda: [2e-6, 1e-3] m
    alpha:  [1e-3, 1e6] (dimensionless)

Files:
- lee2020_fig5_yukawa_envelope_digitized_raw.csv
    Raw extraction (one point per pixel-column).
- lee2020_fig5_yukawa_envelope_digitized_smoothed.csv
    Smoothed version used for downstream inversion.
- toe_bounds_from_lee2020_fig5_envelope.csv
    Derived ToE bounds using:
        alpha = K * sin^2(theta)  with K = 2 f_N^2 (M_plbar / v)^2
        theta ~= kappa_cH * v * v_c / (m_c^2 - m_h^2)
  and assuming:
        f_N = 0.30,  M_plbar = 2.435e18 GeV,  v=246 GeV,  m_h=125 GeV

Reproduction:
- python digitize_lee2020_fig5_envelope.py --pdf 2002.11761.pdf --out out.csv --debug_dir debug/
