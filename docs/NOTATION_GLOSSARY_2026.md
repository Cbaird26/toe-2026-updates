# Notation Glossary (2026)

**Purpose:** Disambiguate symbols that may otherwise cause units or interpretive confusion. The transcript recommended splitting overloaded E (field vs trajectory cost). This glossary makes the distinction explicit.

**Cross-links:** [CANONICAL_SPINE.md](CANONICAL_SPINE.md) | [MQGT_SCF_Minimal_Consistent_Core_2026.tex](../papers_sources/MQGT_SCF_Minimal_Consistent_Core_2026.tex)

---

## Physical fields

| Symbol | Meaning | Units / dimension |
|--------|---------|-------------------|
| **Φc(x)** or **\Phic** | Consciousness scalar field | mass (canonical) |
| **E(x)** or **\Eth** | Ethics scalar field | mass (canonical) |
| **χ(x)** | Alternative notation for ethics field (transcript); use if adopting chi to avoid E-overload | mass |

The physical fields enter the Lagrangian and equations of motion. They are *not* the same as trajectory-level functionals or branch scores.

---

## Trajectory-level and outcome-level quantities

| Symbol | Meaning | Relation to fields |
|--------|---------|-------------------|
| **J_E[Γ]** | Trajectory functional (ethical cost along path Γ) | Integrates over local functional of fields + trajectory state |
| **C[α]** | Alternative notation (transcript): dimensionless cost functional on histories | Equivalent role to J_E |
| **e(x,t)** | Local ethical density | e = 0.7 n(x,t) + 0.3 s(x,t) from observables |
| **E_R(t)** | Aggregate ethical resonance over region V | E_R = ∫_V e(x,t) d³x |
| **ΔE_a** | Branch score (outcome a vs baseline) | ΔE_a = E_R^(a)(t*) - E_R^baseline(t*) |
| **E_i** | Branch score for outcome i (normalized) | E_i = ΔE_i / C_E |

**Critical distinction:** E_i and E_R are *derived* from the estimator pipeline (observables n, s, weights, integration). They are *not* the same mathematical object as the field E(x). The field E(x) is a dynamical degree of freedom; E_i is a dimensionless branch weight used in the tilted Born rule.

---

## Deformation and coupling parameters

| Symbol | Meaning |
|--------|---------|
| **η** | Teleology tilt strength; η → 0 recovers standard Born weights |
| **C_E** | Calibration constant; E_i = ΔE_i / C_E |
| **γ_col** | Collapse strength in GKSL/Lindblad dissipator |
| **Γ** | Effective collapse rate (visibility: V/V₀ ≈ exp(-Γ T Δx²)) |

---

## Recovery limits (standard QM)

- **η → 0** or **ΔE_i → 0** or **C_E → ∞** ⇒ standard quantum mechanics
- **γ_col → 0** ⇒ unitary drift (no collapse deformation)
- **Portal couplings → 0** ⇒ GR+SM (new scalars decouple)
