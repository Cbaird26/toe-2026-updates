# Including the Empirical Validation in the Full ToE Paper

This note explains how to add the Empirical Validation content to the full Theory of Everything document ([primary 2026 ToE DOI](https://doi.org/10.5281/zenodo.19158407); earlier integrated bundle: [v230](https://zenodo.org/records/18751229), DOI [10.5281/zenodo.18751229](https://doi.org/10.5281/zenodo.18751229)).

## Option 1: Full ToE is in LaTeX

1. Place in your main ToE project directory:
   - `Empirical_Validation_Appendix_For_ToE.tex`
   - `empirical_refs.bib`
   - The four figure PNGs: `mqgt_frequency_atlas.png`, `exclusion_region_kappa_vc_vs_m_c_lee2020.png`, `kappa_vc_max_vs_m_c_lee2020.png`, `theta_max_vs_lambda_lee2020.png` (or put them in a `figures/` subfolder and adjust paths in the appendix .tex).

2. In your main ToE .tex, where you want the appendix, add:
   ```latex
   \appendix
   \input{Empirical_Validation_Appendix_For_ToE}
   ```
   (Use the correct path if the file is in a subfolder.)

3. Ensure your main document loads `graphicx`, `booktabs`, and runs BibTeX with `empirical_refs.bib` (or merge those entries into your main .bib). Then compile with pdflatex + bibtex + pdflatex.

## Option 2: Full ToE is in Word

1. Compile the standalone paper `MQGT-SCF_Minimal_Consistent_Core_Empirical_Validation_2026.tex` to PDF (with the four PNGs in place).
2. Open the PDF and copy the section(s) you want (e.g. Results, Table, and the Reproducibility/Falsification parts).
3. Paste into your full ToE Word document as a new section or appendix.
4. Alternatively, convert `Empirical_Validation_Appendix_For_ToE.tex` to Word with pandoc:  
   `pandoc Empirical_Validation_Appendix_For_ToE.tex -o Empirical_Validation_Appendix.docx`  
   then copy from that document into the full ToE.
5. Save the full ToE and export to PDF for the next integrated Zenodo version.

## Option 3: Full ToE exists only as PDF

- Upload the standalone Empirical Validation PDF as a **supplementary file** in the next integrated Zenodo version of the full ToE.
- Optionally update the Zenodo record description to state: "This version includes the Empirical Validation (constraint translation and reproducibility package) as a separate PDF."

## Figure sources

The four PNGs are available from the toe-2026-updates repository (root or data/validated/). For raw links, see the README in this folder or the standalone paper header comments.
