#!/usr/bin/env python3
"""
ANU QRNG Condition-Based Experiment — MQGT-SCF RNG Test 002

Collects quantum random bits in control/intervention blocks, with full audit trail.
Runs statistical analysis: binomial, chi-square, KS, difference in proportions,
permutation test, Benjamini-Hochberg correction. Writes per-block metadata (p_hat,
entropy, runs_z) for diagnostics.

Usage:
  # Pilot: 2 blocks (control + intervention), ~20k bits
  python scripts/anu_qrng_experiment.py --pilot --out artifacts/

  # Full: 20 blocks × 100k bits (2M total, ~$1.25)
  python scripts/anu_qrng_experiment.py --out artifacts/

  # Intervention run (specify type)
  python scripts/anu_qrng_experiment.py --intervention meditation --randomize-blocks --seed 42 --out artifacts/

  # Analyze existing CSV (raw-bit mode, slow for large files)
  python scripts/anu_qrng_experiment.py --analyze artifacts/qrng_experiment_*.csv

  # Block-level analysis only (fast, recommended for routine runs)
  python scripts/anu_qrng_experiment.py --analyze-blocks artifacts/qrng_experiment_*_blocks.json

Requires: scipy for raw-bit analysis. Block analysis uses stdlib only.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Import from sibling module
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))
try:
    from anu_qrng_collect import collect_bits, resolve_api_key, preflight_check
except ImportError:
    collect_bits = None
    resolve_api_key = None
    preflight_check = None


def _block_stats(bits: list[int]) -> dict[str, Any]:
    """Compute p_hat, entropy, runs_z, ones, zeros for a block of bits."""
    n = len(bits)
    ones = sum(bits)
    zeros = n - ones
    p_hat = ones / n if n else 0.5
    p0, p1 = 1 - p_hat, p_hat
    entropy = 0.0
    if p0 > 0 and p1 > 0:
        entropy = -(p0 * math.log2(p0) + p1 * math.log2(p1))
    runs = 1 + sum(1 for i in range(n - 1) if bits[i] != bits[i + 1])
    n0 = zeros
    expected = (2 * ones * n0) / n + 1 if n else 1
    var = (2 * ones * n0 * (2 * ones * n0 - n)) / (n * n * (n - 1)) if n > 1 else 0
    runs_z = (runs - expected) / math.sqrt(var) if var > 0 else 0.0
    return {"p_hat": p_hat, "entropy": entropy, "runs_z": runs_z, "ones": ones, "zeros": zeros}


def run_collection(
    n_blocks: int,
    block_size: int,
    randomize: bool,
    seed: int | None,
    api_key: str | None,
    out_dir: Path,
    dry_run: bool,
    intervention: str | None = None,
    no_fallback: bool = False,
) -> tuple[Path, list[dict[str, Any]]]:
    """Collect bits in blocks with condition labels. Returns (csv_path, block_metadata)."""
    session_id = str(uuid.uuid4())
    conditions = ["control", "intervention"] * ((n_blocks + 1) // 2)
    block_sequence = conditions[:n_blocks]
    if randomize:
        rng = random.Random(seed)
        rng.shuffle(block_sequence)

    stamp = time.strftime("%Y%m%d_%H%M%S")
    csv_path = out_dir / f"qrng_experiment_{stamp}_{session_id[:8]}.csv"

    out_dir.mkdir(parents=True, exist_ok=True)
    block_metadata: list[dict[str, Any]] = []

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["session_id", "request_index", "timestamp_utc", "condition", "bit"],
        )
        writer.writeheader()

        for block_idx, condition in enumerate(block_sequence):
            start_time = datetime.now(timezone.utc).isoformat()
            if dry_run:
                rng = random.Random(seed or 20260314)
                bits = [rng.randint(0, 1) for _ in range(block_size)]
            else:
                bits = collect_bits(block_size, api_key, no_fallback=no_fallback)
            end_time = datetime.now(timezone.utc).isoformat()

            stats = _block_stats(bits)
            block_metadata.append({
                "block_index": block_idx,
                "condition": condition,
                "start_time": start_time,
                "end_time": end_time,
                "n_bits": len(bits),
                "ones": stats["ones"],
                "zeros": stats["zeros"],
                "p_hat": stats["p_hat"],
                "entropy": stats["entropy"],
                "runs_z": stats["runs_z"],
            })

            for b in bits:
                writer.writerow({
                    "session_id": session_id,
                    "request_index": block_idx,
                    "timestamp_utc": start_time,
                    "condition": condition,
                    "bit": b,
                })
            print(f"  Block {block_idx+1}/{n_blocks} ({condition}): {block_size} bits")

    return csv_path, block_metadata


def run_block_analysis(blocks: list[dict[str, Any]], n_perm: int = 10_000) -> dict[str, Any]:
    """Block-level permutation test. Fast; no raw bits needed."""
    control = [b["p_hat"] for b in blocks if b["condition"] == "control"]
    intervention = [b["p_hat"] for b in blocks if b["condition"] == "intervention"]
    if not control or not intervention:
        return {"error": "Need both control and intervention blocks"}

    c_mean = sum(control) / len(control)
    i_mean = sum(intervention) / len(intervention)
    obs_diff = i_mean - c_mean

    all_means = control + intervention
    rng = random.Random(42)
    count = 0
    for _ in range(n_perm):
        rng.shuffle(all_means)
        nc = len(control)
        perm_diff = sum(all_means[nc:]) / len(intervention) - sum(all_means[:nc]) / nc
        if abs(perm_diff) >= abs(obs_diff):
            count += 1
    p = (count + 1) / (n_perm + 1)

    return {
        "control_n": len(control),
        "intervention_n": len(intervention),
        "n_control_blocks": len(control),
        "n_intervention_blocks": len(intervention),
        "control_mean_p1": c_mean,
        "intervention_mean_p1": i_mean,
        "difference": obs_diff,
        "observed_statistic": obs_diff,
        "permutation_p": p,
        "n_permutations": n_perm,
        "block_condition_sequence": [b["condition"] for b in blocks],
    }


def load_experiment_csv(path: Path) -> list[dict[str, Any]]:
    """Load experiment CSV and return list of rows with typed values."""
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["request_index"] = int(row["request_index"])
            row["bit"] = int(row["bit"])
            rows.append(row)
    return rows


def run_analysis(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Run statistical analysis. Requires scipy."""
    try:
        from scipy.stats import binomtest, chisquare, ks_2samp
    except ImportError:
        raise RuntimeError("Analysis requires scipy. Run: pip install scipy")

    control = [r["bit"] for r in rows if r["condition"] == "control"]
    intervention = [r["bit"] for r in rows if r["condition"] == "intervention"]
    all_bits = [r["bit"] for r in rows]

    results: dict[str, Any] = {
        "n_total": len(all_bits),
        "n_control": len(control),
        "n_intervention": len(intervention),
    }

    if not control or not intervention:
        results["error"] = "Need both control and intervention blocks"
        return results

    # Binomial tests vs 0.5
    c_ones = sum(control)
    i_ones = sum(intervention)
    bt_control = binomtest(c_ones, len(control), 0.5)
    bt_intervention = binomtest(i_ones, len(intervention), 0.5)
    results["binomial_control"] = {"k": c_ones, "n": len(control), "pvalue": bt_control.pvalue}
    results["binomial_intervention"] = {"k": i_ones, "n": len(intervention), "pvalue": bt_intervention.pvalue}

    # Chi-square goodness of fit (overall)
    obs = [sum(all_bits), len(all_bits) - sum(all_bits)]
    exp = [len(all_bits) / 2, len(all_bits) / 2]
    chi2, chi2_p = chisquare(obs, exp)
    results["chisquare_overall"] = {"chi2": float(chi2), "pvalue": float(chi2_p)}

    # Difference in proportions
    p1 = c_ones / len(control)
    p2 = i_ones / len(intervention)
    diff = p2 - p1
    pooled = (c_ones + i_ones) / (len(control) + len(intervention))
    se = math.sqrt(pooled * (1 - pooled) * (1 / len(control) + 1 / len(intervention)))
    z = diff / se if se > 0 else float("nan")
    results["diff_proportions"] = {
        "control_p1": p1,
        "intervention_p1": p2,
        "difference": diff,
        "z_score": z,
    }

    # KS test
    ks_stat, ks_p = ks_2samp(control, intervention)
    results["ks_test"] = {"statistic": float(ks_stat), "pvalue": float(ks_p)}

    # Permutation test on mean difference
    n_perm = 1000
    rng = random.Random(42)
    obs_diff = p2 - p1
    combined = control + intervention
    count_extreme = 0
    for _ in range(n_perm):
        rng.shuffle(combined)
        a, b = combined[: len(control)], combined[len(control) :]
        perm_diff = sum(b) / len(b) - sum(a) / len(a)
        if abs(perm_diff) >= abs(obs_diff):
            count_extreme += 1
    perm_p = (count_extreme + 1) / (n_perm + 1)
    results["permutation_test"] = {"observed_diff": obs_diff, "n_perm": n_perm, "pvalue": perm_p}

    # Benjamini-Hochberg on p-values
    pvalues = [bt_control.pvalue, bt_intervention.pvalue, chi2_p, ks_p, perm_p]
    sorted_p = sorted(enumerate(pvalues), key=lambda x: x[1])
    m = len(pvalues)
    bh_reject = []
    for i, (idx, p) in enumerate(sorted_p):
        if p <= (i + 1) / m * 0.05:
            bh_reject.append(idx)
        else:
            break
    results["benjamini_hochberg"] = {"pvalues": pvalues, "rejected_at_005": bh_reject}

    return results


def print_analysis(results: dict[str, Any]) -> None:
    """Print analysis results to stdout."""
    if results.get("error"):
        print(f"Error: {results['error']}")
        return
    print("\n=== QRNG Experiment Analysis ===")
    print(f"  Total N:      {results['n_total']}")
    print(f"  Control N:    {results['n_control']}")
    print(f"  Intervention: {results['n_intervention']}")
    dp = results["diff_proportions"]
    print(f"\n  Control proportion of 1s:      {dp['control_p1']:.6f}")
    print(f"  Intervention proportion of 1s: {dp['intervention_p1']:.6f}")
    print(f"  Difference:                    {dp['difference']:+.6f}")
    print(f"  z-score (diff):                {dp['z_score']:.4f}")
    print(f"\n  Binomial (control) p:     {results['binomial_control']['pvalue']:.6g}")
    print(f"  Binomial (intervention) p: {results['binomial_intervention']['pvalue']:.6g}")
    print(f"  Chi-square (overall) p:    {results['chisquare_overall']['pvalue']:.6g}")
    print(f"  KS test p:                 {results['ks_test']['pvalue']:.6g}")
    print(f"  Permutation test p:        {results['permutation_test']['pvalue']:.6g}")
    print(f"\n  (Protocol recommends α=0.01 for primary; require ≥3 runs, same direction, to interpret)")


def print_block_analysis(summary: dict[str, Any]) -> None:
    """Print block-level analysis summary."""
    if summary.get("error"):
        print(f"Error: {summary['error']}")
        return
    print("\n=== QRNG Block-Level Analysis ===")
    print(f"  Run ID:       {summary.get('run_id', '—')}")
    print(f"  Intervention: {summary.get('intervention', '—')}")
    print(f"  Control blocks (n={summary['control_n']}):  mean P(1) = {summary['control_mean_p1']:.6f}")
    print(f"  Intervention blocks (n={summary['intervention_n']}): mean P(1) = {summary['intervention_mean_p1']:.6f}")
    print(f"  Difference (I - C):   {summary['difference']:+.6f}")
    print(f"  Permutation p ({summary['n_permutations']}): {summary['permutation_p']:.4g}")
    print(f"\n  (Protocol: α=0.01; require ≥3 runs, same direction)")


def main() -> None:
    parser = argparse.ArgumentParser(description="ANU QRNG condition-based experiment")
    parser.add_argument("--out", type=str, default="artifacts", help="Output directory")
    parser.add_argument("--blocks", type=int, default=20, help="Number of blocks")
    parser.add_argument("--block-size", type=int, default=100_000, help="Bits per block")
    parser.add_argument("--pilot", action="store_true", help="Pilot: 2 blocks (~20k bits)")
    parser.add_argument("--randomize-blocks", action="store_true", help="Randomize block order")
    parser.add_argument(
        "--intervention",
        type=str,
        choices=["meditation", "breathwork", "intention", "sham"],
        default=None,
        help="Intervention type for intervention blocks",
    )
    parser.add_argument("--seed", type=int, default=None, help="Random seed for block order")
    parser.add_argument("--analyze", type=str, default="", help="Analyze existing CSV (raw-bit mode, slow for large files)")
    parser.add_argument(
        "--analyze-blocks",
        type=str,
        nargs="+",
        default=[],
        metavar="FILE",
        help="Analyze blocks JSON (single or multiple). Multiple files: pooled permutation test.",
    )
    parser.add_argument("--api-key", type=str, default="", help="ANU API key (or env / artifacts/.anu_api_key)")
    parser.add_argument("--dry-run", action="store_true", help="Use local PRNG (not real QRNG)")
    parser.add_argument(
        "--confirmatory",
        action="store_true",
        help="Preflight + no legacy fallback. Abort on API failure. Required for formal runs.",
    )
    args = parser.parse_args()

    if args.analyze_blocks:
        paths = [Path(p) for p in args.analyze_blocks]
        for p in paths:
            if not p.exists():
                print(f"ERROR: File not found: {p}", file=sys.stderr)
                sys.exit(1)

        all_blocks: list[dict[str, Any]] = []
        per_run: list[dict[str, Any]] = []

        for path in paths:
            with open(path) as f:
                data = json.load(f)
            blocks = data.get("blocks", [])
            if not blocks:
                continue
            summary = run_block_analysis(blocks)
            if not summary.get("error"):
                summary["run_id"] = data.get("run_id", path.stem)
                summary["intervention"] = data.get("intervention")
                per_run.append(summary)
                all_blocks.extend(blocks)

        if len(paths) == 1 and per_run:
            summary = per_run[0]
            summary["analyzed_at"] = datetime.now(timezone.utc).isoformat()
            print_block_analysis(summary)
            out_path = paths[0].parent / f"{paths[0].stem.replace('_blocks', '')}_block_analysis.json"
            with open(out_path, "w") as f:
                json.dump(summary, f, indent=2)
            print(f"\nBlock analysis saved to {out_path}")
        elif len(paths) > 1 and all_blocks:
            print("\n=== Per-run summary ===")
            for s in per_run:
                print(f"  {s.get('run_id', '—')}: diff={s['difference']:+.6f}, p={s['permutation_p']:.4g}")
            pooled = run_block_analysis(all_blocks)
            pooled["runs_combined"] = len(paths)
            pooled["total_blocks"] = len(all_blocks)
            pooled["analyzed_at"] = datetime.now(timezone.utc).isoformat()
            print("\n=== Pooled analysis (all blocks) ===")
            print_block_analysis(pooled)
            out_path = paths[0].parent / "qrng_pooled_block_analysis.json"
            with open(out_path, "w") as f:
                json.dump(
                    {"per_run": per_run, "pooled": pooled, "source_files": [str(p) for p in paths]},
                    f,
                    indent=2,
                )
            print(f"\nPooled analysis saved to {out_path}")
        else:
            print("ERROR: No valid blocks found", file=sys.stderr)
            sys.exit(1)
        return

    if args.analyze:
        path = Path(args.analyze)
        if not path.exists():
            print(f"ERROR: File not found: {path}", file=sys.stderr)
            sys.exit(1)
        rows = load_experiment_csv(path)
        try:
            results = run_analysis(rows)
        except RuntimeError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)
        print_analysis(results)
        out_path = path.parent / f"{path.stem}_analysis.json"
        with open(out_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nAnalysis saved to {out_path}")
        return

    # Collection mode
    if collect_bits is None or resolve_api_key is None:
        print("ERROR: Cannot import anu_qrng_collect. Run from repo root.", file=sys.stderr)
        sys.exit(1)

    n_blocks = 2 if args.pilot else args.blocks
    block_size = args.block_size
    if args.pilot:
        block_size = min(block_size, 10_000)
        print(f"[QRNG Experiment] PILOT — 2 blocks of {block_size} bits (~{2*block_size} total)")

    try:
        api_key, key_path = resolve_api_key(args.api_key, args.out)
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    if args.confirmatory and not args.dry_run:
        if preflight_check is None:
            print("ERROR: Cannot import preflight_check from anu_qrng_collect.", file=sys.stderr)
            sys.exit(1)
        key_src = "CLI" if args.api_key else ("env" if os.environ.get("ANU_QRNG_API_KEY") else "file")
        if key_path:
            key_src = key_path.name
        try:
            preflight_check(api_key, key_src)
            print("  [Confirmatory] Preflight OK. No legacy fallback — abort on API failure.")
        except RuntimeError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)

    out_dir = Path(args.out)
    print(f"[QRNG Experiment] Collecting {n_blocks} blocks × {block_size} bits...")
    if args.intervention:
        print(f"  Intervention type: {args.intervention}")
    csv_path, block_metadata = run_collection(
        n_blocks=n_blocks,
        block_size=block_size,
        randomize=args.randomize_blocks,
        seed=args.seed,
        api_key=api_key,
        out_dir=out_dir,
        dry_run=args.dry_run,
        intervention=args.intervention,
        no_fallback=args.confirmatory,
    )
    print(f"Wrote {csv_path}")

    # Write block metadata with comparison summary
    block_summary = run_block_analysis(block_metadata)
    metadata = {
        "run_id": csv_path.stem,
        "intervention": args.intervention,
        "blocks": block_metadata,
        "block_comparison": {
            **block_summary,
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
        },
    }
    meta_path = csv_path.parent / f"{csv_path.stem}_blocks.json"
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"Wrote {meta_path}")

    if not block_summary.get("error"):
        print_block_analysis({**block_summary, "run_id": csv_path.stem, "intervention": args.intervention})

    # Run raw-bit analysis (optional; slow for large datasets — use --analyze-blocks for fast check)
    total_bits = sum(b.get("n_bits", b.get("bit_count", 0)) for b in block_metadata)
    if total_bits > 500_000:
        print(f"\n  (Skipping raw-bit analysis for {total_bits} bits — use --analyze-blocks on _blocks.json)")
    else:
        rows = load_experiment_csv(csv_path)
        try:
            results = run_analysis(rows)
            print_analysis(results)
            analysis_path = csv_path.parent / f"{csv_path.stem}_analysis.json"
            with open(analysis_path, "w") as f:
                json.dump(results, f, indent=2)
            print(f"\nAnalysis saved to {analysis_path}")
        except RuntimeError as e:
            print(f"Raw-bit analysis skipped: {e}")


if __name__ == "__main__":
    main()
