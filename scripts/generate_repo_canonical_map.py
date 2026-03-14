#!/usr/bin/env python3
"""
Generate REPO_CANONICAL_MAP from cbaird26_repos.json.
Assigns tier, status, duplicate?, merge_target, archive? per forensic consolidation plan.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

TOE_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = TOE_ROOT / "data" / "cbaird26_repos.json"
DOCS_PATH = TOE_ROOT / "docs" / "REPO_CANONICAL_MAP.md"
JSON_OUT = TOE_ROOT / "data" / "repo_canonical_map.json"

# Six primary repos (target architecture)
TIER1_PRIMARY = {
    "MQGT-SCF",
    "toe-empirical-validation",
    "toe-2026-updates",
    "ZoraAI",
    "ZoraAPI",
    "zoraasi-suite",
}

# Support repos that feed primary or are actively used
TIER2_SUPPORT = {
    "mqgt-qrng",
    "mqgt-fifth-force",
    "mqgt-collider",
    "mqgt-constraints-ledger",
    "mqgt-theorems",
    "mqgt-validation-suite",
    "mqgt-core-params",
    "mqgt-data-ingest",
    "mqgt-documentation-site",
    "mqgt-figures",
    "mqgt-papers",
    "mqgt-experiment-design",
    "mqgt-experiment-protocols",
    "mqgt-preregistration",
    "mqgt-validation-tools",
    "mqgt-analysis",
    "mqgt-numerics",
    "mqgt-ops-ci",
    "zora-theory-of-everything",
    "theory-explorer",
    "toe-studio",
    "QuantumMeditationCoach",
    "holocron-public-export",
}

# Duplicate groups: (canonical_target, duplicates)
DUPLICATE_GROUPS = [
    ("toe-2026-updates", ["A-Theory-of-Everything", "A-Theory-of-Everything-Revised", "Theory-of-Everything", "ToE"]),
    ("omnisolve-streamlit", ["omnisolve_2_0_streamlit_app.py", "omnisolve_3_0_streamlit_app.py"]),
    ("quantum-ai-assistant", ["quantum_ai.py"]),
    ("aging-intervention-simulator", ["aging_simulator.py", "anti-aging-simulator"]),
    ("Universe-Explorer", ["universe_explorer.py"]),
    ("quantum-supercomputer", ["QuantumSupercomputer", "QuantumBridge"]),
]

# Merge targets for mqgt-* into toe-empirical-validation
MERGE_TO_EMPIRICAL = {
    "mqgt-qrng": "toe-empirical-validation/qrng/",
    "mqgt-fifth-force": "toe-empirical-validation/fifth-force/",
    "mqgt-collider": "toe-empirical-validation/collider/",
}

# Merge targets for mqgt-* into MQGT-SCF
MERGE_TO_MQGT = {
    "mqgt-theorems": "MQGT-SCF/theory/proofs/",
    "mqgt-analysis": "MQGT-SCF/theory/",
    "mqgt-core-params": "MQGT-SCF/theory/",
}

# Archive candidates: single-purpose, prototype, superseded
ARCHIVE_CANDIDATES = {
    "app.py",
    "bairds_law_app.py",
    "dissertation_app.py",
    "medical_simulations_app.py",
    "microplastic_removal_simulator.py",
    "streamlit_app.py",
    "baird-telehealth-site",
    "darkstar",
    "Dissertation_Data",
    "Hope",
    "A-Theory-of-Everything---Baird-et-al-2025-.pdf",
    "mqgt-astrophysics-cooling",
    "mqgt-astrophysics-sn1987a",
    "mqgt-atomic-clocks",
    "mqgt-casimir",
    "mqgt-cosmology-bbn",
    "mqgt-cosmology-cmb",
    "mqgt-cosmology-lss",
    "mqgt-curve-processing",
    "mqgt-dark-matter",
    "mqgt-emi-testing",
    "mqgt-equivalence-principle",
    "mqgt-gravitational-waves",
    "mqgt-gravitational-waves-propagation",
    "mqgt-legacy-ingest",
    "mqgt-manifests",
    "mqgt-meta",
    "mqgt-neutrinos",
    "mqgt-plotting",
    "mqgt-quantum-optics",
    "mqgt-sensitivity-analysis",
    "mqgt-simulation-core",
    "mqgt-simulation-interference",
    "mqgt-simulation-quantum",
    "mqgt-unit-tests",
    "mqgt-visualization",
    "mqgt-api-schema",
    "mqgt-cli",
    "mqgt-dashboard",
    "mqgt-data-public",
    "mqgt-io",
    "mqgt-scf-thesis",
    "ComprehensivePhysicsSolver",
    "pqs-simulations",
    "susy_simulation.py",
    "wild_simulations.py",
    "ToE-Simulations",
    "theory-of-everything-simulations",
    "QC",
    "quantum-lab",
    "quantum-mechanics-simulator",
    "quantum_component.py",
    "quantum_state_app_with_bloch.py",
    "studio-hub",
}


def _build_duplicate_map() -> dict[str, str]:
    out = {}
    for canonical, dupes in DUPLICATE_GROUPS:
        for d in dupes:
            out[d] = canonical
    return out


def _get_purpose(repo: str, tier: str, duplicate_of: str | None, merge_target: str | None) -> str:
    purposes = {
        "MQGT-SCF": "Physics core: Lagrangian, Φc, E, proofs",
        "toe-empirical-validation": "Experiments: QRNG, fifth-force, collider",
        "toe-2026-updates": "Public entry point, canonical releases",
        "ZoraAI": "Zora agent core",
        "ZoraAPI": "Zora API layer",
        "mqgt-qrng": "QRNG pipeline → merge to toe-empirical-validation/qrng",
        "mqgt-fifth-force": "Fifth-force analysis → merge to toe-empirical-validation/fifth-force",
        "mqgt-collider": "Collider constraints → merge to toe-empirical-validation/collider",
        "mqgt-theorems": "Theorem proofs → merge to MQGT-SCF/theory/proofs",
        "mqgt-papers": "LaTeX papers",
        "zora-theory-of-everything": "Zora + ToE integration",
        "zoraasi-suite": "Zora agents, API, deployment (unified ZoraAI + ZoraAPI)",
        "QuantumMeditationCoach": "Meditation/Phi_c application",
        "holocron-public-export": "Holocron knowledge export",
    }
    if repo in purposes:
        return purposes[repo]
    if duplicate_of:
        return f"Duplicate of {duplicate_of}"
    if merge_target:
        return f"Merge target: {merge_target}"
    if tier == "4-archive":
        return "Archive candidate"
    if repo.startswith("mqgt-"):
        return "MQGT support module"
    return "Support"


def main() -> int:
    if not DATA_PATH.exists():
        print(f"Missing {DATA_PATH}", file=sys.stderr)
        return 1

    data = json.loads(DATA_PATH.read_text())
    repos = data.get("repos", [])
    duplicate_of = _build_duplicate_map()

    rows = []
    for r in repos:
        name = r["name"]
        # Tier
        if name in TIER1_PRIMARY:
            tier = "1-primary"
        elif name in TIER2_SUPPORT:
            tier = "2-support"
        elif name in duplicate_of:
            tier = "3-duplicate"
        elif name in ARCHIVE_CANDIDATES:
            tier = "4-archive"
        else:
            tier = "3-other"

        dup_target = duplicate_of.get(name)
        merge_target = MERGE_TO_EMPIRICAL.get(name) or MERGE_TO_MQGT.get(name)
        archive = tier == "4-archive" or (tier == "3-duplicate" and dup_target)
        purpose = _get_purpose(name, tier, dup_target, merge_target)

        status = "active" if tier in ("1-primary", "2-support") else ("duplicate" if tier == "3-duplicate" else ("archive" if tier == "4-archive" else "other"))
        rows.append({
            "repo": name,
            "clone_url": r.get("clone_url", ""),
            "tier": tier,
            "status": status,
            "purpose": purpose,
            "duplicate_of": dup_target,
            "merge_target": merge_target,
            "archive": archive,
        })

    rows.sort(key=lambda x: (x["tier"], x["repo"].lower()))

    # Write JSON
    DOCS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(JSON_OUT, "w") as f:
        json.dump({"generated_from": str(DATA_PATH), "repos": rows}, f, indent=2)
    print(f"Wrote {JSON_OUT}")

    # Write Markdown
    lines = [
        "# Repo Canonical Map",
        "",
        f"**Source:** [data/cbaird26_repos.json](data/cbaird26_repos.json) (fetched {data.get('fetched_at', 'unknown')})",
        f"**Total repos:** {len(rows)}",
        "",
        "**Tiers:** 1-primary (6 target) | 2-support | 3-duplicate/other | 4-archive",
        "",
        "---",
        "",
        "| Repo | Tier | Status | Purpose | Duplicate? | Merge target | Archive? |",
        "|------|------|--------|---------|------------|--------------|----------|",
    ]
    for r in rows:
        dup = r["duplicate_of"] or "—"
        merge = r["merge_target"] or "—"
        arch = "✓" if r["archive"] else ""
        lines.append(f"| {r['repo']} | {r['tier']} | {r['status']} | {r['purpose'][:45]} | {dup} | {merge} | {arch} |")

    lines.extend([
        "",
        "---",
        "",
        "## Target Architecture (Forensic Six Primary)",
        "",
        "| Repo | Purpose | Maps to |",
        "|------|---------|---------|",
        "| MQGT-SCF | Physics core: lagrangian/, collapse/, consciousness-field/, ethics-field/, proofs/ | — |",
        "| toe-empirical-validation | Experiments: qrng/, fifth-force/, collider/, datasets/ | — |",
        "| zoraasi-suite | AI architecture: agents/, api/, deployment | — |",
        "| toe-papers | LaTeX papers | toe-2026-updates/papers_sources/ |",
        "| toe-release | Public entry point | toe-2026-updates |",
        "| toe-tools | Utilities: repo-indexing, dataset builders, validation | Future / TOE scripts/ |",
        "",
        "## Tier 1 (Primary) — Current GitHub Repos",
        "",
        "- **MQGT-SCF** — Physics core",
        "- **toe-empirical-validation** — Experiments",
        "- **toe-2026-updates** — Public entry point (toe-release)",
        "- **ZoraAI** — Zora agent core",
        "- **ZoraAPI** — Zora API layer",
        "- **zoraasi-suite** — Zora agents, API, deployment",
        "",
        "## Archive Strategy",
        "",
        "Move Tier 4 and duplicates to `cbaird26-archive`. Preserve history.",
        "",
        "## Merge Targets",
        "",
        "- mqgt-qrng, mqgt-fifth-force, mqgt-collider → toe-empirical-validation subdirs",
        "- mqgt-theorems, mqgt-analysis → MQGT-SCF/theory/",
        "- ToE variants (A-Theory-of-Everything, Revised, Theory-of-Everything, ToE) → toe-2026-updates",
        "",
    ])
    DOCS_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {DOCS_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
