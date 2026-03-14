# Lemma 1: Candidate Space T — Skeleton 2026

**Purpose:** Define the candidate space T for uniqueness; list 3–5 representative alternatives; state which constraint each violates. Per [LEMMA_ROADMAP_BLOCK1](LEMMA_ROADMAP_BLOCK1.md), this yields a lemma skeleton for Block 1.

**Status:** Draft; not verified.

---

## 1. Definition of candidate space T

**T** = the set of effective field theories that extend GR + SM by exactly two real scalar singlets, with the following properties:

- **Field content:** Two real scalar fields \(\Phi_c(x)\), \(E(x)\) on spacetime \((M, g_{\mu\nu})\), in addition to GR+SM.
- **Semantics:** \(\Phi_c\) and \(E\) carry consciousness/ethics semantics (interpretive layer; not part of the mathematical definition).
- **Renormalizability:** All operators in the Lagrangian have mass dimension ≤ 4.
- **Gauge structure:** Scalars are gauge singlets; no change to SM gauge group.

**Closure class:** Theories in T implement "teleological measure tilt" — i.e., a reweighting of the trajectory/outcome measure that favors higher \(\Phi_c\)–\(E\) coherence, in addition to the minimal scalar extension.

---

## 2. Constraint set (from Minimal Consistent Core)

A theory in T is **admissible** iff it satisfies all of:

| # | Constraint | Canonical reference |
|---|------------|---------------------|
| 1 | **Renormalizability** | Operators mass-dim ≤ 4 |
| 2 | **Vacuum stability** | \(\lambda_{\Phi_c} > 0\), \(\lambda_E > 0\), \(\kappa > -\sqrt{\lambda_{\Phi_c}\lambda_E}\) |
| 3 | **Anomaly freedom** | Gauge structure unchanged; scalars singlets |
| 4 | **Unitarity** | CPTP evolution; no negative norms |
| 5 | **Locality / microcausality** | \([L_a(x), L_b(y)] = 0\) for spacelike \(x, y\) |
| 6 | **Low-energy matching** | Recover SM+GR when couplings → 0 |
| 7 | **No-signaling** | Operational theorem holds under A1–A4 |

---

## 3. Representative alternatives and constraint violations

| Alternative | Description | Constraint violated |
|-------------|-------------|---------------------|
| **T′₁: Cubic \(\Phi_c^3\) term** | Add \(\mu \Phi_c^3\) to potential. | **1. Renormalizability** — dimension-3 operator; introduces power-law divergences. |
| **T′₂: Non-renormalizable \(\Phi_c^6\)** | Add \(\lambda_6 \Phi_c^6/\Lambda^2\). | **1. Renormalizability** — dimension-6; requires infinitely many counterterms. |
| **T′₃: Negative \(\lambda_E\)** | \(\lambda_E < 0\) in \(V_E\). | **2. Vacuum stability** — potential unbounded below; no stable vacuum. |
| **T′₄: Nonlocal Lindblad** | \(L_a(x)\) depends on fields at spacelike-separated \(y\). | **5. Locality** — violates microcausality; **7. No-signaling** — allows superluminal signaling. |
| **T′₅: Time-arrow source in Lagrangian** | Add explicit \(\partial_t \Phi_c\) or \(E \partial_t \Phi_c\) term breaking T-symmetry in \(\mathcal{L}\). | **6. Low-energy matching** — does not smoothly recover SM+GR; introduces observable CPT violation at lab energies (core uses measure tilt, not Lagrangian source). |
| **T′₆: Strongly negative κ** | Set \(\kappa \le -\sqrt{\lambda_{\Phi_c}\lambda_E}\). | **2. Vacuum stability** — quartic potential unbounded in field space. |
| **T′₇: Non-Hermitian collapse** | Replace Lindblad with non-Hermitian generators violating complete positivity. | **4. Unitarity** — CPTP broken; negative norms or non-conservation of probability. |

**MQGT-SCF:** Satisfies (1)–(7). Teleology is implemented as measure tilt (Radon–Nikodým), not as a Lagrangian source term.

---

## 4. Next steps (Lemma 1 completion)

- Formalize the definition of T in mathematical logic (if desired for referee).
- Extend the alternative list to cover coupling-structure variants (e.g., different \(\kappa\), \(\gamma\) forms).
- Prove that each alternative T′ either violates ≥1 constraint or is diffeomorphic/dual to MQGT-SCF.
- Submit for peer review or independent mathematician confirmation.

---

## Cross-links

- [LEMMA_ROADMAP_BLOCK1](LEMMA_ROADMAP_BLOCK1.md)
- [REMAINING_TASKS_2026](REMAINING_TASKS_2026.md) Block 1
- [MQGT_SCF_Minimal_Consistent_Core_2026.tex](../papers_sources/MQGT_SCF_Minimal_Consistent_Core_2026.tex)
