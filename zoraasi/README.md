# ZoraASI (local build)

Build ZoraASI locally from ChatGPT export logs and knowledge base (RAG). Vault and logs are **confidential**; never commit `data/zoraasi_export/` or the zip.

## Setup

1. **Vault**: Extract `ZoraASI.zip` into `TOE/data/zoraasi_export/` when you have ~2GB free. Or set `VAULT_PATH` to another directory (or path to the zip) that contains `conversations.json` and optional `user.json`, `group_chats.json`, etc.

2. **Python**: Use a venv (recommended on macOS with Homebrew Python):  
   `cd TOE && python3 -m venv .venv && source .venv/bin/activate`  
   then `pip install -r zoraasi/requirements.txt`. From repo root without venv: `pip install -r zoraasi/requirements.txt` if your environment allows.

3. **Ingest** (once): `python zoraasi/scripts/ingest.py` — reads vault, writes curated index and corpus under the vault. Uses streaming so large `conversations.json` is not fully loaded.

4. **Personality/training**: `python zoraasi/scripts/distill_personality.py` — produces `personality_spec.md`, `system_prompt_zoraasi.md`, `few_shot_examples.json`, and training JSONL under vault.

5. **RAG** (once): `python zoraasi/scripts/build_rag_index.py` — indexes your knowledge base (default `~/Downloads/KNOWLEDGE BASE` or set `KNOWLEDGE_BASE_PATH`). Writes `rag_index.json` (and optional `rag_embeddings.json` if Ollama + nomic-embed-text is available) into the vault. Use `--no-embeddings` for keyword-only retrieval.

6. **Chat**: From `TOE`: `python zoraasi/scripts/run_chat.py -m "Your question"` — local (Ollama) or API-backed ZoraASI with RAG context from the knowledge base. Use `--no-rag` to disable RAG. No posting to Moltbook by default; that stays manual/approval.

7. **Refresh from export** (after updating ZoraASI.zip or adding more logs):  
   `./zoraasi/scripts/refresh_from_export.sh /path/to/ZoraASI.zip` — extracts (if zip given), then ingest + distill so the vault stays in sync with your GPT data.

## Moltbook automation (draft → approve → post)

Human-in-the-loop: ZoraASI drafts a post, you approve, then it posts. No automatic posting.

- **Track with you**: Update `data/zoraasi_export/moltbook_context.txt` (or set `MOLTBOOK_CONTEXT`) with what you're working on so drafts stay coherent. Example: "ToE fifth-force bounds, section 3.2" or "Enrollment push this week."
- **Draft and post** (from TOE, venv active):
  ```bash
  python zoraasi/scripts/moltbook_draft_and_post.py
  ```
  This uses local ZoraASI to draft a short post (using your context), saves it to `vault/moltbook_draft.md`, shows it, and asks **Post this to Moltbook as ZoraAI? (y/n)**. If you say yes, it posts and logs to `logs/autonomous_actions/`.
- **Options**: `--dry-run` (only draft, no prompt to post), `--context "string"` or `-c "string"` to pass context this run, `--title "Title"`, `--from-draft path/to/draft.md` to post an existing draft without regenerating, `-y` to skip the approval prompt (use with care).
- **Credentials**: Uses `~/.config/moltbook/credentials.json` (api_key, agent_name). Same as the Moltbook skill; never committed.
- **Later**: Scheduling (e.g. cron) can run the script and leave the draft for you to approve when you're back; or we add a small “pending drafts” flow. Trading automation stays out of scope until you’re ready.

## Troubleshooting: "Operation not permitted" / Ollama connection

- **Start Ollama**: Open the **Ollama** app from Applications (or in a terminal run `ollama serve`). Leave it running, then run ZoraASI again.
- **Use OpenAI instead**: If you can't use local Ollama (e.g. sandbox blocks localhost), use the API backend:
  ```bash
  python zoraasi/scripts/run_chat.py --backend openai --model gpt-4o-mini -m "Your question"
  ```
  Set `OPENAI_API_KEY` in your environment first. (OpenAI defaults to `gpt-4o-mini` if you omit `--model`.)
- **Run from Terminal**: If you're invoking the command from Codex or another sandboxed environment, run the same command in **Terminal.app** (or iTerm) so it can reach `localhost:11434`.

## Safety

Autonomous or high-stakes actions follow [TOE SAFETY_CONSTITUTION.md](../SAFETY_CONSTITUTION.md). Human-in-the-loop for posting, irreversible actions, and goal changes. ZoraASI does not post to Moltbook by default; posting stays manual or via explicit approval.
