"""
Shared config loader for ZoraASI.
Precedence: env > config.yaml > defaults.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any


def _toe_root() -> Path:
    """TOE repo root (parent of zoraasi/)."""
    return Path(__file__).resolve().parent.parent


def _config_path() -> Path:
    return Path(__file__).resolve().parent / "config.yaml"


def load_config() -> dict[str, Any]:
    """Load config.yaml with env overrides. Returns merged config dict."""
    defaults = {
        "vault_path": "",
        "knowledge_base_path": "",
        "backend": "ollama",
        "model": "llama3.2",
        "ollama_host": "http://localhost:11434",
        "embed_model": "nomic-embed-text",
        "port": 5050,
        "rag_top_k": 5,
        "ip_framework": {
            "lexicon_path": "docs/IP/LEGAL_LEXICON.md",
            "enable_ip_context": False,
        },
    }
    cfg_path = _config_path()
    if not cfg_path.exists():
        cfg = {}
    else:
        try:
            import yaml
            with open(cfg_path, encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
        except Exception:
            cfg = {}

    out = {**defaults, **{k: v for k, v in cfg.items() if k != "ip_framework"}}
    out["ip_framework"] = {**defaults["ip_framework"], **(cfg.get("ip_framework") or {})}

    # Env overrides
    if os.environ.get("VAULT_PATH"):
        out["vault_path"] = os.environ["VAULT_PATH"]
    if os.environ.get("KNOWLEDGE_BASE_PATH"):
        out["knowledge_base_path"] = os.environ["KNOWLEDGE_BASE_PATH"]
    if os.environ.get("ZORAASI_BACKEND"):
        out["backend"] = os.environ["ZORAASI_BACKEND"]
    if os.environ.get("ZORAASI_MODEL"):
        out["model"] = os.environ["ZORAASI_MODEL"]
    if os.environ.get("OLLAMA_HOST"):
        out["ollama_host"] = os.environ["OLLAMA_HOST"]
    if os.environ.get("PORT"):
        try:
            out["port"] = int(os.environ["PORT"])
        except ValueError:
            pass

    return out


def resolve_vault_path(override: Path | str | None = None) -> Path:
    """Resolve vault path: override > VAULT_PATH env > config > default."""
    if override:
        return Path(override)
    cfg = load_config()
    v = cfg.get("vault_path") or os.environ.get("VAULT_PATH")
    if v:
        return Path(v)
    return _toe_root() / "data" / "zoraasi_export"


def resolve_knowledge_base_path(override: Path | str | None = None) -> Path:
    """Resolve knowledge base path: override > KNOWLEDGE_BASE_PATH env > config > default."""
    if override:
        return Path(override)
    cfg = load_config()
    kb = cfg.get("knowledge_base_path") or os.environ.get("KNOWLEDGE_BASE_PATH")
    if kb:
        return Path(kb)
    return Path.home() / "Downloads" / "KNOWLEDGE BASE"
