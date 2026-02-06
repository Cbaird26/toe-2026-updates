# Privacy — what stays with you, what doesn’t

Clear data flows and defaults so nothing leaves your machine unless you choose it.

---

## What stays local (no third party)

| Data | Where it lives | Who can see it |
|------|----------------|----------------|
| **ZoraASI vault** | `data/zoraasi_export/` (gitignored) | Only you, on this machine. GPT export, ingested corpus, RAG index, drafts, context. |
| **Knowledge base** | Your paths (e.g. `~/Downloads/KNOWLEDGE BASE`) | Only you. RAG index is built locally and stored in the vault; source docs are never sent out. |
| **Chat with Ollama** | Your machine only | You. Model runs locally; prompts and replies stay on device. No telemetry in our scripts. |
| **Credentials** | `~/.config/moltbook/`, env vars | Only you. Never logged or committed. |
| **Action log** | `logs/autonomous_actions/` | You (and anyone with repo access). Logs *that* something was posted, not the content of posts or any message text. |

So: vault, knowledge base, local chat, and credentials are **local-only** by default.

---

## When data leaves your machine (only if you do this)

| Action | What leaves | Where |
|--------|-------------|--------|
| **You approve a Moltbook post** | The post title and body you approved | Moltbook (https://www.moltbook.com). No ongoing stream; only what you explicitly post. |
| **You use `--backend openai`** | The message and system prompt (and RAG context) you send | OpenAI’s API. Use local Ollama if you want to keep those conversations off third-party servers. |

We don’t send anything else. No telemetry, no analytics, no “phone home,” no tracking.

---

## What we don’t do

- No logging of message content, post body, or user input in our logs (only “Moltbook POST | published as ZoraAI” style lines).
- No sharing of vault, knowledge base, or chat history with any service.
- No tracking or profiling. No cookies or identifiers in our code.
- No scanning of your system beyond the repo and the config paths we document.

---

## Optional privacy habits (no extra friction)

1. **Sensitive chats**  
   Use local Ollama for anything you don’t want on a third party. Use `--backend openai` only when you’re okay with that data going to OpenAI.

2. **Backups**  
   If you back up the machine, keep the vault (and any export zip) in an encrypted or otherwise access-controlled backup so only you can restore it.

3. **Where you run commands**  
   If you use Cursor, Codex, or another cloud-backed tool, their privacy policy applies to what you type there. Running ZoraASI (and especially posting) from Terminal keeps the conversation and drafts entirely on your machine except for what you explicitly post.

4. **Moltbook**  
   Only the text you approve is posted. Drafts stay in the vault until you say yes.

---

## Summary

- **Local by default**: Vault, knowledge base, RAG, local chat, credentials — all stay on your machine.
- **Leave only when you choose**: Moltbook (only approved posts); OpenAI (only if you use `--backend openai`).
- **No hidden flows**: No telemetry, no content logging, no tracking. Privacy is preserved without making your life harder.
