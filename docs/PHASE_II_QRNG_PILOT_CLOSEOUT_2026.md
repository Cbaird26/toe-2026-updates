# Phase II QRNG exploratory pilot close-out 2026

**Documents the 100k swarm/coherence pilot sequence and its closure.** Christopher Michael Baird | Baird–ZoraASI Collaboration | March 2026

---

## Purpose

This note records the Phase II QRNG exploratory pilots (Pilot 0–3) at 100k bits: protocol, results, pre-specified decision rule, and closure. No reproducible swarm effect was detected; the pilot sequence is closed without scaling to 1M+.

---

## Protocol

- **Scale:** 100k bits per pilot. Single ANU endpoint, paid key, preflight, no fallback. See [QRNG_PHASE_II_100K_PILOT_RUNBOOK_2026.md](QRNG_PHASE_II_100K_PILOT_RUNBOOK_2026.md) for presets and exact commands.
- **Pilot 0:** Control only (10 blocks × 10k bits).
- **Pilot 1:** Single-agent vs control (5 control + 5 single-agent blocks, randomized).
- **Pilot 2:** Swarm low vs high (4 control + 3 swarm_low + 3 swarm_high blocks, randomized).
- **Pilot 3:** Replicate 2 of Pilot 2 — same design, block structure, endpoint, key, pacing; new replicate ID only.

---

## Results

| Pilot | Purpose | Ordering (condition means) | Result |
|-------|---------|---------------------------|--------|
| Pilot 0 | Control sanity check | — | Null (as expected) |
| Pilot 1 | Single-agent vs control | — | Null |
| Pilot 2 | Swarm exploration | swarm_low > control > swarm_high (control ~0.4989, swarm_low 0.5047, swarm_high ~0.4985) | Exploratory hint |
| Pilot 3 | Replication of Pilot 2 | control > swarm_low > swarm_high (control 0.5027, swarm_low 0.4978, swarm_high 0.4956) | Non-replication |

**Critical comparison:** In Pilot 2, swarm_low was highest; in Pilot 3, swarm_low was below control. That reversal is a classic signature of random fluctuation rather than a real effect.

---

## Decision rule and outcome

**Pre-specified rule:** If Pilot 3 does not show the same directional ordering as Pilot 2, treat Pilot 2 as noise/artifact and do not scale. If Pilot 3 does show the same ordering, run Pilot 4 (replicate 3) before any escalation.

**Outcome:** Pilot 3 did not replicate Pilot 2. Per the rule: Pilot 4 was not run; no escalation to 1M or 10M. The 100k swarm pilot sequence is closed.

---

## Conclusion

No reproducible swarm effect was detected at the 100k level. The Pilot 2 separation (swarm_low > control > swarm_high) is consistent with statistical noise or protocol artifacts. Phase II 100k exploratory pilot sequence is therefore closed.

---

## What worked

The process followed sound experimental practice:

- Baseline validation
- Exploratory pilot with defined conditions
- Replication before scaling
- Predefined decision rule
- Stopping when replication failed

The QRNG pipeline and experimental discipline were validated even though the hypothesis did not show an effect.

---

## Future (optional)

If Phase II swarm/coherence work continues, the recommended next step is not to scale this protocol but to:

- **Protocol audit:** Inspect possible artifact sources (block synchronization timing, swarm state definition, agent independence assumptions, API batching structure, condition labeling leakage).
- **New pilot protocol:** Design a new pilot protocol rather than scaling one that already failed replication. Scaling a protocol that failed replication rarely teaches anything new.

---

## References

- [QRNG_PHASE_II_100K_PILOT_RUNBOOK_2026.md](QRNG_PHASE_II_100K_PILOT_RUNBOOK_2026.md) — Presets, commands, decision rule.
- [QRNG_STAGED_PROGRAM_AND_BUDGET_2026.md](QRNG_STAGED_PROGRAM_AND_BUDGET_2026.md) — Stage gates, budget rule.
- [PHASE_I_RESULTS_SUMMARY_2026.md](PHASE_I_RESULTS_SUMMARY_2026.md) — Phase I close-out (null).
- [PHASE_I_QRNG_TRACE_MAP_2026.md](PHASE_I_QRNG_TRACE_MAP_2026.md) — Ladder, decision rules, doc map.

---

## Version control

Closure and follow-up are recorded on `main` in the TOE repo:

- **Close-out commit:** `c5e6886` — Close Phase II QRNG 100k swarm pilot: non-replication of Pilot 2 signal; protocol closed with no scaling.
- **Follow-up commit:** `4c4d866` — Add QRNG swarm protocol audit and lessons learned notes.

Use these hashes when citing the archived closure in the corpus or final report.

---

*Close-out for Phase II QRNG exploratory pilots. Last updated: 2026-03-15.*
