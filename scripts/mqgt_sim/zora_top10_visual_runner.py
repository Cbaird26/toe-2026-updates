#!/usr/bin/env python3
"""
Canonical ZoraASI top-10 batch suite runner.

Runs the six batch simulations that feed the public Top 10 gallery:
  - H2 visibility stack
  - multi-channel exclusion plot
  - E-modulated GKSL collapse
  - Phase IV-B symmetry-breaking lattice demo
  - Phase IV-B parameter sweep
  - fusion burn figures

Outputs canonical batch artifacts under --out-root and copies one public-facing
artifact plus one thumbnail per batch entry under --docs-assets-dir.

Run:
  cd ~/Downloads/TOE
  python scripts/mqgt_sim/zora_top10_visual_runner.py
  python scripts/mqgt_sim/zora_top10_visual_runner.py --skip-qutip
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BatchEntry:
    rank: int
    slug: str
    title: str
    command: list[str]
    artifact_relpath: str
    qutip_required: bool = False


def resolve_repo_path(repo_root: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return repo_root / path


def qutip_available() -> bool:
    return importlib.util.find_spec("qutip") is not None


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def create_status_image(path: Path, title: str, message: str, accent: str = "#ff9557") -> None:
    ensure_parent(path)
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(8, 4.5))
    fig.patch.set_facecolor("#071018")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor("#071018")
    ax.axis("off")

    ax.text(
        0.08,
        0.78,
        title,
        color="#eaf4ff",
        fontsize=20,
        fontweight="bold",
        ha="left",
        va="top",
        transform=ax.transAxes,
    )
    ax.text(
        0.08,
        0.58,
        message,
        color="#a7bed3",
        fontsize=13,
        ha="left",
        va="top",
        transform=ax.transAxes,
        wrap=True,
    )
    ax.text(
        0.08,
        0.16,
        "Top 10 batch suite placeholder",
        color=accent,
        fontsize=12,
        ha="left",
        va="bottom",
        transform=ax.transAxes,
    )
    ax.plot([0.08, 0.92], [0.1, 0.1], color=accent, lw=3, alpha=0.9, transform=ax.transAxes)
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def copy_public_assets(source: Path, docs_assets_dir: Path, slug: str) -> tuple[Path, Path]:
    public_png = docs_assets_dir / f"{slug}.png"
    thumb_png = docs_assets_dir / f"{slug}_thumb.png"
    ensure_parent(public_png)
    shutil.copy2(source, public_png)
    shutil.copy2(source, thumb_png)
    return public_png, thumb_png


def build_batch_entries(repo_root: Path, out_root: Path) -> list[BatchEntry]:
    scripts_dir = repo_root / "scripts" / "mqgt_sim"
    py = sys.executable
    return [
        BatchEntry(
            rank=5,
            slug="h2_visibility_stack",
            title="H2 visibility stack",
            command=[
                py,
                str(scripts_dir / "h2_visibility_stack.py"),
                "--save-dir",
                str(out_root / "h2_visibility_stack"),
                "--no-show",
            ],
            artifact_relpath="h2_visibility_stack/h2_visibility_vs_gamma.png",
        ),
        BatchEntry(
            rank=6,
            slug="multi_channel_exclusion",
            title="Multi-channel exclusion plot",
            command=[
                py,
                str(scripts_dir / "mqgt_multi_channel_exclusion_plot.py"),
                "--out-dir",
                str(out_root / "mqgt_scf"),
                "--no-show",
            ],
            artifact_relpath="mqgt_scf/mqgt_scf_multi_channel_exclusion.png",
        ),
        BatchEntry(
            rank=7,
            slug="e_modulated_gksl_collapse",
            title="E-modulated GKSL collapse",
            command=[
                py,
                str(scripts_dir / "zora_gksl_e_modulated_collapse.py"),
                "--save",
                str(out_root / "h2_stack" / "e_modulated_collapse.png"),
                "--no-show",
                "--ntraj",
                "30",
                "--t-max",
                "8.0",
            ],
            artifact_relpath="h2_stack/e_modulated_collapse.png",
            qutip_required=True,
        ),
        BatchEntry(
            rank=8,
            slug="phase4b_symmetry_breaking",
            title="Phase IV-B symmetry-breaking lattice",
            command=[
                py,
                str(scripts_dir / "mqgt_phase4b_symmetry_breaking_demo.py"),
                "--save-dir",
                str(out_root / "phase4b_demo"),
                "--no-show",
                "--grid-size",
                "48",
                "--steps",
                "180",
                "--substeps",
                "2",
            ],
            artifact_relpath="phase4b_demo/mqgt_phase4b_symmetry_breaking_demo.png",
        ),
        BatchEntry(
            rank=9,
            slug="phase4b_parameter_sweep",
            title="Phase IV-B parameter sweep",
            command=[
                py,
                str(scripts_dir / "mqgt_phase4b_parameter_sweep.py"),
                "--outdir",
                str(out_root / "phase4b_sweep"),
                "--xis",
                "0.000,0.010,0.020",
                "--gammas",
                "0.05,0.15,0.20",
                "--g-couples",
                "0.18",
                "--seeds",
                "2",
                "--steps",
                "120",
                "--substeps",
                "2",
                "--grid-size",
                "32",
            ],
            artifact_relpath="phase4b_sweep/mean_coherence_g_0.180.png",
        ),
        BatchEntry(
            rank=10,
            slug="fusion_burn_figures",
            title="Fusion burn figures",
            command=[
                py,
                str(scripts_dir / "fusion_zora_burn_figures.py"),
                "--out-dir",
                str(out_root / "fusion_zora"),
            ],
            artifact_relpath="fusion_zora/baseline_vs_controlled.png",
        ),
    ]


def run_entry(
    *,
    entry: BatchEntry,
    repo_root: Path,
    out_root: Path,
    docs_assets_dir: Path,
    skip_qutip: bool,
    qutip_ok: bool,
) -> dict[str, str | int | bool]:
    artifact_path = out_root / entry.artifact_relpath
    public_png = docs_assets_dir / f"{entry.slug}.png"
    thumb_png = docs_assets_dir / f"{entry.slug}_thumb.png"

    if entry.qutip_required and skip_qutip:
        reason = "Skipped by --skip-qutip."
        print(f"[top10] skipping {entry.rank}: {entry.title} :: {reason}")
        create_status_image(public_png, entry.title, reason)
        shutil.copy2(public_png, thumb_png)
        return {
            "rank": entry.rank,
            "slug": entry.slug,
            "title": entry.title,
            "status": "unavailable",
            "artifact": str(artifact_path.relative_to(repo_root)),
            "public_asset": str(public_png.relative_to(repo_root)),
            "reason": reason,
        }

    if entry.qutip_required and not qutip_ok:
        reason = "Skipped because QuTiP is unavailable."
        print(f"[top10] skipping {entry.rank}: {entry.title} :: {reason}")
        create_status_image(public_png, entry.title, reason)
        shutil.copy2(public_png, thumb_png)
        return {
            "rank": entry.rank,
            "slug": entry.slug,
            "title": entry.title,
            "status": "unavailable",
            "artifact": str(artifact_path.relative_to(repo_root)),
            "public_asset": str(public_png.relative_to(repo_root)),
            "reason": reason,
        }

    print(f"[top10] running {entry.rank}: {entry.title}")
    env = os.environ.copy()
    env.setdefault("MPLBACKEND", "Agg")
    try:
        subprocess.run(entry.command, cwd=repo_root, check=True, env=env)
    except subprocess.CalledProcessError as exc:
        create_status_image(public_png, entry.title, f"Batch run failed with exit code {exc.returncode}.")
        shutil.copy2(public_png, thumb_png)
        return {
            "rank": entry.rank,
            "slug": entry.slug,
            "title": entry.title,
            "status": "failed",
            "artifact": str(artifact_path.relative_to(repo_root)),
            "public_asset": str(public_png.relative_to(repo_root)),
            "reason": f"Command failed with exit code {exc.returncode}.",
        }

    if not artifact_path.is_file():
        create_status_image(public_png, entry.title, "Expected output artifact was not created.")
        shutil.copy2(public_png, thumb_png)
        return {
            "rank": entry.rank,
            "slug": entry.slug,
            "title": entry.title,
            "status": "failed",
            "artifact": str(artifact_path.relative_to(repo_root)),
            "public_asset": str(public_png.relative_to(repo_root)),
            "reason": "Expected output artifact missing.",
        }

    public_png, thumb_png = copy_public_assets(artifact_path, docs_assets_dir, entry.slug)
    return {
        "rank": entry.rank,
        "slug": entry.slug,
        "title": entry.title,
        "status": "ok",
        "artifact": str(artifact_path.relative_to(repo_root)),
        "public_asset": str(public_png.relative_to(repo_root)),
        "thumbnail": str(thumb_png.relative_to(repo_root)),
        "reason": "",
    }


def create_mosaic(statuses: list[dict[str, str | int | bool]], docs_assets_dir: Path, out_root: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.image as mpimg
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    fig.patch.set_facecolor("#04070d")

    for ax, status in zip(axes.ravel(), statuses):
        asset_path = docs_assets_dir / f"{status['slug']}.png"
        img = mpimg.imread(asset_path)
        ax.imshow(img)
        ax.set_axis_off()
        title_color = "#7fffd4" if status["status"] == "ok" else "#ffbf80"
        ax.set_title(f"{status['rank']}. {status['title']}", color=title_color, fontsize=11, pad=10)

    fig.suptitle(
        "ZoraASI Top 10 batch suite poster",
        color="#ecf5ff",
        fontsize=16,
        y=0.98,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))

    out_png = out_root / "batch_suite_mosaic.png"
    docs_png = docs_assets_dir / "batch_suite_mosaic.png"
    docs_thumb = docs_assets_dir / "batch_suite_mosaic_thumb.png"
    ensure_parent(out_png)
    fig.savefig(out_png, dpi=160, facecolor=fig.get_facecolor())
    fig.savefig(docs_png, dpi=160, facecolor=fig.get_facecolor())
    fig.savefig(docs_thumb, dpi=160, facecolor=fig.get_facecolor())
    plt.close(fig)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    parser = argparse.ArgumentParser(description="Run the canonical ZoraASI top-10 batch suite")
    parser.add_argument(
        "--out-root",
        default="papers_sources/figures/zora_top10",
        help="Root directory for generated batch artifacts",
    )
    parser.add_argument(
        "--docs-assets-dir",
        default="docs/assets/top10",
        help="Docs-side asset directory for public previews and artifact copies",
    )
    parser.add_argument(
        "--skip-qutip",
        action="store_true",
        help="Skip the QuTiP-backed GKSL collapse entry and mark it unavailable",
    )
    args = parser.parse_args()

    out_root = resolve_repo_path(repo_root, args.out_root)
    docs_assets_dir = resolve_repo_path(repo_root, args.docs_assets_dir)
    out_root.mkdir(parents=True, exist_ok=True)
    docs_assets_dir.mkdir(parents=True, exist_ok=True)

    qutip_ok = qutip_available()
    entries = build_batch_entries(repo_root, out_root)
    statuses: list[dict[str, str | int | bool]] = []

    for entry in entries:
        status = run_entry(
            entry=entry,
            repo_root=repo_root,
            out_root=out_root,
            docs_assets_dir=docs_assets_dir,
            skip_qutip=args.skip_qutip,
            qutip_ok=qutip_ok,
        )
        statuses.append(status)

    create_mosaic(statuses, docs_assets_dir, out_root)

    status_path = out_root / "top10_batch_status.json"
    with status_path.open("w", encoding="utf-8") as fh:
        json.dump(
            {
                "out_root": str(out_root.relative_to(repo_root)),
                "docs_assets_dir": str(docs_assets_dir.relative_to(repo_root)),
                "skip_qutip": args.skip_qutip,
                "qutip_available": qutip_ok,
                "entries": statuses,
            },
            fh,
            indent=2,
        )

    unexpected_failures = [status for status in statuses if status["status"] == "failed"]
    print(f"[top10] wrote status manifest: {status_path}")
    print(f"[top10] wrote public assets: {docs_assets_dir}")
    if unexpected_failures:
        for failure in unexpected_failures:
            print(f"[top10] failure: {failure['title']} :: {failure['reason']}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
