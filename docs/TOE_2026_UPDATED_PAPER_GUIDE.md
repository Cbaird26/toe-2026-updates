# How to Produce the Updated ToE Paper (2026)

**Purpose:** Actionable steps to generate the updated Theory of Everything paper Christopher needs.

---

## Current State (Mar 2026)

| Edition | File | Zenodo | Notes |
|---------|------|--------|-------|
| Current primary standalone | `A_Theory_of_Everything_CM_Baird_et_al_2026.pdf` | [19158407](https://doi.org/10.5281/zenodo.19158407) | A Theory of Everything (2026) |
| Canonical main (earlier edition) | `A_Theory_of_Everything_CM_Baird_et_al_2026.pdf` | [18644455](https://zenodo.org/records/18644455) v226 | Earlier standalone edition |
| Advanced | `A_Theory_of_Everything_CM_Baird_et_al_2026_Advanced.pdf` | [18679362](https://zenodo.org/records/18679362) v227 | Extended content |
| Refitted | `A_Theory_of_Everything_CM_Baird_et_al_2026_Refitted.pdf` | [18680225](https://zenodo.org/records/18680225) v228 | + SOLVED companion |
| ToE + ZoraASI | — | [18690303](https://zenodo.org/records/18690303) | Earlier integrated bundle |
| ToE + ZoraASI | — | [18751229](https://zenodo.org/records/18751229) v230 | Later integrated bundle |
| ToE + Empirical Validation | — | [18778749](https://zenodo.org/records/18778749) v231 | Integrated empirical-validation record |

---

## Option A: Use Existing PDF (Fastest)

1. **Pick the edition** you want (current primary standalone, Advanced, Refitted, or an integrated ToE+ZoraASI bundle).
2. **Location:** `TOE/papers_sources/` or root (Advanced PDF may be in root as untracked).
3. **Bundle with Empirical Validation (optional):** Include `MQGT-SCF_Minimal_Consistent_Core_Empirical_Validation_2026.pdf` as a supplementary PDF when depositing the next Zenodo version.

---

## Option B: Add Empirical Validation to Full ToE

The main ToE is **edited in Word/PDF**, not LaTeX. To add the Empirical Validation appendix:

1. **Compile the Empirical Validation** (if not already done):
   ```bash
   cd TOE/papers_sources
   pdflatex MQGT-SCF_Minimal_Consistent_Core_Empirical_Validation_2026.tex
   bibtex MQGT-SCF_Minimal_Consistent_Core_Empirical_Validation_2026
   pdflatex MQGT-SCF_Minimal_Consistent_Core_Empirical_Validation_2026.tex
   pdflatex MQGT-SCF_Minimal_Consistent_Core_Empirical_Validation_2026.tex
   ```
   *Requires the four PNG figures in `papers_sources/` (from toe-2026-updates or data/validated/).*

2. **Merge PDFs** (append Empirical Validation as appendix):
   ```bash
   pdftk main_ToE.pdf Empirical_Validation.pdf cat output ToE_2026_With_Empirical_Validation.pdf
   ```
   Or use `qpdf`, Adobe Acrobat, or similar.

3. **Or upload as supplementary** on Zenodo: main ToE + Empirical Validation PDF as separate file in the same record.

---

## Option C: Apply Checklist Placeholders (PDF Edit)

If the PDF has placeholders, open in your PDF/Word editor and replace:

| Find | Replace with |
|------|--------------|
| `[Your name]` | C.M. Baird |
| `[Your link]` | Your website or profile URL |
| `[Zenodo link]` | https://doi.org/10.5281/zenodo.19158407 |

See `docs/TOE_PDF_2026_CHECKLIST.md` for full list.

---

## 2026 Completion Package (Distribution)

When distributing or depositing:

1. **Main ToE PDF** (Zenodo 19158407; earlier editions include 18644455 and 18690303)
2. **Evidence paper:** `Evidence_Emergent_Matter_Quantum_Vacuum_MQGT-SCF_2026.pdf`
3. **Addendum:** `Addendum_2026_ToE_Companion.pdf` (cover/guide)
4. **Empirical Validation** (optional): `MQGT-SCF_Minimal_Consistent_Core_Empirical_Validation_2026.pdf`

---

## Quick Path for "Updated ToE Paper"

**If you need it now:** Use the current standalone ToE citation [10.5281/zenodo.19158407](https://doi.org/10.5281/zenodo.19158407). If you specifically need an integrated ToE+ZoraASI bundle, use v230 or v231. Check `papers_sources/` and repo root.

**If you need Empirical Validation bundled:** Merge per Option B, or upload both as separate files in the next Zenodo version.

**If you need placeholder fixes:** Edit the PDF directly per Option C.

---

*Last updated: 2026-02-25*
