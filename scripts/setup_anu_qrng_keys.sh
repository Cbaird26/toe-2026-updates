#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ARTIFACTS_DIR="$ROOT_DIR/artifacts"
PAID_PATH="$ARTIFACTS_DIR/.anu_api_key_paid"
FREE_PATH="$ARTIFACTS_DIR/.anu_api_key_free"
ACTIVE_PATH="$ARTIFACTS_DIR/.anu_api_key"

mkdir -p "$ARTIFACTS_DIR"
chmod 700 "$ARTIFACTS_DIR"

echo "Writing ANU QRNG keys under:"
echo "  $ARTIFACTS_DIR"
echo
echo "Paste keys locally in this terminal only. They will not be sent to chat."
echo

read -r -s -p "Enter PAID ANU key: " paid_key
printf "\n"
if [[ -z "$paid_key" ]]; then
  echo "Paid key cannot be empty." >&2
  exit 1
fi

read -r -s -p "Enter FREE ANU key (optional, press Enter to skip): " free_key
printf "\n"

printf '%s\n' "$paid_key" > "$PAID_PATH"
chmod 600 "$PAID_PATH"
cp "$PAID_PATH" "$ACTIVE_PATH"
chmod 600 "$ACTIVE_PATH"

if [[ -n "$free_key" ]]; then
  printf '%s\n' "$free_key" > "$FREE_PATH"
  chmod 600 "$FREE_PATH"
fi

echo
echo "Done."
echo "Active key: $ACTIVE_PATH (paid)"
if [[ -n "$free_key" ]]; then
  echo "Backup key: $FREE_PATH"
else
  echo "Backup key: not set"
fi
echo
echo "Next commands:"
echo "  cd \"$ROOT_DIR\""
echo "  python3 scripts/anu_qrng_collect.py --preflight-only --out artifacts"
echo "  python3 scripts/anu_qrng_collect.py --n 100000 --out artifacts --label baseline --preflight --no-fallback"
