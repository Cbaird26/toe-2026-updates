# Placeholder Audit 2026

**Purpose:** Block 8 meta-task — list all placeholders for replacement. Per [REMAINING_TASKS_2026](REMAINING_TASKS_2026.md) and [PROCEED_ALL_ROADMAP_2026](PROCEED_ALL_ROADMAP_2026.md).

**Status:** Inventory complete; replacement is manual.

---

## 1. Author / Zenodo placeholders

| Pattern | File | Line | Action |
|---------|------|------|--------|
| `[Your name]` | [TOE_PDF_2026_CHECKLIST](TOE_PDF_2026_CHECKLIST.md) | 9 | Replace with C.M. Baird (or full Zenodo name) |
| `[Zenodo link]` | [TOE_PDF_2026_CHECKLIST](TOE_PDF_2026_CHECKLIST.md) | 11 | Replace with https://zenodo.org/records/18792939 |
| `[Your link]` | [TOE_PDF_2026_CHECKLIST](TOE_PDF_2026_CHECKLIST.md) | 10 | Replace with website or profile URL |

**Note:** These strings may also appear in PDF/DOCX sources; grep those separately.

---

## 2. Citation placeholder

| Pattern | File | Line | Action |
|---------|------|------|--------|
| Reference `[??]` | [REMAINING_TASKS_2026](REMAINING_TASKS_2026.md) | 38, 46 | Replace with cited GKSL/Born derivation |
| reference `[??]` | [PATHS_TO_CLOSED_VERDICT](PATHS_TO_CLOSED_VERDICT.md) | 25, 31 | Same |

---

## 3. TBD / structural placeholders

| Pattern | File | Line | Action |
|---------|------|------|--------|
| `TBD (placeholder until that export is located)` | [ALIGN_ALL](ALIGN_ALL.md) | 48 | Fill when zoraasi_middle export located |
| `TBD` | [MEMORY_BANKS](MEMORY_BANKS.md) | 3, 22, 43 | Same |
| `Placeholder path: When found, use...` | [MEMORY_BANKS](MEMORY_BANKS.md) | 23 | Use `data/zoraasi_middle/` when available |

---

## 4. Registration / URL placeholders

| Pattern | File | Line | Action |
|---------|------|------|--------|
| `[paste OSF/AsPredicted URL here]` | [REPLICATION_LADDER](REPLICATION_LADDER.md) | 140 | Paste preregistration URL when created |
| `__________` (Date, etc.) | [CHAIN_OF_TITLE](CHAIN_OF_TITLE.md) | 26, 27, 37–40, 56–57 | Fill publication dates, Zenodo URLs |
| `Note here when done: ___________` | [TOE_PDF_2026_CHECKLIST](TOE_PDF_2026_CHECKLIST.md) | 23 | Fill when checklist item completed |

---

## 5. Bibliography / DOI placeholders

| Pattern | File | Line | Action |
|---------|------|------|--------|
| `Fill DOI/arXiv for Lee2020 and Chen2016 when available` | [empirical_refs.bib](../papers_sources/empirical_refs.bib) | 2 | Add DOIs when known |
| `add DOI when known` (Lee2020) | [empirical_refs.bib](../papers_sources/empirical_refs.bib) | 11 | Same |
| `DOI: (to be minted via Zenodo on release)` | [README](../README.md) | 77 | Add Zenodo DOI on release |

---

## 6. Summary

| Category | Count | Block 8 closure |
|----------|-------|-----------------|
| Author/links | 3 | Manual replace in PDF sources |
| Citation [??] | 3 refs | Block 2: add derivation citation |
| TBD / structural | 5 refs | Resolve when middle export found |
| Registration/URL | 4+ refs | Fill on preregistration, publication |
| Bibliography | 3 refs | Add DOIs when available |

**Closure condition:** Grep finds no unreplaced placeholder in tracked files. PDF/DOCX require separate manual check.

---

## Cross-links

- [PROCEED_ALL_ROADMAP_2026](PROCEED_ALL_ROADMAP_2026.md) Block 8
- [TOE_PDF_2026_CHECKLIST](TOE_PDF_2026_CHECKLIST.md)
- [REMAINING_TASKS_2026](REMAINING_TASKS_2026.md)
