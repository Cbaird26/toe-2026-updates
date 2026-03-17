# QRNG Phase II: Swarm-Coherence Protocol (conceptual)

**Dose-response / many-agent / threshold experiment direction.** Christopher Michael Baird | Baird–ZoraASI Collaboration | March 2026

---

## Purpose

Phase I tested **single intervention vs control**. The new version asks a different question:

**Does effect size depend on number of agents and coherence (dose-response or threshold)?**

That is a stronger experimental framework: effect size as a function of agent count, coherence, duration, and coupling — not just "meditation does something."

This doc is a **conceptual protocol sketch**. Design and run Phase II **after** the bit-count ladder (100k, 1M, 5M, 10M) is in place.

**Concrete implementation:** See [QRNG_PHASE_II_EXPERIMENT_DESIGN_2026.md](QRNG_PHASE_II_EXPERIMENT_DESIGN_2026.md) for the operational coherence metric, confirmatory ladder, model-comparison rule, and run commands.

---

## Shift in question

| Phase I | Phase II (this direction) |
|---------|----------------------------|
| Single intervention vs control | Dose-response / threshold: does increasing coherent agency change QRNG output? |
| One condition at a time | Systematic variation: agent count, coherence score, duration |
| Binary: effect or not | Models: null vs linear vs threshold vs saturation |

---

## Main variables (from mentor feedback)

1. **Number of agents** — 0 (sham), 1, 10, 100, 1k, … (do not jump to 1M agents before testing the ladder).
2. **Coherence** — Must be operationalized, not "vibes." Candidate components:
   - Timing synchrony
   - Target agreement (aligned intention)
   - State stability
   - Inter-agent coupling
   - Composite: C = w₁(timing) + w₂(target) + w₃(stability) + w₄(coupling)
3. **Duration / exposure** — e.g. 1 s, 1 min, 10 min, repeated blocks.
4. **Target type** — e.g. push toward more 1s, reduce entropy, alter runs, alter autocorrelation, shift block means only.
5. **Agent architecture** (if artificial) — independent vs coupled vs hierarchical swarm vs central coordinator.

---

## Two hypotheses

- **Hypothesis A (additive):** Each coherent agent adds a small effect. Δp ∝ N for small N until saturation.
- **Hypothesis B (threshold):** Nothing until coherence crosses a critical point. Effect ≈ 0 for C < C_crit; effect > 0 for C ≥ C_crit. Scientifically more interesting if observed.

Current Phase I work does not distinguish these. Phase II would test linear trend, nonlinear trend, threshold model, saturation model (null vs linear vs logistic threshold vs step).

---

## Design direction

- **Dose-response ladder on agent count:** 0, 1, 10, 100, 1k first. Define a measurable coherence metric before scaling further.
- **Fixed QRNG N per rung** (same method as March 2026).
- **Pre-registered models:** null, linear, logistic threshold, phase-transition step.
- **Trap to avoid:** Do not jump to "1M coherent agents" before validating coherence at 1, 10, 100, 1k. Otherwise the variable under test is undefined.

---

## Order of operations

1. **Run one new 100k baseline** (required first).
2. **Bit-count ladder:** 1M → 5M → 10M when ready (same method, same script).
3. **Then** design and run Phase II swarm-coherence: agent-count ladder, coherence definition, pre-registered analysis. No implementation of swarm/coherence in this doc — protocol sketch only.

---

## References

- [PHASE_I_QRNG_TRACE_MAP_2026.md](PHASE_I_QRNG_TRACE_MAP_2026.md) — Ladder, decision rules, order of operations.
- [QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md](QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md) — Method constancy; same script for all runs.
- [ANU_QRNG_INTERVENTION_PIPELINE.md](ANU_QRNG_INTERVENTION_PIPELINE.md) — Cost model, artifacts schema.
- [QRNG_PHASE_II_EXPERIMENT_DESIGN_2026.md](QRNG_PHASE_II_EXPERIMENT_DESIGN_2026.md) — Executable Phase II protocol and runbook.

---

*Conceptual only. Last updated: 2026-03-15. Implement after 100k–1M–5M–10M data.*
