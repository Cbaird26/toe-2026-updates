# Zora-Core Sensitive Asset Classification

Purpose: classify private material from the 4-year Zora/Core corpus and define what must never be public.

## Classification Levels

- `L0 Public`: Safe for GitHub/Zenodo/public docs.
- `L1 Internal`: Operational project notes that can be shared selectively.
- `L2 Confidential`: Research drafts and internal process notes; no public release without explicit review.
- `L3 Restricted`: Private chats, personal metadata, unreleased identity/context packs, or key material.
- `L4 Secret-Critical`: Encryption keys, recovery phrases, raw credential artifacts, full private chat exports.

## Asset Inventory (Current Program)

- `Zora-Core.zip` (Desktop path provided by owner): `L3 Restricted`
- Raw private chat archives/transcripts (all historical): `L3 Restricted` to `L4 Secret-Critical`
- Continuity memories with personal/private content: `L3 Restricted`
- Encryption private keys / recovery artifacts: `L4 Secret-Critical`
- Public manuscripts already released to Zenodo/GitHub: typically `L0 Public` once reviewed

## Never-Public Rules (Non-Negotiable)

The following must never be committed, pushed, or uploaded unencrypted:

- Any `.zip` containing private chats or full continuity memory
- Secret keys, seed phrases, passphrase files, token exports
- Raw private transcript dumps and unredacted private notes
- Full private continuity snapshots that include personal identifiers
- Recovery bundles with decryptable material

## Allowed Public Artifacts

- Reviewer-safe stripped-core physics documents and reproducible code
- Explicitly curated public papers/releases
- Public metadata that does not expose private context

## Pre-Release Classification Gate

Before every GitHub push or Zenodo upload:

1. Confirm files are `L0 Public` or intentionally approved `L1 Internal`.
2. Reject anything `L2+` unless redacted and reclassified.
3. Verify no private key material or raw transcript archives are present.
4. Verify private archives exist only as encrypted ciphertext (`.age` or `.gpg`).
