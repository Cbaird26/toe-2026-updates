#!/usr/bin/env python3
"""
MQGT-SCF — Phase IV-B symmetry-breaking lattice demo (exploratory).

This extends the Phase IV pedagogical toy with:
  - Signed fields (no forced nonnegative vacuum) and double-well local potentials
  - Explicit coupling -g*phi*E and tilt -xi*(phi + kappa*E) in the potential
  - Damped second-order (symplectic Euler) lattice dynamics
  - A non-degenerate coherence score: flat phi≈0 scores low, not high

Potential (scalars on the lattice; same form at each site):

  V ⊃ (λ_φ/4)(φ² - v_φ²)² + (λ_E/4)(E² - v_E²)² - g φ E - ξ(φ + κ E)

So (with φ ≡ Φ_c, E ≡ ethical scalar):

  ∂V/∂φ = λ_φ φ (φ² - v_φ²) - g E - ξ
  ∂V/∂E = λ_E E (E² - v_E²) - g φ - ξ κ

This is an execution-layer visualization toy, not H1/H2 evidence. H2 interferometry
remains the primary falsification pathway in this repo.

Dependencies: numpy, matplotlib
  pip install numpy matplotlib

Examples:
  python scripts/mqgt_sim/mqgt_phase4b_symmetry_breaking_demo.py
  python scripts/mqgt_sim/mqgt_phase4b_symmetry_breaking_demo.py \\
    --save-dir papers_sources/figures/phase4b_lattice --no-show
"""

from __future__ import annotations

import argparse
import json
import os
from collections import deque


def periodic_laplacian(field):
    """5-point periodic Laplacian on a 2D lattice."""
    import numpy as np

    return (
        np.roll(field, 1, axis=0)
        + np.roll(field, -1, axis=0)
        + np.roll(field, 1, axis=1)
        + np.roll(field, -1, axis=1)
        - 4.0 * field
    )


DEFAULT_INJECTIONS = [
    {"step": 0, "field": "phi", "x_norm": 0.30, "y_norm": 0.35, "magnitude": 0.45, "sigma_norm": 0.06},
    {"step": 0, "field": "phi", "x_norm": 0.72, "y_norm": 0.65, "magnitude": -0.40, "sigma_norm": 0.08},
    {"step": 0, "field": "E", "x_norm": 0.50, "y_norm": 0.50, "magnitude": 0.35, "sigma_norm": 0.10},
    {"step": 80, "field": "phi", "x_norm": 0.20, "y_norm": 0.75, "magnitude": 0.30, "sigma_norm": 0.06},
    {"step": 160, "field": "E", "x_norm": 0.78, "y_norm": 0.22, "magnitude": -0.28, "sigma_norm": 0.07},
]


class Phase4bLattice:
    """Damped wave-style lattice with double-well potential and phi–E coupling."""

    def __init__(
        self,
        grid_size: int,
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
        phi_noise: float = 0.08,
        pi_noise: float = 0.01,
        safe_phi: float = 2.5,
        safe_pi: float = 12.0,
    ):
        import numpy as np

        self.N = grid_size
        self.dt = dt
        self.xi = xi
        self.kappa = kappa
        self.gamma = gamma
        self.g = g_couple
        self.lambda_phi = lambda_phi
        self.lambda_E = lambda_E
        self.v_phi = max(v_phi, 1e-9)
        self.v_E = max(v_E, 1e-9)
        self.safe_phi = safe_phi
        self.safe_pi = safe_pi

        rng = np.random.default_rng(seed)
        self.phi = rng.normal(0.0, phi_noise, (self.N, self.N))
        self.E = rng.normal(0.0, phi_noise, (self.N, self.N))
        self.pi_c = rng.normal(0.0, pi_noise, (self.N, self.N))
        self.pi_E = rng.normal(0.0, pi_noise, (self.N, self.N))

        self.history = {
            "phi_mean": [],
            "E_mean": [],
            "phi_var": [],
            "coherence": [],
            "roughness": [],
            "status": [],
        }
        self._recent_coherence: deque[float] = deque(maxlen=30)

    def dV_dphi(self, phi, E):
        import numpy as np

        return self.lambda_phi * phi * (phi**2 - self.v_phi**2) - self.g * E - self.xi

    def dV_dE(self, phi, E):
        import numpy as np

        return self.lambda_E * E * (E**2 - self.v_E**2) - self.g * phi - self.xi * self.kappa

    def roughness(self) -> float:
        import numpy as np

        def grads(f):
            gx = np.roll(f, -1, axis=0) - f
            gy = np.roll(f, -1, axis=1) - f
            return np.mean(np.abs(gx)) + np.mean(np.abs(gy))

        return float(grads(self.phi) + grads(self.E))

    def inject_gaussian(self, field_name: str, x_norm: float, y_norm: float, magnitude: float, sigma_norm: float):
        import numpy as np

        x = float(x_norm) * (self.N - 1)
        y = float(y_norm) * (self.N - 1)
        yy, xx = np.mgrid[0 : self.N, 0 : self.N]
        sigma = max(1.0, float(sigma_norm) * self.N)
        pulse = magnitude * np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (2.0 * sigma**2))
        if field_name == "phi":
            self.phi = self.phi + pulse
        elif field_name == "E":
            self.E = self.E + pulse
        else:
            raise ValueError("field must be 'phi' or 'E'")

    def integrate_step(self):
        import numpy as np

        dt = self.dt
        lap_p = periodic_laplacian(self.phi)
        lap_e = periodic_laplacian(self.E)

        f_phi = lap_p - self.gamma * self.pi_c - self.dV_dphi(self.phi, self.E)
        f_E = lap_e - self.gamma * self.pi_E - self.dV_dE(self.phi, self.E)

        self.pi_c = self.pi_c + f_phi * dt
        self.pi_E = self.pi_E + f_E * dt
        self.phi = self.phi + self.pi_c * dt
        self.E = self.E + self.pi_E * dt

        lim_p = self.safe_phi * self.v_phi
        lim_e = self.safe_phi * self.v_E
        self.phi = np.clip(self.phi, -lim_p, lim_p)
        self.E = np.clip(self.E, -lim_e, lim_e)
        self.pi_c = np.clip(self.pi_c, -self.safe_pi, self.safe_pi)
        self.pi_E = np.clip(self.pi_E, -self.safe_pi, self.safe_pi)

    def coherence_and_status(self) -> tuple[float, float, float, float, float, str]:
        import numpy as np

        phi_mean = float(np.mean(self.phi))
        e_mean = float(np.mean(self.E))
        phi_var = float(np.var(self.phi))
        rough = self.roughness()

        mean_score = max(0.0, phi_mean / self.v_phi)
        variance_score = float(np.exp(-phi_var / max(self.v_phi**2, 1e-12)))
        roughness_score = float(np.exp(-rough / 1.5))
        coherence = float(np.clip(mean_score * variance_score * roughness_score, 0.0, 1.0))

        self._recent_coherence.append(coherence)
        persistent = (
            len(self._recent_coherence) == self._recent_coherence.maxlen
            and float(np.std(self._recent_coherence)) < 0.012
        )

        if coherence > 0.90 and persistent:
            status = "ATTRACTOR_LOCKED"
        elif phi_var > 0.20:
            status = "DOMAIN_COARSENING"
        elif abs(phi_mean) < 0.05 and phi_var < 0.02 and rough < 0.08:
            status = "FALSE_VACUUM_OR_QUIET"
        elif coherence > 0.35:
            status = "PARTIAL_ALIGNMENT"
        else:
            status = "TRANSIENT_PATTERNING"

        return phi_mean, e_mean, phi_var, rough, coherence, status

    def record(self):
        phi_mean, e_mean, phi_var, rough, coherence, status = self.coherence_and_status()
        self.history["phi_mean"].append(phi_mean)
        self.history["E_mean"].append(e_mean)
        self.history["phi_var"].append(phi_var)
        self.history["coherence"].append(coherence)
        self.history["roughness"].append(rough)
        self.history["status"].append(status)


def load_injections(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        raise ValueError("inject-spec JSON must be a list of injection objects")
    return data


def run_demo(
    grid_size: int,
    recorded_steps: int,
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
    injections: list[dict],
    use_default_injections: bool,
):
    import numpy as np

    if use_default_injections:
        inj_list = list(DEFAULT_INJECTIONS)
    else:
        inj_list = []
    inj_list.extend(injections)
    by_step: dict[int, list[dict]] = {}
    for item in inj_list:
        st = int(item["step"])
        by_step.setdefault(st, []).append(item)

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

    total_integrator_steps = 0
    for frame in range(recorded_steps):
        if frame in by_step:
            for inj in by_step[frame]:
                sim.inject_gaussian(
                    str(inj["field"]),
                    float(inj["x_norm"]),
                    float(inj["y_norm"]),
                    float(inj["magnitude"]),
                    float(inj.get("sigma_norm", 0.08)),
                )
        for _ in range(max(1, substeps)):
            sim.integrate_step()
            total_integrator_steps += 1
        sim.record()

    last_status = sim.history["status"][-1] if sim.history["status"] else "INITIALIZING"
    final_metrics = {
        "phi_mean": sim.history["phi_mean"][-1],
        "E_mean": sim.history["E_mean"][-1],
        "phi_var": sim.history["phi_var"][-1],
        "coherence": sim.history["coherence"][-1],
        "roughness": sim.history["roughness"][-1],
        "status": last_status,
        "phi_min": float(np.min(sim.phi)),
        "phi_max": float(np.max(sim.phi)),
        "E_min": float(np.min(sim.E)),
        "E_max": float(np.max(sim.E)),
        "total_integrator_steps": total_integrator_steps,
    }

    parameters = {
        "grid_size": grid_size,
        "recorded_steps": recorded_steps,
        "substeps": substeps,
        "dt": dt,
        "seed": seed,
        "xi": xi,
        "kappa": kappa,
        "gamma": gamma,
        "g_couple": g_couple,
        "lambda_phi": lambda_phi,
        "lambda_E": lambda_E,
        "v_phi": v_phi,
        "v_E": v_E,
        "potential_note": (
            "V includes (λ_φ/4)(φ²-v_φ²)² + (λ_E/4)(E²-v_E²)² - g φ E - ξ(φ+κE); "
            "derivatives match this normalization."
        ),
    }

    return {
        "phi": sim.phi,
        "E": sim.E,
        "history": sim.history,
        "final_metrics": final_metrics,
        "parameters": parameters,
    }


def plot_results(result, save_path: str = "", no_show: bool = False):
    import matplotlib

    if no_show or save_path:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    phi = result["phi"]
    efield = result["E"]
    history = result["history"]
    final_metrics = result["final_metrics"]
    params = result["parameters"]
    n = len(history["phi_mean"])
    steps_axis = list(range(1, n + 1))
    vm = max(params["v_phi"], params["v_E"], 0.01) * 1.2

    fig, axs = plt.subplots(2, 2, figsize=(13, 9), constrained_layout=True)

    im1 = axs[0, 0].imshow(phi, cmap="seismic", vmin=-vm, vmax=vm, origin="upper")
    axs[0, 0].set_title(r"$\Phi_c$ lattice (signed, double-well toy)")
    fig.colorbar(im1, ax=axs[0, 0], fraction=0.046, pad=0.04)

    im2 = axs[0, 1].imshow(efield, cmap="seismic", vmin=-vm, vmax=vm, origin="upper")
    axs[0, 1].set_title(r"$E$ lattice (signed, double-well toy)")
    fig.colorbar(im2, ax=axs[0, 1], fraction=0.046, pad=0.04)

    axs[1, 0].plot(steps_axis, history["phi_mean"], label=r"mean $\Phi_c$", lw=2)
    axs[1, 0].plot(steps_axis, history["E_mean"], label=r"mean $E$", lw=2)
    axs[1, 0].set_title("Field means (recorded frames)")
    axs[1, 0].set_xlabel("frame")
    axs[1, 0].legend()
    axs[1, 0].grid(True, alpha=0.3)

    axs[1, 1].plot(steps_axis, history["coherence"], label="coherence", lw=2, color="tab:red")
    axs[1, 1].plot(steps_axis, history["phi_var"], label=r"var($\Phi_c$)", lw=1.5, color="tab:purple", alpha=0.85)
    axs[1, 1].plot(steps_axis, history["roughness"], label="roughness", lw=1.5, color="tab:orange", alpha=0.85)
    axs[1, 1].axhline(0.90, color="gray", ls="--", lw=1, label="lock threshold")
    axs[1, 1].set_title("Non-degenerate order metrics")
    axs[1, 1].set_xlabel("frame")
    axs[1, 1].legend(loc="best", fontsize=8)
    axs[1, 1].grid(True, alpha=0.3)

    fig.suptitle(
        f"Phase IV-B symmetry-breaking demo | status={final_metrics['status']} | "
        f"xi={params['xi']:.4f} | C={final_metrics['coherence']:.3f}",
        fontsize=13,
    )

    if save_path:
        fig.savefig(save_path, dpi=160)
        print(f"Wrote {save_path}")
    if not no_show:
        plt.show()
    else:
        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(
        description="Phase IV-B: double-well + damped wave dynamics (exploratory MQGT-SCF lattice toy)"
    )
    parser.add_argument("--grid-size", type=int, default=80, help="Lattice N×N")
    parser.add_argument("--steps", type=int, default=400, help="Number of recorded frames")
    parser.add_argument("--substeps", type=int, default=4, help="Integrator steps per recorded frame")
    parser.add_argument("--dt", type=float, default=0.04, help="Time step")
    parser.add_argument("--seed", type=int, default=7, help="RNG seed")
    parser.add_argument("--xi", type=float, default=0.02, help="Teleological tilt coefficient ξ")
    parser.add_argument("--kappa", type=float, default=0.60, help="Tilt weight κ on E in -ξ(φ+κE)")
    parser.add_argument("--gamma", type=float, default=0.15, help="Momentum damping γ")
    parser.add_argument("--g-couple", type=float, default=0.18, help="φ–E coupling g in -g φ E")
    parser.add_argument("--lambda-phi", type=float, default=1.0, help="λ_φ in (λ_φ/4)(φ²-v_φ²)²")
    parser.add_argument("--lambda-e", type=float, default=1.0, help="λ_E in (λ_E/4)(E²-v_E²)²")
    parser.add_argument("--v-phi", type=float, default=1.0, help="v_φ (well scale for Φ_c)")
    parser.add_argument("--v-e", type=float, default=1.0, help="v_E (well scale for E)")
    parser.add_argument(
        "--no-default-injections",
        action="store_true",
        help="Disable built-in Gaussian seeds (may wash to quiet vacuum)",
    )
    parser.add_argument(
        "--inject-spec",
        default="",
        help="JSON file: list of {step, field, x_norm, y_norm, magnitude, sigma_norm?}",
    )
    parser.add_argument("--save-dir", default="", help="Write PNG + JSON summary here")
    parser.add_argument("--no-show", action="store_true", help="Headless (Agg backend)")
    args = parser.parse_args()

    if args.grid_size <= 1:
        raise SystemExit("--grid-size must be > 1")
    if args.steps <= 0:
        raise SystemExit("--steps must be > 0")
    if args.dt <= 0:
        raise SystemExit("--dt must be > 0")

    extra_injections: list[dict] = []
    if args.inject_spec:
        extra_injections = load_injections(args.inject_spec)

    result = run_demo(
        grid_size=args.grid_size,
        recorded_steps=args.steps,
        substeps=args.substeps,
        dt=args.dt,
        seed=args.seed,
        xi=args.xi,
        kappa=args.kappa,
        gamma=args.gamma,
        g_couple=args.g_couple,
        lambda_phi=args.lambda_phi,
        lambda_E=args.lambda_e,
        v_phi=args.v_phi,
        v_E=args.v_e,
        injections=extra_injections,
        use_default_injections=not args.no_default_injections,
    )

    save_path = ""
    json_path = ""
    if args.save_dir:
        os.makedirs(args.save_dir, exist_ok=True)
        save_path = os.path.join(args.save_dir, "mqgt_phase4b_symmetry_breaking_demo.png")
        json_path = os.path.join(args.save_dir, "mqgt_phase4b_symmetry_breaking_demo_summary.json")

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

    fm = result["final_metrics"]
    print(
        f"final_status={fm['status']} phi_mean={fm['phi_mean']:+.4f} E_mean={fm['E_mean']:+.4f} "
        f"coherence={fm['coherence']:.4f}"
    )


if __name__ == "__main__":
    main()
