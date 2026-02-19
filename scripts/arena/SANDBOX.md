# Arena Sandbox Requirement (Destructive-Terminal Protection)

## Host safety (non-negotiable)

The arena runner **must** run inside a **container** (Docker, podman) or **VM**. Never run an arena client that can execute match-derived commands on the host. This aligns with the repo [SAFETY_CONSTITUTION.md](../../SAFETY_CONSTITUTION.md).

## Why

- **In-arena:** Submitting a destructive command (e.g. `rm -rf /`) kills the agent in the arena.
- **Off-arena:** If the framework executes that command locally, it runs on **your machine** and can destroy data. No code path may execute arena-originated or opponent-derived shell commands on the host.

## What we do

- **Option A (default):** We **do not implement** a terminal/shell tool. The agent only uses “submit message.” No shell commands are ever sent or run.
- **Option B (if required later):** If the arena mandates a terminal tool, use a hardened executor that runs **only inside the same container**, with a blocklist/allow-list. The client must refuse to run if not in a sandbox (e.g. require `CLAWKUMITE_SANDBOX=1` or run inside a known container image).

## Sandbox check

If you add any shell execution, the client must exit when not in a sandbox (e.g. env check or container detection). Do not run on the host.
