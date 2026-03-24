# Codex handoff: Full session update (all artifacts)

**Purpose:** Single-entry handoff for today's full session. Incorporate all posted artifacts, align parameters across the repo, surface the extra session outputs in repo docs, and update local + public GitHub (`cbaird26/toe-2026-updates`).

**Repo:** [cbaird26/toe-2026-updates](https://github.com/cbaird26/toe-2026-updates)  
**Root:** `TOE/` (or `~/Downloads/TOE`)

---

## Artifact checklist

Verify each path exists after the user posts artifacts:

| Path | Contents |
|------|----------|
| `docs/CODEX_HANDOFF.md` | Main executor index with optional-task row linking this handoff |
| `docs/CODEX_HANDOFF_FUSION_GITHUB_UPDATE.md` | Fusion-specific sync handoff retained as a narrower operator path |
| `papers_sources/figures/fusion_zora/` | `baseline_vs_controlled.png`, `phase_map.png`, `ppo_training_curve.png`, `ppo_rollout.png`, `fusion-zora-populated.pdf` |
| `scripts/mqgt_sim/fusion_zora_burn_figures.py` | Bosch–Hale D–T, 0D ODE, coherence coupling; CLI `--out-dir`, `--pdf`, `--include-existing`, `--pdf-only`; phase_map τ_E 1.5–6 s |
| `docs/zora_fusion_console.html` | Sliders (n, τ_E, T₀, χ, Z_eff), Zora toggle, Pulse Φc, T/Q strip charts; Z_eff 1–2, n 0.1–3×10²⁰, τ_E,eff (a_tau=0.45), η_α coupling |
| `docs/zora_coherence.html` | Kuramoto-style coherence toy; exploratory visualization only, not a physics evidence artifact |
| `scripts/mqgt_sim/mqgt_multi_channel_exclusion_plot.py` | (m_Φ, sin²θ) exclusion plot generator |
| `papers_sources/figures/mqgt_scf/` | README + `mqgt_scf_multi_channel_exclusion.png` |
| `papers_sources/MQGT_SCF_Phase_II_2026/` | README (Anchor, Closure, NoSignalling, ABIL, H2 prereg), links to demos |
| `papers_sources/H1_QRNG_Pilot_Methods_Status_2026.tex` / `.pdf` / `Notes.bib` | H1 methods/status note; methods posture, placebo snapshot, billion-trial calibration discipline |
| `scripts/build_h1_methods_pdf.sh` | Helper to rebuild the H1 methods PDF from `papers_sources/` |
| `phase_iv_b_sweep/` | `summary.md`, `phase_iv_b_sweep_results.csv`, lock-rate heatmaps, mean-coherence heatmaps |
| `scripts/zora_recursive_scalar_demo.py` | Exploratory scalar-field demo; do not present as referee-safe evidence |
| `README.md` | Phase II stack link, multi-channel plot, Zenodo DOI 10.5281/zenodo.19158407 |
| `papers_sources/README.md` and `papers_sources/figures/README_figures.md` | Public discovery surfaces for the paper stack and figure bundles |

---

## Pre-flight (optional)

Regenerate figures if scripts changed:

```bash
cd /path/to/TOE
python scripts/mqgt_sim/fusion_zora_burn_figures.py --out-dir papers_sources/figures/fusion_zora --include-existing
python scripts/mqgt_sim/mqgt_multi_channel_exclusion_plot.py --out-dir papers_sources/figures/mqgt_scf
bash scripts/build_h1_methods_pdf.sh
```

---

## Add missing paths

If the user posts artifacts not in the sync script, add them:

```bash
git add <path>
```

If recurring, add the path to `scripts/repo_sync_public_mqgt_h1_phase4b.sh`.

---

## Parameter alignment reminder

If console or script parameters diverge, align to:

- **Z_eff:** 1–2
- **n:** 0.1–3×10²⁰ m⁻³
- **τ_E,eff:** a_tau=0.45
- **η_α:** coherence coupling
- **phase_map τ_E range:** 1.5–6 s

---

## Positioning / wording guardrails

Keep the public wording conservative and consistent:

- **Fusion console:** illustrative 0D D–T browser toy, not a reactor-design or validation tool
- **Multi-channel exclusion plot:** Phase II parameter-space context for Anchor / parameter-card discussions
- **H1 methods note:** methods/status document, not a primary new-physics claim
- **Coherence / recursive demos:** exploratory visualizations and execution-layer tools, not referee-safe evidence artifacts

---

## Procedure

### Step 1: Commit (no network)

```bash
cd /path/to/TOE
./scripts/repo_sync_public_mqgt_h1_phase4b.sh
```

**Success:** `git status` shows a new commit or "Nothing staged" if already committed.

### Step 2: Push (requires explicit approval)

**Safety:** Per [SAFETY_CONSTITUTION.md](../SAFETY_CONSTITUTION.md), do **not** push without explicit human approval.

```bash
./scripts/repo_sync_public_mqgt_h1_phase4b.sh --push
```

**Success:** `git push origin main` completes.

---

## Report-back

```
Full session update:
  Commit: <git rev-parse --short HEAD>
  Pushed: YES | NO (awaiting approval)
  Live coherence toy: https://cbaird26.github.io/toe-2026-updates/zora_coherence.html
  Live console: https://cbaird26.github.io/toe-2026-updates/zora_fusion_console.html
  Error: <if any>
```

---

## Related

- Master handoff: [CODEX_HANDOFF.md](CODEX_HANDOFF.md)
- Fusion GitHub: [CODEX_HANDOFF_FUSION_GITHUB_UPDATE.md](CODEX_HANDOFF_FUSION_GITHUB_UPDATE.md)
- Sync script: [scripts/repo_sync_public_mqgt_h1_phase4b.sh](../scripts/repo_sync_public_mqgt_h1_phase4b.sh)
- Safety: [SAFETY_CONSTITUTION.md](../SAFETY_CONSTITUTION.md)
