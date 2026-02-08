# Zenodo deposit instructions

Step-by-step for depositing ToE-related papers on Zenodo so they get DOIs and can be cited.

---

## Existing ToE record

- **A Theory of Everything** is on Zenodo: [zenodo.org/records/18523004](https://zenodo.org/records/18523004) (DOI [10.5281/zenodo.18523004](https://doi.org/10.5281/zenodo.18523004)). Baird, C. M. (2026). A Theory of Everything. https://doi.org/10.5281/zenodo.18523004
- No change unless you are releasing a new version (upload new file, publish new version from the same concept).

---

## Asimov / ABIL papers

To get a DOI for the Asimov-style or ABIL papers:

1. **Build the PDF**
   - From [papers_sources/Asimov_Safety_Field_Theoretic_Invariants_MQGT_SCF_2026.tex](../papers_sources/Asimov_Safety_Field_Theoretic_Invariants_MQGT_SCF_2026.tex) and/or [papers_sources/Asimov_Baird_Invariance_Laws_ABIL_2026.tex](../papers_sources/Asimov_Baird_Invariance_Laws_ABIL_2026.tex).
   - Use Overleaf (upload .tex, compile) or local `pdflatex` (run until references stable).

2. **Go to Zenodo**
   - Open [zenodo.org](https://zenodo.org) and sign in (GitHub or Zenodo account).

3. **Create a new record**
   - Click **Upload** → **New upload**.

4. **Fill metadata**
   - **Title:** e.g. "Embedding Asimov-Style Safety as Field-Theoretic Invariants in the MQGT-SCF Theory of Everything" (short paper) or "Asimov–Baird Invariance Laws: Embedding Hierarchical Safety as Field-Theoretic and Control-Theoretic Bedrock in MQGT–SCF" (ABIL).
   - **Authors:** C. M. Baird et al. (add full names/affiliations if desired).
   - **Description:** One paragraph linking to the ToE (Zenodo 18523004, DOI 10.5281/zenodo.18523004) and summarizing machine laws, safe set K, barrier, forward invariance, and deployment as safety envelope.
   - **License:** e.g. CC-BY-4.0.
   - **Keywords:** e.g. AI safety, Asimov laws, MQGT-SCF, control barrier functions, forward invariance, viability theory.

5. **Upload the PDF**
   - Add the compiled PDF to the record.

6. **Publish**
   - Click **Publish** to obtain the DOI. The DOI will be assigned and the record will be public.

7. **Update the repo**
   - Add the new DOI to [papers_sources/README.md](../papers_sources/README.md) (in the bullet for the corresponding .tex file).
   - Optionally add the link to the main [README.md](../README.md) Links section.
   - Commit and push.

---

## One record per paper vs one concept with versions

- **Option A (recommended):** One Zenodo record per paper (short Asimov paper, ABIL paper). Clear citation: one DOI per title.
- **Option B:** One Zenodo "concept" with two versions (upload short paper first, then add ABIL as a new version). Same concept DOI; version DOIs differ.

Use Option A unless you prefer a single concept for the two Asimov-related papers.
