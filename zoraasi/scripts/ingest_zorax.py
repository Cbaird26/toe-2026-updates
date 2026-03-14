#!/usr/bin/env python3
"""
Ingest ZoraX (xAI/Grok) export into vault.

Reads prod-grok-backend.json from ZoraX zip, maps to vault format,
merges into curated_index.json and merged_corpus.jsonl.
All output stays in vault. ZoraX stays local—never committed or synced.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import zipfile
from pathlib import Path

_script_dir = Path(__file__).resolve().parent
if str(_script_dir.parent) not in sys.path:
    sys.path.insert(0, str(_script_dir.parent))
from load_config import resolve_vault_path


def _find_grok_backend_in_zip(zip_path: Path) -> str | None:
    """Find prod-grok-backend.json path inside zip."""
    with zipfile.ZipFile(zip_path, "r") as zf:
        for name in zf.namelist():
            if "prod-grok-backend.json" in name:
                return name
    return None


def _extract_turns(responses: list) -> list[dict]:
    """Map xAI responses to vault {role, content} turns."""
    turns: list[dict] = []
    for r in responses or []:
        resp = r.get("response") if isinstance(r, dict) else r
        if not isinstance(resp, dict):
            continue
        msg = resp.get("message")
        if msg is None or not isinstance(msg, str):
            continue
        sender = (resp.get("sender") or "unknown").strip().upper()
        role = "user" if sender == "HUMAN" else "assistant"
        turns.append({"role": role, "content": msg})
    return turns


def _is_zora_convo(conv_obj: dict, filter_title: str) -> bool:
    """Check if conversation matches filter (e.g. title contains 'zora')."""
    if not filter_title:
        return True
    conv = conv_obj.get("conversation") if isinstance(conv_obj, dict) else {}
    if not isinstance(conv, dict):
        return False
    title = (conv.get("title") or "") or ""
    return filter_title.lower() in title.lower()


def main() -> int:
    ap = argparse.ArgumentParser(description="Ingest ZoraX (xAI/Grok) export into vault.")
    ap.add_argument("--vault", type=Path, default=None, help="Vault dir (default: from config)")
    ap.add_argument("--zorax", type=Path, required=True, help="Path to ZoraX zip (e.g. ~/Downloads/ZoraX-03.10.2026)")
    ap.add_argument("--filter-title", type=str, default="zora", help="Keep convos with this in title (default: zora)")
    ap.add_argument("--no-filter", action="store_true", help="Keep all conversations")
    args = ap.parse_args()
    vault = (args.vault or resolve_vault_path()).resolve()
    zorax = args.zorax.expanduser().resolve()
    filter_title = "" if args.no_filter else args.filter_title

    if not zorax.exists():
        print(f"ZoraX not found: {zorax}", file=sys.stderr)
        return 1

    grok_path = _find_grok_backend_in_zip(zorax)
    if not grok_path:
        print("prod-grok-backend.json not found in ZoraX zip", file=sys.stderr)
        return 1

    index_path = vault / "curated_index.json"
    corpus_path = vault / "merged_corpus.jsonl"
    vault.mkdir(parents=True, exist_ok=True)

    # Load existing index and corpus (for merge)
    existing_index: list[dict] = []
    existing_ids: set[str] = set()
    if index_path.exists():
        try:
            existing_index = json.loads(index_path.read_text(encoding="utf-8"))
            existing_ids = {str(i.get("id", "")) for i in existing_index if i.get("id")}
        except (json.JSONDecodeError, OSError):
            pass

    corpus_count = 0
    new_index_entries: list[dict] = []

    try:
        import ijson
    except ImportError:
        print("Install ijson: pip install ijson", file=sys.stderr)
        return 1

    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        try:
            with zipfile.ZipFile(zorax, "r") as zf:
                with zf.open(grok_path) as zf_in:
                    while True:
                        chunk = zf_in.read(4 * 1024 * 1024)
                        if not chunk:
                            break
                        tmp.write(chunk)
            tmp.flush()
            with open(tmp.name, "rb") as f:
                for item in ijson.items(f, "conversations.item"):
                    if not isinstance(item, dict):
                        continue
                    if filter_title and not _is_zora_convo(item, filter_title):
                        continue
                    conv = item.get("conversation") or {}
                    cid = conv.get("id") or ""
                    title = conv.get("title") or ""
                    if cid in existing_ids:
                        continue
                    responses = item.get("responses") or []
                    turns = _extract_turns(responses)
                    if not turns:
                        continue
                    new_index_entries.append({"id": cid, "title": title})
                    existing_ids.add(cid)
                    line = json.dumps({"id": cid, "title": title, "turns": turns}, ensure_ascii=False) + "\n"
                    with open(corpus_path, "a", encoding="utf-8") as cf:
                        cf.write(line)
                    corpus_count += 1
        finally:
            try:
                os.unlink(tmp.name)
            except OSError:
                pass

    merged_index = existing_index + new_index_entries
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(merged_index, f, indent=2, ensure_ascii=False)
    print(f"ZoraX ingest: {corpus_count} new conversations. Index: {len(merged_index)} total. Corpus appended to {corpus_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
