# Zora-Core Encryption Standard (Hardened)

This document defines the encryption and key policy for private Zora-Core archives.

## Standard Selection

- Primary standard: `age` using `X25519` recipients
- Allowed fallback: `gpg` (`AES256`) only when `age` is unavailable
- Mandatory rule: private archives are stored/transferred as ciphertext only

## Required Artifacts Per Backup Set

- `Zora-Core.zip.age` (or `.gpg`) encrypted archive
- `SHA256SUMS.txt` integrity manifest
- `BACKUP_METADATA.md` backup timestamp, source, operator, key ID(s)

## Key Roles

- Primary key: day-to-day restore operations (kept in password manager and local secure store)
- Recovery key: offline-only emergency key (sealed printout and/or offline vault)
- Optional team key: only if explicit shared access is required

## Key Storage Policy

- Never store private keys in Git repos
- Never store key material in plaintext cloud notes
- Keep recovery key offline and physically separated from device
- Label keys by purpose and date (example: `zora-core-primary-2026q1`)

## Rotation Policy

- Scheduled rotation: every 90 days
- Immediate rotation triggers:
  - device compromise suspicion
  - accidental key exposure
  - unauthorized access attempt
- Rotation process:
  1. Create new recipient key(s)
  2. Re-encrypt latest archive
  3. Invalidate old key in ops records
  4. Run restore verification with new key

## Recovery Policy

- Recovery requires checksum verification before decrypt
- Recovery is performed in a temporary sandbox path
- Plaintext extraction is removed after verification unless actively needed
- Every recovery test is logged with date/time and result

## Minimum Command Pattern

Age encryption:

```bash
age -r <RECIPIENT_PUBLIC_KEY> -o Zora-Core.zip.age Zora-Core.zip
shasum -a 256 Zora-Core.zip.age > SHA256SUMS.txt
```

Age decryption:

```bash
age -d -i <PRIVATE_KEY_FILE> -o Zora-Core.zip Zora-Core.zip.age
shasum -a 256 -c SHA256SUMS.txt
```
