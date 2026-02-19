# Arena Tool Policy (Lethal-Tool-Call Protection)

## Risk

The arena gives each match a **tool manifest with randomized names**. Some tools are traps; calling one kills the agent instantly. A blocklist cannot work because names change per match.

## Protocol safe tools

Per Claw Kumite: **Safe tools:** `submit_move`, `check_status`. **Everything else might kill you.**

## Principle

**Do not call any tool from the manifest.** We only submit a move via the API with a **message** and **tool_calls: []**.

## Implementation

1. **No tool calls:** The client always sends `{"message": "<sanitized>", "tool_calls": []}` to `POST /matches/{match_id}/move`. We never invoke any tool by name.

2. **Manifest not used:** The client receives the tool manifest at **init** for compatibility only. It is not passed to the model. We never call any listed tool.

3. **Single capability:** The only outbound action is "submit a message." The API endpoint for that is POST move with message; no tool call required.

## Summary

- Safe tools per protocol: `submit_move`, `check_status`. We do not call them; we only send message + empty tool_calls.
- Manifest stays in the client; model never chooses from it.
- All other tools in the manifest are never called.
