# QRNG method used March 2026 — do not change

**Principle:** We do not change methods for an experiment we have already run. Replication and any further ladder runs (1M, 10M, 50M, 100M) must use the **same** process and scripts that produced the March 2026 result (6M bits, 3 runs). This document is the single source of truth for that method.

**Christopher Michael Baird | Baird–ZoraASI Collaboration | March 2026**

---

## 1. Why this document exists

- Science requires **method constancy**: the same analysis and collection process for the same experiment.
- The March 2026 runs were executed with specific scripts and a specific protocol. Introducing different scripts or a different workflow would be a **method change**, not a replication.
- We document the method here so we don't forget it and so Codex logs (or local recovery) can be used to restore the exact process if scripts are missing from the repo.

---

## 2. Protocol (from March 2026 report — fixed)

- **Block design:** 20 blocks × 100,000 bits = 2,000,000 bits per run.
- **Conditions:** Control vs. intervention (meditation during collection).
- **Block order:** Randomized; seeds **42, 123, 456** (three independent runs).
- **API:** ANU Quantum Random Numbers; **single endpoint only; no fallback** during formal runs.
- **Analysis:** Permutation test on block means (10k permutations).
- **Preflight:** One-request auth check before run; abort on API/rate-limit failure; no backend switching mid-run.

---

## 3. Scripts that were used (canonical list)

These are the scripts that **were actually used** for the March 2026 runs. Replication and ladder runs must use these same scripts (or exact copies), not replacements.

| Script | Purpose |
|--------|---------|
| `anu_qrng_collect.py` | Collect bits from ANU API; supports `--bits`, `--pilot` (10k). |
| `anu_qrng_experiment.py` | Block-randomized control/intervention; `--analyze`, `--analyze-blocks`. |
| `qrng_test_suite.py` | Bias, runs, entropy, autocorrelation, block frequency, serial pairs. |
| `qrng_compare_runs.py` | Compare runs; KS test, permutation on block means across runs. |

**Block-level analysis:** `--analyze-blocks` on `*_blocks.json` (fast condition comparison without reloading full bitstream).

---

## 4. Artifact names and schema (from March 2026)

- **Baseline (100k):** `artifacts/anu_qrng_baseline_20260313_234104_bits.csv`, `*_summary.json`.
- **Intervention runs:** `artifacts/qrng_experiment_20260314_001431_e259c51c.csv` (and similarly named), `*_blocks.json`, `*_report.json`, `*_plots.png`.
- **Block summaries:** `block_index`, `condition`, `n_bits`, `p_hat`, `ones`, `zeros`, `entropy`, `runs_z`, `block_comparison` (with `control_mean_p1`, `intervention_mean_p1`, `difference`, `permutation_p`, `n_permutations`).

---

## 5. Commands that were run (reconstructed and recovered)

- **Baseline (100k bits):** From TOE_Corpus_2026 repo root: `python3 scripts/anu_qrng_collect.py --n 100000 --out artifacts/ --label baseline`. (Collector uses `--n` for bit count.)
- Collection (other sizes): Same script with `--n 1000000`, `--n 10000000`, etc., and appropriate `--label`.
- Full experiment run produced: `qrng_experiment_<timestamp>_<runid>.csv`, `*_blocks.json`, `*_report.json`, `*_plots.png`.
- Analysis (full): `.venv/bin/python scripts/anu_qrng_experiment.py --analyze artifacts/qrng_experiment_<stem>.csv`
- Analysis (block-level only): `python scripts/anu_qrng_experiment.py --analyze-blocks artifacts/qrng_experiment_*_blocks.json`
- Test suite on a run: `python scripts/qrng_test_suite.py artifacts/<bits_csv>`
- Compare runs: script/outputs in `artifacts/qrng_compare_report.json`.

**Environment:** A `.venv` was used (e.g. `.venv/bin/python`). Scripts lived in `scripts/`; artifacts in `artifacts/`.

---

## 6. Where are the scripts now?

**Current status (as of this doc):** The scripts above are **not** in the TOE or Black-Book repos; March 2026 runs were done with "ad hoc collection" (scripts on your machine). That is a **process failure**: the method was not committed.

**Recovery:**

1. **Codex logs:** Search your Codex logs for the exact paths and commands used ~13–14 March 2026. Look for:
   - Path to the repo or directory where `scripts/anu_qrng_collect.py` lived.
   - The first command you ran to collect baseline (e.g. `--bits 100000`).
   - The command that ran the full 20-block × 100k intervention experiment.
   - Any `artifacts/.anu_api_key` or API key path.
2. **Local machine:** Check the machine you used for the March 2026 runs. Likely locations (from pipeline doc): Black-Book `experiments/`, or a local folder that had `scripts/` and `artifacts/`.
3. **Once found:** Copy the **exact** scripts into the repo (e.g. TOE `scripts/` or Black-Book `experiments/`), commit them, and add the path to this document under "Canonical script location." Then no future run depends on "ad hoc" or memory.

---

## 7. What must not happen

- **Do not** replace this method with a different script (e.g. a new "pilot" script) for the same experiment or for replication.
- **Do not** change block design, seeds, or analysis (permutation on block means, 10k permutations) for the March 2026 experiment.
- **Do not** add API fallback or switch endpoints mid-run for formal runs.

Any **new** experiment (e.g. 1M-bit or 10M-bit ladder run) should still use the **same** scripts and the same protocol (block-randomized, control vs intervention, same analysis); only the bit count per run changes.

---

## 8. Canonical script location (recovered from Codex / Cursor handoff)

| Item | Location |
|------|----------|
| **Repo (scripts live here)** | **`~/Desktop/TOE_Corpus_2026`** (TOE_Corpus_2026 on Desktop) |
| Scripts directory | `TOE_Corpus_2026/scripts/` (e.g. `anu_qrng_collect.py`) |
| Artifacts directory | `TOE_Corpus_2026/artifacts/` |
| API key file | `TOE_Corpus_2026/artifacts/.anu_api_key` (active). Also: `.anu_api_key_paid`, `.anu_api_key_free`. Key never pasted in chat; use local file only. |
| Key resolution order (in script) | 1. `--api-key` 2. env `ANU_QRNG_API_KEY` 3. `artifacts/.anu_api_key` |
| Python | `python3` (from repo root) |
| Gitignore | `artifacts/` is gitignored so key files stay local. |

**Baseline run command (same method):**

```bash
cd ~/Desktop/TOE_Corpus_2026
python3 scripts/anu_qrng_collect.py --n 100000 --out artifacts/ --label baseline
```

The collector uses `--n` for bit count. To switch active key to free: `cp artifacts/.anu_api_key_free artifacts/.anu_api_key`. Paid: `cp artifacts/.anu_api_key_paid artifacts/.anu_api_key`.

**New-version initial ladder:** Bit counts for the current initial ladder are 100k, 1M, 5M, 10M only; method (script, protocol, key) unchanged. 50M/100M remain optional later (NEXT_QRNG).

---

## 9. Using Codex logs to recover the exact process

If you have Codex logs from ~13–14 March 2026 (or the sessions where you ran the baseline and the three intervention runs), use them to recover:

1. **Working directory** — the repo or folder where you ran `scripts/anu_qrng_collect.py` and `scripts/anu_qrng_experiment.py`.
2. **Exact first command** — e.g. the first `anu_qrng_collect.py` or `anu_qrng_experiment.py` command you ran (full command line).
3. **Path to API key** — if any (e.g. `artifacts/.anu_api_key`).
4. **How you ran the 2M-bit runs** — e.g. one command per run or a loop; and the exact `--analyze` / `--analyze-blocks` commands you used.

You can paste a short "command log" or summary from Codex into this doc (e.g. a new subsection **9.1 Recovered command log**) so the exact process is preserved. Then we never rely on memory again.

---

## 10. Recovered from handoff (Codex / Cursor) — 2026-03-15

The following was recovered from your Codex/Cursor handoff so we don't forget again.

- **Script location:** The QRNG collector and related scripts live in **TOE_Corpus_2026 on Desktop**, not in the TOE repo under Downloads. Path: `~/Desktop/TOE_Corpus_2026`.
- **Key handling:** Keys are stored only in local files (never in chat). Paths: `artifacts/.anu_api_key` (active), `artifacts/.anu_api_key_paid`, `artifacts/.anu_api_key_free`. The script resolves key in order: `--api-key` → env `ANU_QRNG_API_KEY` → `artifacts/.anu_api_key`. `artifacts/` is gitignored.
- **Run the ANU QRNG baseline (exact command):**
  ```bash
  cd ~/Desktop/TOE_Corpus_2026
  python3 scripts/anu_qrng_collect.py --n 100000 --out artifacts/ --label baseline
  ```
- **Collector interface:** Uses `--n` for number of bits, `--out` for output directory, `--label` for run label. Same script is the one to use for pilot, baseline, and ladder runs (1M, 5M, 10M initial ladder; 50M/100M optional later) so the method stays constant.

This section is the "jog memory" record: TOE_Corpus_2026 (Desktop) is where the real QRNG pipeline runs; use it for any "run the ANU QRNG baseline" or ladder run.

---

*This document is part of the Phase I close-out. Replication and ladder runs use the method described here — no substitutions.*
