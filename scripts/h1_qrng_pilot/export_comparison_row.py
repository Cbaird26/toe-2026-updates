#!/usr/bin/env python3
"""
Emit one CSV line compatible with artifacts/h1_pilot/run_comparison_individual.csv
from a collect.py HDF5 file (lsb_v1).
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

import h5py
import numpy as np

from stats_core import analyze_raw_u32


def _csv_escape(s: str) -> str:
    if "," in s or '"' in s or "\n" in s:
        return '"' + s.replace('"', '""') + '"'
    return s


def _fmt_ph(x: float) -> str:
    s = f"{x:.16f}"
    return s.rstrip("0").rstrip(".") if "." in s else s


def _fmt_de(x: float) -> str:
    return f"{x:+.16e}"


def main() -> None:
    p = argparse.ArgumentParser(description="Export one H1 comparison CSV row from .h5")
    p.add_argument("--run-id", required=True)
    p.add_argument("--source", required=True, choices=("anu", "urandom", "placebo"))
    p.add_argument("--h5", required=True)
    p.add_argument("--burnin-bits", type=int, default=0)
    p.add_argument("--holdout-fraction", type=float, default=0.2)
    p.add_argument("--notes", default="", help="Notes column (optional)")
    args = p.parse_args()

    with h5py.File(args.h5, "r") as f:
        meta = f["metadata"]
        raw = f["raw_u32"][:]
        stored = meta.attrs.get("stream_sha256_hex", b"")
        if isinstance(stored, bytes):
            stored = stored.decode()
        h = hashlib.sha256()
        h.update(raw.astype("<u4").tobytes())
        sha_ok = bool(stored) and h.hexdigest() == stored

    pa = analyze_raw_u32(
        raw,
        burnin_bits=args.burnin_bits,
        holdout_fraction=args.holdout_fraction,
    )
    bits_total = pa.n_used_bits
    tr, ho = pa.train, pa.hold

    row = [
        args.run_id,
        args.source,
        str(bits_total),
        str(args.burnin_bits),
        str(args.holdout_fraction),
        _fmt_ph(float(tr["p_hat"])),
        _fmt_de(float(tr["delta_hat"])),
        str(tr["z"]),
        _fmt_ph(float(ho["p_hat"])),
        _fmt_de(float(ho["delta_hat"])),
        str(ho["z"]),
        str(ho["wilson_lo"]),
        str(ho["wilson_hi"]),
        "",
        str(sha_ok),
        _csv_escape(args.notes) if args.notes else "",
    ]
    print(",".join(row))


if __name__ == "__main__":
    main()
