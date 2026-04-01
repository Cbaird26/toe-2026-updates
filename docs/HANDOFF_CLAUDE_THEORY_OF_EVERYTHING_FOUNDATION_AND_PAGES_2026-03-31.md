# Handoff for Claude — Theory of Everything Foundation + GitHub Pages

**Audience:** Next Claude (or Codex) session continuing Christopher Michael Baird’s TOE / MQGT-SCF web work.  
**Repo:** `cbaird26/toe-2026-updates` (GitHub). Local path often `~/Downloads/TOE/`.  
**Human:** Christopher Michael Baird — frustrated with GitHub Pages configuration; treat Pages setup as **high-touch, step-by-step**.

---

## What exists (do not lose this)

### Flagship static app (single HTML, zero build)

- **Path:** [`docs/theory-of-everything-foundation/index.html`](../theory-of-everything-foundation/index.html)
- **Live URL (once Pages works):** `https://cbaird26.github.io/toe-2026-updates/theory-of-everything-foundation/`
- **Contents:** Tabs — Warp Core + toroidal canvas (2D canvas “geometry engine”), Decision Engine (A/B/C), Framework (equations), Suite (links to Zora apps + thesis). ENGAGE runs a warp sequence; **warp visuals use a white-hot pulse** (white button glow, white-blue torus flash, white grid, 3× white center orb, shockwave rings, white wash, header “WARPING”, phase text white) vs calm cyan/colored idle state.
- **Suite tab** includes cards for this app + Fold-Space Engine + Zora Discovery, etc., with LIVE/BETA tags.

### Pages hub (site entry)

- **Path:** [`docs/index.html`](index.html) — hub with primary link to `theory-of-everything-foundation/`, plus ecosystem illustration and top-10 gallery links (no longer only redirecting to ecosystem).

### Documentation

- **Path:** [`docs/PAGES.md`](PAGES.md) — canonical URLs, **Option A (GitHub Actions)** vs **Option B (Deploy from branch `/docs`)**, private-repo note, troubleshooting.

### CI: GitHub Pages via Actions

- **Path:** [`.github/workflows/deploy-github-pages.yml`](../.github/workflows/deploy-github-pages.yml) — on push to `main`, uploads **`docs/`** as the static artifact and deploys with `actions/deploy-pages`.
- **Requires:** Repo **Settings → Pages → Source: GitHub Actions** (not enough to only commit the workflow).

### Other references in README

- [`README.md`](../README.md) — GitHub Pages bullet lists Foundation URL + `PAGES.md`.
- [`docs/SYSTEM_INDEX.md`](SYSTEM_INDEX.md) — “Start here” row for hub + Foundation + `PAGES.md`.

---

## Critical blocker: site still 404 until Pages is turned on

**Observation:** Requests to `https://cbaird26.github.io/toe-2026-updates/` (and nested paths) have returned **404** while files on `main` under `docs/` are present. **Pushing code does not publish the site** until GitHub Pages is configured.

**Simplest fix for the human (prefer this first):**

1. `https://github.com/cbaird26/toe-2026-updates/settings/pages`
2. **Build and deployment → Source:** **Deploy from a branch**
3. Branch: **`main`**, Folder: **`/docs`**
4. Save; wait 5–10 minutes; test in incognito.

**Alternative:** Set Source to **GitHub Actions**, ensure **Actions** workflow “Deploy GitHub Pages” runs green (may need workflow permissions on first run).

**If repo is private:** confirm whether the account allows GitHub Pages for private repos; may need **public** repo or paid feature per current GitHub policy.

---

## Git history pointers (approximate)

- Foundation app added under `docs/theory-of-everything-foundation/` (e.g. commit `9d291e8` range — verify with `git log -- docs/theory-of-everything-foundation/`).
- Hub + `PAGES.md` + README/SYSTEM_INDEX updates (e.g. `6f94461`).
- Pages deploy workflow + expanded `PAGES.md` — user may have merged as “ci: deploy docs/ to GitHub Pages via Actions…” (verify with `git log -- .github/workflows/deploy-github-pages.yml`).

---

## Related apps (not in this single file)

- **Fold-Space Engine:** Vite app under `apps/fold-space-engine/`; build script `scripts/build_fold_space_engine.sh` → output under `docs/fold-space-engine/` for Pages. Separate from the Foundation single-file app.
- **Deployed Zora URLs** (external): Discovery, ZoraASI, Refit variants — listed in Foundation Suite tab and README.

---

## Safety / authority

- **[SAFETY_CONSTITUTION.md](../SAFETY_CONSTITUTION.md)** — no `git push`, credential use, or publishing without explicit human approval when in doubt.
- **MQGT-SCF:** framework is operational / falsifiable; browser demos are illustrative unless tied to preregistered pipelines (see H1/H2 docs elsewhere).

---

## Suggested next actions for Claude

1. Confirm with human whether **`toe-2026-updates` is public or private** and what **Pages → Source** currently shows.
2. If 404 persists after **Deploy from branch → main → /docs**, capture the **exact status line** from Settings → Pages (published URL or error).
3. Avoid duplicating handoff files; update this doc or `PAGES.md` if the resolution changes.
4. Optional: after Pages is green, add one line to `README.md` “Pages live as of &lt;date&gt;” only if the human wants it.

---

## Quick copy-paste for human

```text
Hub:     https://cbaird26.github.io/toe-2026-updates/
Foundation: https://cbaird26.github.io/toe-2026-updates/theory-of-everything-foundation/
Pages settings: https://github.com/cbaird26/toe-2026-updates/settings/pages
```

---

*End handoff — Theory of Everything Foundation + GitHub Pages, 2026-03-31.*
