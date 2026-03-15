# Evidence Registry 2026 (Robust Non-QRNG Campaign)

## Purpose

This registry tracks external evidence pulled during campaign hardening and assigns admissibility tiers for hypothesis decisions.

## Tiering policy

- **Tier A (decisive):** peer-reviewed experimental/lab constraints with clear methods and uncertainty reporting.
- **Tier B (supporting):** preprints or method papers that inform sensitivity design, confounder controls, or analysis robustness.
- **Tier C (context only):** open-source contextual signals; non-decisive and never used alone for falsification/survival claims.

## Registry entries

| ID | Tier | Topic | Source | URL | Use in campaign |
| --- | --- | --- | --- | --- | --- |
| EV-A-001 | A | Fifth-force bounds via neutron star cooling | SCOAP3 / arXiv-backed publication summary (2025) | https://repo.scoap3.org/records/102777 | H3 external coupling exclusion envelope |
| EV-A-002 | A | Solar-system fifth-force constraints | EPJ C (2024) scalar-tensor analysis | https://epjc.epj.org/articles/epjc/abs/2024/04/10052_2024_Article_12723/10052_2024_Article_12723.html | H3 prior/bound calibration |
| EV-B-001 | B | Bayesian inference design for near-field collapse tests | near-field interferometry method paper | https://cronfa.swan.ac.uk/Record/cronfa66604/Download/66604__30904__ad355ba4fa3b4c638b22b3e08466d3c2.pdf | H2 detectability and sample-size design |
| EV-B-002 | B | Timing noise and visibility thresholds | arXiv (2025) gravity-mediated entanglement timing noise | https://www.arxiv.org/pdf/2511.11879 | H2 confounder matrix for drift/noise |
| EV-B-003 | B | Randomness test standards | NIST SP 800-22 test suite | https://www.nist.gov/publications/statistical-test-suite-random-and-pseudorandom-number-generators-cryptographic | H1 non-QRNG robustness methodology |
| EV-B-004 | B | Data leakage inflation risk | Nature Mental Health (2025) data leakage analysis | https://www.nature.com/articles/s41380-025-03336-y | H1/H3 leakage controls and reporting gates |
| EV-B-005 | B | Preregistration templates and standards | OSF/COS preregistration guidance | https://help.osf.io/article/229-select-a-registration-template | H1/H2/H3 prereg completeness |
| EV-C-001 | C | Open contextual signals for horizon scanning | broad web search outputs and non-peer contextual feeds | internal notes only | non-decisive context; never primary evidence |

## Admissibility rules

1. Tier A/B only can influence formal decision gates.
2. Tier C is context and hypothesis-generation only.
3. Any citation used in claims must include URL + retrieval date.
4. Conflicts between sources are logged in the ingest memo before interpretation.

## Audit packet

- Hash manifest and local archive references: [EVIDENCE_AUDIT_PACKET_2026.md](EVIDENCE_AUDIT_PACKET_2026.md)
- Local archive directory: `docs/evidence_archive/`

## Retrieval window

- Initial pull date: 2026-03-03 UTC.
- Update cadence: weekly during active campaign; monthly otherwise.
