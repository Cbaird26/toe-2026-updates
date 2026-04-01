# Claude handoff — docs hub, zoraasi mobile, Foundation mobile shell (April 2026)

**Audience:** Next Claude (or any executor) continuing work in **`cbaird26/toe-2026-updates`** / local **`TOE/`** mirror.  
**Freeze tag (annotated):** `mobile-shell-2026-04-01` → commit **`5363bad`** (“style(docs): align hub with portal reference…”).  
**Note:** Tag `^{}` resolves to that commit; `git rev-parse mobile-shell-2026-04-01` prints the **tag object** hash, not the commit.

---

## 1. What we set out to fix

| Area | Problem | Direction |
|------|---------|-----------|
| **Docs landing** (`docs/index.html`) | Felt tacky / odd copy under the title; JetBrains + orbit diagram didn’t match the “portal” reference | Rebuilt to match the **Zora Framework Portal** reference (Cormorant + IBM Plex, hero, cards) — see user files `index (1).html` style |
| **Zoraasi mobile** (`docs/zoraasi-mobile/`) | Hand-built single-file page was replaced by **upstream Vite build** from `Cbaird26/zoraasi`; mobile layout still broke (“windows”) | **Injected CSS** + build script; later fixed **grid** overflow (not flex) on phones |
| **Foundation app** (`docs/theory-of-everything-foundation/index.html`) | Tab strip vs main content misaligned on notched phones | **Swapped horizontal safe-area** on `.main` / `.footer` (padding TRBL must use `inset-right` on the right, `inset-left` on the left) |
| **Git** | Reproducible snapshot | Annotated tag + push; optional CI workflow for zoraasi bundle |

---

## 2. Files touched (by theme)

### Docs hub — portal-style landing

- **`docs/index.html`**  
  - Fonts: **Cormorant Garamond** + **IBM Plex Mono** (Google Fonts).  
  - Tokens: `--void`, `--panel`, `--border`, `--glow`, `--glow2`, etc. (aligned with reference portal).  
  - Structure: compact **hero** (eyebrow, gradient title span on “docs”, italic tagline), **CTAs** (“Launch Foundation app”, “Pages deploy notes”), **gradient divider**, **`app-grid` / `app-card`** route list with tags (Flagship, Lab, Snapshot, Map, Gallery).  
  - Removed: orbit figure, dot legend, aggressive `overflow-wrap: anywhere` / `word-break` on `body` (moved break behavior to cards only where needed).  
  - Still loads **`js/toe-console-bridge.js`** for same-origin console behavior.

### Zora Discovery mobile (upstream Vite → Pages)

- **`scripts/build_zoraasi_mobile.sh`**  
  - Clones `https://github.com/Cbaird26/zoraasi.git` into **`TOE/.zoraasi_build`**, copies **`scripts/zoraasi-mobile.css`** → `src/mobile.css`, prepends `import "./mobile.css";` to **`src/main.jsx`** if missing, ensures viewport meta in **`index.html`**, runs **`npm ci || npm install`** + **`npm run build`**, copies **`dist/`** → **`docs/zoraasi-mobile/`**.

- **`scripts/zoraasi-mobile.css`** (source of truth for the “skin”)  
  - Safe areas: `#root` uses **`max(12px, env(safe-area-inset-*))`** on all sides; **`width: 100%` + `max-width: 100%`** (avoid **`100vw`** + padding horizontal scroll).  
  - **`#root * { min-width: 0 }`** so grid/flex children can shrink.  
  - **Critical:** Upstream **`App.jsx`** uses a **CSS grid** with  
    `grid-template-columns: minmax(0, 1.7fr) minmax(320px, 0.9fr)`  
    The **`minmax(320px, …)`** track **does not collapse** on narrow screens → horizontal overflow.  
    **Fix:** `@media (max-width: 900px) { #root [style*="minmax(320px"] { grid-template-columns: 1fr !important; } }`  
  - React serializes **`flex-direction`**, not `flexDirection` — older selectors targeting `flexDirection` in `[style]` were wrong; use **`flex-direction`** substrings.  
  - **`h1`** clamped on small viewports; pattern container **`min-height`** softened where inline styles force 760px.

- **`docs/zoraasi-mobile/`** after build: Vite output (`index.html`, `assets/index-*.js`, `assets/index-*.css`, icons, manifest). The **hashed** CSS filename changes each build; **`scripts/zoraasi-mobile.css`** must stay in sync or **re-run the build script** so `index.html` points at new hashes.

- **`.github/workflows/zoraasi-mobile-sync.yml`**  
  - **`workflow_dispatch`**: clone + run `scripts/build_zoraasi_mobile.sh`, commit `docs/zoraasi-mobile` if changed, message ends with **`[skip ci]`** to avoid loops.

### Foundation — mobile shell alignment

- **`docs/theory-of-everything-foundation/index.html`** (inline `<style>`)  
  - **Bug:** `padding` shorthand on `.main` and `.footer` had **left/right safe-area env vars swapped** (used `safe-area-inset-left` on the **right** side and vice versa). Fixed so **right** padding uses **`env(safe-area-inset-right)`** and **left** uses **`env(safe-area-inset-left)`**.  
  - **`html { overflow-x: hidden }`**.  
  - **`@media (max-width: 900px)`:** `.header`, `.tabs`, `.main`, `.footer` get **`width: 100%`**, **`max-width: 100%`**, **`box-sizing: border-box`**; **`.main .panel { min-width: 0 }`**; **`.opt-tabs` / `.lab-tabs`** wrap with gap; **`.tabs`** `scroll-padding-inline` for safe areas.

### Suite link copy (optional)

- Foundation **Suite** tab card for zoraasi-mobile may mention Vite bundle + build script (if present in your revision).

---

## 3. Commands the human already ran successfully

```bash
cd ~/Downloads/TOE
chmod +x scripts/build_zoraasi_mobile.sh
./scripts/build_zoraasi_mobile.sh
git add docs/zoraasi-mobile scripts .github
git commit -m "chore(docs): sync zoraasi-mobile from upstream Vite build"
git push
```

Tag maintenance (tag moved to include portal hub commit):

```bash
git tag -d mobile-shell-2026-04-01
git tag -a mobile-shell-2026-04-01 -m "Freeze: mobile shell + portal-style docs hub"
git push origin :refs/tags/mobile-shell-2026-04-01
git push origin mobile-shell-2026-04-01
```

---

## 4. Live URLs (GitHub Pages from `/docs`)

- **Docs hub:** `https://cbaird26.github.io/toe-2026-updates/`  
- **Foundation:** `https://cbaird26.github.io/toe-2026-updates/theory-of-everything-foundation/`  
- **Zoraasi mobile mirror:** `https://cbaird26.github.io/toe-2026-updates/zoraasi-mobile/`  
- **Canonical upstream Zora Discovery (same app, root deploy):** `https://cbaird26.github.io/zoraasi/`  

**Note:** Do **not** embed one `github.io` Pages site in an iframe inside another — GitHub sets framing headers; use **same-origin static files** (this build) or a **link**.

---

## 5. What to do next (if anything breaks)

| Symptom | Check |
|--------|--------|
| Zoraasi mobile layout wrong after upstream change | Re-run **`./scripts/build_zoraasi_mobile.sh`**; diff **`scripts/zoraasi-mobile.css`** against minified bundle if hashes changed. |
| New horizontal overflow on zoraasi | Inspect **inline `grid-template-columns`** in built JS — may need another **`[style*="…"]`** rule if the author changes the column definition. |
| Foundation tabs vs body offset on iPhone | Re-verify **`.main` / `.footer` / `.tabs` / `.header`** padding use **correct** `safe-area-inset-left` / `right`. |
| Docs hub looks wrong | Compare to freeze at **`5363bad`**; reference HTMLs were under user **`Downloads/index*.html`**. |

---

## 6. Safety / scope

- **`SAFETY_CONSTITUTION.md`** — no push or external publish without human approval when policy applies.  
- Prefer **small, scoped** CSS/HTML changes; avoid rewriting **`Cbaird26/zoraasi`** in TOE unless forking — the build script is the integration point.

---

## 7. Related repo docs

- **[CODEX_HANDOFF.md](CODEX_HANDOFF.md)** — H1 / executor baseline (different workstream).  
- **[docs/PAGES.md](PAGES.md)** — deploy / 404 notes (linked from hub secondary button).
