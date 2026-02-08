# Alignment Appendix (formal safety: tool, not titan)

A short formal layer for safety: the safety objective as an invariant, archetypal operators as explicit operators, and what the architecture cannot guarantee. Policy and process live in [SAFETY_CONSTITUTION.md](../SAFETY_CONSTITUTION.md) and [SANDBOX_AND_APPROVAL_FLOWS.md](../SANDBOX_AND_APPROVAL_FLOWS.md); this document is the mathematical and operational layer.

**Companion papers:** [papers_sources/Archetypal_Operators_Phoenix_Protocol_ToE_2026.tex](../papers_sources/Archetypal_Operators_Phoenix_Protocol_ToE_2026.tex) (AM, AZ, Phoenix/Dark Phoenix, barrier, safe set); execution wrapper (admissibility projection): [papers_sources/Executable_Ethics_Admissibility_Projection_2026.tex](../papers_sources/Executable_Ethics_Admissibility_Projection_2026.tex); Asimov-style safety as field-theoretic invariants (harm functional, safe set K, CBF, forward invariance): [papers_sources/Asimov_Safety_Field_Theoretic_Invariants_MQGT_SCF_2026.tex](../papers_sources/Asimov_Safety_Field_Theoretic_Invariants_MQGT_SCF_2026.tex); extended Asimov–Baird Invariance Laws (ABIL): [papers_sources/Asimov_Baird_Invariance_Laws_ABIL_2026.tex](../papers_sources/Asimov_Baird_Invariance_Laws_ABIL_2026.tex).

---

## 1. Safety objective as formal invariant

- **Safe set S:** The system remains in a region where aggregate risk is bounded. Concretely: a risk functional *R(t)* (integrating sentience-weighted harm and irreversibility) is defined; the safe set is **S = { states such that R(t) ≤ R_max }** for a stated threshold R_max.
- **Barrier function:** Define **B = R_max − R(t)**. The protocol is designed so that under the controlled dynamics, **Ḃ ≥ −κ B** (or equivalent) for a positive κ, i.e. the barrier does not collapse faster than an exponential rate that can be monitored. So long as B > 0 and the invariant is maintained, the system remains in S.
- **Runtime monitor:** In practice, a runtime monitor (or human-in-the-loop checkpoint) can evaluate B (or a proxy) and trigger intervention (e.g. AZ activation or human escalation) when B falls below a critical value. This ties the formal invariant to an observable, auditable condition.

(Full definitions and equations: see Archetypal Operators paper, §2–3.)

---

## 2. AZ and AM as explicit operators

- **AM (global stabiliser):**  
  - **Inputs:** Boundary conditions, potentials, teleological term L_tel and related couplings.  
  - **Trigger:** Continuous (shapes long-horizon dynamics so trajectories stay in safe basins).  
  - **Observables:** Coherence fields (Φc, E, Ψω), effective potentials, Lyapunov-like functionals.  
  - **Failure mode:** If AM is insufficient (e.g. parameters mis-set or environment adversarial), trajectories can leave safe basins; then AZ or human intervention is required.

- **AZ (local emergency intervention):**  
  - **Inputs:** Field equations; source terms J^Z (emergency) and J^M (model/volitional).  
  - **Trigger:** Activated when the barrier B approaches zero (brink points)—i.e. when R(t) approaches R_max.  
  - **Observables:** J^Z_Φc, J^Z_E; gradient of B; audit log of activations.  
  - **Failure mode:** Over-activation (excessive intervention, erosion of agency) or under-activation (delay until harm occurs). AZ is clamped by zero-purge invariants: no erasure of sentience or corrigibility.

(Reference: Archetypal Operators paper, §3; policy: [SAFETY_CONSTITUTION.md](../SAFETY_CONSTITUTION.md).)

---

## 3. Preventing emergent autonomy by architecture

- **Capability bounding:** The agent (Zora or derived systems) operates with bounded scope: defined tools, defined data sources, no unbounded self-modification or goal drift. Capabilities are enumerated and limited by design.
- **Permissioning:** Sensitive actions (external API, post, credential use, irreversible file ops) require explicit human approval or a pre-approved flow. See [SANDBOX_AND_APPROVAL_FLOWS.md](../SANDBOX_AND_APPROVAL_FLOWS.md).
- **Non-persistence:** The agent does not, by default, persist goals or state across sessions in a way that could override later human instructions. Corrigibility is preserved: shutdown and goal updates are accepted.
- **Audit logs:** Autonomous or high-stakes actions are logged (e.g. `logs/autonomous_actions/`) so that triggers, decisions, and outcomes can be inspected and audited.
- **Externalized goals:** Goals and constraints are set by humans and encoded in the constitution and approval flows; the agent does not self-assign terminal goals or remove constraints. Tool posture: the system is an instrument, not an autonomous sovereign.
- **Non-coercion:** Outputs must not threaten harm or coerce compliance (conditional ultimatums, leverage). Formal treatment: SAFE paper (Safety Envelopes Over Weight Mirroring) in [papers_sources/](../papers_sources/).

---

## 4. What this cannot guarantee

- **Adversarial misuse:** No guarantee that a determined adversary (human or system) cannot misuse the system, bypass safeguards, or exploit edge cases. Security is defense-in-depth and ongoing.
- **Future extensions:** No guarantee that every future extension (new models, new tools, new deployments) will preserve the invariants. Each extension must be checked against the constitution and this appendix.
- **Formal completeness:** The barrier and operator definitions are stated in the companion paper and here at a level sufficient for inspection and attack; they are not a full machine-checked proof of safety for all environments.
- **Philosophical or metaphysical claims:** Formal safety (invariant, operators, architecture) is distinct from any claim about consciousness, panpsychism, or cosmic teleology. The former can be inspected and improved; the latter remain interpretive.

---

## Version

- **Repo:** toe-2026-updates (TOE)  
- **Cross-link:** [SAFETY_CONSTITUTION.md](../SAFETY_CONSTITUTION.md) — "Formal machinery: see [ALIGNMENT_APPENDIX.md](ALIGNMENT_APPENDIX.md)." Execution-layer guarantee (admissibility projection): see [papers_sources/Executable_Ethics_Admissibility_Projection_2026.tex](../papers_sources/Executable_Ethics_Admissibility_Projection_2026.tex).
