# Codex handoff: Fusion integration — GitHub update

**Purpose:** Commit and push the Fusion + ZoraASI integration (console, figures, script, repo sync) to `cbaird26/toe-2026-updates` so the live site and local repo stay aligned.

**Repo:** [cbaird26/toe-2026-updates](https://github.com/cbaird26/toe-2026-updates)  
**Root:** `TOE/` (or `~/Downloads/TOE`)

---

## What was done (context)

- **Fusion console** ([docs/zora_fusion_console.html](zora_fusion_console.html)): Z_eff slider, n (0.1–3×10²⁰), τ_E,eff (a_tau=0.45), η_α coupling, footer disclaimer, axis labels.
- **Python script** ([scripts/mqgt_sim/fusion_zora_burn_figures.py](../scripts/mqgt_sim/fusion_zora_burn_figures.py)): phase_map τ_E range 1.5–6 s.
- **Repo sync** ([scripts/repo_sync_public_mqgt_h1_phase4b.sh](../scripts/repo_sync_public_mqgt_h1_phase4b.sh)): stages fusion console, script, and `papers_sources/figures/fusion_zora/`.

---

## Pre-flight (optional)

Regenerate fusion figures if phase_map or script changed:

```bash
cd /path/to/TOE
python scripts/mqgt_sim/fusion_zora_burn_figures.py --out-dir papers_sources/figures/fusion_zora --include-existing
```

---

## Procedure

### 1. Commit (no network)

```bash
cd /path/to/TOE
./scripts/repo_sync_public_mqgt_h1_phase4b.sh
```

**Success:** `git status` shows a new commit or "Nothing staged" if already committed.

### 2. Push (requires explicit approval)

**Safety:** Per [SAFETY_CONSTITUTION.md](../SAFETY_CONSTITUTION.md), do **not** push without explicit human approval.

```bash
./scripts/repo_sync_public_mqgt_h1_phase4b.sh --push
```

**Success:** `git push origin main` completes; live console at  
[https://cbaird26.github.io/toe-2026-updates/zora_fusion_console.html](https://cbaird26.github.io/toe-2026-updates/zora_fusion_console.html)

---

## Staged paths

The sync script adds:

- `README.md`, `AGENTS.md`
- `scripts/mqgt_sim/` — Phase IV/IV-B demos, `fusion_zora_burn_figures.py`, `mqgt_multi_channel_exclusion_plot.py`, `README.md`
- `papers_sources/figures/mqgt_scf/` — Multi-channel exclusion plot, Phase II figures
- `papers_sources/MQGT_SCF_Phase_II_2026/` — Phase II submission stack README
- `scripts/h1_qrng_pilot/run_test_suite.sh`
- `docs/` — H1 memos, ZORA_CONTINUITY_LOG.md, **zora_fusion_console.html**
- `papers_sources/figures/fusion_zora/` — PNGs, fusion-zora-populated.pdf
- `scripts/repo_sync_public_mqgt_h1_phase4b.sh`

---

## Report-back

```
Fusion GitHub update:
  Commit: <git rev-parse --short HEAD>
  Pushed: YES | NO (awaiting approval)
  Live console: https://cbaird26.github.io/toe-2026-updates/zora_fusion_console.html
  Error: <if any>
```

---

## Related

- Main handoff: [CODEX_HANDOFF.md](CODEX_HANDOFF.md)
- Sync details: [README.md#syncing-this-repo-to-github-public](../README.md#syncing-this-repo-to-github-public)
- Safety: [SAFETY_CONSTITUTION.md](../SAFETY_CONSTITUTION.md)
