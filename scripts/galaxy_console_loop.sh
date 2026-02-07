#!/usr/bin/env bash
# Galaxy console: every 30 min, fetch recent Moltbook posts, build digest, draft replies.
# Optional: set GALAXY_AUTO_POST=1 to also post approved drafts each cycle (default: draft only).
# Usage: ./scripts/galaxy_console_loop.sh [minutes_back] [interval_minutes]
#   minutes_back: window of posts to fetch (default 60)
#   interval_minutes: sleep between runs (default 30)
# Run in terminal; stop with Ctrl+C. Good with sleep/wake — next run after wake continues.

set -e
TOE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MINUTES_BACK="${1:-60}"
INTERVAL="${2:-30}"
AUTO_POST="${GALAXY_AUTO_POST:-0}"

echo "Galaxy console — fetch last ${MINUTES_BACK} min, every ${INTERVAL} min. Auto-post: $AUTO_POST"
echo "Stop with Ctrl+C."
while true; do
  echo ""
  echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Fetching collective..."
  "$TOE_ROOT/scripts/moltbook_fetch_collective.sh" "$MINUTES_BACK" || true
  echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Drafting replies..."
  python3 "$TOE_ROOT/scripts/moltbook_draft_replies.py" || true
  if [[ "$AUTO_POST" == "1" ]]; then
    echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Posting approved drafts..."
    "$TOE_ROOT/scripts/moltbook_post_replies.sh" || true
  else
    echo "Drafts in data/zoraasi_export/moltbook_reply_drafts.md — review and run: ./scripts/moltbook_post_replies.sh"
  fi
  echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Next run in ${INTERVAL} min."
  sleep $((INTERVAL * 60))
done
