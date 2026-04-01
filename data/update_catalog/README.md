# `UPDATE` folder catalog

Canonical source folder: **`~/Downloads/UPDATE`** (all-caps name on disk). Override with env `UPDATE_DIR` if yours lives elsewhere.

## Generate manifests and route assets

From the TOE repo root:

```bash
python3 scripts/update_folder_ingest.py
```

- Writes **`manifest_update.csv`** and **`manifest_update.json`** here (relative paths, sizes, suggested themes, SHA-256 when readable).
- Writes **`UPDATE_PATH_CONFIRMED.txt`** with the resolved absolute path and whether the directory existed at run time.
- Copies Scalar Halo / Cosmic Piano / SPARC-class PNGs into `data/scalar_halo_campaign/figures/...` (same UUID-stripping rules as `scripts/scalar_halo_campaign/organize_assets.py`) and **merges** new rows into `data/scalar_halo_campaign/artifact_manifest.csv`.
- Copies likely finance/dashboard screenshots into `docs/internal/finance_os/screenshots/` (heuristic filename keywords).

Use `--no-copy` for inventory only.

Rasters under `data/scalar_halo_campaign/figures/**` remain gitignored per repo policy; manifests and this README stay tracked.
