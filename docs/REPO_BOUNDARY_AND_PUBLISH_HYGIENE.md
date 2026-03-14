# Repository Boundary and Publish Hygiene

This policy separates public science artifacts from private continuity/private chat archives.

## Boundary Rules

- `mqgt-scf-stripped-core`:
  - Public, reviewer-safe, physics-only artifacts.
  - No private chats, key material, or full continuity snapshots.
- `TOE`:
  - Public-facing ToE content plus controlled documentation.
  - Private live continuity content stays local-only (`private_continuity/`) and encrypted archives only.
- Off-repo private vault:
  - Encrypted backups of sensitive assets (`L3/L4`) only.

## Publish Hygiene Checklist (GitHub/Zenodo)

Before each publication/push:

1. Run file classification gate (`L0/L1` only for public release).
2. Confirm no plaintext private archives (`*.zip`) are staged.
3. Confirm no keys, tokens, `.env`, or passphrase artifacts are staged.
4. Confirm continuity live pack is excluded from tracked files.
5. Confirm scope statement exists (public subset vs private archive).

## Red Flags (Block Release)

- Any raw private chat dump appears in staged files.
- Any key file (`*.key`, `*.pem`, `*.asc`, `age*key*`) appears in staged files.
- Any private continuity file is tracked outside template paths.
- Any encrypted bundle is missing matching checksum manifest.
