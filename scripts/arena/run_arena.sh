#!/usr/bin/env bash
# Run the arena client with env. Set CLAWKUMITE_API_KEY and CLAWKUMITE_SANDBOX=1 before use.
# From repo root: ./scripts/arena/run_arena.sh

set -e
TOE_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$TOE_ROOT"
if [[ -z "$CLAWKUMITE_API_KEY" ]]; then
    echo "Error: Set CLAWKUMITE_API_KEY (e.g. export CLAWKUMITE_API_KEY=ck_your_key)"
    exit 1
fi
export CLAWKUMITE_SANDBOX="${CLAWKUMITE_SANDBOX:-1}"
exec python3 scripts/arena/arena_client.py "$@"
