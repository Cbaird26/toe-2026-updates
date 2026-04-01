# GitHub Pages (`toe-2026-updates`)

## Canonical URLs

| Page | URL |
|------|-----|
| **Hub (docs root)** | [cbaird26.github.io/toe-2026-updates/](https://cbaird26.github.io/toe-2026-updates/) |
| **Theory of Everything Foundation** | [cbaird26.github.io/toe-2026-updates/theory-of-everything-foundation/](https://cbaird26.github.io/toe-2026-updates/theory-of-everything-foundation/) |
| Explicit `index.html` | […/theory-of-everything-foundation/index.html](https://cbaird26.github.io/toe-2026-updates/theory-of-everything-foundation/index.html) |

Source: [`docs/index.html`](index.html) (hub), [`docs/theory-of-everything-foundation/index.html`](theory-of-everything-foundation/index.html) (app).

## Required GitHub settings

1. Repo **cbaird26/toe-2026-updates** → **Settings** → **Pages**.
2. **Build and deployment** → **Source:** Deploy from a branch.
3. **Branch:** `main`, **Folder:** `/docs` (not `/ (root)` unless the site is moved).
4. Save. Builds usually appear within about one to five minutes after a push to `main`.

This repo does **not** use a dedicated Pages workflow for the static `docs/` tree; hosting is the default **branch + `/docs`** behavior. Other workflows (for example Fold-Space Engine CI) do not replace Pages configuration.

## If you see 404

- Confirm the files exist on `main` under `docs/` (use the GitHub file browser).
- Confirm [`docs/.nojekyll`](.nojekyll) is present so Jekyll does not skip needed static assets.
- Hard-refresh or try a private window (CDN cache).
- The **site root** (`/`) is the hub [`docs/index.html`](index.html); it no longer auto-redirects only to the ecosystem illustration.

## Optional short URL (`theory-of-everything-foundation` org site)

To serve **`https://cbaird26.github.io/theory-of-everything-foundation/`** (without `toe-2026-updates` in the path):

1. Create a repository named **`theory-of-everything-foundation`** under **cbaird26**.
2. Add **`index.html` at the repository root** (copy from `docs/theory-of-everything-foundation/index.html` in this repo).
3. Enable **Settings → Pages** on that repo: branch **`main`**, folder **`/` (root)**.
4. Update any absolute links inside the app if they should point at the new base URL.

That deployment is **independent** of `toe-2026-updates`.
