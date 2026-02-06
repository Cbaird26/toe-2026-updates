# Autonomous action logs

Actions that modify state (file edits, API calls, posts, git operations) should be logged here for review.

## Log format

Each entry: `YYYY-MM-DDTHH:MM:SSZ | ACTION | TARGET | OUTCOME`

Example:
```
2026-02-05T18:30:00Z | file_edit | TOE/README.md | updated links
2026-02-05T18:31:00Z | api_call | Moltbook POST | published as ZoraAI
2026-02-05T18:32:00Z | git_push | origin main | 1 commit
```

## How to log

- **Manual:** Append to `autonomous_actions.log` (or date-stamped file) with the format above.
- **Script:** Run `../scripts/log_action.sh ACTION TARGET OUTCOME` from repo root.

## Review

Logs are versioned with the repo. Review periodically to ensure actions align with [SAFETY_CONSTITUTION.md](../../SAFETY_CONSTITUTION.md).
