# ZoraX Ingest

Ingest xAI/Grok chat exports (ZoraX) into the ZoraASI vault. **Local only—never committed or synced.**

---

## What Is ZoraX?

ZoraX is an xAI data export containing Grok conversations. Typically obtained via xAI's privacy/data export. Files are named like `ZoraX-03.10.2026` (zip). Contents include `prod-grok-backend.json` (conversations) and asset files. **Most private of private**—keep strictly local.

---

## How to Run

```bash
cd ~/Downloads/TOE
python zoraasi/scripts/ingest_zorax.py \
  --vault ~/Downloads/TOE/data/zoraasi_export \
  --zorax ~/Downloads/ZoraX-03.10.2026
```

**Options:**

- `--vault` — Vault directory (default: from config)
- `--zorax` — Path to ZoraX zip (required)
- `--filter-title zora` — Keep only conversations whose title contains "zora" (default)
- `--no-filter` — Keep all conversations

---

## After Ingest

Run distill to refresh personality and few-shot examples:

```bash
python zoraasi/scripts/distill_personality.py --vault ~/Downloads/TOE/data/zoraasi_export
```

---

## Privacy

- ZoraX paths are in `.gitignore` (`ZoraX*.zip`, `ZoraX-*`)
- ZoraX is **not** added to instantiate discovery—invoke manually
- Output goes to vault only (already gitignored)
- Never add ZoraX to cloud sync, public API, or public corpus

---

## Schema

The xAI `prod-grok-backend.json` structure may evolve. Current parser expects:

- Top level: `{"conversations": [...]}`
- Each item: `{conversation: {id, title, ...}, responses: [{response: {message, sender, ...}}]}`

If the format changes, update `zoraasi/scripts/ingest_zorax.py` accordingly.
