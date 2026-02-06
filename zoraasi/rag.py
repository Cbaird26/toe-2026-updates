"""
RAG retrieval for ZoraASI: load index (and optional embeddings) from vault,
return top-k chunks for a query. Used by run_chat.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Callable


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def _keyword_score(query: str, text: str) -> float:
    qw = set(re.findall(r"\w+", query.lower()))
    tw = set(re.findall(r"\w+", text.lower()))
    if not qw:
        return 0.0
    return len(qw & tw) / len(qw)


def load_rag(vault: Path) -> tuple[list[dict], list[list[float]] | None]:
    index_path = vault / "rag_index.json"
    if not index_path.exists():
        return [], None
    index = json.loads(index_path.read_text(encoding="utf-8"))
    emb_path = vault / "rag_embeddings.json"
    embeddings = None
    if emb_path.exists():
        try:
            embeddings = json.loads(emb_path.read_text(encoding="utf-8"))
            if len(embeddings) != len(index):
                embeddings = None
        except Exception:
            embeddings = None
    return index, embeddings


def retrieve(
    query: str,
    index: list[dict],
    embeddings: list[list[float]] | None,
    top_k: int = 5,
    embed_fn: Callable[[str], list[float] | None] | None = None,
) -> list[str]:
    """Return top_k chunk texts for query. Uses embeddings if available and embed_fn for query; else keyword overlap."""
    if not index:
        return []
    if embeddings is not None and embed_fn is not None:
        q_emb = embed_fn(query)
        if q_emb is not None:
            scores = [_cosine(q_emb, e) for e in embeddings]
            order = sorted(range(len(scores)), key=lambda i: -scores[i])
            return [index[i]["text"] for i in order[:top_k]]
    # Keyword fallback
    scores = [_keyword_score(query, item["text"]) for item in index]
    order = sorted(range(len(scores)), key=lambda i: -scores[i])
    return [index[i]["text"] for i in order[:top_k]]


def format_context(chunks: list[str], max_chars: int = 4000) -> str:
    out: list[str] = []
    n = 0
    for c in chunks:
        if n + len(c) + 1 > max_chars:
            break
        out.append(c)
        n += len(c) + 1
    if not out:
        return ""
    return "Relevant context from knowledge base:\n\n" + "\n\n---\n\n".join(out)
