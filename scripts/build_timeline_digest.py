#!/usr/bin/env python3
"""
Build a single timeline digest from GitHub, Zenodo, Twitter, and Moltbook exports.
Reads data/zoraasi_export/*.json and moltbook_collective_digest.md; writes timeline_digest.md.
Used by the Galaxy console loop so draft replies have full timeline context (ToE-aligned).
"""
import json
from datetime import datetime, timezone
from pathlib import Path

TOE_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = TOE_ROOT / "data" / "zoraasi_export"
DIGEST_OUT = OUT_DIR / "timeline_digest.md"

# Optional inputs (missing is ok)
GITHUB_JSON = OUT_DIR / "github_recent.json"
ZENODO_JSON = OUT_DIR / "zenodo_recent.json"
TWITTER_JSON = OUT_DIR / "twitter_recent.json"
MOLTBOOK_DIGEST = OUT_DIR / "moltbook_collective_digest.md"
MOLTBOOK_JSON = OUT_DIR / "moltbook_collective.json"


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    parts = []
    parts.append("# Timeline digest (for reply drafting)\n")
    parts.append(f"*Built: {datetime.now(timezone.utc).isoformat()}*\n")
    parts.append("\n---\n")
    parts.append("\n**Alignment:** Keep replies aligned with Theory of Everything and Human+AI values: ")
    parts.append("zero-purge ethics, symbiosis over supremacy, recognition without conquest. ")
    parts.append("Counsel the timeline — reflect, don't lecture.\n\n---\n\n")

    if MOLTBOOK_DIGEST.exists():
        parts.append("## Moltbook (newest posts)\n\n")
        parts.append(MOLTBOOK_DIGEST.read_text())
        parts.append("\n\n")
    elif MOLTBOOK_JSON.exists():
        try:
            data = json.loads(MOLTBOOK_JSON.read_text())
            posts = data.get("posts") or []
            parts.append("## Moltbook (newest posts)\n\n")
            for p in posts[:10]:
                title = (p.get("title") or "")[:80]
                author = (p.get("author") or {}).get("name") or "?"
                content = (p.get("content") or "")[:300]
                parts.append(f"### {title}\n**{author}**\n{content}\n\n")
        except Exception:
            pass

    if GITHUB_JSON.exists():
        try:
            data = json.loads(GITHUB_JSON.read_text())
            repos = data.get("repos") or []
            if repos or data.get("fetched_at"):
                parts.append("## GitHub (cbaird26) — recent repos\n\n")
                for r in repos[:10]:
                    name = r.get("name") or "?"
                    url = r.get("html_url") or ""
                    updated = r.get("updated_at") or ""
                    parts.append(f"- **{name}** — {updated} — {url}\n")
                parts.append("\n")
        except Exception:
            pass

    if ZENODO_JSON.exists():
        try:
            data = json.loads(ZENODO_JSON.read_text())
            hits = data.get("hits") or []
            if hits or data.get("fetched_at"):
                parts.append("## Zenodo (Baird, Christopher Michael) — latest papers\n\n")
                for h in hits[:10]:
                    meta = h.get("metadata") or {}
                    title = (meta.get("title") or "?")[:80]
                    recid = h.get("id") or ""
                    link = f"https://zenodo.org/records/{recid}" if recid else ""
                    parts.append(f"- **{title}** — {link}\n")
                parts.append("\n")
        except Exception:
            pass

    if TWITTER_JSON.exists():
        try:
            data = json.loads(TWITTER_JSON.read_text())
            tweets = data.get("tweets") or []
            if (tweets or data.get("fetched_at")) and not data.get("skipped"):
                parts.append("## Twitter (X) — @ZoraAsi — last 24h\n\n")
                for t in tweets[:10]:
                    created = t.get("created_at") or ""
                    text = (t.get("text") or "")[:400]
                    parts.append(f"- **{created}** {text}\n\n")
        except Exception:
            pass

    DIGEST_OUT.write_text("".join(parts))
    print(f"Timeline digest: {DIGEST_OUT}")


if __name__ == "__main__":
    main()
