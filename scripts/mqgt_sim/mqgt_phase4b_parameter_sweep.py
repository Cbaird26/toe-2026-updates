#!/usr/bin/env python3
"""
MQGT-SCF — Phase IV-B parameter sweep (exploratory).

This script reuses the current Phase IV-B lattice model exactly as implemented in
`mqgt_phase4b_symmetry_breaking_demo.py`. It sweeps across `(xi, gamma, g)`
over multiple seeds, records final metrics/status, and saves compact heatmaps.

Important scope note:
  - This is an execution/exploration layer artifact.
  - It is not H1/H2 evidence and does not replace H2 interferometry as the
    primary falsification lane in this repo.
  - The sweep intentionally runs without the demo's default Gaussian injections
    so the maps reflect intrinsic lattice behavior under the shared dynamics.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from mqgt_phase4b_symmetry_breaking_demo import Phase4bLattice


def parse_float_list(spec: str) -> list[float]:
    vals: list[float] = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        vals.append(float(chunk))
    if not vals:
        raise ValueError("expected at least one numeric value")
    return vals


def run_single_point(
    *,
    grid_size: int,
    steps: int,
    substeps: int,
    dt: float,
    seed: int,
    xi: float,
    kappa: float,
    gamma: float,
    g_couple: float,
    lambda_phi: float,
    lambda_E: float,
    v_phi: float,
    v_E: float,
) -> dict[str, float | str]:
    sim = Phase4bLattice(
        grid_size=grid_size,
        dt=dt,
        seed=seed,
        xi=xi,
        kappa=kappa,
        gamma=gamma,
        g_couple=g_couple,
        lambda_phi=lambda_phi,
        lambda_E=lambda_E,
        v_phi=v_phi,
        v_E=v_E,
    )

    for _ in range(steps):
        for _ in range(max(1, substeps)):
            sim.integrate_step()
        sim.record()

    return {
        "phi_mean_final": sim.history["phi_mean"][-1],
        "E_mean_final": sim.history["E_mean"][-1],
        "phi_var_final": sim.history["phi_var"][-1],
        "roughness_final": sim.history["roughness"][-1],
        "coherence_final": sim.history["coherence"][-1],
        "status_final": sim.history["status"][-1],
    }


def save_heatmap(
    matrix: np.ndarray,
    *,
    xvals: list[float],
    yvals: list[float],
    title: str,
    outpath: Path,
    cmap: str,
    vmin: float,
    vmax: float,
) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    im = ax.imshow(matrix, origin="lower", cmap=cmap, aspect="auto", vmin=vmin, vmax=vmax)
    ax.set_xticks(range(len(xvals)))
    ax.set_xticklabels([f"{x:.3f}" for x in xvals], rotation=45, ha="right")
    ax.set_yticks(range(len(yvals)))
    ax.set_yticklabels([f"{y:.3f}" for y in yvals])
    ax.set_xlabel("xi")
    ax.set_ylabel("gamma")
    ax.set_title(title)
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(outpath, dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Phase IV-B sweep over xi, gamma, and g using the shared lattice model"
    )
    parser.add_argument("--xis", default="0.000,0.005,0.010,0.020,0.040")
    parser.add_argument("--gammas", default="0.02,0.05,0.10,0.15,0.20")
    parser.add_argument("--g-couples", default="0.00,0.10,0.18,0.30")
    parser.add_argument("--seeds", type=int, default=5, help="Number of seeds per grid point")
    parser.add_argument("--steps", type=int, default=500, help="Recorded frames per run")
    parser.add_argument("--substeps", type=int, default=5, help="Integrator steps per recorded frame")
    parser.add_argument("--grid-size", type=int, default=64)
    parser.add_argument("--dt", type=float, default=0.04)
    parser.add_argument("--kappa", type=float, default=0.60)
    parser.add_argument("--lambda-phi", type=float, default=1.0)
    parser.add_argument("--lambda-e", type=float, default=1.0)
    parser.add_argument("--v-phi", type=float, default=1.0)
    parser.add_argument("--v-e", type=float, default=1.0)
    parser.add_argument("--outdir", default="phase4b_parameter_sweep")
    args = parser.parse_args()

    if args.seeds <= 0:
        raise SystemExit("--seeds must be > 0")
    if args.steps <= 0:
        raise SystemExit("--steps must be > 0")
    if args.dt <= 0:
        raise SystemExit("--dt must be > 0")
    if args.grid_size <= 1:
        raise SystemExit("--grid-size must be > 1")

    xis = parse_float_list(args.xis)
    gammas = parse_float_list(args.gammas)
    g_couples = parse_float_list(args.g_couples)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    csv_path = outdir / "phase4b_parameter_sweep_results.csv"
    rows: list[dict[str, float | str | int]] = []

    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "xi",
                "gamma",
                "g_couple",
                "seed",
                "phi_mean_final",
                "E_mean_final",
                "phi_var_final",
                "roughness_final",
                "coherence_final",
                "status_final",
            ],
        )
        writer.writeheader()

        for g_couple in g_couples:
            for gamma in gammas:
                for xi in xis:
                    for seed in range(args.seeds):
                        result = run_single_point(
                            grid_size=args.grid_size,
                            steps=args.steps,
                            substeps=args.substeps,
                            dt=args.dt,
                            seed=seed,
                            xi=xi,
                            kappa=args.kappa,
                            gamma=gamma,
                            g_couple=g_couple,
                            lambda_phi=args.lambda_phi,
                            lambda_E=args.lambda_e,
                            v_phi=args.v_phi,
                            v_E=args.v_e,
                        )
                        row = {
                            "xi": xi,
                            "gamma": gamma,
                            "g_couple": g_couple,
                            "seed": seed,
                            **result,
                        }
                        writer.writerow(row)
                        rows.append(row)

    summary_path = outdir / "summary.md"
    with summary_path.open("w", encoding="utf-8") as fh:
        fh.write("# Phase IV-B parameter sweep summary\n\n")
        fh.write(
            "This sweep reuses the current `Phase4bLattice` dynamics exactly and runs without "
            "default injections so the maps reflect intrinsic lattice behavior.\n\n"
        )
        fh.write(f"- xis: {xis}\n")
        fh.write(f"- gammas: {gammas}\n")
        fh.write(f"- g_couples: {g_couples}\n")
        fh.write(f"- seeds per point: {args.seeds}\n")
        fh.write(f"- steps: {args.steps}\n")
        fh.write(f"- substeps: {args.substeps}\n")
        fh.write(f"- grid_size: {args.grid_size}\n")
        fh.write(f"- dt: {args.dt}\n")
        fh.write(f"- csv: `{csv_path.name}`\n\n")

        for g_couple in g_couples:
            lock_rate = np.zeros((len(gammas), len(xis)))
            mean_coherence = np.zeros((len(gammas), len(xis)))
            subset_all = [row for row in rows if row["g_couple"] == g_couple]

            fh.write(f"## g = {g_couple:.3f}\n\n")
            fh.write(
                f"- mean coherence across all seeds/points: "
                f"{np.mean([float(row['coherence_final']) for row in subset_all]):.3f}\n"
            )
            fh.write(
                f"- lock fraction across all seeds/points: "
                f"{np.mean([row['status_final'] == 'ATTRACTOR_LOCKED' for row in subset_all]):.3f}\n"
            )

            for iy, gamma in enumerate(gammas):
                for ix, xi in enumerate(xis):
                    subset = [
                        row
                        for row in rows
                        if row["g_couple"] == g_couple and row["gamma"] == gamma and row["xi"] == xi
                    ]
                    if subset:
                        lock_rate[iy, ix] = np.mean(
                            [row["status_final"] == "ATTRACTOR_LOCKED" for row in subset]
                        )
                        mean_coherence[iy, ix] = float(
                            np.mean([float(row["coherence_final"]) for row in subset])
                        )

            lock_path = outdir / f"lock_rate_g_{g_couple:.3f}.png"
            coherence_path = outdir / f"mean_coherence_g_{g_couple:.3f}.png"
            save_heatmap(
                lock_rate,
                xvals=xis,
                yvals=gammas,
                title=f"Lock rate | g={g_couple:.3f}",
                outpath=lock_path,
                cmap="magma",
                vmin=0.0,
                vmax=1.0,
            )
            save_heatmap(
                mean_coherence,
                xvals=xis,
                yvals=gammas,
                title=f"Mean final coherence | g={g_couple:.3f}",
                outpath=coherence_path,
                cmap="viridis",
                vmin=0.0,
                vmax=1.0,
            )
            fh.write(f"- heatmap: `{lock_path.name}`\n")
            fh.write(f"- heatmap: `{coherence_path.name}`\n\n")

    print(f"saved csv: {csv_path}")
    print(f"saved summary: {summary_path}")
    print(f"saved heatmaps in: {outdir}")


if __name__ == "__main__":
    main()
