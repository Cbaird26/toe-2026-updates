#!/usr/bin/env bash
# Post approved reply drafts to Moltbook and record replied IDs.
# Usage: ./scripts/moltbook_post_replies.sh [path_to_drafts.json]
# Default: data/zoraasi_export/moltbook_reply_drafts.json
# Each draft must have post_id and content. After posting, appends post_id to moltbook_replied.txt.

set -e
TOE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="${TOE_ROOT}/data/zoraasi_export"
DRAFTS_JSON="${1:-${OUT_DIR}/moltbook_reply_drafts.json}"
REPLIED_TXT="${OUT_DIR}/moltbook_replied.txt"
MOLTBOOK_SCRIPT="${MOLTBOOK_SCRIPT:-}"
if [[ -z "$MOLTBOOK_SCRIPT" ]]; then
  for candidate in \
    "$(dirname "$TOE_ROOT")/mqgt_scf_reissue_2026-01-20_010939UTC/skills/moltbook-interact/scripts/moltbook.sh" \
    "$HOME/.cursor/skills-cursor/moltbook-interact/scripts/moltbook.sh" \
    "/Users/christophermichaelbaird/Downloads/mqgt_scf_reissue_2026-01-20_010939UTC/skills/moltbook-interact/scripts/moltbook.sh"; do
    if [[ -x "$candidate" ]]; then MOLTBOOK_SCRIPT="$candidate"; break; fi
  done
fi
if [[ -z "$MOLTBOOK_SCRIPT" || ! -x "$MOLTBOOK_SCRIPT" ]]; then
  echo "Error: Moltbook script not found. Set MOLTBOOK_SCRIPT."
  exit 1
fi

if [[ ! -f "$DRAFTS_JSON" ]]; then
  echo "No drafts file: $DRAFTS_JSON"
  exit 1
fi

count=0
for row in $(jq -c '.drafts[]?' "$DRAFTS_JSON" 2>/dev/null); do
  post_id=$(echo "$row" | jq -r '.post_id // empty')
  content=$(echo "$row" | jq -r '.content // empty')
  if [[ -z "$post_id" || -z "$content" ]]; then continue; fi
  tmp_content="${OUT_DIR}/.reply_content_$$"
  printf '%s' "$content" > "$tmp_content"
  "$MOLTBOOK_SCRIPT" reply "$post_id" "@${tmp_content}" || true
  rm -f "$tmp_content"
  echo "$post_id" >> "$REPLIED_TXT"
  count=$((count + 1))
  echo "Posted reply to $post_id"
done
echo "Posted $count replies. Replied IDs appended to $REPLIED_TXT"
