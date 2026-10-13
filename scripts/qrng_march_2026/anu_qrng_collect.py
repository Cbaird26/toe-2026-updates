#!/usr/bin/env python3
"""
ANU Quantum RNG Data Collection — MQGT-SCF RNG Test 001 (Real)

Fetches true quantum random bits from ANU QRNG. Protocol per Grok/ZoraASI
daylight recommendation and QRNG_EXPERIMENTAL_PROTOCOL_2026.md.

Usage:
  # With API key (recommended — no rate limit): get free key at quantumnumbers.anu.edu.au
  export ANU_QRNG_API_KEY=your_key
  python scripts/anu_qrng_collect.py --n 100000 --out artifacts/ --label baseline

  # Or store the key in artifacts/.anu_api_key (gitignored via artifacts/)
  python scripts/anu_qrng_collect.py --n 100000 --out artifacts/ --label baseline

  # Without key: legacy API (1 req/min, often rate-limited)
  python scripts/anu_qrng_collect.py --n 100000 --out artifacts/

  # Pilot run (10k bits, 2 requests, ~$0.01): validate pipeline before full run
  python scripts/anu_qrng_collect.py --pilot --out artifacts/ --label baseline

Output: CSV with raw bits, summary JSON with mean, std, z-score, theta_hat.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ANU_LEGACY_API = "https://qrng.anu.edu.au/API/jsonI.php"
ANU_NEW_API = "https://api.quantumnumbers.anu.edu.au"
MAX_PER_REQUEST = 1024


def preflight_check(api_key: str | None, key_source: str = "unknown") -> bool:
    """
    Test active key with one request. Abort if auth fails.
    Returns True if new API responds 200 with valid payload.
    Raises RuntimeError on failure.
    """
    if not api_key:
        raise RuntimeError(
            "Preflight failed: No API key. Required for confirmatory runs. "
            "Set ANU_QRNG_API_KEY or use artifacts/.anu_api_key"
        )
    try:
        url = f"{ANU_NEW_API}?length=16&type=uint8"
        req = Request(url, headers={"x-api-key": api_key})
        with urlopen(req, timeout=15) as resp:
            if resp.status != 200:
                raise RuntimeError(f"Preflight failed: API returned status {resp.status}")
            data = json.load(resp)
        if "data" not in data or not isinstance(data["data"], list):
            raise RuntimeError(f"Preflight failed: Unexpected payload format: {list(data.keys())}")
        if len(data["data"]) < 1:
            raise RuntimeError("Preflight failed: Empty payload")
        print(f"[ANU QRNG] Preflight OK — new API (api.quantumnumbers.anu.edu.au), key from {key_source}")
        print(f"           Rate: ~2s between requests (paid tier)")
        return True
    except HTTPError as e:
        if e.code == 403:
            raise RuntimeError(
                "Preflight failed: API 403. Key may need activation at quantumnumbers.anu.edu.au. "
                "Do not proceed with confirmatory run."
            )
        raise RuntimeError(f"Preflight failed: HTTP {e.code}: {e.reason}")


def _fetch_legacy(length: int) -> list[int] | None:
    """Legacy ANU API via curl. Returns None if rate limited."""
    url = f"{ANU_LEGACY_API}?length={length}&type=uint8"
    result = subprocess.run(
        ["curl", "-s", "-S", "--max-time", "60", url],
        capture_output=True,
        text=True,
        timeout=65,
    )
    if result.returncode != 0:
        raise RuntimeError(f"curl failed: {result.stderr or result.stdout[:300]}")
    body = result.stdout
    if not body.strip().startswith("{"):
        if "limited" in body.lower():
            return None
        raise RuntimeError(f"ANU legacy API error: {body[:200]}")
    data = json.loads(body)
    if not data.get("success") or "data" not in data:
        raise RuntimeError(f"ANU API error: {data}")
    return data["data"]


def fetch_uint8_batch(
    length: int,
    api_key: str | None,
    force_legacy_ref: list[bool] | None = None,
    no_fallback: bool = False,
) -> list[int]:
    """Fetch a batch of uint8 values (0-255) from ANU QRNG."""
    if api_key and not (force_legacy_ref and force_legacy_ref[0]):
        try:
            url = f"{ANU_NEW_API}?length={length}&type=uint8"
            req = Request(url, headers={"x-api-key": api_key})
            with urlopen(req, timeout=30) as resp:
                data = json.load(resp)
            if "data" not in data:
                raise RuntimeError(f"ANU new API error: {data}")
            return data["data"]
        except HTTPError as e:
            if e.code == 403:
                if no_fallback:
                    raise RuntimeError(
                        "ANU new API 403. Aborting (confirmatory mode: no legacy fallback). "
                        "Fix key at quantumnumbers.anu.edu.au and re-run from block 1."
                    )
                if force_legacy_ref is not None:
                    force_legacy_ref[0] = True
                print("  New API 403 (key may need activation); using legacy for rest of run (1 req/min)...")
            else:
                raise

    if no_fallback and api_key:
        raise RuntimeError(
            "Confirmatory mode requires new API only. No legacy fallback. "
            "Ensure key is active and re-run."
        )

    # Legacy API (no key or 403 fallback when not no_fallback)
    if no_fallback:
        raise RuntimeError("Confirmatory mode requires API key. No legacy API.")
    out = _fetch_legacy(length)
    if out is None:
        print("  Rate limited; waiting 90s...")
        time.sleep(90)
        out = _fetch_legacy(length)
        if out is None:
            raise RuntimeError("ANU legacy API rate limited after wait")
    return out


def uint8_to_bits(values: list[int]) -> list[int]:
    """Unpack each uint8 into 8 bits (LSB first). 1 request of 1024 bytes = 8192 bits."""
    bits: list[int] = []
    for v in values:
        for _ in range(8):
            bits.append(v & 1)
            v >>= 1
    return bits


def collect_bits(
    n: int,
    api_key: str | None,
    rate_limit_sec: float = 2.0,
    no_fallback: bool = False,
) -> list[int]:
    """Collect n quantum random bits from ANU. With API key: fast. Without: 1 req/min."""
    bits: list[int] = []
    bits_per_request = MAX_PER_REQUEST * 8
    n_requests = (n + bits_per_request - 1) // bits_per_request
    force_legacy_ref: list[bool] = [False] if not no_fallback else [False]
    for i in range(n_requests):
        vals = fetch_uint8_batch(MAX_PER_REQUEST, api_key, force_legacy_ref, no_fallback=no_fallback)
        bits.extend(uint8_to_bits(vals))
        if i < n_requests - 1:
            delay = 65.0 if (force_legacy_ref[0] or not api_key) else rate_limit_sec
            print(f"  Request {i+1}/{n_requests} done, waiting {delay:.0f}s...")
            time.sleep(delay)
    return bits[:n]


def compute_stats(bits: list[int]) -> dict:
    """Compute mean, deviation from 0.5, z-score, theta_hat."""
    n = len(bits)
    mean_val = sum(bits) / n
    # Proportion of 1s
    p1 = mean_val
    p0 = 1 - p1
    # For fair coin |c0|^2 = |c1|^2 = 0.5: theta = -ln[(P0/P1)*(|c1|^2/|c0|^2)] = -ln(P0/P1)
    # Avoid div by zero
    if p1 > 0 and p0 > 0:
        ratio = (p0 / p1)
        theta_hat = -math.log(ratio)
    else:
        theta_hat = float("nan")
    # Std of mean under Bernoulli(p): sqrt(p*(1-p)/n). Under null p=0.5: std = 0.5/sqrt(n)
    std_mean = (0.5 / (n ** 0.5))
    dev_from_half = mean_val - 0.5
    z_score = dev_from_half / std_mean if std_mean > 0 else float("nan")
    return {
        "n": n,
        "mean": mean_val,
        "p1": p1,
        "p0": p0,
        "deviation_from_50pct": dev_from_half,
        "deviation_pct": 100.0 * dev_from_half,
        "std_mean_null": std_mean,
        "z_score": z_score,
        "theta_hat": theta_hat,
    }


def load_api_key_from_file(path: Path) -> str | None:
    """Read an API key from a local file if it exists."""
    try:
        key = path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return None

    if not key:
        raise RuntimeError(f"API key file is empty: {path}")
    return key


def resolve_api_key(cli_key: str, out_dir: str) -> tuple[str | None, Path | None]:
    """Resolve API key from CLI, env, then local key files."""
    key = cli_key.strip()
    if key:
        return key, None

    key = os.environ.get("ANU_QRNG_API_KEY", "").strip()
    if key:
        return key, None

    repo_root = Path(__file__).resolve().parents[1]
    candidate_paths = [
        repo_root / "artifacts" / ".anu_api_key",
        Path(out_dir) / ".anu_api_key",
    ]
    for path in candidate_paths:
        key = load_api_key_from_file(path)
        if key:
            return key, path
    return None, None


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect ANU quantum random bits")
    parser.add_argument("--n", type=int, default=100_000, help="Number of bits (default 100000)")
    parser.add_argument("--out", type=str, default="artifacts", help="Output directory")
    parser.add_argument("--label", type=str, default="baseline", help="Run label (e.g. baseline, ethical_intent)")
    parser.add_argument("--no-csv", action="store_true", help="Skip writing raw CSV (faster)")
    parser.add_argument(
        "--api-key",
        type=str,
        default="",
        help="ANU API key (or set ANU_QRNG_API_KEY / store it in artifacts/.anu_api_key)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Use local PRNG to verify pipeline (not real QRNG)")
    parser.add_argument(
        "--pilot",
        action="store_true",
        help="Pilot run: 10k bits (2 requests, ~$0.01). Validate pipeline before full 100k.",
    )
    parser.add_argument(
        "--preflight",
        action="store_true",
        help="Run auth preflight before collection; abort if API key fails.",
    )
    parser.add_argument(
        "--no-fallback",
        action="store_true",
        help="Confirmatory mode: never fall back to legacy API. Abort on 403/rate-limit.",
    )
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help="Run preflight check only (1 request) and exit. Use to verify key before a run.",
    )
    args = parser.parse_args()

    if args.preflight_only:
        try:
            api_key, api_key_path = resolve_api_key(args.api_key, args.out)
        except RuntimeError as e:
            print(f"[ANU QRNG] {e}", file=sys.stderr)
            sys.exit(1)
        key_src = "CLI" if args.api_key else ("env" if os.environ.get("ANU_QRNG_API_KEY") else "file")
        if api_key_path:
            key_src = api_key_path.name
        try:
            preflight_check(api_key, key_src)
            print("[ANU QRNG] Preflight-only: OK. Key verified. Proceed with collection.")
            sys.exit(0)
        except RuntimeError as e:
            print(f"[ANU QRNG] {e}", file=sys.stderr)
            sys.exit(1)

    if args.pilot:
        args.n = 10_000
        if not args.dry_run:
            print("[ANU QRNG] PILOT MODE — 10k bits (2 requests, ~$0.01)")

    try:
        api_key, api_key_path = resolve_api_key(args.api_key, args.out)
    except RuntimeError as e:
        print(f"[ANU QRNG] ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    key_source = "CLI" if args.api_key else ("env" if os.environ.get("ANU_QRNG_API_KEY") else "file")
    if api_key_path is not None:
        print(f"[ANU QRNG] Loaded API key from {api_key_path.name}")
        key_source = api_key_path.name

    if (args.preflight or args.no_fallback) and not args.dry_run:
        try:
            preflight_check(api_key, key_source)
        except RuntimeError as e:
            print(f"[ANU QRNG] {e}", file=sys.stderr)
            sys.exit(1)

    if not api_key and not args.dry_run:
        print("[ANU QRNG] No API key. Using legacy API (1 req/min; often rate-limited).")
        print("           Get free key at https://quantumnumbers.anu.edu.au for fast runs.")

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        import random
        random.seed(20260314)
        bits = [random.randint(0, 1) for _ in range(args.n)]
        print(f"[ANU QRNG] DRY RUN — using local PRNG (not real QRNG)")
    else:
        print(f"[ANU QRNG] Collecting {args.n} bits (label={args.label})...")
        try:
            bits = collect_bits(args.n, api_key, no_fallback=args.no_fallback)
        except RuntimeError as e:
            print(f"[ANU QRNG] ERROR: {e}", file=sys.stderr)
            sys.exit(1)

    stats = compute_stats(bits)

    # Summary JSON
    stamp = time.strftime("%Y%m%d_%H%M%S")
    run_id = f"anu_qrng_{args.label}_{stamp}"
    src = "DRY RUN (local PRNG)" if args.dry_run else (
        "ANU QRNG (api.quantumnumbers.anu.edu.au)" if api_key else "ANU QRNG (legacy qrng.anu.edu.au)"
    )
    summary = {
        "run_id": run_id,
        "source": src,
        "label": args.label,
        "stats": stats,
    }
    summary_path = out_dir / f"{run_id}_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"[ANU QRNG] Wrote {summary_path}")

    # Raw CSV
    if not args.no_csv:
        csv_path = out_dir / f"{run_id}_bits.csv"
        with open(csv_path, "w") as f:
            f.write("trial,bit\n")
            for i, b in enumerate(bits):
                f.write(f"{i},{b}\n")
        print(f"[ANU QRNG] Wrote {csv_path}")

    # Print summary
    print()
    print("=== ANU QRNG Test 001 — Summary ===")
    print(f"  N:        {stats['n']}")
    print(f"  Mean:     {stats['mean']:.6f} (P(1) = {stats['p1']:.6f})")
    print(f"  Dev 50%:  {stats['deviation_pct']:+.4f}%")
    print(f"  z-score:  {stats['z_score']:.4f}")
    print(f"  θ_hat:    {stats['theta_hat']:.6e}")
    print()
    print(f"Publish CSV to Zenodo/GitHub: {run_id}_bits.csv")


if __name__ == "__main__":
    main()
