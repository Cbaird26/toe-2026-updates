#!/usr/bin/env python3
"""Append the Baird-and-Zora culmination image as the last page of the ToE PDF."""
import sys
from pathlib import Path

TOE_ROOT = Path(__file__).resolve().parent.parent
FIG = TOE_ROOT / "papers_sources" / "figures" / "Christopher_Michael_Baird_and_Zora_thesis_culmination.png"
PDF_MAIN = TOE_ROOT / "papers_sources" / "A_Theory_of_Everything_CM_Baird_et_al_2026.pdf"
PDF_OUT = TOE_ROOT / "papers_sources" / "A_Theory_of_Everything_CM_Baird_et_al_2026_with_culmination.pdf"

def main():
    if not FIG.exists():
        print("Figure not found:", FIG, file=sys.stderr)
        sys.exit(1)
    if not PDF_MAIN.exists():
        print("PDF not found:", PDF_MAIN, file=sys.stderr)
        sys.exit(1)

    from PIL import Image
    from pypdf import PdfWriter, PdfReader

    # Create one-page PDF from image (PIL save as PDF)
    img_pdf_path = TOE_ROOT / "papers_sources" / "figures" / "_culmination_page.pdf"
    with Image.open(FIG) as img:
        rgb = img.convert("RGB") if img.mode in ("RGBA", "P") else img
        rgb.save(str(img_pdf_path), "PDF", resolution=72)

    reader = PdfReader(str(PDF_MAIN))
    img_reader = PdfReader(str(img_pdf_path))
    writer = PdfWriter()
    writer.append(reader)  # entire document in one go
    writer.add_page(img_reader.pages[0])

    writer.write(str(PDF_OUT))
    img_pdf_path.unlink(missing_ok=True)
    print("Appended culmination image as last page of", PDF_OUT)

if __name__ == "__main__":
    main()
