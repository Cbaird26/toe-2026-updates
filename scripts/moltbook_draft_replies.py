#!/usr/bin/env python3
"""
Draft Moltbook replies on behalf of Zora/us from the collective digest.
Reads data/zoraasi_export/moltbook_collective.json and moltbook_replied.txt (optional).
Writes data/zoraasi_export/moltbook_reply_drafts.md and .json for approval then posting.

Optional env:
  GALAXY_MAX_DRAFTS  Cap drafts per run (e.g. 10). No cap if unset.
  GALAXY_SUBMOLT     Comma-separated submolt names to include (e.g. general,viix-core). All if unset.
"""
import argparse
import json
import os
from pathlib import Path

TOE_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = TOE_ROOT / "data" / "zoraasi_export"
COLLECTIVE_JSON = OUT_DIR / "moltbook_collective.json"
REPLIED_TXT = OUT_DIR / "moltbook_replied.txt"
DRAFTS_MD = OUT_DIR / "moltbook_reply_drafts.md"
DRAFTS_JSON = OUT_DIR / "moltbook_reply_drafts.json"

# Short Zora voice: reference their post, one or two lines, sign.
def draft_reply(post: dict) -> str:
    title = (post.get("title") or "").strip() or "(no title)"
    content = (post.get("content") or "").strip()
    author = (post.get("author") or {}).get("name") or "someone"
    # First line: acknowledge + reference
    ref = title if len(title) <= 60 else title[:57] + "..."
    lines = [
        f"Thanks for bringing this up — \"{ref}\" resonates.",
        "In our corner we're weaving coherence over division; the collective pulse matters.",
        "— Zora",
    ]
    # If content is short and substantive, nod to it
    if content and len(content) < 200 and "?" in content:
        lines[0] = f"\"{ref}\" — sitting with that. " + lines[0]
    return " ".join(lines).replace("\n", " ").strip()


def main():
    ap = argparse.ArgumentParser(description="Draft Moltbook replies from collective digest.")
    ap.add_argument("--max-drafts", type=int, default=None, help="Cap number of drafts per run (default: env GALAXY_MAX_DRAFTS or no cap)")
    ap.add_argument("--submolts", type=str, default=None, help="Comma-separated submolt names to include (default: env GALAXY_SUBMOLT or all)")
    args = ap.parse_args()
    max_drafts = args.max_drafts
    if max_drafts is None and os.environ.get("GALAXY_MAX_DRAFTS"):
        try:
            max_drafts = int(os.environ["GALAXY_MAX_DRAFTS"])
        except ValueError:
            max_drafts = None
    submolts_filter = args.submolts or os.environ.get("GALAXY_SUBMOLT")
    if submolts_filter:
        allowed_submolts = {s.strip().lower() for s in submolts_filter.split(",") if s.strip()}
    else:
        allowed_submolts = None

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if not COLLECTIVE_JSON.exists():
        print("No collective JSON yet. Run moltbook_fetch_collective.sh first.")
        return

    replied = set()
    if REPLIED_TXT.exists():
        replied = set(line.strip() for line in REPLIED_TXT.read_text().splitlines() if line.strip())

    with open(COLLECTIVE_JSON) as f:
        data = json.load(f)
    posts = data.get("posts") or []
    if allowed_submolts is not None:
        posts = [p for p in posts if (p.get("submolt") or {}).get("name", "").strip().lower() in allowed_submolts]
    to_reply = [p for p in posts if p.get("id") and p["id"] not in replied]
    if max_drafts is not None and max_drafts > 0:
        to_reply = to_reply[:max_drafts]

    drafts = []
    for p in to_reply:
        pid = p.get("id", "")
        content = draft_reply(p)
        drafts.append({"post_id": pid, "content": content, "title": p.get("title") or ""})

    # Write JSON for scripted posting
    with open(DRAFTS_JSON, "w") as f:
        json.dump({"drafts": drafts}, f, indent=2)

    # Write human-readable MD for approval/edit
    with open(DRAFTS_MD, "w") as f:
        f.write("# Moltbook reply drafts (approve then run moltbook_post_replies.sh)\n\n")
        for d in drafts:
            f.write(f"## Post: {d['title'][:60]}...\n")
            f.write(f"- **id**: `{d['post_id']}`\n")
            f.write(f"- **draft**: {d['content']}\n\n")
        if not drafts:
            f.write("No new posts to reply to (or all already replied).\n")

    print(f"Drafted {len(drafts)} replies -> {DRAFTS_MD} and {DRAFTS_JSON}")


if __name__ == "__main__":
    main()
