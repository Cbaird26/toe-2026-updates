# GitHub Pages (`toe-2026-updates`)

## Canonical URLs

| Page | URL |
|------|-----|
| **Pages hub (docs root)** | [cbaird26.github.io/toe-2026-updates/](https://cbaird26.github.io/toe-2026-updates/) — simple index; Foundation persists dials via `localStorage` (`mqgt_toe_console_v1`) on this origin |
| **Theory of Everything Foundation** | [cbaird26.github.io/toe-2026-updates/theory-of-everything-foundation/](https://cbaird26.github.io/toe-2026-updates/theory-of-everything-foundation/) |
| **Fold-Space Engine Lab** | […/fold-space-engine/](https://cbaird26.github.io/toe-2026-updates/fold-space-engine/) — static lab in `docs/fold-space-engine/` |
| **Warp artifact (HTML snapshot)** | […/artifacts/TOE_FOUNDATION_WARP_BLINDING_x1000.html](https://cbaird26.github.io/toe-2026-updates/artifacts/TOE_FOUNDATION_WARP_BLINDING_x1000.html) |
| Explicit `index.html` | […/theory-of-everything-foundation/index.html](https://cbaird26.github.io/toe-2026-updates/theory-of-everything-foundation/index.html) |

Source: [`docs/index.html`](index.html) (hub), [`docs/theory-of-everything-foundation/index.html`](theory-of-everything-foundation/index.html) (Foundation app), [`docs/js/toe-console-bridge.js`](js/toe-console-bridge.js) (shared dial storage for other `github.io` apps).

## Required GitHub settings (pick one)

If **`https://cbaird26.github.io/toe-2026-updates/`** returns **404**, the site is not being published yet. The files on `main` under `docs/` are not enough by themselves—you must turn Pages on.

### Option A — GitHub Actions (recommended; workflow in repo)

This repo includes [`.github/workflows/deploy-github-pages.yml`](../.github/workflows/deploy-github-pages.yml), which uploads the **`docs/`** folder as the static site on every push to `main`.

1. **Settings** → **Pages** → **Build and deployment** → **Source:** **GitHub Actions** (not “Deploy from a branch”).
2. Push to `main` (or re-run the workflow from the **Actions** tab). First run may need you to approve workflow permissions once.
3. After a green run, the site URL appears under **Settings → Pages** and in the workflow summary. Allow a minute for the CDN.

### Option B — Deploy from branch

1. **Settings** → **Pages** → **Source:** **Deploy from a branch**.
2. **Branch:** `main`, **Folder:** `/docs`.
3. Save and wait a few minutes.

Do **not** leave Source unset, and do not point **Folder** at `/ (root)` unless the HTML lives at the repository root.

**Private repository:** GitHub Pages for private repos may require a **paid** plan or a **public** repo for free project Pages—check [GitHub Pages documentation](https://docs.github.com/pages/getting-started-with-github-pages/about-github-pages). If the repo is private and Pages is blocked, make the repo public or use Actions + allowed visibility per GitHub’s current rules.

## If you see 404

- **Entire site 404** → Pages source not configured (see above) or private-repo limitation.
- Confirm the files exist on `main` under `docs/` ([browse on GitHub](https://github.com/cbaird26/toe-2026-updates/tree/main/docs)).
- Confirm [`docs/.nojekyll`](.nojekyll) is present so Jekyll does not skip needed static assets.
- Hard-refresh or try a private window (CDN cache).
- The **site root** (`/`) is the hub [`docs/index.html`](index.html).

## Optional short URL (`theory-of-everything-foundation` org site)

To serve **`https://cbaird26.github.io/theory-of-everything-foundation/`** (without `toe-2026-updates` in the path):

1. Create a repository named **`theory-of-everything-foundation`** under **cbaird26**.
2. Add **`index.html` at the repository root** (copy from `docs/theory-of-everything-foundation/index.html` in this repo).
3. Enable **Settings → Pages** on that repo: branch **`main`**, folder **`/` (root)**.
4. Update any absolute links inside the app if they should point at the new base URL.

That deployment is **independent** of `toe-2026-updates`.
