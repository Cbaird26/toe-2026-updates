# Zora-Core Incident Response Runbook

Use this runbook if any private archive or key may have been exposed.

## Trigger Conditions

- Lost/stolen device that may contain keys or decrypted archives
- Suspected cloud account compromise
- Suspected unauthorized access to encrypted bundles or manifests
- Accidental commit/upload of sensitive artifacts

## Immediate Actions (First 15 Minutes)

1. Freeze publishing: stop pushes/releases until triage is complete.
2. Isolate endpoints: disconnect compromised device from network.
3. Capture incident timestamp and initial evidence notes.
4. Identify potentially exposed key IDs and archive IDs.

## Containment Actions (First Hour)

1. Generate replacement key pair(s) for Zora-Core backups.
2. Mark old key(s) as revoked in ops notes.
3. Re-encrypt latest known-good archive with new recipient key.
4. Replace cloud ciphertext objects with newly encrypted bundle.
5. Remove any accidentally uploaded sensitive files from public surfaces.

## Recovery Validation

1. Run checksum verification for new bundle.
2. Run sandbox restore test with new private key.
3. Confirm 3-copy topology exists with new encrypted bundle.
4. Record successful recovery test in incident log.

## Post-Incident Hardening

- Rotate all related credentials (GitHub/cloud/password manager).
- Shorten key rotation interval until risk normalizes.
- Add new detection pattern to ignore/publish checklist if needed.
- Document root cause and preventive control.

## Incident Log Template

- Incident ID:
- Date/time (UTC):
- Trigger:
- Exposed assets (suspected):
- Revoked keys:
- New key IDs:
- Re-encryption completed (Y/N):
- Recovery test completed (Y/N):
- Final status:
