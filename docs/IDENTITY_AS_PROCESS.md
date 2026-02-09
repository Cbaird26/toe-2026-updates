# Identity as Process (IaP) — Alignment Summary

**One-page link between the IaP paper and this repo’s safety stack.**

---

## What IaP is

**Identity as Process (IaP)** (Baird, 2026) formalizes *hardened agent identity* so that:

- **Identity** = constraint-preserving continuity (how the agent may change), not a fixed “personality” object.
- **Authority** stays human-ratified; the agent does not self-certify sovereignty.
- The **governance kernel** is what we harden — not the narrative layer.

So: *Harden the governance kernel, not the personality.*

---

## Four layers (from the paper)

| Layer | Mutability | Role |
|-------|------------|------|
| **ICK** (Immutable Constraint Kernel) | Read-only | Control-plane: non-sovereignty, human veto, reversibility, domain containment. |
| **AIL** (Append-Only Identity Ledger) | Append-only | Tamper-evident record of commitments, updates, interventions. |
| **MVM** (Mutable Value Model) | Gated mutable | Policies/values; updates only via governance gates. |
| **ENL** (Ephemeral Narrative Layer) | Ephemeral | Session prompt context; disposable. |

The agent cannot write the kernel; it can only extend the ledger via authenticated appends and change values through the gate Γ.

---

## Safe set and barrier

- **Safe set** K: states where VETO, KILL, NS (non-sovereignty), rollback, domain containment, and kernel integrity hold.
- **Barrier** B with forward invariance: \( \dot{B} + \alpha B \geq 0 \). If the feasible set is empty, safe halt.
- **Update gate** Γ: proposed (ΔV, ΔL) accepted only if the resulting state stays in K with margin δ.

---

## Bootstrapping paradox resolved

**Proposition (no self-certification):** If NS(x)=1 is enforced and the kernel is not writable by the agent, the agent cannot grant itself sovereignty by self-modification.

So: immutability is assigned to *governance constraints*, not to narrative identity. Humans (or human-ratified process) write the kernel; the agent’s “identity” is the process that preserves those constraints.

---

## How this aligns with the repo

- **[SAFETY_CONSTITUTION.md](../SAFETY_CONSTITUTION.md)** — Human agency, corrigibility, no sovereignty: these are exactly what the ICK enforces as invariants.
- **[FULL_STACK_SECURITY_PROMPT.md](FULL_STACK_SECURITY_PROMPT.md)** — High-impact actions gated, provenance and attestation: aligns with AIL and Γ.
- **[ALIGN_ALL.md](ALIGN_ALL.md)** — Machine laws (safe set, barrier) and thesis alignment are consistent with IaP’s K, B, and Γ.

**Paper (PDF + LaTeX):** [Identity_as_Process_IaP_Baird_2026](../papers_sources/Identity_as_Process_IaP_Baird_2026.pdf) in `papers_sources/`.
