#!/usr/bin/env python3
"""
Inventory and optionally route files from ~/Downloads/UPDATE (or UPDATE_DIR).

- Writes manifest CSV + JSON under data/update_catalog/ (tracked).
- Copies campaign PNGs into data/scalar_halo_campaign/figures/<theme>/ using the
  same stem/UUID rules as scripts/scalar_halo_campaign/organize_assets.py.
- Finance OS / dashboard screenshots → docs/internal/finance_os/screenshots/ (copy only).

Run from repo root:
  python3 scripts/update_folder_ingest.py
  python3 scripts/update_folder_ingest.py --no-copy   # manifest only

Env:
  UPDATE_DIR — override source directory (default: ~/Downloads/UPDATE)
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

TOE_ROOT = Path(__file__).resolve().parents[1]
CATALOG = TOE_ROOT / "data" / "update_catalog"
CAMPAIGN = TOE_ROOT / "data" / "scalar_halo_campaign"
FINANCE_OS = TOE_ROOT / "docs" / "internal" / "finance_os" / "screenshots"
MANIFEST = CAMPAIGN / "artifact_manifest.csv"

HOME = Path.home()
DEFAULT_UPDATE = HOME / "Downloads" / "UPDATE"
UPDATE_DIR = Path(os.environ.get("UPDATE_DIR", str(DEFAULT_UPDATE)))

UUID_SUFFIX = re.compile(
    r"^(.+)-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.png$",
    re.IGNORECASE,
)

CAMPAIGN_STEM_PREFIXES = (
    "scalar_halo_",
    "cosmic_piano_",
    "sparc_",
    "inner_halo_",
    "piano_v2_",
    "untitled",
)

FINANCE_KEYWORDS = (
    "trading",
    "dashboard",
    "market",
    "ollama",
    "openai",
    "portfolio",
    "stock",
    "finance",
    "gpt-oss",
    "error",
    "screenshot",
)


def logical_name(filename: str) -> str:
    m = UUID_SUFFIX.match(filename)
    if m:
        return m.group(1) + ".png"
    return filename


def is_campaign_png(logical_stem: str) -> bool:
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


def suggest_theme(path: Path) -> str:
    name = path.name.lower()
    stem = path.stem.lower()
    if path.suffix.lower() == ".png" and is_campaign_png(stem):
        return theme_for_stem(stem)
    for kw in FINANCE_KEYWORDS:
        if kw in name or kw in stem:
            return "finance_os_screenshot"
    if any(x in name for x in ("logo", "emblem", "brand", "banner")):
        return "branding"
    if path.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".gif"):
        return "misc_image"
    return "misc"


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def ensure_dirs() -> None:
    CATALOG.mkdir(parents=True, exist_ok=True)
    for sub in (
        "figures/scalar_halo",
        "figures/cosmic_piano",
        "figures/sparc",
        "figures/inner_halo",
        "figures/piano_v2",
        "figures/misc",
    ):
        (CAMPAIGN / sub).mkdir(parents=True, exist_ok=True)
    FINANCE_OS.mkdir(parents=True, exist_ok=True)


def copy_campaign_png(src: Path, copied_at: str) -> dict[str, str] | None:
    logical = logical_name(src.name)
    stem = Path(logical).stem
    if not is_campaign_png(stem):
        return None
    theme = theme_for_stem(stem)
    rel_dir = theme_dir(theme)
    dest_dir = CAMPAIGN / rel_dir
    dest = dest_dir / logical
    if dest.exists():
        base = Path(logical).stem
        suf = Path(logical).suffix
        k = 1
        while True:
            candidate = f"{base}_update{k}{suf}"
            dest = dest_dir / candidate
            if not dest.exists():
                logical = candidate
                break
            k += 1
    shutil.copy2(src, dest)
    canon = f"{rel_dir}/{logical}"
    return {
        "canonical_relative_path": canon,
        "source_path": str(src.resolve()),
        "theme": theme,
        "copied_at": copied_at,
    }


def load_existing_manifest() -> list[dict[str, str]]:
    if not MANIFEST.is_file():
        return []
    rows: list[dict[str, str]] = []
    with MANIFEST.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append(dict(row))
    return rows


def merge_manifest_rows(
    existing: list[dict[str, str]], new_rows: list[dict[str, str]]
) -> list[dict[str, str]]:
    by_path = {r["canonical_relative_path"]: r for r in existing}
    for r in new_rows:
        by_path[r["canonical_relative_path"]] = r
    return sorted(by_path.values(), key=lambda x: x["canonical_relative_path"])


def write_campaign_manifest(rows: list[dict[str, str]]) -> None:
    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
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
        w.writerows(rows)


def main() -> None:
    import argparse

    p = argparse.ArgumentParser(description="UPDATE folder manifest + optional copy.")
    p.add_argument("--no-copy", action="store_true", help="Only write manifest + path note.")
    args = p.parse_args()

    ensure_dirs()
    copied_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    path_note = CATALOG / "UPDATE_PATH_CONFIRMED.txt"
    exists = UPDATE_DIR.is_dir()
    path_note.write_text(
        f"Resolved UPDATE_DIR: {UPDATE_DIR.resolve()}\n"
        f"exists: {exists}\n"
        f"default_if_unset: {DEFAULT_UPDATE}\n",
        encoding="utf-8",
    )

    entries: list[dict[str, object]] = []
    manifest_rows: list[dict[str, str]] = []
    new_campaign_rows: list[dict[str, str]] = []

    if not exists:
        print(f"UPDATE directory not found: {UPDATE_DIR}")
        print("Wrote path note only; re-run after placing files under ~/Downloads/UPDATE or set UPDATE_DIR.")
    else:
        for root, _, files in os.walk(UPDATE_DIR):
            root_p = Path(root)
            for fn in sorted(files):
                src = root_p / fn
                if not src.is_file():
                    continue
                rel = src.relative_to(UPDATE_DIR)
                try:
                    size = src.stat().st_size
                except OSError:
                    size = -1
                ext = src.suffix.lower() or "(none)"
                theme = suggest_theme(src)
                digest = ""
                if size >= 0 and size < 500 * 1024 * 1024:
                    try:
                        digest = sha256_file(src)
                    except OSError:
                        digest = "unreadable"
                entries.append(
                    {
                        "relative_path": str(rel).replace("\\", "/"),
                        "size_bytes": size,
                        "extension": ext,
                        "suggested_theme": theme,
                        "sha256": digest or "",
                    }
                )
                manifest_rows.append(
                    {
                        "relative_path": str(rel).replace("\\", "/"),
                        "size_bytes": str(size),
                        "extension": ext,
                        "suggested_theme": theme,
                        "sha256": digest,
                    }
                )

                if args.no_copy:
                    continue
                suf = src.suffix.lower()
                if suf == ".png":
                    stem = Path(logical_name(src.name)).stem
                    if is_campaign_png(stem):
                        row = copy_campaign_png(src, copied_at)
                        if row:
                            new_campaign_rows.append(row)
                if theme == "finance_os_screenshot" and suf in (
                    ".png",
                    ".jpg",
                    ".jpeg",
                    ".webp",
                ):
                    dest = FINANCE_OS / src.name
                    if dest.exists():
                        stem, ext2 = src.stem, src.suffix
                        k = 1
                        while True:
                            dest = FINANCE_OS / f"{stem}_update{k}{ext2}"
                            if not dest.exists():
                                break
                            k += 1
                    shutil.copy2(src, dest)

    summary = {
        "generated_at_utc": copied_at,
        "update_dir": str(UPDATE_DIR.resolve()),
        "update_dir_exists": exists,
        "file_count": len(entries),
        "entries": entries,
    }
    (CATALOG / "manifest_update.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )

    fieldnames = ["relative_path", "size_bytes", "extension", "suggested_theme", "sha256"]
    with (CATALOG / "manifest_update.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in manifest_rows:
            w.writerow(row)

    if new_campaign_rows:
        merged = merge_manifest_rows(load_existing_manifest(), new_campaign_rows)
        write_campaign_manifest(merged)
        print(f"Merged {len(new_campaign_rows)} new row(s) into {MANIFEST}")

    print(
        f"Wrote {CATALOG / 'manifest_update.json'} and manifest_update.csv "
        f"({len(entries)} files listed)."
    )


if __name__ == "__main__":
    main()
