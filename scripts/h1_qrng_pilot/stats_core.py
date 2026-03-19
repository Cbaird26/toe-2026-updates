"""
Shared H1 primary statistics (train/hold split, Wilson, z, optional permutation).
Used by analyze.py CLI and placebo_batch.py.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import numpy as np


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


def segment_metrics(n: int, successes: int) -> dict[str, float | int]:
    ph = successes / n
    delta = ph - 0.5
    se = math.sqrt(ph * (1 - ph) / n) if n else float("nan")
    z = delta / math.sqrt(0.25 / n) if n else float("nan")
    lo, hi = wilson_interval(successes, n)
    return {
        "n": n,
        "ones": successes,
        "p_hat": ph,
        "delta_hat": delta,
        "se": se,
        "z": z,
        "wilson_lo": lo,
        "wilson_hi": hi,
    }


@dataclass
class PrimaryAnalysis:
    n_file_bits: int
    n_used_bits: int
    burnin_bits: int
    n_primary: int
    n_train: int
    n_hold: int
    holdout_fraction: float
    train: dict[str, float | int]
    hold: dict[str, float | int]
    p_start: int
    train_end: int
    hold_end: int


def analyze_raw_u32(
    raw: np.ndarray,
    *,
    burnin_bits: int,
    holdout_fraction: float,
    max_bits: int = 0,
) -> PrimaryAnalysis:
    n_file = total_bits_available(raw)
    n_all = n_file if max_bits <= 0 else min(n_file, max_bits)
    if n_all < burnin_bits + 2:
        raise ValueError("Not enough bits after max_bits / burn-in")

    p_start = burnin_bits
    n_primary = n_all - p_start
    n_hold = int(math.floor(n_primary * holdout_fraction))
    n_train = n_primary - n_hold
    if n_train < 1 or n_hold < 1:
        raise ValueError("train or holdout empty")

    train_end = p_start + n_train
    hold_end = train_end + n_hold
    sum_train, sum_hold = train_holdout_sums(
        raw, p_start=p_start, train_end=train_end, hold_end=hold_end
    )
    return PrimaryAnalysis(
        n_file_bits=n_file,
        n_used_bits=n_all,
        burnin_bits=burnin_bits,
        n_primary=n_primary,
        n_train=n_train,
        n_hold=n_hold,
        holdout_fraction=holdout_fraction,
        train=segment_metrics(n_train, sum_train),
        hold=segment_metrics(n_hold, sum_hold),
        p_start=p_start,
        train_end=train_end,
        hold_end=hold_end,
    )


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


def read_primary_bits(raw: np.ndarray, p_start: int, n_primary: int) -> np.ndarray:
    idx = 0
    for wi, word in enumerate(raw):
        v = int(word) & 0xFFFFFFFF
        for k in range(32):
            if idx == p_start:
                return _read_n_bits_from(raw, wi, k, n_primary)
            idx += 1
    return np.zeros(0, dtype=np.uint8)


def permutation_train_delta_pvalue(
    raw: np.ndarray,
    pa: PrimaryAnalysis,
    *,
    n_permutations: int,
    seed: int,
    max_primary_bits_for_perm: int = 5_000_000,
) -> tuple[float, float] | None:
    """Return (obs_delta_train, two-sided MC p-value) or None if skipped."""
    if n_permutations <= 0:
        return None
    if pa.n_primary > max_primary_bits_for_perm:
        return None
    bits = read_primary_bits(raw, pa.p_start, pa.n_primary)
    rng = np.random.default_rng(seed)
    n_train = pa.n_train
    obs = float(np.mean(bits[:n_train]) - 0.5)
    stats = np.empty(n_permutations, dtype=np.float64)
    for i in range(n_permutations):
        perm = rng.permutation(bits)
        stats[i] = float(np.mean(perm[:n_train]) - 0.5)
    p_two = float(np.mean(np.abs(stats) >= abs(obs)))
    return obs, p_two


def primary_analysis_to_flat_dict(pa: PrimaryAnalysis) -> dict[str, Any]:
    """Row-friendly keys for CSV."""
    t, h = pa.train, pa.hold
    return {
        "n_file_bits": pa.n_file_bits,
        "n_used_bits": pa.n_used_bits,
        "burnin_bits": pa.burnin_bits,
        "n_primary": pa.n_primary,
        "n_train": pa.n_train,
        "n_hold": pa.n_hold,
        "holdout_fraction": pa.holdout_fraction,
        "train_ones": t["ones"],
        "train_p_hat": t["p_hat"],
        "train_delta_hat": t["delta_hat"],
        "train_se": t["se"],
        "train_z": t["z"],
        "train_wilson_lo": t["wilson_lo"],
        "train_wilson_hi": t["wilson_hi"],
        "hold_ones": h["ones"],
        "hold_p_hat": h["p_hat"],
        "hold_delta_hat": h["delta_hat"],
        "hold_se": h["se"],
        "hold_z": h["z"],
        "hold_wilson_lo": h["wilson_lo"],
        "hold_wilson_hi": h["wilson_hi"],
    }
