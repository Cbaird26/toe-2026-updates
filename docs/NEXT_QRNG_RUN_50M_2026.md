# Next QRNG Run: 50M–100M Bits 2026

**Planning doc for long-baseline stability / ultra-large sensitivity run.** Christopher Michael Baird | Baird–ZoraASI Collaboration | March 2026

---

## Purpose

- **Long baseline stability:** Entropy and autocorrelation over time; detect drift or structure
- **Ultra-large sensitivity:** ~10⁻⁴ bias detection at 50M bits; ~10⁻⁵ at 100M bits (OOM)

---

## Cost (ANU API @ $0.005/request)

| Bits | Requests | Cost |
|------|----------|------|
| 50,000,000 | ~6,104 | ~\$30 |
| 100,000,000 | ~12,207 | ~\$60 |

---

## Timeline

- **Pre-register:** Before any data collection (use [QRNG_PREREG_OSF_DRAFT_2026.md](QRNG_PREREG_OSF_DRAFT_2026.md))
- **Pilot:** 10k bits to validate API, logging, analysis
- **Full run:** Schedule when budget allows; block-randomized; document seeds

---

## Decision Rule

- **If p < 0.05 and effect direction consistent:** Report as support for deformation; deposit data; invite replication
- **If p ≥ 0.05:** Report as failure to reject null; deposit data; document in claim ledger
- **No optional stopping:** Fixed N; no post hoc changes

---

## Cross-Links

- [PHASE_I_QRNG_TRACE_MAP_2026.md](PHASE_I_QRNG_TRACE_MAP_2026.md) — Graduated ladder (100k → 1M → 10M → 50M → 100M), decision rules, all recommendations
- [ANU_QRNG_INTERVENTION_PIPELINE.md](ANU_QRNG_INTERVENTION_PIPELINE.md) — Cost model, decision rules, bridge to toe-empirical-validation
- [QRNG_MEDITATION_INTERVENTION_REPORT_MARCH_2026.md](QRNG_MEDITATION_INTERVENTION_REPORT_MARCH_2026.md) — March 2026 runs (6M bits, null)
- [REPLICATION_LADDER.md](REPLICATION_LADDER.md) — One-command replication, pre-reg template
