# Reproduction spec for spine repos

This doc specifies what the TOE/MQGT-SCF replication pipeline expects from the spine repo(s) (e.g. **toe-empirical-validation** or **mqgt-analysis**) so that [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md) and [REPLICATION_LADDER.md](REPLICATION_LADDER.md) can point to a single one-command path.

---

## Required entrypoint

- **One command or script** that runs the analysis for at least **one channel** (QRNG preferred, or fifth-force + cosmology), produces figures and/or constraint outputs, and exits with success/failure.
- **Documentation:** A README section that states: (1) clone repo, (2) install dependencies (if any), (3) run the entrypoint (e.g. `./run_all.sh` or `python run_channel.py --channel qrng`), (4) where outputs are written.
- **Pinnable artifact:** Replicators should be able to pin a commit (e.g. `git checkout <SHA>`) and reproduce; the repo may optionally output a checksum of the run for comparison.

---

## Suggested implementation (toe-empirical-validation)

- Add a top-level script `run_all.sh` (or `run_qrng.sh` for QRNG-only) that:
  - Installs or checks for required environment (e.g. Python, key packages).
  - Runs the analysis scripts for the chosen channel.
  - Writes figures/constraints to a known directory (e.g. `output/` or `figures/`).
  - Exits 0 on success.
- In README.md, add a "One-command reproduction" section with the exact clone-and-run steps and a note to pin the commit hash before running.

Once this exists, [FALSIFICATION_PACKET.md](FALSIFICATION_PACKET.md) §5 and [REPLICATION_LADDER.md](REPLICATION_LADDER.md) already reference it; no change needed in this repo unless the repo URL or command name changes.
