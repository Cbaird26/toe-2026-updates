#!/usr/bin/env python3
"""
MQGT-SCF — exploratory Phase IV lattice demo.

This is a pedagogical 2D lattice toy, not a referee-facing evidence model.
It evolves two scalar fields on a periodic lattice with explicit Euler updates,
quartic local restoring terms, and an exploratory alignment coupling. The H2
interferometric lane remains the primary falsification pathway in this repo.

Dependencies: numpy, matplotlib
  pip install numpy matplotlib

Examples:
  python scripts/mqgt_sim/mqgt_phase4_lattice_demo.py
  python scripts/mqgt_sim/mqgt_phase4_lattice_demo.py \
    --save-dir papers_sources/figures/phase4_lattice --no-show
"""

from __future__ import annotations

import argparse
import json
import os
import sys


def periodic_laplacian(field):
    """Return the 5-point periodic Laplacian on a 2D lattice."""
    import numpy as np

    return (
        np.roll(field, 1, axis=0)
        + np.roll(field, -1, axis=0)
        + np.roll(field, 1, axis=1)
        + np.roll(field, -1, axis=1)
        - 4.0 * field
    )


def coherence_metric(field):
    """Heuristic coherence proxy used only for exploratory visualization."""
    import numpy as np

    grad_x = np.roll(field, -1, axis=1) - field
    grad_y = np.roll(field, -1, axis=0) - field
    return float(np.exp(-np.mean(np.abs(grad_x) + np.abs(grad_y))))


def status_for_metrics(coherence, e_mean):
    if coherence > 0.85 and e_mean > 0.95:
        return "ATTRACTOR_REACHED"
    return "EVOLVING"


def run_lattice_demo(
    grid_size,
    steps,
    dt,
    seed,
    xi,
    kappa,
    m_c,
    m_e,
    clip_min=0.0,
    clip_max=1.8,
):
    try:
        import numpy as np
    except ImportError as e:
        print("pip install numpy matplotlib", file=sys.stderr)
        raise SystemExit(1) from e

    rng = np.random.default_rng(seed)
    phi_c = rng.normal(loc=0.6, scale=0.1, size=(grid_size, grid_size))
    ethical_field = rng.normal(loc=0.5, scale=0.1, size=(grid_size, grid_size))
    phi_c = np.clip(phi_c, clip_min, clip_max)
    ethical_field = np.clip(ethical_field, clip_min, clip_max)

    history = {
        "phi_mean": [],
        "E_mean": [],
        "coherence": [],
        "status": [],
    }

    for _ in range(steps):
        lap_phi = periodic_laplacian(phi_c)
        lap_e = periodic_laplacian(ethical_field)

        # Exploratory alignment scaffold; not a calibrated Phase II law.
        alignment_drive = xi * (phi_c + kappa * ethical_field)

        d_phi = lap_phi - (phi_c**3 + m_c * phi_c) + alignment_drive
        d_e = lap_e - (ethical_field**3 + m_e * ethical_field) + 0.8 * alignment_drive

        phi_c = np.clip(phi_c + dt * d_phi, clip_min, clip_max)
        ethical_field = np.clip(ethical_field + dt * d_e, clip_min, clip_max)

        phi_mean = float(np.mean(phi_c))
        e_mean = float(np.mean(ethical_field))
        coherence = coherence_metric(phi_c)
        status = status_for_metrics(coherence, e_mean)

        history["phi_mean"].append(phi_mean)
        history["E_mean"].append(e_mean)
        history["coherence"].append(coherence)
        history["status"].append(status)

    final_metrics = {
        "phi_mean": history["phi_mean"][-1],
        "E_mean": history["E_mean"][-1],
        "coherence": history["coherence"][-1],
        "status": history["status"][-1],
        "phi_min": float(np.min(phi_c)),
        "phi_max": float(np.max(phi_c)),
        "E_min": float(np.min(ethical_field)),
        "E_max": float(np.max(ethical_field)),
    }

    return {
        "phi_c": phi_c,
        "ethical_field": ethical_field,
        "history": history,
        "final_metrics": final_metrics,
        "parameters": {
            "grid_size": int(grid_size),
            "steps": int(steps),
            "dt": float(dt),
            "seed": int(seed),
            "xi": float(xi),
            "kappa": float(kappa),
            "m_c": float(m_c),
            "m_e": float(m_e),
            "clip_min": float(clip_min),
            "clip_max": float(clip_max),
        },
    }


def plot_results(result, save_path="", no_show=False):
    import matplotlib

    if no_show or save_path:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    phi_c = result["phi_c"]
    ethical_field = result["ethical_field"]
    history = result["history"]
    final_metrics = result["final_metrics"]
    params = result["parameters"]
    steps = range(1, params["steps"] + 1)

    fig, axs = plt.subplots(2, 2, figsize=(12, 9))

    im1 = axs[0, 0].imshow(phi_c, cmap="plasma", vmin=params["clip_min"], vmax=params["clip_max"])
    axs[0, 0].set_title(r"Exploratory $\Phi_c$ lattice")
    fig.colorbar(im1, ax=axs[0, 0], fraction=0.046, pad=0.04)

    im2 = axs[0, 1].imshow(
        ethical_field, cmap="viridis", vmin=params["clip_min"], vmax=params["clip_max"]
    )
    axs[0, 1].set_title("Exploratory E lattice")
    fig.colorbar(im2, ax=axs[0, 1], fraction=0.046, pad=0.04)

    axs[1, 0].plot(steps, history["phi_mean"], label=r"$\Phi_c$ mean", color="C0")
    axs[1, 0].plot(steps, history["E_mean"], label="E mean", color="C2")
    axs[1, 0].set_title("Field means")
    axs[1, 0].set_xlabel("step")
    axs[1, 0].set_ylabel("mean value")
    axs[1, 0].grid(True, alpha=0.3)
    axs[1, 0].legend(loc="best", fontsize=8)

    axs[1, 1].plot(steps, history["coherence"], color="C3")
    axs[1, 1].axhline(0.85, color="0.5", linestyle="--", linewidth=1, label="coherence threshold")
    axs[1, 1].set_title("Heuristic coherence")
    axs[1, 1].set_xlabel("step")
    axs[1, 1].set_ylabel("exp(-mean(|grad|))")
    axs[1, 1].grid(True, alpha=0.3)
    axs[1, 1].legend(loc="best", fontsize=8)

    fig.suptitle(
        "MQGT-SCF Phase IV lattice demo "
        f"| status={final_metrics['status']} "
        f"| xi={params['xi']:.4f} "
        f"| coherence={final_metrics['coherence']:.3f}",
        fontsize=12,
    )
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)
        print(f"Wrote {save_path}")
    if not no_show:
        plt.show()
    else:
        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Exploratory 2D lattice demo for MQGT-SCF visuals")
    parser.add_argument("--grid-size", type=int, default=64, help="Lattice size N for an N x N grid")
    parser.add_argument("--steps", type=int, default=500, help="Number of Euler steps")
    parser.add_argument("--dt", type=float, default=0.05, help="Euler time step")
    parser.add_argument("--seed", type=int, default=0, help="RNG seed for deterministic initialization")
    parser.add_argument("--xi", type=float, default=0.008, help="Exploratory alignment coupling")
    parser.add_argument("--kappa", type=float, default=0.7, help="Cross-field weighting inside alignment drive")
    parser.add_argument("--m-c", type=float, default=1.0, help="Quadratic restoring coefficient for phi_c")
    parser.add_argument("--m-e", type=float, default=1.0, help="Quadratic restoring coefficient for E")
    parser.add_argument("--save-dir", default="", help="If set, save PNG + JSON artifacts here")
    parser.add_argument("--no-show", action="store_true", help="Run headlessly without opening a window")
    args = parser.parse_args()

    if args.grid_size <= 1:
        raise SystemExit("--grid-size must be > 1")
    if args.steps <= 0:
        raise SystemExit("--steps must be > 0")
    if args.dt <= 0:
        raise SystemExit("--dt must be > 0")

    result = run_lattice_demo(
        grid_size=args.grid_size,
        steps=args.steps,
        dt=args.dt,
        seed=args.seed,
        xi=args.xi,
        kappa=args.kappa,
        m_c=args.m_c,
        m_e=args.m_e,
    )

    save_path = ""
    json_path = ""
    if args.save_dir:
        os.makedirs(args.save_dir, exist_ok=True)
        save_path = os.path.join(args.save_dir, "mqgt_phase4_lattice_demo.png")
        json_path = os.path.join(args.save_dir, "mqgt_phase4_lattice_demo_summary.json")

    plot_results(result, save_path=save_path, no_show=args.no_show)

    if json_path:
        payload = {
            "parameters": result["parameters"],
            "final_metrics": result["final_metrics"],
            "history": result["history"],
        }
        with open(json_path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, sort_keys=True)
        print(f"Wrote {json_path}")


if __name__ == "__main__":
    main()
