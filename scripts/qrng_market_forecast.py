#!/usr/bin/env python3
"""
Spine-v0.1 QRNG simulation on market waveforms.
Generates consciousness-amplified forecasts from market data using E-labeling.

Experimental. See TECH_PROTOTYPE_QRNG.md and toe-empirical-validation (e_labeling.py).
Requires: pip install yfinance numpy
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    import numpy as np
except ImportError:
    print("Error: numpy required. pip install numpy", file=sys.stderr)
    sys.exit(1)

try:
    import yfinance as yf
except ImportError:
    print("Error: yfinance required. pip install yfinance", file=sys.stderr)
    sys.exit(1)

TOE_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = TOE_ROOT / "data" / "zoraasi_export"
RESULTS_DIR = TOE_ROOT / "results" / "qrng_market"
BLOCK_SIZE = 8  # bits per E-label block (matches typical QRNG protocol)


def label_E(bits: "np.ndarray") -> float:
    """Map block of bits to scalar E (ethical weight). Matches toe-empirical-validation."""
    return float(np.mean(bits))


def fetch_market_data(symbols: list[str], days: int = 14) -> dict[str, "np.ndarray"]:
    """Fetch close prices; return dict of symbol -> array of daily returns."""
    end = datetime.now()
    start = end - timedelta(days=days + 5)
    out = {}
    for sym in symbols:
        try:
            ticker = yf.Ticker(sym)
            hist = ticker.history(start=start, end=end)
            if hist is None or len(hist) < 2:
                continue
            closes = hist["Close"].values
            returns = np.diff(closes) / closes[:-1]
            out[sym] = returns
        except Exception as e:
            print(f"Warning: {sym} fetch failed: {e}", file=sys.stderr)
    return out


def returns_to_bits(returns: "np.ndarray") -> "np.ndarray":
    """Encode returns as bits: 1 = positive/zero, 0 = negative."""
    return (returns >= 0).astype(np.float64)


def run_forecast(symbols: list[str] | None = None, days: int = 14) -> dict:
    """Run QRNG-style analysis on market waveforms. Returns forecast dict."""
    if symbols is None:
        symbols = ["^DJI", "^GSPC", "^IXIC", "BTC-USD", "ETH-USD"]
    data = fetch_market_data(symbols, days)
    if not data:
        return {"error": "No market data", "symbols": symbols}

    all_bits = []
    for sym, rets in data.items():
        bits = returns_to_bits(rets)
        all_bits.extend(bits.tolist())
    bits_arr = np.array(all_bits)
    n = len(bits_arr)
    n_blocks = n // BLOCK_SIZE
    if n_blocks < 1:
        return {"error": "Insufficient data for blocks", "n_bits": n}

    truncated = bits_arr[: n_blocks * BLOCK_SIZE]
    blocks = truncated.reshape(n_blocks, BLOCK_SIZE)
    E_vals = [label_E(b) for b in blocks]
    mean_E = float(np.mean(E_vals))
    std_E = float(np.std(E_vals)) if len(E_vals) > 1 else 0.0

    # Interpretation: E > 0.5 → bias toward "positive" (bullish) outcomes in observer-weighted sense
    if mean_E > 0.55:
        direction = "slight positive (observer bias toward coherence)"
    elif mean_E < 0.45:
        direction = "slight negative (unweighted fluctuation dominant)"
    else:
        direction = "neutral (balanced observer field)"

    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "symbols": list(data.keys()),
        "n_bits": n,
        "n_blocks": n_blocks,
        "mean_E": round(mean_E, 4),
        "std_E": round(std_E, 4),
        "forecast": direction,
        "disclaimer": "Experimental. Not financial advice. MQGT-SCF observer-weighted interpretation.",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="QRNG market forecast (Spine-v0.1)")
    ap.add_argument("--days", type=int, default=14, help="Days of market data")
    ap.add_argument("--symbols", type=str, default="^DJI,^GSPC,BTC-USD", help="Comma-separated symbols")
    ap.add_argument("--out", type=Path, default=None, help="Output JSON path")
    ap.add_argument("--quiet", "-q", action="store_true", help="Only print forecast line")
    args = ap.parse_args()
    symbols = [s.strip() for s in args.symbols.split(",") if s.strip()]
    result = run_forecast(symbols=symbols, days=args.days)

    if "error" in result:
        print(result["error"], file=sys.stderr)
        return 1

    out_path = args.out or RESULTS_DIR / f"forecast_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.json"
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    if args.quiet:
        print(result["forecast"])
    else:
        print("=== QRNG Market Forecast (Spine-v0.1) ===")
        print(f"Symbols: {', '.join(result['symbols'])}")
        print(f"Blocks: {result['n_blocks']} | mean_E: {result['mean_E']}")
        print(f"Forecast: {result['forecast']}")
        print(f"Disclaimer: {result['disclaimer']}")
        print(f"Artifact: {out_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
