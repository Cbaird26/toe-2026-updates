#!/usr/bin/env python3
"""
H1 placebo batch — many fixed-seed replicates through the same HDF5 + analysis path.

Uses in-memory HDF5 (driver='core', backing_store=False) so disk I/O does not
dominate; stream layout and metadata match collect.py disk files.

Emits:
  - Per-replicate CSV (train/hold metrics, optional permutation p-value)
  - Summary JSON with empirical |z| threshold hit rates (false-positive calibration)

See README.md for usage.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from typing import Any

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

try:
    import h5py
    import numpy as np
except ImportError as e:
    print("pip install numpy h5py", file=sys.stderr)
    raise SystemExit(1) from e

from collect import write_collection
from stats_core import (
    analyze_raw_u32,
    permutation_train_delta_pvalue,
    primary_analysis_to_flat_dict,
)


def parse_z_thresholds(s: str) -> list[float]:
    out: list[float] = []
    for part in s.replace(" ", "").split(","):
        if not part:
            continue
        out.append(float(part))
    return sorted(set(out))


def main() -> None:
    p = argparse.ArgumentParser(description="H1 placebo batch — HDF5 schema + analysis null calibration")
    p.add_argument("--replicates", type=int, required=True)
    p.add_argument("--base-seed", type=int, default=0, help="placebo_seed for replicate 0")
    p.add_argument(
        "--seed-stride",
        type=int,
        default=1_000_003,
        help="placebo_seed for replicate r is base_seed + r * stride (large primes reduce overlap)",
    )
    p.add_argument("--target-bits", type=int, default=200_000)
    p.add_argument("--chunk-u32", type=int, default=65_536)
    p.add_argument("--burnin-bits", type=int, default=0)
    p.add_argument("--holdout-fraction", type=float, default=0.2)
    p.add_argument("--extraction-rule-id", default="lsb_v1")
    p.add_argument("--permutations", type=int, default=0, help="MC permutations per replicate (0=skip)")
    p.add_argument(
        "--perm-seed",
        type=int,
        default=0,
        help="numpy RNG seed for permutations; effective seed is perm_seed + replicate index",
    )
    p.add_argument(
        "--z-thresholds",
        type=str,
        default="2,3,5",
        help="Comma-separated |z| thresholds for empirical hit-rate summary (train and hold)",
    )
    p.add_argument(
        "--perm-alpha",
        type=float,
        default=0.05,
        help="Report fraction of replicates with perm_p_two_sided < alpha (if permutations>0)",
    )
    p.add_argument("--out-csv", required=True)
    p.add_argument("--out-summary-json", required=True)
    args = p.parse_args()

    if args.replicates < 1:
        raise SystemExit("--replicates must be >= 1")
    z_list = parse_z_thresholds(args.z_thresholds)
    if not z_list:
        raise SystemExit("need at least one --z-thresholds value")

    os.makedirs(os.path.dirname(os.path.abspath(args.out_csv)) or ".", exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(args.out_summary_json)) or ".", exist_ok=True)

    rows: list[dict[str, Any]] = []
    train_z_list: list[float] = []
    hold_z_list: list[float] = []
    perm_p_list: list[float] = []

    for r in range(args.replicates):
        seed_r = int(args.base_seed + r * args.seed_stride)
        f = h5py.File("in_memory", "w", driver="core", backing_store=False)
        try:
            write_collection(
                f,
                mode="placebo",
                target_bits=args.target_bits,
                chunk_u32=args.chunk_u32,
                burnin_bits=args.burnin_bits,
                holdout_fraction=args.holdout_fraction,
                extraction_rule_id=args.extraction_rule_id,
                placebo_seed=seed_r,
            )
            raw = f["raw_u32"][:]
            meta = f["metadata"]
            sha = meta.attrs.get("stream_sha256_hex", b"")
            if isinstance(sha, bytes):
                sha = sha.decode()
        finally:
            f.close()

        pa = analyze_raw_u32(
            raw,
            burnin_bits=args.burnin_bits,
            holdout_fraction=args.holdout_fraction,
        )
        flat = primary_analysis_to_flat_dict(pa)
        row: dict[str, Any] = {
            "replicate": r,
            "placebo_seed": seed_r,
            "stream_sha256_hex": sha,
        }
        row.update(flat)

        if args.permutations > 0:
            perm = permutation_train_delta_pvalue(
                raw,
                pa,
                n_permutations=args.permutations,
                seed=int(args.perm_seed + r),
            )
            if perm is None:
                row["perm_obs_delta_train"] = ""
                row["perm_p_two_sided"] = ""
                row["perm_skipped"] = True
            else:
                obs_d, p_two = perm
                row["perm_obs_delta_train"] = obs_d
                row["perm_p_two_sided"] = p_two
                row["perm_skipped"] = False
                perm_p_list.append(p_two)
        else:
            row["perm_obs_delta_train"] = ""
            row["perm_p_two_sided"] = ""
            row["perm_skipped"] = ""

        train_z_list.append(float(pa.train["z"]))
        hold_z_list.append(float(pa.hold["z"]))
        rows.append(row)

    fieldnames = list(rows[0].keys()) if rows else []
    with open(args.out_csv, "w", newline="") as fc:
        w = csv.DictWriter(fc, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    def hit_rate(values: list[float], thresh: float) -> float:
        if not values:
            return float("nan")
        return float(sum(1 for v in values if abs(v) >= thresh) / len(values))

    def nominal_two_sided_abs_z_exceed(t: float) -> float:
        """Asymptotic N(0,1): P(|Z| >= t) = erfc(t / sqrt(2)). Heuristic only for finite n."""
        return float(math.erfc(t / math.sqrt(2.0)))

    summary: dict[str, Any] = {
        "schema": "h1_placebo_batch/1",
        "numpy_version": np.__version__,
        "h5py_version": h5py.__version__,
        "replicates": args.replicates,
        "base_seed": args.base_seed,
        "seed_stride": args.seed_stride,
        "target_bits": args.target_bits,
        "chunk_u32": args.chunk_u32,
        "burnin_bits": args.burnin_bits,
        "holdout_fraction": args.holdout_fraction,
        "extraction_rule_id": args.extraction_rule_id,
        "permutations_per_replicate": args.permutations,
        "perm_seed_base": args.perm_seed,
        "z_thresholds": z_list,
        "empirical_hit_rate_abs_z_train": {str(t): hit_rate(train_z_list, t) for t in z_list},
        "empirical_hit_rate_abs_z_hold": {str(t): hit_rate(hold_z_list, t) for t in z_list},
        "nominal_gaussian_two_sided_abs_z_exceedance": {
            str(t): nominal_two_sided_abs_z_exceed(t) for t in z_list
        },
    }
    if perm_p_list:
        summary["permutation_fraction_p_below_alpha"] = float(
            sum(1 for x in perm_p_list if x < args.perm_alpha) / len(perm_p_list)
        )
        summary["perm_alpha"] = args.perm_alpha
        summary["permutation_replicates_counted"] = len(perm_p_list)

    with open(args.out_summary_json, "w") as fo:
        json.dump(summary, fo, indent=2)
        fo.write("\n")

    print(f"Wrote {args.out_csv} ({args.replicates} rows)")
    print(f"Wrote {args.out_summary_json}")
    for t in z_list:
        print(
            f"  P(|z_train| >= {t}) ~ {summary['empirical_hit_rate_abs_z_train'][str(t)]:.4f}  "
            f"P(|z_hold| >= {t}) ~ {summary['empirical_hit_rate_abs_z_hold'][str(t)]:.4f}"
        )
    if perm_p_list:
        print(
            f"  Frac perm_p < {args.perm_alpha}: {summary['permutation_fraction_p_below_alpha']:.4f} "
            f"(n={summary['permutation_replicates_counted']})"
        )


if __name__ == "__main__":
    main()
