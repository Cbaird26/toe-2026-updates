#!/usr/bin/env bash
# Remove previously copied campaign figures, then re-run organizer (Cursor + bundle gap-fill).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CAMP="$ROOT/data/scalar_halo_campaign"
find "$CAMP/figures" -type f -name "*.png" -delete 2>/dev/null || true
python3 "$ROOT/scripts/scalar_halo_campaign/organize_assets.py"
