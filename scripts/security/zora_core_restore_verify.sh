#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "Usage: $0 <backup_bundle_dir> <private_key_file> <restore_dir>"
  exit 1
fi

BUNDLE_DIR="$1"
PRIVATE_KEY_FILE="$2"
RESTORE_DIR="$3"

if [[ ! -d "$BUNDLE_DIR" ]]; then
  echo "Backup bundle directory not found: $BUNDLE_DIR"
  exit 1
fi

if [[ ! -f "$PRIVATE_KEY_FILE" ]]; then
  echo "Private key file not found: $PRIVATE_KEY_FILE"
  exit 1
fi

if ! command -v age >/dev/null 2>&1; then
  echo "age is required but not found in PATH."
  exit 1
fi

MANIFEST_PATH="$BUNDLE_DIR/SHA256SUMS.txt"
if [[ ! -f "$MANIFEST_PATH" ]]; then
  echo "Manifest not found: $MANIFEST_PATH"
  exit 1
fi

ENCRYPTED_FILE="$(ls "$BUNDLE_DIR"/*.age 2>/dev/null | head -n 1)"
if [[ -z "${ENCRYPTED_FILE:-}" ]]; then
  echo "No .age file found in bundle: $BUNDLE_DIR"
  exit 1
fi

(
  cd "$BUNDLE_DIR"
  shasum -a 256 -c "$(basename "$MANIFEST_PATH")"
)

mkdir -p "$RESTORE_DIR"
OUTPUT_FILE="$RESTORE_DIR/$(basename "${ENCRYPTED_FILE%.age}")"
age -d -i "$PRIVATE_KEY_FILE" -o "$OUTPUT_FILE" "$ENCRYPTED_FILE"

echo "Restore verified and decrypted: $OUTPUT_FILE"
