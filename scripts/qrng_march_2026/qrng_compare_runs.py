#!/usr/bin/env python3
"""
QRNG Multi-Run Comparison — MQGT-SCF Baseline vs Baseline / Intervention

Compares multiple QRNG runs: mean, entropy, pair frequencies, KS tests.
Useful to detect "one interesting run that never repeats."

Usage:
  python scripts/qrng_compare_runs.py artifacts/run1.csv artifacts/run2.csv
  python scripts/qrng_compare_runs.py artifacts/*.csv --out artifacts/
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import ks_2samp

# Import load_bits from test suite
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))
from qrng_test_suite import load_bits


def shannon_entropy(bits: np.ndarray) -> float:
    """Shannon entropy in bits per bit."""
    n = len(bits)
    p1 = float(bits.sum()) / n
    p0 = 1 - p1
    if p0 > 0 and p1 > 0:
        return -(p0 * math.log2(p0) + p1 * math.log2(p1))
    return 0.0


def pair_frequencies(bits: np.ndarray) -> dict[str, float]:
    """Frequencies of 00, 01, 10, 11."""
    pairs = {"00": 0, "01": 0, "10": 0, "11": 0}
    for i in range(len(bits) - 1):
        key = f"{int(bits[i])}{int(bits[i+1])}"
        pairs[key] = pairs.get(key, 0) + 1
    n = sum(pairs.values())
    return {k: v / n for k, v in pairs.items()}


def permutation_test_mean_diff(a: np.ndarray, b: np.ndarray, n_perm: int = 1000) -> float:
    """Two-tailed permutation test on mean difference."""
    obs_diff = float(b.mean() - a.mean())
    combined = np.concatenate([a, b])
    na = len(a)
    rng = np.random.default_rng(42)
    count = 0
    for _ in range(n_perm):
        perm = rng.permutation(combined)
        perm_diff = perm[na:].mean() - perm[:na].mean()
        if abs(perm_diff) >= abs(obs_diff):
            count += 1
    return (count + 1) / (n_perm + 1)


def compare_runs(paths: list[Path]) -> dict[str, Any]:
    """Compare multiple QRNG runs."""
    results: list[dict[str, Any]] = []
    bits_list: list[np.ndarray] = []

    for p in paths:
        bits = np.array(load_bits(p), dtype=np.int_)
        bits_list.append(bits)
        p1 = float(bits.sum()) / len(bits)
        entropy = shannon_entropy(bits)
        pairs = pair_frequencies(bits)
        results.append({
            "path": str(p.name),
            "n": len(bits),
            "p1": p1,
            "entropy": entropy,
            "pair_frequencies": pairs,
        })

    # Pairwise comparisons
    pairwise: list[dict[str, Any]] = []
    for i in range(len(bits_list)):
        for j in range(i + 1, len(bits_list)):
            a, b = bits_list[i], bits_list[j]
            ks_stat, ks_p = ks_2samp(a, b)
            perm_p = permutation_test_mean_diff(a, b)
            pairwise.append({
                "run_a": results[i]["path"],
                "run_b": results[j]["path"],
                "ks_statistic": float(ks_stat),
                "ks_pvalue": float(ks_p),
                "permutation_pvalue": perm_p,
            })

    return {
        "runs": results,
        "pairwise": pairwise,
    }


def print_summary(report: dict[str, Any]) -> None:
    """Print console summary."""
    print("\n=== QRNG Run Comparison ===\n")
    for r in report["runs"]:
        print(f"  {r['path']}: N={r['n']}, P(1)={r['p1']:.6f}, H={r['entropy']:.6f}")
    print("\n  Pairwise:")
    for p in report["pairwise"]:
        print(f"    {p['run_a']} vs {p['run_b']}: KS p={p['ks_pvalue']:.4g}, perm p={p['permutation_pvalue']:.4g}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare multiple QRNG runs")
    parser.add_argument("csv", type=str, nargs="+", help="Paths to QRNG CSVs")
    parser.add_argument("--out", type=str, default="", help="Output directory for report JSON")
    args = parser.parse_args()

    paths = [Path(p) for p in args.csv]
    for p in paths:
        if not p.exists():
            print(f"ERROR: File not found: {p}", file=sys.stderr)
            sys.exit(1)

    if len(paths) < 2:
        print("ERROR: Need at least 2 CSV files to compare", file=sys.stderr)
        sys.exit(1)

    report = compare_runs(paths)
    print_summary(report)

    out_dir = Path(args.out) if args.out else paths[0].parent
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "qrng_compare_report.json"
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nReport saved to {out_path}")


if __name__ == "__main__":
    main()
