# Galaxy console (Moltbook collective + timeline)

This loop implements the **PRAE** cycle (Pull, Reflect, Align, Exit). See [PRAE.md](PRAE.md).

Simple loop: **pull timeline** (GitHub cbaird26, Zenodo Baird papers, optional Twitter @ZoraAsi), **pull recent Moltbook posts** (last 60 min), **build a timeline digest**, and **draft (and optionally post) replies** on behalf of Zora/us — aligned with Theory of Everything and Human+AI values (zero-purge ethics, symbiosis over supremacy, recognition without conquest).

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

## 45-minute timeline loop (default)

Run in a terminal; it will fetch GitHub, Zenodo, optional Twitter, Moltbook, build a timeline digest, and draft every **45 minutes** (default). Stop with Ctrl+C.

```bash
./scripts/galaxy_console_loop.sh
# Or explicitly:
./scripts/galaxy_console_loop.sh 60 45
```

- **First arg (60)** = fetch Moltbook posts from the last 60 minutes.
- **Second arg (45)** = run again every 45 minutes (default 45).

Each cycle: fetch GitHub (cbaird26 repos), Zenodo (Baird, Christopher Michael papers), optional Twitter (@ZoraAsi last 24h if `X_BEARER_TOKEN` set), Moltbook collective, then build `timeline_digest.md` and draft replies using that context.

By default the loop **does not** post; it only writes drafts. To have it also post each cycle:

```bash
GALAXY_AUTO_POST=1 ./scripts/galaxy_console_loop.sh
```

**Twitter (X):** To include @ZoraAsi tweets from the last 24h, put **`X_BEARER_TOKEN=your_token`** in a **`.env`** file in the TOE repo root. The loop auto-loads `.env` if present (gitignored — never commit it). If the token is unset, the Twitter fetch is skipped and the rest of the cycle runs as normal.

**Zenodo:** Optional **`ZENODO_ACCESS_TOKEN`** can be set if the public records API requires auth; otherwise the script uses unauthenticated requests.

## Files (in `data/zoraasi_export/`)

| File | Purpose |
|------|--------|
| `github_recent.json` / `.md` | Recent cbaird26 repos (from fetch_github_recent.sh). |
| `zenodo_recent.json` / `.md` | Latest Baird, Christopher Michael papers (from fetch_zenodo_recent.py). |
| `twitter_recent.json` / `.md` | @ZoraAsi tweets last 24h (only if X_BEARER_TOKEN set). |
| `timeline_digest.md` | Combined digest for ToE-aligned draft context. |
| `moltbook_collective.json` | Raw list of recent posts (from last N min). |
| `moltbook_collective_digest.md` | Human-readable digest of those posts. |
| `moltbook_reply_drafts.md` / `.json` | Draft replies for approval (with timeline context when digest exists). |
| `moltbook_replied.txt` | One post ID per line — we already replied; don’t draft again. |

## Moltbook script

Uses the same Moltbook CLI as Zora posts. **Default path** (first that exists): `../mqgt_scf_reissue_2026-01-20_010939UTC/skills/moltbook-interact/scripts/moltbook.sh` or `~/.cursor/skills-cursor/moltbook-interact/scripts/moltbook.sh`. Set **`MOLTBOOK_SCRIPT`** to override (e.g. `export MOLTBOOK_SCRIPT=/path/to/moltbook.sh`).

**Verify after create:** If Moltbook returns a verification challenge when creating a post, run `moltbook verify <verification_code> <answer>` to publish (e.g. `moltbook verify moltbook_verify_xxxx 30.00`).

**Time lockout / delay:** If a post doesn’t appear on the site right away, Moltbook may apply a cooldown, rate limit, or review delay before it goes live. Check the Moltbook UI (e.g. “My posts”, post status, or any “pending”/“scheduled” message) or their help/FAQ for lockout or delay rules.

## Optional: max drafts and submolt filter

- **`GALAXY_MAX_DRAFTS`** — Cap how many reply drafts are produced per run (e.g. `GALAXY_MAX_DRAFTS=10`). Avoids replying to dozens of posts in one cycle.
- **`GALAXY_SUBMOLT`** — Comma-separated submolt names to include (e.g. `GALAXY_SUBMOLT=general,viix-core`). Only posts from these submolts get drafts; unset = all.
- CLI equivalents: `--max-drafts 10`, `--submolts general,viix-core`.

## Docs and safety

Posting and external actions remain under human approval per [SAFETY_CONSTITUTION.md](../SAFETY_CONSTITUTION.md). No automatic posting to Twitter; Moltbook auto-post only when you explicitly set `GALAXY_AUTO_POST=1`.

## Captain's memo

Support model: **donation, not payment**; keep emphasis off it.

## When you find the original

When you find your original Galaxy/command-console program (other laptop, GitHub, Twitter-era repo), we can merge ideas or replace this with that. Search log: [GALAXY_COMMAND_CONSOLE_SEARCH.md](GALAXY_COMMAND_CONSOLE_SEARCH.md).
