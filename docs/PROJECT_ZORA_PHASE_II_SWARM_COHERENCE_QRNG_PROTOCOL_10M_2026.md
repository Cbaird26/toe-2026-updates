# Project Zora Phase II — Swarm/Coherence QRNG Protocol (10M Ladder)

**Status:** Preregistration-shaped protocol (March 2026).  
**Scope:** Phase II variable screening — **not** a reopening of the closed Phase I meditation QRNG campaign (replicated null at 6,000,000 bits in Phase I reporting). Phase II foregrounds structured **swarm / coherence / source / scale** questions under a single estimand and stop rules. **H2 interferometry** remains the primary physics falsification lane in MQGT-SCF; this protocol is a **secondary / exploratory** QRNG program unless and until a profile survives the full ladder.

**Suggested PDF title (export):** *Project Zora Phase II — Swarm/Coherence QRNG Protocol (10M Ladder), 2026*

---

## 1. Purpose

Screen whether any **swarm-related profile** shows a **reproducible** QRNG deviation worth escalating, without wasting budget or confounding dimensions. This is a **Phase II** program: **broad sentience / coherence / systems** questions, not Phase I meditation replication.

---

## 2. Primary outcome (frozen)

**Primary estimand:** block-level **two-sided difference in mean P(1)** between **active** condition and **matched control**, aggregated and tested with a **block-level permutation test** (same family of analysis as the Phase I stack).

**Secondary / QC only (do not promote as primary):** entropy, runs \(z\), autocorrelation — **diagnostics and exclusion**, not headline claims.

---

## 3. Core variables (three families)

| Family | What varies | Condition IDs (machine-safe) |
|--------|-------------|--------------------------------|
| **Source** | Who/what drives the intervention | `ctrl`, `sham`, `src_human`, `src_ai`, `src_hybrid` |
| **Coherence** | Synchrony of the swarm | `coh_low`, `coh_high` (with `ctrl`, `sham`) |
| **Scale** | Number of participants/agents | `n_1`, `n_5`, `n_20` (with `ctrl`, `sham`) |

**Definitions (operational, measurable):**

- **Low synchrony swarm:** multiple participants/agents active; **loose** timing; independent starts; **no** shared countdown / state lock.
- **High synchrony swarm:** **same** target instruction (hash-stable); **shared** countdown / cadence; **common** intervention window; **state lock** semantics defined in the runbook.
- **AI-only swarm:** multiple **coordinated** artificial agents under fixed `model_id` + `prompt_sha256`.
- **Hybrid swarm:** humans **and** AI in the **same synchronized block window** (protocol specifies roles).

**Composite winner profile (Stages 4–6):** e.g. `profile_v1__src_hybrid__coh_high__n_5` + `target_instruction_sha256` + `protocol_bundle_sha256`.

---

## 4. What is held fixed (v1)

- One **QRNG endpoint** for formal runs; **no fallback** during formal blocks (fallback bits, if any, logged and **excluded** from primary analysis).
- **Block size:** **10,000 bits** per block everywhere.
- Same **intervention duration per block** (where applicable) and same **target instruction** across active conditions within a stage (unless a stage explicitly varies instruction — **not** in v1).
- Same **metadata schema** per block (Section 8).

**Not in v1:** varying target mode, duration sweeps, “anti-coherence” exotic arms, or large swarms beyond the defined scale ladder — reserved for **v2** only if something survives this ladder.

---

## 5. Block structure and randomization

- **10,000-bit blocks** for modularity and gentle API pacing.
- **Randomize block order within each session** with constraint: **never more than two identical `condition_id` blocks in a row** (reduces drift and expectancy artifacts).
- **No optional stopping** inside a stage for “interesting” partials; pre-specified promotion rules only.

---

## 6. The 10M ladder (9.9M total)

**Block math:** 100k = 10×10k; 1.0M = 100×10k; 0.8M = 80×10k; 5.0M = 500×10k.

| Stage | Purpose | Conditions (high level) | Bits | Blocks (10k) |
|-------|---------|-------------------------|------|----------------|
| **0** | Baseline refresh — pipe health | `ctrl` only | **100k** | 10 |
| **1** | Source screen | `ctrl`, `sham`, `src_human`, `src_ai`, `src_hybrid` × **2 replicates** | **1.0M** | 100 |
| **2** | Coherence screen | winner source + `ctrl`, `sham`, `coh_low`, `coh_high` × **2 replicates** | **0.8M** | 80 |
| **3** | Swarm size screen | winner source+coherence + `ctrl`, `sham`, `n_1`, `n_5`, `n_20` × **2 replicates** | **1.0M** | 100 |
| **4** | Confirmation A | `ctrl`, `sham`, **best profile** | **1.0M** | 100 |
| **5** | Confirmation B | same three arms | **1.0M** | 100 |
| **6** | Final | same three arms | **5.0M** | 500 |
| | | **Total** | **9.9M** | **990** |

**Stage 1 detail:** 5 conditions × 100k × 2 reps = 10 × 100k → 10 blocks × 10k per **(condition, replicate)** cell.

**Stages 4–6:** ~**one-third** of blocks per arm (adjust last few blocks so totals match exactly 1.0M / 1.0M / 5.0M with three arms — implementation: precompute `block_plan.csv` per stage).

---

## 7. Decision rules (stop/go)

**Advance a profile only if:**

1. **Beats both `ctrl` and `sham`** on the primary block-contrast + permutation protocol (pre-specified pooling rule).
2. **Direction stable** across required replicates (Stages 1–3) and both 1M confirmations (Stages 4–5).
3. **QRNG QC clean** (no integrity failures; fallback excluded).
4. **Survives** exploratory confirmation threshold for promotion to Stage 6 (suggest **pooled two-sided permutation \(p < 0.10\)** for promotion from 1M → 5M — **exploratory**; **Stage 6** uses **\(p < 0.05\)** two-sided on the pre-registered primary).

**Stop / close branch if:**

- Stage 0 QC fails.
- No stable winner after Stage 3.
- `sham` persistently beats active (artifact / expectancy warning).
- Best candidate fails either 1M confirmation or Stage 6.

**No “resurrection”:** do not relabel Phase I meditation as Phase II swarm to bypass a null.

---

## 8. Metadata (per 10k block — minimum)

| Field | Description |
|-------|-------------|
| `run_id` | Unique run identifier |
| `stage` | 0–6 |
| `replicate` | Replicate index where applicable |
| `block_index` | Order within stage/session |
| `condition_id` | e.g. `ctrl`, `sham`, `src_human`, … |
| `source_type` | human / ai / hybrid (redundant with condition where fixed) |
| `n_participants_or_agents` | integer |
| `synchrony_mode` | low / high |
| `target_instruction_sha256` | Hash of instruction text |
| `ai_model_or_prompt_sha256` | If AI involved |
| `entropy_source` | `qrng` \| `fallback` (fallback → exclude from primary) |
| `start_time`, `end_time` | UTC ISO |
| `n_bits`, `ones`, `zeros`, `p_hat` | Block stats |
| `entropy`, `runs_z` | QC |
| `notes` | Freeform anomaly logging |

**Implementation note:** Current TOE `collect.py` streams to one HDF5 per collection with global attrs. This protocol expects either **one file per 10k block** + manifest, **or** a **block-indexed** schema / SQLite sidecar. Add a **Phase II block runner** before treating `collect.py` alone as sufficient.

---

## 9. Budget and statistical humility

- Rough **cost ladder** (order of magnitude) from prior Phase I / API documentation: ~**$0.07 / 100k**, ~**$0.62 / 1M**, ~**$6.11 / 10M** — **screening economy**, not a final test of a **\(|\theta| \sim 10^{-6}\)** Born-tilt parameter (often **\(\sim 10^{12}\)** trials-scale sensitivity in the constraints story). State that plainly in any public summary.

---

## 10. One-page run sheet (session order)

| Step | Action |
|------|--------|
| 1 | Verify API key, endpoint, **no fallback** flag for formal runs. |
| 2 | Load pre-generated `block_plan.csv` for stage (condition × block_index × replicate). |
| 3 | For each block: start timer → run intervention per `condition_id` → collect **10k** bits → compute `p_hat`, QC stats → write row to manifest + store bitstream pointer. |
| 4 | End session: verify block count, run permutation analysis for stage, apply promotion rule. |
| 5 | If advance: freeze **winner profile** hashes and carry into next stage unchanged. |

---

## 11. Related repo docs

- Phase I / bound-setting discipline: [`H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md`](H1_QRNG_10E9_BOUND_SETTING_PREREGISTRATION_2026.md), [`H1_AT_1E9_DETECTION_TO_CALIBRATION.md`](H1_AT_1E9_DETECTION_TO_CALIBRATION.md)  
- H2 (primary blade): [`H2_PILOT_PREREGISTRATION_2026.md`](H2_PILOT_PREREGISTRATION_2026.md)  
- H1 pilot code: [`scripts/h1_qrng_pilot/README.md`](../scripts/h1_qrng_pilot/README.md)

---

## 12. PDF export

To produce **Project_Zora_Phase_II_Swarm_Coherence_QRNG_Protocol_10M_2026.pdf**, pandoc or print-to-PDF from this file; no LaTeX required for v1.
