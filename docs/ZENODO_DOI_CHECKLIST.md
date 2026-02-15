# Zenodo DOI checklist

When Zenodo mints DOIs for releases (after GitHub↔Zenodo is enabled and releases are published):

## 1. Confirm Zenodo↔GitHub

- Zenodo → Account → GitHub → enable for both repos
- Ensure "Create DOI for GitHub releases" is on

## 2. After DOIs appear (per repo)

- **README Cite section:** Replace the "DOI: (to be minted…)" line with the version DOI (e.g. `10.5281/zenodo.12345678`). Optionally add the concept DOI.
- **CITATION.cff:** Uncomment the `identifiers` block at the bottom and set `value` to the version DOI; add concept DOI if desired.

## 3. Which DOI to cite

- **Replication (strict):** Cite the **v0.1** version DOI (contract baseline).
- **General citation:** v0.1.1 (metadata) is fine; v0.1 is the reproducibility anchor.

## 4. .zenodo.json

Both repos have a root `.zenodo.json` with creator and affiliation. Add ORCID to `creators` in that file if desired; Zenodo will use it on the next release.
