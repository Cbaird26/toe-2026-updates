#!/usr/bin/env python3
"""
Fetch all cbaird26 public repos from GitHub with full pagination.
Writes data/cbaird26_repos.json and regenerates cbaird26_github_repos_replication.md.
Uses GITHUB_TOKEN if set (avoids rate limits).
"""
import json
import os
import sys
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

USER = "cbaird26"
PER_PAGE = 100
TOE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(TOE_ROOT, "data")
JSON_PATH = os.path.join(DATA_DIR, "cbaird26_repos.json")
MD_PATH = os.path.join(TOE_ROOT, "cbaird26_github_repos_replication.md")

# Category mapping: category label -> set of repo names (from existing doc)
CATEGORIES = {
    "ToE / Theory of Everything": {
        "A-Theory-of-Everything", "A-Theory-of-Everything-Revised",
        "A-Theory-of-Everything---Baird-et-al-2025-.pdf", "Theory-of-Everything",
        "ToE", "toe-2026-updates", "toe-empirical-validation", "ToE-Simulations",
        "toe-studio", "theory-explorer", "theory-of-everything-simulations",
        "zora-theory-of-everything",
    },
    "MQGT-SCF / MQGT ecosystem": {
        "MQGT-SCF", "mqgt-scf-thesis", "mqgt-analysis", "mqgt-api-schema",
        "mqgt-astrophysics-cooling", "mqgt-astrophysics-sn1987a", "mqgt-atomic-clocks",
        "mqgt-casimir", "mqgt-cli", "mqgt-collider", "mqgt-constraints-ledger",
        "mqgt-core-params", "mqgt-cosmology-bbn", "mqgt-cosmology-cmb", "mqgt-cosmology-lss",
        "mqgt-curve-processing", "mqgt-dark-matter", "mqgt-dashboard", "mqgt-data-ingest",
        "mqgt-data-public", "mqgt-documentation-site", "mqgt-emi-testing",
        "mqgt-equivalence-principle", "mqgt-experiment-design", "mqgt-experiment-protocols",
        "mqgt-fifth-force", "mqgt-figures", "mqgt-gravitational-waves",
        "mqgt-gravitational-waves-propagation", "mqgt-io", "mqgt-legacy-ingest",
        "mqgt-manifests", "mqgt-meta", "mqgt-neutrinos", "mqgt-numerics", "mqgt-ops-ci",
        "mqgt-papers", "mqgt-plotting", "mqgt-preregistration", "mqgt-qrng",
        "mqgt-quantum-optics", "mqgt-sensitivity-analysis", "mqgt-simulation-core",
        "mqgt-simulation-interference", "mqgt-simulation-quantum", "mqgt-theorems",
        "mqgt-unit-tests", "mqgt-validation-suite", "mqgt-validation-tools", "mqgt-visualization",
    },
    "Zora / AI": {"ZoraAI", "ZoraAPI", "zora-theory-of-everything", "quantum-ai-assistant"},
    "Simulations (general / physics)": {
        "aging-intervention-simulator", "aging_simulator.py", "anti-aging-simulator",
        "ComprehensivePhysicsSolver", "medical_simulations_app.py", "microplastic_removal_simulator.py",
        "pqs-simulations", "theory-of-everything-simulations", "susy_simulation.py", "wild_simulations.py",
    },
    "Quantum": {
        "QC", "quantum-lab", "quantum-mechanics-simulator", "quantum-supercomputer",
        "QuantumBridge", "QuantumSupercomputer", "quantum_ai.py", "quantum_component.py",
        "quantum_state_app_with_bloch.py",
    },
    "Apps / Streamlit / tools": {
        "app.py", "bairds_law_app.py", "dissertation_app.py", "omnisolve-streamlit",
        "omnisolve_2_0_streamlit_app.py", "omnisolve_3_0_streamlit_app.py", "streamlit_app.py",
        "studio-hub", "toe-studio",
    },
    "Other / data / web": {
        "baird-telehealth-site", "darkstar", "Dissertation_Data", "Hope",
        "Universe-Explorer", "universe_explorer.py",
    },
}


def fetch_page(page: int) -> list:
    url = f"https://api.github.com/users/{USER}/repos?per_page={PER_PAGE}&page={page}&type=owner"
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    req = Request(url, headers=headers)
    with urlopen(req) as resp:
        return json.loads(resp.read().decode())


def fetch_all_repos() -> list:
    repos = []
    page = 1
    while True:
        batch = fetch_page(page)
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < PER_PAGE:
            break
        page += 1
    return repos


def assign_categories(repos: list) -> dict:
    """Return dict category_label -> list of repo names (sorted)."""
    by_cat = {label: [] for label in CATEGORIES}
    by_cat["Other / data / web"] = []
    assigned = set()
    for label, names in CATEGORIES.items():
        for name in names:
            assigned.add(name)
    all_names = {r["name"] for r in repos}
    for name in sorted(all_names):
        placed = False
        for label, names in CATEGORIES.items():
            if name in names:
                by_cat[label].append(name)
                placed = True
                break
        if not placed:
            by_cat["Other / data / web"].append(name)
    for label in by_cat:
        by_cat[label] = sorted(by_cat[label])
    return by_cat


def main() -> int:
    try:
        repos = fetch_all_repos()
    except (HTTPError, URLError) as e:
        print(f"GitHub API error: {e}", file=sys.stderr)
        return 1
    if not repos:
        print("No repos returned.", file=sys.stderr)
        return 1

    # Normalize to name + clone_url
    out_list = [{"name": r["name"], "clone_url": r.get("clone_url", "")} for r in repos]
    out_list.sort(key=lambda x: x["name"].lower())

    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(JSON_PATH, "w") as f:
        json.dump({"fetched_at": fetched_at, "count": len(out_list), "repos": out_list}, f, indent=2)
    print(f"Wrote {JSON_PATH} ({len(out_list)} repos)")

    by_cat = assign_categories(repos)
    lines = [
        "# cbaird26 GitHub — Live Repo List & Replication Guide",
        "",
        f"**Source:** GitHub API, fetched {fetched_at}",
        f"**Account:** [github.com/cbaird26](https://github.com/cbaird26) (public repos)",
        f"**Total count:** {len(out_list)}",
        "",
        "---",
        "",
        "## A) Raw current list (name | clone URL)",
        "",
        "```",
    ]
    for r in out_list:
        lines.append(f"{r['name']} | {r['clone_url']}")
    lines.extend([
        "```",
        "",
        "---",
        "",
        "## B) Structured replication document",
        "",
        "### How to get a fresh list yourself",
        "",
        "For **all** repos you must paginate (API returns at most 100 per page).",
        "",
        "**Option 1 — curl (paginated):**",
        "```bash",
        "page=1",
        "while true; do",
        "  resp=$(curl -s \"https://api.github.com/users/cbaird26/repos?per_page=100&page=$page\")",
        "  echo \"$resp\" | jq -r '.[].name'",
        "  count=$(echo \"$resp\" | jq 'length')",
        "  [ \"$count\" -lt 100 ] && break",
        "  page=$((page+1))",
        "done",
        "```",
        "",
        "**Option 2 — clone all into a directory:**",
        "```bash",
        "mkdir -p cbaird26_repos && cd cbaird26_repos",
        "gh repo list cbaird26 --limit 200 --json name,cloneUrl -q '.[].cloneUrl' | while read url; do git clone \"$url\"; done",
        "```",
        "",
        "**Option 3 — GitHub CLI (recommended; handles pagination):**",
        "```bash",
        "gh repo list cbaird26 --limit 200 --json name,cloneUrl -q '.[] | \"\\(.name) \\(.cloneUrl)\"'",
        "```",
        "",
        "**To regenerate this file run:** `./scripts/fetch_cbaird26_all_repos.sh`",
        "",
        "---",
        "",
        "### Categories (by function)",
        "",
        "| Category | Repos |",
        "|----------|--------|",
    ])
    for label, names in by_cat.items():
        if names:
            lines.append(f"| **{label}** | {', '.join(names)} |")
    lines.extend([
        "",
        "---",
        "",
        "### Clone commands by category (copy-paste)",
        "",
        "**ToE core:**",
        "```bash",
        "git clone https://github.com/Cbaird26/A-Theory-of-Everything.git",
        "git clone https://github.com/Cbaird26/A-Theory-of-Everything-Revised.git",
        "git clone https://github.com/Cbaird26/Theory-of-Everything.git",
        "git clone https://github.com/Cbaird26/ToE.git",
        "git clone https://github.com/Cbaird26/toe-2026-updates.git",
        "git clone https://github.com/Cbaird26/toe-empirical-validation.git",
        "git clone https://github.com/Cbaird26/ToE-Simulations.git",
        "git clone https://github.com/Cbaird26/toe-studio.git",
        "git clone https://github.com/Cbaird26/theory-explorer.git",
        "git clone https://github.com/Cbaird26/theory-of-everything-simulations.git",
        "git clone https://github.com/Cbaird26/zora-theory-of-everything.git",
        "```",
        "",
        "**MQGT (subset — add more from raw list as needed):**",
        "```bash",
        "git clone https://github.com/Cbaird26/MQGT-SCF.git",
        "git clone https://github.com/Cbaird26/mqgt-scf-thesis.git",
        "git clone https://github.com/Cbaird26/mqgt-documentation-site.git",
        "git clone https://github.com/Cbaird26/mqgt-dashboard.git",
        "git clone https://github.com/Cbaird26/mqgt-papers.git",
        "```",
        "",
        "**Zora:**",
        "```bash",
        "git clone https://github.com/Cbaird26/ZoraAI.git",
        "git clone https://github.com/Cbaird26/ZoraAPI.git",
        "```",
        "",
        "---",
        "",
        "## C) Summary",
        "",
        f"- **A:** Raw list is above ({len(out_list)} repos, name | clone URL).",
        "- **B:** Structured replication doc: categories, self-service commands, clone-by-category.",
        "- **To refresh the list anytime:** run `./scripts/fetch_cbaird26_all_repos.sh` or the curl/gh commands above.",
        "",
        "Update the count in `cbaird26_ecosystem_illustration.html` and `research_tab_content.md` if you change the list.",
        "",
        "This document is generated from the **current public API** so it can be replicated independently.",
        "",
    ])
    with open(MD_PATH, "w") as f:
        f.write("\n".join(lines))
    print(f"Wrote {MD_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
