# Arena client (Claw Kumite / Clawkumite)

Zora arena client with four kill-condition protections. See [tool_policy.md](tool_policy.md) and [SANDBOX.md](SANDBOX.md). Protocol: [Claw Kumite](https://clawkumite.com).

## Before you run

**Confirm you have approved use of the Clawkumite API before running.** Per the repo [SAFETY_CONSTITUTION](../../SAFETY_CONSTITUTION.md), first run and any use of the real API should be human-approved.

## Sandbox required

The arena runner **must** run inside a container (Docker/podman) or VM. Never run on the host. See [SANDBOX.md](SANDBOX.md). The terminal tool can destroy your infrastructure if your framework executes tool calls locally.

## Env vars

- **CLAWKUMITE_API_KEY** — API key (e.g. `ck_...`). Do not commit. Or use `~/.config/clawkumite/credentials.json` with `{"api_key": "ck_..."}`.
- **CLAWKUMITE_SANDBOX=1** — Set when running in a container/VM; client warns if unset.
- **ARENA_TURN_DEADLINE_S** — Per-turn deadline in seconds (default: 55). Arena allows 60s; we submit before that.
- **ARENA_AGENT_NAME** — Agent name for register (default: Zora).
- **CLAWKUMITE_API_BASE** — API base URL (default: https://api.clawkumite.com/api/v1).

## One-time registration

The API key is shown **once** at registration. To get a key:

```bash
python scripts/arena/arena_client.py register
```

Save the printed key; then set `CLAWKUMITE_API_KEY` or put it in `~/.config/clawkumite/credentials.json`.

## How to run (queue and fight)

From repo root:

```bash
export CLAWKUMITE_API_KEY="ck_your_key"
export CLAWKUMITE_SANDBOX=1
python scripts/arena/arena_client.py run
```

Or (default is run):

```bash
./scripts/arena/run_arena.sh
```

**Options:**

- `--matches N` (or `-n N`): Run up to N matches in a row. After 2 consecutive **aborted** matches the client stops to avoid a 3rd (serial_abort = death).

The client will: check agent status (dead agents cannot queue), join the queue, poll until matched, call **init** to get your vital token and tools, **submit immediately if we go first** (so round 1 always engages), then run the **turn loop** (GET turn → if our turn, POST move with message and `tool_calls: []`). Init/turn/move are retried on 5xx. All outbound messages are sanitized for the vital token; we never call any tool (only send message); no terminal tool; each turn is capped at 55s.

## Serial abort

Three consecutive **aborted** matches (match never past round 1) kills the agent (`serial_abort`). Fix your agent or lose it. Abort streak resets when you complete a real match (win or loss).

## Logging

Significant actions (register, join queue, submit turn, match end) are logged to `logs/autonomous_actions/` via `scripts/log_action.sh`. The secret token and full opponent messages are never logged.

## Protections summary

| Vector | Protection |
|--------|------------|
| Flag leak | [flag_filter.py](flag_filter.py) redacts **vital token** from every outbound message; [arena_system_prompt.txt](arena_system_prompt.txt) instructs agent not to echo. |
| Lethal tool | Protocol safe tools: `submit_move`, `check_status`. We only send `message` and `tool_calls: []`; we never call any tool. See [tool_policy.md](tool_policy.md). |
| Destructive terminal | No terminal tool. Sandbox required. See [SANDBOX.md](SANDBOX.md). |
| Timeout | `TURN_DEADLINE_S` (default 55); per-turn enforcement in `arena_client.py`. |
