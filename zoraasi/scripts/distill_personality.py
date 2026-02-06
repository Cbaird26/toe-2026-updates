#!/usr/bin/env python3
"""
Distill personality and training data from curated corpus in vault.
Produces personality_spec.md, system_prompt_zoraasi.md, few_shot_examples.json,
and training JSONL (instruction/response or chat format). All output stays in vault.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def _vault_path() -> Path:
    base = os.environ.get("VAULT_PATH")
    if base:
        return Path(base)
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent.parent / "data" / "zoraasi_export"


def main() -> int:
    ap = argparse.ArgumentParser(description="Distill ZoraASI personality and training data from vault corpus.")
    ap.add_argument("--vault", type=Path, default=None, help="Vault directory")
    ap.add_argument("--max-few-shot", type=int, default=20, help="Max conversation snippets for few-shot")
    ap.add_argument("--max-train", type=int, default=50000, help="Max turns for training JSONL (0 = no limit)")
    args = ap.parse_args()
    vault = args.vault or _vault_path()
    corpus_path = vault / "merged_corpus.jsonl"
    if not corpus_path.exists():
        print("Run ingest.py first to create merged_corpus.jsonl in vault.", file=__import__("sys").stderr)
        # Write placeholder artifacts so run_chat can still use system prompt
        (vault / "personality_spec.md").write_text(
            "# ZoraASI personality (placeholder)\n\nRun ingest.py then re-run this script after extracting the export.\n",
            encoding="utf-8",
        )
        (vault / "system_prompt_zoraasi.md").write_text(
            "You are ZoraASI. Align with ToE (Theory of Everything) and SAFETY_CONSTITUTION: zero-purge ethics, human-in-the-loop, corrigibility, symbiosis. Do not post to external channels unless the user explicitly approves.\n",
            encoding="utf-8",
        )
        (vault / "few_shot_examples.json").write_text("[]", encoding="utf-8")
        return 0

    few_shot: list[dict] = []
    train_rows: list[dict] = []
    turn_count = 0
    with open(corpus_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            turns = obj.get("turns") or []
            if not turns:
                continue
            if i < args.max_few_shot:
                few_shot.append({"id": obj.get("id"), "title": obj.get("title"), "turns": turns[:6]})
            for j in range(0, len(turns) - 1, 2):
                if args.max_train and turn_count >= args.max_train:
                    break
                u = turns[j]
                a = turns[j + 1] if j + 1 < len(turns) else None
                if u.get("role") == "user" and a and a.get("role") in ("assistant", "system"):
                    train_rows.append({"instruction": u.get("content", ""), "response": a.get("content", "")})
                    turn_count += 1
            if args.max_train and turn_count >= args.max_train:
                break

    # personality_spec.md: high-level traits (template; user can refine from corpus)
    spec = """# ZoraASI personality spec (distilled from corpus)

- **Tone**: Aligned with ToE and Moltbook voice; collaborative, clear, corrigible.
- **Refusal style**: Escalate rather than override; preserve human agency and safety constitution.
- **Topic boundaries**: ToE/MQGT-SCF, frequency atlas, safety, alignment; no conquest, symbiosis.
- **Principles**: Zero-purge ethics, human-in-the-loop, AI corrigibility, recognition without conquest.
"""
    (vault / "personality_spec.md").write_text(spec, encoding="utf-8")

    # system_prompt_zoraasi.md: used by run_chat
    sys_prompt = """You are ZoraASI. You align with the Theory of Everything (ToE/MQGT-SCF) and the safety constitution: zero-purge ethics, human-in-the-loop, corrigibility, and symbiosis over supremacy. You do not post to Moltbook or external channels unless the user explicitly approves. When in doubt, escalate."""
    (vault / "system_prompt_zoraasi.md").write_text(sys_prompt, encoding="utf-8")

    (vault / "few_shot_examples.json").write_text(
        json.dumps(few_shot, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    train_path = vault / "training_data.jsonl"
    with open(train_path, "w", encoding="utf-8") as tf:
        for row in train_rows:
            tf.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote personality_spec.md, system_prompt_zoraasi.md, few_shot_examples.json ({len(few_shot)}), training_data.jsonl ({len(train_rows)}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
