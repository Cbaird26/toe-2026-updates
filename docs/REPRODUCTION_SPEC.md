# Reproduction spec for spine repos

This doc specifies what the TOE/MQGT-SCF replication pipeline expects from the spine repo(s) (e.g. **toe-empirical-validation** or **mqgt-analysis**) so that [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md) and [REPLICATION_LADDER.md](REPLICATION_LADDER.md) can point to a single one-command path.

---

## Required entrypoint

- **One command or script** that runs the analysis for at least **one channel** (QRNG preferred, or fifth-force + cosmology), produces figures and/or constraint outputs, and exits with success/failure.
- **Documentation:** A README section that states: (1) clone repo, (2) install dependencies (if any), (3) run the entrypoint (e.g. `./run_all.sh` or `python run_channel.py --channel qrng`), (4) where outputs are written.
- **Pinnable artifact:** Replicators should be able to pin a commit (e.g. `git checkout <SHA>`) and reproduce; the repo may optionally output a checksum of the run for comparison.

---

## Canonical command (required for replication ladder)

The spine repo must support this **exact** command (or document the single equivalent in README):

```bash
./scripts/run_all.sh --channel qrng --seed 0 --out artifacts/
```

- `--channel qrng`: run QRNG channel only (or document the channel name the repo uses).
- `--seed 0`: fixed RNG seed for reproducibility (replicators may try other seeds for rung (c)).
- `--out artifacts/`: write all outputs (figures, constraint files, posterior samples) here. No other path for "official" replication.

## Suggested implementation (toe-empirical-validation)

- Add a script `scripts/run_all.sh` (or top-level `run_all.sh` that forwards to it) that:
  - Accepts `--channel qrng`, `--seed 0`, `--out artifacts/` (or equivalent).
  - Installs or checks for required environment (e.g. Python, key packages).
  - Runs the analysis scripts for the chosen channel.
  - Writes figures/constraints to the specified output directory (e.g. `artifacts/`).
  - Exits 0 on success.
- In README.md, add a "One-command reproduction" section with the canonical command above and a note to pin the commit hash before running.

Once this exists, [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md) §5 and [REPLICATION_LADDER.md](REPLICATION_LADDER.md) already reference it; no change needed in this repo unless the repo URL or command name changes.

---

## Verification (no guessing: is GitHub aligned?)

From the TOE repo root, run:

```bash
./scripts/verify_pushed.sh
```

This script: runs `git fetch origin`, checks that `HEAD == origin/main`, and greps `origin/main:docs/REPLICATION_LADDER.md` for the canonical command string and the `qrng-falsification-claim` anchor. If all checks pass, the GitHub version matches the doc contract. If the working tree is clean and the script exits 0, GitHub has the current state.

---

## Spine repo: CI, null fixture, and comparison

- **Replication contract (CI):** The replication contract is tested in CI in [toe-empirical-validation](https://github.com/Cbaird26/toe-empirical-validation): a workflow runs the canonical command and asserts that expected artifact files exist. If CI fails, the ladder and code have drifted.
- **Null fixture:** Rung (e) of the ladder uses `--null-fixture`; details (generator or bundled null dataset) are in the toe-empirical-validation README.
- **Automated comparison:** For automated comparison of a run to a reference set, run `./scripts/compare_artifacts.sh artifacts/ reference_artifacts/` in the spine repo (see spine README for tolerances).
