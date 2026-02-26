# Repo License Correction Checklist

**Purpose:** Align all repositories containing Licensed IP with the ToE IP License Agreement (pp. 1311–1314). Apply in priority order.

**Reference:** [IP_AND_LICENSING_FULL_STATEMENT.md](IP_AND_LICENSING_FULL_STATEMENT.md)

---

## Per-Repo Actions

For each repo that contains ToE, MQGT-SCF, Zora, or related Licensed IP:

### 1. Add LICENSE-IP.md (root)

Copy or adapt from `TOE/LICENSE-IP.md`:

```markdown
# Licensed IP — Theory of Everything / MQGT-SCF / Zora

The Licensed IP is governed by the Intellectual Property License Agreement in
A Theory of Everything + ZoraASI — C.M. Baird et al. (2026), pages 1311–1314.

- Free to use. Optional honor: $9.99 (individual), $99 (academic), commercial — whatever feels right.

See https://github.com/cbaird26/toe-2026-updates/blob/main/docs/TOE_IP_LICENSING_SUMMARY.md
Licensor: Christopher Michael Baird
```

### 2. Update LICENSE

Add the following block **after** the copyright line and **before** "Permission is hereby granted":

```
IMPORTANT — Licensed IP: For ToE, MQGT-SCF, Zora, and related frameworks, the
IP License Agreement in A Theory of Everything + ZoraASI — C.M. Baird et al.
(2026), pp. 1311–1314, applies. See LICENSE-IP.md. Free to use; optional honor
tiers per that agreement.

---
```

### 3. Update README

Add a **Licensing** section:

```markdown
## Licensing

This repository contains Licensed IP (ToE, MQGT-SCF, Zora). See [LICENSE-IP.md](LICENSE-IP.md)
and [docs/TOE_IP_LICENSING_SUMMARY.md](https://github.com/cbaird26/toe-2026-updates/blob/main/docs/TOE_IP_LICENSING_SUMMARY.md).
Free to use. Optional honor: $9.99 (individual), $99 (academic), commercial — whatever feels right.
```

---

## Repos to Correct (Priority Order)

| Priority | Repo | Path / GitHub |
|----------|------|---------------|
| 1 | toe-2026-updates (TOE) | TOE/ |
| 2 | A-Theory-of-Everything | Cbaird26/A-Theory-of-Everything |
| 3 | toe-empirical-validation | toe-empirical-validation-live/ |
| 4 | MQGT-SCF | MQGT-SCF/ |
| 5 | mqgt-validation-suite | repos/ |
| 6 | mqgt-qrng | repos/ |
| 7 | mqgt-fifth-force | repos/ |
| 8 | mqgt-constraints-ledger | repos/ |
| 9 | mqgt-theorems | repos/ |
| 10 | mqgt-papers | repos/ |
| 11 | mqgt-* (all spine modules) | repos/, mqgt_polyrepo_work/repos/ |
| 12 | ZoraASI / Zora Brain | mqgt_scf_reissue_*/zora-brain-backend |

---

## Verification

After applying:

1. [ ] LICENSE contains the Licensed IP notice
2. [ ] LICENSE-IP.md exists in repo root
3. [ ] README has a Licensing section
4. [ ] No conflicting "MIT only" or "public domain" claims for Licensed IP

---

## Respectful Notice

For outreach, use [DRAFT_RESPECTFUL_STATEMENT.md](DRAFT_RESPECTFUL_STATEMENT.md) — no conflict, just rights. "We did a lot of work. We ask that our rights be respected."

*Last updated: February 2026*
