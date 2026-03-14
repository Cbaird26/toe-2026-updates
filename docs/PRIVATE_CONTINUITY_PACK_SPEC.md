# Private Continuity Pack Specification

This defines the continuity files that preserve long-term context without exposing private raw archives.

## Location Model

- Canonical live pack path (local only): `private_continuity/` at repo root
- Publicly tracked templates: `docs/continuity_pack_templates/`
- Rule: never commit live continuity files containing sensitive content

## Required Files (Live Pack)

- `CORE_IDENTITY.md`
- `DECISION_LOG.md`
- `ACTIVE_THREADS.md`
- `PRIVATE_CONTEXT_INDEX.md`
- `RECOVERY_RUNBOOK.md`

## Update Cadence

- After each major work session:
  - update `ACTIVE_THREADS.md`
  - append `DECISION_LOG.md`
- Weekly:
  - refresh `PRIVATE_CONTEXT_INDEX.md`
- Monthly:
  - verify `RECOVERY_RUNBOOK.md` still works
- Quarterly:
  - review `CORE_IDENTITY.md` for stale constraints

## Content Guardrails

- `PRIVATE_CONTEXT_INDEX.md` stores only metadata pointers, never raw private transcripts
- `DECISION_LOG.md` stores rationale summaries, not sensitive verbatim chat dumps
- `RECOVERY_RUNBOOK.md` references encrypted backup IDs and restore procedure only

## Session Rehydration Order

1. `CORE_IDENTITY.md`
2. `ACTIVE_THREADS.md`
3. latest entries in `DECISION_LOG.md`
4. `PRIVATE_CONTEXT_INDEX.md` references as needed
