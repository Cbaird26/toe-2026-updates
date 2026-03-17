# Codex Handoff: Push and Sync All Repos

**Date:** March 2026  
**Context:** Cursor agent ran sync; use this handoff if pushes need manual verification or fixes.

---

## One-Liner

```bash
cd ~/Downloads/TOE && ./scripts/git_update_all.sh
```

Or step-by-step:

```bash
# 1. TOE
cd ~/Downloads/TOE
git add -A
git status
git commit -m "Sync: corpus REVTeX, indexes" --allow-empty
git pull origin main
git push origin main

# 2. Full sync (Black-Book → toe-empirical-validation, TOE → toe-2026-updates, iCloud)
cd ~/Downloads/mqgt_scf_reissue_2026-01-20_010939UTC
./scripts/sync_to_public_and_push.sh

# 3. Black-Book (if remote is public-toe-empirical-validation)
cd ~/Downloads/mqgt_scf_reissue_2026-01-20_010939UTC
git add -A && git commit -m "Sync" --allow-empty 2>/dev/null || true
git push public-toe-empirical-validation main
```

---

## Repo Map

| Local Path | Remote | Purpose |
|------------|--------|---------|
| `~/Downloads/TOE` | origin → toe-2026-updates | Main corpus, docs, papers_sources |
| `~/Downloads/mqgt_scf_reissue_2026-01-20_010939UTC` (Black-Book) | public-toe-empirical-validation (no origin) | Code, tests, scripts → toe-empirical-validation |
| `~/Downloads/cbaird26-all-repos/toe-2026-updates` | origin | Clone receiving TOE rsync; commits and pushes |
| `~/Downloads/cbaird26-all-repos/toe-empirical-validation` | origin | Clone receiving Black-Book rsync; commits and pushes |

---

## Common Failures

1. **Push rejected (remote has work)**  
   `git pull origin main` (or `git pull --rebase origin main`) then `git push origin main`.

2. **No origin / push fails**  
   Black-Book has no `origin`; use `git push public-toe-empirical-validation main`.

3. **Auth**  
   Run `gh auth status` and re-login if needed.

---

## Verify

```bash
gh repo view Cbaird26/toe-2026-updates
gh repo view Cbaird26/toe-empirical-validation
```

---

## Key Paths

- Sync script: `~/Downloads/mqgt_scf_reissue_2026-01-20_010939UTC/scripts/sync_to_public_and_push.sh`
- Git update script: `~/Downloads/TOE/scripts/git_update_all.sh`
- Pull all repos: `~/Downloads/mqgt_scf_reissue_2026-01-20_010939UTC/scripts/pull_all_repos.sh`
