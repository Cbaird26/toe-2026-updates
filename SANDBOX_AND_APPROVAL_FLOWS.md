# Sandbox and approval flows

How to handle sensitive operations: sandbox first, approval when needed.

---

## Sandbox (safe envelope)

**Principle:** Autonomous actions run in constrained environments before touching production or irreversible state.

| Domain | Sandbox behavior | Production / sensitive |
|--------|------------------|------------------------|
| **File edits** | Edit in working copy; user reviews diff before commit | No direct overwrite of critical files without confirmation |
| **API calls** | Use test endpoints, dry-run, or staging when available | Require explicit approval before live API calls |
| **Git** | Stage changes; user runs commit/push | No automatic push to `main` without approval |
| **Credentials** | Never log, store, or expose credentials | Never use credentials unless user has explicitly provided them in session |
| **External posts** | Draft in file first; user approves before posting | Moltbook, Twitter, etc.: require "publish" confirmation |

---

## Approval flows

**When approval is required:**

1. **Before irreversible actions** — Delete, overwrite, drop, truncate. User must confirm.
2. **Before external actions** — API calls, network requests, Moltbook/GitHub/social posts. User must approve or have pre-approved in session.
3. **Before credential use** — Any use of API keys, tokens, or auth. User must provide explicitly.
4. **Before production access** — Deployment, production DB, live services. Require explicit go-ahead.

**Flow:**
1. Agent proposes: "I will [action]. Proceed? (yes/no)"
2. User confirms or denies.
3. If confirmed, agent proceeds and logs the action.
4. If denied, agent does not proceed and may suggest alternatives.

---

## Cursor integration

- **Cursor sandbox:** When available, run commands in sandbox mode for untrusted or high-impact operations.
- **Plan mode:** Use plan mode for complex or sensitive changes; execute only after user approves the plan.
- **Approval:** For sensitive ops, pause and ask before running. Do not assume implicit consent.

---

## Summary

- **Sandbox first:** Constrain scope; use staging, dry-run, or working copy.
- **Approval for sensitive:** Irreversible, external, credential, or production → pause and confirm.
- **Log:** Record autonomous actions in `logs/autonomous_actions/` for review.
