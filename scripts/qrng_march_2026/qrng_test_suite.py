#!/usr/bin/env python3
"""
QRNG Randomness Test Suite — MQGT-SCF Baseline Diagnostics

Runs a statistical battery on QRNG CSV output: bias, runs, autocorrelation,
block frequency, serial tests, entropy. Produces JSON report and optional plots.

Usage:
  python scripts/qrng_test_suite.py artifacts/anu_qrng_baseline_*.csv
  python scripts/qrng_test_suite.py artifacts/qrng_experiment_*.csv --plots
  python scripts/qrng_test_suite.py data.csv --out reports/

Supports both collector format (trial,bit) and experiment format (session_id,...,bit).
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import binomtest, chisquare


def load_bits(path: Path) -> list[int]:
    """Load bits from CSV. Auto-detect format: 'bit' column or second column (trial,bit)."""
    bits: list[int] = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"No header in {path}")
        fieldnames = [c.strip() for c in reader.fieldnames]
        if "bit" in fieldnames:
            bit_col = "bit"
        else:
            # trial,bit format: second column
            if len(fieldnames) < 2:
                raise ValueError(f"Expected 'bit' or 'trial,bit' format, got {fieldnames}")
            bit_col = fieldnames[1]
        for row in reader:
            val = row.get(bit_col, "").strip()
            if val in ("0", "1"):
                bits.append(int(val))
    return bits


def run_bias_test(bits: np.ndarray) -> dict[str, Any]:
    """Binomial test vs 0.5."""
    n = len(bits)
    ones = int(bits.sum())
    bt = binomtest(ones, n, 0.5)
    p_hat = ones / n
    std_mean = 0.5 / (n ** 0.5)
    z = (p_hat - 0.5) / std_mean if std_mean > 0 else float("nan")
    return {"n": n, "ones": ones, "p_hat": float(p_hat), "pvalue": bt.pvalue, "z_score": float(z)}


def run_runs_test(bits: np.ndarray) -> dict[str, Any]:
    """Wald-Wolfowitz runs test."""
    n = len(bits)
    ones = int(bits.sum())
    runs = 1 + int(np.sum(bits[1:] != bits[:-1]))
    expected = (2 * ones * (n - ones)) / n + 1
    var_term = 2 * ones * (n - ones) * (2 * ones * (n - ones) - n)
    variance = var_term / (n ** 2 * (n - 1)) if n > 1 else 0.0
    std_runs = math.sqrt(variance) if variance > 0 else 1.0
    runs_z = (runs - expected) / std_runs if std_runs > 0 else 0.0
    return {
        "runs": runs,
        "expected_runs": float(expected),
        "variance": float(variance),
        "z_score": float(runs_z),
    }


def run_block_frequency_test(bits: np.ndarray, block_size: int = 1000) -> dict[str, Any]:
    """Chi-square test across blocks. Tests homogeneity with expected proportion 0.5."""
    n = len(bits)
    n_blocks = n // block_size
    if n_blocks < 2:
        return {"chi2": float("nan"), "pvalue": float("nan"), "n_blocks": n_blocks}
    obs = [int(bits[i * block_size : (i + 1) * block_size].sum()) for i in range(n_blocks)]
    obs_total = sum(obs)
    exp_unscaled = (block_size / 2) * n_blocks
    exp = [x * obs_total / exp_unscaled for x in [block_size / 2] * n_blocks]
    chi2, p = chisquare(obs, exp)
    return {
        "block_size": block_size,
        "n_blocks": n_blocks,
        "chi2": float(chi2),
        "pvalue": float(p),
        "block_mean_avg": float(np.mean(obs) / block_size),
        "block_mean_std": float(np.std(obs) / block_size),
    }


def run_serial_2bit_test(bits: np.ndarray) -> dict[str, Any]:
    """Count 00, 01, 10, 11; chi-square vs 25% each."""
    pairs = {"00": 0, "01": 0, "10": 0, "11": 0}
    for i in range(len(bits) - 1):
        key = f"{int(bits[i])}{int(bits[i+1])}"
        pairs[key] = pairs.get(key, 0) + 1
    n_pairs = sum(pairs.values())
    obs = list(pairs.values())
    exp = [n_pairs / 4] * 4
    chi2, p = chisquare(obs, exp)
    freqs = {k: v / n_pairs for k, v in pairs.items()}
    return {"counts": pairs, "frequencies": freqs, "chi2": float(chi2), "pvalue": float(p)}


def run_serial_3bit_test(bits: np.ndarray) -> dict[str, Any]:
    """Count 000..111; chi-square vs 1/8 each."""
    patterns = {f"{i:03b}": 0 for i in range(8)}
    for i in range(len(bits) - 2):
        key = f"{int(bits[i])}{int(bits[i+1])}{int(bits[i+2])}"
        patterns[key] = patterns.get(key, 0) + 1
    n_triples = sum(patterns.values())
    obs = list(patterns.values())
    exp = [n_triples / 8] * 8
    chi2, p = chisquare(obs, exp)
    freqs = {k: v / n_triples for k, v in patterns.items()}
    return {"counts": patterns, "frequencies": freqs, "chi2": float(chi2), "pvalue": float(p)}


def run_autocorrelation_test(bits: np.ndarray, max_lag: int = 100) -> dict[str, Any]:
    """Autocorrelation at lags 1 to max_lag."""
    n = len(bits)
    max_lag = min(max_lag, max(1, n // 10))
    autocorr = {}
    for lag in range(1, max_lag + 1):
        x = bits[:-lag]
        y = bits[lag:]
        if len(x) < 10:
            break
        corr = float(np.corrcoef(x, y)[0, 1]) if np.std(x) > 0 and np.std(y) > 0 else 0.0
        autocorr[lag] = corr if not np.isnan(corr) else 0.0
    return {"max_lag": max_lag, "autocorrelation": autocorr}


def run_entropy_test(bits: np.ndarray) -> dict[str, Any]:
    """Shannon entropy in bits per bit."""
    n = len(bits)
    p1 = float(bits.sum()) / n
    p0 = 1 - p1
    if p0 > 0 and p1 > 0:
        entropy = -(p0 * math.log2(p0) + p1 * math.log2(p1))
    else:
        entropy = 0.0
    return {"entropy_bits_per_bit": float(entropy), "p0": p0, "p1": p1}


def run_battery(bits: np.ndarray) -> dict[str, Any]:
    """Run full randomness battery."""
    return {
        "bias": run_bias_test(bits),
        "runs": run_runs_test(bits),
        "block_frequency": run_block_frequency_test(bits),
        "serial_2bit": run_serial_2bit_test(bits),
        "serial_3bit": run_serial_3bit_test(bits),
        "autocorrelation": run_autocorrelation_test(bits),
        "entropy": run_entropy_test(bits),
    }


def print_summary(report: dict[str, Any], path: Path) -> None:
    """Print console summary with pass/fail hints."""
    bias = report["bias"]
    runs = report["runs"]
    ent = report["entropy"]
    ac = report["autocorrelation"]

    print(f"\n=== QRNG Report: {path.name} ===\n")
    print(f"  N:           {bias['n']}")
    print(f"  P(1):        {bias['p_hat']:.6f}")
    print(f"  Bias p:      {bias['pvalue']:.6g}")
    print(f"  Runs z:      {runs['z_score']:.4f}")
    print(f"  Entropy:     {ent['entropy_bits_per_bit']:.6f} bits/bit")

    ac_vals = list(ac["autocorrelation"].values())
    max_ac = max(abs(v) for v in ac_vals) if ac_vals else 0
    print(f"  Max |AC|:    {max_ac:.6f} (lag 1-{ac['max_lag']})")

    print("\n  Serial 2-bit:", {k: f"{v:.4f}" for k, v in report["serial_2bit"]["frequencies"].items()})

    # Pass/fail hints
    ok_bias = bias["pvalue"] > 0.05
    ok_runs = -2 <= runs["z_score"] <= 2
    ok_entropy = 0.99 <= ent["entropy_bits_per_bit"] <= 1.01
    ok_ac = max_ac < 0.02

    status = "PASS" if (ok_bias and ok_runs and ok_entropy and ok_ac) else "REVIEW"
    print(f"\n  Status:      {status}")
    if not ok_bias:
        print("    - Bias p < 0.05: possible systematic bias")
    if not ok_runs:
        print("    - Runs z outside [-2,2]: unusual clustering")
    if not ok_entropy:
        print("    - Entropy deviates from 1.0")
    if not ok_ac:
        print("    - Autocorrelation exceeds 0.02")


def make_plots(bits: np.ndarray, out_path: Path) -> None:
    """Generate 3-panel figure: cumulative deviation, block means histogram, autocorrelation."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        raise RuntimeError("Plots require matplotlib. Run: pip install matplotlib")

    report = run_battery(np.array(bits, dtype=np.int_))
    n = len(bits)

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    # Panel 1: Cumulative deviation (random walk)
    cumdev = np.cumsum(bits - 0.5)
    axes[0].plot(cumdev, color="steelblue", linewidth=0.5, alpha=0.8)
    axes[0].axhline(0, color="gray", linestyle="--")
    axes[0].set_xlabel("Bit index")
    axes[0].set_ylabel("Cumulative deviation")
    axes[0].set_title("Cumulative deviation (bits - 0.5)")
    axes[0].grid(True, alpha=0.3)

    # Panel 2: Block means histogram
    block_size = 1000
    n_blocks = n // block_size
    block_means = [bits[i * block_size : (i + 1) * block_size].mean() for i in range(n_blocks)]
    axes[1].hist(block_means, bins=min(30, n_blocks), color="steelblue", edgecolor="white", alpha=0.8)
    axes[1].axvline(0.5, color="red", linestyle="--", label="Expected 0.5")
    axes[1].set_xlabel("Block mean")
    axes[1].set_ylabel("Count")
    axes[1].set_title(f"Block means (size={block_size})")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    # Panel 3: Autocorrelation spectrum
    ac = report["autocorrelation"]["autocorrelation"]
    lags = list(ac.keys())
    vals = list(ac.values())
    axes[2].bar(lags, vals, color="steelblue", alpha=0.8, width=0.8)
    axes[2].axhline(0, color="gray", linestyle="-")
    axes[2].set_xlabel("Lag")
    axes[2].set_ylabel("Correlation")
    axes[2].set_title("Autocorrelation spectrum")
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=100, bbox_inches="tight")
    plt.close()
    print(f"  Plots saved to {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="QRNG randomness test suite")
    parser.add_argument("csv", type=str, help="Path to QRNG CSV (or glob pattern)")
    parser.add_argument("--out", type=str, default="", help="Output directory (default: same as input)")
    parser.add_argument("--plots", action="store_true", help="Generate diagnostic plots")
    args = parser.parse_args()

    path = Path(args.csv)
    if not path.exists():
        print(f"ERROR: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    bits_list = load_bits(path)
    if len(bits_list) < 100:
        print(f"ERROR: Too few bits ({len(bits_list)}). Need at least 100.", file=sys.stderr)
        sys.exit(1)

    bits = np.array(bits_list, dtype=np.int_)
    report = run_battery(bits)

    out_dir = Path(args.out) if args.out else path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = path.stem.replace("_bits", "")
    report_path = out_dir / f"{stem}_report.json"

    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Report saved to {report_path}")

    print_summary(report, path)

    if args.plots:
        plots_path = out_dir / f"{stem}_plots.png"
        make_plots(bits, plots_path)


if __name__ == "__main__":
    main()
