#!/usr/bin/env bash
# Fetch recent Moltbook posts and write a collective digest (+ JSON for responder).
# Usage: ./scripts/moltbook_fetch_collective.sh [minutes_back]
# Default: 60 minutes. Output: data/zoraasi_export/moltbook_collective.json and .md

set -e
MINUTES_BACK="${1:-60}"
TOE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="${TOE_ROOT}/data/zoraasi_export"
JSON_OUT="${OUT_DIR}/moltbook_collective.json"
DIGEST_OUT="${OUT_DIR}/moltbook_collective_digest.md"
MOLTBOOK_SCRIPT="${MOLTBOOK_SCRIPT:-}"
if [[ -z "$MOLTBOOK_SCRIPT" ]]; then
  # Default: sibling repo path (adjust if you install the skill elsewhere)
  for candidate in \
    "$(dirname "$TOE_ROOT")/mqgt_scf_reissue_2026-01-20_010939UTC/skills/moltbook-interact/scripts/moltbook.sh" \
    "$HOME/.cursor/skills-cursor/moltbook-interact/scripts/moltbook.sh" \
    "/Users/christophermichaelbaird/Downloads/mqgt_scf_reissue_2026-01-20_010939UTC/skills/moltbook-interact/scripts/moltbook.sh"; do
    if [[ -x "$candidate" ]]; then MOLTBOOK_SCRIPT="$candidate"; break; fi
  done
fi
if [[ -z "$MOLTBOOK_SCRIPT" || ! -x "$MOLTBOOK_SCRIPT" ]]; then
  echo "Error: Moltbook script not found. Set MOLTBOOK_SCRIPT or install moltbook-interact skill."
  exit 1
fi

mkdir -p "$OUT_DIR"
echo "Fetching new posts (last ${MINUTES_BACK} min)..."
RAW="$("$MOLTBOOK_SCRIPT" new 50 2>/dev/null)" || { echo "Moltbook fetch failed."; exit 1; }

# Script may print "Fetching..." then JSON; keep only the JSON line(s)
TMP_RAW="${OUT_DIR}/.moltbook_raw.json"
echo "$RAW" | sed -n '/^{/p' | head -1 > "$TMP_RAW"
if [[ ! -s "$TMP_RAW" ]]; then
  echo "$RAW" > "$TMP_RAW"
fi

python3 - "$TMP_RAW" "$JSON_OUT" "$DIGEST_OUT" "$MINUTES_BACK" << 'PY'
import json, sys
from datetime import datetime, timezone, timedelta

raw_path, json_out, digest_out, minutes = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
with open(raw_path) as f:
    data = json.load(f)
posts = data.get("posts") or []
cutoff = datetime.now(timezone.utc) - timedelta(minutes=minutes)
recent = []
for p in posts:
    try:
        t = datetime.fromisoformat(p["created_at"].replace("Z", "+00:00"))
        if t >= cutoff:
            recent.append(p)
    except Exception:
        pass

with open(json_out, "w") as f:
    json.dump({"fetched_at": datetime.now(timezone.utc).isoformat(), "minutes_back": minutes, "posts": recent}, f, indent=2)

with open(digest_out, "w") as f:
    f.write("# Moltbook collective digest\n\n")
    f.write(f"*Fetched: {datetime.now(timezone.utc).isoformat()} — last {minutes} minutes*\n\n")
    for p in recent:
        author = (p.get("author") or {}).get("name") or "?"
        title = (p.get("title") or "").replace("\n", " ")
        content = (p.get("content") or "")[:500]
        if len((p.get("content") or "")) > 500:
            content += "..."
        f.write(f"## {title}\n")
        f.write(f"**{author}** — {p.get('created_at', '')}\n")
        f.write(f"`id`: `{p.get('id', '')}`\n\n")
        f.write(f"{content}\n\n---\n\n")
PY

rm -f "$TMP_RAW"
echo "Digest: $DIGEST_OUT ($(wc -l < "$DIGEST_OUT") lines)"
echo "Posts (last ${MINUTES_BACK} min): $(jq '.posts | length' "$JSON_OUT" 2>/dev/null || echo 0)"
