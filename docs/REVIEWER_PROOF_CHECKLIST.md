# Reviewer-Proof Checklist (TOE 2026)

Use this gate before submission, preprint update, Zenodo release, or public claim refresh.

## 1) Canonical spine integrity

- [ ] `docs/CANONICAL_SPINE.md` reflects current A-H closure map.
- [ ] `docs/INTEGRATED_MANUSCRIPT_INDEX.md` points to one canonical source per hardening item.
- [ ] No competing definitions of solved-vs-hardening status across docs.

## 2) Theorem completeness (no-signaling package)

- [ ] Core manuscript includes explicit assumptions block (locality, microcausality, linear CPTP, spacelike support separation).
- [ ] Lemma chain and theorem statement are present, not only narrative prose.
- [ ] Scope boundaries / failure modes are explicitly listed.
- [ ] Teleology companion wording is aligned to the same assumption structure.

## 3) Ethics operationalization

- [ ] `e(x,t)` is defined from preregistered observables and weights.
- [ ] Aggregate `E_R(t)` and branch score `Delta E_a` are explicitly defined.
- [ ] Normalization `E_a = Delta E_a / C_E` is stated in canonical text.
- [ ] Protocol boundary separates canonical estimator from sensitivity-analysis alternatives.

## 4) Parameter hygiene and bounds

- [ ] Core parameter table includes role, prior class, and identifiability/bound status.
- [ ] Empirical paper mirrors canonical symbols and bound sources.
- [ ] No symbol drift (`eta`, `gamma_col`, `kappa`, `m_c`, coupling constants) across core + empirical docs.
- [ ] Every free parameter has at least one stated source channel or explicit unbounded status.

## 5) Flagship falsifier quality

- [ ] One primary observable is designated as flagship.
- [ ] Effect-size/scaling equation is explicit.
- [ ] Null expectation and decisive sensitivity threshold are explicit.
- [ ] Falsification packet and empirical paper use the same flagship definition.

## 6) Matter/brain coupling canonicalization

- [ ] Main text contains one canonical source-term model (`J_{Phi_c}`, `J_E`).
- [ ] Alternative couplings are quarantined to appendix/sensitivity analysis.
- [ ] No headline results depend on non-canonical couplings without explicit labeling.

## 7) Reproducibility and release artifacts

- [ ] Falsification packet has one-command reproduction path and artifact pinning guidance.
- [ ] Commit hashes / DOI versions used for claims are documented.
- [ ] Figure/table dependencies are declared and reproducible.
- [ ] Cross-links to replication ladder and checklist docs are valid.

## 8) Final release gate

- [ ] Internal consistency pass complete (notation, assumptions, equations).
- [ ] Reviewer-hostile read-through complete (attempted failure modes documented).
- [ ] Public-facing claims restricted to what is proven/tested in current version.
