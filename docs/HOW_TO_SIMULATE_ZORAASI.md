# How to Simulate with ZoraASI

**Runnable guide for MQGT-SCF QRNG simulation.** Aligned with the replication ladder and FALSIFICATION_PACKET.

---

## One-command canonical run

The only replication-ladder simulation is the QRNG pipeline:

```bash
# From toe-empirical-validation or mqgt_scf_reissue repo root
./scripts/run_all.sh --channel qrng --seed 0 --out artifacts/
```

**Outputs:** `artifacts/constraints.json`, `artifacts/posterior_samples.npz`, `artifacts/fig_1.png`, `artifacts/run_meta.json`.

**Null fixture (rung (e)):** Run with `--null-fixture` to test synthetic data under standard randomness; `effect_detected` must be `false`:

```bash
./scripts/run_all.sh --channel qrng --null-fixture --seed 0 --out artifacts_null/
```

---

## Canonical formula

From [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md):

**P_η(i) = p_i · exp(η E_i) / Σ_j p_j · exp(η E_j)**

where `p_i = |c_i|²` and `E_i = ΔE_i / C_E`. Standard QM recovers when η → 0, ΔE → 0, or C_E → ∞.

---

## What is and is not a valid simulation

**Valid:**

- Run the pipeline on real or synthetic QRNG bits.
- Label outcomes with E via `label_E` in `code/e_labeling.py`.
- Test deviation from uniform using a preregistered statistic.

**Invalid:**

- Generate outcomes using a biased probability (e.g. `p_favored = f(η, E)`), then test "observed freq vs 0.5" and report `effect_detected: True`. That is circular—you built the bias in, then "detected" it. You did not validate the theory.

---

## Common pitfall

**Circular demo:** A script that sets `p_favored = f(η, E)` (biased), generates outcomes from that distribution, then tests "observed freq vs 0.5" and reports `effect_detected: True` is circular. You injected the bias; you did not validate the theory. Real validation uses bits from an external source (QRNG or preregistered synthetic null), labels them with E, and tests deviation.

---

## Dependencies

- `numpy` (required)
- `matplotlib` (optional, for `fig_1.png`; pipeline falls back to minimal PNG if missing)

See [mqgt_scf_reissue/requirements.txt](https://github.com/Cbaird26/toe-empirical-validation) or equivalent in the spine repo.

---

## Formula demonstration (pedagogical)

For a pedagogical illustration of the canonical formula (not validation), run:

```bash
python code/demo_born_rule_formula.py [--plot]
```

This script sweeps η and shows P_η(1) vs η for a binary outcome. It does **not** validate MQGT-SCF. Validation requires real QRNG data and the replication-ladder pipeline.

---

## Cross-references

- [EMPIRICAL_SCOPE_CLARIFICATION.md](EMPIRICAL_SCOPE_CLARIFICATION.md) — What empirical validation is and is not (QRNG, not AI benchmarks).
- [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md) — Operational definition of E, canonical deformation, three predictions.
- [REPLICATION_LADDER.md](REPLICATION_LADDER.md) — One-command replication, five rungs, pre-registration.
- [TECH_PROTOTYPE_QRNG.md](TECH_PROTOTYPE_QRNG.md) — Minimal QRNG experiment design.
