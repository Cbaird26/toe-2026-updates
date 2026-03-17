# Codex brief: Grant Cursor agent terminal execution and output

**Purpose:** Get the Cursor AI agent to successfully run a command on the user’s machine and see the output, so the agent can run ANU QRNG experiments and then read the resulting data in the same session.

**Context:** The user (Christopher Michael Baird) uses Cursor with the TOE workspace. The Cursor agent needs to run:

```bash
cd ~/Downloads/TOE
python3 scripts/anu_qrng_collect.py --n 100000 --out artifacts/ --label baseline
```

This script:

1. Reads an API key from `artifacts/.anu_api_key` (user has already stored it there).
2. Makes HTTPS requests to `https://api.quantumnumbers.anu.edu.au` (ANU Quantum Random Numbers API).
3. Writes output files into `artifacts/` (e.g. `anu_qrng_baseline_*_bits.csv`, `*_summary.json`).

**Current behavior:** When the Cursor agent runs this command (and requests `network` and `all` permissions), the run reports **exit code 0**, **0 ms** duration, and **no stdout/stderr**. So either:

- The command is not actually executed on the host, or
- The execution environment has no network or filesystem access, or
- The terminal output is not returned to the agent.

The user needs the **agent** to run it (not run it themselves in a separate terminal) so the agent can then read the generated artifacts and extrapolate/analyze the data in the same conversation.

**What we need from Codex:**

1. **How can we configure Cursor** (or the workspace, or a permission/setting) so that when the Cursor agent runs a terminal command with “full” / “network” / “all” permissions:
   - The command **actually runs** on the host (user’s Mac),
   - With **network access** (so the script can call the ANU API),
   - With **read/write access** to the workspace (e.g. `~/Downloads/TOE`) and optionally to `~/Desktop/TOE_Corpus_2026`,
   - And the **command output (stdout/stderr) and real exit code and duration** are **returned to the agent**?

2. If Cursor has a documented way to “run agent commands on host with full permissions” or “disable sandbox for agent terminal,” what is it and where is it configured?

3. If the issue is that the workspace does not include the path where the script runs (e.g. only `~/Downloads/TOE` is in the workspace and the agent’s shell can’t see it), what is the recommended setup (e.g. add folder to workspace, run from workspace root only) so the agent’s terminal has a working directory inside the workspace and can run Python and write to `artifacts/`?

**Exact command the agent will run (once access works):**

```bash
cd ~/Downloads/TOE && python3 scripts/anu_qrng_collect.py --n 100000 --out artifacts/ --label baseline
```

**Deliverable:** Clear steps or configuration (for Cursor and/or the user) so that when the user says “run the ANU QRNG baseline,” the Cursor agent can run this command, see its output, and then read the resulting files in `TOE/artifacts/` to extrapolate the data. If Codex can provide a script or setting that enables this, please include it.

---

*TOE = Theory of Everything workspace. ANU QRNG = Australian National University Quantum Random Number Generator API. Method doc: TOE/docs/QRNG_METHOD_MARCH_2026_DO_NOT_CHANGE.md*
