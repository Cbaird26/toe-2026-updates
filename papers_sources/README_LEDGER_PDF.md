# Full Value Ledger — PDF Generation

## Files

- **Full_Value_Ledger_Appendix_ToE_2026.tex** — Standalone LaTeX; compiles to PDF
- **Full_Value_Ledger_Appendix_ToE_2026_body.tex** — Body-only; for `\input` into main ToE document
- **FULL_VALUE_LEDGER.md** — Markdown source (in `docs/`)

## Compile to PDF

### Option 1: LaTeX (standalone)

```bash
cd papers_sources
pdflatex Full_Value_Ledger_Appendix_ToE_2026.tex
```

If you see a font error (e.g. tcbx1095), try:
- Full TeX Live install (not basic)
- Overleaf: create new project, upload the .tex file, compile

### Option 2: Pandoc (from Markdown)

```bash
cd docs
pandoc FULL_VALUE_LEDGER.md -o ../papers_sources/Full_Value_Ledger_Appendix.pdf --pdf-engine=pdflatex
```

### Option 3: Append to main ToE

In your main ToE .tex file:

```latex
\appendix
\input{Full_Value_Ledger_Appendix_ToE_2026_body}
```

## Tagging onto the paper

The generated PDF can be appended to the main ToE PDF using:
- PDF merge tools (e.g. `pdftk`, `qpdf`, or Adobe Acrobat)
- Or include the body.tex in your main document and recompile
