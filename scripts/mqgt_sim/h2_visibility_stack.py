#!/usr/bin/env python3
"""
Phase II H2 interferometric visibility stack (paper-aligned).

Observable (Phase II):  V/V0 = exp(-Γ T Δx²)
  Γ in s⁻¹ m⁻², T superposition hold time (s), Δx path separation (m).

Exclusion floor (reference point from abstract):
  T_ref = 1e-6 s, Δx_ref = 1e-3 m, fractional visibility loss δ_total ≈ 1.15e-3
  ⇒ Γ_floor = -ln(1 - δ_total) / (T_ref Δx_ref²) ≈ 1.15×10⁹ s⁻¹ m⁻²

This script is a reproducible research artifact, not a substitute for lab noise
budgets or instrument models.

  pip install numpy matplotlib
  python scripts/mqgt_sim/h2_visibility_stack.py
  python scripts/mqgt_sim/h2_visibility_stack.py --save-dir papers_sources/figures/h2_stack
"""

from __future__ import annotations

import argparse
import os
import sys


def visibility_ratio(Gamma, T, dx):
    """V/V0 = exp(-Γ T Δx²). Gamma can be array."""
    import numpy as np

    return np.exp(-np.asarray(Gamma) * T * (dx**2))


def gamma_floor(T: float, dx: float, delta_total: float) -> float:
    """
    Γ such that 1 - V/V0 = δ_total at fixed T, Δx (small-δ: Γ ≈ δ/(T Δx²)).
    """
    import numpy as np

    if not (0 < delta_total < 1):
        raise ValueError("delta_total must be in (0, 1)")
    return float(-np.log(1.0 - delta_total) / (T * dx**2))


def main() -> None:
    p = argparse.ArgumentParser(description="H2 visibility + exclusion landscape (Phase II)")
    p.add_argument(
        "--save-dir",
        default="",
        help="If set, save PNGs here (no display)",
    )
    p.add_argument("--t-ref", type=float, default=1e-6, help="Reference T (s)")
    p.add_argument("--dx-ref", type=float, default=1e-3, help="Reference Δx (m)")
    p.add_argument(
        "--delta-total",
        type=float,
        default=1.15e-3,
        help="Target fractional visibility loss at floor point",
    )
    p.add_argument("--no-show", action="store_true", help="With --save-dir, skip plt.show()")
    args = p.parse_args()

    try:
        import matplotlib

        if args.save_dir:
            matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as e:
        print("pip install numpy matplotlib", file=sys.stderr)
        raise SystemExit(1) from e

    T_ref = args.t_ref
    dx_ref = args.dx_ref
    delta_total = args.delta_total
    Gf = gamma_floor(T_ref, dx_ref, delta_total)

    os.makedirs(args.save_dir, exist_ok=True) if args.save_dir else None

    # --- 1. V/V0 vs Γ at reference (T_ref, dx_ref) ---
    Gamma_vals = np.logspace(6, 11, 500)
    V_ratio = visibility_ratio(Gamma_vals, T_ref, dx_ref)

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.semilogx(Gamma_vals, V_ratio, lw=2, color="C0")
    ax1.axvline(Gf, ls="--", color="C3", lw=1.5, label=rf"$\Gamma_{{\rm floor}}\approx {Gf:.3e}$ s$^{{-1}}$m$^{{-2}}$")
    ax1.set_xlabel(r"$\Gamma$ (s$^{-1}$ m$^{-2}$)")
    ax1.set_ylabel(r"$V/V_0$")
    ax1.set_title(
        rf"H2 visibility suppression: $V/V_0=\exp(-\Gamma T\Delta x^2)$, "
        rf"$T={T_ref:g}$ s, $\Delta x={dx_ref:g}$ m"
    )
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1.05)
    fig1.tight_layout()
    if args.save_dir:
        fig1.savefig(os.path.join(args.save_dir, "h2_visibility_vs_gamma.png"), dpi=150)
    print(f"Gamma_floor (reference) = {Gf:.6e} s^-1 m^-2")

    # --- 2. 2D: log10(Γ required) for fixed δ_total across (T, Δx) ---
    T_vals = np.logspace(-8, -3, 120)
    dx_vals = np.logspace(-6, -2, 120)
    T_grid, dx_grid = np.meshgrid(T_vals, dx_vals, indexing="xy")
    Gamma_req = -np.log(1.0 - delta_total) / (T_grid * dx_grid**2)
    log10_G = np.log10(np.clip(Gamma_req, 1e-30, None))

    fig2, ax2 = plt.subplots(figsize=(10, 7))
    cf = ax2.contourf(T_grid, dx_grid, log10_G, levels=50, cmap="viridis")
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    cbar = fig2.colorbar(cf, ax=ax2)
    cbar.set_label(r"$\log_{10}(\Gamma_{\rm floor})$  (s$^{-1}$ m$^{-2}$)")
    ax2.set_xlabel(r"Superposition time $T$ (s)")
    ax2.set_ylabel(r"Path separation $\Delta x$ (m)")
    ax2.set_title(
        rf"H2 exclusion landscape ($\delta={delta_total:g}$: "
        rf"$\Gamma=-\ln(1-\delta)/(T\Delta x^2)$)"
    )
    ax2.scatter(
        [T_ref],
        [dx_ref],
        c="white",
        s=80,
        marker="*",
        edgecolors="k",
        zorder=5,
        label="Abstract reference point",
    )
    ax2.legend(loc="lower left", fontsize=9)
    fig2.tight_layout()
    if args.save_dir:
        fig2.savefig(os.path.join(args.save_dir, "h2_exclusion_landscape.png"), dpi=150)

    if args.save_dir:
        print(f"Saved figures under {args.save_dir}")
    if not args.save_dir and not args.no_show:
        plt.show()
    else:
        plt.close("all")


if __name__ == "__main__":
    main()
