#!/usr/bin/env bash
# Fetch recent cbaird26 repos from GitHub and write JSON + short digest.
# Output: data/zoraasi_export/github_recent.json, github_recent.md
# Uses GitHub API (no auth for public repos) or gh CLI if available.

set -e
TOE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="${TOE_ROOT}/data/zoraasi_export"
JSON_OUT="${OUT_DIR}/github_recent.json"
MD_OUT="${OUT_DIR}/github_recent.md"
mkdir -p "$OUT_DIR"

fetch_with_gh() {
  gh api "users/cbaird26/repos?sort=updated&per_page=10" --jq '
    [.[] | {name, full_name, description, updated_at, html_url, default_branch}]
  ' 2>/dev/null
}

fetch_with_curl() {
  curl -sS -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/users/cbaird26/repos?sort=updated&per_page=10" \
    | python3 -c '
import json, sys
data = json.load(sys.stdin)
if isinstance(data, dict) and data.get("message"):
  sys.exit(1)
out = [{"name": r.get("name"), "full_name": r.get("full_name"), "description": r.get("description") or "", "updated_at": r.get("updated_at"), "html_url": r.get("html_url"), "default_branch": r.get("default_branch")} for r in (data if isinstance(data, list) else [])]
print(json.dumps(out))
'
}

if command -v gh &>/dev/null; then
  RAW="$(fetch_with_gh)" || true
fi
if [[ -z "$RAW" ]]; then
  RAW="$(fetch_with_curl)" || true
fi
if [[ -z "$RAW" ]]; then
  echo "GitHub fetch skipped (gh not available and curl failed)."
  echo '{"fetched_at": null, "repos": []}' > "$JSON_OUT"
  echo "# GitHub (cbaird26) — no data" > "$MD_OUT"
  exit 0
fi

TMP_JSON="${OUT_DIR}/.github_recent_tmp.json"
echo "$RAW" > "$TMP_JSON"
python3 - "$TMP_JSON" "$JSON_OUT" "$MD_OUT" << 'PY'
import json, sys
from datetime import datetime, timezone

tmp_path, json_out, md_out = sys.argv[1], sys.argv[2], sys.argv[3]
with open(tmp_path) as f:
    repos = json.load(f)
if not isinstance(repos, list):
    repos = []

payload = {
    "fetched_at": datetime.now(timezone.utc).isoformat(),
    "repos": repos,
}
with open(json_out, "w") as f:
    json.dump(payload, f, indent=2)

with open(md_out, "w") as f:
    f.write("# GitHub (cbaird26) — recent repos\n\n")
    f.write(f"*Fetched: {payload['fetched_at']}*\n\n")
    for r in repos:
        name = r.get("name") or "?"
        url = r.get("html_url") or ""
        desc = (r.get("description") or "")[:200]
        updated = r.get("updated_at") or ""
        f.write(f"- **{name}** — {updated}\n  {url}\n  {desc}\n\n")
PY
rm -f "$TMP_JSON"

echo "GitHub: $JSON_OUT ($(python3 -c "import json; print(len(json.load(open('$JSON_OUT'))['repos']))") repos)"
