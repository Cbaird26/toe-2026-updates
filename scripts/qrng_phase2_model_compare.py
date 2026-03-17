#!/usr/bin/env python3
"""
Compare preregistered Phase II models on the session manifest.

Usage:
  python3 scripts/qrng_phase2_model_compare.py artifacts/phase2_sessions.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
import time
from pathlib import Path


def read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def as_float(value: str, field: str) -> float:
    if value == "":
        raise ValueError(f"Missing required field: {field}")
    return float(value)


def solve_linear_system(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    size = len(rhs)
    aug = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]

    for col in range(size):
        pivot = max(range(col, size), key=lambda idx: abs(aug[idx][col]))
        if abs(aug[pivot][col]) < 1e-12:
            raise ValueError("Singular matrix in weighted least squares")
        aug[col], aug[pivot] = aug[pivot], aug[col]

        pivot_val = aug[col][col]
        for j in range(col, size + 1):
            aug[col][j] /= pivot_val

        for row in range(size):
            if row == col:
                continue
            factor = aug[row][col]
            for j in range(col, size + 1):
                aug[row][j] -= factor * aug[col][j]

    return [aug[row][size] for row in range(size)]


def weighted_least_squares(design: list[list[float]], y: list[float], weights: list[float]) -> tuple[list[float], float]:
    cols = len(design[0])
    xtwx = [[0.0 for _ in range(cols)] for _ in range(cols)]
    xtwy = [0.0 for _ in range(cols)]

    for i, row in enumerate(design):
        w = weights[i]
        for a in range(cols):
            xtwy[a] += w * row[a] * y[i]
            for b in range(cols):
                xtwx[a][b] += w * row[a] * row[b]

    beta = solve_linear_system(xtwx, xtwy)
    rss = 0.0
    for i, row in enumerate(design):
        y_hat = sum(beta[j] * row[j] for j in range(cols))
        rss += weights[i] * ((y[i] - y_hat) ** 2)
    return beta, rss


def information_criteria(rss: float, n: int, k: int) -> tuple[float, float]:
    rss = max(rss, 1e-18)
    aic = n * math.log(rss / n) + 2 * k
    if n - k - 1 > 0:
        aicc = aic + (2 * k * (k + 1)) / (n - k - 1)
    else:
        aicc = float("inf")
    bic = n * math.log(rss / n) + k * math.log(n)
    return aicc, bic


def fit_null(y: list[float], weights: list[float]) -> dict[str, object]:
    beta, rss = weighted_least_squares([[1.0] for _ in y], y, weights)
    return {"name": "null", "params": {"beta0": beta[0]}, "rss": rss, "k": 1}


def fit_linear(x: list[float], y: list[float], weights: list[float]) -> dict[str, object]:
    design = [[1.0, value] for value in x]
    beta, rss = weighted_least_squares(design, y, weights)
    return {"name": "linear", "params": {"beta0": beta[0], "beta1": beta[1]}, "rss": rss, "k": 2}


def step_thresholds(x: list[float]) -> list[float]:
    unique = sorted(set(x))
    if len(unique) < 2:
        return unique
    return [(unique[i] + unique[i + 1]) / 2.0 for i in range(len(unique) - 1)]


def fit_step(x: list[float], y: list[float], weights: list[float]) -> dict[str, object]:
    best: dict[str, object] | None = None
    for threshold in step_thresholds(x):
        basis = [1.0 if value >= threshold else 0.0 for value in x]
        beta, rss = weighted_least_squares([[1.0, b] for b in basis], y, weights)
        candidate = {
            "name": "step_threshold",
            "params": {"beta0": beta[0], "amplitude": beta[1], "threshold": threshold},
            "rss": rss,
            "k": 3,
        }
        if best is None or candidate["rss"] < best["rss"]:
            best = candidate
    if best is None:
        raise ValueError("Unable to fit step threshold model")
    return best


def logistic_basis(x: list[float], threshold: float, scale: float) -> list[float]:
    values: list[float] = []
    for point in x:
        z = max(min((point - threshold) / scale, 60.0), -60.0)
        values.append(1.0 / (1.0 + math.exp(-z)))
    return values


def fit_logistic(x: list[float], y: list[float], weights: list[float]) -> dict[str, object]:
    unique = sorted(set(x))
    span = max(unique) - min(unique) if unique else 0.0
    scale_candidates = [max(span * frac, 1e-6) for frac in (0.05, 0.1, 0.2, 0.5, 1.0)]

    best: dict[str, object] | None = None
    for threshold in step_thresholds(x):
        for scale in scale_candidates:
            basis = logistic_basis(x, threshold, scale)
            beta, rss = weighted_least_squares([[1.0, b] for b in basis], y, weights)
            candidate = {
                "name": "logistic_threshold",
                "params": {
                    "beta0": beta[0],
                    "amplitude": beta[1],
                    "threshold": threshold,
                    "scale": scale,
                },
                "rss": rss,
                "k": 4,
            }
            if best is None or candidate["rss"] < best["rss"]:
                best = candidate
    if best is None:
        raise ValueError("Unable to fit logistic threshold model")
    return best


def summarize_rungs(rows: list[dict[str, float]]) -> list[dict[str, float]]:
    grouped: dict[int, list[dict[str, float]]] = {}
    for row in rows:
        grouped.setdefault(int(row["agent_count"]), []).append(row)

    summary: list[dict[str, float]] = []
    for agent_count in sorted(grouped):
        group = grouped[agent_count]
        summary.append(
            {
                "agent_count": agent_count,
                "sessions": len(group),
                "mean_effective_agents": statistics.fmean(item["effective_agents"] for item in group),
                "mean_coherence": statistics.fmean(item["coherence_score"] for item in group),
                "mean_delta_p": statistics.fmean(item["delta_p"] for item in group),
                "mean_z_score": statistics.fmean(item["z_score"] for item in group),
            }
        )
    return summary


def prepare_rows(raw_rows: list[dict[str, str]]) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for raw in raw_rows:
        if raw.get("status") and raw["status"] not in {"completed", "planned"}:
            continue
        if raw.get("deviation_from_50pct", "") == "":
            continue

        bits = as_float(raw.get("bits_collected", "") or raw.get("bits_requested", ""), "bits_collected")
        coherence = as_float(raw["coherence_score"], "coherence_score")
        effective_agents = (
            as_float(raw["effective_agents"], "effective_agents")
            if raw.get("effective_agents", "") != ""
            else as_float(raw["agent_count"], "agent_count") * coherence
        )
        rows.append(
            {
                "agent_count": as_float(raw["agent_count"], "agent_count"),
                "coherence_score": coherence,
                "effective_agents": effective_agents,
                "delta_p": as_float(raw["deviation_from_50pct"], "deviation_from_50pct"),
                "z_score": as_float(raw["z_score"], "z_score"),
                "se": 0.5 / math.sqrt(bits),
                "bits": bits,
            }
        )
    if len(rows) < 4:
        raise ValueError("Need at least 4 completed sessions to compare models")
    return rows


def choose_interpretation(models: list[dict[str, object]]) -> str:
    ranked = sorted(models, key=lambda item: item["aicc"])
    best = ranked[0]
    null_model = next(model for model in ranked if model["name"] == "null")
    if best["name"] == "null" or (null_model["aicc"] - best["aicc"]) < 4:
        return "no_support"
    if best["name"] == "linear" and best["params"]["beta1"] > 0:
        return "additive_candidate"
    if best["name"] in {"step_threshold", "logistic_threshold"} and best["params"]["amplitude"] > 0:
        linear_model = next(model for model in ranked if model["name"] == "linear")
        if (linear_model["aicc"] - best["aicc"]) >= 4:
            return "threshold_candidate"
    return "ambiguous_nonnull"


def compare_models(manifest_path: Path, out_path: Path | None) -> int:
    raw_rows = read_manifest(manifest_path)
    rows = prepare_rows(raw_rows)

    x = [row["effective_agents"] for row in rows]
    y = [row["delta_p"] for row in rows]
    weights = [1.0 / (row["se"] ** 2) for row in rows]

    models = [
        fit_null(y, weights),
        fit_linear(x, y, weights),
        fit_step(x, y, weights),
        fit_logistic(x, y, weights),
    ]

    for model in models:
        aicc, bic = information_criteria(model["rss"], len(rows), model["k"])
        model["aicc"] = aicc
        model["bic"] = bic

    models.sort(key=lambda item: item["aicc"])
    best_name = models[0]["name"]
    interpretation = choose_interpretation(models)

    report = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "manifest": str(manifest_path),
        "n_sessions": len(rows),
        "n_rungs": len({row["agent_count"] for row in rows}),
        "best_model": best_name,
        "interpretation": interpretation,
        "models": models,
        "rung_summary": summarize_rungs(rows),
    }

    if out_path is None:
        out_path = manifest_path.parent / f"{manifest_path.stem}_model_compare.json"
    with out_path.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    print(f"[Phase II] Wrote model comparison: {out_path}")
    print(f"[Phase II] Best model: {best_name} ({interpretation})")
    for model in models:
        print(
            f"  - {model['name']}: AICc={model['aicc']:.3f}, "
            f"BIC={model['bic']:.3f}, params={json.dumps(model['params'], sort_keys=True)}"
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compare QRNG Phase II models on the session manifest")
    parser.add_argument("manifest", help="Path to phase2_sessions.csv")
    parser.add_argument("--out", default="", help="Optional JSON output path")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    out_path = Path(args.out) if args.out else None

    try:
        return compare_models(manifest_path, out_path)
    except Exception as exc:  # noqa: BLE001 - print a readable CLI error
        print(f"[Phase II] ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
