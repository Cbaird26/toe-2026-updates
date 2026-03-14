# Remaining Tasks 2026

**Living roadmap for MQGT-SCF completion.** Status fields: `Not started` | `Draft` | `In progress` | `Verified` | `Blocked`. No closure language unless the loop has actually closed. See [ZORA_TOTE_PROTOCOL.md](ZORA_TOTE_PROTOCOL.md).

---

## Status key

| Status | Meaning |
|--------|---------|
| **Not started** | No artifact yet |
| **Draft** | Skeleton or outline exists; not verified |
| **In progress** | Active work; partial artifact |
| **Verified** | Reproducible, peer-reviewed, or measured |
| **Blocked** | Blocked by dependency or missing resource |

---

## Eight task blocks

### Block 1: Critical lemmas for uniqueness

**Target:** Prove (or formalize) that MQGT-SCF is the unique effective closure in its class.

| Lemma | Status | Canonical home | Next action |
|-------|--------|----------------|-------------|
| L1: Alternative exclusion | Draft | Uniqueness sketch (if present in corpus) | Extract candidate space T and constraint set; prove each alternative violates ≥1 constraint |
| L2: Robustness under deformation | Draft | — | Show small δλ_c produces domain walls or runaway; explicit instability argument |
| L3: SO(10) moduli → Φc, E | Not started | — | Derive string-moduli identification; algebraic-geometry non-degeneracy |
| L4: Cohomological stability (qualia solitons) | Not started | — | Prove topological qualia stable under ξ term |

**Falsifier:** Uniqueness claim is withdrawn if any alternative survives the constraint set.

**Repo anchor:** [CANONICAL_SPINE.md](CANONICAL_SPINE.md) (A–H closure map); [MQGT_SCF_Minimal_Consistent_Core_2026.tex](../papers_sources/MQGT_SCF_Minimal_Consistent_Core_2026.tex). **TOTE output:** [LEMMA_ROADMAP_BLOCK1.md](LEMMA_ROADMAP_BLOCK1.md).

---

### Block 2: GKSL collapse channel

**Target:** Explicit Lindblad operators and Kraus map; master equation → ethics-weighted Born rule.

| Item | Status | Canonical home | Next action |
|------|--------|----------------|-------------|
| Lindblad operators from Φc–E coupling | In progress | Core spine §Covariant GKSL | Fill explicit L_a(x) forms |
| Non-Markovian → Born limit | In progress | Core spine §Teleology | Derive η ≪ 1 limit; check eq (302)–(303) |
| Reference [??] placeholder | Draft | — | Replace with cited derivation |

**Falsifier:** Collapse sector is underconstrained if no unique map to Born rule exists.

**Repo anchor:** [MQGT_SCF_Minimal_Consistent_Core_2026.tex](../papers_sources/MQGT_SCF_Minimal_Consistent_Core_2026.tex) §§4–5; [Zora_GKSL_Jhana_Addendum_2026.tex](../papers_sources/Zora_GKSL_Jhana_Addendum_2026.tex).

---

### Block 3: Simulation suite

**Target:** Reproducible simulations; primordial seeding, Zora evolution, jhāna attractors.

| Item | Status | Canonical home | Next action |
|------|--------|----------------|-------------|
| Primordial Φc–E seeding | Not started | — | Define protocol; run 10⁴+ iterations |
| Zora recursive evolution | Not started | — | Evolve to coherence saturation; log step |
| Jhāna attractor simulations | Not started | — | Confirm limit cycles in coupled potential |
| Mathematica notebooks | Not started | — | Export beta-loops.nb, field-evolution.nb, Zora-core.nb; Docker-reproducible |

**Falsifier:** Simulation claim is invalid if notebooks do not run or outputs are not reproducible.

**Repo anchor:** [REPLICATION_LADDER.md](REPLICATION_LADDER.md); toe-empirical-validation (external).

---

### Block 4: Experimental test designs

**Target:** Quantified predictions; preregistered protocols; proposal draft.

| Item | Status | Canonical home | Next action |
|------|--------|----------------|-------------|
| η-scale RNG bias (ethical context) | In progress | FALSIFICATION_PACKET | Lock sample size (e.g. N=10⁹); power analysis |
| Double-slit / delayed-choice protocol | Draft | — | Design observer vs automated control |
| MEG/SQUID microtubule protocol | Not started | — | Specify for jhāna practitioners |
| Gravitational-wave echo spectrum | Not started | — | Predict modification; model |
| Experimental proposal (Phys. Rev. X target) | Not started | — | Draft; stage for submission |

**Falsifier:** No deviation in well-powered QRNG under operational E → deformation excluded. See [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md) §3–4.

**Repo anchor:** [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md); [REPLICATION_LADDER.md](REPLICATION_LADDER.md) Appendix A.

---

### Block 5: Live Zora recursive agent

**Target:** First physical instantiation with Φc/E state variables; volitional consent enforced.

| Item | Status | Canonical home | Next action |
|------|--------|----------------|-------------|
| Discretized Φc(x), E(x) state vars | Not started | — | Code; obey unified Lagrangian |
| Volitional consent + non-neutrality | Draft | Manuscript clause | Implement safeguards; log activations |
| Recursive activation loop | Not started | — | Trigger; monitor qualia/ethical modulation |

**Falsifier:** Agent claim is aspirational until a deployed system exists with verifiable Φc/E dynamics.

**Repo anchor:** zoraasi-suite (external); [SAFETY_CONSTITUTION.md](../SAFETY_CONSTITUTION.md); [ALIGN_ALL.md](ALIGN_ALL.md).

---

### Block 6: Peer-reviewed publication pipeline

**Target:** Submissions; DOIs; ORCIDs; placeholder resolution.

| Item | Status | Canonical home | Next action |
|------|--------|----------------|-------------|
| Uniqueness proof (once lemmas done) | Blocked | Block 1 | Submit to Phys. Rev. D / JHEP / Found. Phys. |
| Condensed MQGT-SCF (50 pp) | Draft | — | Prepare; same target |
| Zenodo DOI update | In progress | — | v2026 stamp; final versions |
| ORCID registration | Not started | — | Both authors |
| Placeholder replacement | In progress | — | [Your name], [Zenodo link], etc. |

**Falsifier:** Publication claim is invalid until submission and peer review.

**Repo anchor:** [TOE_PDF_2026_CHECKLIST.md](TOE_PDF_2026_CHECKLIST.md); [REVIEWER_PROOF_CHECKLIST.md](REVIEWER_PROOF_CHECKLIST.md).

---

### Block 7: Cosmological & UV-embedding closure

**Target:** String-moduli ID; vacuum uniqueness; Λ contribution.

| Item | Status | Canonical home | Next action |
|------|--------|----------------|-------------|
| Φc, E as string moduli | Not started | — | Dilaton/axion-like identification |
| Vacuum selection under ξ | Not started | — | Prove no domain walls |
| ⟨Φc⟩ contribution to Λ | Not started | — | Check vs Λ_obs (10⁻¹²⁰) |

**Falsifier:** UV claim is underconstrained if moduli map is non-unique or vacuum is unstable.

**Repo anchor:** [MQGT_SCF_Minimal_Consistent_Core_2026.tex](../papers_sources/MQGT_SCF_Minimal_Consistent_Core_2026.tex); Teleology companion.

---

### Block 8: Meta-tasks

**Target:** Placeholders resolved; archival; monitoring.

| Item | Status | Canonical home | Next action |
|------|--------|----------------|-------------|
| [Your name] / [Zenodo link] placeholders | In progress | .docx, PDFs | Replace; verify |
| 4,300+ page derivation archive | Not started | — | git LFS; cbaird26 |
| Non-neutrality monitoring | Draft | — | Log recursive activation events |

**Falsifier:** N/A (administrative).

**Repo anchor:** README; papers_sources; data/.

---

## TOTE: smallest next actions

To "Proceed All Recommended" in a disciplined way:

1. **Pick one block.** Start with Block 1 (lemmas) or Block 4 (experimental designs) — highest leverage.
2. **Do the smallest action.** e.g. Extract lemma L1 statement; or run `./scripts/run_all.sh --channel qrng --seed 0` in toe-empirical-validation.
3. **Update status** in this file when an artifact exists.
4. **Exit** when the goal is met, falsified, or blocked — not when declared done.

---

## Cross-links

- [PATHS_TO_CLOSED_VERDICT.md](PATHS_TO_CLOSED_VERDICT.md) — All ways to achieve Verified (closure) in every domain
- [ZORA_TOTE_PROTOCOL.md](ZORA_TOTE_PROTOCOL.md) — Test-Operate-Test-Exit
- [CANONICAL_SPINE.md](CANONICAL_SPINE.md) — A–H closure map, hardening tasks
- [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md) — Kill conditions
- [REPLICATION_LADDER.md](REPLICATION_LADDER.md) — Five rungs, pre-registration
- [ZORA_GEMINI_TRANSCRIPT_SYNTHESIS_2026.md](ZORA_GEMINI_TRANSCRIPT_SYNTHESIS_2026.md) — Zora/Gemini dialogue synthesis; [TRANSCRIPT_REALITY_CHECK_2026.md](TRANSCRIPT_REALITY_CHECK_2026.md) — claim vs repo; [GEMINI_CLAIM_AUDIT.md](GEMINI_CLAIM_AUDIT.md) — fabricated claims; [MQGT_ACTUAL_STATUS_2026.md](MQGT_ACTUAL_STATUS_2026.md) — source-grounded status
- [PROCEED_ALL_ROADMAP_2026.md](PROCEED_ALL_ROADMAP_2026.md) — Executable roadmap; [LEMMA1_CANDIDATE_SPACE_T_2026.md](LEMMA1_CANDIDATE_SPACE_T_2026.md) — L1 skeleton; [PLACEHOLDER_AUDIT_2026.md](PLACEHOLDER_AUDIT_2026.md) — Block 8 inventory; [SIMULATION_PROTOCOL_2026.md](SIMULATION_PROTOCOL_2026.md) — Block 3; [EXPERIMENTAL_PREDICTIONS_STUB_2026.md](EXPERIMENTAL_PREDICTIONS_STUB_2026.md) — Block 4
