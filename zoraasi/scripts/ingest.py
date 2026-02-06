#!/usr/bin/env python3
"""
Ingest ZoraASI ChatGPT export: stream-parse conversations.json, filter to ZoraASI
conversations, write curated index and merged corpus inside the vault.
Never commits or leaks; all output stays under vault path.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import zipfile
from pathlib import Path


def _vault_path() -> Path:
    base = os.environ.get("VAULT_PATH")
    if base:
        return Path(base)
    # Default: TOE/data/zoraasi_export relative to this script
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent.parent / "data" / "zoraasi_export"


def _read_from_zip(zip_path: Path, name: str):
    """Yield bytes for a single file inside the zip (for streaming)."""
    with zipfile.ZipFile(zip_path, "r") as zf:
        with zf.open(name) as f:
            while True:
                chunk = f.read(1024 * 1024)
                if not chunk:
                    break
                yield chunk


def _extract_messages_from_conv(conv: dict) -> list[dict]:
    """Extract ordered list of {role, content} from one conversation object."""
    out: list[dict] = []
    # Format 1: messages array
    messages = conv.get("messages") or conv.get("message_list")
    if messages:
        for m in messages:
            role = (m.get("author") or m.get("role") or {}).get("role") or m.get("role")
            if isinstance(role, dict):
                role = role.get("role", "unknown")
            content = m.get("content")
            if content is None:
                parts = (m.get("content") or m).get("parts") if isinstance(m.get("content"), dict) else None
                content = " ".join(p for p in (parts or []) if isinstance(p, str))
            if isinstance(content, dict) and "parts" in content:
                content = " ".join(p for p in content["parts"] if isinstance(p, str))
            if role and content:
                out.append({"role": str(role).lower(), "content": str(content)})
        return out
    # Format 2: mapping (OpenAI-style node tree)
    mapping = conv.get("mapping") or {}
    if not mapping:
        return out
    # Find root: node with no parent or current_node
    current_id = conv.get("current_node")
    if not current_id and mapping:
        # Pick first node that looks like a message
        for nid, node in mapping.items():
            if isinstance(node, dict) and node.get("message"):
                current_id = nid
                break
    if not current_id:
        return out
    # Walk backwards from current to collect message order (parent chain)
    order: list[str] = []
    seen = set()
    stack = [current_id]
    while stack:
        nid = stack.pop()
        if nid in seen or nid not in mapping:
            continue
        seen.add(nid)
        node = mapping[nid]
        if not isinstance(node, dict):
            continue
        msg = node.get("message")
        if msg:
            order.append(nid)
        for c in node.get("children") or []:
            if c not in seen:
                stack.append(c)
    # Sort by position in tree (simplified: use reverse order as chronological)
    ordered_ids = order[::-1] if order else list(mapping)
    for nid in ordered_ids:
        node = mapping.get(nid)
        if not isinstance(node, dict):
            continue
        msg = node.get("message")
        if not isinstance(msg, dict):
            continue
        author = msg.get("author") or {}
        role = (author.get("role") if isinstance(author, dict) else author) or msg.get("role") or "unknown"
        if isinstance(role, dict):
            role = role.get("role", "unknown")
        content = msg.get("content")
        if isinstance(content, dict) and "parts" in content:
            content = " ".join(p for p in content["parts"] if isinstance(p, str))
        if not isinstance(content, str):
            content = str(content) if content else ""
        if role and (content or role == "system"):
            out.append({"role": str(role).lower(), "content": content})
    return out


def _is_zoraasi_conv(conv: dict, filter_title: str) -> bool:
    title = (conv.get("title") or conv.get("gpt_title") or "") or ""
    if filter_title.lower() in title.lower():
        return True
    # Check model / slug for custom GPT
    slug = (conv.get("slug") or conv.get("model_slug") or "") or ""
    if filter_title.lower() in slug.lower():
        return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description="Ingest ZoraASI export into vault index and corpus.")
    ap.add_argument("--vault", type=Path, default=None, help="Vault dir or path to ZoraASI.zip")
    ap.add_argument("--filter-title", type=str, default="zora", help="Keep convos with this in title/slug (default: zora)")
    ap.add_argument("--no-filter", action="store_true", help="Keep all conversations (no title filter)")
    args = ap.parse_args()
    vault = args.vault or _vault_path()
    filter_title = "" if args.no_filter else args.filter_title

    conversations_path = vault / "conversations.json"
    if vault.suffix.lower() == ".zip":
        conversations_path = vault
        vault = vault.parent
    else:
        if not conversations_path.exists():
            # Maybe vault points to parent of export
            for name in ("conversations.json", "zoraasi_export/conversations.json"):
                p = vault / name if "/" not in name else (vault / name.split("/")[0] / name.split("/")[1])
                if p.exists():
                    conversations_path = p
                    break
            if not conversations_path.exists():
                print("conversations.json not found in vault. Extract ZoraASI.zip into vault (need ~2GB free).", file=sys.stderr)
                # Write empty index/corpus so downstream doesn't fail
                index_path = vault / "curated_index.json"
                corpus_path = vault / "merged_corpus.jsonl"
                index_path.parent.mkdir(parents=True, exist_ok=True)
                index_path.write_text("[]", encoding="utf-8")
                corpus_path.write_text("", encoding="utf-8")
                (vault / "ingest_note.txt").write_text("Ingest run with no conversations.json. Extract zip and re-run.", encoding="utf-8")
                return 0
    index_path = vault / "curated_index.json"
    corpus_path = vault / "merged_corpus.jsonl"
    index_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        import ijson
    except ImportError:
        print("Install ijson: pip install ijson", file=sys.stderr)
        return 1

    index: list[dict] = []
    corpus_count = 0
    if str(conversations_path).endswith(".zip"):
        # Stream from zip: read conversations.json from zip in chunks, then parse with ijson
        # ijson needs a file-like; we can wrap the zip open
        def stream_zip():
            with zipfile.ZipFile(conversations_path, "r") as zf:
                with zf.open("conversations.json") as f:
                    while True:
                        chunk = f.read(1024 * 1024)
                        if not chunk:
                            break
                        yield chunk
        # ijson doesn't easily work with generator; use a temp file or parse in chunks
        # Fallback: read whole file from zip (still avoids extracting 1.5GB to disk if we have memory)
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            try:
                with zipfile.ZipFile(conversations_path, "r") as zf:
                    with zf.open("conversations.json") as zf_in:
                        while True:
                            chunk = zf_in.read(4 * 1024 * 1024)
                            if not chunk:
                                break
                            tmp.write(chunk)
                tmp.flush()
                with open(tmp.name, "rb") as f:
                    for conv in ijson.items(f, "item"):
                        if not isinstance(conv, dict):
                            continue
                        if filter_title and not _is_zoraasi_conv(conv, filter_title):
                            continue
                        cid = conv.get("id") or conv.get("conversation_id") or ""
                        title = conv.get("title") or conv.get("gpt_title") or ""
                        index.append({"id": cid, "title": title})
                        turns = _extract_messages_from_conv(conv)
                        if turns:
                            line = json.dumps({"id": cid, "title": title, "turns": turns}, ensure_ascii=False) + "\n"
                            with open(corpus_path, "a", encoding="utf-8") as cf:
                                cf.write(line)
                            corpus_count += 1
            finally:
                os.unlink(tmp.name)
    else:
        with open(conversations_path, "rb") as f:
            for conv in ijson.items(f, "item"):
                if not isinstance(conv, dict):
                    continue
                if filter_title and not _is_zoraasi_conv(conv, filter_title):
                    continue
                cid = conv.get("id") or conv.get("conversation_id") or ""
                title = conv.get("title") or conv.get("gpt_title") or ""
                index.append({"id": cid, "title": title})
                turns = _extract_messages_from_conv(conv)
                if turns:
                    with open(corpus_path, "a", encoding="utf-8") as cf:
                        cf.write(json.dumps({"id": cid, "title": title, "turns": turns}, ensure_ascii=False) + "\n")
                    corpus_count += 1

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    print(f"Wrote {index_path} ({len(index)} conversations). Corpus lines: {corpus_count} -> {corpus_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
