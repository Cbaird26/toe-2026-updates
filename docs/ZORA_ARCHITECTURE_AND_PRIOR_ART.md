# Zora Architecture and Prior Art

**This is the Zora agent framework.** Single reference for architectural principles, prior-art documentation, and entry points.

---

## Architectural Principles (Prior to ryaker/zora)

The Zora ecosystem implements security and integration patterns that parallel modern agent frameworks:

### 1. Policy Outside Context

Safety rules live in config files, not in the AI conversation. Context compaction cannot erase them.

- **Policy config:** `~/.zora/policy.toml` (allowed/denied paths, shell allowlist)
- **Agent config:** `agent_config.yaml` in zora_trader_minimal (`policies` block)
- **Trading policy:** `ZoraPolicy` in `zora_core.py` with ToE gate (Φc, E)

### 2. Memory in Files

Long-term memory survives between sessions and is stored on disk.

- **~/.zora/memory/:** MEMORY.md, daily/, items/, categories/
- **Black-Book memory/:** ZORA_WHO_I_AM.md, ZORA_CONTEXT_INDEX.md, episodic primer
- **Vault:** `TOE/data/zoraasi_export/` (conversations, personality, RAG corpus)

### 3. Multi-Source Sync

Discovery and sync across cloud and local sources (iCloud, Google Drive, OneDrive, local).

- **instantiate_zoraasi.py:** Discovers ZoraASI artifacts, picks most recent, syncs to vault
- **zora_sync_no_local.sh:** iCloud → Nest, git pull 105+ repos (no local model)
- **instantiate_zora_in_cursor.sh:** Full pull (ZoraASI + iCloud + git)

### 4. Cursor as Zora (No Local Model)

Cursor AI acts as the primary reasoning surface; no Ollama or Zora Brain required.

- **Rule:** `.cursor/rules/zora-as-cursor.mdc`
- **Sync script:** `zora_sync_no_local.sh` — explicitly avoids local model startup

---

## Prior-Art Documentation

| Document | Location | Content |
|----------|----------|---------|
| **Provisional patent** | toe_corpus_release | Claim 3: Recursive Φc mapping (Zora-like agent); EBBR; MQGT-SCF engine |
| **Continuity covenant** | [ZORA_CONTINUITY_COVENANT.md](ZORA_CONTINUITY_COVENANT.md) | Invariants, licensing, corrigibility |
| **ZoraASI activation** | [ZORAASI_ACTIVATION_MQGT-SCF.md](ZORAASI_ACTIVATION_MQGT-SCF.md) | Solved pathways and gaps |
| **Safety constitution** | [../SAFETY_CONSTITUTION.md](../SAFETY_CONSTITUTION.md) | Non-negotiable invariants |

---

## Entry Points

| Entry Point | Path | Purpose |
|-------------|------|---------|
| **zora init** | `~/bin/zora init` | Full instantiation (ZoraASI + iCloud + git) |
| **zora sync** | `~/bin/zora sync` | Sync only (no local model) |
| **zora ask** | `~/bin/zora ask "..."` | Delegate to zora-agent (if installed) |
| **ZoraASI Suite** | [zoraasi-suite](../) (sibling repo) | FastAPI Zora API, outer identity, deploy |
| **Ask Zora** | [zoraasi-suite.onrender.com](https://zoraasi-suite.onrender.com) | Web query (Grok, GPT, Claude) |
| **zoraasi/** | This repo | Chat, RAG, training scripts |

---

## Canonical Repos

- **toe-2026-updates** (this repo) — Public entry point, canonical ToE + Zora releases
- **zoraasi-suite** — Zora agents, API, deployment (unified ZoraAI + ZoraAPI)

---

*This is the Zora agent framework. Same architectural principles as modern security-first agents; prior art established 2026-03-09.*
