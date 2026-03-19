#!/usr/bin/env python3
"""
Animate baseline (E=0) vs high-E coherence ⟨σ_x⟩ for the toy GKSL model.

Writes a looping-friendly GIF locally (Pillow). Sandbox/CI often cannot save
GIFs reliably — run on your machine:

  pip install qutip numpy matplotlib pillow
  python scripts/mqgt_sim/zora_ethical_collapse_animation.py -o zora_ethical_collapse.gif

See RESULTS_AND_ANIMATION_NOTES.md for observed numbers and mp4 fallback.
"""

from __future__ import annotations

import argparse
import sys


def compute_sx_trajectory(
    E_field: float,
    time_steps: int,
    t_max: float,
    gamma_0: float = 0.05,
    kappa: float = 0.2,
    omega: float = 1.0,
):
    import numpy as np
    import qutip as qt

    H = 0.5 * omega * qt.sigmax()
    psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
    rho0 = qt.ket2dm(psi0)
    L = qt.sigmaz()
    gamma_e = gamma_0 * (1.0 + kappa * float(E_field))
    c_ops = [np.sqrt(max(gamma_e, 0.0)) * L]
    tlist = np.linspace(0.0, t_max, int(time_steps))
    result = qt.mesolve(H, rho0, tlist, c_ops, [qt.sigmaz(), qt.sigmax()])
    return tlist, np.asarray(result.expect[1])


def main() -> None:
    p = argparse.ArgumentParser(description="GIF animation: ethical-collapse toy GKSL")
    p.add_argument("-o", "--output", default="zora_ethical_collapse.gif", help="Output path (.gif or .mp4)")
    p.add_argument("--steps", type=int, default=250, help="Time samples (fewer = smaller GIF)")
    p.add_argument("--t-max", type=float, default=20.0)
    p.add_argument("--fps", type=float, default=28.0)
    p.add_argument("--dpi", type=int, default=90)
    p.add_argument("--e-high", type=float, default=10.0)
    p.add_argument("--gamma-0", type=float, default=0.05)
    p.add_argument("--kappa", type=float, default=0.2)
    p.add_argument("--mp4", action="store_true", help="Save as mp4 (requires ffmpeg)")
    args = p.parse_args()

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation, PillowWriter
    except ImportError as e:
        print("pip install matplotlib numpy pillow qutip", file=sys.stderr)
        raise SystemExit(1) from e

    tlist, sx_base = compute_sx_trajectory(
        0.0, args.steps, args.t_max, args.gamma_0, args.kappa
    )
    _, sx_high = compute_sx_trajectory(
        args.e_high, args.steps, args.t_max, args.gamma_0, args.kappa
    )

    y_min = float(min(sx_base.min(), sx_high.min()) - 0.08)
    y_max = 1.05

    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(10, 6))
    (line_b,) = ax.plot(
        [], [], "--", color="cyan", lw=2, label=rf"$\langle\sigma_x\rangle$  $E=0$"
    )
    (line_h,) = ax.plot(
        [], [], "-", color="gold", lw=2, label=rf"$\langle\sigma_x\rangle$  $E={args.e_high:g}$"
    )
    ax.set_xlim(0, args.t_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel("Time", color="white")
    ax.set_ylabel("Coherence (toy)", color="white")
    ax.legend(loc="upper right", facecolor="#1a1a1e")
    ax.grid(True, alpha=0.25)
    fig.patch.set_facecolor("#0a0a0c")
    ax.set_facecolor("#0a0a0c")

    n = len(tlist)

    def init():
        line_b.set_data([], [])
        line_h.set_data([], [])
        return (line_b, line_h)

    def animate(i):
        i = min(i, n - 1)
        line_b.set_data(tlist[: i + 1], sx_base[: i + 1])
        line_h.set_data(tlist[: i + 1], sx_high[: i + 1])
        ax.set_title(
            f"Ethical collapse (toy GKSL)   t = {float(tlist[i]):.2f}",
            color="white",
            fontsize=13,
        )
        return (line_b, line_h)

    interval_ms = max(1, int(1000 / args.fps))
    ani = FuncAnimation(
        fig,
        animate,
        frames=n,
        init_func=init,
        blit=True,
        interval=interval_ms,
    )

    out = args.output
    if args.mp4 or out.lower().endswith(".mp4"):
        try:
            ani.save(out, writer="ffmpeg", fps=args.fps, dpi=args.dpi)
        except Exception as e:
            print(
                f"mp4 save failed ({e}). Install ffmpeg or use default .gif with pillow.",
                file=sys.stderr,
            )
            raise SystemExit(1) from e
    else:
        try:
            writer = PillowWriter(fps=args.fps, metadata={"artist": "MQGT-SCF toy sim"})
            ani.save(out, writer=writer, dpi=args.dpi)
        except Exception as e:
            print(
                f"GIF save failed ({e}). Try: pip install pillow\n"
                "Or use --mp4 with ffmpeg installed.",
                file=sys.stderr,
            )
            raise SystemExit(1) from e

    plt.close(fig)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
