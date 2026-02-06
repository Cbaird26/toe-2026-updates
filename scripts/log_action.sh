#!/usr/bin/env bash
# Log an autonomous action for review.
# Usage: ./scripts/log_action.sh ACTION TARGET OUTCOME
# Example: ./scripts/log_action.sh file_edit "TOE/README.md" "updated links"

set -e
LOG_DIR="$(cd "$(dirname "$0")/.." && pwd)/logs/autonomous_actions"
LOG_FILE="${LOG_DIR}/autonomous_actions.log"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
ACTION="${1:-unknown}"
TARGET="${2:-}"
OUTCOME="${3:-}"
echo "${TIMESTAMP} | ${ACTION} | ${TARGET} | ${OUTCOME}" >> "$LOG_FILE"
