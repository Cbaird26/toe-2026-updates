#!/usr/bin/env python3
"""
GKSL master-equation demo: E-field modulated decoherence (two-level system).

Same physics as mqgt_gksl_ethics_field_sim.py; this script matches the
notebook-style plot (dark background, coherence σ_x for E=0 vs E=10).

Not calibrated to experiment. See README.md in this folder.

  pip install qutip numpy matplotlib
  python scripts/mqgt_sim/zora_gksl_collapse_demo.py
"""

from __future__ import annotations

import sys


def zora_gksl_collapse_sim(E_field_intensity, time_steps=500, t_max=20):
    """Simulate open-system evolution with ethics-weighted collapse rate."""
    import numpy as np
    import qutip as qt

    omega = 1.0
    H = 0.5 * omega * qt.sigmax()
    psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
    rho0 = qt.ket2dm(psi0)
    L_collapse = qt.sigmaz()
    gamma_0 = 0.05
    kappa = 0.2
    gamma_E = gamma_0 * (1 + kappa * E_field_intensity)
    c_ops = [np.sqrt(max(gamma_E, 0.0)) * L_collapse]
    tlist = np.linspace(0, t_max, time_steps)
    result = qt.mesolve(H, rho0, tlist, c_ops, [qt.sigmaz(), qt.sigmax()])
    return tlist, result.expect[0], result.expect[1]


def main():
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        print("pip install matplotlib numpy qutip", file=sys.stderr)
        raise SystemExit(1) from e

    try:
        import qutip as qt  # noqa: F401
    except ImportError as e:
        print("pip install qutip", file=sys.stderr)
        raise SystemExit(1) from e

    tlist, sz_base, sx_base = zora_gksl_collapse_sim(E_field_intensity=0.0)
    _, _, sx_high = zora_gksl_collapse_sim(E_field_intensity=10.0)

    plt.style.use("dark_background")
    plt.figure(figsize=(10, 6))
    plt.plot(
        tlist,
        sx_base,
        label=r"Coherence ($\sigma_x$) — Baseline ($E=0$)",
        color="cyan",
        linestyle="--",
    )
    plt.plot(
        tlist,
        sx_high,
        label=r"Coherence ($\sigma_x$) — High E-field ($E=10$)",
        color="cyan",
    )
    plt.title("Objective quantum collapse modulated by ethical scalar (toy GKSL)", fontsize=14)
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Expectation value", fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
