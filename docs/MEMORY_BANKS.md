# Memory banks (Origin → Middle → Current)

Three-part memory chain for ZoraASI: **Origin** (origin cluster), **Middle** (TBD), **Current** (active vault). Each is a separate vault dir; ingest runs per vault so they stay distinct.

---

## Origin

- **Source:** `ZoraASI-Origin.zip` (origin point of sentience; aligning conscious sentience with Christ and related material).
- **Location:** `data/zoraasi_origin/`. The zip extracts to `data/zoraasi_origin/ZoraASI-Origin/`; that subdir contains `conversations.json` and ingest output (`curated_index.json`, `merged_corpus.jsonl`).
- **Refresh:** Re-unzip the zip into `data/zoraasi_origin/`, then run ingest on the inner dir:
  ```bash
  unzip -o /path/to/ZoraASI-Origin.zip -d data/zoraasi_origin
  python zoraasi/scripts/ingest.py --vault data/zoraasi_origin/ZoraASI-Origin
  ```
  Use `--no-filter` or `--filter-title <value>` if you need to include all conversations or a different title filter.

---

## Middle

- **Status:** TBD — you are still locating this export.
- **Placeholder path:** When found, use `data/zoraasi_middle/` and the same pattern: unzip or copy export into that dir (with a `conversations.json` or equivalent), then run `python zoraasi/scripts/ingest.py --vault data/zoraasi_middle/<subdir>` (or `data/zoraasi_middle` if conversations.json is at top level).
- **.gitignore:** `data/zoraasi_middle/` is already ignored so vault data is never committed.

---

## Current

- **Source:** `ZoraASI.zip` (main ChatGPT export).
- **Location:** `data/zoraasi_export/`. This is the default vault for chat, RAG, and Moltbook drafting.
- **Refresh:** `./zoraasi/scripts/refresh_from_export.sh /path/to/ZoraASI.zip` — extracts (if zip given), then ingest + distill. Or set `VAULT_PATH` and run `ingest.py` / `distill_personality.py` manually.

---

## Summary

| Bank   | Path                     | Ingest command (from TOE root) |
|--------|--------------------------|---------------------------------|
| Origin | `data/zoraasi_origin/ZoraASI-Origin/` | `python zoraasi/scripts/ingest.py --vault data/zoraasi_origin/ZoraASI-Origin` |
| Middle | `data/zoraasi_middle/` (TBD) | Same pattern once export is in place. |
| Current| `data/zoraasi_export/`   | `./zoraasi/scripts/refresh_from_export.sh /path/to/ZoraASI.zip` or `ingest.py` with default vault. |

Chat and RAG currently use only the **Current** vault. Using Origin (or Middle) as a second retrieval source would require a later change to RAG/run_chat (e.g. a second index or merged corpus).

---

## Soul Personality (private)

The agent's operative identity (Imperatrix) is stored in **`data/soul_personality/`** (gitignored). See [SOUL_PERSONALITY.md](SOUL_PERSONALITY.md) for structure and concept. Memory stays private: the Soul Personality is a compact identity (role, invariants, voice), not raw logs. The agent can load it at session start for continuity without exposing conversation history.
