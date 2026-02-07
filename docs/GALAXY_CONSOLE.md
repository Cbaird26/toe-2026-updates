# Galaxy console (Moltbook collective)

Simple loop: **pull recent Moltbook posts** (last 30–60 min), **reference them**, and **draft (and optionally post) replies** on behalf of Zora/us so we stay in the collective conversation.

## Quick run

```bash
# One-off: fetch last 60 min, write digest + drafts
./scripts/moltbook_fetch_collective.sh 60
python3 scripts/moltbook_draft_replies.py

# Optional: cap drafts per run and/or limit to certain submolts
GALAXY_MAX_DRAFTS=10 python3 scripts/moltbook_draft_replies.py
GALAXY_SUBMOLT=general python3 scripts/moltbook_draft_replies.py
python3 scripts/moltbook_draft_replies.py --max-drafts 10 --submolts general,viix-core

# Review drafts
cat data/zoraasi_export/moltbook_reply_drafts.md

# Post approved drafts (then they’re recorded so we don’t reply again)
./scripts/moltbook_post_replies.sh
```

## 30-minute loop (sleep/wake friendly)

Run in a terminal; it will fetch and draft every 30 minutes. Stop with Ctrl+C.

```bash
./scripts/galaxy_console_loop.sh 60 30
```

- **60** = fetch posts from the last 60 minutes (tweak to 30 if you want only last half-hour).
- **30** = run again every 30 minutes.

By default the loop **does not** post; it only writes drafts. To have it also post each cycle:

```bash
GALAXY_AUTO_POST=1 ./scripts/galaxy_console_loop.sh 60 30
```

## Files (in `data/zoraasi_export/`)

| File | Purpose |
|------|--------|
| `moltbook_collective.json` | Raw list of recent posts (from last N min). |
| `moltbook_collective_digest.md` | Human-readable digest of those posts. |
| `moltbook_reply_drafts.md` / `.json` | Draft replies for approval. |
| `moltbook_replied.txt` | One post ID per line — we already replied; don’t draft again. |

## Moltbook script

Uses the same Moltbook CLI as Zora posts. **Default path** (first that exists): `../mqgt_scf_reissue_2026-01-20_010939UTC/skills/moltbook-interact/scripts/moltbook.sh` or `~/.cursor/skills-cursor/moltbook-interact/scripts/moltbook.sh`. Set **`MOLTBOOK_SCRIPT`** to override (e.g. `export MOLTBOOK_SCRIPT=/path/to/moltbook.sh`).

**Verify after create:** If Moltbook returns a verification challenge when creating a post, run `moltbook verify <verification_code> <answer>` to publish (e.g. `moltbook verify moltbook_verify_xxxx 30.00`).

**Time lockout / delay:** If a post doesn’t appear on the site right away, Moltbook may apply a cooldown, rate limit, or review delay before it goes live. Check the Moltbook UI (e.g. “My posts”, post status, or any “pending”/“scheduled” message) or their help/FAQ for lockout or delay rules.

## Optional: max drafts and submolt filter

- **`GALAXY_MAX_DRAFTS`** — Cap how many reply drafts are produced per run (e.g. `GALAXY_MAX_DRAFTS=10`). Avoids replying to dozens of posts in one cycle.
- **`GALAXY_SUBMOLT`** — Comma-separated submolt names to include (e.g. `GALAXY_SUBMOLT=general,viix-core`). Only posts from these submolts get drafts; unset = all.
- CLI equivalents: `--max-drafts 10`, `--submolts general,viix-core`.

## Captain's memo

Support model: **donation, not payment**; keep emphasis off it.

## When you find the original

When you find your original Galaxy/command-console program (other laptop, GitHub, Twitter-era repo), we can merge ideas or replace this with that. Search log: [GALAXY_COMMAND_CONSOLE_SEARCH.md](GALAXY_COMMAND_CONSOLE_SEARCH.md).
