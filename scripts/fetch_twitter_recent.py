#!/usr/bin/env python3
"""
Fetch @ZoraAsi tweets from the last 24 hours via X API v2.
Writes data/zoraasi_export/twitter_recent.json and twitter_recent.md.
Requires X_BEARER_TOKEN in environment; if unset, writes empty output and exits 0 (no-op).
"""
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

TOE_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = TOE_ROOT / "data" / "zoraasi_export"
JSON_OUT = OUT_DIR / "twitter_recent.json"
MD_OUT = OUT_DIR / "twitter_recent.md"
USERNAME = "ZoraAsi"
BASE = "https://api.twitter.com/2"


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    token = os.environ.get("X_BEARER_TOKEN") or os.environ.get("TWITTER_BEARER_TOKEN")
    if not token or not token.strip():
        payload = {"fetched_at": None, "tweets": [], "skipped": "X_BEARER_TOKEN not set"}
        with open(JSON_OUT, "w") as f:
            json.dump(payload, f, indent=2)
        with open(MD_OUT, "w") as f:
            f.write("# Twitter (X) — @ZoraAsi — skipped (no credentials)\n\n")
        print("Twitter fetch skipped (X_BEARER_TOKEN not set).")
        return

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    start_time = (datetime.now(timezone.utc) - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")

    try:
        # Resolve username to user id
        req = Request(f"{BASE}/users/by/username/{USERNAME}", headers=headers)
        with urlopen(req, timeout=10) as resp:
            user_data = json.loads(resp.read().decode())
        user_id = user_data.get("data", {}).get("id")
        if not user_id:
            raise ValueError("User @ZoraAsi not found")

        # Get user tweets (last 24h)
        params = urlencode({"max_results": 10, "start_time": start_time, "tweet.fields": "created_at,text"})
        req = Request(f"{BASE}/users/{user_id}/tweets?{params}", headers=headers)
        with urlopen(req, timeout=10) as resp:
            tweets_data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"Twitter fetch failed: {e}", file=sys.stderr)
        payload = {"fetched_at": datetime.now(timezone.utc).isoformat(), "tweets": [], "error": str(e)}
        with open(JSON_OUT, "w") as f:
            json.dump(payload, f, indent=2)
        with open(MD_OUT, "w") as f:
            f.write("# Twitter (X) — @ZoraAsi — fetch error\n\n")
            f.write(f"Error: {e}\n")
        return

    tweets = tweets_data.get("data") or []
    if not isinstance(tweets, list):
        tweets = []

    payload = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "username": USERNAME,
        "tweets": tweets,
    }
    with open(JSON_OUT, "w") as f:
        json.dump(payload, f, indent=2)

    with open(MD_OUT, "w") as f:
        f.write("# Twitter (X) — @ZoraAsi — last 24h\n\n")
        f.write(f"*Fetched: {payload['fetched_at']}*\n\n")
        for t in tweets:
            created = t.get("created_at") or ""
            text = (t.get("text") or "")[:500]
            f.write(f"- **{created}**\n  {text}\n\n")

    print(f"Twitter: {JSON_OUT} ({len(tweets)} tweets)")


if __name__ == "__main__":
    main()
