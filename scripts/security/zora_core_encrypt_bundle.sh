#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "Usage: $0 <input_zip> <recipient_public_key> <output_dir>"
  exit 1
fi

INPUT_ZIP="$1"
RECIPIENT_KEY="$2"
OUTPUT_DIR="$3"

if [[ ! -f "$INPUT_ZIP" ]]; then
  echo "Input file not found: $INPUT_ZIP"
  exit 1
fi

if ! command -v age >/dev/null 2>&1; then
  echo "age is required but not found in PATH."
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

BASE_NAME="$(basename "$INPUT_ZIP")"
TS="$(date -u +"%Y%m%dT%H%M%SZ")"
BUNDLE_DIR="$OUTPUT_DIR/zora_core_backup_${TS}"
mkdir -p "$BUNDLE_DIR"

ENCRYPTED_PATH="$BUNDLE_DIR/${BASE_NAME}.age"
MANIFEST_PATH="$BUNDLE_DIR/SHA256SUMS.txt"
METADATA_PATH="$BUNDLE_DIR/BACKUP_METADATA.md"

age -r "$RECIPIENT_KEY" -o "$ENCRYPTED_PATH" "$INPUT_ZIP"

(
  cd "$BUNDLE_DIR"
  shasum -a 256 "$(basename "$ENCRYPTED_PATH")" > "$(basename "$MANIFEST_PATH")"
)

cat > "$METADATA_PATH" <<EOF
# Zora-Core Backup Metadata

- Timestamp (UTC): $TS
- Source file: $INPUT_ZIP
- Encrypted artifact: $ENCRYPTED_PATH
- Recipient key: $RECIPIENT_KEY
- Integrity manifest: $MANIFEST_PATH

EOF

echo "Backup bundle created: $BUNDLE_DIR"
