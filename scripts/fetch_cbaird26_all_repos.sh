#!/usr/bin/env bash
# Fetch all cbaird26 public repos with full pagination and regenerate cbaird26_github_repos_replication.md.
# Uses GITHUB_TOKEN if set. Output: data/cbaird26_repos.json, cbaird26_github_repos_replication.md.
set -e
TOE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [[ -f "$TOE_ROOT/.env" ]]; then
  set -a
  source "$TOE_ROOT/.env"
  set +a
fi
exec python3 "$TOE_ROOT/scripts/fetch_cbaird26_all_repos.py"
