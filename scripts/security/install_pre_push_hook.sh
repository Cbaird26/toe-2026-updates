#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
HOOK_PATH="${REPO_ROOT}/.git/hooks/pre-push"
CHECK_SCRIPT="${REPO_ROOT}/scripts/security/safe_push.sh"

if [[ ! -d "${REPO_ROOT}/.git" ]]; then
  echo "Not a git repo: ${REPO_ROOT}"
  exit 1
fi

cat > "${HOOK_PATH}" <<EOF
#!/usr/bin/env bash
set -euo pipefail
"${CHECK_SCRIPT}"
EOF

chmod +x "${HOOK_PATH}"
echo "Installed pre-push hook: ${HOOK_PATH}"
echo "Hook will fail closed on risky matches."
