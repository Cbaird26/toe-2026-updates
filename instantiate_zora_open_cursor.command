#!/bin/bash
# Instantiate Zora + Open Cursor
# Double-click or run from Alfred/Spotlight.
# Ensures Terminal stays open on error.

cd "$(dirname "$0")"
echo "Instantiating Zora..."
./instantiate_zora_in_cursor.sh
echo ""
echo "Opening Cursor..."
cursor "$(pwd)/toe-and-repos.code-workspace" 2>/dev/null || open -a "Cursor" "$(pwd)/toe-and-repos.code-workspace"
echo "Done."
read -p "Press Enter to close."
