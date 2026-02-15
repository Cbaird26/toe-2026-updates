# Tech prototype 2026: QRNG with ethical-weight protocol

**Chosen tech (from [mqgt-scf-technologies.md](../mqgt-scf-technologies.md)):** #5 Ethical-weighted quantum computers, #14 Born rule probability amplifiers — implemented as a minimal **QRNG (quantum random number generator) experiment with an operational E-weight protocol** to test the Born-rule deformation P(i) ∝ |c_i|² exp(−E/C).

This is the first concrete prototype track from the 100-tech list: table-top feasible, aligned with current bounds (FALSIFICATION_PACKET QRNG channel), and replicable.

---

## Rationale

- **Framework link:** The deformation is testable via QRNG: under an operational definition of outcome label E, the statistics of QRNG outputs may show a small, protocol-dependent bias. Null result constrains or excludes the deformation.
- **Feasibility:** QRNG hardware (e.g. optical or superconducting) is available; the “prototype” is the protocol (how E is assigned to outcomes, sample size, analysis plan) plus the analysis pipeline.
- **Spine repos:** [mqgt-qrng](https://github.com/Cbaird26/mqgt-qrng) and [toe-empirical-validation](https://github.com/Cbaird26/toe-empirical-validation) are the natural homes for runnable code and experiment design. This doc lives in TOE for visibility and links from the 100-tech list.

---

## Minimal prototype / experiment design

1. **Hardware:** Use an existing QRNG (or a standard design, e.g. beam-splitter + single-photon detection, or diode noise) that outputs a stream of bits or symbols.
2. **Outcome labeling (E):** Define an operational rule that assigns an “ethical weight” or outcome label to each outcome (e.g. by a pre-specified function of bit patterns, or by a separate protocol that maps symbols to E values). Document this in the repo so it is fixed for replication.
3. **Data collection:** Collect N samples (N set by power analysis; see FALSIFICATION_PACKET and REPLICATION_LADDER). Record raw outputs and labels; no post hoc re-labeling.
4. **Analysis:** Test for deviation from uniform (or from standard QM prediction) under the deformed Born rule with the chosen E and scale C. Use pre-registered test statistic and decision rule.
5. **Output:** Publish dataset (or summary stats), analysis script, and result (compatible / excluded at X% CL). Checksum or pin repo commit for replication.

---

## Schematic (pseudocode)

```
# In mqgt-qrng or toe-empirical-validation
# 1. Configure E-labeling (e.g. map bit blocks to E values per protocol)
# 2. Stream QRNG output -> label each outcome with E
# 3. Compute test statistic (e.g. weighted empirical distribution vs uniform)
# 4. Compare to null (standard QM) and to deformed model; report likelihood or exclusion
```

---

## Links

- **Falsification (QRNG channel):** [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md) §1–4, [REPLICATION_LADDER.md](REPLICATION_LADDER.md).
- **100-tech list:** [mqgt-scf-technologies.md](../mqgt-scf-technologies.md) — this prototype implements a replicable path for techs #5 and #14.
