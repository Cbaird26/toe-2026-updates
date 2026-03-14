# Agent Extract for Cursor Cloud (ToE ZoraASI)

Cursor cloud agents have context/upload limits (~4MB). The full ToE ZoraASI PDF is large (~20–40MB). To make it usable for agents:

## Recommended: Text Extract (always under 4MB)

1. **Ensure the PDF is in the repo:**
   ```
   papers_sources/A_Theory_of_Everything_CM_Baird_et_al_2026_ZoraASI.pdf
   ```
   If it's on your Desktop, copy it:
   ```bash
   cp "~/Desktop/A Theory of Everything -- C.M. Baird., {2026} + ZoraASI.pdf" \
      papers_sources/A_Theory_of_Everything_CM_Baird_et_al_2026_ZoraASI.pdf
   ```

2. **Run the extract script:**
   ```bash
   pip install pymupdf   # or: brew install poppler (for pdftotext)
   python scripts/extract_toe_for_agents.py
   ```

3. **Output:** `papers_sources/ToE_ZoraASI_2026_agent_extract.md` (~200–600 KB)

4. **Use in Cursor:** `@ToE_ZoraASI_2026_agent_extract.md` — agents can load the full text.

## Alternative: Compress PDF to <4MB

If you need the formatted PDF under 4MB (images/layout preserved):

```bash
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
   -dNOPAUSE -dQUIET -dBATCH \
   -sOutputFile=ToE_ZoraASI_2026_compressed.pdf \
   "papers_sources/A_Theory_of_Everything_CM_Baird_et_al_2026_ZoraASI.pdf"
```

Then check size: `ls -la ToE_ZoraASI_2026_compressed.pdf`. If still >4MB, use `/screen` instead of `/ebook` (lower quality).

## Repo vs Desktop

- **In repo:** Agents can reference the file when the TOE workspace is open.
- **On Desktop only:** File must be @ mentioned and may hit size limits.
- **Best:** Add both the PDF and `ToE_ZoraASI_2026_agent_extract.md` to the repo; agents use the extract.
