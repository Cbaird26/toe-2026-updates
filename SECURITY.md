# Security — full protection without extra friction

What’s already in place, and a few light guardrails that don’t make daily use harder.

---

## Already in place

| Area | Protection |
|------|------------|
| **Secrets** | No API keys or credentials in repo. Moltbook uses `~/.config/moltbook/credentials.json`; OpenAI uses `OPENAI_API_KEY` env. `.gitignore` covers `.env`, `.env.*`, `*.pem`, `*.key`. |
| **Vault** | `data/zoraasi_export/`, `ZoraASI_vault/`, `ZoraASI.zip` are gitignored. Logs and GPT export never committed. |
| **Posting** | Moltbook posts only after you approve (y/n). No automatic posting. SANDBOX_AND_APPROVAL_FLOWS and SAFETY_CONSTITUTION apply. |
| **Logging** | Autonomous actions (e.g. Moltbook POST) logged in `logs/autonomous_actions/` for review. |
| **Network** | Moltbook script talks only to `https://www.moltbook.com`. Credentials sent only there. |
| **Code** | No credentials in source; scripts read config from home dir or env at runtime. |

---

## Zero-friction additions

1. **Credentials directory permissions** (one-time)  
   So only your user can read the Moltbook config:
   ```bash
   chmod 700 ~/.config/moltbook
   chmod 600 ~/.config/moltbook/credentials.json
   ```
   No extra steps after that.

2. **Pre-push check (optional)**  
   Avoid accidentally pushing vault or secrets. From repo root:
   ```bash
   git config core.hooksPath .githooks
   chmod +x .githooks/pre-push
   ```
   The hook in `.githooks/pre-push` is already there; it blocks push if vault or credential paths are in the commit. If you don’t use hooks, skip this; your normal workflow is unchanged.

3. **Sensitive commands in Terminal**  
   Run anything that uses credentials or posts (e.g. `moltbook_draft_and_post.py`, or scripts that call APIs) from Terminal.app, not from a sandboxed environment (e.g. Codex) that might log or capture output. One-line reminder; no tool change.

4. **Backup of vault**  
   If you back up the machine, keep the vault (and any export zip) in an encrypted volume or backup that only you can restore. No change to how you run scripts.

5. **No logging of secrets**  
   Scripts never print or log API keys, tokens, or credential file contents. If we add new scripts, we keep that rule. No action needed from you.

---

## What we don’t do (to keep life simple)

- No mandatory 2FA or key entry for local ZoraASI/Ollama.
- No encrypting the vault with a password you type each run.
- No blocking automation; approval for posting is the only gate.
- No scanning or modifying your system beyond the repo and the config paths we document.

---

## Prevention stack (skeleton-key / credential-leak)

**Problem in one line:** Persistence makes agents useful but also makes credential leaks structural (keys in memory/vault). Platform primitives matter: skeleton keys by default mean the game is lost before agent-level sandboxing.

**Layers we document (for future or platform adoption):**

- **Platform / least privilege:** No skeleton keys by default; scoped capabilities, IAM-style roles.
- **Credential shape:** Scoped delegations, short-lived tokens, capability tokens (bounded blast radius).
- **Rolling encryption:** Encrypt vault at rest with a key that rotates or is session-derived; exfiltrated dumps age out.
- **Authenticator / step-up:** High-impact actions (e.g. post) gated by a second factor the agent does not hold (we already have y/n approval; could strengthen to separate channel).
- **Memory isolation:** Keys never in persistable context; scripts read creds at runtime and do not pass them into agent context (we already do this for Moltbook).
- **Provenance / registry:** Signed skills, "who signed this?" discoverable; prevents bad installs, not only detection after.
- **Defaults:** "Ask first, persist later" instead of persist-by-default.

**What we do today:** Credentials outside repo, approval before post, no secrets in logs, vault gitignored, backup encrypted (recommended). Optional: credentials dir permissions, pre-push hook.

No code or script changes in this section; this is guidance and future-reference only.

---

## Quick checklist

- [ ] `data/zoraasi_export/` and export zip stay out of git (already in `.gitignore`).
- [ ] Moltbook credentials only in `~/.config/moltbook/` (or env), never in repo.
- [ ] Run posting/API scripts from Terminal when possible.
- [ ] Optional: `chmod 700 ~/.config/moltbook` and `chmod 600 .../credentials.json`.
- [ ] Optional: pre-push hook to block vault/secrets from being pushed.

That’s full security for this system without making your life harder.

**Full-stack security prompt (for agents/briefings):** see [docs/FULL_STACK_SECURITY_PROMPT.md](docs/FULL_STACK_SECURITY_PROMPT.md).
