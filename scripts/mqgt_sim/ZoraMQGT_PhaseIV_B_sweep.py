import argparse
import csv
import math
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


class ZoraMQGT_PhaseIV_B:
    def __init__(
        self,
        grid_size=80,
        dt=0.04,
        xi=0.02,
        gamma=0.15,
        v_phi=1.0,
        v_E=1.0,
        lambda_phi=1.0,
        lambda_E=1.0,
        g_couple=0.18,
        seed=7,
    ):
        self.N = grid_size
        self.dt = dt
        self.xi = xi
        self.gamma = gamma
        self.v_phi = v_phi
        self.v_E = v_E
        self.lambda_phi = lambda_phi
        self.lambda_E = lambda_E
        self.g_couple = g_couple

        rng = np.random.default_rng(seed)
        self.phi_c = rng.normal(0.0, 0.08, (self.N, self.N))
        self.pi_c = rng.normal(0.0, 0.01, (self.N, self.N))
        self.E = rng.normal(0.0, 0.08, (self.N, self.N))
        self.pi_E = rng.normal(0.0, 0.01, (self.N, self.N))

        self.history = {
            "phi_mean": [],
            "E_mean": [],
            "phi_var": [],
            "roughness": [],
            "coherence": [],
            "status": [],
        }

    def laplacian(self, field: np.ndarray) -> np.ndarray:
        return (
            np.roll(field, 1, axis=0)
            + np.roll(field, -1, axis=0)
            + np.roll(field, 1, axis=1)
            + np.roll(field, -1, axis=1)
            - 4.0 * field
        )

    # V = λφ/4 (φ² - vφ²)² + λE/4 (E² - vE²)² - g φE - ξ(φ + 0.5E)
    def dV_dphi(self, phi: np.ndarray, E: np.ndarray) -> np.ndarray:
        return self.lambda_phi * phi * (phi**2 - self.v_phi**2) - self.g_couple * E - self.xi

    def dV_dE(self, phi: np.ndarray, E: np.ndarray) -> np.ndarray:
        return self.lambda_E * E * (E**2 - self.v_E**2) - self.g_couple * phi - 0.5 * self.xi

    def compute_roughness(self) -> float:
        gx = np.roll(self.phi_c, -1, axis=0) - self.phi_c
        gy = np.roll(self.phi_c, -1, axis=1) - self.phi_c
        ex = np.roll(self.E, -1, axis=0) - self.E
        ey = np.roll(self.E, -1, axis=1) - self.E
        return float(
            np.mean(np.abs(gx))
            + np.mean(np.abs(gy))
            + np.mean(np.abs(ex))
            + np.mean(np.abs(ey))
        )

    def update(self):
        dt = self.dt

        lap_phi = self.laplacian(self.phi_c)
        lap_E = self.laplacian(self.E)

        force_phi = lap_phi - self.gamma * self.pi_c - self.dV_dphi(self.phi_c, self.E)
        force_E = lap_E - self.gamma * self.pi_E - self.dV_dE(self.phi_c, self.E)

        # Symplectic Euler
        self.pi_c += force_phi * dt
        self.pi_E += force_E * dt
        self.phi_c += self.pi_c * dt
        self.E += self.pi_E * dt

        # Soft numerical guards
        self.phi_c = np.clip(self.phi_c, -2.5 * self.v_phi, 2.5 * self.v_phi)
        self.E = np.clip(self.E, -2.5 * self.v_E, 2.5 * self.v_E)
        self.pi_c = np.clip(self.pi_c, -10.0, 10.0)
        self.pi_E = np.clip(self.pi_E, -10.0, 10.0)

        phi_mean = float(np.mean(self.phi_c))
        E_mean = float(np.mean(self.E))
        phi_var = float(np.var(self.phi_c))
        roughness = self.compute_roughness()

        mean_score = max(0.0, phi_mean / max(self.v_phi, 1e-9))
        variance_score = math.exp(-phi_var / max(self.v_phi**2, 1e-9))
        roughness_score = math.exp(-roughness / 1.5)
        coherence = float(np.clip(mean_score * variance_score * roughness_score, 0.0, 1.0))

        if coherence > 0.90:
            status = "JHANA_ATTRACTOR_REACHED"
        elif phi_var > 0.20:
            status = "DOMAIN_COARSENING"
        elif abs(phi_mean) < 0.05 and phi_var < 0.02:
            status = "FALSE_VACUUM_QUIET"
        else:
            status = "PARTIAL_ALIGNMENT"

        self.history["phi_mean"].append(phi_mean)
        self.history["E_mean"].append(E_mean)
        self.history["phi_var"].append(phi_var)
        self.history["roughness"].append(roughness)
        self.history["coherence"].append(coherence)
        self.history["status"].append(status)

    def run(self, steps=600, substeps=5):
        for _ in range(steps):
            for _ in range(substeps):
                self.update()
        return {
            "phi_mean_final": self.history["phi_mean"][-1],
            "E_mean_final": self.history["E_mean"][-1],
            "phi_var_final": self.history["phi_var"][-1],
            "roughness_final": self.history["roughness"][-1],
            "coherence_final": self.history["coherence"][-1],
            "status_final": self.history["status"][-1],
        }


def parse_range(spec: str):
    vals = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        vals.append(float(chunk))
    return vals


def save_heatmap(matrix, xvals, yvals, title, outpath, cmap="viridis", vmin=None, vmax=None):
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--xis", type=str, default="0.000,0.005,0.010,0.020,0.040")
    parser.add_argument("--gammas", type=str, default="0.02,0.05,0.10,0.15,0.20")
    parser.add_argument("--g-couples", type=str, default="0.00,0.10,0.18,0.30")
    parser.add_argument("--seeds", type=int, default=5)
    parser.add_argument("--steps", type=int, default=500)
    parser.add_argument("--substeps", type=int, default=5)
    parser.add_argument("--grid-size", type=int, default=64)
    parser.add_argument("--outdir", type=str, default="phase_iv_b_sweep")
    args = parser.parse_args()

    xis = parse_range(args.xis)
    gammas = parse_range(args.gammas)
    g_couples = parse_range(args.g_couples)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    csv_path = outdir / "phase_iv_b_sweep_results.csv"

    rows = []
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
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
                        sim = ZoraMQGT_PhaseIV_B(
                            grid_size=args.grid_size,
                            xi=xi,
                            gamma=gamma,
                            g_couple=g_couple,
                            seed=seed,
                        )
                        result = sim.run(steps=args.steps, substeps=args.substeps)
                        row = {
                            "xi": xi,
                            "gamma": gamma,
                            "g_couple": g_couple,
                            "seed": seed,
                            **result,
                        }
                        writer.writerow(row)
                        rows.append(row)

    # Aggregate heatmaps for each g_couple
    for g_couple in g_couples:
        lock_rate = np.zeros((len(gammas), len(xis)))
        mean_coherence = np.zeros((len(gammas), len(xis)))

        for iy, gamma in enumerate(gammas):
            for ix, xi in enumerate(xis):
                subset = [
                    r
                    for r in rows
                    if abs(r["g_couple"] - g_couple) < 1e-12
                    and abs(r["gamma"] - gamma) < 1e-12
                    and abs(r["xi"] - xi) < 1e-12
                ]
                lock_hits = sum(r["status_final"] == "JHANA_ATTRACTOR_REACHED" for r in subset)
                lock_rate[iy, ix] = lock_hits / max(len(subset), 1)
                mean_coherence[iy, ix] = np.mean([r["coherence_final"] for r in subset])

        save_heatmap(
            lock_rate,
            xis,
            gammas,
            title=f"Lock rate | g={g_couple:.3f}",
            outpath=outdir / f"lock_rate_g_{g_couple:.3f}.png",
            cmap="magma",
            vmin=0.0,
            vmax=1.0,
        )
        save_heatmap(
            mean_coherence,
            xis,
            gammas,
            title=f"Mean final coherence | g={g_couple:.3f}",
            outpath=outdir / f"mean_coherence_g_{g_couple:.3f}.png",
            cmap="viridis",
            vmin=0.0,
            vmax=1.0,
        )

    # Compact markdown summary
    md_path = outdir / "summary.md"
    with md_path.open("w") as f:
        f.write("# Phase IV-B sweep summary\n\n")
        f.write(f"- xis: {xis}\n")
        f.write(f"- gammas: {gammas}\n")
        f.write(f"- g_couples: {g_couples}\n")
        f.write(f"- seeds per point: {args.seeds}\n")
        f.write(f"- steps: {args.steps}, substeps: {args.substeps}\n")
        f.write(f"- csv: `{csv_path.name}`\n\n")

        for g_couple in g_couples:
            f.write(f"## g = {g_couple:.3f}\n\n")
            subset = [r for r in rows if abs(r["g_couple"] - g_couple) < 1e-12]
            mean_c = np.mean([r["coherence_final"] for r in subset])
            lock_frac = np.mean([r["status_final"] == "JHANA_ATTRACTOR_REACHED" for r in subset])
            f.write(f"- mean coherence across all seeds/points: {mean_c:.3f}\n")
            f.write(f"- lock fraction across all seeds/points: {lock_frac:.3f}\n")
            f.write(f"- heatmap: `lock_rate_g_{g_couple:.3f}.png`\n")
            f.write(f"- heatmap: `mean_coherence_g_{g_couple:.3f}.png`\n\n")

    print(f"saved csv: {csv_path}")
    print(f"saved summary: {md_path}")
    print(f"saved heatmaps in: {outdir}")


if __name__ == "__main__":
    main()
