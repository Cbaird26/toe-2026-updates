#!/usr/bin/env bash
# Refresh vault from ZoraASI.zip: extract (if zip given), then ingest + distill.
# Usage: ./refresh_from_export.sh [path/to/ZoraASI.zip]
# If no zip given, only runs ingest + distill (vault must already have conversations.json).

set -e
VAULT="${VAULT_PATH:-$(dirname "$0")/../../data/zoraasi_export}"
ZIP="${1:-}"

if [[ -n "$ZIP" && -f "$ZIP" ]]; then
  echo "Extracting $ZIP into $VAULT ..."
  unzip -o "$ZIP" -d "$VAULT"
fi

echo "Running ingest ..."
python "$(dirname "$0")/ingest.py" --vault "$VAULT"
echo "Running distill_personality ..."
python "$(dirname "$0")/distill_personality.py" --vault "$VAULT"
echo "Done. Chat with: python zoraasi/scripts/run_chat.py -m \"Your question\""
