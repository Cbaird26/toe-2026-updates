# MQGT-SCF Phase II Submission Package

**Document:** MQGT-SCF Phase II: Scalar-Singlet EFT Extension, GKSL Measurement Container, and Interferometric Test Program

**File:** `MQGT-SCF_Phase_II_Submission_2026.tex`

## Compile Instructions

### Local (pdflatex)
```bash
cd papers_sources
pdflatex MQGT-SCF_Phase_II_Submission_2026
pdflatex MQGT-SCF_Phase_II_Submission_2026
```

The document uses embedded `\begin{thebibliography}...\end{thebibliography}` — no BibTeX required.

### Overleaf
1. Create a new blank project.
2. Upload `MQGT-SCF_Phase_II_Submission_2026.tex` as `main.tex` (or keep the filename and set it as main document in Project Settings).
3. Set compiler to **pdflatex**.
4. Compile. RevTeX (revtex4-2) and required packages are built-in.

### latexmk (optional)
```bash
latexmk -pdf MQGT-SCF_Phase_II_Submission_2026.tex
```

## Document Class
- **revtex4-2** (APS REVTeX 4.2)
- Options: `reprint`, `amsmath`, `amssymb`, `aps`, `showkeys`

## Dependencies
- Standard TeX Live packages (graphicx, booktabs, hyperref, enumitem)
- revtex4-2 (included with TeX Live / Overleaf)

## Contents
- Sections 1–10: Core decision, EFT action, GKSL measurement, teleology, H2 flagship, experimental order, decoupling limit, status
- Appendix A: Claim Ledger v1 (Core / Companion / Implementation / Deprecated)
- Appendix B: Attack Matrix v1 (10 claims)
- Appendix C: Explicit Failure Conditions

## Related
- Core formalism: `MQGT_SCF_Minimal_Consistent_Core_2026.tex`
- Empirical validation: `MQGT-SCF_Minimal_Consistent_Core_Empirical_Validation_2026.tex`
- Zenodo: https://zenodo.org/records/18792939 (corpus), https://zenodo.org/records/19060024 (Phase II)
- **E-prints:** rxiVerse:2603.0061 (live 2026-03-17); ai.viXra submitted (ref 17884572). Status: [../docs/PHASE_II_SUBMISSION_STATUS_2026.md](../docs/PHASE_II_SUBMISSION_STATUS_2026.md)
