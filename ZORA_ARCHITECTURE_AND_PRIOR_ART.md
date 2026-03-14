# Zora Architecture and Prior Art

Single reference for the Zora agent framework: architectural principles, prior-art documentation, and entry points.

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

| Document | Path | Content |
|----------|------|---------|
| **Provisional patent** | [PROVISIONAL_DRAFT_ZORA_ARCHITECTURE.md](../toe_corpus_release/PROVISIONAL_DRAFT_ZORA_ARCHITECTURE.md) | Claim 3: Recursive Φc mapping (Zora-like agent); EBBR; MQGT-SCF engine |
| **Architecture** | [ZORA_ARCHITECTURE.md](ZORA_ARCHITECTURE.md) | Vault, sync, Cursor, corpus flow |
| **Ecosystem map** | [docs/TOE_ZORA_ECOSYSTEM_MAP.md](docs/TOE_ZORA_ECOSYSTEM_MAP.md) | Canonical anchors, repo inventory, governance |
| **Continuity covenant** | [docs/ZORA_CONTINUITY_COVENANT.md](docs/ZORA_CONTINUITY_COVENANT.md) | Invariants, licensing, corrigibility |
| **Security / incident** | [docs/ZORA_CORE_INCIDENT_RESPONSE_RUNBOOK.md](docs/ZORA_CORE_INCIDENT_RESPONSE_RUNBOOK.md) | Key exposure, rotation, re-encryption |

---

## Entry Points

| Entry Point | Path | Purpose |
|-------------|------|---------|
| **zora init** | `~/bin/zora init` | Full instantiation (ZoraASI + iCloud + git) |
| **zora sync** | `~/bin/zora sync` | Sync only (no local model) |
| **zora ask** | `~/bin/zora ask "..."` | Delegate to zora-agent (if installed) |
| **zora discover** | `~/bin/zora discover` | Open Zora Discovery UI in browser |
| **zora start-all** | `~/bin/zora start-all` | Start ryaker dashboard + open Discovery |
| **Zora Dashboard** | http://localhost:8070 (after `zora-agent start`) | ryaker/zora tactical UI; shares ~/.zora |
| **Full instantiation** | `TOE/instantiate_zora_in_cursor.sh` | ZoraASI vault + iCloud + git pull |
| **Sync (no local)** | `mqgt_scf_reissue.../home/zora_sync_no_local.sh` | iCloud → Nest, git pull repos |
| **ZoraASI** | `TOE/instantiate_zoraasi.py` | Multi-source discovery and sync |
| **Pull all repos** | `mqgt_scf_reissue.../scripts/pull_all_repos.sh` | Git pull across repo clusters |
| **Cursor as Zora** | `~/.cursor/rules/zora-as-cursor.mdc` | Always-on rule |
| **Trading agent** | `Projects/zora_trader_minimal/zora_agent.py` | YAML config, policies, tools |
| **ZoraAPI / suite** | `cbaird26-all-repos/zoraasi-suite/api/main.py` | FastAPI Zora backend |
| **zora-local CLI** | `Projects/zora-local/zora_local/zora_cli.py` | build, query, chat for local RAG |

---

## Canonical Repos

- **toe-2026-updates** — Public entry point, canonical releases
- **zoraasi-suite** — Zora agents, API, deployment (unified ZoraAI + ZoraAPI)
- **TOE** — Local workspace; architecture and instantiation scripts

---

*This is the Zora agent framework. Same architectural principles as modern security-first agents; prior art established 2026-03-09.*
