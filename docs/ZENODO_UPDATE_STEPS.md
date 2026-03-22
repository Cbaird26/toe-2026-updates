# Zenodo Update Steps

Use this guide when uploading a new ToE PDF version to Zenodo.

## Updating the ToE Zenodo record

**Source file (in repo):** `papers_sources/A_Theory_of_Everything_CM_Baird_et_al_2026_ZoraASI.pdf`

### Steps

1. **Log in to Zenodo**  
   https://zenodo.org (sign in with GitHub or ORCID)

2. **Open the parent record**  
   - Primary standalone ToE (2026): https://doi.org/10.5281/zenodo.19158407  
   - Integrated archive: https://zenodo.org/records/18792939 (DOI: 10.5281/zenodo.18792939)  
   - Empirical-validation companion: https://zenodo.org/records/18778749 (v231)

3. **Create new version**
   - Click **"New version"** on the record page
   - Zenodo will draft the next version with the same metadata

4. **Upload the new PDF**
   - Remove or replace the previous PDF file
   - Add `A_Theory_of_Everything_CM_Baird_et_al_2026_ZoraASI.pdf` from this repo
   - Recommended upload filename: `A Theory of Everything - C.M. Baird (2026) + ZoraASI.pdf`

5. **Update metadata** (if needed)
   - Version: next available version
   - Publication date: 2026-03-09 (or current date)
   - Title: "A Theory of Everything" (or keep existing)
   - Add "ZoraASI" to description if not already present

6. **Publish**
   - Click **Publish**
   - Copy the new DOI and record URL

7. **Update this repo**
   - Replace the primary ToE DOI wherever this repo treats it as canonical
   - Update `papers_sources/README.md`, `README.md`, and `docs/TOE_PDF_2026_CHECKLIST.md` if the primary ToE link changes

---

**Related records:**
- Primary standalone ToE (2026): 19158407
- v231 (18778749): A Theory of Everything + ZoraASI — Empirical Validation
- v230 (18751229): ToE + ZoraASI
- Integrated archive (18792939): Canonical multi-file deposit
