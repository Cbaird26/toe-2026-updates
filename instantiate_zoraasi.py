#!/usr/bin/env python3
"""
ZoraASI Multi-Source Instantiation

Discovers ZoraASI artifacts across Cloud, Google Drive, OneDrive, iCloud, and
local filesystem; selects the single most-recent source; syncs to canonical vault;
runs ingest + distill; writes manifest. Does NOT launch run_chat, serve_webui, or API.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# --- Paths ---
TOE_ROOT = Path(__file__).resolve().parent
CANONICAL_VAULT = TOE_ROOT / "data" / "zoraasi_export"
ZORAASI_SCRIPTS = TOE_ROOT / "zoraasi" / "scripts"

# Configurable via env
HOME = Path.home()
GOOGLE_DRIVE = Path(os.environ.get("GOOGLE_DRIVE_PATH", HOME / "Library/CloudStorage/GoogleDrive-cbaird26@gmail.com"))
ICLOUD_DOCS = Path(os.environ.get("ICLOUD_PATH", HOME / "Library/Mobile Documents/com~apple~CloudDocs"))
ONEDRIVE_BASE = Path(os.environ.get("ONEDRIVE_PATH", HOME / "Library/CloudStorage"))
CLOUD_VAULT_PATH = os.environ.get("ZORA_VAULT_URL") or os.environ.get("CLOUD_VAULT_PATH")

# Artifact names to search
ZIP_NAMES = ("ZoraASI.zip", "ZoraASI-Origin.zip")
DIR_NAMES = ("zoraasi_export", "ZoraASI", "ZoraASI-Origin")
CONVERSATIONS_JSON = "conversations.json"


@dataclass
class Artifact:
    path: Path
    artifact_type: str  # "zip" | "dir"
    mtime: float
    source_label: str

    def __lt__(self, other: "Artifact") -> bool:
        return self.mtime < other.mtime


def _find_conversations_json(root: Path) -> Optional[Path]:
    """Find conversations.json under root (direct or in subdir)."""
    direct = root / CONVERSATIONS_JSON
    if direct.exists():
        return direct
    for p in root.rglob(CONVERSATIONS_JSON):
        return p
    return None


def _get_dir_mtime(d: Path) -> float:
    """Use conversations.json mtime if present, else dir mtime."""
    cj = _find_conversations_json(d)
    if cj:
        return cj.stat().st_mtime
    return d.stat().st_mtime


def _is_valid_vault_dir(d: Path) -> bool:
    return _find_conversations_json(d) is not None


def _scan_dir(parent: Path, source_label: str, artifacts: list[Artifact], max_depth: int = 8) -> None:
    """Recursively scan for ZoraASI artifacts under parent. Limit depth to avoid slow scans."""
    if max_depth < 0:
        return
    try:
        if not parent.exists() or not parent.is_dir():
            return
        for child in parent.iterdir():
            try:
                if child.is_file() and child.suffix.lower() == ".zip" and child.name in ZIP_NAMES:
                    artifacts.append(Artifact(
                        path=child, artifact_type="zip", mtime=child.stat().st_mtime,
                        source_label=source_label,
                    ))
                elif child.is_dir() and child.name in DIR_NAMES and _is_valid_vault_dir(child):
                    artifacts.append(Artifact(
                        path=child, artifact_type="dir", mtime=_get_dir_mtime(child),
                        source_label=source_label,
                    ))
                elif child.is_dir() and not child.name.startswith("."):
                    _scan_dir(child, source_label, artifacts, max_depth - 1)
            except OSError:
                continue
    except OSError:
        pass


def discover_artifacts() -> list[Artifact]:
    """Discover ZoraASI artifacts from all configured sources."""
    artifacts: list[Artifact] = []

    # Local computer
    local_paths = [
        TOE_ROOT / "data" / "zoraasi_export",
        HOME / "Desktop" / "ZoraCore" / "Zora-Core",
        HOME / "Desktop" / "ZoraCore" / "ZoraCore",
        HOME / "Downloads" / "Archives",
        HOME / "Desktop" / "Project Zora - Desktop" / "vault",
        HOME / "Downloads" / "TOE" / "data" / "zoraasi_export",
        HOME / "Downloads" / "ZoraASI",
        HOME / "Downloads" / "ZoraASI-Origin",
    ]
    for p in local_paths:
        if p.exists():
            if p.is_file() and p.suffix.lower() == ".zip" and p.name in ZIP_NAMES:
                artifacts.append(Artifact(p, "zip", p.stat().st_mtime, "local"))
            elif p.is_dir():
                if p.name in DIR_NAMES and _is_valid_vault_dir(p):
                    artifacts.append(Artifact(p, "dir", _get_dir_mtime(p), "local"))
                elif p.name in ("Zora-Core", "ZoraCore", "Archives", "vault"):
                    for f in p.iterdir():
                        if f.is_file() and f.name in ZIP_NAMES:
                            artifacts.append(Artifact(f, "zip", f.stat().st_mtime, "local"))
                        elif f.is_dir() and f.name in DIR_NAMES and _is_valid_vault_dir(f):
                            artifacts.append(Artifact(f, "dir", _get_dir_mtime(f), "local"))
                else:
                    _scan_dir(p, "local", artifacts, max_depth=2)

    # Google Drive
    gd = GOOGLE_DRIVE / "My Drive" if (GOOGLE_DRIVE / "My Drive").exists() else GOOGLE_DRIVE
    if gd.exists():
        _scan_dir(gd, "google_drive", artifacts, max_depth=6)

    # iCloud
    for sub in ("Zora", "TOE COMPLETE", "Archives", "Downloads"):
        ic = ICLOUD_DOCS / sub
        if ic.exists():
            _scan_dir(ic, "icloud", artifacts, max_depth=6)

    # OneDrive (skip if not mounted; set ONEDRIVE_PATH env to override)
    if ONEDRIVE_BASE.exists():
        for d in ONEDRIVE_BASE.iterdir():
            if d.is_dir() and "onedrive" in d.name.lower():
                _scan_dir(d, "onedrive", artifacts, max_depth=6)
                break

    # Cloud env (manifest-only; no local path to scan)
    if CLOUD_VAULT_PATH:
        p = Path(CLOUD_VAULT_PATH)
        if p.exists():
            if p.is_dir() and _is_valid_vault_dir(p):
                artifacts.append(Artifact(p, "dir", _get_dir_mtime(p), "cloud"))
            elif p.is_file() and p.suffix.lower() == ".zip":
                artifacts.append(Artifact(p, "zip", p.stat().st_mtime, "cloud"))

    return artifacts


def pick_best(artifacts: list[Artifact]) -> Optional[Artifact]:
    """Pick single most-recent artifact by mtime."""
    if not artifacts:
        return None
    return max(artifacts, key=lambda a: a.mtime)


def sync_to_canonical(best: Artifact) -> Path:
    """Sync best artifact to canonical vault. Returns the vault dir to pass to ingest (may be subdir)."""
    CANONICAL_VAULT.parent.mkdir(parents=True, exist_ok=True)

    if best.artifact_type == "zip":
        with zipfile.ZipFile(best.path, "r") as zf:
            zf.extractall(CANONICAL_VAULT)
        # Find where conversations.json landed
        conv = _find_conversations_json(CANONICAL_VAULT)
        if conv:
            return conv.parent
        return CANONICAL_VAULT

    # Dir: if already the canonical vault (or subdir of it), skip copy
    try:
        best_resolved = best.path.resolve()
        canon_resolved = CANONICAL_VAULT.resolve()
        if best_resolved == canon_resolved or str(best_resolved).startswith(str(canon_resolved) + os.sep):
            conv = _find_conversations_json(best.path)
            return conv.parent if conv else best.path
    except OSError:
        pass

    # Dir: copy into canonical
    if CANONICAL_VAULT.exists():
        shutil.rmtree(CANONICAL_VAULT)
    shutil.copytree(best.path, CANONICAL_VAULT)
    conv = _find_conversations_json(CANONICAL_VAULT)
    return conv.parent if conv else CANONICAL_VAULT


def run_ingest(vault: Path) -> bool:
    """Run ingest.py. Returns True on success."""
    ingest = ZORAASI_SCRIPTS / "ingest.py"
    if not ingest.exists():
        print(f"WARNING: ingest.py not found at {ingest}")
        return False
    env = os.environ.copy()
    env["VAULT_PATH"] = str(vault)
    r = subprocess.run(
        [os.environ.get("PYTHON", "python3"), str(ingest), "--vault", str(vault)],
        cwd=str(TOE_ROOT), env=env, capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"ingest failed: {r.stderr}")
        return False
    print(r.stdout or "ingest OK")
    return True


def run_distill(vault: Path) -> bool:
    """Run distill_personality.py. Returns True on success."""
    distill = ZORAASI_SCRIPTS / "distill_personality.py"
    if not distill.exists():
        print(f"WARNING: distill_personality.py not found at {distill}")
        return False
    env = os.environ.copy()
    env["VAULT_PATH"] = str(vault)
    r = subprocess.run(
        [os.environ.get("PYTHON", "python3"), str(distill), "--vault", str(vault)],
        cwd=str(TOE_ROOT), env=env, capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"distill failed: {r.stderr}")
        return False
    print(r.stdout or "distill OK")
    return True


def write_manifest(source_path: str, source_mtime: float, vault_path: Path, refreshed_at: str) -> None:
    """Write instantiation manifest."""
    manifest = {
        "source_path": source_path,
        "source_mtime": source_mtime,
        "source_mtime_iso": datetime.fromtimestamp(source_mtime, tz=timezone.utc).isoformat(),
        "vault_path": str(vault_path),
        "VAULT_PATH": str(vault_path),
        "refreshed_at": refreshed_at,
        "ready_for_remote": True,
    }
    manifest_path = TOE_ROOT / "data" / "zoraasi_instantiation.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Manifest: {manifest_path}")


def main() -> int:
    print("ZoraASI Multi-Source Instantiation")
    print("Discovering artifacts...")

    artifacts = discover_artifacts()
    sources = {}
    for a in artifacts:
        sources[a.source_label] = sources.get(a.source_label, 0) + 1
    if sources:
        print("Sources scanned:", ", ".join(f"{k}({v})" for k, v in sorted(sources.items())))
    if not artifacts:
        print("ERROR: No ZoraASI artifacts found. Check Cloud, Google Drive, iCloud, OneDrive, and local paths.")
        return 1

    best = pick_best(artifacts)
    if not best:
        return 1
    print(f"Best source: {best.path} (mtime {best.mtime}, {best.source_label})")

    print("Syncing to canonical vault...")
    try:
        vault = sync_to_canonical(best)
    except Exception as e:
        print(f"ERROR: Sync failed: {e}")
        return 1

    print("Running ingest...")
    if not run_ingest(vault):
        return 1

    print("Running distill_personality...")
    if not run_distill(vault):
        return 1

    refreshed_at = datetime.now(timezone.utc).isoformat()
    write_manifest(str(best.path), best.mtime, vault, refreshed_at)

    print("Done. Vault ready for remote run_chat/serve_webui with VAULT_PATH=", str(vault))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
