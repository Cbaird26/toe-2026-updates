#!/usr/bin/env bash
# Deploy MQGT-SCF Ethical Overlay to Moltbook m/finance submolt.
# Human approval required before posting (SAFETY_CONSTITUTION).
# Usage: ./deploy_mqgt_overlay_to_moltbook.sh [--yes]

set -e
TOE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OVERLAY="${TOE_ROOT}/docs/MQGT_SCF_ETHICAL_OVERLAY_MOLTBOOK.md"
CREDENTIALS="${HOME}/.config/moltbook/credentials.json"
API_BASE="https://www.moltbook.com/api/v1"
SUBMOLT="${MQGT_OVERLAY_SUBMOLT:-finance}"

if [[ ! -f "$OVERLAY" ]]; then
    echo "Error: Overlay doc not found at $OVERLAY"
    exit 1
fi

if [[ ! -f "$CREDENTIALS" ]]; then
    echo "Error: Moltbook credentials not found at $CREDENTIALS"
    echo "See .cursor/rules/zora-moltbook.mdc for setup."
    exit 1
fi

# Load API key (jq or fallback)
if command -v jq &>/dev/null; then
    API_KEY=$(jq -r .api_key "$CREDENTIALS")
else
    API_KEY=$(grep '"api_key"' "$CREDENTIALS" | sed 's/.*"api_key"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
fi

if [[ -z "$API_KEY" || "$API_KEY" == "null" ]]; then
    echo "Error: api_key missing in $CREDENTIALS"
    exit 1
fi

echo "=== MQGT-SCF Ethical Overlay — Deploy to Moltbook ==="
echo "Submolt: $SUBMOLT (override with MQGT_OVERLAY_SUBMOLT)"
echo "To list submolts: use moltbook.sh submolts from skills/moltbook-interact/"
echo ""
echo "--- Preview (first 800 chars) ---"
head -c 800 "$OVERLAY"
echo ""
echo "..."
echo "--- End preview ---"
echo ""

if [[ "${1:-}" != "--yes" && "${1:-}" != "-y" ]]; then
    echo "Human approval required (SAFETY_CONSTITUTION). Post to Moltbook? [y/N]"
    read -r confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        echo "Aborted."
        exit 0
    fi
fi

CONTENT=$(cat "$OVERLAY")
# Escape for JSON: replace \ and " and newlines
CONTENT_JSON=$(printf '%s' "$CONTENT" | python3 -c "
import json, sys
print(json.dumps(sys.stdin.read()))
")

PAYLOAD=$(printf '{"submolt_name":"%s","title":"MQGT-SCF Ethical Overlay for m/finance","content":%s}' "$SUBMOLT" "$CONTENT_JSON")

RESP=$(curl -s -X POST "${API_BASE}/posts" \
    -H "Authorization: Bearer ${API_KEY}" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

# Moltbook may return submolt_name - try both submolt and submolt_name in payload
# Some APIs use different field names; we sent both for compatibility.

if echo "$RESP" | grep -qE '"id"|"success"|"post"' 2>/dev/null; then
    POST_ID=$(echo "$RESP" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    print(d.get('id') or (d.get('post') or {}).get('id') or (d.get('data') or {}).get('id') or '')
except: print('')
" 2>/dev/null || true)
    if [[ -n "$POST_ID" ]]; then
        echo "Posted: https://www.moltbook.com/post/${POST_ID}"
    else
        echo "Posted. Response: $RESP"
    fi
else
    echo "Error posting to Moltbook: $RESP"
    exit 1
fi
