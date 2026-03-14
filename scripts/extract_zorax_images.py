#!/usr/bin/env python3
"""
Extract sample images from ZoraX (xAI/Grok export) to vault.

Reads prod-mc-asset-server content files from ZoraX zip, detects image format,
extracts first N to vault/zorax_sample/. Vault is gitignored; stays local.
"""
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

TOE = Path(__file__).resolve().parent.parent
VAULT = TOE / "data" / "zoraasi_export"
OUTPUT_DIR = VAULT / "zorax_sample"
ZORAX_DEFAULT = Path.home() / "Downloads" / "ZoraX-03.10.2026"

# Magic bytes for image formats
MAGIC = {
    b"\xff\xd8\xff": ".jpg",
    b"\x89PNG": ".png",
    b"RIFF": ".webp",  # RIFF....WEBP
}
MAX_EXTRACT = 20


def _detect_ext(data: bytes) -> str:
    """Detect image extension from magic bytes."""
    if len(data) < 12:
        return ".bin"
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if data.startswith(b"\x89PNG"):
        return ".png"
    if data.startswith(b"RIFF") and len(data) >= 12 and data[8:12] == b"WEBP":
        return ".webp"
    return ".bin"


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract sample Grok images from ZoraX to vault.")
    ap.add_argument("--zorax", type=Path, default=ZORAX_DEFAULT)
    ap.add_argument("--vault", type=Path, default=VAULT)
    ap.add_argument("-n", type=int, default=MAX_EXTRACT, help="Max images to extract")
    args = ap.parse_args()
    zorax = args.zorax.expanduser().resolve()
    output_dir = args.vault / "zorax_sample"
    n = max(1, min(args.n, 50))

    if not zorax.exists():
        print(f"ZoraX not found: {zorax}", file=__import__("sys").stderr)
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)
    count = 0

    with zipfile.ZipFile(zorax, "r") as zf:
        asset_paths = [p for p in zf.namelist() if "prod-mc-asset-server" in p and p.endswith("/content")]
        for path in asset_paths[: n * 3]:  # oversample in case some aren't images
            if count >= n:
                break
            try:
                data = zf.read(path)
                if len(data) < 500:  # skip tiny files
                    continue
                ext = _detect_ext(data)
                if ext == ".bin":
                    continue
                name = path.split("/")[-2] if "/" in path else path
                out_path = output_dir / f"{name}{ext}"
                out_path.write_bytes(data)
                count += 1
            except (zipfile.BadZipFile, OSError, KeyError):
                continue

    print(f"Extracted {count} images to {output_dir}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
