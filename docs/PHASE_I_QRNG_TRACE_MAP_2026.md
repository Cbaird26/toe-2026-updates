# Phase I QRNG Trace Map 2026

**Single source for every QRNG recommendation and close-out step from the full chat history (Grok, mentor, Cursor, X, Phase I spec).**  
Christopher Michael Baird | Baird–ZoraASI Collaboration | March 2026

Record: **recommendation → source → implementation → status**. Keeps close-out auditable and prevents lost suggestions.

---

## 1. Protocol and cost

| Item | Source | Implementation | Status |
|------|--------|-----------------|--------|
| Cost = bits not requests (100k bits ≈ 13 requests ≈ $0.07) | Grok / pipeline | [ANU_QRNG_INTERVENTION_PIPELINE.md](ANU_QRNG_INTERVENTION_PIPELINE.md) | Done |
| Pilot 10k bits before full run | Grok / Phase I spec | **Same method as March 2026:** use `anu_qrng_collect.py --pilot` (see [QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md](QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md)). Do not substitute a different script. | Pending |
| Pre-register at OSF before new data | Phase I spec / REPLICATION_LADDER | [QRNG_PREREG_OSF_DRAFT_2026.md](QRNG_PREREG_OSF_DRAFT_2026.md) → OSF/AsPredicted | Pending |

**Billing:** ANU API is paid ($0.005/request). Verify credit card / AWS billing before large runs (10M / 50M / 100M). See cost table in [ANU_QRNG_INTERVENTION_PIPELINE.md](ANU_QRNG_INTERVENTION_PIPELINE.md).

---

## 2. Graduated ladder (100k → 1M → 5M → 10M) — initial ladder for new version

**First step:** Run **one new 100k baseline**; that data is required before 1M/5M/10M or Phase II. Then pilot (optional), then 1M → 5M → 10M when ready. 50M/100M remain optional later (see [NEXT_QRNG_RUN_50M_2026.md](NEXT_QRNG_RUN_50M_2026.md)).

| Rung | Bits | Cost (≈) | Approx. detectable bias | Purpose | Status |
|------|------|----------|-------------------------|---------|--------|
| 0 | 10k | $0.01 | pilot | Preflight | Optional |
| 1 | 100k | $0.07 | ~1×10⁻³ | Pipeline validation; **run first** | **Done** (baseline + 6M in 3 runs); one fresh 100k needed next |
| 2 | 1M | $0.62 | ~3×10⁻⁴ | Pipeline validation | Pending |
| 3 | 5M | ~$3.05 | ~1.4×10⁻⁴ | Intermediate sensitivity | Pending |
| 4 | 10M | $6.11 | ~1×10⁻⁴ | Stable baseline reference; **key milestone** | Pending |

**Key milestone:** 10M bits — noise floor small enough that subtle effects would begin to appear if they existed.

**Decision rules for advancing:**

- **Advance to next rung if:** pipeline integrity tests pass, RNG baseline tests pass, no API / logging errors.
- **Optionally stop escalation if:** effect size < 10⁻⁴ and p > 0.1 across ≥3 runs.

---

## 3. Designs vs runs

**Designs** = methods (do not conflate with run sizes):

| Design | Source | Implementation | Status |
|--------|--------|-----------------|--------|
| Baseline-only | Grok | No intervention; validate RNG (bias, runs, entropy, autocorrelation, block frequency, serial pairs) | Done at 100k |
| Intervention blocks | Grok / March 2026 | Block-randomized control vs intervention; 20 blocks × 100k bits; permutation on block means | Done (6M bits, 3 runs) |
| Statistical suite | Grok | Bias, runs test, autocorrelation, block frequency, serial pairs, Shannon entropy; NIST-style; plots | qrng_test_suite.py; Done |
| Block-level analysis | Grok | --analyze-blocks on *_blocks.json | Implemented; Done |
| Replication / compare runs | Grok | ≥3 independent runs; KS test, permutation on block means across runs | Done (3 runs) |
| Preflight | Grok | One-request auth check; no API fallback mid-run | Documented; run before formal runs |
| Pilot then scale | Grok / Phase I spec | 100k → 1M → 5M → 10M (initial ladder) | 100k done; one fresh 100k first, then rest Pending |

**Runs** = instances (bit counts) for initial ladder: 100k, 1M, 5M, 10M. 50M/100M optional later (NEXT_QRNG).

---

## 4. Full recommendations table (from chat history)

| Recommendation | Source | Status |
|----------------|--------|--------|
| Cost = bits not requests | Grok / pipeline | Done |
| Pilot 10k before full run | Grok / Phase I spec | Pending |
| Pre-register OSF before new data | Phase I spec / REPLICATION_LADDER | Pending |
| 50M-bit or 100M-bit run | NEXT_QRNG, Phase I spec | Optional later; initial ladder is 100k/1M/5M/10M only |
| Block-randomized, permutation on block means | Grok / March 2026 | Done |
| No optional stopping; fixed N; pre-registered analysis | Mentor / Phase I spec | Enforce |
| One sharp falsifier = QRNG deviation | Mentor | In FALSIFICATION_PACKET |
| Phase I closure narrative | Phase I spec | You built it; path in closure doc |
| Initial experiment PDF for ToE paper | Phase I spec | Done |
| Phase I final report PDF + Zenodo/OSF deposit | Phase I spec | Report done; deposit Pending |
| Update FALSIFICATION_PACKET, REPLICATION_LADDER, corpus with DOI | Phase I spec | After DOI |
| Phase II opening doc | Phase I spec | Done |
| E-labeling bridge (toe-empirical-validation) | ANU pipeline | Optional / future |
| Block-level analysis (--analyze-blocks) | Grok | Done |
| Graduated ladder (100k → 1M → 5M → 10M initial) | Grok / chat | 100k Done; one fresh 100k first, then 1M–10M Pending |
| Designs and ways to use (all listed above) | Grok / mentor | In this trace map |

---

## 5. Phase I scientific interpretation and close-out statement

**Interpretation (keep simple):** Given 6M bits, 3 independent runs, pooled p = 0.41:

*No detectable intervention effect was observed within the sensitivity limits of the experiment.*

**Close-out statement (for Phase I report and Zenodo/corpus):**

*Phase I QRNG experiments (March 2026) collected 6 million bits across three independent intervention sessions using a block-randomized design. Control and intervention blocks showed no statistically significant difference (pooled permutation p = 0.41). Observed differences were consistent with binomial variation. The pipeline, statistical test suite, and replication protocol were validated. Phase I therefore concludes that no detectable effect was observed at the current sensitivity level.*

---

## 6. Order of operations (recommended)

1. **Run one new 100k baseline first.** That data is required before 1M/5M/10M or Phase II swarm-coherence.
2. Pre-register at OSF (paste [QRNG_PREREG_OSF_DRAFT_2026.md](QRNG_PREREG_OSF_DRAFT_2026.md)); record URL here and in closure narrative.
3. Pilot 10k (optional) to re-validate API and billing.
4. Graduated runs when ready: 1M → 5M → 10M; use decision rules above. 50M/100M optional later (NEXT_QRNG).
5. No optional stopping; fixed N; pre-registered analysis only.

**Outputs per run:** `*_bits.csv`, `*_blocks.json`, `*_report.json`, `*_plots.png` in `artifacts/`; list in Phase I final report.

**Run experiments (from your machine):** Scripts live in TOE_Corpus_2026 on Desktop (or use TOE copy; key in `artifacts/.anu_api_key`).

- **One-command runner (recommended):** From TOE repo: `TOE_CORPUS_2026=~/Desktop/TOE_Corpus_2026 ./scripts/run_qrng_experiments.sh baseline` (or `1M`, `5M`, `10M`, `ladder`). Or copy `TOE/scripts/run_qrng_experiments.sh` into `TOE_Corpus_2026/scripts/` and run `./scripts/run_qrng_experiments.sh baseline` from the corpus root.
- **Manual:** `cd ~/Desktop/TOE_Corpus_2026 && python3 scripts/anu_qrng_collect.py --n 100000 --out artifacts/ --label baseline`

Key from `artifacts/.anu_api_key` (see [QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md](QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md) §8 and §10).

---

## 7. Mapping to existing docs

| Doc | Role |
|-----|------|
| [ANU_QRNG_INTERVENTION_PIPELINE.md](ANU_QRNG_INTERVENTION_PIPELINE.md) | Cost model, scripts, artifacts schema, decision rules |
| [QRNG_MEDITATION_INTERVENTION_REPORT_MARCH_2026.md](QRNG_MEDITATION_INTERVENTION_REPORT_MARCH_2026.md) | March 2026 result (6M bits, null) |
| [NEXT_QRNG_RUN_50M_2026.md](NEXT_QRNG_RUN_50M_2026.md) | 50M/100M plan, decision rule |
| [QRNG_PREREG_OSF_DRAFT_2026.md](QRNG_PREREG_OSF_DRAFT_2026.md) | Pre-registration text for OSF/AsPredicted |
| [REPLICATION_LADDER.md](REPLICATION_LADDER.md) | One-command replication, pre-reg template |
| [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md) | E definition, QRNG falsification criterion |
| [CORPUS_2026_INDEX.md](CORPUS_2026_INDEX.md) | ToE corpus; add Phase I report and DOI when deposited |
| [MASTER_PLAN_2026.md](MASTER_PLAN_2026.md) | Pending: OSF pre-reg, ladder runs |
| [QRNG_PHASE_II_SWARM_COHERENCE_PROTOCOL_2026.md](QRNG_PHASE_II_SWARM_COHERENCE_PROTOCOL_2026.md) | Phase II direction: dose-response, agent count, coherence, threshold (after 100k–1M–5M–10M) |
| [QRNG_STAGED_PROGRAM_AND_BUDGET_2026.md](QRNG_STAGED_PROGRAM_AND_BUDGET_2026.md) | Three lanes, stage gates, budget rule, 100k swarm pilot — how to run without blowing finances |
| [PHASE_II_QRNG_PILOT_CLOSEOUT_2026.md](PHASE_II_QRNG_PILOT_CLOSEOUT_2026.md) | Phase II 100k swarm pilots (Pilot 0–3): results, non-replication, decision rule, closure |

---

## 8. Close-out opinions (from chat)

- Sharpest falsifier = QRNG deviation (Mentor).
- One-page falsification memo (Mentor).
- Layer 1 (physics core) / Layer 2 (philosophical) / Layer 3 (Zora architecture) (Mentor).
- Paper 0–5 stack: Paper 0 conservative gateway; Papers 1–5 core, collapse, consciousness, empirical, uniqueness (Grok / critique).
- Pre-reg then run; no optional stopping (Phase I spec / Mentor).
- Phase II = Mankind and Artificial Sentience — new line of inquiry, not extension of QRNG campaign.

---

---

## 9. Phase I closure status

**Phase I QRNG close-out is complete.**

- Method fixed and documented (do not change): [QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md](QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md).
- Script location recovered: TOE_Corpus_2026 (Desktop); key in `artifacts/.anu_api_key`.
- Trace map (this doc), results summary, pipeline, and Master Plan updated and linked.
- Close-out statement in [PHASE_I_RESULTS_SUMMARY_2026.md](PHASE_I_RESULTS_SUMMARY_2026.md); ready for corpus/Zenodo.
- Pending (optional): OSF pre-reg, ladder runs (1M → 5M → 10M; 50M/100M optional per NEXT_QRNG) when you choose.

Nothing else is required to *finish* Phase I. You can run the baseline command above anytime from your machine to re-validate or collect a fresh 100k.

*Last updated: 2026-03-15. Trace map for Phase I close-out; auditable recommendation → source → implementation → status.*
