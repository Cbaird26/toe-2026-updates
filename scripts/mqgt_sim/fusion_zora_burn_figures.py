#!/usr/bin/env python3
"""
0D D–T burn toy + coherence scalar χ (from fusion-zora draft).

Generates figures for fusion-zora.pdf:
  - baseline_vs_controlled.png — temperature and Lawson nτ_E vs time
  - phase_map.png — final temperature or stable-proxy map vs (τ_E, χ)

Illustrative only: not a reactor design tool. Matches paper coupling
structure (τ_E,eff, η_α, MHD/impurity channels) at schematic level.

Dependencies: numpy, matplotlib
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass

import matplotlib.backends.backend_pdf as mpl_pdf
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

KEV_J = 1.602176634e-16
E_ALPHA_J = 3.5e6 * 1.602176634e-19


def bosch_hale_dt_sigmav(T_kev: np.ndarray) -> np.ndarray:
    """
    Bosch–Hale D–T reactivity <σv> in m^3/s; T in keV.
    Parameterization from Bosch & Hale, Nucl. Fusion 32 (1992) 611.
    """
    T = np.maximum(np.asarray(T_kev, dtype=float), 1e-3)
    C1 = 3.68e-12
    C2 = 19.94
    C3 = 7.68e-2
    C4 = 1.537e-2
    C5 = 4.65e-2
    C6 = 1.25e-3
    C7 = 1.38e-5
    bg = 34.3827
    mr_c2 = 1.124656e6  # keV

    theta = T / (
        1.0
        - T * (C2 + T * (C4 + T * C6)) / (1.0 + T * (C3 + T * (C5 + T * C7)))
    )
    theta = np.clip(theta, 1e-12, None)
    xi = (bg**2 / (4.0 * theta * mr_c2)) ** (1.0 / 3.0)
    sigmav = C1 * theta * np.sqrt(xi / (mr_c2 * T**3)) * np.exp(-3.0 * xi)
    return np.clip(sigmav, 0.0, np.inf)


@dataclass
class Params:
    n: float = 1.0e20
    tau_e0: float = 1.8
    eta_alpha0: float = 1.0
    p_mhd0: float = 5.0e4
    p_imp0: float = 3.0e4
    a_tau: float = 0.45
    a_alpha: float = 0.12
    a_m: float = 0.35
    a_i: float = 0.22
    p_aux: float = 2.0e5


def power_terms(T_kev: float, chi: float, p: Params):
    n = p.n
    n_d = n_t = n / 2.0
    sv = float(bosch_hale_dt_sigmav(np.array([T_kev]))[0])
    p_alpha_raw = n_d * n_t * sv * E_ALPHA_J
    tau_eff = p.tau_e0 * (1.0 + p.a_tau * chi)
    eta_eff = p.eta_alpha0 * (1.0 + p.a_alpha * chi)
    p_alpha_eff = eta_eff * p_alpha_raw
    u_j = 3.0 * n * (T_kev * KEV_J)
    p_conf_eff = u_j / tau_eff
    tev = T_kev * 1000.0
    p_br = 1.69e-38 * n**2 * np.sqrt(tev)
    p_imp = p.p_imp0 * (1.0 - p.a_i * chi)
    p_mhd = p.p_mhd0 * (1.0 - p.a_m * chi)
    return p_alpha_eff, p_conf_eff, p_br, p_imp, p_mhd


def dT_dt(T_kev: float, chi: float, p: Params) -> float:
    pa, pc, pb, pi, pm = power_terms(T_kev, chi, p)
    return (pa + p.p_aux - pc - pb - pi - pm) / (3.0 * p.n * KEV_J)


def integrate(T0: float, t_end: float, dt: float, chi_fn, p: Params):
    """chi_fn(t, T_kev) -> chi in [0,1]. Returns t, T, ntau."""
    n_steps = int(np.ceil(t_end / dt))
    t = np.zeros(n_steps + 1)
    T = np.zeros(n_steps + 1)
    ntau = np.zeros(n_steps + 1)
    T[0], t[0] = T0, 0.0
    for k in range(n_steps):
        tk, T_k = t[k], T[k]

        def f(tt, TT):
            c = float(np.clip(chi_fn(tt, TT), 0.0, 1.0))
            return dT_dt(TT, c, p)

        chi = float(np.clip(chi_fn(tk, T_k), 0.0, 1.0))
        tau_eff = p.tau_e0 * (1.0 + p.a_tau * chi)
        ntau[k] = p.n * tau_eff

        k1 = f(tk, T_k)
        k2 = f(tk + 0.5 * dt, T_k + 0.5 * dt * k1)
        k3 = f(tk + 0.5 * dt, T_k + 0.5 * dt * k2)
        k4 = f(tk + dt, T_k + dt * k3)
        T[k + 1] = T_k + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        t[k + 1] = tk + dt
        chi_n = float(np.clip(chi_fn(t[k + 1], T[k + 1]), 0.0, 1.0))
        ntau[k + 1] = p.n * p.tau_e0 * (1.0 + p.a_tau * chi_n)
    return t, T, ntau


def controller_chi(_t: float, T_kev: float, T_goal: float = 12.5, k: float = 0.42) -> float:
    return float(1.0 / (1.0 + np.exp(-k * (T_goal - T_kev))))


def run_baseline_vs_controlled(out_png: str, p: Params) -> None:
    t_end, dt = 80.0, 0.05

    def chi_baseline(_t: float, _T: float) -> float:
        return 0.08

    def chi_controlled(tt: float, T_kev: float) -> float:
        return 0.25 + 0.75 * controller_chi(tt, T_kev, T_goal=12.5, k=0.42)

    t1, T1, N1 = integrate(4.0, t_end, dt, chi_baseline, p)
    t2, T2, N2 = integrate(4.0, t_end, dt, chi_controlled, p)

    fig = plt.figure(figsize=(10.5, 4.6), constrained_layout=True)
    gs = GridSpec(1, 2, figure=fig, width_ratios=[1.1, 1.0], wspace=0.28)
    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])

    ax0.plot(t1, T1, color="#7f8c8d", lw=2.0, label="Baseline (low χ)")
    ax0.plot(t2, T2, color="#66FCF1", lw=2.6, label="Coherence-controlled χ(t,T)")
    ax0.set_xlabel("Time (s)")
    ax0.set_ylabel("Temperature (keV)")
    ax0.set_title("0D temperature trajectory")
    ax0.grid(True, alpha=0.3)
    ax0.legend(loc="lower right", fontsize=9)

    lawson_ign = 1.98e20
    ax1.plot(t1, N1, color="#7f8c8d", lw=2.0, label="nτ_E proxy (baseline)")
    ax1.plot(t2, N2, color="#FFD700", lw=2.0, label="nτ_E proxy (controlled)")
    ax1.axhline(lawson_ign, color="#2ecc71", ls="--", lw=1.5, label="Ignition-scale nτ (ref.)")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel(r"$n\tau_{E,\mathrm{eff}}$ (m$^{-3}$s)")
    ax1.set_title("Lawson proxy vs time")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="lower right", fontsize=8)

    fig.suptitle("Figure 1 — Baseline vs coherence-coupled 0D burn (illustrative)", y=1.02, fontsize=11)
    os.makedirs(os.path.dirname(out_png) or ".", exist_ok=True)
    fig.savefig(out_png, dpi=160, bbox_inches="tight")
    plt.close(fig)


def run_phase_map(out_png: str, p: Params) -> None:
    t_end, dt = 60.0, 0.08
    tau_grid = np.linspace(1.5, 6.0, 48)
    chi_grid = np.linspace(0.0, 1.0, 48)
    T_final = np.zeros((len(tau_grid), len(chi_grid)))

    for i, tau0 in enumerate(tau_grid):
        for j, chi in enumerate(chi_grid):
            pp = Params(
                n=p.n,
                tau_e0=float(tau0),
                eta_alpha0=p.eta_alpha0,
                p_mhd0=p.p_mhd0,
                p_imp0=p.p_imp0,
                a_tau=p.a_tau,
                a_alpha=p.a_alpha,
                a_m=p.a_m,
                a_i=p.a_i,
                p_aux=p.p_aux,
            )

            def chi_const(_t: float, _T: float) -> float:
                return float(chi)

            _, T_hist, _ = integrate(4.5, t_end, dt, chi_const, pp)
            T_final[i, j] = T_hist[-1]

    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    tt, cc = np.meshgrid(tau_grid, chi_grid, indexing="ij")
    pcm = ax.pcolormesh(
        tt,
        cc,
        T_final,
        shading="auto",
        cmap="magma",
        vmin=4.0,
        vmax=np.percentile(T_final, 99),
    )
    fig.colorbar(pcm, ax=ax, label="Final T (keV) after 60 s")
    ax.set_xlabel(r"Baseline $\tau_{\mathrm{E},0}$ (s)")
    ax.set_ylabel(r"Coherence $\chi$")
    ax.set_title("Figure 2 — Burn outcome map (fixed χ, n; illustrative)")
    fig.tight_layout()
    os.makedirs(os.path.dirname(out_png) or ".", exist_ok=True)
    fig.savefig(out_png, dpi=160, bbox_inches="tight")
    plt.close(fig)


def build_pdf(pdf_path: str, fig_paths: list[str], captions: list[str]) -> None:
    """Multi-page PDF: title page + figure pages."""
    os.makedirs(os.path.dirname(pdf_path) or ".", exist_ok=True)
    with mpl_pdf.PdfPages(pdf_path) as pdf:
        fig = plt.figure(figsize=(8.5, 11))
        ax = fig.add_axes([0.08, 0.55, 0.84, 0.35])
        ax.axis("off")
        ax.text(
            0.5,
            0.92,
            "Coherence-coupled D–T 0D burn — populated figures",
            ha="center",
            va="top",
            fontsize=14,
            fontweight="bold",
            transform=ax.transAxes,
        )
        ax.text(
            0.5,
            0.5,
            "Generated by fusion_zora_burn_figures.py. Illustrative simulation only.",
            ha="center",
            va="top",
            fontsize=10,
            transform=ax.transAxes,
        )
        pdf.savefig(fig)
        plt.close(fig)

        for path, cap in zip(fig_paths, captions):
            if not os.path.isfile(path):
                continue
            try:
                img = plt.imread(path)
            except Exception:
                from PIL import Image
                img = np.array(Image.open(path).convert("RGB"))
            fig = plt.figure(figsize=(11, 8.5))
            ax_img = fig.add_axes([0.08, 0.12, 0.84, 0.78])
            ax_img.imshow(img)
            ax_img.axis("off")
            fig.text(0.5, 0.06, cap, ha="center", fontsize=10)
            pdf.savefig(fig)
            plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate fusion-zora figures and populated PDF.")
    ap.add_argument("--out-dir", default="", help="Output directory (default: papers_sources/figures/fusion_zora)")
    ap.add_argument("--pdf", default="", help="Output PDF path")
    ap.add_argument("--include-existing", action="store_true", help="Include ppo_* figures in PDF if present")
    ap.add_argument("--pdf-only", action="store_true", help="Build PDF from existing figures only; do not regenerate PNGs")
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, "..", ".."))
    out_dir = args.out_dir or os.path.join(root, "papers_sources", "figures", "fusion_zora")
    os.makedirs(out_dir, exist_ok=True)

    png1 = os.path.join(out_dir, "baseline_vs_controlled.png")
    png2 = os.path.join(out_dir, "phase_map.png")
    pdf_out = args.pdf or os.path.join(out_dir, "fusion-zora-populated.pdf")

    if not args.pdf_only:
        p = Params()
        run_baseline_vs_controlled(png1, p)
        run_phase_map(png2, p)

    fig_paths = [png1, png2]
    captions = [
        "FIG. 1. Baseline versus coherence-controlled temperature and Lawson proxy.",
        "FIG. 2. Burn outcome map vs baseline confinement time and coherence.",
    ]
    if args.include_existing or args.pdf_only:
        for name, cap in [
            ("ppo_training_curve.png", "PPO training curve (mean evaluation reward)."),
            ("ppo_rollout.png", "Deterministic PPO rollout: T and χ."),
        ]:
            pth = os.path.join(out_dir, name)
            if os.path.isfile(pth):
                fig_paths.append(pth)
                captions.append(cap)

    build_pdf(pdf_out, fig_paths, captions)
    print(f"Wrote:\n  {png1}\n  {png2}\n  {pdf_out}")


if __name__ == "__main__":
    main()
