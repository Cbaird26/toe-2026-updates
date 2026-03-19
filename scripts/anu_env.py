#!/usr/bin/env python3
"""Shared ANU QRNG environment loading and key resolution."""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_FILES = (".env.anu", ".env")


def load_repo_env(*, override: bool = False) -> None:
    """Load ignored local env files from the repo root without overriding shell exports."""
    for name in ENV_FILES:
        _load_env_file(REPO_ROOT / name, override=override)


def _load_env_file(path: Path, *, override: bool) -> None:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        if override or key not in os.environ:
            os.environ[key] = value


def resolve_anu_api_key(cli_key: str = "", preferred_tier: str = "auto") -> tuple[str | None, str | None]:
    """
    Resolve ANU API key from CLI or environment.

    Order:
      1. CLI key
      2. ANU_API_KEY
      3. ANU_QRNG_API_KEY
      4. Tier-aware vars (ANU_API_KEY_PAID / ANU_API_KEY_FREE)
    """
    load_repo_env()

    key = cli_key.strip()
    if key:
        return key, "CLI"

    for var_name in ("ANU_API_KEY", "ANU_QRNG_API_KEY"):
        key = os.environ.get(var_name, "").strip()
        if key:
            return key, var_name

    tier = (preferred_tier or os.environ.get("ANU_API_KEY_MODE", "auto")).strip().lower()
    if tier not in {"auto", "paid", "free"}:
        tier = "auto"

    if tier == "paid":
        candidates = ("ANU_API_KEY_PAID", "ANU_API_KEY_FREE")
    elif tier == "free":
        candidates = ("ANU_API_KEY_FREE", "ANU_API_KEY_PAID")
    else:
        candidates = ("ANU_API_KEY_PAID", "ANU_API_KEY_FREE")

    for var_name in candidates:
        key = os.environ.get(var_name, "").strip()
        if key:
            return key, var_name

    for path in _candidate_key_files():
        key = _read_key_file(path)
        if key:
            return key, path.name

    return None, None


def _candidate_key_files() -> tuple[Path, ...]:
    cwd = Path.cwd()
    return (
        REPO_ROOT / "artifacts" / ".anu_api_key",
        cwd / "artifacts" / ".anu_api_key",
        cwd / ".anu_api_key",
    )


def _read_key_file(path: Path) -> str | None:
    try:
        key = path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return None
    if not key:
        return None
    return key
