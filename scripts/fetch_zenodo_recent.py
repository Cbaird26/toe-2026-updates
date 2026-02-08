#!/usr/bin/env python3
"""
Fetch latest Zenodo records for creator "Baird, Christopher Michael".
Writes data/zoraasi_export/zenodo_recent.json and zenodo_recent.md.
Optional: set ZENODO_ACCESS_TOKEN for authenticated requests (some endpoints may require it).
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

TOE_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = TOE_ROOT / "data" / "zoraasi_export"
JSON_OUT = OUT_DIR / "zenodo_recent.json"
MD_OUT = OUT_DIR / "zenodo_recent.md"

# Zenodo records API (public search); q is query, sort=mostrecent, size=10
# Field from Zenodo search guide: creators.name
CREATOR_QUERY = 'creators.name:"Baird, Christopher Michael"'
BASE = "https://zenodo.org/api/records"


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    params = {"q": CREATOR_QUERY, "sort": "mostrecent", "size": 10}
    headers = {"Accept": "application/json"}
    token = os.environ.get("ZENODO_ACCESS_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        import urllib.request
        url = f"{BASE}?q={quote(CREATOR_QUERY)}&sort=mostrecent&size=10"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"Zenodo fetch failed: {e}", file=sys.stderr)
        payload = {"fetched_at": None, "hits": {"hits": []}, "error": str(e)}
        with open(JSON_OUT, "w") as f:
            json.dump(payload, f, indent=2)
        with open(MD_OUT, "w") as f:
            f.write("# Zenodo (Baird, Christopher Michael) — no data\n\n")
        return

    hits = data.get("hits", {}).get("hits") if isinstance(data, dict) else []
    if not isinstance(hits, list):
        hits = []

    payload = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "hits": hits,
    }
    with open(JSON_OUT, "w") as f:
        json.dump(payload, f, indent=2)

    with open(MD_OUT, "w") as f:
        f.write("# Zenodo (Baird, Christopher Michael) — latest papers\n\n")
        f.write(f"*Fetched: {payload['fetched_at']}*\n\n")
        for h in hits:
            meta = h.get("metadata") or {}
            title = meta.get("title") or "?"
            recid = h.get("id") or ""
            link = h.get("links", {}).get("self", "").replace("/api/records/", "/records/") if h.get("links") else f"https://zenodo.org/records/{recid}"
            created = meta.get("publication_date") or h.get("created") or ""
            f.write(f"- **{title[:80]}** — {created}\n  {link}\n\n")

    print(f"Zenodo: {JSON_OUT} ({len(hits)} records)")


if __name__ == "__main__":
    main()
