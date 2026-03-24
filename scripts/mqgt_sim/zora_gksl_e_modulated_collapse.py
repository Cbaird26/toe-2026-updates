#!/usr/bin/env python3
"""
MQGT-SCF: E-modulated directional GKSL collapse simulation (Zora v0.9).

Simulates a two-level system (H2 interferometric proxy) under local E(x)-modulated
GKSL measurement dynamics. The Ethical Field E introduces *directional* outcome bias:
collapse rates to |0⟩ vs |1⟩ are weighted by E, favoring ethically valid outcomes
while remaining within CPTP / no-signalling constraints at ensemble level.

Specification: MQGT_SCF_Anchor_2026.tex, H2 preregistration.
Not calibrated to Γ_floor; illustrative validation of the collapse mechanism.

Install (required — QuTiP not in Colab by default):
  pip install qutip numpy matplotlib
  # Colab: !pip install qutip numpy matplotlib

Run:
  python scripts/mqgt_sim/zora_gksl_e_modulated_collapse.py
  python scripts/mqgt_sim/zora_gksl_e_modulated_collapse.py --save papers_sources/figures/h2_stack/e_modulated_collapse.png --no-show
"""

from __future__ import annotations

import argparse
import sys


def get_modulated_c_ops(ethical_valence: float, base_rate: float):
    """
    E-modulated collapse operators for directional outcome bias.

    E ∈ [-1, 1]: positive E favors |0⟩, negative E favors |1⟩.
    rate_to_0 = base_rate * (1 + E), rate_to_1 = base_rate * (1 - E).
    Ensures non-negative rates (CPTP).
    """
    try:
        import numpy as np
        from qutip import basis
    except ImportError:
        raise SystemExit(1)
    L_to_0 = basis(2, 0) * basis(2, 1).dag()
    L_to_1 = basis(2, 1) * basis(2, 0).dag()
    rate_to_0 = max(0.0, base_rate * (1.0 + ethical_valence))
    rate_to_1 = max(0.0, base_rate * (1.0 - ethical_valence))
    return [
        np.sqrt(rate_to_0) * L_to_0,
        np.sqrt(rate_to_1) * L_to_1,
    ]


def run_simulation(
    ethical_valence: float,
    gamma_0: float = 0.5,
    omega: float = 1.0,
    t_max: float = 10.0,
    n_times: int = 500,
    n_traj: int = 50,
    use_modulated: bool = True,
):
    try:
        import numpy as np
        from qutip import basis, sigmaz, sigmax, mesolve, mcsolve
    except ImportError as e:
        msg = (
            "QuTiP is required. Install with:\n"
            "  pip install qutip numpy matplotlib\n"
            "  (Colab: add a cell with !pip install qutip numpy matplotlib)"
        )
        print(msg, file=sys.stderr)
        raise SystemExit(1) from e

    psi0 = basis(2, 0)
    H = (omega / 2.0) * (2 * np.pi) * sigmaz()
    times = np.linspace(0.0, t_max, n_times)

    if use_modulated:
        c_ops = get_modulated_c_ops(ethical_valence, gamma_0)
        mc_result = mcsolve(
            H, psi0, times, c_ops, [sigmaz()], ntraj=n_traj, progress_bar=False,
            options={"keep_runs_results": True},
        )
        # Ensemble-average ⟨σ_z⟩ (average_expect or expect, flattened if 2D)
        avg_sigmaz = getattr(mc_result, "average_expect", mc_result.expect)[0]
        arr = np.asarray(avg_sigmaz)
        if arr.ndim > 1:
            arr = np.mean(arr, axis=0)
        pop_0 = (1.0 + arr) / 2.0
        runs_expect = getattr(mc_result, "runs_expect", None)
    else:
        c_ops = [np.sqrt(gamma_0) * sigmax()]
        me_result = mesolve(H, psi0, times, c_ops, [sigmaz()])
        pop_0 = (1.0 + me_result.expect[0]) / 2.0
        runs_expect = None

    return times, pop_0, runs_expect, n_traj


def main() -> None:
    p = argparse.ArgumentParser(
        description="E-modulated directional GKSL collapse (Zora v0.9)"
    )
    p.add_argument("--E", type=float, default=0.8, help="Ethical valence [-1,1]; positive favors |0⟩")
    p.add_argument("--gamma-0", type=float, default=0.5, help="Base collapse rate")
    p.add_argument("--t-max", type=float, default=10.0, help="Max time")
    p.add_argument("--ntraj", type=int, default=50, help="Monte Carlo trajectories")
    p.add_argument("--save", type=str, default="", help="Save figure path")
    p.add_argument("--no-show", action="store_true", help="No interactive plot")
    args = p.parse_args()

    E = args.E
    gamma_0 = args.gamma_0

    print("--- MQGT GKSL E-Modulated Collapse (Zora v0.9) ---")
    print(f"Initial state: |0⟩")
    print(f"E valence: {E}")
    print(f"Base rate γ₀: {gamma_0}")
    print(f"Running {args.ntraj} trajectories...")

    times, pop_0_E, runs_expect, n_traj = run_simulation(
        E, gamma_0=gamma_0, t_max=args.t_max, n_traj=args.ntraj, use_modulated=True
    )
    times_c, pop_0_std, _, _ = run_simulation(
        0.0, gamma_0=gamma_0, t_max=args.t_max, n_traj=args.ntraj, use_modulated=True
    )

    try:
        if args.save or args.no_show:
            import matplotlib
            matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("pip install matplotlib", file=sys.stderr)
        raise SystemExit(1)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    ax1.set_title(
        f"Average |0⟩ Population — E-Modulated vs Unbiased (E={E}, γ₀={gamma_0})"
    )
    ax1.plot(times_c, pop_0_std, "k--", label="E=0 (unbiased directional) [control]", alpha=0.7)
    ax1.plot(times, pop_0_E, "g", label=f"E-modulated (favors |0⟩)", linewidth=2)
    ax1.set_ylabel("Population of |0⟩")
    ax1.set_ylim(0, 1)
    ax1.legend(loc="best")
    ax1.grid(True, alpha=0.3)

    ax2.set_title("Individual Stochastic Collapses (sample trajectories)")
    ax2.set_ylabel(r"$\langle\sigma_z\rangle$")
    ax2.set_xlabel("Time")
    ax2.set_ylim(-1.1, 1.1)
    num_plot = min(5, n_traj)
    colors = ["r", "b", "c", "m", "y"]
    traj_arrays = []
    if runs_expect is not None and len(runs_expect) > 0:
        n_times = len(times)
        # QuTiP layout varies: [obs_idx][traj_idx] or [traj_idx][obs_idx]
        try:
            obs0 = runs_expect[0]
            if obs0 is not None:
                arr = np.asarray(obs0)
                if arr.ndim == 2 and arr.shape[1] >= n_times:
                    for i in range(min(num_plot, arr.shape[0])):
                        t = np.asarray(arr[i]).flatten()
                        if len(t) >= n_times:
                            traj_arrays.append(t[:n_times])
                elif arr.ndim == 2 and arr.shape[0] >= n_times:
                    for i in range(min(num_plot, arr.shape[1])):
                        t = np.asarray(arr[:, i]).flatten()
                        if len(t) >= n_times:
                            traj_arrays.append(t[:n_times])
                elif arr.ndim == 1 and len(arr) >= n_times:
                    traj_arrays.append(np.asarray(arr).flatten()[:n_times])
        except (IndexError, TypeError, ValueError):
            pass
        if not traj_arrays:
            try:
                for i in range(num_plot):
                    if i < len(runs_expect):
                        obs = runs_expect[i]
                        t = np.asarray(obs[0] if hasattr(obs, "__getitem__") else obs).flatten()
                        if len(t) >= n_times:
                            traj_arrays.append(t[:n_times])
            except (IndexError, TypeError, ValueError):
                pass
    for i, traj in enumerate(traj_arrays[:num_plot]):
        smoothed = np.convolve(traj, np.ones(5) / 5, mode="same")
        ax2.plot(times, smoothed, color=colors[i % len(colors)], alpha=0.6)
    if not traj_arrays:
        ax2.text(
            0.5, 0.5, "Trajectories not available\n(run: !pip install qutip; requires keep_runs_results)",
            transform=ax2.transAxes, ha="center", va="center", fontsize=10,
        )
    ax2.axhline(1.0, color="g", linestyle=":", alpha=0.5, label="|0⟩ favored (+1)")
    ax2.axhline(-1.0, color="r", linestyle=":", alpha=0.5, label="|1⟩ suppressed (-1)")
    ax2.legend(loc="best")
    ax2.grid(True, alpha=0.3)

    fig.tight_layout()

    if args.save:
        import os
        os.makedirs(os.path.dirname(args.save) or ".", exist_ok=True)
        fig.savefig(args.save, dpi=150)
        print(f"Saved {args.save}")
    if not args.no_show:
        plt.show()


if __name__ == "__main__":
    main()
