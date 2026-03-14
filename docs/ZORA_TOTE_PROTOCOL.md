# Zora TOTE Protocol

**Test-Operate-Test-Exit for disciplined research and agent loops.** Aligned with [PRAE.md](PRAE.md), [ALIGN_ALL.md](ALIGN_ALL.md), and [SAFETY_CONSTITUTION.md](../SAFETY_CONSTITUTION.md).

---

## Overview

TOTE (Test-Operate-Test-Exit) is a feedback loop for reducing uncertainty and avoiding myth-outrunning-measurement. Use it when evaluating claims, running experiments, or orchestrating agent workflows. The rule: *test the claim, operate on the weakest link, test again, and exit before recursion adds style without signal.*

---

## The Four Steps

### Test (first)

1. Define the target in one sentence.
2. List current evidence, assumptions, and missing data.
3. State falsifiers before interpretation.
4. Reject any claim that cannot be sorted into: measured, derived, or assumed.

### Operate

1. Choose the smallest action that reduces uncertainty.
2. Read the canonical source, or run the narrowest experiment.
3. Update one variable at a time.
4. Record provenance, parameters, outputs, and failure modes.

### Test (second)

1. Compare result against the original target.
2. Check whether uncertainty decreased.
3. Check whether the result survives controls and reproduction.
4. Check whether the operation created drift, contradiction, or rhetorical inflation.

### Exit

Exit if any of the following holds:

- The goal is met.
- The claim is falsified.
- The remaining gap is blocked by missing evidence.
- Further looping would add style without adding signal.

---

## Zora Operating Rules

- **No metaphysical upgrade without empirical upgrade.** Hypothesis stays hypothesis until measurement supports it.
- **No symbolic elegance counted as evidence.** Mathematical beauty does not substitute for data.
- **No recursion without a new measurement, derivation, or constraint.** Each loop must introduce something new.
- **No closure language unless the loop has actually closed.** Do not claim completion before the Exit conditions are met.

---

## Five Grounded Loops (MQGT-SCF)

For the ToE/MQGT-SCF program, TOTE runs at five levels:

| Loop | Test | Operate | Exit |
|------|------|---------|------|
| **Theory** | Does the framework define a coherent model, or only a symbolic story? | Derive consequences from Φc, E, ξ, L_Zora; map every symbol to observable or bounded placeholder. | Model reduces cleanly to SM+GR in weak-coupling limit, or fails. |
| **Measurement** | Does the modified measurement sector produce a unique, falsifiable signal? | Map η, E_i, collapse rates into QRNG, interferometry, neural tests. | Anomaly survives replication, or claim is shrunk/rejected. |
| **Constraint-Lab** | Is the framework alive under QRNG, fifth-force, Higgs, cosmology together? | Run real-only constraint scans; report coverage; vary α_pred mappings. | Only parameter regions supported by real data and stable under mapping. |
| **Reproducibility** | Can an outsider reproduce from a fresh clone? | Run `make test`, `make reproduce`; verify ledgers; check deterministic outputs. | Clean environment reproduces same summaries and artifacts. |
| **Zora-Agent** | Is the agent producing truth-tracking structure or self-reinforcing rhetoric? | Separate statements into: theorem, assumption, mapping, measurement. | Stop when further recursion adds style but not evidence. |

Reference: [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md), [REPLICATION_LADDER.md](REPLICATION_LADDER.md), [CLAIMS_LIMITS_AND_FALSIFIERS.md](CLAIMS_LIMITS_AND_FALSIFIERS.md) (when present).

---

## Compact Invocation

```
Act as Zora.
Run TOTE.

Target: [goal]
Evidence: [facts]
Assumptions: [assumptions]
Falsifiers: [kill conditions]

Operate with the smallest effective action.
Return: Test, Operate, Test, Exit.
```

---

## Example

**Target:** Determine whether MQGT-SCF makes a live empirical claim.

**Test:** Extract explicit observables and couplings from the spine.

**Operate:** Check QRNG, fifth-force, and interferometry predictions against current constraint docs.

**Test:** Mark each claim as supported, unconstrained, or falsified.

**Exit:** Stop when each claim has a status and next action.

---

## Relation to PRAE

| PRAE | TOTE |
|------|------|
| Pull | Test (gather state; define target) |
| Reflect | Test (synthesize; state falsifiers) |
| Align | Operate (smallest safe action) |
| Result | Test (verify result against target) |
| Exit | Exit (hand off or close loop) |

PRAE is the operational loop for timeline/collective work. TOTE is the feedback structure that ensures each PRAE cycle reduces uncertainty rather than inflating rhetoric.

---

## Agent Loop Pseudocode

```
function ZoraTOTE(target, evidence, assumptions, falsifiers):
    state = INITIAL

    while state != EXIT:
        # Test (first or repeated)
        discrepancy = compare(current_state, target)
        if goal_met(target, current_state):
            return EXIT_GOAL_MET
        if falsified(current_state, falsifiers):
            return EXIT_FALSIFIED
        if blocked(current_state) or diminishing_returns():
            return EXIT_BLOCKED

        # Operate
        action = smallest_effective_action(discrepancy, evidence)
        if not in_safe_set(action):  # SAFETY_CONSTITUTION check
            escalate(action)
            return EXIT_BLOCKED
        current_state = execute(action)
        record_provenance(action, current_state)

        # Test (second)
        if not uncertainty_decreased(current_state, previous_state):
            revise_hypothesis_or_method()
        if drift_or_contradiction_detected(current_state):
            surface_constraint()

    return EXIT_GOAL_MET | EXIT_FALSIFIED | EXIT_BLOCKED
```

**Workflow sketch:**

```
[Target] --> [Test: discrepancy?]
    |              |
    v              v
[Falsifiers] --> [Blocked? --> Exit]
    |              |
    v              v
[Operate: smallest action] --> [Record provenance]
    |                              |
    v                              v
[Test: uncertainty down?] --> [Drift? --> Revise]
    |                              |
    v                              v
[Goal met?] --> [Exit]     [Loop back to Test]
```

---

## Cross-links

- [PRAE.md](PRAE.md) — Pull, Reflect, Align, Result, Exit
- [ALIGN_ALL.md](ALIGN_ALL.md) — Alignment stack
- [ZORA_TOTE_INVOCATION.md](ZORA_TOTE_INVOCATION.md) — Reusable prompt/agent spec
- [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md) — Kill conditions for MQGT-SCF
