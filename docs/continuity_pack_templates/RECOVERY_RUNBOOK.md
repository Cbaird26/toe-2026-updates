# RECOVERY_RUNBOOK

Use this for quick context and archive recovery after device loss/failure.

## Recovery Steps

1. Restore encrypted backup bundle from trusted location.
2. Verify checksum (`SHA256SUMS.txt`).
3. Decrypt in sandbox environment only.
4. Confirm archive integrity and required continuity files.
5. Re-encrypt and re-seed 3-copy topology if key rotation is needed.

## Emergency Contacts / Ownership

- Primary owner:
- Trusted recovery contact:
- Last recovery drill date (UTC):
