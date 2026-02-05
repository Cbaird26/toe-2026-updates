#!/usr/bin/env python3
"""Generate a publishable-ish frequency ladder figure for MQGT-SCF.

This is a translation-layer visualization: it maps MQGT-SCF constraint channels
onto a single frequency (Hz) axis.

It intentionally avoids claiming that 'frequency causes reality'; it just shows
where different experimental/physical regimes sit in the frequency domain.

Outputs:
  - /mnt/data/mqgt_frequency_atlas.png
  - /mnt/data/mqgt_frequency_atlas.pdf

No external dependencies beyond matplotlib + numpy.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt

# Physical constants (exact SI definitions)
C = 299_792_458.0  # m/s
H = 6.626_070_15e-34  # J s
E_CHARGE = 1.602_176_634e-19  # J / eV


def lambda_to_feq_hz(lam_m: float) -> float:
    """Equivalent frequency tag for a Yukawa-range mediator.

    f_eq ≈ c / (2π λ)

    This is a convenience mapping (range -> timescale/energy scale), not a claim
    about a literal oscillation in the apparatus.
    """
    return C / (2.0 * math.pi * lam_m)


def f_to_e_ev(f_hz: float) -> float:
    """Convert frequency to energy in eV via E = h f."""
    return (H * f_hz) / E_CHARGE


@dataclass(frozen=True)
class Band:
    label: str
    f_min: float
    f_max: float
    y: float


def main() -> None:
    # --- MQGT-SCF channel placement (approximate, for visualization)
    # Values chosen to match the narrative you’ve been using.
    hubble_hz = 2.18e-18
    higgs_equiv_hz = 3.0e25
    planck_freq_hz = 1.85e43

    # Eöt-Wash digitized range (from your notes)
    lam_min = 2.995e-5   # m  (~30 µm)
    lam_max = 9.289e-4   # m  (~0.93 mm)
    feq_max = lambda_to_feq_hz(lam_min)
    feq_min = lambda_to_feq_hz(lam_max)

    # QRNG device bandwidth (illustrative; implementation-dependent)
    qrng_min, qrng_max = 1.0, 1e9

    bands = [
        Band("Cosmology (Hubble-scale clock)", hubble_hz/3, hubble_hz*3, 3.0),
        Band("Fifth-force (Eöt-Wash λ → f_eq)", feq_min, feq_max, 2.0),
        Band("QRNG (device/DAQ bandwidth)", qrng_min, qrng_max, 1.0),
        Band("Higgs / collider (energy↔frequency)", higgs_equiv_hz/3, higgs_equiv_hz*3, 0.0),
    ]

    # Landmark frequency annotations (minimal set to keep the figure readable)
    landmarks = [
        (1.0/86400.0, "1/day"),
        (7.83, "Schumann\n~7.83 Hz"),
        (20.0, "Hearing\n~20 Hz"),
        (2e4, "Hearing\n~20 kHz"),
        (9_192_631_770.0, "Cs-133\n(1 s)"),
        (4.3e14, "Visible\n(red)"),
        (7.5e14, "Visible\n(violet)"),
        (planck_freq_hz, "Planck\n~1/t_P"),
    ]

    # --- Build plot
    fig, ax = plt.subplots(figsize=(12, 5.8))

    # Log frequency axis
    ax.set_xscale("log")
    ax.set_xlim(1e-20, 1e44)
    ax.set_ylim(-0.7, 3.7)

    # Plot bands using default color cycle (no explicit colors)
    for b in bands:
        ax.plot([b.f_min, b.f_max], [b.y, b.y], linewidth=10, solid_capstyle='butt', label=b.label)

    # Add landmark vertical lines (thin) with labels
    for f, name in landmarks:
        if f <= 0:
            continue
        # Keep within axis range
        if f < 1e-20 or f > 1e44:
            continue
        ax.axvline(f, linewidth=1, alpha=0.35)
        ax.text(f, 3.55, name, rotation=90, va='top', ha='center', fontsize=8)

    # Eöt-Wash annotation block
    e_min_ev = f_to_e_ev(feq_min)
    e_max_ev = f_to_e_ev(feq_max)
    note = (
        "Eöt-Wash digitized window (your CSV)\n"
        f"λ ≈ {lam_min*1e6:.1f}–{lam_max*1e3:.2f} (µm–mm)\n"
        f"f_eq ≈ {feq_min:.2e}–{feq_max:.2e} Hz\n"
        f"E_eq ≈ {e_min_ev:.2e}–{e_max_ev:.2e} eV\n"
        "(f_eq = c/(2πλ); E = h f)"
    )
    ax.text(1.2e-10, 2.35, note, fontsize=9, va='top')

    # Axis labels
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(["Higgs/collider", "QRNG", "Fifth-force", "Cosmology"])
    ax.set_xlabel("Frequency (Hz) on a log scale")

    ax.set_title("MQGT-SCF: Constraint Channels on a Frequency Axis (translation layer, not evidence)")

    # Legend
    ax.legend(loc='lower right', fontsize=8, framealpha=0.9)

    ax.grid(True, which='both', axis='x', alpha=0.2)

    fig.tight_layout()

    png_path = "/mnt/data/mqgt_frequency_atlas.png"
    pdf_path = "/mnt/data/mqgt_frequency_atlas.pdf"
    fig.savefig(png_path, dpi=300)
    fig.savefig(pdf_path)

    # Also print the computed window values (useful for logs)
    print("Eot-Wash window")
    print(f"  lambda_min = {lam_min:.6e} m, lambda_max = {lam_max:.6e} m")
    print(f"  f_eq range  = {feq_min:.6e} to {feq_max:.6e} Hz")
    print(f"  E_eq range  = {e_min_ev:.6e} to {e_max_ev:.6e} eV")
    print(f"Saved: {png_path}")
    print(f"Saved: {pdf_path}")


if __name__ == "__main__":
    main()
