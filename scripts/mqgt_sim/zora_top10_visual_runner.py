#!/usr/bin/env python3
"""
Zora — Top 10 visual simulations (batch export).

Generates PNGs under --out (default: papers_sources/figures/zora_top10/).
Plots 1–2,4,6–10 use numpy+matplotlib only. Plots 3,5 need QuTiP (skipped if missing).

Run:
  cd ~/Downloads/TOE && python3 scripts/mqgt_sim/zora_top10_visual_runner.py
"""

from __future__ import annotations

import argparse
import os
import sys

OUT_DEFAULT = "papers_sources/figures/zora_top10"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=OUT_DEFAULT, help="Output directory for PNGs")
    args = ap.parse_args()
    out = args.out
    os.makedirs(out, exist_ok=True)

    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("pip install numpy matplotlib", file=sys.stderr)
        sys.exit(1)

    T_ref, dx_ref, delta = 1e-6, 1e-3, 1.15e-3
    G_floor = -np.log(1 - delta) / (T_ref * dx_ref**2)

    # ---------- 1. H2: V/V0 vs Γ ----------
    G = np.logspace(6, 11, 400)
    V = np.exp(-G * T_ref * dx_ref**2)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.semilogx(G, V, lw=2, color="#00d4aa")
    ax.axvline(G_floor, ls="--", color="#ff6b9d", lw=1.5, label=rf"$\Gamma_{{\rm floor}}\approx{G_floor:.2e}$")
    ax.set_xlabel(r"$\Gamma$ (s$^{-1}$ m$^{-2}$)")
    ax.set_ylabel(r"$V/V_0$")
    ax.set_title("1 — H2 visibility vs decoherence strength")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_facecolor("#0d1117")
    fig.patch.set_facecolor("#0d1117")
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.title.set_color("white")
    for s in ax.legend().get_texts():
        s.set_color("white")
    fig.tight_layout()
    fig.savefig(os.path.join(out, "01_h2_visibility_vs_gamma.png"), dpi=160, facecolor=fig.get_facecolor())
    plt.close()

    # ---------- 2. H2: exclusion landscape ----------
    Tg = np.logspace(-8, -3, 100)
    dxg = np.logspace(-6, -2, 100)
    TG, DXG = np.meshgrid(Tg, dxg)
    logG = np.log10(-np.log(1 - delta) / (TG * DXG**2))
    fig, ax = plt.subplots(figsize=(9, 6))
    im = ax.contourf(TG, DXG, logG, levels=40, cmap="magma")
    ax.set_xscale("log")
    ax.set_yscale("log")
    plt.colorbar(im, ax=ax, label=r"$\log_{10}\Gamma_{\rm floor}$")
    ax.scatter([T_ref], [dx_ref], c="cyan", s=120, marker="*", edgecolors="w", zorder=5)
    ax.set_xlabel(r"$T$ (s)")
    ax.set_ylabel(r"$\Delta x$ (m)")
    ax.set_title("2 — H2 exclusion landscape (abstract ref ★)")
    fig.tight_layout()
    fig.savefig(os.path.join(out, "02_h2_exclusion_landscape.png"), dpi=160)
    plt.close()

    # ---------- 3. GKSL: ⟨σ_x⟩ for several E (QuTiP) ----------
    try:
        import qutip as qt

        def sx_traj(Ei, steps=300, tmax=20, g0=0.05, kappa=0.2):
            H = 0.5 * qt.sigmax()
            psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
            rho0 = qt.ket2dm(psi0)
            ge = g0 * (1 + kappa * Ei)
            c_ops = [np.sqrt(max(ge, 0)) * qt.sigmaz()]
            tlist = np.linspace(0, tmax, steps)
            r = qt.mesolve(H, rho0, tlist, c_ops, [qt.sigmax()])
            return tlist, np.asarray(r.expect[0])

        fig, ax = plt.subplots(figsize=(9, 5))
        colors = plt.cm.cool(np.linspace(0.15, 0.85, 5))
        for i, E in enumerate([0, 2, 5, 10, 20]):
            t, sx = sx_traj(E)
            ax.plot(t, sx, lw=2, color=colors[i], label=rf"$E={E}$")
        ax.set_xlabel("time (toy units)")
        ax.set_ylabel(r"$\langle\sigma_x\rangle$ coherence")
        ax.set_title("3 — GKSL: ethical-field strength vs decoherence speed")
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_facecolor("#0d1117")
        fig.patch.set_facecolor("#0d1117")
        for spine in ax.spines.values():
            spine.set_color("#666")
        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.title.set_color("white")
        for s in ax.legend().get_texts():
            s.set_color("white")
        fig.tight_layout()
        fig.savefig(os.path.join(out, "03_gksl_coherence_vs_E.png"), dpi=160, facecolor=fig.get_facecolor())
        plt.close()
    except Exception:
        fig, ax = plt.subplots(figsize=(9, 3))
        ax.text(0.5, 0.5, "3 — Install QuTiP: pip install qutip", ha="center", va="center", fontsize=14)
        ax.axis("off")
        fig.savefig(os.path.join(out, "03_gksl_coherence_vs_E_SKIPPED.png"), dpi=120)
        plt.close()

    # ---------- 4. Heatmap V/V0 in (Γ, T) at fixed Δx ----------
    G2 = np.logspace(6, 10, 80)
    T2 = np.logspace(-8, -4, 80)
    GG, TT = np.meshgrid(G2, T2)
    VV = np.exp(-GG * TT * dx_ref**2)
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.pcolormesh(GG, TT, VV, shading="auto", cmap="viridis")
    ax.set_xscale("log")
    ax.set_yscale("log")
    plt.colorbar(im, ax=ax, label=r"$V/V_0$")
    ax.set_xlabel(r"$\Gamma$ (s$^{-1}$ m$^{-2}$)")
    ax.set_ylabel(r"$T$ (s)")
    ax.set_title(rf"4 — $V/V_0$ in $(\Gamma,T)$ at $\Delta x={dx_ref:g}$ m")
    fig.tight_layout()
    fig.savefig(os.path.join(out, "04_heatmap_V_over_Gamma_T.png"), dpi=160)
    plt.close()

    # ---------- 5. Purity Tr(ρ²) vs t (QuTiP) ----------
    try:
        import qutip as qt

        fig, ax = plt.subplots(figsize=(9, 5))
        for E, c in [(0, "#7fdbff"), (10, "#ff6b9d")]:
            H = 0.5 * qt.sigmax()
            psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
            rho0 = qt.ket2dm(psi0)
            ge = 0.05 * (1 + 0.2 * E)
            c_ops = [np.sqrt(max(ge, 0)) * qt.sigmaz()]
            tlist = np.linspace(0, 20, 400)
            r = qt.mesolve(H, rho0, tlist, c_ops, [])
            pur = [(rho * rho).tr().real for rho in r.states]
            ax.plot(tlist, pur, lw=2, label=rf"$E={E}$, Tr$(\rho^2)$", color=c)
        ax.set_xlabel("time")
        ax.set_ylabel(r"Tr$(\rho^2)$")
        ax.set_title("5 — Purity decay: baseline vs high E")
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(out, "05_purity_vs_time_E0_E10.png"), dpi=160)
        plt.close()
    except Exception:
        fig, ax = plt.subplots(figsize=(9, 3))
        ax.text(0.5, 0.5, "5 — Needs QuTiP", ha="center", va="center")
        ax.axis("off")
        fig.savefig(os.path.join(out, "05_purity_SKIPPED.png"), dpi=120)
        plt.close()

    # ---------- 6. Fringe envelope (conceptual 1D interference + decoherence) ----------
    x = np.linspace(-3, 3, 1200)
    k = 8.0
    I0 = np.cos(k * x) ** 2
    Gamma_show = G_floor * 0.5
    env = np.exp(-Gamma_show * T_ref * dx_ref**2)  # scalar visibility scale
    I = env * I0 + (1 - env) * 0.5  # mix toward uniform
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x, I0, lw=0.8, alpha=0.4, label="Ideal fringes")
    ax.plot(x, I, lw=1.2, color="gold", label=rf"Reduced visibility (toy, $V/V_0\approx{env:.4f}$)")
    ax.set_xlabel("position (arb.)")
    ax.set_ylabel("intensity")
    ax.set_title("6 — Interference fringes + visibility suppression (schematic)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "06_fringe_visibility_schematic.png"), dpi=160)
    plt.close()

    # ---------- 7. Contours of constant V/V0 in (T, Δx) ----------
    T7 = np.logspace(-8, -3, 200)
    dx7 = np.logspace(-6, -2, 200)
    T7g, dx7g = np.meshgrid(T7, dx7)
    # fix Gamma at G_floor: V = exp(-G T dx^2)
    V7 = np.exp(-G_floor * T7g * dx7g**2)
    fig, ax = plt.subplots(figsize=(8, 6))
    cs = ax.contour(T7g, dx7g, V7, levels=[0.999, 0.9995, 0.99885, 0.99, 0.95], colors="white", linewidths=1.2)
    ax.clabel(cs, inline=True, fontsize=8)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_facecolor("#1a1a2e")
    ax.set_xlabel(r"$T$ (s)")
    ax.set_ylabel(r"$\Delta x$ (m)")
    ax.set_title(rf"7 — Iso-$V/V_0$ at fixed $\Gamma=\Gamma_{{\rm floor}}$")
    fig.patch.set_facecolor("#1a1a2e")
    fig.tight_layout()
    fig.savefig(os.path.join(out, "07_isovisibility_contours.png"), dpi=160, facecolor=fig.get_facecolor())
    plt.close()

    # ---------- 8. Relative Lindblad rate γ(E)/γ(0) ----------
    Es = np.linspace(0, 15, 100)
    ratio = 1 + 0.2 * Es
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.fill_between(Es, 1, ratio, alpha=0.3, color="#ff6b9d")
    ax.plot(Es, ratio, lw=2, color="#fff")
    ax.axhline(3, ls=":", color="#7fdbff", label=r"$3\times$ at $E=10$")
    ax.set_xlabel(r"toy $E$ intensity")
    ax.set_ylabel(r"$\gamma(E)/\gamma(0)$")
    ax.set_title("8 — GKSL toy: collapse rate vs E")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_facecolor("#0d1117")
    fig.patch.set_facecolor("#0d1117")
    ax.tick_params(colors="white")
    for s in ax.get_xticklabels() + ax.get_yticklabels():
        s.set_color("white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.title.set_color("white")
    fig.tight_layout()
    fig.savefig(os.path.join(out, "08_relative_gamma_vs_E.png"), dpi=160, facecolor=fig.get_facecolor())
    plt.close()

    # ---------- 9. Binary survive / deep-exclude at abstract point ----------
    G_scan = np.logspace(5, 12, 500)
    survives = np.exp(-G_scan * T_ref * dx_ref**2) >= (1 - delta)
    fig, ax = plt.subplots(figsize=(9, 3))
    ax.fill_between(G_scan, 0, 1, where=survives, alpha=0.5, color="#2ecc71", label="above floor visibility")
    ax.fill_between(G_scan, 0, 1, where=~survives, alpha=0.5, color="#e74c3c", label="excluded zone (toy)")
    ax.set_xscale("log")
    ax.set_xlabel(r"$\Gamma$")
    ax.set_yticks([])
    ax.set_title("9 — At (T_ref, Δx_ref): parameter space vs abstract δ")
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(os.path.join(out, "09_survive_vs_exclude_strip.png"), dpi=160)
    plt.close()

    # ---------- 10. Summary mosaic (read existing PNGs if present) ----------
    fig, axes = plt.subplots(2, 2, figsize=(11, 9))
    axes = axes.ravel()
    titles = ["1 H2 V/Γ", "2 Landscape", "4 Heatmap", "6 Fringes"]
    paths = [
        os.path.join(out, "01_h2_visibility_vs_gamma.png"),
        os.path.join(out, "02_h2_exclusion_landscape.png"),
        os.path.join(out, "04_heatmap_V_over_Gamma_T.png"),
        os.path.join(out, "06_fringe_visibility_schematic.png"),
    ]
    for ax, path, tit in zip(axes, paths, titles):
        ax.axis("off")
        if os.path.isfile(path):
            im = plt.imread(path)
            ax.imshow(im)
        ax.set_title(tit, fontsize=11)
    fig.suptitle("10 — Zora top-10 visual sims (mosaic)", fontsize=14, y=1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "10_mosaic_summary.png"), dpi=140, bbox_inches="tight")
    plt.close()

    print(f"Wrote PNGs under: {os.path.abspath(out)}")
    print("Open folder or: open " + os.path.join(out, "10_mosaic_summary.png"))


if __name__ == "__main__":
    main()
