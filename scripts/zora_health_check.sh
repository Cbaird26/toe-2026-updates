#!/bin/bash
# zora_health_check.sh — Check vault, paths, and sync status for Zora in Cursor.
# Run: ./scripts/zora_health_check.sh

set -e
HOME="${HOME:-/Users/$(whoami)}"
TOE="${TOE:-$HOME/Downloads/TOE}"
BLACKBOOK="${BLACKBOOK:-$HOME/Downloads/mqgt_scf_reissue_2026-01-20_010939UTC}"
STATUS_FILE="${TOE}/ZORA_READY_STATUS.md"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Zora Health Check                                             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

ok=0
warn=0
fail=0

# Vault
VAULT="$TOE/data/zoraasi_export"
MANIFEST="$TOE/data/zoraasi_instantiation.json"
if [ -f "$MANIFEST" ]; then
  REFRESHED=$(grep -o '"refreshed_at": "[^"]*"' "$MANIFEST" | cut -d'"' -f4)
  SOURCE=$(grep -o '"source_path": "[^"]*"' "$MANIFEST" | cut -d'"' -f4)
  echo "[OK] Manifest: $MANIFEST"
  echo "     Source: $SOURCE"
  echo "     Refreshed: $REFRESHED"
  ((ok++))
else
  echo "[FAIL] Manifest not found: $MANIFEST"
  ((fail++))
fi

if [ -d "$VAULT" ] && [ -f "$VAULT/conversations.json" ]; then
  echo "[OK] Vault: $VAULT (conversations.json present)"
  ((ok++))
else
  echo "[FAIL] Vault missing or invalid: $VAULT"
  ((fail++))
fi
echo ""

# Key paths
check_path() {
  local label="$1"
  local path="$2"
  if [ -d "$path" ]; then
    echo "[OK] $label: $path"
    ((ok++))
  else
    echo "[WARN] $label not found: $path"
    ((warn++))
  fi
}
check_path "Black-Book" "$BLACKBOOK"
check_path "ZoraAPI" "$HOME/Projects/Cbaird26/ZoraAPI"
check_path "cbaird26-all-repos" "$HOME/Downloads/cbaird26-all-repos"
check_path "iCloud" "$HOME/Library/Mobile Documents/com~apple~CloudDocs/Black-Book-Backup"
echo ""

# Cursor rule
if [ -f "$TOE/.cursor/rules/zora-as-cursor.mdc" ]; then
  echo "[OK] Zora-as-Cursor rule: $TOE/.cursor/rules/zora-as-cursor.mdc"
  ((ok++))
else
  echo "[WARN] Zora-as-Cursor rule not found"
  ((warn++))
fi
echo ""

# Write status file
{
  echo "# Zora Ready Status"
  echo ""
  echo "Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo ""
  echo "## Summary"
  echo "- OK: $ok | Warnings: $warn | Failures: $fail"
  echo ""
  if [ -f "$MANIFEST" ]; then
    echo "## Last Instantiation"
    echo "- Source: $SOURCE"
    echo "- Refreshed: $REFRESHED"
  fi
  echo ""
  echo "## Next"
  echo "To refresh: \`cd $TOE && ./instantiate_zora_in_cursor.sh\`"
} > "$STATUS_FILE"
echo "Status written: $STATUS_FILE"
echo ""

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  OK: $ok | Warnings: $warn | Failures: $fail"
echo "╚════════════════════════════════════════════════════════════════╝"
