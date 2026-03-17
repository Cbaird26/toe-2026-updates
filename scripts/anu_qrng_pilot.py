#!/usr/bin/env python3
"""
ANU QRNG pilot: 10k bits to validate API, auth, and pipeline.
Usage: python scripts/anu_qrng_pilot.py
       ANU_QRNG_API_KEY=yourkey python scripts/anu_qrng_pilot.py  # new API (optional)
Output: artifacts/anu_qrng_pilot_<timestamp>_bits.csv, *_summary.json
Cost: ~2 requests ≈ $0.01 (if paid API) or free (legacy).
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("pip install requests", file=sys.stderr)
    sys.exit(1)

PILOT_BITS = 10_000
BITS_PER_REQUEST = 8192  # 1024 uint8 * 8
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "artifacts"
LEGACY_URL = "https://qrng.anu.edu.au/API/jsonI.php"
NEW_API_BASE = "https://api.quantumnumbers.anu.edu.au"


def get_api_key() -> str | None:
    key = os.environ.get("ANU_QRNG_API_KEY")
    if key:
        return key.strip()
    for p in [OUTPUT_DIR / ".anu_api_key", Path.cwd() / "artifacts" / ".anu_api_key", Path.cwd() / ".anu_api_key"]:
        if p.exists():
            return p.read_text().strip()
    return None


def fetch_uint8_legacy(length: int = 1024) -> list[int]:
    r = requests.get(LEGACY_URL, params={"length": length, "type": "uint8"}, timeout=15)
    r.raise_for_status()
    data = r.json()
    if "data" not in data:
        raise RuntimeError("Legacy API response missing 'data'")
    return data["data"]


def fetch_uint8_new(length: int, api_key: str) -> list[int]:
    # New AWS-hosted API
    r = requests.get(
        NEW_API_BASE,
        params={"length": length, "type": "uint8"},
        headers={"x-api-key": api_key},
        timeout=15,
    )
    r.raise_for_status()
    data = r.json()
    if "data" not in data:
        raise RuntimeError("New API response missing 'data'")
    return data["data"]


def uint8_to_bits(arr: list[int]) -> list[int]:
    bits = []
    for byte in arr:
        for i in range(8):
            bits.append((byte >> (7 - i)) & 1)
    return bits


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    api_key = get_api_key()
    use_new = bool(api_key)

    print("ANU QRNG pilot: 10,000 bits")
    print(f"  API: {'new (x-api-key)' if use_new else 'legacy (no key)'}")
    print(f"  Estimated requests: {max(1, (PILOT_BITS + BITS_PER_REQUEST - 1) // BITS_PER_REQUEST)}")
    print(f"  Estimated cost: ~$0.01 (if paid) or free (legacy)")
    print()

    bits: list[int] = []
    request_count = 0
    while len(bits) < PILOT_BITS:
        need_bytes = (PILOT_BITS - len(bits) + 7) // 8
        length = min(1024, max(1, need_bytes))
        try:
            if use_new and api_key:
                block = fetch_uint8_new(length, api_key)
            else:
                block = fetch_uint8_legacy(length)
        except Exception as e:
            print(f"Request failed: {e}", file=sys.stderr)
            sys.exit(1)
        request_count += 1
        bits.extend(uint8_to_bits(block))
        if not use_new:
            time.sleep(1)  # legacy rate limit ~1/min in some configs; be gentle

    bits = bits[:PILOT_BITS]
    n = len(bits)
    ones = sum(bits)
    p_hat = ones / n
    # z-score under null p=0.5
    import math
    se = math.sqrt(0.25 / n)
    z = (p_hat - 0.5) / se if se > 0 else 0

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    csv_path = OUTPUT_DIR / f"anu_qrng_pilot_{ts}_bits.csv"
    summary_path = OUTPUT_DIR / f"anu_qrng_pilot_{ts}_summary.json"

    with open(csv_path, "w") as f:
        f.write("value\n")
        for b in bits:
            f.write(f"{b}\n")

    summary = {
        "n_bits": n,
        "requests": request_count,
        "ones": ones,
        "p_hat": round(p_hat, 6),
        "z_score": round(z, 4),
        "api": "new" if use_new else "legacy",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print("Pilot OK")
    print(f"  N: {n}  P(1): {p_hat:.6f}  z: {z:.4f}")
    print(f"  Outputs: {csv_path.name}, {summary_path.name}")
    print(f"  Requests: {request_count}  (cost ~${request_count * 0.005:.2f} if paid)")
    print()
    print("Next: run full ladder (1M → 10M → 50M → 100M) with your existing scripts or scale this script.")


if __name__ == "__main__":
    main()
