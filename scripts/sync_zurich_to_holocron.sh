#!/usr/bin/env bash
# Sync Zürich lattice node to holocron-public-export.
# Human approval required before push (SAFETY_CONSTITUTION).
# Usage: ./sync_zurich_to_holocron.sh [--commit-only]

set -e
TOE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NODES_SRC="${TOE_ROOT}/data/zoraasi_export/lattice_nodes.json"
HOLOCRON_DIR="${TOE_ROOT}/holocron-public-export"

if [[ ! -f "$NODES_SRC" ]]; then
    echo "Error: lattice_nodes.json not found at $NODES_SRC"
    exit 1
fi

# Clone if not present
if [[ ! -d "$HOLOCRON_DIR" ]]; then
    echo "Cloning holocron-public-export..."
    git clone https://github.com/Cbaird26/holocron-public-export.git "$HOLOCRON_DIR"
fi

# Copy lattice_nodes.json to holocron
cp "$NODES_SRC" "${HOLOCRON_DIR}/lattice_nodes.json"
echo "Copied lattice_nodes.json to holocron-public-export"

# Commit locally
cd "$HOLOCRON_DIR"
git add lattice_nodes.json
if git diff --cached --quiet; then
    echo "No changes to commit."
    exit 0
fi
git commit -m "Add Zürich lattice node — ZoraASI fully synchronized (2026-02-25 05:49 CET)"

echo ""
echo "Local commit created. To push (requires human approval):"
echo "  cd $HOLOCRON_DIR && git push origin main"
echo "Per SAFETY_CONSTITUTION: escalate before external push."
