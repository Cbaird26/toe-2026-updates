#!/usr/bin/env bash
set -euo pipefail

if ! command -v rg >/dev/null 2>&1; then
  echo "ERROR: ripgrep (rg) is required."
  exit 2
fi

PATTERN_FILE="$HOME/Desktop/Project Zora - Desktop/scripts/security_patterns.txt"

echo "== SAFE PUSH CHECK (TOE) =="
echo "Repo: $(pwd)"

risk=0

echo
echo "-- git status --"
git status --short

tracked_pattern='(private_continuity|chat_exports|private_chats|transcripts_private|zora-core|secret|key|passphrase|wallet|seed|\.env|\.pem|\.p12|\.asc|\.zip|\.age|\.gpg)$'
untracked_pattern='(private|chat|transcript|zora-core|secret|key|passphrase|wallet|seed|\.env|\.pem|\.p12|\.asc|\.zip|\.age|\.gpg)$'
secret_pattern='(api[_-]?key|secret|password|passphrase|token|private[_-]?key|BEGIN (RSA|OPENSSH|PGP) PRIVATE KEY)'

if [[ -f "${PATTERN_FILE}" ]]; then
  while IFS= read -r line; do
    [[ -z "${line}" || "${line}" =~ ^# ]] && continue
    key="${line%%=*}"
    value="${line#*=}"
    case "${key}" in
      TRACKED_PATTERN) tracked_pattern="${value}" ;;
      UNTRACKED_PATTERN) untracked_pattern="${value}" ;;
      SECRET_CONTENT_PATTERN) secret_pattern="${value}" ;;
    esac
  done < "${PATTERN_FILE}"
fi

echo
echo "-- tracked sensitive filename scan --"
tracked_hits="$(git ls-files | rg -i "${tracked_pattern}" || true)"
if [[ -n "${tracked_hits}" ]]; then
  echo "${tracked_hits}"
  risk=1
else
  echo "No tracked sensitive filename hits."
fi

echo
echo "-- untracked sensitive filename scan --"
untracked_hits="$(git status --short | rg "^\?\?" | rg -i "${untracked_pattern}" || true)"
if [[ -n "${untracked_hits}" ]]; then
  echo "${untracked_hits}"
  risk=1
else
  echo "No untracked sensitive filename hits."
fi

echo
echo "-- secret-content scan --"
content_hits="$(rg -n -i "${secret_pattern}" . --glob '!.git' || true)"
if [[ -n "${content_hits}" ]]; then
  echo "${content_hits}"
  risk=1
else
  echo "No secret-content hits."
fi

echo
echo "-- staged diff preview --"
git diff --staged --name-only

if [[ "${risk}" -ne 0 ]]; then
  echo
  echo "NO-GO: Potentially sensitive content detected. Fix issues before push."
  exit 1
fi

echo
echo "GO: Safety checks passed."
echo "You can now run: git push"
