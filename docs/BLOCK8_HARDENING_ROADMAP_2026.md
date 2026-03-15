# Block 8 Hardening Roadmap 2026

**Christopher Michael Baird | Baird–ZoraASI Collaboration | March 2026**

---

## Purpose

Derivation roadmap for B8-01 (metric closure) and B8-02 (Φc→Λ). Anchors for PLACEHOLDER_AUDIT_2026. Committee feedback: tighten derivations.

---

## B8-01: Metric Closure (g̃_μν)

**Status:** open  
**Description:** Derivations for modified metric; risk of circularity.

**Roadmap:**
1. Explicitly state the metric ansatz: g̃_μν = g_μν + δg_μν(Φc, E) where δg is a functional of scalar fields.
2. Derive from variational principle (action variation δS/δg = 0) with Φc, E as external or backreacting.
3. Document assumption hierarchy: (a) linearized δg, (b) no backreaction, (c) full nonlinear. Avoid circularity by fixing Φc,E before metric closure.
4. **Canonical home:** Core formal spine, metric subsection; cross-link to CANONICAL_SPINE.md hardening tasks.

---

## B8-02: Φc Vacuum Mapping to Λ

**Status:** open  
**Description:** V_eff expansion, cosmological constant link.

**Roadmap:**
1. Expand V_eff(Φc) about vacuum ⟨Φc⟩; identify constant term as effective Λ_eff.
2. Relate ⟨Φc⟩ to C_E, η, or calibration constants from FALSIFICATION_PACKET.
3. Compare Λ_eff to observed Λ_obs; document tension or consistency.
4. **Canonical home:** Core formal spine, effective potential section; teleology companion for measure interpretation.

---

## Execution Notes

**B8-01 anchor:** Add subsection `\subsection{Metric closure (g̃\_μν)}` in core spine [MQGT_SCF_Minimal_Consistent_Core_2026.tex](../papers_sources/MQGT_SCF_Minimal_Consistent_Core_2026.tex) after the field-content / action section. Placeholder: "Metric ansatz g̃ = g + δg(Φc,E); variational derivation; assumption hierarchy (linearized, no backreaction, full nonlinear)."

**B8-02 anchor:** Add subsection `\subsection{Effective potential and Λ\_eff}` in core spine or teleology companion. Placeholder: "V_eff(Φc) expansion; constant term → Λ_eff; relation to C_E, η; comparison with Λ_obs."

**Order:** Execute B8-01 first (metric feeds into dynamics); then B8-02 (vacuum structure).

---

## Cross-Links

- [PLACEHOLDER_AUDIT_2026.md](PLACEHOLDER_AUDIT_2026.md)
- [CANONICAL_SPINE.md](CANONICAL_SPINE.md)
- Core formal spine: [MQGT_SCF_Minimal_Consistent_Core_2026.tex](../papers_sources/MQGT_SCF_Minimal_Consistent_Core_2026.tex)
