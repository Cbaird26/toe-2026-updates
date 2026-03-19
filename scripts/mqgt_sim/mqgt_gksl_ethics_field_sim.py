#!/usr/bin/env python3
"""
MQGT-SCF — illustrative GKSL master-equation simulation.

Toy model: a two-level system evolves under a Lindblad dissipator whose rate
is modulated by a scalar parameter E (interpreted here as an "ethical field"
intensity in companion work). This is *not* calibrated to H2, QRNG, or any
experiment; it demonstrates numerically how a larger effective collapse rate
accelerates decoherence (loss of coherence / off-diagonal density-matrix terms).

See: papers_sources/MQGT-SCF_Phase_II_Submission_2026.tex (GKSL container;
flagship falsifier remains interferometric H2, not this script).

Dependencies: numpy, matplotlib, qutip
  pip install qutip numpy matplotlib
"""

from __future__ import annotations

import argparse
import sys


def run_simulation(
    e_intensity: float,
    time_steps: int,
    t_max: float,
    omega: float = 1.0,
    gamma_0: float = 0.05,
    kappa: float = 0.2,
):
    try:
        import numpy as np
        import qutip as qt
    except ImportError as e:
        print(
            "Missing dependency. Install with:\n  pip install qutip numpy matplotlib",
            file=sys.stderr,
        )
        raise SystemExit(1) from e

    H = 0.5 * omega * qt.sigmax()
    psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
    rho0 = qt.ket2dm(psi0)
    L_collapse = qt.sigmaz()
    gamma_e = gamma_0 * (1.0 + kappa * float(e_intensity))
    c_ops = [np.sqrt(max(gamma_e, 0.0)) * L_collapse]
    tlist = np.linspace(0.0, t_max, int(time_steps))
    result = qt.mesolve(H, rho0, tlist, c_ops, [qt.sigmaz(), qt.sigmax()])
    return tlist, result.expect


def main() -> None:
    p = argparse.ArgumentParser(description="Illustrative GKSL sim (E-modulated collapse rate)")
    p.add_argument("--e-baseline", type=float, default=0.0, help="E intensity (baseline curve)")
    p.add_argument("--e-high", type=float, default=10.0, help="E intensity (high curve)")
    p.add_argument("--steps", type=int, default=500, help="Time steps")
    p.add_argument("--t-max", type=float, default=20.0, help="Max time")
    p.add_argument("--save", type=str, default="", help="Save plot to path (e.g. gksl_sim.png)")
    p.add_argument("--no-show", action="store_true", help="Do not open plot window")
    p.add_argument("--gamma-0", type=float, default=0.05, help="Baseline Lindblad rate scale")
    p.add_argument("--kappa", type=float, default=0.2, help="E coupling: gamma = gamma0*(1+kappa*E)")
    args = p.parse_args()

    t_b, exp_b = run_simulation(
        args.e_baseline, args.steps, args.t_max, gamma_0=args.gamma_0, kappa=args.kappa
    )
    _, exp_h = run_simulation(
        args.e_high, args.steps, args.t_max, gamma_0=args.gamma_0, kappa=args.kappa
    )

    import matplotlib

    if args.no_show or args.save:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.plot(t_b, exp_b[0], label=r"$\langle\sigma_z\rangle$ (E=0)", alpha=0.9)
    ax.plot(t_b, exp_b[1], "--", label=r"$\langle\sigma_x\rangle$ coherence (E=0)", alpha=0.9)
    ax.plot(t_b, exp_h[0], label=rf"$\langle\sigma_z\rangle$ (E={args.e_high:g})", alpha=0.9)
    ax.plot(t_b, exp_h[1], "--", label=rf"$\langle\sigma_x\rangle$ (E={args.e_high:g})", alpha=0.9)
    ax.set_xlabel("time")
    ax.set_ylabel("expectation")
    ax.set_title("Toy GKSL: higher E → faster decoherence (illustrative)")
    ax.legend(loc="best", fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    if args.save:
        fig.savefig(args.save, dpi=150)
        print(f"Wrote {args.save}")
    if not args.no_show:
        plt.show()


if __name__ == "__main__":
    main()
