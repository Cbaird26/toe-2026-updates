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
import math
import sys

try:
    import h5py
    import numpy as np
except ImportError as e:
    print("pip install numpy h5py", file=sys.stderr)
    raise SystemExit(1) from e


def wilson_interval(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = successes / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    half = (z / denom) * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    return (center - half, center + half)


def total_bits_available(raw: np.ndarray) -> int:
    return int(raw.size) * 32


def train_holdout_sums(
    raw: np.ndarray,
    *,
    p_start: int,
    train_end: int,
    hold_end: int,
) -> tuple[int, int]:
    """Single scan; sums ones in [p_start, train_end) and [train_end, hold_end)."""
    idx = 0
    s_tr = s_ho = 0
    for word in raw:
        v = int(word) & 0xFFFFFFFF
        for k in range(32):
            if idx >= hold_end:
                return s_tr, s_ho
            if idx >= p_start:
                bit = (v >> k) & 1
                if idx < train_end:
                    s_tr += bit
                else:
                    s_ho += bit
            idx += 1
    return s_tr, s_ho


def _read_n_bits_from(raw: np.ndarray, wi: int, k0: int, n_primary: int) -> np.ndarray:
    out = np.empty(n_primary, dtype=np.uint8)
    o = 0
    wi = int(wi)
    k = int(k0)
    while o < n_primary and wi < raw.size:
        v = int(raw[wi]) & 0xFFFFFFFF
        while k < 32 and o < n_primary:
            out[o] = (v >> k) & 1
            o += 1
            k += 1
        if k == 32:
            k = 0
            wi += 1
    return out


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

    n_file = total_bits_available(raw)
    n_all = n_file if args.max_bits <= 0 else min(n_file, args.max_bits)

    if n_all < args.burnin_bits + 2:
        raise SystemExit("Not enough bits after --max-bits / burn-in")

    p_start = args.burnin_bits
    n_primary = n_all - p_start
    n_hold = int(math.floor(n_primary * args.holdout_fraction))
    n_train = n_primary - n_hold
    if n_train < 1 or n_hold < 1:
        raise SystemExit("train or holdout empty; adjust --holdout-fraction or collect more bits")

    train_end = p_start + n_train
    hold_end = train_end + n_hold

    sum_train, sum_hold = train_holdout_sums(raw, p_start=p_start, train_end=train_end, hold_end=hold_end)

    def report(label: str, n: int, successes: int) -> None:
        ph = successes / n
        delta = ph - 0.5
        se = math.sqrt(ph * (1 - ph) / n) if n else float("nan")
        z = delta / math.sqrt(0.25 / n) if n else float("nan")
        lo, hi = wilson_interval(successes, n)
        print(f"{label}: n={n} ones={successes} p_hat={ph:.10f} delta={delta:+.3e} SE={se:.3e} z={z:+.3f}")
        print(f"  Wilson 95%: [{lo:.6f}, {hi:.6f}]")

    print(f"File: {args.h5_path}")
    print(f"Bits in file: {n_file}  used: {n_all}  burnin={args.burnin_bits}  primary={n_primary}")
    print(f"Split: train={n_train}  holdout={n_hold}  (holdout_fraction={args.holdout_fraction})")
    report("TRAIN", n_train, sum_train)
    report("HOLD ", n_hold, sum_hold)

    if args.permutations > 0:
        if n_primary > 5_000_000:
            raise SystemExit("Refusing permutations for n_primary > 5e6 (RAM). Subsample or use --max-bits.")
        bits = _read_n_bits_from_for_perm(raw, p_start, n_primary)
        rng = np.random.default_rng(args.seed)
        obs = float(np.mean(bits[:n_train]) - 0.5)
        stats = np.empty(args.permutations, dtype=np.float64)
        for i in range(args.permutations):
            perm = rng.permutation(bits)
            stats[i] = float(np.mean(perm[:n_train]) - 0.5)
        p_two = float(np.mean(np.abs(stats) >= abs(obs)))
        print(f"Permutation |delta_train| >= |obs|: p~={p_two:.4f} (n={args.permutations}) obs_delta={obs:+.3e}")


def _read_n_bits_from_for_perm(raw: np.ndarray, p_start: int, n_primary: int) -> np.ndarray:
    """Same bit ordering as train_holdout_sums."""
    idx = 0
    for wi, word in enumerate(raw):
        v = int(word) & 0xFFFFFFFF
        for k in range(32):
            if idx == p_start:
                return _read_n_bits_from(raw, wi, k, n_primary)
            idx += 1
    return np.zeros(0, dtype=np.uint8)


if __name__ == "__main__":
    main()
