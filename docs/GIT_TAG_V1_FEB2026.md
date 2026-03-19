# Git Tag: v1.0-Feb2026 (February Baseline)

**Purpose:** Freeze the pre–Phase II state as a provenance anchor. Tag the commit that represents the February 2026 baseline (Word/PDF drafts before Phase II lock-in).

---

## Command

From the repo root:

```bash
cd ~/Downloads/TOE   # or path to toe-2026-updates

# Find the commit you want to tag (e.g. last commit before Phase II conversion)
# If current HEAD is post–Phase II, use a specific commit hash.
git log --oneline -20

# Tag (replace COMMIT_HASH with the hash of the Feb baseline commit, or omit for current HEAD)
git tag -a v1.0-Feb2026 -m "February 2026 baseline: pre-Phase-II expansive formulation"

# Push tag to origin
git push origin v1.0-Feb2026
```

If you want to tag the **current** HEAD (i.e. the state right before tagging):

```bash
git tag -a v1.0-Feb2026 -m "February 2026 baseline: pre-Phase-II expansive formulation"
git push origin v1.0-Feb2026
```

---

## Release note text (for GitHub Releases, if created)

**v1.0-Feb2026 — February 2026 Baseline**

Pre–Phase II expansive formulation. Historical anchor for the corpus before:
- Phase II scalar-singlet EFT lock-in
- GKSL measurement container formalization
- H2 interferometric visibility blade
- REVTeX corpus conversion

The Phase II start (March 2026) supersedes this baseline for referee-facing work. This tag is retained for provenance and transparency.

---

## Optional: Create GitHub Release

1. GitHub → cbaird26/toe-2026-updates → Releases → Draft a new release
2. Choose tag: v1.0-Feb2026
3. Title: February 2026 Baseline
4. Paste the release note text above
5. Publish
