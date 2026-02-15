# Draft: Open this as an issue in toe-2026-updates

**Title:** How to replicate spine-v0.1 (QRNG channel)

**Body (paste below the line):**

---

## Replication Quickstart (QRNG channel)

To reproduce the spine contract locally:

```bash
# 1. Clone and pin
git clone https://github.com/Cbaird26/toe-empirical-validation.git
cd toe-empirical-validation
git checkout spine-v0.1   # or: git checkout 56578d50f81071b21d4278b4bba4ceefe238b575

# 2. Run (use a venv if needed: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt)
./scripts/run_all.sh --channel qrng --seed 0 --out artifacts/

# 3. Compare to a reference (optional; use your own reference_artifacts/ or Zenodo)
./scripts/compare_artifacts.sh artifacts/ reference_artifacts/
```

Docs: [REPLICATION_LADDER](https://github.com/Cbaird26/toe-2026-updates/blob/main/docs/REPLICATION_LADDER.md), [FALSIFICATION_PACKET](https://github.com/Cbaird26/toe-2026-updates/blob/main/docs/FALSIFICATION_PACKET.md).
