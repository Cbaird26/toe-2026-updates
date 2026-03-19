#!/usr/bin/env python3
"""
H1 pilot — primary analysis on collect.py HDF5 (lsb_v1 extraction).

Bit order matches collect.py: for word index i and k in 0..31,
  X_{32*i + k} = (raw_u32[i] >> k) & 1.

Computes burn-in exclusion, train/holdout split, p_hat, delta, SE, Wilson CI, z.
Optional permutation stress (loads primary bits into RAM — capped).
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

try:
    import h5py
    import numpy as np
except ImportError as e:
    print("pip install numpy h5py", file=sys.stderr)
    raise SystemExit(1) from e

from stats_core import analyze_raw_u32, permutation_train_delta_pvalue


def main() -> None:
    p = argparse.ArgumentParser(description="H1 QRNG pilot — analyze HDF5 from collect.py")
    p.add_argument("h5_path")
    p.add_argument("--burnin-bits", type=int, default=0)
    p.add_argument("--holdout-fraction", type=float, default=0.2)
    p.add_argument("--max-bits", type=int, default=0, help="Cap usable bits from file start (0 = all)")
    p.add_argument("--permutations", type=int, default=0, help="MC permutation count (0=off)")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--verify-sha256", action="store_true", help="Rehash raw_u32 and compare")
    args = p.parse_args()

    with h5py.File(args.h5_path, "r") as f:
        meta = f["metadata"]
        rule = meta.attrs.get("extraction_rule_id", b"")
        if isinstance(rule, bytes):
            rule = rule.decode()
        if rule != "lsb_v1":
            print(f"Warning: extraction_rule_id={rule!r} — this script implements lsb_v1 only.", file=sys.stderr)

        raw = f["raw_u32"][:]
        stored_hash = meta.attrs.get("stream_sha256_hex", b"")
        if isinstance(stored_hash, bytes):
            stored_hash = stored_hash.decode()

    if args.verify_sha256:
        h = hashlib.sha256()
        h.update(raw.astype("<u4").tobytes())
        calc = h.hexdigest()
        if stored_hash and calc != stored_hash:
            raise SystemExit(f"SHA256 mismatch: file={stored_hash} recomputed={calc}")
        print("stream_sha256: OK")

    try:
        pa = analyze_raw_u32(
            raw,
            burnin_bits=args.burnin_bits,
            holdout_fraction=args.holdout_fraction,
            max_bits=args.max_bits,
        )
    except ValueError as e:
        raise SystemExit(str(e)) from e

    def report(label: str, seg: dict) -> None:
        print(
            f"{label}: n={seg['n']} ones={seg['ones']} p_hat={seg['p_hat']:.10f} "
            f"delta={seg['delta_hat']:+.3e} SE={seg['se']:.3e} z={seg['z']:+.3f}"
        )
        print(f"  Wilson 95%: [{seg['wilson_lo']:.6f}, {seg['wilson_hi']:.6f}]")

    print(f"File: {args.h5_path}")
    print(
        f"Bits in file: {pa.n_file_bits}  used: {pa.n_used_bits}  burnin={pa.burnin_bits}  primary={pa.n_primary}"
    )
    print(f"Split: train={pa.n_train}  holdout={pa.n_hold}  (holdout_fraction={pa.holdout_fraction})")
    report("TRAIN", pa.train)
    report("HOLD ", pa.hold)

    if args.permutations > 0:
        perm = permutation_train_delta_pvalue(
            raw,
            pa,
            n_permutations=args.permutations,
            seed=args.seed,
        )
        if perm is None:
            raise SystemExit(
                "Permutations skipped (n_primary too large). Use --max-bits or reduce data."
            )
        obs, p_two = perm
        print(
            f"Permutation |delta_train| >= |obs|: p~={p_two:.4f} (n={args.permutations}) obs_delta={obs:+.3e}"
        )


if __name__ == "__main__":
    main()
