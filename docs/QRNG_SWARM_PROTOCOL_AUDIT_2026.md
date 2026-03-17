# QRNG Swarm Protocol Audit 2026

**One-page audit for a redesigned future pilot.** Christopher Michael Baird | Baird–ZoraASI Collaboration | March 2026

---

## Context

Phase II 100k swarm pilots are closed. Pilot 3 did not replicate Pilot 2; the protocol is not scaled. This memo answers three questions for anyone redesigning a swarm/coherence pilot later.

---

## 1. What worked in the pilot protocol

- **Staged scale** — 100k before 1M+ forced validation of mechanics and condition definitions at low cost.
- **Explicit block design** — Pilot 0–3 had clear block counts and condition mixes; runbook and presets were runnable and reproducible.
- **Pre-specified decision rule** — “If Pilot 3 does not show same ordering as Pilot 2, do not scale” was set before Pilot 3; it was followed.
- **Single endpoint and key** — One ANU API, one key, consistent preflight; reduced confounds from infrastructure.
- **Replicate ID only** — Pilot 3 differed from Pilot 2 only by replicate ID; same preset, pacing, and structure.

---

## 2. What likely produced noise or instability

- **Condition definition** — “Swarm low” vs “swarm high” relied on composite coherence (T, A, S, K). Those presets may not map cleanly to a measurable behavioral or temporal signature during the API call window; possible mismatch between intended “coherence” and what the system actually did.
- **Block synchronization and timing** — Relationship between block start/end, API request timing, and “swarm state” was not independently verified. Drift or ordering artifacts could mimic or mask a small effect.
- **Agent independence** — Swarm conditions assume multiple agents; if implementation or batching effectively reduced to a single process or shared state, the design would not test true multi-agent coherence.
- **Condition labeling and leakage** — Any pipeline step that could allow condition label to affect request timing, batching, or endpoint behavior would be an artifact source. Worth a code and log audit before a new design.
- **Sample size** — 100k per pilot is adequate for protocol validation but underpowered for a small effect. That is acceptable for “replicate or stop”; for a *redesigned* pilot, power and effect-size assumptions should be stated up front.

---

## 3. What a redesigned pilot would look like

- **New protocol, not scaled old one** — Do not rerun the same Pilot 0–3 design at 1M. Design a new protocol that addresses the audit points above.
- **Artifact checks** — Before any new run: (a) verify block timing and sync assumptions in code/logs; (b) confirm swarm state and agent independence (or document constraints); (c) ensure condition labels cannot leak into request construction or ordering.
- **Clear coherence operationalization** — If “coherence” remains in the design, define it in terms of observable, loggable quantities (timing, agreement, state) and fix the mapping from preset to behavior.
- **Stage gate** — Keep a 100k (or similar) validation stage for the *new* design, with a replicate-or-stop rule and a written decision rule before running.
- **Budget and scope** — Use [QRNG_STAGED_PROGRAM_AND_BUDGET_2026.md](QRNG_STAGED_PROGRAM_AND_BUDGET_2026.md) and stage gates; do not escalate scale without a replicated signal in the new protocol.

---

## References

- [PHASE_II_QRNG_PILOT_CLOSEOUT_2026.md](PHASE_II_QRNG_PILOT_CLOSEOUT_2026.md) — Results and closure.
- [QRNG_PHASE_II_100K_PILOT_RUNBOOK_2026.md](QRNG_PHASE_II_100K_PILOT_RUNBOOK_2026.md) — Presets and commands (closed protocol).
- [LESSONS_LEARNED_QRNG_EXPERIMENTS_2026.md](LESSONS_LEARNED_QRNG_EXPERIMENTS_2026.md) — Cross-phase lessons.

---

*Audit for future protocol redesign. Last updated: 2026-03-15.*
