# Codex Handoff — Update GitHub (Phase II submission status)

**Task:** Commit and push the Phase II submission status and doc updates to the TOE repo on GitHub.

**Repo:** `~/Downloads/TOE` (or workspace path to TOE). Default branch: `main` (confirm with `git branch`).

---

## Files to stage and commit

Stage these paths (all relative to TOE root):

- `docs/PHASE_II_SUBMISSION_STATUS_2026.md` (new)
- `docs/VIXRA_SUBMISSION_CHECKLIST.md`
- `docs/AI_VIXRA_SUBMISSION_BLOCK.md`
- `docs/RXIVERSE_SUBMISSION_BLOCK.md`
- `docs/ARXIV_SUBMISSION_BLOCK.md`
- `docs/CORPUS_2026_INDEX.md`
- `docs/INTEGRATED_MANUSCRIPT_INDEX.md`
- `docs/PHASE_II_CROSS_REFERENCE.md`
- `docs/PHYSICS_ONLY_SUBMISSION_PACKET_2026.md`
- `docs/CODEX_HANDOFF_GITHUB_UPDATE.md` (this file)
- `docs/CODEX_HANDOFF_UPDATE_ALL_PARAMETERS_AND_REPOS.md`
- `papers_sources/README_Phase_II_Submission.md`
- `README.md`

---

## Commands to run

From TOE repo root:

```bash
cd ~/Downloads/TOE   # or your TOE path

git add \
  docs/PHASE_II_SUBMISSION_STATUS_2026.md \
  docs/VIXRA_SUBMISSION_CHECKLIST.md \
  docs/AI_VIXRA_SUBMISSION_BLOCK.md \
  docs/RXIVERSE_SUBMISSION_BLOCK.md \
  docs/ARXIV_SUBMISSION_BLOCK.md \
  docs/CORPUS_2026_INDEX.md \
  docs/INTEGRATED_MANUSCRIPT_INDEX.md \
  docs/PHASE_II_CROSS_REFERENCE.md \
  docs/PHYSICS_ONLY_SUBMISSION_PACKET_2026.md \
  docs/CODEX_HANDOFF_GITHUB_UPDATE.md \
  docs/CODEX_HANDOFF_UPDATE_ALL_PARAMETERS_AND_REPOS.md \
  papers_sources/README_Phase_II_Submission.md \
  README.md

git status --short   # verify staged files

git commit -m "Phase II submission status: rxiVerse:2603.0061 live, ai.viXra submitted, arXiv ready; update all docs and README"

git push origin main
```

If the default branch is not `main`, use that branch name in the push (e.g. `git push origin master`).

---

## Commit message (exact)

```
Phase II submission status: rxiVerse:2603.0061 live, ai.viXra submitted, arXiv ready; update all docs and README
```

---

## Context

- Phase II paper is live on rxiVerse (2603.0061, 2026-03-17) and submitted to ai.viXra (form ref 17884572). All parameters and doc cross-references updated; push so GitHub reflects current state.
- This handoff and PHYSICS_ONLY_SUBMISSION_PACKET_2026.md are included in the commit.
- No .tex or code changes; documentation and README only.

---

## Success criteria

- `git status` clean (or only expected untracked files) after push.
- `git log -1` shows the commit with the message above.
- Remote (e.g. github.com/Cbaird26/toe-2026-updates or equivalent) shows the new commit.

---

## If push fails

- **Auth:** Ensure credentials or SSH key are set for GitHub.
- **Branch:** If repo uses `master`, run `git push origin master` instead.
- **Remote:** Confirm with `git remote -v`; push to the correct `origin`.
