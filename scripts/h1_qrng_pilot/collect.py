#!/usr/bin/env python3
"""
H1 pilot — append raw uint32 stream to HDF5 with SHA-256 audit trail.

Modes:
  urandom  OS cryptographic random (pipeline / harness; not a physics claim)
  placebo  NumPy PCG64 (numpy.random.Generator) — known null for pipeline calibration
  anu      ANU Quantum Numbers JSON API (requires ANU_API_KEY env var)

Extraction rule id: lsb_v1 — bit order is little-endian within each uint32:
  global bit index t = 32*i + k uses X_t = (raw_u32[i] >> k) & 1, k = 0..31.

Preregistration: docs/H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import socket
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Literal

SCHEMA_VERSION = "h1_qrng_pilot/1"

try:
    import h5py
    import numpy as np
except ImportError as e:
    print("pip install numpy h5py", file=sys.stderr)
    raise SystemExit(1) from e


def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def fetch_anu_uint16(length: int, api_key: str, timeout: float = 30.0) -> np.ndarray:
    """
    ANU Quantum Numbers JSON API (uint16 array).
    https://quantumnumbers.anu.edu.au/documentation
    """
    if length < 1 or length > 1024:
        raise ValueError("length must be in [1, 1024] for this helper")
    base = "https://api.quantumnumbers.anu.edu.au/"
    qs = urllib.parse.urlencode({"length": length, "type": "uint16", "size": 1})
    url = f"{base}?{qs}"
    req = urllib.request.Request(
        url,
        headers={"x-api-key": api_key},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    if not payload.get("success"):
        raise RuntimeError(payload.get("message", payload))
    data = payload.get("data")
    if not isinstance(data, list):
        raise RuntimeError(f"unexpected ANU payload: {payload!r}")
    arr = np.asarray(data, dtype=np.uint16)
    if arr.size != length:
        raise RuntimeError(f"ANU length mismatch: wanted {length}, got {arr.size}")
    return arr


def uint16_to_uint32_lsb_blocks(u16: np.ndarray) -> np.ndarray:
    """Pack pairs of uint16 into uint32 (little-endian pair) for raw_u32 storage."""
    if u16.size % 2 != 0:
        u16 = u16[:-1]
    if u16.size == 0:
        return np.zeros(0, dtype=np.uint32)
    a = u16[0::2].astype(np.uint32)
    b = u16[1::2].astype(np.uint32)
    return (b << 16) | a


def urandom_uint32_chunk(n: int) -> np.ndarray:
    """n uint32s from OS CSPRNG."""
    nbytes = n * 4
    blob = os.urandom(nbytes)
    return np.frombuffer(blob, dtype=np.uint32, count=n)


def placebo_uint32_chunk(n: int, rng: np.random.Generator) -> np.ndarray:
    """n uint32s from fixed-seed NumPy Generator (PCG64 by default)."""
    # high is exclusive; use Python int 2**32 (np.uint32(2**32) wraps — do not use)
    return rng.integers(0, 2**32, size=n, dtype=np.uint32)


def open_h5_out(path: str) -> h5py.File:
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    return h5py.File(path, "w")


def write_metadata(
    f: h5py.File,
    *,
    mode: str,
    target_bits: int,
    chunk_u32: int,
    burnin_bits: int,
    holdout_fraction: float,
    extraction_rule_id: str,
    placebo_seed: int | None = None,
) -> None:
    meta = f.create_group("metadata")
    meta.attrs["schema_version"] = SCHEMA_VERSION
    meta.attrs["extraction_rule_id"] = extraction_rule_id
    meta.attrs["collection_mode"] = mode
    meta.attrs["target_bits"] = int(target_bits)
    meta.attrs["chunk_uint32"] = int(chunk_u32)
    meta.attrs["burnin_bits_prereg"] = int(burnin_bits)
    meta.attrs["holdout_fraction_prereg"] = float(holdout_fraction)
    meta.attrs["started_utc"] = _now_utc_iso()
    meta.attrs["hostname"] = socket.gethostname()
    meta.attrs["python_version"] = sys.version.split()[0]
    if mode == "placebo" and placebo_seed is not None:
        meta.attrs["placebo_seed"] = int(placebo_seed)
        meta.attrs["placebo_rng"] = "numpy.random.Generator (default PCG64)"


def write_collection(
    f: h5py.File,
    *,
    mode: Literal["urandom", "anu", "placebo"],
    target_bits: int,
    chunk_u32: int,
    burnin_bits: int,
    holdout_fraction: float,
    extraction_rule_id: str,
    placebo_seed: int | None = None,
    anu_batch: int = 1024,
    sleep_anu: float = 0.05,
) -> dict[str, float | int | str]:
    """
    Write raw_u32 + chunk_timestamp_ns + metadata to an open HDF5 file (same layout for all modes).

    Returns summary dict with raw_u32_count, stream_sha256_hex, elapsed_wall_s.
    """
    if target_bits < 1:
        raise ValueError("target_bits must be >= 1")
    if not (0.0 <= holdout_fraction < 1.0):
        raise ValueError("holdout_fraction must be in [0, 1)")
    if mode == "anu" and not os.environ.get("ANU_API_KEY"):
        raise ValueError("ANU mode requires ANU_API_KEY in the environment")
    if mode == "placebo" and placebo_seed is None:
        raise ValueError("placebo mode requires placebo_seed")

    bits_per_u32 = 32
    n_u32_needed = (target_bits + bits_per_u32 - 1) // bits_per_u32

    h = hashlib.sha256()
    written_u32 = 0
    t0 = time.time_ns()

    write_metadata(
        f,
        mode=mode,
        target_bits=target_bits,
        chunk_u32=chunk_u32,
        burnin_bits=burnin_bits,
        holdout_fraction=holdout_fraction,
        extraction_rule_id=extraction_rule_id,
        placebo_seed=placebo_seed,
    )
    dset = f.create_dataset(
        "raw_u32",
        shape=(0,),
        maxshape=(None,),
        dtype="u4",
        chunks=(chunk_u32,),
        compression="gzip",
        compression_opts=1,
    )
    ts = f.create_dataset(
        "chunk_timestamp_ns",
        shape=(0,),
        maxshape=(None,),
        dtype="i8",
        chunks=(min(1024, max(1, n_u32_needed // chunk_u32)),),
    )

    def append_block(block: np.ndarray) -> None:
        nonlocal written_u32
        if block.size == 0:
            return
        n = dset.shape[0]
        dset.resize((n + block.size,))
        dset[n : n + block.size] = block
        h.update(block.astype("<u4").tobytes())
        written_u32 += int(block.size)
        m = ts.shape[0]
        ts.resize((m + 1,))
        ts[m] = time.time_ns()

    if mode == "urandom":
        while written_u32 < n_u32_needed:
            take = min(chunk_u32, n_u32_needed - written_u32)
            append_block(urandom_uint32_chunk(take))
    elif mode == "placebo":
        rng = np.random.default_rng(int(placebo_seed))
        while written_u32 < n_u32_needed:
            take = min(chunk_u32, n_u32_needed - written_u32)
            append_block(placebo_uint32_chunk(take, rng))
    else:
        api_key = os.environ["ANU_API_KEY"]
        batch = max(1, min(1024, anu_batch))
        while written_u32 < n_u32_needed:
            need = n_u32_needed - written_u32
            u16 = fetch_anu_uint16(batch, api_key)
            blk = uint16_to_uint32_lsb_blocks(u16)
            if blk.size > need:
                blk = blk[:need]
            append_block(blk)
            time.sleep(sleep_anu)

    meta = f["metadata"]
    meta.attrs["finished_utc"] = _now_utc_iso()
    elapsed = (time.time_ns() - t0) * 1e-9
    meta.attrs["elapsed_wall_s"] = elapsed
    meta.attrs["raw_u32_count"] = written_u32
    meta.attrs["stream_sha256_hex"] = h.hexdigest()

    return {
        "raw_u32_count": written_u32,
        "stream_sha256_hex": h.hexdigest(),
        "elapsed_wall_s": elapsed,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="H1 QRNG pilot — HDF5 collector with SHA-256 audit")
    p.add_argument("--mode", choices=("urandom", "anu", "placebo"), required=True)
    p.add_argument("--out", required=True, help="Output .h5 path")
    p.add_argument("--target-bits", type=int, default=1_000_000)
    p.add_argument("--chunk-u32", type=int, default=65_536, help="HDF5 chunk size (uint32 rows)")
    p.add_argument("--burnin-bits", type=int, default=0, help="Recorded for prereg; analysis applies")
    p.add_argument("--holdout-fraction", type=float, default=0.2)
    p.add_argument(
        "--extraction-rule-id",
        default="lsb_v1",
        help="Must match analyze.py (default: LSB of each uint32)",
    )
    p.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Required for --mode placebo (int seed for numpy.random.Generator)",
    )
    p.add_argument("--anu-batch", type=int, default=1024, help="ANU uint16 count per HTTP call (max 1024)")
    p.add_argument("--sleep-anu", type=float, default=0.05, help="Seconds between ANU calls (be polite)")
    args = p.parse_args()

    if args.mode == "placebo" and args.seed is None:
        raise SystemExit("--mode placebo requires --seed (fixed integer for reproducible null stream)")

    with open_h5_out(args.out) as f:
        summary = write_collection(
            f,
            mode=args.mode,
            target_bits=args.target_bits,
            chunk_u32=args.chunk_u32,
            burnin_bits=args.burnin_bits,
            holdout_fraction=args.holdout_fraction,
            extraction_rule_id=args.extraction_rule_id,
            placebo_seed=args.seed,
            anu_batch=args.anu_batch,
            sleep_anu=args.sleep_anu,
        )

    print(f"Wrote {args.out}")
    print(f"  raw_u32 rows: {summary['raw_u32_count']}")
    print(f"  stream_sha256: {summary['stream_sha256_hex']}")


if __name__ == "__main__":
    main()
