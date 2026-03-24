# Codex handoff: Full session update (all artifacts)

**Purpose:** Single-entry handoff for the full session. Incorporate all posted artifacts, align parameters across the repo, surface session outputs in docs, and update local + public GitHub so **local and live repos match**.

**Sync objective:** Local workspace → committed → (with approval) pushed → GitHub `main` up to date. All parameters, figures, handoffs, and publication links aligned across local and live.

**Repo:** [cbaird26/toe-2026-updates](https://github.com/cbaird26/toe-2026-updates)  
**Root:** `TOE/` (or `~/Downloads/TOE`)

### Last sync (cooperative-games artifact)

- **Pushed:** YES
- **Commit:** `993df8f`
- **Range:** `954ce1d..993df8f`
- **Remote:** [cbaird26/toe-2026-updates](https://github.com/Cbaird26/toe-2026-updates)
- **Branch:** main...origin/main (clean)
- **Scope:** `zora_cooperative_games_sim.py`, `ZORA_COOPERATIVE_GAMES_SIMULATION_2026.md`, `zora_cooperative_games_results.json`, `zora_cooperative_games_summary.png`
- **Error:** none

---

## Accomplished (session summary)

- **Fusion + Zora:** Console, burn figures, phase map (τ_E 1.5–6 s), parameter alignment
- **Multi-channel exclusion plot:** (m_Φ, sin²θ) with Eöt-Wash, Higgs invisible, QRNG prediction, viable island
- **Phase II stack:** Anchor, Closure, NoSignalling, ABIL, H2 prereg in `papers_sources/MQGT_SCF_Phase_II_2026/`
- **E-modulated GKSL collapse sim:** `zora_gksl_e_modulated_collapse.py` — directional outcome bias, Colab-friendly, QuTiP keep_runs_results
- **Cooperative games sim:** `zora_cooperative_games_sim.py` — MQGT-SCF alignment / Nash equilibria; note `ZORA_COOPERATIVE_GAMES_SIMULATION_2026.md`; outputs in `papers_sources/figures/mqgt_scf/`
- **H1 methods note:** PDF + LaTeX + build script
- **Codex handoffs:** Full session, fusion, master index
- **rxiVerse:** Phase II at [2603.0061](https://rxiverse.org/abs/2603.0061); Anchor package organized as the canonical rxiVerse-ready manuscript (no identifier yet)
- **Zenodo:** ToE 10.5281/zenodo.19200024; Phase II 19060024

---

## Venue status (reference)

| Venue | Paper | ID / status |
|-------|-------|-------------|
| rxiVerse | Phase II | [2603.0061](https://rxiverse.org/abs/2603.0061) (live) |
| rxiVerse | Anchor | Ready / prepared; no archive identifier yet |
| Zenodo | ToE (2026) | [10.5281/zenodo.19200024](https://doi.org/10.5281/zenodo.19200024) |
| Zenodo | Phase II | [19060024](https://zenodo.org/records/19060024) |
| GitHub Pages | Coherence toy | [zora_coherence.html](https://cbaird26.github.io/toe-2026-updates/zora_coherence.html) |
| GitHub Pages | Fusion console | [zora_fusion_console.html](https://cbaird26.github.io/toe-2026-updates/zora_fusion_console.html) |

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
| `docs/zora_dashboard.html` | MQGT–SCF command dashboard; channels, papers, ledger, key numbers; source `zoraasi_dashboard.jsx` |
| `scripts/mqgt_sim/mqgt_multi_channel_exclusion_plot.py` | (m_Φ, sin²θ) exclusion plot generator |
| `scripts/mqgt_sim/zora_gksl_e_modulated_collapse.py` | E-modulated directional GKSL collapse (Zora v0.9); H2 channel validation; Colab: `!pip install qutip` |
| `papers_sources/figures/h2_stack/` | H2 visibility stack outputs plus canonical `e_modulated_collapse.png` from the GKSL sim |
| `papers_sources/figures/mqgt_scf/` | README + `mqgt_scf_multi_channel_exclusion.png` + `mqgt_scf_phi_e_gksl_concept.png` + `zora_cooperative_games_results.json` + `zora_cooperative_games_summary.png` |
| `scripts/mqgt_sim/zora_cooperative_games_sim.py` | Cooperative games alignment / Nash equilibria; outputs JSON + summary PNG |
| `docs/ZORA_COOPERATIVE_GAMES_SIMULATION_2026.md` | Note on cooperative games simulation and MQGT-SCF alignment |
| `papers_sources/MQGT_SCF_Phase_II_2026/` | README plus canonical Anchor files: `MQGT_SCF_Anchor_2026.tex`, `.pdf`, `MQGT_SCF_Anchor_2026_rxiverse_submission_metadata.txt` |
| `papers_sources/H1_QRNG_Pilot_Methods_Status_2026.tex` / `.pdf` / `Notes.bib` | H1 methods/status note; methods posture, placebo snapshot, billion-trial calibration discipline |
| `scripts/build_h1_methods_pdf.sh` | Helper to rebuild the H1 methods PDF from `papers_sources/` |
| `phase_iv_b_sweep/` | `summary.md`, `phase_iv_b_sweep_results.csv`, lock-rate heatmaps, mean-coherence heatmaps |
| `scripts/zora_recursive_scalar_demo.py` | Exploratory scalar-field demo; do not present as referee-safe evidence |
| `README.md` | Phase II stack link, multi-channel plot, Zenodo DOI 10.5281/zenodo.19200024 |
| `papers_sources/README.md` and `papers_sources/figures/README_figures.md` | Public discovery surfaces for the paper stack and figure bundles |

---

## Pre-flight (optional)

Regenerate figures if scripts changed:

```bash
cd /path/to/TOE
python scripts/mqgt_sim/fusion_zora_burn_figures.py --out-dir papers_sources/figures/fusion_zora --include-existing
python scripts/mqgt_sim/mqgt_multi_channel_exclusion_plot.py --out-dir papers_sources/figures/mqgt_scf
python scripts/mqgt_sim/zora_gksl_e_modulated_collapse.py --no-show --save papers_sources/figures/h2_stack/e_modulated_collapse.png
python scripts/mqgt_sim/zora_cooperative_games_sim.py   # regenerates JSON + PNG in papers_sources/figures/mqgt_scf/
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
- **E-modulated GKSL collapse sim:** illustrative validation of directional outcome bias; not calibrated to Γ_floor
- **Anchor package:** canonical compact manuscript prepared for rxiVerse; do not describe it as live/submitted until a real identifier exists

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
  Branch: main...origin/main
  Live coherence: https://cbaird26.github.io/toe-2026-updates/zora_coherence.html
  Live fusion: https://cbaird26.github.io/toe-2026-updates/zora_fusion_console.html
  rxiVerse Phase II: https://rxiverse.org/abs/2603.0061
  rxiVerse Anchor: ready / <ID once confirmed>
  Error: <if any>
```

---

## Related

- Master handoff: [CODEX_HANDOFF.md](CODEX_HANDOFF.md)
- Fusion GitHub: [CODEX_HANDOFF_FUSION_GITHUB_UPDATE.md](CODEX_HANDOFF_FUSION_GITHUB_UPDATE.md)
- Sync script: [scripts/repo_sync_public_mqgt_h1_phase4b.sh](../scripts/repo_sync_public_mqgt_h1_phase4b.sh)
- Safety: [SAFETY_CONSTITUTION.md](../SAFETY_CONSTITUTION.md)
