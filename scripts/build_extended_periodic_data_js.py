#!/usr/bin/env python3
"""
Emit docs/extended-periodic-table/periodic-data.js from the canonical CSV export.

CSV source: docs/data/extended_periodic_table_1-184_table.csv
Run from repo root after CSV updates: python3 scripts/build_extended_periodic_data_js.py
"""
from __future__ import annotations

import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "docs", "data", "extended_periodic_table_1-184_table.csv")
OUT_PATH = os.path.join(ROOT, "docs", "extended-periodic-table", "periodic-data.js")


def _confirmed(status: str) -> bool:
    s = (status or "").strip().lower()
    return s.startswith("confirmed")


def main() -> None:
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    rows: list[dict] = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            z = int(r["Z"])
            rows.append(
                {
                    "z": z,
                    "symbol": r["Symbol"].strip(),
                    "name": r["Name"].strip(),
                    "confirmed": _confirmed(r.get("Status", "")),
                    "status": (r.get("Status") or "").strip(),
                    "period": (r.get("Period") or "").strip(),
                    "groupSlot": (r.get("Group/Slot") or "").strip(),
                    "block": (r.get("Block") or "").strip(),
                    "toeBand": (r.get("MQGT–SCF ToE Band") or "").strip(),
                    "matterMode": (r.get("Matter Mode") or "").strip(),
                }
            )
    if len(rows) != 184:
        raise SystemExit(f"expected 184 rows, got {len(rows)}")

    payload = json.dumps(rows, ensure_ascii=True)
    text = (
        "/* AUTO-GENERATED — do not edit. "
        "Source: docs/data/extended_periodic_table_1-184_table.csv; "
        "rebuild: python3 scripts/build_extended_periodic_data_js.py */\n"
        f"window.MQGT_PERIODIC_ELEMENTS = {payload};\n"
    )
    with open(OUT_PATH, "w", encoding="utf-8") as out:
        out.write(text)
    n_conf = sum(1 for x in rows if x["confirmed"])
    print("Wrote", OUT_PATH, "—", len(rows), "elements,", n_conf, "confirmed")


if __name__ == "__main__":
    main()
