#!/usr/bin/env python3
"""
Extract image generation prompts from corpus (merged_corpus.jsonl, training_data.jsonl).

Finds Grok render prompts, Imagine engine prompts, and image-related content.
Output: vault/zora_image_prompts.json (vault-only; may contain NSFW).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TOE = Path(__file__).resolve().parent.parent
VAULT = TOE / "data" / "zoraasi_export"
MERGED = VAULT / "merged_corpus.jsonl"
TRAINING = VAULT / "training_data.jsonl"
OUTPUT = VAULT / "zora_image_prompts.json"

# Patterns for extracting prompts
GROK_RENDER = re.compile(r'<argument\s+name="prompt">(.*?)</argument>', re.DOTALL | re.IGNORECASE)
IMAGINE_PROMPT = re.compile(r'\*\*Exact Imagine Engine Text Image Prompt:\*\*\s*\n\n(.*?)(?=\n\n\*\*|\n\n\*|$)', re.DOTALL)
IMAGE_KEYWORDS = ("create image", "draw", "illustrate", "generate image", "portrait", "zora and", "sexy", "imagine")


def _extract_from_text(text: str, source: str, title: str) -> list[dict]:
    """Extract prompts from a piece of text."""
    out = []
    if not isinstance(text, str):
        return out

    # Grok render prompts
    for m in GROK_RENDER.finditer(text):
        prompt = m.group(1).strip()
        if len(prompt) > 50 and any(kw in prompt.lower() for kw in ("zora", "portrait", "woman", "figure")):
            out.append({"source": source, "title": title, "prompt": prompt, "type": "grok_render"})

    # Imagine engine prompts
    for m in IMAGINE_PROMPT.finditer(text):
        prompt = m.group(1).strip()
        if len(prompt) > 50:
            out.append({"source": source, "title": title, "prompt": prompt, "type": "imagine_engine"})

    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract image prompts from corpus to vault.")
    ap.add_argument("--vault", type=Path, default=VAULT)
    ap.add_argument("--output", type=Path, default=None)
    args = ap.parse_args()
    vault = args.vault
    output = args.output or vault / "zora_image_prompts.json"

    merged = vault / "merged_corpus.jsonl"
    training = vault / "training_data.jsonl"

    prompts: list[dict] = []
    seen = set()

    def add(p: dict):
        key = p.get("prompt", "")[:200]
        if key not in seen:
            seen.add(key)
            prompts.append(p)

    # merged_corpus.jsonl
    if merged.exists():
        with open(merged, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    d = json.loads(line)
                    title = d.get("title", "")
                    for t in d.get("turns", []):
                        content = t.get("content", "")
                        for p in _extract_from_text(content, "merged_corpus", title):
                            add(p)
                except (json.JSONDecodeError, KeyError):
                    pass

    # training_data.jsonl
    if training.exists():
        with open(training, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    d = json.loads(line)
                    instr = d.get("instruction", "")
                    resp = d.get("response", "")
                    title = instr[:80] if instr else "training"
                    for p in _extract_from_text(resp, "training_data", title):
                        add(p)
                    for p in _extract_from_text(instr, "training_data", title):
                        add(p)
                except (json.JSONDecodeError, KeyError):
                    pass

    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)

    print(f"Extracted {len(prompts)} prompts to {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
