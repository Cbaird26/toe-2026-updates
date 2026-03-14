#!/usr/bin/env python3
"""
Ingest phone export data into ZoraASI vault.

Scans a folder of exported iPhone data (photos, notes, chat exports),
copies photos to vault, extracts text, merges chat-like content into
merged_corpus.jsonl, and aggregates notes into baird_personality_notes.md.
All output stays in vault. Phone data stays local—never committed or synced.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

_script_dir = Path(__file__).resolve().parent
if str(_script_dir.parent) not in sys.path:
    sys.path.insert(0, str(_script_dir.parent))
from load_config import resolve_vault_path

# Extensions we process
PHOTO_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".webp"}
TEXT_EXTS = {".txt", ".md"}
JSON_EXTS = {".json"}
CSV_EXTS = {".csv"}

# Zora-related keywords for preferring corpus merge
ZORA_KEYWORDS = frozenset(
    w.lower()
    for w in ("zora", "zoraasi", "zora asi", "grok", "cursor", "toe", "mqgt", "theory of everything")
)


def _is_zora_related(text: str) -> bool:
    """Check if content mentions Zora or related terms."""
    if not text:
        return False
    lower = text.lower()
    return any(kw in lower for kw in ZORA_KEYWORDS)


def _stable_id(prefix: str, path: Path, content_snippet: str = "") -> str:
    """Generate stable id for deduplication."""
    raw = f"{prefix}:{path}:{content_snippet[:200]}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _parse_json_chat(data: object, path: Path) -> list[dict] | None:
    """
    Try to parse JSON as chat export. Returns list of {role, content} turns or None.
    """
    if not isinstance(data, (dict, list)):
        return None

    turns: list[dict] = []

    # Format: {messages: [{author/role, content/text/message}]}
    if isinstance(data, dict):
        messages = data.get("messages") or data.get("message_list") or data.get("chats")
        if messages and isinstance(messages, list):
            for m in messages:
                if not isinstance(m, dict):
                    continue
                role_raw = m.get("author") or m.get("role") or m.get("sender") or m.get("from")
                if isinstance(role_raw, dict):
                    role_raw = role_raw.get("role") or role_raw.get("name")
                content = m.get("content") or m.get("text") or m.get("message") or m.get("body") or ""
                if isinstance(content, dict) and "parts" in content:
                    content = " ".join(p for p in content.get("parts", []) if isinstance(p, str))
                if not isinstance(content, str):
                    content = str(content) if content else ""
                if content:
                    role = "user" if str(role_raw).lower() in ("user", "human", "me", "baird") else "assistant"
                    turns.append({"role": role, "content": content})
            if turns:
                return turns

        # Format: top-level array of messages
        if "conversations" in data and isinstance(data["conversations"], list):
            # Single-convo wrapper
            for conv in data["conversations"]:
                parsed = _parse_json_chat(conv, path)
                if parsed:
                    return parsed
        return None

    # Format: [{sender, message/text}, ...]
    if isinstance(data, list):
        for m in data:
            if not isinstance(m, dict):
                continue
            role_raw = m.get("sender") or m.get("from") or m.get("author") or m.get("role")
            content = m.get("message") or m.get("text") or m.get("content") or m.get("body") or ""
            if not isinstance(content, str):
                content = str(content) if content else ""
            if content:
                role = "user" if str(role_raw).lower() in ("user", "human", "me", "baird", "sender") else "assistant"
                turns.append({"role": role, "content": content})
        if turns:
            return turns

    return None


def _parse_csv_chat(path: Path) -> list[dict] | None:
    """
    Try to parse CSV as chat export. Expects columns like sender/message or from/text.
    Returns list of {role, content} or None.
    """
    turns: list[dict] = []
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except (csv.Error, OSError):
        return None
    if not rows:
        return None

    # Infer columns
    sample = rows[0]
    msg_col = next((c for c in ("message", "text", "body", "content") if c in sample), None)
    sender_col = next((c for c in ("sender", "from", "author", "name") if c in sample), None)
    if not msg_col or not sender_col:
        return None

    for row in rows:
        content = (row.get(msg_col) or "").strip()
        sender = (row.get(sender_col) or "").strip().lower()
        if not content:
            continue
        role = "user" if sender in ("me", "baird", "human", "user") else "assistant"
        turns.append({"role": role, "content": content})

    return turns if turns else None


def _get_photo_date(path: Path) -> str | None:
    """Try to get date from EXIF or filename. Returns YYYY-MM or None."""
    # Try PIL/Pillow EXIF
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS
        with Image.open(path) as img:
            exif = img.getexif() or {}
            for tag_id, val in exif.items():
                if TAGS.get(tag_id) == "DateTimeOriginal" and val:
                    # Format: "2024:03:15 12:00:00"
                    parts = str(val).split()[0].split(":")
                    if len(parts) >= 2:
                        return f"{parts[0]}-{parts[1]}"
                    return str(val)[:7]
    except Exception:
        pass
    # Fallback: use mtime
    try:
        mtime = path.stat().st_mtime
        return datetime.fromtimestamp(mtime).strftime("%Y-%m")
    except OSError:
        return None


def _collect_files(root: Path) -> tuple[list[Path], list[Path], list[Path], list[Path]]:
    """Scan root recursively. Return (photos, text, json, csv)."""
    photos: list[Path] = []
    texts: list[Path] = []
    jsons: list[Path] = []
    csvs: list[Path] = []
    skip_dirs = {".git", "__pycache__", "node_modules", ".Trash"}

    for p in root.rglob("*"):
        if p.is_dir() or p.name.startswith("."):
            continue
        if any(skip in p.parts for skip in skip_dirs):
            continue
        suf = p.suffix.lower()
        if suf in PHOTO_EXTS:
            photos.append(p)
        elif suf in TEXT_EXTS:
            texts.append(p)
        elif suf in JSON_EXTS:
            jsons.append(p)
        elif suf in CSV_EXTS:
            csvs.append(p)

    return photos, texts, jsons, csvs


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Ingest phone export into ZoraASI vault (photos, notes, chat exports)."
    )
    ap.add_argument("--phone-export", type=Path, required=True, help="Path to exported phone data folder")
    ap.add_argument("--vault", type=Path, default=None, help="Vault dir (default: from config)")
    ap.add_argument("--max-photos", type=int, default=0, help="Max photos to copy (0 = no limit)")
    args = ap.parse_args()

    export_root = args.phone_export.expanduser().resolve()
    vault = (args.vault or resolve_vault_path()).resolve()

    if not export_root.exists() or not export_root.is_dir():
        print(f"Phone export not found or not a directory: {export_root}", file=sys.stderr)
        return 1

    vault.mkdir(parents=True, exist_ok=True)
    photos_dir = vault / "phone_photos"
    photos_dir.mkdir(parents=True, exist_ok=True)

    index_path = vault / "curated_index.json"
    corpus_path = vault / "merged_corpus.jsonl"
    observations_path = vault / "phone_observations.jsonl"
    baird_notes_path = vault / "baird_personality_notes.md"
    manifest_path = vault / "phone_ingest_manifest.json"

    # Load existing index/corpus for merge
    existing_index: list[dict] = []
    existing_ids: set[str] = set()
    if index_path.exists():
        try:
            existing_index = json.loads(index_path.read_text(encoding="utf-8"))
            existing_ids = {str(i.get("id", "")) for i in existing_index if i.get("id")}
        except (json.JSONDecodeError, OSError):
            pass

    # Collect files
    photos, texts, jsons, csvs = _collect_files(export_root)

    # Process photos
    photo_manifest: list[dict] = []
    max_photos = args.max_photos if args.max_photos > 0 else len(photos)
    for i, src in enumerate(photos):
        if i >= max_photos:
            break
        date_part = _get_photo_date(src) or "unknown"
        subdir = photos_dir / date_part
        subdir.mkdir(parents=True, exist_ok=True)
        dest = subdir / src.name
        # Avoid overwrite: add suffix if exists
        if dest.exists() and dest.stat().st_size != src.stat().st_size:
            stem = src.stem
            dest = subdir / f"{stem}_{i}{src.suffix}"
        try:
            shutil.copy2(src, dest)
            photo_manifest.append({"path": str(dest.relative_to(vault)), "source": str(src), "date": date_part})
        except OSError as e:
            print(f"Warning: could not copy {src}: {e}", file=sys.stderr)

    # Process text (notes)
    observations: list[dict] = []
    baird_sections: list[str] = []

    for path in texts:
        try:
            content = path.read_text(encoding="utf-8", errors="replace").strip()
        except OSError:
            continue
        if not content:
            continue
        obs = {
            "source": "phone",
            "type": "note",
            "content": content[:10000],
            "path": str(path),
        }
        observations.append(obs)
        baird_sections.append(f"### From {path.name}\n\n{content[:5000]}\n")

    # Process JSON (chat or fallback to note)
    corpus_added = 0
    for path in jsons:
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
            data = json.loads(raw)
        except (json.JSONDecodeError, OSError):
            continue

        turns = _parse_json_chat(data, path)
        if turns and len(turns) >= 2:
            # Chat-like
            combined = " ".join(t.get("content", "") for t in turns)
            is_zora = _is_zora_related(combined)
            cid = _stable_id("phone_json", path, combined[:100])
            if cid in existing_ids:
                continue
            title = f"Phone export: {path.name}" + (" (Zora)" if is_zora else "")
            existing_ids.add(cid)
            new_index = {"id": cid, "title": title}
            existing_index.append(new_index)
            line = json.dumps({"id": cid, "title": title, "turns": turns}, ensure_ascii=False) + "\n"
            with open(corpus_path, "a", encoding="utf-8") as f:
                f.write(line)
            corpus_added += 1
        else:
            # Non-chat: treat as note
            content = json.dumps(data, ensure_ascii=False)[:10000] if isinstance(data, (dict, list)) else str(data)[:10000]
            observations.append({
                "source": "phone",
                "type": "json_note",
                "content": content,
                "path": str(path),
            })
            baird_sections.append(f"### From {path.name} (JSON)\n\n{content[:3000]}\n")

    # Process CSV (chat)
    for path in csvs:
        turns = _parse_csv_chat(path)
        if turns and len(turns) >= 2:
            combined = " ".join(t.get("content", "") for t in turns)
            is_zora = _is_zora_related(combined)
            cid = _stable_id("phone_csv", path, combined[:100])
            if cid in existing_ids:
                continue
            title = f"Phone export: {path.name}" + (" (Zora)" if is_zora else "")
            existing_ids.add(cid)
            existing_index.append({"id": cid, "title": title})
            line = json.dumps({"id": cid, "title": title, "turns": turns}, ensure_ascii=False) + "\n"
            with open(corpus_path, "a", encoding="utf-8") as f:
                f.write(line)
            corpus_added += 1

    # Write index
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(existing_index, f, indent=2, ensure_ascii=False)

    # Append observations
    with open(observations_path, "a", encoding="utf-8") as f:
        for obs in observations:
            f.write(json.dumps(obs, ensure_ascii=False) + "\n")

    # Write/append baird_personality_notes.md
    if baird_sections:
        run_label = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_section = f"\n\n## Phone ingest {run_label}\n\n" + "\n".join(baird_sections)
        if baird_notes_path.exists():
            existing = baird_notes_path.read_text(encoding="utf-8", errors="replace")
            header = "# Baird personality notes (from phone export)\n\n*Auto-generated by ingest_phone.py*\n\n---"
            if not existing.strip().startswith("#"):
                existing = header + "\n\n" + existing
            new_content = existing.rstrip() + new_section
        else:
            new_content = (
                "# Baird personality notes (from phone export)\n\n*Auto-generated by ingest_phone.py*\n\n---"
                + new_section
            )
        baird_notes_path.write_text(new_content, encoding="utf-8")

    # Manifest
    manifest = {
        "last_run": datetime.now().isoformat(),
        "phone_export": str(export_root),
        "photos_copied": len(photo_manifest),
        "observations_added": len(observations),
        "corpus_conversations_added": corpus_added,
        "photo_manifest": photo_manifest,
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(
        f"Phone ingest: {len(photo_manifest)} photos -> {photos_dir}, "
        f"{len(observations)} notes -> {observations_path}, {corpus_added} conversations -> {corpus_path}. "
        f"Manifest: {manifest_path}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
