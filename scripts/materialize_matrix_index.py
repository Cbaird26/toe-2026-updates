#!/usr/bin/env python3
"""Materialize docs/zora-matrix-builder/index.html from ~/Downloads/zora-matrix-fixed.html."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = Path.home() / "Downloads" / "zora-matrix-fixed.html"
DST = ROOT / "docs" / "zora-matrix-builder" / "index.html"


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"Missing source: {SRC}")
    DST.parent.mkdir(parents=True, exist_ok=True)
    text = SRC.read_text(encoding="utf-8")
    DST.write_text(text, encoding="utf-8")
    marker = DST.with_name(".matrix_index_materialized")
    marker.write_text(str(len(text)), encoding="utf-8")
    print(f"Wrote {DST} ({len(text)} bytes)")


if __name__ == "__main__":
    main()
