# Downloads layout — canonical vs reference bundles (2026)

This note records **which local trees are treated as canonical** for active work, versus **read-only archives** that may duplicate Zenodo/GitHub content. It does **not** delete or move folders automatically.

## Canonical (authoritative working copies)

| Path | Role |
|------|------|
| `~/Downloads/TOE/` | **Primary ToE / MQGT-SCF git repo** (`cbaird26/toe-2026-updates` mirror). Papers, `docs/`, `scripts/`, `data/scalar_halo_campaign/` manifest discipline, H1 tooling. |
| `~/Projects/Cbaird26/` | Long-lived clones (e.g. ZoraAPI, MQGT theory) when present. |

## Reference / snapshot bundles (do not treat as “the repo”)

Multiple dated **`mqgt_*` / `mqgt_scf_reissue_*` / `mqgt_reissue_bundle_*` / `reissued_files *`** folders under `~/Downloads/` are typically **bundle exports or mirrors**. They are useful for diffing and provenance, but **day-to-day edits** should land in **TOE** (or the specific product repo), not spread across duplicate trees.

**Rule of thumb:** one logical change → one git repo → one commit path. Copy *from* bundles *into* TOE when promoting material.

## Black-Book nest (continuity)

Per project rules, the **Black-Book** path  
`~/Downloads/mqgt_scf_reissue_2026-01-20_010939UTC/`  
remains the **continuity / Zora nest** for sync scripts and canon material; it is not replaced by TOE.

## Optional hygiene (human-approved only)

- Periodically **zip** inactive bundle folders if you need disk space; keep at least one verified Zenodo/GitHub pointer for each published artifact.
- Do **not** bulk-delete sibling folders without checking for **untracked** work inside them.

## See also

- [SYSTEM_INDEX.md](SYSTEM_INDEX.md) — navigation inside this repo  
- [handoffs/2026-03/README.md](handoffs/2026-03/README.md) — March 2026 Finance OS handoffs (moved under `docs/handoffs/`)
