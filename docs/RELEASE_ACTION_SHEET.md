# Release Action Sheet

**Purpose:** Ordered execution gates for canonical 2026 release. Execute in sequence.

---

## Gates

| # | Gate | Command / Action | Status |
|---|------|------------------|--------|
| 1 | Refresh repo list | `python scripts/fetch_cbaird26_all_repos.py` | — |
| 2 | Generate repo canonical map | `python scripts/generate_repo_canonical_map.py` | — |
| 3 | Licensing | Apply [REPO_LICENSE_CORRECTION_CHECKLIST.md](REPO_LICENSE_CORRECTION_CHECKLIST.md) to Tier 1 repos | — |
| 4 | Paper-doc alignment | Confirm each of Papers 1–7 (or 1–5) maps to single canonical LaTeX per [PAPER_BY_PAPER_CORRECTION_ROADMAP_2026.md](PAPER_BY_PAPER_CORRECTION_ROADMAP_2026.md) | — |
| 4a | Paper-by-paper correction pass | Run [PAPER_BY_PAPER_CORRECTION_ROADMAP_2026.md](PAPER_BY_PAPER_CORRECTION_ROADMAP_2026.md) checklist before reviewer-proof pass | — |
| 5 | Zenodo | Create/update deposits per [ZENODO_STRATEGY_2026.md](ZENODO_STRATEGY_2026.md) | — |
| 6 | Empirical | Hardware QRNG acquisition, artifact publication, external replication | — |
| 7 | Reviewer-proof pass | Run [REVIEWER_PROOF_CHECKLIST.md](REVIEWER_PROOF_CHECKLIST.md) before public push | — |
| 8 | Repo consolidation | Merge mqgt-* into toe-empirical-validation, archive duplicates | — |

---

## Quick Reference

- **Paper correction roadmap:** [PAPER_BY_PAPER_CORRECTION_ROADMAP_2026.md](PAPER_BY_PAPER_CORRECTION_ROADMAP_2026.md)
- **Paper guide:** [TOE_2026_UPDATED_PAPER_GUIDE.md](TOE_2026_UPDATED_PAPER_GUIDE.md)
- **Ecosystem map:** [TOE_ZORA_ECOSYSTEM_MAP.md](TOE_ZORA_ECOSYSTEM_MAP.md)
- **Canonical plan:** [CANONICAL_2026_RELEASE_PLAN.md](CANONICAL_2026_RELEASE_PLAN.md)
- **Repo map:** [REPO_CANONICAL_MAP.md](REPO_CANONICAL_MAP.md)
- **Project atlas:** [PROJECT_ATLAS.md](PROJECT_ATLAS.md)
- **Theory analysis:** [TOE_FRAMEWORK_REVIEWER_ANALYSIS.md](TOE_FRAMEWORK_REVIEWER_ANALYSIS.md)
