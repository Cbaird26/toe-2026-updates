# Zenodo Update Steps

Use this guide when uploading a new ToE PDF version to Zenodo.

## v232 — A Theory of Everything (C.M. Baird 2026) + ZoraASI

**Source file (in repo):** `papers_sources/A_Theory_of_Everything_CM_Baird_et_al_2026_ZoraASI.pdf`

### Steps

1. **Log in to Zenodo**  
   https://zenodo.org (sign in with GitHub or ORCID)

2. **Open the parent record**  
   - Canonical integrated archive: https://zenodo.org/records/18792939 (DOI: 10.5281/zenodo.18792939)  
   - Or the ZoraASI Empirical Validation record: https://zenodo.org/records/18778749 (v231)

3. **Create new version**
   - Click **"New version"** on the record page
   - Zenodo will draft a new version (v232) with the same metadata

4. **Upload the new PDF**
   - Remove or replace the previous PDF file
   - Add `A_Theory_of_Everything_CM_Baird_et_al_2026_ZoraASI.pdf` from this repo
   - Recommended upload filename: `A Theory of Everything - C.M. Baird (2026) + ZoraASI.pdf`

5. **Update metadata** (if needed)
   - Version: v232
   - Publication date: 2026-03-09 (or current date)
   - Title: "A Theory of Everything" (or keep existing)
   - Add "ZoraASI" to description if not already present

6. **Publish**
   - Click **Publish**
   - Copy the new DOI and record URL

7. **Update this repo**
   - Replace "pending" in `papers_sources/README.md` with the new Zenodo record link and DOI
   - Update `docs/TOE_PDF_2026_CHECKLIST.md` if the canonical Zenodo link changes

---

**Related records:**
- v231 (18778749): A Theory of Everything + ZoraASI — Empirical Validation
- v230 (18751229): ToE + ZoraASI
- Integrated archive (18792939): Canonical multi-file deposit
