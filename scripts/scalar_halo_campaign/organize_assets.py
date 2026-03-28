#!/usr/bin/env python3
"""
Copy Scalar Halo / Cosmic Piano / SPARC-related PNGs from Cursor chat assets into
data/scalar_halo_campaign/, merge non-duplicate tables/scripts/reports (and gap-fill
PNGs) from Downloads/scalar_halo_artifact_bundle, and write artifact_manifest.csv.

Run from anywhere:
  python3 scripts/scalar_halo_campaign/organize_assets.py

Optional env:
  SCALAR_HALO_BUNDLE   — override bundle directory (default: ~/Downloads/scalar_halo_artifact_bundle)
  SCALAR_HALO_ASSETS   — override Cursor assets directory
"""
from __future__ import annotations

import csv
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

TOE_ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = TOE_ROOT / "data" / "scalar_halo_campaign"
HOME = Path.home()
DEFAULT_ASSETS = (
    HOME
    / ".cursor/projects/Users-christophermichaelbaird-Downloads-mqgt-frequency-atlas-bundle-2/assets"
)
ASSETS = Path(os.environ.get("SCALAR_HALO_ASSETS", DEFAULT_ASSETS))
DEFAULT_BUNDLE = HOME / "Downloads" / "scalar_halo_artifact_bundle"
BUNDLE = Path(os.environ.get("SCALAR_HALO_BUNDLE", DEFAULT_BUNDLE))

# Strip trailing UUID segment: name-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.png
UUID_SUFFIX = re.compile(
    r"^(.+)-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.png$",
    re.IGNORECASE,
)

# Only ingest Cursor assets that belong to this campaign (skip unrelated chat images).
CAMPAIGN_STEM_PREFIXES = (
    "scalar_halo_",
    "cosmic_piano_",
    "sparc_",
    "inner_halo_",
    "piano_v2_",
    "untitled",  # e.g. Untitled27.png after UUID strip; excludes unrelated misc chat images
)


def is_campaign_png(filename: str, logical_stem: str) -> bool:
    low = logical_stem.lower()
    return any(low.startswith(p) for p in CAMPAIGN_STEM_PREFIXES)


def theme_for_stem(stem: str) -> str:
    s = stem.lower()
    if s.startswith("scalar_halo"):
        return "scalar_halo"
    if s.startswith("cosmic_piano"):
        return "cosmic_piano"
    if s.startswith("sparc"):
        return "sparc"
    if s.startswith("inner_halo"):
        return "inner_halo"
    if s.startswith("piano_v2"):
        return "piano_v2"
    return "misc"


def theme_dir(theme: str) -> str:
    return f"figures/{theme}"


def logical_name(filename: str) -> str:
    m = UUID_SUFFIX.match(filename)
    if m:
        return m.group(1) + ".png"
    return filename


def ensure_layout() -> None:
    for sub in (
        "figures/scalar_halo",
        "figures/cosmic_piano",
        "figures/sparc",
        "figures/inner_halo",
        "figures/piano_v2",
        "figures/misc",
        "tables",
        "scripts",
        "reports",
    ):
        (CAMPAIGN / sub).mkdir(parents=True, exist_ok=True)


def copy_cursor_pngs(copied_at: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if not ASSETS.is_dir():
        print(f"Assets directory not found (skip PNG ingest): {ASSETS}")
        return rows

    pngs = sorted(ASSETS.glob("*.png"))
    names_used: dict[str, set[str]] = {}

    for src in pngs:
        logical = logical_name(src.name)
        stem = Path(logical).stem
        if not is_campaign_png(src.name, stem):
            continue
        theme = theme_for_stem(stem)
        rel_dir = theme_dir(theme)
        dest_dir = CAMPAIGN / rel_dir
        bucket = names_used.setdefault(rel_dir, set())

        if logical in bucket or (dest_dir / logical).exists():
            base = Path(logical).stem
            suf = Path(logical).suffix
            k = 1
            while True:
                candidate = f"{base}_{k}{suf}"
                if candidate not in bucket and not (dest_dir / candidate).exists():
                    logical = candidate
                    break
                k += 1
        bucket.add(logical)
        dest = dest_dir / logical
        shutil.copy2(src, dest)
        canon = f"{rel_dir}/{logical}"
        rows.append(
            {
                "canonical_relative_path": canon,
                "source_path": str(src),
                "theme": theme,
                "copied_at": copied_at,
            }
        )
    return rows


def merge_bundle(copied_at: str) -> list[dict[str, str]]:
    """Fill gaps from bundle: tables/scripts/reports, and PNGs not already present."""
    rows: list[dict[str, str]] = []
    if not BUNDLE.is_dir():
        print(f"Bundle directory not found (skip merge): {BUNDLE}")
        return rows

    for src in sorted(BUNDLE.iterdir()):
        if not src.is_file():
            continue
        name = src.name
        if name == "artifact_manifest.csv":
            continue

        suf = src.suffix.lower()
        if suf in (".csv", ".json"):
            dest = CAMPAIGN / "tables" / name
            theme = "bundle_table" if suf == ".csv" else "bundle_json"
        elif suf == ".py":
            dest = CAMPAIGN / "scripts" / name
            theme = "bundle_script"
        elif suf == ".md":
            dest = CAMPAIGN / "reports" / name
            theme = "bundle_report"
        elif suf == ".tex":
            dest = CAMPAIGN / "scripts" / name
            theme = "bundle_tex"
        elif suf == ".png":
            stem_lower = src.stem.lower()
            if not (
                stem_lower.startswith("scalar_halo")
                or stem_lower.startswith("cosmic_piano")
                or stem_lower.startswith("sparc")
                or stem_lower.startswith("inner_halo")
                or stem_lower.startswith("piano_v2")
            ):
                continue
            theme = theme_for_stem(src.stem)
            rel_dir = theme_dir(theme)
            dest = CAMPAIGN / rel_dir / name
        else:
            continue

        if dest.exists():
            continue
        shutil.copy2(src, dest)
        rel = dest.relative_to(CAMPAIGN).as_posix()
        rows.append(
            {
                "canonical_relative_path": rel,
                "source_path": str(src),
                "theme": theme,
                "copied_at": copied_at,
            }
        )
    return rows


def write_manifest(rows: list[dict[str, str]]) -> None:
    manifest = CAMPAIGN / "artifact_manifest.csv"
    rows_sorted = sorted(rows, key=lambda r: r["canonical_relative_path"])
    with manifest.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "canonical_relative_path",
                "source_path",
                "theme",
                "copied_at",
            ],
        )
        w.writeheader()
        w.writerows(rows_sorted)
    stamp = rows_sorted[0]["copied_at"] if rows_sorted else ""
    print(f"Wrote {manifest} ({len(rows_sorted)} rows{f', stamp {stamp}' if stamp else ''})")


def main() -> None:
    copied_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    ensure_layout()

    rows = copy_cursor_pngs(copied_at)
    n_cursor = len(rows)
    rows.extend(merge_bundle(copied_at))
    n_bundle = len(rows) - n_cursor

    write_manifest(rows)
    print(
        f"Ingested {n_cursor} figure(s) from Cursor assets; "
        f"added {n_bundle} file(s) from bundle gaps."
    )


if __name__ == "__main__":
    main()
