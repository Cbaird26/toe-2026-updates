#!/usr/bin/env bash
# Quick check: list recent cbaird26 repos and print Zenodo search URL for Baird, Christopher Michael.
set -e
echo "=== GitHub (cbaird26) — recent repos ==="
if command -v gh &>/dev/null; then
  gh repo list Cbaird26 --limit 20 2>/dev/null || echo "(gh not installed or not authenticated; install GitHub CLI or run: gh auth login)"
else
  echo "Install GitHub CLI (gh) for repo list: https://cli.github.com/"
fi
echo ""
echo "=== Zenodo (Baird, Christopher Michael) ==="
echo "Open: https://zenodo.org/search?q=metadata.creators.person_or_org.name%3A%22Baird%2C%20Christopher%20Michael%22&l=list&p=1&s=10&sort=bestmatch"
