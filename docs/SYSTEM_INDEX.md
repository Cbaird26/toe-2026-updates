# TOE system index (navigation)

This file is a **compact map of the repo**—where to start, where papers and builds live, and how to tidy generated files. It does not replace the full [README.md](../README.md) or [AGENTS.md](../AGENTS.md).

## Start here

| Need | Go to |
|------|--------|
| Human + agent onboarding | [AGENTS.md](../AGENTS.md) |
| Project overview, Zenodo, GitHub Pages | [README.md](../README.md) (ToE thesis Zenodo v258: [10.5281/zenodo.19325026](https://doi.org/10.5281/zenodo.19325026)) |
| **GitHub Pages hub + Foundation URL** | Live: [cbaird26.github.io/toe-2026-updates/](https://cbaird26.github.io/toe-2026-updates/) · flagship: […/theory-of-everything-foundation/](https://cbaird26.github.io/toe-2026-updates/theory-of-everything-foundation/) · checklist: [PAGES.md](PAGES.md) |
| Safety and logging rules | [SAFETY_CONSTITUTION.md](../SAFETY_CONSTITUTION.md) |
| Alignment one-pager | [ALIGN_ALL.md](ALIGN_ALL.md) |
| Codex / CI / H1 tests | [CODEX_HANDOFF.md](CODEX_HANDOFF.md) |
| March 2026 Finance OS / repo-boundary handoffs | [handoffs/2026-03/README.md](handoffs/2026-03/README.md) |
| `~/Downloads/` bundle discipline (canonical vs archives) | [DOWNLOADS_CANONICAL_LAYOUT.md](DOWNLOADS_CANONICAL_LAYOUT.md) |
| GitHub visibility audit (manual table; no API automation) | [GITHUB_REPO_VISIBILITY_AUDIT_2026.md](GITHUB_REPO_VISIBILITY_AUDIT_2026.md) |

## Papers and PDF order (March 2026 stack)

| Topic | Location |
|-------|-----------|
| Paper inventory and build notes | [papers_sources/README.md](../papers_sources/README.md) |
| Merge order + addendum choice (physics vs full) | [TOE_RECENT_WORK_STACK_2026.md](TOE_RECENT_WORK_STACK_2026.md) |
| Concatenate six PDFs into one file | `scripts/merge_toe_scientific_pdf_stack.sh` (see stack doc) |
| Referee-safe boundary | [PHYSICS_ONLY_SUBMISSION_PACKET_2026.md](PHYSICS_ONLY_SUBMISSION_PACKET_2026.md) |
| Phase II submission stack (Anchor, etc.) | [papers_sources/MQGT_SCF_Phase_II_2026/README.md](../papers_sources/MQGT_SCF_Phase_II_2026/README.md) |

## Build / refresh scripts (common)

| Output | Command |
|--------|---------|
| Recent work addendum PDF(s) | `bash scripts/build_toe_recent_work_addendum_pdf.sh` or `--physics` |
| H1 methods PDF | `bash scripts/build_h1_methods_pdf.sh` |
| Scalar Halo manifest + figures refresh | `bash scripts/scalar_halo_campaign/refresh_scalar_halo_campaign.sh` |
| Remove LaTeX junk under the repo (safe paths) | `bash scripts/cleanup_repo_artifacts.sh` (use `--dry-run` first) |

## Data trees

| Tree | Role |
|------|------|
| `data/zoraasi_export/` | ZoraASI vault (gitignored; see instantiate scripts) |
| `data/scalar_halo_campaign/` | Scalar Halo / Cosmic Piano campaign; [README](../data/scalar_halo_campaign/README.md), `artifact_manifest.csv` |
| `data/update_catalog/` | Machine-readable inventory of `~/Downloads/UPDATE` (see [README](../data/update_catalog/README.md)); run `scripts/update_folder_ingest.py` |
| `papers_sources/figures/` | Tracked figures for papers and gallery |

## Outside this repo (manual discipline)

See **[DOWNLOADS_CANONICAL_LAYOUT.md](DOWNLOADS_CANONICAL_LAYOUT.md)** for which trees are canonical versus snapshot bundles. Treat **Black-Book** (`mqgt_scf_reissue_*`) and **all-repos mirror** paths from [AGENTS.md](../AGENTS.md) / Cursor rules as separate sync surfaces; reorganize those only with a dedicated plan and backups.

## Cleaning up

- **Generated LaTeX:** aux, log, out, toc, synctex, fls, latexmk—see `scripts/cleanup_repo_artifacts.sh`. It skips `.git/`, virtualenvs, and `logs/`.
- **Large merged PDFs:** `papers_sources/TOE_scientific_stack_merged_*.pdf` is gitignored by default; delete locally if you need disk space.
