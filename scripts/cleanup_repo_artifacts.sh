#!/usr/bin/env bash
# Remove common LaTeX / pdfTeX build artifacts from the TOE working tree (not inside .git, venvs, or logs/).
#
# Usage:
#   bash scripts/cleanup_repo_artifacts.sh --dry-run    # list only
#   bash scripts/cleanup_repo_artifacts.sh --delete     # remove files
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MODE="dry-run"

for arg in "$@"; do
  case "$arg" in
    --dry-run) MODE="dry-run" ;;
    --delete) MODE="delete" ;;
    -h|--help)
      sed -n '1,12p' "$0" | tail -n +2
      exit 0
      ;;
    *)
      echo "Unknown option: $arg (use --dry-run or --delete)" >&2
      exit 1
      ;;
  esac
done

collect() {
  find "$ROOT" -type f \( \
      -name '*.aux' -o -name '*.log' -o -name '*.out' -o \
      -name '*.toc' -o -name '*.lof' -o -name '*.lot' -o \
      -name '*.bbl' -o -name '*.blg' -o -name '*.synctex.gz' -o \
      -name '*.fls' -o -name '*.fdb_latexmk' -o -name '*.xdv' \
    \) \
    ! -path '*/.git/*' \
    ! -path '*/.venv/*' \
    ! -path '*/venv/*' \
    ! -path '*/env/*' \
    ! -path '*/logs/*' \
    ! -path '*/node_modules/*' \
    -print
}

if [[ "$MODE" == "dry-run" ]]; then
  echo "Dry run — would remove:"
  collect | sed 's/^/  /' || true
  n="$(collect | wc -l | tr -d ' ')"
  echo "Total: $n file(s). Run with --delete to remove."
  exit 0
fi

# delete
while IFS= read -r f; do
  rm -f "$f"
  echo "removed: $f"
done < <(collect)

echo "OK: LaTeX artifact cleanup finished under $ROOT"
