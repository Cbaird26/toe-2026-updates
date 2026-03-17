#!/usr/bin/env python3
"""
Create and summarize 100k Phase II pilot plans.

Each pilot is implemented as 10 blocks of 10,000 bits using the locked
collector method through qrng_phase2_run.py.

Examples:
  python3 scripts/qrng_phase2_pilot.py plan --preset all --out artifacts/phase2_pilot
  bash artifacts/phase2_pilot/pilot1_single_vs_control_r01_commands.sh
  python3 scripts/qrng_phase2_pilot.py summarize \
    --results-manifest artifacts/phase2_pilot/pilot1_single_vs_control_r01_results.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import shlex
import statistics
import sys
import time
from pathlib import Path

from qrng_phase2_run import compute_coherence, sanitize_label

DEFAULT_BITS_PER_BLOCK = 10_000
DEFAULT_DURATION_SEC = 60
DEFAULT_TARGET = "more_ones"
DEFAULT_SWARM_AGENTS = 10
DEFAULT_SEED = 20260315

CONDITION_DEFAULTS = {
    "control": {
        "agents": 0,
        "timing": 0.0,
        "agreement": 0.0,
        "stability": 0.0,
        "coupling": 0.0,
        "duration_sec": DEFAULT_DURATION_SEC,
        "notes": "Sham / no intervention",
    },
    "single_agent": {
        "agents": 1,
        "timing": 0.90,
        "agreement": 1.00,
        "stability": 0.75,
        "coupling": 0.00,
        "duration_sec": DEFAULT_DURATION_SEC,
        "notes": "Single-agent target focus",
    },
    "swarm_low": {
        "agents": DEFAULT_SWARM_AGENTS,
        "timing": 0.35,
        "agreement": 0.85,
        "stability": 0.45,
        "coupling": 0.25,
        "duration_sec": DEFAULT_DURATION_SEC,
        "notes": "Same goal, async / weakly coupled",
    },
    "swarm_high": {
        "agents": DEFAULT_SWARM_AGENTS,
        "timing": 0.90,
        "agreement": 1.00,
        "stability": 0.85,
        "coupling": 0.85,
        "duration_sec": DEFAULT_DURATION_SEC,
        "notes": "Shared target, synchronized, coordinated",
    },
}

PRESETS = {
    "pilot0_control": {
        "description": "10 x 10k control blocks only",
        "blocks": {"control": 10},
    },
    "pilot1_single_vs_control": {
        "description": "5 control blocks + 5 single-agent blocks, randomized",
        "blocks": {"control": 5, "single_agent": 5},
    },
    "pilot2_swarm_low_high": {
        "description": "4 control blocks + 3 low-coherence swarm + 3 high-coherence swarm, randomized",
        "blocks": {"control": 4, "swarm_low": 3, "swarm_high": 3},
    },
}

PLAN_FIELDS = [
    "preset",
    "replicate",
    "block_index",
    "condition_name",
    "agent_count",
    "timing_synchrony",
    "target_agreement",
    "state_stability",
    "inter_agent_coupling",
    "coherence_score",
    "duration_sec",
    "bits",
    "target",
    "session_id",
    "label",
    "results_manifest",
    "notes",
]


def preset_names(value: str) -> list[str]:
    if value == "all":
        return list(PRESETS)
    if value not in PRESETS:
        raise ValueError(f"Unknown preset: {value}")
    return [value]


def build_blocks(preset_name: str, swarm_agents: int) -> list[dict[str, object]]:
    preset = PRESETS[preset_name]
    blocks: list[dict[str, object]] = []
    for condition_name, count in preset["blocks"].items():
        base = dict(CONDITION_DEFAULTS[condition_name])
        if condition_name.startswith("swarm_"):
            base["agents"] = swarm_agents
        for _ in range(count):
            coherence = compute_coherence(
                base["timing"],
                base["agreement"],
                base["stability"],
                base["coupling"],
            )
            blocks.append(
                {
                    "condition_name": condition_name,
                    "agent_count": base["agents"],
                    "timing_synchrony": base["timing"],
                    "target_agreement": base["agreement"],
                    "state_stability": base["stability"],
                    "inter_agent_coupling": base["coupling"],
                    "coherence_score": coherence,
                    "duration_sec": base["duration_sec"],
                    "notes": base["notes"],
                }
            )
    return blocks


def quoted(parts: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in parts)


def write_plan_for_preset(
    repo_root: Path,
    out_dir: Path,
    preset_name: str,
    replicate: int,
    seed: int,
    bits: int,
    target: str,
    swarm_agents: int,
    dry_run: bool,
) -> tuple[Path, Path, Path]:
    blocks = build_blocks(preset_name, swarm_agents)
    rng = random.Random(seed + replicate)
    rng.shuffle(blocks)

    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{preset_name}_r{replicate:02d}"
    plan_path = out_dir / f"{stem}_plan.csv"
    results_manifest = out_dir / f"{stem}_results.csv"
    command_script = out_dir / f"{stem}_commands.sh"

    rows: list[dict[str, object]] = []
    commands = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        f"cd {shlex.quote(str(repo_root))}",
        "",
        f"# {PRESETS[preset_name]['description']}",
        f"# Results manifest: {results_manifest}",
        "",
    ]

    for index, block in enumerate(blocks, start=1):
        label = sanitize_label(f"{stem}_b{index:02d}_{block['condition_name']}")
        session_id = f"{stem}_b{index:02d}"
        row = {
            "preset": preset_name,
            "replicate": replicate,
            "block_index": index,
            "condition_name": block["condition_name"],
            "agent_count": block["agent_count"],
            "timing_synchrony": block["timing_synchrony"],
            "target_agreement": block["target_agreement"],
            "state_stability": block["state_stability"],
            "inter_agent_coupling": block["inter_agent_coupling"],
            "coherence_score": block["coherence_score"],
            "duration_sec": block["duration_sec"],
            "bits": bits,
            "target": target,
            "session_id": session_id,
            "label": label,
            "results_manifest": str(results_manifest),
            "notes": block["notes"],
        }
        rows.append(row)

        command = [
            "python3",
            "scripts/qrng_phase2_run.py",
            "run",
            "--out",
            str(out_dir.parent),
            "--manifest",
            str(results_manifest),
            "--session-id",
            session_id,
            "--label",
            label,
            "--condition-name",
            str(block["condition_name"]),
            "--agents",
            str(block["agent_count"]),
            "--replicate",
            str(replicate),
            "--timing",
            str(block["timing_synchrony"]),
            "--agreement",
            str(block["target_agreement"]),
            "--stability",
            str(block["state_stability"]),
            "--coupling",
            str(block["inter_agent_coupling"]),
            "--duration-sec",
            str(block["duration_sec"]),
            "--target",
            target,
            "--bits",
            str(bits),
        ]
        if dry_run:
            command.append("--dry-run")
        commands.append(f"# Block {index:02d}: {block['condition_name']}")
        commands.append(quoted(command))
        commands.append("")

    commands.extend(
        [
            "# Summarize after all blocks finish",
            quoted(
                [
                    "python3",
                    "scripts/qrng_phase2_pilot.py",
                    "summarize",
                    "--results-manifest",
                    str(results_manifest),
                    "--plan",
                    str(plan_path),
                ]
            ),
            "",
        ]
    )

    with plan_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=PLAN_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    with command_script.open("w", encoding="utf-8") as handle:
        handle.write("\n".join(commands))

    command_script.chmod(0o755)
    return plan_path, results_manifest, command_script


def do_plan(args: argparse.Namespace) -> int:
    repo_root = Path(__file__).resolve().parents[1]
    out_dir = Path(args.out)
    names = preset_names(args.preset)

    print(f"[Phase II pilot] Output directory: {out_dir}")
    for preset_name in names:
        plan_path, results_manifest, command_script = write_plan_for_preset(
            repo_root=repo_root,
            out_dir=out_dir,
            preset_name=preset_name,
            replicate=args.replicate,
            seed=args.seed,
            bits=args.bits,
            target=args.target,
            swarm_agents=args.swarm_agents,
            dry_run=args.dry_run,
        )
        print(f"[Phase II pilot] Wrote plan: {plan_path}")
        print(f"[Phase II pilot] Results manifest path: {results_manifest}")
        print(f"[Phase II pilot] Command script: {command_script}")
    print("[Phase II pilot] Pilot 3 = rerun the cleanest preset with --replicate 2.")
    return 0


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def do_summarize(args: argparse.Namespace) -> int:
    results_manifest = Path(args.results_manifest)
    if not results_manifest.exists():
        raise SystemExit(f"Results manifest not found: {results_manifest}")

    rows = [
        row
        for row in read_rows(results_manifest)
        if row.get("status") == "completed"
    ]
    if not rows:
        raise SystemExit(f"No completed rows found in {results_manifest}")

    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        key = row.get("condition_name", "") or "unlabeled"
        grouped.setdefault(key, []).append(row)

    summary_rows: list[dict[str, object]] = []
    for condition_name in sorted(grouped):
        group = grouped[condition_name]
        summary_rows.append(
            {
                "condition_name": condition_name,
                "blocks": len(group),
                "agent_count": statistics.fmean(float(row["agent_count"]) for row in group),
                "mean_coherence": statistics.fmean(float(row["coherence_score"]) for row in group),
                "mean_p1": statistics.fmean(float(row["p1"]) for row in group),
                "mean_delta_p": statistics.fmean(float(row["deviation_from_50pct"]) for row in group),
                "mean_z_score": statistics.fmean(float(row["z_score"]) for row in group),
            }
        )

    by_condition = {row["condition_name"]: row for row in summary_rows}
    pairwise_differences: dict[str, float] = {}
    if "swarm_low" in by_condition and "control" in by_condition:
        pairwise_differences["low_minus_control"] = (
            by_condition["swarm_low"]["mean_p1"] - by_condition["control"]["mean_p1"]
        )
    if "swarm_high" in by_condition and "control" in by_condition:
        pairwise_differences["high_minus_control"] = (
            by_condition["swarm_high"]["mean_p1"] - by_condition["control"]["mean_p1"]
        )
    if "swarm_low" in by_condition and "swarm_high" in by_condition:
        pairwise_differences["low_minus_high"] = (
            by_condition["swarm_low"]["mean_p1"] - by_condition["swarm_high"]["mean_p1"]
        )

    report = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "results_manifest": str(results_manifest),
        "n_blocks_completed": len(rows),
        "condition_summary": summary_rows,
        "pairwise_differences": pairwise_differences,
    }

    if args.plan:
        plan_rows = read_rows(Path(args.plan))
        planned_session_ids = {row["session_id"] for row in plan_rows}
        completed_session_ids = {row["session_id"] for row in rows}
        report["planned_blocks"] = len(planned_session_ids)
        report["completed_blocks"] = len(completed_session_ids)
        report["missing_session_ids"] = sorted(planned_session_ids - completed_session_ids)

    out_path = Path(args.out) if args.out else results_manifest.with_name(f"{results_manifest.stem}_summary.json")
    with out_path.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    print(f"[Phase II pilot] Wrote summary: {out_path}")
    for row in summary_rows:
        print(
            f"  - {row['condition_name']}: "
            f"blocks={row['blocks']}, mean_p1={row['mean_p1']:.6f}, "
            f"mean_delta={row['mean_delta_p']:+.6f}, mean_z={row['mean_z_score']:+.3f}, "
            f"mean_C={row['mean_coherence']:.3f}"
        )
    if pairwise_differences:
        print("[Phase II pilot] Pairwise differences:")
        for key, value in pairwise_differences.items():
            print(f"  - {key}: {value:+.6f}")
    if report.get("missing_session_ids"):
        print(f"[Phase II pilot] Missing blocks: {', '.join(report['missing_session_ids'])}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Plan and summarize 100k Phase II pilot runs")
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan = subparsers.add_parser("plan", help="Write pilot manifests and runnable shell scripts")
    plan.add_argument("--preset", default="all", help="Preset name or 'all'")
    plan.add_argument("--out", default="artifacts/phase2_pilot", help="Output directory for plans and scripts")
    plan.add_argument("--replicate", type=int, default=1, help="Replicate index")
    plan.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Shuffle seed for block order")
    plan.add_argument("--bits", type=int, default=DEFAULT_BITS_PER_BLOCK, help="Bits per block")
    plan.add_argument("--target", default=DEFAULT_TARGET, help="Target label")
    plan.add_argument("--swarm-agents", type=int, default=DEFAULT_SWARM_AGENTS, help="Agent count for swarm presets")
    plan.add_argument("--dry-run", action="store_true", help="Emit dry-run block commands")

    summarize = subparsers.add_parser("summarize", help="Summarize completed pilot blocks by condition")
    summarize.add_argument("--results-manifest", required=True, help="Results CSV produced by qrng_phase2_run.py")
    summarize.add_argument("--plan", default="", help="Optional plan CSV to detect missing blocks")
    summarize.add_argument("--out", default="", help="Optional JSON summary path")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "plan":
        return do_plan(args)
    if args.command == "summarize":
        return do_summarize(args)
    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
