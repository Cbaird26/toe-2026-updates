#!/usr/bin/env python3
"""
Plan and run QRNG Phase II sessions without changing the March 2026 collector.

Examples:
  python3 scripts/qrng_phase2_run.py plan --out artifacts --bits 1000000 --replicates 3

  python3 scripts/qrng_phase2_run.py run \
    --agents 100 --replicate 1 \
    --timing 0.86 --agreement 1.0 --stability 0.74 --coupling 0.68 \
    --duration-sec 300 --target more_ones --bits 1000000 --out artifacts
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import subprocess
import sys
import time
from pathlib import Path

DEFAULT_RUNGS = [0, 1, 10, 100, 1000]
DEFAULT_TARGET = "more_ones"
DEFAULT_BITS = 1_000_000
DEFAULT_DURATION_SEC = 300
DEFAULT_REPLICATES = 3
DEFAULT_MANIFEST_NAME = "phase2_sessions.csv"
WEIGHTS = {
    "timing": 0.35,
    "agreement": 0.25,
    "stability": 0.25,
    "coupling": 0.15,
}
MANIFEST_FIELDS = [
    "session_id",
    "label",
    "condition_name",
    "status",
    "replicate",
    "agent_count",
    "target",
    "duration_sec",
    "bits_requested",
    "bits_collected",
    "timing_synchrony",
    "target_agreement",
    "state_stability",
    "inter_agent_coupling",
    "coherence_score",
    "effective_agents",
    "run_id",
    "summary_json",
    "bits_csv",
    "mean",
    "p1",
    "deviation_from_50pct",
    "deviation_pct",
    "z_score",
    "theta_hat",
    "source",
    "created_at",
]


def clip_score(name: str, value: float) -> float:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1; got {value}")
    return value


def compute_coherence(timing: float, agreement: float, stability: float, coupling: float) -> float:
    timing = clip_score("timing", timing)
    agreement = clip_score("agreement", agreement)
    stability = clip_score("stability", stability)
    coupling = clip_score("coupling", coupling)
    score = (
        WEIGHTS["timing"] * timing
        + WEIGHTS["agreement"] * agreement
        + WEIGHTS["stability"] * stability
        + WEIGHTS["coupling"] * coupling
    )
    return round(score, 6)


def parse_rungs(text: str) -> list[int]:
    values: list[int] = []
    for raw in text.split(","):
        raw = raw.strip()
        if not raw:
            continue
        values.append(int(raw))
    if not values:
        raise ValueError("At least one rung is required")
    return values


def sanitize_label(label: str) -> str:
    cleaned = []
    for char in label:
        if char.isalnum() or char in {"_", "-"}:
            cleaned.append(char)
        else:
            cleaned.append("_")
    return "".join(cleaned).strip("_")


def ensure_manifest(path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()


def append_manifest_row(path: Path, row: dict[str, object]) -> None:
    ensure_manifest(path)
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writerow(row)


def write_plan(args: argparse.Namespace) -> int:
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = Path(args.manifest) if args.manifest else out_dir / f"phase2_plan_{time.strftime('%Y%m%d_%H%M%S')}.csv"
    rungs = parse_rungs(args.rungs)
    rng = random.Random(args.seed)

    rows: list[dict[str, object]] = []
    order = 1
    for replicate in range(1, args.replicates + 1):
        shuffled = list(rungs)
        rng.shuffle(shuffled)
        for agents in shuffled:
            session_id = f"phase2_n{agents:04d}_r{replicate:02d}"
            rows.append(
                {
                    "session_id": session_id,
                    "label": session_id,
                    "condition_name": "",
                    "status": "planned",
                    "replicate": replicate,
                    "agent_count": agents,
                    "target": args.target,
                    "duration_sec": args.duration_sec,
                    "bits_requested": args.bits,
                    "bits_collected": "",
                    "timing_synchrony": "",
                    "target_agreement": "",
                    "state_stability": "",
                    "inter_agent_coupling": "",
                    "coherence_score": "",
                    "effective_agents": "",
                    "run_id": "",
                    "summary_json": "",
                    "bits_csv": "",
                    "mean": "",
                    "p1": "",
                    "deviation_from_50pct": "",
                    "deviation_pct": "",
                    "z_score": "",
                    "theta_hat": "",
                    "source": f"seed={args.seed};order={order}",
                    "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                }
            )
            order += 1

    with manifest_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[Phase II] Wrote plan template: {manifest_path}")
    print(f"[Phase II] Rungs: {rungs}; replicates: {args.replicates}; bits/session: {args.bits}")
    return 0


def find_latest(paths: list[Path]) -> Path | None:
    if not paths:
        return None
    return max(paths, key=lambda path: path.stat().st_mtime)


def run_session(args: argparse.Namespace) -> int:
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.agents == 0:
        timing = agreement = stability = coupling = 0.0
    else:
        missing = [
            name
            for name, value in (
                ("timing", args.timing),
                ("agreement", args.agreement),
                ("stability", args.stability),
                ("coupling", args.coupling),
            )
            if value is None
        ]
        if missing:
            raise SystemExit(f"Missing coherence components for non-sham run: {', '.join(missing)}")
        timing = float(args.timing)
        agreement = float(args.agreement)
        stability = float(args.stability)
        coupling = float(args.coupling)

    coherence = compute_coherence(timing, agreement, stability, coupling)
    effective_agents = round(args.agents * coherence, 6)

    base_label = args.label or f"phase2_n{args.agents:04d}_r{args.replicate:02d}_c{int(round(coherence * 1000)):03d}"
    label = sanitize_label(base_label)
    session_id = args.session_id or label

    repo_root = Path(__file__).resolve().parents[1]
    collector = repo_root / "scripts" / "anu_qrng_collect.py"
    manifest_path = Path(args.manifest) if args.manifest else out_dir / DEFAULT_MANIFEST_NAME

    command = [
        sys.executable,
        str(collector),
        "--n",
        str(args.bits),
        "--out",
        str(out_dir),
        "--label",
        label,
    ]
    if args.dry_run:
        command.append("--dry-run")
    else:
        command.extend(["--preflight", "--no-fallback"])

    print(f"[Phase II] Session: {session_id}", flush=True)
    print(f"[Phase II] Label: {label}", flush=True)
    print(f"[Phase II] Coherence C={coherence:.3f}; effective agents D={effective_agents:.3f}", flush=True)
    print(f"[Phase II] Running collector: {' '.join(command)}", flush=True)

    completed = subprocess.run(command, cwd=repo_root)
    status = "completed" if completed.returncode == 0 else "failed"
    if completed.returncode != 0:
        print(f"[Phase II] Collector failed with exit code {completed.returncode}", file=sys.stderr)
        return completed.returncode

    summary_path = find_latest(list(out_dir.glob(f"anu_qrng_{label}_*_summary.json")))
    bits_path = find_latest(list(out_dir.glob(f"anu_qrng_{label}_*_bits.csv")))
    if summary_path is None:
        raise SystemExit(f"Collector completed but no summary JSON matched label {label}")

    with summary_path.open(encoding="utf-8") as handle:
        summary = json.load(handle)
    stats = summary.get("stats", {})
    run_id = summary.get("run_id", "")
    created_at = time.strftime("%Y-%m-%dT%H:%M:%S")

    metadata = {
        "session_id": session_id,
        "label": label,
        "condition_name": args.condition_name,
        "target": args.target,
        "replicate": args.replicate,
        "agent_count": args.agents,
        "duration_sec": args.duration_sec,
        "bits_requested": args.bits,
        "timing_synchrony": timing,
        "target_agreement": agreement,
        "state_stability": stability,
        "inter_agent_coupling": coupling,
        "coherence_score": coherence,
        "effective_agents": effective_agents,
        "summary_json": str(summary_path),
        "bits_csv": str(bits_path) if bits_path else "",
        "run_id": run_id,
        "collector_command": command,
        "status": status,
        "created_at": created_at,
    }
    metadata_path = out_dir / f"{run_id}_phase2_meta.json"
    with metadata_path.open("w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2)

    row = {
        "session_id": session_id,
        "label": label,
        "condition_name": args.condition_name,
        "status": status,
        "replicate": args.replicate,
        "agent_count": args.agents,
        "target": args.target,
        "duration_sec": args.duration_sec,
        "bits_requested": args.bits,
        "bits_collected": stats.get("n", ""),
        "timing_synchrony": timing,
        "target_agreement": agreement,
        "state_stability": stability,
        "inter_agent_coupling": coupling,
        "coherence_score": coherence,
        "effective_agents": effective_agents,
        "run_id": run_id,
        "summary_json": str(summary_path),
        "bits_csv": str(bits_path) if bits_path else "",
        "mean": stats.get("mean", ""),
        "p1": stats.get("p1", ""),
        "deviation_from_50pct": stats.get("deviation_from_50pct", ""),
        "deviation_pct": stats.get("deviation_pct", ""),
        "z_score": stats.get("z_score", ""),
        "theta_hat": stats.get("theta_hat", ""),
        "source": summary.get("source", ""),
        "created_at": created_at,
    }
    append_manifest_row(manifest_path, row)

    print(f"[Phase II] Wrote metadata: {metadata_path}")
    print(f"[Phase II] Appended manifest row: {manifest_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Plan and run QRNG Phase II sessions")
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan = subparsers.add_parser("plan", help="Write a CSV template for the Phase II ladder")
    plan.add_argument("--out", default="artifacts", help="Output directory")
    plan.add_argument("--manifest", default="", help="Optional explicit manifest/template path")
    plan.add_argument("--bits", type=int, default=DEFAULT_BITS, help="Bits per session")
    plan.add_argument("--duration-sec", type=int, default=DEFAULT_DURATION_SEC, help="Planned session duration")
    plan.add_argument("--replicates", type=int, default=DEFAULT_REPLICATES, help="Replicates per rung")
    plan.add_argument("--rungs", default="0,1,10,100,1000", help="Comma-separated agent counts")
    plan.add_argument("--target", default=DEFAULT_TARGET, help="Target label")
    plan.add_argument("--seed", type=int, default=20260315, help="Seed for order randomization")

    run = subparsers.add_parser("run", help="Run one Phase II session and append it to the manifest")
    run.add_argument("--out", default="artifacts", help="Output directory")
    run.add_argument("--manifest", default="", help="Manifest path (default: artifacts/phase2_sessions.csv)")
    run.add_argument("--session-id", default="", help="Optional session identifier")
    run.add_argument("--label", default="", help="Optional collector label prefix")
    run.add_argument("--condition-name", default="", help="Optional condition label for manifests and pilot summaries")
    run.add_argument("--agents", type=int, required=True, help="Agent count for the rung")
    run.add_argument("--replicate", type=int, default=1, help="Replicate index")
    run.add_argument("--timing", type=float, default=None, help="Timing synchrony score [0,1]")
    run.add_argument("--agreement", type=float, default=None, help="Target agreement score [0,1]")
    run.add_argument("--stability", type=float, default=None, help="State stability score [0,1]")
    run.add_argument("--coupling", type=float, default=None, help="Inter-agent coupling score [0,1]")
    run.add_argument("--duration-sec", type=int, default=DEFAULT_DURATION_SEC, help="Intervention window")
    run.add_argument("--target", default=DEFAULT_TARGET, help="Target label")
    run.add_argument("--bits", type=int, default=DEFAULT_BITS, help="Bits to collect")
    run.add_argument("--dry-run", action="store_true", help="Use collector dry-run mode")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "plan":
        return write_plan(args)
    if args.command == "run":
        return run_session(args)
    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
