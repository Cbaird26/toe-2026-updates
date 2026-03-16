# Phase I QRNG Results Summary

**Christopher Michael Baird | Baird–ZoraASI Collaboration | March 2026**

Short summary for ToE corpus or Zenodo deposit. Tells the whole story in one place.

---

## What was done

Phase I tested whether meditation (or focused ethical intention) during QRNG collection produces measurable deviation from standard quantum randomness, as suggested by the MQGT-SCF ethics-weighted collapse channel. The design was block-randomized control vs intervention, with permutation testing on block means.

**Scale:** 6 million bits total, in three independent runs of 2M bits each (20 blocks × 100k bits per run). Block order was randomized (seeds 42, 123, 456). Single ANU API endpoint; no fallback.

**Pipeline:** ANU Quantum Random Numbers API → raw bits → block summaries → bias, runs, entropy, autocorrelation tests → permutation test on control vs intervention block means (10k permutations).

---

## Result

Control and intervention blocks showed **no statistically significant difference** (pooled permutation p = 0.41). Observed differences were consistent with binomial variation. Run 3 showed a sign flip (intervention slightly below control), as expected under the null when no real effect exists.

---

## Phase I close-out statement

*Phase I QRNG experiments (March 2026) collected 6 million bits across three independent intervention sessions using a block-randomized design. Control and intervention blocks showed no statistically significant difference (pooled permutation p = 0.41). Observed differences were consistent with binomial variation. The pipeline, statistical test suite, and replication protocol were validated. Phase I therefore concludes that no detectable effect was observed at the current sensitivity level.*

**Interpretation:** No detectable intervention effect was observed within the sensitivity limits of the experiment.

---

## Ladder and next steps

Sensitivity scales with bit count. The planned progression is:

| Bits | Approx. cost | Approx. detectable bias |
|------|--------------|--------------------------|
| 100k | $0.07 | ~1×10⁻³ |
| 1M | $0.62 | ~3×10⁻⁴ |
| 10M | $6.11 | ~1×10⁻⁴ |
| 50M | ~$30 | ~4×10⁻⁵ |
| 100M | ~$60 | ~3×10⁻⁵ |

Phase I closed at the 100k-block level (6M bits). Optional next steps: pre-register at OSF, then run 1M → 10M → 50M → 100M as budget allows, with decision rules (advance if pipeline and baseline pass; optionally stop if effect size < 10⁻⁴ and p > 0.1 across ≥3 runs). See [PHASE_I_QRNG_TRACE_MAP_2026.md](PHASE_I_QRNG_TRACE_MAP_2026.md) and [ANU_QRNG_INTERVENTION_PIPELINE.md](ANU_QRNG_INTERVENTION_PIPELINE.md).

---

## Phase II

Phase II — **Mankind and Artificial Sentience** — is a new line of inquiry (artificial sentience experiments, consciousness protocol, AI-related empirical work), not an extension of the QRNG campaign. Phase I closure is complete at the current sensitivity level.

The QRNG Phase II exploratory swarm pilots (Pilot 0–3 at 100k bits) were run and closed with no reproducible effect; Pilot 3 did not replicate Pilot 2’s ordering. See [PHASE_II_QRNG_PILOT_CLOSEOUT_2026.md](PHASE_II_QRNG_PILOT_CLOSEOUT_2026.md) for protocol, results, decision rule, and closure.

---

## References

- [QRNG_MEDITATION_INTERVENTION_REPORT_MARCH_2026.md](QRNG_MEDITATION_INTERVENTION_REPORT_MARCH_2026.md) — Full March 2026 report.
- [PHASE_I_QRNG_TRACE_MAP_2026.md](PHASE_I_QRNG_TRACE_MAP_2026.md) — All recommendations, ladder, designs, decision rules.
- [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md) — E definition, QRNG falsification criterion.
- [REPLICATION_LADDER.md](REPLICATION_LADDER.md) — One-command replication, pre-registration.

---

*One- to two-page summary for corpus or Zenodo. Last updated: 2026-03-15.*
