#!/usr/bin/env python3
"""
Digitize the Yukawa |alpha|(lambda) *envelope* curve from Lee et al. (PRL 124, 101101 (2020)),
Figure 5 (bottom panel).

This script is deliberately "boringly reproducible":
- It renders the arXiv PDF page that contains Fig. 5 using PyMuPDF,
- crops to the bottom-panel plot region (hard-coded pixel boxes for a fixed render scale),
- detects the excluded-region background (pale yellow) via an RGB threshold,
- extracts the boundary curve by scanning upward from the bottom axis for the first yellow pixel,
- maps pixel coordinates -> physical (lambda, alpha) using log-log axis limits.

IMPORTANT:
- This produces an *approximate digitization* of the published figure, NOT an author-provided data table.
- Axis limits are taken from the tick labels visible in the plot:
    lambda in [2e-6, 1e-3] meters
    alpha in [1e-3, 1e6] (dimensionless)
  If you believe the true plot limits differ, change those constants below.

Dependencies:
    pip install pymupdf pillow numpy pandas

Usage:
    python digitize_lee2020_fig5_envelope.py \
        --pdf lee2020_inverse_square.pdf \
        --out lee2020_fig5_yukawa_envelope_digitized.csv

"""

from __future__ import annotations

import argparse
import math
import os
from typing import Tuple, List

import fitz  # PyMuPDF
import numpy as np
import pandas as pd
from PIL import Image


# ---- Tunable parameters (pin these for reproducibility) ----

# Which page (0-indexed) contains Fig. 5 bottom plot in the arXiv PDF.
PDF_PAGE_INDEX = 3

# Render scale; changing this will change crop boxes.
RENDER_SCALE = 2.0

# First crop: isolate the whole Fig. 5 block from the page render.
# These were determined empirically for the arXiv PDF at RENDER_SCALE=2.0.
CROP_FIG5_BLOCK = (120, 720, 1120, 1490)  # (left, top, right, bottom)

# Second crop: isolate the *bottom panel* plot area from the Fig. 5 block crop.
CROP_BOTTOM_PANEL = (520, 70, 1000, 475)

# "Excluded region" background color threshold (pale yellow in the paper plot).
# Pixel is considered yellow if R and G are very high but B is noticeably lower.
YELLOW_THRESH = dict(r_min=240, g_min=240, b_max=220)

# Axis limits read from the plotted tick labels.
LAMBDA_MIN_M = 2e-6
LAMBDA_MAX_M = 1e-3
ALPHA_MIN = 1e-3
ALPHA_MAX = 1e6


def is_yellow(rgb: np.ndarray) -> bool:
    r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])
    return (r >= YELLOW_THRESH["r_min"]) and (g >= YELLOW_THRESH["g_min"]) and (b <= YELLOW_THRESH["b_max"])


def find_plot_axes_bbox(img_arr: np.ndarray) -> Tuple[int, int, int, int]:
    """
    Find approximate axis bounding box by locating dark border lines.

    Returns: (x_left, x_right, y_top, y_bottom)
    """
    h, w, _ = img_arr.shape
    dark = np.all(img_arr < 120, axis=2)  # includes grey/black borders
    col_counts = dark.sum(axis=0)
    row_counts = dark.sum(axis=1)

    x_left = int(np.argmax(col_counts))
    right_region = np.arange(int(w * 0.7), w)
    x_right = int(right_region[np.argmax(col_counts[right_region])])

    top_region = np.arange(0, int(h * 0.5))
    y_top = int(top_region[np.argmax(row_counts[top_region])])

    bottom_region = np.arange(int(h * 0.7), h)
    y_bottom = int(bottom_region[np.argmax(row_counts[bottom_region])])

    return x_left, x_right, y_top, y_bottom


def digitize_envelope(img_arr: np.ndarray) -> pd.DataFrame:
    """
    Digitize the boundary between white (allowed) and yellow (excluded) regions.
    """
    x_left, x_right, y_top, y_bottom = find_plot_axes_bbox(img_arr)

    xs: List[int] = []
    ys: List[int] = []

    for x in range(x_left + 2, x_right - 2):
        y_found = None
        for y in range(y_bottom - 2, y_top + 1, -1):
            if is_yellow(img_arr[y, x]):
                y_found = y
                break
        if y_found is not None:
            xs.append(x)
            ys.append(y_found)

    if not xs:
        raise RuntimeError("No yellow pixels found; check crop boxes or YELLOW_THRESH.")

    # Pixel -> data mapping (log-log)
    log_lambda_min = math.log10(LAMBDA_MIN_M)
    log_lambda_max = math.log10(LAMBDA_MAX_M)
    log_alpha_min = math.log10(ALPHA_MIN)
    log_alpha_max = math.log10(ALPHA_MAX)

    lambdas = []
    alphas = []

    for x, y in zip(xs, ys):
        x_frac = (x - x_left) / (x_right - x_left)
        loglam = log_lambda_min + x_frac * (log_lambda_max - log_lambda_min)
        lam = 10 ** loglam

        y_frac = (y - y_top) / (y_bottom - y_top)
        loga = log_alpha_max - y_frac * (log_alpha_max - log_alpha_min)
        a = 10 ** loga

        lambdas.append(lam)
        alphas.append(a)

    df = pd.DataFrame({"lambda_m": lambdas, "alpha_max": alphas}).sort_values("lambda_m").reset_index(drop=True)
    return df


def render_pdf_page(pdf_path: str, page_index: int) -> Image.Image:
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_index)
    pix = page.get_pixmap(matrix=fitz.Matrix(RENDER_SCALE, RENDER_SCALE))
    return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True, help="Path to arXiv PDF (e.g. 2002.11761.pdf)")
    ap.add_argument("--out", required=True, help="Output CSV path")
    ap.add_argument("--debug_dir", default=None, help="Optional directory to write debug crops/images")
    args = ap.parse_args()

    page_img = render_pdf_page(args.pdf, PDF_PAGE_INDEX)

    fig5_block = page_img.crop(CROP_FIG5_BLOCK)
    bottom_panel = fig5_block.crop(CROP_BOTTOM_PANEL)

    if args.debug_dir:
        os.makedirs(args.debug_dir, exist_ok=True)
        page_img.save(os.path.join(args.debug_dir, "page.png"))
        fig5_block.save(os.path.join(args.debug_dir, "fig5_block.png"))
        bottom_panel.save(os.path.join(args.debug_dir, "bottom_panel.png"))

    img_arr = np.array(bottom_panel.convert("RGB"))
    df = digitize_envelope(img_arr)
    df.to_csv(args.out, index=False)

    print(f"Wrote {len(df)} points to {args.out}")


if __name__ == "__main__":
    main()
