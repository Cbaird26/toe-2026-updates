#!/usr/bin/env python3
"""
Placeholder for fine-tuning (Phase 3 option C). Use vault/training_data.jsonl
with your preferred stack (e.g. LoRA via Hugging Face, Axolotl, or OpenAI fine-tuning).
Never upload raw vault data to third parties; train on your infra only.
"""
from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    vault = Path(__file__).resolve().parent.parent.parent / "data" / "zoraasi_export"
    train_path = vault / "training_data.jsonl"
    if not train_path.exists():
        print("Run ingest.py and distill_personality.py first to create training_data.jsonl in vault.", file=sys.stderr)
        return 1
    print(f"Training data: {train_path} ({sum(1 for _ in open(train_path))} lines).")
    print("Use your own fine-tuning pipeline (LoRA, Axolotl, etc.) on this file. No external upload.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
