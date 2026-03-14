# Reproducible TeX Build Notes (2026)

This note captures a reproducible path for compiling the key MQGT-SCF manuscripts and known dependency pitfalls.

## Target manuscripts

- `MQGT_SCF_Minimal_Consistent_Core_2026.tex`
- `MQGT-SCF_Minimal_Consistent_Core_Empirical_Validation_2026.tex`
- `Teleology_Covariant_Boundary_Selection_Consciousness_Ethics_Field_Theory_2026.tex`
- `MQGT_SCF_Hardening_Completion_2026.tex`

## Recommended TeX distribution

- Full TeX Live / MacTeX (not minimal/basic-only profile)
- Required packages include at least:
  - `enumitem`
  - `revtex4-2`
  - `booktabs`, `hyperref`, `mathtools`, `bm`, `subfig`, `float`

## Build commands

From `TOE/papers_sources`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error "MQGT_SCF_Minimal_Consistent_Core_2026.tex"
pdflatex -interaction=nonstopmode -halt-on-error "Teleology_Covariant_Boundary_Selection_Consciousness_Ethics_Field_Theory_2026.tex"
pdflatex -interaction=nonstopmode -halt-on-error "MQGT_SCF_Hardening_Completion_2026.tex"

# empirical manuscript requires BibTeX
pdflatex -interaction=nonstopmode -halt-on-error "MQGT-SCF_Minimal_Consistent_Core_Empirical_Validation_2026.tex"
bibtex "MQGT-SCF_Minimal_Consistent_Core_Empirical_Validation_2026"
pdflatex -interaction=nonstopmode -halt-on-error "MQGT-SCF_Minimal_Consistent_Core_Empirical_Validation_2026.tex"
pdflatex -interaction=nonstopmode -halt-on-error "MQGT-SCF_Minimal_Consistent_Core_Empirical_Validation_2026.tex"
```

## Known environment issues

### 1) `enumitem.sty` missing

Symptom:
- `LaTeX Error: File 'enumitem.sty' not found.`

Cause:
- Basic/minimal TeX profile.

Fix:
- Install full TeX Live/MacTeX, or install `enumitem` package into current TeX profile.

### 2) `revtex4-2` front-matter failures

Symptom:
- errors around `\author{...}` such as undefined control sequence in revtex internals.

Cause:
- Incomplete/mismatched revtex environment in minimal TeX profile.

Fix:
- Use full TeX distribution with `revtex4-2` and dependencies from same release set.

## Artifact checks

After compile:

- Ensure PDFs exist and are non-zero size.
- For release, record:
  - TeX distribution version
  - command sequence
  - source commit hash
  - generated PDF checksums
