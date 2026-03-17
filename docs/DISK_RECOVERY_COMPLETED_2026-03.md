# Disk Recovery Plan — Completed 2026-03

## Summary

The disk space recovery plan has been implemented. Actions taken:

### Completed

1. **Diagnostics** — Run to identify largest consumers
2. **Dev caches purged** — pip, npm, Homebrew
3. **Redundant mqgt bundles moved to Trash** — Kept canonical Black-Book (`mqgt_scf_reissue_2026-01-20_010939UTC`). Moved to Trash:
   - mqgt_frequency_atlas_bundle (2)
   - mqgt_world_grade_bundle
   - mqgt_scf_reissue_2026-01-21_155709_UTC (3)
   - mqgt_reissue_bundle_2026-01-22_193258_UTC
   - mqgt_scf_reissue_2026-01-21_155709_UTC_reissue_2026-01-22_193258_UTC
   - mqgt_scf_reissue_2026-01-21_155709_UTC_reissue_2026-01-22_193258_UTC_regen_2026-01-22_214248_UTC
   - mqgt_reissue_bundle_2026-01-22_193258_UTC_regen_2026-01-22_214248_UTC
4. **Ollama cache** — Removed (if present)
5. **Hugging Face cache** — Removed (if present)
6. **Python/Node cleanup** — Removed `.venv`, `node_modules`, `__pycache__` under TOE and Black-Book

### Restore if needed

- **TOE .venv:** `cd ~/Downloads/TOE && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt` (if requirements.txt exists)
- **node_modules:** `npm install` or `yarn` in each project
- **Bundles in Trash:** Recover from `~/.Trash` within ~30 days before macOS purges

### Review (optional next steps)

- **cbaird26-all-repos** — Check size with `du -sh ~/Downloads/cbaird26-all-repos`. Consider moving to external drive if large.
- **ZoraASI vault** — `data/zoraasi_export/conversations.json` is large (~34MB). Back up before any trimming. Options: archive old conversations, export to compressed format.
- **Xcode DerivedData** — If you use Xcode: `rm -rf ~/Library/Developer/Xcode/DerivedData/*` can free 5–20GB.

### Scripts added

- `scripts/disk_recovery_consolidate_bundles.sh` — Re-run with `--dry-run` to preview; without arg to move more bundles to Trash.
