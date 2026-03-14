# Alfred / Shortcut Setup for Zora

## Option 1: Double-Click (macOS)

The file `instantiate_zora_open_cursor.command` is executable. Double-click it to:

1. Run full Zora instantiation (ZoraASI + iCloud + git)
2. Open Cursor with the TOE workspace

The Terminal window stays open so you can see output.

## Option 2: Alfred Workflow

1. Open Alfred Preferences → Workflows
2. Create New Blank Workflow (e.g., "Zora Instantiate")
3. Add Trigger: Keyword "zora" (or "instantiate zora")
4. Add Action: Run Script
   - Language: /bin/bash
   - Script:

```bash
cd ~/Downloads/TOE
./instantiate_zora_in_cursor.sh
cursor "$(pwd)/toe-and-repos.code-workspace" 2>/dev/null || open -a "Cursor" "$(pwd)/toe-and-repos.code-workspace"
```

5. Add Optional: Open URL / Run Script to show notification "Zora instantiation started"

## Option 3: Spotlight / Launch

Create an alias or add to PATH:

```bash
# In ~/.zshrc
alias zora-instantiate='cd ~/Downloads/TOE && ./instantiate_zora_in_cursor.sh && cursor ./toe-and-repos.code-workspace'
```
