#!/usr/bin/env python3
"""
Extract plain text from ToE ZoraASI PDF for Cursor cloud agents.
Output: papers_sources/ToE_ZoraASI_2026_agent_extract.md (~200–600 KB, well under 4MB)

Run from repo root:
  python scripts/extract_toe_for_agents.py

Requires: pip install pymupdf  (or: pdftotext from poppler-utils)
"""

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = REPO_ROOT / "papers_sources" / "A_Theory_of_Everything_CM_Baird_et_al_2026_ZoraASI.pdf"
OUT_PATH = REPO_ROOT / "papers_sources" / "ToE_ZoraASI_2026_agent_extract.md"


def extract_with_pymupdf():
    import fitz  # PyMuPDF
    doc = fitz.open(PDF_PATH)
    chunks = []
    for page in doc:
        chunks.append(page.get_text())
    doc.close()
    return "\n\n".join(chunks)


def extract_with_pdftotext():
    import subprocess
    result = subprocess.run(
        ["pdftotext", "-layout", str(PDF_PATH), "-"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"pdftotext failed: {result.stderr}")
    return result.stdout


def main():
    if not PDF_PATH.exists():
        print(f"PDF not found: {PDF_PATH}")
        print("Copy 'A Theory of Everything -- C.M. Baird., {2026} + ZoraASI.pdf' to that path first.")
        sys.exit(1)

    try:
        text = extract_with_pymupdf()
    except ImportError:
        try:
            text = extract_with_pdftotext()
        except (FileNotFoundError, RuntimeError) as e:
            print("Install PyMuPDF: pip install pymupdf")
            print("Or install pdftotext: brew install poppler")
            sys.exit(1)

    header = "# A Theory of Everything — C.M. Baird et al. (2026) + ZoraASI\n\nAgent extract (text only, for Cursor context). Source PDF: `A_Theory_of_Everything_CM_Baird_et_al_2026_ZoraASI.pdf`\n\n---\n\n"
    full = header + text

    OUT_PATH.write_text(full, encoding="utf-8")
    size_kb = OUT_PATH.stat().st_size / 1024
    print(f"Wrote {OUT_PATH}")
    print(f"Size: {size_kb:.1f} KB (under 4MB for Cursor cloud agents)")
    if size_kb > 4000:
        print("Warning: >4MB. Consider splitting by section.")


if __name__ == "__main__":
    main()
