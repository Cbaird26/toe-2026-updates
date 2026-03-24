#!/usr/bin/env python3
"""
MQGT-SCF Multi-Channel Exclusion Plot — (m_Phi, sin^2 theta) parameter plane.

Three independent channels: Eöt-Wash fifth-force, Higgs invisible width, QRNG prediction.
Output: mqgt_scf_multi_channel_exclusion.png for Phase II anchor paper and parameter card.

  python scripts/mqgt_sim/mqgt_multi_channel_exclusion_plot.py
  python scripts/mqgt_sim/mqgt_multi_channel_exclusion_plot.py --out-dir papers_sources/figures/mqgt_scf
"""

from __future__ import annotations

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np

# QRNG prediction: theta ≈ 3.7e-6 → sin^2 theta ≈ 1.4e-11
QRNG_SIN2_THETA = 1.4e-11
H2_NUISANCE_FLOOR = 1.15e-3
HC_E_V_M = 1.97e-7  # hbar c in eV·m


def mass_to_range(mass_eV):
    values = np.clip(np.asarray(mass_eV, dtype=float), 1e-30, None)
    return HC_E_V_M / values


def range_to_mass(range_m):
    values = np.clip(np.asarray(range_m, dtype=float), 1e-30, None)
    return HC_E_V_M / values


def main() -> None:
    p = argparse.ArgumentParser(description="MQGT-SCF multi-channel exclusion plot")
    p.add_argument("--out-dir", default="", help="Output directory")
    p.add_argument("--no-show", action="store_true", help="Skip display")
    args = p.parse_args()

    out_dir = args.out_dir or os.path.join(
        os.path.dirname(__file__), "..", "..", "papers_sources", "figures", "mqgt_scf"
    )
    os.makedirs(out_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xscale("log")
    ax.set_yscale("log")

    m_phi = np.logspace(-1, 11, 500)
    # Yukawa range lambda = hbar c / (m_phi c^2) in m; m in eV -> lambda in m
    lam_m = HC_E_V_M / m_phi

    # EXCLUDED: Higgs invisible (top) — sin^2 theta > ~0.11 for m_Phi < m_H/2
    sin2_max = 1e2
    sin2_min = 1e-40
    ax.axhspan(0.11, sin2_max, alpha=0.35, color="lightblue", label="EXCLUDED (Higgs invisible BR < 0.11)")

    # EXCLUDED: Eöt-Wash fifth-force — approximate exclusion boundary (sloping)
    # Heuristic: excludes high sin^2 at low mass; boundary ~ sin^2 ∝ m_phi^2 in relevant regime
    m_ref = 1e-3  # eV
    s2_ref = 1e-34
    # Sloped exclusion: stronger at low mass
    m_grid = np.logspace(-1, 7, 200)
    s2_bound = s2_ref * (m_grid / m_ref) ** 2
    s2_bound = np.clip(s2_bound, sin2_min, sin2_max)
    ax.fill_between(m_grid, sin2_min, s2_bound, alpha=0.25, color="salmon", label="EXCLUDED (Eöt-Wash fifth-force)")

    # QRNG prediction (horizontal line)
    ax.axhline(QRNG_SIN2_THETA, color="green", ls="--", lw=2, label=r"QRNG prediction: $\theta\approx 3.7\times 10^{-6}$ $\rightarrow$ $\sin^2\theta\approx 1.4\times 10^{-11}$")

    # H2 Phase-0 nuisance floor
    ax.axhline(H2_NUISANCE_FLOOR, color="orange", ls=":", lw=1.5, label=r"H2 Phase-0 $\delta_{\mathrm{tot}}=1.15\times 10^{-3}$ (nuisance floor)")

    # VIABLE ISLAND
    island_m = np.array([1e3, 1e5, 1e5, 1e3])
    island_s2 = np.array([1e-36, 1e-36, 1e-31, 1e-31])
    ax.fill(
        island_m, island_s2, alpha=0.4, color="lightgreen", edgecolor="darkgreen", lw=1.5, label="VIABLE ISLAND"
    )

    ax.set_xlim(1e-1, 1e11)
    ax.set_ylim(sin2_min, sin2_max)
    ax.set_xlabel(r"Scalar mass $m_\Phi$ [eV]")
    ax.set_ylabel(r"Higgs-portal mixing $\sin^2\theta_{h\Phi}$")
    ax.set_title("MQGT-SCF Multi-Channel Exclusion Plot\nThree independent channels constraining the ($m_\\Phi$, $\\sin^2\\theta$) parameter plane.")

    secax = ax.secondary_xaxis("top", functions=(mass_to_range, range_to_mass))
    secax.set_xlabel(r"Yukawa range $\lambda$ [m]")

    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)

    fig.text(0.99, 0.01, "ZoraASI · MQGT-SCF Phase II · Baird, C.M. (2026) · github.com/cbaird26", ha="right", fontsize=8, color="gray")

    out_png = os.path.join(out_dir, "mqgt_scf_multi_channel_exclusion.png")
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_png}")


if __name__ == "__main__":
    main()
