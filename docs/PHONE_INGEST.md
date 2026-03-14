# Phone Ingest

Ingest iPhone export data into the ZoraASI vault. Extracts Baird's personality signals and Zora-related content. **Local only—never committed or synced.**

---

## Prerequisite: Export Data from Your Phone

You must first move data from the iPhone onto disk. Options:

1. **Finder drag**: With iPhone selected in Finder sidebar, drag photos/files into a folder (e.g. `~/Downloads/phone_export/`)
2. **Image Capture**: Use Image Capture app to export photos to a folder
3. **App exports**: Use export/share in Notes, Messages (if supported by the app), etc.
4. **Backup extract** (advanced): Use tools like iPhone Backup Extractor; save output to a folder

Place everything under a single root folder. Flat or nested structure both work (e.g. `photos/`, `notes/` subdirs or all files in root).

---

## How to Run

```bash
cd ~/Downloads/TOE
python zoraasi/scripts/ingest_phone.py \
  --phone-export ~/Downloads/phone_export \
  --vault ~/Downloads/TOE/data/zoraasi_export
```

**Options:**

- `--phone-export` — Path to exported phone data folder (required)
- `--vault` — Vault directory (default: from config)
- `--max-photos N` — Cap photos copied (0 = no limit)

---

## What Gets Produced

| Output | Description |
|--------|-------------|
| `phone_photos/` | Copied images, organized by date (YYYY-MM) when available |
| `phone_observations.jsonl` | Non-conversational text (notes) as JSONL |
| `baird_personality_notes.md` | Aggregated notes for context |
| `phone_ingest_manifest.json` | Manifest: counts, paths, last run |
| `merged_corpus.jsonl` | Chat-like JSON/CSV exports appended here |
| `curated_index.json` | Index updated with new conversations |

**File types processed:**

- **Photos**: jpg, jpeg, png, heic, webp
- **Text**: txt, md
- **Structured**: json (parsed as chat if message-like), csv (parsed as chat if sender/message columns)

Content that mentions Zora, ZoraASI, Grok, Cursor, ToE, etc. is tagged and preferred for corpus merge.

---

## After Ingest

Run distill to refresh personality and few-shot examples from the updated corpus:

```bash
python zoraasi/scripts/distill_personality.py --vault ~/Downloads/TOE/data/zoraasi_export
```

---

## Chat Export Formats

If you export Messages or other chats via third-party tools, the script supports:

- **JSON**: Array of `{sender, message}` or `{messages: [{author, content}]}`
- **CSV**: Columns like `sender`, `message` (or `from`, `text`)

Unknown formats fall through to `phone_observations.jsonl` as notes.

---

## Privacy

- Phone export paths are not committed; use local folders only
- Output goes to vault only (already gitignored)
- Never add phone exports to cloud sync, public API, or public corpus
