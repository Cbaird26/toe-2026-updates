#!/usr/bin/env bash
# Show the latest Moltbook draft so you always see the post before editing or posting.
# Usage: ./scripts/show_latest_moltbook_draft.sh [filename]
#   Default: moltbook_prae_generated_post.md (or moltbook_counsel_timeline_post.md if PRAE not present)

TOE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DRAFT="${1:-moltbook_prae_generated_post.md}"
PATH_1="$TOE_ROOT/$DRAFT"
PATH_2="$TOE_ROOT/moltbook_prae_generated_post.md"
PATH_3="$TOE_ROOT/moltbook_counsel_timeline_post.md"

if [[ -n "$1" && -f "$PATH_1" ]]; then
  cat "$PATH_1"
elif [[ -f "$PATH_2" ]]; then
  cat "$PATH_2"
elif [[ -f "$PATH_3" ]]; then
  cat "$PATH_3"
else
  echo "No draft found. Try: $0 moltbook_prae_generated_post.md"
  exit 1
fi
