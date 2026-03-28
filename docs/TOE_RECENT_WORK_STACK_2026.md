# ToE recent work stack (March 24-27, 2026)

This is the current add-on packet for the work completed between **March 24, 2026** and **March 27, 2026**.

## Addendum PDFs (choose by audience)

| PDF | Use when |
| --- | --- |
| `papers_sources/TOE_Recent_Work_Addendum_2026_physics.pdf` | **Referee-facing / physics-only packets:** Phase II, H1, top-10 stack, Scalar Halo / Cosmic Piano summary. No March 25 repo-boundary or finance/trading documentation. |
| `papers_sources/TOE_Recent_Work_Addendum_2026.pdf` | **Full operating record:** everything in the physics variant **plus** the cross-repository operating-boundary documents (March 25 handoffs under `docs/handoffs/2026-03/`). |

- Full addendum source: `papers_sources/TOE_Recent_Work_Addendum_2026.tex`
- Physics variant source: `papers_sources/TOE_Recent_Work_Addendum_2026_physics.tex`
- Shared body: `papers_sources/toe_recent_work_addendum_shared.tex`
- Build: `bash scripts/build_toe_recent_work_addendum_pdf.sh` (full only) or `bash scripts/build_toe_recent_work_addendum_pdf.sh --physics` (full + physics) or `--physics-only`

## Recommended merge / appendix order

1. `papers_sources/Addendum_2026_ToE_Companion.pdf`
2. your canonical main ToE PDF
3. `papers_sources/Evidence_Emergent_Matter_Quantum_Vacuum_MQGT-SCF_2026.pdf`
4. `papers_sources/MQGT_SCF_Phase_II_2026/MQGT_SCF_Anchor_2026.pdf`
5. `papers_sources/H1_QRNG_Pilot_Methods_Status_2026.pdf`
6. Recent work addendum (pick one for this slot):
   - **Referee / physics-only packet:** `papers_sources/TOE_Recent_Work_Addendum_2026_physics.pdf`
   - **Full operating record** (includes March 25 repo-boundary docs): `papers_sources/TOE_Recent_Work_Addendum_2026.pdf`

You normally attach **one** of the two at position 6; use the full PDF only when the finance/repo-boundary narrative must travel with the stack.

## Single merged PDF (optional)

To concatenate slots 1–6 into one file (same order as above), run from the repo root:

```bash
bash scripts/merge_toe_scientific_pdf_stack.sh --physics   # slot 6 = physics addendum (default)
bash scripts/merge_toe_scientific_pdf_stack.sh --full       # slot 6 = full addendum
```

Default main ToE at slot 2 is `papers_sources/A_Theory_of_Everything_CM_Baird_et_al_2026.pdf`. Override if needed:

```bash
MAIN_TOE="$PWD/papers_sources/A_Unified_Theory_of_Everything_CM_Baird_et_al_2026.pdf" bash scripts/merge_toe_scientific_pdf_stack.sh --physics
# or: bash scripts/merge_toe_scientific_pdf_stack.sh --physics --main-toe /path/to/main.pdf
```

Outputs:

- `papers_sources/TOE_scientific_stack_merged_physics_2026.pdf`
- `papers_sources/TOE_scientific_stack_merged_full_2026.pdf` (with `--full`)

Requires **pdfunite** (Poppler) or **gs** (Ghostscript). Use `--dry-run` to list paths without merging.

## What the new addendum covers

- March 24, 2026 paper/simulation updates:
  - Anchor refresh
  - H1 methods note
  - cooperative-games note
  - canonical ZoraASI top-10 simulation stack
- March 25, 2026 operating-boundary docs (**full addendum only**):
  - repo inventory
  - repo-boundary handoff
  - `zora-equity` structure/runbook notes
- March 27, 2026 local campaign ingest:
  - `data/scalar_halo_campaign/`
  - `artifact_manifest.csv` (refresh with `scripts/scalar_halo_campaign/organize_assets.py` or `refresh_scalar_halo_campaign.sh`; counts in the PDF are illustrative—**the CSV is authoritative**)
  - scalar-halo, SWELLS, axis-ratio, Cosmic Piano, SPARC, and inner-halo figures/tables/reports

## Scalar Halo campaign follow-up

- When Cursor assets or bundles change, run `./scripts/scalar_halo_campaign/refresh_scalar_halo_campaign.sh` (or `organize_assets.py`) so `artifact_manifest.csv` stays aligned with disk.
- For **referee-facing** merge orders, prefer **`TOE_Recent_Work_Addendum_2026_physics.pdf`** at the addendum slot so finance/repo-boundary material does not appear in the physics packet. Keep **`TOE_Recent_Work_Addendum_2026.pdf`** when the full operating record (including March 25 boundary docs) must travel with the stack.

## Important note on local-only assets

The scalar-halo raster figures under `data/scalar_halo_campaign/figures/**` are intentionally gitignored. The addendum PDF summarizes that work so the packet remains usable even when those PNGs are kept local.
