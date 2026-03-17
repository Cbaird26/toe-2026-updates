# QRNG Staged Program and Budget 2026

**Single reference: how we run the QRNG program without blowing finances.** Christopher Michael Baird | Baird–ZoraASI Collaboration | March 2026

This is a **staged quantitative experimental program with theoretical scaffolding**. It is not yet mixed methods (that would require formal phenomenology, interviews, or subjective ratings analyzed alongside QRNG outcomes).

---

## 1. Three lanes (keep them separate)

| Lane | Question | Status |
|------|----------|--------|
| **Lane 1 — Measurement** | Is the QRNG pipeline stable, reproducible, and cheap? | Stay boring. Already going well: ANU pipeline, baseline, cost model, preflight. |
| **Lane 2 — Confirmatory** | Is there a measurable effect under a pre-registered protocol? | Fixed N, no optional stopping, one primary outcome. This is where money can burn if you scale without decision rules. |
| **Lane 3 — Exploratory / Phase II** | What new hypotheses are worth testing now that QRNG works? | Coherence, agent swarms, dose-response, threshold, artificial sentience. Must not drain budget until Lane 2 has a stopping rule. |

---

## 2. Stage gates (each step earns the next)

- **Stage A — Finish the cheap ladder:** 1M, 5M, 10M. Low cost; answers pipeline stability and whether any effect appears at scale. See [PHASE_I_QRNG_TRACE_MAP_2026.md](PHASE_I_QRNG_TRACE_MAP_2026.md) for ladder and order of ops.
- **Stage B — Pause and evaluate after 10M:** Do not auto-escalate. Ask: consistent effect? Stable direction? Meaningful p? Effect above noise? If basically no, do not rush to 50M/100M.
- **Stage C — Then choose branch:**
  - **Branch 1 (deeper confirmatory):** If hint of something real → 50M, maybe 100M, same design, no new hypotheses midstream.
  - **Branch 2 (Phase II exploratory):** If simple effect stays null → close Phase I as documented null; move to agent count, coherence, threshold, artificial-sentience protocol at **100k first** (tiny lab rat), then scale only if protocol and direction justify it.

---

## 3. Budget rule

- **Hard rule:** Do not spend 50M/100M money unless 10M gives a reason. More bits on a null just buy a more precise null — useful science but a conscious choice, not drift.
- **Stage A cap:** Finish 1M / 5M / 10M only (already cheap).
- **Stage C cap:** Unlock 50M/100M or Phase II swarm only if Stage B justifies it.

---

## 4. Methodological principles (from mentor)

- **One primary hypothesis at a time.** Phase I: control vs intervention. Phase II: effect as function of coherence/agent count. Do not test meditation, coherence, agent count, ethics, E-labels, and sentience all at once.
- **Separate confirmatory from exploratory.** Confirmatory = pre-registered, fixed design, one main question. Exploratory = protocol pilot, model-building, theory-generating. Both valuable; mixing them causes wobble.
- **Let null results count.** A good null means: pipeline works, effect smaller than sensitivity, hypothesis needs revision, you are not fooling yourself. That is real progress.

---

## 5. Phase II at 100k first (swarm/coherence pilot)

- **Purpose:** Test protocol mechanics and whether coherence is measurable; **not** to detect ultra-tiny effects. "Tiny lab rat first, kaiju later."
- **Suggested 100k design:** 10 blocks × 10,000 bits (e.g. 4 control, 3 low-coherence, 3 high-coherence); conditions randomized; ~20 requests total; one endpoint, preflight, gentle pacing (no fallback).
- **Coherence (operational):** Low = same goal, independent/async, weak shared state. High = shared target, synchronized timing, shared state/coordinator. Define a simple score (e.g. synchrony + target agreement + shared-state level) before collection.
- **Pilot ladder:** Pilot 0 = control 100k; Pilot 1 = single-agent vs control 100k; Pilot 2 = low- vs high-coherence swarm 100k; Pilot 3 = repeat cleanest design. Only if effect direction is stable, scale to 1M then 10M. Do **not** start at "1M agents" — test 1, 10, 100, maybe 1k at the protocol level first.
- **Exact commands / manifests:** Use [QRNG_PHASE_II_100K_PILOT_RUNBOOK_2026.md](QRNG_PHASE_II_100K_PILOT_RUNBOOK_2026.md) and `scripts/qrng_phase2_pilot.py`.

---

## 6. API keys

- One paid key is enough. No need to keep making new keys for 100k/1M/10M/swarm pilots. Use one endpoint, preflight before runs; existing runner already uses `--preflight --no-fallback`.

---

## 7. One-line summary

*Finish the cheap ladder (1M, 5M, 10M), close Phase I honestly if it stays null, then move to a pre-registered Phase II threshold/coherence design at 100k first — instead of endlessly scaling the same null experiment. That protects both science and wallet.*

---

## References

- [PHASE_I_QRNG_TRACE_MAP_2026.md](PHASE_I_QRNG_TRACE_MAP_2026.md) — Ladder, order of operations, decision rules.
- [QRNG_PHASE_II_SWARM_COHERENCE_PROTOCOL_2026.md](QRNG_PHASE_II_SWARM_COHERENCE_PROTOCOL_2026.md) — Phase II variables, hypotheses A/B, design direction.
- [QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md](QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md) — Method constancy; same script for all runs.

---

*Last updated: 2026-03-15. Single reference for "how we do this without blowing finances."*
