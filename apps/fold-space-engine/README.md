# Fold-Space Engine (MQGT–SCF interactive lab)

**Internal surface:** the Probability Sculptor panel is the default view. Fold-Space Engine, Timeline Selector, Jhāna Engine, Teleological Accelerator, and Qualion Chamber share the same React shell as companion panels.

This is **illustrative software**—a canvas visualization and toy controls—not a claim about deployable hardware.

## Correctness checks

Automated tests cover the **branch weight normalization** used by the Probability Sculptor and Timeline Selector:

- `npm test` runs Vitest on `src/math.js` (probabilities sum to 1; uniform limit at \(\eta=0\); invalid \(Z\) rejected).

Canvas rendering and particle dynamics are not formally verified here; they are visualization-only.

## Develop

```bash
cd apps/fold-space-engine
npm install
npm run dev
```

Open the URL Vite prints (usually `http://127.0.0.1:5173`).

## Build local static bundle

From the **repository root**:

```bash
bash scripts/build_fold_space_engine.sh
```

This runs tests, builds with Vite (`base: ./`), and copies `apps/fold-space-engine/dist/*` into `docs/fold-space-engine/` for local or private use.

## Source lineage

Original single-file prototype: `~/Downloads/FOLD-SPACE ENGINE.jsx` — integrated here with extracted `math.js` for testable probability logic.
